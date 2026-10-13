# CFG679D: does the KiDS early-type inner shortfall replicate in DES Y3? IN PROGRESS, no verdict

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (db10b5368), before any DES lensing number and before the KiDS twin.
- **Lane id:** CFG679D. CFG679 is another chat's mechanism contract, and block 670–679 is used up.
- **Download:** approved by the owner 2026-10-12. Data live only under `_external_data/cfg679_des/` (gitignored), with a SHA-256
  logged per piece.

## Status 2026-10-13
| part | state |
|---|---|
| probe (`PROBE.md`) | done; the server is the bottleneck (0.08–0.6 MB/s, stalls > 10 min) |
| stellar-mass lens catalogue (ra, dec, z, mstar) | COMPLETE, 1.141 GB, 36/36 slices |
| metacal sources (ra, dec, e_1, e_2, weight; ~16 GB) | downloading unattended (`--light-guard`: pauses only below 8 GB free+inactive) |
| GOLD g, r, i; index select_bin lists | not yet fetched; GOLD column names still to be read |
| KiDS twin, main + MUTATE (`run_chain.sh`) | queued; the memory guard holds it while a ≥ 20 GB PM run is live |
| DES measurement `cfg679_des.py` | not written yet; it is written against the frozen criteria once the inputs are on disk |

Scripts: `cfg679_lib.py` (memory guard, range reads), `cfg679_probe.py`, `cfg679_download.py`, `cfg679_common.py` (E = 0 ε estimator),
`cfg679_kids_twin.py`.

κ = ½ fitted; the footings are never pooled; the cold energy's mass is still required; not theory closed.
