# AN2_aest_3d_fold: FROZEN CRITERIA, stages S0 and S1

Committed alone, before any script or computed number of this lane. Revises section 4 of `SCOPE_DRAFT.md`. **Not blind:** AN1's result is known, and so is my expectation of an earlier fold. Authority: `OWNER_DECISION_2026-11-02_ONE_ACTION_LANE.md`; the owner's go covers S0 and S1 only. **S2 and S3 do not run, whatever S1 says.** kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, never pooled. A gravitating field, never a particle. The cold sector stays retired by the decision of 2026-11-01: nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. No download.

## 1. Question
AN1's caveat: a radial flow focuses on its centre by symmetry. Does the single-valued field reach the well, M_d >= M_ph inside R_test, before its first fold, once the peak isn't spherical?

## 2. System
AN1's reduced system (Q0 -> infinity, quadratic K, **K_B = 0 only**), in L1's comoving PM form. x comoving, p = a^2 dx/dt, Xi = -h, all densities mean-subtracted:
    lap_x Psi = 4 pi G (rho_m0 / a) delta_m
    div_x[(1 - mu(y)) grad_x Xi] - a^2 mu_K^2 Xi = 4 pi G (rho_x0 / a) delta_d,   y = |grad_x Xi| / (a a0),  mu(y) = y/(1+y)
    field: dp/dt = -grad_x(Psi - Xi);   baryons: dp/dt = -grad_x Psi
Hold solver and mesh: copied from `L1_khronon_pm/khronon_pm.py` (Mesh, CIC, Anderson fixed point), tolerance 1e-6, cap 400 iterations; particle arrays float64, so compression can be read. L1 is read, not edited. Solver failure rule: section 6.

## 3. Setup, frozen
- **Background:** AN1's class exactly: flat, h 0.672, rho_x0 33.2, rho_b0 33.2/5.35 Msun/kpc^3 comoving, constant Lambda, no radiation, same on both footings. Start z_i = 20, first-order Zel'dovich, f = 1 at start, as AN1.
- **Masses and tests:** M_tot 1e12 and 1e15 Msun; R_test = R_last = 36 kpc and R500 = 1350 kpc, physical. q_t = q(M_tot) = (3 M_tot / 4 pi rho_m0)^(1/3).
- **Peak:** one deterministic ellipsoidal Gaussian, delta_L(q) = d0 exp(-(1/2) sum q_i^2 / R_i^2) minus its box mean, centred on a mesh node, no other structure. d0 and R_G are AN1's A1 values for that mass (`edge_amp`, `gbar`). R_1 R_2 R_3 = R_G^3. Displacement from an FFT of the analytic field. Short axis along x_0, long along x_2. e = 0 is AN1's profile. Keeping d0 fixed means a row compares peak to peak at the same central height.
- **Shape from a stated formula, not tuned.** Height nu = d0 [D(0)/D(z_i)] / sigma_G(R_G), with sigma_0, sigma_1, sigma_2 from the Gaussian filter at R_G and the record's dust-limit spectrum `L1_khronon_pm/work/class_modelB_pk.npz`; gamma = sigma_1^2/(sigma_0 sigma_2). This spectrum sets shape only and enters no grade. Limit, disclosed: its amplitude isn't derived in this lane, and a suppressed field spectrum would mean greater height and smaller e, nearer to e = 0.
  xbar = mean of x under P(x|nu) proportional to f(x) exp(-(x - gamma nu)^2 / (2(1 - gamma^2))).
  P(e,p|x) from BBKS 1986 Eq. 7.6, from memory, PROVISIONAL: proportional to exp(-(5/2) x^2 (3e^2 + p^2)) W(e,p), W = e (e^2 - p^2)(1 - 2p)[(1+p)^2 - 9e^2], on the domain where curvature eigenvalues are ordered and positive, with BBKS's f(x) as normaliser. **Check KN below guards the memory.**
  - **Shape A:** the mode of P(e,p|xbar).
  - **Shape B:** e at the 90th percentile of the marginal P(e|xbar); p the mode of P(p|e) at that e.
  - Curvature eigenvalues l_1,2,3 = (x/3)(1+3e+p), (x/3)(1-2p), (x/3)(1-3e+p); R_i^2 proportional to 1/l_i.
