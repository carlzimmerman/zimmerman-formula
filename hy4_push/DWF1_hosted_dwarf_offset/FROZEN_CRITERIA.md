# DWF1 frozen criteria: what moves a hosted dwarf UP under form B, without moving the field population

Lane HY4-9. TEST lane: it relabels nothing, adopts nothing, is not registered, and changes no frozen label of RB2, X1,
XF1, SE2, S1, U1, SCS2, SCS3, EFN1, DD1 or HIS1. kappa = 1/2 FITTED; not theory closed. Cold dark energy is a gravitating
field component, never a particle. Footings are graded separately and never pooled: canonical a0 = 9.3603e-11 m/s^2,
alt a0 = 1.1312e-10 m/s^2.

Frozen before any DWF1 script exists and before any graded DWF1 number is computed. Any change after this freeze goes in
an AMENDMENT_A#.md committed alone and labelled post hoc.

---

## 0. The anomaly this lane takes as its target (RB2, on disk)

RB2 (closure_2026_11_09/RB2_form_b_hosted_rows, RESULT.md, rb2.out) reads **B FAILS ON THE HOSTED ROWS** on both
footings. Its graded class residuals (Delta, see section 1 for the sign) are

| class | N | B (canonical) | B (alt) | law alone, static field (canonical / alt) |
|---|---|---|---|---|
| MW ultra-faint | 31 | +0.634 [+0.433, +0.865] | +0.592 [+0.391, +0.822] | +1.566 / +1.561 |
| bright M31 | 25 | +0.273 [+0.085, +0.473] | +0.231 [+0.046, +0.429] | +0.633 / +0.600 |
| MW classical (8) and Coma UDGs (9) | | B CONSISTENT on both | B CONSISTENT on both | |
| LG field (control, no host) | 13 | +0.054 | +0.017 | +0.058 / +0.023 |

DD1 independently finds the ultra-faints fail every candidate rule it tries (worst class under P1: +0.97 dex, 5.0 se).
HIS1's formation reading fails its H3 test on the isolated faint gas-rich rotators (-0.278 / -0.315 +- 0.080 dex, below
the law). RB2 also names four LOW rows (DF2, DF4, NGC 147, IC 1613) that no tide can reach; this lane does not re-grade
them, they are the other side of the same anomaly and are listed only as context.

## 1. Sign convention (this is the whole question)

**Delta = log10(g_obs / g_pred)** at r_1/2, dex, exactly X1's and RB2's. A positive Delta means the measured field
exceeds the prediction, i.e. **the system carries MORE non-baryonic mass than the law gives it**.

- "A hosted dwarf sits HIGH / UP" = it carries more non-baryonic mass than the prediction = Delta > 0.
- "A physical effect moves a hosted dwarf UP" = it moves the **predicted non-baryonic mass up**, i.e. it moves **Delta
  down toward 0**. This is the direction a candidate must have to close the anomaly. (Candidate (b) is pre-declared in the
  brief to move them "the OTHER way", i.e. Delta up; that fixes the convention.)
- The size a candidate must deliver, to be the answer to the anomaly: **-0.63 dex** for the MW ultra-faints
  (canonical; -0.59 alt) and **-0.27 dex** for the bright M31 dwarfs (-0.23 alt), on the class median, with the 95 %
  interval coming to contain 0.
- It must do this **without moving the LG field population** (13 systems, no host): the field class's shift must stay
  inside +-0.05 dex.

## 2. Rows, data paths and estimators (copied from the lanes named; nothing imported from another lane's folder)

- **Rows:** X1's sample and classes, verbatim (rebuild_2026_10_22/X1_hosted_recount). Graded: **MW ultra-faint** (31) and
  **bright M31** (25). Control, graded for the "does not move the field" clause: **LG field** (13). Reported, not graded:
  MW classical (8), M31 others (5), M31 dE (3), MW other.
- **Data read as data, not recomputed:**
  - `rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv` (both footings): per-system Delta and sdMC for
    `iso AQUAL L*0`, `AQUAL + EFE L*0 (exact MOND + EFE)`, `v3 L*floor`, `Newton`; plus `d_host_kpc`, `x_e_mid`,
    `y_plummer`, `rh_pc`, `logMstar`, `sigma`.
  - `rebuild_2026_10_22/X1_hosted_recount/x1_stage_tables_{canonical,alt}.json`: X1's committed `iso0` / `emb0` tables
    (log10 g_pred/g_bar at three y values, E-W and E-V) and each system's `xe` (E_lo / E_mid / E_hi) and `y0`.
  - `closure_2026_11_09/RB2_form_b_hosted_rows/rb2.json`: RB2's per-system B residuals (`Delta.iso`, `Delta.prim`,
    `Delta.strong`), `rJ_over_r12`, `d_kpc`, `peri`.
