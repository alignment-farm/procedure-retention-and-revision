# Scope evidence and rehearsal during procedural correction

**Status: Commissioned follow-up, 14 September 2026.** Develop and run a bounded
comparison addressing the question below. Preparing this handoff did not launch
experiments. The investigator owns the workload, methods, resource sizing and
routine execution, and can proceed independently of the other ancillary studies.

**Does selective correction require information identifying its scope,
rehearsal preserving prior computation, or both?** The root's
[concurrent-study assessment](../../construct-2/studies/2026-09-14-concurrent-findings.md)
records the synthesis and prospective expectations motivating this follow-up.

## What the accepted result leaves unresolved

The accepted [FINDINGS.md](FINDINGS.md), publication
`9696af5ef32a86571b66bcedec3b3cd241aef9a0`, establishes a useful starting point:
the FK-acquired state finishes the sequence with 96/96 fresh routes correct
under filtered replay. Complete calls remain 19/96, and five previously correct
calls on unchanged old inputs are lost. This supports selective routing under
the tested assistance, while the stronger R4 prediction of preserving argument
behavior was not met in that sequence.

All correction arms began from the corresponding common B-replay state. Replay
then supplied unaffected examples and an investigator-known validity mask that
removed obsolete copper/fast records. Positive correction examples alone did
not uniquely identify the scope. The comparison therefore cannot separate scope
information from rehearsal's protection of previously learned behavior. Matching
optimizer steps excluded a simple update-count explanation, but did not match
boundary information, label diversity or token cost.

## Explanations to distinguish

- **Scope information explains most of the locality gain.** A small amount of
  evidence distinguishing changed from unchanged conditions could recover routing
  locality without broad replay. This would weaken the claim that revisiting a
  larger archive is necessary for the observed correction.
- **Broader rehearsal has a separate protective role.** After boundary information
  is matched, rehearsing unaffected behavior could still prevent paired losses
  or improve correction across fresh inputs. That would support a retention
  benefit beyond simply clarifying the intended change, without by itself
  identifying an internal computational mechanism.
- **Both matter, with different effects.** Boundary evidence could limit the
  routing change while broader rehearsal protects other relations or argument
  production. Conversely, perfect routing with continuing argument losses would
  further narrow selective editability to the decision component.

Begin with the working setup and change only what is needed to distinguish these
accounts. Useful contrasts include correction examples alone versus correction
with informative boundary cases, followed by narrower versus broader rehearsal
with comparable boundary-information access. These are design leads, not a
mandatory factorial or frozen protocol. A boundary example itself also rehearses
behavior; specify what the chosen contrasts can isolate and what remains joined.

Use common functioning starting states for comparisons. The two inherited
acquisitions share seed 41; they are not independent replications. Where feasible,
include independently acquired starts to test whether the explanation survives
beyond those selected states, recording acquisition attempts and selection.
Reproducing every previous arm is unnecessary. The investigator may develop a
more informative contrast within the same question.

## Evidence needed for the interpretation

Make each arm's boundary information explicit: contrasting examples, verbal
scope statements and supplied validity labels are different interventions.
Hold that access comparable when attributing a difference to broader rehearsal.
Disclose which history is removed, how obsolescence is established and whether
the investigator supplies the answer. Do not attribute a correct validity mask
to the learner unless it actually learns or infers it.

Prevent training duration or extra compute from becoming an unexamined replay
explanation. Choose controls appropriate to the claim and report target and
replay updates, tokens and costs separately; equal steps are not equal evidence
or compute. Use the earlier shorter-budget result when deciding what comparison
is informative, rather than assuming a longer endpoint is preferable.

Use fresh in-scope and unchanged inputs for the developed claim. Measure scoped
correction, overbroad changes and stale answers alongside paired before/after
losses on identical unchanged targets. Keep route choice, syntactic validity,
argument production and whole-call correctness distinguishable: a malformed
argument with the right tool is not evidence of a wrong routing choice. Report
both correction acquisition and preservation of previously demonstrated behavior.

The existing [research guidance](AGENTS.md) applies. Calibrate on development
material and pursue purposeful diagnosis if a proposed treatment does not learn;
verified updates alone are insufficient. Fix selection before fresh evaluation
of a developed claim, preserve failed attempts, and close on explanatory progress,
a demonstrated limitation or a concrete resource constraint. Coordinate heavy
Mac Studio use with the other investigators.

Preserve the accepted findings, frozen protocols and evidence. Publish the
follow-up separately with its methods, supporting records and reproduction
instructions, then link it from the README. No new editing algorithm or full
procedural retention should be claimed from routing locality alone.
