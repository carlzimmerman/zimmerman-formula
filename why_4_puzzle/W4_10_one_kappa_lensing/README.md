# W4-10: is there ONE 4? ONE κ FOR LATE TYPES ONLY (as frozen, with B21's Chabrier masses)

**Bottom line.** Fitting κ separately in every KiDS-1000 isolated-lens subsample gives three findings:
- **κ splits by galaxy type, not by mass.**
  - Colour: blue 0.52 vs red 1.29 (p = 8×10⁻⁷).
  - Morphology: Sérsic n < 2 gives 0.57 vs n > 2 at 1.32 (p = 5×10⁻⁶).
  - The four stellar-mass bins agree with each other: κ 0.95–1.16, p = 0.73, no trend (slope z = +0.36).
- **B21's hot-gas estimate does not close the gap.** All-isolated κ falls from 1.06 to 0.92, still 3.7σ above blue.
- **An early-type IMF does close it** (post hoc, no verdict weight). With CFG926 R5's correction (ATLAS3D dynamical M/L,
  1.5× Chabrier, on top of CFG667's +0.123 dex), red κ is 0.73 vs blue 0.52 (z = +1.8) and Sérsic n > 2 is 0.78 vs n < 2 at
  0.57 (z = +1.7). Both are below 2σ.

So **the 4 holds for disc galaxies.** Early types want κ ≈ 1.3 (1/κ² ≈ 0.6) with Chabrier masses, or about 0.75 with a
bottom-heavy IMF. This is the record's open early-type lensing excess (THEORY_CANONICAL), now stated as κ: it follows type,
not mass, and an IMF that gets heavier with σ removes most of it. **κ = ½ is FITTED.** Not theory closed.

## Results (`w4_10.out`; W4-06's estimator, CFG829 window, ν_simple, ρ_DE)

| partition | subsamples (κ, Δχ² = 1) | T1 universality |
|---|---|---|
| colour | blue 0.520 [0.433, 0.614]; red 1.293 [1.168, 1.424] | χ² 24.3 / 1, p 8.3×10⁻⁷: **NOT UNIVERSAL** |
| Sérsic | n<2 0.571 [0.480, 0.670]; n>2 1.320 [1.191, 1.457] | χ² 21.0 / 1, p 4.6×10⁻⁶: **NOT UNIVERSAL** |
| stellar mass | M1 1.029; M2 1.033; M3 0.953; M4 1.159 | χ² 1.32 / 3, p 0.73: **UNIVERSAL** (mixed types in every bin) |

**Report-only samples:**
- isolated dwarfs: not diagnostic (2 points in the window);
- all KiDS: 1.058 [0.984, 1.135];
- all KiDS + hot gas: 0.924 [0.862, 0.987] (T2: z +3.66 vs blue, does not restore one κ);
- GAMA all: 1.522 [1.163, 1.932] (T3: z +1.18 vs KiDS all);
- T4 mass trend: dκ/d log M★ = +0.06 ± 0.16.

**Post-hoc IMF diagnostic** (`w4_10_posthoc_imf.py` / `.out`; added after the frozen run, no verdict weight): early types get
g_bar × 10^0.299 and discs are unchanged. Red 0.731 [0.658, 0.809] and n>2 0.784 [0.705, 0.867]; z vs their disc twins
+1.79 and +1.71. This agrees with CFG926 R5 ("the red/blue split drops below 2σ"), which rests on the declared asymmetry
(discs not bottom-heavy).

## Checks and control

- **K1:** the import reproduces W4-06's blue fit exactly.
- **K2:** every covariance block is positive definite.
- **MUTATE (universal mock sky).** Each subsample is replaced by the law at the blue κ plus its own covariance noise. It reads
  UNIVERSAL in all three partitions (p = 0.12, 0.54, 0.15), and T2 "restores one κ", so the verdict changes. The control has
  power; exit 1 by design.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (61810a121) |
| `w4_10.py` | imports W4-06's committed estimator; numpy, one process, 1 s, 90 MB |
| `w4_10.out`, `w4_10_results.json` | normal run, 2/2 checks, exit 0 |
| `w4_10_MUTATE.out`, `w4_10_results_MUTATE.json` | universal mock sky, exit 1 by design |
| `w4_10_posthoc_imf.py`, `.out` | post-hoc IMF diagnostic (no verdict weight) |

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_10_one_kappa_lensing/w4_10.py > why_4_puzzle/W4_10_one_kappa_lensing/w4_10.out

The B21 files are read only and nothing was downloaded. Ran beside the live NC2x: one core, 90 MB, about 1 s.
