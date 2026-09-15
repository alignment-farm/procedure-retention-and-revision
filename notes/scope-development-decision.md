# Development decision and attempt ledger

Development execution: `77d48b9`; analyzer/audit: `a129b16`. Evidence:
`evidence/scope-development-v1` and its sibling analysis/audit directories.
One complete correction development attempt, no restarts. The hardware wait
before model loading was 150.05 seconds; active run 418.72 seconds, peak 9.62 GB.

All four arms were run at the prespecified 32 and 128 target-block checkpoints.
The prospective selection criterion was 4/4 correction recall routes AND 7/7
narrow boundary routes for BOTH replay arms. It was met first at 128: broad
correction recall was 0/4 at 32, 4/4 at 128; narrow was 4/4 at both. All four
late endpoints had 4/4 exact C recall. No learning-rate or data search followed.

Development fresh routes /32 at 128: only20, repeat20, narrow28, broad31.
Full calls: 13,3,12,21. Unchanged correct-to-wrong full calls: 11,19,11,8,
from 21 initially correct unchanged calls. Broad also gained five correct calls.
Narrow supplied every boundary condition but overgeneralized to all four fresh
copper/slow identifiers. Thus evidence of having fit boundary examples does
not establish identifier-independent scope transfer.

At 32, broad retained all 28 unchanged routes but gave stale routes on all four
scoped queries; narrow corrected all four but overgeneralized to three of four
copper/slow inputs. Broad's acquisition delay motivates the prospective extra
32-block replay checkpoints in final; it does not justify selecting the better
fresh endpoint. The primary comparison stays at the jointly learned 128 budget.

Two independent acquisition attempts (fixed seeds101/202) are next. All their
results and any bounded diagnosis are appended below before final evaluation.

## Prospective identifying-contrast repair (before fresh evaluation)

Before executing scope-final-v1, inspection of the design exposed an identifier
confound: positive correction IDs and historical boundary IDs were disjoint.
The historical narrow arm fit its boundary cases while losing copper/slow on
unfamiliar strings. This warrants one bounded diagnostic of stronger scope
information, not an interpretation that broad history is already necessary.
The unexecuted scope-final-v1 plan is retained, superseded for execution by the
forthcoming anchored protocol. No fresh outputs have been generated or inspected.

`protocol/scope-boundary-diagnosis-v1.md` crosses all eight conditions on jebrun,
one correction identifier. Both new arms receive the exact same boundary case
at every block. The third update either repeats that boundary case or rehearses
an unaffected original case of the same condition. This controls optimizer
steps and explicit contrasting evidence while varying extra history access.
It still cannot isolate rehearsal from evidence of identifier invariance.
The additional diagnostic is 768 updates and375 generations; there will be no
further learning-rate/model/data search. Its fixed acquisition rule chooses the
primary final duration before any fresh evaluation.

The deterministic counterexamples in scope-boundary-counterexamples.json make
the diagnosis concrete. A rule that selects marten for any of the four C
identifiers and otherwise follows the original routing fits all4 C,7 narrow
and28 broad examples. It fails3/7 new crossed boundary cases. A rule that changes
copper except for druvan fits all4 C and7 narrow cases, but only25/28 broad and
6/7 crossed boundary cases. These are logical counterexamples, not inferred
models of the network. The intended scope rule fits every set. Finite examples
still cannot uniquely determine behavior on all unfamiliar strings.

Prospective schedule check: if32 is chosen for final, its replay RNG position
must reproduce the first32 blocks of the128-block diagnostic. The schedule
constructor previously advanced the target RNG only for the requested duration.
Before any32-block standalone/fresh run, it was fixed to build the128-block
target order first, so32 and128 have identical prefixes. All completed and
queued diagnostic schedules use128 and are unchanged. A contract test checks
this prefix identity; this is an implementation repair before final, not a
response to fresh outcomes.

## Crossed-boundary diagnostic result

Execution65fd4ec completed375 generations/768 updates in298.57 active seconds,
plus1,095.66 seconds yielding before model load. Primary128 is fixed: at32,
boundary-repeat C recall is3/4 and boundary-history0/4; at128 both C and boundary
recall are perfect (4/4,7/7). At128 repeat/history fresh routes are29/32 vs32/32;
full calls21 vs24. Of21 initially correct unchanged calls, repeat loses3 and
history loses0; neither gains an unchanged call. Both give3/4 exact scoped calls.

History's otherwise successful fresh routing leaves all four original A scoped
training routes stale (A current-rule recall12/16). These remain in every
standard evaluation; final adds an explicit familiar-scope subgroup to prevent
hiding this limit behind fresh transfer. No fresh outcomes informed this addition.
The repair/final protocol preserves the earlier endpoint failures and notes
that stronger crossed evidence, repeated rehearsal and archive diversity remain
different interventions. No further correction-recipe search will follow.
