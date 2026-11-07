# WL1 result: the law switched by khronon multi-streaming. KiDS passes; the hosts' retained phantom over-sources CMB lensing. FAIL (stage 2)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane. The key is not in v3s or AC2q.
Footings: canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2. They are never pooled.

- **Criteria:** FROZEN_CRITERIA.md, committed and pushed alone before any script (origin c371c8ce59).
- **Amendment:** AMENDMENT_A1.md, filed after stage 1's numbers and before any stage-2 number, with disclosure (origin
  bcaa90c6dc). It replaces stage 2's 15.6 Mpc grid reading. That grid cannot contain any host's shell-crossed region.
- **Script:** wl1.py, giving wl1.json/.out (main) and wl1_MUTATE.json/.out. Logs are in run_main.txt and run_mutate.txt.
- **Compute:** one thread, nice 15, about 30 s, RSS 145 MB.
- **Reuse:** GB1's battery executed from its source; QX5's KiDS loader; QX7 iter_4, SV5 iter_1/iter_2 and the
  Driver+2022 GSMF from closure_program_2026_10_27/population.

## The key, and why it was not already dead
K_ms keeps the law's phantom ON where the khronon flow has folded (multi-stream) and OFF on the single-stream linear
web.
- **Dead-key list:** every dead key in SEED 11-06 and DIRECTION 11-07 splits discs from hot systems. K_ms splits
  collapsed hosts from the web instead.
- **DX1 D4:** D4 kills history-based removal of a cold component. K_ms is a present-state count acting on the phantom.
- **OUTER_EDGE_CHECK:** that check concerns the action's own switch. K_ms is an added switch.

## Numbers (canonical / alt; margins from wl1.json)

| Item | Canonical | Alt | Line | Reading |
|---|---|---|---|---|
| R_ms ceiling, law-on turnaround today with dust, at M_b 10^9.4 / 10^10.9 | 1.47 / 3.49 Mpc | 1.54 / 3.65 Mpc | none | input |
| R_ms lower reading, law-on, baryons only | 0.92 / 2.18 Mpc | 0.96 / 2.28 Mpc | none | input |
| **K-G6 KiDS 59 pts, ceiling** (4G DeltaSigma shift vs law) | +0.0011 dex | +0.0009 dex | abs <= 0.05 | PASS (margin 0.049) |
| **K-G6, lower reading** | +0.0051 | +0.0043 | abs <= 0.05 | PASS (margin 0.045) |
| K-G6, self-consistent R_ms (Newton outside R_ms), dust / no dust | -0.039 / -0.137 | -0.039 / -0.137 | abs <= 0.05 | reported: PASS / FAIL |
| **GB1 G1-G8** | equal to L0 on every row | equal to L0 on every row | no row worse than L0 | PASS (max r/R_ms 0.08, at KiDS) |
| **Stage 2 q_pop = rho_ph,pop / rho_d at z 1** | **0.936** (r_pop 3.75) | **1.079** (r_pop 4.32) | <= 0.0354 (r <= 1.072) | **FAIL, x26 / x30** |
| q_pop at z 0.5 / 2 | 1.31 / 0.54 | 1.51 / 0.62 | <= 0.0354 | reported (x37 / x15; x43 / x18) |
| q_pop at z 1 with the self-consistent R_ms (NC) | 0.384 | 0.423 | <= 0.0354 | reported (x11 / x12) |
| Stages 3-4 (SV5 iter_2 C2-C4, QX3 shape) | none | none | none | NOT REACHED |

**Known-answer checks.** All PASS:
- KA-SV5: r 74.7424 / 89.3630 and Sigma_* 7.969 / 5.998 rho_DE.
- KA-GB1: L0 class means |d| = 0.
- KA-K: KiDS base 0.141707 / 0.101597, equal to QX7 iter_4.
- KA-P: 4G DeltaSigma / g_law = 1.0014 at y = 1e-4.
- KA-T: the Newtonian shell r_ta is 0.90 x QX10's 5.55 rho_m rule, within 20 %.
- KA-A1: the GSMF over 9-12 gives 0.957 of the analytic total.

**MUTATE.** Every arm bites:
- Switch ON: KiDS shift 0, GB1 = L0, and the web gain is SV5's 74.7 / 89.4 by identity.
- Switch OFF: G1 SPARC FAILS (Z +0.43), and K-G6 FAILS (-1.48 / -1.52 dex).
- R_ms x 100: K-G6 moves to 0.
- A1 R_ms -> 0: q_pop = 0.

