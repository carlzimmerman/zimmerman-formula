# CFG186 — does SPARC's a₀ depend on a galaxy's speed through the CMB frame? (door 11C, gate G7)

## Bottom line, in plain language
**SPARC cannot test gate G7. The test is NON-DIAGNOSTIC, and G7 stays open.**
- **What G7 needs.** G7 asks whether a₀ changes by more than 10% between a galaxy at rest in the CMB frame and one moving at 600 km/s (β = 0.10 in a₀ = ā₀[1 + β(w/600 km/s)²]). Seeing that would require measuring β to about ±0.05.
- **What SPARC gives.** The 68 SPARC galaxies with distances that do not come from their redshift give ±0.45 at the very best (idealised) and ±2.2 in realistic mocks. That power row was computed and declared before the fit.
- **The fit.** β = +0.89 ± 0.67. This is not a detection:
  - shuffling the speeds among galaxies reproduces it 8% of the time;
  - the noise-injection null reproduces it 56% of the time.
- **The limit.** The conservative 95% upper limit is **β < 2.8**: a₀ could be up to ~3.8× higher at 600 km/s and SPARC would not have seen it.
- **KM1's khronon.** It predicts β = 0.11–0.27 over the record's c14 window, far inside what SPARC allows. It is **neither confirmed nor excluded**: the conditional bound is only ε = c₂ ≳ 1 × 10⁻⁶, 10–26× short of the window.
- **Do not cite β = +0.89 as a hint for KM1.** It is 1.8σ-level. It falls to +0.31 when a free sky dipole is allowed. The per-galaxy table gives +0.30 ± 0.29 (p = 0.38).

**A deeper limitation, independent of sample size.** A galaxy's speed through the CMB frame is only measured along the line of sight.
- Every nearby galaxy moves with the Local Group at ~620 km/s through the CMB frame. So KM1's effect would be mostly a **common** shift of a₀ for the whole Local Volume, which the fitted a₀ (and κ = ½, FITTED) absorbs. SPARC cannot see it at all.
- The line-of-sight proxy u² ≈ (V_LG·n̂)² (correlation of u with V_LG·n̂: r = 0.76) mostly tests a sky pattern aligned with the LG motion, not speed as such.
- A decisive G7 test needs galaxies with redshift-independent distances spread over regions that move at genuinely different 3D speeds through the CMB frame (many galaxies to ≳ 100 Mpc, with 3D flow reconstructions). SPARC is not that sample.

## What was run
Frozen question with five addenda: `FROZEN_QUESTION.md`. It was written before any script, and every change is dated relative to the fit.

**The speed.**
- Heliocentric velocity comes from four on-disk catalogues:
  - NED (via `sparc_cosmicweb_match.csv`): 126 galaxies;
  - the Updated Nearby Galaxy Catalog: 20;
  - Kourkchi & Tully 2017: 16;
  - 2MRS: 2.
  Where catalogues overlap, the median |Δv| is 2 km/s. The one gross mismatch is a 2MRS source at cz = 11 512 km/s within 1.5′ of UGC01281, evidently a background galaxy; NED is used for it.
- The velocity is converted to the CMB frame (v_sun = 369.8 km/s toward l, b = 264.0°, 48.3°). The line-of-sight peculiar velocity is u = c(z_CMB − z_cos(D))/(1 + z_cos(D)), with H₀ = 67.66 (73 as a variant).
- **Primary proxy W1:** w² → u². **Variant W2:** the galaxy shares the LG's transverse motion (V_LG = 627 km/s toward 276°, 30°, from memory; consistent to 0.8° with v_sun,CMB − v_sun,LG).

**The sample.** 68 clean galaxies with redshift-independent distances: 37 TRGB, 3 Cepheid, 26 Ursa Major, 2 SNIa.
- The distance error on u is σ_u ≈ H₀e_D: median 16 km/s for TRGB and 169 km/s for Ursa Major.
- Hubble-flow galaxies are excluded. Their distance was made from their own redshift, so u is **circular** (it reflects sky position and the flow model). Their fit (β at the bound of 20) is reported only as a warning.

