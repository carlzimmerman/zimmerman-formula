# NV2_external_field_xcop_lenses: E1 is now computable for X-COP, but no residual row can be graded with it. The isolated-lens rebuild FAILED, KiDS-bright E1 is noise-dominated, and the L3+E1 fit is inadmissible and breaks gate 3

Criteria `FROZEN_CRITERIA.md` (762bd78121), committed alone before the download. Amendments, each committed alone:
- `AMENDMENT_A1.md` (edf79eadcf): after the download and control 3's first run, before any E1 value. The record's E1 csv was built in 2M++ mode `ks115`, not `full`.
- `AMENDMENT_A2.md` (275c4c46b0): post-result disclosures, before any fit.

Scripts:
- `nv2_download.py`: the one approved download.
- `nv2_e1.py`: the E1 estimator and controls 3-4, and Step 0.
- `nv2_env.py`: E1 per system for NV1's machinery.
- `nv2_core.py`, `nv2_cand.py`, `nv2_stage3.py`, `nv2.py`: NV1's scripts copied with attribution; E1 only.

Run with `PYTHONHASHSEED=0 nice -n 10 python3 -I <script> <mode>`, one thread. The peak physical footprint was 0.70 GB (Step 0). Downloaded data are not committed. Caches, per-lens arrays and logs are gitignored.

**Not blind** (see the criteria). κ = ½ FITTED. The cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. A pass is a description of data, not a theory.

## Download (owner-approved, the only one)
- **What:** 2MPZ (Bilicki+14), SuperCOSMOS Science Archive, `TWOMPZ..twompzPhotoz`, freeform SQL, CSV. Columns `twomassID, ra, dec, kCorr, zPhoto, zSpec`.
- **Cones:** 12, one per X-COP cluster, radius 1.2 × asin(30 Mpc / D_c), from 5.70° (A2142) to 10.78° (A1644).
- **Size:** COUNT first, 70,879 rows and an estimated 5.0 MB. Downloaded: **70,879 rows (69,026 unique), 7.09 MB**, into `_external_data/nv2_2mpz_cones_2026-11-04/`.
- **Record:** the queries, timestamps, per-cone rows and sha256 are in `nv2_download.json`.
- **Archive behaviour:** no login or CAPTCHA was asked. The archive cancelled some queries. The script retried them and resumed after the first run stopped (A2).

## E1 (the record's Chae-2021 sum, truncated at 30 Mpc for every system)
- **Control 3, estimator known answers: all pass.** Point mass to 1e-16; a uniform field to 0.16 %; the antipodal shell to 2e-14; the truncation edge. The record's `gext_vectors.csv` is reproduced to 5e-6 dex on all 175 galaxies, in mode `ks115` (A1).
- **SPARC (2M++):** median E1 −3.02, 16-84 % range [−3.60, −2.79], σ_E1 0.45 (the noclu-maxclu bracket). Against the record's full-sky E1: Spearman 0.94, median offset −0.07 dex. Depth (`full` − `ks115`) moves it by 1e-4 dex.
- **Control 4, photo-z fidelity (as frozen):**
  - **KiDS-bright:** Spearman 0.386. **NOISE-DOMINATED**, so KiDS lens E1 is NOT COMPUTABLE.
  - **2MPZ:** 0.998, usable.
  - **Caveat (A2):** the frozen 2MPZ model barely perturbs its test sources (Ks ≤ 11.5, 99 % spectroscopic). With every source perturbed, Spearman is 0.425 (reported, not gated).

**X-COP E1 (2MPZ + MCXC, 200 photo-z draws, coverage 1.00 everywhere).** Train clusters are marked T.

| Cluster | E1 | σ_E1 | of which MC |
|---|---|---|---|
| A1795 T | −2.83 | 0.48 | 0.006 |
| A2142 T | −2.96 | 0.51 | 0.006 |
| A644 T | −3.87 | 0.60 | 0.090 |
| ZW1215 T | −2.99 | 0.50 | 0.002 |
| A2029 | −2.95 | 0.54 | 0.004 |
| A2319 | −3.61 | 0.48 | 0.055 |
| A85 | −3.71 | 0.53 | 0.015 |
| A1644 | −2.86 | 0.46 | 0.004 |
| A2255 | −3.57 | 0.62 | 0.026 |
| A3158 | −2.92 | 0.48 | 0.009 |
| A3266 | −4.04 | 0.53 | 0.111 |
| RXC1825 | −3.58 | 0.55 | 0.064 |

- Members within 2 R500 at a consistent redshift, and each cluster's own MCXC entry, are excluded as "self".
- **σ is dominated by the noclu-maxclu bracket,** not by photo-z noise.

## Step 0: rebuilding Brouwer+21's isolated lenses FAILED
- **Criterion, as published:** no neighbour with M★ > 0.1 M★,lens within a 3D 3 h70⁻¹ Mpc built from photo-z distances; 0.1 < z < 0.5; M★ < 10¹¹.
- **Result:** **486,584 isolated, 62.9 % of 773,192 candidates,** against B21's 259,383 ± 5 %. B21 publishes no per-bin counts. NV2 finds 164,363 / 105,896 / 105,303 / 110,899 per bin.
- **Lenses are graded NOT COMPUTABLE,** and that holds twice over, given control 4.
- **First run had a bug** (99.5 % isolated). It is disclosed and fixed (A2).
- **The record's count-calibrated rebuild** (181,477 lenses, a |Δχ| < 10 Mpc window) was not used. It is a calibration, not B21's criterion.
- **Lens E1, UNGRADED** (5000 lenses per bin, coverage ≥ 0.8, lens-weighted):

