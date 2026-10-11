# CFG626 FROZEN CRITERIA -- kernel re-check of CFG620 (anisotropic maximum-entropy velocity target) with the repaired nu_mono

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-11.
Lane folder: `campaign_fresh_gravity/CFG626_kernel_recheck_anisotropic_target/`. All other lane folders and `sol61_push/` are read
only and never edited. No PM runs. No downloads.

## Seen before this freeze (stated)

- CFG620's README, FROZEN_CRITERIA (93abcbeb6, committed as CFG598), scripts and all its numbers (results, MUTATE, post JSON).
- The external review `sol61_push/orbit_selection_2026_10_11/REPORT.md` (read as data): it states that the repaired kernel admits
  a positive isotropic high-binding-energy distribution for its inner cusp, while the exponential kernel needs strong
  low-angular-momentum suppression there.
- Analytic expectation (not a computed number of this lane): with the repaired kernel, h(y) = y (nu(y) - 1) is monotone rising
  above Y_P = 2.54, so the point-mass phantom M_ph(r) = r^2 h(r_M^2/r^2) falls like r^2 inward (a cusp, rho ~ 1/r up to the
  logarithmic tail), not like exp(-r_M/r). The compact "hollow" of CFG620 may therefore be absent under the repaired kernel.
- That CFG559's KiDS scoring (the source of CFG620's Q2 numbers, via CFG529/CFG100/CFG495 machinery) already uses the repaired
  nu_mono. CFG620's Q2 reading was therefore a cross-kernel reading; under the repaired kernel it becomes a same-kernel reading.

## What is tested

Whether CFG620's headline results depend on the kernel. The pipeline, cells, gates, verdict rules and MUTATE controls are
CFG620's, unchanged, with ONLY the kernel swapped.

## Settings (as CFG620 except the kernel)

kappa = 1/2 FITTED; footings 9.3603e-11 (can) and 1.1312e-10 (alt), judged separately, never pooled. Candidate B; G9; no EFE;
round per-region phantom; the cold energy's MASS is still required; no dark-matter particle species; not "theory closed".
alpha O(1) FREE, tau as CFG544. No new constants.

**Kernel (the one change).** nu_mono exactly as the PM engines build it (`CFG596_lean_pm_1024/cfg596_pm.py` lines defining
h_rar, dh_rar, Y_P, DELTA = 0.05, LYG, DH_MONO, H_MONO, nu_mono; copied verbatim): h_rar(y) = y / expm1(sqrt y); Y_P = the root
of dh_rar in (1, 5); dh_mono = max(dh_rar, DELTA h_rar(Y_P) / (y + Y_P)) integrated on the 240001-point log grid 1e-12..1e12;
nu_mono(y) = 1 + H_MONO(y) / y. It equals the exponential form 1/(1 - exp(-sqrt y)) for y below about 2.5 (to the table's
interpolation accuracy, reported) and has the monotone tail above.

## Code path (declared)

A thin driver `cfg626.py` imports CFG620's `cfg620.py` / `cfg620_lib.py` read only and runs them unchanged, with:

1. **Kernel swap (env `CFG626_KERNEL` = `mono` | `exp`).** In `mono` mode the phantom function is replaced everywhere the
   exponential form enters: CFG544's `nu_m1` (hence `Mph_enc`, the toy's rho_ph, Jeans target, IC sampling, r99_analytic, C4),
   CFG541's `nu_m1` (hence `Model`: rho_ph, the analytic exhaustion radius r_*, the drift-only release dW), the copy of CFG544
   loaded by CFG550 inside CFG554, and CFG620's `law_S` (Part S exact law: M_ph = M_b(r) (nu_mono(M_b(r)/r^2) - 1) in units
   G = M_b = r_M = a0 = 1). In `exp` mode CFG620's own functions are left untouched.
2. **Cell geometry from CFG541's own Model in both modes.** r_*, f_ret, r_ta, M_cat and dW_per_mass for all 6 cells are computed
   with CFG541's `Model(M_b, a, a0, fret_census(M_b))` (`analytic_rstar()`, and `run(alpha=1)` + `energy()` for dW, CFG541's own
   computation), instead of being read from `cfg541_results.json`. Checked before this freeze (not a lane number): with the
   exponential kernel this reproduces the JSON's r_analytic_kpc and dW_per_mass bit-for-bit for MW and cluster, both footings.
   f_ret, r_ta and M_cat do not depend on the kernel; r_*, the time unit r_*/V_f, the code-unit M_b = r_M/r_* and dW do.
