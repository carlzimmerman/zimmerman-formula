# CFG550 FROZEN CRITERIA -- the velocity part of the settling dynamics, derived from a principle (no knobs)

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-10.

## Question

CFG544 (criteria b6eb542c5, results c2be5aa17): class-A settling moves cold energy in position only, so the settled cold
energy keeps sigma = 0, collapses radially and overfills the core; the derived two-sided deficit (FIX-1) pumps energy in;
an Ornstein-Uhlenbeck relaxation toward the Jeans dispersion of the current density (FIX-2) passes every test but its target
temperature is POSITED. This lane asks whether the velocity-space part of the settling, relaxation AND target, follows from
the same statement as the position drift (CFG542 Pb: dz/dt = L dE + M dS, M dE = 0, coherent zero-entropy partner phi),
with no constant beyond G, alpha (O(1) FREE, = 1 here, CFG541/542), tau = (4 pi G rho_m)^(-1/2), the local state, and the
law's own inputs that class A already takes (rho_ph and the baryons, hence g_law = G (M_b + M_ph)(<r)/r^2 and Phi_law).

Settings: kappa = 1/2 FITTED; footings 9.3603e-11 (can) and 1.1312e-10 (alt), judged separately, never pooled; kernel
nu(y) = 1/(1 - exp(-sqrt y)); candidate B; G9; no EFE (round per-region phantom); MS1 (the switch reads baryons). The cold
energy's MASS is still required. No dark-matter particle species. Not "theory closed". Read-only use of CFG539/541/542/544
(no file there is edited). No PM runs, no downloads. Compute: `nice -n 10`, <= 4 processes.

## Routes (declared now)

**(a0) strict kinetic GENERIC.** S must satisfy the degeneracy L dS = 0, i.e. S is a Vlasov Casimir, S = -int C(f_c).
Velocity-space transfers at fixed x, compensated by the partner (M dE = 0). sympy: the stationarity condition and whether a
normalisable f_c with a finite temperature exists; and the alternative with matter-internal energy-conserving pair
transfers (Landau type, no partner): which temperature it relaxes to.

**(a1) reference-measure lift (primary).** The law fixes (rho_ph, Phi_law) per region; its phase-space form is the isotropic
ergodic DF f_ph(E_law) of the UNTRUNCATED phantom in Phi_law (Eddington). Velocity part of S:
S_v = -(1/Theta) int rho_c T_ph KL( p_c(.|x) || p_ph(.|x) ) d^3x, with p_ph = f_ph/rho_ph and T_ph(x) its second moment,
T_ph(r) = (1/rho_ph) int_r^inf rho_ph g_law dr' (isotropic Jeans of the untruncated phantom in the law's field). M built
pair-wise in velocity at fixed x with the partner compensation (e_v' - e_v, -(v'^2 - v^2)/2), mobility rate alpha/tau.
Continuum: Fokker-Planck / OU toward T_ph at rate alpha/tau (Maxwellian moment closure of p_ph in the toy; disclosed).
Position part: FIX-1 two-sided deficit against rho_ph (as CFG544).

**(b) Lynden-Bell / maximum entropy in the law's potential, temperature as a Lagrange multiplier.** (b1) with the coherent
partner (energy freely exchanged, dS/d eps_phi = 0): is beta = 1/T fixed? (b2) closed (sink removed): T fixed by energy
conservation of CFG541's reservoir-to-settled history; compare with the required K_f (CFG541 JSON: dW_per_mass,
Kf_per_mass, read only); a mismatch > 0.1 dex in sigma^2 means wrong temperature. (b3) LB with the phantom's own occupation
cap eta = f_ph: the only beta values that add no constant are beta = 0 and beta = infinity; report both limits.

**(c) forced alternative: phase-space inside-out fill (the beta -> infinity limit of b3).** One-sided phase-space deficit
max(f_ph - f_c, 0) with chemical potential E_law: at fixed supply M_cat the minimiser is the bathtub
f_t = f_ph(E) Theta(E_t - E), E_t fixed by M_cat (no constant). Its density marginal rho_t and second moment T_t(r) are the
targets: velocity relaxation (OU in the Maxwellian closure, truncated at v_t(r) = sqrt(2 (E_t - Phi_law(r))) by a
Gaussian-reversible OU proposal with rejection outside v_t; pure friction where v_t = 0) and the two-sided position drift
against rho_t (the density marginal of the same phase-space deficit). The softened edge of rho_t is a prediction.

## Analytic checks (sympy where possible)

- **A1 target emerges.** SIS (Phi_law = V_f^2 ln r, rho_ph = V_f^2/(4 pi G r^2)): f proportional to exp(-E/T) reproduces
  rho_ph iff T = V_f^2/2 (and its amplitude); the Jeans integral gives V_f^2/2. No temperature inserted. Deep untruncated
  T_ph/V_f^2 = 0.5 within 2% in every cell (numeric).
- **A2 GENERIC structure (a1, c).** Discrete velocity-cell model: M symmetric PSD, M dE = 0, dE/dt = 0, dS/dt >= 0,
  stationary iff p_c = p_ph; mass exact; continuum limit = OU/Fokker-Planck with friction alpha/tau and target T_ph.
- **A3 energy-exchange sign.** Rate of energy from phi to matter = gamma int rho_c (3 T_target - <v^2>): sign allowed both ways
  by M (dS >= 0 for either sign)?
