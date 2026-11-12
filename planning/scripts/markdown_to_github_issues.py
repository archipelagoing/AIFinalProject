#!/usr/bin/env python3
"""Export Compass Markdown tickets as detailed GitHub Issues.

The default mode is read-only: it validates the plan and writes JSON payloads.
Use --create only after editing issue-assignees.json with real repository and
GitHub handles. Creation is protected by an explicit confirmation phrase.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLANNING = ROOT / "planning"
DEFAULT_PLAN = PLANNING / "COMPASS_ENGINEERING_PLAN.md"
DEFAULT_MATRIX = PLANNING / "COMPASS_COVERAGE_MATRIX.csv"
TICKET = re.compile(
    r"^- \[ \] \*\*(?P<id>CMP-[A-Z0-9-]+) — (?P<title>.+?)\.\*\* "
    r"\*\*Implementation:\*\* (?P<implementation>.*?) "
    r"\*\*Acceptance:\*\* (?P<acceptance>.*?) "
    r"\*\*Required evidence:\*\* (?P<evidence>.*)$"
)
OWNER = re.compile(r"^##### (?P<owner>Dev [1-4])(?: — .+)?$")
GATE_MILESTONES = {
    "CMP-1112-": "Gate 1 — Foundations",
    "CMP-1114-": "Gate 2 — Vertical Slice",
    "CMP-1119-": "Gate 3 — Wrapped Alpha",
    "CMP-1121-": "Gate 4 — End-to-End Beta",
    "CMP-1126-": "Gate 5 — Release Candidate",
    "CMP-1128-": "Gate 6 — Robustness Review",
}
GATE_FINAL_TICKETS = {
    "CMP-1112": "05",
    "CMP-1114": "03",
    "CMP-1119": "05",
    "CMP-1121": "03",
    "CMP-1126": "05",
    "CMP-1128": "03",
}
RISK_DELIVERY_PARTNERS = {
    "CMP-1112-D2-02": ("Dev 1", "Add edge-case fixtures and independently verify cents/sign/refund/transfer expectations."),
    "CMP-1112-D1-03": ("Dev 3", "Verify imported-row identity is compatible with model evidence references and safe tool inputs."),
    "CMP-1112-D2-04": ("Dev 4", "Implement and test the user-visible invalid-tool/evidence error state."),
    "CMP-1114-D3-02": ("Dev 2", "Audit financial examples, leakage boundaries, and deterministic tool-trace correctness."),
    "CMP-1119-D2-05": ("Dev 1", "Add source-data and correction/recompute cases to the golden suite."),
    "CMP-1119-D3-01": ("Dev 2", "Verify reproducibility metadata and evaluate numeric-grounding cases independently."),
    "CMP-1121-D2-03": ("Dev 1", "Add evidence/provenance failure cases and inspect unsupported-claim blocks."),
    "CMP-1119-D4-01": ("Dev 3", "Verify model identity, fixture-only responses, and safe handoff to constrained tools."),
    "CMP-1121-D4-01": ("Dev 3", "Audit held-out split integrity and reproduce the paired failure examples."),
    "CMP-1126-D2-01": ("Dev 4", "Automate the benchmark artifact view and verify a clean-machine run."),
    "CMP-1126-D3-01": ("Dev 1", "Audit synthetic-data provenance, split integrity, and evidence artifacts."),
    "CMP-1126-D3-03": ("Dev 2", "Verify no financial-data transmission and document the model-download exception."),
    "CMP-1126-D4-03": ("Dev 3", "Reproduce the device measurement and check the model/config evidence."),
    "CMP-1128-D4-01": ("Dev 3", "Test offline recovery, adapter identity, and model-integration failure handling."),
    "CMP-1128-D2-03": ("Dev 1", "Independently reconcile every displayed demo amount and chart axis to golden fixtures."),
}


@dataclass(frozen=True)
class Issue:
    identifier: str
    title: str
    owner: str
    implementation: str
    acceptance: str
    evidence: str
    source_line: int
    requirements: list[dict[str, str]]
    milestone: str | None = None

    @property
    def github_title(self) -> str:
        return f"[{self.identifier}] {self.title}"

    def body(self) -> str:
        profile = enrichment(self)
        requirements = "\n".join(
            f"- `{row['requirement_id']}` — {row['requirement_description']} "
            f"({row['mapping_status'].lower()}; {row['verification_status'].lower()})"
            for row in self.requirements
        ) or "- No candidate requirement mapping recorded."
        dependencies = "\n".join(f"- {identifier}" for identifier in profile["proposed_dependencies"]) or "- No blocking issue inferred; confirm shared contracts at kickoff."
        code_paths = "\n".join(f"- `{path}`" for path in profile["target_code_areas"])
        labels = ", ".join(f"`{label}`" for label in profile["labels"])
        return f"""## Goal

