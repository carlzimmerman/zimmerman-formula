# UX1_action_class: CONDITIONAL LEAD under the frozen labels, held only by K8, which is v3s plus a separate dust and not a new class. No structurally different class passes

**Plain answer.** I found no covariant action for the exact law outside what failed. The bimetric, nonlocal, mimetic and two-potential classes all miss at least one gate. The one row that reaches the frozen CONDITIONAL LEAD label is the record's own v3s with a separate dust beside it. Its one open gate is health, and it carries the double count the v3s verdict already named. This is a statement about the ten listed candidates, not a no-go theorem.

Criteria `FROZEN_CRITERIA.md` (31ed37d44d, alone first, not blind). Script `ux1_gates.py`, solver `ux1_q2.py`, numbers `ux1_gates.out` and `.json`. kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s^2, never pooled. No dark matter particle. The cold sector stays retired: nothing here reinstates it, only the owner can. Not theory closed. Nothing here says the data favour the framework.

## The table
PASS, FAIL or ND (not decided). [LIT] is from a fetched arXiv abstract or from memory, PROVISIONAL. [REC] is read from the record, not rerun.

| | Candidate, credit | G1 static law | G2 Solar System | G3 health | G4 dust term | Non-PASS |
|---|---|---|---|---|---|---|
| K1 | BIMOND, Milgrom 2009 | PASS | **FAIL**: Q2 passes, planets fail | ND | FAIL, none in the action | 3 |
| K2 | BIMOND + twin dust, Milgrom 2010 | PASS | **FAIL**, same | ND | PASS, dust era, locked branch | 2 |
| K3 | Bigravity, Hassan-Rosen 2011; dRGT potential | **FAIL**, no M^(1/2)/r | not reached | PASS [LIT] | FAIL without a species | 3 |
| K4 | Nonlocal, Deffayet-Woodard 2011 | PASS | FAIL, no screen | **FAIL** [REC 10.5281/zenodo.22255522] | FAIL | 3 |
| K5 | Second field completing gamma_L, this lane | PASS | PASS only with the negative-norm field | **FAIL** | ND (C7's runaway is for one dust shape) | 3 |
| K6a | Mimetic f(box phi), Chamseddine-Mukhanov 2013 | ND | ND | **FAIL**, ghost or gradient | PASS | 3 |
| K6b | Mimetic with matter coupling, Vagnozzi 2017 | ND | ND | ND | PASS | 3 |
| K7 | QUMOND two-potential parent, Milgrom 2010 | PASS | FAIL (1.69-3.70 canonical, 1.90-4.03 alt, E2) | **FAIL**, indefinite | FAIL | 3 |
| K8 | v3s + separate P(X) or mimetic dust | PASS, baryons-only source | PASS [REC C6, E2] | **ND** | PASS | **1** |
| K9 | Refracted gravity, Matsakos-Diaferio; covariant form Sanna et al. | ND (density-only form FAILS) | ND | ND | ND | 4 |
| K10 | Superfluid, Berezhiani-Khoury 2015 | ND | ND | ND | FAIL [REC STANDING item 4] | 4 |

**How K8 gets its label, and why it isn't an escape.**
- Its G3 is ND because 2D and 3D evolution and a moving-interface proof are open in v3s (V3_FULL_PICTURE), and I did no health calculation for the two sectors together. It doesn't come from a clean run.
- G1 passes only with baryons as the source. Reported G5: forest-passing dust falls in, capture 0.76 against a tolerance of 0.20 / 0.03 (X22), and at least 0.54 of the fair share even with GR-only dust (X57 M1). So the law on baryons does not hold in galaxies. That is the v3s verdict's objection and BOLTZ1's open decision, not a new result.
- Its law sector keeps the literal K(Q) or DBI problems (Q6, Q7), and the owner has closed v3s. Nothing here reopens it.

## The result worth keeping: K1's Q2 passes without a screen, and the tail still sinks it
Writing out BIMOND's weak field gives g = g_N + a g*, with a the twin Einstein-term coefficient and a + b = 1, and div[s grad f*] = a div F_N. The exact law fixes s = a^2 g/a0, and a cancels (sympy, A1 to A6). So with psi = a f* and h = |grad psi|:

    div[ h/(a0 - h) grad psi ] = div F_N,   g = g_N + grad psi

This is neither AQUAL nor QUMOND, and the anomalous field has a hard cap, h < a0. Near the Sun the l = 2 part of psi follows a stiff regular branch, c2 ~ r^3 (ODE, slope 3.0000 at 1e-3 r_M), so q falls as r instead of going to a constant. Q2 at Saturn, as a fraction of the Hees line 9e-27 s^-2:

| | E0 | E1 | E2 | E3 |
|---|---|---|---|---|
| canonical | 0.029 | 0.058 | 0.077 | 0.107 |
| alt | 0.033 | 0.059 | 0.078 | 0.108 |

AQUAL on the same solver gives 2.44-4.55 / 2.85-5.15 x the line, reproducing E2 to 0.45 % in all eight cells. These K1 numbers match the solve at 0.1 r_M onto that ODE, since the full solve can't converge on the cap at Saturn's radius. Note r^3 is not the r^2 form Hees fits, so this is a comparison of size at Saturn only.

**It doesn't help.** The radial tail is the law itself: g - g_N = a0 g/(g + a0) -> a0. At SPARC's 99th percentile h is 0.957 a0 canonical, 0.949 a0 alt. M1 read that as planets 1.0e4 to 6.4e4 x their bounds canonical, 1.2e4 to 7.7e4 alt. Only Q2 is escaped.

## What blocks a screen (the attempted general results)
- **T-B, PROVED IN STATED CLASS.** One static field h driven by a local convex functional has dh/dg_N = 1/W'' > 0, so it can't roll over at planets. It extends M1's T2 to BIMOND's form. A roll-over needs an indefinite functional, which is K7 (det -4).
- **T-A, PROVED IN STATED CLASS.** A linear Lorentz-invariant kernel with positive spectral weight has d(k^2 D)/dk^2 = sum w mu^2/(k^2 + mu^2)^2 >= 0. So it can't weaken an extra force toward short distance. 1/(k^2 + e k^4) has a negative-residue pole. K5 is the concrete case: a positive-norm second field lowers the stiffness, and the gamma_L sign needs a negative-norm field.
- **T-C, NUMERIC ONLY.** omega^2 = A k^4 on a tilted slice has nonreal roots above kappa_c (none at 0.5 kappa_c, two from 0.9 kappa_c, at A 1e-4, tilt 0.01), and none on the rest slice. So k^4 stiffness needs a global time function. This reproduces I1 for one case; it is not a theorem.

**What these leave open, so no universal no-go is claimed:** nonlinear derivative screens other than M1's cubic and quartic galileons; two-scale operators that aren't linear kernels; a global-foliation theory other than the khronon; a law exact only below some x and different above it, which fails G1 as frozen and which data don't reach above x about 22.

## Corrections to the trilemma as stated
1. **"Screening needs gamma_L" is too strong.** O1 reports velocity screening passing Cassini with gamma_L removed (estimate), though it fails satellites and Coma. K1 passes Q2 with no screen. What needs protecting is the a0 tail on planets, and Q2 is the smaller problem.
2. **"Untwisted fails growth"** is the mu_K cap, as M1 found, and it applies to one K(Q) doing both jobs. A separate dust removes the growth horn and brings in the double count instead. So the working form is: **law, planets and a dust that stays out of galaxies**, and the third is where the record has no action.

## K2, reported only: an action-level exclusion that I did not grade as a pass
The cold sector is retired, and this reinstates nothing. It is here because the requirements list says the record has no process for rows 4 and 11.
- Milgrom's twin matter repels ordinary matter in the deep regime [LIT, 1001.4444]. My reduction agrees: ghat = g_N - (b/a) h for a baryon source, repulsive once (b/a) h > g_N.
- With the two scale factors locked, the Friedmann equation of g has a dust term if rho_d/rho_b = a/b (L1). Then the difference field's source a rho_b - b rho_d vanishes at the cosmic ratio. So a system at that ratio has no law term, and a baryon-rich one does. This is a selector by baryon fraction, untested on any data.

**Its costs, all computed or plain:**
- G2 fails as above, and G3 is ND. Together that is two non-PASS gates.
- One shared vacuum term breaks locking unless a = b (L2), so late times need a second vacuum number or the metrics unlock.
- The adiabatic point is not protected: d'' = K sqrt(d) has d = K^2 t^4/144 from d = 0 with no seed (L3). ESTIMATE of the separation at t = 1/H0 with today's density held fixed and weight w/a^2 = 1: 2.06 Mpc canonical, 2.49 Mpc alt, on BOLTZ1's native h and Omega_m. Not an evolved calculation. X57's M6 limits on depleted patches apply.
- The radiation era was not done: baryon-side photons alone break locking. The a/b ratio becomes a coupling set by the abundance, a new number.

## Failed checks and limits
27 of 29 checks pass.
- **B4 FAIL.** I expected at least two negative velocity-Hessian directions on every homogeneous background, with the law's own M at Y < 0, so one constraint would leave a negative mode. Result on 3348 samples: 1099 all-negative, 2178 two-negative, **71 one-negative**. So 97.9 % have the negative mode by that argument and 2.1 % don't. The backgrounds are off-shell, and the argument is interlacing, not a full Dirac reduction. **So K1 and K2's G3 stays ND, not FAIL.** What is proved is the extra degree of freedom: velocity rank 2 -> 3 (B3). Boulanger, Damour, Gualtieri, Henneaux 2001 [LIT, hep-th/0009109] rule out consistent two-derivative graviton cross-couplings under their assumptions, and I did not check how BIMOND's nonpolynomial form sits there. This doesn't change the verdict, since G2 already fails.
- **C2b FAIL.** Two K1 cells, canonical E1 and alt E2, stalled at step 8e-6. Their values sit on the trend of their neighbours and at 0.058 and 0.078 of the line, so the Q2 reading stands.
- **First B3 check failed and was replaced.** It compared M'' = 0 with M'' not 0 and found 3 -> 3, since the cross term already acts at M' not 0. The first run's output, which then crashed on a coding error in section K, is kept as `ux1_gates_RUN1_crash.out`.
- **The solver took several failed versions.** Primal Newton stalled on the cap, and an early flux-function form was noisy. Those were caught by the E2 known answer, before any K1 number counted. A resolution check moved c2(0.1) by 2.7 % (C3).
- **Scope of the minisuperspace.** K1 and K2 G3 use FRW only. Y is Milgrom's combination as I recalled it; I did not check his full variants, or twin-sector scalars.
- **Literature is PROVISIONAL.** Abstracts were fetched for 0912.0790, 1001.4444, 1708.00603, 1708.02951, 2109.11217, hep-th/0009109 and 2512.09353. Fetching corrected me: Vagnozzi 2017 uses a matter coupling, not f(box phi), hence the K6a/K6b split. Takahashi-Kobayashi 2017 [LIT] report K6a's instability, which `I1` reproduces on Minkowski: L = (3 - 2/f'') zeta_dot^2 + (grad zeta)^2. Babichev, Deffayet, Esposito-Farese 2011 (k-mouflage) is covered only through M1's R2c. Milgrom 2512.09353 says he has no consistent cosmological model yet [LIT].
- **Not run:** K4, K8 and K10 are record readings. K9 is an abstract plus one scaling check.

## Reproduce
`OMP_NUM_THREADS=1 nice -n 15 python3 -W ignore ux1_gates.py` (exits 1, because of B4 and C2b). Twin `UX1_MUTATE=1`, writing `ux1_gates_MUTATE.*`. A rerun is byte-identical in `.out` and `.json`. The twin passes 23 of 29: its three mutations bite on A1, A4, A5 and E2, on top of the same B4 and C2b. The sign flip in A1 and the dropped factor in A4 and A5 change only the sympy lines, so the Q2 numbers don't test them; the known-answer check C1 covers those.

No deposit. PAPER67, the ledger, the outside summary and other lanes are untouched. kappa = 1/2 FITTED. Not theory closed.