## What it means
1. **The predicted kill did not land.**
   - Under the law, an isolated galaxy's turnaround radius today is 1-3.7 Mpc. That is large enough to hold every KiDS
     bin out to 2.8 Mpc.
   - So on its generous frozen readings, a multi-stream switch keeps galaxy lensing and every GB1 row exactly as the
     plain law has them.
   - The pass leans on the law-on collapse. If the switch is applied inside the collapse itself, so that shells outside
     R_ms fall under Newton, R_ms shrinks to 0.13-0.83 Mpc. KiDS then passes only with the cold component counted
     (-0.039) and fails without it (-0.137).
2. **The real wall is arm (i)'s two halves against each other.**
   - KiDS needs each galaxy to keep its phantom out to about 1-3 Mpc, roughly 1e12-1e13 Msun per L* galaxy.
   - Summed over the observed stellar mass function, that retained phantom is a lensing source of 0.9-1.1 times the
     whole dust target at z 1. This holds with M_b = M*, the lower R_ms and bias 1, all chosen to make it small.
   - CMB lensing allows 3.5 % of the target. Moving the switch from the web to the hosts does not remove the law's
     extra lensing. It concentrates the extra lensing in the hosts, where KiDS measures it, and the CMB-lensing kernel
     still integrates it.
   - The overshoot is 26x / 30x at the graded epoch. It is still 11x with the self-consistent radius.
3. **Scope.** This holds for any arm-(i) key that keeps the law on where KiDS needs it. The q_pop statistic depends
   only on the phantom retained inside the KiDS range, not on how the switch is keyed. So WL1 also closes SV5's
   two-switch escape at arm (i): arm (ii) never gets a law-off web that is consistent with galaxy lensing.

## Not done or not evaluable
- q_pop assumes the retained phantom adds to the dust's lensing at bias 1, and uses the z = 0 GSMF at z 0.5-2. A
  full halo-model lensing spectrum on PR4 was not run. The 11-43x margin is the reason no such run was needed for the
  label.
- The khronon's own fold radius was not solved in 3D. Turnaround is used as its ceiling, since AC14 gives the clock a
  Hubble-sized pressure scale, so the clock is carried by the converging flow.
- Stages 3-4 were not reached. Lean was not used.

## Post-result scope note (added after grading; the frozen criteria are unchanged)
**Split with EW3 (Repository session).** WL1 grades the shared SV5 two-switch door: law off on the single-stream web,
the charge-switched K(Q) sector on the law-off web, and the KiDS shell-crossing kill. EW3 grades only the switch
candidates WL1 does not cover, cites WL1, and stops if WL1 covers everything. EW3 (520ed75443) holds a map row only.
This wording arrived after WL1's criteria were frozen and graded, so it is recorded here, not in FROZEN_CRITERIA.md.

**EW3's two ungraded notes, answered (reported, not graded, post-result).**
1. *KiDS points beyond turnaround, per mass bin.* EW3's turnaround radii (QX10's rule: 0.59 / 0.71 / 0.83 Mpc) are
   WL1's self-consistent NC reading. Source: per_bin_reported.py, giving per_bin_reported.out. The shift vs the
   plain law per mass bin (log M_b 9.4 / 10.45 / 10.7 / 10.9; R_max of the points 0.50 / 1.69 / 2.25 / 2.83 Mpc) is:

   | R_ms reading | Shift per bin, both footings | Result |
   |---|---|---|
   | NC (QX10 turnaround) | -0.009 / -0.041 / -0.047 / -0.058 | top bin beyond 0.05 on its own |
   | NL (Newton, no dust) | -0.083 / -0.137 / -0.155 / -0.168 | all bins fail |
   | Ceiling / lower (law-on turnaround, the graded readings) | at most +0.008 | all bins pass |

   So EW3's sharpened kill holds wherever the shells beyond turnaround are Newtonian. The graded law-on readings pass,
   because the law-on turnaround already reaches 1.7-3.7 Mpc. Either way, stage 2 sets the label.
2. *A charge-keyed law cannot turn back on (law off gives D.P = 0, Sigma = 2X on both the web and outskirts).*
   - WL1's key reads the khronon fold (the sign of the label-map Jacobian J), not the charge. That objection does not
     apply to it.
   - Whether arm (ii)'s charge-switched dust still separates hosts from the web once the law is off in the outskirts
     was NOT checked. Stage 3 was not reached, because stage 2 fails first.
   - EW3's point stands as a second obstacle for arm (ii) under any law-off outskirts: Sigma = 2X there equals the
     web's.