- **Baryons:** AN1's rule (amendment A1 and its code), extended by rank. Rank by Lagrangian ellipsoidal radius (sum q_i^2 R_G^2/R_i^2)^(1/2), which at e = 0 is AN1's order. Target r_f from cumulative baryon charge: 1e12: first 6.72e10 Msun on the spherical exponential R_d 3.565 kpc; 1e15: beta model beta 2/3, r_c 0.15 R500, up to 1.19e14 within R500. Rest r_f = infinity. A baryon stops when falling (radial physical velocity from the centre <= 0) with r <= r_f, set to r_f along its own direction if finite, or at its own r if infinite. A stopped baryon stays fixed in physical space. R500 stays 1.35 Mpc as AN1.
- **Grid:** N^3 field particles plus N^3 baryon particles on the same lattice, mesh N^3, L = 8 q_t, **N = 128**, CIC. Cell: 114 kpc (1e12), 1.14 Mpc (1e15) comoving.

## 4. Resolution, stated up front
**The fold is measured on a grid, and I expect it to depend on the grid.** Forces are softened below a cell, which delays any fold reaching sub-cell scale: the bias runs toward "later", the direction that would look like a win. Discs aren't resolved. R_last is about one cell at z 2 and R500 under two cells at z 1.5 for those masses. M_d inside R_test is a particle count, read with its count, and is not resolved structure. pi/mu is 31 Mpc at mu 0.1, larger than the 1e12 box, and 55 kpc at mu 56.6, about a cell at 1e12 and far below one at 1e15. AN1's N 1500 has a comoving spacing about 47 times finer than this grid.

## 5. Fold
**Definition.** Each Lagrangian lattice cube is split into its 6 Kuhn tetrahedra, using unwrapped positions. J_tet is the map's piecewise-linear Jacobian. **A fold is det J_tet <= 0, with det J_tet > 0 at the previous step**: orientation reversed, a real crossing. There's no compression threshold, so a compressed held shell, det small and positive, doesn't fire however small. Fold time: linear interpolation of the minimum det to zero between the two steps. **Persistence:** the same tet, or more than one tet, must be inverted at the next step. An inversion that reverses inside one step is logged as TRANSIENT and doesn't count, and the count is reported.
**Two times, each row:** t_any, first fold anywhere; t_q, first fold with Lagrangian |q| <= q_t. A row stops one step after t_q. If t_any < t_q, the steps between lie past the first fold; t_q is then reported as conditional, because the slow branch's hold equation is instantaneous, and is flagged. **Nothing past t_q is computed or reported.**
**Fold shape.** Eigenvalues j_1 <= j_2 <= j_3 of the symmetrised J by centred differences (span 2 lattice spacings) at the fold site, at the last step before inversion: sheet if j_2 > 0.25; filament if j_2 <= 0.25 < j_3; point if j_3 <= 0.25. All eigenvalues reported.
**Row reads at the last step before t_q:** M_d, M_b, particle counts inside R_test about the peak centre, M_ph as in AN1 from g_law with mu = x/(1+x), r_fold, max y. Also, at each step, whether M_d >= M_ph inside R_test.

## 6. Numerics
Time-step: KDK in cosmic time with exact background; dt = min of eta dx/|xdot|_max, eta (dx a^2/|F|_max)^(1/2), 10 eta/omega_max, and dln a <= 0.2 eta. omega^2 as AN1's limiter, cell by cell: 4 pi G rho_d max(k^2/(k^2 c_L + mu^2), |k^2/(k^2 c_L + mu^2) - 1|), k = pi/dx physical, c_L = (1+y)^-2.
**eta by a pre-stated convergence test (check KT).** AN1's first eta failed its checks, so this comes first. Candidates 0.05, 0.025, 0.0125. Rows T1 = (1e12, mu 0.1, shape B, canonical), T2 = (1e15, mu 56.6, shape B, canonical), N = 64. Adopt the largest eta whose t_q moves by <= 1 % at eta/2 on both. If none passes: NO VERDICT, numbers only.
**Solver failure:** a step with hold residual > 1e-5 ends the row UNRESOLVED at that time. Steps with residual between 1e-6 and 1e-5 are counted and reported.
**Row end:** FOLD; NO FOLD by z = 0; or UNRESOLVED (solver, or 20000 steps).

## 7. Rows
**The 16 S1 rows:** {1e12, 1e15} x {mu 0.1, 56.6 /Mpc} x {shape A, shape B} x {canonical, alt}, N = 128, adopted eta, K_B = 0.

