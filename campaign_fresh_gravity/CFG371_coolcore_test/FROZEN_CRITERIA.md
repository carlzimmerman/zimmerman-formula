# CFG371 FROZEN CRITERIA: cool-core vs non-cool-core clusters, a falsification test of the induced settling principle

Committed alone, before any script. kappa = 1/2 FITTED and fixed. nu_mono, canonical primary, alt reported. No dark-matter particle
species: the cold MASS is still required and is kept. No knob scans. Never "theory closed". Owner (2026-10-06, chat "Nobel Prize and
neutrinos"): "yes" to prediction 1 of the inductive synthesis. The orchestrator was told first.

**Principle under test (induced from CFG364-370 and cm08-cm15).** One conserved cold fluid. Where baryons cool, it settles over a few
cooling times into the configuration that IS the a0 law. The unsettled part is extra mass, with unsettled fraction
e = exp(-tau/t_cool).
**Prediction.** At fixed cluster mass, a region whose gas cools fast carries LESS dark excess beyond the law than one whose gas
cannot cool.
**Falsifier.** No correlation, or the opposite sign.

## Data and quantities (all from the repo's X-COP FITS; declared)
- Clusters: the 7 X-COP clusters with hydro_mass, fgas_profile AND mstar files (PRIMARY). The 12 with M_star := 0.10 M_gas where
  mstar is missing are SECONDARY, reported.
- Inner radius r_in = 0.1 R500 (inside the core region; outside the innermost data point of each profile).
- Local gas density at r: rho_gas(r) = (dM_gas/dr)/(4 pi r^2), from the FGAS profile by a log-log finite difference.
- kT = mu m_p G M500/(2 R500) (isothermal; declared). Real cool cores are cooler, which shortens t_cool further; only the ranking is
  used.
- Cooling: Tozzi & Norman with the CORRECTED unit 1e-22 (CFG370). t_cool in cm12's convention.
- **Cooling indicator:** t_c = t_cool at the innermost common radius 0.03 R500. Classes: COOLING if t_c < 7.7 Gyr (the standard
  CC/NCC line), else NON-COOLING. Reported.
- **Inner excess:** X_in = (M_hse(<r_in) - M_law(<r_in)) / (5.364 M_b(<r_in)), the retained fraction at 0.1 R500, where
  M_law = nu_mono(g_N,b/a0) M_b and M_b = M_gas + M_star.

## Tests
- **T1 (sign, PRIMARY):** Spearman rho(t_c, X_in) over the 7. The principle predicts rho > 0.
- **T2 (split):** the median X_in of COOLING vs NON-COOLING (when both classes have >= 2 members). The principle predicts
  COOLING < NON-COOLING.
- **T3 (amplitude, reported):** the predicted e(r_in) = exp(-tau/t_cool(r_in)), tau = 10.3 Gyr, against X_in. Report the median
  ratio. Not scored.

## Verdict (declared)
- **SUPPORTED:** rho >= +0.50 with one-sided permutation p < 0.10 (N = 7), AND T2 in the predicted direction (or T2 undefined).
- **CONTRADICTED:** rho <= 0, OR T2 in the opposite direction by more than 0.1.
- **INCONCLUSIVE:** anything else. The 12-cluster secondary is reported, never pooled with the primary.
- N = 7 has low power. Say so whatever the outcome.

## Controls
- C1: the corrected cooling's bremsstrahlung term matches free-free at 1 keV to 1% (CFG370 check).
- C2: the finite-difference density integrates back to M_gas within 5% between 0.03 and 1 R500 for every cluster.
- MUTATE: t_c is randomly permuted across clusters (seed 371). rho must fall below +0.50 OR the T2 direction must break, rc 1.

Local compute only. No downloads.
