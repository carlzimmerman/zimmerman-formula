# MK2 AMENDMENT A4 (an added row; committed alone)

**What existed when this was written.** Graded numbers already existed for rows a1, b, c, d, g and h (`mk2_rows.out`)
and for row e on the canonical footing (`run_sparc.txt`). None existed for the row added here. Nothing below changes a
frozen row, line, grid, known answer or label rule.

**Why.** The lead asked for it. COL1 found that a cold clock falls in and folds (BREAKS DOWN). FLD1 found that the folded
region stops 1.3 to 5.4 times short of where KiDS sees the law. Both rest on the clock being cold. With the exponential
term the clock's dust has a fixed sound speed, so around a galaxy it may be pressure-supported instead.

## Row i: is the clock static out to the law's range?

For each c_s on the common grid (10 to 1e4 km/s, 0.025 dex), both footings, at log M_b 8, 9.4, 10.45, 10.7 and 10.9
(the four KiDS masses of COL1 / FLD1, k = 1, as FLD1 used them).

- **(a) A static solution.** Does the hydrostatic clock (static clock, n = n_mean exp(phi/x_T), A = grad Phi) solve the
  action's static equations out to 1 Mpc, including the dust's own gravity? Operationally: the capped static state of
  rows e / f exists on the branch (A1: Hernquist x_a 0.2, continuation in decreasing c_s from no dust; A2: global cap,
  X = PD1's share).
  - Reported: r_c, the radius where the state's charge reaches the share, which is where form B's law ends.
  - A state with r_c < 1 Mpc is still a solution to 1 Mpc: beyond r_c the charge has ended and the field is Newtonian.
- **(b) Supersonic infall.** v_inf(r) = sqrt(2 [Phi(R_ta) - Phi(r)]) is the speed of a cold shell released at rest from
  today's turnaround radius R_ta (FLD1's R_ta at z 0, below). It falls in the static capped law potential of (a) at no
  dust.
  - This is an upper estimate: shells passing r today turned around earlier, at smaller radii.
  - It is evaluated at r = 10, 100, 300 and 1000 kpc where r < R_ta (beyond R_ta nothing is falling in today).
  - Reported beside: the same with the baryons' Newtonian potential only (a clock that has no law yet, A = 0).
  - Supersonic means v_inf/c_s > 1. There, COL1's fold could return.
- **(c) Reachability by pressure.** The sound-crossing times 300 kpc/c_s and 1 Mpc/c_s, against the age t0. t0 is
  computed from F1A's B2 background on each footing (flat, Omega_m = (omega_b + omega_d)/h^2, radiation included). The
  line is t_sound(R_need) <= t0, with R_need = max(r_c, 1 Mpc).
- **(d) The law's range today under this term.**
  - R_law = r_c if (a), (b) and (c) hold at that mass.
  - Otherwise the row says where it fails: the supersonic radii, or the radius sound cannot cross within t0.
  - R_law is printed beside FLD1's R_fold(z 0), ONE1's inner and middle window edges, and PD1's cap R_cap.

**FLD1's inputs** (canonical, physical kpc, from `fable52_push/FLD1_fold_reach/RESULT.md`; FLD1 says alt differs by
under 0.5 % in R_fold, and its cap is 9 % smaller):

| log M_b | R_ta | R_fold(0) | inner / middle window edge | R_cap |
|---|---|---|---|---|
| 8 | 40 | 21 | - / - | 23 |
| 9.4 | 120 | 62 | 81 / 190 | 116 |
| 10.45 | 268 | 139 | 272 / 637 | 389 |
| 10.7 | 325 | 169 | 362 / 849 | 518 |
| 10.9 | 378 | 197 | 456 / 1069 | 653 |

**Label for row i, per footing:**
- **STATIC TO THE LAW'S RANGE [c_s interval]** if some grid c_s satisfies (a), (b) and (c) at all five masses (the
  interval is the set of such values).
- **NOT** if none does.
- **NOT EVALUABLE** if an input cannot be computed.

Row i is reported beside the graded rows. It does not enter MK2's frozen label rule, which this amendment does not
change.

**What it does not show.** It is a static and timescale argument, not an evolution run. A subsonic estimate says pressure
could hold the clock up. It does not show that the state forms, that infall stops without a caustic, or that the
early, colder universe (the comoving Jeans length was smaller then) does not fold before pressure acts.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
