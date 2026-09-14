# Sources and adaptation scope

Read 14 September 2026. Versioned HTML is cached and hashed in retrieval.json;
single-client HTTP retrieval uses a descriptive User-Agent and three-second
spacing. No arXiv API/OAI calls. SEAL HTML reused from experience-selection cache
without modifying that study. Code revisions and exact retrieved file paths are
in code-revisions.json; tree inventories and inspected source files are under
upstream/. Author code is read for comparison, not imported by this experiment.

- [WISE 2405.14768v3](https://arxiv.org/html/2405.14768v3), §2.3 and §3: copied FFN side memory, activation-margin routing and sharding/merging address reliability, generalization and locality. EasyEdit WISE.py edit, masked gradient and activation-loss paths inspected. Our plain LoRA replay has no learned memory router, sharding or WISE loss; not a reproduction.
- [MQuAKE 2305.14795v3](https://arxiv.org/html/2305.14795v3), §3–4 and Appendix B: edited-fact recall is distinct from multi-hop consequences; revised 3k data remove conflicting edits. README and MeLLo notebook inspected (decomposition, retrieval and answer revision). Our context list resolves superseded labels explicitly, but performs neither MeLLo retrieval nor multi-hop reasoning. Emitting the correct tool call is our complete task, not evidence of multi-hop propagation.
- [SEAL 2506.10943v2](https://arxiv.org/html/2506.10943v2), §3 and §5/Figure 6: learns self-edit generation through post-update reward; sequential passages expose forgetting. SFT training and few-shot evaluation sources inspected. We use checked labels and fixed optimizers, no self-edit generator or outer RL loop.
- [LOKI 2606.19679v1](https://arxiv.org/html/2606.19679v1), method and experiments: uses weight-derived null-space constraints and adaptive layer selection to limit interference. Author loki_main.py insertion, key caching and projection paths inspected. No LOKI projection or layer-selection algorithm is implemented here.

The empirical method adapts procedure-transfer runtime.py and the task schema
from publication dcdc0d6f54dde235549f8abfba407598b6635667. CE-128 and forward-128
adapters are copied from evidence c183674bcecf9346d84e233aa5c084b1a9acb3ac.
They were selected in that diagnosis as earliest checkpoints reaching >=15/16
whole-call recall. The five original acquisition matrix attempts are CE at
0.0005, reverse KL at 0.0005 and 0.00005, forward KL at the same rates; only CE
and forward-high meet that selection rule. We are explicitly studying these
acquired states, not estimating the chance that arbitrary updates acquire a
procedure. All local new-learning and correction attempts will be reported.

Runtime transitively adapts procedure-acquisition-and-reuse 08d8ec1b0b757e8a537a14d708bd895e8829ac68.
Model Qwen/Qwen3-4B-Instruct-2507 cdbee75f17c01a7cc42f958dc650907174af0554;
MLX-LM 86b48c461feebf87c58788655b7e57b5574b9e6d. uv.lock pins native packages.
Model symlink is read-only use; the copied hash manifest is verified at run start.
This is a bounded conditional-routing adaptation with substantial prior overlap,
not a new general editing method or an independently replicated acquisition study.

The four author-code pins are retrieval-time HEADs, not asserted to be the
releases used in the versioned papers. In particular, the inspected LOKI path
also caches edited-request keys; its memory-free motivation concerns avoiding
an external past-knowledge corpus/feature preprocessing, not zero stored state.
This study makes no reproduced author-method performance claim.
