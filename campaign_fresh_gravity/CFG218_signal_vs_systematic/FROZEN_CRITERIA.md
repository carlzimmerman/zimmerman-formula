# CFG218 — the signal-to-systematic ladder: which of today's samples could separate flat from rival, and how precise must the baryon-mass calibration be? FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, before any CFG218 number. **κ = ½ FITTED, NOT DERIVED.** This is a forecast built on quantities the record already holds. It scores no data against a law and gives no verdict on either law.

## Question

For each decomposition sample used today, how large is the rival-vs-flat separation at that sample's own accelerations and redshifts (the signal), how large is the offset its baryon-mass route can produce (the systematic), and how large is its statistical band? Where does the signal exceed both?

## Exposure, disclosed

- Everything in CFG213, CFG215, CFG216 and CFG217, including the committed route biases b_s and the confidence intervals.
- Nothing new is computed from data in this lane beyond the separation defined below.

## Samples (the primary series of CFG215, plus RC100)

- MUSE-DARK (SED + H₂ route, 109), RC41 (prior-anchored, 41), NOEMA3D (SED + CO, 10), CRISTAL (SED + dust gas, 9) and RC100 (100).
- Per galaxy, g_bar and z are exactly those of the source lane. RC100 uses CFG216's (g_bar, z).

## Definitions

- **Signal.** S_i = |log₁₀[ν(g_bar,i/(A0_f E(z_i)))/ν(g_bar,i/A0_f)]|, the rival-vs-flat difference in log D at the galaxy's own g_bar and z (ν_mono, canonical).
  - The sample signal S_s is the median over galaxies.
- **Statistical band.** σ_s = the half-width of the sample's 95% CI on its median δ, taken from the source lane's committed results (CFG213/215/216, ν_mono canonical, flat law).
- **Systematic.**
  - **b_s** = the sample's median log₁₀(M_ind/M_fit), as committed in CFG215.
  - The offset in δ that a baryon-mass error of size e produces at fixed g_obs is Y_s(e) = |median δ_flat| under g_bar → g_bar × 10^e, computed exactly from the sample's galaxies with the flat inversion for the true baryons.
  - S_sys,s = Y_s(b_s).
  - The **precision needed** e_s is the mass error at which Y_s(e_s) = S_s/3. That is the calibration for a 3σ-equivalent separation.
- **Classification (frozen):**
  - "systematic-limited" iff S_sys,s > S_s;
  - "statistics-limited" iff σ_s > S_s;
  - "discriminating" iff S_s > 3 max(S_sys,s, σ_s/1.96), the second term being the 1σ statistical error;
  - otherwise "marginal".
- **The differential version for a within-sample z lever arm (RC100):**
  - the needed differential calibration e_diff is the change between z = 0.6 and z = 2.5 that shifts the slope of δ_flat by the rival-true expectation divided by 3, using CFG217's data-side curve;
  - the value −0.075 dex (flat-exact) and −0.25 dex (rival-exact) from CFG217 are cited as computed there, not recomputed.
- **The mass-route context**, quoted for each sample: the fit-vs-independent offset b_s and the prior width (MUSE-DARK: no prior; RC41/RC100: 0.2 dex; NOEMA3D: measured CO; CRISTAL: 1 dex).

## Reported, not graded

- Each sample's fraction of galaxies with g_bar/a₀ < 3.
- The rival-vs-flat separation and the precision needed at the sample's lowest-g_bar quartile.

## Controls

- **C1.** S_i = 0 at z = 0.
- **C2.** Y_s(0) = 0, and Y_s(e) is monotone in |e|.
- **C3.** The signal median for CRISTAL reproduces the rival-vs-flat separation implied by CFG213's committed per-galaxy D_flat and D_rival (median of the log ratio; to 1e-6).
- **MUTATE=1.** The rival's a₀ factor is set to 1, so E ≡ 1. Every signal must be 0, and every sample must then be classified "systematic-limited" or "statistics-limited" (never "discriminating").

## Figure

For each sample: the signal S_s (bar), the systematic S_sys,s and the statistical band σ_s, on a log scale, with the classification.
