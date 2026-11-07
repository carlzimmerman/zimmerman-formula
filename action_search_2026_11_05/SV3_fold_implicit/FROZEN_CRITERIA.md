# SV3 frozen criteria: AC14 successor, implicit integrator, "does AC2q fold like v3s?" (planar, subset)

Frozen before any SV3 graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter
particle. No LCDM input. Footings 9.3603e-11 / 1.1312e-10 m/s^2, never pooled.

## Disclosure

Written AFTER AC14's result (criteria ad9d747016, result bde9320c80, NO VERDICT). AC14's numbers are on the
record and were read before writing this file, including its K2/K3 J differences (3e-5 and 1e-4 on the
no-fold rows; 0.12 and 0.28 with a 1e-2 floor on the fold rows). Before freezing, one timing probe was run on
a synthetic row that is not in the grid (M-1 0.5, Pi0 0.03, s^2 1e-4, gamma 3e-5). It printed cost only:
7 s at N 2000, 37 s at N 8000. The Jacobian was checked against finite differences on a random N 200 state
(max difference 7e-7, FD noise). No physical, stress, K or MUTATE row was run before this commit.

## AC14 failure modes this lane addresses

1. The explicit DOP853 integrator stalled (step underflow) on all 216 stiffness-on AC2q rows and on the 80
   v3s phantom twins. The excluded edge cells fold first. As J -> 0 there the pressure gamma Pi/J and its
   stiffness (~ J^-3) diverge, and E1's tanh taper leaves a nonzero gamma in those cells.
2. MUTATE-B (Mach 0.3 power gate) stalled in the same way. It read UNDECIDED, so the gate did not bite.
3. The K2/K3 J tolerance (<= 1e-3 relative, floored at 1e-2) is badly posed where J -> 0.
4. Not changed by AC14: the interior first fold is always the front-most interior cell (fold_cell_frac
   0.949875 on every AC14 fold). So the edge treatment acts directly on the graded cell. That is why this
   lane adds an edge-sensitivity check (K4).

## Physics (AC10, unchanged in the interior)

AC10 S1's label system is imported from `../AC10_nonlinear_clock/ac10.py`, and none of AC10's or AC14's files
are edited. It is unchanged in the interior: charge, multistream-safe planar Gauss, sheet, A2-POST charge
taper, stiffness force -gamma d_x max(Pi, 0) with Pi = Pi_c/J, initial data, stream extent, J_thr 1e-3,
J_reg 0.05, t_max 6 and the 5 % edge exclusion.

## Declared changes (method only)

