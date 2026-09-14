# Resource use

2026-09-14: host mac.lan is the 64 GiB M1 Ultra used by sibling studies.
Observed experience-selection development-v1 training PID 4104; deferred all
model loading/training while preparing methods. No other investigator's files
or processes are modified. This study advertises intended use here and rechecks
active Python training before each heavy run, yielding while another is active.
No cross-session messaging facility is available in the exposed tools. This is
passive coordination through visible job activity, not an exclusive reservation;
process snapshots during execution will disclose any overlap and timing limits.
Native MLX runtime and verified cached bf16 Qwen weights reused read-only; model
hashes checked before training. Expected peak <12 GB, hard limit 40 GB.

At 20:43:12 UTC the first development run started after experience-selection's
301-second development run ended. At 20:43:33 experience-selection began its
confirmatory sequence; our 15-second monitor observed overlap at 20:43:44.
Stopped our own PID 4367 with SIGINT once inspected. Partial evidence remains
in evidence/development-v1, status failed; this is a resource interruption,
not a learning-failure endpoint. Initial acquired-state recall was 16/16.
Do not use its time measurements for isolated hardware costs.

The restart waited about 13.5 minutes before model loading while the sibling
completed its three-run sequence. At elapsed 816.93 seconds it verified model
hashes and began the run, with no competing experiment visible. Waiting is
recorded separately from active work; no model weights were loaded during this
initial wait. Source commit for the restart: 22fd99ee76c703f590b934b643056183a5629e6d.
