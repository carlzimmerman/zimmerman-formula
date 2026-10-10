# CFG558 FROZEN CRITERIA -- velocity part: is isotropy forced, overfill removal, alpha-robustness by the age

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-10.

## Starting point (read only: CFG516, CFG541, CFG542, CFG544, CFG550, CFG554)

CFG554 (criteria 01ad75492): (b) FIX-2 = two-sided drift (FIX-1) + Ornstein-Uhlenbeck relaxation at rate alpha/tau toward the
isotropic Jeans dispersion sigma_J^2 = (1/rho_c) int_r^R rho_c g dr' of the CURRENT cold-energy density in the CURRENT field of
real mass is a valid metriplectic relaxation (S2: M symmetric PSD, M dE = 0 with the zero-entropy partner phi, dS >= 0;
S3: angular momentum conserved by momentum-conserving pairs) and passes G550 in all 4 cells, but its isotropic target is the
entropy maximiser only with the SCALAR hydrostatic constraint (S1f) instead of the exact TENSOR Jeans moment (route a, which
fails in clusters). FIX-2 fails at alpha x 0.5 (still evolving at 10 Gyr) and does not remove overfill (P 0.30-0.43).

Settings: kappa = 1/2 FITTED; footings 9.3603e-11 (can) and 1.1312e-10 (alt), judged separately, never pooled; kernel nu_mono
(the bench imports CFG544's kernel, equal to nu_mono at the toy's y; disclosed, as in CFG544/554); candidate B; G9 (only real
mass gravitates: every Jeans field is baryons + cold energy, never the phantom); no EFE; MS1. The cold energy's MASS is still
required. No dark-matter particle species. Not "theory closed". No PM runs, no downloads. Compute: nice -n 10, <= 4 processes.
No constant beyond G, alpha (O(1) FREE), tau = (4 pi G rho_m)^(-1/2), the law's rho_ph and the local state.

## Q1 -- is the isotropic (scalar) constraint FORCED? (sympy + toy)

sympy items:
- I1 (equivariance): delta E/delta f = v^2/2 + Phi, delta S_B/delta f = -ln f - 1, and the position-block drive delta S/delta f
  = -psi/Theta (round psi, CFG541/542) are invariant under v -> R v at fixed x (R orthogonal); so the velocity block of M
  (pairs at fixed x, partner taking Delta(v^2/2)) and the position block are SO(3)_v-equivariant. The position block is
  v-independent (couples to the zeroth moment only); the velocity block couples to the second moment only through
  Delta(v^2/2), i.e. the trace.
- I2 (invariant linear constraints): the general symmetric 3x3 A with R A R^T = A for the rotation generators is A = a I
  (sympy solve), so every SO(3)_v-invariant linear constraint on Pi_ij is a constraint on tr Pi.
- I3 (invariance theorem, Gaussian family): S_B of a Gaussian at fixed tr C is maximised at C = (tr C/3) I (sympy).
- I4 (what the bracket alone imposes): maximise S_B at fixed rho(x) and fixed tangential momentum (the quantities the velocity
  block conserves; energy is taken by the zero-entropy partner, so no energy multiplier): the stationary point
  f = exp(-1 - mu - eta.v) is not normalisable (sympy: the integral diverges). So the dissipative bracket alone supplies NO
  temperature profile; the profile must come from the reversible flow L (Vlasov), whose exact moment stationarity is TENSOR.
- I5 (tensor multiplier term): the route-(a) term d_j lambda_i Pi_ij is SO(3)_v invariant iff sym grad lambda is proportional
  to I, i.e. iff lambda' = lambda/r (isothermal) (re-derives CFG554 S1b on this lane's footing).