3. **Outputs** go to `../_external_data/cfg626_work/<mode>/` (CFG620's output names), and are copied into the lane folder as
   `cfg626_results_<mode>.json` etc. CFG620's folder is never written. NPROC = 2 (machine constraint, below); the work
   distribution does not affect any number (each run has its own seeded RNG, seed 544).

Everything else -- the orbit library, maximum-entropy solver, LP tests (HiGHS, 60 s per LP), sampler, FIX-A / FIX-AG / FIX-2
operators, bench, ICs B / C / F, the injected overfill IC, run lengths, reading times, G550, gate_age, edge, H and sigma_H, energy
accounting, label code, MUTATE code -- is CFG620's code executed unchanged.

## Hollow / inner region under the repaired kernel (declared now)

CFG620 detects "hollow cells" automatically (rho_ph rising somewhere in (RMIN, r_*)). That detection is kept and reported per cell
for both kernels ("hollow exists": Part S and toy). If a cell that is hollow under the exponential kernel is NOT hollow under the
repaired kernel, the bench H statistic, HOLLOW HELD rule and the MI(b) hollow tooth are evaluated, in `mono` mode, on the
**inner region** r < r_pk,exp, where r_pk,exp is CFG620's toy r_pk converted to the same physical radius (r_pk,exp x
r_*,exp / r_*,mono in the new code units). This is done by giving CFG620's `hollow_toy` that radius as fallback; the cell's own
detection result is recorded separately. Cells with no exponential hollow (MW) remain non-hollow. In Part S, if the repaired
profile is monotone, CFG620's code puts the former hollow inside its "outer" LP region (0.05 r_M .. 0.9 r_*); the LP ISO
"outer" d_min is then the isotropic-support test for that region, and the median beta in 0.05 r_M <= r < r_pk,exp(Part S, r_M
units) is computed from the stored profile.

## Runs

- **mono (primary):** CFG620's full main run (cells, CS, sympy K1-K6, Part S, Part N, dW, 78 bench runs) and its MUTATE run
  (MF, MT; MI read from the mono main JSON), both footings.
