#!/usr/bin/env python3
"""PAPER72 audit: each quoted number appears in the TeX and, as the literal given, in the committed lane file named beside it
(working tree, HEAD or origin/main: the shared checkout has diverged, and PD1 / PD2 are committed on origin only); a few graded
numbers are also read from the lane's JSON and rounded; the two numbers that are the paper's own arithmetic (w0's coefficient and
the recombination bound on mu_K) are recomputed here from QX17's FRW formula; naming rules; no local paths; no pending placeholder.
Version 1.1 adds the lanes of 2026-11-10 (fable52_push/, closure_2026_11_10/), the two notes of that day and the older lanes quoted by
Section 7, and makes "committed" stricter: a source's working-tree copy must equal a committed copy (PAPER72's own files excepted).
Run: python3 PAPER72_audit.py (exit 0 only if all pass).
--mutate changes one digit of each source literal (and of each TeX number in the JSON and arithmetic checks); exit 0 only if
every mutated literal then fails.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os, re, subprocess, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEX = open(os.path.join(HERE, "PAPER72_law_with_cold_dark_energy_counted_once_2026.tex"), encoding="utf-8").read()
C = "closure_2026_11_09/"; F = "fable52_push/"; P = "qwen_claude_field_theory/papers_2026/"
DEC = C + "OWNER_DECISION_2026-11-09_FINAL_FORM_B.md"
PD1 = C + "PD1_phantom_is_dust/RESULT.md"; PD1o = C + "PD1_phantom_is_dust/pd1.out"
PD1b = C + "PD1_phantom_is_dust/pd1_a1_share5.41_fcpre1.0.out"; PD1a2 = C + "PD1_phantom_is_dust/pd1_a2.out"
PD2 = C + "PD2_sheet_captured_phantom_dust/RESULT.md"
RB1 = C + "RB1_form_b_hot_systems/RESULT.md"; RB1o = C + "RB1_form_b_hot_systems/rb1.out"; RB1j = C + "RB1_form_b_hot_systems/rb1.json"
RB2 = C + "RB2_form_b_hosted_rows/RESULT.md"; RB2o = C + "RB2_form_b_hosted_rows/rb2.out"
KO2 = C + "KO2_kids_own_field_by_type/RESULT.md"; KO2o = C + "KO2_kids_own_field_by_type/ko2.out"
KO2b = C + "KO2_kids_own_field_by_type/ko2_formB.out"; KO2j = C + "KO2_kids_own_field_by_type/ko2.json"
KO2c = C + "KO2_kids_own_field_by_type/FROZEN_CRITERIA.md"; KO2a4 = C + "KO2_kids_own_field_by_type/AMENDMENT_A4.md"
ONEn = F + "ONE1_counted_once/PREFREEZE_NOTE.md"; ONEo = F + "ONE1_counted_once/one1_prefreeze_look.out"
ONE = F + "ONE1_counted_once/RESULT.md"; ONEk = F + "ONE1_counted_once/one1_kids.out"
HE1 = F + "HE1_held_out_envelope/RESULT.md"
FB1 = F + "FB1_form_b_from_the_action/NOTE.md"; FB1o = F + "FB1_form_b_from_the_action/fb1_check.out"
QX17 = "closure_2026_11_06/QX17_covariant_field_equations/RESULT.md"
CO1 = C + "CO1_form_b_cosmology_computed/RESULT.md"; CO1o = C + "CO1_form_b_cosmology_computed/co1.out"
CO1j = C + "CO1_form_b_cosmology_computed/co1.json"
CO2c = C + "CO2_form_b_amplitude_pinned/FROZEN_CRITERIA.md"; CO2a = C + "CO2_form_b_amplitude_pinned/AMENDMENT_A1.md"
CO2o = C + "CO2_form_b_amplitude_pinned/co2.out"; CO2j = C + "CO2_form_b_amplitude_pinned/co2.json"
CO2r = C + "CO2_form_b_amplitude_pinned/co2_rows.out"; CO2s = C + "CO2_form_b_amplitude_pinned/co2_shear.out"
CO2R = C + "CO2_form_b_amplitude_pinned/RESULT.md"; CO2p = C + "CO2_form_b_amplitude_pinned/co2_posthoc.out"
CO2pj = C + "CO2_form_b_amplitude_pinned/co2_posthoc.json"
RER = C + "RERUNS_2026-11-09.md"
TPA = F + "TPA1_two_phase_action/RESULT.md"
SCS = F + "SCS1_static_clock_coupled_stability/RESULT.md"; SCSd = F + "SCS1_static_clock_coupled_stability/"
K3F = F + "KO3F_spec_veto_power_forecast/README.md"; K3Fj = F + "KO3F_spec_veto_power_forecast/ko3f_forecast.json"
P69 = P + "PAPER69_closure_by_verdict_2026.zenodo.json"; P70 = P + "PAPER70_field_equations_closure_2026.zenodo.json"
P71 = P + "PAPER71_switch_theorems_kids_outer_points_2026.zenodo.json"
# version 1.1: the lanes that landed on 2026-11-10 and the older lanes quoted by Section 7's survey of media
D = "closure_2026_11_10/"
SCS2 = F + "SCS2_static_clock_stability_discs/RESULT.md"; SCS3 = F + "SCS3_external_field_stability/RESULT.md"
MK1 = F + "MK1_one_dust_constant/RESULT.md"; MK2 = F + "MK2_exponential_dust_term/RESULT.md"
COL1 = F + "COL1_clock_collapse/RESULT.md"; FLD1 = F + "FLD1_fold_reach/RESULT.md"
REL1 = F + "REL1_relative_acceleration/RESULT.md"; SHP1 = F + "SHP1_cold_component_shape/RESULT.md"
TK1 = D + "TK1_expansion_keyed_dust/RESULT.md"; AKD1 = D + "AKD1_acceleration_keyed_dust/RESULT.md"
LFS1 = D + "LFS1_leafwise_flux_supply/RESULT.md"; CLS1 = D + "CLS1_cluster_state_in_action/RESULT.md"
KL1 = D + "KL1_lensing_amplitude_survey_assumptions/RESULT.md"
KL1j = D + "KL1_lensing_amplitude_survey_assumptions/kl1.json"; KL1cj = D + "KL1_lensing_amplitude_survey_assumptions/kl1c.json"
KL1R = D + "KL1R_blind_legacy_regrade/RESULT.md"; DG1 = D + "DG1_dwarf_gas_history/RESULT.md"
NH2 = D + "NH2_ngc1052_host_mass/RESULT.md"; XCV1 = D + "XCV1_xcop_nonhydrostatic_mass/RESULT.md"
GO1 = D + "GO1_group_outskirts/RESULT.md"; RER2 = D + "RERUNS_2026-11-10.md"
MED = D + "MEDIUM_DESIGN_2026-11-10.md"; MEDo = D + "MEDIUM_DESIGN_check.out"; THY = D + "THEORY_ASSEMBLED_2026-11-10.md"
R22 = "rebuild_2026_10_22/"
M5 = R22 + "M5_equilibrium_law/README.md"; PH1 = R22 + "PH1_two_phase_cold_energy/README.md"
IJ1 = R22 + "IJ1_isothermal_jeans_halos/README.md"; HF1 = R22 + "HF1_hybrid_fermion/README.md"
TM1 = R22 + "TM1_tethered_medium/README.md"; QX28 = "closure_2026_11_06/QX28_superfluid_two_phase/README.md"
FA3 = "closure_2026_11_07/FA3_nonlocal_action_search/RESULT.md"; WM1 = C + "WM1_warm_component_law_baryons/RESULT.md"
RETIRE = R22 + "OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md"
# round 2 of version 1.1: DCN1, the note R541 and its five lanes, X38's statement of route E
DCN1 = F + "DCN1_disc_centre_null/RESULT.md"; R541 = D + "R541_why_the_cold_share/NOTE.md"
R541A = D + "R541A_clock_matter_coupling/RESULT.md"; R541B = D + "R541B_early_symmetry_breaking/RESULT.md"
R541C = D + "R541C_made_in_inflation/RESULT.md"; R541D = D + "R541D_baryon_current_cogenesis/RESULT.md"
R541E = D + "R541E_b_minus_l_variant/RESULT.md"; X38 = R22 + "X38_a0_surface_density_halos/README.md"
GO1a = D + "GO1_group_outskirts/RESULT.md"
# (fragment in the TeX, source file, literal in that file)
L = [
 # header
 ("PAPER69 (DOI 10.5281/zenodo.24025170", P69, "10.5281/zenodo.24025170"),
 ("PAPER70 (v2.1, DOI 10.5281/zenodo.24092073", P70, "\"doi\": \"10.5281/zenodo.24092073\""),
 ("PAPER71 (v1.1, DOI 10.5281/zenodo.24095262", P71, "\"doi\": \"10.5281/zenodo.24095262\""),
 # abstract and section 1
 ("about 5.4 times the baryons", ONEn, "about 5.4 times the baryons"),
 ("canonical $a_0=9.3603\\times10^{-11}$", RB1, "canonical (a0 9.3603e-11)"),
 ("alt $1.1312\\times10^{-10}$", RB1, "alt (1.1312e-10)"),
 ("a cold component of 5.41 times the baryons", DEC, "needs a cold component of 5.41 times the baryons"),
 ("X-COP by $+0.4675$/$+0.4345$\\,dex", DEC, "fail, +0.4675 / +0.4345 dex"),
 ("X-COP by $+0.4675$/$+0.4345$\\,dex", PD1o, "X-COP +0.4675 (law-only +0.4675)"),
 ("X-COP by $+0.4675$/$+0.4345$\\,dex", PD1o, "X-COP +0.4345 (law-only +0.4345)"),
 ("the Bullet ($Z=-4.55$, the mass sits on the gas)", DEC, "fail, Z -4.55: the mass sits on the gas"),
 ("the Bullet ($Z=-4.55$, the mass sits on the gas)", PD1o, "law-only KA row FAIL (Z -4.55, -4.54)"),
 ("($+1.12$\\,dex with a static external field, $+1.41$ with a moving host)", DEC, "+1.12 dex with a static external field, +1.41 with a moving host"),
 ("($+1.12$\\,dex with a static external field, $+1.41$ with a moving host)", RB2o, "can main +1.120 half +1.121 moving +1.412"),
 ("As graded there it is FAIL/FAIL", PD1, "PD1 RESULT: FAIL / FAIL"),
 ("As graded there it is FAIL/FAIL", PD2, "PD2 RESULT: FAIL / FAIL"),
 ("rotation curves (rms 0.0563/0.0558 against a line of 0.0660)", DEC, "rms 0.0563 / 0.0558 against a line of 0.0660"),
 ("rotation curves (rms 0.0563/0.0558 against a line of 0.0660)", PD1o, "P2 SPARC PASS: rms 0.0563 (line 0.0660)"),
 ("rotation curves (rms 0.0563/0.0558 against a line of 0.0660)", PD1o, "P2 SPARC PASS: rms 0.0558"),
 ("(worst $-0.635$\\,dex)", DEC, "worst -0.635 dex"),
 ("(worst $-0.635$\\,dex)", PD1o, "min -0.635"),
 ("in a reported bracket ($+0.019$/$+0.010$)", DEC, "+0.019 / +0.010"),
 ("in a reported bracket ($+0.019$/$+0.010$)", PD1b, "X-COP PASS +0.019/"),
 ("in a reported bracket ($+0.019$/$+0.010$)", PD1b, "X-COP PASS +0.010/"),
 ("The choice is of a form, not of a pass", DEC, "It is chosen as a form, not as a pass."),
 ("It reopens the cold sector retired on 2026-11-01 for this one reading", DEC, "It reopens the cold sector for this one reading."),
 # section 2 (the action)
 ("Poisson's with source $\\rho_b+D\\!\\cdot\\!P$", QX17, "(E4)_00 gives Poisson with rho_b + D.P"),
 ("to leading order, $D\\!\\cdot\\!P+\\mu_K^2(Q-1)/K$", QX17, "To leading order rho_Q = D.P + mu_K^2 (Q - 1)/K"),
 ("$J(g)=(a_0^2/K)[u-\\ln(1+u)]$", FB1o, "J = P.A - W equals (a0^2/K)[u - ln(1 + u)]: True"),
 ("$\\partial_j\\Pi_{ij}=(D\\!\\cdot\\!P)\\,g_i$", FB1, "d_j Pi_ij = (D.P) g_i pointwise"),
 ("In the deep field $J=g^2/2K$", FB1, "in the deep field J = g^2 / (2K)"),
 ("$\\sigma^2=\\tfrac12\\sqrt{GM_ba_0}$", FB1, "sigma^2 = (1/2) sqrt(G M_b a0)"),
 ("The identity holds for any $J(g)$ with a curl-free field", FB1, "the identity holds for any J(g) with P = dJ/dg and a curl-free field"),
 ("it is not evidence for this $J$", FB1, "It is not evidence that this J is the right one."),
 # TPA1
 ("lane TPA1 found the action's law-on phase gradient-unstable, with no ghost", TPA, "a gradient instability, with no ghost, in the law-on phase"),
 ("wherever the clock's own dust density is below a critical value", TPA, "is gradient-unstable wherever its own dust density is below n_crit"),
 # SCS1: the coupled stability of the static state
 ("and in a planar background", SCS, "TPA1 froze a planar 2+1 lapse"),
 ("Lane SCS1 then coupled gravity around a point mass and labels the state STABLE on both footings", SCS, "**SCS1: STABLE / STABLE (canonical / alt).**"),
 ("Lane SCS1 then coupled gravity around a point mass and labels the state STABLE on both footings", SCS, "With gravity coupled, the static clock of action (A) is linearly stable."),
 ("two independent routes find no growing mode at any wavenumber", SCS, "independent routes find no growing mode, at any wavenumber, on either footing."),
 ("disturbances oscillate at 0.08 to 12 times the local free-fall rate", SCS, "Their rates run from 0.08 to 12 times the local free-fall rate"),
 ("The clock's gradient coefficient is its own charge density, $n_d+D\\!\\cdot\\!P$", SCS, "The clock's gradient coefficient is n_d + D.P, not n_d + p'."),
 ("In TPA1's planar background $D\\!\\cdot\\!P=p'$, which is negative", SCS, "In it D.P = p', which is negative because the field falls outward."),
 ("around a point mass $D\\!\\cdot\\!P=p'+2p/r$ is the phantom density, which is positive", SCS, "Around a real point mass D.P = p' + 2p/r is the phantom density, and it is positive."),
 ("SCS1 reproduces TPA1's numbers in the planar background, and the growth returns when that background is put back into the coupled system", SCS, "SCS1 reproduces TPA1's numbers exactly in its planar model (KA1), and turning the planar background back on in the coupled system brings the growth back (M3)."),
 ("TPA1's other findings stand", SCS, "Its other findings stand"),
 ("the note's sentence has been corrected", FB1, "**Corrected when SCS1 landed (2026-11-10).** The paragraph above is wrong for a point mass."),
 ("The result is linear, and for point masses only", SCS, "This is linear stability only."),
 ("The result is linear, and for point masses only", SCS, "Only point masses were analysed."),
 ("For flattened baryons the law's phantom density can be negative in places, and there the same closed form gives growth", SCS, "For flattened systems the law's phantom density can be negative in places."),
 ("For flattened baryons the law's phantom density can be negative in places, and there the same closed form gives growth", SCS, "There G = n_d + D.P < 0 gives bounded growth at gamma_L = 0"),
 ("SCS1 did not analyse discs or extended spherical distributions", SCS, "Discs are therefore not settled. Extended spherical baryon distributions were not run either."),
 ("At the dust constant the CMB needs, the static state is Jeans-unstable at the local free-fall rate (e-folding times of 17\\,Myr to 3.9\\,Gyr)", SCS, "At the CMB-required mu_K* the static state is not stable."),
 ("At the dust constant the CMB needs, the static state is Jeans-unstable at the local free-fall rate (e-folding times of 17\\,Myr to 3.9\\,Gyr)", SCS, "with e-folding times of 17 Myr to 3.9 Gyr"),
 ("that is the cosmological setting and not the form's galaxy setting", SCS, "It is the cosmological setting, not form B's galaxy setting."),
 ("The lane's three amendments are post hoc and disclosed", SCSd + "AMENDMENT_A1.md", "# SCS1 AMENDMENT A1 (post hoc; committed alone, before any graded run)"),
 ("The lane's three amendments are post hoc and disclosed", SCSd + "AMENDMENT_A2.md", "# SCS1 AMENDMENT A2 (post hoc; committed alone, before the final route-2 run)"),
 ("The lane's three amendments are post hoc and disclosed", SCSd + "AMENDMENT_A3.md", "# SCS1 AMENDMENT A3 (post hoc; committed alone, before the final route-2 run)"),
 ("one mutation arm does not bite, being a field redefinition, as the lane said before any run", SCS, "**does not bite** (change exactly 0), as disclosed before any run: it is the field redefinition"),
 ("its lead session re-ran both of its routes and recompiled its Lean file (13 theorems); the first route reproduces with only timing lines differing", F + "README.md", "re-run by the lead: route 1, the covariant WKB script, reproduces with only timing lines differing, and `SCS1.lean` recompiles with exit 0, 13 theorems, twin failing"),
 ("the second gives every label identical and every eigenvalue equal to better than one part in a million", F + "README.md", "route 2, the radial solve, re-run in about an hour: every label identical and every eigenvalue equal to better than one part in a million; the stiffness output identical"),
 ("which SCS1 finds does not hold around a point mass", SCS, "So TPA1's \"UNHEALTHY\" for the law-on static clock does not hold for a point mass."),
 ("linearly stable around a point mass and, away from the centre, around isolated discs with gravity coupled; a disc in an external field NO VERDICT with STABLE excluded; the earlier instability belonged to a planar background", SCS, "**SCS1: STABLE / STABLE (canonical / alt).**"),
 ("linearly stable around a point mass and, away from the centre, around isolated discs with gravity coupled; a disc in an external field NO VERDICT with STABLE excluded; the earlier instability belonged to a planar background", F + "README.md", "Isolated discs STABLE / STABLE; discs in an external field NO VERDICT / NO VERDICT"),
 ("linearly stable around a point mass and, away from the centre, around isolated discs with gravity coupled; a disc in an external field NO VERDICT with STABLE excluded; the earlier instability belonged to a planar background", SCS, "**TPA1 item 6's S = 1 instability is an artefact of its background.**"),
 ("With gravity coupled the static state is linearly stable around a point mass. Version 1.1", SCS, "With gravity coupled, the static clock of action (A) is linearly stable."),
 ("the nonlinear outcome has not been computed", SCS, "Finite disturbances, mode coupling and caustics of the irrotational clock are not computed."),
 ("the nonlinear outcome has not been computed", SCS2, "**The nonlinear outcome.** Where the external-field brackets grow, nothing here says what the growth turns into"),
 ("Point masses and isolated discs away from their centres are computed and stable", SCS, "**SCS1: STABLE / STABLE (canonical / alt).**"),
 ("Point masses and isolated discs away from their centres are computed and stable", SCS2, "| **STABLE / STABLE** | D.P > 0 in every cell, on both grids. No growing mode on either route. |"),
 ("The lead session and TPA1 expected the instability to survive the coupling to gravity", SCS, "The lead's and TPA1's expectation (the gradient instability survives coupling) is not."),
 ("SCS1's expectation before its freeze, stable with the earlier result planar, is the outcome", SCS, "**My pre-freeze expectation (STABLE, TPA1's result planar) is the outcome.**"),
 ("and SCS1's three amendments", SCS, "**A2** (zero tolerance 1e-12 of the largest eigenvalue) and **A3**"),
 ("With gravity coupled the static state is linearly stable around a point mass; an instability", SCS, "With gravity coupled, the static clock of action (A) is linearly stable."),
 ("an instability found earlier belonged to a planar background", SCS, "**TPA1 item 6's S = 1 instability is an artefact of its background.**"),
 ("the e-folding times on its grid are 5.0\\,Myr to 0.62\\,Gyr", TPA, "On the frozen grid the e-folding time is 5.0 Myr to 0.62 Gyr."),
 ("With the metric frozen (the decoupling limit)", TPA, "Every analysis was done in the decoupling limit (metric frozen)."),
 ("(EQUATIONS COMPLETE; health UNHEALTHY)", TPA, "**TPA1: EQUATIONS COMPLETE. Health: UNHEALTHY**"),
 ("its switch wall and its dust phase are healthy", TPA, "The wall itself is stable"),
 ("its switch wall and its dust phase are healthy", TPA, "The S = 0 phase is healthy."),
 ("The note on form B read the form's static state, which has almost no dust of its own, as lying in that range", FB1, "The static state of section 1 has almost no dust of its own (mu_K = 0 in galaxies), so it sits in that unstable range"),
 # abstract
 ("the Bullet passes only if the subcluster's stripped gas is counted", RB1, "**CONSISTENT [STRIPPING-DEPENDENT]**: S1 passes, S1/2 passes, S0 (= PD1 A2) fails"),
 ("Its CMB, lensing and growth rows hold when computed, on an amended reading of that lane's checks.", CO1, "The primary CMB, CMB lensing and the growth rate hold when computed."),
 ("With the amplitude of fluctuations pinned by large-angle polarisation, CMB lensing matches the prediction to 0.3$\\sigma$ and the growth rate passes", CO2o, "(-0.30 sigma) PASS | 0.9929 +- 0.0239 (-0.30 sigma) PASS"),
 ("With the amplitude of fluctuations pinned by large-angle polarisation, CMB lensing matches the prediction to 0.3$\\sigma$ and the growth rate passes", CO2o, "1.95 / 2.14 PASS | 1.95 / 2.14 PASS"),
 ("the absolute fit is excluded at 3$\\sigma$ by the frozen line and reads tension once the reference run's realisation noise is corrected, a check made after grading", CO2o, "LABEL canonical: AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA (for form B as stated, gravity-only S0"),
 ("the absolute fit is excluded at 3$\\sigma$ by the frozen line and reads tension once the reference run's realisation noise is corrected, a check made after grading", CO2o, "LABEL alt: AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA (for form B as stated, gravity-only S0"),
 ("the absolute fit is excluded at 3$\\sigma$ by the frozen line and reads tension once the reference run's realisation noise is corrected, a check made after grading", CO2c, "p < 0.0027 EXCLUDED AT 3 SIGMA"),
 ("tension and not exclusion", CO2s, "constant factor (bracket): chi2 153.74, p 4.42e-03 (TENSION)"),
 ("tension and not exclusion", CO2s, "constant factor (bracket): chi2 155.04, p 3.73e-03 (TENSION)"),
 ("This is the tension that any cold component fitted to the CMB carries; the form states neither gas ejection nor neutrino mass, and does not relieve it", CO2c, "A fail here is the weak-lensing amplitude tension that any cold-component fit to the CMB carries; it is not peculiar to form B, and form B does not relieve it."),
 # RB1
 ("(RB1): NOT FALSIFIED (ONE-SIDED) on both footings", RB1, "RB1 RESULT: NOT FALSIFIED (ONE-SIDED) / NOT FALSIFIED (ONE-SIDED)"),
 ("$R=5.41$ times the baryons", RB1, "R = 5.41"),
 ("the two-sided amount gate stays FAIL as PD1 graded it", RB1, "the two-sided amount gate stays FAIL as PD1 graded it"),
 ("The 20 hydrostatic groups read", RB1o, "G-H n 20:"),
 ("0.597$ [0.556, 0.637] at $R_{500}$, none above 1", RB1o, "median f_ret 0.597 [0.556, 0.637], 0 above 1"),
 ("Form B reads the missing 40\\,\\%", RB1, "40 % of the baryons a fair share would bring are not inside R500"),
 ("reads 1.095 [0.885, 1.259], with 4 of 7 clusters above 1", RB1o, "median f_ret 1.095 [0.885, 1.259], 4 above 1"),
 ("the class reads 1.057 [1.046, 1.072]", RB1o, "C-X at R500 1.057 [1.046, 1.072] FAILS"),
 ("this row is a reported bracket, and graded there the gate would fail", RB1, "This row is a reported bracket and is not graded; graded at R500, gate 1 would FAIL."),
 ("the same class reads 0.959", RB1o, "C-X M_NFW at R500 (A1, post hoc) 0.959"),
 ("turns on about 10\\,\\% in the hydrostatic mass", RB1, "turns on about 10 % in the hydrostatic mass"),
 ("slope $+0.160$ [$+0.080$, $+0.225$]", RB1o, "slope +0.160 [+0.080, +0.225]"),
 ("0.72 / 0.63 / 0.55 / 0.47 / 0.35", RB1o, "model 0.72 / 0.63 / 0.55 / 0.47 / 0.35"),
 ("0.71 / 0.66 / 0.58 / 0.46 / 0.32 (canonical)", RB1o, "data 0.71 / 0.66 / 0.58 / 0.46 / 0.32"),
 ("$-0.007$ / $+0.033$ / $+0.006$ / $-0.030$ / $-0.041$\\,dex against a line of 0.10", RB1, "-0.007 / +0.033 / +0.006 / -0.030 / -0.041** (line 0.10)"),
 ("under the frozen known answer the gate is NO VERDICT", RB1, "Under the frozen KA-2, gate 3 is NO VERDICT."),
 ("PD1's 2.6$\\sigma$ deficit", PD1, "The subcluster's mass inside 300 kpc is 2.6 sigma low."),
 ("the amounts read $-0.45$ / $+0.37$ (main / sub) and pass", RB1o, "Z -0.45/+0.37"),
 ("they read $+0.49$ / $-2.58$ and fail", RB1o, "Z +0.49/-2.58"),
 ("they read $+0.49$ / $-2.58$ and fail", PD1a2, "M300 Z +0.49, -2.58"),
 ("No measurement on disk fixes the subcluster's gas before the merger", RB1, "No measurement on disk fixes the subcluster's pre-merger gas"),
 # RB2
 ("(RB2): B FAILS ON THE HOSTED ROWS on both footings", RB2, "B FAILS ON THE HOSTED ROWS (both footings)"),
 ("from $+1.120$ to $+0.326$\\,dex (alt $+0.283$)", RB2, "+0.326 [-0.066, +0.723] / +0.283"),
 ("from $+1.120$ to $+0.326$\\,dex (alt $+0.283$)", RB2, "main +1.120 / +1.075"),
 ("on statistics alone it is [$+0.105$, $+0.547$]", RB2, "On statistics alone the interval is [+0.105, +0.547]"),
 ("as a class ($+0.281$/$+0.241$)", RB2, "+0.281 [-0.015, +0.573] / +0.241"),
 ("with Draco, Ursa Minor and Sextans high row by row", RB2, "Draco +0.63, Ursa Minor +0.57 and Sextans +0.50 sit far above"),
 ("$+0.634$ [$+0.433$, $+0.865$] (alt $+0.592$)", RB2, "+0.634 [+0.433, +0.865] / +0.592"),
 ("$+0.273$ [$+0.085$, $+0.473$] (alt $+0.231$)", RB2, "+0.273 [+0.085, +0.473] / +0.231"),
 ("since that would be a change after the freeze", RB2, "because it would be a change after the freeze"),
 ("sit 0.74 and 0.94\\,dex below B", RB2, "sit 0.74 and 0.94 dex below B"),
 ("holds 17 and about 100 times the mass B gives it", RB2, "17 times (DF2, 1.2e13 Msun inside 79 kpc) and about 100 times"),
 ("holds 17 and about 100 times the mass B gives it", RB2o, "'ratio': 16.57"),
 ("holds 17 and about 100 times the mass B gives it", RB2o, "'ratio': 99.30"),
 ("NGC\\,147 and IC\\,1613 sit 0.56 and 0.54\\,dex below B", RB2, "sits 0.56 / 0.59 dex below B"),
 ("NGC\\,147 and IC\\,1613 sit 0.56 and 0.54\\,dex below B", RB2, "sits 0.54 / 0.58 dex below B"),
 ("the law with its external field leaves them as low", RB2, "These two are just as low under the law with its external field"),
 ("Crater\\,II is the one low row tides can reach", RB2, "Crater II**, the one LOW row tides can reach"),
 ("two classes stay high and four low rows cannot be reached", RB2, "Two graded classes fail high on both footings, and four LOW rows cannot be"),
 # KO2
 ("(KO2): NO VERDICT for late and early types on both footings", KO2, "NO VERDICT for late types and NO VERDICT for early types, on both footings"),
 ("All 181,477 KiDS lenses", KO2, "All 181,477 lenses."),
 ("(888,795 pool objects)", KO2, "888,795 pool objects"),
 ("One of 13 known answers failed", KO2o, "checks: 12 of 13 pass"),
 ("a cross-shear pull of 3.11 among 15 amplitudes", KO2b, "largest pull giant ext +3.11; |pull| > 2: 2, > 3: 1 of 15"),
 ("the frozen bracket rule gives NOT SEPARATED for both types", KO2, "Without KA-3b the label would still be NOT SEPARATED for both types"),
 ("One mutation twin did not bite", KO2, "One MUTATE twin (M3) did not bite."),
 ("$0.487\\pm0.071$ in the primary design", KO2o, "early R +0.487 +- 0.050 (s_tot 0.071)"),
 ("$0.739\\pm0.115$ with lens and neighbour amplitudes untied", KO2o, "early R +0.739 +- 0.103 (s_tot 0.115)"),
 ("(0.038/0.007 in the primary design)", KO2, "form B 0.038 / 0.007 (canonical / alt)"),
 ("(0.038/0.007 in the primary design)", KO2b, "canonical primary noiseless : late R +0.038"),
 ("(0.038/0.007 in the primary design)", KO2b, "alt primary noiseless : late R +0.007"),
 ("$0.277\\pm0.183$ tied", KO2o, "late R +0.277 +- 0.176 (s_tot 0.183)"),
 ("$1.071\\pm0.199$ untied", KO2o, "late R +1.071 +- 0.193 (s_tot 0.199)"),
 ("reads $1.030\\pm0.282$ untied", KO2b, "canonical untied with WX noise : late R +1.030 +- 0.282"),
 ("(late outer-to-inner ratio $0.93\\pm0.13$, early $1.09\\pm0.08$)", KO2, "R_s 0.93 +- 0.13"),
 ("(late outer-to-inner ratio $0.93\\pm0.13$, early $1.09\\pm0.08$)", KO2, "R_s 1.09 +- 0.08"),
 ("(late outer-to-inner ratio $0.93\\pm0.13$, early $1.09\\pm0.08$)", KO2o, "R_s 0.930 +- 0.129"),
 ("(late outer-to-inner ratio $0.93\\pm0.13$, early $1.09\\pm0.08$)", KO2o, "R_s 1.089 +- 0.076"),
 ("reported that host-free late types show no outer signal ($-0.19\\pm0.39$ against $1.34\\pm0.18$ for early types)", F + "KO1_kids_outer_points/RESULT.md", "-0.19 +- 0.39 / 1.34 +- 0.18"),
 ("reported that host-free late types show no outer signal ($-0.19\\pm0.39$ against $1.34\\pm0.18$ for early types)", P + "PAPER71_switch_theorems_kids_outer_points_2026.tex", "Host-free late types show no outer signal ($-0.19\\pm0.39$"),
 ("Both labelled it a lead and not a result: seen after the freeze and sharing the veto's edge", F + "KO1_kids_outer_points/RESULT.md", "was seen after the freeze, sits in a sub-split and shares the edge effect. It is a lead, not a result."),
 ("Both labelled it a lead and not a result: seen after the freeze and sharing the veto's edge", P + "PAPER71_switch_theorems_kids_outer_points_2026.tex", "That split was seen after the freeze and shares the edge effect; it is a lead, not a result."),
 ("the deficit appears only inside the host-free subset ($-0.03\\pm0.28$)", KO2, "R6, KO1's host-free lenses, neighbours modelled:** late -0.03 +- 0.28"),
 ("the deficit appears only inside the host-free subset ($-0.03\\pm0.28$)", KO2o, "R6 hostfree_ko1: late -0.032 +- 0.282"),
 # ONE1 pre-freeze look
 ("committed before KO2 had a lensing number", ONEn, "committed before KO2 has any lensing number on disk"),
 ("It is post hoc and models no neighbours", ONEn, "Post hoc. It reads no shear"),
 ("It is post hoc and models no neighbours", ONEn, "No neighbours are modelled."),
 ("form B reads 0.510 against a measured $0.607\\pm0.094$", ONEo, "R_s 0.607 +- 0.094"),
 ("form B reads 0.510 against a measured $0.607\\pm0.094$", ONEo, "X 59.50: bins [0.296 0.383 0.508 0.674] middle 1.031 inner 1.004 R_s model 0.510"),
 ("form B reads 0.510 against a measured $0.607\\pm0.094$", ONEn, "| 1.0 R_h | 0.607 +- 0.094 | 0.510 (+1.0 sigma)"),
 ("4.2$\\sigma$ off on the other side", ONEn, "| 1 (-4.2) [-4.2] |"),
 ("4.2$\\sigma$ off on the other side", ONEo, "R_s model 1.000 (measured - model) / sigma -4.18"),
 ("form B reads 0.525 against $0.811\\pm0.134$, 2.1$\\sigma$ low, with the law 1.4$\\sigma$ off", ONEn, "| 1.6 R_h | 0.811 +- 0.134 | 0.525 (+2.1)"),
 ("form B reads 0.525 against $0.811\\pm0.134$, 2.1$\\sigma$ low, with the law 1.4$\\sigma$ off", ONEn, "| 1 (-1.4) [-1.4] |"),
 ("form B reads 0.525 against $0.811\\pm0.134$, 2.1$\\sigma$ low, with the law 1.4$\\sigma$ off", ONEo, "R_s model 0.525 (measured - model) / sigma +2.14"),
 ("The note read from it that one share does not fit late and early types together", ONEn, "One share for both types does not fit both."),
 ("ONE1's frozen type-difference line passes at every veto", ONE, "The frozen type-difference line passes at every veto"),
 ("KO2's late-type ratio would be at most about 0.5", ONEn, "R_ext for late types is below the law's floor: at most about 0.5."),
 ("the tied design meets that ($0.277\\pm0.183$) and the untied one does not ($1.071\\pm0.199$)", KO2o, "late R +0.277 +- 0.176 (s_tot 0.183)"),
 ("the tied design meets that ($0.277\\pm0.183$) and the untied one does not ($1.071\\pm0.199$)", KO2o, "late R +1.071 +- 0.193 (s_tot 0.199)"),
 ("Rotation curves & pass, rms 0.0563/0.0558 (line 0.0660)", PD1o, "P2 SPARC PASS: rms 0.0563 (line 0.0660)"),
 ("Rotation curves & pass, rms 0.0563/0.0558 (line 0.0660)", PD1o, "P2 SPARC PASS: rms 0.0558"),
 # ONE1 graded row
 ("KiDS host-free PASSES/PASSES by its frozen gate at the widest veto, for PD1's share and for that row only", ONE, "**KiDS host-free: PASSES / PASSES** (canonical / alt), for PD1's own share"),
 ("KiDS host-free PASSES/PASSES by its frozen gate at the widest veto, for PD1's share and for that row only", ONE, "This label covers the KiDS host-free row only"),
 ("The shape ratio there is 0.811 against a model of 1.003 ($-1.14\\sigma$", ONE, "| **1.6 R_h (graded)** | 0.811 / 1.003 (-1.14)"),
 ("The shape ratio there is 0.811 against a model of 1.003 ($-1.14\\sigma$", ONEk, "KO1 1.6 R_h | all: data 0.811+-0.134 model 1.003 (no nb 0.861) k 2.50 z -1.14"),
 ("alt 0.809 against 0.847)", ONE, "| **1.6 R_h** | 0.809 / 0.847 (-0.23)"),
 ("late types read 0.084 against 0.792 ($-1.46\\sigma$)", ONE, "0.084 / 0.792 (-1.46)"),
 ("early types 0.882 against 0.999", ONE, "0.882 / 0.999 (-0.65)"),
 ("(0.607 against 0.924, $-2.68\\sigma$)", ONE, "| 1.0 R_h (reported) | 0.607 / 0.924 (-2.68)"),
 ("The law with no end gives 0.98 at the widest veto, also inside 2$\\sigma$", ONE, "the law with no end gives 0.98 / 0.98"),
 ("The law with no end gives 0.98 at the widest veto, also inside 2$\\sigma$", ONEk, "1.6 R_h 0.978 (z -1.26)"),
 ("so the pass does not separate form B from the law", ONE, "The pass says KiDS cannot tell this reading from the law with no end."),
 ("the late-type error there (0.42) is too large to test discs", ONE, "veto the late-type error (0.42) is too large to test them"),
 ("The look's 0.510 to 0.525 was mainly a matter of calibration", ONEn, "| 1.0 R_h | 0.607 +- 0.094 | 0.510 (+1.0 sigma)"),
 ("The look's 0.510 to 0.525 was mainly a matter of calibration", ONEn, "0.525 (+2.1)"),
 ("The look's 0.510 to 0.525 was mainly a matter of calibration", ONE, "1. **The calibration.**"),
 ("the model reads 0.86/0.73 at the widest veto without neighbours and 1.00/0.85 with them", ONE, "PD1's share gives R_s 0.86 / 0.73 without neighbours and 1.00 / 0.85 with them at 1.6 R_h"),
 # HE1
 ("(HE1): FAILS on both footings", HE1, "**HE1: FAILS / FAILS** (canonical / alt)"),
 ("none of its three stated shares, at any outer radius, passes its first four gates together", HE1, "No X at any R_out passes G1 to G4 together"),
 ("none of its three stated shares, at any outer radius, passes its first four gates together", HE1, "every X of the stated set fails"),
 ("Post hoc and with low power, at the widest veto the record's share fits those stacks ($p$ 0.73/0.83), as does the law", HE1, "The veto edge (reported, post hoc, low power)."),
 ("Post hoc and with low power, at the widest veto the record's share fits those stacks ($p$ 0.73/0.83), as does the law", HE1, "At 1.6 R_h the X_share model fits (p 0.73 / 0.83), as do the law (p 0.25 / 0.22)"),
 ("only timing lines differ", F + "README.md", "only timing lines differ"),
 ("were each re-run by a session other than the one that wrote it, and their labels reproduced", RER, "Each lane below was re-run by a session other than the one that wrote it"),
 ("were each re-run by a session other than the one that wrote it, and their labels reproduced", RER, "| RB1 `closure_2026_11_09/RB1_form_b_hot_systems/` | `rb1.py`, one thread, 48 s | Every label reproduces"),
 ("were each re-run by a session other than the one that wrote it, and their labels reproduced", RER, "| RB2 `closure_2026_11_09/RB2_form_b_hosted_rows/` | `rb2.py`, one thread, 12 s | Every label reproduces"),
 ("were each re-run by a session other than the one that wrote it, and their labels reproduced", RER, "Both labels reproduce (LATE NO VERDICT, EARLY NO VERDICT on both footings; R_ext late +0.277 +- 0.183, early +0.487 +- 0.071)"),
 ("were each re-run by a session other than the one that wrote it, and their labels reproduced", RER, "Both labels reproduce (ROWS HOLD with an inherited halo list; NO VERDICT with M4 as frozen)"),
 ("were each re-run by a session other than the one that wrote it, and their labels reproduced", RER, "HE1 and TPA1 were re-run by the session that leads `fable52_push/`; its README records them."),
 ("KO2, RB1, RB2, CO1, CO2, HE1, TPA1 and ONE1 were each re-run", RER, "Both labels reproduce (AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA on both footings; P4 chi2 157.89 / 159.35, p 2.58e-03 / 2.12e-03)"),
 ("KO2, RB1, RB2, CO1, CO2, HE1, TPA1 and ONE1 were each re-run", RER, "all 502 values of `co2_posthoc.json` are identical (every correction TENSION, p 0.003 to 0.013)"),
 ("KO2, RB1, RB2, CO1, CO2, HE1, TPA1 and ONE1 were each re-run", RER, "its README has recorded it since (the KiDS script's label and every graded number reproduce)"),
 ("before any graded number was computed (KO2 ran a model-only design toy before its freeze and says so)", KO2, "ko2_design_toy.py (pre-freeze, model only)"),
 ("The envelope exists, is stable and fills 0.2\\,\\% of space or less", HE1, "It is stable, it leaves discs alone (except the cap share at the highest masses), and it fills about 0.2 % of space or less."),
 ("It fails KiDS's late-type stacks", HE1, "It fails where it was expected to fail: KiDS's late-type lenses."),
 ("Its fifth gate fails as frozen on two clusters near $R_{500}$ only, and the label does not rest on it", HE1, "G5 fails as frozen on two clusters, near R500 only."),
 ("Its fifth gate fails as frozen on two clusters near $R_{500}$ only, and the label does not rest on it", HE1, "The label does not rest on G5."),
 ("Re-run by its lead session: both labels and every number in \\texttt{he1.json} reproduce", F + "README.md", "re-run by the lead: both labels and every number in `he1.json` reproduce, only timing lines differ"),
 ("Re-run by its lead session: the KiDS script's label and every graded number reproduce", F + "README.md", "re-run by the lead: the KiDS script's label and every graded number reproduce"),
 ("its Lean file recompiles (10 theorems) and its twin fails", F + "README.md", "`ONE1.lean` recompiles with exit 0, 10 theorems, and its twin fails"),
 ("was removed from the machine on the evening of 2026-11-09", F + "README.md", "was removed from the machine on the evening of 2026-11-09"),
 ("a build inside the repository has been used since 22:17 that evening", F + "README.md", "A build has been inside the repository's own `fable_independent_2026/lean_2026` since 22:17"),
 ("the static dust term $-\\mu_K^2\\Phi/K$", FB1, "carries dust -mu_K^2 Phi / K in every well"),
 # CO1
 ("(CO1): ROWS HOLD on the amended reading, with an inherited halo list", CO1, "**ROWS HOLD / ROWS HOLD (canonical / alt), with an inherited halo list.**"),
 ("(CO1): ROWS HOLD on the amended reading, with an inherited halo list", CO1, "the label above rests on AMENDMENT A1"),
 ("That row replays a fit stored by an earlier lane, and its yardstick is the likelihood package's own test point, not a framework quantity", CO1, "it is a yardstick for adequacy and not a framework quantity"),
 ("That row replays a fit stored by an earlier lane", CO1, "C1 is a re-run. F1A's stored best fits replay"),
 ("($-1.66$/$-1.89\\sigma$ against a 2$\\sigma$ line", CO1o, "(-1.66 sigma) | 0.9564 +- 0.0230 (-1.89 sigma) | |pull| <= 2"),
 ("and 5.1/8.8\\,\\% at $k=3\\,h$", CO1o, "R_cold at k = 1 / 3 / 5 h/Mpc | 1.006 / 1.051 / 1.090 | 1.010 / 1.088 / 1.159"),
 ("on the 104 points the reference run supports", CO1, "C5 keeps 104 of 225 published KiDS points (the S0 run's k range)"),
 ("(a bracket with constant-factor scaling, which understates it)", CO1, "A constant factor understates how the nonlinear spectrum responds to"),
 ("($-65.21$/$-65.07$ against a line of 9", CO1o, "| -65.21 (chi2 3740.16) PASS | -65.07 (chi2 3740.30) PASS | <= 9"),
 ("cold to baryon 5.410/5.412, fitted", CO1o, "cold / baryon at that fit (fitted) | 5.410 | 5.412"),
 ("PR4 lensing reads $0.9617\\pm0.0231$/$0.9564\\pm0.0230$ of the predicted amplitude", CO1o, "0.9617 +- 0.0231 (-1.66 sigma) | 0.9564 +- 0.0230 (-1.89 sigma)"),
 ("shape $\\chi^2$ 8.56 over 9 bandpowers", CO1o, "PR4 lensing shape chi2 (9 bandpowers) | 8.56 PASS | 8.56 PASS"),
 ("(largest pull 1.22/1.23)", CO1o, "max |pull| 1.22 PASS | 2.29 / 2.23, max |pull| 1.23 PASS"),
 ("the matter power changes by 0.6/1.0\\,\\% at $k=1$", CO1, "changes the matter power by 0.6 / 1.0 % at k = 1 h/Mpc"),
 ("raw KiDS-1000 cannot see it", CO1, "Raw KiDS-1000 cannot see it"),
 ("Read as frozen it is NO VERDICT", CO1o, "(read with M4 as frozen, which did not bite: NO VERDICT)"),
 ("the label rests on an amendment committed before any graded number", CO1, "the label above rests on AMENDMENT A1, committed before any graded"),
 ("a mass function, a bias and a concentration relation calibrated on simulations", CO1, "Tinker 2008 mass function, Tinker 2010 bias, Duffy 2008 c(M)"),
 ("the power at $k=1$ would be 2.9 times higher and raw KiDS would reject it", CO1, "the power at k = 1 would be 2.9 times higher and raw KiDS would reject it"),
 ("the cluster share tied to the baryons present (5.41 times them) and counted inside $R_{200c}$", CO1, "needs the cluster share tied to the baryons present (5.41 times"),
 ("the cluster share tied to the baryons present (5.41 times them) and counted inside $R_{200c}$", CO1, "share is counted inside R200c"),
 ("RB1 grades the same bookkeeping at $R_{500}$ or the last measured radius", RB1o, "class median f_ret at the outermost aperture"),
 ("RB1 grades the same bookkeeping at $R_{500}$ or the last measured radius", RB1, "| Lovisari groups, R500, KVM18 stars |"),
 ("RB1 grades the same bookkeeping at $R_{500}$ or the last measured radius", RB1, "X-COP, last radius (1.0-1.65 R500), M_FORW"),
 ("The fit's $\\sigma_8$ is 0.8405/0.8429, with no low-multipole data to hold it", CO1o, "sigma8 at that fit (S0 engine 0.811) | 0.8405 | 0.8429"),
 ("The fit's $\\sigma_8$ is 0.8405/0.8429, with no low-multipole data to hold it", CO1, "the fit has no low-L data"),
 ("at 0.811 with $p=0.014$ and form B at its own amplitude with $p=0.0015$/0.0009", CO1, "fits the record's S0 run at sigma8 0.811 with p 0.014, and form B at the fit's own amplitude with p 0.0015 / 0.0009"),
 ("at 0.811 with $p=0.014$", CO1o, "p of the same | 0.0142 /"),
 ("The forest row stays carried", CO1, "the Lyman-alpha forest row (stays carried)"),
 ("CO1 left the amplitude open", CO1, "The amplitude is not solved."),
 # CO2
 ("(CO2): AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA as frozen, on both footings; not robust", CO2o, "LABEL canonical: AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA"),
 ("(CO2): AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA as frozen, on both footings; not robust", CO2o, "LABEL alt: AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA"),
 ("(CO2): AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA as frozen, on both footings; not robust", CO2o, "Known answers: KA1 PASS, KA2 PASS, KA3 PASS, KA4 PASS, KA5 PASS"),
 ("with the Planck 2018 low-multipole polarisation table added", CO2c, "plus the Planck 2018 SimAll EE table, L 2 to 29"),
 ("from 0.0697/0.0729 to $0.0532\\pm0.0066$ on both footings", CO2o, "0.0532 +- 0.0066 (was 0.0697) | 0.0532 +- 0.0066 (was 0.0729)"),
 ("(a width along the degeneracy only, which understates the profile width)", CO2c, "this understates the profile width"),
 ("$\\sigma_8$ from 0.8405/0.8429 to 0.8271", CO2o, "0.8271 (0.8405); S8 0.8481 | 0.8271 (0.8429); S8 0.8481"),
 ("the cold to baryon ratio stays at 5.411/5.412", CO2o, "3.0432 (was 3.0752); 5.411 | 3.0432 (was 3.0811); 5.412"),
 ("The pinned fit is adequate ($-63.79$/$-63.75$ against a line of 9)", CO2o, "-63.79 PASS | -63.75 PASS | <= 9"),
 ("PR4 lensing reads $0.9928\\pm0.0239$/$0.9929\\pm0.0239$ of the prediction", CO2o, "0.9928 +- 0.0239 (-0.30 sigma) PASS | 0.9929 +- 0.0239 (-0.30 sigma) PASS"),
 ("from $-1.66$/$-1.89$ unpinned", CO2r, "(-0.30 sigma; unpinned -1.66)"),
 ("from $-1.66$/$-1.89$ unpinned", CO2r, "(-0.30 sigma; unpinned -1.89)"),
 ("DESI DR1 $f\\sigma_8$ passes ($\\chi^2$ 1.95 over four bins)", CO2o, "1.95 / 2.14 PASS | 1.95 / 2.14 PASS"),
 ("DESI DR1 $f\\sigma_8$ passes ($\\chi^2$ 1.95 over four bins)", CO2r, "BGS 0.483 (+1.13 / +0.98), LRG1 0.484 (-0.49 / -1.03), LRG2 0.471 (-0.20 / -0.14), LRG3 0.449 (+0.62 / +0.31); chi2 1.95 / 2.14 -> PASS"),
 ("on the record's gravity-only run moved by the run's own response", CO2c, "*Amplitude move, primary: the run's own response.*"),
 ("reads $\\chi^2$ 157.89/159.35 on 104 points", CO2o, "chi2 157.89, p 2.58e-03 EXCLUDED AT 3 SIGMA | chi2 159.35, p 2.12e-03 EXCLUDED AT 3 SIGMA"),
 ("reads $\\chi^2$ 157.89/159.35 on 104 points", CO2s, "104 KiDS points"),
 ("just below the frozen 3$\\sigma$ line of 0.0027", CO2c, "p < 0.0027 EXCLUDED AT 3 SIGMA"),
 ("the same row reads $p=0.0044$/0.0037, tension and not exclusion", CO2o, "chi2 153.74, p 4.42e-03 | chi2 155.04, p 3.73e-03"),
 ("the same row reads $p=0.0044$/0.0037, tension and not exclusion", CO2c, "0.0027 <= p < 0.05 TENSION"),
 ("the reference run alone at the same amplitude reads $\\chi^2$ 156.88/156.85", CO2o, "156.88 / 156.18 | 156.85 / 156.16"),
 ("with the neutrino bracket $p=0.0090$/0.0077", CO2o, "sigma8 0.8152, p 8.96e-03 | sigma8 0.8152, p 7.72e-03"),
 ("with one 0.06\\,eV neutrino (a bracket at the pinned parameters, not a refit)", CO2c, "this bracket is not a refit"),
 ("is best at $\\sigma_8=0.7358\\pm0.0162$/$0.7341\\pm0.0161$", CO2o, "0.7358 +- 0.0162 (p 0.147) | 0.7341 +- 0.0161 (p 0.152)"),
 ("the pinned value sits 5.62/5.78 widths above it", CO2o, "+5.62; +37.52 | +5.78; +39.36"),
 ("Unpinned, the same row reads $p=0.0004$/0.0002", CO2o, "chi2 170.95, p 3.98e-04 | chi2 175.47, p 2.00e-04"),
 ("DES Y3 through the same path reads $p=0.050$/0.051 (reported, not graded)", CO2o, "chi2 74.69, p 0.050 | chi2 74.67, p 0.051"),
 ("DES Y3 through the same path reads $p=0.050$/0.051 (reported, not graded)", CO2c, "DES Y3 through the same path"),
 ("a gravity-only run with nothing ejecting gas beyond $R_{200c}$, and the inherited halo list", CO2c, "for form B as stated, gravity-only S0, nothing ejecting gas beyond R200c; inherited halo list in R"),
 ("it is not peculiar to form B, and form B does not relieve it", CO2c, "it is not peculiar to form B, and form B does not relieve it"),
 ("are conventional but were chosen with CO1's numbers in view, which the lane states as a limit", CO2c, "they are chosen with those numbers in view; that is a limit of this lane"),
 ("Its one amendment, a known-answer tolerance, is post hoc and was committed before any graded number", CO2a, "CO2 AMENDMENT A1 (post hoc; committed alone, while the fits run and before any graded number exists)"),
 ("Its one amendment, a known-answer tolerance, is post hoc and was committed before any graded number", CO2a, "KA3's tolerance goes from 0.1 to 0.25"),
 ("absolute fit excluded at 3$\\sigma$ as frozen ($p=0.0026$/0.0021), tension once the reference run's realisation is corrected", CO2o, "chi2 157.89, p 2.58e-03 EXCLUDED AT 3 SIGMA | chi2 159.35, p 2.12e-03 EXCLUDED AT 3 SIGMA"),
 ("absolute fit excluded at 3$\\sigma$ as frozen ($p=0.0026$/0.0021), tension once the reference run's realisation is corrected", CO2R, "3 sigma as frozen, TENSION once the reference run's realisation is corrected"),
 ("raw KiDS prefers $\\sigma_8$ 0.736 against 0.827, 5.1 to 5.8 of its widths", CO2R, "raw KiDS-1000 is best at sigma8 **0.736 +- 0.016**"),
 ("raw KiDS prefers $\\sigma_8$ 0.736 against 0.827, 5.1 to 5.8 of its widths", CO2R, "The pinned fit gives 0.827"),
 ("raw KiDS prefers $\\sigma_8$ 0.736 against 0.827, 5.1 to 5.8 of its widths", CO2R, "The amplitude gap hardly moves: 5.1 to 5.8 widths"),
 ("the CMB pins $\\sigma_8$ at 0.8271 and raw KiDS prefers 0.736 for the form's spectrum, 5.1 to 5.8 of its widths lower", CO2o, "sigma8 (unpinned; S0 engine 0.811) | 0.8271 (0.8405)"),
 ("the CMB pins $\\sigma_8$ at 0.8271 and raw KiDS prefers 0.736 for the form's spectrum, 5.1 to 5.8 of its widths lower", CO2R, "That is 5.1 to 5.8 KiDS widths"),
 ("The weak-lensing amplitude is not solved", CO2R, "**Not solved:** the weak-lensing amplitude."),
 ("Form B states neither gas expelled from haloes nor neutrino mass", CO2R, "the usual ways out are gas expelled from haloes and neutrino mass, and form B states neither"),
 # CO2: the abstract's wording and the check made after grading
 ("With the amplitude of fluctuations pinned by large-angle polarisation, CMB lensing matches the prediction to 0.3$\\sigma$ and the growth rate passes", CO2R, "predicts the PR4 lensing power to 0.3 sigma"),
 ("prefers an amplitude five of its own widths lower", CO2R, "That is 5.1 to 5.8 KiDS widths"),
 ("the absolute fit is excluded at 3$\\sigma$ by the frozen line and reads tension once the reference run's realisation noise is corrected, a check made after grading", CO2R, "a check made after grading moves it to TENSION"),
 ("the form states neither gas ejection nor neutrino mass", CO2R, "the usual ways out are gas expelled from haloes and neutrino mass, and form B states neither"),
 ("as frozen, on both footings; not robust", CO2R, "The label is not robust"),
 ("CO2, below, pins the amplitude and finds that these absolute $p$-values carry the reference run's realisation noise", CO2R, "**CO1's absolute KiDS p values carry the same noise**"),
 ("$\\sigma_8$ is 0.8152 and the gap is 4.89/5.04 widths", CO2o, "sigma8 0.8152, p 8.96e-03 | sigma8 0.8152, p 7.72e-03"),
 ("$\\sigma_8$ is 0.8152 and the gap is 4.89/5.04 widths", CO2p, "pinned is +5.62 widths away (Delta chi2 +37.52), neutrino bracket +4.89"),
 ("$\\sigma_8$ is 0.8152 and the gap is 4.89/5.04 widths", CO2p, "pinned is +5.78 widths away (Delta chi2 +39.36), neutrino bracket +5.04"),
 ("The widths are KiDS's alone", CO2R, "The widths are KiDS's alone."),
 ("Across every variant below the gap is 5.1 to 5.8 widths, and the lane calls it its robust statement", CO2R, "The amplitude gap hardly moves: 5.1 to 5.8 widths"),
 ("Across every variant below the gap is 5.1 to 5.8 widths, and the lane calls it its robust statement", CO2R, "This gap is the robust statement."),
 ("The graded row is an absolute fit", CO2R, "An absolute fit does not, and P4 is an absolute fit."),
 ("The reference run is a single box of 100\\,Mpc/$h$ whose large-scale power is a high draw", CO2R, "the reference run is one box of 100 Mpc/h whose large-scale power is a high draw"),
 ("its starting spectrum is 1.48 times its own linear spectrum in its third bin", CO2R, "is 0.80, 1.03, **1.48**, 1.01, 1.06 in its first five bins"),
 ("its starting spectrum is 1.48 times its own linear spectrum in its third bin", CO2p, "k 0.197: 1.477"),
 ("A difference of two models on the same run cancels this; an absolute fit does not", CO2R, "A difference of two models on the same run (CO1's d_cold) cancels this."),
 ("(the run's own starting ratio with two tapers, and two 200\\,Mpc/$h$ runs below $k=0.5\\,h$\\,Mpc$^{-1}$)", CO2R, "| R1: divided by the run's own starting ratio (full to k 0.3, none above 1) | 0.0060 / 0.0049 | TENSION"),
 ("(the run's own starting ratio with two tapers, and two 200\\,Mpc/$h$ runs below $k=0.5\\,h$\\,Mpc$^{-1}$)", CO2R, "| R1b: the same, full to k 0.2, none above 0.5 | 0.0058 / 0.0047 | TENSION"),
 ("(the run's own starting ratio with two tapers, and two 200\\,Mpc/$h$ runs below $k=0.5\\,h$\\,Mpc$^{-1}$)", CO2R, "| R2: CFG411's 200 Mpc/h S0 run below k 0.5 | 0.0127 / 0.0102 | TENSION"),
 ("(the run's own starting ratio with two tapers, and two 200\\,Mpc/$h$ runs below $k=0.5\\,h$\\,Mpc$^{-1}$)", CO2R, "| R2b: CFG424's 200 Mpc/h S0 run (seed 360) below k 0.5 | 0.0042 / 0.0034 | TENSION"),
 ("$p$ is 0.003 to 0.013: tension each time", CO2R, "Every correction reads TENSION, with p from 0.003 to 0.013."),
 ("The check is post hoc, is reported and changes no label", CO2R, "## Post hoc: the reference run's realisation noise (co2_posthoc.py; reported, changes no label)"),
 ("the lane says it would not quote the exclusion without it", CO2R, "I would not quote the exclusion without the second half."),
 ("(its reference row, $p=0.014$, reads 0.021 to 0.049 corrected)", CO2R, "(its S0 row, p 0.014, reads 0.021 to 0.049 with the corrections)"),
 ("CO1's label rests on a difference and is not affected", CO2R, "CO1's label rests on d_cold, a difference, and is not affected."),
 ("the fit keeps massless neutrinos and the shear row uses 104 of the 225 published KiDS points", CO2R, "F1A's massless-neutrino setting is kept in the fit"),
 ("the fit keeps massless neutrinos and the shear row uses 104 of the 225 published KiDS points", CO2R, "104 of 225 published KiDS points"),
 ("the known answer passes the frozen tolerance too", CO2R, "It passes the frozen 0.1 too"),
 ("now that the CMB side is pinned: a refit that carries neutrino mass, in place of the bracket at fixed parameters", CO2R, "the neutrino row is a bracket at fixed parameters"),
 ("the shear row on more than one reference run, and on all of the published points", CO2R, "One reference run, gravity-only, 104 of 225 published KiDS points; the realisation noise above."),
 ("CO2's realisation check, which was made after grading", CO2R, "Found after P4 was graded."),
 ("put the optical depth at 0.055 to 0.060, $\\sigma_8$ near 0.828, PR4 lensing within 1$\\sigma$", CO2c, "tau 0.055 to 0.060; sigma8 about 0.828; PR4 lensing amplitude within 1 sigma of the prediction"),
 ("raw KiDS near the line between tension and exclusion", CO2c, "expected to be TENSION or EXCLUDED AT 3 SIGMA, near the line between them"),
 ("The optical depth came out just below that range (0.0532)", CO2o, "0.0532 +- 0.0066 (was 0.0697)"),
 ("CO2's low-multipole table is Planck 2018 and its high-multipole spectra are PR4", CO2c, "The low-L table is Planck 2018 (SimAll); the high-L spectra are PR4"),
 ("CO1's restated mutation arm, CO2's tolerance amendment", CO1, "the label above rests on AMENDMENT A1"),
 ("CO1's restated mutation arm, CO2's tolerance amendment", CO2a, "KA3's tolerance goes from 0.1 to 0.25"),
 ("which CO2's weak-lensing row reuses", CO2c, "form B's layout, CO1's `co1_hm.json`"),
 # gate table and open items
 ("FAIL, about 3$\\sigma$ with systematics", DEC, "about +3.0 to +3.5 with systematics"),
 ("Groups & not falsified (one-sided), $f_{\\rm ret}$ 0.597", RB1o, "median f_ret 0.597"),
 ("$w_0=I_0/4\\mu_K^2$", QX17, "w0 = I0/(4 mu_K^2)"),
 ("Our arithmetic, not a lane", RER, "w0 = 3 (H0/c)^2 Omega_c / (4 mu_K^2) = 1.063e-8 / mu_K^2 per Mpc^2 for H0 70 and Omega_c 0.26, which gives w = 1/2 at z 1089 for mu_K = 3.71 per Mpc"),
 ("$w=w_0/(w_0+a^3)$", QX17, "w = w0/(w0 + a^3), w0 = I0/(4 mu_K^2)"),
 ("the galaxy-lensing bound is 0.1", FB1, "the record's galaxy-lensing bound is mu_K at most 0.1 per Mpc"),
 ("needs $\\mu_K$ of 1.78/1.74 per Mpc, 17 to 18 times the galaxy bound", FB1, "the K(Q) dust needs mu_K 1.78 / 1.74 per Mpc to close it, 17 to 18 times the galaxy bound"),
 ("form B needs 40\\,\\% of their baryons to lie outside $R_{500}$", RB1, "The groups' f_ret of 0.60 at R500 says 40 % of the baryons"),
 ("need a host 17 to 100 times heavier than the form gives", RB2, "need a host 17 to 100 times heavier than B gives NGC 1052"),
 ("This is the spiral wall of the 2026-11-01 ledger", FB1, "This is the spiral wall of the 2026-11-01 ledger."),
 # what would decide it
 ("Form B needs $f_{\\rm ret}=1$ at turnaround; a census that falls short falsifies it", RB1, "B needs f_ret(<r_ta) = 1 exactly. A census that falls short at turnaround falsifies B."),
 ("A measured mass for NGC\\,1052 inside 79 and 165\\,kpc", RB2, "1.4e14 Msun inside 165 kpc"),
 ("A measured mass for NGC\\,1052 inside 79 and 165\\,kpc", RB2, "1.2e13 Msun inside 79 kpc"),
 ("is 0.68/0.62 of the law in KO1 and is forecast at 0.57/0.52 with such a veto, against about 0.47 needed", K3F, "| 1.6 R_h | 0.68 / 0.62 | 0.57 / 0.52 |"),
 ("is 0.68/0.62 of the law in KO1 and is forecast at 0.57/0.52 with such a veto, against about 0.47 needed", K3F, "A 3 sigma call needs about 0.47."),
 ("Gaia DR4 (2026-12-02), scored as pre-registered", DEC, "Gaia DR4 (2026-12-02): the pre-registration is unchanged and is scored as frozen."),
 # own estimates
 ("put the error on the disc ratio near 0.2", KO2, "The brief: late error near 0.2."),
 ("early types at 0.7 to 1.0", KO2, "Early 0.7 to 1.0"),
 ("A model-only toy at the freeze gave the brief's ratio about twice the error of its replacement (0.37 against 0.19)", KO2c, "0.37 on a[outer] / a[inner] (the brief's statistic) and 0.19 on the tied ratio R_ext"),
 ("measured an error of 0.278 on discs", KO2o, "late R +0.207 +- 0.274 (s_tot 0.278)"),
 ("The RB1 brief expected X-COP near 0.96; it reads 1.095", RB1, "X-COP about 0.96 at the last bin (1.095 on M_FORW"),
 ("RB2 expected M31's bright dwarfs to be borderline; they fail", RB2, "Bright M31 \"borderline\": MISS. It fails"),
 ("The Bullet estimate, closer than 2.6$\\sigma$ once the stripped gas is counted, held", RB1, "the Bullet closer than 2.6 sigma (right under S1 and S1/2, not under S0)"),
 ("so did the group range", RB1, "groups 0.5-0.9 (0.60, right)"),
 ("and the Coma shift", RB2, "Coma at the isolated +0.33 / +0.29, B CONSISTENT on main widths. HIT."),
 # method
 ("KO2's four amendments", KO2a4, "AMENDMENT"),
 ("the third, form B's prediction, was committed before any fitted amplitude was opened", KO2, "A3 was committed before any fitted amplitude was opened."),
 ("RB2 has no amendment", RB2, "No amendment."),
 ("fiducial flat background ($\\Omega_m$ 0.3, $H_0$ 70)", KO2c, "(flat, Omega_m 0.3, H0 70)"),
 ("one externally calibrated bracket in RB1 is labelled as such", RB1o, "bracket NFW Duffy (EXTERNALLY CALIBRATED)"),
 # ---------------- version 1.1 ----------------
 # header
 ("version 1.1, 2026-11-10 (v1.0: DOI 10.5281/zenodo.24106867)", P + "PAPER72_law_with_cold_dark_energy_counted_once_2026.zenodo.json", "\"doi\": \"10.5281/zenodo.24106867\""),
 # abstract
 ("states the theory in six rules (Section~7)", THY, "6. **The joint.** How a falling clock becomes a standing one is NOT derived."),
 ("The collapse was computed and breaks down: a clock that starts as dust folds at the centre, and the equations give no answer beyond that moment", COL1, "**BREAKS DOWN / BREAKS DOWN** (canonical / alt)"),
 ("The collapse was computed and breaks down: a clock that starts as dust folds at the centre, and the equations give no answer beyond that moment", COL1, "equations give no answer beyond that moment."),
 ("The static state is stable around isolated discs away from their centres; a disc in an external field has no verdict, with stability excluded there, and a disc's own centre is open", SCS2, "| **STABLE / STABLE** | D.P > 0 in every cell, on both grids. No growing mode on either route. |"),
 ("The static state is stable around isolated discs away from their centres; a disc in an external field has no verdict, with stability excluded there, and a disc's own centre is open", SCS2, "| External field along the axis (0.01 and 0.1 a0; 2D) | **NO VERDICT / NO VERDICT** |"),
 ("No dust term tried, keyed on the clock's offset, on its expansion or on its acceleration, joins the falling state to the standing one", THY, "So no dust term built from the clock's own first-order kinematics, its offset, its expansion or its acceleration, joins the two states."),
 ("the clock's leafwise flux cannot supply the halo", LFS1, "**Answer: no.** In action (A) the leafwise flux is not a separate supply."),
 ("the action has no cluster state at the form's own dust constant", CLS1, "**At form B's own mu_K (>= 198.25 per Mpc): NO STATE / NO STATE, proven on all seven clusters.**"),
 ("A survey of media with more structure than one clock finds no class without a failing verdict", MED, "only that every class named here has a failing verdict"),
 ("most of the weak-lensing gap was the survey's superseded release and our own inputs", KL1, "1. **The survey's own release: the largest single piece.**"),
 ("most of the weak-lensing gap was the survey's superseded release and our own inputs", KL1, "2. **Our massless neutrinos: the largest piece on our side.**"),
 ("the form's amplitude sits 1.71/1.88 of the survey's widths high with an acceptable fit", KL1, "| KiDS-Legacy | **1.71 / 1.88** (2.06 / 2.23 with ln det) | 0.26 / 0.24 | **CONSISTENT** |"),
 ("while DES Y3 stays at 2.18/2.23 on a re-scanned fit", KL1, "| DES Y3, polished scan | **2.18 / 2.23** | 0.28 | **GAP STAYS** |"),
 ("These readings rest on post hoc amendments: the lane's amended label is GAP STAYS and its frozen labels are NO VERDICT", KL1, "**Under AMENDMENTS C1 + C2 + C3 (post hoc): GAP STAYS / GAP STAYS, driven by DES Y3.**"),
 ("The two failing dwarf classes do not survive the record's own systematics budget", DG1, "**Part A outcome: neither FAILS HIGH survives, on either footing.**"),
 ("and a gas-history reading does not explain them", DG1, "| **Lane label (history)** | **HISTORY DOES NOT CLOSE THEM** | **HISTORY DOES NOT CLOSE THEM** |"),
 ("The form's data rows are computed without the joint between its two states, and several of them fail or have no verdict. The form is not complete.", THY, "The theory is predictive without the joint: every row of section 2 is computed from rules 3 to 5. It is not complete,"),
 # section 2: SCS2 and SCS3
 ("Version 1.1: lane SCS2 analysed discs. Isolated discs (razor-thin exponential and Kuzmin at four masses, a thick disc, a disc with a bulge) are STABLE on both footings", SCS2, "razor-thin exponential and Kuzmin at log M_b 9.4, 10.45, 10.7, 10.9; thick disc; disc + bulge"),
 ("Version 1.1: lane SCS2 analysed discs. Isolated discs (razor-thin exponential and Kuzmin at four masses, a thick disc, a disc with a bulge) are STABLE on both footings", SCS2, "| **STABLE / STABLE** |"),
 ("$D\\!\\cdot\\!P$ is positive in every cell on both grids and no mode grows on either route", SCS2, "D.P > 0 in every cell, on both grids. No growing mode on either route."),
 ("With a uniform external field along the axis or in the plane the label is NO VERDICT on both footings", SCS2, "| External field along the axis (0.01 and 0.1 a0; 2D) | **NO VERDICT / NO VERDICT** |"),
 ("With a uniform external field along the axis or in the plane the label is NO VERDICT on both footings", SCS2, "| External field in the plane (0.01 and 0.1 a0; 3D, one grid) | **NO VERDICT / NO VERDICT** |"),
 ("both routes find unstable regions, and the magnitudes are not converged or rest on one grid", SCS2, "Unstable in regions on both routes and both grids. The magnitudes are not converged."),
 ("both routes find unstable regions, and the magnitudes are not converged or rest on one grid", SCS2, "Unstable in regions on both routes. There is only one grid."),
 ("Lane SCS3 took the external-field case alone and also returns NO VERDICT on both footings", SCS3, "# SCS3 RESULT: is the static clock stable around a disc in a uniform external field?"),
 ("Lane SCS3 took the external-field case alone and also returns NO VERDICT on both footings", SCS3, "| External field along the axis (2D; 0.01 and 0.1 a0) | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | **NO VERDICT / NO VERDICT** |"),
 ("Lane SCS3 took the external-field case alone and also returns NO VERDICT on both footings", SCS3, "| External field in the plane (3D; 0.01 and 0.1 a0) | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | **NO VERDICT / NO VERDICT** |"),
 ("Extended spherical distributions remain unanalysed", SCS, "Extended spherical baryon distributions were not run either."),
 # gate table
 ("BREAKS DOWN (version 1.1): the falling clock folds at the centre and the equations give no answer beyond", COL1, "**BREAKS DOWN / BREAKS DOWN** (canonical / alt)"),
 ("BREAKS DOWN (version 1.1): the falling clock folds at the centre and the equations give no answer beyond", COL1, "the innermost clock shells reach the centre together and fold there: a caustic."),
 ("NO VALUE for a quadratic and for an exponential term", MK1, "**NO VALUE / NO VALUE.** With the quadratic K(Q) of action (A)"),
 ("NO VALUE for a quadratic and for an exponential term", MK2, "**NO VALUE / NO VALUE.** With L_K(Q) = (n_* x_T/K) exp((Q - 1)/x_T) in action (A)"),
 ("keyed on the expansion BREAKS AT TURNAROUND", TK1, "**Label, canonical and alt: BREAKS AT TURNAROUND.**"),
 ("keyed on the acceleration BREAKS AT A1", AKD1, "**Label, canonical and alt: BREAKS AT A1** (NOT WELL-POSED AROUND FRW)."),
 # what stays open, item 1 (COL1, FLD1, REL1, LFS1)
 ("Version 1.1: lane COL1 computed it and labels it BREAKS DOWN on both footings", COL1, "**BREAKS DOWN / BREAKS DOWN** (canonical / alt)"),
 ("A clock that starts as cold dust in the Hubble flow at $z=10$ around a baryon point mass", COL1, "The clock starts as cold dust in Hubble flow at z = 10 and a baryon point mass"),
 ("folds at the centre within 0.063 to 0.154\\,Gyr", COL1, "Within 0.063 to 0.154 Gyr the innermost clock shells reach the centre together and fold there"),
 ("at the three dust constants its brief asked for and at all four masses", COL1, "at every mu_K the brief asked for: 3.71, 1.78 / 1.74 and 0.1 per Mpc, at all four masses"),
 ("and the equations give no answer beyond that moment; one of its known answers fails, so its law-off rows and one bracket are NO VERDICT", COL1, "KA3 (the law-off polytrope) fails at its innermost shell, so the law-off rows (MUTATE M1) and the mu_K 198 bracket are NO VERDICT (A3)."),
 ("Lane FLD1 (DOES NOT on both footings)", FLD1, "**DOES NOT / DOES NOT** (canonical / alt). Every known answer passes."),
 ("holds every SPARC galaxy's last measured radius (175 of 175)", FLD1, "The folded region holds every SPARC galaxy's last measured radius (175 of 175;"),
 ("every galaxy of the high-redshift sample on disk at its stated extent (100 of 100)", FLD1, "at 2.2 R_e and at 4 R_e (100 of 100;"),
 ("stops 1.3 to 5.4 times short of the KiDS windows", FLD1, "lies 1.3 to 2.3 times beyond"),
 ("stops 1.3 to 5.4 times short of the KiDS windows", FLD1, "the middle window's edge 3.1 to 5.4 times beyond"),
 ("stops 1.3 to 5.4 times short of the KiDS windows", F + "README.md", "1.3 to 5.4 times short of KiDS's windows"),
 ("1.1 to 4.2 times short of the form's own cap (canonical)", FLD1, "lies 1.1 to 4.2 times beyond R_fold(0) for log M_b 8 to 11.5 (canonical; alt 1.0 to 3.8)"),
 ("Lane REL1 tried the law on the clock's acceleration relative to the baryons: NOT WELL-DEFINED", REL1, "**Label, canonical and alt: NOT WELL-DEFINED.**"),
 ("since matter's equation of motion becomes fourth order", REL1, "That turns the baryons' equation of motion from second order into fourth order"),
 ("Lane LFS1 asked whether the clock's leafwise flux can supply the halo: ILL-POSED, and the answer is no; the flux adds no charge", LFS1, "**Label, canonical and alt: ILL-POSED.**"),
 ("Lane LFS1 asked whether the clock's leafwise flux can supply the halo: ILL-POSED, and the answer is no; the flux adds no charge", LFS1, "it adds no charge."),
 # item 2
 ("Version 1.1: isolated discs are stable too away from their centres (SCS2)", SCS2, "Form B's static state around an isolated disc is linearly stable with gravity coupled."),
 ("A disc in a uniform external field, where the law's phantom density is negative in places, has no verdict (SCS2, SCS3)", SCS2, "Negative phantom density, and with it growth, appears only when a uniform external field is imposed."),
 ("A disc in a uniform external field, where the law's phantom density is negative in places, has no verdict (SCS2, SCS3)", SCS3, "| **NO VERDICT / NO VERDICT** | UNSTABLE on 11 of 16 / 10 of 16 backgrounds |"),
 # item 3 (MK1, MK2, TK1, AKD1)
 ("Version 1.1: lane MK1 labels the question NO VALUE on both footings", MK1, "# MK1 RESULT: one dust constant mu_K? NO VALUE / NO VALUE (canonical / alt)."),
 ("The CMB needs $\\mu_K$ of at least 198 per Mpc for the component to be cold by $z=3400$", MK1, "It needs >= 198 just for the component to be cold by z 3400"),
 ("and $2.51\\times10^{4}$ for its lensing shape", MK1, "The CMB needs mu_K >= 2.51e4 per Mpc for its lensing shape"),
 ("far above anything the galaxy rows allow", MK1, "Every galaxy, group and Solar-System row ends far below that."),
 ("Lane MK2 returns NO VALUE for an exponential dust term (as frozen NO VALUE/NO VERDICT)", MK2, "# MK2 RESULT: the exponential dust term. NO VALUE / NO VALUE (canonical / alt). As frozen: NO VALUE / NO VERDICT"),
 ("A stiffness keyed on the clock's expansion BREAKS AT TURNAROUND (TK1)", TK1, "# TK1 RESULT: dust stiffness keyed on the clock's expansion theta (2026-11-10)"),
 ("A stiffness keyed on the clock's expansion BREAKS AT TURNAROUND (TK1)", TK1, "**Label, canonical and alt: BREAKS AT TURNAROUND.**"),
 ("one that falls with the clock's acceleration BREAKS AT A1 (AKD1)", AKD1, "The key must make the stiffness fall with A, so M_2'(0) < 0."),
 ("one that falls with the clock's acceleration BREAKS AT A1 (AKD1)", AKD1, "**Label, canonical and alt: BREAKS AT A1**"),
 # item 4 (CLS1)
 ("Lane CLS1 searched the action for a cluster state. As frozen its label is STATE EXISTS-PARTIAL, with 0 of 7 clusters holding a state", CLS1, "**Label, canonical and alt: STATE EXISTS-PARTIAL / STATE EXISTS-PARTIAL as frozen. 0 of 7 clusters have a state.**"),
 ("at the form's own dust constant (198.25 per Mpc and above) it is NO STATE on both footings, proven on all seven", CLS1, "**At form B's own mu_K (>= 198.25 per Mpc): NO STATE / NO STATE, proven on all seven clusters.**"),
 # item 5 (GO1)
 ("Version 1.1: lane GO1 tried the census in group outskirts and is NOT EVALUABLE: the lensing on disk does not reach the turnaround radius", GO1, "# GO1 RESULT: NOT EVALUABLE [r_ta NOT REACHED] / NOT EVALUABLE [r_ta NOT REACHED]. Form B's turnaround census is not reached by KiDS-1000"),
 ("Version 1.1: lane GO1 tried the census in group outskirts and is NOT EVALUABLE: the lensing on disk does not reach the turnaround radius", GO1, "So the turnaround radius is not located"),
 # item 6 (XCV1)
 ("Version 1.1: lane XCV1 regraded X-COP with a mass that does not assume hydrostatic equilibrium: NO VERDICT as frozen, since a known answer fails", XCV1, "| **frozen** | **NO VERDICT** (KA-3 failed) | **NO VERDICT** |"),
 ("Version 1.1: lane XCV1 regraded X-COP with a mass that does not assume hydrostatic equilibrium: NO VERDICT as frozen, since a known answer fails", XCV1, "The caustic mass assumes no hydrostatic equilibrium and no gas physics."),
 ("under its post hoc amendment the class is AT THE CEILING with the central value above it", XCV1, "Under the post-hoc A1: AT THE CEILING / AT THE CEILING, central value above it."),
 # item 8 (DG1)
 ("Version 1.1: with the record's systematics budget and the dispersion upper limits counted, neither class's interval excludes zero (DG1); the medians stay high", DG1, "Then both intervals contain 0, on both footings."),
 ("Version 1.1: with the record's systematics budget and the dispersion upper limits counted, neither class's interval excludes zero (DG1); the medians stay high", DG1, "It is not a pass: every median stays high."),
 # item 9 (NH2)
 ("Version 1.1: lane NH2 set NGC\\,1052's measured mass against that need: NO VERDICT as frozen, since two known answers fail", NH2, "**Label as frozen: NO VERDICT / NO VERDICT** (canonical / alt). Two known answers fail"),
 ("under its post hoc reading tides cannot reach DF4 and DF2 is not decided", NH2, "**DF4: TIDES CANNOT REACH / TIDES CANNOT REACH**"),
 ("under its post hoc reading tides cannot reach DF4 and DF2 is not decided", NH2, "**DF2: NOT DECIDED / NOT DECIDED.**"),
 ("under its post hoc reading tides cannot reach DF4 and DF2 is not decided", NH2, "## Post hoc reading A1 (named; not frozen)"),
 # item 12 (KL1)
 ("On the surveys' current data the gap is 1.71/1.88 widths on KiDS-Legacy, with an acceptable fit, and 2.18/2.23 on DES Y3 (2.89/2.82 on the frozen scan)", KL1, "Every survey's fit is acceptable."),
 ("On the surveys' current data the gap is 1.71/1.88 widths on KiDS-Legacy, with an acceptable fit, and 2.18/2.23 on DES Y3 (2.89/2.82 on the frozen scan)", KL1, "| KiDS-Legacy | **1.71 / 1.88** (2.06 / 2.23 with ln det) | 0.26 / 0.24 | **CONSISTENT** |"),
 ("On the surveys' current data the gap is 1.71/1.88 widths on KiDS-Legacy, with an acceptable fit, and 2.18/2.23 on DES Y3 (2.89/2.82 on the frozen scan)", KL1, "| DES Y3, polished scan | **2.18 / 2.23** | 0.28 | **GAP STAYS** |"),
 ("the amended label is GAP STAYS and the frozen labels are NO VERDICT", KL1, "- **As frozen: NO VERDICT / NO VERDICT.** The MUTATE arm MA2 could not bite on DES Y3."),
 ("the amended label is GAP STAYS and the frozen labels are NO VERDICT", KL1, "- **As frozen: NO VERDICT / NO VERDICT.** The MUTATE arm MC1 does not bite."),
 # what would decide it
 ("was computed in version 1.1 and breaks down (COL1)", COL1, "**BREAKS DOWN / BREAKS DOWN** (canonical / alt)"),
 ("What would decide the joint now is an equation for what the clock is behind a fold", COL1, "**Anything after the first caustic.** The equations give no answer there. A completion needs a new term or a new"),
 ("KL1 made the refit and put the measured gas in", KL1, "A real refit of CO2's CMB fit with the 0.06 eV floor"),
 ("KL1 made the refit and put the measured gas in", KL1, "4. **The gas RB1 measured: worth about 0.3 widths, less than I expected.**"),
 ("it finds the single reference run to be the limiting input", KL1, "The single box is now the limiting assumption, not the surveys'."),
 # section 7: intro and re-runs
 ("The closure session re-ran DG1's main run (not its mutation twin), all three parts of KL1 and AKD1 from copies, and every label and stored number reproduced apart from run times and memory", RER2, "| `dg1.py` (the main run), one thread, 737 s, peak RSS 0.58 GB, exit 0 | Every label and every graded number reproduces"),
 ("The closure session re-ran DG1's main run (not its mutation twin), all three parts of KL1 and AKD1 from copies, and every label and stored number reproduced apart from run times and memory", RER2, "Every label and every stored number reproduces. Part A as frozen NO VERDICT"),
 ("The closure session re-ran DG1's main run (not its mutation twin), all three parts of KL1 and AKD1 from copies, and every label and stored number reproduced apart from run times and memory", RER2, "All 15,717 values in the twelve Part C JSON outputs are identical."),
 ("The closure session re-ran DG1's main run (not its mutation twin), all three parts of KL1 and AKD1 from copies, and every label and stored number reproduced apart from run times and memory", RER2, "Label reproduces: BREAKS AT A1 on both footings. All 2099 values in the nine JSON outputs are identical"),
 ("a re-run reproduces a lane's arithmetic and is not an independent derivation", RER2, "The KL1 re-runs reproduce the lane's arithmetic; they are not independent derivations"),
 ("KL1's second part was also regraded by lane KL1R, with the same labels", RER2, "Part B was also regraded blind by another session"),
 ("KL1's second part was also regraded by lane KL1R, with the same labels", KL1R, "**The labels agree:** frozen NO VERDICT / NO VERDICT, for the same"),
 ("for the lanes under \\texttt{fable52\\_push/}, what their lead session checked is recorded in that folder's \\texttt{README.md}", F + "README.md", "checked by the lead: all 88 backgrounds re-solved from scratch"),
 # the six rules
 ("\\textbf{Fields.} The metric, one clock field that picks a slicing, and a polarization on its slices. Matter couples to the metric only.", THY, "**Fields.** The metric, one clock field tau (a preferred slicing with unit normal n), and a polarization vector P on the clock's slices. Matter couples to the metric only."),
 ("The clock equation is a conserved current. The universe carries 5.41 units of its charge per unit of baryons, a fitted number.", THY, "The clock equation is a conserved current."),
 ("The clock equation is a conserved current. The universe carries 5.41 units of its charge per unit of baryons, a fitted number.", THY, "The universe carries 5.41 units of it per unit of baryons (fitted to the acoustic peaks)."),
 ("Where the clock free-falls with the expansion the charge is cold dust. This is the cold component of cosmology.", THY, "Where the clock free-falls with the expansion, P = 0 and N is pressureless. This is the cold component of cosmology."),
 ("Where the clock stands still around baryons its own equations give the law, with $a_0=\\tfrac12c\\sqrt{G\\rho_{\\rm DE}}$", THY, "a0 = (1/2) c sqrt(G rho_DE)"),
 ("The halo is the charge itself and gravitates and lenses as mass.", THY, "the halo is the charge itself"),
 ("A hot system holds 5.41 times the baryons that fell into it. A body that brought no charge has no halo.", THY, "for a hot system 5.41 times the baryons that fell in (RB1)"),
 ("A hot system holds 5.41 times the baryons that fell into it. A body that brought no charge has no halo.", THY, "A body that brought no charge has no halo"),
 ("How a falling clock becomes a standing one is not derived.", THY, "How a falling clock becomes a standing one is NOT derived."),
 ("The data rows of this note are computed from rules 3 to 5, and several of them fail or have no verdict.", THY, "every row of section 2 is computed from rules 3 to 5"),
 ("the hot branch of rule 5 is a rule and not a solution of the action", THY, "rule 5's hot branch is not a solution at all"),
 # what the landed verdicts force on the joint
 ("\\textbf{Not a wall at a fixed place.} HE1 FAILS, and PAPER71's switch class is closed.", HE1, "**HE1: FAILS / FAILS** (canonical / alt)"),
 ("\\textbf{Not a wall at a fixed place.} HE1 FAILS, and PAPER71's switch class is closed.", F + "README.md", "now every action-based switch as a class"),
 ("MK1 and MK2 return NO VALUE (Section~5, item 3)", MK1, "**NO VALUE / NO VALUE.**"),
 ("MK1 and MK2 return NO VALUE (Section~5, item 3)", MK2, "**NO VALUE / NO VALUE.**"),
 ("The offset is about $10^{-6}$ both in the background at $z=3400$ and in a galaxy's well today.", MK1, "The clock offset Q - 1 is about 1e-6 both in the expanding background at z 3400 and in a galaxy well today."),
 ("Lane TK1 keyed the dust stiffness on the clock's expansion: BREAKS AT TURNAROUND", TK1, "**Label, canonical and alt: BREAKS AT TURNAROUND.**"),
 ("The key keeps the expanding background well posed, with a margin of 1.19 on the Jeans line.", TK1, "the action stays well posed around FRW, and the dust is"),
 ("The key keeps the expanding background well posed, with a margin of 1.19 on the Jeans line.", TK1, "Jeans line met with a margin of 1.19"),
 ("there short waves grow without bound, 2 to 140\\,Myr before the turnaround, and the region never turns around", TK1, "the new term's k^4 piece makes short waves grow without bound."),
 ("there short waves grow without bound, 2 to 140\\,Myr before the turnaround, and the region never turns around", TK1, "This happens 2 to 140 Myr before the GR turnaround on the primary values"),
 ("there short waves grow without bound, 2 to 140\\,Myr before the turnaround, and the region never turns around", TK1, "Then the region does not turn around at all."),
 ("Lane AKD1: BREAKS AT A1. The key is a negative copy of the law's own term.", AKD1, "**Label, canonical and alt: BREAKS AT A1**"),
 ("Lane AKD1: BREAKS AT A1. The key is a negative copy of the law's own term.", AKD1, "a negative copy of the law's own term"),
 ("Its weight against the law is $3.9\\times10^{14}$/$4.2\\times10^{14}$ at $z=3400$ and $4.5\\times10^{11}$/$4.9\\times10^{11}$ at $z=1100$", AKD1, "R is 3.9e14 / 4.2e14 at z 3400 and 4.5e11 / 4.9e11 at z 1100."),
 ("so the clock's inertia is negative on every sub-horizon scale there, until $z=11.6$/11.4", AKD1, "**negative on every sub-horizon scale: a ghost**"),
 ("so the clock's inertia is negative on every sub-horizon scale there, until $z=11.6$/11.4", AKD1, "The ghost lasts until z 11.6 / 11.4, where R falls through 1."),
 ("A shape that is flat at zero acceleration has the same sign problem in the outskirts of static wells; that is a reported class bound and not a label.", AKD1, "A shape that is flat at Y = 0 escapes the cosmological ghost but fails there."),
 ("Not the law on the clock's acceleration relative to the baryons.} REL1: NOT WELL-DEFINED.", REL1, "**Label, canonical and alt: NOT WELL-DEFINED.**"),
 ("COL1: BREAKS DOWN. Nothing in the action removes the infall energy.", COL1, "Nothing in action (A) removes infall energy."),
 ("It has to reach further than today's fold.} FLD1: DOES NOT.", FLD1, "**DOES NOT / DOES NOT** (canonical / alt)."),
 ("LFS1: ILL-POSED. CLS1: NO STATE at the form's own dust constant.", LFS1, "**Label, canonical and alt: ILL-POSED.**"),
 ("LFS1: ILL-POSED. CLS1: NO STATE at the form's own dust constant.", CLS1, "**At form B's own mu_K (>= 198.25 per Mpc): NO STATE / NO STATE, proven on all seven clusters.**"),
 ("So no dust term tried that is built from the clock's own first-order kinematics, its offset, its expansion or its acceleration, joins the two states.", THY, "So no dust term built from the clock's own first-order kinematics, its offset, its expansion or its acceleration, joins the two states."),
 # media with more structure than one clock
 ("which is not a lane, sets the classes of medium the record has tried against four properties the data ask for", MED, "A design note, not a lane: no criteria, no label, nothing graded."),
 ("conserved and cold; passing through itself; hot and at full share in clusters; locked to the baryons in galaxies", MED, "| Conserved, and cold in the expanding universe at 5.41 times the baryons |"),
 ("conserved and cold; passing through itself; hot and at full share in clusters; locked to the baryons in galaxies", MED, "| Passes through itself and through gas |"),
 ("conserved and cold; passing through itself; hot and at full share in clusters; locked to the baryons in galaxies", MED, "| Hot and at full share in clusters |"),
 ("conserved and cold; passing through itself; hot and at full share in clusters; locked to the baryons in galaxies", MED, "| Locked to the baryons in galaxies, with no second halo beside the law |"),
 ("any local, momentum-conserving, normally self-gravitating medium whose equilibrium is the law (M5: NO-GO, a theorem)", M5, "## Verdict: NO-GO for every candidate (theorem)."),
 ("two phases (PH1: NO-GO)", PH1, "## Verdict (frozen §0): NO-GO"),
 ("a superfluid with phonons (QX28: FAILS at G3, G4, G5, G6 and G8)", QX28, "FAILS at G3, G4, G5, G6 and G8"),
 ("a self-interacting isothermal inner halo (IJ1: FAILS)", IJ1, "RESULT: IJ FAILS (both footings)"),
 ("a light fermion beside the law (HF1: fails its first gate at 5 of 6 masses with 1 undetermined; the lane says this kills the family on its inputs and is not a no-go theorem)", HF1, "FAILS GATE 1 AT 5 OF 6 m, 1 UNDETERMINED"),
 ("a warm component beside it (WM1: FAIL AT SEEDING, a gate added after its first result, which failed on groups)", WM1, "# WM1 RESULT: FAIL AT SEEDING / FAIL AT SEEDING"),
 ("the tethered medium (TM1: it does not resolve law against clumping, and its scored rows fail or are conditional)", TM1, "It does not resolve law versus clumping"),
 ("its scored rows fail or are conditional", TM1, "**CONDITIONAL** (on catchment, C)"),
 ("its scored rows fail or are conditional", TM1, "**CONDITIONAL** (on settling, S)"),
 ("nonlocal, history and global actions (FA3: no candidate survives)", FA3, "No candidate survives"),
 ("Route E, in which cold dark energy clumps everywhere, gravity is Newtonian and the law is emergent, had its cold sector retired by the owner on 2026-11-01.", RETIRE, "# Owner decision, 2026-11-01: route E's cold sector is retired"),
 ("Route E, in which cold dark energy clumps everywhere, gravity is Newtonian and the law is emergent, had its cold sector retired by the owner on 2026-11-01.", MED, "| The law as an emergent regularity of ordinary cold halos (route E) | retired by the owner on 2026-11-01"),
 ("One class had no lane: a medium in thermal contact with the baryons where their acceleration exceeds $a_0$.", MED, "thermal contact with the baryons only where their acceleration exceeds a0"),
 ("One class had no lane: a medium in thermal contact with the baryons where their acceleration exceeds $a_0$.", MED, "A search found no lane on a medium coupled to the baryons."),
 ("The note works it out as our own arithmetic, not a graded result.", MED, "These are hand estimates with stated inputs, not a Boltzmann computation and not a lane."),
 ("The contact needs an opacity $\\pi G/a_0$ of 22.4/18.5\\,cm$^2$\\,g$^{-1}$", MED, "kappa = pi G / a0 = 22.4 / 18.5 cm^2/g"),
 ("The contact needs an opacity $\\pi G/a_0$ of 22.4/18.5\\,cm$^2$\\,g$^{-1}$", MEDo, "opacity pi G / a0 = 2.240 m^2/kg = 22.4 cm^2/g"),
 ("The contact needs an opacity $\\pi G/a_0$ of 22.4/18.5\\,cm$^2$\\,g$^{-1}$", MEDo, "opacity pi G / a0 = 1.854 m^2/kg = 18.5 cm^2/g"),
 ("mean free path against baryons at $z=1100$ is 25.8/31.1\\,pc", MEDo, "z 1100: baryon density 5.61e-19 kg/m^3; mean free path 25.8 pc"),
 ("mean free path against baryons at $z=1100$ is 25.8/31.1\\,pc", MEDo, "z 1100: baryon density 5.61e-19 kg/m^3; mean free path 31.1 pc"),
 ("its drag at a relative speed of 30\\,km\\,s$^{-1}$ is 0.73/0.61 of the expansion rate, so it does not stay decoupled from the plasma", MEDo, "drag rate at a relative speed of 30 km/s: 0.73 of the expansion rate"),
 ("its drag at a relative speed of 30\\,km\\,s$^{-1}$ is 0.73/0.61 of the expansion rate, so it does not stay decoupled from the plasma", MEDo, "drag rate at a relative speed of 30 km/s: 0.61 of the expansion rate"),
 ("its drag at a relative speed of 30\\,km\\,s$^{-1}$ is 0.73/0.61 of the expansion rate, so it does not stay decoupled from the plasma", MED, "The cold component that fits the acoustic peaks has to stay decoupled from the plasma. This one does not."),
 ("a cluster's gas is 0.14 to 0.68 optical depths (canonical), so it would be dragged with the Bullet's gas", MEDo, "gas column n_e 0.01 cm^-3 over 500 kpc: 0.0302 g/cm^2 -> optical depth 0.68"),
 ("a cluster's gas is 0.14 to 0.68 optical depths (canonical), so it would be dragged with the Bullet's gas", MEDo, "gas column n_e 0.001 cm^-3 over 1000 kpc: 0.0060 g/cm^2 -> optical depth 0.14"),
 ("a cluster's gas is 0.14 to 0.68 optical depths (canonical), so it would be dragged with the Bullet's gas", MED, "The medium would be dragged with the gas"),
 # the data rows since version 1.0: KL1 and KL1R
 ("CO2's gap of 5.62/5.78 KiDS-1000 widths came apart into pieces", KL1, "| 0.0026 / 0.0021 | EXCLUDED AT 3 SIGMA | 0.7358 / 0.7341 +- 0.016 | 5.62 / 5.78 |"),
 ("The largest is the survey's own release", KL1, "1. **The survey's own release: the largest single piece.**"),
 ("KiDS-Legacy prefers $\\sigma_8=0.7767$/0.7748 where KiDS-1000 preferred 0.7358/0.7341", KL1, "| B0 CO2's target 0.8271 | 215.56 / 218.01 | 0.025 / 0.020 | TENSION | 0.7767 / 0.7748 +- 0.0115 | 4.40 / 4.60 |"),
 ("KiDS-Legacy prefers $\\sigma_8=0.7767$/0.7748 where KiDS-1000 preferred 0.7358/0.7341", KL1, "| A0 CO2 (sigma8 0.8271) | 157.89 / 159.35 | 0.0026 / 0.0021 | EXCLUDED AT 3 SIGMA | 0.7358 / 0.7341 +- 0.016 |"),
 ("The largest on our side is the massless neutrinos: a refit of the CMB fit with one 0.06\\,eV neutrino gives $\\sigma_8=0.8121$/0.8120", KL1, "2. **Our massless neutrinos: the largest piece on our side.**"),
 ("The largest on our side is the massless neutrinos: a refit of the CMB fit with one 0.06\\,eV neutrino gives $\\sigma_8=0.8121$/0.8120", KL1, "A real refit of CO2's CMB fit with the 0.06 eV floor (not CO2's fixed-parameter row) gives sigma8 **0.8121 / 0.8120**."),
 ("The covariance evaluated at the model and the gas RB1 measured outside $R_{500}$ are smaller pieces", KL1, "3. **The covariance evaluated at the survey's fiducial: worth about 0.4 widths.**"),
 ("The covariance evaluated at the model and the gas RB1 measured outside $R_{500}$ are smaller pieces", KL1, "4. **The gas RB1 measured: worth about 0.3 widths, less than I expected.**"),
 ("As frozen, the lane's first two parts read NO VERDICT, because a mutation arm cannot bite on DES Y3", KL1, "- **As frozen: NO VERDICT / NO VERDICT.** The MUTATE arm MA2 could not bite on DES Y3."),
 ("Under a post hoc amendment, KiDS-1000 with DES Y3 reads TENSION (KiDS-1000 gap 3.95/4.06 widths)", KL1, "**TENSION / TENSION under A1**"),
 ("Under a post hoc amendment, KiDS-1000 with DES Y3 reads TENSION (KiDS-1000 gap 3.95/4.06 widths)", KL1, "KiDS-1000 at ALL: p 0.038 / 0.037, gap 3.95 / 4.06 KiDS-1000 widths."),
 ("KiDS-Legacy with DES Y3 reads AMPLITUDE CONSISTENT WITH RAW LENSING ($p=0.111$/0.101 for Legacy)", KL1, "- **Under AMENDMENT A1 (post hoc): AMPLITUDE CONSISTENT WITH RAW LENSING / AMPLITUDE CONSISTENT WITH RAW LENSING.**"),
 ("KiDS-Legacy with DES Y3 reads AMPLITUDE CONSISTENT WITH RAW LENSING ($p=0.111$/0.101 for Legacy)", KL1, "- KiDS-Legacy: p 0.111 / 0.101."),
 ("with Legacy still 2.13/2.30 of its widths below the form", KL1, "| **BALL** | **198.33 / 199.49** | **0.111 / 0.101** | **CONSISTENT** | 0.7875 / 0.7855 +- 0.0116 | **2.13 / 2.30** (ln det 2.50 / 2.70) |"),
 ("Lane KL1R, a regrade of that part by another session, returns the same two readings", KL1R, "# KL1R RESULT: blind, independent regrade of KL1 Part B"),
 ("Lane KL1R, a regrade of that part by another session, returns the same two readings", KL1R, "| Under amendment A1 (post hoc) | AMPLITUDE CONSISTENT WITH RAW LENSING | AMPLITUDE CONSISTENT WITH RAW LENSING |"),
 ("Lane KL1R, a regrade of that part by another session, returns the same two readings", KL1R, "| **Frozen (KL1 Part B + PB1, as written)** | **NO VERDICT** | **NO VERDICT** |"),
 ("With the reference run's known draw corrected and the cold component responding to the moved gas", KL1, "**The gate:** C0 (the box's draw corrected, R1) + C2 (the cold component's slow-loss response)"),
 ("under three post hoc amendments, GAP STAYS, driven by DES Y3", KL1, "- **Under AMENDMENTS C1 + C2 + C3 (post hoc): GAP STAYS / GAP STAYS, driven by DES Y3.**"),
 ("KiDS-Legacy 1.71/1.88 widths and consistent (2.06/2.23 with the full Gaussian likelihood)", KL1, "| KiDS-Legacy | **1.71 / 1.88** (2.06 / 2.23 with ln det) | 0.26 / 0.24 | **CONSISTENT** |"),
 ("KiDS-Legacy 1.71/1.88 widths and consistent (2.06/2.23 with the full Gaussian likelihood)", KL1, "(2.5 / 2.7 with the full Gaussian likelihood)"),
 ("DES Y3 2.18/2.23 on the polished scan (2.89/2.82 on the frozen scan), KiDS-1000 3.72/3.85", KL1, "| DES Y3, polished scan | **2.18 / 2.23** | 0.28 | **GAP STAYS** |"),
 ("DES Y3 2.18/2.23 on the polished scan (2.89/2.82 on the frozen scan), KiDS-1000 3.72/3.85", KL1, "| KiDS-1000 (reported) | 3.72 / 3.85 | 0.059 / 0.057 | GAP STAYS |"),
 ("Held to Legacy's own alignment model under its own prior, Legacy reads 1.57/1.83 and stays consistent", KL1, "Legacy reads\n  gap 1.57 / 1.83, p 0.25 / 0.24: CONSISTENT."),
 ("Gas taken from a stellar-mass-selected stack is a bracket and barely moves anything", KL1, "- **C1 (gas from the kSZ stack) is a BRACKET** by the frozen rule, and it barely moves anything."),
 ("The lane concludes that the remaining gap is the size of the reference run's realisation noise", KL1, "- **The remaining gap is now the size of our own model's realisation noise.**"),
 ("two independent 200\\,Mpc/$h$ runs spliced in at low $k$ put DES Y3 at 1.31/1.27 against 3.49/3.43 widths", KL1, "The two independent 200 Mpc/h runs, spliced in below k 0.5 (C0's edges R2 and R2b), put DES at 1.31 / 1.27 against 3.49 / 3.43 widths"),
 # DG1
 ("\\textbf{Hosted dwarfs (DG1): HISTORY DOES NOT CLOSE THEM on both footings.}", DG1, "| **Lane label (history)** | **HISTORY DOES NOT CLOSE THEM** | **HISTORY DOES NOT CLOSE THEM** |"),
 ("RB2's two failing classes rested on measurement scatter alone", DG1, "RB2's two FAILS HIGH rested on measurement scatter alone."),
 ("With the record's joint systematics budget re-derived for the form and the dispersion upper limits counted, both intervals contain zero on both footings", DG1, "Put the record's own joint budget on them (SE2's rule, re-derived for B) and count the dispersion upper limits the class left out. Then both intervals contain 0, on both footings."),
 ("the ultra-faints read $+0.550$ [$-0.090$, $+1.175$] (alt $+0.509$ [$-0.110$, $+1.141$])", DG1, "| **+0.550 [-0.090, +1.175]** (39, 9 limits) |"),
 ("the ultra-faints read $+0.550$ [$-0.090$, $+1.175$] (alt $+0.509$ [$-0.110$, $+1.141$])", DG1, "| **+0.509 [-0.110, +1.141]** |"),
 ("M31's bright dwarfs $+0.299$ [$-0.181$, $+0.774$] (alt $+0.258$ [$-0.237$, $+0.747$])", DG1, "| **+0.299 [-0.181, +0.774]** (22) |"),
 ("M31's bright dwarfs $+0.299$ [$-0.181$, $+0.774$] (alt $+0.258$ [$-0.237$, $+0.747$])", DG1, "| **+0.258 [-0.237, +0.747]** |"),
 ("this is the standing RB2 gave Coma's ultra-diffuse galaxies and not a pass", DG1, "the same standing RB2 gave the Coma UDGs. It is not a pass: every median stays high."),
 ("brings the class medians to $-0.045$, $+0.037$ and $-0.010$\\,dex", DG1, "| G1 MW ultra-faint (26): after history [before, same rows +0.584 / +0.546] | -0.045 [-0.242, +0.218]"),
 ("brings the class medians to $-0.045$, $+0.037$ and $-0.010$\\,dex", DG1, "| G1 bright M31 (10) [before +0.367 / +0.325] | +0.037 [-0.219, +0.257]"),
 ("brings the class medians to $-0.045$, $+0.037$ and $-0.010$\\,dex", DG1, "| G1 MW classical (8) [before +0.281 / +0.241] | -0.010 [-0.104, +0.202]"),
 ("and fails the per-galaxy gates: inside the ultra-faints the rank correlation of the residual with the predicted history is $+0.06$", DG1, "Inside the 26 ultra-faints, the rank correlation of the residual with the predicted history is +0.06"),
 ("and a two-number stellar-mass power law fits better (rms 0.306 against 0.343\\,dex)", DG1, "A two-number stellar-mass power law fits the graded residuals better than history does: rms 0.306 against 0.343 dex"),
 ("The lane is post hoc to RB2's class numbers and says so.", DG1, "Post hoc to RB2's class numbers"),
 # SHP1
 ("Its label is THE LAW'S SHAPE ON ROTATION CURVES, LENSING ABOVE; NOT ONE SHAPE (R3b) on both footings", SHP1, "**THE LAW'S SHAPE ON ROTATION CURVES, LENSING ABOVE; NOT ONE SHAPE (R3b)** / the same (canonical / alt)."),
 ("On rotation curves (2700 points in 149 galaxies) everything that is not baryons follows the law's shape in every bin at the standard mass-to-light ratios, the worst bin median within 0.057\\,dex", SHP1, "SPARC has 2700 points in 149 galaxies. The worst bin median is within 0.057 dex canonical"),
 ("On rotation curves (2700 points in 149 galaxies) everything that is not baryons follows the law's shape in every bin at the standard mass-to-light ratios, the worst bin median within 0.057\\,dex", SHP1, "**Rotation curves follow it in every bin.**"),
 ("KiDS isolated lenses have the same shape at $1.40\\pm0.03$/$1.28\\pm0.03$ times the law with the published stars only", SHP1, "KiDS isolated lenses (B21 as published) sit 1.40 +- 0.03 / 1.28 +- 0.03 times the law"),
 ("and sit below it with the published hot gas counted as baryons", SHP1, "With B21's hot gas counted as baryons they sit below instead"),
 ("A separate halo of PD1's 59.5\\,$M_b$ on top of the law is excluded on every reading", SHP1, "The record's full cosmic share, PD1's 59.5 M_b, is excluded on every reading"),
 # our own estimates (viii) to (xi)
 ("The closure session expected the survey's newer release to cut the weak-lensing gap from about five widths to one or two", KL1, "It expected the release to cut the gap from about 5 widths to 1 or 2."),
 ("and the neutrino floor, the covariance and the gas together to be worth about one more", KL1, "It expected A1 to A3 to be worth about 1 width."),
 ("The release cut the $\\sigma_8$ gap by about 45\\,\\% and left 4.4/4.6 of Legacy's narrower widths", KL1, "The release cut the sigma8 gap by about 45 % (0.091 -> 0.050), which is 4.4 / 4.6 in Legacy's narrower widths."),
 ("the three inputs were worth 2.3 more widths on Legacy and 1.7 on KiDS-1000", KL1, "They were worth 2.3 more widths on Legacy and 1.7 on KiDS-1000."),
 ("It expected gas from the stellar-mass-selected stack to be worth 0.5 to 1 widths; it was worth 0.05 to 0.09 and only a bracket", KL1, "C1 0.5 to 1: it was 0.05 to 0.09, and only a bracket."),
 ("DG1 found the class medians matched and the per-galaxy gates failed", DG1, "brings every graded class to zero"),
 ("DG1 found the class medians matched and the per-galaxy gates failed", DG1, "But it does not pick out which dwarfs are high."),
 ("It proposed the acceleration key and wrote that its gradient term had a healthy sign.", AKD1, "The closure chat's hand algebra had the sign the other way (\"a healthy-sign gradient term\")."),
 ("AKD1 found the sign the other way: the term is kinetic, with a negative coefficient", AKD1, "So |grad delta ln Q|^2 is a kinetic term, and with a negative coefficient it is negative inertia."),
 # method, version 1.1
 ("KL1's amendments A1, C1, C2 and C3, on which its readings other than NO VERDICT rest", KL1, "- **AMENDMENT_A1.md** (e01d1b9a35, post hoc, every label seen)"),
 ("KL1's amendments A1, C1, C2 and C3, on which its readings other than NO VERDICT rest", KL1, "### Part C amendments (all post hoc, each committed alone before the numbers it governs)"),
 ("DG1's amendment", DG1, "AMENDMENT_A1.md (443fedfd84, POST HOC, committed alone before the final run)"),
 ("TK1's, FLD1's and REL1's amendments", TK1, "AMENDMENT A1 813946cec9 / 175bea03be (post hoc, alone, before the graded A3 runs)"),
 ("TK1's, FLD1's and REL1's amendments", FLD1, "- **A1 is post hoc**: development runs at N = 600 on A4's grid showed the artefact."),
 ("TK1's, FLD1's and REL1's amendments", REL1, "AMENDMENT A1 96c0968d9e (post hoc,"),
 ("MK2's second, third and fourth amendments", MK2, "- A2 0fe15b8cbf, POST HOC: a global share cap."),
 ("MK2's second, third and fourth amendments", MK2, "- A3 19f958a654, POST HOC: KA4's groups leg checked with the cap off"),
 ("SCS2's second to fourth, SCS3's four and DCN1's six", SCS2, "A2 cb6ac0fe9a and A3 ac13205c89 (post hoc, before any graded route), A4 3cf66462aa (post hoc, after the graded frozen-fit route-1 run)."),
 ("SCS2's second to fourth, SCS3's four and DCN1's six", SCS3, "amendments A1 f51866c8d4, A2 63ed365df0, A3 fe9811fe03, A4 b34295ebcd, all post hoc"),
 ("and the readings of NH2 and XCV1 other than NO VERDICT", NH2, "## Post hoc reading A1 (named; not frozen)"),
 ("and the readings of NH2 and XCV1 other than NO VERDICT", XCV1, "| A1 (post hoc): class, 5 measured-star clusters | **AT THE CEILING**"),
 ("AKD1 has no amendment; its extra readings were added after the freeze and set no label", AKD1, "**Post-freeze reported readings** (`akd1_extra.*`, disclosed, label-setting nothing)"),
 ("The KiDS-Legacy release was fetched on the owner's go and sits beside the repository, not in it.", KL1, "- The KiDS-Legacy release, untracked, beside the repository."),
 ("The KiDS-Legacy release was fetched on the owner's go and sits beside the repository, not in it.", KL1j, "KiDS-Legacy (fetched on the owner's go)"),
 # ---------------- version 1.1, round 2 ----------------
 ("with stability excluded there, and a disc's own centre is open", SCS3, "Nothing about the sign is in doubt. **STABLE is excluded.**"),
 ("with stability excluded there, and a disc's own centre is open", SCS3, "Whether the static clock is stable at a disc's own centre is open."),
 ("a disc in an external field NO VERDICT with STABLE excluded", SCS3, "Nothing about the sign is in doubt. **STABLE is excluded.**"),
 ("away from the centre, around isolated discs", SCS3, "So **\"stable around isolated discs\" (SCS2) covers r >= 0.002-0.010 R_d, not the centre.**"),
 ("No dust term tried, keyed on the clock's offset", MK2, "**Other dust terms.** Only the exponential (and the quadratic, as known answer) was graded."),
 ("with an acceptable fit, while DES Y3 stays at 2.18/2.23 on a re-scanned fit", KL1, "Every survey's fit is acceptable."),
 ("with an acceptable fit, while DES Y3 stays at 2.18/2.23 on a re-scanned fit", KL1, "The polished scan (AMENDMENT C3: restarts to below 1e-4, two sweeps) gives width 0.0235 / 0.0230 and gap 2.18 / 2.23"),
 ("several of them fail or have no verdict. The form is not complete.", THY, "FAILS on pooled isolated lenses (1.34 / 1.39, 44 of 59 points over)"),
 ("several of them fail or have no verdict. The form is not complete.", THY, "It is not complete, because rules 3 and 4 are two solutions of one action that the action does not connect"),
 # section 2: SCS2's known answer, SCS3, DCN1
 ("SCS2's frequency known answer fails with its frozen fit and passes under its fourth amendment, which is post hoc and followed a graded run", SCS2, "KA1's frequency test passes with A4's fit (1.2e-3) and fails with the frozen fit (3.9 %)"),
 ("SCS2's frequency known answer fails with its frozen fit and passes under its fourth amendment, which is post hoc and followed a graded run", SCS2, "- **A4 is post hoc after a graded run.**"),
 ("it says that the sign is not in doubt and that STABLE is excluded there", SCS3, "Nothing about the sign is in doubt. **STABLE is excluded.**"),
 ("It also says that SCS2's label for isolated discs does not cover the centre, and that whether the static clock is stable at a disc's own centre is open", SCS3, "So **\"stable around isolated discs\" (SCS2) covers r >= 0.002-0.010 R_d, not the centre.** Whether the static clock is stable at a disc's own centre is open."),
 ("Lane DCN1 then took the centre. Every reading it froze before its outcome was seen is NO VERDICT, each on a known-answer gate", DCN1, "**Every reading frozen before the outcome was seen is NO VERDICT, each on a known-answer gate.**"),
 ("under the last of its six post hoc amendments, two of them written after the outcome was seen, it reads ARTEFACT on both footings, with the isolated centre stable", DCN1, "Six amendments, all post hoc, each committed alone"),
 ("under the last of its six post hoc amendments, two of them written after the outcome was seen, it reads ARTEFACT on both footings, with the isolated centre stable", DCN1, "**A5 and A6 were written after the outcome was seen**"),
 ("under the last of its six post hoc amendments, two of them written after the outcome was seen, it reads ARTEFACT on both footings, with the isolated centre stable", DCN1, "## Label (per footing): **ARTEFACT / ARTEFACT** (A6, the last of six readings)"),
 ("under the last of its six post hoc amendments, two of them written after the outcome was seen, it reads ARTEFACT on both footings, with the isolated centre stable", DCN1, "**STABLE AT THE CENTRE / STABLE AT THE CENTRE** (4 / 4)"),
 # section 5
 ("at the three dust constants its brief asked for and at all four masses", COL1, "at every mu_K the brief asked for: 3.71, 1.78 / 1.74 and 0.1 per Mpc, at all four masses"),
 ("every galaxy of the high-redshift sample on disk at its stated extent (100 of 100)", FLD1, "**RC100's outer radii** are the sample's stated extent (mean 2.2 R_e, maximum 4 R_e), not per-galaxy measurements."),
 ("every galaxy of the high-redshift sample on disk at its stated extent (100 of 100)", FLD1, "at 2.2 R_e and at 4 R_e (100 of 100;"),
 ("A disc's own centre is open, and the nonlinear outcome has not been computed", SCS3, "Whether the static clock is stable at a disc's own centre is open."),
 ("MK1 also corrects the bound quoted above: 0.1 is the first failing grid value, and the bound lies between 0.03 and 0.1", MK1, "0.1 is S4's first failing grid value: S4's guard held at 0.03 and failed at 0.1"),
 ("MK1 also corrects the bound quoted above: 0.1 is the first failing grid value, and the bound lies between 0.03 and 0.1", MK1, "The bound lies between 0.03 and 0.1."),
 ("Version 1.1: MK1 corrects the sentence before: 1.78/1.74 is only where the mean residual is zero, the shape passes at no $\\mu_K$, so the dust does not close X-COP at any value", MK1, "That is only where the mean Delta is zero. At no mu_K does the shape pass"),
 ("Version 1.1: MK1 corrects the sentence before: 1.78/1.74 is only where the mean residual is zero, the shape passes at no $\\mu_K$, so the dust does not close X-COP at any value", MK1, "So the dust does not close X-COP at any mu_K."),
 ("and `17 to 18 times' should read `18 to 60 times'", MK1, "\"17-18 times the galaxy bound\" should read \"18 to 60 times\"."),
 ("and 2.18/2.23 on DES Y3 (2.89/2.82 on the frozen scan)", KL1, "| DES Y3, frozen scan | 2.89 / 2.82 | 0.28 | GAP STAYS |"),
 ("These are post hoc readings: the amended label is GAP STAYS and the frozen labels are NO VERDICT", KL1, "- **Under AMENDMENTS C1 + C2 + C3 (post hoc): GAP STAYS / GAP STAYS, driven by DES Y3.**"),
 ("These are post hoc readings: the amended label is GAP STAYS and the frozen labels are NO VERDICT", KL1, "- **As frozen: NO VERDICT / NO VERDICT.** The MUTATE arm MC1 does not bite."),
 ("Point masses and isolated discs away from their centres are computed and stable", SCS3, "So **\"stable around isolated discs\" (SCS2) covers r >= 0.002-0.010 R_d, not the centre.**"),
 # section 7: intro, rules, 7.2, survey, data rows
 ("The lanes in this section landed on 2026-11-10, after version 1.0, except the earlier lanes named in the survey of media", RER2, "# Verification re-runs, 2026-11-10"),
 ("re-ran DG1's main run (not its mutation twin)", RER2, "Not re-run: DG1's MUTATE twin (`dg1.py --mutate`, about 580 s)."),
 ("every label and stored number reproduced apart from run times and memory", RER2, "Of the 5482 values in `dg1.json`, 5 differ, all of them run time or memory."),
 ("every label and stored number reproduced apart from run times and memory", RER2, "two differ, both the `runtime_s` of the neutrino refits"),
 ("The action is lane QX17's action (A), which is PAPER70's.", THY, "The action is QX17's (A)."),
 ("It is not derived: in the action it is an integration constant (note R541, which is not a graded lane)", R541, "# R541 NOTE: why is the cold share 5.41? NOT DERIVED. In the adopted action it is FREE (an integration constant)"),
 ("It is not derived: in the action it is an integration constant (note R541, which is not a graded lane)", R541, "**This is a note, not a graded lane.**"),
 ("four attempts to derive it are EXCLUDED on both footings", R541, "four are EXCLUDED and one only TRADES 5.41 for more fitted constants. None fixes the number."),
 ("a clock-matter coupling (R541A)", R541A, "# R541A RESULT: a clock-matter coupling does not fix the cold share; the induced density rides with the baryons. EXCLUDED / EXCLUDED (canonical / alt)"),
 ("a Gauss-Bonnet source (R541C)", R541C, "# R541C RESULT: a Gauss-Bonnet source gamma tau G_GB makes no lasting cold dark energy. EXCLUDED / EXCLUDED (canonical / alt)"),
 ("a baryon-current coupling (R541D)", R541D, "# R541D RESULT: a baryon-current coupling ties the charge but makes antibaryons, 4.3 million times too many. EXCLUDED / EXCLUDED (canonical / alt)"),
 ("a coupling to $B-L$ (R541E)", R541E, "EXCLUDED / EXCLUDED (canonical / alt)"),
 ("a coupling to $B-L$ (R541E)", R541E, "# R541E RESULT: coupling the clock to B minus L"),
 ("A fifth, an early potential on the clock (R541B), reads TRADES: it moves the number into the potential's height and does not fix it.", R541B, "# R541B RESULT: an early potential V(tau) on the clock moves 5.41 into V's height; it does not fix it. TRADES / TRADES (canonical / alt)"),
 ("Each line rests on a lane's verdict on both footings; where a sentence is a reported reading and not a label, it says so.", AKD1, "A2, the A4 weight W, A6 and the brackets are reported."),
 ("that is a reported class bound and not a label", AKD1, "A2, the A4 weight W, A6 and the brackets are reported."),
 ("Of functions of the offset, only a quadratic and an exponential were graded", MK2, "**Other dust terms.** Only the exponential (and the quadratic, as known answer) was graded."),
 ("MK1's statement about any function of the offset alone is a requirement and not a graded result", MK1, "**What a dust term would have to do differently (a requirement only).**"),
 ("One kinetic function with a narrow interval of changed compressibility is named in the two assembly notes", THY, "Still alive and untested as a result: one kinetic function with a narrow interval of changed compressibility"),
 ("One kinetic function with a narrow interval of changed compressibility is named in the two assembly notes", MED, "a single kinetic function with a narrow interval of changed compressibility (DT2)"),
 ("its linear and static checks pass there, and whether a forming halo can reach its static state is not computed", MED, "linear and static checks pass; whether a forming halo can reach its static state is not computed"),
 ("and SCS3 says that STABLE is excluded", SCS3, "STABLE is excluded"),
 ("done as the action's own static equation the mean-zero value is 1.53/1.46", MK1, "1.53 / 1.46"),
 ("every one of its 24 resolved solves has", DCN1, "on every one of the 24 resolved local solves"),
 ("positive in every cell and no growing rate", DCN1, "every cell has D.P > 0"),
 ("positive in every cell and no growing rate", DCN1, "every route-L rate is negative"),
 ("with 1 undetermined; the lane says this kills the family on its inputs and is not a no-go theorem", HF1, "This kills the family on these inputs, not all light fermions, and it isn't a no-go theorem."),
 ("a gate added after its first result, which failed on groups", WM1, "## A2 update: gate 0, seeding (graded first; added after the first result, disclosed in AMENDMENT_A2.md)"),
 ("a gate added after its first result, which failed on groups", WM1, "FAIL / FAIL with first failing gate 2, groups."),
 ("it does not resolve law against clumping, and its scored rows fail", TM1, "It does not resolve law versus clumping"),
 ("it does not resolve law against clumping, and its scored rows fail", TM1, "| 1 Growth on FRW | **FAIL** (healthy, but no growth)"),
 ("Route E, in which cold dark energy clumps everywhere, gravity is Newtonian and the law is emergent", X38, "Route E: cold dark energy clumps everywhere, gravity is Newtonian, the law is emergent."),
 ("had its cold sector retired by the owner on 2026-11-01", RETIRE, "# Owner decision, 2026-11-01: route E's cold sector is retired"),
 ("which the lane's frozen list counts against the form", KL1, "Part B's frozen list counts a gap above 2 widths **against form B**."),
 ("it says its blindness was not clean, since KL1's headline numbers were visible before it began", KL1R, "The blindness was not clean: KL1's headline numbers were visible in context before this lane began"),
 ("and that it is not an independent check of the shared machinery", KL1R, "It is **not** an independent check of the shared machinery"),
 ("(a mutation arm does not bite, and on alt a known answer fails on DES Y3)", KL1, "- **As frozen: NO VERDICT / NO VERDICT.** The MUTATE arm MC1 does not bite."),
 ("(a mutation arm does not bite, and on alt a known answer fails on DES Y3)", KL1, "On alt, KC1 also fails on DES Y3"),
 ("DES Y3 2.18/2.23 on the polished scan (2.89/2.82 on the frozen scan)", KL1, "| DES Y3, frozen scan | 2.89 / 2.82 | 0.28 | GAP STAYS |"),
 ("at disc ratios of 0.3 or 0.8 that pass fails", SHP1, "The pass holds at the standard mass-to-light ratios only. At Upsilon_disk 0.3 or 0.8 (bulge 0.5 / 1.0) R1 fails"),
 # method, round 2
 ("COL1's four amendments", COL1, "- **Four post-hoc amendments, each committed alone before the runs they govern.**"),
 ("MK2's second, third and fourth amendments", MK2, "- A4 9754a17af7, the lead's added row i: written after rows a1-h had graded numbers; row i had none."),
 ("SCS2's second to fourth, SCS3's four and DCN1's six", DCN1, "Six amendments, all post hoc, each committed alone"),
 ("GO1's amendment", GO1a, "AMENDMENT A1 05f48b8a6d is post hoc, committed alone before the graded run, and disclosed."),
 ("SHP1's check made after grading", SHP1, "**Post-hoc check** (`shp1_posthoc.py`, written after `shp1.out` was read; not in the criteria; grades nothing)."),
 ("WM1's seeding gate was added after its first result.", WM1, "## A2 update: gate 0, seeding (graded first; added after the first result, disclosed in AMENDMENT_A2.md)"),
 ("the note R541 and its lanes R541A to R541E are under \\texttt{closure\\_2026\\_11\\_10/}", R541, "**Dated addition, 2026-11-10 evening.** The ingredients of section 7 were then tested in five lanes with frozen"),
]
# (fragment in the TeX, JSON file, key path, format, the number as the TeX prints it)
J = [
 ("0.597$ [0.556, 0.637]", RB1j, ["gate1", "canonical", "classes", "G-H", "median"], ".3f", "0.597"),
 ("0.597$ [0.556, 0.637]", RB1j, ["gate1", "canonical", "classes", "G-H", "lo"], ".3f", "0.556"),
 ("0.597$ [0.556, 0.637]", RB1j, ["gate1", "canonical", "classes", "G-H", "hi"], ".3f", "0.637"),
 ("reads 1.095 [0.885, 1.259]", RB1j, ["gate1", "canonical", "classes", "C-X", "median"], ".3f", "1.095"),
 ("reads 1.095 [0.885, 1.259]", RB1j, ["gate1", "canonical", "classes", "C-X", "hi"], ".3f", "1.259"),
 ("with 4 of 7 clusters above 1", RB1j, ["gate1", "canonical", "classes", "C-X", "n_above1"], "d", "4"),
 ("slope $+0.160$ [$+0.080$, $+0.225$]", RB1j, ["gate2", "canonical", "slope", "slope"], "+.3f", "+0.160"),
 ("slope $+0.160$ [$+0.080$, $+0.225$]", RB1j, ["gate2", "canonical", "slope", "lo"], "+.3f", "+0.080"),
 ("slope $+0.160$ [$+0.080$, $+0.225$]", RB1j, ["gate2", "canonical", "slope", "hi"], "+.3f", "+0.225"),
 ("$-0.007$ / $+0.033$", RB1j, ["gate3", "canonical", "main", "bins", 0], "+.3f", "-0.007"),
 ("$-0.030$ / $-0.041$", RB1j, ["gate3", "canonical", "main", "bins", 4], "+.3f", "-0.041"),
 ("$0.277\\pm0.183$ tied", KO2j, ["foot", "canonical", "fits", "primary", "R", "late", "R"], ".3f", "0.277"),
 ("$0.277\\pm0.183$ tied", KO2j, ["foot", "canonical", "fits", "primary", "R", "late", "s_tot"], ".3f", "0.183"),
 ("$0.487\\pm0.071$ in the primary design", KO2j, ["foot", "canonical", "fits", "primary", "R", "early", "R"], ".3f", "0.487"),
 ("$0.487\\pm0.071$ in the primary design", KO2j, ["foot", "canonical", "fits", "primary", "R", "early", "s_tot"], ".3f", "0.071"),
 ("$1.071\\pm0.199$ untied", KO2j, ["foot", "canonical", "fits", "B3 untied", "R", "late", "R"], ".3f", "1.071"),
 ("$1.071\\pm0.199$ untied", KO2j, ["foot", "canonical", "fits", "B3 untied", "R", "late", "s_tot"], ".3f", "0.199"),
 ("$0.739\\pm0.115$ with lens", KO2j, ["foot", "canonical", "fits", "B3 untied", "R", "early", "R"], ".3f", "0.739"),
 ("$0.739\\pm0.115$ with lens", KO2j, ["foot", "canonical", "fits", "B3 untied", "R", "early", "s_tot"], ".3f", "0.115"),
 ("measured an error of 0.278 on discs", KO2j, ["foot", "canonical", "fits", "secondary", "R", "late", "s_tot"], ".3f", "0.278"),
 # KO3F: the 0.68 / 0.62 are KO1's published errors (README); the JSON holds the forecast columns, so only 0.57 / 0.52 are read here
 ("forecast at 0.57/0.52 with such a veto", K3Fj, ["rows", "F1.6 V1000 hybrid veto, all KiDS", "canonical", "sigma_late", 1], ".2f", "0.57"),
 ("forecast at 0.57/0.52 with such a veto", K3Fj, ["rows", "F1.6 V1000 hybrid veto, all KiDS", "alt", "sigma_late", 1], ".2f", "0.52"),
 # CO2: the p-values the TeX prints to four decimals, read from the lane's JSON
 ("$p=0.0026$/0.0021, just below", CO2j, ["rows", "P4", "canonical", "p"], ".4f", "0.0026"),
 ("$p=0.0026$/0.0021, just below", CO2j, ["rows", "P4", "alt", "p"], ".4f", "0.0021"),
 ("the same row reads $p=0.0044$/0.0037", CO2j, ["rows", "P4", "canonical", "constant_factor", "p"], ".4f", "0.0044"),
 ("the same row reads $p=0.0044$/0.0037", CO2j, ["rows", "P4", "alt", "constant_factor", "p"], ".4f", "0.0037"),
 ("with the neutrino bracket $p=0.0090$/0.0077", CO2j, ["rows", "brackets_shear", "canonical", "one_0p06eV_neutrino", "p"], ".4f", "0.0090"),
 ("with the neutrino bracket $p=0.0090$/0.0077", CO2j, ["rows", "brackets_shear", "alt", "one_0p06eV_neutrino", "p"], ".4f", "0.0077"),
 # CO2's check made after grading: the ends of the two quoted ranges and the neutrino gap, from its JSON
 ("$p$ is 0.003 to 0.013: tension each time", CO2pj, ["rows", "R2b", "alt", "pinned", "p"], ".3f", "0.003"),
 ("$p$ is 0.003 to 0.013: tension each time", CO2pj, ["rows", "R2", "canonical", "pinned", "p"], ".3f", "0.013"),
 ("reads 0.021 to 0.049 corrected", CO2pj, ["rows", "R2b", "canonical", "S0_alone_engine", "p"], ".3f", "0.021"),
 ("reads 0.021 to 0.049 corrected", CO2pj, ["rows", "R2", "canonical", "S0_alone_engine", "p"], ".3f", "0.049"),
 ("the gap is 4.89/5.04 widths", CO2pj, ["rows", "as_graded", "canonical", "nu_minus_best_in_widths"], ".2f", "4.89"),
 ("the gap is 4.89/5.04 widths", CO2pj, ["rows", "as_graded", "alt", "nu_minus_best_in_widths"], ".2f", "5.04"),
 ("the pinned value sits 5.62/5.78 widths above it", CO2pj, ["rows", "as_graded", "canonical", "pinned_minus_best_in_widths"], ".2f", "5.62"),
 ("the pinned value sits 5.62/5.78 widths above it", CO2pj, ["rows", "as_graded", "alt", "pinned_minus_best_in_widths"], ".2f", "5.78"),
 ("Unpinned, the same row reads $p=0.0004$/0.0002", CO2j, ["rows", "brackets_shear", "canonical", "unpinned_sigma8_response", "p"], ".4f", "0.0004"),
 ("Unpinned, the same row reads $p=0.0004$/0.0002", CO2j, ["rows", "brackets_shear", "alt", "unpinned_sigma8_response", "p"], ".4f", "0.0002"),
 ("($-0.30\\sigma$ on both footings", CO2j, ["rows", "P2", "canonical", "pull"], "+.2f", "-0.30"),
 ("($-0.30\\sigma$ on both footings", CO2j, ["rows", "P2", "alt", "pull"], "+.2f", "-0.30"),
 ("$\\sigma_8$ from 0.8405/0.8429 to 0.8271", CO2j, ["rows", "P2", "canonical", "sigma8"], ".4f", "0.8271"),
 ("$\\sigma_8$ from 0.8405/0.8429 to 0.8271", CO2j, ["rows", "P2", "alt", "sigma8"], ".4f", "0.8271"),
 # version 1.1: KL1's graded numbers, read from its JSON outputs (Parts A and B: kl1.json; Part C: kl1c.json)
 ("CO2's gap of 5.62/5.78 KiDS-1000 widths", KL1j, ["rows", "canonical", "A0", "KiDS", "gap_widths"], ".2f", "5.62"),
 ("CO2's gap of 5.62/5.78 KiDS-1000 widths", KL1j, ["rows", "alt", "A0", "KiDS", "gap_widths"], ".2f", "5.78"),
 ("KiDS-Legacy prefers $\\sigma_8=0.7767$/0.7748", KL1j, ["partB", "rows", "canonical", "B0", "best_sigma8"], ".4f", "0.7767"),
 ("KiDS-Legacy prefers $\\sigma_8=0.7767$/0.7748", KL1j, ["partB", "rows", "alt", "B0", "best_sigma8"], ".4f", "0.7748"),
 ("where KiDS-1000 preferred 0.7358/0.7341", KL1j, ["rows", "canonical", "A0", "KiDS", "best_sigma8"], ".4f", "0.7358"),
 ("where KiDS-1000 preferred 0.7358/0.7341", KL1j, ["rows", "alt", "A0", "KiDS", "best_sigma8"], ".4f", "0.7341"),
 ("neutrino gives $\\sigma_8=0.8121$/0.8120", KL1j, ["rows", "canonical", "A1", "KiDS", "target_sigma8"], ".4f", "0.8121"),
 ("neutrino gives $\\sigma_8=0.8121$/0.8120", KL1j, ["rows", "alt", "A1", "KiDS", "target_sigma8"], ".4f", "0.8120"),
 ("(KiDS-1000 gap 3.95/4.06 widths)", KL1j, ["rows", "canonical", "ALL", "KiDS", "gap_widths"], ".2f", "3.95"),
 ("(KiDS-1000 gap 3.95/4.06 widths)", KL1j, ["rows", "alt", "ALL", "KiDS", "gap_widths"], ".2f", "4.06"),
 ("($p=0.111$/0.101 for Legacy)", KL1j, ["partB", "rows", "canonical", "BALL", "p"], ".3f", "0.111"),
 ("($p=0.111$/0.101 for Legacy)", KL1j, ["partB", "rows", "alt", "BALL", "p"], ".3f", "0.101"),
 ("with Legacy still 2.13/2.30 of its widths", KL1j, ["partB", "rows", "canonical", "BALL", "gap_widths"], ".2f", "2.13"),
 ("with Legacy still 2.13/2.30 of its widths", KL1j, ["partB", "rows", "alt", "BALL", "gap_widths"], ".2f", "2.30"),
 ("KiDS-Legacy 1.71/1.88 widths and consistent", KL1cj, ["rows", "canonical", "GATE|Legacy", "gap_widths"], ".2f", "1.71"),
 ("KiDS-Legacy 1.71/1.88 widths and consistent", KL1cj, ["rows", "alt", "GATE|Legacy", "gap_widths"], ".2f", "1.88"),
 ("(2.06/2.23 with the full Gaussian likelihood)", KL1cj, ["rows", "canonical", "GATE|Legacy", "with_logdet", "gap_widths"], ".2f", "2.06"),
 ("(2.06/2.23 with the full Gaussian likelihood)", KL1cj, ["rows", "alt", "GATE|Legacy", "with_logdet", "gap_widths"], ".2f", "2.23"),
 ("DES Y3 2.18/2.23 on the polished scan", KL1cj, ["polish", "canonical", "GATE", "gap_widths"], ".2f", "2.18"),
 ("DES Y3 2.18/2.23 on the polished scan", KL1cj, ["polish", "alt", "GATE", "gap_widths"], ".2f", "2.23"),
 ("KiDS-1000 3.72/3.85", KL1cj, ["rows", "canonical", "GATE|KiDS", "gap_widths"], ".2f", "3.72"),
 ("KiDS-1000 3.72/3.85", KL1cj, ["rows", "alt", "GATE|KiDS", "gap_widths"], ".2f", "3.85"),
 ("Legacy reads 1.57/1.83 and stays consistent", KL1cj, ["rows", "canonical", "C3b_own_prior|Legacy", "gap_widths"], ".2f", "1.57"),
 ("Legacy reads 1.57/1.83 and stays consistent", KL1cj, ["rows", "alt", "C3b_own_prior|Legacy", "gap_widths"], ".2f", "1.83"),
 ("put DES Y3 at 1.31/1.27 against 3.49/3.43 widths", KL1cj, ["rows", "canonical", "GATE_R2|DES", "gap_widths"], ".2f", "1.31"),
 ("put DES Y3 at 1.31/1.27 against 3.49/3.43 widths", KL1cj, ["rows", "alt", "GATE_R2|DES", "gap_widths"], ".2f", "1.27"),
 ("put DES Y3 at 1.31/1.27 against 3.49/3.43 widths", KL1cj, ["rows", "canonical", "GATE_R2b|DES", "gap_widths"], ".2f", "3.49"),
 ("put DES Y3 at 1.31/1.27 against 3.49/3.43 widths", KL1cj, ["rows", "alt", "GATE_R2b|DES", "gap_widths"], ".2f", "3.43"),
 ("sits 1.71/1.88 of the survey's widths high", KL1cj, ["rows", "canonical", "GATE|Legacy", "gap_widths"], ".2f", "1.71"),
 ("while DES Y3 stays at 2.18/2.23", KL1cj, ["polish", "canonical", "GATE", "gap_widths"], ".2f", "2.18"),
 ("(2.89/2.82 on the frozen scan)", KL1cj, ["rows", "canonical", "GATE|DES", "gap_widths"], ".2f", "2.89"),
 ("(2.89/2.82 on the frozen scan)", KL1cj, ["rows", "alt", "GATE|DES", "gap_widths"], ".2f", "2.82"),
]
# the paper's own arithmetic, from QX17's FRW row: rho = I0 (1 + w0/a^3)/(8 pi G a^3) with I0 = 3 (H0/c)^2 Omega_c (per Mpc^2),
# w0 = I0 / (4 mu_K^2); w0 = a^3 at z = 1089 gives the bound on mu_K
H0, CKM, OMC, A_REC = 70.0, 299792.458, 0.26, 1.0 / 1090.0
COEF = 3.0 * (H0 / CKM) ** 2 * OMC / 4.0
MUK = math.sqrt(COEF / A_REC ** 3)
A = [
 ("$w_0=1.063\\times10^{-8}/\\mu_K^2$", f"{COEF:.3e}".replace("e-08", "e-8"), "1.063e-8"),
 ("so at $\\mu_K=3.71$ per Mpc the component still has $w=\\tfrac12$", f"{MUK:.2f}", "3.71"),
 ("still has $w=\\tfrac12$ at $z=1089$", f"{1 / A_REC - 1:.0f}", "1089"),
 ("with $H_0$ 70 and $\\Omega_c$ 0.26", f"{H0:.0f} {OMC}", "70 0.26"),
]
NOTES = [
]
def ws(s): return re.sub(r"\s+", " ", s)
_cache = {}
def src(path):
    """working-tree file, plus the copies at HEAD and at origin/main (another session may hold the newer one)."""
    if path not in _cache:
        t = ""
        fp = os.path.join(ROOT, path)
        if os.path.exists(fp): t += open(fp, encoding="utf-8", errors="replace").read()
        for ref in ("HEAD", "origin/main"):
            r = subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{path}"], capture_output=True, text=True)
            if r.returncode == 0: t += "\n" + r.stdout
        _cache[path] = t
    return _cache[path]
_ccache = {}
def committed(path):
    """committed at HEAD or on origin/main, and (v1.1) the working-tree copy, if there is one, equals a committed copy:
    a literal must not pass from an uncommitted edit. PAPER72's own files are exempt from the second clause (this version
    changes them); a literal read from them must still be in a committed copy, which the deposited block of its .zenodo.json is."""
    if path not in _ccache:
        refs = [r for r in ("HEAD", "origin/main")
                if subprocess.run(["git", "-C", ROOT, "cat-file", "-e", f"{r}:{path}"], capture_output=True).returncode == 0]
        ok_ = bool(refs)
        fp = os.path.join(ROOT, path)
        if ok_ and os.path.exists(fp) and not os.path.basename(path).startswith("PAPER72_"):
            wt = open(fp, "rb").read()
            ok_ = any(subprocess.run(["git", "-C", ROOT, "show", f"{r}:{path}"], capture_output=True).stdout == wt for r in refs)
        _ccache[path] = ok_
    return _ccache[path]
def jsrc(path):
    fp = os.path.join(ROOT, path)
    if os.path.exists(fp): return json.load(open(fp))
    return json.loads(subprocess.run(["git", "-C", ROOT, "show", f"origin/main:{path}"], capture_output=True, text=True, check=True).stdout)
def dig(d, keys):
    for k in keys: d = d[k]
    return d
def mutate(lit):
    m = re.search(r"\d", lit)
    if not m: return lit
    d = str((int(m.group()) + 1) % 10)
    return lit[:m.start()] + d + lit[m.end():]
ok = 0; bad = []
for frag, path, lit in L:
    in_tex = frag in TEX
    l2 = mutate(lit) if MUT else lit
    in_src = ws(l2) in ws(src(path))
    if MUT:
        if not re.search(r"\d", lit) or not in_src: ok += 1
        else: bad.append(("mutant survived", frag, path))
    elif in_tex and in_src and committed(path): ok += 1
    else: bad.append(("tex" if not in_tex else ("src" if in_src is False else "uncommitted"), frag, path, lit))
for frag, path, keys, fmt, num in J:
    val = format(dig(jsrc(path), keys), fmt)
    n2 = mutate(num) if MUT else num
    good = frag in TEX and num in frag.replace("$", "") and val == n2 and committed(path)
    if MUT:
        if val != n2: ok += 1
        else: bad.append(("mutant survived", frag, path))
    elif good: ok += 1
    else: bad.append(("json", frag, path, f"file gives {val}, TeX {num}"))
for frag, val, num in A:
    n2 = mutate(num) if MUT else num
    if MUT:
        if val != n2: ok += 1
        else: bad.append(("mutant survived", frag, "arithmetic"))
    elif frag in TEX and val == num: ok += 1
    else: bad.append(("arithmetic", frag, f"computed {val}, TeX {num}"))
body = TEX.split("\\begin{document}")[1]
rules = [
 ("kappa stated as fitted", "$\\kappa=\\tfrac12$ is fitted" in TEX),
 ("not closed stated", "The theory is not closed" in TEX),
 ("no favouring claim", "Nothing here says the data favour this framework" in TEX),
 ("no completion claimed", "It does not complete the theory" in TEX),
 ("cold dark energy is not a particle", "it is not a particle" in TEX),
 ("no local paths", "/Users/" not in TEX),
 ("no 'cold dark matter'", "cold dark matter" not in TEX.lower() and "cdm-like" not in TEX.lower()),
 ("no pending placeholder", "\\pend{" not in body and not any(l.startswith("% PENDING") for l in TEX.splitlines())),
 ("chosen as a form, not a pass", "The choice is of a form, not of a pass" in TEX),
 ("RB1's gate is stated as one-sided", "can fail from one side only" in TEX and "can fail from above only" in TEX),
 ("post hoc items are marked", "Post hoc items are marked in their lanes" in TEX and "post hoc amendment" in TEX),
 ("lanes relabel nothing", "The lanes relabel nothing" in TEX and "none relabels an earlier lane" in TEX),
 ("lanes are not registered", "None is registered in the closure record" in TEX),
 ("own wrong estimates are listed", "\\section{Our own estimates}" in TEX),
 ("the failed known answer and the twin that did not bite are disclosed", "One of 13 known answers failed" in TEX and "One mutation twin did not bite" in TEX),
 ("footings never pooled", "never pooled" in TEX),
 ("version line", "Working note (PAPER72), version 1.1" in TEX),
]
if not MUT:
    for name, good in rules:
        if good: ok += 1
        else: bad.append(("rule", name, ""))
for b in bad: print("FAIL", *b)
if not MUT:
    for n in NOTES: print("NOTE", n)
total = len(L) + len(J) + len(A) + (0 if MUT else len(rules))
print(f"{ok} of {total} checks pass" + (" (mutate: each mutated literal must fail)" if MUT else ""))
print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
sys.exit(0 if not bad else 1)
