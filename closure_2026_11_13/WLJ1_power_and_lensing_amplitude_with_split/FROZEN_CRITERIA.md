# WLJ1 FROZEN CRITERIA: the matter-power redistribution rows (24) and the weak-lensing amplitude rows (25), computed with the crossing-speed split

Committed alone, before any WLJ1 script exists and before any number for the split is computed. TEST lane: adopts nothing,
relabels nothing, registers nothing. Not a blind lane. Footings canonical (a0 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2),
graded separately, never pooled. Cold dark energy is a gravitating field component, never a particle. kappa = 1/2 and the
share 5.41 are FITTED. No outcome here is read as the data favouring the framework. Light compute: one thread, `nice -n 10`,
`python3 -I -B`, under 6 GB. No download. Nothing outside this folder is written; every other lane's code is executed
read-only from its own path or copied with the source named.

## 0. What is graded and what was seen before this freeze

`closure_2026_11_13/CJ1_candidate_completion/SCORECARD.md` lines 62-63 mark row 24 (matter-power redistribution: CO1, HLF1)
and row 25 (weak-lensing amplitude: CO2, KL1, BX1, LWB1, LWB1R) NOT GRADED FOR THIS FORM, "Not computed with the v* split".
This lane computes them with rule 6 of `COMPLETED_FORM.md` (the crossing-speed joint).

Seen before this freeze (no WLJ1 number exists): CJ1's COMPLETED_FORM and SCORECARD; the criteria, amendments and results of
CO1, HLF1, CO2, KL1 (Parts A to C, amendments C1 to C3), BX1 (A1), LWB1 (A1), LWB1R (READING, RESULT); the scripts
`co1_shear.py`, `co1_linear.py`, `co2_shear.py`, `hlf1_hm.py`, `kl1c.py`, `kl1c_polish.py` (head), `kl1c_gas.py` (head),
`bx1_regrade.py`, `lwb1.py`, `lwb1r.py`; JNT2's `jnt2_common.py`, `jnt2_hm.py` and `jnt2_hm.out`; FZS1's `fzs1_hm.py`;
FRZ1's `frz1_hm.py` library part; CFG592's `Pmat`. All of those lanes' numbers for the adopted form and the reference are
known to me (quoted in section 2). No ratio, spectrum or gate number for the split at z <= 3 has been computed by anyone.

## 1. The three cases (all at the same parameters, same halo list, same baryons)

Machinery: FZS1's `fzs1_hm.py` executed read-only from its own path up to its "checkpointed run" marker, as JNT2's
`jnt2_hm.py` does (it executes FRZ1's `frz1_hm.py` library: CFG556's halo model re-evaluated at z, CO1's layout made z-aware,
FLD1's R_fold). Spectra and ratios exactly as JNT2's `ratios_J`: R_tot = 1 + (P_case - P_Lta) / P_std, R_bar = 1 + (P_Rb -
P_Lta) / P_std, R_cold = R_tot / R_bar.

- **REF, the pure reference:** every halo in FRZ1's layout "Rb" (the cold reference, same baryons). R_tot = R_bar, R_cold = 1.
- **ADOPT, the adopted form, no split:** every halo in FRZ1's layout "B" at every radius (R_set = r_ta, no boundary). At z = 0
  this is CO1's primary layout, the one CO1, HLF1, CO2, KL1, BX1, LWB1 and LWB1R graded (FZS1's KA-Z0 showed equality to 1e-10).
