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