{profile["goal"]}

## Scope

{self.implementation}

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
{code_paths}

## Contract and safeguards

{profile["contract"]}

## UX and design requirements

{profile["design_reference"]}

## Non-goals

{profile["non_goals"]}

## Proposed dependency review

{dependencies}

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

{self.acceptance}

## Candidate requirement mapping

{requirements}

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `{profile["test_command"]}`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** {self.evidence}

## Ownership and source

- **Planned owner:** {self.owner}
- **Cross-owner reviewer role:** {profile["reviewer_role"]}
- **Risk delivery partner:** {profile["delivery_partner"] or "None; standard cross-owner review applies."}
- **Partner contribution:** {profile["partner_contribution"] or "N/A"}
- **Priority:** {profile["priority"]}
- **Issue type:** {profile["issue_type"]}
- **Estimate:** {profile["estimate_hours"]} hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** {labels}
- **Deadline milestone:** {self.milestone or "Set before creation"}
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line {self.source_line}](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L{self.source_line})
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.
"""


def enrichment(issue: Issue) -> dict[str, object]:
    """Return a conservative, ticket-specific execution profile from plan facts.

    These fields make the backlog ready for review, not immutable technical truth.
    Leads must confirm paths and inferred dependencies at kickoff.
    """
    words = f"{issue.title} {issue.implementation}".lower()
    if any(term in words for term in ("privacy", "deletion", "consent", "offline")):
        area = "privacy"
    elif issue.owner == "Dev 2" or any(term in words for term in ("cents", "spending", "financial", "refund", "transfer", "scenario", "x-ray", "chart")):
        area = "finance"
    elif issue.owner == "Dev 3" or any(term in words for term in ("slm", "model", "training", "qlora", "colab", "tool-call")):
        area = "model"
    elif issue.owner == "Dev 1" or any(term in words for term in ("import", "csv", "pdf", "transaction", "dataset", "coverage")):
        area = "data"
    elif any(term in words for term in ("test", "smoke", "accessibility", "benchmark", "qa")):
        area = "qa"
    else:
        area = "frontend"

    if any(term in words for term in ("benchmark", "evaluation", "colab", "training decision", "pilot", "rubric")):
        issue_type = "Research"
    elif any(term in words for term in ("test", "smoke", "regression", "property-based", "accessibility")):
        issue_type = "Test"
    elif any(term in words for term in ("schema", "contract", "migration", "seed", "setup", "record")):
        issue_type = "Task"
    else:
        issue_type = "Feature"

    p0_terms = ("import", "csv", "pdf", "schema", "cents", "refund", "transfer", "privacy", "deletion", "provenance", "tool", "evidence", "grounded", "duplicate")
    p2_terms = ("mascot", "animation", "motion", "polish", "stretch")
    priority = "P0" if any(term in words for term in p0_terms) else "P2" if any(term in words for term in p2_terms) else "P1"
    estimate = 5 if any(term in words for term in ("pdf", "qlora", "fine-tun", "end-to-end", "benchmark", "accessibility", "cross-platform")) else 2 if issue_type in {"Task", "Test"} else 3

    code_areas = {
        "data": ["compass/importer.py", "compass/mapping.py", "compass/db.py", "fixtures/", "tests/python/"],
        "finance": ["compass/contracts.py", "compass/analytics.py", "compass/questions.py", "compass/scenarios.py", "tests/python/"],
        "model": ["compass/ollama.py", "training/ (planned)", "evaluation/ (planned)", "tests/python/"],
        "frontend": ["docs/index.html", "docs/app.js", "docs/styles.css", "app.py", "tests/"],
        "qa": ["tests/", "scripts/", ".github/workflows/", "docs/"],
        "privacy": ["compass/db.py", "app.py", "scripts/audit_privacy.py", "tests/python/"],
    }[area]
    contracts = {
        "data": "Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.",
        "finance": "Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.",
        "model": "The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.",
        "frontend": "Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.",
        "qa": "Use synthetic fixtures only. Record reproducible commands and results; failure evidence is as important as a passing screenshot.",
        "privacy": "Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.",
    }[area]
    non_goals = {
        "data": "Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.",
        "finance": "Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.",
        "model": "Do not grant arbitrary tool/network access or train on real user statements.",
        "frontend": "Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.",
        "qa": "Do not change fixtures, thresholds, or evaluation splits merely to turn a failing check green.",
        "privacy": "Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.",
    }[area]
    test_command = "npm test" if area == "frontend" else "python -m pytest -q" if area != "qa" else "python -m pytest -q && npm test"
    reviewer = {"Dev 1": "Dev 2 (financial/data-contract review)", "Dev 2": "Dev 1 (data/provenance review)", "Dev 3": "Dev 4 (interaction and safety-state review)", "Dev 4": "Dev 3 (model-state and accessibility review)"}[issue.owner]
    gate_prefix = issue.identifier.split("-D", 1)[0]
    prior_gate = {"CMP-1112": None, "CMP-1114": "CMP-1112", "CMP-1119": "CMP-1114", "CMP-1121": "CMP-1119", "CMP-1126": "CMP-1121", "CMP-1128": "CMP-1126"}[gate_prefix]
    proposed_dependencies = ["CMP-1112-D1-01 — Repository and shared API contract"] if issue.identifier != "CMP-1112-D1-01" else []
    if prior_gate:
        developer = issue.identifier.split("-", 2)[2].split("-", 1)[0]
        proposed_dependencies.append(f"{prior_gate}-{developer}-{GATE_FINAL_TICKETS[prior_gate]} — Previous gate integration for {issue.owner}")
    labels = [f"priority:{priority}", f"area:{area}", f"type:{issue_type.lower()}", "needs:review"]
    if priority == "P0" and area in {"data", "finance", "privacy"}:
        labels.append("risk:financial-correctness")
    return {
        "goal": f"Deliver {issue.title.lower()} for the {issue.milestone or 'current delivery gate'} without weakening Compass's local-first, evidence-backed guarantees.",
        "priority": priority,
        "area": area,
        "issue_type": issue_type,
        "estimate_hours": estimate,
        "target_code_areas": code_areas,
        "contract": contracts,
        "design_reference": "Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.",
        "non_goals": non_goals,
        "proposed_dependencies": proposed_dependencies,
        "test_command": test_command,
        "reviewer_role": reviewer,
        "delivery_partner": RISK_DELIVERY_PARTNERS.get(issue.identifier, (None, None))[0],
        "partner_contribution": RISK_DELIVERY_PARTNERS.get(issue.identifier, (None, None))[1],
        "labels": labels,
    }


def load_matrix(path: Path) -> dict[str, list[dict[str, str]]]:
    mapping: dict[str, list[dict[str, str]]] = {}
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            mapping.setdefault(row["ticket_id"], []).append(row)
    return mapping


def parse_plan(plan: Path, matrix: Path, milestones: dict[str, str] | None = None) -> list[Issue]:
    requirements = load_matrix(matrix)
    issues: list[Issue] = []
    owner = "Unassigned"
    for line_number, line in enumerate(plan.read_text(encoding="utf-8").splitlines(), start=1):
        if match := OWNER.match(line):
            owner = match["owner"]
            continue
        if match := TICKET.match(line):
            identifier = match["id"]
            milestone = next((name for prefix, name in (milestones or GATE_MILESTONES).items() if identifier.startswith(prefix)), None)
            issues.append(Issue(
                identifier=identifier,
                title=match["title"],
                owner=owner,
                implementation=match["implementation"],
                acceptance=match["acceptance"],
                evidence=match["evidence"],
                source_line=line_number,
                requirements=requirements.get(identifier, []),
                milestone=milestone,
            ))
    ids = [issue.identifier for issue in issues]
    if len(issues) != 96 or len(set(ids)) != len(ids):
        raise ValueError(f"Expected 96 unique CMP tickets; found {len(issues)} ({len(set(ids))} unique).")
    if any(issue.owner == "Unassigned" for issue in issues):
        raise ValueError("At least one ticket is missing a Dev 1–4 owner heading.")
    return issues


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    if not config.get("repo") or config["repo"] == "OWNER/REPOSITORY":
        raise ValueError("Set a real owner/repository in the assignee config.")
    if not isinstance(config.get("assignees"), dict):
        raise ValueError("The assignee config must include an assignees object.")
    if config.get("milestones") is not None and not isinstance(config["milestones"], dict):
        raise ValueError("milestones must map CMP prefixes to existing GitHub milestone titles.")
    return config


def issue_exists(repo: str, title: str) -> bool:
    result = subprocess.run(
        ["gh", "issue", "list", "--repo", repo, "--state", "all", "--search", f'"{title}" in:title', "--json", "title"],
        check=True, capture_output=True, text=True,
    )
    return any(issue["title"] == title for issue in json.loads(result.stdout))


def create_issues(issues: list[Issue], config: dict, limit: int | None) -> None:
    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI (gh) is required for --create. Install it and run `gh auth login`.")
    selected = issues[:limit] if limit else issues
    for issue in selected:
        if issue_exists(config["repo"], issue.github_title):
            print(f"SKIP existing: {issue.github_title}")
            continue
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as body_file:
            body_file.write(issue.body())
            body_path = Path(body_file.name)
        try:
            command = ["gh", "issue", "create", "--repo", config["repo"], "--title", issue.github_title, "--body-file", str(body_path)]
            for label in dict.fromkeys([*config.get("labels", []), *enrichment(issue)["labels"]]):
                command.extend(["--label", label])
            if handle := config["assignees"].get(issue.owner):
                command.extend(["--assignee", handle])
            if milestone := issue.milestone or config.get("milestone"):
                command.extend(["--milestone", milestone])
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"CREATED {issue.identifier}: {result.stdout.strip()}")
        finally:
            body_path.unlink(missing_ok=True)


def developer_guide(owner: str, issues: list[Issue]) -> str:
    """Render one developer's complete, reviewable implementation guide."""
    primary = [issue for issue in issues if issue.owner == owner]
    partner = [issue for issue in issues if enrichment(issue)["delivery_partner"] == owner]
    role = {
        "Dev 1": "Import to insight — data provenance, import/review experience, and financial evidence.",
        "Dev 2": "Spending to decisions — financial correctness, deterministic tools, and evidence-backed decision flows.",
        "Dev 3": "Model science to interaction — training, evaluation, grounded conversation, and meaningful model-driven interaction.",
        "Dev 4": "Runtime to reliable journey — safe tool execution, adapter/runtime integration, consumer-device performance, and end-to-end reliability.",
    }[owner]
    text = f"# {owner} implementation guide\n\n"
    text += f"**Product slice:** {role}\n\n"
    text += "> This guide lists your 24 primary tickets and required risk-partner work. It is generated from the authoritative planning backlog; do not mark a ticket complete without the specified evidence and cross-owner review.\n\n"
    text += "## Definition of done for every ticket\n\n"
    text += "- Implement only the approved scope and retain the product's local-first/evidence-backed guarantees.\n- Run the stated verification command using synthetic fixtures.\n- Link the PR, test output, and screenshot/log/JSON evidence.\n- Obtain the named cross-owner review and record pass/fail against acceptance criteria.\n\n"
    text += "## Required risk-partner contributions\n\n"
    if partner:
        for issue in partner:
            profile = enrichment(issue)
            text += f"- **{issue.identifier} — {issue.title}** (primary: {issue.owner}): {profile['partner_contribution']}\n"
    else:
        text += "No extra risk-pair contribution is currently assigned. Continue cross-review responsibilities.\n"
    text += "\n## Primary ticket backlog\n"
    current_milestone = None
    for issue in primary:
        profile = enrichment(issue)
        if issue.milestone != current_milestone:
            current_milestone = issue.milestone
            text += f"\n## {current_milestone}\n"
        dependencies = "; ".join(profile["proposed_dependencies"]) or "Confirm at technical kickoff; no inferred blocker."
        partner_line = f"{profile['delivery_partner']} — {profile['partner_contribution']}" if profile["delivery_partner"] else "No risk delivery partner; obtain the standard cross-owner review."
        paths = ", ".join(f"`{path}`" for path in profile["target_code_areas"])
        text += f"\n### {issue.identifier} — {issue.title}\n\n"
        text += f"**Priority/type/estimate:** {profile['priority']} · {profile['issue_type']} · {profile['estimate_hours']} hours\n\n"
        text += f"**Goal:** {profile['goal']}\n\n"
        text += f"**Scope:** {issue.implementation}\n\n"
        text += f"**Target code areas:** {paths}\n\n"
        text += f"**Contract and safeguards:** {profile['contract']}\n\n"
        text += f"**Non-goals:** {profile['non_goals']}\n\n"
        text += f"**Dependencies to confirm:** {dependencies}\n\n"
        text += f"**Risk partner:** {partner_line}\n\n"
        text += f"**Acceptance:** {issue.acceptance}\n\n"
        text += f"**Verify:** `{profile['test_command']}`; attach {issue.evidence}\n"
    return text