- **SPLIT at f:** JNT2's `lay_J` copied (cited): a halo whose FRZ1 `v_vir` (its v200c) exceeds v*(z) = v*(0) / E(z),
  v*(0) = a0 / (10 (1 + 5.41) H0) = 668.5 / 807.9 km/s (`jnt2_common.vstar_kms`), takes "Rb" at every radius; a slower halo
  takes "B" inside R_set = f R_fold (FZS1's `rset_com`, FLD1's fold radius, capped at r_ta) and "Rb" beyond, the cold mass at
  R_set conserved (FZS1's junction). f = 1.25, 2, 3 graded; f = infinity in slow haloes (R_set = r_ta) reported only.
- Reported only, not graded: UNSPLIT at f (FZS1's settled family, no boundary) at f = 1.25, 2, 3, to show what the boundary
  alone does.

**Redshift.** Every gate below takes a ratio R(k) held in z (CO1 section 3 line 66: "Held in z: the z = 0 ratios are used at
every z"; LWB1 and LWB1R read CO1's stored R_tot(k)). **Primary, for every case: the case's own z = 0 ratio held in z**, so the
gates run unchanged. The split is z-dependent, so a frozen z bracket (section 5) feeds each case's own ratio at z: at the
CFG592 nodes z = 0, 0.5, 1 for C5 and P4 (each node's spectrum multiplied by that node's R; above z 1 the z = 1 node's
growth-scaled spectrum, as CFG592's `Pmat` does), and on z = 0, 0.5, 1, 1.5, 2, 2.5, 3 (linear in z between them) for C4.
KL1, BX1, LWB1 and LWB1R are run held only; their z bracket is left out and said so.

**Power-ratio table (reported):** R_cold (the case's nonlinear matter power over the reference's) and R_tot at k = 0.1, 0.3,
1, 3, 10 h/Mpc at z = 0, 0.5, 1, per case and footing; the switch speed v*(z), the lightest M200c above it on the grid and the
analytic M200c at v*(z) (10 G M H(z) = v*^3); the number of grid haloes on the reference layout.

## 2. The gates, as the record froze them (quoted; file and line)

**Row 24.**
- **G-C4, CO1 C4** (`closure_2026_11_09/CO1_form_b_cosmology_computed/FROZEN_CRITERIA.md` lines 76-79): "S(L) = [integral of
  w(z)^2 P_lin((L + 1/2) / chi, z) R_cold(k) over z <= 3 ...] / [the integral without R] ... r_eff = A(X) / A(S X). Lines:
  |r_eff - 1| <= 2 sigma_A,rel (C2's) and the shape chi^2 of S X <= 18.48." Code: `co1_linear.py` `limber_setup`, `S_of`,
  `amp_fit`, `c4` (copied, cited); CLASS at CO1's stored C1 parameters (`co1_linear.json`); PR4 bandpowers through QX3 iter2.
  Adopted form: r_eff - 1 = +0.00003 / +0.00005, PASS.
- **G-C5, CO1 C5** (same file, lines 81-90): "d_cold = chi^2(S0 x R_tot) - chi^2(S0 x R_bar). Robustness set as CFG596:
  widen2, noIA, fade, DESI distances. Label by klass(d_cold, robust, N_kept >= 10): EXCLUDED (d >= 9 and every robust variant
  >= 9), TENSION (d >= 4), CONSISTENT (d < 4 and every robust variant < 9), otherwise NOT DIAGNOSTIC." Tooth: "VISIBLE ... if
  that chi^2_min >= 9". Code: `co1_shear.py`'s `grade` (copied, cited), CFG592's library executed unchanged, CFG596's S0 run.
  Adopted form: +1.15 / +2.21 CONSISTENT. CO1's lane rule (lines 94-98): ROWS HOLD if C1 to C4 PASS and C5 CONSISTENT; C1 to
  C3 are the linear rows, untouched by any layout (the split changes only the 1-halo layout), carried from CO1 / CO2 as PASS.
- **G-HLF1, HLF1 Part A** (`closure_2026_11_10/HLF1_own_halo_list_forest/FROZEN_CRITERIA.md` lines 76-92): CO1's rows with
  the own list (Tinker 2008 x r_j and Tinker 2010 x the bin's bias ratio inside [1e13, 5.62e14] Msun/h, `hlf1_halos.json`)
  against the inherited list; "NOT RESOLVED: f_res < 0.5 at k = 1 ..."; "ROWS MOVE (row, size): ... if the own list changes
  the C4 status or the C5 klass label or the CO1 lane label against the inherited run"; "ROWS HOLD WITH THE OWN LIST:
  otherwise". f_res by lines 76-78 (per grid point d_i at k = 1, 1-halo plus 2-halo, as `hlf1_hm.py`'s A.2 code, copied).
  The own list enters FRZ1's z = 0 population by HLF1's `own_factors` rule (W_M x fw, BIAS x fb, A_MISS and NORM_TA
  recomputed). Adopted form: ROWS HOLD WITH THE OWN LIST (under HLF1's A1; NO VERDICT as frozen, MA1).
- **HLF1 Part B (the forest row)** is the forest at matter level with R(k, z); for the split it is row 21, computed by JNT2 and
  JNT2R. It is not recomputed here; RESULT.md quotes JNT2's committed word.

**Row 25.**
- **G-P4, CO2 P4** (`closure_2026_11_09/CO2_form_b_amplitude_pinned/FROZEN_CRITERIA.md` lines 41-51, labels 57-62): S0 x R_tot
  moved to the pinned sigma8 0.8271 by the run's own response; "Lines: p >= 0.05 CONSISTENT; 0.0027 <= p < 0.05 TENSION;
  p < 0.0027 EXCLUDED AT 3 SIGMA". Code: `co2_shear.py` (copied, cited). Adopted form: chi^2 157.89 / 159.35, p 0.0026 /
  0.0021, EXCLUDED AT 3 SIGMA.
- **G-KL1, KL1 Part C gate** (`closure_2026_11_10/KL1_lensing_amplitude_survey_assumptions/FROZEN_CRITERIA_PARTC.md` lines
  111-131; AMENDMENT C3's polished DES scan; AMENDMENTS C1 + C2 + C3 are the reading the scorecard carries): GATE = C0 (R1) +
  C2 (A3_AD) at the neutrino-floor sigma8, covariance at the model (gamma 2); per survey CONSISTENT if |g| <= 2 and p >= 0.05,
  GAP STAYS if g > 2, OVERSHOOT if g < -2, POOR FIT if |g| <= 2 and p < 0.05; overall on KiDS-Legacy (frozen scan; C3b re-reads
  it if outside CONSISTENT) and DES Y3 (polished scan). Code: `kl1c.py` up to its "rows (frozen order)" marker and
  `kl1c_polish.py` up to `RES = dict(`, executed read-only from their own path, as BX1's `bx1_regrade.py` does. Adopted form:
  Legacy +1.71 / +1.88 CONSISTENT, DES polished +2.18 / +2.23 GAP STAYS -> GAP STAYS.
- **G-BX1, BX1 gate** (`closure_2026_11_10/BX1_fixed_amplitude_reference/FROZEN_CRITERIA.md` lines 99-107): KL1's gate with
  BX1's 512^3 pair-A splice (`bx1_splice_pairA_N512.json` through KL1's `load200`); same per-survey and overall rules.
  Adopted form: Legacy +1.51 / +1.72, DES polished +1.85 / +1.83, AMPLITUDE CONSISTENT (A1 interim reading).
- **G-LWB1, LWB1 J** (`closure_2026_11_12/LWB1_lensing_amplitude_crosscheck/FROZEN_CRITERIA.md` lines 66-78): "NO VERDICT if
  the best fit has p < 0.01 ... or if the label of J changes between pi_max 40, 80 and 100"; "NO POWER if width > 0.05";
  "AMPLITUDE CONSISTENT if -2 <= g <= 2; GAP STAYS if 2 < g <= 3; TENSION if g > 3 or g < -2". Code: `lwb1.py` up to its
  "primary and brackets" marker, executed read-only from its own path, its `HM` (CO1's stored R_tot) replaced by the case's.
  Adopted form: J +0.90 / +0.87 AMPLITUDE CONSISTENT, FRAGILE.
- **G-LWB1R, LWB1R J** (`closure_2026_11_12/LWB1R_blind_lensing_regrade/READING.md`, the same frozen lines): `lwb1r.py`
  executed read-only from its own path without its `main()` call, its `CO1` replaced by the case's; `main()`'s inner
  `proj_set` / `tmpl` / `fit_all` copied (cited). Adopted form: J +0.91 / +0.87 AMPLITUDE CONSISTENT, FRAGILE.

**How KL1's and BX1's R enters (frozen transfer rule).** Their gate R is A3_AD (`kl1c_gas.json`: CO1's layout with RB1's gas
moved and the cold component's adiabatic response), not CO1's R_tot. The split is not rebuilt with RB1's gas. Primary: the
gate's R for a case is A3_AD(k) x [R_tot,case(k) / R_tot,ADOPT(k)] (z = 0, held). ADOPT therefore reproduces the gate exactly
(known answer). Bracket: additive, A3_AD + (R_tot,case - R_tot,ADOPT). The fiducial covariance context of `make_ctx` keeps
CO1's R_tot, as the gate froze it.

## 3. Labels (per gate, per f, per footing)

Gate words map to this lane's words:
- **ROW HOLDS WITH THE SPLIT:** C4 PASS; C5 CONSISTENT; CO1 rule ROWS HOLD; HLF1 ROWS HOLD WITH THE OWN LIST; P4 CONSISTENT;
  KL1 / BX1 AMPLITUDE CONSISTENT; LWB1 / LWB1R J AMPLITUDE CONSISTENT.
- **ROW FAILS WITH THE SPLIT:** C4 FAIL; C5 EXCLUDED; HLF1 ROWS MOVE to a worse CO1 label; P4 EXCLUDED AT 3 SIGMA; KL1 / BX1
  GAP STAYS, OVERSHOOT or POOR FIT; LWB1 / LWB1R J GAP STAYS or TENSION.
- **NO VERDICT:** C5 TENSION or NOT DIAGNOSTIC; P4 TENSION; HLF1 NOT RESOLVED; LWB J NO POWER or a label change across pi_max
  40 / 80 / 100 or p < 0.01; any of this lane's known answers guarding the gate fails; a twin guarding it does not bite. The
  gate's own word is printed in brackets beside it (e.g. "NO VERDICT [TENSION]").
- **FRAGILE (bracket named)** when a frozen bracket of section 5 gives a different word from the primary.
- **EQUALS THE REFERENCE THERE** (printed with the held word) when the split's word equals REF's word on that gate, and
  |s_SPLIT - s_REF| <= |s_SPLIT - s_ADOPT|, and |s_SPLIT - s_REF| <= 0.25 x D, where s is the gate statistic (C4 |r_eff - 1|;
  C5 d_cold; HLF1 own-list d_cold; P4 chi^2; KL1 / BX1 the larger of Legacy's and DES's g; LWB J g) and D is the distance from
  s_REF to the gate's nearest line (C4 0.0481; C5 4; P4 the chi^2 at p 0.0027 and 0.05 for N = 104; KL1 / BX1 / LWB +-2). D is
  reported as the size of change the gate could have seen.
- Beside each word: whether it differs from ADOPT's word on the same gate (computed here by the same pipeline). **A HOLDS that
  differs from ADOPT's word is a hit that needs an independent blind re-grade, and is reported as that, not as a pass.** A fail
  is verified as hard as a hold (its known answers, twins and brackets all printed).
- **Lane-as-frozen notes.** Several lanes read NO VERDICT as frozen for causes that do not depend on the layout (CO1 M4 as
  written; HLF1 MA1; KL1 MC1 and MA2; BX1 KA3 and MB2; LWB1 KA1). The same cause applies to all three cases; it is printed beside
  the word as "[lane as frozen: NO VERDICT, cause independent of the layout]" and does not change this lane's word.
- **Row word (per f, footing):** ROW FAILS WITH THE SPLIT if any gate of the row fails; ROW HOLDS WITH THE SPLIT if every gate
  holds; NO VERDICT otherwise. ADOPT's row word is computed by the same rule.
- f = infinity and UNSPLIT are labelled the same way and reported, never graded.

## 4. Known answers (tolerances; a failing one makes every label on the gates it guards NO VERDICT)

- **KA-H1:** ADOPT at z = 0 through the copied machinery against CO1's stored `co1_hm.json` primary R_tot, R_bar, R_cold: max
  relative difference <= 1e-8 per footing.
- **KA-H2 (nulls):** SPLIT with the boundary at infinity and f = infinity equals ADOPT (<= 1e-12); SPLIT with every halo above
  the boundary equals REF (|R_cold - 1| <= 1e-12).
- **KA-H3 (JNT2 reproduced):** SPLIT at f = 2 at z 2.2 and 4.4 against JNT2's stored `jnt2_hm.json` "f2.00|<footing>" R_cold:
  <= 1e-9 relative.
- **KA-H4:** every SPLIT, twin and bracket layout at z = 0, 0.5 and 1 conserves M_ta (<= 1e-9) and is non-decreasing.
- **KA-H5:** ADOPT with HLF1's own list against HLF1's stored `hlf1_hm_own.json` primary R_tot: <= 1e-8.
- **KA-H6 (brackets reproduced, per bracket, not gating the primary):** ADOPT under each layout bracket against CO1's stored
  bracket R_tot: <= 1e-6. A bracket that fails is printed NOT REPRODUCED and not used.
- **KA-G1:** ADOPT through the copied C5 grade reproduces CO1's stored C5 (d_cold, the four robust variants, chi^2 S0 / R_bar /
  R_tot, the tooth) to 0.005, and CFG596's S0 rows (KiDS 104, 144.26; DES 52, 68.64) to 0.01.
- **KA-G2:** ADOPT r_eff and shape chi^2 in C4 against CO1's stored values: 1e-6 and 1e-3.
- **KA-G3:** ADOPT P4 chi^2 (response and constant factor) and CO2's brackets against `co2_shear.json`: 0.01.
- **KA-G4:** ADOPT with the own list through C4 and C5 against HLF1's stored `hlf1_rows_own.json` / `hlf1_shear_own.json`:
  d_cold and robust to 0.005, r_eff to 1e-6.
- **KA-G5:** ADOPT through KL1's gate reproduces KL1's stored Part C GATE rows (`parts/partc_<footing>_<group>.json`, Legacy,
  DES, KiDS-1000, and C3b on Legacy) and the polished DES GATE (`parts/polish_<footing>.json`): gap and chi^2 at the target to
  0.01.
- **KA-G6:** ADOPT through BX1's gate reproduces BX1's stored GATE_BX1 and C3b_BX1 rows (`parts/bx1_<footing>_<group>.json`,
  polished DES included): 0.01.
- **KA-G7 / KA-G8:** ADOPT reproduces LWB1's stored primary (five vectors) and pi_max 80 / 100 J rows (`lwb1.json`), and
  LWB1R's stored primary J (`lwb1r.json`): best sigma8 to 0.0005 and gap to 0.01.
- **KA-R:** REF gives d_cold = 0 and r_eff = 1 exactly.

## 5. Brackets (reported; a bracket that flips the split's word makes it FRAGILE with that bracket named)

Run on REF, ADOPT and SPLIT. On C5 and P4 at every graded f; on KL1, BX1, LWB1 and LWB1R at f = 2 only (the cost of a full scan),
which is said beside every f = 1.25 and 3 word on those gates.
- **z bracket** (section 1): C5 and P4 at the nodes; C4 with R(k, z) to z 3. C4 applied at z <= 1 only, reported.
- **CO1's layout brackets** (CO1 criteria line 103-106), through FRZ1's layout options: core prefactor 1 and 0; galaxy rule in
  the virial scope; gas core 0.2 R200c; Press-Schechter with Mo-White bias; c(M) x 0.7 and x 1.3 -> C5 d_cold. CO1's KiDS
  amplitude bracket (S0 scaled by (sigma8 of C3 / 0.811)^2) -> C5. Not available in FRZ1's layout, left out and said so:
  the regime boundary at M200m 1e13 and CFG556's kernel.
- **CO2's brackets:** one 0.06 eV neutrino (sigma8 0.8152); the case's own prefactor-0 layout; CO1's unpinned sigma8 (response);
  the constant factor.
- **KL1:** C3b on Legacy (part of the reading); C0's edges R2 and R2b (frozen scans). **BX1:** C3b_BX1. Both: the additive
  transfer rule.
- **LWB1:** pi_max 80, 100 (gating), 300; point-mass term; R_min 5 and 12; no magnification column; wp correlation 0.5; N = 1.
  The CAMB halofit bracket is left out. **LWB1R:** pi_max 80, 100 (gating); point-mass term; R_min 5 and 12.
- BX1's splice-noise tag uses BX1's stored sigma_g (layout-independent), not recomputed.

## 6. Mutation twins (separate `_MUTATE` outputs; each must bite)

- **TW-B (boundary at 2 v*(z)), at f = 2:** bites if, at z = 0 on both footings, (a) fewer grid haloes take the reference layout
  than in SPLIT f = 2, and (b) |R_cold,TW-B(k 3) - 1| >= 1.2 |R_cold,SPLIT(k 3) - 1|. If it does not bite, every SPLIT label is
  NO VERDICT.
- **TW-L (the layout change doubled), at f = 2:** R_cold' = 1 + 2 (R_cold,SPLIT - 1), R_tot' = R_bar R_cold'. Bites on a gate if
  |s_TW-L - s_SPLIT| >= 0.5 |s_SPLIT - s_REF| for that gate's statistic (C5 d_cold on KiDS, P4 chi^2, C4 |r_eff - 1|, and on
  KL1 / BX1 / LWB1 / LWB1R their g), on both footings. A gate on which it does not bite reads NO VERDICT for the SPLIT, unless
  s_SPLIT equals s_REF to the gate's numerical floor (C5 and P4: 0.002 in chi^2; g: 0.002), in which case the gate is reported
  as unable to see the layout at all (EQUALS THE REFERENCE THERE, with D).

## 7. Hand estimate (before any code; unverified)

- Switch mass at z = 0: v*(0)^3 = 10 G M H0 gives M200c 1.03e14 / 1.82e14 Msun (6.9e13 / 1.2e14 Msun/h); at z 0.5 about
  3.4e13 / 6e13 Msun; at z 1 about 1.0e13 / 1.8e13 Msun. So today only clusters and the richest groups take the reference;
  groups between v_stiff and v* keep CO1's cluster rule, whose change sits inside R200c, well inside f R_fold for f >= 1.25.
- Ratios at z = 0: the clusters above v* carry most of ADOPT's k = 1 signal. Expected R_cold - 1 at k 1 about 0.002 / 0.004
  (ADOPT 0.006 / 0.010), at k 3 about 0.03 / 0.06 (ADOPT 0.051 / 0.088), nearly the same for f = 1.25, 2, 3 and infinity
  (galaxies hold their dust inside 0.25 to 0.5 r_ta and R_fold is about 0.52 r_ta). At z 0.5 and 1 smaller still (more haloes
  above v*). At k 0.1 and 0.3: 1 to 1e-3.
- C4: |r_eff - 1| about 1e-5, PASS for all cases. C5: d_cold about +0.4 / +1.0, CONSISTENT. HLF1: ROWS HOLD WITH THE OWN LIST.
  Row 24 HOLDS with the split as for ADOPT, and EQUALS THE REFERENCE THERE on C4 and probably on C5.
- P4: chi^2 between REF's 156.18 / 156.16 and ADOPT's 157.89 / 159.35, about 156.8 / 157.6, so p about 0.003: TENSION on both
  footings, where ADOPT reads EXCLUDED AT 3 SIGMA (p 0.0026 / 0.0021). If so the split's word (NO VERDICT [TENSION]) differs from
  ADOPT's (FAILS) only because ADOPT sat 0.0001 to 0.0006 in p under the line; FRAGILE expected (the nodes bracket moves it
  further toward REF; CO2's own realisation corrections already put ADOPT at TENSION). The robust statement, KiDS's best sigma8
  about 5.5 widths below the pinned value, will not move by more than about 0.1 width.
- KL1 and BX1: g shifts by -0.02 to -0.1 widths; words unchanged (KL1 GAP STAYS on DES, so FAILS; BX1 CONSISTENT, so HOLDS).
  LWB1 / LWB1R: shifts below 0.01 widths at R >= 8 h^-1 Mpc; EQUALS THE REFERENCE THERE, J CONSISTENT, FRAGILE as for ADOPT.
- Row 25 word: FAILS with the split (KL1's DES), as for ADOPT. The split does not touch the weak-lensing amplitude tension
  that any cold component fitted to the CMB carries.
- Twins: TW-B bites (2 v* hands most clusters back to the law's layout); TW-L bites on C5 and P4, and may fail to bite where the
  gate sees nothing (LWB), which the rule above reports as EQUALS THE REFERENCE THERE.

## 8. Files and commits

`wlj1_hm.py` (ratios, known answers H, twins, brackets) -> `wlj1_hm.json/.out`, `wlj1_hm_MUTATE.json/.out`; `wlj1_c4.py` ->
`wlj1_c4.json/.out`; `wlj1_shear.py` (C5, HLF1 Part A, P4) -> `wlj1_shear.json/.out`; `wlj1_kl1bx1.py <footing> <group>` ->
`parts/wlj1_kl1bx1_<footing>_<group>.json/.out`; `wlj1_lwb.py` -> `wlj1_lwb.json/.out`; `wlj1_grade.py` -> `wlj1_grade.json/.out`;
twins in the same scripts write `*_MUTATE*` outputs. Commit order: this file alone; scripts and outputs; RESULT.md last.
Any change after this freeze is a dated amendment committed alone, the as-frozen reading reported first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
