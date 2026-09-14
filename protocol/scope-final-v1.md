# Fixed fresh comparison: matched scope conditions and archive breadth

14 September 2026. Fixed after scope-development-v1 and before fresh evaluation.
Primary endpoint: **128 target blocks**, selected by the development protocol's
earliest successful joint acquisition rule. Narrow learns 4/4 corrections and
7/7 boundary examples at both 32 and 128. Broad learns 0/4 corrections at 32 and
4/4 at 128, retaining 7/7 boundary examples at both. Thus 128 is the primary
matched acquisition endpoint. Preserve and freshly evaluate the 32-block
checkpoints of BOTH replay arms as a prospective budget diagnostic. Report
every specified endpoint, never choose one from final output.

Retain all four arms in scope-development-v1: only, repeat, narrow, broad. Same
model, optimizer, targets, oracle validity mask and condition-matched schedules.
All start-state/arm combinations use the identical target order. Narrow/broad
have identical condition order as well; they differ only in which historical
identifier realizes each replay condition after their first identical cycle.
Every arm restores its designated common starting adapter and resets AdamW.
No validation, rule text or examples enter a student generation prompt.

Four starts are fixed: inherited CE and FK B-replay-128, plus independently
initialized CE seeds 101 and 202 following A128/B32. All acquisition attempts
are included in the record. Check acquisition and later-learning training recall
before interpreting subsequent changes as retention. If either independent
start fails, diagnose on training/development material before fresh evaluation;
record the failed state and any bounded repair. Do not silently replace it.
Inherited CE/FK share original seed 41; the two additional seeds are independent
adapter initializations and acquisition orders on the same task/base model,
not independent populations or tasks.

Fresh identifiers: RNG 2026091429, 12 strings, three each of lengths 4,6,8,10.
Cross all eight channel/priority conditions (96 queries). Assert disjointness
from training, study development, accepted final identifiers and pinned prior
evaluation identifiers. Freshness concerns strings, not new condition
combinations or new task wording. Never use these outputs for treatment selection.
Also score all 16 A, 16 B and four C training cases separately at every state.

Per start: common before reference, all four 128-block endpoints, and narrow /
broad at 32 blocks. **28 states × 132 = 3,696 main generations**, **3,584 updates**.
Only has 128 target updates; repeat has 128 targets +128 immediate repetitions;
narrow/broad each have 128 targets +128 replay updates. The intermediate replay
checkpoints use 32+32 updates, but cost records include the entire retained
trajectory. Per-source token counts and update/generation times are separate.

Report C route/full acquisition; fresh in-scope route/full/stale counts; 36
unchanged old and 48 later-channel routes; overbroad copper/slow choices;
syntactic validity, identifier/suffix and full calls. Use the fixed scope_task
anchored-tool convention independently of malformed arguments. Also retain the
accepted strict-route metric. Pair all 84 identical unchanged targets with each
start's pre-correction state and report correct-to-wrong and wrong-to-correct
transitions for every component. Do not describe stale scope answers as retained
behavior. Analyze each acquired state separately; no pooled independent-trial
p-values or confidence intervals for crossed conditions.

This tests archive/identifier diversity beyond seven examples already covering
all unchanged conditions. Narrow examples jointly supply boundary information
and rehearsal. Further examples also give more evidence that routing is
identifier-invariant; a breadth benefit cannot uniquely identify protection of
an internal computation. The mask is investigator-known, and both arms exclude
four obsolete copper/fast A records. No learner validity discovery is claimed.
No new editing algorithm, external action execution or general memory-placement
ranking is tested. Preserve the accepted findings/protocol/evidence unchanged.

Development used 896 updates, 612 generations and 418.72 active seconds (150.05
seconds additional hardware wait), peak 9.62 GB. Final has 4× the updates and
6.04× the generations, so an active ceiling of 60 minutes gives headroom for
the already specified comparison and audits. Peak allocation ceiling remains
40 GB; no new model download or paid calls. Cooperatively yield to visible
sibling jobs; record all checks, waits and interruptions. Timers are not an
exclusive isolated-hardware benchmark. This is a bounded follow-up, not an
open-ended training search.
