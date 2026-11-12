# STR1 — FROZEN CRITERIA (lane HY4-2, 2026-11-11)

Lane id **STR1**. Written alone, before any script and before any number. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed. Footings never pooled: a0 = 9.3603e-11 (canonical), 1.1312e-10 (alt) m/s^2.

## 0. The question this lane grades

The law's static halo is held by the anisotropic stress

    Pi_ij = J(g) delta_ij - g_i g_j / (K (1+u)),   K = 4 pi G,  u = g/a0,  J(g) = (a0^2/K)(u - ln(1+u)),

and in the deep field **Pi_rr = -Pi_tt exactly**, so the radial "dispersion" is **negative**:
sigma_r^2 = -v_inf^2/2, sigma_t^2 = +v_inf^2/2, v_inf^4 = G M_b a0. No kinetic gas can have sigma_r^2 < 0, so the
halo is a medium under **radial tension**.

The question: **can that anisotropic stress carry the lensing signal**, so that KiDS's outer amplitude does not
require 30 to 100 M_b of actual cold mass?

## 1. What is derived before any number is read (Part A of `str1.py`)

Newtonian / isotropic gauge, static, spherically symmetric, source T^i_j = diag(p_r, p_t, p_t):

    ds^2 = -(1 + 2 Psi/c^2) c^2 dt^2 + (1 - 2 Phi/c^2)(dr^2 + r^2 dOmega^2).