**The likelihood.**
- For every galaxy, a 2D profile curve χ²(log a₀, distance): ν_mono kernel; Υ_disk, Υ_bul and inclination profiled with the LML 2018 priors; distance on a grid with its Gaussian prior.
- **The distance is shared** by the rotation curve (a₀ ∝ D⁻² in the deep regime) and the speed (u = cz_CMB − H₀D), so the correlated error is inside the likelihood.
- Birge scaling and an intrinsic-scatter softening (τ = 0.34 dex) act on the data part at fixed distance, never on the distance prior (Addendum 2).
- The curves reproduce CFG182's 1D curves to 95% |Δχ²| = 0.027.

## Results (`cfg186_b_fit.out`, `cfg186_a_curves_power.out`, `cfg186_c_pergalaxy_table.out`)
| quantity | value |
|---|---|
| power row, declared before the fit (W1, H₀ 67.66) | σ_β Fisher 0.45; mocks 2.25 → β_det(2σ) = **4.5** vs G7 line 0.10 → **NON-DIAGNOSTIC** |
| power row, W2 / H₀ = 73 | β_det 8.1 / 4.3 |
| primary fit | **β = +0.89**; bootstrap σ 0.67; 2.5–97.5% [−0.05, +3.43]; ā₀ = 8.0 × 10⁻¹¹ m/s² |
| speed-shuffle null (2000) | centred (median −0.02, 16–84% ±0.50); **p = 0.078** (0.10 within method groups) |
| noise-injection null (1000) | p = 0.56 (this null is biased; see "Process") |
| 95% upper limit on β | declared Neyman 1.80; shuffle Neyman 2.00 (two-sided [−0.15, 2.00]); bootstrap 2.78 → **quoted 2.78** (largest) |
| KM1 translation (β = 2.67 × 10⁻⁶/ε, sphere-averaged D/3, W1) | ε = c₂ ≥ 9.6 × 10⁻⁷ at 95%; KM1's window (β 0.11–0.27) **not reached** |
| SIGNAL lines | S1 fail (p 0.078 / 0.56); S2 fail (TRGB-type subsample 1.3σ); S3 pass (H₀ = 73 moves β by 0.07); S4 pass (apex / antapex agree) → **no signal** |
| G7 | **no verdict (NON-DIAGNOSTIC)** |

