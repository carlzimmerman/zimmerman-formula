# CFG837 (lane SHELL) FROZEN CRITERIA: can the radial-shell tether dynamics fix the free fraction F from the baryon loss fraction f_loss?

Date 2026-10-18. Round 2 of the parameter-reduction workflow (no-compute round). Dir: `campaign_fresh_gravity/CFG837_shell_bound_fraction/`.
Written BEFORE `DERIVATION.md`. kappa = 1/2 is FITTED; Omega_c/Omega_b = 5.364 measured; footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) never
pooled; no dark-matter particle species; raw data / framework-native only; not "theory closed". NOTHING is executed in this lane (a 1024^3 run is
live); every number is hand arithmetic and is shown.

## 0. Disclosure: what was seen before this freeze
- READ: `PARAMRED_2026-10-16/E_FREE/{FROZEN_CRITERIA,CONDITIONS,DERIVATION}.md`; `THEORY_CANONICAL_2026-10-16.md`; CFG747 criteria, README, `cfg747.py`;
  CFG776 criteria, README, `cfg776.py`; ledger rows CFG745, 748, 749, 776, 777, 801, 804, 806, 810, 811, 812, 813, 814, 721; READMEs of CFG804, 806, 811,
  812, 814, 721.
- The single-shell energy integral (Phi_eff = -1/r + m^2/(3 r^3), shell at rest with m = sqrt(p) r) was sketched in my head while reading CFG776, so
  the threshold structure was NOT unknown when these criteria were written. The criteria therefore fix the classes, the target intervals, the
  pass rules and the error-catching checks; they are NOT a blind prediction. Outcomes are labelled "derivation", never "prediction".

## 1. The quantities (fixed now; every input is quoted from the cited file, none is chosen here)
- p = M_peak / M_now = N = 1 / f_ret (peak baryon mass over present baryon mass, catchment accounting of CFG804). f_loss = 1 - 1/p = 1 - f_ret.
- Units G = a0 = M_now = 1: lengths r_M = sqrt(G M_now / a0), velocity V_flat = (G M_now a0)^(1/4), time t0 = sqrt(r_M / a0), energy V_flat^2 per unit
  mass, mass M_now.
- Equation of motion (CFG747): r'' = -1/r^2 + m(<r)^2 / r^4, m = enclosed cold-energy mass; static law m = r.
- F as the E-lane defines it (E_FREE `DERIVATION.md` Step 1, `FROZEN_CRITERIA.md` T2): M_free = F * S, S = 5.364 (1/f_ret - 1) M_b,now = 5.364 (N - 1) M_now.
- F_dyn (this lane): U / S, with U = the tethered cold mass that is unbound (energy >= 0) in the shell dynamics after the baryon mass falls from p to 1.
  u = U / M_c is the unbound share of the total tethered cold mass M_c = 5.364 p M_now; F_dyn = u / f_loss.

## 2. Classes and target intervals (copied from E_FREE; margins re-derived by hand in DERIVATION.md section 6)
| class | f_ret (source) | f_loss | needed free mass | F interval |
|---|---|---|---|---|
| E early types, log M* 10.8 | 0.10-0.18, N 5.6-10 (CFG804) | 0.8214-0.9000 | 0.55-0.80 M* inside 100 kpc (CFG745) | [0.0114, 0.0324] |
| C clusters | 0.636-0.686 (CFG814 measured outskirt slope) | 0.314-0.364 | 1.9-4.5 M_b (X-COP, CFG745) | [0.619, 1.0] (raw upper 1.83 cut by F <= 1) |
| other cluster retention values in the record, for the "is it consistent" test | 0.90 census median (CFG813); 0.60 pinned by an artefact (CFG812) | 0.10; 0.40 | | |
| A5 late types / SPARC | same census as E at the same catchment mass (CFG811: early types retain only 1.5x less, PROVISIONAL, quoted from memory there) | | zero free mass | F = 0 |

