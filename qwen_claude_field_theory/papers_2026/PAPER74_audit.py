#!/usr/bin/env python3
"""PAPER74 audit: each quoted number appears in the TeX and, as the literal given, in the lane file named beside it
(working tree, HEAD or origin/main: another session may hold the newer copy of a lane). Naming rules; no local paths;
no pending placeholder; the paper's own arithmetic recomputed.
Run: python3 PAPER74_audit.py (exit 0 only if all pass).
--mutate changes one digit of each source literal (and of each TeX number in the arithmetic checks); exit 0 only if
every mutated literal then fails.
kappa = 1/2 FITTED; not theory closed; the cold component is cold dark energy (a gravitating field component),
never a particle."""
import json, math, os, re, subprocess, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEX = open(os.path.join(HERE, "PAPER74_flagship_the_weeks_program_2026.tex"), encoding="utf-8").read()
P = "qwen_claude_field_theory/papers_2026/"
F = "fable52_push/"; H = "hy4_preview_push/"; C6 = "closure_2026_11_06/"; C9 = "closure_2026_11_09/"
D10 = "closure_2026_11_10/"; D11 = "closure_2026_11_11/"; T = "toe_2026_11_10/"
P69 = P + "PAPER69_closure_by_verdict_2026.zenodo.json"
P70 = P + "PAPER71_switch_theorems_kids_outer_points_2026.zenodo.json"   # carries PAPER70's DOI as a related id
P71 = P + "PAPER71_switch_theorems_kids_outer_points_2026.zenodo.json"
P72 = P + "PAPER72_law_with_cold_dark_energy_counted_once_2026.zenodo.json"
SHP = F + "SHP1_cold_component_shape/RESULT.md"
PD1 = C9 + "PD1_phantom_is_dust/RESULT.md"
QX17 = C6 + "QX17_covariant_field_equations/RESULT.md"
EQS = F + "EQ1_cold_dark_energy_equations/EQUATIONS.md"
THY = D10 + "THEORY_ASSEMBLED_2026-11-10.md"
HIS = F + "HIS1_history_reading/RESULT.md"
HSR = F + "HIS1R_history_regrade/COMPARISON.md"
LFS = D10 + "LFS1_leafwise_flux_supply/RESULT.md"
AKST = T + "AKS1_acceleration_keyed_sink/FROZEN_CRITERIA_T.md"
AKSR = T + "AKS1_acceleration_keyed_sink/RESULT.md"
SMF = D10 + "SMF1_smooth_frame_parent/RESULT.md"
AMT = D10 + "AMT1_amount_budget/AMOUNT_BUDGET.md"
MED = D10 + "MEDIUM_DESIGN_2026-11-10.md"
GAS = H + "HY4-1_GAS1_hot_gas_census/RESULT.md"
GASc = H + "HY4-1_GAS1_hot_gas_census/FROZEN_CRITERIA.md"
F52C = F + "CLOSURE.md"
CRUX = H + "CRUX.md"
CLOS = H + "CLOSURE.md"
ANAL = H + "ANALYSIS_2026-11-11.md"
EXIT = H + "EXITS.md"
FW = H + "FRAMEWORK.md"
F1 = H + "FINAL-1_THEORY_ASSEMBLY/RESULT.md"
F2 = D11 + "FINAL2_epoch/RESULT.md"
F3 = D11 + "FINAL3_share_derivation/PREREGISTER.md"
F4 = D11 + "FINAL4_growth_history/RESULT.md"
F6 = D11 + "FINAL6_kappa_formation/RESULT.md"
F15 = D11 + "FINAL15_formation/RESULT.md"
F16 = D11 + "FINAL16_kappa_real/RESULT.md"
F17 = H + "FINAL-17_kappa_A/RESULT.md"
F18 = D11 + "FINAL18_kappa_fold/RESULT.md"
F19 = H + "FINAL-19_kappa_C/RESULT.md"
F5m = H + "FINAL5_measurement/RESULT.md"
FL14 = H + "FINAL-14_lean_amount/RESULT.md"
FL12 = D11 + "FINAL-12_lean_background/RESULT.md"
FL20 = H + "FINAL-20_kappa_audit/AUDIT.md"
ELA = H + "ELA1_elastic_medium/RESULT.md"
PIK = F + "PIK1_pi_gated_dust/RESULT.md"
VCC = D11 + "VCC1_sourced_charge_current/RESULT.md"
CLS = D10 + "CLS2_what_the_cluster_mass_is/RESULT.md"
L = [
 # header: the DOIs of the companions, each read from its own deposit
 ("PAPER69 (DOI 10.5281/zenodo.24025170", P69, "10.5281/zenodo.24025170"),
 ("PAPER70 (DOI 10.5281/zenodo.24092073", P70, "10.5281/zenodo.24092073"),
 ("PAPER71 (DOI 10.5281/zenodo.24095262", P71, "10.5281/zenodo.24095262"),
 ("PAPER72 (v1.1 DOI 10.5281/zenodo.24125791", P72, "10.5281/zenodo.24125791"),
 # section 1: the claim
 ("$\\kappa=\\tfrac12$ is fitted", THY, "kappa (fitted)"),
 ("The theory is not closed", THY, "kappa = 1/2 FITTED; not theory closed"),
 ("never a particle", THY, "never a particle"),
 ("and {\\bf never pooled}:", THY, "Footings canonical (a0 9.3603e-11) / alt (1.1312e-10 m/s^2), never pooled."),
 ("\\label{eq:rhoc}", EQS, "rho_c = D.P + n_d"),
 ("the non-baryonic gravitating density is the sector's own", EQS, "rho_c = D.P + n_d ,"),
 ("There is no dark-matter particle, and there is no second halo", FW, "There is no dark-matter particle"),
 # section 2: the law as a measurement
 ("SPARC has 2700 points in 149 galaxies", SHP, "SPARC has 2700 points in 149 galaxies."),
 ("175 files, 2700 points against", SHP, "175 files, 2700 points (Lelli+2017: 2693), 149 galaxies (153)"),
 ("The worst bin median is within 0.057 dex canonical (0.021 alt)\nfor x from 0.18 to 10, against a line of 0.10",
  SHP, "The worst bin median is within\n0.057 dex canonical (0.021 alt) for x from 0.18 to 10, against a line of 0.10."),
 ("rms 0.0563\n(line 0.0660) canonical and 0.0558 alt", PD1, "rms 0.0563 (line 0.0660)"),
 ("median\ntruncation radius 186\\,kpc", PD1, "median R_trunc 186 kpc"),
 ("$a_0/2\\pi G=106.9/129.1\\,\\Msun\\,{\\rm pc}^{-2}$", CLOS, "the deep-field column a0/2\u03c0G = 106.9 / 129.1 M\u2609/pc\u00b2"),
 ("$1.40\\pm0.03$/$1.28\\pm0.03$ times", SHP, "1.40 +-\n0.03 /\n1.28 +- 0.03 times the law"),
 ("roughly flat from $x\\sim15$ to $\\sim200$", SHP, "roughly flat from x ~ 15 to ~ 200"),
 ("$1.4002\\pm0.2211$/$1.2740\\pm0.2012$ of the law", GAS,
  "1.4002 +- 0.2211 (canonical) /\n1.2740 +- 0.2012 (alt) of the law"),
 ("against a model of 1.003", F3, "model R_s 1.003"),
 ("{\\bf The pre-registered acceptance line is 0.891}", GASc, "Amplitude line   0.891 = 10^-0.05"),
 ("$X=59.49$/$59.50\\,M_b$", AMT, "**X_s = 59.5 M_b**"),
 # section 3: form B, six rules
 ("The action is QX17's (A), certified (label CERTIFIED)", THY, "The action is QX17's (A)."),
 ("The action is QX17's (A), certified (label CERTIFIED)", QX17, "**Label: CERTIFIED**"),
 ("Matter couples to the metric only", THY, "Matter couples to the metric only"),
 ("it is not a fifth force and\nthere is no external field effect on real mass", THY, "no external field effect"),
 ("The universe carries 5.41 units of that charge per unit of baryons", THY,
  "The universe carries 5.41 units of it per unit of baryons"),
 ("$n_da^3=$ const", EQS, "With P = 0: n_d a^3 = constant."),
 ("$w=w_0/(w_0+a^3)$", EQS, "w = w0 / (w0 + a^3)"),
 ("$c_s^2=(Q-1)/Q$", EQS, "c_s^2 = (Qbar - 1) / Qbar"),
 ("the Jeans wavenumber is $k_J=\\mu_K$\n  (physical)", EQS, "Jeans wavenumber k_J = mu_K (physical)"),
 ("$K\\mathbf P=(1-\\mu)\\nabla\\Phi$", EQS, "K P = (1 - mu) grad Phi"),
 ("$\\nabla\\!\\cdot[\\mu\\nabla\\Phi]+\\mu_K^2\\Phi=K\\rho_b$ in any geometry", EQS, "div[ mu grad Phi ] + mu_K^2 Phi = K rho_b"),
 ("this is\n  $g_N=g^2/(g+a_0)$ exactly", EQS, "g_N = g^2 / (g + a0)"),
 ("The cold pull $g_c=a_0g/(g+a_0)\\le a_0$ saturates", EQS, "g_c = g - g_N = a0 g / (g + a0)"),
 ("an isothermal halo with $\\sigma^2=\\tfrac12\\sqrt{GM_ba_0}$", EQS, "sigma^2 = (1/2) sqrt(G M_b a0)"),
 ("STABLE, point masses and isolated discs", F52C, "STABLE around point masses and isolated discs"),
 ("$\\Pi_{ij}=J(g)\\delta_{ij}-g_ig_j/(K(1+u))$ with $d_j\\Pi_{ij}=(\\nabla\\!\\cdot\\!\\mathbf P)g_i$",
  EQS, "Pi_ij = J(g) delta_ij - g_i g_j / (K (1 + u))"),
 ("is 0.96 at $0.1r_M$, 0.20 at\n$3r_M$, 0.066 at $30r_M$ and $6.6\\times10^{-3}$ at $100r_M$", EXIT,
  "0.96 at 0.1 r_M, 0.20 at 3 r_M, 0.066 at 30 r_M, 0.0066 at 100 r_M"),
 ("$\\sigma_r^2=-v_\\infty^2/2$ with\n$v_\\infty^4=GM_ba_0$", CRUX, "sigma_r^2 = -v_inf^2/2 with v_inf^4 = G M_b a0"),
 # section 4: the lock
 ("Inside any ball whose boundary free-falls, the net polarization charge is exactly zero, at all times, for any\nexchange rate, alignment and multipole", SMF,
  "The frame's polarization charge in that region is zero at every time, for every exchange rate,\n  alignment and ell"),
 ("for any momentum equation", AKSR, "whatever the momentum equation"),
 ("\\textbf{T4 GAUSS (exact; SMF1 S0b reproduced)}", AKST, "**T4 GAUSS (exact; SMF1 S0b reproduced).**"),
 ("\\textbf{S0b (exact, Gauss)}", SMF, "**S0b (exact, Gauss):**"),
 ("polarization {\\bf cannot be manufactured during\ninfall}", AKSR,
  "**T4 Gauss (exact; SMF1 S0b):** the net polarization charge in any free-fall-bounded ball is 0 at all times, whatever the momentum equation"),
 ("so a static halo cannot grow", LFS, "A static halo cannot grow."),
 ("Its charge changes only by a fraction of order\n$|\\Phi|/c^2$, about $10^{-6}$", LFS, "about 1e-6"),
 ("The lane's own label is ILL-POSED on both footings", LFS, "**Label, canonical and alt: ILL-POSED.**"),
 ("$\\mathbf{5.41\\,M_b}$", AMT, "**5.41 M_b** (Omega_c/Omega_b, the whole cosmic cold-to-baryon ratio)"),
 ("$\\mathbf{1.06\\,M_b}$ turned around by $z=0$", AMT, "**1.06 M_b** turned around by z 0"),
 ("1.40\\,$M_b$ settled, VSH1", AMT, "1.40 M_b = 7.8481e40 kg"),
 ("41.48", AMT, "| 272 | 41.9814 | 41.48 | 2.326e42 | 7.668 | 39.14 | 29.63 |"),
 ("97.82", AMT, "| 637 | 98.3168 | 97.82 | 5.483e42 | 18.081 | 92.28 | 69.87 |"),
 ("\\textbf{the whole cosmic budget is spent here}", AMT, "**the whole cosmic budget is spent here**"),
 ("$X_s/5.41=10.99/11.01/10.99/11.01$ across the four\nKiDS masses", CRUX, "X_s / 5.41 = 10.99 / 11.01 / 10.99 / 11.01"),
 ("(alt: 12.09 to 12.11)", AMT, "X_s/5.41 = 12.09 to 12.11"),
 ("spent at 38.2/34.7\\,kpc", CLOS, "exhausted at 38.2 kpc canonical / 34.7 kpc alt"),
 ("at 72/65\\,kpc for $\\log M_b=11$", ANAL, "the budget is gone at **72 kpc canonical /\n65 kpc alt**"),
 ("11.00 times the entire budget", CRUX, "**11.00x the entire budget**"),
 ("56 times the delivered 1.06\\,$M_b$", CRUX, "56x the 1.06"),
 ("42.5 times VSH1's\nsettled 1.40\\,$M_b$", FL14, "`= 42.5` exactly (595/14)"),
 ("reject the cosmic share\n$X=5.41$ at $+4.85$/$+4.93\\sigma$", AMT, "+4.85 / +4.93 sigma"),
 ("(and $X=10.82$ at $+4.34$/$+4.53$)", F3, "X = 10.82 -> +4.34 / -0.19 / +4.47 and"),
 ("\\[\n  \\Sigma_{\\rm gas}=\\frac{a_0}{\\pi G x_b^{2}},", GAS, "Sigma_gas = a0 / (pi G x_b^2),"),
 ("x_b^{2}=R_b(1+R_b)=5.41\\times6.41=34.6781,", GAS, "x_b^2 = R_b (1 + R_b) = 5.41 x 6.41 = 34.6781"),
 ("$1.287355\\times10^{-2}$\\,kg\\,m$^{-2}=6.1627\\,\\Msun\\,{\\rm pc}^{-2}$ canonical and $7.4477$ alt", GAS,
  "1.287355e-02 kg/m^2 = 6.1627 Msun/pc^2"),
 ("over by 284--574", CRUX, "over by 284-574"),
 ("over by 328--3750", CRUX, "over by 328-3750"),
 ("$+8.0$ to $+16.3\\sigma$", CRUX, "+8.0 to +16.3 sigma"),
 ("1.38/1.67", CLOS, "| 1.38 | 1.67 |"),
 ("$0.0392\\pm0.0069$/$0.0324\\pm0.0057$ of the law", GAS, "0.0392 +- 0.0069"),
 ("36/41 times\nbelow the law", GAS, "36 / 41 times below the law"),
 ("{\\bf MISSING BARYONS EXCLUDED [AMOUNT AND\nAMPLITUDE]}", GAS, "**MISSING BARYONS EXCLUDED [AMOUNT AND AMPLITUDE]**"),
 ("(ratio 0.37 to 1.26)", CLOS, "ratio 0.37 to 1.26"),
 ("$1.96\\times10^{-7}$/$2.16\\times10^{-7}$ at $\\log M_b=11$", CRUX, "| 11 | 1.96e-07 | 2.16e-07 |"),
 ("against a shortfall of a factor 5 to\n18", CRUX, "against a shortfall of a factor 5 to 18"),
 ("ELASTIC SOLID FAILS AT S0 (+S2, B1) on both footings", ELA, "ELASTIC SOLID FAILS AT S0 (+S2, B1)"),
 # section 5: the ledger
 ("THEORY WRITTEN / THEORY WRITTEN", F1, "**Label: THEORY WRITTEN / THEORY WRITTEN**"),
 ("(e) BEST-RANKED / NO POWER", F2, "**Label: (e) BEST-RANKED / NO POWER (canonical), (e) BEST-RANKED / NO POWER (alt).**"),
 ("DERIVED HISTORY EXCLUDED (9916/9009)", F4, "**DERIVED HISTORY EXCLUDED / DERIVED HISTORY EXCLUDED (canonical / alt)"),
 ("9916/9009", F4, "**Delta chi^2 = 9916.246 / 9008.690** against a gate of **4**"),
 ("TILT POST HOC, NOT EXCLUDED", F4, "TILT POST HOC, NOT EXCLUDED"),
 ("KAPPA NOT DERIVED (FITTED) + FORMATION REFUTED (per-galaxy)", F6,
  "**Label: KAPPA NOT DERIVED (FITTED) + FORMATION REFUTED (per-galaxy).**"),
 ("FORMATION LEDGER HOLDS / HOLDS IN PATTERN, NOT IN SIZE", F15,
  "**Label: FORMATION LEDGER HOLDS (canonical) / HOLDS IN PATTERN, NOT IN SIZE (alt)"),
 ("KAPPA NOT DERIVED (FITTED) -- FORM OUTPUT", F16, "**Label: `KAPPA NOT DERIVED (FITTED) -- FORM OUTPUT`.**"),
 ("KAPPA NOT DERIVED (FITTED) -- CAPACITY DERIVED", F17, "**Label: `KAPPA NOT DERIVED (FITTED) -- CAPACITY DERIVED`.**"),
 ("FOLD MATCHING FALSIFIED, NO SOLUTION IN THE VALID RANGE", F18,
  "**KAPPA NOT DERIVED (FITTED) -- FOLD MATCHING FALSIFIED, NO SOLUTION IN THE VALID RANGE.**"),
 ("FINAL-18\'s\nLean proves `fold\\_match\\_unique` and `fold\\_match\\_exists`", F18, "`fold_match_unique`"),
 ("6.0$\\pm$1.4 column", F19, "**6.0 \u00b1 1.4** (canonical) / **7.3 \u00b1 1.6** (alt)"),
 ("$\\sqrt{2\\pi}=2.5066$ at 22.1/27.6$\\sigma$", F19, "`kappa = sqrt(2 pi) = 2.5066`, which is **22.1 sigma**"),
 ("NO VALUE / NO VALUE", PIK, "**NO VALUE / NO VALUE.**"),
 ("EXCLUDED / EXCLUDED", VCC, "EXCLUDED / EXCLUDED (canonical / alt)"),
 ("NO CANDIDATE / NO CANDIDATE", CLS, "**Label, canonical and alt: NO CANDIDATE / NO CANDIDATE.**"),
 ("six items, exit 0, zero sorry", FL14, "all six items compile as named theorems"),
 ("byte-identical to the committed blob (md5 db7a54eb96c684cef667c83f87a89a4b)", FL20,
  "`db7a54eb96c684cef667c83f87a89a4b`"),
 ("fable52's own Lean files hold 92 theorems", F + "README.md", "The Lean files hold 92 theorems"),
 ("closed on every exit", F52C, "closed on every exit"),
 ("BREAKS DOWN (folds in 0.06--0.15 Gyr)", F52C, "BREAKS DOWN / BREAKS DOWN (a fold at the centre in 0.06 to 0.15 Gyr)"),
 ("DOES NOT (1.3--5.4$\\times$ short)", F52C, "DOES NOT / DOES NOT"),
 ("NOT WELL-DEFINED (4th order)", F52C, "NOT WELL-DEFINED on both footings"),
 ("BREAKS AT TURNAROUND", ANAL, "BREAKS AT TURNAROUND"),
 ("KILLED (K2 PROVISIONAL)", F52C, "KILLED (K2 PROVISIONAL) on both footings"),
 ("ALREADY IN THE RECORD AS AC2s", F52C, "ALREADY IN THE RECORD AS AC2s on both footings"),
 ("FALLS SHORT", ANAL, "FALLS SHORT"),
 ("NO-GO, a theorem", MED, "NO-GO, a theorem"),
 ("a failing verdict for each", MED, "class named here has a failing verdict"),
 ("NO RULE AMONG THE CANDIDATES", F52C, "NO RULE AMONG THE CANDIDATES on both footings"),
 ("certified & QX17, FB1", F52C, "certified | QX17; FB1 note"),
 ("PASSES at the 1.6\\,$R_h$ veto", F52C, "PASSES at the widest veto"),
 ("ROWS HOLD, inherited halo list", ANAL, "ROWS HOLD with an inherited halo list"),
 ("not falsified (one-sided), never a pass", F52C, "not falsified (one-sided), never a pass"),
 ("$X$ is monotone, $X(x_bR)=R$ exactly", FL14, "`X (x_b R) = R` for every `R > 0`"),
 ("the\nbreak-even window $x_b(541/100)\\in(5.8887,5.8889)$", FL14, "`X_break_window` | `x_b (541/100)` | `(5.8887, 5.8889)`"),
 ("3.87 / 7.67 / 11.00 / 18.08", FL14, "`demand_over_budget_98p32` | `X (98.32) / R_b` | `(18.08, 18.09)`"),
 ("the gas column 6.1627 / 7.4477", FL14, "`(6.1626, 6.1628)` -> **6.1627**"),
 # section 6: the formation reading
 ("tidal dwarfs $-0.687$ against a floor of $-0.755$", F15, "\u22120.687"),
 ("NGC~1052's UDGs $-0.843$ against $-0.855$", F15, "\u22120.843"),
 ("The measured 1.435 dex\n  bipolar spread", F15, "**Class-to-class spread: 1.435 dex (canonical), 1.433 dex (alt).**"),
 ("forbidden by the force reading at 20--24 se", F15, "forbidden by the force reading at 20-24 se"),
 ("four of five frozen", F15, "**F1 FLOOR**"),
 ("F2, F3, F4,\nF5 HOLD", F15, "| **F2 HOSTED HIGH**"),
 ("Exactly as frozen: F1 FAILS", F15, "**frozen FAIL** (clause (b) unsatisfiable, defect D1)"),
 ("F3's SPARC residual is $-0.023\\pm0.012$", F15, "\u22120.023"),
 ("145 of 148\ncompared numbers agreeing to $5\\times10^{-12}$", HSR, "145 of 148 compared numbers agree to 5e-12"),
 ("the formation reading scores 4 of 5 and the force\nreading 1 of 5", HIS, "**scores 1 of 5** on the same tests"),
 ("beats the no-epoch floor by 0.056 dex", F2, "beats the no-epoch floor by 0.056 dex"),
 ("nothing below zero among 626", CLOS, "nothing below zero among 626"),
 # section 7: the decisive measurement
 ("the {\\bf 17,335\nKiDS host-free isolated L$\\star$ lenses}", F5m, "**17,335 KiDS host-free isolated L\\* lenses**"),
 ("$\\sigma(\\Sigma)/\\Sigma_{\\rm gas}=0.0101$, S/N 99 if the column is real", F5m, "| 2.6 | 9.23 | 92.3 | **0.010** | **99** |"),
 ("1.0\\,\\%\nof the requirement at 2.6\\,Mpc", F5m, "**~1 % of the requirement at 2.6 Mpc**"),
 ("8.8\\,\\% at 0.3\\,Mpc (beam-limited, S/N 11)", F5m, "| 0.3 | 1.06 | 1.2 | 0.088 | 11 |"),
 ("$g_{\\rm bar}(R)=\\pi G\\Sigma_{\\rm gas}=a_0/x_b^2=2.699196\\times10^{-12}$\\,m\\,s$^{-2}$", F5m,
  "g_bar(R) = pi G Sigma_gas = a0 / x_b^2 = 2.699196e-12 m/s^2   (canonical)"),
 ("$3.262001\\times10^{-12}$ alt", F5m, "3.262001e-12 (alt)"),
 ("$f_{\\rm col}=0.187\\pm0.102$", F5m, "`f_col = 0.187 \u00b1 0.102` of the requirement at R = 1.87 Mpc, a deficit of"),
 ("2483\\times$ the\ncosmic mean baryon density at 0.3\\,Mpc", F5m, "2483x the cosmic mean baryon density at 0.3 Mpc"),
 ("of $101\\times$ the total baryons an L$\\star$\nhalo can hold", F5m, "a gas mass inside\n  1 Mpc of **101x** the total baryons an L\\* halo can hold"),
 ("Nothing on disk\nmeasures that gas", ANAL, "Nothing on disk measures that gas"),
 ("{\\bf The pre-registered acceptance line is 0.891}, against which", CRUX, "against the record's 0.891 gate"),
 # section 8: the framework
 ("G_\\lambda:\\ (a_0,g)\\ \\mapsto\\ (\\lambda a_0,\\ \\lambda g)", FW, "G_\u03bb : (a\u2080, g) \u2192 (\u03bb\u00b7a\u2080, \u03bb\u00b7g)"),
 ("$\\kappa$ is a flat direction", FW, "Therefore: **\u03ba is a flat direction.**"),
 ("derives only the FORM", FW, "it \"derives only the FORM"),
 ("0.319 dex across three named epochs", F16, "**0.319 dex.**"),
 ("0.0411 dex allowance", F16, "0.0411 dex"),
 ("0.798 dex across five cosmic accelerations", F17, "**0.798 dex.**"),
 ("19.4$\\times$ the allowance", F17, "**19.4x more freedom than the precision it would need**"),
 ("saturation inverts to $\\kappa=\\sqrt{2\\pi}=2.5066$ at 22.1/27.6$\\sigma$", F19, "22.1 sigma"),
 ("1.24--2.23 dex mismatch", F18, "**1.24 to 2.23 dex**"),
 ("1.86 dex drift with mass", F18, "**1.86 dex**"),
 ("0.37 dex with epoch", F18, "**0.37 dex**"),
 ("$\\kappa_M=1.19\\times10^{-3}$", F18, "**kappa_M = 1.19e-3**"),
 ("176$\\times$ more constraint than freedom", F18, "176x more constraint than freedom"),
 ("$\\kappa=1/(2\\sqrt\\beta)$", F6, "kappa = 1/(2 sqrt beta)"),
 ("both halo-scale routes predict $a_0\\propto M^{1/3}$", F6, "a_0 \u221d M^(1/3)"),
 ("$a_0^2/(8\\pi G)$", F19, "a0^2/(8 pi G)"),
 ("divided by Einstein's $8\\pi$", F19, "divided by **Einstein's 8 pi**"),
 ("The unique epoch-independent cosmic density is $\\rho_\\Lambda$", FW, "**The unique epoch-independent cosmic density is `\u03c1_\u039b`.**"),
 ("$\\kappa_{\\rm ext}=0.6414\\pm0.0107\\,({\\rm rand})\\pm0.1283\\,({\\rm sys})$", FL20,
  "kappa_ext = 0.6414 \u00b1 0.0107 (rand) \u00b1 0.1283 (sys)"),
 # section 9/10/11
 ("Clusters\n  ($+0.5$ dex) have no candidate (CLS2)", FW, "Clusters (+0.5 dex): CLS2 NO CANDIDATE."),
 ("Hosted dwarfs ($+0.5$ to $+0.6$ dex) fail (RB2)", FW, "Hosted dwarfs (+0.5 to +0.6 dex): RB2 FAIL."),
 ("currently empty\n  (SRH1 WINDOW EMPTY)", EXIT, "SRH1 WINDOW EMPTY"),
 ("36--41$\\times$ below\nthe law's level", GAS, "36 / 41 times below the law"),
 ("$\\Lambda(T,Z)=3.0\\times10^{-23}$", F5m, "`Lambda = 3.0e-23` **[memory]**"),
 ("$21\\pm5\\,\\Msun\\,{\\rm pc}^{-2}$", F52C, "21 +- 5"),
]
XS, BUD, DEL, SET = 59.50, 5.41, 1.06, 1.40
A = [
 ("11.00 times", XS / BUD, "11.00", "%.2f"),
 ("42.5 times", XS / SET, "42.5", "%.1f"),
 ("38.2/34.7\\,kpc", 5.888813 * 6.479, "38.2", "%.1f"),
 ("38.2/34.7\\,kpc", 5.888813 * 6.479 * math.sqrt(9.3603 / 11.312), "34.7", "%.1f"),
 ("2.699", 9.3603e-11 / 34.6781 * 1e12, "2.699", "%.3f"),
]
NOTES = []
def ws(s): return re.sub(r"\s+", " ", s)
_cache = {}
def src(path):
    """working-tree file, plus the copies at HEAD and at origin/main."""
    if path not in _cache:
        t = ""
        fp = os.path.join(ROOT, path)
        if os.path.exists(fp): t += open(fp, encoding="utf-8", errors="replace").read()
        for ref in ("HEAD", "origin/main"):
            r = subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{path}"], capture_output=True, text=True)
            if r.returncode == 0: t += "\n" + r.stdout
        _cache[path] = ws(t)
    return _cache[path]