def write_developer_guides(directory: Path, issues: list[Issue]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    index = """# Compass developer guides

Generated from the enriched 96-ticket backlog. Read the guide matching your assigned developer role. Each person owns a visible product slice, tests, integration evidence, and cross-domain risk work—not a narrow support-only function.

## Main contribution by developer

| Developer | Main contribution | Must also contribute |
| --- | --- | --- |
| Dev 1 | Import-to-insight: statement ingestion, provenance, correction/review, coverage, and evidence integrity. | Financial golden cases, model/data provenance review, frontend flows, and integration tests. |
| Dev 2 | Spending-to-decisions: exact financial rules, deterministic tools, X-Ray, insights, scenarios, and numerical audit. | Import/model data checks, UI delivery, reproducibility work, and cross-feature tests. |
| Dev 3 | Model-science-to-interaction: training, grounded conversation, evaluation, uncertainty, and meaningful model-driven interaction. | Import/evidence compatibility, financial claim checks, interaction design, and end-to-end integration. |
| Dev 4 | Runtime-to-reliable-journey: safe tool execution, adapter/runtime integration, consumer-device performance, and complete-flow reliability. | Frontend implementation, accessible interaction states, model/finance benchmark evidence, and release testing. |

## Saturday merge rubric — November 28, 2026

When all feature branches are merged into `main`, evaluate a **fresh checkout of `main`** using only synthetic fixtures. Record the result in the Gate 6 parent issue and attach commands, logs, screenshots, benchmark JSON, and remaining-defect links. This scores closeness to a release candidate; it does not replace individual ticket acceptance.

| Category | Points | What must be demonstrated |
| --- | ---: | --- |
| Financial and data correctness | 30 | Exact-cent golden suite; imports/corrections/refunds/transfers/unknowns reconcile; every shown total has inspectable evidence. |
| Complete user journey | 20 | Import → review/correct → Ask → X-Ray → Wrapped → Confessional → What If? → deletion works from a clean checkout. |
| Grounded model behavior and evaluation | 15 | Tool allowlist/schema blocks invalid calls; no unsupported numeric claim in release suite; base-vs-tuned evidence and local performance results are attached. |
| Privacy, resilience, and safety | 15 | Local-only/offline boundary tested, deletion verified, malformed input handled, no real financial data/telemetry, and no unresolved P0/P1 privacy or safety defect. |
| Accessibility and responsive quality | 10 | Keyboard, reduced motion, contrast, screen-reader alternatives, and supported mobile/desktop layouts pass documented checks. |
| Release evidence and reproducibility | 10 | Clean setup, CI, fixtures, model/config hashes, benchmark commands/results, known limitations, and demo evidence are present. |
| **Total** | **100** | **Score only from attached evidence, never from claimed completion.** |

### Hard gates

- **Not releasable regardless of score:** any P0 defect; fabricated/unsupported financial amount; privacy or deletion failure; broken clean-checkout core journey; or missing evidence for a claimed benchmark.
- **90–100:** release-candidate ready; only documented P2 issues remain.
- **75–89:** conditionally complete; merge is acceptable, but freeze requires an explicit owned repair list and rerun of affected evidence.
- **Below 75:** not ready for freeze; stop stretch/polish work and swarm the lowest-scoring category.

### Required Saturday evidence by developer

- **Dev 1:** import/provenance/privacy result, coverage checks, and source-data fixture evidence.
- **Dev 2:** financial golden-suite result, evidence/X-Ray audit, and scenario/chart verification.
- **Dev 3:** base-vs-tuned comparison, safety/grounding result, latency/RAM measurement, and model/config hash.
- **Dev 4:** full end-to-end recording/log, accessibility/responsive audit, usability/demo evidence, and known-issues list.

## Individual guides

"""
    for owner in ("Dev 1", "Dev 2", "Dev 3", "Dev 4"):
        filename = f"{owner.replace(' ', '_')}_README.md"
        (directory / filename).write_text(developer_guide(owner, issues), encoding="utf-8")
        index += f"- [{owner}]({filename})\n"
    (directory / "README.md").write_text(index, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--output", type=Path, help="Write issue payloads as JSON; default prints a summary.")
    parser.add_argument("--markdown-output", type=Path, help="Write all enriched issue descriptions as a readable Markdown review file.")
    parser.add_argument("--developer-guides-dir", type=Path, help="Write one complete Markdown implementation guide for each developer.")
    parser.add_argument("--config", type=Path, help="JSON config with repository, labels, milestone, and Dev 1–4 handles.")
    parser.add_argument("--create", action="store_true", help="Create non-duplicate issues through GitHub CLI.")
    parser.add_argument("--confirm", help='Required with --create: exactly "CREATE COMPASS ISSUES".')
    parser.add_argument("--limit", type=int, help="Create/export only the first N tickets (useful for a pilot).")
    args = parser.parse_args()

    config = load_config(args.config) if args.config else {}
    issues = parse_plan(args.plan, args.matrix, config.get("milestones"))
    selected = issues[:args.limit] if args.limit else issues
    payload = [{**asdict(issue), "enrichment": enrichment(issue), "github_title": issue.github_title, "body": issue.body()} for issue in selected]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {len(payload)} detailed issue payloads to {args.output}")
    else:
        print(f"Validated {len(issues)} tickets; selected {len(selected)}. Use --output to inspect JSON or --create to publish.")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        review = "# Compass enriched GitHub Issue review\n\n"
        review += "> Local review artifact. Validate proposed priorities, paths, dependencies, estimates, and labels before creating GitHub Issues.\n\n"
        review += "\n\n---\n\n".join(f"# {issue.github_title}\n\n{issue.body()}" for issue in selected) + "\n"
        args.markdown_output.write_text(review, encoding="utf-8")
        print(f"Wrote {len(selected)} readable issue descriptions to {args.markdown_output}")
    if args.developer_guides_dir:
        write_developer_guides(args.developer_guides_dir, issues)
        print(f"Wrote 4 developer implementation guides to {args.developer_guides_dir}")

    if args.create:
        if args.confirm != "CREATE COMPASS ISSUES":
            raise ValueError('Refusing to create issues. Re-run with --confirm "CREATE COMPASS ISSUES" after reviewing the JSON output.')
        if not args.config:
            raise ValueError("--create requires --config planning/issue-assignees.json")
        create_issues(selected, config, args.limit)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
