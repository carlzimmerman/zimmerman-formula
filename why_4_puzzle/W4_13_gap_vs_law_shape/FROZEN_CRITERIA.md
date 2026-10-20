# W4-13: is the within-galaxy gas/star gap a law-shape effect? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-13 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Observational lane (`obs`). **κ = ½ is FITTED.** Not theory closed.

## Question

p64 (A) found that, inside galaxies, gas-dominated points want an a₀ about 2.5× lower than star-dominated points: Δ_g =
−0.408 ± 0.085 dex at Υ_d 0.5. W4-12 showed that no plausible universal M/L or gas correction removes it. p64 tested only two
kernels with nearly the same transition shape (simple μ and RAR). Star points sit near y ≈ 1 and gas points deep, so the
transition **shape** of the law moves the star points' inferred a₀ much more than the gas points'. **Does any declared law
form close the gap, and if so, does SPARC's RAR allow it?**

## Declared law forms (fixed list; no scan beyond it)

- **Family L_n:** g² − g_N^n g^{2−n} = a₀ g_N, inverted per point as a₀ = (g² − g_N^n g^{2−n})/g_N.
  - n = 1 is the canonical simple μ (CFG / THEORY_CANONICAL).
  - n = 2 is AG4's quadratic a₀-line, ν₂ = √(1 + 1/y).
  - n = 0.5 and n = 1.5 are declared as one softer and one intermediate form. This is a four-member menu, not a fit.
- **RAR (exponential):** a₀ = g_N / ln(1 − g_N/g)², as p64.

## Measurements

- **Δ_g per law** at the p64 fiducial (Υ_d 0.5, f_gas 1), with p64's sample of 11 galaxies, point classes and statistic:
  median over galaxies of [median log a₀(gas) − median log a₀(stars)], bootstrap 2000, seed 64. The p64 code is copied;
  **K1:** n = 1 must reproduce −0.408 and RAR −0.406 to 2e-3.
- **SPARC RAR fit per law:**
  - Sample: Q ≤ 2 and i ≥ 30°, every point with g_obs, g_bar > 0, Υ_d 0.5, Υ_b 0.7.
  - Forward model g = g(g_N; a₀, law), solved per point. a₀ is free (one parameter per law).
  - χ² uses σ_log g = 2e_V/(V ln 10).
  - Report χ²_min and Δχ² against the best declared law.

## Verdict (frozen)

- **GAP IS LAW-SHAPE:** some declared law gives |Δ_g| < 2σ **and** its RAR Δχ² ≤ 9 against the best declared law.
- **GAP NOT LAW-SHAPE:** every law with |Δ_g| < 2σ has RAR Δχ² > 9, or no law closes the gap.
- Also report: the a₀ (κ_Λ) each law's RAR fit wants, and the sign of the trend of Δ_g with n.

**Hand expectation (disclosed):**
- n = 2 makes the gap larger: star-point a₀ rises by a factor of about (1 + g_N/g).
- n = 0.5 makes it smaller and might close it, but its transition is softer than the RAR allows.
- Expected verdict: **GAP NOT LAW-SHAPE.** That is a guess; the fit decides.

## Control (`W4_13_MUTATE=1`, separate outputs, exit 1 when it bites)

- **M1, mock law-shape world.** Replace every SPARC V_obs by the n = 0.5 law's prediction at the declared a₀ = ½ c√(Gρ_Λ),
  with the same g_bar.
  - Δ_g under n = 0.5 must then be within 2σ of 0.
  - Δ_g under n = 1 must be nonzero beyond 2σ.
  - So the test can attribute a gap to law shape when one is planted.

## Register

One `obs` row, then `kappa_campaign_lee.py` rerun. Nothing downloaded.