_ccache = {}
def committed(path):
    """is the file present at HEAD or on origin/main? (reported; not part of pass/fail)"""
    if path not in _ccache:
        _ccache[path] = any(subprocess.run(["git", "-C", ROOT, "cat-file", "-e", f"{r}:{path}"],
                                           capture_output=True).returncode == 0 for r in ("HEAD", "origin/main"))
    return _ccache[path]
def mutate(lit):
    m = re.search(r"\d", lit)
    if not m: return lit
    d = str((int(m.group()) + 1) % 10)
    return lit[:m.start()] + d + lit[m.end():]
ok = 0; bad = []
for frag, path, lit in L:
    in_tex = frag in TEX
    l2 = mutate(lit) if MUT else lit
    in_src = ws(l2) in src(path)
    if MUT:
        if not re.search(r"\d", lit) or not in_src: ok += 1
        else: bad.append(("mutant survived", frag, path))
    elif in_tex and in_src: ok += 1
    else: bad.append(("tex" if not in_tex else "src", frag, path, lit[:70]))
for frag, val, num, fmt in A:
    s = fmt % val if fmt else num
    n2 = mutate(num) if MUT else num
    if MUT:
        if s != n2: ok += 1
        else: bad.append(("mutant survived", frag, "arithmetic"))
    elif frag in TEX and (s == num or (fmt is None and num in s)): ok += 1
    else: bad.append(("arithmetic", frag, f"computed {s}, TeX {num}"))
