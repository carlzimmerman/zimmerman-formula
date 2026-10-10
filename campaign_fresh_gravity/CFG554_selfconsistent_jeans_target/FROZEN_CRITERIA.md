# CFG554 FROZEN CRITERIA -- the self-consistent Jeans target of the velocity part, from a principle (no knobs)

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-10.

## Question

CFG544 (criteria b6eb542c5): FIX-2 = two-sided position drift + Ornstein-Uhlenbeck velocity relaxation at rate alpha/tau toward
an isotropic Maxwellian with sigma_J^2(r) = (1/rho_c) int_r^R rho_c g dr' (isotropic Jeans dispersion of the CURRENT cold-energy
density in the CURRENT Newtonian field of real mass, baryons + cold energy) passes the kinetic gate in all 4 cells, but its
target is POSITED. CFG550 (criteria 2717e0197): the phase-space lift with the law's phantom as reference DERIVES T = V_f^2/2 but
FAILS (edge heating, spill, cluster blow-up); the metriplectic velocity block (pairs at fixed x, partner compensation) has
M symmetric PSD, M dE = 0, dS >= 0 for ANY reference measure, so the structure does not select the target. This lane asks
whether a principle selects the self-consistent (current-density) Jeans target, with no constant beyond G, alpha (O(1) FREE,
= 1 here; robustness x0.5 / x2), tau = (4 pi G rho_m)^(-1/2) and the local state.

Settings: kappa = 1/2 FITTED; footings 9.3603e-11 (can) and 1.1312e-10 (alt), judged separately, never pooled; kernel
nu(y) = 1/(1 - exp(-sqrt y)); candidate B; G9 (only real mass gravitates: the Jeans field is baryons + cold energy, never the
phantom); no EFE; MS1. The cold energy's MASS is still required. No dark-matter particle species. Not "theory closed".
Read-only use of CFG541/542/544/550 (no file there is edited). No PM runs, no downloads. Compute: `nice -n 10`, <= 4 processes.

## Routes (declared now)

