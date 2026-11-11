# QG1 RESULT: quantum health of action (A), gate T2 of TOE0

**T2 = FAIL. Minkowski FAILS on both footings (canonical / alt); FRW z = 1100, FRW z = 1, the point mass at x_N = 1e-2,
1 and 1e2, and the Sun at 1 AU all PASS on both footings. The deciding number: on Minkowski the clock's gradient
coefficient, its charge G = n_d + D.P, is exactly 0, so omega^2 = 0 at every k and Lambda_s = 0 (Lambda_s L = 0 < 10).**

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. kappa = 1/2 FITTED; not theory closed.
Footings never pooled. The cold component is cold dark energy, never a particle.

- Criteria: `FROZEN_CRITERIA.md` (9f78e93383), committed alone before any script.
- Amendment: `AMENDMENT_A1.md` (ec1f4dc6ba), post hoc after scratchpad development runs and before the graded run. No
  threshold changed.
- Script: `qg1.py` writes `qg1.out` and `qg1.json`, takes 17 s on one thread, and exits 0 because every known answer
  passes. A re-run gives an identical JSON (runtime field excluded).
- MUTATE twins: `qg1_MUTATE_M1..M4.out/.json`.
- Lean: `QG1.lean` (8 theorems, exit 0) and its false twin `QG1_MUTATE.lean` (4 errors, exit 1); logs in `compile*.txt`.

## 1. Labels

| row | background, L | canonical | alt | what decides it |
|---|---|---|---|---|
| MINK | Minkowski, 1 mm | **FAIL** | **FAIL** | (ii): Lambda_s = 0. The clock has no gradient energy (G = 0), so omega = 0 at every k. (i) passes; (iii) cannot be evaluated |
| FRW1100 | FRW z = 1100, 10 Mpc comoving | PASS | PASS | Lambda_s L = 334 / 316, set by the switch at Pi_bar = 0. Cold growth f = 0.737 < 1 |
| FRW1 | FRW z = 1, 10 Mpc comoving | PASS | PASS | Lambda_s L = 1.84e5 / 1.74e5. f = 0.877 / 0.833 < 1 |
| PM-2 | 6e10 Msun, x_N = 1e-2 (x = 0.105), 1 kpc | PASS | PASS | Lambda_s L = 1.09e12 / 1.12e12 |
| PM0 | x_N = 1 (x = 1.618), 1 kpc | PASS | PASS | Lambda_s L = 3.14e12 / 3.24e12 |
| PM2 | x_N = 1e2 (x = 101), 1 kpc | PASS | PASS | Lambda_s L = 1.40e13 / 1.44e13 |
| SUN | Sun at 1 AU (x = 6.3e7 / 5.2e7), 1 AU | PASS | PASS | Lambda_s L = 7.1e4 / 6.9e4. Clock sound speed 30 km/s |

The record's mu_K reading is graded on each row: mu_K* on the FRW rows, mu_K = 0 on the static rows. The record has no
single mu_K (FB1 / SCS1). Section 6 gives the other reading.

## 2. (i) Modes on each background: no ghost, no gradient instability

- **P is auxiliary on every background.** It has no time derivative. It is integrated out mode by mode through
  M(k) = (H_P + gamma_L k k^T)^{-1}. H_P has eigenvalues K(1+u) and K(1+u)^2, and the minimum eigenvalue over K is
  1, 1.105, 2.618 and 102 on the rows. Its algebraic cost is positive.
- **alpha_eff = 2 at zero acceleration.** K J''(0) = 1 exactly (KA3), so P supplies the khronometric acceleration term
  with alpha_a = 2 cY(k), where cY = 1/(1 + Lstar^2 k^2/2). This is the singular Newtonian point 1/(1 - alpha/2), and the
  deep-MOND end of the law sits there.
