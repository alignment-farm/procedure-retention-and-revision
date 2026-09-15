# Scope evidence and rehearsal during procedural correction

14 September 2026. Bounded follow-up complete; the broader retention and revision
question remains open. Fresh execution: **`692f592`**. Evidence and audits:
**`1c461a7`**, completed instrument audit **`a9a7194`**. The accepted
[first findings](FINDINGS.md) remain unchanged.

**Seven crossed boundary examples can recover perfect fresh routing without a
broader archive. Historical rehearsal has an additional, conditional effect on
complete calls.** With the same boundary examples and optimizer-step budget,
history reduces losses of previously correct calls in three starting states,
but increases them in the fourth. All 16 primary endpoints lose some previously
correct unchanged calls. One history treatment also leaves four familiar
in-scope answers stale despite correcting most unfamiliar inputs.

[Fixed protocol](protocol/scope-anchored-final-v1.md) ·
[All results and component losses](evidence/scope-final-v1-analysis/compact-tables.md) ·
[Attempt and selection record](notes/scope-development-decision.md) ·
[Reproduction](notes/scope-reproduction.md)

## What the comparison changes

The original procedure routes copper to kestrel and violet to marten. Later
learning adds amber to marten and teal to kestrel. Every call uppercases its
identifier and appends `-Q` only for fast priority. The correction changes
**only copper/fast to marten**. Other routes and all argument rules are unchanged.

Four positive corrections use four identifiers. Seven new, investigator-labeled
boundary examples cover every unchanged channel/priority condition on **jebrun**,
which is also a correction identifier. Thus one identifier appears in all eight
conditions. No verbal rule or examples enter the student's generation prompt.

Each arm restores the same pre-correction weights within its starting state and
resets AdamW. The primary endpoint is 128 target blocks:

| Treatment | Correction updates | Boundary updates | Historical updates | Total updates | Distinct checked cases |
|---|---:|---:|---:|---:|---:|
| Corrections only | 128 | 0 | 0 | 128 | 4 |
| Triple corrections | 384 | 0 | 0 | 384 | 4 |
| Repeat boundary | 128 | 256 | 0 | 384 | 11 |
| Add history | 128 | 128 | 128 | 384 | 39 |

The two boundary arms receive identical correction and first boundary examples
in identical order. The third update either repeats that boundary case or uses
an old example with the **same channel and priority**, changing the identifier.
Consequently, condition exposure and tool/suffix labels match. History cycles
all 28 valid old/later examples; four obsolete copper/fast records are removed,
not relabeled. The investigator supplies this validity decision. The learner
does not discover obsolete history.

This matches access to the seven explicit boundary cases, not total information.
The small set itself rehearses behavior; history adds identifier diversity and
evidence of invariance across identifiers. The contrast measures the effect of
replacing boundary repetitions with historical examples. It cannot identify a
pure scope-information effect or an internal protection mechanism.

## Fresh routing and complete calls separate

Twelve fresh identifiers, three each of lengths 4, 6, 8 and 10, cross all eight
conditions: 12 corrected-scope and 84 unchanged queries. They are disjoint from
training, development and prior evaluation identifiers. These are unfamiliar
strings, not unseen condition combinations or paraphrases. Four original
in-scope training inputs are also evaluated under their **new** target.

At 128, all 16 correction endpoints recall all four correction calls exactly.
Both boundary treatments also recall all seven boundary calls, and every
history endpoint recalls all 28 valid historical calls. These are functioning
writes, but fitting supplied examples does not guarantee selective transfer.

Scope cells below show **correct routes / complete calls**, each out of 12.
Routing recognizes the initial tool independently of argument syntax; a correct
tool followed by a malformed argument is still an incorrect complete call.

| Starting state | Treatment | Fresh scope route / call | Other fresh routes /84 | Familiar scope routes /4 | All fresh calls /96 |
|---|---|---:|---:|---:|---:|
| Inherited CE | Repeat boundary | 12 / 4 | 77 | 4 | 27 |
| Inherited CE | Add history | 11 / 4 | 83 | 0 | 46 |
| Inherited FK | Repeat boundary | 12 / 0 | 84 | 4 | 14 |
| Inherited FK | Add history | 12 / 8 | 82 | 4 | 57 |
| CE seed 101 | Repeat boundary | 12 / 4 | 84 | 4 | 35 |
| CE seed 101 | Add history | 12 / 9 | 84 | 4 | 74 |
| CE seed 202 | Repeat boundary | 12 / 4 | 81 | 4 | 30 |
| CE seed 202 | Add history | 12 / 2 | 84 | 4 | 23 |

The small boundary set achieves 96/96 fresh routes from inherited FK and seed
101, and corrects all four familiar scope routes. Thus broad history is not
necessary for routing locality in these regimes. FK nevertheless has **zero
correct complete calls on the 12 fresh corrected inputs** under boundary
repetition. Perfect routing does not establish preserved argument behavior.

Both correction-only controls achieve 12/12 scoped routes but only 48/84
unchanged routes in every start. All 12 copper/slow queries are overgeneralized;
new-channel routing is 24/48. Their complete calls range from 1 to 14/96.
Tripling updates does not recover locality. The boundary examples change this
outcome, while supplying rehearsal as well as scope evidence.

History removes copper/slow overgeneralization in all four starts. Its remaining
errors differ: inherited CE gives one stale fresh scope route and one wrong
later-channel route; FK gives two wrong later-channel routes. CE history also
preserves the obsolete route on all four original scoped inputs. Those records
were excluded from replay, but their learned effects were not erased. A simple
[counterexample rule](notes/scope-familiar-counterexample.json)—retain the old
rule on original identifiers and apply the revision elsewhere—fits every
supplied training example. This demonstrates remaining information ambiguity,
not the network's internal mechanism.

