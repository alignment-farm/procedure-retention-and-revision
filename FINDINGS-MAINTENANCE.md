# Complete procedures can survive supported revision, but preservation is fragile

**Third-phase findings, 15 September 2026. Experiments and audits complete;
local publication available for root assessment.**

One of four fixed treatment trajectories preserves all 192 complete work orders
through two successive scoped corrections. The others finish at 120/192,
132/192 and 130/192, despite correctly applying the newest correction. Adding
familiar identities to correction evidence does not make preservation reliable.
A maintained executable policy completes the matched 672-use sequence without
model updates, using stronger investigator-supplied information.

[Fixed protocol](protocol/maintenance-final-v1.md) ·
[All final tables](evidence/maintenance-final-v1-analysis/tables.md) ·
[Development and selection](notes/maintenance-development-decision.md) ·
[Reproduction](notes/maintenance-reproduction.md)

## What was maintained

A work order has an entity, channel, priority, certification and binary stock.
Eligibility controls reservation; reservation permits shipment; shipment changes
inventory and terminal status. The checker executes the proposed five-field
procedure and independently rejects illegal actions or incorrect resulting state.
Initially certification is required everywhere. Revision 1 waives it for
copper/fast orders; revision 2 additionally waives it for violet/slow orders.
For example, an uncertified copper/fast order with stock 1 must change from held
with stock 1 to reserved, shipped and stock 0. The first waiver must survive the
second update.

Each acquired state starts two paired treatments. **Novel** supplies correction
and contrasting boundary examples on four new entities. **Bridged** replaces two
of those entities with two familiar acquired entities. Both receive the same
condition/label sequence, 192 updates per revision and identical historical
rehearsal. The intervention changes identity overlap in both correction and
boundary examples. Two other acquired entities receive no current-revision
correction labels. Four fresh entities appear only in evaluation.

Correction authority, negative-boundary selection and archive validity are
supplied by the investigator. Each revision scans 64 historical records and
excludes eight obsolete labels. Revision 2 also supplies eight relabeled records
from the first revision for rehearsal. This support is identical between arms;
it is not learned obsolescence detection. No rules or examples enter the trained
model's inference prompts.

## Acquisition, selection and development

There are three acquisition trajectories, with every assessed checkpoint retained:

| State | Updates | Familiar complete | Development complete | Decision |
|---|---:|---:|---:|---|
| Development seed311 | 256 | 64/64 | 32/32 | First passing state |
| Final seed401 | 256 | 64/64 | 32/32 | First passing state |
| Final seed402 | 256 | 41/64 | 18/32 | Failed readiness; continue |
| Final seed402 | 512 | 64/64 | 32/32 | First passing state |

The predeclared 256/512/1024 ladder selected using development material only.
No 1024-update attempt was needed. Both selected final states score 192/192 on
the full original-policy evaluation. Their acquisition budgets differ, so
cross-state differences cannot be attributed to initialization alone. Comparisons
within each state share identical saved weights and correction budgets.

Original development corrected all new obligations but lost unchanged behavior:
first-revision complete scores were 132/160 and 140/160; both second endpoints
were 120/160. One bounded diagnostic replaced broadly cycled boundary examples
with unchanged ineligible examples, keeping correction, history and update counts
fixed. Both first-revision endpoints improved to 160/160. The fixed selection
rule therefore chose negative boundaries for final evaluation. This diagnoses
boundary-content/frequency allocation jointly. The final tests the selected
recipe on fresh entities and acquired states; it does not independently replicate
the broad-versus-negative causal contrast. All original failures remain in the
[development evidence](evidence/maintenance-development-v1-verified-analysis/tables.md).

## Fresh results: new corrections and preservation diverge

Primary denominators use the full 192-order pass once. Each pass is followed by
a fixed 32-order repeat batch; repeats are use events, not independent samples.

| Acquired state | Support identities | After revision 1 | After revision 2 | First waiver correct after revision 2 | Unchanged successes lost / gained at revision 2 |
|---|---|---:|---:|---:|---:|
| seed401 / A256 | Novel | 192/192 | 192/192 | 24/24 | 0 / 0 |
| seed401 / A256 | Bridged | 192/192 | 120/192 | 0/24 | 72 / 0 |
| seed402 / A512 | Novel | 179/192 | 132/192 | 12/24 | 60 / 13 |
| seed402 / A512 | Bridged | 179/192 | 130/192 | 0/24 | 61 / 12 |

Each second-boundary unchanged set has 168 orders. The paired counts use each
arm's actual preceding output. Thus repaired earlier errors appear as gains,
and an already wrong order is not counted as a newly lost success. Previously
correct familiar unchanged orders lost at that boundary are respectively
0/56, 24/56, 20/56 and 19/56, with gains 0, 0, 4 and 4.

The newest revision is correct on all 24 obligations at seven of eight endpoints.
At seed402/bridged's first endpoint, the formerly acquired but withheld `robnak`
copper/fast, uncertified, stock-1 order remains held instead of shipping: 23/24
obligations are correct. Directly relabeled familiar cases are all correct, but
this additional learned instance is stale. Fresh-entity revision obligations
score 8/8 at every endpoint. Before each update, the corresponding new-policy
obligations score 0/24, so the intervening material was meaningfully learned.

Latest-correction success does not imply older-correction retention. Both bridged
final endpoints lose the first waiver entirely, even though its eight acquired
records were relabeled and rehearsed. The one stale first-stage obligation is
reported separately from this later forgetting.

