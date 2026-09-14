# Reproduction (execution in progress)

Run on Apple Silicon with 64 GiB unified memory. Use uv; the lock pins MLX0.32.2
and MLX-LM 86b48c461feebf87c58788655b7e57b5574b9e6d. No Docker inference endpoint
is used as a training API. All experiments use native gradients.

```
uv sync --python 3.14.7 --extra adaptation --frozen
uv run --no-sync python -c 'from huggingface_hub import snapshot_download; snapshot_download("Qwen/Qwen3-4B-Instruct-2507", revision="cdbee75f17c01a7cc42f958dc650907174af0554", local_dir="models/qwen3-4b-instruct", allow_patterns=["*.json", "*.safetensors", "*.jinja", "*.txt"])'
uv run --no-sync python -m unittest discover -s tests -v
uv run --no-sync python scripts/experiment.py --output evidence/NEW-DEVELOPMENT
uv run --no-sync python scripts/analyze.py evidence/NEW-DEVELOPMENT
uv run --no-sync python scripts/audit_saved.py evidence/NEW-DEVELOPMENT
```

A local read-only-use model symlink avoids downloading another copy during this
session. Independent reproduction needs only the pinned model, owned runtime,
committed inherited adapters and manifests, not a sibling checkout. Runtime
checks model file hashes against sources/model-reference.json before training.
Sources/checkpoints/provenance.json pins inherited binary hashes. Parent study's
acquisition attempts and selection rule are disclosed in sources/README.md.

Each run rejects an existing output directory, snapshots its executable sources
and protocol, logs the code commit, every update and generation, saves all named
checkpoints and hashes every output. Analyzer output and reload audit use new
sibling directories. Never overwrite or silently replace completed or failed
runs. A KeyboardInterrupt writes a failed status and partial hash manifest.
Reload audit checks tokens from all generations and re-generates three cases
per checkpoint in a separate process; these repeats do not enter accuracy counts.

Before loading the model the runner yields to visible sibling experiment or
confirmatory processes. Rechecks occur between operations at five-second
intervals. This is cooperative observation, not an atomic reservation; disclose
any overlap and do not treat the timers as isolated performance benchmarks.
The process monitor is optional, writes only a local log, and launches no jobs.

The partial first development attempt has 136 generations and 30 logged updates;
an interrupted in-flight update can be unlogged. It is retained at 22fd99e and
summarized in notes/interrupted-attempt.json. The second attempt starts from the
original acquired adapter, not the partially modified first-attempt state.

The fixed fresh comparison is run with:

```
uv run --no-sync python scripts/experiment.py --phase final --output evidence/NEW-FINAL
uv run --no-sync python scripts/analyze.py evidence/NEW-FINAL
uv run --no-sync python scripts/audit_saved.py evidence/NEW-FINAL
```

Final protocol evolved prospectively at a43e449, f858aa4 and8356de8; measured
resource sizing and completed development are at9747992, the final run's code
revision. The final run uses12 fresh identifiers, both inherited starting states,
early-budget and matched-update references, and separately labeled example and
complete-rule contexts. All later updates use hard-label CE, including those
starting from the inherited forward-KL adapter; this does not compare CE and KL
as revision objectives. The final active timeout is40 minutes with40 GB peak.
Run model reload audits after other shared-hardware jobs finish.

Only the acquired weights cross stage boundaries; each phase initializes a new
AdamW optimizer. Persistence claims concern saved adapter weights, not resuming
optimizer state or preserving conversational context. Replay's validity filter
uses the investigator-known copper/fast scope; no learned filtering policy is
implemented.

Completed final analysis and reload audit use revision4d9028d. The analyzer
checks3036 responses and2560 updates; the audit matches48 checkpoint probes and
32 source recall records. The longest canonical answer is13 tokens, below the
48-token generation limit. Compact publication tables can be regenerated with:

```
uv run --no-sync python scripts/report_tables.py evidence/NEW-FINAL-analysis
```

Historical source acquisition costs are recorded separately in
sources/checkpoints/acquisition-costs.json: each inherited checkpoint used128
updates; the source's five-arm diagnostic matrix used1280 updates. This study
reuses those learned states and does not reclassify their acquisition as free.
