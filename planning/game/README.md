# Compass game planning

This folder presents the Compass delivery plan as a cooperative systems game. It is planning material only. Product requirements remain in [`PRODUCT_SPEC.md`](../../PRODUCT_SPEC.md); the team split and delivery decisions remain in [`TEAM_SPLIT_DRAFT.md`](../TEAM_SPLIT_DRAFT.md).

## Play it

From this folder, run:

```sh
python3 compass_sorry.py
```

After an issue's code, test, and evidence are accepted, choose `i`, enter the player and GitHub issue ID, and roll. Use `g` only after the team passes its actual Thursday/Saturday checkpoint. The game saves locally in `saves/`, which is ignored by Git.

## Planned GitHub roll verification

The current game asks the team to confirm that an issue's evidence was accepted. A future `sync` command can verify GitHub activity before allowing a roll:

```text
Developer pushes a commit
→ game checks GitHub for a newer commit from that player
→ player enters the completed issue ID
→ team confirms evidence
→ game allows the roll and records that commit SHA
```

The save would store each player's last verified commit SHA. A player could not earn another roll until GitHub shows a newer commit. The first version should use the installed `gh` command after `gh auth login`, rather than saving a GitHub token in the game file.

New commits show activity; they do not prove a feature is complete. The recommended rule is **new commit + issue ID + accepted evidence**. A stricter later version can require a linked pull request with passing checks or a merge before a roll.

## The win condition

The team wins when a person can complete this trustworthy local journey:

```text
Import a supported statement
→ review or correct records
→ discover a financial story
→ inspect the source receipts
→ ask Compass a question
→ explore a conditional What If?
→ delete local data successfully
```

The final submission also needs evidence that the finance calculations are correct, the model was genuinely evaluated, the application works locally, and the report only makes claims supported by measured results.

## Players and their pieces

| Player | Piece | Owns | Does not own |
| --- | --- | --- | --- |
| A | Records and app foundation | App shell/navigation, import/review, corrections, coverage, privacy/deletion, local setup | Finance rules, model training, conversation runtime, other players' bugs |
| B | Financial story | Financial tools, evidence/X-Ray, charts, Guess/Reveal, awards, What If?, Wrapped pages | App-wide navigation, training, conversation runtime, packaging |
| C | Model lab | Synthetic data, baseline, fine-tuning, model export, evaluation, error analysis | Product UI, runtime integration, packaging |
| D | Conversation engine | Local inference, tool validation/dispatch, chat, Confessional, consented memory, runtime tests | App shell, Wrapped pages, whole-product QA, packaging |

Each player delivers their own implementation, tests, setup notes, evidence, and report contribution. Having Codex does not make a player the automatic integrator or cleanup person.

## Rules of play

1. **Own the result, not merely a pull request.** A feature is complete only with its behavior, verification, setup note, and evidence.
2. **Hand off a contract, not an idea.** Before another player depends on work, provide an input/output example, expected result, known limitations, and a way to verify it.
3. **A failure returns to the subsystem that caused it.** The demo runner logs the issue; the feature owner repairs it.
4. **Freeze shared interfaces before parallel work.** Change a shared schema only after telling its consumers and updating its fixture/example in the same change.
5. **Fixtures are allowed during construction, but they are not the finish line.** Mark fixture-backed UI clearly; call it complete only after the real integrated path works.
6. **Financial correctness, privacy, and deletion are hard gates.** If any of these fail, feature polish and stretch work stop until the issue is repaired.
7. **The model may choose an approved tool but may not invent money.** B's deterministic tools calculate totals; model-generated text must carry verified evidence for numerical claims.
8. **Conversation context is not financial truth.** Confessional or memory input requires consent, can be forgotten, and cannot rewrite transaction records or be presented as a verified fact.
9. **Integration is planned work.** Every checkpoint includes time to connect components and run the shared journey. This counts toward workload.
10. **Rebalance named tasks, not vague anxiety.** Transfer a bounded task with an outcome, estimate, and new owner; do not assign “help with whatever is needed.”
11. **Do not claim more than the evidence shows.** A demo, small pilot, or unverified ticket is not proof of product impact, model quality, or user demand.
12. **No silent scope growth.** New file formats, animations, model experiments, or story features wait until the core journey and hard gates are passing.

## Handoff cards

Before passing a piece to another player, the producing player supplies a small handoff card.

| From → to | Required card |
| --- | --- |
| A → B/D | Transaction ID, immutable source reference, corrected fields, account/date coverage, invalid-row error example |
| B → C/D | Tool name and argument schema, exact-cent result, included/excluded IDs, formula, coverage, unsupported-request result |
| C → D | Model/adapter revision, export/loading instructions, prompt/tool format, sample response, context limit, behavior limitations |
| D → A/B | Conversation-state requirements, runtime startup requirements, successful and failed chat examples |

## Rounds and checkpoints

| Round | Dates | Shared objective |
| --- | --- | --- |
| Round 1 | Nov 11–14 | Connect the first journey: import → correction → question → receipt |
| Round 2 | Nov 16–21 | Complete the product loop: Wrapped → evidence → conversation → What If? → delete |
| Round 3 | Nov 23–28 | Verify data, finance, model behavior, runtime safety, accessibility, and local setup |
| Final round | Nov 29–Dec 3 | Repair release-blocking failures, freeze the measured version, record the demo, and write the report |

Thursday and Saturday are review deadlines, not starting lines. Before each checkpoint, every player posts what works, evidence, blockers, and the next handoff. The coordinator runs the checklist; they do not inherit ownership of discovered failures.

## Hard gates and scoring evidence

The team cannot call the product ready with any of the following:

- Incorrect or unsupported displayed financial amount.
- Fabricated transaction or missing evidence for a numerical claim.
- Privacy or deletion failure.
- Broken supported core journey from a clean setup.
- Missing evidence for a claimed benchmark or study result.

The score is evidence, not confidence: automated tests, reproducible commands, benchmark JSON, screenshots/recordings, reviewed fixtures, and written known limitations.

## Final boss

From a clean local setup, use fictional data to complete the entire journey. Then prove the financial totals, model version and evaluation results, privacy/deletion behavior, and known limitations. Freeze those artifacts before writing the final report. Each player supplies their own report section, figure or table, limitations paragraph, and reproducibility note.
