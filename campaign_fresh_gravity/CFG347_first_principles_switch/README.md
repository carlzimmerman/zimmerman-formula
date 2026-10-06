# CFG347: a first-principles bound-only switch from the framework's own structure?

Criteria: `FROZEN_CRITERIA.md` (commit 9c57125bd, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; c_T = 1; beta = 0; the switch reads baryons only; no DM particle (the cold mass is still required).

**Verdict (frozen rule): PARTIAL.** Two zero-constant routes tie: the unsaturated slaved theta_b ramp (R1) and the
dynamical theta_b switch (R3). Both pass (a) and (c) and fail (b). The costed R3 (3 new constants) is also PARTIAL:
it fails (b) at its most lenient admissible point. No first-principles candidate exists in the theta_b-reader class.
The obstructions are inequalities certified in Lean (11 theorems). This is a scoped result, not a closure.

## Which record gate each route is
- **R1 (theta_b = div u_b, threshold 0)** is XR36's turnaround gate, the same variable. It is not CFG172D: CFG172D
  put the flow theta inside V0's khronon theta-equation.
- **R2 (leaf comparison theta_b/<K>_h)** is XR36's normalised variable with the natural width Delta_x = 1.
- **R3** gives the switch its own kinetic term (CFG337's lesson):
  S = Int sqrt(-g)[ -(Z/2)(d sigma)^2 - (Z M^2/2) sigma^2 + C sigma nabla_mu u_b^mu ], with the MOND sector times
  f(sigma) = 1 - S(sigma), S = DE12's C-infinity step, and threshold theta_on = Z M^2 / C = a0/c.
  - The trigger is velocity-linear: C sigma div u_b = -C u_b . d sigma, a gyroscopic coupling.
  - Its effective theta-Lagrangian is a Legendre transform, so it is convex. That is how it escapes XR36's mirror-lemma ghost.

## Results
| test | R1 saturated | R1 ramp | R2 leaf | R3 zero-constant | R3 costed |
|---|---|---|---|---|---|
| (a) FRW | PASS | PASS | PASS | PASS | PASS |
| (b) bound | FAIL (flicker) | FAIL (overshoot) | FAIL | FAIL (reach, timing) | FAIL (fidelity) |
| (c) transition | FAIL (ghost) | PASS (m(k) >= rho) | FAIL | PASS | PASS |
| new constants | 0 | 0 | 0 | 0 | 3 (c_sigma, M, Z) |

- **(a) FRW, all routes.**
  - sigma_FRW = 3H c/a0 >= 20.97 (canonical) / 17.41 (alt). f = 0 in a finite neighbourhood, so the MOND term is
    absent from the quadratic action.
  - L341's harness gives D/D_LCDM = 1.00000000 and sigma_8 = 0.8101.
- **(b1) static bound.** Steady rotation and pressure support give theta_b = 0 exactly (sympy), so f = 1 and the
  system follows nu_mono statically.
- **(b2) R1/R2 fidelity.** A 10% compression at Omega(30 kpc) gives x = 0.1 Omega/theta_*:
  - 0.29-6.6 with theta_* = 3H, where the saturated W falls to 0-0.89;
  - 33-154 with theta_* = a0/c.

  The slaved gate flickers, or overshoots by up to 154x. The R2 ramp also adds a d<K>/dt force of 0.36-1.03 times
  gravity at 30 kpc (sympy: force = -W' dB/dx d(1/theta_*)/dt).
- **(b3) R3 zero-constant.** With c_sigma = c, the range ell = c/M is at least 267 r_ta for M = 3H, 800 r_ta for H and
  7800 r_ta for a0/c. The requirement is ell <= 0.257 r_ta. The switch averages theta_b over hundreds of Mpc, so it
  cannot be ON inside a bound region. The timing rule M >= sqrt3 H fails for M = H and for a0/c.
- **(b2) R3 costed, most lenient point.**
  - Constants: M = sqrt3 H(4) = 10.9 H0, ell = 45.5 kpc, c_sigma = 33.5 km/s, Z M^2 = B_edge,max (R = 1).
  - The gas mode moves 100% on 48 of 48 rows.
  - The Lean bound T5 needs G/(b/9 + A/10) <= 1; the measured ratio is 9.8e3-8.3e5.
  - Per-host constants (lenient, not scored) pass 12/48. With theta_on = 3H0 (sensitivity), universal passes 0/48
    and lenient 26/48.
  - Cause: theta_on <= 3H forces a large coupling C = Z M^2/theta_on.
- **(c) R3 health.**
  - The kinetic matrix is diag(rho, Z), so there is no ghost.
  - The gyroscopic term is principal: (c_s^2 - v)(c_sig^2 - v) = (C^2/(rho Z)) v, and its speeds^2 are real and positive.
  - Every root satisfies w >= min(A, 0) >= -Gamma_g^2, so growth never exceeds Jeans, uniformly in k (Hadamard). 20000
    random cases gave 0 violations; Lean T3, T3d, T4 certify it.
  - R1 saturated shows a ghost on 24/24 layers. R1 ramp has W'' = 0, so m(k) >= rho.
- **Switch width the theory picks.**
  - R1: the slaved pole 1/k_g = 132-1756 kpc.
  - R3 costed: sqrt(B_edge/rho)/theta_on = 16 Mpc to 2 Gpc.
  - Both exceed the 100 kpc tolerance. R1 overlaps CFG337's C2 ell_min (183-378 kpc), but it is a ghost there.
- **Reported liabilities (not scored).**
  - Causality: a luminal switch with any trigger coupling has a strictly superluminal characteristic (Lean T6).
    Criterion B allows this only relative to the khronon foliation. The costed point's fast speed is 0.05-5.2 c.
  - The R1 ramp's delta W x delta B mixing with the field sector was not evaluated, because the ramp already fails (b).

## The obstruction in one line
The switch must be OFF in the Hubble flow, so its threshold is theta_on <= 3H. Bound systems have
Omega_dyn >> H and v_B = sqrt(B/rho_b) >> c_s. A theta_b reader therefore takes one of three forms:
- slaved and saturated: a ghost (mirror lemma, T1-T2);
- slaved and unsaturated: flicker or overshoot by Omega_dyn delta/theta_on;
- dynamical: either luminal with a Hubble-scale mass (range >> r_ta, T7) or coupled with G >> b/9 + A/10 (T5n).

A theorem covers the zero-constant tier within this class. The costed failure is shown at the most lenient point,
which is an example, not a theorem over all shapes.

## Controls
- **C1:** XR36's gate returns 1/k_g = 132.2-1756.0 kpc with a ghost on 24/24 layers (recorded: 132-1756).
- **C2:** in the GR limit the system reduces to gas plus Jeans.
- **MUTATE (threshold sign flipped):** the switch is ON on FRW. Growth is 28.8x / 33.9x and sigma_8 is 23.32 / 27.48,
  reproducing the audit's chassis values. The run exits 1.

## Lean
`CFG347_switch_certificates.lean`: 11 theorems, no sorry, standard axioms only.
- T1 mirror lemma (MVT); T2 slaved ghost;
- T3 / T3d gyroscopic roots; T4 Jeans bound;
- T5 fidelity bound and T5n its contrapositive;
- T6 luminal superluminality; T7 luminal range;
- T8 FRW-off neighbourhood and T8n the margin 3 H0 c/a0 > 17.

The output is in `.out`.

## Run
```
python3 campaign_fresh_gravity/CFG347_first_principles_switch/cfg347_switch.py > campaign_fresh_gravity/CFG347_first_principles_switch/cfg347_switch.out          # rc 0, ~1 s
CFG347_MUTATE=1 python3 campaign_fresh_gravity/CFG347_first_principles_switch/cfg347_switch.py > campaign_fresh_gravity/CFG347_first_principles_switch/cfg347_switch_MUTATE.out   # rc 1
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG347_first_principles_switch/CFG347_switch_certificates.lean
```
DE12's `transition()` and L341's growth harness are exec'd read-only.

**Scope:**
- quadratic level; quasi-static WKB on DE12's 24 host layers;
- r_ta from the EdS turnaround overdensity 5.55 (an approximation);
- fidelity measured on the 1e6 K gas mode at 30 kpc;
- the R3 trigger coupling is linear in sigma; a Z2 (sigma^2 theta_b) variant was not run.
