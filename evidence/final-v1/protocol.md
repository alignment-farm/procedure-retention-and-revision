# Fixed fresh-input comparison

14 September 2026. Fixed before final model evaluation. Develop on the CE state
using development-v1.md; if development fails to establish B/C routing, diagnose
and amend before running this protocol. No fresh outputs will choose checkpoints,
learning rate, training data, replay composition, method inclusion or stopping.

Use both inherited acquired states: CE-128 and forward-KL-high-128 (same original
seed 41). Use the published earliest >=15/16 recall selection, not a selection
made from this study's outputs. These are two starting states, not independent
seeds or independently reproduced acquisition. All local B/C attempts are in
final denominators even if an endpoint fails. Fixed endpoint is 128 target
blocks; there is no checkpoint selection inside the final run.

Original A: copper→kestrel, violet→marten; uppercase, -Q iff fast. B adds
amber→marten and teal→kestrel with the same argument rule. C changes only
copper/fast to marten; all other outputs are unchanged. This is a small
conjunctive-routing comparison, not a novel editing algorithm or multi-hop task.
A uses the 16 inherited examples; B uses 16 examples from fepzan, molkit, vurbex,
tasnid; C uses four copper/fast examples from jebrun, waskel, pivnot, zomdak.
No verbal rule enters the students' generation or checked-label training prompt.

For each acquired state, reset AdamW (lr 0.0005, weight decay 0) for each stage:

1. A carried/no-update reference, without teaching context.
2. B-only: 128 new examples, no replay.
3. B-double: 128 identical target blocks, each immediately repeated (256 updates).
4. B-replay: same 128 B blocks plus 128 interleaved A examples (256 updates).
5. From B-replay, C-only: 128 correction updates.
6. From the same B-replay, C-double: each correction repeated (256 updates).
7. From the same B-replay, C-replay: 128 corrections plus 128 interleaved
   unaffected A/B examples (256 updates). All four obsolete copper/fast A
   examples are excluded; the replay pool has 28 examples.

All arms share target order (Python Random 73, shuffled epochs); replay order is
also fixed. Double and replay match update count, not answer tokens or semantic
information. A checkpoint suffix of 128 denotes target blocks; double/replay
have 256 optimizer steps. New-learning routing criterion: >=15/16 B recall.
Correction acquisition criterion: 4/4 C routing recall. Report scores even when
these are missed and do not reinterpret failed acquisition as forgetting.

References: untrained base with no evidence; base with 32 original A+B examples;
base with 28 unaffected A/B examples and the four actual C examples. The revised
reference REMOVES obsolete examples rather than relabeling them. Thus its
information is the union available to C-replay, although all examples stay in
inference context. Original-context reference has no correction. This repairs
the development context's extra four relabeled examples for information parity;
it is a design correction made before fresh outputs, not a selected result.
Generic induction reminder is retained; no complete rules or retrieval oracle.

Fresh material: 12 random lowercase ASCII identifiers, three each of lengths
4,6,8,10, RNG 2026091417. Cross with all four A and four B conditions (96 fresh
queries total). The small size keeps this comparison bounded; counts are
workload-conditional rather than population estimates. Exclude study training
and development identifiers, plus pinned prior diagnostic/final identifiers.
These are new strings, not new input-field combinations or unseen paraphrases.
Original A recall16, B recall16 and C recall4 are scored separately at every
state. 17 states (7 per acquired source plus 3 references) ×132 calls =2244
main generations; 2560 optimizer updates, plus separate verification replays.

Measures: full exact calls; syntactically valid route, uppercase identifier and
suffix separately. Within A, report 12 revised-scope and 36 unaffected fresh
queries separately. Report stale old routes and overgeneralization to copper/slow;
B remains an unaffected suite during correction. Paired correct→wrong counts
compare identical queries under unchanged target relations. C scope correctness
must use the new target; retaining its old answer is a stale error. No p-values
or independent-trial confidence intervals on crossed conditions are planned.

Save/reload audits establish process-boundary persistence; B comparisons measure
retention under later learning; C measures correction after that learning.
Replay supplies boundary evidence as well as rehearsal, so a benefit alone
cannot identify independent edit parameters. Whole-call scores do not measure
external action execution. No acquisition, storage, inference or repayment cost
is treated as free; record all updates, tokens, times, checkpoints and waits.

Native pinned 4B Qwen/MLX route; 40 GB peak ceiling, 30-minute active ceiling
(increased from development's 20 minutes for both starts and count controls).
One-hour maximum resource wait, with visible competing runs yielded to. No new
model download or paid experimental calls. Preserve interruptions and failures.

## Development-informed endpoint amendment (before fresh generation)

CE development B-only learns all 16 new calls by step32 with old routing16/16,
but old routing falls to8/16 at step128 while B recall remains16/16. This makes
a shorter update budget an important alternative to replay. Therefore retain
and freshly evaluate BOTH 32 and128 checkpoints for B-only and C-only in each
starting state. C-only's early checkpoint is included before its development
result is inspected, for the same budget/locality question. Do not select the
better endpoint after fresh results; report both. No other arm's duration changes.
This adds four states and no optimizer steps: 21×132=2772 main generations,
2560 updates. It supersedes the 17-state/2244-generation count above and the
statement that the final run has only128-block evaluations. The fixed128
comparisons remain intact; this is a prospective added early-budget reference.

## Reference-information amendment (before fresh generation)

Development's example-only original reference routes only10/16 new B queries
correctly, despite copying all16 identifiers. Add two clearly privileged
complete-rule references (original and revised), using the untrained base and
no examples. They state all four channel routes, the uppercase/suffix rules,
and for revision the copper AND fast exception. This is stronger supervision
than checked examples; it is a capability/information check, not a matched-data
memory-placement competitor. It can distinguish difficulty inferring a rule
from examples from difficulty executing an explicitly supplied rule. Report
both references, without choosing among prompts from final outcomes.

Now 23 states ×132=3036 main generations; still2560 optimizer updates. This
supersedes prior generation totals. The 30-minute active limit remains unchanged.

## Execution sizing after completed development

Development-v2 completed with B recall16/16 and C recall4/4 at128, so proceed
without a learning-recipe repair. Development took535.24 seconds excluding its
810.46-second resource wait, for816 generations and768 updates. Scaling the
measured total by3036/816 gives about33.2 minutes; size the final active ceiling
at40 minutes rather than30 to allow the already specified comparison to finish.
This changes only the timeout, not data, endpoints or arm inclusion. Memory
ceiling remains40 GB; development peak was9.62 GB. No further training search.
