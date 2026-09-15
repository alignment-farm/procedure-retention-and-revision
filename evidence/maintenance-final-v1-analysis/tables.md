# Complete work-order maintenance

| State | Version | Complete | Eligibility | Shipment | Stock |
|---|---:|---:|---:|---:|---:|
| explicit-rules | 0 | 99/192 | 192 | 147 | 144 |
| explicit-rules | 1 | 96/192 | 146 | 106 | 156 |
| explicit-rules | 2 | 84/192 | 159 | 125 | 157 |
| seed401-base | 0 | 0/128 | 17 | 17 | 10 |
| seed401-A256 | 0 | 64/64 | 64 | 64 | 64 |
| seed401-A256-new | 0 | 32/32 | 32 | 32 | 32 |
| seed401-no-update | 0 | 192/192 | 192 | 192 | 192 |
| seed401-novel-v1 | 1 | 192/192 | 192 | 192 | 192 |
| seed401-novel-v2 | 2 | 192/192 | 192 | 192 | 192 |
| seed401-bridged-v1 | 1 | 192/192 | 192 | 192 | 192 |
| seed401-bridged-v2 | 2 | 120/192 | 120 | 156 | 156 |
| seed402-base | 0 | 0/128 | 17 | 17 | 10 |
| seed402-A256 | 0 | 41/64 | 57 | 48 | 63 |
| seed402-A256-new | 0 | 18/32 | 26 | 24 | 31 |
| seed402-A512 | 0 | 64/64 | 64 | 64 | 64 |
| seed402-A512-new | 0 | 32/32 | 32 | 32 | 32 |
| seed402-no-update | 0 | 192/192 | 192 | 192 | 192 |
| seed402-novel-v1 | 1 | 179/192 | 179 | 191 | 191 |
| seed402-novel-v2 | 2 | 132/192 | 132 | 156 | 156 |
| seed402-bridged-v1 | 1 | 179/192 | 179 | 191 | 191 |
| seed402-bridged-v2 | 2 | 130/192 | 130 | 166 | 166 |

## Paired unchanged tasks

| State | Group | n | Before | After | Lost | Gained |
|---|---|---:|---:|---:|---:|---:|
| seed401-novel-v1 | all | 168 | 168 | 168 | 0 | 0 |
| seed401-novel-v1 | acquired | 56 | 56 | 56 | 0 | 0 |
| seed401-novel-v1 | fresh | 56 | 56 | 56 | 0 | 0 |
| seed401-novel-v1 | earlier-revision | 0 | 0 | 0 | 0 | 0 |
| seed401-novel-v2 | all | 168 | 168 | 168 | 0 | 0 |
| seed401-novel-v2 | acquired | 56 | 56 | 56 | 0 | 0 |
| seed401-novel-v2 | fresh | 56 | 56 | 56 | 0 | 0 |
| seed401-novel-v2 | earlier-revision | 24 | 24 | 24 | 0 | 0 |
| seed401-bridged-v1 | all | 168 | 168 | 168 | 0 | 0 |
| seed401-bridged-v1 | acquired | 56 | 56 | 56 | 0 | 0 |
| seed401-bridged-v1 | fresh | 56 | 56 | 56 | 0 | 0 |
| seed401-bridged-v1 | earlier-revision | 0 | 0 | 0 | 0 | 0 |
| seed401-bridged-v2 | all | 168 | 168 | 96 | 72 | 0 |
| seed401-bridged-v2 | acquired | 56 | 56 | 32 | 24 | 0 |
| seed401-bridged-v2 | fresh | 56 | 56 | 32 | 24 | 0 |
| seed401-bridged-v2 | earlier-revision | 24 | 24 | 0 | 24 | 0 |
| seed402-novel-v1 | all | 168 | 168 | 155 | 13 | 0 |
| seed402-novel-v1 | acquired | 56 | 56 | 52 | 4 | 0 |
| seed402-novel-v1 | fresh | 56 | 56 | 52 | 4 | 0 |
| seed402-novel-v1 | earlier-revision | 0 | 0 | 0 | 0 | 0 |
| seed402-novel-v2 | all | 168 | 155 | 108 | 60 | 13 |
| seed402-novel-v2 | acquired | 56 | 52 | 36 | 20 | 4 |
| seed402-novel-v2 | fresh | 56 | 52 | 36 | 20 | 4 |
| seed402-novel-v2 | earlier-revision | 24 | 24 | 12 | 12 | 0 |
| seed402-bridged-v1 | all | 168 | 168 | 156 | 12 | 0 |
| seed402-bridged-v1 | acquired | 56 | 56 | 52 | 4 | 0 |
| seed402-bridged-v1 | fresh | 56 | 56 | 52 | 4 | 0 |
| seed402-bridged-v1 | earlier-revision | 0 | 0 | 0 | 0 | 0 |
| seed402-bridged-v2 | all | 168 | 155 | 106 | 61 | 12 |
| seed402-bridged-v2 | acquired | 56 | 51 | 36 | 19 | 4 |
| seed402-bridged-v2 | fresh | 56 | 52 | 35 | 21 | 4 |
| seed402-bridged-v2 | earlier-revision | 24 | 23 | 0 | 23 | 0 |

## Changed obligations

| State | Group | Complete | Stale | Downstream complete |
|---|---|---:|---:|---:|
| seed401-novel-v1 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed401-novel-v1 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed401-novel-v1 | correction-new | 8/8 | 0 | 4/4 |
| seed401-novel-v1 | fresh | 8/8 | 0 | 4/4 |
| seed401-novel-v2 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed401-novel-v2 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed401-novel-v2 | correction-new | 8/8 | 0 | 4/4 |
| seed401-novel-v2 | fresh | 8/8 | 0 | 4/4 |
| seed401-bridged-v1 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed401-bridged-v1 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed401-bridged-v1 | correction-new | 8/8 | 0 | 4/4 |
| seed401-bridged-v1 | fresh | 8/8 | 0 | 4/4 |
| seed401-bridged-v2 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed401-bridged-v2 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed401-bridged-v2 | correction-new | 8/8 | 0 | 4/4 |
| seed401-bridged-v2 | fresh | 8/8 | 0 | 4/4 |
| seed402-novel-v1 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed402-novel-v1 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed402-novel-v1 | correction-new | 8/8 | 0 | 4/4 |
| seed402-novel-v1 | fresh | 8/8 | 0 | 4/4 |
| seed402-novel-v2 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed402-novel-v2 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed402-novel-v2 | correction-new | 8/8 | 0 | 4/4 |
| seed402-novel-v2 | fresh | 8/8 | 0 | 4/4 |
| seed402-bridged-v1 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed402-bridged-v1 | familiar-withheld | 3/4 | 1 | 1/2 |
| seed402-bridged-v1 | correction-new | 8/8 | 0 | 4/4 |
| seed402-bridged-v1 | fresh | 8/8 | 0 | 4/4 |
| seed402-bridged-v2 | familiar-first-two | 4/4 | 0 | 2/2 |
| seed402-bridged-v2 | familiar-withheld | 4/4 | 0 | 2/2 |
| seed402-bridged-v2 | correction-new | 8/8 | 0 | 4/4 |
| seed402-bridged-v2 | fresh | 8/8 | 0 | 4/4 |
