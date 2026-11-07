# FS2 frozen criteria: a viscosity-free fold reading for AC14's open door ("does AC2q fold like v3s?", planar)

Frozen before any FS2 script is committed or any FS2 number exists. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. No LCDM input. Footings 9.3603e-11 / 1.1312e-10 m/s^2, graded
separately, never pooled.

## Disclosure (what was seen before freezing)

FS2 succeeds FS1 (`closure_2026_11_06/FS1_fold_shock_capturing/`, criteria f716e2f98f, result a7591831b0, pushed
as 6320d7430a). FS1's label was NO VERDICT for one reason: K-visc failed. Doubling (c_Q, c_L) moved phantom
absolute fold times (first interior J <= J_thr = 1e-3) by up to 8 %, and 2 HELD rows' J_min by 10.2 %. Every
other FS1 check passed, and all 480 rows converged.

Everything FS1 committed was read, including the post-result reading `post_visc.py` (information only):
- pair ratios r = t_AC2q / t_v3s moved by <= 5.6e-4 under x2 viscosity;
- clock-only r moved by <= 1e-4 under x2 and x0.5;
- FS1's bracket: 137 SAME-FOLD, 23 SAME-HELD (J_min 1.3e-3 to 3.8e-3), 80 clock-only DIFF-TIME EARLIER
  (r 0.9468 to 0.9471, shock arrival).

Read before freezing, these are grid constants and not graded numbers:
- the stiffness sound-speed scale sqrt(gamma max(Pi0, s^2)) per row class: phantom 2.2e-4 to 1.41e-2 (both
  models); clock-only and soft AC2q 2.0e-5 to 1.1e-4; clock-only and soft v3s 0;
- the generation order of the 160 stiffness-on AC2q rows alternates phantom / clock-only. That is why FS1's
  every-8th sample held phantom rows only.

No FS2 probe was run. No time at the FS2 level below was computed or looked at for any row before this file
was committed. FS1's per-run JSON files do not record it.

## Why the graded observable is the first time J reaches J_reg (written before running)

FS1 showed that the absolute time of the J_thr event in pressure-carrying rows is set inside the captured shock
layer. The cell that reaches J_thr sits in the shocked layer. Its minimum J is fixed by the viscosity
coefficient at every cell count, so the ladder converges while K-visc fails. A reading of J below the shock
jump measures the numerical shock profile, not the action. FS2 therefore grades a reading taken above the shock
layer, where the flow is set by the gravitating dynamics and the jump conditions, not by the viscosity:

**t_reg: the first time min over interior cells of J reaches J_reg = 0.05.**

The reasons this is the physical fold quantity:
1. **It is AC10's own regularization line.** AC10 (frozen) calls a stream REGULAR when J_min >= J_reg. The
   door's question, whether AC2q's pressure keeps a stream from collapsing where v3s collapses, is decided
   at J_reg in the frozen system: a stream that never reaches J_reg is held, and a stream that does reach it
   has collapsed by a factor of 20 in label length. FS2 does not invent a new threshold. It moves the reading
   from J_thr to the line AC10 already uses to separate fold from no fold.
2. **Pressure is dynamically negligible at J_reg on every row.** For p = K/(2 J^2), the Eulerian sound speed is
   c_E = sqrt(K / J). At J = J_reg and the grid's largest K (c0 = 1.41e-2, K = 2.0e-4), c_E = 0.063. That
   compares with the initial stream speed 1, so every row is hypersonic down to J_reg. The compression to
   J_reg is therefore either:
   - smooth, dust-like collapse, where the MC limiter switches Q off (psi = 1 on a linear velocity field); or
   - the arrival of a shock whose post-shock J lies below J_reg.

   In the second case the crossing time is set by the shock's Rankine-Hugoniot speed, which the conservative
   scheme gets right independent of the viscosity coefficient at convergence. Neither case reads J inside the
   shock profile.
3. **It keeps the comparison the door asks for.** For the dust v3s twins, t_reg lies just before the J_thr fold
   that AC14/AC10 read. For the AC2q rows, a regularization would show as REGULAR (never reaching J_reg) or as
   a later t_reg. An earlier collapse would show as an earlier t_reg.

