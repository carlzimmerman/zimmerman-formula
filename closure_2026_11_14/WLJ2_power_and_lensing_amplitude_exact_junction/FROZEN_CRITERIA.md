# WLJ2 FROZEN CRITERIA: rows 24 (matter-power redistribution) and 25 (weak-lensing amplitude) with the law exact inside the settled radius

Committed alone, before any script of this lane exists and before any number of this lane is computed. TEST lane, NOT
blind. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt
(a0 = 1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy is a gravitating field component; no particle
is added. kappa = 1/2 and the share 5.41 are FITTED. Rule 6 is a candidate, NOT ADOPTED. A HOLDS, or a relief of the
tension, found here is a hit that awaits an independent blind re-grade, never more. Nothing here can say the data favour
the framework.

## 0. What I had seen before this freeze (I am not blind)

- WLJ1 (`closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/`): FROZEN_CRITERIA.md, AMENDMENT_A1.md,
  AMENDMENT_A2.md, RESULT.md (every number in it), the scripts `wlj1_hm.py`, `wlj1_c4.py`, `wlj1_shear.py`,
  `wlj1_kl1bx1.py`, `wlj1_lwb.py`, `wlj1_grade.py`, the stage timings in its logs and `.out` tails, the canonical polish
  and legacy `.out` lines, and the P4 scan numbers in `wlj1_shear.json` (pinned minus best in KiDS widths: REF 5.409 /
  5.408, ADOPT 5.622 / 5.779, split f 2 5.458 / 5.515; width 0.016) and REF's P4 chi^2_data 147.70, p 0.00315.
- XJ1 (`closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface/`): FROZEN_CRITERIA.md, AMENDMENT_A1 to A5, RESULT.md
  (every number in it: flux-level holds at Ec3, E0.5, Ec2, E0.75; E1 NO VERDICT / FAILS; E2, Ezv, E3 fail; matter level;
  lensing G4 passes at every radius; caustics at 0.68 / 0.535 R_fold at z 0), `xj1_lib.py`, `xj1_lib2.py`,
  `xj1_matter3.py` and the head of `xj1_matter.py`, the head of `xj1_ka_tables3.py`, `xj1_shells.py`, the headers of
  `xj1_lens.py`; the key lists of `xj1_ka_tables{,2,3}.json`, `xj1_matter3_canonical.json`, `xj1_lens{,3}.json`, the first
  `surfaces` entry of each tables file (z 2.2 canonical), XJ1's stored Ec3 matter entry (canonical) and one s_table entry
  of `xj1_lens.json`; the structure and the last rows of `shells/xj1_shells_canonical_M10.45.json` (667 rows from z 10.0
  to z 0; at z 0 R_fold 139.3, R_2 95.0, R_3 74.6 kpc). I have not read XJ1's `parts_*`, `tmp_a` or `logs`, nor
  `COMPLETED_FORM_V2_CANDIDATE.md`.
- FWN1R's `fwn1r_lib.py` (its `rec()`, `vstar`, `split_fn`, `tables`).
- No WLJ2 number exists. Nobody has computed rows 24 or 25 with the exact junction.

## 1. Cases (same parameters, halo list, baryons and machinery as WLJ1)

Machinery: WLJ1's, unchanged except where named. FZS1's `fzs1_hm.py` prefix (FRZ1's halo model at z, CO1's layout made
z-aware, FLD1's R_fold) is the namespace returned by FWN1R's `rec()`, reached through XJ1's `xj1_lib2.py` imported
read-only from XJ1's folder with bytecode off, after its `install()` (which swaps FZS1's loaded FLD1 series for XJ1's
8-column shell runs in memory; first five columns checked equal to 1e-9). Spectra and ratios exactly as WLJ1:
R_tot = 1 + (P_case - P_Lta) / P_std, R_bar = 1 + (P_Rb - P_Lta) / P_std, R_cold = R_tot / R_bar.

Boundary for every case below except REF and ADOPT: WLJ1's, a halo with FRZ1 v_vir > v*(z) = v*(0) / E(z) takes "Rb" at
every radius (JNT2's `vstar_kms`, v*(0) = 668.5 / 807.9 km/s).

| key | inside the settled radius | settled radius | role |
|---|---|---|---|
| REF | - | - | the pure reference ("Rb" everywhere) |
| ADOPT | - | - | the law's layout "B" at every radius, no boundary (control) |
| S2 | the law's cold halo rescaled by s (FZS1's junction) | 2 R_fold | WLJ1's SPLIT f = 2, the record's junction (control) |
| **Ec3** | the law exact (XJ1's junction E) | third caustic R_3(z, M_b) | graded |
| **Ec2** | E | second caustic R_2(z, M_b) | graded |
| **E0.5** | E | 0.5 R_fold | graded |
| **E0.75** | E | 0.75 R_fold | graded |
| **E1** | E | R_fold (the first caustic) | graded |
| E2 | E | 2 R_fold | reported: the contrast that fails the forest |

The exact junction E (XJ1 criteria section 1, unchanged): for a slow halo, M_E(r) = M_B(r) for r <= R_set; beyond,
M_E = Bar + C_B(R_set) + t [C_R(r) - C_R(R_set)], t = [C_tot - C_B(R_set)] / [C_tot - C_R(R_set)]; R_set capped at r_ta;
R_set at r_ta (den <= 0) gives "B" at every radius; regime "L" haloes and R_set <= 0 give "Rb". R_set from XJ1's
`rsurf_com(hb, ft, z, col, mult)`: col = XJ1's `COL_K[3]`, `COL_K[2]` (shell columns R_3, R_2) with mult 1, or
`COL_FOLD` with mult 0.5, 0.75, 1, 2.

**The layout function** is XJ1's `exact_fn` formula copied (cited) with WLJ1's `lay_case` plumbing of the layout options
(`opt` to mode "B", `optR` to "Rb" and `Bar`), so that CO1's layout brackets can be applied to E cases as WLJ1 applies
them to its split. Known answer KA-L below proves the copy equals XJ1's `exact_fn` with no options.

**Redshift (WLJ1's, unchanged).** Primary for every case: its own z = 0 ratio held in z. Bracket: each case's own ratio
at the CFG592 nodes z 0, 0.5, 1 for C5 and P4; on z 0, 0.5, ..., 3 (linear between) for C4. KL1, BX1, LWB1, LWB1R held only.

**Twins** (WLJ1 section 6, with Ec2 in the place of S2): **TW-B** = Ec2 with the boundary at 2 v*(z); **TW-L** =
R_cold' = 1 + 2 (R_cold,Ec2 - 1), R_tot' = R_bar R_cold'. Ec2 is the middle of the five graded radii (R_3 < 0.5 < R_2 <
0.75 < 1 in R_fold). The S2 control's twin results are WLJ1's stored ones (`wlj1_grade_MUTATE.json`, read-only).

## 2. Ambiguities in XJ1's library below z = 2.2, and my choices (stated before any number)

1. **Redshift range of the surfaces.** XJ1's shell runs (`shells/xj1_shells_<footing>_M<logMb>.json`) hold the full
   series from z 10 to z 0 (667 rows), so R_2 and R_3 exist at every node z 0 to 3 these gates need, read with FZS1's
   interpolation unchanged (linear in z along the series; log R linear in log M_b between the 12 masses; M_b^(1/3)
   beyond the ends). No shell is run here. XJ1 graded nothing below z 2.2 except reported z 0 ratios; the use below
   z 2.2 is this lane's. If a surface column is 0 at some table mass and node z, the halo gets "Rb" (XJ1's R <= 0
   rule); the count is reported (known answer KA-Z0 below asks it to be zero at z 0 to 3).
2. **Extrapolation.** At z 0 slow haloes reach M_b above 10^12 Msun (M200c up to 6.9e13 / 1.2e14 Msun/h), outside
   FLD1's table; R_set there follows FZS1's M_b^(1/3) rule, as WLJ1's split already did. Said, not changed.
3. **The cap.** At low z, 2 R_fold (and possibly R_fold) exceeds r_ta for many haloes (FLD1: R_ta / R_fold 1.92 at z
   0); those haloes take "B" at every radius. The share capped is reported per case, z and footing.
4. **One namespace.** XJ1's `exact_fn` and `rsurf_com` read FWN1R's `rec()` namespace, while WLJ1's `wlj1_hm.py`
   executes its own copy of the same FZS1 prefix. Two copies would carry two `set_z` states. Choice: every case (REF,
   ADOPT and S2 included) is built in the one namespace `rec()` after `install()`. Guarded by KA-X1 (WLJ1's stored arrays
   reproduced) and KA-H3 (JNT2's).
5. **v*.** WLJ1 uses JNT2's `vstar_kms`, XJ1 FWN1R's `vstar`. I use JNT2's (the gates are WLJ1's); KA-V asks them equal
   to 1e-12 relative at every node z.
6. **KL1's deskids group** (frozen-scan DES and KiDS-1000, reported only under WLJ1's A2, except the ADOPT KiDS-1000
   known-answer rows) is run last; its ADOPT rows run first within it. If it does not finish, the grader reads the
   gate from Legacy and polished DES (the gating rows), reports the missing KiDS-1000 column as missing, and the KL1 /
   BX1 known answer is read from the rows that exist. This is the only change to WLJ1's grader beyond the case list,
   the twin case and this lane's words.
