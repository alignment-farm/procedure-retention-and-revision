# State/support reproduction

Use the locked environment and hash-verified Qwen3-4B model described in
maintenance-reproduction.md. Native MLX performs actual gradient updates;
no serving endpoint is used for training. Run commands sequentially with new
output directories; runners yield to observed sibling Python model scripts.

Diagnostic protocol: protocol/state-support-development-v1.md, source a31fde0.
The run snapshots its exact executed files before model loading. Both starting
states and diagonal outputs must exactly reproduce the accepted publication;
diagonal adapter bytes must also match. Full original SHA256SUMS is checked.

```sh
uv run --no-sync python -m unittest discover -s tests -v
uv run --no-sync python scripts/state_support_experiment.py --output evidence/NEW-CROSSING
uv run --no-sync python scripts/state_support_analyze.py evidence/NEW-CROSSING --output evidence/NEW-CROSSING-ANALYSIS
uv run --no-sync python scripts/state_support_audit.py evidence/NEW-CROSSING --output evidence/NEW-CROSSING-AUDIT
```

Analysis re-executes the independent scorer, verifies complete schedules, matched
restores, manifests, and paired unchanged outcomes. Audit retokenizes every
response and update and reloads all endpoint adapters in a separate process,
covering both revised scopes, familiar and fresh entities, and failed outputs.
Audit calls are not new accuracy samples. Observed execution time is not an
isolated hardware benchmark. Cached primary sources and adaptation scope remain
in state-support-methods.md.

## Frozen fresh assessment

Protocol and acquisition/crossing source fixed at795b649. The acquisition runner
saves both histories for every ready seed, with no revision-1 success filter.
The crossing's `--phase final` disables only comparison against nonexistent
published revision-2 results; it still verifies the entire input manifest and
reproduces every recorded starting output after reload.

```sh
uv run --no-sync python scripts/state_support_acquire.py --output evidence/NEW-ACQUISITIONS
uv run --no-sync python scripts/state_support_experiment.py --phase final --seed 501 --start-run evidence/NEW-ACQUISITIONS --output evidence/NEW-SEED501
uv run --no-sync python scripts/state_support_experiment.py --phase final --seed 502 --start-run evidence/NEW-ACQUISITIONS --output evidence/NEW-SEED502
uv run --no-sync python scripts/state_support_analyze.py evidence/NEW-SEED501 --output evidence/NEW-SEED501-ANALYSIS
uv run --no-sync python scripts/state_support_analyze.py evidence/NEW-SEED502 --output evidence/NEW-SEED502-ANALYSIS
uv run --no-sync python scripts/state_support_audit.py evidence/NEW-ACQUISITIONS --output evidence/NEW-ACQUISITIONS-AUDIT
uv run --no-sync python scripts/state_support_audit.py evidence/NEW-SEED501 --output evidence/NEW-SEED501-AUDIT
uv run --no-sync python scripts/state_support_audit.py evidence/NEW-SEED502 --output evidence/NEW-SEED502-AUDIT
```

Use the acquisition criterion events to retain and diagnose any exhausted ladder;
do not run missing-checkpoint commands for a seed that never acquired the task.
All observed attempts belong in the report, including failed readiness and
incomplete revision-1 states. The full-phase report accepts `--runs`, `--analyses`,
`--audits`, and a new `--output`; pass development plus both fresh crossings,
acquisition, and their four corresponding audit directories. It checks schedules,
readiness selection, repeat identity, response scoring, hashes and audit counts,
then reports per-seed interactions and native-unit investigation costs.

The initial diagnostic analysis is retained. `state-support-development-v1-analysis-v2`
adds actual directly trained cases and waiver-by-identity breakdowns without changing
any endpoint, denominator or selection; exact analysis source is snapshotted.
