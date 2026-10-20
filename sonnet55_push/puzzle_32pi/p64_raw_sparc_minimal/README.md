# p64: raw SPARC with the fewest assumptions

Criteria: `FROZEN_CRITERIA.md` (d8b8fa3e4, committed alone 2026-10-20 by the session that froze it).
- Amendment 1 (3ed1622da): run condition, two implementation readings, (C) declared UNTESTED.
- Amendment 2 (a07bf55af): the frozen M2 window looks mis-set; the lever arithmetic was written before any script.

The script was written from the frozen text on 2026-10-20 by a parallel session (the why_4_puzzle lanes), on the owner's
instruction to swing every remaining κ lane. It ran beside the live NC2x under CFG894 §11: one core, 89 MB, 4 s.
**κ = ½ is FITTED.** Not theory closed.

## (B) κ with no H₀ anywhere: ½ inside 1σ

The sample is the ten TRGB/Cepheid/SN-distance gas-dominated galaxies (CFG449's S0 rule). **K1 PASS:** CFG442's ten
ν_mono single fits are reproduced to 0.0000 dex. With ρ_Λ = ω_Λ·3(100 km/s/Mpc)²/(8πG), κ is:

| estimator | log a₀ | κ (Planck ω_Λ 0.3112) | κ (CFG886 BAO+BBN ω_Λ 0.3302) |
|---|---|---|---|
| E1 pooled weighted fit | −9.955 ± 0.070 | 0.593 (½ inside 2σ) | 0.576 (inside 1σ) |
| E2 median over galaxies | −9.982 ± 0.123 | **0.557** (inside 1σ) | **0.541** (inside 1σ) |
| E3 mean over galaxies | −9.940 ± 0.091 | 0.614 (inside 1σ) | 0.596 (inside 1σ) |
| E4 ML with intrinsic scatter | −9.958 ± 0.084 | 0.589 (inside 1σ) | 0.572 (inside 1σ) |

- **Intrinsic scatter:** τ = 0.226 dex (1σ interval 0.168–0.307), not consistent with 0.
- **Systematics:** the estimator spread is 0.042 dex. A ladder zero point of 0.01 / 0.017 dex in distance moves E2 by −0.022 /
  −0.038 dex.
- **RAR-kernel cross-check:** E2 κ = 0.559 / 0.543.
- **Reading.** The H₀-free κ from the TRGB dwarfs is 0.54–0.61. It is consistent with ½, and it sits above CFG493's
  0.417 ± 0.095 (which includes the H₀-dependent MIGHTEE and WALLABY routes) by about 1σ.

## (A) Within-galaxy gas versus stars: UNDETERMINED as frozen, kernel-robust, and large at SPS M/L

The sample is 11 galaxies with at least 3 valid gas-dominated and 3 valid star-dominated points each. Δ_g is the median
log a₀ over gas points minus the median over star points, per galaxy; the population value is the median over galaxies, with
2000 bootstrap resamples (seed 64).
- **Every cell of the frozen grid is negative.** At the SPS fiducial (Υ_d 0.5, f_gas 1.00), Δ_g = −0.408 ± 0.085 dex (4.8σ).
  It shrinks toward high Υ_d and low f_gas: at Υ_d 0.8 with f_gas 0.85 it is −0.152 ± 0.081 (1.9σ).
- **The frozen verdict is UNDETERMINED.** Not every core cell is beyond 3σ, so it is not CONTRAST. No core cell is within 1σ of
  zero, so it is not ABSORBED either.
- **Kernel-robust:** the frozen RAR inversion gives −0.406 ± 0.083, the same as simple μ. The gap is not a kernel-shape artefact.
- **Distance and inclination** levers move Δ_g by only 0.017 / 0.011 dex.
- **Reading rule (frozen).** The gap is consistent with:
  1. cold energy tracking stars more than cold gas;
  2. a gas-mass-scale error or an uncorrected pressure term in gas-rich outskirts.

  M1 shows that removing 30% of the gas moves Δ_g by only +0.14 dex. So absorbing the full fiducial gap through the gas scale
  alone would need gas masses about 3× too high. Through M/L it would need Υ_d above 0.8. It is never a cold-energy detection.
- **The same direction as W4-10.** Star-dominated systems want a higher effective κ there too: red and early-type lenses give
  1.29 against 0.52 for blue. Both point to the 4 being a gas/star-averaged value under SPS masses.

## (C) One flux scale: UNTESTED

The SPARC table on disk has no coordinates, and downloads are forbidden (Amendment 1). The frozen pre-freeze expectation was
already UNTESTED.

## Controls

- **K1** PASS.
- **MUTATE** (`MUTATE=1`, `p64_raw_sparc_minimal_MUTATE.out`, exit 1 by design):
  - **M1** (gas × 0.7) moves Δ_g by +0.137 dex. PASS.
  - **M2** (D × 1.10) moves E2 by −0.092 dex. That is a **FAIL against the frozen window** (−0.15 to −0.30), but it lands inside
    the −0.083 to −0.124 predicted by Amendment 2 before any script existed. The control bites; its frozen window was mis-set.
  - **M3** (ω_Λ labels swapped): the κ columns exchange. PASS.

## Disclosure: first run

The first normal run (`p64_raw_sparc_minimal_firstrun_noRAR.out`, kept) omitted the frozen RAR-kernel cross-check. It was
added and the normal run redone. No other value changed.

## Files

`p64_raw_sparc_minimal.py`, `.out`, `_results.json`, `_MUTATE.out`, `_results_MUTATE.json`, `_firstrun_noRAR.out`.

    OMP_NUM_THREADS=1 nice -n 10 python3 p64_raw_sparc_minimal.py > p64_raw_sparc_minimal.out
    MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 p64_raw_sparc_minimal.py > p64_raw_sparc_minimal_MUTATE.out