- **The record's external-field machinery** (this is the arbiter for candidate (a) and (c)): X1's exact AQUAL solve with a
  uniform background, `d10_solver.Solver2D(grid, y, x_e, Lam, isolated=False)` from
  `doors_push_2026_10_22/D10_native_Lstar` (read-only import), E-W (est 0) at r_1/2 = (4/3) R_h, Plummer a = R_h, in
  X1's units (a = 1, a0 = 1), `logG(y, xe, Lam) = log10(6 * wo * (4/3) / y)`. This is the same call X1's stage `tables`
  used to make its committed `emb0` tables; X1 validated it against F2's independent AQUAL solver (C3c, 1.8e-3) and
  against route F (C3b, 2.8e-3). Screening is OFF (Lam = 0) in the graded reading, because form B's graded law is the
  brief's algebraic law with no screening.
- **The host's field:** X1's / S1's `g_host(R, M_b, a0) = 0.5 gN (1 + sqrt(1 + 4 a0 / gN))`, `gN = G M_b/(R + 3 kpc)^2`,
  with MHOST = MW 6.0e10, M31 1.0e11, field 6.0e10 Msun (S1's constants), and X1's distance rule `Rh_X1`. The graded
  external field is `x_e = g_host / a0` at E_mid; E_lo (4.0e10) and E_hi (Mb_hi) are reported as a bracket.
- **Statistic:** XF1's C2, verbatim as RB2 graded it: bootstrap median over the class's systems of Delta_i + N(0, sd_i),
  4,000 resamples, seed 11, 95 % interval from the 2.5 / 97.5 percentiles (`boot_median`, copied).

## 3. Candidates and their pre-registered kills

Each candidate is graded on the MW ultra-faint and bright M31 classes, on both footings, and on the LG field control.

### (a) The host's external field: "the dwarf sees the host's field, the law is nonlinear, so the host's field adds"

**What is computed.** For every graded row, the prediction of the record's exact AQUAL solve **with** the host's field at
the dwarf's distance, `x_e_mid`, against the prediction **without** it (x_e = 0, which is form B's isolated law, the same
quantity RB2 graded). The per-system shift is `s_i = Delta[EFE]_i - Delta[B]_i`; the class shift is the difference of the
C2 medians. Secondary reading: X1's `v3 L*floor` column (the law with screening at the L* floor, external field on),
which is the "law alone" row RB2 printed.

- **KILL A1 (sign):** fires if the class-median shift is **positive** (the host's field lowers the prediction, i.e. moves
  the dwarf DOWN in non-baryonic mass) for the MW ultra-faints, on a footing.
- **KILL A2 (size):** fires if the shift's magnitude in the favourable direction is below 0.3 dex (a candidate that moves
  the right way by less than a third of the 0.63 dex gap is not the answer).
- Field-population clause: the LG field class shift is reported against the +-0.05 dex line.

### (b) A formation-time amount (HY4-5's reading) plus tidal stripping

**What is computed.** The tidal-stripping half is graded with RB2's own Jacobi machinery, read from `rb2.json`: each
row's B residual at RB2's primary edge and at its **strong-tide edge** (pericentre, k = 3 at the 16th-percentile
pericentre from the LVD orbit), and the class C2 medians of both. The formation-time amount half: **HY4-5's reading is
not on disk at this freeze** (no HY4-5 folder, no HY4-5 output, anywhere in the repository; the only HY4 files are
`hy4_push/` and `hy4_preview_push/`, which contain no formation-time amount for these systems). That half of the row is
therefore left **UNGRADED**, and DWF1 says so. It is not filled with an estimate.

- **KILL B1:** fires if the strong-tide-edge class median **exceeds** the primary-edge class median (stripping removes
  non-baryonic mass, so it moves the residual up, the pre-declared "OTHER way"), for the MW ultra-faints, on a footing.

### (c) The amount set when the dwarf fell in, at the host's field

**What is computed.** The prediction of the record's exact AQUAL solve at the dwarf's **own** y0 (baryons and size as
measured today, so nothing is invented) and at the host's field at a ladder of infall distances
`d_inf / d_today in {1, 1.5, 2, 3, 4, 6, 8, infinity}`, with `x_e(d_inf) = g_host(d_inf, M_host)/a0`. The amount is then
frozen at that value and the residual recomputed. The ladder covers the whole range without needing an infall distance
that is not on disk; `d_inf = infinity` is the kindest case (no host field at infall).

