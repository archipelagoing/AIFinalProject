"""Real-browser release smoke and optional 60–90s fictional-data demo recording.

Uses its own temporary SQLite workspace and browser profile, never .local/compass.db.
Install requirements-dev.txt and Playwright Chromium first. Outputs are ignored.
"""

import argparse
import asyncio
from contextlib import closing
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlparse
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]

# Prevent backend Internet connections during the smoke run, including dependencies.
SERVER_BOOTSTRAP = """
import os, socket, sys
from pathlib import Path
original_connect = socket.socket.connect
def local_connect(self, address):
    if self.family in (socket.AF_INET, socket.AF_INET6) and address[0] not in ('127.0.0.1', '::1', 'localhost'):
        with Path(os.environ['COMPASS_EGRESS_LOG']).open('a') as output:
            output.write('Blocked non-loopback connection\\n')
        raise OSError('Release smoke blocks external network connections')
    return original_connect(self, address)
socket.socket.connect = local_connect
from streamlit.web.cli import main
sys.exit(main())
"""


class Server:
    def __init__(self, directory: Path):
        self.directory = directory
        with closing(socket.socket()) as probe:
            probe.bind(("127.0.0.1", 0))
            self.port = probe.getsockname()[1]
        self.url = f"http://127.0.0.1:{self.port}"
        self.process = None
        self.log = None

    async def start(self):
        env = os.environ | {"COMPASS_DB_PATH": str(self.directory / "demo.db"),
                            "COMPASS_EGRESS_LOG": str(self.directory / "egress.log")}
        self.log = (self.directory / "server.log").open("a")
        self.process = subprocess.Popen([
            sys.executable, "-c", SERVER_BOOTSTRAP, "run", str(ROOT / "app.py"),
            f"--server.port={self.port}", "--server.address=127.0.0.1",
            "--server.headless=true", "--browser.gatherUsageStats=false",
        ], cwd=ROOT, env=env, stdout=self.log, stderr=subprocess.STDOUT)
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise RuntimeError("Temporary demo server exited; inspect its log.")
            try:
                with urlopen(self.url + "/_stcore/health", timeout=1) as response:
                    if response.status == 200:
                        return
            except OSError:
                pass
            await asyncio.sleep(0.2)
        raise TimeoutError("Temporary demo server did not start.")

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=3)
            self.process = None
        if self.log:
            self.log.close()
            self.log = None


