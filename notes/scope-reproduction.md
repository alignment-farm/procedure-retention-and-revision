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
