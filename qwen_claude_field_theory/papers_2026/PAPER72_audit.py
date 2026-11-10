#!/usr/bin/env python3
"""PAPER72 audit: each quoted number appears in the TeX and, as the literal given, in the committed lane file named beside it
(working tree, HEAD or origin/main: the shared checkout has diverged, and PD1 / PD2 are committed on origin only); a few graded
numbers are also read from the lane's JSON and rounded; the two numbers that are the paper's own arithmetic (w0's coefficient and
the recombination bound on mu_K) are recomputed here from QX17's FRW formula; naming rules; no local paths; no pending placeholder.
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
RER = C + "RERUNS_2026-11-09.md"
TPA = F + "TPA1_two_phase_action/RESULT.md"
K3F = F + "KO3F_spec_veto_power_forecast/README.md"; K3Fj = F + "KO3F_spec_veto_power_forecast/ko3f_forecast.json"
P69 = P + "PAPER69_closure_by_verdict_2026.zenodo.json"; P70 = P + "PAPER70_field_equations_closure_2026.zenodo.json"
P71 = P + "PAPER71_switch_theorems_kids_outer_points_2026.zenodo.json"
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
 ("lane TPA1 finds the action's law-on phase gradient-unstable, with no ghost", TPA, "a gradient instability, with no ghost, in the law-on phase"),
 ("wherever the clock's own dust density is below a critical value", TPA, "is gradient-unstable wherever its own dust density is below n_crit"),
 ("For a point mass that value is 0.08 to 0.9 of the law's phantom density", TPA, "For a point mass this is 0.08 to 0.9 of the law's phantom density"),
 ("the e-folding times on its grid are 5.0\\,Myr to 0.62\\,Gyr", TPA, "On the frozen grid the e-folding time is 5.0 Myr to 0.62 Gyr."),
 ("With the metric frozen (the decoupling limit)", TPA, "Every analysis was done in the decoupling limit (metric frozen)."),
 ("(EQUATIONS COMPLETE; health UNHEALTHY)", TPA, "**TPA1: EQUATIONS COMPLETE. Health: UNHEALTHY**"),
 ("its switch wall and its dust phase are healthy", TPA, "The wall itself is stable"),
 ("its switch wall and its dust phase are healthy", TPA, "The S = 0 phase is healthy."),
 ("unstable in the decoupling limit; coupled analysis not done", TPA, "decoupling limit"),
 ("The note on form B reads the form's static state, which has almost no dust of its own, as lying in that range", FB1, "The static state of section 1 has almost no dust of its own (mu_K = 0 in galaxies), so it sits in that unstable range"),
 ("which is how the note on form B reads the form's galaxies", FB1, "so it sits in that unstable range"),
 ("TPA1 states this for its law-on phase", TPA, "a gradient instability, with no ghost, in the law-on phase"),
 # abstract
 ("the Bullet passes only if the subcluster's stripped gas is counted", RB1, "**CONSISTENT [STRIPPING-DEPENDENT]**: S1 passes, S1/2 passes, S0 (= PD1 A2) fails"),
 ("Its CMB, lensing and growth rows hold when computed, on an amended reading of that lane's checks, with the amplitude of fluctuations unsolved", CO1, "The primary CMB, CMB lensing and the growth rate hold when computed."),
 ("Its CMB, lensing and growth rows hold when computed, on an amended reading of that lane's checks, with the amplitude of fluctuations unsolved", CO1, "The amplitude is not solved."),
 ("No solution has been computed that takes infalling dust to the static state", FB1, "It is a computation inside the action, not a missing postulate, and it has not been done."),
 ("that state is unstable in the one limit analysed", TPA, "Every analysis was done in the decoupling limit (metric frozen)."),
 ("and no cluster state has been solved", FB1, "and no other state has been solved"),
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
 ("before any graded number was computed (KO2 ran a model-only design toy before its freeze and says so)", KO2, "ko2_design_toy.py (pre-freeze, model only)"),
 ("The envelope exists, is stable and fills 0.2\\,\\% of space or less", HE1, "It is stable, it leaves discs alone (except the cap share at the highest masses), and it fills about 0.2 % of space or less."),
 ("It fails KiDS's late-type stacks", HE1, "It fails where it was expected to fail: KiDS's late-type lenses."),
 ("Its fifth gate fails as frozen on two clusters near $R_{500}$ only, and the label does not rest on it", HE1, "G5 fails as frozen on two clusters, near R500 only."),
 ("Its fifth gate fails as frozen on two clusters near $R_{500}$ only, and the label does not rest on it", HE1, "The label does not rest on G5."),
 ("Re-run by its lead session: both labels and every number in \\texttt{he1.json} reproduce", F + "README.md", "re-run by the lead: both labels and every number in `he1.json` reproduce, only timing lines differ"),
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
def committed(path):
    return any(subprocess.run(["git", "-C", ROOT, "cat-file", "-e", f"{ref}:{path}"], capture_output=True).returncode == 0
               for ref in ("HEAD", "origin/main"))
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
 ("version line", "Working note (PAPER72), version 1.0" in TEX),
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