- **C-REP (reproduction control, exp mode through the same driver):** cells and dW for all 6 cells; Part S and Part N; and the
  bench subset {A_C_a1.0 (13.8 Gyr, reads 5 and 13.8), b_C (5 Gyr), C2p_vlasov_F (2 Gyr)} x 6 cells = 18 runs. (A full exp
  rerun is not repeated, to keep within the machine constraint; the exp column of every comparison is CFG620's committed JSON.)

**C-REP passes iff:** every cell field (r_*, M_b, M_cat, r_ta, f_ret, dt, t_unit, C4, r99_analytic, r_pk_toy) and dW541 equal
CFG620's JSON to <= 1e-12 relative; Part N solver error, beta shell / inner / edge equal to <= 1e-9 absolute; Part S solver error,
hollow flag, r_pk, beta hollow / bulk medians and edge ratio equal to <= 1e-9; and in all 18 bench runs logXJ, D, dln_r99,
d_logXJ_last2, d_D_last2, sink and (hollow cells) H at every read equal to <= 1e-9 absolute. Part S LP d_min values are compared
and reported; an LP that hit the 60 s limit in either run is disclosed and not counted against C-REP (CFG620 disclosure 5).
**If C-REP fails, no kernel verdict is given.**

## Controls (CFG620's, per mode)

CS (kernel-free; must be identical to CFG620's), C2', C4, mass exact: as CFG620, with CFG620's disclosed readings (CS outside the
inner boundary layer; C4 at the toy's resolution) reported both as frozen and as read. C5 (FIX-2 reproduces CFG544's JSON) is an
exponential-kernel item: in mono mode it cannot hold by construction and is replaced by C-REP; the mono value is reported.

## Headlines and the kernel-robust / kernel-dependent rule (declared now)

Per footing separately (can, alt). Exp = CFG620's committed JSON; mono = this lane. A headline is **KERNEL-ROBUST** iff the
stated condition holds on BOTH footings; **KERNEL-DEPENDENT** otherwise (stated per footing). "Formerly hollow cells" = cluster
and compact (CFG620's hollow cells).

1. **Hollow exists.** Robust iff each formerly hollow cell is hollow under mono (Part S and toy).
2. **Hollow / inner region held (FIX-A, alpha = 1, IC-B 10 Gyr and IC-C 5 Gyr).** Robust iff HOLLOW HELD (|H| <= 0.15 +
   2 sigma_H) in every formerly hollow cell under both kernels, AND FIX-2's overfill of that region (H >= +0.3 at IC-B or IC-C)
   holds under both. If item 1 is dependent, item 2 is read on the inner region and reported as "inner region held" (the item
   then tests a different physical statement and is labelled so).
3. **Anisotropy (Part S target).** Robust iff in every formerly hollow cell the mono median beta over 0.05 r_M <= r < r_pk,exp is
   negative and within a factor 2 of CFG620's beta_hollow_median (0.5 <= ratio <= 2), AND the bulk median |beta| <= 0.1 under
   both, AND the edge sigma_r^2/sigma_t^2 (last bin) <= 0.05 under both, AND the LP ISO outcome in that region is the same
   ("locally isotropic support exists" iff d_min <= 0.02; cluster and compact).
4. **Sharp edge.** (a) Frozen-time label (SHARP / SOFTENED at alpha = 1, IC-B 10 / IC-C 5 Gyr) identical; and (b) at 13.8 Gyr,
   alpha in {1, 2}, every cell and IC has |ln(r_99/r_99,an)| <= 0.1 under both. Robust iff (a) and (b).
5. **Steadiness at the frozen times (G550, alpha = 1).** Robust iff the per-cell G550 pass/fail pattern (IC-B 10 Gyr, IC-C 5 Gyr)
   is identical; "robust in label" (reported separately) iff the target label is identical.
6. **Steadiness by 13.8 Gyr at alpha >= 1.** Robust iff every alpha in {1, 2} run passes gate_age and the edge item at 13.8 Gyr
   under both kernels.
7. **alpha x 0.5.** Robust iff the alpha label is identical AND the alpha = 0.5 IC-B edge fails (> 0.1) in every cell under both.
8. **Overfill.** Robust iff the overfill label is identical (NOT HANDLED: some P > 0.2). P per cell reported side by side.
9. **KiDS edge reading (Q2).** CFG620 read CFG559's sharp row because FIX-A's settled end state is sharp. Rule: the sharp-row
   reading (CFG559's kinetic gain withdrawn) applies iff all alpha in {1, 2} FIX-A runs have |ln(r_99/r_99,an)| <= 0.1 at 13.8
   Gyr. Robust iff the same branch applies under both kernels. No new KiDS fit; the numbers stay CFG559's (repaired-kernel)
   numbers.

Also reported side by side, no verdict weight: Part S / N self-consistency, energy (COMPATIBLE), blow-up, Lyapunov largest rise,
FIX-AG edges and H, beta in the shell, the MUTATE teeth (MI, MF, MT) and whether each bites under mono.

## Frozen label

The six CFG620 labels (target, edge, works in compact, overfill, alpha, Lyapunov) and the "as frozen" control status are recomputed
by CFG620's label code in mono mode. "The frozen label changes" iff any of the six differs from CFG620's. Under the inner-region
fallback the target label's hollow item is the inner-region item (stated with the label).

## Machine constraint (hard)

At most 2 compute processes of 1 thread, total RSS <= 3 GB, `nice -n 10`. Before each stage `vm_stat` free + inactive >= 6 GB,
else wait. The 1024^3 PM job (cfg596_pm.py) and the cfg625 driver are never signalled, killed or starved. Large intermediates in
`../_external_data/cfg626_work/`; console logs deleted after the run.

## Reporting

`cfg626.py` (driver), `cfg626_compare.py` (side-by-side table and the verdicts, read only from JSON), results JSON and `.out`
per mode, README (numbers read from the JSON). Dated disclosures for anything changed after this freeze; this text is never
edited. Commits with specific paths only; no push.
