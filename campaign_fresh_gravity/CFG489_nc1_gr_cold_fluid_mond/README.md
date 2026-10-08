# CFG489: NC1 ("GR + Lambda, MOND only in the cold fluid") fails its attractor test. NC1 is DEAD by the frozen rule

Criteria: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), committed alone first in 6cce7b447. Correction 1 (numerics only) was
appended and committed alone in 32b3f9a35, before the scored run. Theory plus offline numerics; no downloads.

| run | outputs | checks | exit code |
|---|---|---|---|
| main (scored, corrected numerics) | `cfg489_nc1.out`, `cfg489_results.json` | 8/9 (C-energy fails by the committed reading, see Controls) | 1 |
| MUTATE (`CFG489_MUTATE=1`) | `cfg489_nc1_MUTATE.out`, `cfg489_results_MUTATE.json` | 6/7 (the anti-relaxation member must fail step 1, and does) | 1, as required |
| run 2 (frozen numerics, kept) | `cfg489_nc1_run2.out`, `cfg489_results_run2.json` | 7/9 (C-static and C-energy fail) | 1 |
| run 1 (killed), run 3 (aborted) | `cfg489_nc1_run1_partial.out`, `cfg489_nc1_run3_aborted.out` | logs only | - |

    CFG489_THREADS=4 OMP_NUM_THREADS=1 nice -n 15 python3 campaign_fresh_gravity/CFG489_nc1_gr_cold_fluid_mond/cfg489_nc1.py
    CFG489_MUTATE=1 CFG489_THREADS=4 OMP_NUM_THREADS=1 nice -n 15 python3 campaign_fresh_gravity/CFG489_nc1_gr_cold_fluid_mond/cfg489_nc1.py