**AN1 reference, t_ref** (strict line, `AN1_aest_nonlinear_dust/an1_cf1e-4.jsonl`), t in Gyr:
| Row | canonical z, t | alt z, t |
|---|---|---|
| 1e12, mu 56.6 | 1.399, 4.541 | 1.399, 4.541 |
| 1e15, mu 56.6 | 1.630, 3.978 | 1.630, 3.978 |
| 1e15, mu 0.1 | 0.269, 10.597 | 0.269, 10.593 |
| 1e12, mu 0.1 | **no reference**: no fold by 10.206 Gyr, budget | **no reference**: no fold by 10.239 Gyr, budget |

**Comparison, each row with a reference.** NO LATER if t_q <= 1.05 t_ref. LATER if t_q > 1.05 t_ref, or no fold. All comparison times are in t, not z.
**Rows with no reference (the 4 at 1e12, mu 0.1): these can't count as "no later".** AN1 gives only a bound. Each is reported in one of two classes, neither of which enters the NO LATER count:
- **BEFORE AN1's LAST DEFINED TIME:** t_q < AN1's t at budget. AN1's spherical row hadn't folded by then. That's stated, and is not called "no later than spherical", because the spherical fold time doesn't exist in the record.
- **NO COMPARISON:** t_q at or after that time, or no fold, or UNRESOLVED.
They're also read against the 3D e = 0 row at the same mass and mu (section 8, KE), as a report only.

## 8. Checks. A failed check means NO VERDICT: numbers only, no label
| Id | Known answer | Size | Line |
|---|---|---|---|
| KN | BBKS memory: numerical integral of the normalised P(e,p|x) over the domain at x = 1, 2, 3, 5, against 1 with the f(x) I recall | | <= 1e-3 |
| KZ | Plane wave, pure dust, single sine mode, Zel'dovich crossing exact from the growth ODE on this background; crossing near z = 1. KZ2: same at mu 1.24e8 with the hold on | 64^3 | t <= 5e-3 |
| KE1 | S0 ellipsoid ODE, quad form and DOP853, against a separately written integration, Carlson R_D and LSODA | | t <= 1e-6 |
| KE2 | Engine against S0: smooth-edged homogeneous ellipsoid (edge width 10 % of radius), pure dust, shape B axes at 1e12's height, long semi-axis L/8: first-axis fold t against the ODE | 96^3 | t <= 3 % |
| KE | **e = 0 against AN1:** canonical at 128^3 for 1e12 mu 56.6, 1e15 mu 56.6, 1e15 mu 0.1: t_q against t_ref; shape reads "point". 1e12 mu 0.1 e = 0 also runs, reported only, no reference | 128^3 | t <= 5 % |
| KD | det J analytic: smooth displacement with known Jacobian, max error at sampled tets; synthetic homologous compression to det 1e-9 doesn't fire; a synthetic fold fires within one lattice spacing and on the right step; fold shape reads sheet, filament, point on synthetic cases | 64^3 | 2e-3; exact |
| KC | L1's KC with my copied solver: static Plummer point mass, 128^3, L 0.32 Mpc/h, M 1e11 Msun/h, both footings: AQUAL vs law; PN baryon; field net force | 128^3 | 0.01 |
| KR | SIGTERM mid-run then resume: same fold time | 32^3 | 1e-10 rel. |
| KT | Section 6 | 64^3 | 1 % |
| KB | Box: same cell, doubled box: (N 64, L) against (N 128, 2L), row (1e12, mu 0.1, shape B, canonical), where long range and elongation are worst | | t <= 3 % |
| KM | MUTATE twin, separate outputs: force sign flipped on Xi, and the tracker takes |det| | | must fail KC and KD |

**Resolution test KG, a separate kind of check.** Rows G1 = (1e12, mu 0.1, shape A, canonical) and G2 = (1e15, mu 56.6, shape A, canonical) at 64^3 and 96^3, with the 128^3 row. Line: |t_q(128) - t_q(96)|/t <= 5 %. 64 to 96 is reported. A miss doesn't void the numbers: it caps the label at NOT RESOLVED for that mass and mu, because that is what the scope's label means. KG's 64 and 96 run before other rows are read. If a row has no fold at some N, that counts as a miss.