7. **What does not overlap with XJ1.** XJ1's lensing G4 inputs and its z 0 s table come from SRH1's lens profile (a
   point baryon mass, ONE1's KiDS galaxy-galaxy gate), not from FRZ1's halo model; they share no number with this lane
   and are not used. The overlap used is XJ1's matter-level R_cold and its profile tables (KA-XJ below).

## 3. The gates (WLJ1's, exactly as it finally graded them: its criteria with A1 and A2)

Row 24: G-C4 (CO1 C4, PR4 lensing, line |r_eff - 1| <= 2 sigma_A,rel = 0.0481 and shape chi^2 <= 18.48), G-C5 (CO1 C5,
raw KiDS d_cold, klass with the robust set, tooth), CO1's row rule, G-HLF1 (HLF1 Part A, own list, f_res >= 0.5 at k 1).
Row 25: G-P4 (CO2 P4, raw KiDS at the pinned sigma8, p lines 0.05 / 0.0027), G-KL1 (KL1 Part C gate, Legacy frozen scan
with C3b, DES polished, |g| <= 2 and p >= 0.05), G-BX1 (the same with BX1's splice), G-LWB1 and G-LWB1R (J label, pi_max
40 / 80 / 100). KL1 / BX1 transfer rule: A3_AD x [R_tot,case / R_tot,ADOPT] (z 0 held); additive transfer as bracket.
All lines, labels, code paths, brackets and lane-as-frozen notes are WLJ1's sections 2, 3 and 5 word for word, with
"SPLIT" read as the case and "f = 2" (where WLJ1 ran a costly bracket only at f = 2) read as Ec2. Labels:
- **ROW HOLDS WITH THE EXACT JUNCTION / ROW FAILS WITH THE EXACT JUNCTION / NO VERDICT** per gate, case, footing, by WLJ1's
  mapping; **FRAGILE** (bracket named); **EQUALS THE REFERENCE THERE** by WLJ1's rule (|s_E - s_REF| <= |s_E - s_ADOPT|
  and <= 0.25 D); the word printed beside whether it differs from ADOPT's; a HOLDS that differs from ADOPT's is a hit.