On a shared machine with 4 workers, main takes about 19 min and MUTATE about 9 min (MUTATE reads main's JSON). The
1-D hydro core `cfg489_core.c` is compiled at run time into a temporary directory and called through ctypes.

## Verdict

| step | result |
|---|---|
| (1) G1 well-posedness | **PASS** at the target state, on every frozen background. But off the target the scored law is unstable (see below), and relativistic causality is only COND |
| (2) H3 attractor | **FAIL.** 18 of 20 scored cells crash, and the 2 that finish miss the law by 0.105 / 0.122 dex (the line is 0.05) |
| (3) H3 energy | **FAIL.** The target is 2.2 to 7.7 times more bound than the infall it must come from. Without a sink it cannot be reached |
| (4) G14 capture | **COND.** It passes with the record's local-density relaxation time and fails by 1e4 to 1e5 with an orbital one |

**NC1 is DEAD** by the frozen rule, because step (2) fails. The chassis question goes back to CFG484's runner-up, R04
(C-H/K plus a Horava UV sector M_*). Its decisive test is CFG319's moving-black-hole count redone with the z = 3 Horava
terms at the universal horizon.

**Constants.** None in the chassis. None new in the fluid sector either:
- lambda = 1 is the zero-constant t_dyn rate;
- s = +1 and gamma = 5/3 are structural choices, never scanned.

kappa = 1/2 is fitted, and the amount 5.364 is an input. No dark-matter particle is added; the cold fluid's mass is still
required. This is not "theory closed".

**The plain reading.**
- Moving MOND into a dissipative cold-fluid law gives a system that is well-posed at its target.
- But the target cannot be reached from cosmic infall with one rule for every object:
  - the energy is wrong by a large factor;
  - the scored law turns unstable while the fluid is still far below its target.
- Every relative tried misses too: P2, the nonlocal F-H flow, pure hydro, and switching the settling on late.

## What was tested

Gravity is the Newtonian limit of GR. The baryons are a static host. The cold fluid is a gamma = 5/3 gas, and its
target is

    rho_t = div[F(|A|) A_hat] / 4 pi G,   F(g) = g - g_N(g)   (nu_mono scored, P2 reported)

Here A is the fluid's TRUE 4-acceleration, A = Dv/Dt + grad Phi (sympy, control K1).

The scored member M1 is a relaxing settling stress:

    tau Dp_s/Dt = -(p_s - s (P/rho)(rho - rho_t)),   s = +1,   tau = 1/sqrt(4 pi G rho_m)   (lambda = 1)

Reported relatives:
- M2: tau -> 0;
- M3: CFG462's F-H flow made inertial (nonlocal);
- the "A-hyd" variant, where A is read from grad P alone;
- the EC form, where the settling stress's work is drawn from the fluid's own heat.

## Step (1): the dispersion relation

The linearised M1 system gives the cubic

    (w^2 + w_J^2 - c_s^2 k^2)(1 + B - i w tau) = k^2 C

sympy derives it from the linear system and checks its tau = 0 and s = 0 limits (control K2). Every background enters
only through n = k.N.k, and K3 shows 0 < n < 1 for both kernels.

| member / reading | homogeneous | deep SIS (60 cells) | frozen-coefficient sweep | high-k character |
|---|---|---|---|---|
| **M1 (scored)** | PASS, sup growth = w_J (Jeans) | 60/60 PASS | all PASS | the extra mode is damped as k^2 (parabolic) |
| M2 (tau -> 0) | PASS | 60/60 | all PASS | frequency bounded |
| M3 (F-H, nonlocal) | PASS | 60/60 | all PASS | hyperbolic |
| M1 with A read from grad P only | **FAIL**, growth ~ k^(4/3) | 0/60 | FAIL | Hadamard ill-posed |
| M2 with A read from grad P only | **FAIL**, growth ~ k^2 | 0/60 | FAIL | Hadamard ill-posed |

- **Well-posedness needs A to be the true 4-acceleration.** The target then includes the settling stress's own push, and
  that self-consistency regularises the system. Read from grad P alone, the target's grad A term makes the system
  ill-posed (CFG484's worry, confirmed).
- **Causality: COND.** The parabolic k^2 mode has unbounded signal speed in the Newtonian limit, so a covariant version
  needs an Israel-Stewart / BDNK-type regulator. That is untested.
- **Found after the freeze (reported, not a verdict input): M1 is unstable off its target.**
  - Linearise about a state with R = rho_t/rho different from 1. With gamma = 5/3 and s = +1, the high-k stiffness is
    K_eff = c_s^2 (1 + s(1 - R)) + s sigma^2 (R - 1 + n). It turns negative for R > 3.5 + 1.5 n.
  - Growth then appears at every large k. Its rate is about w_J sqrt((gamma - 1) R): bounded in k, but not in R.
  - The frozen line fails for R >~ 30.
  - An isothermal fluid has no such instability: K_eff = sigma^2 (1 + s n) > 0 for every R.
  - A settling fluid passes exactly through this regime. During infall the inner fluid sits at R ~ 1e2 to 1e5.

## Step (2): 1-D attractor runs (cosmic-share infall, CFG461's z_c = 1 turnaround)

Scored: M1 with nu_mono, 20 cells (point masses 1e9 to 1e12, CFG473's Hernquist a = 0.1 to 3 r_M, and CFG44's far-shell
pair, each on both footings). D40 is the largest |log V_c/V_law| out to the supply edge x_e = 5.85 r_M.

| cells | outcome |
|---|---|
| Hernquist (8) and far-shell (4) | all crash (dt < 1e-9) at t = 1.4 to 6, during the cold infall. Only 0.02 to 0.07 of 5.364 M_b is inside x_e by then |
| point 1e9, 1e10, 1e12 (6) | crash at t = 42 to 125, after partly settling (0.9 to 1.9 of 5.364 inside x_e) |
| point 1e11 canonical / alt | finish and are settled. **D40 = 0.105 / 0.122 dex**, with 3.16 / 2.74 of 5.364 inside x_e |

**Are the crashes physics? Checked as hard as a pass would be.**
- **They are not a time-step artefact.** At CFL 0.1 instead of 0.25 the same 6 point cells crash, and 1e11 gives the
  same D (0.105 / 0.122).
- **They are not a resolution artefact.** N = 480 crashes too.
- **The trigger is the off-target instability.** Take the exact target state and dilute the fluid outside 1 r_M:
  - to R = 10 with M1 on: it crashes in t = 0.19;
  - to R = 2 with M1 on: no crash;
  - to R = 10 with the settling off (pure hydro): no crash.
- **The C-static control now passes** (D = 4e-4 / 5e-4 over 20 t_e). So the code holds the exact target when it is given
  one.
- **Run 2's crashes were partly numerical.** Run 2 used the frozen numerics, whose first shell carried 23 times its
  neighbour's mass. Those numerics failed C-static, which is why correction 1 was made. Under the corrected numerics the
  crashes persist, but later for the point masses.

**Every run that finishes misses, whatever the member** (D40 in dex; point masses, canonical then alt):

| run | 1e9 | 1e10 | 1e11 | 1e12 |
|---|---|---|---|---|
| M1 (scored) | crash | crash | 0.105 / 0.122 | crash |
| P2 kernel | crash | 0.154 / 0.174 | 0.082 / 0.097 | crash |
| M3, F-H (nonlocal) | 0.312 / 0.336 | 0.232 / 0.254 | 0.151 / 0.170 | 0.083 / 0.098 |
| pure hydro (s = 0) | - | 0.224 (canonical) | - | - |

M2 crashes at once in every cell. Its implicit instantaneous solve is numerically unstable here (reported, not
scored).

Two more runs miss as well:
- **M1 switched on only after the gas has virialised** (hydro until t_coll + 5 t_e) reaches D = 0.138 at +10 t_e, then
  crashes.
- **M3's miss is ordered by mass**: 0.31 at 1e9 down to 0.08 at 1e12. That is the order of the energy deficit below.

The far-shell test could not be scored, because both members of the pair crash, identically and early.

## Step (3): energy

- **(3a) Static budget.** (E_t - E_i)/|E_t| runs from -0.54 (1e12) to -0.87 (1e9 alt) for the point masses. It is -0.64
  to -0.80 for the Hernquist and far-shell hosts. The line is 0.1 in magnitude.
  - So the target state is 2.2 to 7.7 times more bound than the cold turnaround sphere it must form from.
  - With no sink the fluid cannot get there. This repeats CFG461/462 (contraction factors R_vir/r_e = 3.50 / 2.38 /
    1.62 / 1.11 canonical) inside a time evolution.
- **(3b) Reservoir work.**
  - Where it can be measured (the two 1e11 cells), the settling stress drew 0.92 / 1.23 |E_t| from an outside reservoir.
  - The crashed cells had drawn up to 10 |E_t| before crashing (1e9 alt: 35.4 against |E_t| = 3.58).
- **(3c) Energy-conserving form (reported).** The settling stress's work is taken from the fluid's own heat.
  - Every EC run crashes.
  - The settling entropy production is negative in 18 of 20 cells (positive only for the two 1e11 cells): the stress turns heat into work, against the second
    law.
  - 1e12 hits the heat floor 3.5e6 times.

## Step (4): capture by the Sun (v_rel = 230 km/s through the MW fluid, CFG484 N1d inputs)

- **(4a) Liouville cap.** 1.1e-7 (Mars) and 8.5e-9 (Saturn) of the ephemeris bounds on the canonical footing; the alt
  footing is similar. PASS.
- **(4b) In-transit relaxation, scored.**
  - The relaxation time from the local fluid density is tau = 60 / 56 Myr. The crossing time is about 1e-9 of that.
  - Even if the fluid were trying to build the Sun's own nu_mono target (76,893x / 13,786x the bound), at most
    1.4e-3 / 1.3e-3 of the bound (canonical) and 1.9e-3 / 1.8e-3 (alt) can be built, a safety factor of 3 included.
    PASS.
- **(4c) Orbital-time reading** (the CFG464 ledger formula applied at r). tau = 109 days at Mars, so the fluid relaxes
  fully in transit: 76,893x and 13,786x the bounds. FAIL.
- **So G14 is COND.** It passes only because the record's t_dyn uses the local matter density, and the Sun's mass is not
  local density at 1 AU.
- Reported: the Bondi-Hoyle radius is 0.02 AU, and 3e-10 Msun is accreted into the Sun in 4.6 Gyr.

## MUTATE

- **Anti-relaxation (s = -1) fails step (1)** in every member and background. For M1 the growth goes as k^2 (sup = 1e16
  w_J). The 1-D run crashes at t = 1.6. The run exits 1, as required.
- **Target a0 -> 2 a0.** Only one cell can be compared (1e11 canonical; the others crash in main or in MUTATE).
  - The attractor moves by only +0.015 dex, against the +0.060 predicted (rms 0.046). So it does NOT move as predicted.
  - The finished equilibrium follows the target's a0 at about a quarter of the expected size. It is set mostly by the
    thermal and energy state, not by the law.
- **A coincidence was caught, and it is not a result.** With the 2 a0 target, the 1e12 cells (which crash in main)
  finish at 0.037 / 0.051 dex from the TRUE law. A doubled-a0 target can offset part of the energy-limited miss; it says
  nothing for the true-a0 law.

## Controls (main)

Load-bearing, passing:
- K1: the 4-acceleration of a moving fluid (sympy).
- K2: the cubic (sympy).
- K3: n in (0, 1).
- K4: the C target routine reproduces P2's M(sqrt(1+x^2) - 1) to 2e-14; the nu_mono edge is 5.84976.
- K5: CFG461's contraction factors, 3.498 / 1.967 / 1.340.
- K6: CFG484 N1d's ratios, to 1e-4.
- C-static: the point mass and Hernquist a = 1.

**C-energy fails by the committed reading.** Correction 1 says a crashed run cannot certify conservation.
- The run C-energy is defined on, the EC run of the 1e10 point mass, crashes at t = 89 of 319.
- Up to that point it conserves energy to 7.2e-4 |E_t|, inside the 2e-3 line.
- The pure-hydro run conserves energy to 2.8e-4 over its whole length.
- So main exits 1 because of a control whose run the physics crashes, not because of an integrator fault.

Reported: C-heat / C-cool (the exact target with e scaled by 1.2 / 0.8) settle at D = 0.029 / 0.032. The target's grip
against a 20% wrong temperature is about 0.03 dex.

## Disclosures

**Not blind.** The source lanes were read first, and the expected outcomes were written into the frozen file. They were:
- (1) pass;
- (2) and (3) likely fail;
- (4) pass under local tau and fail under orbital tau.

The off-target instability was not expected. It is reported as a post-freeze finding.

**Correction 1 (32b3f9a35, numerics only).**
- Run 2 used the frozen numerics: wall 0.02 r_M, wall target 0, and a grid geometric in enclosed mass.
- It failed the load-bearing C-static control: the Hernquist target crashed at t = 0.25 through a grid-scale sawtooth
  beside a first shell 23 times heavier than its neighbour.
- Every scored cell of run 2 crashed there at t = 0.3 to 2 (`cfg489_nc1_run2.out`, kept).
- The correction changed four things:
  - the wall moved to 0.05 r_M, with its own target and an inert core of the law's phantom inside it;
  - the shell masses became smooth geometric;
  - the step cap went from 4e7 to 2e8;
  - nothing else.
- Before committing it, I ran the corrected numerics once on the 1e10 canonical point cell, with the smallest shell at
  1e-4 M_b and no core. It finished at D40 = 0.180.
  - In the committed setup (2e-4 M_b and a core) that cell crashes instead.
  - This shows the crash onset is sensitive to the numerics, while the miss is not.

**Readings for cases the text did not foresee** (committed with correction 1):
- a crashed run cannot certify C-energy;
- if both resolutions crash, the outcome counts as consistent;
- a crashed run's W_res is untested, not passed.

**Runs.**
- Run 1 was SIGTERM-killed on the shared machine before writing outputs. Its log is kept; it showed K3 failing on
  floating point (P2's g_N' rounds to 1.0 at 1e8 a0).
- K3 is now computed in cancellation-free form: same identity, same line.
- Run 3 aborted on an overflow in the N = 480 mass grid (log kept), and was fixed before run 4.
- From run 2 on, everything ran under `nice -n 15` with 4 workers and 1 BLAS thread, at the coordinator's request. This
  changes no physics.

**Post-freeze diagnostics** (none is a verdict input):
- the off-target linear analysis;
- the CFL 0.1 re-run;
- the R = 2 / 10 dilution test;
- the late switch-on;
- the frozen-numerics re-checks.

## What this lane cannot say

- It tests one declared relaxation law (M1) and reports four relatives. DEAD applies to NC1 as CFG484 posed it, scored
  through M1. It does not exclude every possible fluid dynamics. For example, an isothermal closure avoids the off-target
  instability, but not the energy deficit.
- The setup is limited: spherical, static baryons, the Newtonian limit, one collapse redshift, and one infall initial
  state. The baryons sit in place from turnaround.
- It derives nothing about kappa, the amount 5.364, or the switch (H4 is not tested). It says nothing about data
  favouring the framework.