- **KILL C1 (monotonicity / the bound):** fires if, for every graded row and every rung of the ladder,
  `pred(y0, x_e(d_inf)) <= pred(y0, 0)` to within 1e-6 dex. (Then no external field at infall can give the dwarf MORE
  non-baryonic mass than form B's isolated law already gives it, so (c) can never move a hosted dwarf UP.)
- **KILL C2 (best case):** fires if the kindest rung of the ladder (d_inf -> infinity, i.e. no field at infall) returns
  B's residual **unchanged** (|shift| < 0.01 dex), so (c) does not close any of the gap.
- **Reported, not graded:** the infall size that (c) would need. For each rung, the factor `r_h(infall)/r_h(today)`
  (equivalently the y ratio, at fixed baryons) that would make `pred(y_inf, x_e(d_inf))` equal B's prediction plus the
  0.63 dex needed. This is a requirement, not a measurement: no dwarf's infall size is on disk.

## 4. Lane label

Per footing, from the graded kills:

- **NO CANDIDATE MOVES A HOSTED DWARF UP:** every graded candidate is killed (A1 or A2 for (a), B1 for (b), C1 and C2 for
  (c)) and no candidate's after-residual brings the MW ultra-faint 95 % interval to contain 0.
- **A CANDIDATE MOVES A HOSTED DWARF UP:** some candidate's after-residual for the MW ultra-faints has a 95 % interval
  containing 0, with a class shift of -0.3 dex or better, and the LG field control stays inside +-0.05 dex.
- **SPLIT:** anything else, with the cells printed.

## 5. Known answers (a failure stops grading; every number printed in dwf1.out)

- **KA1 (B reproduced).** RB2's B class medians and 95 % intervals for MW ultra-faint, bright M31, MW classical and LG
  field, recomputed here from X1's `x1_per_system.csv` (`iso AQUAL L*0`) through XF1's C2, must equal rb2.out to
  **0.01 dex** (RB2 used the analytic law and X1's tables use the exact solver; RB2's own KA4 puts that difference at
  0.006 dex, so the line is 0.01).
- **KA2 (the EFE solve is X1's).** My new solves at (y, x_e_mid, Lam = 0), E-W, must reproduce X1's committed `emb0`
  table at each of its three y values to **1e-3** dex, over all graded rows.
- **KA3 (the isolated limit).** The same call at x_e = 0 must reproduce X1's committed `iso0` table to **1e-9**.
- **KA4 (the EFE column is the record's EFE).** X1's per-system `Delta[AQUAL + EFE L*0 (exact MOND + EFE)]` column,
  recomputed through X1's `pred_draws(..., "emb0", 0)` from the committed tables, to **1e-9**.
- **KA5 (the cut and the estimator, RB2's).** RB2's per-system `Delta.iso` and `rJ_over_r12.prim`, read from rb2.json,
  agree with X1's `Delta[iso AQUAL L*0]` to 0.01 dex; the r_J -> infinity limit returns the isolated law and r_J -> 0
  returns Newton (RB2's KA5, re-checked on the copied code to 1e-12).
- **KA6 (monotone in the field).** On a grid y in {1e-4, 1e-3, 1e-2} x x_e in {0, 0.005, 0.01, ..., 0.5}, `logG` is
  non-increasing in x_e. Printed; it is the content of KILL C1 in the clean case.

## 6. MUTATE (separate outputs dwf1_MUTATE.out / dwf1_MUTATE.json; the arm must fail)

- **M1, X1's own host-field bug:** the background passed to the solver is the Newtonian `y_e = x_e^2/(1 + x_e)` instead of
  the total `x_e` (this is verbatim X1's `--mutate` arm). Bites iff the MW ultra-faint EFE shift falls by more than
  **0.1 dex** against the exact-EFE shift, on both footings.
- **M2, the infall field overstated:** rung `d_inf = d_today` replaced by `x_e -> 10 x_e(d_today)`. Bites iff the MW
  ultra-faint residual at that rung exceeds the rung-1 residual by more than 0.1 dex.
- **M3, the arm that must fail:** with M1 active, **KA2 must FAIL** (my solves no longer reproduce X1's `emb0` by more
  than 0.05 dex on at least one graded row), and the mutate run must exit non-zero. This is the "mutation arm must fail"
  clause: a pipeline that reproduces X1's external-field tables must be shown to break when the external-field
  background is wrong.

## 7. What was seen before this freeze (not blind; disclosed)

- Read in full: RB2's FROZEN_CRITERIA.md and RESULT.md; X1's README and the columns of `x1_per_system.csv`;
  SCS2's and SCS3's RESULT.md (the external-field families are NO VERDICT, UNSTABLE in regions);
  EFN1's RESULT.md (the nonlinear outcome of that instability is NO VERDICT); HIS1's RESULT.md (H3 fails on the isolated
  faint rotators); DD1's RESULT.md (NO RULE; the ultra-faints fail every candidate); fable52_push/README.md (the RB2
  quote).
- **Computed in a scratch probe before this freeze, from X1's committed CSV only (no solve, no new physics):** the C2
  class medians of X1's own columns, which are the "before" and "after" of candidate (a). They are disclosed here so
  nothing is hidden:
  - MW ultra-faint: iso +0.632 [+0.430, +0.864] / +0.591 [+0.389, +0.821]; AQUAL+EFE +1.369 [+1.033, +1.757] /
    +1.336 [+1.003, +1.727]; v3 L*floor +1.566 / +1.561.
  - bright M31: iso +0.267 [+0.085, +0.468] / +0.228 [+0.044, +0.428]; AQUAL+EFE +0.606 / +0.567; v3 +0.633 / +0.600.
  - LG field: iso +0.053 / +0.016; AQUAL+EFE +0.054 / +0.017 (shift +0.001 dex).
  - x_e_mid medians (canonical): UF 0.1514, bright M31 0.0787, LG field 0.0107. UF per-system EFE-minus-iso shift:
    median +0.790 dex, from +0.051 (Eridanus II) to +1.382 (Bootes III).
  So candidate (a)'s direction was already visible before the freeze. The kill lines, the ladder for (c), the MUTATE
  expectations and every per-system table were frozen before the lane's own script ran.
- **Not computed before this freeze:** any solve by this lane (the D10 solver was exercised once on a synthetic
  (y = 1e-3, x_e = 0 / 0.038 / 0.15) triple to time it, which showed log10 g_pred/g_bar falling 1.784 -> 1.342 -> 0.800;
  that is the direction KILL A1 and KILL C1 assert, seen on a synthetic point before the freeze and disclosed here);
  any per-system (c) number; any MUTATE number.

## 8. Hand estimate (frozen, to be marked HIT / MISS)

- (a) MW ultra-faints: shift **+0.74 +- 0.1 dex** (wrong sign); bright M31 **+0.34 dex**; LG field **+0.001 dex**
  (the field population is not moved, so the "without moving the field" clause is met and the sign is what kills it).
- (b) strong-tide edge: MW ultra-faints **+0.634 -> +0.695** (canonical), i.e. up, the pre-declared other way; the
  largest per-system move about +1.94 dex (Antlia II).
- (c) best rung (no field at infall) returns B unchanged, **+0.632**; at `d_inf = 2 d_today` (x_e about 0.04 for the
  median ultra-faint) the UF residual lands about **+1.0 to +1.2**; at `d_inf = d_today` it is the (a) number, **+1.37**.
- (c) requirement: closing 0.63 dex at x_e about 0.04 needs the dwarf to have been about **4 to 6 times larger** at
  infall (y_inf about y_today / 20 to / 30).
- Lane label: **NO CANDIDATE MOVES A HOSTED DWARF UP** on both footings.

## 9. Limits stated now

- Spherical, isotropic, equilibrium Plummer dwarfs; the Wolf (E-W) estimator; mass follows light; Upsilon_V = 2; stars
  only; an instantaneous tidal cut. Exactly RB2's and X1's limits, so the numbers are comparable to theirs.
- The external field is X1's / S1's convention: the host's own law field at the dwarf's distance from a point mass
  (MW 6.0e10, M31 1.0e11, 3 kpc softening) at E_mid, with E_lo / E_hi as a reported bracket. Not a new measurement.
- The external-field configuration is exactly the one SCS2 and SCS3 could not decide (UNSTABLE in regions, NO VERDICT on
  the magnitudes) and whose nonlinear outcome EFN1 could not decide (NO VERDICT). This lane grades the *size and sign of
  the effect if it is turned on*; it does not say that configuration is stable or that it exists.
- (c) uses each dwarf's baryons and size as measured today. No infall distance, no infall size and no gas history for
  these systems is on disk; those are reported as requirements, never as measurements.
- No LCDM-calibrated quantity enters a graded row.

Compute: one thread, under 1 GB, minutes. Outputs: dwf1.py, dwf1.out, dwf1.json, dwf1_MUTATE.out, dwf1_MUTATE.json,
RESULT.md. Any change after this freeze goes in an AMENDMENT_A#.md committed alone and labelled post hoc.

kappa = 1/2 FITTED; not theory closed. Relabels nothing.