## 3. Questions and pass rules (classes and rules fixed before the numbers are compared)
- **Q1 tautology.** F(f_loss) is VACUOUS iff F is defined from f_loss (F = f_loss, or M_free defined through f_ret) or iff the quantity mapped
  (U) is defined as the free mass. Procedure: read the definitions in section 1 and the E_FREE files; state exactly which inputs enter the numerator
  (M_needed) and which the denominator (S). Also test the identification "tether-unbound = free" against CFG749, CFG776, CFG812.
- **Q2 derived F_dyn(f_loss, r/r_M).** Derive, from the energy integral E = v^2/2 + Phi_eff(r; m) with unbound iff E >= 0: (a) sudden loss, (b) adiabatic
  loss; limits f_loss -> 0, -> 1; which dimensionless numbers other than f_loss survive; whether an extra scale (M_OF = 10^13.03 M_sun of CFG721, or any
  other) is produced or needed.
- **Q3 comparison.** Evaluate the derived F_dyn at each class's OWN record f_loss (section 2) and ask the inverse question: what f_loss would the formula
  need to reach each class's F interval, and is that f_loss inside the record's census range?

Verdicts (decided by these rules, not after looking):
- **REDUCTION**: a derived F_dyn(f_loss, r/r_M) with no new constant, (i) giving F in the E interval at the E f_loss AND in the C interval at the C f_loss,
  (ii) the unbound-to-free identification itself derived (not defined), (iii) not contradicting A5 (late types F = 0 at their f_loss).
- **PARTIAL**: derived exactly for one regime (sudden or adiabatic) or one class, the rest not.
- **NO REDUCTION**: any one of: (a) F identical to f_loss by definition; (b) a new constant or scale is needed; (c) the f_loss needed for either class is
  outside the record's census values listed in section 2; (d) monotone ordering wrong: the rule needs F_C > F_E at f_loss,C < f_loss,E with F increasing in
  f_loss; (e) the unbound-to-free identification is a postulate.
- **NOT DIAGNOSTIC**: the derivation cannot be completed by hand.
- Overall lane label (E_FREE vocabulary): CONSTRAINT TIGHTENED if a branch is killed or a postulate shown to be needed; NO RESULT otherwise.

## 4. Error-catching checks (decided now)
- **C1 dimensions.** Every formula restored to physical units once (energy V_flat^2, r in r_M, t in t0).
- **C2 limits.** p -> 1 (shell at the bottom of its well, apocentre -> pericentre, period -> small-oscillation period); p -> 3 (energy -> 0, apocentre -> infinity);
  p -> infinity.
- **C3 second derivation routes.** (i) the marginal case p = 3 integrated directly from the equation of motion against the energy integral; (ii) the apocentre root
  substituted back into the energy equation for two values of p; (iii) the half-period computed by direct quadrature of dt = dr / v at p = 1.5 and 2 and compared with
  the small-oscillation period in the p -> 1 limit; (iv) the adiabatic energy obtained twice, once from the equilibrium-tracking shell, once by integrating dH/dt = dPhi/dM_b.
- **C4 rank-Hamiltonian identity.** The CFG747/776 discrete energy rewritten by Abel summation as a sum of per-rank energies; checked against the script's own energy().
- **C5 scale invariance.** (r, m, E) -> (lambda r, lambda m, E / lambda) maps solutions to solutions, so r/r_M can enter only through the numerical inner core.
- **C6 record cross-check (order of magnitude only).** Half-swing times against CFG776's quoted expulsion time, 50-100 t0 at 5-11 r_M.
- **C7 numerical cross-check script** `cfg837_shell_check.py` is WRITTEN, NOT RUN, UNTESTED; it is QUEUED behind the live 1024^3 run. Nothing in the verdict depends on it.
- **C8 coincidence guard.** Any near-equality of a derived threshold to a record number (for example a mass scale) is checked for common variable and common
  construction before it is allowed to be called a finding.

## 5. Trial count
Five derivation items are reported: T1 tautology audit; T2 sudden single-shell threshold; T3 adiabatic; T4 crossing (rank-energy bound and ordering);
T5 class comparison. No parameter is scanned or tuned; the only numbers that enter are those in section 2 and the units of section 1.