## Net gains can hide lost behavior

These comparisons pair the **same 84 unchanged inputs and target answers** with
each start's pre-correction responses. “Lost” means correct before, incorrect
after; “gained” means the reverse. Revised-scope inputs are excluded from these
retention counts because their target legitimately changes.

| Start | Correct before | Repeat: lost / gained | History: lost / gained |
|---|---:|---:|---:|
| Inherited CE | 37 | 19 / 5 | 15 / 20 |
| Inherited FK | 41 | 33 / 6 | 7 / 15 |
| CE seed 101 | 13 | 8 / 26 | 5 / 57 |
| CE seed 202 | 37 | 17 / 6 | 24 / 8 |

History reduces paired call losses in three starts, beyond access to any missing
channel/priority boundary condition. It worsens them in seed 202. Its large net
gains are often new successes: seed 101 improves from 13 to 65 correct unchanged
calls while still losing five of the original 13. CE improves 37 to 42 while
losing 15. These are not complete preservation.

Components also trade off. In FK, history reduces identifier losses from 33 to
six, but increases suffix losses from four to seven and route losses from zero
to two. In seed 202, it fixes three routing failures while increasing identifier
losses from 16 to 24. [All paired components](evidence/scope-final-v1-analysis/paired.json)
remain separate; improvements do not identify independently editable parameters.

## Development, acquisition and budget decisions

Initial development used seven historical boundary cases with identifiers
absent from all corrections. Identifier-specific exceptions fit those data.
One bounded diagnostic introduced the crossed jebrun cases above; the original
development and superseded, unexecuted final plan are preserved. Both diagnostic
arms first met joint correction/boundary recall at 128, fixing the primary
endpoint before fresh evaluation. No fresh result selected a recipe or checkpoint.

The inherited CE and FK states share original acquisition seed 41 and the
accepted B-replay preparation. They are not independent replications. Two new
CE acquisitions, seeds 101 and 202, each reach 16/16 original training calls.
Seed 101's 32-update later-learning stage routes all old/new training inputs,
but completes only 4/16 old and 11/16 new calls. Seed 202 initially routes only
8/16 in each set. One repair restores its acquired state and adds old replay:
32 target blocks still fail; 128 reaches 16/16 exact old and new calls. This
establishes a functioning start without isolating why that repair worked.
All attempts are in the [ledger](notes/scope-development-decision.md).

The final therefore tests four common starts with different histories, including
two independently acquired adapters. It is not four independent replications of
one complete pipeline. Every start uses the same subsequent correction recipe;
“FK” denotes acquisition provenance, not the correction objective.

Both boundary arms' 32-block checkpoints are also reported. Only FK with history
meets both training criteria there. It selects all 96 fresh tools, but only 65
calls have valid syntax and 22 are exact. At 128, it has 94 correct tools and
57 exact calls. Shorter learning is neither uniformly sufficient nor uniformly
preferable; these endpoints were retained without choosing between them from
fresh outcomes.

## Costs, checks and interpretation

The pinned Qwen3-4B-Instruct-2507 bf16 model uses rank-8 q/v LoRA in the last
eight blocks, scale 2, no dropout, and hard-label CE with AdamW at 0.0005 and
zero weight decay. Model revision, package/code pins and author-method overlap
are in [source provenance](sources/README.md). This adapts ordinary supervised
LoRA/replay, with substantial overlap with WISE/SEAL's locality and interference
questions; it is not a new editing algorithm or an author-method reproduction.

Each repeated-boundary/history arm uses 384 updates and respectively
30,614/30,536 training input tokens and 3,724/3,762 answer tokens per start.
Equal steps do not imply exact token or compute equality. The final run uses
5,120 updates, 3,892 generations and 28 checkpoint files: 923.6 seconds in
updates, 1,264.7 in generation, 2,401.4 elapsed, and 9.62 GB peak MLX allocation.
Training consumes 407,928 input and 50,936 answer tokens; inference consumes
277,340 prompt and 41,979 generated tokens. One 655,360-parameter adapter is
2,624,893 bytes; the final checkpoint files total 73.50 MB.

Including both developments, both new acquisitions and the repair, the
follow-up records **7,360 updates and 5,131 generations**, 56.1 active experimental
minutes plus 20.8 minutes yielding to shared hardware. Separate audit and
investigator time are outside those timers. Reused acquisition/preparation costs
remain in the accepted source ledger. No new model download or paid experimental
call was needed. [Complete costs](evidence/scope-costs.json). These observational
timers are not isolated benchmarks, energy measurements or repayment estimates.

Seven contract tests pass. Audits verify all response tokens and all updates'
token counts, reproduce 147 saved-state probes exactly, and match 216 reused-start
recall records. Every score, denominator, update schedule, checkpoint hash and
common-start/base-reset invariant is checked. The longest canonical answer is
13 tokens. All 62 generations reaching the 48-token cap had already diverged
from their canonical answer; appending tokens could not repair their exact-call
score. Five outputs have unknown initial tools, all in one failed early endpoint.
[Instrument audit](evidence/scope-instrument-audit.json),
[final reload audit](evidence/scope-final-v1-audit/audit.json).

The bounded answer is that broader history is unnecessary for some routing
successes and has a separate, state-dependent effect on preservation and new
call successes under matched boundary-case access. The small set already
rehearses behavior, so pure scope information and rehearsal remain joined.
One task, one model, few acquired states, oracle labels/filtering and unfamiliar
strings within a fixed input format limit generality. Calls were emitted, not
executed. Full procedural retention, automatic history revision and a general
memory-placement ranking are not established.