- Row word per case and footing: FAILS if any gate fails, HOLDS if every gate holds, NO VERDICT otherwise.
- **Row 24 summary word per footing:** the common row word of Ec3, Ec2, E0.5, E0.75, E1 if all five share it; otherwise
  "NOT RESOLVED (the word depends on the radius)" with each case's word.

## 4. Row 25: does the exact junction RELIEVE, LEAVE UNCHANGED or WORSEN the tension? (rule frozen here)

"The tension" is what WLJ1 named it: raw KiDS wants sigma8 about 5.4 KiDS widths below the CMB-pinned value, and the
lensing-amplitude gates sit at their gaps. Seven statistics, all in widths, positive meaning the data want less amplitude
than the model's target, taken from the same numbers WLJ1 printed:

| | statistic | source | floor delta |
|---|---|---|---|
| T1 | KiDS-1000 raw: pinned minus best sigma8, in widths | P4 scan (`P4_scan`) | 0.02 |
| T2 | KL1 gate, DES Y3 polished g | `polish` group, GATE | 0.15 |
| T3 | KL1 gate, KiDS-Legacy g | `legacy` group, GATE | 0.05 |
| T4 | BX1 gate, DES Y3 polished g | `polish` group, GATE_BX1 | 0.15 |
| T5 | BX1 gate, KiDS-Legacy g | `legacy` group, GATE_BX1 | 0.05 |
| T6 | LWB1 J g | `lwb1` primary | 0.02 |
| T7 | LWB1R J g | `lwb1r` primary | 0.02 |

