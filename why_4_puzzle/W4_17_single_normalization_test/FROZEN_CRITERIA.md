# W4-17: is the within-galaxy a₀ residual a single stellar-M/L normalisation error? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20.** No real-data W4-17 statistic exists yet. A **synthetic pre-freeze calibration**
(`w4_17_prefreeze_calibration.py` / `.out`, planted worlds only, committed with this file) fixed the signature directions
**before** freezing. This is the lesson from W4-14/15/16, whose control or signature directions were mis-set. Append-only.
Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`. Observational lane (`obs`). **κ = ½ is FITTED.** Not theory closed.

## Question

Two of my results look inconsistent:
- **p64 (A):** on 11 galaxies, the within-galaxy gas/star gap Δ_g persists at Υ_d 0.8 (−0.22).
- **W4-16:** on 129 galaxies, the full-point slope s vanishes near Υ_d 0.7.

The calibration shows two things. Under a pure M/L normalisation error, every residual statistic crosses zero at the **same**
Υ*, the true one. Under a radial M/L gradient they cross at different, high Υ*. **On the same galaxies, do Δ_g, s and Δ_r (the
outer-half minus inner-half median log a₀) vanish at one common Υ*?**

## Calibration (disclosed; synthetic only)

- **World A** (exact law, true Υ 0.5): Υ* = 0.500 / 0.500 / 0.500 for Δ_g / s / Δ_r.
- **World B** (planted inner-heavy radial M/L): Υ* = 1.063 / 1.293 / 1.214. They disagree, and all are above 1.
- The slope s responds about twice as strongly to Υ as Δ_g. In world A, going from Υ 0.5 to 0.8 moves Δ_g by +0.22 and s by −0.46.

## Statistics (fixed; as the calibration code)

- Sample: SPARC Q ≤ 2, i ≥ 30°, at least 8 valid points.
- **S11:** galaxies with at least 3 gas-dominated and 3 star-dominated valid points at the fiducial (the p64 set).
- **S_all:** every galaxy.
- **Δ_g:** median log a₀ over gas points minus the median over star points, per galaxy; then the median over galaxies.
- **s:** the unweighted least-squares slope of log a₀,ᵢ against log g_bar, per galaxy (as calibrated; not W4-16's WLS), then the
  median.
- **Δ_r:** median log a₀ beyond the galaxy's median radius minus the median inside it, then the median.
- **Υ grid:** 0.3–1.4 in steps of 0.1, with Υ_b = 1.4Υ_d.
- **Υ*:** linear interpolation of the zero crossing.
- **CI:** galaxy bootstrap, 500 resamples, seed 64. σ(Υ*) is the bootstrap std over resamples that cross.

## Verdict (frozen; on S11, the only set where all three statistics exist)

- **SINGLE NORMALISATION:** the three Υ* agree pairwise within 2σ, and all lie in [0.4, 1.0].
- **NOT A SINGLE NORMALISATION (gradient-like):** some pair disagrees by more than 2σ, or Δ_g's or Δ_r's Υ* is above 1.0 or does
  not cross on the grid.
- **UNDETERMINED:** otherwise.
- Also reported: Υ* for s and Δ_r on S_all, and their agreement.

## Control (`W4_17_MUTATE=1`)

The script runs worlds A and B through the identical pipeline and bootstrap.
- A must return SINGLE NORMALISATION at Υ* ≈ 0.5.
- B must return NOT A SINGLE NORMALISATION.

Exit 1 when both behave.

## Register

One `obs` row, then `kappa_campaign_lee.py` rerun. Nothing downloaded.
