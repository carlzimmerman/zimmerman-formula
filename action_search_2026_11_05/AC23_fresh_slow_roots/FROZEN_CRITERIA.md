# AC23 frozen criteria: AC2q's slow roots on fresh dark-energy-like witnesses, with per-witness power

Frozen before any AC23 script exists and before any fresh-grid number is computed. Kappa = 1/2 FITTED;
not theory closed. Adopts nothing. Rules: closure_2026_11_06/SWARM_BRIEF.md.

## Why

AC13 (c8377c403f) is NO VERDICT (no power) as frozen. Its power gate needed the planted tachyon to bite on
every witness, and it failed on the 2 decelerating eps_phi = 2 witnesses. AC13 read "HARMLESS on the 6
dark-energy-like witnesses" only after seeing the data, so that reading is not a label. AC23 gives a clean
label on witnesses no earlier lane used. Power is graded per witness. AC13 found a second discriminator
after the data (det K changes sign under the flipped stiffness), and AC23 freezes it as a gate here.

## Scope: dark-energy-like clocks only (eps_phi <= 0.5)

The physical late-time clock in this framework is the dark-energy scalar. a0 is tied to rho_DE, so the
expansion it drives accelerates: eps = -Hdot/H^2 < 1. eps_phi = 2 is a decelerating fixture (eps > 1), so
it is not the physical clock, and there AC13 showed no control can grow 1e3 in 7 e-folds. It is outside
AC23's scope and is not run. AC13's two eps_phi = 2 witnesses stay as AC13 left them.

## Fresh grid and witness rule (selection, not grading)

Grid A, 81 cells, every value new against AC3/AC4/AC5/AC13
(AC3 used eps_phi {.05,.5,2}, eps_m {.01,.3,.9}, Lstar {.001,1,100}, k {10,100,10000}):
- eps_phi in {0.1, 0.25, 0.4}
- eps_m in {0.2, 0.6, 0.95}
- H Lstar in {0.0003, 0.003, 0.03}
- k/H in {3, 30, 300}

Frozen roots use AC3's own algebra, exactly AC3 finite_v3's definition: the same source exec, a = H = 1,
m2 = 1, roots of det(G - w^2 K + i w A) = 0 as a quadratic in w^2, at 40 and 80 digits. The two precisions
must agree to 1e-25.
- A cell is a WITNESS if it has a real negative root w^2 < 0.
- If grid A gives fewer than 3 witnesses, grid B is added, also fresh: same eps_phi; eps_m in {0.45, 0.8};
  H Lstar in {1e-4, 0.01, 0.1}; k/H in {1, 50, 1000}.
- If there are more than 16 witnesses, the 16 with the most negative w^2/H^2 are taken.
- Known answer KA2: the same scanner applied to AC3's 81 cells reproduces AC3's committed roots to 1e-25
  relative and its 8 witnesses exactly.

## Runs (per witness, rtol 1e-9 and 1e-11)

AC13's run() is imported unchanged, with only its output directory redirected: AC5's build(), AC5's
rolling-clock flow with lambda = sqrt(2 eps_phi), and the streaming maxima.
- gr (pol_on 0), main (AC2q, pol_on (1 - 2 gamma s^2)^2 at gamma s^2 = 4.0e-17) and m2 (flipped
  stiffness), all to N = 20.
- plant (main plus -(2H)^2 K q) to N_obs = ln 1101.
- R = max over both seeds of max_t |q| / max_t |q_GR|, as in AC13 grade.py.
- Graded at N_obs = ln 1101. N = 10, 15, 20 are reported only.

## Lines (stated before running)

- KA1: AC13 witness (.05, .3, .001, 10), main, rtol 1e-9, rerun by AC23's import. It must reproduce AC13's
  committed max_I, max_II and detK_over_a6_min at N_obs to 1e-10 relative.
- KA2: as above.
- Convergence, per witness: R at N_obs agrees between the two tolerances to 1e-3 relative.
- Omega drift <= 1e-6 on main and gr to N_obs.
- POWER, per witness: the witness is POWERED if the plant reaches R >= 1e3 at N_obs at both tolerances.
  An unpowered witness is NO VERDICT for that witness.
- det K discriminator (second gate): main must keep min det K / a^6 > 0 over the run to N_obs. It has power
  on a witness if m2 reaches det K / a^6 <= 0 there, or fails at a kinetic singularity, by N = 20. The
  det K bite is reported per witness.
- Label:
  - FAIL if main R >= 1e3 at N_obs, or main min det K / a^6 <= 0, on any converged witness.
  - NO VERDICT (no power) if fewer than 3 witnesses are POWERED.
  - NO VERDICT if KA1 or KA2 fails, or any powered witness fails convergence or the Omega line.
  - PASS (HARMLESS, scoped) if every powered witness has main R <= 10 at N_obs and main det K > 0.
  - UNDECIDED otherwise (10 < R < 1e3 on a powered witness).
- The FAIL line 1e3 and the HARMLESS line 10 are AC5's and AC13's frozen lines, kept.

## Scope stated now

A PASS means: on rolling-clock FRW fixtures with dark-energy-like clocks, at fresh parameters, AC2q's slow
frozen roots do not amplify beyond 10x the GR control over the 7 e-folds since z = 1100. On each powered
witness the measurement can see a Hubble-rate wrong term, and the kinetic matrix stays positive. A PASS does
not cover the radiation era, decelerating fixtures, nonlinear health, sourced backgrounds or adoption.
