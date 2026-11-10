# Fictional Compass release demo

[Watch/download the 72.76-second MP4](compass-demo.mp4).

Recorded on 2026-11-10 using the real local Streamlit UI at 1280×900, an isolated Chromium profile, and a temporary database containing only the bundled fictional statements. There is no audio; on-screen captions explain each step. The server is actually stopped and started with the same temporary database during the restart segment. The user's default database is never opened.

| Approximate time | Shown |
| --- | --- |
| 0–9s | Empty local workspace and fictional-demo controls |
| 9–18s | Checking and savings imports; May surplus $747.06 |
| 18–27s | Ask Compass calculation and included source rows |
| 27–36s | ALDI category changed to Food at home; original prediction retained |
| 36–45s | Replacement rent: $522.06 surplus and static extrapolation |
| 45–54s | Additional rent: −$752.94 surplus and warning |
| 54–63s | Actual server restart; imports persist |
| 63–72.76s | Saved category visible after restart |

[Answer evidence screenshot](answer-evidence.png), [390×844 mobile scenario](mobile-scenario.png), and [empty state after confirmed deletion/reload](empty-after-delete.png) provide still evidence. The [browser smoke report](smoke-report.json) is from a separate successful smoke run of the same story, followed by mobile and deletion checks. `recorded: false` describes that smoke run, not the accompanying MP4. It observed no external browser hosts/backend attempts or uncaught browser errors. This is scoped test evidence, not a security certification or physical-phone test.

Reproduce with `python scripts/release_smoke.py --record` after the optional tooling setup in the [root README](../../README.md#release-smoke-and-recorded-demo). The script records a WebM in ignored `artifacts/release/`; this MP4 was converted with local FFmpeg using H.264, CRF 26, yuv420p and fast-start metadata. The encoded frame, screenshots and duration were inspected. No generated server logs, personal uploads, browser profile or database are included in these published assets.
