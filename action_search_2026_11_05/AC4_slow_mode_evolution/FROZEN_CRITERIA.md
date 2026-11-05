# AC4 frozen criteria: evolve AC3's slow-mode witnesses on their own background

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED;
not theory closed. Adopts nothing. Candidate action: AC2 (single canonical
clock, smooth unswitched stiffness), via the shared P=0 quadratic block.

## Question

AC3's frozen-frequency check found one negative omega^2 in 8 of 81 cases
(all H*Lstar = 0.001, k_phys/H = 10 or 100; omega^2/H^2 between -0.898 and
-0.167). AC3 itself says frozen roots below H are not a controlled diagnostic
and names the next equation. Do those modes actually grow when the
coefficients evolve with the background?

## Equation (AC3's stated next equation, from the same quadratic Lagrangian)

Same build as AC3 finite_v3.py: reduced ADM Lagrangian `Lred` from
action_scale_investigation_2026_11_05/single_clock.py, with F1 = Rm = 1,
F0 = v^2/2, cY = 1/(1 + Lstar^2 k^2/(2 a^2)) (k comoving), M^2 = 1.
Write L2 = qdot.K.qdot/2 + qdot.B.q + q.P.q/2 with q = (Z, C). Integrate

    K qddot + (Kdot + B - B^T) qdot + (Bdot - P) q = 0

together with the background flow a' = aH, H' = -eps H^2 - v^2/2,
v' = -3Hv, eps' = eps(-6H - 2H'/H) (constant V, canonical stiff matter,
not dust, not realistic late cosmology). Start at a = H = 1 with AC3's
(eps_phi, eps_m, Lstar, k), v = sqrt(2 eps_m). Integrate forward until
a = e^5 (5 e-folds), cap t = 1000/H0.

Initial data, two families per case: (I) Z=1, C=0; (II) Z=0, C=1; both
velocities zero.

## Cases

All 81 AC3 finite cases. The 8 witnesses (negative frozen root) are the
primary set; the other 73 are run so a growth anywhere is not missed.

## Control and graded quantity

GR control: identical run with the polarization term removed (cY = 0),
which AC2 states recovers the canonical two-scalar action exactly.
R = max_t ||q||_inf (candidate) / max_t ||q||_inf (GR control), same
initial data, per family; a case's R is the larger of the two families.

## Lines (stated before running)

- PASS (no amplification beyond GR): R <= 10 on every case.
- FAIL (instability): R >= 1e3 on any case. Over 5 e-folds this needs a
  sustained growth rate above about 1.4 H beyond the GR control.
- UNDECIDED: 10 < R < 1e3 anywhere (Hubble-rate growth; this test cannot
  separate it from ordinary gravitational growth).

## Numerics

- Convergence pair: DOP853 at rtol 1e-9 and 1e-11 (atol 1e-13 relative to
  initial amplitude). R must agree to 1e-4 relative; otherwise that case is
  NO VERDICT and cannot be counted as a pass.
- Known answer (exact, from the Lagrangian): the symplectic product
  Omega(u,w) = u.Pi(w) - w.Pi(u), Pi = K qdot + B q, between families I
  and II is conserved. Line: max |Omega(t) - Omega(0)| / max(|Omega(0)|,
  max_t |u.Pi(w)|) <= 1e-6 on every main and control run.

## Negative controls (separate outputs, must bite)

- M1, wrong equation: drop Kdot from the equation of motion. The Omega
  conservation check must fail on at least one case.
- M2, flipped stiffness: the source's own --mutate sign (polarization term
  with negative sign). Reported; expected to amplify on witnesses. If it
  does not reach R >= 1e3, that is stated, and no line above changes.

## Scope stated now

A PASS says only: on these FRW backgrounds, AC3's slow frozen roots do not
amplify beyond the GR control. It does not establish nonlinear health,
sourced backgrounds, Solar-System/galaxy/lensing regrades, a derivation of
xi or kappa, or adoption of AC2. A FAIL kills AC2's isotropic FRW sector as
written.