**I1, integrator.** scipy Radau IIA (order 5, implicit, L-stable), with rtol 1e-10 and atol 1e-12 (AC14's).
It uses an analytic sparse Jacobian made of three parts:
- the sheet, -rho_b(x) on the diagonal;
- self-gravity, -(M-1) s^2 on the diagonal plus the x_min and x_max columns;
- the banded pressure operator.

The sort-order jumps of the planar Gauss sum are left out of the Jacobian (they are delta functions). The
Jacobian only drives Newton, and accuracy is set by Radau's error control. The fold event is AC10's
interior-minimum-J event (terminal). A second, non-terminal event records the first time interior J drops
below J_reg.

**E3, edge treatment (replaces E1).** The excluded 5 % edge cells at each end carry no stiffness: they are
pressureless dust, with AC10's gravity and the A2-POST charge taper unchanged. At each interior/edge interface
the ghost pressure equals the adjacent interior cell's pressure (a transmissive, zero-gradient boundary), so the
interface node feels no pressure force. Physical justification:
- The edge cells fold first.
- What they do after folding (shock, multistream) is AC14's declared out-of-scope post-fold physics. The
  inviscid P ~ 1/J law cannot represent it, and that is what stalled AC14.
- A transmissive ghost is the standard non-reflecting truncation. It adds no grid-scale force. A vacuum ghost
  (P = 0) would add an interface force ~ gamma Pi/dq, which grows with N and therefore cannot converge.

E3 removes the stiffness singularity from cells that are never graded. Interior cells keep AC10's pressure law
exactly, up to the first interior fold, where the run stops.

**K4, edge sensitivity (declared because the graded cell borders the edge).** For every row with interior
stiffness on (gamma > 0 and Pi0 > 0), the deciding rung is rerun with E3b, a linear-extrapolation ghost
(P_ghost = max(2 P_1 - P_2, 0), applied on both sides). The row keeps its label only if:
- E3b gives the same label; and
- for FOLD rows, |t_E3b/t_E3a - 1| <= 1e-3 (the ladder tolerance).

Otherwise the row is UNDECIDED (edge-sensitive). For rows with interior stiffness off, E3a and E3b are
identical by construction, and K4 is not run.

## Subset (rule fixed here, before any row is run)

The population is the 160 AC2q rows in `ac10.physical_rows()` with interior stiffness on (gamma > 0 and
Pi0 > 0): 80 phantom and 80 clock-only, 80 per footing.

AC14's 56 UNDECIDED soft AC2q rows had Pi0 < 0. Their pressure lived only in the tapered edge cells, so under
E3 they are pure dust and are out of this population. AC14 already graded 24 soft pairs equal to 4.7e-6.

The subset is every 5th row of that population, in generation order, starting at index 0. That gives 32 AC2q
rows. Because 5 is coprime to the kind period 2, the subset covers both kinds, both footings, all five radii,
both w, both M - 1 ends and both Lstar. Their 32 v3s twins (same foot, r, w, M-1, Lstar, kind) are run too.
Phantom twins have stiffness on; clock-only twins have Pi0 = 0, so stiffness is off. The labels apply to this
subset only.

## Convergence (AC14's ladder)

- The ladder is N = 2000/4000/8000.
- The label must be the same on all three rungs. For FOLD, the fold time may change by at most 1e-3
  (relative) between the last two rungs.
- If that fails, a row gets one extra rung at N = 16000 and is judged on 8000 vs 16000.
- A row that still fails is NOT CONVERGED.
- A run that ends with a solver stop, or that hits the wall-time cap, makes its row UNDECIDED.

A row is REGULAR only if all of the following hold to t_max = 6:
- interior J never reaches J_thr;
- interior J never drops below J_reg;
- the solver status is 0.

**Wall-time cap (declared up front).** 1500 s per single run. A run that hits the cap is recorded as TIMEOUT,
and its row is UNDECIDED. Compute settings: nice 15, at most 3 worker processes, 1 thread each. Every rung is
checkpointed in parts/. SIGTERM stops a run without writing it, and a rerun resumes from the checkpoints.

## Checks (all must hold, or NO VERDICT)

**K0 (new integrator vs the AC10 record).** At gamma = 0, SV3 (Radau, E3) must give the same fold time as
`ac10.run` (DOP853) to within 1e-6 relative. This is tested on the K1 zero-charge row and on the first soft
v3s physical row. It replaces AC14's 1e-12, which assumed the same integrator. The line is set at 100x the
rtol-limited event accuracy.

**K1 (as AC14).** The zero-charge coupled code must match an independent two-label integration to 1e-6. The
thin-sheet delay must equal v_cross/(K Sigma_b) within 2 %.

**K2/K3 (re-posed tolerance).** AC14's own-crossing-speed method and stress rows are kept:
- A1 at Pi0 0.2 and 1.0;
- A2 at Pi0 = s^2 = 0.4 and 2.0.

All have gamma 0 and M - 1 = 1, and they use the same predictions (A1 threshold 1/sqrt 2, A2 threshold 1).
PASS needs three things:
- (i) The first-passage fold/no-fold outcome matches the prediction and the per-label equation on all four
  rows.
- (ii) Fold rows: the first time J reaches J_thr agrees between the numeric run and the per-label equation to
  <= 5e-3 relative. This line comes from the error budget of the graded comparison. The label line is
  |t_AC2q/t_v3s - 1| <= 1e-2, and two independent code errors of at most 5e-3 each cannot by themselves move a
  pair across it.
- (iii) J agrees to <= 1e-3 relative, evaluated only where the per-label J >= J_reg, over first passage, on all
  four rows. J is bounded away from 0 there, so the relative measure is well posed.

**MUTATE-A (as AC14, separate outputs).** A repulsive sheet on the zero-charge stream must read REGULAR.

**MUTATE-B (power gate, replaces AC14's, separate outputs).** This is an acoustic standing wave in the same
code, with the same pressure operator, E3 edges and I1:
- no sheet, M - 1 = 0, s^2 = 0, Pi0 = 0.1;
- initial v = 1 + A sin(k(q - q_0)), with k = 4 pi / span (two wavelengths) and A k = 1/5.5;
- gamma set so that the label sound speed sqrt(gamma Pi0) = A/0.3 (Mach 0.3).

It is verified in the per-label (per-mode) equation first, analytically, before any run:
- Dust twin (gamma = 0). J = 1 + A k cos(k(q - q_0)) t exactly (ballistic), so it reaches J_thr at
  t_d = (1 - 1e-3)/(A k) = 5.4945 < t_max.
- With pressure. The linear mode equation delta'' = -c0^2 k^2 delta gives J = 1 - 0.3 cos(.) sin(c0 k t), so
  J >= 0.7 >= J_reg. Simple-wave steepening for P ~ 1/J (c_L^2 = gamma Pi0 / J^3) gives a breaking time of
  about 4/(3 A k) = 7.3 > t_max, so the wave stays shock-free through t_max.

The gate bites only if both of the following hold:
- the pressure row reads REGULAR, converged on the ladder;
- the dust twin reads FOLD, converged, with |t/t_d - 1| <= 1e-3.

If the pressure row folds or is UNDECIDED, the method cannot see pressure regularization, and no verdict
stands.

**MUTATE-C (K4 has power).** The A1 stress row (Pi0 0.2, M - 1 = 1, sheet on), with gamma = 1e-2, is run at
N 2000 with E3a and with a vacuum ghost (P = 0 outside the interior). The vacuum ghost adds an interface force
~ gamma Pi0/dq ~ 1.3, comparable to the sheet. The two runs must differ: either a different label, or fold
times differing by > 1e-3. If they do not, K4 cannot see an edge effect, and no verdict stands.

**X > 0 (as AC14).** min X/X_bg = 1 - (v_max w/c)^2 must be > 0.99.

## Labels (subset-scoped; AC14's labels)

- **FAIL-SAME-AS-V3S (caustics inherited, in subset).** All of the following hold:
  - all checks hold;
  - all 32 AC2q subset rows are FOLD and converged;
  - all 32 twins are FOLD and converged;
  - |t_AC2q/t_v3s - 1| <= 1e-2 on every pair.
- **PASS (AC2q regularizes).** All checks hold, and some converged AC2q row is REGULAR while its converged v3s
  twin is FOLD.
- **SAME-AS-V3S, NOT ALL FOLD.** All checks hold, every pair converged, and each AC2q label equals its twin's,
  but some pairs are REGULAR in both.
- **WORSE.** A converged AC2q row is FOLD while its converged twin is REGULAR.
- **NO VERDICT.** A check fails, a MUTATE does not bite, or any subset row is NOT CONVERGED or UNDECIDED.
  This includes TIMEOUT and K4 edge-sensitive rows.

## Out of scope

Out of scope, as AC14:
- the post-fold interior (stiffness shocks);
- 3D and spherical cases;
- the nonlinear hold law;
- the moving Sun;
- the 128 AC2q stiffness-on rows that are not in the subset (no label is claimed for them).

AC14's Mach 0.3 sheet row is not rerun. A label here is about the planar interior first caustic, under E3,
in the declared subset.
