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

Final-v1 (source9747992) completed in1754.56 seconds with no resource waits;
peak MLX allocation9,620,274,204 bytes. The118 process-monitor samples contain
no other study's Python experimental process. This observational check is not
an exclusive hardware reservation and does not monitor every possible service.
The separate final reload audit took16.32 seconds after model initialization;
its48 generations are verification, excluded from main accuracy denominators.

Follow-up, 14 September 2026: the scope/rehearsal comparison is preparing
896 correction updates and 612 development generations, then two independent
128-update acquisitions with 32-update later learning. Expected allocation is
under 12 GB. Observed experience-selection followup_experiment.py PID6815;
this runner yields before model load and checks all visible sibling scripts
using Python every five seconds. No cross-session messaging facility is exposed.
Coordination remains passive and timers are not isolated performance benchmarks.
Final scope will be fixed from development and sized below one active hour.
Wait ceiling is two hours (development protocol's active limit is unchanged).

Follow-up completion: scope-final-v1 (692f592) ran2,401.42 seconds with no observed
competing Python jobs or waits, peak9,615,195,164 MLX bytes. Across the five new
experimental runs, active time is3,364.25 seconds plus1,245.71 seconds explicitly
waiting for shared hardware. Independent acquisition and its repair had no waits.
The first development reload auditor yielded after a sibling run began; its
unseparated wait remains in that audit's own timer and is not included in the
experimental active-time total. All other final audit jobs ran sequentially.
These are observational measurements, not an exclusive reservation or isolated
performance benchmark. No model download, paid experimental call, or supporting
service installation was needed. Current hardware was rechecked in
scope-hardware.json. All work and records remain in this study.

Maintenance phase, 15 September 2026: preparing work-order development, one
256/512/1024-update bounded acquisition ladder and paired 192-update corrections
per revision. Native host verified mac.lan; no competing Python script visible
at preparation. Expected <12 GB, hard 40 GB, one active hour per run. No external
messaging channel is exposed; use the existing observational yielding protocol.

Maintenance development completed: 1,148.25 s wall time, including 60.02 s shared
resource wait; peak MLX allocation 9,614,539,804 bytes. Routing calibration was
16/16 full calls. The diagnostic queued after completion. Its initial process check was empty;
PID5235 began during model initialization. At 13.96 seconds the diagnostic
paused before its first generation, with model weights resident. This corrects
the initial progress-update assumption that it had yielded before loading.
Initialization briefly overlapped experience-selection PID5235; neither
diagnostic training nor generation had started. The sibling note advertises a bounded
1,152-update development job after our PID4678 exited. No sibling files changed.
Planned negative-boundary diagnostic: 384 updates and 480 generations, expected
about four active minutes. This one additional diagnostic is justified by scoped
corrections transferring while inducing off-scope eligibility and shipment errors;
it changes boundary-example allocation at fixed update count, not model size.
The eventual two-seed fresh comparison is sized at roughly 30 active minutes,
with the same model/allocation limits and no concurrent local model job.

The boundary diagnostic completed at 674.89 s wall / 440.40 s waiting, peak
9,614,851,100 MLX bytes; both corrected endpoints are160/160 complete. The fresh
comparison at0c4c819 queued behind experience-selection PID5491, which had already
started its three-site development-v3 sequence. Its initial check found that job,
so final model loading has not started during this wait. Fresh runtime budget is
now about22 active minutes after retaining full primary evaluations but reducing
redundant repeated queries. This is the study's last planned experimental model
run, followed by saved-state/token audits; no correction search uses fresh results.
