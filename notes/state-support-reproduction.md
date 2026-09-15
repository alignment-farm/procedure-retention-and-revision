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

## Completed evidence

Diagnostic source `a31fde0`; acquisition/fresh protocol `795b649`; first fresh
crossing and final analysis behavior captured at `0115c04` and subsequent unchanged
model-run source snapshots. Fresh evidence was committed at `92521f4` (acquisition),
`6a2ca27` (501), and `66c35a2` (502). Audit sources include the strengthened target
and negative-boundary probe selector at `d1c4e62`. Exact run revisions remain in
events.jsonl, rather than being inferred from when an artifact was committed.

The completed `evidence/state-support-phase-audit/report.json` verifies4,736
response records,4,096 update-token records and221 reload probes across four
separate-process audits. Sixteen CPU instrument/schedule/probe tests pass.
There were no interrupted attempts or diagonal discrepancies in this phase.
The only failed readiness checkpoints were501/502 at256 updates; all remained
in the model audit. Every final checkpoint, including failed procedures, was
reloaded. Repeated revision-1 responses matched their first-pass responses.

Regenerate the complete phase ledger after the commands above, substituting your
new directories consistently:

```sh
uv run --no-sync python scripts/state_support_report.py --runs evidence/state-support-development-v1 evidence/state-support-fresh-acquisition-v1 evidence/state-support-final-seed501-v1 evidence/state-support-final-seed502-v1 --analyses evidence/state-support-development-v1-analysis-v2 evidence/state-support-final-seed501-v1-analysis evidence/state-support-final-seed502-v1-analysis --audits evidence/state-support-development-v1-audit evidence/state-support-fresh-acquisition-v1-audit evidence/state-support-final-seed501-v1-audit evidence/state-support-final-seed502-v1-audit --output evidence/NEW-STATE-SUPPORT-PHASE-AUDIT
```

Experimental totals:4,096 updates;366,020 input and32,768 loss tokens;4,736
generations with389,728 prompt and37,823 completion tokens;2,212.07 active seconds;
52,497,860 bytes of newly saved adapters. Audit127.07 seconds and221 generations
are separate. Prior artifact reuse and original acquisition are disclosed in the
findings. No candidate would deploy all twelve experimental revision-2 cells;
these totals are investigation costs, not a cost per maintained work order.