Floors: T2 / T4 0.15 is WLJ1's observed case-to-case scatter of the polished DES scan (0.05 to 0.15 widths); T3 / T5
0.05 and T1 0.02 are about 3 times the smallest layout effect WLJ1 resolved smoothly on those statistics (split against
REF: +0.05 / +0.11 on T1 and T3); T6 / T7 0.02 is twice LWB1R's case-to-case scatter (0.01).

Per graded case and footing, Delta_i = T_i(case) - T_i(REF):
- a statistic is **used** if (a) the known answers guarding its gate pass on that footing (WLJ1's and KA-X2 below), and
  (b) TW-L at Ec2 bites on it (|T_TWL - T_Ec2| >= 0.5 |T_Ec2 - T_REF|) or it is unseen (|T_Ec2 - T_REF| <= delta_i);
- **RELIEVES** if some used Delta_i < -delta_i and no used Delta_i > +delta_i;
- **WORSENS** if some used Delta_i > +delta_i and no used Delta_i < -delta_i;
- **LEAVES UNCHANGED** if every used |Delta_i| <= delta_i;
- **NOT RESOLVED (mixed)** if both directions appear; **NO VERDICT** if no statistic is used or TW-B does not bite.
- Beside it, reported: every Delta_i, and each gate's own word (TENSION / EXCLUDED, GAP STAYS / CONSISTENT, J label)
  against REF's.

**Row 25 summary word per footing:** the common word of Ec3, Ec2, E0.5, E0.75, E1 if all five share it; otherwise "NOT
RESOLVED (the word depends on the radius)" with each case's word. E2, S2 and ADOPT are put through the same rule and
reported. **Known answer of the rule, KA-W:** ADOPT must read WORSENS on each footing (WLJ1: T1 +0.21 / +0.37, T3 +0.23 /
+0.38) or that footing's row-25 summary word is NO VERDICT. A RELIEVES is a hit awaiting a blind re-grade. A WORSENS or a
LEAVES UNCHANGED is verified as hard: its known answers, twins and brackets are printed beside it.

## 5. Known answers (a failing one makes every label on what it guards NO VERDICT on that footing)

- **WLJ1's own**, unchanged in substance: KA-H1 (ADOPT vs CO1's stored ratios 1e-8), KA-H2 (nulls 1e-12), KA-H3 (S2 at z
  2.2 / 4.4 vs JNT2's stored, 1e-9), KA-H4 (every layout of this lane, twins and brackets included, conserves M_ta to
  1e-9 and is non-decreasing at z 0, 0.5, 1), KA-H5, KA-H6, KA-G1 to KA-G8 and KA-R with A1's 1e-12 and A2's DES rule.
- **KA-X1 (WLJ1 reproduced, halo model):** REF, ADOPT and S2 at z 0 to 3, the own list and the seven brackets equal
  WLJ1's stored `wlj1_hm.json` arrays (R_tot, R_bar, R_cold) to 1e-10 relative; S2's f_res equals WLJ1's to 1e-10.
