# Scope/rehearsal follow-up reproduction

The accepted run and FINDINGS.md are preserved. This follow-up uses the same
locked environment, model revision, source manifests, and native MLX gradients.
See the original [reproduction instructions](reproduction.md) for model setup.
No inference service is used as a training API. All commands run from this study.

```sh
uv sync --python 3.14.7 --extra adaptation --frozen
uv run --no-sync python -m unittest discover -s tests -v
uv run --no-sync python scripts/scope_experiment.py --output evidence/NEW-SCOPE-DEV
uv run --no-sync python scripts/scope_analyze.py evidence/NEW-SCOPE-DEV
uv run --no-sync python scripts/scope_audit.py evidence/NEW-SCOPE-DEV
uv run --no-sync python scripts/scope_experiment.py --phase acquisition --output evidence/NEW-SCOPE-ACQUISITION
uv run --no-sync python scripts/scope_analyze.py evidence/NEW-SCOPE-ACQUISITION
uv run --no-sync python scripts/scope_audit.py evidence/NEW-SCOPE-ACQUISITION
```

Run each hardware command sequentially. Runner resource checks recognize sibling
Python scripts and yield before loading a model; timing is observational, not
an exclusive reservation. Analyzer needs no model. Audit loads the model and
checks three saved responses per checkpoint across a process boundary. Audit
repetitions do not enter the accuracy denominators.

The runner writes a new directory only, snapshots executable sources and the
applicable prospective protocol, records Git revision, verifies model hashes,
logs each update (source, case, loss, gradient norm, time and token counts), saves
all endpoints and verifies frozen-base and reset invariants. The analyzer
recomputes scores, denominators, condition schedules, common initial states,
paired losses and costs. Raw generations include prompt/completion tokens and
IDs for independent inspection. SHA256SUMS covers all completed run files.

The scope scorer is separate from the accepted scorer. It recognizes only an
initial `kestrel` or `marten` with a word boundary followed by whitespace, `(` or
end of output. A malformed argument can retain an identifiable route; strict
format, strict route, exact identifier, suffix and full call remain separate.
No recognizable initial tool is marked unknown. This convention is fixed before
development and fresh generation, with explicit malformed-output tests.

The narrow archive is seven checked examples (druvan on unchanged old conditions;
fepzan on new conditions). The broad archive contains all 28 valid A/B examples.
Both receive the same condition sequence and the same known obsolescence mask.
Their first seven replay updates are identical. Afterward broad cycles identifiers
within each condition, while narrow repeats its example. The treatment difference
is archive/identifier breadth given complete condition coverage. It cannot
separate boundary evidence from the rehearsal inherent in the narrow examples.
No arm infers archive validity; the investigator excludes the four obsolete
copper/fast records. No rules or checked examples enter generation prompts.

Independent acquisition seeds 101 and 202 reinitialize zero-output LoRA adapters
and vary acquisition data order, using fixed hard-label CE. They do not vary
pretrained base weights or model family, and are not independent tasks. All
attempts and any diagnostic changes must be reported. The two inherited starts
share original seed 41 and remain separately labeled as inherited CE and FK.

## Bounded diagnostic and independent-start repair

The original prospective scope-final-v1 comparison was superseded before any
fresh evaluation: its historical boundary cases did not share correction IDs.
The retained diagnostic instead supplies all unchanged conditions on jebrun,
also a correction identifier. Each arm gets the identical target and boundary
updates; its third update either repeats that boundary case or replays history.

```sh
uv run --no-sync python scripts/scope_experiment.py --anchored --arms boundary-repeat boundary-history --output evidence/NEW-BOUNDARY-DIAGNOSIS
uv run --no-sync python scripts/scope_analyze.py evidence/NEW-BOUNDARY-DIAGNOSIS
uv run --no-sync python scripts/scope_audit.py evidence/NEW-BOUNDARY-DIAGNOSIS
uv run --no-sync python scripts/scope_experiment.py --phase acquisition --seeds 202 --later-blocks 128 --later-replay --reuse-acquisition evidence/NEW-SCOPE-ACQUISITION --output evidence/NEW-ACQUISITION-REPAIR
uv run --no-sync python scripts/scope_analyze.py evidence/NEW-ACQUISITION-REPAIR
uv run --no-sync python scripts/scope_audit.py evidence/NEW-ACQUISITION-REPAIR
```

