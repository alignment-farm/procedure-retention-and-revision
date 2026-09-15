# Scope follow-up counts

Route recognizes an anchored tool name independently of argument syntax. Full requires the exact complete call.

| State | C recall route/full /4 | Boundary route /7 | Scope route/full | Other old route | Later route | All full | Unchanged full lost/gained |
|---|---:|---:|---:|---:|---:|---:|---:|
| ce-before | 0/0 | 7 | 0/0 /12 | 36/36 | 42/48 | 37/96 | —/— |
| ce-only-128 | 4/4 | 4 | 12/4 /12 | 24/36 | 24/48 | 14/96 | 29/2 |
| ce-triple-128 | 4/4 | 4 | 12/5 /12 | 24/36 | 24/48 | 13/96 | 33/4 |
| ce-boundary-repeat-32 | 3/3 | 7 | 12/4 /12 | 24/36 | 48/48 | 31/96 | 19/9 |
| ce-boundary-repeat-128 | 4/4 | 7 | 12/4 /12 | 29/36 | 48/48 | 27/96 | 19/5 |
| ce-boundary-history-32 | 0/0 | 5 | 0/0 /12 | 36/36 | 46/48 | 43/96 | 8/14 |
| ce-boundary-history-128 | 4/4 | 7 | 11/4 /12 | 36/36 | 47/48 | 46/96 | 15/20 |
| forward-before | 0/0 | 7 | 0/0 /12 | 36/36 | 48/48 | 41/96 | —/— |
| forward-only-128 | 4/4 | 4 | 12/2 /12 | 24/36 | 24/48 | 7/96 | 36/0 |
| forward-triple-128 | 4/4 | 4 | 12/2 /12 | 24/36 | 24/48 | 12/96 | 34/3 |
| forward-boundary-repeat-32 | 0/0 | 3 | 0/0 /12 | 16/36 | 25/48 | 1/96 | 41/1 |
| forward-boundary-repeat-128 | 4/4 | 7 | 12/0 /12 | 36/36 | 48/48 | 14/96 | 33/6 |
| forward-boundary-history-32 | 4/4 | 7 | 12/3 /12 | 36/36 | 48/48 | 22/96 | 32/10 |
| forward-boundary-history-128 | 4/4 | 7 | 12/8 /12 | 36/36 | 46/48 | 57/96 | 7/15 |
| seed101-before | 0/0 | 7 | 0/0 /12 | 36/36 | 48/48 | 13/96 | —/— |
| seed101-only-128 | 4/4 | 4 | 12/3 /12 | 24/36 | 24/48 | 11/96 | 13/8 |
| seed101-triple-128 | 4/4 | 4 | 12/0 /12 | 24/36 | 24/48 | 1/96 | 13/1 |
| seed101-boundary-repeat-32 | 0/0 | 3 | 0/0 /12 | 12/36 | 27/48 | 14/96 | 11/12 |
| seed101-boundary-repeat-128 | 4/4 | 7 | 12/4 /12 | 36/36 | 48/48 | 35/96 | 8/26 |
| seed101-boundary-history-32 | 4/4 | 6 | 12/9 /12 | 25/36 | 48/48 | 67/96 | 6/51 |
| seed101-boundary-history-128 | 4/4 | 7 | 12/9 /12 | 36/36 | 48/48 | 74/96 | 5/57 |
| seed202-before | 0/0 | 7 | 0/0 /12 | 36/36 | 48/48 | 37/96 | —/— |
| seed202-only-128 | 4/4 | 4 | 12/2 /12 | 24/36 | 24/48 | 6/96 | 35/2 |
| seed202-triple-128 | 4/4 | 4 | 12/0 /12 | 24/36 | 24/48 | 1/96 | 36/0 |
| seed202-boundary-repeat-32 | 4/4 | 6 | 10/3 /12 | 33/36 | 45/48 | 27/96 | 15/2 |
| seed202-boundary-repeat-128 | 4/4 | 7 | 12/4 /12 | 33/36 | 48/48 | 30/96 | 17/6 |
| seed202-boundary-history-32 | 0/0 | 5 | 0/0 /12 | 36/36 | 24/48 | 3/96 | 34/0 |
| seed202-boundary-history-128 | 4/4 | 7 | 12/2 /12 | 36/36 | 48/48 | 23/96 | 24/8 |
