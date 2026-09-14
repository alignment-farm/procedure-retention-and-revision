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
