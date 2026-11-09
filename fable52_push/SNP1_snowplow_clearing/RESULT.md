# SNP1 RESULT (criteria 9ff5f59a72)

**SNP1: FAILS / FAILS** (canonical / alt). Failing gate **G-K at every nucleation epoch**; G-F2 as well at z_n 6 and 3.
**SAME UNDER THE ENERGY-CONSERVING BRACKET** (that bracket also fails G-F2 at z_n 1.5, through the lightest bin). The brackets
X = 0 (share never bound) and X = 3 also FAIL, X = 0 on G-K alone.

TEST lane, quarantined. Adopts nothing and relabels nothing. Not registered. kappa = 1/2 FITTED; not theory closed. Footings never
pooled (canonical / alt below). Every known answer passes, every MUTATE arm bites, SNP1.lean compiles (28 theorems, standard axioms
only) and its twin does not.

The question: can the law's own wall pressure (SWT1 T3) clear the cold component from around galaxies and keep it out, in the
record's expanding background? Answer: **it can clear the inner 200 kpc only if the wall nucleates late (z_n 1.5), and nowhere
does it reach KiDS's range.** With the record's share bound, the wall stalls at 6-98 kpc or collapses (z_n 6, 3), or stops at
207-309 kpc (z_n 1.5);
with no bound share at all it reaches 0.43-0.63 of R_K for the three heavier bins. The static stable balance against today's mean
density is already short (0.72-0.91 R_K), so the G-K fail does not hinge on the dynamics.

## 1. Part A, exact (Lean, SNP1.lean)

Forces in a0 M_b; y = G M_b / (a0 R^2), u the law's field inside the wall, r_M = sqrt(G M_b / a0).

- **A.1 The wall's force is bounded.** F_w = 4 pi R^2 p_wall = a0 M_b W / y <= a0 M_b, and <= (2/3) a0 M_b sqrt(y). Sharper, new:
  u^3 / (2 (1 + u)^2) < W(u) < u^3 / (1 + u)^2, so **(1/2) a0 M_b mu < F_w < a0 M_b mu**, mu = u / (1 + u). A shell weighing more
  than a0 M_b feels a net inward force whatever the baryons do.
