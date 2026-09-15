# Learning history and current support in procedural revision

**Fourth phase commissioned, 15 September 2026.** Develop and execute a bounded
investigation under [AGENTS.md](AGENTS.md). The investigator owns the protocol,
implementation, numerical resource budget and routine execution. Preparing this
brief has not launched experiments.

**Why do two states that complete the same tasks respond differently to later
revision: their learning history, the current supporting examples, or an
interaction between the two?**

## Starting evidence

The accepted [complete-maintenance publication](FINDINGS-MAINTENANCE.md), at
`28aa881833ac2f9cf478b0d2f8a0f233ecc90023`, follows two successive policy revisions.
For seed 401, Novel and Bridged both complete 192/192 cases after revision 1.
They enter revision 2 with different weights and different support identities.
Novel then completes 192/192; Bridged completes 120/192 and loses the earlier
waiver entirely. The published comparison identifies the effect of the whole
support strategy across revisions, not the effect of current support alone.

The two relevant starting artifacts are
[seed401-novel-v1.safetensors](evidence/maintenance-final-v1/seed401-novel-v1.safetensors)
and [seed401-bridged-v1.safetensors](evidence/maintenance-final-v1/seed401-bridged-v1.safetensors).
Their provenance, manifests, generations and update histories remain in
[maintenance-final-v1](evidence/maintenance-final-v1/), with the
[frozen protocol](protocol/maintenance-final-v1.md) and
[reproduction guide](notes/maintenance-reproduction.md).

Optimizers reset at each revision. Both second-revision arms receive 192 updates:
64 correction, 64 boundary and 64 historical updates. Ten historical updates
rehearse the first waiver. The investigator supplies validity filtering and
relabels earlier-waiver examples; this is not learned correction authority.
The current support changes familiar identity overlap in both correction and
boundary examples, while the historical sequence is shared.

Root's post hoc reading of [events.jsonl](evidence/maintenance-final-v1/events.jsonl)
found different late pre-step losses on the same old-waiver examples in the two
evolving trajectories. This is a descriptive lead, not an established warning
signal or proof of the cause. Intermediate complete generations and frozen-state
logit margins were not saved; obtaining them requires additional model work.

## First identifying comparison

Cross the two revision-1 states with the two revision-2 support sets, or develop
an equally informative controlled comparison:

| Revision-1 weights | Novel current support | Bridged current support |
|---|---|---|
| Novel history | Published preserving trajectory | Missing crossing |
| Bridged history | Missing crossing | Published failing trajectory |

Keep the inherited state and current support independently identifiable in the
implementation and results. For a current-support contrast, restore identical
starting weights and match the optimizer initialization, condition/label order,
history, update count and relevant resources. For an inherited-state contrast,
apply identical current support. Preserve measured token differences. Verify
checkpoint provenance and starting behavior, and establish comparability with
the published diagonal trajectories using proportionate reproduction checks.
Preserve and diagnose any discrepancy before attributing it to the crossing.

If outcomes follow the inherited state under common support, the prior learning
path matters beyond assessed accuracy. If they follow current support across
states, the immediate intervention is the stronger explanation. An interaction
would make the value of the same support conditional on the acquired state.
These conclusions concern the tested states; neither outcome identifies an
internal algorithm or a generally protective set of examples.

Score complete procedures and their resulting states. Separate the newest
revision, retention of the earlier waiver, and paired losses/gains on unchanged
orders. Preserve directly supported, additional familiar and fresh-identity
outcomes. Equal initial aggregate accuracy is a property of the measured suite,
not proof of equivalent margins or representations. Other available starts may
be informative, but their differing readiness and acquisition budgets must remain
visible rather than being treated as equivalent replications.

## Diagnosis and a fresh test of the explanation

The selected seed-401 states and their diagonal outcomes are already known.
The first crossing is diagnostic development. Use it to choose a bounded test
that could challenge the resulting explanation on fresh material. For a claim
about acquired-state susceptibility, new task tickets alone do not provide new
acquired states. Match the freshness boundary to the claim and retain any
acquisition failures with purposeful diagnosis.

The investigator may choose a focused follow-on contrast if the crossing leaves
an important ambiguity. For example, changing only update order with the example
multiset fixed could test temporal sensitivity; separating familiar identities
in correction from those in boundary evidence could identify their contribution.
These are leads, not a required experiment matrix. Close on an explanatory
result, a demonstrated limitation or a concrete resource constraint. A positive
preservation effect and indefinite tuning are unnecessary.

Root's prospective **MR1** expectation is that some equally successful states
will differ under identical current support. A result primarily explained by
current support would weaken that account. Any observation proposed as an advance
warning must be available before the decision it supports and face separate
evaluation; late training losses cannot retrospectively predict earlier damage.
This commission asks for an explanation of maintenance reliability. A full
adaptive controller is not required.

## Resources, prior work and publication

Use the established native MLX route and existing artifacts as starting resources,
verifying current availability and coordinating heavyweight shared-device work
under [AGENTS.md](AGENTS.md). No other study's next result is a prerequisite.
The investigator chooses the budget for the identifying comparison and fresh
assessment, recording meaningful expansions and unsuccessful development.

The prior [maintenance methods](notes/maintenance-methods.md) and
[source record](sources/README.md) supply editing/rehearsal context. Relevant
additional method leads are GEM [1706.08840v6](https://arxiv.org/html/1706.08840v6),
A-GEM [1812.00420v2](https://arxiv.org/html/1812.00420v2), and gradient-based sample
selection [1903.08671v5](https://arxiv.org/html/1903.08671v5). Root inspected their
methods, not their implementations. They are prior art for interference control,
not algorithms this commission requires implementing or novel contributions to
claim. Inspect the closest method/code before adopting a new intervention.

Charge acquisition or artifact reuse, diagnostic inference, updates and any
monitoring in their actual units. Separate investigation costs from costs a
deployed method would incur. The prior competent formal-policy reference has
privileged executable information. It remains relevant context; a mechanistic
crossing need not repeat the whole cost campaign. A new claim of useful economy
would require comparable complete quality and competent explicit evidence.

Preserve all three accepted publications and frozen protocols. Publish a
separate findings note with identifiable Git revision, complete comparisons,
development/fresh boundaries, costs and reproduction evidence. A concise local
publication is sufficient; no separate manuscript is required.

The root [reliability note](../../construct-2/notes/MAINTENANCE_RELIABILITY.md)
connects this question to the program. This brief contains the context needed to
proceed even when that root checkout is absent or older. Routine development
and execution within the stated scope need no further root approval.
