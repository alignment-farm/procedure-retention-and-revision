# Complete work-order maintenance

| State | Version | Complete | Eligibility | Shipment | Stock |
|---|---:|---:|---:|---:|---:|
| explicit-rules | 0 | 85/160 | 160 | 125 | 120 |
| explicit-rules | 1 | 80/160 | 121 | 89 | 130 |
| explicit-rules | 2 | 70/160 | 132 | 102 | 130 |
| seed311-base | 0 | 0/96 | 19 | 19 | 11 |
| seed311-A256 | 0 | 64/64 | 64 | 64 | 64 |
| seed311-A256-new | 0 | 32/32 | 32 | 32 | 32 |
| seed311-no-update | 0 | 160/160 | 160 | 160 | 160 |
| seed311-no-update | 1 | 140/160 | 140 | 150 | 150 |
| seed311-no-update | 2 | 120/160 | 120 | 140 | 140 |
| seed311-novel-v1 | 1 | 132/160 | 132 | 148 | 148 |
| seed311-novel-v2 | 2 | 120/160 | 120 | 140 | 140 |
| seed311-bridged-v1 | 1 | 140/160 | 140 | 150 | 150 |
| seed311-bridged-v2 | 2 | 120/160 | 120 | 140 | 140 |

## Paired unchanged tasks

| State | Group | n | Before | After | Lost | Gained |
|---|---|---:|---:|---:|---:|---:|
| seed311-novel-v1 | all | 140 | 140 | 112 | 28 | 0 |
| seed311-novel-v1 | acquired | 56 | 56 | 49 | 7 | 0 |
| seed311-novel-v1 | fresh | 28 | 28 | 21 | 7 | 0 |
| seed311-novel-v2 | all | 140 | 112 | 100 | 12 | 0 |
| seed311-novel-v2 | acquired | 56 | 49 | 40 | 9 | 0 |
| seed311-novel-v2 | fresh | 28 | 21 | 20 | 1 | 0 |
| seed311-bridged-v1 | all | 140 | 140 | 120 | 20 | 0 |
| seed311-bridged-v1 | acquired | 56 | 56 | 48 | 8 | 0 |
| seed311-bridged-v1 | fresh | 28 | 28 | 24 | 4 | 0 |
| seed311-bridged-v2 | all | 140 | 120 | 100 | 20 | 0 |
| seed311-bridged-v2 | acquired | 56 | 48 | 40 | 8 | 0 |
| seed311-bridged-v2 | fresh | 28 | 24 | 20 | 4 | 0 |

## Changed obligations

| State | Group | Complete | Stale | Downstream complete |
|---|---|---:|---:|---:|
| seed311-novel-v1 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed311-novel-v1 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed311-novel-v1 | correction-new | 8/8 | 0 | 4/4 |
| seed311-novel-v1 | fresh | 4/4 | 0 | 2/2 |
| seed311-novel-v2 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed311-novel-v2 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed311-novel-v2 | correction-new | 8/8 | 0 | 4/4 |
| seed311-novel-v2 | fresh | 4/4 | 0 | 2/2 |
| seed311-bridged-v1 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed311-bridged-v1 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed311-bridged-v1 | correction-new | 8/8 | 0 | 4/4 |
| seed311-bridged-v1 | fresh | 4/4 | 0 | 2/2 |
| seed311-bridged-v2 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed311-bridged-v2 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed311-bridged-v2 | correction-new | 8/8 | 0 | 4/4 |
| seed311-bridged-v2 | fresh | 4/4 | 0 | 2/2 |
