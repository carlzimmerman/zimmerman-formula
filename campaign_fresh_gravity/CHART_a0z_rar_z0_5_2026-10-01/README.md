# a₀ from z = 0 to 5.5, and the RAR at z ≈ 2–5.7 (chart, 2026-10-01)

> **Descriptive compilation; not a verdict; calibration-limited. No law is separated, preferred or disfavoured. ΛCDM has no a₀: the purple curve is an effective-a₀ PROXY. κ = ½ is FITTED.** Plot only: `chart_a0z_rar.py` reads committed files and computes nothing new (no fit, no estimator). Requested by the owner: a clean z = 0–5 chart from the best-calibrated data, including the z ≈ 2 RAR and implied-a₀ work (CFG227/228/229). It is a simplified companion to `CHART_a0z_combined_2026-09-30/` (which carries every sub-variant and both systematic bands).

Figure: `chart_a0z_rar_2026-10-01.png`.

## Panel A: implied a₀ against redshift
- **Curves** (CFG223 `cfg223_results.json`): flat a₀, a₀ ∝ H(z), the ΛCDM effective-a₀ proxy, a₀ ∝ √ρ_DE (DESI CPL), all in units of 10⁻¹⁰ m s⁻² on the canonical footing (9.3603e-11). Grey box at z ≈ 0 = the two footings (9.36e-11 / 1.131e-10), quoted from the record.
- **Points** (read from `CHART_a0z_combined_2026-09-30/chart_a0z_points.csv`, which is tied to the lane JSONs): RC100 four quartiles (class D); ALESS 122.1, the only class-M galaxy with a root (CFG229), and the six class-M galaxies with no root as floor triangles; the ALPINE6 pooled point (CFG228) with the five individual rooted rotators as faint squares without bars; CRISTAL independent route (class L, R_e and R_out) with the fit route as hollow circles. Thick bar 68 %, thin 95 % statistical; the shaded box is the INNER calibration band only (RC100/CRISTAL ±0.15 dex baryons; class M and ALMA their joint class bands; not on a common footing across lanes). The outer bands are on the 09-30 chart.
- CRISTAL points are nudged in z by at most 0.24 for legibility (true z 5.19–5.26).
- Top axis: age of the universe in flat ΛCDM (H₀ = 67.4, Ω_m = 0.315), for orientation only.

## Panel B: the RAR at z ≈ 2–5.7
g_obs against g_bar for every z ≥ 2 galaxy the record holds with stars, gas and a velocity: class M (CFG229 `GO`/`GB`), the ALPINE rotators + SPT0418-47 (CFG228 `GO`/`GB`, horizontal bar = joint inner band), CRISTAL class L and Amvrosiadis class S (CFG227 `cfg227_points.csv`, inner gas band), class D (RC100 z ≥ 2, CRISTAL fit route) as grey dots. Curves: g_bar ν_mono(g_bar/a₀) at the canonical a₀ and at a₀ × E(z) for z = 2.5 and 5 (E from CFG223's curve). Points below the 1 : 1 line have no a₀ solution (ν ≥ 1). CFG227 is read with its CFG237 correction (class M is not empty; S1's D < 1 comes mostly from SED stellar masses, not α_CO).

## How to read it
The headline sentence on the figure is the record's: at the declared calibration bands no sample separates flat a₀ from a₀ ∝ H(z) (blind pre-flights CFG227/228/229; CFG240 calibration wall). The height of an ALMA point is a calibration statement (the pressure term alone moves ALPINE6 from no root to s* 4.33), not evolution. The z ≈ 2 class-M discs sit at g_bar ≫ a₀ (Newtonian regime) and six of seven have baryons above the dynamics.

## Controls
`chart_a0z_rar_2026-10-01.out`: 6/6 pass (ALESS 122.1 and ALPINE6 plotted a₀ equal their lane JSON `a0_imp`; 6/7 class-M no-root; 2/7 ALMA no-root; 12 class-L rows; flat curve ≡ 1). `MUTATE=1` swaps the two plotted a₀ values; the tie check fails as it should (`chart_a0z_rar_2026-10-01_MUTATE.out`, 6/7).

## Run
`python3 campaign_fresh_gravity/CHART_a0z_rar_z0_5_2026-10-01/chart_a0z_rar.py` (a few seconds).
