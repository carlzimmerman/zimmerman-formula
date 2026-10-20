# p64 — raw SPARC with the fewest assumptions: is the cold energy per baryon the same for gas and stars, and what κ do the TRGB dwarfs give? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any p64 script exists.** Runs only when no 1024³ job is live. Append-only after this commit.

## Why this lane

The 2026-10-19/20 read-only audit of the κ error budget found five things:

1. **Statistics are set by rotation-curve reduction, not by distances.**
   - The 10 TRGB gas-dominated galaxies of CFG449/CFG442 scatter by 0.315 dex per galaxy.
   - Their quoted distance and inclination errors explain only about 0.14 dex.
   - SPARC and LVG TRGB distances agree to within 0.5% for 7 of the 10.
   - Two reductions of the same dwarfs (SPARC vs LITTLE THINGS) differ by 0.08–0.49 dex.
   - On those same 10 galaxies, κ moves from 0.46 to 0.54 to 0.60 between a point-weighted fit, the galaxy median and the galaxy mean.
2. **The ladder term is an assumption.** CFG493 sets it to 0.01 dex in distance with no calibration cited. A Cosmicflows-4-sized systematic would make it about 0.04 dex in a₀.
3. **The HI flux tie is untested for these dwarfs.** The tie is a SPARC−ALFALFA median of +0.053 dex over 35 mostly massive galaxies, none of them among the 10. Single-dish and interferometric scales disagree by 0.1–0.3 dex.
4. **ρ_Λ can come without H₀ or Planck.** TRGB distances plus ω_Λ need no H₀. CFG886 (5614bd0a5) gives ω_Λ ≈ 0.330 from BAO+BBN with flatness and w = −1, against Planck's 0.311.
5. **Kernel.** The canonical kernel is the simple μ (THEORY_CANONICAL 2026-10-14), and it equals the RAR form to 0.4% at these accelerations.

A separate result from the same audit is the clue this lane tests. SPARC gas-dominated galaxies imply an a₀ 1.46–2.4× lower than star-dominated ones, under every kernel (v02 S1/S2), and the record says the cause was never investigated. MIGHTEE's per-galaxy level anti-correlates with gas fraction.

## Inputs (on disk; nothing fetched)

- `real_research/data/sparc_data/*_rotmod.dat`: R, V_obs, e_V, V_gas, V_disk, V_bul per radius, at SPARC's adopted D.
- `real_research/data/SPARC_Lelli2016c.mrt`: D, e_D, f_D, i, e_i, Q. `SPARC_table.txt` is a saved 404 page and is never read.
- `real_research/data/alfalfa_a100_haynes2018.tsv` and `alfalfa_a100_positions.tsv`, for the flux tie.
- ω_Λ: Planck 0.3112 (0.685 × 0.674²) and CFG886's BAO+BBN value, read from its committed output.

## Assumptions that remain, stated (each one is varied or flagged)

- **Circular orbits.** No asymmetric-drift or pressure correction; SPARC's dwarf curves are a mix. FLAGGED: it biases dwarfs low and cannot be varied without σ profiles.
- **SPARC's mass models.** V_gas already includes ×1.33 helium and no H₂. f_gas is varied.
- **Disc and bulge M/L.** Υ_d is varied; Υ_b = 1.4 Υ_d.
- **Kernel.** The canonical simple μ inverts in closed form, point by point: **a₀,ᵢ = g_obs (g_obs − g_bar)/g_bar**, defined where g_obs > g_bar. The RAR inversion is reported as a cross-check.
- g_obs = V_obs²/R; g_bar = (V_gas|V_gas| + Υ_d V_disk² + Υ_b V_bul²)/R.

## (A) Within-galaxy gas-vs-star contrast: the cold-energy test

**Sample.** Galaxies with Q ≤ 2, i ≥ 30°, at least 3 gas-dominated points (V_gas|V_gas| ≥ 0.7 V_bar²) and at least 3 star-dominated points (Υ_d V_disk² + Υ_b V_bul² ≥ 0.7 V_bar²).

**Statistic.** Δ_g = median log a₀(gas points) − median log a₀(star points), computed per galaxy. Distance and inclination act on both sets through one factor, so a common error largely cancels. The residual comes from the levers, which differ (d ln a₀/d ln g_obs ≈ 2 deep, ≈ 3 near y ≈ 1). The script measures it by moving each galaxy's D and i by ±1σ.

**Grid.**
- Υ_d ∈ {0.3, 0.4, 0.5, 0.6, 0.7, 0.8} (population synthesis 0.4–0.8 at 3.6 µm).
- f_gas ∈ {0.70, 0.85, 1.00, 1.15}.

The population value is the median Δ_g over galaxies, with a galaxy bootstrap of 2000 resamples and seed 64.

**Verdict (frozen):**
- **CONTRAST:** median Δ_g differs from 0 at > 3σ for every Υ_d ∈ [0.4, 0.8] and every f_gas ∈ [0.85, 1.15]. The sign is recorded. Δ_g < 0 means gas points imply less cold energy per baryon than star points.
- **ABSORBED:** some Υ_d in [0.4, 0.8] together with some f_gas in [0.85, 1.15] gives |Δ_g| < 1σ.
- **UNDETERMINED:** otherwise, or fewer than 8 galaxies qualify.

