# Compass — GitHub Pages prototype

This is the browser implementation of the core workflow in [`ProtoToDo.md`](../archive/alpha-0.1/ProtoToDo.md). The implemented Python/Streamlit application is separate; see the [repository guide](../REPOSITORY_GUIDE.md). This edition is dependency-free HTML, CSS, and JavaScript, with browser localStorage replacing SQLite. No Python server, cloud AI, account, or API key is used by the published app.

## Run locally

From the repository root, with Python 3 installed:

```sh
python3 -m http.server 4173 --directory docs
```

Open http://localhost:4173/. Alternatively run `npm start` with Node installed. On Windows, `py -3 -m http.server 4173 --directory docs` also works. Use HTTP rather than opening `index.html` as a file: JavaScript modules and demo CSV fetching require a web origin.

## Automated verification

Requires Node.js 22 or later; no `npm install` is necessary.

```sh
npm test
```

Tests cover all 164 reference classifications, six monthly totals, integer cents, malformed and duplicate imports, conflict handling, refund/transfer exclusions, corrections, saved-state reopening/deletion, five question intents, and the exact May scenarios. Test oracles stay outside `docs/` and are never inputs to production calculations.

The published demo, source evidence, category correction/recalculation, reload persistence, rent scenarios, June unresolved warning, and a roughly 520-pixel layout were verified in native Chrome on 2026-11-10. See [BROWSER_QA.md](../archive/alpha-0.1/BROWSER_QA.md) in the source repository. Uploaded-file picker errors, actual confirmed browser deletion, physical-phone testing, and full keyboard/screen-reader coverage remain pending. Passing unit tests is not evidence that these remaining checks passed.

## Deploy from the main repository

The workflow at [`.github/workflows/pages.yml`](../.github/workflows/pages.yml) tests changes, then publishes **only `docs/`** from `main`. Pull requests run checks without publishing.

1. In `archipelagoing/AIFinalProject`, open **Settings → Pages**.
2. Select **GitHub Actions** as the publishing source.
3. Commit and push the prototype files to `main`.
4. Check **Actions → Test and deploy Compass to GitHub Pages**. If the source setting was enabled after a push, use **Run workflow**.
5. After a successful deployment, use the URL shown in the workflow's `github-pages` environment. The standard project URL is `https://archipelagoing.github.io/AIFinalProject/`.

All application URLs are relative, including styles, JavaScript modules, icons, and demo CSVs. No build step or router fallback is required. Navigation uses hashes, so refreshes on `#transactions`, `#ask`, and `#whatif` keep working.

GitHub's workflow setup reference: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Demo walkthrough

1. Open the app in a fresh browser workspace. Choose **Explore fictional demo**.
2. May 2026 should show income **$3,700.00**, net expenses **$2,952.94**, and surplus **$747.06**. Click a metric to inspect evidence.
3. Open **Ask Compass** and choose a supported question. Expand its evidence rows.
4. Open **Transactions**, review a row, change its category, and save. The source data stays unchanged; category totals and answers recalculate.
5. Open **What If?**. Keep proposed rent at **$1,500**, confirm the existing **$1,275** rent, and calculate in replacement mode: **$522.06** monthly surplus, **$3,132.36** over six static months.
6. Switch to additional rent: **−$752.94** monthly, **−$4,517.64** over six static months. Existing rent remains in the baseline.
7. Select June. The **$80 ATM withdrawal** remains unresolved and excluded from verified totals. Review it as an expense to see the surplus change.
8. Reload to verify that imports and classification corrections remain. Reimporting the identical source, even under a renamed filename, adds no records and preserves corrections.
9. **Clear saved data** requires a confirmation checkbox. Reload to verify empty state; demo files remain available. On small screens, deletion and privacy controls are in the footer.

## Supported CSV and storage contract

```csv
date,description,amount,account,transaction_id
2026-05-01,OAK TERRACE APARTMENTS RENT,-1275.00,Checking,example-1
```

- Date: real `YYYY-MM-DD` calendar date. Amount: exact signed decimal; at most two fractional digits. Positive means inflow, negative means outflow.
- All five headers are required. A transaction ID cell may be blank when the source has no IDs; identity then uses statement SHA-256 and row ordinal.
- Quoted commas, escaped quotes, UTF-8 BOM, CRLF, and quoted multiline values are supported. UI files are limited to 5 MB; browser quota may be lower in practice. Storage failures are visible and preserve existing saved data.
- Imports are staged and saved atomically. An invalid row rejects the entire statement with its record number. Renamed identical files are recognized by content digest.
- Distinct IDs scoped by account preserve repeated purchases. Distinct rows without IDs also survive within one file. Overlapping IDs, conflicting IDs, or identical-looking cross-file purchases block the incoming statement with an explanation; source review is required. There is no automatic merge or overlap-resolution UI yet.
- Original row values, source amount, filename, import digest, account, source ID and source record number are preserved. Classification overrides are separate.
- Rules recognize supplied demo descriptions; unmatched descriptions remain unknown. Rule explanations can be inspected in each review dialog. Custom category names are supported.
- `income` adds to verified income; negative `expense` increases expenses; positive `refund` reduces category expenses; `transfer` and `unknown` are excluded. Income/refund/expense corrections must agree with the original amount's sign.
- The baseline is classified income minus net expenses. All monetary arithmetic uses safe integer cents; unsafe ranges are rejected.
- Replacement rent requires explicit confirmation of rent already included in the baseline, including when one candidate is detected. It never silently uses all Housing spending. Changes to classifications require reconfirmation.
- Projection = baseline + income change − added spending − rent delta. Rent delta = proposed − existing for replacement, or full proposed rent for additional. Six months = 6 × projected surplus.

## Supported questions

- “How much did I earn?”
- “What were my expenses?”
- “How much did I spend on restaurants?”
- “What were my five largest expenses?”
- “What was my surplus?”

Questions use the selected month. Add `in May 2026` or `in 2026-05` to select another imported month. A month name without a year is accepted only when exactly one imported month matches. Unrecognized or ambiguous questions are rejected with supported examples; there is no unrestricted chat model.

## Privacy boundary and limitations

The host serves static files; the app optionally fetches the two fictional CSVs from the same host. User-selected CSV contents are never sent by the application to a backend, model, or analytics service. No third-party scripts, fonts, telemetry, or CDNs are included. Host requests still expose normal web-request metadata to the hosting provider.

Records, original row values, filenames, and corrections are saved under `compass:alpha:1` in browser localStorage. They survive reloads on the same origin/profile, but can be lost if storage is cleared, blocked, full, or evicted. Other scripts on the same origin can access browser storage. This prototype does not encrypt local records, back them up, or provide a security-audited vault. Use fictional data for the public demo.

Clear-data removes only the Compass storage key; it does not remove other applications' data or bundled fixtures. Browser storage is per origin, not per repository path. Test deployments and localhost therefore have separate workspaces.

Activity dates are displayed, but full statement coverage is unverified. Transfer pairs need unique same-date/opposite-amount evidence across accounts; incomplete evidence is flagged. “Reviewed” describes classification review and never means bank reconciliation. No starting balances are available, so surplus and six-month results are not account balances. Projections are illustrative, with no statistical confidence claims.

Deferred: Streamlit/SQLite, Ollama/SLM integration and evaluation, PDF/OCR, arbitrary column mapping, automatic bank sync, saved scenarios, savings targets, export/backup, recorded demo video, and production security review. This browser prototype does not claim completion of the original local-app alpha or the four-week AI research project.