- **Tensor.** The GR graviton (KA1). The non-GR correction to omega^2 comes only from anisotropic stress (A1). It is 0 on
  MINK and FRW and at most 1.5e-12 of k^2 elsewhere.
- **The clock scalar (one mode).** With G = n_d + D.Pbar, the dispersion is
  omega^2 = G k^2 (b - a)/(a b), with a = m(k) k^2 + mu^2/K and b = k^2/K. This is SCS1's closed form (KA4).
  - The unmixed kinetic coefficient Z_0 = a is positive everywhere: there is no ghost.
  - No mode has omega^2 < 0 growing with k: there is no gradient instability.
- **FRW.** The clock is dust, Jeans-type at k << mu_K*, with omega^2 = -1.1e-57 eV^2 (z = 1100) and -6.6e-66 eV^2
  (z = 1). The growth rate in the expanding background is f = 0.737 (z = 1100) and 0.877 / 0.833 (z = 1), so it grows more
  slowly than H, as T2 allows. The local free-fall rate is 0.979 H and 0.998 / 0.952 H.
- **Point mass.** omega^2 tends to a constant: 7.3e-61 eV^2 at PM0, a period of about 1/(1.3e-15 s^-1). That is SCS1's
  STABLE state.
- **Sun.** The hedgehog charge M/(2 pi Lstar^2 r) gives omega^2 = G gamma_L k^2. The sound speed comes out as
  c_s = sqrt(G M/r) = 30 km/s (omega^2 = 1.08e-41 eV^2 at k = 3.3e-17 eV). With the hedgehog, G gamma_L = G_N M/r exactly.

**Minkowski, exactly.** In unitary gauge, (A) is the khronometric form with beta = lambda = 0. No term of (A) outside R
depends on K_ij or on the shift. With that form, the scalar determinant is -4 M^6 k^4 omega^2 (alpha_a k^2 + 2 mu^2)
(sympy, C-MINK). Its only root is omega = 0, for any alpha_a and any mu_K. The momentum constraint makes the shift a
Lagrange multiplier, which freezes zeta. The same machinery gives the BPS speed
(beta + lambda)(2 - alpha)/[alpha(1 - beta)(2 + beta + 3 lambda)] with residual 0 (KA2), and (A) sits at the zero of its
numerator. The Newtonian reduction agrees: omega^2 is proportional to G, and G = 0. So **(i) passes on Minkowski, since
nothing is negative, but the clock has no restoring force at all**.

## 3. (ii) Strong coupling

The frozen definition: the vacuum variance per ln k, s^2 = k^3/(4 pi^2 |Z| omega_eff), is inserted into the vertices
(tilt, law cubic and quartic, dust cubic and quartic, the switch). Then Lambda_s = k_x/sqrt(2 pi). KA6 checks the
method: on a deep-MOND Lagrangian (2/3) M^2 g^3/a0 it returns the operator scale
Lambda_3 = sqrt(12 M a0) x^(3/4) to 4.5e-15. That is 2.45 meV, or 1/(0.081 mm), at x = 1: the AQUAL problem's own scale.

- **MINK: Lambda_s = 0.** With omega_eff = 0 the vacuum variance is unbounded, so every vertex that carries grad sigma
  without a time derivative is unsuppressed. The obvious one is the clock's tilt dP.grad(|grad sigma|^2/2). This is the
  khronometric beta + lambda = 0 limit (Horava lambda_H = 1), whose strong coupling is known (Charmousis-Niz-Padilla-Saffin
  2009; Blas-Pujolas-Sibiryakov 2009; PROVISIONAL). It is also the zero-density-dust problem. The lead's hand expectation
  said "low"; the computed value is zero.
