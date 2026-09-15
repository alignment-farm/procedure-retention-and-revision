# Development decision, 15 September 2026

The complete seed401 crossing (source a31fde0, 490.90 active seconds) reproduces
both starting states, all published diagonal responses, and both diagonal adapter
files exactly. No discrepancy repair or alternative crossing was attempted.

| History / current support | Complete | Earlier waiver | Newest waiver |
|---|---:|---:|---:|
| Novel / Novel | 192/192 | 24/24 | 24/24 |
| Novel / Bridged | 122/192 | 0/24 | 24/24 |
| Bridged / Novel | 120/192 | 0/24 | 24/24 |
| Bridged / Bridged | 120/192 | 0/24 | 24/24 |

Both starts complete192/192. Current Novel support improves complete success by
70 orders under Novel history and zero under Bridged history: interaction70/192.
Common Novel support separates the starts by72 orders; common Bridged support
separates them by2. Neither an inherited-state-only nor support-only account
explains this table. The failing cells also wrongly waive certification outside
the two corrected scopes (46 or48 orders); the loss is not only stale earlier
waivers. All newest-waiver obligations succeed, so ineffective new learning is
not the explanation. These are endpoint behavior facts, not an internal mechanism.

Selected fresh test: two new acquisitions501/502, both revision-1 histories, full
crossings; directional interaction expectation fixed in protocol/state-support-final-v1.md
at795b649 before fresh acquisition. No intervention, update-order change, extra
seed selection or predictive margin monitor. New tickets alone would not test
new acquired-state susceptibility. Retain incomplete starting states and all
readiness failures; do not use final results to select revisions or histories.