- **A4 Eddington existence.** f_ph >= 0 for the untruncated phantom in Phi_law, each cell: necessary condition rho_ph
  monotone in Psi (decreasing in r); numeric Eddington inversion min f / max f. If it fails, the isotropic lift does not
  exist in that cell (reported; the moment closure T_ph is still defined).
- **A5 Lyapunov (full system: Vlasov + drift + relaxation).** Candidates: F; F + c F_v (c >= 0); E_N - T S_B; E_N + Casimirs;
  the phase-space KL relative to f_ph; F - T_ph H. ESTABLISHED only if sympy proves dL/dt <= 0 for all states for some L;
  else NOT ESTABLISHED, with the cross terms shown (and, numerically, any rise of F or F + F_v along a bench run).
- **A6 angular momentum.** Does the velocity part conserve each element's / the total j? (sympy)
- **A7 causality.** Any new propagation or speed bound on alpha; largest particle speed / c in the bench.

## Bench (the CFG544 spherical N-body toy, imported unchanged from `../CFG544_settling_kinetic_consistency/cfg544.py`)

Same N = 30000, eps, RMIN, 100 bins, alpha = 1, seed 544, dt, Vlasov integrator (individual substeps, correction 1), drift
step, energy accounting; only the velocity step's target (and, for route c, the deficit's target density) is changed.
Cells: MW-like and cluster-like x can / alt. Runs per bench variant (a1, c): IC-B 10 Gyr, IC-C 5 Gyr, overfill pair
(IC-E baseline and IC-E + 0.3 M_ph(<0.3 r_*) injection) 5 Gyr. Controls re-run: C2 (IC-E pure Vlasov 2 Gyr) and
C5 = reproduce CFG544's FIX-2 IC-C end state (logX, D) in all 4 cells to 1e-6 (proves the import is unchanged).

**Gate G550 (per cell, per run IC-B and IC-C):** |D| <= 0.1 (T1 vs rho_ph, median of 16 log bins in 0.1-0.9 r_*) AND
|log10 X_J| <= 0.1, where X_J = sum m v^2/3 / sum m sigma_J^2(r_i), sigma_J^2 the isotropic Jeans dispersion of the CURRENT
cold-energy density in the current field (a stationarity test, not a target), AND both changed by <= 0.05 dex over the last
2 Gyr. CFG544's frozen kinetic gate (X against the sharp-edge truncated sigma_eq) is reported alongside for comparability.

**Edge:** PRESERVED (with kinetic softening) iff -0.1 <= ln(r_99/r_99,analytic) <= C2_cell + 0.1 for IC-B and IC-C in all 4
cells, with C2_cell the pure-Vlasov softening from CFG544's JSON (+0.255 / +0.333 / +0.445 / +0.539 for MW can / MW alt /
cluster can / cluster alt). Route c: also ln(r_99,rho_t / r_99,analytic) (the derived softening) is reported.
**Overfill:** P (CFG544 definition) at 5 Gyr; HANDLED iff P <= 0.2 in all 4 cells.
**Energy:** sink = -(drift work + relaxation work), per M_cat V_f^2; gross out (drift) and gross in (relaxation) reported.
COMPATIBLE iff IC-B net in [0, 1.0] and IC-C whole-history net (CFG541 dW_per_mass/V_f^2 + IC-C net) in [0, 1.0], all cells;
rate over the last 2 Gyr reported (a steady two-way throughput is reported as such).

## Labels (per route)

- **DERIVED:** A1 and A2 pass, G550 passes in all 4 cells on IC-B and IC-C, energy COMPATIBLE, overfill HANDLED, edge
  PRESERVED, A4 holds in all cells, angular momentum conserved, Lyapunov ESTABLISHED.
- **DERIVED WITH OPEN ITEMS:** A1, A2, G550 (all cells, IC-B and IC-C) and energy COMPATIBLE pass; every other failed item
  (overfill, edge, A4, angular momentum, Lyapunov) listed as open.
- **POSITED:** the route yields no finite target temperature unless one is inserted (T free / multiplier undetermined).
- **INCONSISTENT:** the route's structure gives no finite or a wrong temperature (T -> infinity, T fixed at the source
  value sigma = 0, or fixed but off by > 0.1 dex in sigma^2), or the derived target fails G550 in any cell.
- Lyapunov: ESTABLISHED / NOT ESTABLISHED, attached to every label.

## MUTATE (`CFG550_MUTATE=1`, writes `_MUTATE` outputs, exit 1 if all teeth bite)

- MT: target temperature x 2 (a1 and c) on IC-C: must FAIL G550 in all 4 cells.
- MS: entropy functional sign flipped: sympy dS/dt <= 0 (H-theorem broken) and a velocity-space Fokker-Planck run in one bin
  shows the KL to the target growing.
- MK: sink removed (no partner): sympy M dE != 0 for the velocity transfers, and in a bench IC-C run (MW can, 2 Gyr) the
  matter energy changes by > 1e-2 |E_0| beyond the integrator error (energy not conserved without the partner).

## Reporting

`cfg550.py` -> `cfg550.out`, `cfg550_results.json`; MUTATE -> `cfg550_MUTATE.out`, `cfg550_results_MUTATE.json`;
`README.md`; `VELOCITY_PART.md` (the equations). Every number quoted from the JSON. Corrections after this commit are dated
disclosures; this text is not edited.