async def run(record: bool, output: Path):
    from playwright.async_api import async_playwright, expect

    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(ROOT / ".local/playwright"))
    output.mkdir(parents=True, exist_ok=True)
    outbound = []
    errors = []
    checkpoints = []
    allowed = {"127.0.0.1", "localhost", "::1"}

    async def guard(route):
        if urlparse(route.request.url).hostname not in allowed:
            outbound.append(urlparse(route.request.url).hostname)
            await route.abort()
        else:
            await route.continue_()

    async def configure(context):
        await context.route("**/*", guard)
        context.on("page", lambda page: page.on("pageerror", lambda error: errors.append(str(error))))
        def websocket(ws):
            if urlparse(ws.url).hostname not in allowed:
                outbound.append(urlparse(ws.url).hostname)
        # Browser contexts have no direct websocket event; observe each page.
        context.on("page", lambda page: page.on("websocket", websocket))

    async def choose(page, label, value):
        await settle(page)
        combo = page.get_by_role("combobox", name=label, exact=True)
        await combo.evaluate("el => el.scrollIntoView({block: 'center', behavior: 'instant'})")
        await expect(combo).to_be_in_viewport()
        await combo.focus()
        await combo.press("ArrowDown")
        option = page.get_by_role("option").filter(has_text=value).first
        await expect(option).to_be_visible()
        await option.click()
        await settle(page)

    async def settle(page):
        # Widget deltas arrive before the script-finished message. Let the rerun
        # start, then wait for Streamlit to release its running/stale UI state.
        await page.wait_for_timeout(300)
        await expect(page.get_by_test_id("stStatusWidget")).not_to_be_visible(timeout=15000)
        await page.wait_for_function("!document.querySelector('[data-stale=\"true\"]')", timeout=15000)

    async def metric(page, label, value):
        await settle(page)
        element = page.get_by_test_id("stMetric").filter(has_text=re.compile(r"^" + re.escape(label)))
        await expect(element).to_contain_text(value)
        await settle(page)
        await element.evaluate("el => el.scrollIntoView({block: 'center'})")

    with tempfile.TemporaryDirectory(prefix="compass-release-") as temp:
        server = Server(Path(temp))
        try:
            await server.start()
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True, args=["--disable-background-networking", "--disable-component-update", "--disable-sync"])
                options = {"viewport": {"width": 1280, "height": 900}, "reduced_motion": "reduce"}
                if record:
                    options |= {"record_video_dir": str(output), "record_video_size": {"width": 1280, "height": 900}}
                context = await browser.new_context(**options)
                await configure(context)
                page = await context.new_page()
                page.set_default_timeout(15000)
                started = time.monotonic()

                async def checkpoint(number, caption, anchor=None):
                    await settle(page)
                    if anchor is not None:
                        await anchor.evaluate("el => el.scrollIntoView({block: 'center', behavior: 'instant'})")
                    await page.evaluate("""text => {
                      let banner = document.getElementById('demo-caption');
                      if (!banner) {banner=document.createElement('div'); banner.id='demo-caption'; document.body.appendChild(banner);}
                      banner.textContent=text;
                      Object.assign(banner.style,{position:'fixed',bottom:'0',left:'0',right:'0',padding:'16px 24px',background:'#102d2a',color:'white',font:'18px system-ui',zIndex:'999999',pointerEvents:'none'});
                    }""", f"FICTIONAL DATA · {caption}")
                    await page.screenshot(path=str(output / f"{number:02}-checkpoint.png"))
                    checkpoints.append(caption)
                    print(f"Checkpoint {number}: {caption}", flush=True)
                    if record:
                        await asyncio.sleep(max(0, started + number * 9 - time.monotonic()))

                await page.goto(server.url)
                await expect(page.get_by_text("No transactions imported yet.", exact=False)).to_be_visible()
                await page.get_by_role("button", name="Load fictional checking statement").scroll_into_view_if_needed()
                await checkpoint(1, "Start with an empty local workspace")

                await page.get_by_role("button", name="Load fictional checking statement").click()
                await metric(page, "Verified surplus", "$747.06")
                await page.get_by_role("button", name="Load fictional savings statement").click()
                await metric(page, "Accepted rows", "6")
                await metric(page, "Verified surplus", "$747.06")
                await checkpoint(2, "Import checking + savings · May surplus $747.06")

                await page.get_by_role("textbox", name="Your question", exact=True).fill("What was my surplus in May 2026?")
                await page.get_by_role("button", name="Ask Compass", exact=True).click()
                await metric(page, "Ask Compass result", "$747.06")
                await page.get_by_text("Answer evidence — included source rows", exact=True).scroll_into_view_if_needed()
                await expect(page.get_by_text("Answer evidence — included source rows", exact=True)).to_be_visible()
                await checkpoint(3, "Ask Compass · $747.06 surplus with source-row evidence",
                                 page.get_by_text("Answer evidence — included source rows", exact=True))

                await page.get_by_text("Review and correct classifications", exact=True).click()
                await settle(page)
                await page.get_by_role("combobox", name="Transaction to review", exact=True).click()
                await page.get_by_role("option").filter(has_text="ALDI").first.click()
                await settle(page)
                # Selecting a row reruns Streamlit and replaces the old row's form.
                await expect(page.get_by_role("textbox", name="Effective category", exact=True)).to_have_value("Groceries")
                await page.get_by_role("textbox", name="Effective category", exact=True).fill("Food at home")
                await page.get_by_role("button", name="Save classification", exact=True).click()
                await expect(page.get_by_text("Rows with saved overrides: 1 / 28", exact=True)).to_be_attached(timeout=15000)
                await settle(page)
                # A full st.rerun can rebuild the expander after saving the form.
                if not await page.get_by_role("textbox", name="Effective category", exact=True).is_visible():
                    await page.get_by_text("Review and correct classifications", exact=True).click()
                await expect(page.get_by_role("textbox", name="Effective category", exact=True)).to_have_value("Food at home")
                await settle(page)
                await page.get_by_role("textbox", name="Effective category", exact=True).click()
                await checkpoint(4, "Correct a category · original source data stays intact")

                await choose(page, "Rent mode", "replace")
                await metric(page, "Projected monthly surplus", "$522.06")
                await checkpoint(5, "Replace $1,275 rent with $1,500 · surplus $522.06")
                await choose(page, "Rent mode", "additional")
                await metric(page, "Projected monthly surplus", "−$752.94")
                await expect(page.get_by_text("Negative projected surplus:", exact=False)).to_be_visible()
                await checkpoint(6, "Additional $1,500 rent · surplus −$752.94")

                server.stop()
                await server.start()
                await page.reload()
                await metric(page, "Verified surplus", "$747.06")
                await checkpoint(7, "Restart the actual server · imported records persist")
                await page.get_by_text("Review and correct classifications", exact=True).click()
                await settle(page)
                await page.get_by_role("combobox", name="Transaction to review", exact=True).click()
                await page.get_by_role("option").filter(has_text="ALDI").first.click()
                await settle(page)
                await expect(page.get_by_role("textbox", name="Effective category", exact=True)).to_have_value("Food at home")
                await page.get_by_role("textbox", name="Effective category", exact=True).scroll_into_view_if_needed()
                await checkpoint(8, "Saved correction survives restart · fictional-data demo complete")
                video = page.video
                await context.close()
                if video:
                    await video.save_as(str(output / "compass-demo.webm"))
                    original = Path(await video.path())
                    if original.name != "compass-demo.webm":
                        original.unlink(missing_ok=True)

                mobile = await browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
                await configure(mobile)
                phone = await mobile.new_page()
                await phone.goto(server.url)
                await metric(phone, "Verified surplus", "$747.06")
                assert await phone.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), "Mobile page overflows horizontally"
                await phone.screenshot(path=str(output / "mobile-snapshot.png"))
                await choose(phone, "Rent mode", "additional")
                await metric(phone, "Projected monthly surplus", "−$752.94")
                await phone.screenshot(path=str(output / "mobile-scenario.png"))
                await mobile.close()

                deletion = await browser.new_context(viewport={"width": 1280, "height": 900})
                await configure(deletion)
                cleanup = await deletion.new_page()
                await cleanup.goto(server.url)
                await cleanup.get_by_text("Privacy and local data", exact=True).click()
                await settle(cleanup)
                await expect(cleanup.get_by_role("button", name="Clear all local data", exact=True)).to_be_disabled()
                await cleanup.get_by_text("I understand all imported Compass records will be deleted", exact=True).click()
                await expect(cleanup.get_by_role("checkbox", name="I understand all imported Compass records will be deleted", exact=True)).to_be_checked()
                await settle(cleanup)
                await cleanup.get_by_role("textbox", name="Type DELETE to confirm", exact=True).fill("DELETE")
                await cleanup.get_by_role("textbox", name="Type DELETE to confirm", exact=True).press("Enter")
                await settle(cleanup)
                await cleanup.get_by_role("button", name="Clear all local data", exact=True).click()
                await expect(cleanup.get_by_text("No transactions imported yet.", exact=False)).to_be_visible()
                await cleanup.reload()
                await expect(cleanup.get_by_text("No transactions imported yet.", exact=False)).to_be_visible()
                await expect(cleanup.get_by_role("button", name="Load fictional checking statement")).to_be_visible()
                await cleanup.screenshot(path=str(output / "deleted-empty-state.png"))
                await deletion.close()
                await browser.close()
            backend_egress = (server.directory / "egress.log").exists()
            report = {"ok": not outbound and not errors and not backend_egress,
                      "fictional_only": True, "temporary_database": True,
                      "actual_server_restart": True, "mobile_viewport": "390x844",
                      "confirmed_deletion_survived_reload": True,
                      "external_browser_hosts_attempted": sorted(set(outbound)),
                      "external_backend_attempts": backend_egress, "browser_errors": errors,
                      "checkpoints": checkpoints, "recorded": record}
            (output / "smoke-report.json").write_text(json.dumps(report, indent=2) + "\n")
            assert report["ok"], "Browser/privacy smoke failed; inspect smoke-report.json"
            print(json.dumps(report), flush=True)
        finally:
            server.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true", help="Hold eight checkpoints for a roughly 72-second video")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/release")
    args = parser.parse_args()
    asyncio.run(run(args.record, args.output.resolve()))
