| Acquired state | Later learning | Old route /48 | New route /48 | Old call /48 | New call /48 |
|---|---|---:|---:|---:|---:|
| ce | None | 48 | 12 | 19 | 8 |
| ce | 32 new | 48 | 48 | 20 | 21 |
| ce | 128 new | 24 | 48 | 6 | 12 |
| ce | 256 new | 25 | 48 | 9 | 20 |
| ce | 128 new +128 replay | 44 | 40 | 7 | 8 |
| forward | None | 48 | 24 | 15 | 8 |
| forward | 32 new | 48 | 48 | 2 | 4 |
| forward | 128 new | 47 | 48 | 6 | 13 |
| forward | 256 new | 41 | 48 | 10 | 12 |
| forward | 128 new +128 replay | 47 | 47 | 8 | 7 |

| Acquired state | Correction updates | Scope route /12 | Other old route /36 | New-channel route /48 | Full calls /96 | Stale /12 | Overbroad /12 |
|---|---|---:|---:|---:|---:|---:|---:|
| ce | 32 corrections | 12 | 23 | 24 | 9 | 0 | 12 |
| ce | 128 corrections | 12 | 24 | 24 | 5 | 0 | 12 |
| ce | 256 corrections | 12 | 24 | 24 | 6 | 0 | 12 |
| ce | 128 corrections +128 replay | 12 | 30 | 43 | 9 | 0 | 5 |
| forward | 32 corrections | 11 | 24 | 22 | 6 | 0 | 12 |
| forward | 128 corrections | 12 | 24 | 24 | 5 | 0 | 12 |
| forward | 256 corrections | 10 | 20 | 18 | 8 | 0 | 10 |
| forward | 128 corrections +128 replay | 12 | 36 | 48 | 19 | 0 | 0 |

| Context reference | Old/current route /48 | New-channel route /48 | Full calls /96 |
|---|---:|---:|---:|
| base | 24 | 24 | 0 |
| explicit-original | 42 | 27 | 38 |
| explicit-revised | 36 | 39 | 50 |
| rule-original | 48 | 48 | 86 |
| rule-revised | 48 | 48 | 81 |