**D1** the linearized Einstein equations (sympy, exact in the source, first order in the metric perturbation):

    (i)   G^0_0            = -2 lap(Phi)/c^2                     ->  lap(Phi) = 4 pi G rho
    (ii)  G^r_r - G^theta_theta = (1/c^2)[(Phi-Psi)'' - (Phi-Psi)'/r]  = (8 pi G/c^2)(p_r - p_t)
    (iii) G^r_r + 2 G^theta_theta = -(2/c^2) lap(Phi-Psi)        ->  lap(Phi-Psi) = -4 pi G (p_r + 2 p_t)/c^2

**D2** hence the two combinations that carry physics:

    lap[(Phi+Psi)/2] = 4 pi G [ rho + (p_r + 2 p_t)/(2 c^2) ]      <- the LENSING source
    lap(Psi)         = 4 pi G [ rho + (p_r + 2 p_t)/c^2 ]          <- the TOLMAN / ACTIVE source

**D3** the photon. With c dt = n dl and n = sqrt((1-2 Phi/c^2)/(1+2 Psi/c^2)) = 1 - (Phi+Psi)/c^2 + ...,
the convergence is

    kappa = Sigma_eff / Sigma_crit,   Sigma_eff = INT [ rho + (p_r + 2 p_t)/(2 c^2) ] dz.

The factor 1/2 (not 1) is the one that belongs to lensing; the Tolman/active source carries the factor 1.
**D4** the Tolman / active mass of a static configuration (Tolman 1930; = the ADM mass for a static,
asymptotically flat spacetime):

    M_T = INT [ rho + (p_r + 2 p_t)/c^2 ] sqrt(-g) d^3x   ->   M_T = M_ADM.

**D5** with **p_r = -p_t**: p_r + 2 p_t = +p_t = rho sigma_t^2 > 0. The correction is therefore *positive*
(the exit gets the sign it wants) and equals

    convergence:  sigma_t^2/(2 c^2) of the source      Tolman/active: sigma_t^2/c^2.

**D6** exact algebra for the law's halo (Part B), with x = r/r_M, r_M = sqrt(G M_b/a0):

    u(x) = (1 + sqrt(1+4x^2))/(2 x^2),   M_c(<r) = M_b X(x),  X = (sqrt(1+4x^2)-1)/2,
    rho_h = M_b / (2 pi r_M^3 x sqrt(1+4x^2)),   Pi_tt = (a0^2/4 pi G)(u - ln(1+u)),
    Pi_rr = Pi_tt - (a0^2/4 pi G) u^2/(1+u),
    sigma_t^2 = Pi_tt/rho_h -> (1/2) sqrt(G M_b a0) = v_inf^2/2   as x -> infinity, with the correction O(1/x).

**D7** the equilibrium identity (momentum conservation), verified symbolically:
d Pi_rr/dr + (2/r)(Pi_rr - Pi_tt) + rho_h g = 0 identically in x.

## 2. The numbers required (Part C), both footings, never pooled

**N1** profiles at x = 0.1, 1, 3, 10, 30, 100: rho_h, Pi_rr, Pi_tt, sigma_r^2/c^2, sigma_t^2/c^2,
(Pi_rr+Pi_tt)/Pi_tt, and the equilibrium residual.

**N2** the kill ratio R(x) = Delta_M_stress(<r) / M_missing(<r) on a grid of x in (0, 10], for three numerators

    A (the graded one):  (1/2 c^2) INT_0^r (p_r + 2 p_t) 4 pi r'^2 dr'      [the lensing correction]
    B (2x generous):     (1/c^2)    INT_0^r (p_r + 2 p_t) 4 pi r'^2 dr'      [the Tolman correction]
    C (maximally generous): (1/c^2) INT_0^r (|p_r| + 2|p_t|) 4 pi r'^2 dr'

and three denominators

    1 (the graded one):  M_c(<r) = M_b X(x)                        [the whole phantom halo]
    2 (narrower):        max(M_c(<r) - 5.41 M_b, 0)                [excess over the whole cosmic budget]
    3 (narrowest):       max(M_c(<r) - 1.4 M_b, 0)                 [excess over the charge VSH1 delivers]

**N3** the maximum of each R over the grid, per footing.

**N4** v_inf^2/(2c^2) at v_inf = 200 km/s, and at log M_b = 9 ... 15.

**N5** the value of sigma_t^2/c^2 that *would* be needed to carry 5x, 11x and 20x of M_b.

## 3. THE KILL, pre-registered (this is the task's kill, stated before the run)

**K1 (graded).** The exit LIVES only if

    max over 0 < r <= 10 r_M of  R(r)  >  0.10

on a footing, with the primary definitions (numerator A, denominator 1). If the maximum is <= 0.10 on both
footings the exit does not live and the lane says so. All nine (numerator, denominator) combinations are
printed; the exit is given every one of them, and the *largest* of the nine is what the exit may claim.

**K2 (dominant energy condition).** A stress can carry at most 100% of the mass it is the stress *of*
(|p| <= rho c^2). Carrying F times M_b of missing mass with a medium of mass M_med requires
sigma_t^2/c^2 = 2 F M_b/M_med (lensing) or F M_b/M_med (Tolman). With M_med = 5.41 M_b (the whole cosmic
budget) and F = 29.5 (30 r_M), that is 10.9 c^2; with M_med = 1.4 M_b (what falls in), 42 c^2. Report the
required sigma_t^2/c^2 and the DEC violation factor.

**K3 (M5).** State what sigma_r^2 < 0 requires of the medium (a static shear modulus: an elastic solid, or a
radially reinforced filament network) and check the requirement against **M5's three hypotheses**
(local, momentum-conserving, normally self-gravitating). Which one must be dropped, and what the record
says about that escape.

## 4. Labels (frozen before the run)

    max R <= 0.10 on both footings              ->  "STRESS CANNOT PAY / STRESS CANNOT PAY"
    max R >  0.10 on both footings              ->  "STRESS PAYS / STRESS PAYS"
    the footings disagree                       ->  "SPLIT: <canonical label> / <alt label>"
    any KA below fails, or the run is incomplete ->  "NO VERDICT / NO VERDICT"

## 5. Known-answer checks (KAs); a failure forces NO VERDICT

- **KA1** the halo equilibrium residual |d Pi_rr/dr + (2/r)(Pi_rr - Pi_tt) + rho_h g| / (rho_h g) <= 1e-9 at
  every x on the grid (symbolic identity in Part B, numeric in Part C).
- **KA2** deep-field identity: (Pi_rr + Pi_tt)/Pi_tt -> 0 as 1/x; at x = 100 the value must be <= 1e-2
  (the record's hand value is 6.6e-3).
- **KA3** sigma_t^2 / (v_inf^2/2) -> 1 as x -> infinity; at x = 100 the value must be within 1e-2 of 1.
- **KA4** the derivation reduces correctly: (a) p_r = p_t = 0 gives lap[(Phi+Psi)/2] = 4 pi G rho and
  Phi = Psi; (b) the isotropic specialization p_r = p_t = p gives the lensing source rho + 3p/(2 c^2) and
  the active source rho + 3p/c^2, which must match the independent 1PN/PPN result for a static perfect fluid
  in GR (n - 1 = 2U + 3 Phi_4 - U^2 - Phi_2 with lap(U) = -4 pi G rho, lap(Phi_4) = -4 pi G p): coefficient
  3/2 for lensing, 3 for the active mass. This is the cross-check that fixes the factor 1/2.
- **KA5** the point-mass vacuum check: for p = 0 the exterior isotropic Schwarzschild gives Phi = Psi = -GM/r,
  Phi - Psi = 0, and the deflection is the usual 2x Newtonian.
- **KA6** the halo mass integral closes: INT_0^r rho_h 4 pi r'^2 dr' = M_c(<r) = M_b X(x) to 1e-9.

## 6. MUTATE (each must bite, or the number it guards is not load-bearing)

- **M1** gas instead of a solid: set p_r = +p_t = rho sigma^2 (no tension). The correction becomes
  3 sigma^2/(2c^2) at most; report it. If it does not change the label, the sign of p_r is not what carries
  the verdict.
- **M2** use the Tolman factor 1 instead of 1/2 (numerator B).
- **M3** use |p_r| + 2|p_t| (numerator C).
- **M4** shrink the denominator to the excess over the budget (denominator 2) and over the delivered charge
  (denominator 3).
- **M5** extended baryons (Hernquist, a_h = 0.05, 0.2, 0.5 r_M) instead of a point mass: the point-mass
  profiles are singular at x -> 0 (rho_h ~ 1/x, sigma_t^2 ~ 1/x), so the ratio at small x is an artefact.
  The extended runs bound the true inner value; report the max over 0 < x <= 10 for each.
- **M6** footing swap: if canonical and alt differ in label, say so; they must not be pooled.

## 7. What this lane does NOT grade

The amount budget (HY4-1/GAS1), the elastic solid's own gates (ELA1, HY4-7), the conservation-law escape
(HY4-4/VCC1), the share X_s = 59.5 M_b (an input rule in the record, not an output here). This lane grades
one thing: **whether the anisotropic stress can carry the convergence**. It reports the medium requirement
and the M5 check as required, without grading them.

## 8. Outputs

`FROZEN_CRITERIA.md` (this file) -> `str1.py` -> `str1.out` -> `RESULT.md`, with the same label on both
footings.
