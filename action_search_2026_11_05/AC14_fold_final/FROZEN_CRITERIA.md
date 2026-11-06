# AC14 frozen criteria: a final label for "does AC2q fold like v3s?" (planar, nonlinear)

Frozen before any AC14 script exists or any AC14 number is produced. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. Footings 9.3603e-11 / 1.1312e-10 m/s^2, never pooled.

## Why a new lane

AC10 (criteria 552db86f89, result 4895500fe2) is NO VERDICT as frozen. There were three reasons:

1. K2/K3 assumed crossing speed w = 1. A slab's own charge pushes its front to 1.09-1.23, and late
   turnaround folds occur before t_max.
2. Only 12 of the 240 AC2q physical rows were run, because the full grid was too slow.
3. The interior reading was post-fold. The excluded front edge cells fold first. Where the stiffness is on,
   the inviscid code then sends pressure spikes from those cells (J <= 0, pressure set to 0 next to Pi > 0)
   into the interior. The interior then stalls at J ~ 0.18 in AC2q and v3s alike. Two soft AC2q rows at
   11 kpc did not converge.

AC14 keeps AC10's physics unchanged. It imports `ac10.py` (physical_rows, stress_rows, constants and the
ladder logic) and edits none of AC10's files. It corrects (1), runs all rows (2), and removes the edge
artifact behind (3) with a device declared here, before any run.

## Physics (identical to AC10)

The planar label system is AC10 S1's: AC2q is v3s's label system with charge Pi = D.P + s^2; P sees Pi - s^2;
Poisson sees Pi. The stiffness force is -gamma d_x max(Pi, 0). The v3s twin has s = 0 and the switch on
Pi = D.P. Physical rows: AC10's `physical_rows()`, all of them: 240 AC2q rows and their 240 v3s twins (5 radii,
2 w, 2 ends of the M - 1 bracket, 2 Lstar, 3 kinds: phantom, clock-only and soft; both footings). Initial data,
sheet, stream extent, J_thr = 1e-3, J_reg = 0.05, t_max = 6 and the 5 % edge exclusion are AC10's.

## Declared numerical device E1 (edge stiffness taper)

The stiffness coefficient is tapered in label space with the same tanh profile T(q) that AC10 already uses for
the edge charge (A2-POST): gamma_cell = gamma T(q). The taper lies wholly inside the excluded 5 % edge cells, and
T >= 1 - 1e-4 at the first interior cell, so interior labels feel gamma to 1e-4. The force is
-d_x[gamma_cell max(Pi, 0)], and the outer boundary values are 0 (T -> 0 there). Folded edge cells therefore
exert no pressure, and no spike from them reaches the interior. Interior physics is unchanged.

The graded reading is AC10's frozen interior one: the first time the minimum interior J reaches J_thr. Every
integration stops at that event. A row is REGULAR only if interior J stays >= J_reg to t_max = 6. Anything else
is UNDECIDED.

## Convergence

AC10's ladder is N = 2000/4000/8000. The fold time must change by <= 1e-3 (relative) between the last two rungs,
and the label must not change. A row that fails at 8000 gets one more rung, N = 16000, and is then judged on
8000 vs 16000 with the same lines. A row that still fails is NOT CONVERGED.

## Checks (all must hold, or NO VERDICT)

- K0 (device is inert without pressure): at gamma = 0 the AC14 integrator equals ac10.run's fold time to 1e-12
  relative on the K1 zero-charge row and on one soft physical row.
- K1 (as AC10): the zero-charge coupled code equals an independent two-label integration to 1e-6. The thin-sheet
  delay after crossing equals v_cross/(K Sigma_b) within 2 %.
- K2/K3, re-stated with each slab's own measured crossing speed. This corrects AC10's w = 1 assumption, using
  AC10's A1-POST method. The front-most interior cell is followed along its own trajectory. v_c is that cell's
  speed at sheet crossing. Its J during first passage (up to its first turnaround) is compared with the exact
  per-label equation J'' = -K rho_b(x(t)) J + K(M-1)(Pi_0 - s^2 J), integrated along the same trajectory.
  Predictions (K Sigma_b = 1, so tau_f = v_c):
  - A1 (v3s, s = 0): a first-passage fold iff sqrt(K(M-1) Pi_0) v_c <= 1/sqrt 2.
  - A2 (AC2q, clock-only, Pi_0 = s^2): a first-passage fold iff sqrt(K(M-1) s^2) v_c <= 1 (AC10 A2).
  The stress rows are new, chosen far from both thresholds for any v_c in [1, 1.3]. All have gamma = 0 and
  M - 1 = 1:
  - A1: Pi_0 = 0.2 (predict fold), Pi_0 = 1.0 (predict no first-passage fold);
  - A2: Pi_0 = s^2 = 0.4 (predict fold), Pi_0 = s^2 = 2.0 (predict no first-passage fold).

  PASS requires all three of the following. If v_c falls outside [1, 1.3] for a row, the prediction is
  recomputed from the measured v_c; the formula does not change.
  - the numeric first-passage outcome matches the prediction on all four rows;
  - the numeric outcome matches the per-label equation's outcome;
  - the maximum relative J difference, numeric vs per-label equation, is <= 1e-3.
- MUTATE-A (AC10's, separate outputs): a repulsive sheet on the zero-charge stream must be REGULAR.
- MUTATE-B (AC10's power gate, separate outputs, with E1 active): an AC2q clock-only row, Pi_0 = 0.1, Mach 0.3
  (gamma = (1/0.3)^2/0.1), must be REGULAR. If it folds, the method cannot see pressure regularization, and no
  verdict stands.
- X > 0: min X/X_bg up to the fold, at PN order 1 - (v_max w/c)^2, must be > 0.99.

## Labels (for the question "does AC2q remove the khronon caustic that v3s has?")

- **FAIL-SAME-AS-V3S (caustics inherited).** All of the following hold:
  - all checks hold;
  - every one of the 240 AC2q rows is FOLD and converged;
  - every v3s twin is FOLD and converged;
  - |t_AC2q/t_v3s - 1| <= 1e-2 on every pair.
- **PASS (AC2q regularizes).** All checks hold, and at least one converged AC2q row is REGULAR while its
  converged v3s twin is FOLD.
- **SAME-AS-V3S, NOT ALL FOLD.** All checks hold, every pair converged, and each AC2q label equals its twin's,
  but some pairs are REGULAR in both. Reported as such: X14's "caustics generic" is then not supported in scope
  for those rows, and AC2q adds nothing.
- **WORSE.** A converged AC2q row folds where its converged v3s twin is REGULAR.
- **NO VERDICT** only if a check fails, a MUTATE does not bite, or any physical row is NOT CONVERGED or UNDECIDED.

Out of scope, stated now: the post-fold interior, i.e. stiffness-shock evolution after the first caustic. That
needs a shock-capturing scheme; the run stops at the first interior fold. Also out of scope: 3D or spherical
cases, the nonlinear hold law (constant M per row, as AC10), and the moving Sun (AC11/AC12). E1 is a numerical
treatment of the excluded edge only. A label here is a statement about the interior first caustic of the
planar problem only.
