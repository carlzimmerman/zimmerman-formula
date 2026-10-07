# CFG473: is the extra force needed to hold an isothermal cold fluid at the law's target a LOCAL function of y = g_N/a₀? FROZEN before any script exists

Owner chat 10-07 (council computational round; follows CFG472). κ = ½ fitted; units G = a₀ = M_b = 1 (a footing rescales r_M only). No DM particle; the cold mass is still required.

**Setup.**
- CFG472's baryons: Hernquist, a = 0.1, 0.3, 1, 3 r_M.
- The fluid sits exactly at the target ρ_ph = (1/4πr²) dM_ph/dr, with M_ph = (ν_mono(g_N) − 1) M_b(<r).
- Its velocity dispersion is σ² = V_f²/2 = 1/2 (BTFR-fixed).
- Total gravity is then the law, g = ν g_N.
- The non-gravitational radial acceleration needed for hydrostatic balance is f(r) = σ² d ln ρ_ph/dr + ν g_N (positive = outward push needed). In the deep regime f → 0 identically (sympy check K1).

**Statistic.** f/a₀ against y = g_N/a₀ for each a. On a common log-y grid over y ∈ [0.1, 10] (interpolated where each profile covers it), the locality spread S(y) = max_a |log10(f_a / median_a f)|, taking |f| and recording the sign separately. Also report the fraction of radii where f > 0 (outward).

**Verdict.**
- **LOCAL** if max over y of S ≤ 0.04 dex and the sign agrees across a at every y.
- **NONLOCAL** if max S > 0.15 dex or the sign disagrees anywhere.
- Otherwise WEAKLY LOCAL.
- LOCAL would make f(y) a candidate universal coupling to test against G9. NONLOCAL would say the holding force depends on the baryons' global structure, like Gap 1's enclosed-mass object.

**Controls.**
- K1: f(r) → 0 for a point mass in the deep regime (r ≥ 30 r_M) to 1% of ν g_N.
- K2: the numerical d ln ρ_ph/dr is checked against an analytic point-mass deep limit (−2/r) to 1% at r ≥ 30.

**MUTATE.** σ² ×2. The deep-regime f is no longer 0 (K1 must fail); exit 1 when detected.
