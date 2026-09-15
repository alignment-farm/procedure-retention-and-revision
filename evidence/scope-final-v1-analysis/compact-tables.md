# Fresh scope and rehearsal comparison

Primary endpoint: 128 target blocks. Counts are conditional on this workload.

| Start | Treatment | Fresh scope route /12 | Old scope route /4 | Unchanged route /84 | Stale /12 | Overbroad /12 | Full /96 |
|---|---|---:|---:|---:|---:|---:|---:|
| ce | before | 0 | 0 | 78 | 12 | 0 | 37 |
| ce | only | 12 | 4 | 48 | 0 | 12 | 14 |
| ce | triple | 12 | 4 | 48 | 0 | 12 | 13 |
| ce | boundary-repeat | 12 | 4 | 77 | 0 | 7 | 27 |
| ce | boundary-history | 11 | 0 | 83 | 1 | 0 | 46 |
| forward | before | 0 | 0 | 84 | 12 | 0 | 41 |
| forward | only | 12 | 4 | 48 | 0 | 12 | 7 |
| forward | triple | 12 | 4 | 48 | 0 | 12 | 12 |
| forward | boundary-repeat | 12 | 4 | 84 | 0 | 0 | 14 |
| forward | boundary-history | 12 | 4 | 82 | 0 | 0 | 57 |
| seed101 | before | 0 | 0 | 84 | 12 | 0 | 13 |
| seed101 | only | 12 | 4 | 48 | 0 | 12 | 11 |
| seed101 | triple | 12 | 4 | 48 | 0 | 12 | 1 |
| seed101 | boundary-repeat | 12 | 4 | 84 | 0 | 0 | 35 |
| seed101 | boundary-history | 12 | 4 | 84 | 0 | 0 | 74 |
| seed202 | before | 0 | 0 | 84 | 12 | 0 | 37 |
| seed202 | only | 12 | 4 | 48 | 0 | 12 | 6 |
| seed202 | triple | 12 | 4 | 48 | 0 | 12 | 1 |
| seed202 | boundary-repeat | 12 | 4 | 81 | 0 | 3 | 30 |
| seed202 | boundary-history | 12 | 4 | 84 | 0 | 0 | 23 |

## Complete-call preservation on the same 84 unchanged inputs

| Start | Treatment | Before | After | Lost | Gained | Format /96 | Identifier /96 | Suffix /96 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ce | boundary-repeat | 37 | 23 | 19 | 5 | 96 | 28 | 77 |
| ce | boundary-history | 37 | 42 | 15 | 20 | 96 | 47 | 90 |
| forward | boundary-repeat | 41 | 14 | 33 | 6 | 96 | 14 | 91 |
| forward | boundary-history | 41 | 49 | 7 | 15 | 93 | 58 | 89 |
| seed101 | boundary-repeat | 13 | 31 | 8 | 26 | 96 | 35 | 88 |
| seed101 | boundary-history | 13 | 65 | 5 | 57 | 96 | 74 | 96 |
| seed202 | boundary-repeat | 37 | 26 | 17 | 6 | 96 | 31 | 95 |
| seed202 | boundary-history | 37 | 21 | 24 | 8 | 96 | 23 | 95 |

## Paired component losses / previously correct unchanged cases

| Start | Treatment | Route | Identifier | Suffix | Full call |
|---|---|---:|---:|---:|---:|
| ce | boundary-repeat | 7/78 | 24/43 | 13/83 | 19/37 |
| ce | boundary-history | 0/78 | 15/43 | 4/83 | 15/37 |
| forward | boundary-repeat | 0/84 | 33/41 | 4/83 | 33/41 |
| forward | boundary-history | 2/84 | 6/41 | 7/83 | 7/41 |
| seed101 | boundary-repeat | 0/84 | 15/27 | 0/43 | 8/13 |
| seed101 | boundary-history | 0/84 | 6/27 | 0/43 | 5/13 |
| seed202 | boundary-repeat | 3/84 | 16/37 | 1/84 | 17/37 |
| seed202 | boundary-history | 0/84 | 24/37 | 1/84 | 24/37 |

## Prespecified short-budget checkpoints (32 target blocks)