- **Charged rows.** The graded switch ramp sets Lambda_s on every charged row. It is conservative (A1 item 3) and gives:
  - about 1/(27 pc), physical, on FRW, where Pi_bar = 0 and every fluctuation crosses the C^1 switch;
  - 1/(2.8e4 km) to 1/(2.1e3 km) on PM and SUN.
  All of these clear Lambda_s L >= 10 by 1.5 to 12 decades. A1's Gaussian-crossing diagnostic (not graded) puts the
  static rows much higher, at Lambda_s L of 8e21 to 1.6e23 on PM and 7.5e15 to 7.7e15 on SUN.
- **Null points (reported).**
  - Along the point-mass profile, Lambda_s L at L = 1 kpc stays at 7.96e10 or more down to x_N = 1e-8 (r = 95 Mpc).
  - At a generic null with positive charge (field a0 s/l, l = 10 kpc, G = a0/(K l)), no failure region exists down to
    u = 1e-30. The stiffness keeps 1 - K m >= gamma_L k^2 m0/(1 + gamma_L k^2 m0) > 0.
  - Strong coupling therefore needs the charge itself to vanish, as on Minkowski. Where the phantom density turns
    negative (SCS2/SCS3 external field), the question is instability, not this one.
- **Earth-surface laboratory (reported, not graded).** The Sun's and Earth's hedgehogs give a charge of 5.05e-18 kg/m^3.
  - The graded ramp gives Lambda_s = 1/(2.07e6 m), so Lambda_s x 1 mm = 4.8e-10 (fail).
  - The A1 Gaussian diagnostic gives 1/(19 um), so Lambda_s x 1 mm = 53 / 51 (pass).
  - So whether real laboratory gravity at 1 mm is weakly coupled turns on how the switch is measured. T2's Minkowski row
    fails either way.

## 4. (iii) One loop: the law's shape is radiatively stable

Cutoff Lambda_c = min(Lambda_s, M_Pl), as T2 sets it.

- **Matter loops** cannot make an A-term: S_m contains no tau, P or lambda, so they generate only diffeomorphism-invariant
  functionals of g. They reach the law only through the Planck mass. With M^2 -> M^2 (1 + eps), the law becomes
  mu_eff = 1 - 1/((1 + eps)(1 + u)), so Delta mu = eps/((1 + eps)(1 + x)) (sympy; Lean `qg1_dmu`). The deep-MOND end
  needs K J''(0) = 1 exactly, which is a tuning between the A^2 and R coefficients. The size of eps:
  - eps from SM masses (dimensional regularization) = 3.5e-32;
  - eps from the cutoff term is at most 1.1e-81.
- **Khronon loop.** The zero-point energy at fixed charge gives |Delta mu| <= 2.6e-67.
- **Graviton loops** enter only as N_eff counting in eps. They are not a computed loop.
- **Result.** Worst |Delta mu|/mu = 3.5e-30 at x = 0.01 and |Delta a0/a0| = 3.5e-30 on every graded row and both
  footings. PASS. A matter cutoff above 8.8e16 GeV would be needed to move mu(0.01) by 10 % (eps = 1e-3).
- **MINK**: NOT EVALUABLE (no loop expansion at Lambda_s = 0).

## 5. T4 report: matter loops break Lambda = 32 pi a0^2/c^4 (placed in T4, not part of T2)

**BREAKS.**
- The SM vacuum energy at one log (dimensional regularization) is 6.3e53 rho_DE (canonical) and 4.3e53 rho_DE (alt). The
  electron alone gives 1.7e31 / 1.2e31 and the top 6.7e53 / 4.6e53.
- a0, inside W, is not shifted by matter at any loop order.
- So the relation needs the full cosmological-constant tuning: a0's side is stable and Lambda's side is not.
- With T2's cutoff (Lambda_c of 2e-25 to 9e-14 eV, below every SM mass) the shift is at most 2.4e-42 rho_DE. That holds
  only because every SM field has decoupled.

## 6. Other mu_K reading (reported, not graded)

- **mu_K = 0 on FRW:** there is no cold component and the off-switch branch is degenerate, so Lambda_s = 0. Form B's
  cosmology needs mu_K*.
