# Complete work-order maintenance: prospective development v1

15 September 2026. Adaptation of owned runtime at 8c370c2, not a reproduction
of WISE, MQuAKE, SEAL or LOKI. Cached versioned sources and pinned author code
in sources/README.md remain applicable. MQuAKE's consequence evaluation motivates
checking executable downstream state; WISE/SEAL motivate sequential locality.
No new editing algorithm is claimed.

## Workload and boundary

A work order has an entity, channel copper/violet, priority slow/fast,
certification 0/1 and stock 0/1. Initially certification is required everywhere.
An eligible order with stock reserves one unit and ships it; ineligible orders
are held without mutation; eligible zero-stock orders wait. Output has five
space-separated fields: eligibility PASS/FAIL, RESERVE/SKIP, SHIP/SKIP, final
stock, and SENT/HELD/WAIT. The entity identifies the order through its input;
no identifier copying is required. Each query is an independent sandbox reset.
The checker executes proposed reservation/shipping and validates legality and
final state independently of the canonical-string oracle.

Revision 1 waives certification for copper/fast. Revision 2 also waives it for
violet/slow, preserving revision 1. Both affect eligibility, and positive-stock
cases additionally require reservation, shipping and changed inventory/status.
These are finite Boolean procedures, not open-ended plans or real deployments.

## Development and bounded diagnosis

Four acquired entities cross all 16 conditions (64 examples). Train a newly
initialized rank-8 LoRA using existing runtime/CE/AdamW 0.0005 for 256 updates.
Evaluate all 64 recall and 32 new-entity cases. Readiness requires >=60/64 complete
recall and >=28/32 new complete cases; full/component denominators always retained.
If unmet, continue the SAME acquisition to 512 then 1024 updates; preserve every
checkpoint. If still unmet, inspect error structure before one changed-recipe
attempt. No retention interpretation from failed acquisition.

Two paired arms start from the earliest functioning checkpoint. In each revision,
64 blocks each contain one correction, one contrasting boundary, one valid
historical replay update. Novel-only correction identities are four new entities;
bridged identities are two of the four acquired entities and two of those same
new entities. All conditions/labels/counts/optimizer resets match. The same arm's
correction entities also receive unchanged boundary cases, ruling out a pure
entity-wide waiver. Both arms replay the identical investigator-relabelled valid
history, EXCLUDING all newly changed cases (otherwise familiar correction would
leak into the novel-only arm). Previously revised cases remain valid rehearsal.
Identity composition is the intervention; information is not semantically equal.
The remaining two acquired entities test effects on formerly learned but not
directly corrected instances. All 16 conditions are evaluated on acquired,
correction and two new entities at each revision. No-update and unadapted-model
complete-rule context references use identical cases. Complete-rule context has
privileged investigator-authored rule information, explicitly costed.

Two recurring query passes per revision use identical cases; pass 2 verifies
repeatability without query-driven updates. Acquisition, revision and query costs
are separate. No claim of autonomous obsolescence detection: investigator scans
64 historical records per revision against authoritative old/new labels and
filters the changed records. Log scans, exclusions, examples, tokens, updates,
checkpoint bytes, wall time, resource waits and all responses. Experimental
calibration/search/audits are not deployed-method costs. Zero paid calls.

Final selection and fresh material will be fixed after development. Two independent
adapter seeds planned, same pretrained base, no task-population inference.

## Resources and evidence

Native MLX on mac.lan, cached pinned Qwen3-4B weights verified by owned runtime.
No model installation. Expected <12 GB, hard 40 GB, active run ceiling one hour,
shared-resource wait ceiling two hours. Passive coordination follows existing
notes/resource-use.md: inspect all visible sibling Python experiments before
loading and between operations, yield during contention, record observations.
No cross-investigator messaging tool is exposed. Do not claim isolated timing.
Every run uses a new evidence directory, snapshots source/protocol, records Git
revision, saves adapters and all raw generations, and hashes completed evidence.
