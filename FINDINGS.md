# Routing retention and scoped revision under later learning

14 September 2026. First bounded comparison complete; the broader research
question remains open. Evidence and audits: **`ba27ecd`**; execution **`9747992`**;
analysis **`4d9028d`**.

**One acquired state finishes later learning and correction with all 96 fresh
routing decisions correct, but only 19 complete calls.** With replay, the
forward-KL-acquired adapter applies the revised route to 12/12 in-scope inputs
and outputs the intended routes on 84/84 others. Only 3/12 revised calls have
the correct arguments. Among 36 unchanged old inputs, five previously correct
calls become wrong across the sequence, while one previously wrong call improves.
The same replay recipe from the CE-acquired state achieves 85/96 routes and 9/96
complete calls. This supports a bounded result about maintaining and revising
routing, without establishing independently editable parameters or retention of
the complete procedure.

## Comparison and evidence access

The old procedure maps copper→kestrel and violet→marten. Later learning adds
amber→marten and teal→kestrel. Every call uppercases an identifier and appends
`-Q` iff priority is fast. The correction changes **only copper/fast** to marten;
other routes and argument rules remain unchanged. Twelve fresh identifiers,
three each of lengths 4, 6, 8, 10, cross the eight channel/priority combinations:
48 old-channel queries, 48 new-channel queries. The corrected scope has 12;
unchanged old behavior has 36. These are new strings, not unseen condition
combinations or paraphrases. [Fixed protocol](protocol/final-v1.md).

CE and FK denote the two published acquired checkpoints from procedure-transfer
(`c183674`, publication `dcdc0d6`). Both used original seed 41 and were the earliest
checkpoints reaching at least 15/16 recall in its five-arm acquisition matrix.
Reverse KL at two rates and low-rate forward KL did not meet that criterion;
the [source record](sources/README.md) preserves this selection history. These
are two starting states, **not independent acquisition replications or seeds**.
Both reproduce 16/16 old training calls here. All subsequent updates use
hard-label CE; FK is acquisition provenance, not a revision objective.

The model is pinned Qwen3-4B-Instruct-2507 bf16 with rank 8 q/v LoRA in the last
eight blocks, scale 2, no dropout, AdamW 0.0005 and zero weight decay. Each stage
resets the optimizer. Within each acquired state and stage, arms share starting
weights and target order. New learning uses 16 checked examples; correction uses
four. Replay adds 128 old-example
updates during new learning, or 128 updates from 28 unaffected old/new examples
during correction. Every correction arm starts from the state produced by new
learning with replay. Count controls replace replay with immediate repetition of the new
target, matching optimizer steps, not information or token counts.

Replay's validity mask uses the **investigator-known correction scope** to
exclude four obsolete examples. It supplies boundary evidence as well as
rehearsal; this is not learned discovery of obsolete history. The revised
example-context reference receives the same 28 unaffected examples plus four
actual corrections, each once. Complete-rule references additionally receive
oracle descriptions of the entire relation. No teaching context or verbal rule
is supplied at student generation. [Access and interpretation limits](notes/interpretation-boundaries.md).

Development used separate identifiers and retained every scheduled checkpoint.
Its late interference motivated fixed 32-update references; difficulty with
example induction motivated separate complete-rule references. The final example
context removes obsolete records instead of adding extra relabeled examples.
These changes preceded all fresh evaluation. One hardware-overlap interruption
is preserved, followed by a complete development run. [Decision record](notes/development-decision.md).

## Retention depends on budget and acquired state

**All six new-learning arms finish with 16/16 complete training calls.** Their
new material was learned. Every number below is a count out of 48 fresh queries;
“call” requires the entire canonical answer. Routing also requires canonical call
syntax, so malformed arguments can lower its score.

| Acquired state | Later learning | Old route /48 | New route /48 | Old call /48 | New call /48 |
|---|---|---:|---:|---:|---:|
| CE | None | 48 | 12 | 19 | 8 |
| CE | 32 new | 48 | 48 | 20 | 21 |
| CE | 128 new | 24 | 48 | 6 | 12 |
| CE | 256 new | 25 | 48 | 9 | 20 |
| CE | 128 new + 128 replay | 44 | 40 | 7 | 8 |
| FK | None | 48 | 24 | 15 | 8 |
| FK | 32 new | 48 | 48 | 2 | 4 |
| FK | 128 new | 47 | 48 | 6 | 13 |
| FK | 256 new | 41 | 48 | 10 | 12 |
| FK | 128 new + 128 replay | 47 | 47 | 8 | 7 |

At 32 updates, both acquired states retain every old route and route every new
input correctly. Continuing to 128 loses 24 old routes from CE but only one from
FK. Repeating new examples for 256 updates does not reproduce replay's old-route
retention. Replay preserves all old training calls, yet has no consistent
fresh-input advantage over the shorter budget. FK's two 47/48 replay scores each
contain one malformed argument with the correct `kestrel` prefix, rather than
an incorrect tool selection. Complete-call behavior can decline sharply even
when routing remains correct: FK's old calls fall from 15/48 to 2/48 at 32 updates.
[All components and counts](evidence/final-v1-analysis/tables.md).

## Correction transfer and locality are different outcomes

**All six correction arms finish with 4/4 complete correction training calls.**
The table uses the revised target. “Overbroad” counts copper/slow calls incorrectly
sent to marten; errors on the new channels are additional unaffected-behavior
failures. Malformed calls are failures, not automatically stale answers.