**Reading rule.** CONTRAST is consistent with two explanations, and both must always be named:
1. cold energy tracking stars more than cold gas;
2. an error in the gas mass scale (f_gas outside 0.85–1.15) or an uncorrected pressure term in gas-rich outskirts.

CONTRAST is never presented as a cold-energy detection. Linking it to the KiDS early-type excess (CFG669/721) or to CFG745 is a hypothesis for a later lane.

## (B) κ from the TRGB gas-dominated galaxies, with the estimator spread

**Sample.** CFG449's S0 rule: f_D ∈ {2, 3, 5}, Q ≤ 2, at least 3 gas points (V_gas|V_gas| ≥ 0.7 V_bar² at Υ_d = 0.5).

**Control K1.** With ν_mono, the per-galaxy single fits must reproduce CFG442's 10 values to 0.01 dex. This is a code identity.

**Per galaxy.** log a₀ is the median of a₀,ᵢ over its gas points (simple μ, Υ_d = 0.5). Its error propagates e_D (lever measured), e_i (V ∝ 1/sin i) and e_V.

**Estimators, all reported:**
- **E1:** point-weighted pooled fit, as in CFG449.
- **E2:** median over galaxies.
- **E3:** mean over galaxies.
- **E4:** maximum likelihood with an intrinsic-scatter term τ (normal in log a₀, with per-galaxy errors), plus a profile interval on τ.

**κ.** κ = a₀ / (c √(G ρ_Λ)), with ρ_Λ = ω_Λ · 3(100 km/s/Mpc)²/(8πG), for both ω_Λ values. No H₀ enters anywhere.

**Systematics.** The ladder zero point is reported at 0.01 dex and at 0.017 dex in distance. The estimator spread max(E) − min(E) is reported as a systematic.

**Report-only verdict.** For each estimator and each ω_Λ: is ½ inside 1σ, inside 2σ, or outside? Is τ consistent with 0?

## (C) One flux scale for the TRGB dwarfs

Cross-match the (B) sample to ALFALFA α.100 by position (≤ 60″ and |Δcz| ≤ 50 km/s). If at least 3 match, report the median log(M_HI,SPARC / M_HI,α.100) and κ on that tie. Otherwise the verdict is **UNTESTED**. Pre-freeze expectation, from declinations: at most 2 of the 10 lie in α.100's sky (D631-7, DDO154), so UNTESTED is likely.

## MUTATE (must bite)

- **M1:** gas masses ×0.7 in (A). Median Δ_g must move by more than 0.05 dex.
- **M2:** all distances ×1.10 in (B). E2's log a₀ must move by between −0.15 and −0.30 dex.
- **M3:** in (B), swap the ω_Λ labels. The two κ columns must exchange.

## Honesty

- No knob scan beyond the frozen grid.
- Fixing the gas fraction rule, the point cuts and the bootstrap seed now is part of the freeze.
- κ = ½ stays FITTED.
- If K1 fails, (B) is VOID as frozen and is reported as such.

## Files to be produced (after the 1024³ chain)

`p64_raw_sparc_minimal.py`, `.out`, `_results.json`, `_MUTATE.out`, `README.md`.

## Amendment 1 (appended 2026-10-20, before any p64 script exists): run condition and two implementation readings

- **Run condition.** The frozen text says p64 runs "only when no 1024³ job is live". The owner instructed a parallel session
  to swing every remaining κ lane. The record's rule for lanes beside a live 1024³ job is CFG894 `KAPPA_CAMPAIGN_RULES.md` §11
  (2026-10-20): light single-core only. p64 is numpy over 175 small files plus a 2000-resample bootstrap, which is light. It runs
  under §11 beside the live NC2x (chain7b).
- **Implementation reading 1, (A) point classes.** Gas-dominated and star-dominated points are classified once, at the
  fiducial Υ_d = 0.5 and f_gas = 1.00. The same point sets are held fixed across the Υ_d × f_gas grid, so only a₀,ᵢ changes
  with the grid. This matches (B), which also classifies at Υ_d = 0.5. A galaxy needs at least 3 valid (g_obs > g_bar) points
  of each class at the fiducial.
- **Implementation reading 2, (B) E1.** The point-weighted pooled fit uses CFG449's weights (1/(e_V/V_obs)²) and minimiser,
  with the simple-μ kernel stated in "Kernel" above. K1 alone uses ν_mono, as frozen.
- **(C) data note, declared before the script.** The SPARC master table on disk has no coordinates, and the rules forbid
  downloads, so the positional cross-match cannot be made. (C) is reported UNTESTED, as the frozen pre-freeze expectation
  already anticipated.
- **The κ input.** CFG886's BAO+BBN ω_Λ is read from its committed output (cfg886.out line "(a) PRIMARY BAO+BBN": h, Ω_m;
  ω_Λ = (1 − Ω_m)h², flat, w = −1).
- Nothing else changes: no cut, grid, seed, estimator, verdict rule or MUTATE.
