# EP1 frozen criteria: AC2q's slow frozen roots on decelerating (eps_phi = 2) backgrounds

Frozen before any EP1 script exists and before any EP1 number is computed. Kappa = 1/2 FITTED; not theory
closed. Adopts nothing. Rules: closure_2026_11_06/SWARM_BRIEF.md (own terms, no LCDM input, both footings,
frozen criteria first, every number from a committed script with JSON).

## Why

AC13 (c8377c403f) left its 2 eps_phi = 2 witnesses NO VERDICT (no power): the planted -(2H)^2 K q term reached
only R 9.4-9.8 there (3e3-1.9e4 on the dark-energy-like witnesses). AC23 (43009b6e76) passed 16/16 fresh
dark-energy-like witnesses and scoped eps_phi = 2 out. EP1 gives eps_phi = 2 a label.

## Analysis (stated before running; the reason AC13's plant had no power)

On AC5's rolling clock with lambda = sqrt(2 eps_phi), eps_phi = lambda^2 / 2 is the scaling attractor, so at
eps_phi = 2 the total eps >= 2 at all times, H ~ a^-2 and aH ~ a^-1. A comoving k then has k/(aH) = (k/H0) a,
growing to (k/H0) x 1101 by N_obs: the modes go deeper inside the horizon and gradient pressure (order k^2/a^2)
dominates any Hubble-rate term. The planted -(2H)^2 K q is added to that stiffness and is swamped by it, so it
cannot grow. That is a fact about the plant, not about the measurement. On eps < 1 backgrounds the opposite
holds (modes leave the horizon and the plant dominates), which is why AC13 and AC23 had power there.

A power control on eps_phi = 2 must therefore be a wrong term that gradient pressure cannot stabilise. Two
are frozen, both with AC23's lines:

- PW-R (stiffness replaced): main's K, Kdot and A kept, the stiffness S replaced by -(2H)^2 K. A Hubble-rate
  tachyon with no gradient pressure. With Hubble friction (3 - eps) at eps = 2 the e-fold growth exponent of
  q'' + q' - 4 q = 0 is r = (sqrt 17 - 1)/2 = 1.56, so about e^(1.56 x 7.0) = 5.6e4 against a GR control that
  does not grow. Expected to bite (reported prediction, not a line).
- PW-D (det K discriminator, AC23's frozen second gate): m2 (flipped stiffness) reaches det K / a^6 <= 0, or
  stops at a kinetic singularity, by N_obs. AC13 already shows this on its 2 eps_phi = 2 fixtures
  (-6.1e8, -6.1e10); EP1 grades it on fresh witnesses.

A witness is POWERED only if BOTH bite (PW-R R >= 1e3 at N_obs at both tolerances, and PW-D at both
tolerances). AC13's additive plant is still run (rtol 1e-11) and reported, not graded.

## Fresh witnesses (selection, not grading)

eps_phi = 2 only. Every other value is new against AC3 (eps_m .01/.3/.9, H Lstar .001/1/100, k/H
10/100/1e4), AC23 grid A (.2/.6/.95, 3e-4/3e-3/3e-2, 3/30/300) and AC23 grid B (.45/.8, 1e-4/.01/.1, 1/50/1000).

- Grid A, 27 cells: eps_m {0.5, 0.75, 0.97}, H Lstar {5e-4, 5e-3, 5e-2}, k/H {5, 20, 60}.
- Grid B, added only if grid A gives fewer than 3 witnesses: eps_m {0.85, 0.93}, H Lstar {2e-4, 2e-3, 2e-2},
  k/H {8, 40, 150}.
- Witness: a real negative frozen root w^2 < 0, by AC23 scan.py's roots() (AC3 finite_v3's algebra, a = H = 1,
  m2 = 1, 40 and 80 digits agreeing to 1e-25), executed from AC23's committed file.
- Cap: the 6 most negative w^2 / H^2 (cost: k/(aH) reaches k x 1101, about 1e5 radians at k = 60).
- If grids A + B give fewer than 3 witnesses, AC13's 2 eps_phi = 2 fixtures are added to the graded set and
  the label carries "(includes AC13 fixtures, not blind)". If they still give fewer than 3 POWERED, the label
  is NO VERDICT (no power).

## Runs (per witness; window N_obs = ln 1101, the same as AC13 for eps_phi = 2)

