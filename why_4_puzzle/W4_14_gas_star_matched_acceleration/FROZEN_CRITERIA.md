# W4-14: gas versus stars at the same acceleration: is the gap about baryons or about acceleration? (frozen, committed alone)

**Status: FROZEN 2026-10-20, before any W4-14 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Observational lane (`obs`). **κ = ½ is FITTED.** Not theory closed.

## Question

Inside galaxies, gas-dominated points imply a lower a₀ than star-dominated points by about 0.4 dex. This holds under every
declared law (W4-13) and survives any plausible universal mass correction (W4-12). Within a galaxy, though, gas points also sit
at lower g_bar and larger radius. An acceleration- or radius-dependent effect would mimic the gap. Examples are an external-field
effect, which weakens the boost at low internal acceleration, or outskirts physics. **At the same g_bar, pooled across SPARC,
do gas-dominated and star-dominated points still disagree?**

## Method (fixed)

- **Sample:** SPARC Q ≤ 2 and i ≥ 30°.
  - Gas-dominated points: V_gas|V_gas| ≥ 0.7 V_bar².
  - Star-dominated points: 0.5 V_disk² + 0.7 V_bul² ≥ 0.7 V_bar².
  - Both classified at the fiducial Υ_d 0.5, f_gas 1, as p64. Points need g_obs > g_bar > 0.
  - Per point: log a₀,ᵢ (simple μ: g_obs(g_obs − g_bar)/g_bar). RAR inversion as a cross-check.
- **Bins:** log g_bar from −12.0 to −9.5 in 0.25 dex steps.
- **Per bin and class:** the median over galaxies of each galaxy's median log a₀ in that bin, so each galaxy counts once per bin.
  A bin is usable if both classes have ≥ 3 galaxies.
- **Statistic:** Δ_bin = (gas) − (star). The combined Δ_match is the inverse-variance mean over usable bins, with σ from a
  galaxy bootstrap (2000 resamples, seed 64, resampling galaxies across all bins).

## Verdict (frozen)

- **BARYON-TYPE:** Δ_match < 0 at more than 3σ. Gas still implies less a₀ than stars at the same acceleration.
- **ACCELERATION:** |Δ_match| < 2σ, with at least 3 usable bins. The within-galaxy gap is then an acceleration/radius effect.
- **INTERMEDIATE:** otherwise. **NOT DIAGNOSTIC:** fewer than 3 usable bins.
- Also report: the within-galaxy gap restricted to the galaxies and acceleration range of the usable bins, so the two
  statistics are comparable.

**Hand expectation (disclosed):** INTERMEDIATE or NOT DIAGNOSTIC. Gas-dominated points rarely reach high g_bar and star-dominated
points rarely reach low g_bar, so the overlap bins near −11 to −10.5 may be few.

## Controls (`W4_14_MUTATE=1`, separate outputs, exit 1 when both bite)

- **M1, label shuffle within each bin** (seed 64). Δ_match must fall within 2σ of 0.
- **M2, a planted acceleration-only effect.** Replace V_obs by the simple-μ law with a₀(g_bar) = a₀* (g_bar/10⁻¹¹)^0.25, with
  a₀* = ½c√(Gρ_Λ) and no type dependence.
  - The within-galaxy gap must appear (|Δ_g| > 2σ).
  - The matched Δ_match must stay within 2σ of 0.
  - This shows the test separates acceleration effects from baryon-type effects.

## Register

One `obs` row, then `kappa_campaign_lee.py` rerun. Nothing downloaded.
