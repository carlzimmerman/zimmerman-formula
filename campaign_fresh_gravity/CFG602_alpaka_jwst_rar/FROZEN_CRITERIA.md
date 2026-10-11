# CFG602 FROZEN CRITERIA: a JWST-baryon RAR point for ALPAKA IDs 1, 3, 13 (arXiv:2601.03338 decomposition)

Written 2026-10-10 before any CFG602 number is computed. Inputs read so far are the committed data tables only (`data_assembly/arxiv_tables/alpaka_jwst2026_*.csv`, `alpaka1_*`), CFG272's README, and the arXiv 2601.03338 abstract/HTML summary. Nothing downloaded. κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; a₀ flat; ν_mono; cold energy mass required; not "theory closed". RAW data vs framework-native only.

## Question
Do the three JWST-baryon ALPAKA discs (ID1 z 0.561, ID3 z 1.445, ID13 z 2.103) give a RAR point that can say anything about a₀? (No paper published one; 2601.03338 mentions no MOND.)

## Definitions (no fitted quantity)
- g_obs = V_ext² / R_ext, V_ext and R_ext from the ALPAKA I table / digitised outer ring (`alpaka1_kinematics.csv`, `alpaka1_outer_summary.csv`).
- Baryons from 2601.03338's fiducial fit: M_b = M*_dyn + M_gas (`alpaka_jwst2026_fiducial_fit.csv`), central values and the table's own errors, in quadrature with V_ext and inclination errors by 10^4 Monte Carlo draws (seed 602).
- The enclosed fraction f of M_b inside R_ext is NOT tabulated, so two brackets are declared: **B_max** f = 1 (all baryons inside R_ext; gives g_bar upper, D lower) and **B_half** f = 0.5. g_bar = G f M_b / R_ext² (spherical shortcut as CFG272).
- y = g_bar / a₀ per footing; D = g_obs / g_bar; law prediction D_law(y) = nu_mono(y).

## Labels (per disc, per footing)
- **CONDITIONED** if y(B_max) ≤ 1 (then nu_mono ≥ 1.5 and a₀ moves D by ≥ 0.1 dex over a factor-2 change); else **ILL-CONDITIONED** (CFG240 conditioning).
- **CONSISTENT** if |log10(D / nu_mono(y))| ≤ 2 sigma of the Monte Carlo (both brackets); **TENSION** if outside in both; **BRACKET-DEPENDENT** otherwise.
- Verdict for the lane: **A₀-INFORMATIVE** only if at least one disc is CONDITIONED and not BRACKET-DEPENDENT on both footings; otherwise **NOT INFORMATIVE FOR a₀ (reported D only)**.

## Controls and MUTATE
- K1: ID13's stars-only B0 D at R_ext reproduces CFG272's committed D = 0.442 within 0.02 when M_gas is set to zero and M* to the SED value (uses the same inputs).
- K2: alt footing differs from canonical only by a₀ (g_bar, g_obs identical).
- **MUTATE:** V_ext × 2 must turn at least one CONSISTENT label into TENSION; if no label changes the labelling has no teeth.
