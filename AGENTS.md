# Procedure retention and revision

Read [README.md](README.md) first. This independent ancillary study owns its
methods, protocols, implementation, evidence and local publication. Investigate
retention under later learning and scoped revision of acquired procedural
relations. The parent [study map](../../construct-2/studies/README.md) owns theory
and synthesis, following the
[ancillary-study approach](../../construct-2/notes/ANCILLARY_STUDY.md).

## Research practice

- Develop and execute a bounded empirical comparison using the README's starting
  evidence. Workload discovery and purposeful acquisition diagnosis belong here;
  routine experimental choices do not require further root approval.
- Distinguish acquisition, persistence across a stated boundary, retention under
  intervening learning, scoped correction and new-input transfer. Keep learned
  component behavior separate from complete-task performance and cost claims.
- Check the closest primary methods and implementations. Record exact paper
  versions and code revisions, distinguish reproduction from adaptation, and
  scale novelty claims to the overlap. Follow the root's
  [arXiv guidance](../../construct-2/AGENTS.md#research-sources), including caching,
  a descriptive User-Agent and shared rate limits.
- Preserve failed attempts and consequential design changes. A negative result
  alone is not a stop condition. If acquisition fails, use bounded diagnostics
  to distinguish causes or establish a functioning regime; finite gradients and
  verified writes are not acquisition. Close on explanatory progress, a
  demonstrated limitation or a concrete resource constraint. Neither a neural
  win nor indefinite search is required.
- Use development material for calibration and fresh evaluation for claims
  developed through it. Report all acquisition attempts and selection decisions;
  do not silently restrict retention claims to convenient successful writes.
- Keep records proportional and inspectable. Publish local findings, evidence
  and reproduction instructions with identifiable Git revisions. Acceptance of
  a publication and retirement of a research question are separate decisions.

Reuse pinned sibling code or artifacts with provenance into this study's own
workspace. Do not modify the root or other studies. This investigation does not
depend on future results from concurrent projects; coordinate shared resource
use without creating a central workflow or scheduler.

## Model resources

- Dedicated Mac Studio M1 (64 GB unified memory), serving over Tailscale through
  Docker Model Runner (preferred). Chat-completions endpoint:
  `https://mac-studio-7hr7.taile71f88.ts.net/engines/v1/chat/completions`
- Local open-weight models with `docker model`.
- OpenAI models with `codex`.
- SpaceXAI models with `agent`.

The pinned [diagnosis](../procedure-transfer/DIAGNOSIS.md) records a native MLX
route for teacher distributions and student gradients on the Mac Studio. Verify
the model revision, mutable-state access and resource needs for this study's
chosen method; an inference-serving endpoint is not a gradient API. Preparation
did not test services, install models or execute experiments.

Before heavy shared-hardware runs, coordinate with the other active investigators
so overlapping jobs do not contend for memory or invalidate timing measurements.
Research design and analysis can proceed concurrently. Keep method and resource
sizing local; explain a material expansion beyond the initial bounded study.

## Dependency management

- Use `uv` for Python package and project management.
- Use Docker and Compose/Dockerfiles for supporting resources when needed.