**Systematics** (β ± bootstrap σ, with each row's own speed-shuffle p):

| row | β | shuffle p |
|---|---|---|
| H₀ = 73 | +0.82 ± 0.70 | 0.068 |
| z frozen at the catalogue distance | +0.73 ± 0.48 | 0.088 |
| TRGB + Cepheid + SNIa only | +0.80 ± 0.61 | 0.12 |
| Galactic north | +0.72 ± 0.50 | 0.17 |
| no τ softening | +1.52 ± 1.10 | 0.15 |
| no Birge scaling | +0.87 ± 0.83 | 0.080 |
| W2 (coherent LG flow) | −0.45 | 0.50 |
| LG-apex hemisphere | +2.5 ± 3.0 | 0.020 |
| antapex hemisphere | −0.04 ± 0.69 | 0.96 |

- W2's bootstrap σ collapses (0.13) because the estimator sits near the model's pole; the shuffle p is the honest number. Ursa Major and the 12 Galactic-south galaxies are also pinned at the pole, so their bootstrap σ is not usable.
- With a **free sky dipole**, β → +0.31 ± 0.61 (the dipole takes |D| = 0.41 toward l, b = 250°, −50°).
- A distance term leaves β unchanged (+0.92; γ = +0.02).
- Single-galaxy jackknife: β ∈ [+0.68, +1.29].
- **SECONDARY** (the record's per-galaxy a₀ table; fixed nuisances, no errors, 52 galaxies): β = +0.30 ± 0.29, p = 0.38.

## Controls
- **Fitter exactness (FIT0 / M0):** noiseless synthetic curves with β = 0.30 return 0.3000.
- **Optimizer:** warm-started profiles match 6 cold starts to 0.0000. The spline in distance matches direct profiles to 0.04 near each minimum.
- **MUTATE** (β = 0.30 injected into the rotation curves before anything is built): β̂ rises from +0.89 to +1.43.
  - **The declared check M1 FAILED:** Δβ = +0.54 against the window [0.24, 0.36]. The MUTATE run keeps rc = 1.
  - **Cause:** the window wrongly assumed additivity. The model is multiplicative, (1 + β_obs z)(1 + 0.30 z), so with β_obs = 0.89 the shift is expected at 0.43–0.57.
  - **Verified two ways:** the same injection applied to the real curves at the curve level gives +0.57; with the real factor held fixed, the extra factor recovers γ = 0.335 against the injected 0.30.
  - The pipeline bites; the declared window was mis-specified (Addendum 5).

## Process (what went wrong and was fixed, in order; every earlier output is kept)
1. **Addendum 1, part A first run** (`*_firstrun.*`): a curve-edge extrapolation bug (three TRGB galaxies prefer a₀ below the grid) made the objective unbounded. Fixed with a non-decreasing continuation. The spline check tolerance was redefined; its first-run failure stays on record.
2. **Addendum 2, part A second run** (`*_secondrun.*`): the declared weighting scaled the distance prior along with the data (e_D inflated ~2.7×). That gave the speed–distance coupling a cheap per-galaxy freedom, and the β = 0 mocks ran away. Fixed so the prior is never scaled.
3. **Addendum 3, before part B:** the power row came out NON-DIAGNOSTIC. The mocks are skewed (median β̂ +1.46 at β = 0), so the Neyman grid was extended to 10 and the "z frozen" variant added.
4. **Addendum 4, after part B's first run** (`cfg186_b_fit_firstrun.*`):
   - The noise mocks misrepresent the estimator. Noiseless injections on the real curves are recovered 1:1, but the Gaussian mocks inflate β̂ about 3×.
   - A shuffle-based Neyman construction and per-row shuffle p values were added. The quoted limit is the largest of three.
   - The verdict did not change.
5. **Addendum 5, after MUTATE:** the M1 failure and its diagnosis, as above.

**Standing reminders.**
- κ = ½ stays FITTED; nothing here bears on it.
- The Ω_Λ / a₀ tie is not used.
- Never cite this lane as a bound at the G7 level, or as support for KM1.

## Files and rerun (from the repository root; each script < 3 min on 14 cores)
```
python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_a_curves_power.py            # velocities, sample, 2D curves, power row
python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_b_fit.py                     # fit, nulls, systematics, limits, KM1, G7
MUTATE=1 python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_a_curves_power.py   # beta = 0.30 injected (curves)
MUTATE=1 python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_b_fit.py            # MUTATE fit (after the real run; rc = 1, M1)
python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_c_pergalaxy_table.py         # SECONDARY table
```
**Supporting files:**
- `cfg186_common.py`: loader, velocities, 2D profile, curves, fitter, pool tasks.
- `cfg186_a_curves.npz` / `_MUTATE.npz`: the coarse 2D curves.
- `*_results*.json`: every number quoted above.


## Disclosure after the independent referee CFG193 (04dcc6b46; appended 2026-09-29; the text above is left as first written)
NON-DIAGNOSTIC holds; the sample, speeds, Fisher row and lever arm reproduce. One disclosure. The profile fits bound the inclination at ±8 σ_Inc (capped to [5°, 90°]) and the Υ parameters at ±10 prior-σ. The frozen text says only "inclination Gaussian", so these boxes are UNDECLARED implementation choices. For NGC2403 the box binds: the unboxed solution sits at −8.26 σ_Inc. With the box removed, β̂ moves from +0.887 to about +0.49 (p 0.22; 95% upper limit 3.0), and the referee's own fit with the box imposed gives +0.93. The earlier "optimiser stuck in a local minimum" reading is withdrawn by both sides: inside the box, 40 cold starts reproduce the stored values exactly (the orchestrating session checked every x node of NGC2403's t = −4 row, plus F571-8, UGC05764 and UGC00731). β̂ is therefore fragile to an undeclared nuisance bound. Quote both values; no verdict changes. An unexplained residual of about 0.15 in χ² remains in 364 UGC00731 cells.