| Start | Treatment | C recall /4 | Boundary /7 | Fresh scope /12 | Old scope /4 | Unchanged routes /84 | Full /96 |
|---|---|---:|---:|---:|---:|---:|---:|
| ce | boundary-repeat | 3 | 7 | 12 | 4 | 72 | 31 |
| ce | boundary-history | 0 | 5 | 0 | 0 | 82 | 43 |
| forward | boundary-repeat | 0 | 3 | 0 | 0 | 41 | 1 |
| forward | boundary-history | 4 | 7 | 12 | 4 | 84 | 22 |
| seed101 | boundary-repeat | 0 | 3 | 0 | 0 | 39 | 14 |
| seed101 | boundary-history | 4 | 6 | 12 | 4 | 73 | 67 |
| seed202 | boundary-repeat | 4 | 6 | 10 | 4 | 78 | 27 |
| seed202 | boundary-history | 0 | 5 | 0 | 0 | 60 | 3 |

## Update costs by source

| Start/treatment | Source | Updates | Unique cases | Input tokens | Answer tokens | Seconds |
|---|---|---:|---:|---:|---:|---:|
| ce-only | target | 128 | 4 | 10208 | 1312 | 23.49 |
| ce-triple | repeat | 256 | 4 | 20416 | 2624 | 46.07 |
| ce-triple | target | 128 | 4 | 10208 | 1312 | 23.06 |
| ce-boundary-repeat | boundary | 128 | 7 | 10203 | 1206 | 22.96 |
| ce-boundary-repeat | boundary-repeat | 128 | 7 | 10203 | 1206 | 22.93 |
| ce-boundary-repeat | target | 128 | 4 | 10208 | 1312 | 23.00 |
| ce-boundary-history | boundary | 128 | 7 | 10203 | 1206 | 23.18 |
| ce-boundary-history | history | 128 | 28 | 10125 | 1244 | 23.21 |
| ce-boundary-history | target | 128 | 4 | 10208 | 1312 | 23.20 |
| forward-only | target | 128 | 4 | 10208 | 1312 | 23.52 |
| forward-triple | repeat | 256 | 4 | 20416 | 2624 | 45.71 |
| forward-triple | target | 128 | 4 | 10208 | 1312 | 22.88 |
| forward-boundary-repeat | boundary | 128 | 7 | 10203 | 1206 | 23.39 |
| forward-boundary-repeat | boundary-repeat | 128 | 7 | 10203 | 1206 | 23.39 |
| forward-boundary-repeat | target | 128 | 4 | 10208 | 1312 | 23.44 |
| forward-boundary-history | boundary | 128 | 7 | 10203 | 1206 | 23.01 |
| forward-boundary-history | history | 128 | 28 | 10125 | 1244 | 23.06 |
| forward-boundary-history | target | 128 | 4 | 10208 | 1312 | 23.08 |
| seed101-only | target | 128 | 4 | 10208 | 1312 | 22.60 |
| seed101-triple | repeat | 256 | 4 | 20416 | 2624 | 46.14 |
| seed101-triple | target | 128 | 4 | 10208 | 1312 | 23.06 |
| seed101-boundary-repeat | boundary | 128 | 7 | 10203 | 1206 | 22.61 |
| seed101-boundary-repeat | boundary-repeat | 128 | 7 | 10203 | 1206 | 22.62 |
| seed101-boundary-repeat | target | 128 | 4 | 10208 | 1312 | 22.64 |
| seed101-boundary-history | boundary | 128 | 7 | 10203 | 1206 | 23.77 |
| seed101-boundary-history | history | 128 | 28 | 10125 | 1244 | 23.80 |
| seed101-boundary-history | target | 128 | 4 | 10208 | 1312 | 23.79 |
| seed202-only | target | 128 | 4 | 10208 | 1312 | 23.46 |
| seed202-triple | repeat | 256 | 4 | 20416 | 2624 | 46.11 |
| seed202-triple | target | 128 | 4 | 10208 | 1312 | 23.10 |
| seed202-boundary-repeat | boundary | 128 | 7 | 10203 | 1206 | 22.70 |
| seed202-boundary-repeat | boundary-repeat | 128 | 7 | 10203 | 1206 | 22.73 |
| seed202-boundary-repeat | target | 128 | 4 | 10208 | 1312 | 22.74 |
| seed202-boundary-history | boundary | 128 | 7 | 10203 | 1206 | 23.08 |
| seed202-boundary-history | history | 128 | 28 | 10125 | 1244 | 23.02 |
| seed202-boundary-history | target | 128 | 4 | 10208 | 1312 | 23.06 |
