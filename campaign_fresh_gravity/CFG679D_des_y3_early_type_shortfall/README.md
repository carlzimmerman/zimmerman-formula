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
| GOLD id + g, r, i; index select_bin lists; stellar-mass coadd ids; R11/R22 on 20 chunks; selection-response lists (optional) | not fetched; listed in `GOLD_NEEDED.md`; queued in `run_after_mcal.sh` (started 2026-10-13, waits for `mcal: COMPLETE`, then fetches them one after another with the same restart pattern; it does not run the measurement) |
| KiDS twin, main + MUTATE | **DONE** (below); control K-T1 PASS (max relative deviation 0.0 against CFG503's committed table) |
| DES measurement `cfg679_des.py` | **written and self-tested on synthetic data only** (below). It refuses to measure (exit 3) until every input above is complete. No DES lensing number exists |
| lens side on the real stellar-mass catalogue (`--lens-only`) | done **without the r < 20 cut** (GOLD not on disk), so the counts are provisional (below) |

Scripts: `cfg679_lib.py` (memory guard, range reads), `cfg679_probe.py`, `cfg679_download.py` (+ `cfg679_download_meta.py`: column
listing, index, selection-response modes), `cfg679_common.py` (E = 0 ε estimator), `cfg679_kids_twin.py`, `cfg679_des.py`,
`run_after_mcal.sh`.

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

## `cfg679_des.py` self-test (synthetic data only; `cfg679_des_selftest.out`)
Five independent synthetic realisations, each with ε_true = 0.5 and 0.0. Each realisation has 5,400–5,500 isolated lenses, 3 M
sources plus unsheared cluster members (to test the boost), a fixed e₂ sign convention (s = −1) and shape noise 0.005. The low shape
noise is chosen for power, not realism. Canonical footing injected. The whole pipeline runs: isolation, colour split, matched weights,
<Σcrit⁻¹>, response, randoms + boost, 50 patches, GLS ε, ladder, controls, M1, M2.

| check (canonical) | ε_true 0.5: mean ± SE (5 seeds) | ε_true 0.0 |
|---|---|---|
| early K-in | +0.486 ± 0.087 | −0.011 ± 0.072 |
| early K9 | +0.486 ± 0.034 | −0.001 ± 0.030 |
| all K-in | +0.490 ± 0.084 | −0.020 ± 0.069 |
| all K9 | +0.492 ± 0.015 | +0.000 ± 0.016 |
| M1 rotated K-in / K9 | −1.077 ± 0.070 / −1.036 ± 0.033 | −1.078 ± 0.068 / −1.036 ± 0.034 |

- Sign control picks the injected convention; cross shear |Z| < 3, randoms p > 0.001 and the M2 tooth pass in 10/10 runs.
- The ladder never reads R under rotation.
- **Disclosed:**
  - The per-realisation frozen M1 bar (|ε + 1| ≤ 2σ) is met in 4/5 realisations in each band, not 5/5.
  - Seed-to-seed scatter is 0.7–1.6 × the quoted GLS σ, highest in K-in.
  - The ensemble pass bars were set after five exploratory single-realisation runs.
  - A first version showed a +0.016 K9 bias. It came from randoms placed in the synthetic source margin, where lens discs are
    truncated. The synthetic footprint was fixed; the estimator was not changed.

## Lens side on the real catalogue, provisional (`cfg679_des_lenscounts.out`; no source read)
- **Cuts and counts.** 0.2 < z < 0.5 leaves 18,294,963 of 35,653,240. With log M* < 11.0 there are 17,017,589 lens candidates, of which
  **27,183 are f30-isolated**. The sign-control sample (log M* ≥ 11.2) holds 410,015.
- **These counts are provisional.** Without GOLD magnitudes the r < 20 cut is NOT applied, to the pool or to the lenses. The pool is
  therefore far denser than the frozen r < 20 pool, and the isolated fraction (0.16 %) is far below KiDS's (32 %). The real run recomputes
  everything after the GOLD match.
- **Isolation check.** The KD-tree isolation agrees with a brute-force cylinder test on 600 real lenses (300 isolated, 300 not;
  0 disagreements).
- Counts per (z, log M*) cell are in the JSON.

## Implementation choices not spelled out by the frozen text (disclosed 2026-10-13, before any DES lensing number)
1. **Early/late split.** The split by f_E is applied to the isolated, in-footprint DES lenses (the f30 analogue of the KiDS fraction).
2. **Sign-control radii.** R = 0.3–2 Mpc is physical, as are all KiDS radii. Its lenses use the same z and r cuts, with no isolation.
3. **"No boost; no random subtraction".** Reported as three estimators: no boost (random-subtracted), no random subtraction (boosted),
   and neither (the KiDS-twin-like one).
4. **R_b.** Uses the unweighted mean of (R11 + R22)/2, as written; the weight-averaged value is logged as a diagnostic.
5. **Selection response.** If only global sheared lists exist, one global value is applied to every bin. If no lists are usable, it
   is neglected; both cases are logged.
6. **Randoms.** Each lens is used exactly NRAND = 5 times as a random's parent, in a random order. Random sums are kept per (patch,
   class, cell), which is enough for every weighting in section 5.
7. **C2 gate.** Applied to the early and all samples, with matched weights.
8. **Covariance.** It is checked for finiteness. numpy/Accelerate prints spurious matmul warnings on finite input; they are
   silenced.
9. **Memory guard.** The self-test and `--lens-only` use the light guard (free+inactive ≥ 8 GB), not `cfg679_lib.guard`, which
   blocks while any PM run holds > 20 GB. They held ≤ 3.6 GB RSS in one process while the 1024³ run was live. The real measurement
   calls `cfg679_lib.guard`.