Toy items: (T-iii) the realised end states of the Q2 version are reported with their measured anisotropy beta and the TENSOR
Jeans residual of the particle state (median |resid| over shells 0.1-0.9 r_*, resid = [P_r' + 2(P_r - P_t)/r + rho g]/(rho g)),
to show whether the full dynamics keeps tensor balance with an isotropic reference.

**Label rule (Q1):** ISOTROPY FORCED iff I1-I5 pass AND the counter-argument (iii) is refuted STRUCTURALLY, i.e. the tensor
constraint is shown inconsistent with a committed structural requirement of the framework (Pb's GENERIC conditions, the round
rule, G9, the CFG550/554 velocity block), not merely with the bench. A bench failure of the tensor route (CFG554 clusters,
MUTATE MI below) does not refute it structurally: then the scalar constraint is SELECTED by the bench and the label is
ISOTROPY CHOSEN (with the reduction to a single stated principle reported).

## Q2 -- overfill removal, no knob (the "Q2 version", V3)

Rule declared now. Drift: CFG544 two-sided (FIX-1), unchanged. Velocity relaxation: OU at rate alpha/tau (radial about zero,
tangential as CFG544/554; spherical bench stores |v_t|, J = 0 by construction) toward the ISOTROPIC target

    rho_hat = min(rho_c, rho_ph)                    (the T1-admissible part of the current density, per bin)
    P_hat(r) = int_r^R rho_hat g dr'                (g = field of the CURRENT real enclosed mass, baryons + all cold energy, G9)
    sigma_*^2(r) = P_hat(r) / rho_hat(r)            (the hydrostatic temperature of the admissible density)

with the same bin/face construction as CFG544's ou_step (piecewise-constant rho per bin, g at bin centres from the current
enclosed mass, face cumulative sum, bin-centre average). Where rho_c <= rho_ph at and outside r, sigma_*^2 = FIX-2's sigma_J^2
exactly. In an overfilled region the actual pressure is q P_hat (q = rho_c/rho_hat >= 1); the net force density on the cold
energy is -P_hat grad q, so the overfill expands by its own excess pressure; the energy comes from the sink (two-way exchange
allowed by Pb's M). rho_ph enters only as the T1 comparison density, never in Phi (G9).
sympy: S2' -- for a NONLOCAL state-dependent reference p*[rho] (two sites, p* at site 1 depending on rho at both sites) the
extra term in delta S/delta f is v-independent and equals T0/Theta at p_c = p* (so CFG554 S2 carries over); C8 numeric
identity: on rho_c = rho_ph (cap inactive) sigma_*^2 equals FIX-2's sigma_J^2 to machine precision.

**Overfill test (CFG544 definition, unchanged):** IC-E baseline and IC-E + 0.3 M_ph(<0.3 r_*), alpha = 1, P at 5 Gyr.
**OVERFILL HANDLED** iff P <= 0.2 in all 4 cells (MW, cluster x can, alt) AND V3 passes G550 at alpha = 1 on IC-B (10 Gyr) and
IC-C (5 Gyr) in all 4 cells with edge PRESERVED and energy COMPATIBLE (CFG554 definitions, allowances C2_cell = +0.255 /
+0.333 / +0.445 / +0.539). Else NOT HANDLED (reasons listed).

## Q3 -- alpha-robustness by the age

V3 at alpha = 0.5, 1, 2 (x the default 1), IC-B and IC-C, all 4 cells, run to 15 Gyr; snapshots every 0.25 Gyr; reported at
10, 13.8 and 15 Gyr. Gate at t = 13.8 Gyr (the snapshot nearest 13.8): |log10 X_J| <= 0.05 AND |D| <= 0.05 AND both changed by
<= 0.05 dex over the preceding 2 Gyr AND edge -0.1 <= ln(r_99/r_99,analytic) <= C2_cell + 0.1. **alpha-ROBUST (by the age)**
iff the gate passes for all 3 alphas x 2 ICs x 4 cells; else NOT (failing run-cells listed).
Settling time t90(alpha, run): for x in {D, log X_J} with |x_0 - x_15| >= 0.05, the earliest snapshot time after which
|x(t) - x_15| <= 0.1 |x_0 - x_15| holds at every later snapshot; t90 = the max over those x. Also t_band: earliest time after
which |D| <= 0.05 and |log X_J| <= 0.05 hold at every later snapshot (None if never).

## Checks (reported; those marked * enter the labels)

G9 (target field = real mass only)*; energy with sink (IC-B net in [0, 1], IC-C whole-history in [0, 1] V_f^2 per M_cat,
alpha = 1)*; H-theorem of the dissipative sub-flow: (sympy S2' + CFG554 S2) and numerically the per-shell moment KL to the
target, sum over occupied bins inside r_ta of rho V (3/2)(s/sigma_*^2 - 1 - ln(s/sigma_*^2)) with s the bin's mean
(v_r^2 + v_t^2)/3, evaluated immediately before and after the velocity step at every snapshot: report the fraction of
snapshots where it decreases; full-system Lyapunov: ESTABLISHED only if sympy proves dL/dt <= 0 for all states, else NOT
ESTABLISHED*; T1/edge with kinetic softening (allowances above)*; angular momentum (CFG554 S3 + its rotating-shell numeric
test re-run)*; integrator error and blow-up (CFG554 definitions; none allowed)*; mass exact*.

## Controls (all must pass, else no label)

- C2: IC-E pure Vlasov 2 Gyr passes the end gate (|log X| <= 0.1, |D| <= 0.1) in all 4 cells (as CFG554).
- C5: V3's code with the cap disabled (rho_hat = rho_c) on IC-C 5 Gyr reproduces CFG544's fix2_C end state (logX, D) to 1e-6
  in all 4 cells.
- C8: the identity above.
- mass exact in every run.

## Labels

- ISOTROPY FORCED / CHOSEN (Q1 rule).
- OVERFILL HANDLED / NOT (Q2 rule).
- alpha-ROBUST (by the age) / NOT (Q3 rule).
- Overall VELOCITY PART:
  - DERIVED: ISOTROPY FORCED, the overfill rule derived (no inserted assumption), OVERFILL HANDLED, alpha-ROBUST, all * checks
    pass, Lyapunov ESTABLISHED.
  - DERIVED WITH OPEN ITEMS: ISOTROPY FORCED, V3 passes G550 at alpha = 1 (IC-B, IC-C, all cells), energy COMPATIBLE, no
    blow-up; each other failed item listed open.
  - POSITED: ISOTROPY CHOSEN (or the overfill rule needs an inserted assumption), whatever the bench says; bench verdicts and
    structural results attached.
  - INCONSISTENT: V3 fails G550 at alpha = 1 in any cell, or blows up, or energy not COMPATIBLE.
  INCONSISTENT takes precedence over POSITED. The projection rho_hat = min(rho_c, rho_ph) is declared here; whether it counts
  as derived (T1 is the law's inequality, CFG541) or inserted is stated in the README with its reason; if inserted, the overall
  label cannot exceed POSITED.

## MUTATE (`CFG558_MUTATE=1`, writes `_MUTATE` outputs; exit 1 iff all teeth bite)

- MI (tensor constraint swapped in): the route-(a) maximum-entropy anisotropic target of CFG554 (its solver imported unchanged)
  computed on rho_hat in place of the isotropic sigma_*^2, IC-B 10 Gyr alpha = 1, all 4 cells: must FAIL G550 in BOTH cluster
  cells (reproducing CFG554 (a)'s cluster failure).
- MO (overfill rule removed, rho_hat = rho_c, i.e. FIX-2): overfill pair at alpha = 1: P > 0.2 in all 4 cells.
- Reported, not a tooth: alpha x 0.25, IC-B and IC-C, 15 Gyr, all cells: the Q3 gate at 13.8 Gyr and t90.

## Reporting

`cfg558.py` -> `cfg558.out`, `cfg558_results.json`; MUTATE -> `cfg558_MUTATE.out`, `cfg558_results_MUTATE.json`; `README.md`;
`VELOCITY_PART_v3.md`. Every number quoted from the JSON. Corrections after this commit are dated disclosures; this text is
not edited.
