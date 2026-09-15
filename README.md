# Procedure retention and revision

**Status: [Scope evidence and rehearsal follow-up completed locally](FINDINGS-SCOPE.md); first comparison accepted.**

Seven crossed boundary examples recover all 96 fresh routes in two of four
starting states. With the same boundary-case access and update count, adding
history reduces losses of previously correct calls in three starts and increases
them in one. None of the 16 primary endpoints preserves every previously correct
unchanged call; one history treatment also leaves familiar corrected-scope
answers stale.
The broader research question remains open.

[Follow-up findings](FINDINGS-SCOPE.md) · [Fixed methods](protocol/scope-anchored-final-v1.md) · [Evidence](evidence/scope-final-v1-analysis/compact-tables.md) · [Reproduction](notes/scope-reproduction.md)

## Accepted first comparison

One replay regime finishes later learning and a scoped correction with 96/96
fresh routing decisions correct, but only 19/96 complete calls. The same recipe
from a different acquired state achieves 85/96 routes and 9/96 calls. Update budget,
replay information and acquired state matter; correct routing does not guarantee
preservation of argument behavior. The broader research question remains open.

[Protocol](protocol/final-v1.md) · [Evidence and audits](evidence/final-v1-analysis/compact-tables.md) · [Reproduction](notes/reproduction.md) · [Source provenance](sources/README.md)

The [follow-up brief](FOLLOWUP.md) commissioned the now-completed comparison of
scope evidence and rehearsal. The accepted [findings](FINDINGS.md), frozen
protocol and evidence remain the record of the first comparison. The original
study brief follows for context.

## Original study brief

**Can an acquired procedural relation survive later learning and accept a scoped
revision that transfers to unfamiliar inputs, while preserving unaffected
behavior?** This investigation takes up Construct-2's
[S2 question](../../construct-2/studies/README.md#s2-can-a-learned-procedure-survive-later-learning-and-accept-a-scoped-correction).
It asks what happens to something learned when subsequent experience arrives.

## Begin the investigation

Read the starting publication and closest methods below, then develop and run
the first bounded empirical comparison. Establish the behavior being retained,
introduce intervening learning or a scoped correction, and measure what changes.
The investigator owns the workload, methods, resource sizing and implementation;
this brief is not a frozen protocol. Routine development and experiments within
these resources are authorized without another root approval step. This project
can proceed independently of the concurrent experience-selection and changed-goal
studies. A literature-only handoff is not the intended first outcome when an
informative local comparison is feasible.

## Starting evidence

[Procedure-transfer's diagnosis](../procedure-transfer/DIAGNOSIS.md), publication
commit `dcdc0d6f54dde235549f8abfba407598b6635667`, with evidence at
`c183674bcecf9346d84e233aa5c084b1a9acb3ac`, supplies functioning acquisition
regimes. Hard-label imitation and forward KL each reach 16/16 training-call
recall at selected diagnostic checkpoints. Both route 48/48 fresh development
inputs correctly, while complete calls score 28/48 and 17/48 respectively.
These are one-seed diagnostic findings, not an independently confirmed transfer
advantage. They establish a concrete starting behavior without establishing
reliable unfamiliar-string production or later retention.

The root's [procedural-learning note](../../construct-2/notes/PROCEDURAL_LEARNING.md)
conjectures that reusable routing can be selectively revised (R4). Initial
transfer does not establish independently editable parameters. The present
study tests that stronger claim rather than assuming it.

Reuse the pinned [implementation](../procedure-transfer/scripts/diagnosis_v2.py),
[diagnostic protocol](../procedure-transfer/protocol/diagnosis-v2.md), saved
checkpoints and [reproduction instructions](../procedure-transfer/notes/reproduction.md)
where useful, recording provenance. Develop study-owned data and keep any reused
calibration cases distinct from fresh evaluation. A different task is appropriate
if it more clearly distinguishes procedural revision from a small lookup edit.

## Experimental direction

The first comparison should separate explanations: a reusable relation survives
and changes within its intended scope; updates merely bias a familiar answer;
or learning and revision interfere with unaffected behavior. These are starting
contrasts for local design, not a requirement to run every arm or method.

- **Persistence:** does the acquired behavior survive removal of teaching context
  and the stated storage/session boundary? Saving and reloading an adapter alone
  says nothing about resistance to subsequent learning.
- **Retention:** what changes after intervening learning, relative to the acquired
  state without those updates? Establish that the intervening material was also
  learned; ineffective updates do not test a meaningful retention tradeoff.
- **Scoped correction and transfer:** does a valid change apply to new inputs in
  its scope, leave other relations intact, and affect the appropriate downstream
  actions? Measure stale answers and overgeneralized revisions separately.
- **Unaffected behavior and cost:** retain component and complete-task measures,
  including identifier production where applicable. Record acquisition, rehearsal,
  revision, storage and inference costs; a component gain does not establish
  complete-task repayment.

Compare appropriate carried-state and no-intervening-update references, with an
explicit-evidence alternative when drawing conclusions about memory placement.
Disclose each arm's access to original experience, revisions, validation and
replay. Exact examples, learned relations and supplied complete rules carry
different information. A simple two-entry routing correction can calibrate the
instrument, but is not automatically a new procedural contribution. Seek an
informative comparison of later learning, correction consequences and unaffected
behavior, with novelty claims scaled to the actual overlap.

Successful acquisition of the relation being studied is sufficient to begin;
perfect complete-call behavior is not required. If acquisition fails, pursue
bounded diagnosis rather than interpret the result as forgetting. Preserve all
attempts and acquisition denominators. Development can revise a weak recipe;
test a developed claim using fresh material and a selection rule fixed before
that evaluation. A negative result can be informative without ending work on an
unexplained learning failure.

## Closest prior work and reading leads

These are versioned starting sources from the root's
[paper map](../../construct-2/studies/README.md#3-paper-map-what-we-can-build-on), not methods reproduced
by this prepared project. Inspect the relevant primary methods and code before
claiming a contribution beyond them.

- [WISE, 2405.14768v3](https://arxiv.org/html/2405.14768v3), §§2.3, 3.1–3.3:
  sequential editing, retention, generalization and locality are substantial
  existing overlap.
- [MQuAKE, 2305.14795v3](https://arxiv.org/html/2305.14795v3), §§3.3–4:
  distinguish an edited component from its consequences; inspect the revised
  evaluation data and external-memory reference.
- [SEAL, 2506.10943v2](https://arxiv.org/html/2506.10943v2), §§3–5:
  acquisition and interference across sequential edits.
- [LOKI, 2606.19679v1](https://arxiv.org/abs/2606.19679v1): an additional reading
  lead; the root's earlier review covered its abstract only.

## Resources and publication

[AGENTS.md](AGENTS.md#model-resources) describes the available model routes and
shared-hardware coordination. The diagnostic study demonstrates native MLX
gradient access on the Mac Studio; reproduce or adapt that route locally rather
than infer training access from the serving endpoint. No numerical run budget is
assigned here. Size a focused comparison after checking feasibility; a large
training campaign is outside this initial expectation.

Publish a concise `FINDINGS.md` and link it here, with local methods, supporting
evidence, reproduction instructions and identifiable Git revisions. A separate
manuscript is optional. The root will assess the implications for where accumulated
experience should live; experimental decisions and repairs remain in this project.