Order: KN, KD, KC, KZ, KE1, KE2, KR, KM, KT, KB, KE, KG, then the rows. Only KT, KB, KE, KG may read fold times at the science rows before the rows themselves; that's disclosed. A check failure stops the reading of rows until reported; rows may still be computed for numbers.

## 9. Labels (S1, lane)
Applied only if every check in section 8 passes.
- **FOLDS NO LATER THAN SPHERICAL:** all 12 reference rows NO LATER; KG passes. The statement names the 4 no-reference rows and their class, and doesn't include them.
- **DELAYED, STILL ENDS:** a reference row is LATER **and** later than the canonical 3D e = 0 row at its mass and mu by > 5 %, KG passes, and no row has M_d >= M_ph inside R_test at any step before t_q. A row LATER than AN1 but within 5 % of its own grid's e = 0 reads as grid bias, and the label is NOT RESOLVED.
- **WELL CANDIDATE AT [rows], NOT CONFIRMED:** M_d >= M_ph inside R_test at a step before t_q, with at least 8 field particles inside. S1 can't confirm one resolution up, so the scope's REACHES THE WELL isn't available here; no capture read against X22 or LM1 counts.
- **NO FOLD CANDIDATE AT [rows], NOT CONFIRMED:** no fold by z = 0. Same limit.
- **NOT RESOLVED:** KG misses, or more than 10 % of rows (2 or more of 16) are UNRESOLVED.
- **NO VERDICT:** any check in section 8 other than KG fails.
Precedence: NO VERDICT, then NOT RESOLVED, WELL or NO FOLD candidates, DELAYED, FOLDS NO LATER. Any result beyond FOLDS NO LATER is also rerun at 64^3 and 96^3 at canonical before being stated, to show its trend with N. **Low mu reads NOT RESOLVED for the stop rule** if KG's G1 misses, or a mu 0.1 row is UNRESOLVED or NO COMPARISON.
Every label is about this reduced system: one deterministic peak, K_B = 0, no angular momentum beyond what the tide gives, no discs resolved. None says the action class works or fails in general.

## 10. Stop rule
Frozen from the scope: S2 would be indicated if S1 reads anything but FOLDS NO LATER THAN SPHERICAL, or leaves low mu NOT RESOLVED. **By the owner's instruction S2 does not run in this session either way:** the report says what the rule points to and stops. S3 isn't indicated by S1. No completion in any stage.

## 11. S0
Homogeneous ellipsoid, dust limit: a_i''/a_i = OL H0^2 - 4 pi G rho_bar(a) [(1+delta)/3 + (b_i/2 - 1/3) delta]·(the ODE form written out in the script), b_i from the axis ratios, sum b_i = 2, no external tide. Central strain l_i = d0 b_i/2 at z_i, from AN1's d0 for each mass, for e = 0, shape A, shape B. Reports z of first-axis collapse against the spherical value. This is the dust limit, and it's the only stage that speaks to mu 2.04e4 and 1.24e8, as a read; it grades nothing.

## 12. Hand expectation (before any number)
- At mu 56.6 and at z above that where pi/mu is small: dust-like. First-axis sheet folds earlier than the spherical point: shape A by about 0.1-0.5 in z, B more. 1e15 has smaller e by its height, so a smaller shift.
- At mu 0.1, 1e15: AN1 strict z 0.27, a sub-cell focus at this grid, so **KE at this row is the check I think likeliest to miss**. Shapes should fold earlier off-centre, unless the hold term, which is long range, stiffens the sheet.
- 1e12, mu 0.1: I expect a fold before z = 0, not confidently before AN1's bound at about z 0.3.
- M_d stays under M_ph at R_test throughout. Likely label FOLDS NO LATER with the 4 rows stated apart.

## 13. Compute
nice 15, one thread per job, at most 2 jobs concurrently; footprint target under 1 GB, RSS reported; preemptible, checkpoint on SIGTERM, resume bit-identical; no snapshots; outputs under 100 MB. Stop and report if free disk falls under 15 GB. **If any row's CPU time exceeds 67.5 min (3 x the scope's upper figure of 6 thread-hours over 16 rows), checkpoint, stop and report; the grid isn't shrunk after seeing numbers.** CPU time, not wall, because the machine is loaded by other lanes.

## 14. Not in S0, S1
S2, S3. Fold time against AN1's floors in 3D. K_B 0.078. Finite Q0. Any completion or any continuation past the fold. Random fields or substructure. Baryon pressure, feedback.
