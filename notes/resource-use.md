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
