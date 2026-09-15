# Complete-procedure maintenance reproduction

Use the study's locked native MLX environment and pinned model setup in
[reproduction.md](reproduction.md). `uv sync --python 3.14.7 --extra adaptation
--frozen` installs the same runtime. Model Qwen/Qwen3-4B-Instruct-2507 revision
`cdbee75f17c01a7cc42f958dc650907174af0554`; MLX-LM source
`86b48c461feebf87c58788655b7e57b5574b9e6d`. The runner checks cached weight hashes,
uses actual gradients, and never treats the serving endpoint as a training API.

Run model commands sequentially. Resource guards observe sibling Python jobs and
yield; this is passive coordination rather than a reservation or isolated timing.
All output arguments must name NEW directories. The following names are examples.

```sh
uv run --no-sync python -m unittest discover -s tests -v
uv run --no-sync python scripts/maintenance_experiment.py --output evidence/NEW-MAINTENANCE-DEV
uv run --no-sync python scripts/maintenance_analyze.py evidence/NEW-MAINTENANCE-DEV --output evidence/NEW-MAINTENANCE-DEV-ANALYSIS
uv run --no-sync python scripts/maintenance_explicit.py evidence/NEW-MAINTENANCE-DEV --output evidence/NEW-MAINTENANCE-EXPLICIT
uv run --no-sync python scripts/maintenance_boundary_diagnosis.py evidence/NEW-MAINTENANCE-DEV --output evidence/NEW-MAINTENANCE-BOUNDARY
uv run --no-sync python scripts/maintenance_analyze.py evidence/NEW-MAINTENANCE-BOUNDARY --output evidence/NEW-MAINTENANCE-BOUNDARY-ANALYSIS
uv run --no-sync python scripts/maintenance_audit.py evidence/NEW-MAINTENANCE-DEV --output evidence/NEW-MAINTENANCE-DEV-AUDIT
uv run --no-sync python scripts/maintenance_audit.py evidence/NEW-MAINTENANCE-BOUNDARY --output evidence/NEW-MAINTENANCE-BOUNDARY-AUDIT
```

## Provenance and all development attempts

- Original development execution `b9b4f4e`, archived source in its evidence folder.
  Seed311 passed the first 256-update acquisition checkpoint (64/64 recall and
  32/32 development transfer), so no 512/1024 acquisition attempt was made.
  Both identity treatments and both revision endpoints are retained.
- Prompted complete-rule reference is preserved despite poor execution. The
  added executable-policy reference's source was first committed at `a43cde6`;
  its earlier launch reports `b9b4f4e`, and exact executed files are snapshotted.
- Negative-boundary diagnosis fixed and launched from `42c491a`; it restores the
  hash-checked development checkpoint. This is not an independent acquisition.
- Initial CPU analysis used `42c491a`. Strengthened analysis `c4f94e1` adds source
  snapshots, acquisition-order and common-checkpoint checks, and hashes. It
  reproduced every original analysis output byte-for-byte in a new directory.

Final runner removes redundant unchanged-model queries: its no-update output is
collected twice under version 0 and rescored under versions 1 and 2, since the
version is absent from that prompt. Rescoring is not additional inference or a
new sample. The weak prompted-rule reference uses one pass per version; the
competent executable-policy reference uses both recurring passes. The original
development's extra no-update generations remain in its experimental ledger.

## What is checked and what costs mean

The environment scorer independently executes the five-field action proposal and
rejects illegal reservation/shipment, omitted shipment, wrong inventory or false
terminal status. Canonical exact match and components remain separate fields.
Mutation tests change every output field on every condition/version and require
rejection. The formal-policy interpreter is separate from both oracle and scorer;
its trace conserves stock + reserved + shipped units at each step.

Analysis rechecks every saved score, denominator, update schedule, common starting
hash, acquisition sequence and frozen-base invariant. Separate-process audit
retokenizes every prompt/target, decodes every response token record, and reloads
saved adapters to reproduce outcome-diverse probes. Audit generations are excluded
from accuracy denominators. Checkpoint-only persistence does not establish
resistance to learning; the revision sequence provides that separate measurement.

Each candidate deployed trajectory has one initial acquisition, two corrections,
and two fixed query passes at each of three policy versions. Experimental totals
also include the other treatment, development, no-update references, weak
prompted-rule references, calibration and audits. Do not sum shared acquisitions
as if both were needed to deploy one trajectory. Cost files retain tokens, updates,
seconds and bytes separately. Investigator policy construction, correction
authority and identification of obsolete records are supplied, not learned.
Second-revision historical rehearsal includes eight investigator-relabeled records
from revision 1, as well as dropping the eight newly obsolete revision-2 records.
No human-effort, electricity or assistant-orchestration dollar estimate is made.
Zero paid experimental model calls does not mean zero total research cost.