**(a) Maximum entropy at fixed density, constrained by the exact kinetic stationarity (primary).** The velocity block acts at
fixed x, so its accessible states have rho_c(x) fixed. Maximise S_B = -int f ln f subject to (i) int f d^3v = rho_c(x) for all
x, (ii) the tensor Jeans condition J_i(x) = d_j Pi_ij + rho_c d_i Phi = 0 for all x (Pi_ij = int f v_i v_j d^3v; J = 0 is
d_t(rho u)|_Vlasov = 0, the exact moment-level stationarity of the reversible flow at the current density), Phi the current
Newtonian potential of baryons + cold energy. Multipliers mu(x), lambda_i(x). sympy items:
- S1a: the maximiser is a Gaussian in v with inverse covariance -2 sym(grad lambda) (no temperature inserted);
- S1b: spherical symmetry, lambda = lambda(r) r_hat: sigma_r^2 = -1/(2 lambda'), sigma_t^2 = -r/(2 lambda) per tangential
  component; isotropic iff lambda proportional to r, i.e. iff isothermal;
- S1c: SIS check: rho = V_f^2/(4 pi G r^2), g = V_f^2/r: lambda = -r/V_f^2 solves the constraint, sigma^2 = V_f^2/2;
- S1d: second variation -int (delta f)^2/f < 0 on a linear constraint set: the maximiser is unique when it exists;
- S1e: the integrated constraint int r.J = 0 is the virial theorem 2K = int rho_c r.grad Phi (by parts): a total-energy
  constraint is redundant;
- S1f: with an extra isotropy constraint (Pi_rr = Pi_tt) or with the scalar (fluid) hydrostatic constraint
  grad(tr Pi/3) + rho grad Phi = 0 in place of (ii), the maximiser is the isotropic Maxwellian at sigma_J^2 = FIX-2's target.
  The scalar constraint is the Euler-fluid statement, not the exact Vlasov moment; this is recorded as the extra assumption
  that FIX-2's isotropy needs.
The radial problem: with Lambda = -lambda > 0, P = rho sigma_r^2: Lambda' = rho/(2P), P' = -rho g - 2P/r + rho/Lambda,
isotropic start Lambda = c r_in, P = rho_in/(2c) at the inner face of the innermost occupied bin, outer condition P = 0 at the
outer face R of the outermost occupied bin inside r_ta; c by shooting (vectorised bracket refinement; the positive side of the
bracket is taken). If the shooting does not bracket in a step, that step uses no relaxation for the run's particles and the
step is counted as a solver failure. Numerical scheme (disclosed choice): piecewise-constant rho per bin, g of the current
enclosed mass at bin centres as in FIX-2, RK2 with 8 substeps per bin, recomputed every step.
Bench operator: OU at rate alpha/tau, radial component toward sigma_r^2(r), each tangential component toward sigma_t^2(r).

**(b) FIX-2 as a metriplectic relaxation toward the instantaneous isotropic Jeans projection.** sympy S2 (discrete velocity
cells at one x, reference p*[rho] depending on the state through rho): M symmetric PSD, M dE = 0 with the partner, dS/dt a sum
of squares, mass exact, stationary iff p_c = p*; the rho-dependence of p* adds only a v-independent term to dS/df (so it does
not move the velocity equilibrium) and vanishes at p_c = p* (so the position drift is unchanged on the velocity-equilibrium
manifold). Angular momentum S3: radial component single-particle moves about zero mean; tangential components by
momentum-conserving pair transfers with the partner (M dE = 0 kept): sympy d<v_t>/dt = 0 (mean rotation kept), d<v_r>/dt =
-gamma <v_r>, stationary states Gaussian with free tangential mean; total j = sum x cross v conserved because radial changes
do not change j. Numeric test (A-num): a rotating 3-D particle set in one shell, 2000 operator steps, total j vector conserved
to <= 1e-10 relative with the per-shell noise-mean subtraction, while CFG544's FIX-2 operator decays it. The spherical bench
stores |v_t| with isotropic orientation, so its total j is zero by construction (disclosed): route (b)'s bench run = FIX-2
exactly. The target of (b) is derived from a principle only through S1f (scalar constraint), so route (b)'s target label is
POSITED unless S1f's assumption is shown forced (it is forced only for isothermal rho by S1b).

**(c) forced alternative: maximum entropy at fixed density with the GLOBAL (integrated) Jeans constraint only (virial).**
Constraint int r.J = 0 alone: the maximiser is an isotropic Maxwellian with a single temperature T_v = int rho_c r g / (3 M)
over the cold energy inside r_ta (current state, recomputed every step). Bench operator: OU toward T_v (isotropic).

## Bench (CFG544 toy imported unchanged from `../CFG544_settling_kinetic_consistency/cfg544.py`, read only)

Same N = 30000, eps, RMIN, 100 bins, seed 544, dt, Vlasov integrator, drift step (two-sided, FIX-1), energy accounting; only the
velocity step's target changes. alpha is set per job in the imported module (robustness runs only). Cells: MW-like and
cluster-like x can / alt. Runs: routes a and c: IC-B 10 Gyr, IC-C 5 Gyr, overfill pair (IC-E baseline and IC-E + 0.3
M_ph(<0.3 r_*)) 5 Gyr. Route b: FIX-2 IC-B 10 Gyr, IC-C 5 Gyr (= control C5), overfill pair 5 Gyr. Robustness: routes a and b,
alpha = 0.5 and 2, IC-B and IC-C, all cells.

**Gate G550 (CFG550's, per cell, per run IC-B and IC-C):** |D| <= 0.1 AND |log10 X_J| <= 0.1 at the end, AND both changed by
<= 0.05 dex over the last 2 Gyr (X_J against the isotropic Jeans dispersion of the current density; by the virial theorem the
global X_J does not depend on anisotropy). CFG544's sharp-edge gate reported alongside.
**Edge:** PRESERVED iff -0.1 <= ln(r_99/r_99,analytic) <= C2_cell + 0.1 for IC-B and IC-C in all 4 cells, C2_cell = +0.255 /
+0.333 / +0.445 / +0.539 (CFG544 JSON, MW can / MW alt / cluster can / cluster alt).
**Overfill:** P (CFG544 definition) at 5 Gyr; HANDLED iff P <= 0.2 in all 4 cells.
**Energy:** sink = -(drift work + relaxation work) per M_cat V_f^2; gross out (drift) and in (relaxation) reported.
COMPATIBLE iff IC-B net in [0, 1.0] and IC-C whole-history net (CFG541 dW_per_mass/V_f^2 + IC-C net) in [0, 1.0], all cells;
the last-2-Gyr rate reported (two-way throughput allowed by M, reported as such).
**Blow-up:** any snapshot with cumulative gross relaxation input > 10 V_f^2 per M_cat or a particle speed > 50 V_f. None
allowed (CFG550's cluster failure must not recur).
**Feasibility (route a):** solver failures <= 1% of steps in every run.
**Robustness:** G550 passes at alpha = 0.5 and 2 (IC-B, IC-C, all cells).
**Lyapunov (full system: Vlasov + drift + relaxation):** ESTABLISHED only if sympy proves dL/dt <= 0 for all states for some
L; else NOT ESTABLISHED with cross terms shown; numerically, the largest rise of F along bench runs is reported.
Also reported (S4): whether the route-a maximiser is an exact Vlasov steady state (it is iff ln f = -beta E - gamma L^2 + c).

## Controls (all must pass, else no label)

- C2: IC-E pure Vlasov 2 Gyr passes the end gate in all 4 cells.
- C5: FIX-2 IC-C end state (logX, D) reproduces CFG544's JSON to 1e-6 in all 4 cells (import unchanged).
- C6: the route-a solver on a Gaussian density rho ~ exp(-r^2/2T) in the harmonic field g = r (T = 1, R = 8, same bin
  construction) returns sigma_r^2/T and sigma_t^2/T within 2% for r <= 3 (isothermal => isotropic, S1b).
- mass exact in every run.

## Labels (per route)

- **DERIVED:** target from a principle with no inserted assumption beyond the stationarity of the reversible flow (route a:
  S1a-e pass; route c: its maximiser), S2 pass, feasible, G550 all cells IC-B and IC-C, no blow-up, energy COMPATIBLE,
  overfill HANDLED, edge PRESERVED, angular momentum conserved (S3 + A-num), robustness pass, Lyapunov ESTABLISHED.
- **DERIVED WITH OPEN ITEMS:** target from a principle, S2, feasible, G550 (alpha = 1, all cells, IC-B and IC-C), no blow-up,
  energy COMPATIBLE; each other failed item (overfill, edge, angular momentum, robustness, Lyapunov) listed as open.
- **POSITED:** the target needs an inserted assumption (route b: isotropy / scalar closure, S1f), whatever the bench says;
  the structural result (S2, S3) and the bench verdict are attached.
- **INCONSISTENT:** the derived target is infeasible, or fails G550 in any cell (alpha = 1), or blows up, or energy is not
  COMPATIBLE.
- Lyapunov ESTABLISHED / NOT ESTABLISHED attached to every label.

## MUTATE (`CFG554_MUTATE=1`, writes `_MUTATE` outputs, exit 1 if all teeth bite)

- MT: route-a target x 2 (both components) on IC-C: must FAIL G550 in all 4 cells.
- MJ: Jeans constraint removed. With the zero-entropy partner the multiplier is then undetermined (beta = 0, CFG550 b1); the
  only knob-free reference left is the law's phase-space phantom, T_ph (CFG550 a1). Route-a operator toward T_ph (isotropic)
  on IC-C 5 Gyr: must fail (G550 fails OR edge outside the allowance OR blow-up) in all 4 cells.
- MK: sink removed: sympy M dE != 0 for the velocity transfers without the partner component; bench route a IC-C MW can 2 Gyr:
  matter energy changes by > 1e-2 |E_0| beyond the integrator error.

## Reporting

`cfg554.py` -> `cfg554.out`, `cfg554_results.json`; MUTATE -> `cfg554_MUTATE.out`, `cfg554_results_MUTATE.json`; `README.md`;
`VELOCITY_PART_v2.md` (the equations). Every number quoted from the JSON. Corrections after this commit are dated
disclosures; this text is not edited.
