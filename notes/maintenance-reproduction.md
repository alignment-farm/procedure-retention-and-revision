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
competent executable-policy reference uses the same full pass and repeat batch
as each learned trajectory. Final repeats all conditions on one familiar and
one fresh entity (32 orders), after each full 192-order pass. Development used
two full passes; every paired repeat was identical. This resource-saving change
was fixed before any fresh evaluation; all 192 primary test cases remain. The original
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
saved adapters to reproduce probes covering corrected familiar/fresh cases,
withheld familiar cases, earlier waivers, acquisition transfer and output forms. Audit generations are excluded
from accuracy denominators. Checkpoint-only persistence does not establish
resistance to learning; the revision sequence provides that separate measurement.

Each candidate deployed trajectory has one initial acquisition, two corrections,
and a full query pass plus a fixed repeat batch at each of three policy versions. Experimental totals
also include the other treatment, development, no-update references, weak
prompted-rule references, calibration and audits. Do not sum shared acquisitions
as if both were needed to deploy one trajectory. Cost files retain tokens, updates,
seconds and bytes separately. Investigator policy construction, correction
authority and identification of obsolete records are supplied, not learned.
Second-revision historical rehearsal includes eight investigator-relabeled records
from revision 1, as well as dropping the eight newly obsolete revision-2 records.
No human-effort, electricity or assistant-orchestration dollar estimate is made.
Zero paid experimental model calls does not mean zero total research cost.

## Frozen fresh execution

Execution revision **0c4c819**. The negative-boundary recipe was selected using
only the fixed development diagnostic. Seeds401/402 and fresh entity names are
prospective, and readiness checks use the original development material.

```sh
uv run --no-sync python scripts/maintenance_experiment.py --phase final --seeds 401 402 --boundary-mode negative --output evidence/NEW-MAINTENANCE-FINAL
uv run --no-sync python scripts/maintenance_analyze.py evidence/NEW-MAINTENANCE-FINAL --output evidence/NEW-MAINTENANCE-FINAL-ANALYSIS
uv run --no-sync python scripts/maintenance_explicit.py evidence/NEW-MAINTENANCE-FINAL --output evidence/NEW-MAINTENANCE-FINAL-EXPLICIT
uv run --no-sync python scripts/maintenance_costs.py evidence/NEW-MAINTENANCE-FINAL --output evidence/NEW-MAINTENANCE-FINAL-COSTS
uv run --no-sync python scripts/maintenance_audit.py evidence/NEW-MAINTENANCE-FINAL --output evidence/NEW-MAINTENANCE-FINAL-AUDIT
```

The formal-policy reference has already completed 672/672 fresh use events;
its source, versioned policies, traces and native-unit costs are preserved in
maintenance-final-explicit-v1. Final neural execution and separate-process audits are complete. All final
source and protocol snapshots were written before model loading.


## Completed whole-phase audit

Final analysis records pre-update compliance under each new policy explicitly:
all newly changed obligations were incorrect before their update. This descriptive
check was added at `c0e7543`; it changes no endpoint, scoring rule or selection.

The initial reload auditor was interrupted during a shared-resource wait because
its output-form-only probe selection could omit revised conditions. Preserve its
partial `maintenance-development-v1-audit` directory and
[repair record](maintenance-audit-repair.json). The replacement selector at
`49af5ee` is regression-tested for corrected familiar, withheld familiar, fresh,
earlier-waiver and acquisition-transfer coverage. The completed replacement uses
`maintenance-development-v1-audit-v2`; the other two audit names are unchanged.
Every completed audit captures its exact sources and Git revision before loading.

Completed checks verify 6,752 work-order response records, 32 routing-calibration
records and 3,712 training-token counts. They reproduce 133 work-order probes
and six routing probes across processes, including failed endpoints. All 320 final
repeat outputs match their corresponding initial outputs, including failures.
The three completed audits take 87.50 seconds; audit generations are separate
from experimental accuracy denominators. The interrupted auditor's unseparated
partial waiting timer is excluded from active-cost totals.

Regenerate the whole-phase audit with corresponding new directories:

```sh
uv run --no-sync python scripts/maintenance_phase_audit.py --runs evidence/maintenance-development-v1 evidence/maintenance-boundary-diagnosis-v1 evidence/maintenance-final-v1 --final-run evidence/maintenance-final-v1 --formal evidence/maintenance-final-explicit-v1 --audits evidence/maintenance-development-v1-audit-v2 evidence/maintenance-boundary-diagnosis-v1-audit evidence/maintenance-final-v1-audit --output evidence/NEW-MAINTENANCE-PHASE-AUDIT
```

This CPU-only command verifies file hashes, sums every acquisition attempt and
experimental cost, and checks that all four candidate use sequences match the
formal-policy reference exactly. Numerical model-run totals exclude the separately
recorded deterministic interpreter runs and verification calls. The updated cost
ledger derives archive-maintenance counts from recorded operations; a temporary
regression reproduced every original development cost total exactly.
