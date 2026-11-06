# AC20: smoothing the stiffness switch. v3s: REPAIR (1D) with a contact form, no new constant; AC2q: NOT A REPAIR as frozen

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Lane rules: closure_2026_11_06/SWARM_BRIEF.md.
Top-level criteria e6d1ad6114. Four iterations, each frozen before its numbers. Lean:
fable_independent_2026/lean_2026/AC20_smooth_switch.lean (10 theorems, 0 errors, standard axioms only) and its MUTATE twin
(fails on exactly its 5 false claims; 2 true sanity claims pass).

AC16 proved that v3s and AC2q have no C1 solution across a transverse switch interface: the force -gamma d_x max(Pi, 0)
jumps there. X3 showed that any smoothing with F'' > 0 on the soft side is Hadamard ill-posed (c^2 = Pi F'' < 0). So the
admissible repairs keep F = 0 for Pi <= 0 and raise the contact order at Pi = 0.

| iteration | form | (a) 1D C1 across the switch | (b) statics | AC2q FRW | label |
|---|---|---|---|---|---|
| 1 | (gamma_n/n) Pi_+^n, n = 3 | FAIL (Lipschitz; slope jump -0.0955, prediction -0.1005) | CHANGED | - | not a repair |
| 1 | same, n = 4 | PASS | CHANGED (screening length scales with charge, up to 29x) | - | not a repair |
| 2-4 | (gamma/2) Pi_+^4/(Pi_+ + a)^2, a = s^2 | PASS (iter_4: Richardson 0.0009 / 0.0068; t_inv ~ a^0.45) | PRESERVED (<= 4.1e-5 at Cassini, 3e-6 inside Lstar) | FRW stiffness 11 gamma/16, healthy but not = AC2q | **v3s: REPAIR (1D)**; AC2q: not a repair |
| 3-4 | spline, exact for Pi >= b, contact 4 | b = 0.4 PASS, b = 0.2 FAIL (pre-asymptotic) | PRESERVED (<= 2e-5) | EXACT (1 - 2 gamma s^2)^2 | not a repair as frozen |
| 3-4 | spline, contact 6 (3D-ready) | not run | - | - | FAIL: not convex (C^3 and C^2 knots both) |

**What the v3s repair is.** Replace -(gamma/2) max(D.P, 0)^2 with -(gamma/2) (D.P)_+^4/((D.P)_+ + 2 rho_DE)^2:
- The scale 2 rho_DE comes from the a0 law, so there is no new constant.
- The form equals v3s to a relative 2 rho_DE / D.P everywhere the record graded statics.
- Its force is continuous at the switch, and the stiff side stays a hyperbolic gas (c^2 = Pi F'' >= 0).
- So the 1D PN system has C1 solutions across the switch. They last only about sqrt(a/Pi) of a sound-crossing time,
  then form ordinary gas shocks. Weak and shock solutions are not graded.
- The soft side is untouched, so AC10/X14's caustic folds are unchanged: this repair does nothing for caustics.

**What it does not show.** 3D: data with contact order 4 is in H^s only for s < 2, short of the s > 5/2 that 3D
symmetric-hyperbolic theory needs, and no convex polynomial spline of the forms tried reaches contact order 6. For
AC2q, neither form passed every frozen line: the contact form shifts FRW, and the spline missed one resolution row.

Bookkeeping fixes, each recorded in its iteration's README:
- iter_1: sympy assumptions in the n = 2 control.
- iter_2: crash in C-e's fixture factor.
- iter_3: the spline force was zero below b (sympify symbol), first run kept.
- iter_4: harness gains an optional v_0 (default unchanged; reproduces iter_1's N = 400 numbers).