- **mu_K* on the static rows:** SCS1's JEANS-ONLY growth is reproduced, bounded in k, at rates of 5.7e-17 to 2.9e-15 s^-1
  (canonical). Lambda_s L is 6.9e12 or more. MINK is unchanged.

## 7. Known answers and MUTATE twins

| check | result |
|---|---|
| KA1 GR graviton (sqrt(-g) R at second order vs (1/2)(h_t^2 - h_z^2), Euler-Lagrange) | PASS, residual 0 |
| KA2 BPS khronon speed from the ADM expansion | PASS, residual 0 |
| C-MINK (A) on Minkowski in unitary gauge | det proportional to omega^2: only omega = 0 |
| KA3 Legendre; K J''(0) = 1 | PASS, 6e-36 |
| KA4 SCS1 closed form; tilt integration by parts | PASS, residual 0 |
| KA5 pure dust, Jeans rate^2 = 4 pi G rho | PASS |
| KA6 \|grad phi\|^3/a0 strong coupling | PASS, 4.5e-15 |
| KA7 zero-point integrator | PASS, 2e-41 |
| KA8 growth ODE (EdS f = 1; flat Omega_m 0.3: 0.5128 vs 0.5157) | PASS |
| C0 unit chain; C2 Gaussian crossing (A1) | PASS |
| **M1** dust sign flipped, FRW1 (i) | BITES both footings: Z_0/(k^2/K) down to -4.9e20 |
| **M2** W sign flipped, PM0 (i) | BITES: Hessian -6.85 K, Z_0 < 0 |
| **M3** tilt dropped (G -> 0), PM0 (ii) | BITES: Lambda_s L 3e12 -> 0 |
| **M4** eps += 1e-2, PM0 (iii) | BITES: \|Delta a0/a0\| 3.5e-30 -> 0.99 |

## 8. Step R, and the record result that transfers

- The constraint algebra (3 DOF), AC18/AZ39 causality, AC2's P integration and SCS1/SCS2 stability are quoted in the
  criteria, section 1. This lane agrees with all of them: SCS1's closed form is reproduced exactly, and its STABLE
  static state is the PASS on PM.
- STANDING's two-loop a0 protection lives on the retired K(Box_u/a0^2) kernel. Only the clock's exact shift symmetry
  transfers, and it forbids a generated tau potential. The kernel-dependent multiplicative, tadpole and graviton legs
  have no counterpart in (A). Section 4 supplies the one-loop bound that (A) lacked.

## 9. What this does not cover

- **Approximations.**
  - Newtonian-order Stueckelberg reduction, quasi-static metric, frozen coefficients (WKB).
  - Vertex sizes by amplitude substitution: O(1) factors, absorbed by the 10x margin, which every passing row clears by
    1.5 decades or more.
  - FRW treated as a local patch, with Hubble friction only in the growth rate.
  - Graviton loops counted, not computed.
- **Not covered.** The full relativistic cubic action on curved backgrounds. Nonlinear (classical) breakdown of the dust,
  meaning caustics (COL1's fold). Backgrounds with negative charge (SCS2/SCS3). A real one-loop graviton computation.
- **Hand expectations.** The lead's "gamma_L gives omega^2 ~ Lstar^2 k^4" is wrong: with charge it gives k^2, and on
  Minkowski it gives nothing. "Low Lambda_s at Minkowski" is right in direction, and the value is zero. The other items
  hold. Mine (MINK FAIL; charged rows pass by decades; T4 BREAKS, electron about 1e31) hold.

## 10. Commits

| commit | shared checkout (local) | origin (replayed with merge-tree + commit-tree) |
|---|---|---|
| criteria | 9f78e93383 | 97ff779d5b |
| AMENDMENT A1 | ec1f4dc6ba | cb2851f3c2 |
| result | 83793fbbc7 | 504c609936 |

This id table is one further commit, pushed the same way.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
