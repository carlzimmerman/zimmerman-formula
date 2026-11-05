# AC5 frozen criteria: AC3's slow modes on a background where the clock keeps rolling

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED;
not theory closed. Adopts nothing. Candidate: AC2 (single canonical clock,
smooth unswitched stiffness), via the shared P=0 quadratic block.

## Why AC5

AC4 (README) returned NO VERDICT and showed its test had no power: on a
constant potential the clock stops rolling (eps_phi ~ a^-6), modes leave the
horizon, and the flipped-stiffness control did not bite. AC5 changes only
the background, so that the clock keeps rolling, and adds a power gate.

## Background

Exponential clock potential V(phi) = V0 exp(-lambda phi), M = 1. In unitary
gauge the reduced quadratic Lagrangian `Lred` of
action_scale_investigation_2026_11_05/single_clock.py depends on the
background only through a, H, eps_phi, v (V enters through the Friedmann
identity it already uses), so the same Lred applies. Only the flow changes:

    a' = aH,  H' = -eps H^2 - v^2/2,  v' = -3Hv,
    eps' = 2 eps ( -3H + lambda V / (sqrt(2 eps) H) - H'/H ),
    V = (3 - eps) H^2 - v^2/2.

lambda = 0 is AC4's flow exactly. Per case, lambda = sqrt(2 eps_phi0), the
scaling-attractor value, so eps_phi stays near its starting value instead
of decaying. Matter is AC3/AC4's canonical stiff scalar (v ~ a^-3).

## Cases, equation, control, graded quantity

Unchanged from AC4 FROZEN_CRITERIA.md: all 81 AC3 finite cases (8 witnesses
primary), K qddot + (Kdot + B - B^T) qdot + (Bdot - P) q = 0 with Bdot - P and
Kdot simplified exactly (AC4 evolve.py), families I (Z=1) and II (C=1), GR
control cY = 0, R = max_t ||q||_inf / max_t ||q_GR||_inf (dense output, 8
points per step), window a = 1 to a = e^5, DOP853 rtol 1e-9 and 1e-11.

## Lines (stated before running)

- Convergence: R agrees between the two tolerances to 1e-3 relative.
  Changed from AC4's 1e-4 because AC4 measured a sampling floor of about
  2e-4 for max-over-oscillation (evidence_diag_tolerance.json there). A case
  missing it is NO VERDICT.
- Known answer: Omega(u,w) conserved, drift <= 1e-6 on every main/control run.
- Known answer: with lambda = 0, this code reproduces AC4's main R for
  cases (.05,.3,.001,10) and (.05,.3,.001,100) to 1e-8 relative.
- POWER GATE: the M2 flipped-stiffness twin must reach R >= 1e3 on at least
  one witness. If it does not, the label is NO VERDICT (no power), whatever
  the main run shows.
- PASS: power gate met, every case converged, Omega line met, R <= 10 on
  every main case.
- FAIL: R >= 1e3 on any converged main case.
- UNDECIDED: otherwise (10 < R < 1e3 somewhere).

Power is reported per witness and per eps_phi: a pass only covers the
eps_phi values where M2 bit.

## Negative controls (separate outputs)

- M1: drop Kdot; Omega conservation must fail on at least one witness.
- M2: the source's --mutate sign (flipped polarization stiffness); the
  power gate above.

## Scope stated now

A PASS says: on rolling-clock exponential backgrounds, at the eps_phi where
the control shows power, AC3's slow frozen roots do not amplify beyond GR.
It is not nonlinear health, sourced backgrounds, Solar-System/galaxy/lensing
regrades, a derivation of xi or kappa, or adoption of AC2.
