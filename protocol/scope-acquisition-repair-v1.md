# Bounded later-learning repair for seed202

14 September 2026. Both new independent A128 attempts reached16/16 exact original
recall. Seed101 B32 routes16/16 old and16/16 new cases (full4/16 and11/16).
Seed202 B32 routes8/16 old and8/16 new (full6/16 and8/16); it fails the functioning
start criterion. Preserve that failed attempt in scope-acquisition-v1.

One bounded repair, before fresh evaluation: restore seed202's saved A128,
reset AdamW, and train128 B target blocks, each followed by one original A replay
example. Same model/rate/LoRA and prior data; no new labels. This is the accepted
B-replay regimen applied to the independent acquisition, with its own fixed
seed202 B order. Reproduce the original A shuffle operations without training
to keep that B order. Replay order uses RNG73, balanced shuffled cycles of16.

Evaluate A/B/C recall at32 and128 target blocks. Save both and report both.
Choose earliest where A and B routing recall are each>=15/16, conditional on
the already verified A acquisition. Whole calls are reported separately and
not a selection criterion. No fresh strings enter this repair. If neither
passes, retain the failed seed and report the concrete limitation; no replacement
seed or further training search is authorized by this local plan.

Budget256 updates and108 recall generations (36 repeat acquisition verification,
36 at each B endpoint),25 active minutes/40 GB ceiling, shared hardware yielding.
The repeated A recall verifies the reused state; it is not a third independent
acquisition. Final starts will explicitly identify any repaired B state.