Seed202's initial B32 failure is preserved, not overwritten. The repair restores
its functioning A128 checkpoint and checks both B32-replay and B128-replay.
Repeated A recall during repair is verification of reused weights, not a new
independent acquisition. Selection concerns training routes; complete calls
are disclosed separately. Final starts are pinned in a local path manifest,
which is copied to the run. Every referenced checkpoint directory is hash-checked.

The first development reload audit was launched from a129b16 before audit code
was strengthened during its resource wait. Its exact executed source is archived
with execution-provenance.json; the audit's disk-at-completion hash is explicitly
distinguished from its loaded source. It checks612 response token records and27
reload probes. Later audits also verify every recorded training-token count.
A CPU-only regression of the strengthened analyzer atd85418c reproduced all
initial development/acquisition summaries, paired counts and costs exactly.

## Frozen fresh comparison

Execution revision: **692f592**. The actual selection uses seed101 B32-only and
seed202 B128-replay, after the latter failed both initial B32-only and repair
B32-replay. All source files/checkpoints are committed. To reproduce the final
comparison directly from these fixed carried states:

```sh
uv run --no-sync python scripts/scope_experiment.py --phase final --anchored --starts ce forward seed101 seed202 --blocks 128 --start-manifest notes/scope-starts.json --output evidence/NEW-SCOPE-FINAL
uv run --no-sync python scripts/scope_analyze.py evidence/NEW-SCOPE-FINAL
uv run --no-sync python scripts/scope_report.py evidence/NEW-SCOPE-FINAL
uv run --no-sync python scripts/scope_audit.py evidence/NEW-SCOPE-FINAL
```

Check out the recorded execution revision for exact historical reproduction.
To use newly reproduced acquisitions instead of the committed carried states,
write a new four-entry path manifest matching scope-starts.json and pass that
file; preserve the same prospectively selected endpoints. No original evidence
folder is overwritten. The final has3,892 generations and5,120 updates across
28 states. The 32-block boundary checkpoints are additional reported budget
controls;128 remains the primary endpoint for every start, without fresh-based
selection. The current scorer separately identifies the four familiar original
A scope cases so their stale responses are not hidden by new-string transfer.

## Completed audits and cost ledger

Fresh execution completed all28 states,3,892 generations and5,120 updates.
Its analyzer checks every score, denominator, scheduled example, checkpoint hash,
common start and frozen-base/reset invariant. Across all five follow-up runs,
separate-process audits decode5,131 token records and reproduce147 checkpoint
probes exactly. They also match216 existing recall records at reused starts.
The CPU instrument audit verifies the first development run's896 training-token
counts, completing verification of all7,360 follow-up updates' token counts.

Regenerate the aggregate ledger and completion-limit analysis with new outputs:

```sh
uv run --no-sync python scripts/scope_costs.py --output evidence/NEW-SCOPE-COSTS.json
uv run --no-sync python scripts/scope_instrument_audit.py --output evidence/NEW-SCOPE-INSTRUMENT-AUDIT.json
```

These two commands aggregate the committed run names, including every failed
learning endpoint. They do not launch a model or alter experimental evidence.
The instrument audit uses the tokenizer only. Its first implementation compared
a Transformers BatchEncoding object to a token list; the explicit return_dict=false
repair matches MLX's wrapper and all612 recorded development prefixes. The
failed checker and repair are documented in scope-audit-repair.json. No training,
scoring rule, generation budget or empirical result changed.

The longest canonical answer needs13 tokens. There were62 final generations at
the48-token limit; every one was already a divergent, incorrect call prefix.
More appended tokens could not make that recorded prefix an exact answer.
Five outputs have no recognizable initial tool, all at the early failed FK
boundary-repeat checkpoint; they remain unknown errors, not assigned an invented
route. Perfect tool selection can coexist with malformed or repeating arguments.

The first development audit's timer includes a resource wait that it did not
separate. Audit times are not added to the aggregate experimental active-time
claim; verification counts are reported separately. Later audit source files
and execution revisions are captured at launch in their audit directories.
