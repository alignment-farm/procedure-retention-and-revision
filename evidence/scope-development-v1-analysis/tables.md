# Scope follow-up counts

Route recognizes an anchored tool name independently of argument syntax. Full requires the exact complete call.

| State | C recall route/full /4 | Boundary route /7 | Scope route/full | Other old route | Later route | All full | Unchanged full lost/gained |
|---|---:|---:|---:|---:|---:|---:|---:|
| ce-before | 0/0 | 7 | 0/0 /4 | 12/12 | 16/16 | 21/32 | —/— |
| ce-only-32 | 4/4 | 4 | 4/3 /4 | 8/12 | 8/16 | 14/32 | 10/0 |
| ce-only-128 | 4/4 | 4 | 4/3 /4 | 8/12 | 8/16 | 13/32 | 11/0 |
| ce-repeat-32 | 4/4 | 4 | 4/0 /4 | 8/12 | 8/16 | 2/32 | 19/0 |
| ce-repeat-128 | 4/4 | 4 | 4/1 /4 | 8/12 | 8/16 | 3/32 | 19/0 |
| ce-narrow-32 | 4/4 | 7 | 4/1 /4 | 9/12 | 16/16 | 7/32 | 15/0 |
| ce-narrow-128 | 4/4 | 7 | 4/2 /4 | 8/12 | 16/16 | 12/32 | 11/0 |
| ce-broad-32 | 0/0 | 7 | 0/0 /4 | 12/12 | 16/16 | 26/32 | 2/7 |
| ce-broad-128 | 4/4 | 7 | 4/3 /4 | 11/12 | 16/16 | 21/32 | 8/5 |
