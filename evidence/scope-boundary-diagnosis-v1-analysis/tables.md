# Scope follow-up counts

Route recognizes an anchored tool name independently of argument syntax. Full requires the exact complete call.

| State | C recall route/full /4 | Boundary route /7 | Scope route/full | Other old route | Later route | All full | Unchanged full lost/gained |
|---|---:|---:|---:|---:|---:|---:|---:|
| ce-before | 0/0 | 7 | 0/0 /4 | 12/12 | 16/16 | 21/32 | —/— |
| ce-boundary-repeat-32 | 3/3 | 7 | 3/3 /4 | 8/12 | 16/16 | 21/32 | 3/0 |
| ce-boundary-repeat-128 | 4/4 | 7 | 4/3 /4 | 9/12 | 16/16 | 21/32 | 3/0 |
| ce-boundary-history-32 | 0/0 | 5 | 0/0 /4 | 12/12 | 14/16 | 13/32 | 8/0 |
| ce-boundary-history-128 | 4/4 | 7 | 4/3 /4 | 12/12 | 16/16 | 24/32 | 0/0 |
