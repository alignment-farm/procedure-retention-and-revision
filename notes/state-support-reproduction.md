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
