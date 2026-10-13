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
| metacal sources (ra, dec, e_1, e_2, weight; ~16 GB) | downloading unattended via `run_download.sh`, which restarts after server timeouts (resumable, chunk map cached); `--light-guard` pauses only below 8 GB free+inactive |
| GOLD g, r, i; index select_bin lists | not yet fetched; GOLD column names still to be read |
| KiDS twin, main + MUTATE | **DONE** (below); control K-T1 PASS (max relative deviation 0.0 against CFG503's committed table) |
| DES measurement `cfg679_des.py` | not written yet; it is written against the frozen criteria once the inputs are on disk |

Scripts: `cfg679_lib.py` (memory guard, range reads), `cfg679_probe.py`, `cfg679_download.py`, `cfg679_common.py` (E = 0 ε estimator),
`cfg679_kids_twin.py`.

κ = ½ fitted; the footings are never pooled; the cold energy's mass is still required; not theory closed.

## KiDS twin (the comparator; E = 0, framework-native), from `cfg679_kids_twin_results.json`
Values are ε ± σ, canonical / alt.

| sample | K-in (primary) | K9 |
|---|---|---|
| f30 early | **+0.567 ± 0.191 / +0.437 ± 0.175** | +0.919 ± 0.123 / +0.755 ± 0.113 |
| f30 late | +0.015 ± 0.259 / −0.069 ± 0.237 | −0.103 ± 0.117 / −0.180 ± 0.107 |
| f30 all | +0.373 ± 0.155 / +0.259 ± 0.142 | +0.536 ± 0.089 / +0.403 ± 0.081 |
| f30 early, z > 0.2 (DES range) | +0.611 ± 0.198 / +0.478 ± 0.182 | +0.970 ± 0.126 / +0.802 ± 0.115 |

- **Agreement with CFG531.** Twin early K-in canonical is +0.567 ± 0.191, against CFG531's +0.538 ± 0.193 with the ΛCDM-built E.
  Dropping E moves the inner band little.
- **Outer bands.** K-mid, K-out and K9 rise without E, as expected: the twin's own profile has no environment term, so any
  neighbour mass shows up as ε there. That is why K-in is the primary band.
- **MUTATE.**
  - Per-lens random shear sign: ε ≈ −1 in every band and sample (early K-in −0.887 ± 0.164 / −0.897 ± 0.150).
  - Newtonian own profile: early K-in +7.5, K9 +10.0. Mass beyond the baryons is detected, so the tooth bites.
  - The MUTATE K-mid values (−1.25 to −1.33) sit about 2σ below −1. They are reported, not hidden.

## Disclosed code fixes after the freeze (no criteria change; made before any DES number)
1. **`cfg679_common.stack`.** Groups holding no lens of the sample carry NaN tables, and 0 × NaN made every ε NaN on the
   first run. The fix sums over groups with weight > 0.
2. **`cfg679_kids_twin.py` K-T1.** The table key lacked CFG503's `P|` prefix, so the control could not compare and reported
   FAIL. After the fix: PASS, deviation 0.0.
3. **`cfg679_download.py`.** A DES server read timeout during chunk-index lookup killed the run. The chunk map is now cached in
   `pieces.json`, and `run_download.sh` restarts the job; finished pieces are skipped.
