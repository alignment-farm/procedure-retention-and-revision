# State and support interact in a bounded procedural revision task

**Local publication complete, 15 September 2026. Evidence and audits: `c6eb90c`.**

The seed 401 diagnostic rules out both a starting-state-only and a current-support-only
explanation of the previously published maintenance difference. Two states that
both complete 192/192 orders respond differently to identical current support;
changing current support also changes one state's outcome. The interaction is
large in these selected states. Its prespecified direction recurs in both fresh
acquisitions, with interactions of +7 and +34 complete orders versus +70 in
development. In one fresh state, Novel support is harmful relative to Bridged
support, although it helps the other history from the same acquisition. There
is no uniformly preserving combination: no seed 502 cell completes all 192 orders.
All failed readiness checks and imperfect revision-1 states are retained.

## Controlled comparison

All results use the pinned Qwen3-4B-Instruct-2507 base and the accepted eight-layer,
rank-eight LoRA adaptation, with unchanged model hashes. Restore independently
identified revision-1 weights, then cross them with Novel
and Bridged revision-2 evidence. Every cell resets AdamW and receives the same
192-update condition/label order: 64 correction, 64 negative-boundary and 64 history
updates, including ten earlier-waiver rehearsals. Only correction/boundary
identities change with current support. Both histories receive identical current
support within a column. Each starting state is restored independently within a row.

Novel support uses four identities outside the original acquisition set; Bridged
uses two originally acquired identities and two target identities. These names
describe original acquisition overlap, not whether an identity is unseen at
revision 2. The history label names the support used for revision 1. Evaluation
prompts supply order facts and output format, without explicit policy rules.

The diagnostic reproduces all 384 starting outputs, both published 192-order
endpoint outputs and both diagonal adapter files exactly. The original runtime,
model, task and checker are unchanged. Optimizer state does not carry across
revisions. All cells use 17,148 input and 1,536 supervised target tokens: totals
match, but 64 paired update positions differ by one input token in offsetting
directions. This is an identity intervention with measured token differences,
not an assumed equal-token experiment.

| Acquisition | Initial Novel / Bridged complete | NN | NB | BN | BB | Interaction |
|---|---|---:|---:|---:|---:|---:|
| 401, selected diagnostic | 192 / 192 | 192 | 122 | 120 | 120 | +70 |
| 501, fresh | 182 / 192 | 192 | 185 | 120 | 120 | +7 |
| 502, fresh | 183 / 192 | 143 | 133 | 121 | 145 | +34 |

All endpoint counts are out of 192; first letter denotes inherited history,
second current support. Interaction is `(NN − NB) − (BN − BB)` in complete orders.
The prospective fresh expectation was positive within each seed; zero or negative
would challenge it. These finite, correlated orders are not independent state
replications, and no population confidence interval or p-value is claimed.

## What is preserved and what changes

For 401, every cell completes the newest waiver 24/24. Only NN retains the earlier
waiver 24/24; the others score 0/24. Relative to their identical perfect starts,
unchanged orders lost are 0, 70, 72, 72, with no gains. The three failing cells also
wrongly waive certification outside the corrected scopes on 46/48, 48/48 and 48/48
orders. Thus merely learning the newest correction does not preserve the complete
procedure, even on repeatedly supplied boundary examples.

For 501, NN and NB both retain the earlier waiver 24/24 and complete the newest
waiver 24/24. NN repairs ten initially wrong unchanged orders and loses none;
NB repairs ten and loses seven. BN and BB each lose 72 unchanged orders, including
all 24 earlier-waiver obligations. Novel-history states therefore do better despite
a lower initial aggregate score. The seven-order support effect is much smaller
than development's 70; perfect preservation is not synonymous with mere waiver recall.

For 502, all newest-waiver obligations again succeed. Earlier-waiver counts are
23, 13, 0, 24 out of 24 for NN/NB/BN/BB. Unchanged losses/gains are 49/9, 59/9, 71/0, 47/0.
NN incorrectly waives all 48 still-ineligible orders despite retaining 23/24 earlier
waivers; BB retains that waiver perfectly but fails 47 other unchanged orders.
Novel support helps Novel history by 10 orders and harms Bridged history by 24.
The preferred support therefore reverses across these acquired states. This
identifies conditional support value for the tested states; the internal cause
remains unresolved.

The equal 192/192 diagnostic starts support the commission's MR1 expectation
within that selected pair. The fresh findings extend the interaction, not the
equal-accuracy replication: the fresh starting accuracies differ.
Detailed analyses preserve components, complete state validity, directly trained
correction/boundary/history examples, other familiar identities and fresh identities.
Fresh identities are disjoint from training and readiness evaluation; task templates
and policy structure are shared. Repeated passes and audit probes are not new samples.

