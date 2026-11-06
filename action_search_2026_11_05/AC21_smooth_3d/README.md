# AC21: the smoothed switch in 3D, and an AC2q smoothing that keeps FRW exact

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Lane rules: closure_2026_11_06/SWARM_BRIEF.md.
Top-level criteria: FROZEN_CRITERIA.md (3891804624). There are seven iterations, and each one's criteria were
frozen before any of its numbers existed:

| iteration | criteria commit |
|---|---|
| iter_3 | f5b0b7270d |
| iter_4 | 3b4cb45230 |
| iter_5 | 0165486423 |
| iter_6 | 3ed022ae9f |
| iter_7 | b3931c241b |

Lean: fable_independent_2026/lean_2026/AC21_smooth_3d.lean has 16 theorems, 0 errors and 0 sorry, using only the
standard axioms. Its MUTATE twin fails on exactly its 4 false claims and passes 1 true sanity claim.

## Results

| question | label |
|---|---|
| Classical 3D theory across a transverse switch: what does it need? (iter_1 T1-T3) | **PASS (theorem).** In the variable w = int sqrt(F''/Pi) dPi, the PN charge-velocity system is symmetric hyperbolic with symmetrizer I, speeds v.k (x2) and v.k +- c\|k\|, and c = sqrt(Pi F''). Kato/Majda H^s theory then applies across the switch iff (i) F is a pure power Pi^m near 0, so c is linear in w (c = (m-1)/2 w exactly), and (ii) m > d + 2, so transverse data w0 ~ x_+^((m-1)/2) lie in H^s for some s > d/2 + 1. |
| AC20's contact form (gamma/2) Pi^4/(Pi+a)^2 in 3D | **NOT A 3D REPAIR.** c(w) = 3/2 w - w^(5/3) + ..., which is not C2 in w, and m = 4 is not > 5. It is a 1D repair only, as AC20 found. The AC20 m = 4 spline fails the same way. |
| Count cross-check against AC20's 1D numerics | Consistent. m = 3 is a finite kink in 1D (3 is not > 3) and m = 4 is C1 (4 > 3). |
| A 3D-admissible smoothing that keeps v3s statics and AC2q's FRW exact | **EXISTS (iter_6).** The search took four failed families first, all kept on the record (iters 1, 3, 4, 5). |
| PN sign inside the smoothing layer (iter_1 T7) | **PASS (general).** AC17's Lagrangian with a general local stiffness gives B = s + (gamma/2) s F'(s) + mu^2(1-N)/(K N^2) + x0 W' sin^2 theta >= s for any convex F with F(0) = F'(0) = 0, and A_eff = Psi^6 [N (2 + gamma F'(s))^2/(2 gamma F'') + mu^2/(K N)] > 0 iff F'' > 0. Every closed form was checked with sympy against AC17 (beta = 0, C = 2 reproduces AC17's A_eff). |
| Curved switch surface, 2D (iter_2, iter_7) | **iter_7: C1 FAIL as frozen, by one line.** The b = 0.8 row passes (Delta_inf 0.000, r 2.02, crossing ratio 1.04). The b = 0.4 row has its jump go to zero (Delta_inf 4e-5 against a 0.017 line, r 2.37), but its first-crossing ratio is 1.1045 against the [0.9, 1.1] line. Its crossing times drift (0.104, 0.092, 0.096, 0.090, 0.081), not the sqrt(2) collapse of v3s (ratio 1.415). All three controls discriminate: the n = 3 kink holds (r 1.001), v3s shows N3b (1.415), and compatible data give 0.00085. |

**Overall 3D label: NOT PASSED as frozen.** The analytic part passes: the theorem, a smoothing that meets its
hypotheses, statics, AC2q's FRW and the PN sign. One curved-interface numerical row misses its crossing-time line
narrowly. Read after the run, the b = 0.4 crossing is a resolution-limited soft-side fold near the interface, not
an interface kink: the jump converges to zero, and v3s's signature is absent. That reading is not graded. Settling
it needs a longer ladder (N > 12800) or smaller N steps, frozen first.

**The iter_6 form.** With q = Pi/b, F = gamma b^2 f(q), and the C^4 smoothstep
S(t) = t^5 (126 - 420 t + 540 t^2 - 315 t^3 + 70 t^4):

    f'' = A q^4                                       0 < q <= 1/2
        = A q^4 (1 - S(4x)) + B x^5 (1-x)^5            1/2 <= q <= 5/8     (x = 2q - 1)
        = B x^5 (1-x)^5                                5/8 <= q <= 9/10
        = B x^5 (1-x)^5 + S(5x - 4)                    9/10 <= q <= 1
        = 1                                            q >= 1   (F = (gamma/2) Pi^2 exactly)

- The constants are A = 734183424/8922115 (about 82.29) and B = 3165142806/44610575 (about 70.95). Both are
  exact rationals, solved from the two moment conditions f'(1) = 1 and f(1) = 1/2.
- The form is C^4 at every knot (checked exactly with sympy).
- f'' > 0 on (0, inf) structurally: every term is >= 0, and S, 1 - S >= 0 in Bernstein form (Lean
  `layer_nonneg`). The smallest value on the layer is 0.0048.
- max \|f' - q\| = 0.34, under the S-b line of 1.
- The form is a pure power Pi^6 near 0 (m = 6 > 5), and F'' > 0 makes c(w) as smooth as the blend, C^4.
- **v3s:** b = rho_DE. The statics bounds depend only on b, and they are 1.6e-5 / 2.0e-5 (Cassini), 1.0e-6 / 1.5e-6
  (globulars) and 2.4e-5 / 3.5e-5 % (Lstar floor shift), canonical / alt.
- **AC2q:** b = X. The FRW background sits at Pi = 2X > b, so the stiffness equals AC2q's exactly on \|D.P\| < X.
  That gives g1 = gamma, g2 = 2 gamma and the factor (1 - 2 gamma s^2)^2, AC7's exactly (Lean `frw_exact`).
- The choices tau = 1/2, x1 = 1/4, x0 = 4/5 and n = 5 are construction choices, taken as the first qualifying member
  of a search order declared in advance. They are pure numbers, not physical constants, and no gate was tuned.
  The scales come from the a0 law: rho_DE for v3s, and the clock's X for AC2q.

## Failures on the record (each one frozen, run and labelled)

- **iter_1 T4:** none of the six minimal-degree blends is convex. NO-GO for that family.
- **iter_3:** the LP polynomial family up to degree 20 certifies no member. The best minimum Bernstein coefficient was
  -1.28. NO-GO.
- **iter_4 and iter_5:** every (tau, n) and (tau, x0, n) gives A and B of opposite sign. NO-GO.
  - The obstruction, read after iter_5: f'' = 1 + h'' with h'' of zero mass and zero mean. A positive combination
    of shapes therefore needs the target mean to lie between the shapes' own means.
  - iter_6 made the left piece decay fast, and the first quadruple in its order qualified.
- **iter_2:** NO VERDICT as frozen. The smoothed rows' jump fell as N^-3 (r = 8.0, Delta_inf about 1e-5), outside the
  band r in [1.6, 2.4] that was written for first-order convergence. The v3s control was read after its own
  crossing: its first crossing time fell by about sqrt(2) per doubling (AC16's N3b signature) and dropped below
  t_meas for N >= 6400. iter_7 reran on fresh data with the corrected statistic, frozen before it ran.
- **Code fixes**, all made before any graded number depended on them:
  - iter_1 T2: integrating with symbolic m gave a wrong ratio. The fix integrates per integer m; the first run is
    superseded.
  - iter_2: evaluating f' through the expanded global polynomial lost about 1e-4 to cancellation. Caught in a
    smoke test; the fix evaluates a local Horner form.

## Controls

- iter_1 MUTATE (gamma -> -gamma; pure max form through T3): c^2 < 0 and m = 2 fails every d. It bites (exit 1).
- iter_2 MUTATE (v3s through the row statistic): fails. It bites (exit 1). iter_7 MUTATE (same): it bites (exit 1).
- Lean MUTATE: m = 4 claimed admissible in 3D, B >= s claimed without F' >= 0, the winner's B claimed negative, and
  FRW exactness claimed below the knot. All four fail; the true sanity claim passes.

## What it does not show

- This is the PN charge-velocity system, as in AC16/AC20, not the full covariant system.
- Local well-posedness only. The stiff side still forms ordinary gas shocks after about a sound-crossing time,
  as in AC20. Shocks and weak solutions are not graded.
- The soft side is untouched, so the caustic folds of AC10/X14 are unchanged.
- The data are transverse to the switch.
- The 3D statement rests on Kato's theorem with the hypotheses verified here. The numerics check C1 on a curved
  interface; they cannot see the dimension count.
- No data are graded and no constant is derived. The form is a candidate change to the action. Nothing is adopted;
  adoption is the owner's call.