- **KA-X2 (WLJ1 reproduced, gates), per gate and footing:** REF, ADOPT and S2 through this lane's scripts against WLJ1's
  stored files: C4 r_eff to 1e-9 and shape chi^2 to 1e-6; C5 d_cold, the robust variants, chi^2 and the tooth to 1e-4;
  HLF1 own-list d_cold to 1e-4; P4 chi^2 to 1e-4 and T1 to 1e-3; KL1 / BX1 Legacy and polished DES gap and chi^2 to
  0.01 (WLJ1's own KA-G5 tolerance, for the reason of its A2); deskids rows reported; LWB1 / LWB1R J best sigma8 to
  0.0005 and gap to 0.01 (WLJ1's KA-G7 / G8 tolerance).
- **KA-L (the layout copy):** with no options, this lane's E layout equals XJ1's `exact_fn` row for row (same r grid,
  max |M difference| = 0) for every halo at z 0, 0.5, 1 and 2.2, every case, both footings.
- **KA-E (XJ1's, at this lane's redshifts z 0, 0.5, 1, 1.5, 2, 2.5, 3, every case, every slow halo):** (i) M_E = M_B for
  r <= R_set to 1e-12; (ii) M_E(r_ta) = M_ta to 1e-9; (iii) non-decreasing to 1e-9 M_ta; (iv) t >= -1e-12 (XJ1's A1);
  (vi) every halo above v*(z) carries "Rb" exactly.
- **KA-E0 (the null):** an E case with R_set sent to 0 (mult 0) gives |R_cold - 1| <= 1e-12 at z 0; with R_set forced to
  r_ta and no boundary it equals ADOPT to 1e-12.
- **KA-XJ (XJ1 reproduced where it overlaps):** (a) this lane's R_cold for E1, E2, E0.5, E0.75, Ec2, Ec3 at z 2.2, 3.0,
  4.4, interpolated at k 1, 3, 5, 10 h/Mpc, equals XJ1's stored `R_cold_at_k1_3_5_10` (`xj1_matter{,2,3}_<footing>.json`)
  to 1e-9 relative; (b) the per-(z, footing) t min / max, s min / max and R_set / R_fold min / median / max over the slow
  haloes at z 2.2, 3.0, 4.4 equal XJ1's stored `surfaces` (`xj1_ka_tables{,2,3}.json`) to 1e-9 relative.
- **KA-V:** JNT2's `vstar_kms` equals FWN1R's `vstar` to 1e-12 relative at z 0, 0.5, ..., 3 on both footings.
- **KA-Z0:** at z 0 to 3 no table mass has R_2 or R_3 equal to 0 (else the count is printed and the case is NO VERDICT
  at that node's bracket only; the primary is z 0).
- KA-H4, KA-E and KA-E0 guard every E label; KA-X1 / KA-X2 guard the comparison with WLJ1 and the controls' words; KA-XJ
  guards the claim that this lane's layout is XJ1's.

## 6. Twins (each must bite; WLJ1's rules with Ec2 in the place of S2)

- **TW-B (boundary 2 v*, at Ec2):** bites if at z 0 on both footings fewer grid haloes take "Rb" than in Ec2 and
  |R_cold,TW-B(k 3) - 1| >= 1.2 |R_cold,Ec2(k 3) - 1|. If it does not bite, every E label is NO VERDICT (and so is the
  row-25 word).
- **TW-L (layout change doubled, at Ec2):** bites on a gate if |s_TWL - s_Ec2| >= 0.5 |s_Ec2 - s_REF|; a gate on which it
  does not bite reads NO VERDICT for every E case unless s_Ec2 equals s_REF to the gate's floor (C5, P4, g: 0.002; C4
  1e-9), in which case the gate is reported as unable to see the layout (EQUALS THE REFERENCE THERE).

## 7. Reported (never a label)

Power-ratio table (R_cold and R_tot at k 0.1, 0.3, 1, 3, 10 h/Mpc at z 0, 0.5, 1 per case and footing); haloes on "Rb";
per case and z the t and s ranges, the share of R_set capped at r_ta, R_set / R_fold (min, median, max); f_res; the
unsplit-free comparison with S2 (record's junction at 2 R_fold) and E2 (exact junction at 2 R_fold), which isolates the
junction's own effect at the same radius.

## 8. Hand estimate (before any number; low confidence)

At z 0 the caustics sit at 0.54 and 0.68 R_fold, about 0.28 and 0.35 r_ta. Inside, the law's halo unscaled; XJ1's lens
chain gave s 0.57 to 0.93 at z 0 for galaxies (the law holds more cold mass inside than the reference), so the exact
junction keeps more central cold mass than the record's junction at the same radius, and puts less (t < 1) outside.
Guess for R_cold - 1 at z 0, k 3: Ec3 +0.015 / +0.03, Ec2 +0.02 / +0.035, E1 +0.025 / +0.04 (canonical / alt), between
S2 (+0.0135 / +0.029) and the full law in slow haloes (+0.030 / +0.056); k 10 above 1.05. E2 close to f infinity (cap).
- Row 24: C4 PASS (|r_eff - 1| ~1e-5), C5 d_cold +0.3 to +0.9 / +0.6 to +1.5 CONSISTENT, HLF1 holds; ROW HOLDS for every
  graded case (85 %), mostly EQUALS THE REFERENCE THERE on C4; HLF1 NOT RESOLVED somewhere (f_res < 0.5) 15 %.
- Row 25, per gate: P4 p near 0.0027 (REF 0.00315); E cases cross into EXCLUDED at 3 sigma for E1 / E2 and maybe Ec2
  (50 %); KL1 GAP STAYS on DES for every case (REF included) and TW-L does not bite on KL1 (70 %), so KL1 NO VERDICT;
  BX1 canonical CONSISTENT, alt NO VERDICT (WLJ1's KA-G6 carries over, 90 %); LWB J CONSISTENT, EQUALS THE REFERENCE
  THERE. Row 25 per case: FAILS (P4 EXCLUDED) or NO VERDICT; not HOLDS (95 %).
- Row 25 summary word: **WORSENS** on both footings (60 %): T1 +0.05 to +0.2 widths, T3 +0.05 to +0.2; LEAVES UNCHANGED
  (20 %) if every Delta is under its floor at the caustics; NOT RESOLVED by radius or mixed (12 %); RELIEVES (8 %).
  The amplitude tension, 5.4 widths, is not something a layout below v* can remove: expected |Delta T1| < 0.3.
- Twins: TW-B bites (75 %: 2 v* hands groups and clusters to the exact junction, whose inner radius keeps much of the
  law's cluster excess); TW-L bites on C4, C5, P4, LWB1R, not on KL1.

## 9. Compute and files

Memory under 6 GB, one process at a time, one thread, `nice -n 19`, `python3 -I -B`; before each stage `df -g .` and
`sysctl -n vm.swapusage` (no start under 10 GB free disk or over 12 GB swap used; stop under 8 GB). Long stages run in
the background and are waited on by process id or marker file, never `pgrep -f`. No web, no download. Nothing written
outside this folder; XJ1's and WLJ1's folders are read-only and XJ1's `parts_*`, `tmp_a` and `logs` are not read. The
KiDS-Legacy release (untrusted data) is passed as an argument.

Scripts (copies of WLJ1's, cited, with only the case list, the layout, the twin case and the words changed, plus the
known answers above): `wlj2_hm.py`, `wlj2_c4.py`, `wlj2_shear.py`, `wlj2_kl1bx1.py`, `wlj2_lwb.py`, `wlj2_grade.py`, with
`*_MUTATE` outputs for the twins. Order of stages: hm, c4, shear, lwb1r, lwb1, kl1bx1 (per footing: legacy, polish,
then deskids), grade. If a long stage cannot finish, what exists is committed and what is missing is said.
Commits: this file alone; then scripts with outputs; then RESULT.md. Any later change is a dated AMENDMENT_A#.md
committed alone before the numbers it governs are read; the as-frozen reading is reported first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