All 1,536 primary trained-endpoint outputs have valid syntax. Whenever eligibility
is correct, the whole procedure is correct (1,316/1,316). Errors include withholding
eligible certified orders, granting eligibility outside the waiver scopes and
forgetting a prior waiver. These errors propagate to shipment and state. For
example, seed401/bridged finally ships every uncertified copper/slow stock-1
order, consuming inventory that should remain untouched. Identifier copying is
excluded from this workload by design.

All 320 final repeat outputs exactly match their corresponding first-pass token
sequences, including failures. Repetition within a policy version involves no
query-driven learning. The no-update carried reference remains correct on the
original policy and scores 168/192 and 144/192 under the revisions. Its identical
prompts are rescored without manufacturing additional inference observations.

## Complete quality and maintenance cost

A candidate sequence comprises a full pass and repeat batch at each of three
policy versions: 672 uses. Initial observations and acquisition are shared within
a pair, then attributed to each candidate for deployment accounting. Experimental
totals count that shared work once. See the [native-unit ledger](evidence/maintenance-final-v1-costs/costs.json).

| Candidate | Complete uses | Initial + revision updates | Measured training seconds | Recurring inference seconds |
|---|---:|---:|---:|---:|
| seed401 / Novel | 672/672 | 256 + 384 | 118.62 | 186.56 |
| seed401 / Bridged | 588/672 | 256 + 384 | 118.06 | 186.59 |
| seed402 / Novel | 587/672 | 512 + 384 | 166.28 | 186.60 |
| seed402 / Bridged | 584/672 | 512 + 384 | 166.98 | 186.67 |
| Maintained formal policy | 672/672 | 0 | 0 | 0.001 measured execution sum |

Acquisition verification additionally uses 96 or 192 generations (26.69 or
52.32 seconds), including the failed seed402 checkpoint. Initial training uses
22,912 or 45,824 input tokens. Each arm's two revisions use 384 updates, including
128 correction, 128 boundary and 128 rehearsal updates, with 3,072 loss tokens;
input-token totals are 34,296 for Novel and 34,298 for Bridged. Each candidate's
recurring use has 55,392 prompt tokens and 5,375–5,378 completion tokens.

Each current adapter occupies 2,624,893 bytes, alongside 8,044,982,000 bytes of
base weights. The ledger explicitly serializes all unique training case/target
pairs: 20,901 bytes for Novel and 17,917 for Bridged, including obsolete labels.
These are sufficient archive representations, not minimal storage bounds.

The competent explicit-memory reference uses a maintained JSON eligibility policy
and a fixed transition interpreter. Its current policy is 215 bytes and its
interpreter function 815 source bytes, plus the Python runtime. Each revision
adds one investigator-authored clause. The entire formal evaluation harness takes
0.023 seconds; short execution timers do not support a general latency ratio.
This reference receives executable rules and manual construction, stronger
information than correction examples. It is distinct from the unadapted prompted
rule reference, which scores 99/192, 96/192 and 84/192 and remains in the record.

There is no demonstrated amortization advantage here: one learned trajectory
matches explicit-policy quality with additional training and model inference;
three produce failures at similar inference cost. Rule construction, evidence
selection, correction authority, assistant orchestration and electricity are
unpriced. Zero paid experimental model calls is not zero research cost. Timing
is observational on shared hardware, with resource waits reported separately.

## Evidence, prior work and limits

Execution is pinned at **0c4c819**; final analysis at **c0e7543**. Sources, protocols,
model hashes, update records, raw generations and all checkpoints are retained.
The three experimental model runs contain 3,712 updates, 6,752 work-order
generations and 32 routing-calibration generations. Their combined active time
is 2,822.31 seconds (47.0 minutes), plus 1,201.05 seconds waiting for hardware.
The formal interpreter separately executes 960 development and 672 final orders.

The [completed phase audit](evidence/maintenance-phase-audit/report.json) verifies
all 6,784 model response-token records and all 3,712 update-token counts. Separate
processes reproduce 133 work-order and six routing probes exactly, including
corrected familiar/fresh, withheld familiar, earlier-waiver and acquisition-transfer
cases. The three completed audits take 87.50 seconds with no resource waits;
their probes are excluded from experimental accuracy denominators. Exact input
sequences match between each candidate and the formal-policy reference.

The first auditor was interrupted before completion after a coverage gap was
found: output-form diversity alone could miss the changed scope. Its source and
the [repair record](notes/maintenance-audit-repair.json) are preserved. The incomplete
waiting timer is excluded from numerical active-time totals. No experimental
endpoint or score changed. Audit implementation is pinned at **49af5ee**;
completed evidence is linked in the phase audit above. The 14 instrument tests pass.

The initial routing calibration reproduced 16/16 complete calls, and the
work-order development acquisition reproduced 160/160 after reload into the
separate diagnostic process. Storage-boundary persistence and retention under
subsequent learning are separate measurements.

This is a plain supervised LoRA/rehearsal adaptation, with substantial overlap
with WISE's locality/retention question, MQuAKE's consequence evaluation, SEAL's
sequential interference and LOKI's preservation objective. Cached versions
2405.14768v3, 2305.14795v3, 2506.10943v2 and 2606.19679v1 and exact inspected author
code revisions are in the [source record](sources/README.md) and
[maintenance methods note](notes/maintenance-methods.md). None of those author
algorithms is reproduced, and no new editing algorithm is claimed.

Scope is one model family, two selected final acquired states, 16 Boolean
conditions, binary stock and two additive waivers. Fresh entities vary identity
within this procedure; every condition is represented in training or support.
The plan is emitted at once and checked in an independently reset sandbox.
The result establishes a functioning path for complete behavioral preservation
and concrete failures of reliability under the same fixed recipe. Parameter-level
independence, longer workflows and economical autonomous maintenance remain open.
Local completion, root acceptance and retirement of the broader question are
separate decisions.