- **A.2 A settled shell of fixed mass m M_b is unstable** (the proposer's hand algebra holds). Equilibrium is Psi(u) = W / y^2 = k,
  k = m (1 + m/2); Psi is strictly decreasing, so the root is unique, the net outward force y (Psi - k) is positive outside R_eq
  (expelled) and negative inside (falls). Bracket k (k + 1) < (R_eq / r_M)^2 < 2k (2k + 1); deep closed form R_eq = (3/2) k r_M.

| shell | k | exact R_eq / r_M | deep (3/2) k | Lean bracket | R_eq, log M_b 9.4 / 10.45 / 10.7 / 10.9 (canonical; alt) |
|---|---|---|---|---|---|
| the record's share, m = R = 5.562 | 21.03 | 31.92 | 31.54 | 21.5-42.6 | 62 / 207 / 276 / 347 kpc (56 / 188 / 251 / 316) |
| 3 x the share | 155.9 | 234.2 | 233.8 | 156-312 | 0.45 / 1.52 / 2.02 / 2.55 Mpc (0.41 / 1.38 / 1.84 / 2.32) |

- **A.3 A shell that sweeps up the mean background has a unique, stable balance** (F_w strictly falls with R, the swept weight
  strictly rises). Deep limits: R^2 (2 pi G rho) = v_f^2 for M_s << M_b, R^5 (4 pi^2 G rho^2) = 3 M_b v_f^2 for M_s >> M_b.

| log M_b | swept balance at today's mean, Mpc (canonical / alt) | / R_K | with IGM baryons, / R_K | R_K, Mpc |
|---|---|---|---|---|
| 9.4 | 0.729 / 0.744 | 1.45 / 1.48 | 1.36 / 1.39 | 0.504 |
| 10.45 | 1.498 / 1.528 | **0.89 / 0.91** | 0.84 / 0.85 | 1.687 |
| 10.7 | 1.778 / 1.814 | **0.79 / 0.81** | 0.75 / 0.76 | 2.250 |
| 10.9 | 2.038 / 2.080 | **0.72 / 0.74** | 0.68 / 0.69 | 2.833 |

  The balance scales as M_b^0.3 against R_K ~ M_b^0.5. In the heavy-shell limit R ~ F^(1/5) (A3c), so reaching R_K at log M 10.9
  statically would take about 5x the law's wall force (scaling, not run).
- **B.** A sticky merge conserves momentum and loses (1/2) M m (V - v)^2 / (M + m) >= 0; reflection off a moving wall keeps the
  speed in the wall's frame.

## 2. Part B, dynamics (graded: sticky snowplow, X = 1)

R_h,n, the record's NC radius at nucleation where the share sits (kpc, log M 9.4 / 10.45 / 10.7 / 10.9): z_n 6: 46 / 103 / 125 /
146; z_n 3: 80 / 180 / 218 / 254; z_n 1.5: 125 / 281 / 340 / 396.

### G-F2: cold component inside 200 kpc at z 0 (line 0.9 M_b, all four masses)

| z_n | canonical (9.4 / 10.45 / 10.7 / 10.9) | alt | gate | what the wall did |
|---|---|---|---|---|
| 6 | 7.86 / 7.46 / 7.44 / 7.43 | same | **FAIL / FAIL** | stalls at nucleation (6-18 kpc) or collapses (10.9 canonical) |
| 3 | 7.81 / 7.41 / 6.53 / 5.28 | same | **FAIL / FAIL** | stalls inside the share at 63-98 kpc, holding 1.6-5.9 M_b |
| 1.5 | 0.00 / 0.00 / 0.00 / 0.00 | same | PASS / PASS | stalls at 236-309 kpc holding 4.5-6.4 M_b; 9.4 breaks out (z 0.57-0.63) to 207-235 kpc |

At z_n 1.5 the heavy bins' shells sit beyond the fixed-mass R_eq (A.2), so the wall pushes outward; what holds them is the pressure
of the share still outside. The pass is thin: the shells sit 1.03-1.55 x 200 kpc.

### G-K: wall at z 0 beyond R_K = sqrt(G M_b / 1.38e-15) for all four masses

| z_n | R_w (kpc), canonical | R_w / R_K canonical | R_w / R_K alt | KiDS points outside the wall (of 59) | gate |
|---|---|---|---|---|---|
| 6 | 14 / 6 / 9 / 0 | 0.03 / 0.004 / 0.004 / 0 | 0.04 / 0.003 / 0.003 / 0.003 | 58 / 57 | **FAIL / FAIL** |
| 3 | 63 / 81 / 79 / 72 | 0.13 / 0.05 / 0.04 / 0.03 | 0.14 / 0.06 / 0.04 / 0.03 | 44 / 43 | **FAIL / FAIL** |
| 1.5 | 207 / 236 / 260 / 278 | 0.41 / 0.14 / 0.12 / 0.10 | 0.47 / 0.15 / 0.13 / 0.11 | 28 / 26 | **FAIL / FAIL** |

### G-L: population filling through SWT1's compensated statistic (line 0.0354 at z 1)

| z_n | q at z 1 (graded), canonical / alt | filling at z 1 | q at z 0 / 0.5 / 2 (canonical) | gate |
|---|---|---|---|---|
| 6 | 0.0000 / 0.0000 | 0.0000 | 0.0000 / 0.0000 / 0.0000 | PASS / PASS |
| 3 | 0.0002 / 0.0003 | 0.0001 / 0.0002 | 0.0000 / 0.0001 / 0.0003 | PASS / PASS |
| 1.5 | 0.0010 / 0.0012 | 0.0007 / 0.0009 | 0.0009 / 0.0018 / (no wall yet) | PASS / PASS |

G-L passes because the walls stay small. Every filling here is also under GAL1's tighter 0.0197.

## 3. Robustness and brackets (reported; same gates)

### Energy-conserving bracket, X = 1 (elastic front, free collisionless layers, wall force on the innermost cold)

| z_n | cold < 200 kpc, canonical | R_w / R_K canonical (alt) | KiDS outside | G-L z 1 | verdict |
|---|---|---|---|---|---|
| 6 | 7.64 / 7.15 / 7.15 / 7.05 | 0.05 / 0.02 / 0.02 / 0.02 (same) | 55 / 54 | 0.0000 | FAILS G-F2, G-K |
| 3 | 6.19 / 6.51 / 6.23 / 4.53 | 0.12 / 0.06 / 0.05 / 0.04 (0.13 / 0.07 / 0.06 / 0.05) | 40 / 40 | 0.0004 / 0.0005 | FAILS G-F2, G-K |
| 1.5 | **2.88** / 0 / 0 / 0 (alt 2.27 / 0 / 0 / 0) | 0.25 / 0.13 / 0.12 / 0.10 (0.34 / 0.14 / 0.12 / 0.11) | 30 / 27 | 0.0003 / 0.0004 | FAILS G-F2, G-K |

Same verdict; the one gate that differs is G-F2 at z_n 1.5, where ejected layers of the lightest bin fall back inside 200 kpc. The
elastic front moves sqrt(2) slower than the snowplow, so dropping the sticky idealisation does not move the wall outward.

### X = 0 (no bound share) and X = 3

| bracket | G-F2 | R_w / R_K at z 0, canonical (alt), by z_n 6 / 3 / 1.5 for log M 10.45, 10.7, 10.9 | KiDS outside | G-L z 1 (z 0) | verdict |
|---|---|---|---|---|---|
| sticky, X = 0 | PASS (0 inside 200 kpc) | 0.60-0.46 / 0.60-0.47 / 0.55-0.43 (0.63-0.45); 9.4 reaches 0.93-1.11 | 8-10 | PASS 0.009-0.028 (z 0: 0.044-0.067, over the line) | FAILS G-K |
| energy, X = 0 | PASS | 0.51-0.39 / 0.48-0.38 / 0.42-0.33 (0.53-0.34) | 11-14 | PASS 0.003-0.013 | FAILS G-K |
| sticky, X = 3 | FAIL (8.6-19.0 M_b) | walls stall or collapse, <= 0.03 | 58-59 | PASS | FAILS G-F2, G-K |
| energy, X = 3 | FAIL (8.4-19.0 M_b) | <= 0.06 | 52-59 | PASS | FAILS G-F2, G-K |

Even with the share never bound, the sticky wall reaches only 0.43-0.63 of R_K for the three heavier bins, below the static balance
of A.3. For log M 10.45 (z_n 6) the shell at 1.02 Mpc carries 8.4 M_b against 5.2 M_b of mean content inside that radius (the
record's flow ahead of it is slowed by the galaxy, and the mean inside R_h,n was frozen at nucleation), and it is still advancing at
z 0 (84 km/s against 66 km/s of Hubble flow there).

### Sticky brackets on the graded case (X = 1, four masses)

- Nucleation radius 0.3 r_M or 3 r_M: z_n 6 and 3 still stall or collapse inside the share (5.3-7.9 M_b inside 200 kpc); z_n 1.5
  still clears 200 kpc (201-310 kpc).
- Pressureless share (p_B = 0): z_n 6 collapses for every mass; z_n 3 collapses except 9.4; z_n 1.5 goes further (275-583 kpc).
  Without the share's pressure there is no stall: a shell inside R_eq falls, outside it is expelled (A.2).
- None of them reaches R_K.

## 4. Checks

- **Known answers, all PASS.** KA-1 F_w vs 4 pi R^2 swt1.p_wall 4.4e-16, vs quadrature 1.5e-10. KA-2 my ln-a integrator with the
  wall off vs swt1.r_ta, three masses at a = 1 and 0.5: <= 1.0e-6. KA-3 every exact R_eq inside the Lean bracket; k = 1e4 vs (3/2) k
  2.5e-5; the share started at rest at 0.99 R_eq falls (-8.0e-4), at 1.01 R_eq rises (+7.5e-4). KA-4 snowplow vs the analytic
  momentum solution 8.1e-13, momentum exact. KA-5 elastic front speed exact, ejecta 2 V_f to 4e-16, ejecta kinetic energy / work
  1.5e-8 (234 layers). KA-6 compensated on NC at z 1: 0.0180 / 0.0182 (SWT1's); 59 KiDS points.
- **MUTATE, all bite** (snp1_MUTATE.out; X = 1, all z_n, both footings). M-OFF: G-F2 fails for every mass (3.0-7.9 M_b). M-SIGN:
  every wall collapses. M-x100: every wall rises at least 2x, to 1.35-4.56 Mpc.
- **Lean.** SNP1.lean: 28 theorems, `exit 0`, axioms propext, Classical.choice, Quot.sound only; two unused-variable warnings
  (compile.txt). SNP1_MUTATE.lean (the true file plus six false versions): `exit 1`, seven errors, all inside the false versions
  (compile_MUTATE.txt). Five lemmas and one definition (W's derivative, W <= y, the deep bound) are copied from SWT1.lean.
- **Disclosed.** (a) A smoke test of the library on log M 10.45 (X 0 and 1) before the graded run showed a bookkeeping bug: while
  the shell is stalled or advancing in the share, the swept front is the shell itself, but the G-F2 count used the nucleation
  radius and counted swept mass twice. Fixed before the graded run (no model change; the smoke-test numbers had already shown the
  10.45 shell stalling at 6 kpc for z_n 6 and at 236 kpc for z_n 1.5, which the graded run reproduces). (b) The Lean fixes after the
  first compile were type ascriptions and tactic order only; no statement changed. (c) The E-bracket timing (0.1 s a run) kept the
  full GSMF grid; the contingency was not used.
- **Against my pre-freeze estimate.** Label as expected (FAILS on G-K). The static balance matched (0.73 / 1.50 / 1.78 / 2.04 Mpc
  vs 0.73 / 1.5 / ~1.8 / 2.0); the dynamics fall further short than I guessed. At z_n 1.5 I expected the 10.45 shell to break out of
  the share; it stalls at 0.84 R_h,n, just beyond 200 kpc. The proposer's estimate (G-K narrow pass, G-L fail at filling >= 0.1) is
  the reverse of what the runs show: G-K fails, G-L passes at z 1.

## 5. What the lane shows, and what it does not

- It closes README item 3 for this class of model. The law's wall pressure does clear a share that is still diffuse (SWT1 T3), and
  if it switches on late (z 1.5) it keeps the inner 200 kpc clean. It cannot carry what it clears: a fixed-mass shell is unstable,
  and a swept shell's stable balance sits at 0.7-0.9 R_K today for the bins that matter.
- **The two-phase reading needs the law on out to KiDS's range, and the law's own field stress cannot hold the wall there.** The
  wall would need about 5x the law's force statically and more dynamically. So, within this model, the two-phase reading does not
  deliver itself; if the KiDS outer points are the lens's own field, something other than the law's wall must hold the component
  out. Lane KO1, which landed in parallel (shared-checkout a11a8a9523, regrade b78153e61b), reads LAW LEVEL HOLDS / LAW LEVEL
  HOLDS on those points, which makes G-K the binding gate. SNP1 does not depend on KO1.
- It does not test: non-spherical walls, an infalling halo that grows after nucleation (unbound infall onto the share is not
  tracked; including it can only add mass inside 200 kpc), hydrodynamic or collisional carriers, a nucleation that sweeps from
  inside the galaxy's own disc, or KiDS's covariance. It grades no mechanism for the switch.

## Files

FROZEN_CRITERIA.md (9ff5f59a72, shared checkout), snp1.py -> snp1.json / snp1.out, snp1_MUTATE.json / snp1_MUTATE.out (from
`python3 snp1.py --mutate`), SNP1.lean, SNP1_MUTATE.lean, compile.txt, compile_MUTATE.txt. One thread, 78 s (graded) and 5 s
(MUTATE), peak 0.23 GB. A second graded run reproduced snp1.out line for line (timings aside). Lean compiled with `lake env lean` from the copy of fable_independent_2026/lean_2026 that has its Mathlib
build.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
