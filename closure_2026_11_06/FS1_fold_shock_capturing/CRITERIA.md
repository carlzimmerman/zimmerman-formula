# FS1 frozen criteria: a shock-capturing label for AC14's open door ("does AC2q fold like v3s?", planar)

Frozen before any FS1 script is committed or any graded FS1 number exists. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. No LCDM input. Footings 9.3603e-11 / 1.1312e-10 m/s^2, graded
separately, never pooled.

## Disclosure (what was seen before freezing)

Written after AC14 (criteria ad9d747016, result bde9320c80: NO VERDICT; 216 AC2q + 80 v3s phantom rows UNDECIDED
because the explicit inviscid DOP853 code stalls at the first edge fold). AC10's and AC14's numbers were read.
SV3_fold_implicit (2febd29269, criteria only, implicit Radau, subset of 32) exists; FS1 is independent of it,
touches none of its files, and uses a different method (explicit shock capturing, full grid).

Before freezing, a numpy prototype of the scheme below (scratch, not committed) was run at N = 2000 only, on
seven rows, to choose the method and estimate cost. What it printed:
- soft v3s row 1 (dust interior): t_fold 1.2588781565 (AC14 N 2000: 1.2588784082);
- soft AC2q row 1: 1.2588783640 (AC14: 1.2588785770);
- clock-only v3s row 1 (dust): 1.2828263548 (AC14: 1.2828263550);
- clock-only AC2q row 1: FOLD at 1.2159836 (AC14: UNDECIDED, stall). This is earlier than its v3s twin by
  5 %. Probable reading (not yet checked): the stream's leading cells, which carry the uniform clock pressure,
  shock instead of crossing, and the first interior cell reaches J_thr when that shock arrives;
- phantom AC2q, weakest stiffness (c0 = sqrt(gamma Pi0) 2.2e-4): FOLD at 1.21787;
- phantom AC2q, median stiffness: FOLD at 2.18877;
- phantom AC2q, strongest stiffness (c0 1.2e-2): no interior J <= J_thr seen to t = 4.7 (J_min 3.9e-3,
  shock-held); the run hit a 900 s probe cap before t_max.
Cost: 4-60 s per N 2000 run. None of these is a graded number. All graded numbers come from the committed
script and its JSON.

## Physics (AC10's planar label system, unchanged)

The system is imported from `action_search_2026_11_05/AC10_nonlinear_clock/ac10.py`, and no AC10/AC14/SV3 file
is edited. Imported unchanged: physical_rows() (240 AC2q + 240 v3s twins), constants, initial data, the sheet
(erf, width WB 1e-3, K Sigma_b = 1), the multistream-safe planar Gauss sum with node charges, the A2-POST tanh
charge taper inside the 5 % edge cells, J_thr 1e-3, J_reg 0.05, t_max 6, and the 5 % edge exclusion of the reading.
The stiffness force is AC10's continuum -gamma d_x max(Pi, 0), Pi = Pic/J, and only single-stream cells (J > 0)
carry pressure.

## Declared method (FS1 scheme S)

