# CFG362 FROZEN CRITERIA: can inflation fix the cold fluid amount (stochastic misalignment)?

Committed alone, before any script. kappa = 1/2 FITTED and fixed. No dark-matter particle species: the cold MASS is
still required and is kept. No knob scans. Never "theory closed". Owner (2026-10-06): "swing it" on the inflation route
proposed after CFG360 (baryon tie, NO-GO). (ID note: CFG361 was taken by a parallel session; CFG360 collided and the
orchestrator relabelled its lane CFG360-DE.)

**Question.** The CFG288 wave field (complex Phi, V = rho_Lambda + m^2 |Phi|^2, minimally coupled) has a free amount.
If a long de Sitter phase (inflation, Hubble rate H_I, NOT part of the framework) drives Phi to its stochastic
equilibrium, the start value is erased and the amount is fixed by (H_I, m). Does that relation survive the gates, and
what does it predict?

## Model (declared)
- Each real component of Phi obeys the Starobinsky-Yokoyama moment equation
  d<phi^2>/dN = H^2/(4 pi^2) - (2 m^2 / (3 H^2)) <phi^2>, so <phi^2>_eq = 3 H^4/(8 pi^2 m^2), relaxation N_rel = 3 H^2/(2 m^2).
- Complex field (two components): rho at oscillation onset = m^2 <|Phi|^2> = 3 H_I^4/(8 pi^2) (the mean). In one Hubble patch
  |Phi|^2 is exponentially distributed (chi-squared, 2 dof), so the local amount is a random draw around that mean.
- Onset: H(T_osc) = m in the radiation era, H = 1.66 sqrt(g*) T^2/M_Pl, with a declared step table for g*(T); then
  n = rho/m per entropy is conserved: rho_c0 = m (rho_osc/m)/s_osc x s_0.
- Target: rho_c0 = omega_c rho_crit/h^2 = 0.1200 x 1.05375e-5 GeV/cm^3; s_0 = 2891.2 cm^-3.
- Mass window from CFG360 T0b: [2e-20 eV (CFG288), 2.78 eV (CFG360)], read from CFG360's committed JSON.

## Tests
**T0 (controls).**
- T0a: integrate the moment equation numerically. It must reproduce <phi^2>_eq and N_rel analytically, to 1%.
- T0b: reproduce rho_c0/s_0 from the inputs.
- T0c: read the mass window from CFG360's results JSON.

**T1 (the relation).** Solve for H_I(m) over the window (a map of the declared window, not a fit). Report the power-law
slope d ln H_I / d ln m.

**T2 (equilibration is physically allowed).** PRIMARY gate: N_rel must not exceed the de Sitter entropy,
S_dS = pi M_Pl^2/H_I^2 (Arkani-Hamed, Dubovsky, Nicolis, Trincherini, Villadoro 2007: the semiclassical bound on the
number of e-folds). REPORTED ONLY: the trans-Planckian censorship conjecture, N < ln(M_Pl/H_I).

**T3 (consistency).**
- (a) The field is light during inflation: m < H_I/10.
- (b) Inflation can reheat above BBN: V^(1/4) = (3 H_I^2 Mbar_Pl^2)^(1/4) > 5 MeV.
- (c) The fluid is in place before z = 1e5 (CFG288): T_osc > 1e5 T_0.
- (d) Minimal coupling during inflation (no xi R |Phi|^2) is declared, not tested.

**T4 (isocurvature).** The uncorrelated CDM isocurvature from the last ~60 e-folds is S ~ 2 sqrt(2/3) m/H_I per log k
(from (H/2pi)/phi_rms). It must satisfy P_S < 0.04 P_zeta (Planck 2018, uncorrelated), with P_zeta = 2.1e-9.

**T5 (prediction and falsifier).** Report the tensor ratio r = 2 H_I^2/(pi^2 Mbar_Pl^2 P_zeta) over the window, and the
H_I a detection at r = 1e-3 would imply. If that H_I lies above the window's maximum, a B-mode detection excludes the route
for every fluid mass.

**T6 (draw scatter).** Report the 5-95% range of the local amount from the exponential |Phi|^2 distribution. This sets
how "fixed" the amount actually is.

**MUTATE.** Multiply the noise term by 10 (H/2pi -> 10 H/2pi). T0a must FAIL (the analytic reproduction breaks), rc = 1.

## Verdict classes (declared)
- **CONDITIONAL-TESTABLE:** T2-T4 pass over a non-empty part of the window. The amount is fixed up to the T6 draw, given
  H_I. That is ONE new constant (H_I) for one removed (the amount): relocated, not reduced, unless H_I is independently
  measured. State the falsifier.
- **NO-GO:** T2, T3 or T4 fails over the whole window.
- **OPEN:** a gate cannot be decided with local compute.

Local compute only. No downloads. g*(T) is approximate; report the sensitivity of H_I to g* x 2.