EP1's runner is AC13's run() with one added kind (plantR = PW-R) and its output directory redirected; KA1
proves the copy reproduces AC13. Kinds: gr, main (AC2q at gamma s^2 = 4.0e-17, pol_on (1 - 2 gamma s^2)^2),
m2, plantR at rtol 1e-9 and 1e-11; plant (AC13's additive term) at rtol 1e-11. plant and plantR are not
symplectic, so no Omega line on them. R = max over both seeds of max_t |q| / max_t |q_GR|, as in AC13/AC23.
N = 20 is not run on eps_phi = 2 (AC13's declared deviation: k/(aH) grows as e^N, infeasible).

Reported only: along each main background, the minimum eigenvalue of K^-1 S / H^2 at N = 0, 1, ..., 7 (shows
whether the a = 1 slow root survives as k/(aH) grows).

## Known answers

- KA1: AC13's 2 eps_phi = 2 fixtures (2,.9,.001,10) and (2,.9,.001,100), kinds main, gr, plant, m2 at
  rtol 1e-9, rerun through EP1's runner: max_I, max_II and detK_over_a6_min at N_obs match AC13's committed
  parts to 1e-10 relative.
- KA2: AC23's numbers. (a) AC23's committed grade.py, executed on its committed parts with only its output
  path redirected into EP1's directory, gives label PASS (HARMLESS, scoped), n_powered 16, max_R_main_Nobs and
  min_main_detK_Nobs equal to AC23's committed GRADE.json to 1e-12 relative. (b) AC23 witness
  (0.25, 0.6, 0.0003, 3) main at rtol 1e-9, rerun through EP1's runner to N_obs, matches AC23's committed
  part at N_obs (max_I, max_II, detK) to 1e-10 relative.
- KA3: the scanner on AC3's 27 eps_phi = 2 cells reproduces AC3's committed roots to 1e-25 relative and its
  eps_phi = 2 witness set (exactly the 2 AC13 fixtures).

## MUTATE (must bite, else the label is NO VERDICT)

- M-A: grading m2 in place of main must give UNSTABLE.
- M-B: grading plantR in place of main must give UNSTABLE.

## Lines and labels (AC5/AC13/AC23 lines kept: FAIL 1e3, HARMLESS 10, convergence 1e-3, Omega 1e-6)

- UNSTABLE (fixture named) if, on any converged witness, main R >= 1e3 at N_obs, or main min det K / a^6 <= 0
  (or a kinetic-singularity stop) at either tolerance.
- NO VERDICT (no power) if fewer than 3 witnesses are POWERED. The bracket reported: max main R and min main
  det K over the witnesses, and the PW-R / PW-D values that failed.
- NO VERDICT if KA1, KA2 or KA3 fails, if a MUTATE does not bite, or if a powered witness fails convergence
  (R at rtol 1e-9 vs 1e-11 within 1e-3 relative) or the Omega line (main and gr drift <= 1e-6 to N_obs).
- HARMLESS (scoped) if every powered witness has main R <= 10 at N_obs and main det K / a^6 > 0 throughout.
- NO VERDICT, bracket 10 < R < 1e3, otherwise (the AC13/AC23 "UNDECIDED" case).

## REACHED / NOT REACHED (a separate label: does any physical AC2q history reach eps_phi = 2?)

Derivation (exact algebra, stated now). For a canonical clock, eps_phi = phidot^2 / (2 H^2) =
(3/2)(rho_phi + p_phi) / rho_tot, and every other NEC-respecting component adds to eps, so eps_phi <= eps.
With rho_phi + p_phi = (1+z) rho_phi'(z) / 3: eps_phi(z) = (1+z) rho_phi'(z) / (2 rho_tot(z)).
(i) Reaching eps_phi = 2 needs Omega_phi (1 + w_phi) = 4/3, so Omega_phi >= 2/3 AND w_phi >= 1/3: the clock
must hold at least two thirds of the budget while redshifting at least as fast as radiation. That is not a
dark-energy phase. (ii) The fixture family itself (exponential V, lambda = 2) has eps >= 2 always, so q >= 1
and it never accelerates. The physical clock is the dark-energy scalar (a0 tied to rho_DE), which drives the
measured acceleration, so the lambda = 2 fixture is not a physical AC2q history.

Graded on the record's own measured dark-energy history, CFG689's primary (BAO+SN, curvature free), from its
committed JSON: rho_DE(z) = the node density w(z) (linear in z between nodes 0, 0.4, 0.7, 1.0, 1.5, 2.33, as
CFG689 interpolates), rho_tot lower bound = omega_b + omega_c times (1+z)^3 minus |omega_k| bound (best + 2 x
posterior sd) times (1+z)^2 (radiation, neutrinos and rho_DE dropped, which raises the bound). eps_phi bound
evaluated on a z grid of step 0.001 on [0, 2.33] for (best) the best-fit nodes and (worst) each interval's
slope taken from node_{i+1} + 2 sd and node_i - 2 sd.
- NOT REACHED on the measured span if the worst-case eps_phi bound stays < 2 on all of [0, 2.33] (margin
  reported).
- REACHED if the best-fit bound reaches 2 anywhere.
- Otherwise NOT DECIDED by the record's data.
- Beyond z = 2.33 the record has no rho_DE node. There only (i) applies, reported as a condition, not a
  measurement.

## Scope stated now

HARMLESS means: on rolling-clock FRW fixtures with eps_phi = 2 (decelerating), at fresh parameters, AC2q's slow
frozen roots do not amplify beyond 10x the GR control over 7.0 e-folds, the measurement sees a Hubble-rate
instability with no gradient pressure, and the kinetic matrix stays positive where the flipped stiffness makes
it negative. It is not the radiation era, not nonlinear, not sourced, not adoption. Both footings: AC2q's only
footing-dependent number here is gamma s^2 (2.4e-17 canonical, 4.0e-17 alt); pol_on differs from 1 by <= 1.6e-16
on both (AC13), so one run at 4.0e-17 grades both, as in AC13/AC23.