## Acquisition, freshness and limits

Both new acquisitions fail 256 updates and pass the fixed 512 checkpoint: 501 moves
from 48/64 training and 24/32 development to 64/64 and 32/32; 502 moves from 40/64 and 20/32
to 64/64 and 32/32. Neither 1024 continuation nor seed replacement is used.
The first 501 failure correctly gates eligibility but claims SENT without reserving
or shipping stocked certified orders. 502 also has eligibility errors. The
unchanged recipe at 512 establishes functioning complete acquisition; these failures
are not attributed to forgetting. See the [diagnosis](notes/state-support-acquisition-diagnosis.md).

After revision 1, both fresh Novel histories incorrectly reject some certified
violet/slow orders, while both Bridged histories score 192/192. No history is
filtered out or repaired. Consequently, the fresh pairs do **not** independently
repeat the equal-accuracy starting condition. The equal-score hidden-susceptibility
finding remains diagnostic; fresh comparisons test the conditional value of support
for the actual acquired states. Two initialization/order seeds on one task do not
identify a general protective support set or an internal algorithm.

The investigator supplies correction authority, obsolete-label filtering and
relabeling, including rehearsal of the earlier waiver. This is fixed supervised
LoRA, not autonomous correction or a new editor. The work-order task is one
five-field proposal executed atomically with reset stock, not open-ended planning.
Cached WISE 2405.14768v3 and SEAL 2506.10943v2 methods and pinned author code are
substantial prior context; this crossing reproduces neither algorithm. See
[methods contact](notes/state-support-methods.md) and [source pins](sources/code-revisions.json).
No late training loss is presented as an advance warning.

## Costs, evidence and reproduction

The four experimental runs use **4,096 updates and 4,736 generations**, including
both failed readiness checkpoints and all diagnostic/fresh cells. They consume
366,020 training input tokens and 32,768 loss tokens, plus 389,728 inference prompt
and 37,823 completion tokens. Active experimental time is 2,212.07 seconds
(36.87 minutes), with no recorded resource waits and a maximum MLX allocation of
9,614,900,252 bytes. New adapter checkpoints total 52,497,860 bytes. These are
investigation costs; a deployed trajectory would not execute every crossing.

Four independent audit processes verify all 4,736 response records and 4,096
update-token records, and reproduce 221 checkpoint probes, including failed
readiness and revision endpoints. Audit time is 127.07 seconds with zero waits;
those extra generations are excluded from experimental accuracy denominators.
All saved revision-1 repeats match. Sixteen instrument, schedule and probe tests
pass. Observational resource checks do not establish exclusive hardware or
isolated performance timings. No paid experimental model call, model download,
or service installation was needed; human construction and assistant orchestration
costs are not assigned invented prices. The fresh portion took 28.69 active minutes,
above the rough 20-minute estimate but within the fixed counts and resource ceilings.

The [complete ledger and audit](evidence/state-support-phase-audit/report.json)
retains costs by run, all readiness attempts and each controlled contrast.
The prior seed 401 states are reused,
not newly acquired: two 2,624,893-byte artifacts, originally produced by one shared
256-update acquisition and two 192-update first revisions. Reuse is not free
learning. The competent executable-policy reference remains privileged context
from the accepted maintenance phase; no new economy or repayment claim is made.

- Diagnostic execution: `a31fde0`; [protocol](protocol/state-support-development-v1.md),
  [complete crossing](evidence/state-support-development-v1-analysis-v2/tables.md),
  [selection decision](notes/state-support-development-decision.md).
- Fresh protocol and implementation fixed at `795b649` before acquisition;
  [protocol](protocol/state-support-final-v1.md),
  [seed501 table](evidence/state-support-final-seed501-v1-analysis/tables.md),
  [seed502 table](evidence/state-support-final-seed502-v1-analysis/tables.md).
  Detailed scored subsets: [401](evidence/state-support-development-v1-analysis-v2/analysis.json),
  [501](evidence/state-support-final-seed501-v1-analysis/analysis.json),
  [502](evidence/state-support-final-seed502-v1-analysis/analysis.json).
- [Reproduction commands](notes/state-support-reproduction.md); every model run
  snapshots exact sources, protocol, Git revision, manifest, updates and generations.

The three accepted publications are preserved. This local publication does not
constitute root acceptance or retirement of the broader research question.