1. **Conservative pressure.** For a cell of uniform charge Pic, -gamma d_x(Pic/J) = -d_q p with
   p(J) = gamma Pic / (2 J^2): a barotropic p-system in label (mass) coordinates, Lagrangian sound speed
   C = sqrt(gamma Pic / J^3). The interior has uniform Pic, so this is AC10's equation exactly there. It is
   written in flux form so that shocks have the Rankine-Hugoniot speeds (AC10's nodal -gamma dPi/dx form is
   the same smooth equation, but it is not conservative). Cell pressure p_i = K_i/(2 J_i^2), K_i = gamma
   max(Pic_i, 0), for J_i > 0, and 0 otherwise. Node force -(P_i - P_{i-1})/m, with m = dq at interior nodes
   and dq/2 at the two end nodes. The ghost outside each end is P = gamma max(s^2, 0)/2, which is the background
   clock at J = 1 (AC10's ghost was Pi = s^2).
2. **Shock capturing.** A limited artificial viscosity on compressing pressure cells (K_i > 0, J_i > 0,
   dv_i = v_{i+1} - v_i < 0): Q_i = (1 - psi_i) [c_Q dv_i^2 / J_i + c_L C_i |dv_i|], with c_Q = 1 and c_L = 0.5.
   psi_i is the Christensen MC limiter, max(0, min(1, (r_L + r_R)/2, 2 r_L, 2 r_R)), with r_L = dv_{i-1}/dv_i
   and r_R = dv_{i+1}/dv_i. It is 1 on a linear velocity field, so Q vanishes in smooth flow, and it switches
   on at shocks. P_i = p_i + Q_i. Q = 0 in cells with K_i = 0, so **pressureless rows are AC10's semidiscrete
   label system exactly**: dust labels cross and multistream as in AC10.
3. **Time integration.** SSP-RK3 (Shu-Osher) with
   dt = min(0.05 WB / max|v|, 0.4 dq / max_i sigma_i), where
   sigma_i = C_i + 2 c_Q (1 - psi_i) |min(dv_i, 0)| / J_i.
   The run continues through edge folds and edge shocks. Folded edge dust cells carry no pressure, as in AC10,
   and pressure cells cannot fold under the CFL step. The interior event is located inside each step by cubic
   Hermite interpolation of every interior cell's J(t), using J and dJ/dt = dv/dq at both ends of the step.
   A non-terminal all-cell event, the first J <= J_thr over all cells, is recorded too (AC10's A2-POST
   reading, for KA2).
4. **Core.** The integrator is a C core compiled by the committed Python driver. K0 below checks it against a
   committed numpy reference implementation of the same scheme.

Graded reading (AC10/AC14's frozen one): the first time min interior J <= J_thr. The run stops there (FOLD),
or at t_max.

## Run classes

- **FOLD**: interior J reaches J_thr at t_fold <= t_max.
- **HELD**: interior J > J_thr at every step to t_max, with J_min recorded. It is reported as REGULAR if
  J_min >= J_reg (AC10's line), and as SHOCK-HELD if J_thr < J_min < J_reg (pressure-held compression, which
  AC10/AC14 had no class for).
- **UNDECIDED**: a non-finite state, more than 2e8 steps, or more than 4 h wall time on one run.

## Convergence ladder

N = 2000/4000/8000. A row is converged if its class is the same on all three rungs and:
- FOLD: |t_8000/t_4000 - 1| <= 2.5e-3;
- HELD: |Jmin_8000/Jmin_4000 - 1| <= 0.1.

The FOLD line is a quarter of the pair line below, so two rows' ladder errors together cannot carry a pair
across it. A row that fails gets N = 16000 and is judged on 8000 vs 16000 with the same lines; the class at
16000 must equal the class at 8000. A row that still fails is NOT CONVERGED. The deciding rung is the last rung
used. Its last-rung change e (relative fold-time change, or J_min change for HELD) is carried into the pair
decision.

## Pair outcomes (AC2q row vs its v3s twin; both converged)

With r = t_AC2q/t_v3s and E = e_AC2q + e_v3s:
- SAME-FOLD: both FOLD, |r - 1| + E <= 1e-2.
- SAME-HELD: both HELD.
- DIFF-TIME: both FOLD, |r - 1| - E > 1e-2. Reported with its sign: EARLIER (r < 1) or LATER.
- DIFF-LABEL: one FOLD, one HELD. REGULARIZES if AC2q is HELD and v3s is FOLD; WORSE if the reverse.
- UNRESOLVED: both FOLD, and neither SAME-FOLD nor DIFF-TIME.
- Any non-converged member makes the pair OPEN.

## Checks (all gating; any failure gives NO VERDICT)

- **K0 (core = reference).** The C core equals the committed numpy reference on three rows at N = 500: soft
  v3s row 1, clock-only AC2q row 1, and the strongest phantom AC2q row, the last run to t = 1.5 if it does
  not fold. Fold time (or J_min at the stop) must agree to <= 1e-9 relative.
- **K1 (AC14's).** On the zero-charge row at N 2000, the coupled code must match an independent two-label
  integration to 1e-6, and the thin-sheet delay must equal v_cross/(K Sigma_b) within 2 %.
- **KA1 (reproduce AC14's soft pairs).** Take the 24 soft pairs that AC14 read FOLD/FOLD. In FS1, both members
  must be FOLD and converged, and max |r - 1| <= 5e-6. Each FS1 fold time must also equal AC14's at the same N
  (AC14's deciding rung) to <= 1e-5 relative.
- **KA2 (reproduce AC10's first-fold numbers).** Take AC10's A2-POST first fold over all cells (t_fold_all) at
  its last rung, on every row of AC10's 12-pair subset where AC10's A2-POST ladder converged. FS1's all-cell
  first J <= J_thr time at the same N must agree to <= 2.5e-3 relative. AC10's K1 coupled time must also
  agree: 1.2828263550 to 1e-6.
- **K2/K3 (AC14's stress rows, re-posed with a well-posed J tolerance).** The rows are AC14's: A1 v3s
  Pi0 0.2 / 1.0; A2 AC2q Pi0 = s^2 0.4 / 2.0; all with gamma 0 and M - 1 = 1, at N 2000. Use AC14's own-v_cross
  method on the front-most interior cell, with the per-label equation J'' = -rho_b(x(t)) J + (M-1)(Pi0 - s^2 J)
  along its own trajectory, over first passage. PASS needs all three of:
  - (i) the first-passage fold/no-fold outcome matches the prediction (A1: omega v_c <= 1/sqrt 2; A2:
    Omega v_c <= 1) and the per-label equation, on all four rows;
  - (ii) on fold rows, the J -> 0 measure is posed in time, not in J. For each level
    l in {0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.001}, the first time the numeric J reaches l must agree with the
    per-label equation's to <= 5e-3 relative. Near a fold J(t) crosses zero with finite slope, so time-at-level
    is well conditioned where relative J is not;
  - (iii) on no-fold rows, J must agree to <= 1e-3 relative where the per-label J >= J_reg.
- **K-visc (the viscosity has no say).** On a sample (every 8th of the 160 stiffness-on AC2q rows in generation
  order, from index 0, plus their 20 v3s twins), rerun the deciding rung with (c_Q, c_L) = (2, 1). The class
  must not change. FOLD: |dt/t| <= 2.5e-3. HELD: |dJmin/Jmin| <= 0.1.
- **K-dt (the time step has no say).** On the same sample, rerun the deciding rung with cfl 0.2 and sheet
  fraction 0.025, using the same lines.
- **MUTATE-A (AC14's).** A repulsive sheet (sheet = -1) on the zero-charge stream must be HELD, REGULAR.
- **MUTATE-B (AC14's power gate).** An AC2q clock-only row with Pi0 = s^2 = 0.1, M - 1 = 1,
  gamma = (1/0.3)^2/0.1 (Mach 0.3) must be HELD, REGULAR, and converged on the ladder. The method must be able
  to see pressure regularization. AC14 could not run this row.
- **MUTATE-P (powered planted difference).** The planted change is sheet = 1.03 (Sigma_b +3 %). Each planted row
  is graded against its unplanted twin with the pair logic above, at its deciding rung, with its ladder error.
  - P1 (dust, exact size). On the zero-charge row (equal to the clock-only v3s rows' dynamics: the charge excess
    is 0), the planted fold time must equal the independent two-label integration with sheet 1.03 to <= 1e-6,
    and the pair logic must return DIFF-TIME.
  - P2 (stiffness on). Take the first phantom AC2q physical row in generation order whose FS1 class is FOLD.
    The pair logic must return DIFF-TIME or DIFF-LABEL.
  - P3 (clock-pressure shock). On clock-only AC2q row 1, the pair logic must return DIFF-TIME or DIFF-LABEL.
  If any planted difference goes undetected, the method has no power at the 1e-2 line, and no verdict stands.
- **X > 0 (AC14's).** min X/X_bg = 1 - (v_max w/c)^2 > 0.99 on every physical row.

## Reported, not gating

- **K4 (edge sensitivity).** For every pair with a DIFF outcome, the deciding rung of both members is rerun with
  E-b: edge cells pressureless (K = 0 in the 5 % edge cells at both ends). The E-b outcome is reported next to
  the graded one.
  - E-a (graded) is the physical choice. For clock-only AC2q the charge is uniform s^2 right to the stream ends
    (the A2-POST taper acts on the excess, which is 0), so the edge cells are the same fluid as the interior.
    The 5 % exclusion is a reading convention, not unphysical matter.
  - If a DIFF outcome disappears under E-b, it is reported as edge-carried (the stream's own leading part
    shocks), and the label line says so.
- Per FOLD row: whether the fold cell had Q > 0 or a shocked neighbour within 3 cells at t_fold
  (shock-arrival vs free fold).
- The count of rows in which edge cells reached J <= J_thr before the interior event. These are runs that went
  past the first edge fold, where AC14 stalled.

## Lane labels

- **FOLDS-SAME-AS-V3S.** All checks pass, all 240 pairs are converged, and every pair is SAME-FOLD or SAME-HELD.
  The number of SAME-HELD pairs is stated. If it is nonzero, the label reads "FOLDS-SAME-AS-V3S (n pairs held
  in both)": AC2q then adds nothing, and X14's "caustics generic" is not supported for those rows.
- **DIFFERS.** All checks pass, and at least one converged pair is DIFF-TIME or DIFF-LABEL. The label names the
  rows and the sub-type (EARLIER / LATER / REGULARIZES / WORSE), counts per footing, and the K4 E-b reading. It
  stands even if other pairs are OPEN; those are listed.
- **NO VERDICT.** A check fails, or no pair is DIFF and some pair is OPEN or UNRESOLVED. It is given with the
  bracket: the counts of SAME / OPEN / UNRESOLVED pairs, the range of r over resolved FOLD pairs, and the J_min
  range of non-converged rows.

## Compute

nice 15, at most 4 worker processes, 1 thread each. Checkpoints go per row and per rung in `parts/`
(MUTATE/K-visc/K-dt/K4 in separate dirs). SIGTERM stops the current rung without writing it, and a rerun
resumes. RSS stays well under 1 GB.

## Out of scope

- The post-interior-fold evolution (the run stops at the first interior J_thr).
- 3D and spherical cases.
- The nonlinear hold law (constant M per row, as AC10).
- The moving Sun.

A label here is about the planar first interior J_thr event under scheme S, with physical (E-a) edges.