| Bin | E1 | sd | per-lens σ |
|---|---|---|---|
| 1 | −4.31 | 0.15 | 0.51 |
| 2 | −4.28 | 0.14 | 0.52 |
| 3 | −4.26 | 0.14 | 0.53 |
| 4 | −4.26 | 0.14 | 0.55 |

## Sign test (NV1's, unchanged): NOT COMPUTABLE on both footings
- **Train trend:** with E1 on all 79 train systems, ρ = −0.24, p = 0.040 (canonical), and −0.27, p = 0.016 (alt). Systems with a stronger external field sit below NP2's rule.
- **No target group has E1.** IC 1613 has no SPARC alias, the Local Group dwarfs and ultra-faints have no estimator, and the lens bins are not computable. T30's "want" was 0 in any case.

## Controls before the fit (`nv2_controls.out`): all frozen ones pass on both footings
| Control | Result |
|---|---|
| Known answer | X-COP +0.4675, LT −0.0252 |
| Zero-weight E1 rule | U: 5 computed rows match RQ3's law card. S: 7 rows match the plain law on S. 0 mismatches |
| Checker | flags the bump (2572 violations); zero rule clean |
| Admissible plant | converged, clean, G3 SPARC 0.123 / 0.195, G4 −0.003 |
| Planted boost 0.15 z_E | true E1: dm/dE 0.363 against 0.362 planted, gates 3-4 pass. Shuffled E1: G3 and G4 fail, SPARC-even rms 0.196 against 0.125 |

- The printed "FAILED" comes from the reverse S check, as in NV1 A2 (not gated; the flag is recomputed as frozen).

## Real fit, L3+E1, mode F (`nv2_real.out`)
| | Canonical | Alt |
|---|---|---|
| λ | 2 | 2 |
| ML length of E1 (standardised) | **0.02** | **0.02** |
| Checker | **24 violations, INADMISSIBLE** (13 SPARC-even rows non-monotone end to end) | **25, INADMISSIBLE** (14) |
| G1 X-COP train | +0.000 / 0.001 P | +0.000 / 0.001 P |
| G2 SPARC train | 0.024 / 0.175 P | 0.024 / 0.177 P |
| **G3 SPARC even** | **0.251 / 0.195 F** | **0.254 / 0.196 F** |
| **G3 X-COP unseen** | **+0.420 / 0.453 F** | **+0.397 / 0.431 F** |
| G4 LT (8 galaxies with E1) | −0.095 P | −0.098 P |
| G5 on U | not passed (A1-A3 NOT COMPUTABLE) | same |
| Mean ∂m/∂E1 | −6.4 | −6.4 |
| E1-shuffle MUTATE | G3 S 0.260 F, X +0.342 F | G3 S 0.260 F, X +0.323 F, G4 −0.100 F |
| RQ3 U card | B23 PASS, B25 PASS, **B24 FAIL** (passes under NP2) | same |

**What the fit does.** As with NV1's E2, the ML length of 0.02 makes E1 a per-system label. The rule fits train exactly (G1 rms 0.001, G2 0.024), then misses unseen SPARC galaxies and the unseen clusters (X-COP holdout +0.42). It also turns non-monotone.

**Target rows, before (NP2 L3 F) → after (NV2).** Every target row is NOT COMPUTABLE for E1, on both footings and both cards:
- **A10, A12, A13:** no E1 in the Local Group.
- **A30:** lenses NOT COMPUTABLE.
- **A5-A7:** on U, the SPARC block needs every LITTLE THINGS galaxy, and only 8 of 20 have E1. On the frozen S card, RQ3's SPARC block raises an IndexError once IC 1613 is dropped. The plain law and NP2 on the same S card fail the same way, so this is a property of the S card here, not of the rule.
- **Empty dwarf list on S:** S-card A12 and A13 print FAIL with Z = NaN for every rule, because no dwarf has E1. These are read as not computable and no move is counted.

No row moves, so there is no PARTIAL.

## Verdict (frozen labels, per footing)
- **E1 (L3+E1): UNDETERMINED (INADMISSIBLE)** on both footings. It also fails gate 3 on SPARC and X-COP, and gate 5 is not computable.
- **Lane: NO SINGLE NON-LOCAL VARIABLE ON RECORD RESOLVES** on canonical and alt. There are no PARTIAL movers.
- **Sign test: NOT COMPUTABLE.**
- **Lenses: NOT COMPUTABLE.** Step 0 FAILED and KiDS E1 is noise-dominated.
- **What does change:** X-COP E1 is now on record, and the train trend (ρ ≈ −0.25) has the sign an external-field effect would give. No residual row can test it, because the rows that want less gravity (IC 1613) and more (dwarfs, lensing) still have no E1.

## Departures, all disclosed
1. **A1:** the record mode is `ks115`, not `full`.
2. **A2 (download):** the dec band and the retries.
3. **A2 (Step 0):** the index bug in the first run, fixed.
4. **A2 (control 4):** the frozen 2MPZ fidelity model is weak. Its worst case (0.425) is reported, not gated.
5. **A2 (X-COP self exclusion):** it uses the observed redshift.
6. **Code fixes after crashes, no number changed:**
   - NP2's checker crashed on an empty CX1 set (no CX1 row has E1); the set is now skipped.
   - The labeller's card key was left as `NV1_` by the copy; the first `real` run crashed before labelling, and the rerun reproduced every fit number.
7. **M★ for KiDS = MASS_BEST + 0.15 + 0.056 dex** (fluxscale stand-in plus B21's GAMA normalisation). MAG_GAAP_r is not on disk. As frozen.
8. **E1 differs by catalogue** (2M++, 2MPZ, KiDS: depth and mass estimator). This is uncalibrated, as frozen.
9. **RQ3 support files** are byte-identical copies.

κ = ½ FITTED. Not theory closed.