| Acquired state | Correction updates | Scope route /12 | Other old route /36 | New-channel route /48 | Full calls /96 | Stale /12 | Overbroad /12 |
|---|---|---:|---:|---:|---:|---:|---:|
| CE | 32 corrections | 12 | 23 | 24 | 9 | 0 | 12 |
| CE | 128 corrections | 12 | 24 | 24 | 5 | 0 | 12 |
| CE | 256 corrections | 12 | 24 | 24 | 6 | 0 | 12 |
| CE | 128 corrections + 128 replay | 12 | 30 | 43 | 9 | 0 | 5 |
| FK | 32 corrections | 11 | 24 | 22 | 6 | 0 | 12 |
| FK | 128 corrections | 12 | 24 | 24 | 5 | 0 | 12 |
| FK | 256 corrections | 10 | 20 | 18 | 8 | 0 | 10 |
| FK | 128 corrections + 128 replay | 12 | 36 | 48 | 19 | 0 | 0 |

Correction-only training commonly produces the revised tool across conditions,
including copper/slow and teal. At 128 updates, both starts get 12/12 scoped routes
right while sending all 12 copper/slow inputs to the wrong tool and routing
only 24/48 new-channel inputs correctly. Neither shorter correction nor extra repetitions establishes
locality. Positive corrected examples alone do not uniquely identify the scope.

Replay controls this spread, completely on the tested routing cases only for
FK. That endpoint also completes all 16 old and 16 new training calls under the
current rule. Its scoped routing improves from 0/12 under the same new goal before correction
to 12/12 afterward. CE starts at 2/12 under that goal and reaches 12/12, but still
overgeneralizes on five copper/slow inputs. Thus an aggregate in-scope success
is insufficient evidence of a scoped procedure. [No-correction references](evidence/final-v1-analysis/revision-reference.json).

The successful FK routing result still loses five originally correct calls among
36 unchanged old queries; complete correctness changes 11→7 because one other
call improves. CE loses 12 such calls, changing 15→3. These compare **identical
queries with unchanged target answers**, not stale answers that should have been
revised. [Paired errors](evidence/final-v1-analysis/pipeline-retention.json).

## Explicit information helps in different ways

Original references are scored under the old rule; revised references under the
correction. Each uses the unadapted base model.

| Context reference | Old/current route /48 | New-channel route /48 | Full calls /96 |
|---|---:|---:|---:|
| No evidence | 24 | 24 | 0 |
| Original examples | 42 | 27 | 38 |
| Revised examples | 36 | 39 | 50 |
| Original complete rule | 48 | 48 | 86 |
| Revised complete rule | 48 | 48 | 81 |

The revised example reference gives stale routes on 12/12 fresh scoped queries
and misses all four correction training cases despite their presence in context.
Its 50 correct calls therefore do not establish successful revision. The revised
complete rule gives 12/12 exact scoped calls and 81/96 complete calls overall.
Clear rule access supports substantially more complete execution in this setup,
but neither reference is a generally optimized prompting method. Full rules
supply stronger information than examples; their construction is not automated
or cost-free here. These results do not establish a universal memory-placement
ranking.

## Costs, verification and scope

The final run uses 2,560 updates, 3,036 generations and 16 saved checkpoints:
463.3 seconds in recorded updates, 1,135.6 in generation, 1,754.6 elapsed,
9.62 GB peak MLX allocation on the 64 GiB M1 Ultra. It scores 203,480 training
input tokens and 25,654 answer tokens; inference uses 434,030 prompt tokens and
32,539 generated tokens. One adapter contains 655,360 parameters and occupies
2,624,893 bytes. [Per-arm costs](evidence/final-v1-analysis/arm-costs.json).

Development adds 768 updates and 816 generations, 535.2 active seconds plus 810.5
seconds waiting for other investigators' hardware use. The interrupted attempt
has 30 logged updates and 136 generations; an in-flight update may be unlogged.
The two inherited acquisitions each used 128 updates; their source's diagnostic
search used 1,280. [Historical acquisition costs](sources/checkpoints/acquisition-costs.json).
No paid experimental model calls or new weight downloads were needed. These are
local timers and allocation counts, not energy, investigator-cost or useful-cost
repayment estimates. Final process monitoring observed no competing Python
experiment; it was not an exclusive reservation.

Four contract tests pass. The [analyzer](evidence/final-v1-analysis/audit.json)
checks every hash, score, denominator and update sequence, equal stage starts,
and frozen-base/reset invariants. The [separate-process audit](evidence/final-v1-audit/audit.json)
checks all 3,036 token records and reproduces 48 probes across the 16 checkpoints
exactly; 32 inherited recall records match the original source. Development has
24 additional checkpoint replays. Verification generations are excluded from
accuracy denominators. Canonical answers need at most 13 tokens, below the 48-token
limit. [Reproduction](notes/reproduction.md).

This adapts standard supervised LoRA and replay, not a new editing algorithm.
[WISE v3](https://arxiv.org/html/2405.14768v3) already studies sequential editing,
generalization and locality; [SEAL v2](https://arxiv.org/html/2506.10943v2) measures
interference across self-edits. [MQuAKE v3](https://arxiv.org/html/2305.14795v3)
separates edited components from consequences; our complete-call measure does
not test its multi-hop setting. [LOKI v1](https://arxiv.org/html/2606.19679v1)
uses stronger locality machinery that is not implemented here. Exact paper
versions, author-code revisions and inspected paths are [recorded locally](sources/README.md).

The contribution is a bounded sequential comparison with functioning acquisition,
controlled update-count alternatives and fresh-input error separation. One small
routing family, one original seed, an oracle-assisted replay mask, positive-example
scope ambiguity and imperfect identifier production limit generality. Calls were
emitted, not executed in an external environment. Successful final routing does
not establish an internal symbolic program, independently editable parameters,
or preservation of unrelated language abilities. This completes the initial
comparison; it does not retire the broader retention-and-revision question.