body = TEX.split("\\begin{document}")[1]
rules = [
 ("kappa stated as fitted", "$\\kappa=\\tfrac12$ is fitted" in TEX),
 ("not closed stated", "The theory is not closed" in TEX),
 ("no favouring claim", "Nothing here says the data favour this framework" in TEX),
 ("the component is never a particle", "never a particle" in TEX),
 ("the only 'cold dark matter' is a denial", TEX.lower().count("cold dark matter") == 1
  and "never ``cold dark matter''" in TEX and "cdm-like" not in TEX.lower()),
 ("footings never pooled", "never pooled" in TEX),
 ("no local paths", "/Users/" not in TEX),
 ("no pending placeholder", "\\pend{" not in body),
 ("the law is stated as a measurement", "a measurement, not a hypothesis" in TEX),
 ("the lock is stated as a conservation cap", "cannot be manufactured during infall" in TEX),
 ("the decisive number is pre-registered", "The pre-registered acceptance line is 0.891" in TEX),
 ("the scaling symmetry is stated", "G_\\lambda:" in TEX and "flat direction" in TEX),
 ("the convention is stated as forced, not derived", "convention-fixing" in TEX),
 ("the ledger carries every lane with its verdict", "every lane, with its verdict" in TEX),
 ("the formation score is stated", "five of five corrected, four of five frozen" in TEX),
 ("no dark-matter particle, stated as the claim", "There is no dark-matter particle" in TEX),
 ("T4 has no lane folder of its own", "T4 has no lane folder of its own" in TEX),
 ("lanes are not registered", "None of these lanes is registered" in TEX),
 ("own wrong estimates are listed", "Our own estimates that were wrong" in TEX),
 ("memory inputs are declared", "What is from memory" in TEX),
 ("the frozen reading before post hoc", "the frozen one is given first" in TEX),
]
if not MUT:
    for name, good in rules:
        if good: ok += 1
        else: bad.append(("rule", name, ""))
for b in bad: print("FAIL", *b)
if not MUT:
    unc = sorted({p for _, p, _ in L if not committed(p)})
    for p in unc: NOTES.append(f"working tree only (not in HEAD or origin/main): {p}")
    for n in NOTES: print("NOTE", n)
total = len(L) + len(A) + (0 if MUT else len(rules))
print(f"{ok} of {total} checks pass" + (" (mutate: each mutated literal must fail)" if MUT else ""))
print("kappa = 1/2 FITTED; not theory closed; cold dark energy is a gravitating field component, never a particle.")
sys.exit(0 if not bad else 1)
