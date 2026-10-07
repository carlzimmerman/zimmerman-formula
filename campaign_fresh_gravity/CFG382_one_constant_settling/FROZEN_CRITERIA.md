# CFG382 FROZEN CRITERIA: one dimensionless fluid-lapse coupling. Does it pay for itself?

Committed alone, before any script. kappa = 1/2 FITTED and fixed. No dark-matter particle species: the cold MASS is still required and
is kept. No knob scans: lambda is fixed ONCE from one anchor, every other number is a prediction. Never "theory closed". Owner
(2026-10-06, chat "Nobel Prize and neutrinos"): "yeah swing bro". The orchestrator was told first.

**Why.** CFG381: the khronon cannot absorb the settling reaction through gravity alone, so a direct fluid-lapse coupling is forced
(+1 constant). Make it dimensionless. The only local rate the lapse field supplies is from its divergence (div g = -4 pi G rho_tot):
Gamma = lambda sqrt(4 pi G rho_tot(r)). The coupling multiplies (rho_c - rho_target[g]) (CFG373), so it vanishes where nu -> 1
(the record's single open row: "a coupling that vanishes where nu -> 1").

## Calibration (the ONE fit)
e = exp(-Gamma tau) with tau = 10.3 Gyr (since z = 2). MW anchor: e = 0.14 at 30 kpc (L191). rho_tot(30 kpc) = V^2/(4 pi G r^2) with
V = 200 km/s (isothermal; bracket 180-230 km/s reported). Solve for lambda.

## Predictions (no further freedom; local rho_tot at each anchor's measurement radius)
- **P1 groups:** the 20 Lovisari groups, rho_tot(R500) = M500/(4 pi R500^3) (isothermal local rule, h70 as published).
  Median e against 0.60 +- 0.15.
- **P2 clusters:** the 12 X-COP clusters, rho_tot(R500) by the same rule. Median e against 0.576 +- 0.15.
- **P3 pincer:** Gamma_MW >= 1.73 H_Lambda (CFG245 T-RAR line) and Gamma_cluster <= 1.93 H_Lambda (generous C max; 1.04 central
  reported).
- **P4 UFD direction (scored):** typical MW ultra-faint, r = r_half = 30 pc, sigma = 4 km/s, rho_tot = 3 sigma^2/(4 pi G r^2).
  The record shows UFDs carry LARGE excess (CFG336; cm15 +0.3 dex), so the prediction must give e >= 0.5. (If the formula settles
  UFDs fully, this fails; that is declared now.)
- tau brackets (z = 1, 7.7 Gyr; z = 4, 12.2 Gyr) are reported. lambda is re-fixed in each, consistently.

## Verdict (declared)
- **PAYS FOR ITSELF:** P1, P2 and P3 pass on the primary (V = 200, tau since z = 2).
- **PARTIAL:** two of the three pass.
- **FAILS:** one or none.
- P4 is reported alongside. If P4 fails it is named as a conflict (UFDs would need their early, pre-reionisation history:
  CFG338/344).
- The growth / sigma8 consequence needs a PM run (the orchestrator's engine). It is not run here.

## Controls
- C1: the calibration reproduces e_MW = 0.14 exactly.
- C2: the local-density rule returns M/(4 pi R^3) for an isothermal test profile.
- MUTATE: lambda x 3. The predictions must move: P1/P2 e changes by > 0.2. rc 1.

Local compute only. No downloads.
