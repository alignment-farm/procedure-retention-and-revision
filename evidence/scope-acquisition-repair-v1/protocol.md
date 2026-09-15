# Scope evidence versus rehearsal: bounded development

14 September 2026, prospective. Preserve final-v1 and its accepted publication.
Use the owned pinned runtime, model, LoRA and CE optimizer without changes.
This is an ablation of supervised replay, not a reproduction of WISE or SEAL.
Cached primary sources and pinned author code remain in sources/; WISE's
locality/activation and replay losses and SEAL's SFT implementation were
reinspected. No new literature claim or editing algorithm is proposed.

Start from the accepted CE B-replay-128 checkpoint, verifying its manifest.
Every correction arm restores this identical state and resets AdamW.
Four target examples change copper/fast to marten. All seven other conditions
are unchanged. No verbal scope statement or teaching context enters inference.

Arms, at both 32 and 128 target blocks (retain and report every endpoint):

- only: one corrected example per block.
- repeat: that corrected example immediately repeated, matching replay steps.
- narrow: target then one unaffected example; seven unique examples, one per
  unchanged channel/priority condition. Old channels use druvan, new fepzan.
- broad: target then one unaffected example; all 28 valid inherited A/B examples.

Narrow and broad receive EXACTLY the same sequence of channel/priority
conditions. Broad cycles all four identifiers within each condition; narrow
repeats one. Their first seven replay examples are identical. Both receive
the same investigator-known validity filter; four obsolete copper/fast history
examples are removed. Neither learns which records are obsolete. Narrow already
rehearses computation and covers all unchanged conditions. This isolates added
identifier diversity/history coverage beyond that narrow rehearsal, not a pure
scope-information effect independent of rehearsal. only/repeat lack boundary
evidence. Token costs are measured, not assumed equal from equal steps.

Use original four development identifiers (32 crossed inputs) plus A/B/C recall
(36). Score an anchored initial tool token independently of canonical syntax;
ambiguous/no initial tool is unknown, not automatically the other route. Keep
strict route, format, identifier, suffix and full call separately. Count stale
and overbroad tool selections even with malformed arguments. Pair before/after
on the identical 28 unchanged development queries. No real tools execute.

Final budget selection: choose the earliest of 32 and 128 where BOTH narrow
and broad acquire 4/4 correction routes and retain 7/7 narrow boundary routes.
If neither meets this, retain the failure and perform one bounded diagnosis
before final selection. Do not select from fresh outcomes. Final will include
both inherited CE/FK starts and two independently initialized CE acquisitions
(seeds 101, 202), with all acquisition attempts reported. Initially train A for
128 updates and B for 32, reflecting the accepted short-budget finding. Test
>=15/16 A and B recall routes before calling a start functioning. A failed
acquisition warrants bounded training-only diagnosis, not silent exclusion.

Development ceiling: 25 active minutes, 40 GB MLX allocation; final sizing after
measured development. No model download/paid call. Check visible sibling Python
jobs every five seconds and yield on overlap. Record snapshots and wait time;
this is passive coordination, not exclusive reservation or timing isolation.
All updates, generations, executable snapshots, hashes and git revision retained.