What FS2 gives up, stated in advance: FS2 does not decide whether a shock-held stream's post-shock J lies above
or below J_thr. FS1 showed that at this resolution that is viscosity-set, and FS2 makes no claim about it. FS1's
J_thr reading is recomputed and reported, but it is not graded.

The pair ratio r alone (the parent brief's third option) is not chosen as the graded statistic. A ratio of two
viscosity-set times can be stable without either time being physical, so stability of r is not evidence that r
measures the action. r at J_thr is reported, with its own K-visc movement, as information.

## Physics and method (FS1's, unchanged)

- AC10's planar label system, imported unchanged from `action_search_2026_11_05/AC10_nonlinear_clock/ac10.py`:
  physical_rows() (240 AC2q + 240 v3s twins), constants, initial data, sheet, Gauss sum, A2-POST taper,
  J_thr 1e-3, J_reg 0.05, t_max 6, and the 5 % edge exclusion.
- FS1 scheme S, unchanged:
  - conservative p = K/(2 J^2);
  - Christensen-limited viscosity (c_Q = 1, c_L = 0.5) on pressure cells only;
  - SSP-RK3, dt = min(0.05 WB / max|v|, 0.4 dq / max sigma);
  - cubic-Hermite events.
- The FS2 core is FS1's C core with one addition. For each level l in
  {0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002}, it records the first time min interior J <= l, located by
  the same per-cell cubic Hermite root in the step where it happens. This includes the step that ends the run.
  At each level crossing it also records whether any cell within 3 of the crossing cell had Q > 0 (reported).
- The stopping rule is FS1's (first interior J <= J_thr, or t_max). Because 0.05 > J_thr, every run that stops
  at J_thr has passed J_reg.
- No line of FS1's step, force or J_thr event is changed. The added code only reads the state.
- An independent numpy reference (`fs2_ref.py`, FS1's reference plus the level events) is committed for K0.

## Run classes (graded observable)

- **REACH**: interior J reaches J_reg at t_reg <= t_max.
- **REGULAR**: interior J > J_reg at every step to t_max. J_min is recorded.
- **UNDECIDED**: as FS1 (a non-finite state, more than 2e8 steps, or more than 4 h wall time).

## Convergence ladder

FS1's ladder, applied to t_reg: N = 2000/4000/8000 (+16000).
- REACH: |t_8000/t_4000 - 1| <= 2.5e-3.
- REGULAR: |Jmin_8000/Jmin_4000 - 1| <= 0.1.
- The class must be the same on every rung used.
- A row that fails gets N = 16000 and is judged on 8000 vs 16000.
- The deciding rung's last change e is carried into the pair decision.

## Pair outcomes (AC2q row vs its v3s twin; both converged), with r = t_reg,AC2q / t_reg,v3s and E = e_AC2q + e_v3s

- **SAME-REACH**: both REACH, |r - 1| + E <= 1e-2.
- **SAME-REGULAR**: both REGULAR.
- **DIFF-TIME**: both REACH, |r - 1| - E > 1e-2. Reported as EARLIER (r < 1) or LATER.
- **DIFF-LABEL**: one REACH, one REGULAR. REGULARIZES if AC2q is REGULAR, WORSE if the reverse.
- **UNRESOLVED**: both REACH, and neither SAME-REACH nor DIFF-TIME.
- **OPEN**: any member not converged.

## Checks (all gating; any failure gives NO VERDICT)

- **KA (FS1's numbers).** FS2 reruns every rung FS1 ran in `FS1_fold_shock_capturing/parts/` (1455 rung files).
  - For every rung, FS2's FS1-reading fields must equal FS1's file to <= 1e-9 relative: the class at J_thr,
    t_fold, t_fold_all, J_min and J_min_all. The step count must match exactly.
  - FS1's frozen grade logic applied to FS2's J_thr fields must give FS1's bracket exactly: 137 SAME-FOLD,
    23 SAME-HELD, 80 DIFF-TIME.
  - On FS1's K-visc sample, FS2's x2-viscosity reruns must equal FS1's `parts_checks` files to <= 1e-9.
- **K0 (core = reference).** On FS1's three K0 rows at N = 500 (soft v3s row 1, clock-only AC2q row 1, and the
  strongest phantom AC2q row run to t = 1.5), the core's t_fold (or J_min) and every recorded level time must
  equal `fs2_ref.py` to <= 1e-9 relative.
- **K1.** On the zero-charge row at N 2000, t_reg must equal the independent two-label integration's first
  J <= J_reg time on the front interior cell to <= 1e-6 (FS1's method). FS1's K1 at J_thr must still pass.
- **K2/K3.** FS1's stress-row checks, rerun with FS2's core, with FS1's lines.
- **K-visc (graded observable).** The sample is every 4th phantom AC2q row (20), every 4th clock-only AC2q row
  (20) and every 8th soft AC2q row (10), each in generation order from index 0, plus all 50 v3s twins.
  Rerun each at its deciding rung for t_reg with (c_Q, c_L) = (2, 1) and with (0.5, 0.25). On both variants:
  - the class must not change;
  - REACH: |dt_reg / t_reg| <= 2.5e-3;
  - REGULAR: |dJmin / Jmin| <= 0.1.
  Reported, not gating: the same shifts at every recorded level, and at J_thr. These show where the shock
  layer starts to set the reading.
- **K-dt.** On the same sample, rerun the deciding rung with cfl 0.2 and sheet fraction 0.025, with the same
  lines.
- **MUTATE-A.** A repulsive sheet (sheet = -1) on the zero-charge stream must be REGULAR on every rung.
- **MUTATE-B.** FS1's Mach 0.3 clock-only row (Pi0 = s^2 = 0.1, M - 1 = 1, gamma = (1/0.3)^2/0.1) must be
  REGULAR and converged.
- **MUTATE-P (planted Sigma_b +3 %, sheet = 1.03).** Each planted row is graded against its unplanted twin with
  the pair logic above.
  - P1: the zero-charge row. The planted t_reg must equal the two-label integration with sheet 1.03 at J_reg
    to <= 1e-6, and the pair logic must return DIFF-TIME.
  - P2: the first phantom AC2q physical row in generation order whose FS2 class is REACH. The pair logic must
    return DIFF-TIME or DIFF-LABEL.
  - P3: clock-only AC2q row 1. The pair logic must return DIFF-TIME or DIFF-LABEL.
- **X > 0.** min X/X_bg > 0.99 on every physical row (FS1's line).

## Reported, not gating

- **K4 E-b** (edge cells pressureless) on every DIFF pair, at the deciding rungs. A DIFF that disappears under
  E-b is reported as edge-carried.
- Per REACH row: whether the J_reg crossing cell had Q > 0 within 3 cells (shock arrival vs smooth collapse).
- FS1's J_thr pair outcomes recomputed (equal to FS1's by KA), with r at J_thr and its K-visc shift.
- The level profile: pair r at each recorded level.

## Lane labels

- **FOLDS-SAME-AS-V3S.** All checks pass, all 240 pairs are converged, and every pair is SAME-REACH or
  SAME-REGULAR. The number of SAME-REGULAR pairs is stated.
- **DIFFERS.** All checks pass, and at least one converged pair is DIFF-TIME or DIFF-LABEL. The label names the
  rows and the sub-type (EARLIER / LATER / REGULARIZES / WORSE), gives counts per footing, and gives the K4 E-b
  reading. It stands even if other pairs are OPEN; those are listed.
- **NO VERDICT.** A check fails, or no pair is DIFF and some pair is OPEN or UNRESOLVED. It is given with the
  bracket: outcome counts, the r range over resolved REACH pairs, and the J_min of non-converged rows.

"Fold" in an FS2 label means the first interior J_reg crossing under scheme S with physical (E-a) edges.

## Compute

nice 15, at most 4 worker processes, 1 thread each. Checkpoints go per row and rung in `parts/` (checks in
`parts_checks/`). SIGTERM loses only the running rung, and a rerun resumes. RSS stays well under 1 GB. This
lane's grader is loaded by file path, never by `import grade`: AC10's directory is on sys.path, and its
grade.py rewrites AC10's GRADE.json.

## Out of scope

- Evolution after the interior J_thr event.
- Whether shock-held post-shock J lies above or below J_thr.
- 3D cases, the hold law and the moving Sun.
