#!/usr/bin/env python3
"""PAPER70 audit (v1.9): each quoted number appears in the TeX and, as the literal given, in the committed file named
beside it; naming rules; no local paths; no pending placeholder. Run: python3 PAPER70_audit.py (exit 0 only if all pass).
--mutate changes one digit of each source literal; exit 0 only if every mutated literal then fails.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, re, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEX = open(os.path.join(HERE, "PAPER70_field_equations_closure_2026.tex"), encoding="utf-8").read()
C = "closure_2026_11_06/"
Q17 = C + "QX17_covariant_field_equations/RESULT.md"; Q17A = C + "QX17A_ac2q_field_equations/RESULT.md"
Q17B = C + "QX17B_adm_lean_solutions/RESULT.md"; Q17C = C + "QX17C_fd_spherical_solver/RESULT.md"
GB1 = C + "GB1_all_gates_battery/RESULT.md"; KD1 = C + "KD1_unpinned_kq_dust/RESULT.md"
LD1 = C + "LD1_late_decaying_cold/RESULT.md"; HC1 = C + "HC1_hot_fermion_all_gates/RESULT.md"
SE1 = C + "SE1_shock_entropy_sector/RESULT.md"; SE2 = C + "SE2_step_as_systematics/RESULT.md"
EV1 = C + "EV1_environment_reread/RESULT.md"; NOGO = C + "ALL_GATES_NOGO_2026_11_06.md"
CF = C + "CLOSURE_FINAL.md"; VH = "rebuild_2026_10_22/VH1_v3s_health_gates/README.md"
P68 = "qwen_claude_field_theory/papers_2026/PAPER68_screened_khronon_action_2026.zenodo.json"
SEED = C + "SEED_2026_11_06.md"
L = [
 ("$a_0=9.3603\\times10^{-11}$", VH, "9.3603e-11"), ("$1.1312\\times10^{-10}$", VH, "1.1312e-10"),
 ("PAPER67 (DOI 10.5281/zenodo.23968171", P68, "10.5281/zenodo.23968171"),
 ("PAPER68 (DOI 10.5281/zenodo.23990944", P68, "10.5281/zenodo.23990944"),
 ("PAPER69 (DOI 10.5281/zenodo.24025170", SEED, "10.5281/zenodo.24025170"),
 ("$K|P|=a_0u/(1+u)$", Q17, "attained at K|P| = a0 u/(1+u)"),
 ("P equation max rel $3.8\\times10^{-41}$", Q17, "PASS, max rel 3.8e-41"),
 ("khronon equation $1.8\\times10^{-41}$", Q17, "PASS, max rel 1.8e-41"),
 ("full stress tensor $1.2\\times10^{-40}$", Q17, "PASS, max rel 1.2e-40"),
 ("fails at 0.17--0.78", Q17, "K2 then fails at 0.17-0.78"),
 ("fails at 0.23/0.39/$7.3\\times10^{-3}$", Q17A, "K2 fails at 0.23 / 0.39 / 7.3e-3"),
 ("has 12 theorems, standard axioms only", Q17B, "has 12 theorems, standard axioms only"),
 ("converges in 1--6 steps", Q17C, "converges in 1-6 Newton steps"),
 ("(worst $3.9\\times10^{-7}$)", Q17C, "| 3.9e-7 |"),
 ("to $7.1\\times10^{-6}$ of", Q17C, "| 7.1e-6 |"),
 ("on the law to $4.8\\times10^{-6}$", Q17C, "| 4.8e-6 |"),
 ("$4.1\\times10^{-6}$ (Sun)", Q17C, "Full minus weak is 4.1e-6 relative for the Sun"),
 ("$5.4\\times10^{-7}$ (galaxy)", Q17C, "5.4e-7 for the galaxy"),
 ("only 0.71/0.67 of the law", Q17C, "gives 0.71 / 0.67 at 1e3 Lstar"),
 ("at least 3.97\\,$\\sigma_U$", GB1, "by at least 3.97 sigma_U"),
 ("cosmic capture 4.111", KD1, "| 4.111 | 4.112 |"),
 ("$\\chi^2$ 46.3/53.0 against 18.48", LD1, "**46.3, FAIL**"), ("$\\chi^2$ 46.3/53.0 against 18.48", LD1, "**53.0, FAIL**"),
 ("against 18.48", LD1, "line 18.48"),
 ("11.1377\\,eV", HC1, "m = 11.1377 eV"), ("$\\chi^2$ 166.0--194.2", HC1, "chi^2 166.0-194.2"),
 ("FAILS 7 of 9 gates", HC1, "it blocks on 7 of 9 gates"),
 ("(f $\\le$ 0.04)", SE1, "(f <= 0.04)"),
 ("X-COP $+0.440$", SE2, "| **+0.440** |"), ("groups $+0.232$", SE2, "| **+0.232** |"),
 ("Coma UDGs $+1.120$", SE2, "| **+1.120** |"),
 ("about 1.6$\\times$ the phantom", EV1, "about 1.6x the phantom"), ("Coma UDGs 4--46$\\times$", EV1, "4-46x for Coma UDGs"),
 ("largest time-mean on any rung 0.147 of the line", CF, "Largest time-mean on any rung 0.147 of the line"),
 ("$\\le0.33$ / $0.19$", NOGO, "<= 0.33 / 0.19"), ("$\\sim4.2$ / $3.8$", NOGO, "~4.2 / 3.8"),
 ("1.2--3.5 / 0.9--2.9", NOGO, "1.2-3.5 / 0.9-2.9"), ("$\\sim0.9$ / $0.8$", NOGO, "~0.9 / 0.8"),
 ("$\\sim1.7$ / $1.3$", NOGO, "~1.7 / 1.3"), ("Coma UDGs (NOT A TEST, UA1) & $\\sim80$", NOGO, "| Coma UDGs | ~80 |"),
 ("($w\\le0.01$), lensing $\\chi^2\\le18.5$", NOGO, "(w <= 0.01), and lensing chi^2 <= 18.5"),
 ("$\\mu_K\\ge8.9\\times10^6$", NOGO, "mu_K >= 8.9e6"), ("galaxies allow at most 79", NOGO, "galaxies need <= 0.1-79"),
]
SE2R = SE2; CH = C + "FRW_RECONCILIATION_CHAIN/CHAIN.md"; SE3H = C + "FRW_RECONCILIATION_CHAIN/SE3_HANDOFF.md"; CQ2 = "cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/README.md"
OM = "campaign_fresh_gravity/DR4_OUTCOME_MAP_2026-10-15.md"; AT2 = "rebuild_2026_10_22/AT2_a0z_on_disk_samples/README.md"
V3W = "rebuild_2026_10_22/V3W_v3s_weak_spots/README.md"; PRED = "closure_2026_11_07/PREDICTIONS_2026_11_07.md"
L += [
 ("multiplies the induced lapse term by $(1-z)^2$, not the legacy $(1-2z)^2$", CH, "The legacy (1 - 2z)^2 is wrong for A1 as defined"),
 ("$c^2=z/(1-z+z^2)$", CH, "UV c^2 = z/(1-z+z^2)"),
 ("Lean, 11 theorems, standard axioms only", SE3H, "| Lean, 11 theorems, standard axioms only |"),
 ("MUTATE 3/3 fail", SE3H, "3/3 planted false claims fail"),
 ("bounded by $1.1\\times10^{-10}$", SE3H, "The bound is 1.1e-10 (was 2.2e-10)"),
 ("AC7 Q2 / AC10--AC15 post-Newtonian chain carries the legacy factor", SE3H, "AC7 Q2 / AC10-AC15 post-Newtonian chain still carries the literal legacy factor"),
 ("$+0.440$ [$+0.372$, $+0.484$]", SE2R, "| **+0.440** | [+0.412, +0.463] | [+0.372, +0.484] |"),
 ("$+0.408$ [$+0.341$, $+0.451$]", SE2R, "| **+0.408** | [+0.380, +0.431] | [+0.341, +0.451] |"),
 ("$+0.232$ [$+0.078$, $+0.362$]", SE2R, "| **+0.232** | [+0.156, +0.318] | [+0.078, +0.362] |"),
 ("$+0.194$ [$+0.041$, $+0.324$]", SE2R, "| **+0.194** | [+0.119, +0.279] | [+0.041, +0.324] |"),
 ("$+1.120$ [$+0.541$, $+1.718$]", SE2R, "| **+1.120** | [+0.823, +1.421] | [+0.541, +1.718] |"),
 ("$+1.075$ [$+0.472$, $+1.673$]", SE2R, "| **+1.075** | [+0.774, +1.372] | [+0.472, +1.673] |"),
 ("X-ray ellipticals & $+0.067$ & $+0.050$", SE2R, "| +0.067 | [-0.064, +0.179] |"),
 ("X-ray ellipticals & $+0.067$ & $+0.050$", SE2R, "| +0.050 | [-0.078, +0.159] |"),
 ("KiDS early/late & $+0.085$ & $+0.084$", SE2R, "| +0.085 | [-0.000, +0.162] |"),
 ("KiDS early/late & $+0.085$ & $+0.084$", SE2R, "| +0.084 | [+0.001, +0.163] |"),
 ("bright M31 dSphs (21) & $+0.228$ & $+0.219$", SE2R, "| +0.228 | [+0.006, +0.455] |"),
 ("bright M31 dSphs (21) & $+0.228$ & $+0.219$", SE2R, "| +0.219 | [-0.006, +0.447] |"),
 ("($z$ 3.04 / 2.55)", SE2R, "| 3.04 | 0.0025 |"), ("($z$ 3.04 / 2.55)", SE2R, "| 2.55 | 0.0087 |"),
 ("$\\gamma_\\infty$ 1.0019 / 1.0100", CQ2, "pipeline γ_inf V3S (spread) | 1.0019 (0.0200) | 1.0100 (0.0068)"),
 ("plain QUMOND (1.1494 / 1.2081)", CQ2, "plain QUMOND (1.1494 / 1.2081)"),
 ("SHA-256 1d65509dbf", CQ2, "SHA-256 1d65509dbf"),
 ("EXCLUDED for $\\hat\\gamma$ in 1.083--1.23", PRED, "v3s is EXCLUDED for γ̂ in 1.083 – 1.23"),
 ("$\\sigma_{\\rm sys}<0.048$ / 0.058", PRED, "σ_sys(b) < 0.048 canonical / 0.058 alt"),
 ("(owner decision 413c1c8e24)", PRED, "413c1c8e24"),
 ("KILL iff $R-1\\ge\\max(0.01,3\\sigma_R)$", PRED, "KILL iff R − 1 ≥ max(0.01, 3σ_R)"),
 ("(N 30,000, $\\sigma_{\\rm sys}$ 0.020)", PRED, "(N = 30,000, σ_sys 0.020, canonical)"),
 ("all 52 cells are BLOCKED", AT2, "52 (sample, z*) cells, 52 BLOCKED"),
 ("(0.30--0.60\\,dex) is 4--11$\\times$", AT2, "common mode (0.30-0.60 dex) is 4-11x above the largest e_3σ (0.084 dex)"),
 ("(0.084\\,dex at $z^*$ 2.33)", AT2, "0.055 / 0.072 / 0.074 / 0.084 dex at z* 1.0 / 1.2 / 1.5 / 2.33"),
 ("to $\\le6.5\\times10^{-5}$ at 310\\,kpc", V3W, "M_lens/M_dyn = 1 to ≤ 6.5e-5 (at 310 kpc)"),
 ("$A=1.129\\pm0.206$ (canonical)", V3W, "A = 1.129 ± 0.206"), ("$1.035\\pm0.187$ (alt)", V3W, "A = 1.035 ± 0.187"),
]
OQ2 = C + "OQ2_one_quantity_powered/RESULT.md"; FS2 = C + "FS2_fold_viscosity_free/README.md"
OE = "closure_2026_11_07/OUTER_EDGE_CHECK_2026_11_07.md"; C7 = "closure_2026_11_07/CLOSURE_2026_11_07.md"
Q76 = C + "QX7_unified_cold_switch/iter_6_efe_capped_wells/README.md"; Q77 = C + "QX7_unified_cold_switch/iter_7_collisionless_remnant/README.md"
Q32 = C + "QX32_aspherical_hse_field/README.md"
L += [
 ("(OQ2 kept by the owner)", C7, "OWNER: \"Keep OQ2\""),
 ("gap up to 0.497 / 0.483", OQ2, "0.497"), ("gap up to 0.497 / 0.483", OQ2, "0.483 / 0.372"),
 ("($F_{\\rm web,max}$ 0.00481 / 0.00435;", OQ2, "F_web,max = 0.00481"), ("0.00481 / 0.00435", OQ2, "F_web,max = 0.00435"),
 ("SEPARATED NO, as frozen", OQ2, "**NO** (as frozen"),
 ("S1 reading is DEAD on both footings, every start", OQ2, "DEAD, every start, both f*"),
 ("DIFFERS, both footings", FS2, "DIFFERS (frozen)"), ("fold 1.2\\,\\% earlier", FS2, "reaches J_reg 1.2 % before"),
 ("(DIFF-TIME EARLIER, edge-carried)", FS2, "**DIFF-TIME EARLIER**"), ("read SAME-REACH", FS2, "SAME-REACH (r 0.99990-1.00004)"),
 ("no row is REGULAR", FS2, "No row is REGULAR"),
 ("NO EDGE IN THE ACTION", C7, "NO EDGE IN THE ACTION"),
 ("$\\Sigma/X=2+\\rho_{\\rm ph}/\\rho_{\\rm DE}\\ge2$", OE, "Sigma/X = 2 + rho_ph/rho_DE"),
 ("FAIL (clusters, 0/20 cells, both footings)", Q76, "FAIL (clusters, 0/20 cells both footings)"),
 ("misfit to +0.870", Q76, "+0.870 canonical"),
 ("SHAPE FAIL, both footings", Q77, "SHAPE FAIL, both footings"),
 ("NEGLIGIBLE ($\\le$\\,0.005\\,dex, wrong sign)", Q32, "NEGLIGIBLE (<= 0.005 dex, wrong sign)"),
]
EW1 = "closure_2026_11_07/EW1_everywhere_matrix/README.md"; EW3 = "closure_2026_11_07/EW3_two_switch/README.md"
PX1 = "closure_2026_11_07/PI6_BLEND_ADOPTION_CASE_2026_11_07.md"
L += [
 ("(23 rows $\\times$ 17 columns, every cell sourced)", EW1, "23 rows x 17 columns"),
 ("NO ROW PASSES EVERY COLUMN", EW1, "NO ROW PASSES EVERY COLUMN"),
 ("UDGs, causality with well-posedness, and a derived $a_0$ stay uncovered", EW1, "Three columns stay uncovered by every framework row"),
 ("(+0.123 / +0.103)", EW1, "**PASS +0.123 / +0.103**"),
 ("EW3 keeps the map row only, no graded number", EW3, "EW3 keeps the map row only"),
 ("whose case for and against was written for the owner (PX1", PX1, "It adopts nothing"),
]
WL1 = "closure_2026_11_07/WL1_web_law_switch/RESULT.md"
L += [
 ("FAIL (stage 2, population phantom)", WL1, "FAIL (stage 2)"),
 ("all 59 points lie inside", WL1, "K-G6 KiDS 59 pts"),
 ("$q_{\\rm pop}$ 0.936 / 1.079", WL1, "**0.936** (r_pop 3.75)"), ("0.936 / 1.079", WL1, "**1.079** (r_pop 4.32)"),
 ("against a line of 0.0354", WL1, "<= 0.0354 (r <= 1.072)"),
 ("($\\times$26 / $\\times$30;", WL1, "FAIL, x26 / x30"),
 ("$\\times$11 / $\\times$12 self-consistent", WL1, "reported (x11 / x12)"),
 ("any key that keeps the law on where KiDS needs it", WL1, "keeps the law on where KiDS needs it"),
]
FA2 = "closure_2026_11_07/FA2_local_action_search/RESULT.md"; FA3 = "closure_2026_11_07/FA3_nonlocal_action_search/RESULT.md"
L += [
 ("no local action found; C1, C2 and C3 all FAIL", FA2, "no local action found. C1 FAIL, C2 FAIL, C3 FAIL, both footings"),
 ("KiDS shift +0.283 / +0.260", FA2, "**+0.283 FAIL**"), ("+0.283 / +0.260", FA2, "**+0.260 FAIL**"),
 ("the natural local form does not screen", FA2, "natural local form does not screen"),
 ("to 0.3\\,Mpc or less", FA2, "L_max =\n0.3 Mpc"),
 ("the static operator is not elliptic (radial)", FA2, "the static operator is not elliptic (radial only)"),
 ("NO CANDIDATE SURVIVES, both footings", FA3, "No candidate survives"),
 ("(r 75.4 / 78.8;", FA3, "W1 web (r 75.4 / 78.8 at tau_gal)"),
 ("NO VERDICT on G1--G7", FA3, "**NO VERDICT** (G1-G7; history not carried)"),
 ("I1's MUTATE M1 did not bite as frozen", FA3, "**NO, as frozen**"),
 ("peak RSS (1.87\\,GB)", FA3, "ru_maxrss read 1.87 GB"),
]
EW2 = "closure_2026_11_07/EW2_aest_nonlinear/README.md"
L += [
 ("NO-GO FOR THE CLASS, both footings", EW2, "NO-GO FOR THE CLASS"),
 ("$r$ 1.037 / 1.045 at 10", EW2, "r = 1.037 / 1.045 at mu 10"),
 ("($\\mu\\le0.063$\\,Mpc$^{-1}$)", EW2, "PASS only for mu <= 0.063"),
 ("the gap is $\\times$160", EW2, "(gap x160;"), ("\\texttt{window\\_empty}", EW2, "Lean `window_empty`"),
 ("static dust $\\le$\\,0.03\\,$M_b$", EW2, "static dust <= 0.03 M_b"),
 ("need of 2.39 / 2.07\\,$M_b$", EW2, "need 2.39 / 2.07 M_b"),
 ("(0\\,\\% of X-COP radii)", EW2, "0 % at every host member"),
 ("Primary CMB FAIL (read)", EW2, "FAIL [C7 read, not rerun]"),
 ("no label moves & EW2", EW2, "no label moves"),
]
Z70 = "qwen_claude_field_theory/papers_2026/PAPER70_field_equations_closure_2026.zenodo.json"
L += [("deposited as DOI 10.5281/zenodo.24040313", Z70, '"doi": "10.5281/zenodo.24040313"')]
NA2 = "closure_2026_11_07/NA2_compact_baryon_remnant/RESULT.md"
L += [
 ("FAILS (rows), both footings: X-COP shape, groups shape, Bullet", NA2, "canonical: FAILS (X-COP shape, groups shape, Bullet)"),
 ("(lower bound 0.054 / 0.050", NA2, "lower bound B1 0.054 / 0.050"),
 ("every key is S1 DEAD (gaps 1.50", NA2, "gap 1.50 dex"), ("1.50--2.53\\,dex", NA2, "60.9 vs 0.178; gap 2.53"),
 ("$10^2$--$1.8\\times10^2\\,M_\\odot$", NA2, "window shrinks to\n1e2-1.8e2 Msun"),
 ("(rms 0.1208 / 0.1138)", NA2, "+0.0185 / **0.1208**"), ("0.1208 / 0.1138", NA2, "+0.0173 / **0.1138**"),
 ("between the gas and the stars", NA2, "The extra mass lies between the gas and the stars"),
 ("11 / 9 of 20 (canonical) and 10 / 8 (alt) against 16 needed", NA2, "pass 11 / 9 of 20 (canonical) and 10 / 8 (alt), against the 16 needed"),
 ("peaked at 1188\\,MB", NA2, "peaks at 1188 MB"),
]
NA1 = "closure_2026_11_07/NA1_fa1_last_doors/RESULT.md"
L += [
 ("I5 DEAD BY REDUCTION, both footings", NA1, "I5 DEAD BY REDUCTION / DEAD BY REDUCTION; I7 DEAD / DEAD (canonical / alt)"),
 ("$[-6.2\\times10^{-15},+1.3\\times10^{-15}]$", NA1, "B X in [-6.2e-15, +1.3e-15]"),
 ("at most $6.8\\times10^{-20}$", NA1, "at most 6.8e-20"),
 ("no monotone weight passes S1", NA1, "FAIL: no monotone F"),
 ("web lensing $r$ 72--86 against 1.072", NA1, "r stays at 72-86 against a line of 1.072"),
 ("(2.240 / 2.463\\,meV)", NA1, "2.240e-3 eV"), ("2.240 / 2.463", NA1, "2.463e-3 eV"),
 ("forms only at $z$ of about 9", NA1, "the network forms only at z of about 9"),
 ("($w$ 0.167 at $z$ 3400)", NA1, "(w 0.167 at z 3400)"),
 ("at most 3.7$\\times10^{-4}$ of the baryons", NA1, "**3.7e-4**"),
 ("at most 1.3$\\times10^{-8}$ in clusters", NA1, "walls <= 1.3e-8"),
 ("gauge monopoles are particle-like", NA1, "gauge monopoles are particle-like"),
 ("MUTATE M2 and M4 bite only weakly", NA1, "**bites** (weak"),
 ("the first run peaked at 1.025\\,GB", NA1, "The first run peaked at 1.025 GB RSS"),
 ("the rerun at 0.858\\,GB", NA1, "Peak RSS: 0.858 GB main"),
]
EW4 = "closure_2026_11_07/EW4_nuhdm_resolve/README.md"
L += [
 ("does NOT pass every EW1 column", EW4, "nuHDM does NOT pass every column EW1 has"),
 ("X-COP 6/7 consistent", EW4, "**6/7 consistent**"),
 ("$M_{\\rm req}/M_b$ 1.8--3.4", EW4, "M_req/M_b = 1.8-3.4"),
 ("32--62\\,\\% of the supply", EW4, "That uses 32-62 % of the fair-share"),
 ("phase space never binding", EW4, "Phase space never binds"),
 ("(14/20 / 11/20 against 16;", EW4, "**14/20 / 11/20** (line 16)"),
 ("ellipticals FAIL 0/7", EW4, "**FAIL 0/7** (phase space)"),
 ("KiDS G6 $-0.098$\\,dex FAIL", EW4, "**G6 -0.098 / -0.098 dex**"),
 ("+2716 / +2599", EW4, "Delta +2716 / +2599"),
 ("SPARC PASS (not robust)", EW4, "**PASS (not robust)**"),
 ("NO POWER on X-COP", EW4, "**NO POWER**"),
 ("7 clusters, not 12", EW4, "X-COP is 7 clusters, not 12"),
 ("AGC 114905 and Malin 1 FAIL for any fermion", EW4, "chi2_min over ANY fermion 843.6"),
]
OD = "closure_2026_11_07/OWNER_DECISION_2026-11-07_ADOPT_PI6_BLEND.md"
L += [
 ("The owner adopted the $\\Pi^6$ blend", OD, 'answered **"Adopt the blend"**'),
 ("$F(\\Pi)=b^2f(\\Pi/b)$ with $b=\\rho_{\\rm DE}$", OD, "F = gamma b^2 f(Sigma/b), with b = rho_DE"),
 ("$f(q)=(122363904/44610575)\\,q^6$", PX1, "f = (122363904/44610575) q^6 exactly"),
 ("($m=6>d+2=5$)", OD, "(m = 6 > d + 2 = 5)"),
 ("$C^4$ convex blend", OD, "It is C4 and convex"),
 ("with $b=X$", OD, "blend with b = X"),
 ("(largest effect $\\le1.4\\times10^{-4}$\\,dex)", OD, "largest effect <= 1.4e-4 dex"),
 ("well-posedness is local in time", OD, "Well-posedness is **local in time**"),
 ("non-radial ($l\\ge1$) modes are untested", OD, "Non-radial (l >= 1) modes are untested"),
 ("folds are unchanged", OD, "**Folds are unchanged.**"),
 ("power 6 is not forced", OD, "**Power 6 is not forced.**"),
 ("The AC16 row remains the label of the raw switch", OD, "The AC16 row remains the label **of the raw switch**"),
]
KX1 = "closure_2026_11_07/KX1_kids_joint_budget/RESULT.md"; DED = "closure_2026_11_07/DEDUCTION_2026_11_07.md"
L += [
 ("NO VERDICT as frozen (the 4$\\times$ MUTATE cannot bite on cell C3)", KX1, "**DOES NOT BITE** -> frozen NO VERDICT"),
 ("no cell softens, both footings", KX1, "no cell softens"),
 ("KILL HOLDS on C2 and C4", KX1, "| C2 (1.47, 3.5) | **KILL HOLDS**"),
 ("the raw +0.15--0.20\\,dex excess", DED, "Brouwer's raw +0.15-0.20"),
 ("$-0.21$ to $+0.05$\\,dex (canonical)", KX1, "| 1 (9.4, 122-285) | +0.029 | -0.207"),
 ("$-0.25$ to $+0.01$ (alt)", KX1, "the posterior excesses are -0.249 / -0.019 / -0.034 / +0.013"),
 ("0.05--0.24\\,dex (canonical) and 0.00--0.20 (alt)", KX1, "0.05-0.24 dex (canonical) and 0.00-0.20 (alt)"),
 ("against the window's 0.17--0.25", KX1, "The window's\n0.17-0.25 dex"),
 ("canonical C4's hold rests on it", KX1, "So canonical C4's hold rests on the extrapolated bin"),
 ("The escape cell, a late kick above the galaxy escape speed, is closed by X-COP", DED, "**X-COP FAILS at every kick**"),
 ("closed by KiDS once the hot gas is measured rather than assumed", DED, "excluded by lensing once the gas is measured rather than assumed"),
 ("so every form of the puff cell is closed", DED, "So Cell B is closed on every form"),
]
UA1 = "closure_2026_11_07/UA1_fragile_rows/RESULT.md"
L += [
 ("\\emph{Coma UDGs: NOT A TEST} on both footings", UA1, "Coma UDGs drop to NOT A TEST"),
 ("2 of 9 are admissible", UA1, "That is 2 of 9, NOT A TEST"),
 ("No orbit or proper motion exists on disk for any of the 9", UA1, "No orbit or proper motion exists on disk for any of the 9 UDGs"),
 ("5 or more would be graded (not computed)", UA1, "5 or more UDGs would be graded. Those cells were not computed"),
 ("it does not say systematics explain the step", UA1, "It does **not** say that systematics explain the UDG step"),
 ("$+0.259$ [$+0.052$, $+0.459$] (canonical)", UA1, "+0.259, 95 % [+0.052, +0.459]"),
 ("$+0.221$ [$+0.009$, $+0.415$] (alt)", UA1, "+0.221, 95 % [+0.009, +0.415]"),
 ("the cross-catalogue term is 0.064\\,dex", UA1, "m_G = 0.064 dex"),
 ("the Eckmiller group masses are PROVISIONAL", UA1, "so they are PROVISIONAL here"),
 ("drops the median by 0.088 / 0.087\\,dex", UA1, "The median drops by 0.088 / 0.087 dex"),
 ("stay EXPLAINED (15 of 25)", UA1, "leaving 15 of 25, still EXPLAINED"),
 ("\\textbf{The residue is X-COP + groups + CMB lensing}", UA1, "**X-COP + groups + CMB lensing**"),
]
CE2 = "closure_2026_11_07/CE2_late_heated_window/RESULT.md"
L += [
 ("FAIL on every cell, C3 included, both footings", CE2, "FAIL, all four cells, both footings, C3 included"),
 ("($\\chi^2$ 8.70--11.69;", CE2, "PASS 8.70 (0.13)"), ("8.70--11.69", CE2, "PASS 11.69 (3.12)"),
 ("($R_f$ 1.000)", CE2, "Rf = 1.000 at every z < 1 bin"),
 ("X-COP +0.324 / +0.287", CE2, "C3 fails GX (+0.324 / +0.287"),
 ("(inner bin +0.48", CE2, "the centre (+0.48)"),
 ("groups 0--1 of 20", CE2, "GG (0-1 of 20)"),
 ("Mach 1.7--1.9", CE2, "Mach is 1.7-1.9"),
 ("arrived after the numbers", CE2, "KX1 narrowing (arrived AFTER CE2's numbers"),
 ("peaked at 1.48\\,GB", CE2, "peak RSS was 1.48 GB"),
 ("The elimination is complete for every ingredient the record can build", DED, "The elimination is complete for every ingredient the record can build"),
 ("Which of the three gives way is not decidable on disk", DED, "Which of the three gives way is not decidable on disk"),
 ("not independent evidence (QX15)", DED, "(QX15: not independent evidence)"),
]
RS3 = "closure_2026_11_07/RS3_residual_surface/RESULT.md"
L += [
 ("NO VERDICT as frozen: the Newtonian-$f$ MUTATE does not bite", RS3, "**Label: NO VERDICT as frozen. The Newtonian-f MUTATE (M2) does not bite"),
 ("on the frozen variable list (from the brief)", RS3, "g_obs is on the brief's frozen list"),
 ("Main reading NO PAIR, both UDG readings", RS3, "The main reading is NO PAIR, under both UDG"),
 ("($\\chi^2/N$ 0.433 / 0.440)", RS3, "chi^2/N 0.433, SPARC z -1.96 | 0.440"),
 ("($\\chi^2/N$ 1.483 / 1.434)", RS3, "depth+sigma GRID6, chi^2/N 1.483"), ("1.483 / 1.434", RS3, "**1.434; SPARC -3.87"),
 ("$-4.49$ / $-3.87$", RS3, "SPARC -4.49, X-COP +3.82, UDGs +3.46"),
 ("+3.82 / +3.48 and the UDGs at +3.46 / +3.48", RS3, "X-COP +3.48, UDGs +3.48"),
 ("no pair passes leave-one-out after dropping any class", RS3, "Without g_obs, no pair passes leave-one-out after dropping any class"),
 ("GB1's 145 galaxies", RS3, "**SPARC N:** 145 (GB1's set"),
]
Q17D = "closure_2026_11_07/QX17D_blend_field_equations/RESULT.md"
L += [
 ("(residuals $\\le7.1\\times10^{-40}$)", Q17D, "PASS 7.1e-40"),
 ("fails the metric equation by up to 14\\,\\%", Q17D, "**FAIL 1.4e-1**"),
 ("CERTIFIED with $\\Pi F'(\\Pi)\\,h_{mn}$ in the stress tensor", Q17D, "R2 CERTIFIED, for G and for B"),
]
ws = lambda t: re.sub(r"\s+", " ", t)
cache = {}
def src(p):
    if p not in cache:
        fp = os.path.join(ROOT, p)
        if os.path.exists(fp): cache[p] = ws(open(fp, encoding="utf-8").read())
        else:  # local main may lag origin: read the committed file from origin/main
            import subprocess
            r = subprocess.run(["git", "-C", ROOT, "show", "origin/main:" + p], capture_output=True, text=True)
            cache[p] = ws(r.stdout) if r.returncode == 0 else ""
    return cache[p]
GL1 = "closure_2026_11_07/GL1_limber_kernel_reread/RESULT.md"; GL3 = "closure_2026_11_07/GL3_kernel_reread_web/RESULT.md"
CK1 = "closure_2026_11_07/CK1_kicked_carrier_regrade/RESULT.md"; CK2 = "closure_2026_11_07/CK2_release_speed/RESULT.md"
CK4 = "closure_2026_11_07/CK4_kicked_carrier_cosmology/RESULT.md"; UNI = "closure_2026_11_07/UNIFICATION_STATEMENT_2026_11_07.md"
L += [
 ("min $\\rho_{\\rm ph}/\\rho_{\\rm DE}$ +0.000507 / +0.000462", CK2, "+0.000507"), ("+0.000507 / +0.000462", CK2, "| +0.000462 |"),
 ("NO RELEASE TERM, both footings", CK2, "**NO RELEASE TERM (canonical and alt).**"),
 ("FAILS (rows) at every $v_k$ on both footings", CK1, "FAILS (rows) at every v_k in {500, 525, 550, 575, 600, 625, 650} km/s on both footings"),
 ("the binding gate is the SPARC high-mass tail", CK1, "binding gate\nT (SPARC high-mass tail"),
 ("$v_k$ 550 passes and 575 / 600 fail the forest", CK4, "575 and 600: FAIL** on GFo"),
 ("NO VERDICT (the CMB-lensing gate has no power)", CK4, "NO VERDICT (GL has no power)"),
 ("0.98--1.006 at $L$ 20--400", GL1, "1.005 / 1.006 / 1 / 0.991 / 0.984 / 0.980"), ("against 0.045--33 without it", GL1, "0.045 / 0.239 / 1 / 5.26 / 15.0 / 33.0"),
 ("$\\mu_J$ $2.51\\times10^4$", GL1, "mu_J 2.51e4"), ("$\\mu_J$ 631; the binding side is BBN", GL1, "mu_J **631**"),
 ("($\\mu_B$ $8.89\\times10^6$, unchanged)", GL1, "BBN (mu_B 8.89e6)"),
 ("$\\mu_{\\min}$ 631, still above 79.43", GL1, "**HOLDS**: 631 > 79.43"),
 ("best $\\Delta\\chi^2$ 92.59, 0/35", GL1, "best 92.59, 0/35 pass"), ("best 2.78, 1/35 ($\\beta$ 0.80, $\\mu_0$ 1259)", GL1, "beta 0.80, mu0 1259"),
 ("closest 17.87, 0/31", GL1, "closest 17.87, 0/31"), ("31/31 inside the lensing line", GL1, "**31/31**"),
 ("window 857 / 857, clusters 0 / 857", GL1, "FAIL (clusters) [0/857]"),
 ("J1 $\\Delta\\chi^2_{TT}$ 4.30 / 1.05 / 77.2 / 3.47", GL1, "J1 dchi^2_TT 4.30 / 1.05 / 77.2 / 3.47"),
 ("from $\\times316$ to $\\times7.9$", GL1, "(x316) to 631 / 79 (x7.9)"),
 ("$r$ 74.74 / 89.36 & 32.53 / 38.66", GL3, "| 74.74 / 89.36 | 32.53 / 38.66 |"),
 ("$\\Delta\\chi^2$ 0.019, PASS & 33.5 / 34.1, FAIL", GL3, "0.019 / 0.019, PASS | 33.5 / 34.1, FAIL"),
 ("none / none / none & 2.0 / 1.5 / 0.75", GL3, "none / none / none | 2.0 / 1.5 / 0.75"),
 ("$M^*$ $\\Delta\\chi^2$ 876.7, FAIL & 0.016; K-mono 0.52", GL3, "876.7 / 541.7, FAIL | 0.016 / 0.52"),
 ("NA1 I5, web $r$ & 72.2--89.4 & 27.4--38.7", GL3, "| 72.2-89.4 | 27.4-38.7 |"),
 ("75.39 / 78.77 & 19.12 / 18.75", GL3, "| 75.39 / 78.77 | 19.12 / 18.75 |"),
 ("KiDS still fails there ($-0.074$)", GL3, "KiDS at 1 Mpc is -0.074 / -0.074"),
 ("$\\mu_w$ 0.63 / 1.0, gap $\\times10$ / $\\times16$", GL3, "0.63 / 1.0 (gap x10 / x16)"),
 ("$F_{\\rm web,max}$ 0.00481 / 0.00435 & 0.00798 / 0.00720", GL3, "0.00481 / 0.00435; DEAD | 0.00798 / 0.00720; DEAD"),
 ("$\\Delta\\chi^2$ 140.1 / 70.0, FAIL & 0.006 / 0.004, PASS", GL3, "140.1 / 70.0, FAIL | 0.006 / 0.004, PASS"),
 ("(to $\\le4.5\\times10^{-16}$ on the web side)", GL3, "the largest\n  relative difference is 4.5e-16"),
 ("CK1 FAILS it on every kick", CK1, "FAILS (rows) at every v_k"),
]
_u = src(UNI); _i = _u.index("## 3. The statement"); _q = ws(_u[_i + len("## 3. The statement"):].replace("Kappa = 1/2 FITTED; not theory closed.", "")).strip()
_tq = ws(TEX[TEX.index("\\begin{quote}") + len("\\begin{quote}"):TEX.index("\\end{quote}")].replace("\\_", "_")).strip()
UQ_OK = (_q == _tq)
NC2 = "closure_2026_11_07/NC2_born_clumped_cosmology/RESULT.md"; NC3 = "closure_2026_11_07/NC3_member_vs_field_early_types/RESULT.md"
L += [
 ("a bias of only 0.99670--1.00142", NC2, "Tolerated b 0.99670-1.00142 (canonical)"),
 ("carries 45--1866", NC2, "b = 45-1866 at recombination"),
 ("$\\Delta$ +4.10e4 / +5.57e5 / +6.35e6", NC2, "b 1.2: +4.10e4 / +4.08e4; 1.5: +5.57e5; 2.0: +6.35e6"),
 ("at most 0.13--0.28\\,\\% of the component in clumps", NC2, "The forest allows at most 0.13-0.28 % of the component in clumps"),
 ("(+75.9 / +239.8) and passes at $10^{13}$", NC2, "84.4 (+75.9) **FAIL** | 248.3 (+239.8) **FAIL**"),
 ("UNRESOLVED by rule, both footings", NC3, "## Label: UNRESOLVED on both footings"),
 ("+0.011 [$-0.044$, +0.065] / +0.012 [$-0.043$, +0.068]", NC3, "| 95 % CI | [-0.044, +0.065] | [-0.043, +0.068] |"),
 ("at most about 16\\,\\% extra mass", NC3, "carry no more than about 16 % extra"),
 ("stripping cannot hide a residue", NC3, "The stripping budget does not rescue a hidden residue"),
 ("with every interval containing 0", NC3, "Every CI contains 0"),
 ("the exhaustion covers initial conditions as well as mechanisms", DED, "covers mechanisms AND initial conditions"),
]
NC4 = "closure_2026_11_07/NC4_born_clumped_spectrum/RESULT.md"
L += [
 ("FAILS (rows) on both footings, binding K3", NC4, "**FAILS (rows): K3, K5; binding K3**"),
 ("hold 0.0133 of the cosmic baryons", NC4, "| host baryons inside R500 / rho_b | 0.0133 | 0.0133 |"),
 ("0.0091 / 0.0078 of the cold component", NC4, "C = 0.0091 / 0.0078 of the cosmic cold dark energy (A 110 / 128)"),
 ("(0.025 / 0.022 in the most generous bracket)", NC4, "bracket C = 0.025 / 0.022 (A 40 / 45)"),
 ("110 / 128 times the observed host abundance (40 / 45 generous)", NC4, "(A 40 / 45)"),
 ("is 0.75 / 0.68", NC4, "C <= 0.75 / 0.68"),
 ("rms 0.166 / 0.143 at best", NC4, "rms 0.166 / 0.143 (line 0.10)"),
 ("(slope 0.6--2.3 / 0.8--2.2 per dex)", NC4, "| 0.6-2.3 per dex | 0.8-2.2 per dex |"),
 ("($\\langle V/V_{\\max}\\rangle$ 0.403--0.465)", NC4, "<V/Vmax> was 0.403-0.465"),
 ("still leave the shortfall $\\ge13$", NC4, "A factor of 2-3 would still leave A >= 13"),
 ("$r_c$ 50--100\\,kpc passes NA2's per-bin rule for 7/7 clusters", NC4, "r_c **50, 75, 100 kpc**"),
 ("($r_c$ 100\\,kpc: rms 0.086 / 0.086)", NC4, "rms 0.086, bins +0.04 / +0.02 / -0.05; alt F 3.37,\n  rms 0.086"),
 ("(0.0091 / 0.0078; at most 0.025 / 0.022", NC4, "C = 0.0091 / 0.0078"),
]
MS3 = "closure_2026_11_06/MS3_moving_sun_light/README.md"
L += [
 ("MS3: PASS (moving Sun, scoped), FINAL for the door, with no MS4", MS3, "There is no MS4"),
 ("MS3: PASS (moving Sun, scoped)", MS3, "**PASS (moving Sun, scoped).**"),
 ("the largest at 0.617 of it (G1 Mars, M490 REFLECT bracket)", MS3, "| G1 Mars | [0, 0.617] | M490 REFLECT"),
 ("not on a converged extrapolation", MS3, "So the PASS rests on the frozen time-spread classes (NOISE, OSCILLATORY), not on a converged extrapolation."),
 ("a different memory allocator setting", MS3, "MallocMediumZone=0"),
]
F1A = "closure_2026_11_07/F1A_primary_cmb_audit/RESULT.md"; GL4 = "closure_2026_11_07/GL4_qx15_cells_kernel/RESULT.md"
L += [
 ("deposited as DOI 10.5281/zenodo.24044606", Z70, '"doi": "10.5281/zenodo.24044606"'),
 ("F1 CONFIRMED, both footings", F1A, "## Label: F1 CONFIRMED on both footings"),
 ("$\\Delta$ +172,915.6 / +166,674.4", F1A, "| **G1** DeltaMB on B2 | **+172,915.6** | **+166,674.4** |"),
 ("($\\Delta_{\\rm cal}$ $-65.21$ / $-65.07$ against $\\chi^2_{\\rm cal}$ 3805.37)", F1A, "| **G2** Delta_cal (chi2_cal 3805.37) | **-65.21** (adequate) | **-65.07** (adequate) |"),
 ("$\\omega_d/\\omega_b$ 5.410 / 5.412 (0.973 of 5.562)", F1A, "**5.410** (0.973 of 5.562"),
 ("($Q\\le3.4\\times10^{-11}$ at $z$ 1100)", DED, "(Q <= 3.4e-11 at z 1100)"),
 ("(CLASS differs by 3.8)", F1A, "CLASS and CAMB differ by 3.8 on Pcut"),
 ("one check peaked at 1.81\\,GB for 10\\,s", F1A, "KA-P peaked at 1.81 GB for 10 s"),
 ("QX15 cells C1 / C2 / C4 (found by F1A)", F1A, "QX15's cell Delta_cell and P1 numbers sit on the wrong kernel"),
 ("$\\Delta_{\\rm cell}$ +0.66 / +0.27 / +0.57, PASS", GL4, "| C1 | +0.66 / +0.67 | PASS"),
 ("$+1.1\\times10^{-5}$ / $+6.5\\times10^{-6}$ / $+1.1\\times10^{-5}$", GL4, "| +6.5e-6 / +6.6e-6 | PASS"),
 ("$\\Delta_{\\rm cell}$ +5.95 / +6.03, TENSION", GL4, "| C3 | +5.95 / +6.03 | TENSION"),
 ("$+4.1\\times10^{-5}$ / $+4.2\\times10^{-5}$, PASS", GL4, "| +4.1e-5 / +4.2e-5 | PASS | **MOVES** to PASS"),
 ("+192.46 / +189.91, bites", GL4, "+192.46 / +189.91, bites"),
 ("its one unresolved failure is a contradiction rather than a gap", DED, "Its one unresolved failure is now a proven contradiction, not\na gap"),
]
KQ1 = "closure_2026_11_07/KQ1_kq_dust_cluster_core/RESULT.md"
L += [
 ("CANNOT FORM CORE, both footings", KQ1, "overall: **CANNOT FORM CORE**"),
 ("for every $\\mu_K$ in 0.1--$10^4$", KQ1, "No mu_K in 0.1-1e4 Mpc^-1"),
 ("falls like $\\ln(r_s/r)$", KQ1, "which falls like ln(r_s / r)"),
 ("a surface near 160\\,kpc", KQ1, "sits at r_s ~ 160 kpc"),
 ("inner bin over by 1.1\\,dex", KQ1, "the inner bin is over-filled by\n  1.1 dex"),
 ("needs a 360--400\\,kpc core", KQ1, "the core is 360-400 kpc"),
 ("rms anywhere is 0.226 / 0.222", KQ1, "The best per-bin rms anywhere is 0.226 / 0.222"),
 ("($\\mu_K$ 19.05) is $4.67\\times10^5$ below the BBN bound", KQ1, "closest is 4.67e5 times below"),
 ("galaxy capture stays at 4.111 / 4.112", KQ1, "| 4.1786 / 4.1110 | 3.7833 / 4.1121 |"),
 ("(rms 0.091)", KQ1, "rms 0.0908"),
 ("no term on the table reproduces", DED, "is a target no term on the\ntable reproduces"),
]
AK1 = "closure_2026_11_07/AK1_fold_release_layer/README.md"
L += [
 ("= 577.6 / 571.3\\,km/s)", AK1, "v_k = 2c(a0 L*/c^2)^(1/3) = 577.6 / 571.3 km/s"),
 ("NO VERDICT (check failed)", AK1, "NO VERDICT (check failed).**"),
 ("reads 317.7 / 309.2\\,km/s", AK1, "V reads 317.7 / 309.2 km/s"),
 ("$v_{\\rm post}$ 0.024--0.157\\,km/s", AK1, "| 0.024-0.157 | 121-139 |"),
 ("$R_\\delta$ $5\\times10^{-10}$--$3\\times10^{-7}$", AK1, "| 5e-10 - 2e-8 |"),
 ("all 160 readings outside the bands", AK1, "160 converged readings fall outside the frozen bands"),
 ("($d\\ln V/d\\ln v_f$ 1.000 / 0.95)", AK1, "d ln V / d ln v_f = 1.000 (clock-only) and 0.95 (phantom)"),
 ("(ratio 1.000, where the identity predicts 1.260)", AK1, "(ratio 1.000; the identity predicts 1.260)"),
 ("(22.53 / 24.04\\,kpc, not 2.09 / 2.25)", AK1, "The formula gives 22.53 / 24.04 kpc, not the brief's 2.09 / 2.25 kpc"),
 ("($1-X/X_{\\rm bg}\\le2.4\\times10^{-7}$)", AK1, "Max (1 - X/X_bg) = 2.4e-7"),
]
OKD = "closure_2026_11_07/OWNER_DECISION_2026-11-07_ACCEPT_CORRECTED_KERNEL_LABELS.md"
L += [
 ("deposited as DOI 10.5281/zenodo.24047420", Z70, '"doi": "10.5281/zenodo.24047420"'),
 ("The owner accepted the corrected values as the standing labels on 2026-11-07", OKD, "Accept, ship v1.3"),
 ("the frozen RESULT files are not edited", OKD, "The original frozen RESULT files are not edited"),
 ("none of them opens a door", OKD, "None of the accepted moves opens a door"),
 ("no row in the record is pending", OKD, "no row in the record is marked pending"),
 ("with the kernel corrected 0.00798 / 0.00720", GL3, "0.00798 / 0.00720; DEAD"),
 ("(1.0\\,Mpc with the kernel corrected", GL3, "| 0.3 / 0.3 Mpc | 1.0 / 1.0 Mpc |"),
 ("19.1 / 18.8 with the kernel corrected", GL3, "75.39 / 78.77 | 19.12 / 18.75"),
 ("$\\mu\\ge0.63$ / 1.0 with the kernel corrected", GL3, "0.63 / 1.0 (gap x10 / x16)"),
 ("$\\times$10 / $\\times$16 with the kernel corrected", GL3, "(gap x10 / x16)"),
 ("(27--39 with the kernel corrected)", GL3, "| 72.2-89.4 | 27.4-38.7 |"),
 ("that gate reads NO VERDICT", GL1, "**GL gate MOVES** to NO VERDICT"),
]
CMB1 = "closure_2026_11_07/CMB1_cmb_requirement_anatomy/RESULT.md"; CMB2 = "closure_2026_11_07/CMB2_prerecombination_dof/RESULT.md"
F1A2 = "closure_2026_11_07/F1A_primary_cmb_audit/AMENDMENT_A2.md"
VR1 = "closure_2026_11_08/VR1_vacuum_response_identity/RESULT.md"; SA1 = "closure_2026_11_08/SA1_settling_age_cold_component/REDUCTION.md"
L += [
 ("deposited as DOI 10.5281/zenodo.24047508", Z70, '"doi": "10.5281/zenodo.24047508"'),
 ("deposited as DOI 10.5281/zenodo.24047634", Z70, '"doi": "10.5281/zenodo.24047634"'),
 ("moves H1/H2 by +343\\,$\\sigma$ and H3/H2 by +197\\,$\\sigma$", CMB1, "moves the odd/even ratio H1/H2 by +343 sigma and the third-to-second ratio H3/H2 by +197 sigma"),
 ("ratio 0.57 inside [0.5, 2]", CMB1, "ratio 0.57, so M1 fails"),
 ("Block C CLUSTERING PINNED, both footings", CMB1, "| Block C label | **CLUSTERING PINNED** | **CLUSTERING PINNED** |"),
 ("no piece carries more than 19\\,\\%", CMB1, "No single piece carries more than 19 %"),
 ("$\\omega_X$ 0.108", CMB1, "| E best fit omega_X / omega_b | 0.108 / 0.0215 (R 5.0) | 0.108 / 0.0230 (R 4.7) |"),
 ("recovers 79\\,\\%", CMB1, "| Share of DeltaMB recovered by E, f_E | **0.79** | **0.79** |"),
 ("$\\Delta_E$ +35,812 / +35,378", CMB1, "| **+35,812** | **+35,378** |"),
 ("H3/H2 misses by $-36.8\\,\\sigma$", CMB1, "| H3 / H2, the third peak | 0.976 (0.009) | +0.9 | +66.4 / +61.6 | **-36.8 / -36.7** |"),
 ("H1/H2 and the first peak by $-16\\,\\sigma$", CMB1, "| first peak L1 | 223.1 (2.2) | -1.1 | +84.3 / +65.1 | -15.9 / -15.7 |"),
 ("the cold fit meets every feature within 1.1\\,$\\sigma$", CMB1, "The cold fit meets every feature within 1.1 sigma"),
 ("still share 0.043 / 0.024", CMB2, "0.043 / 0.024 still"),
 ("the clock about $10^{-20}$", CMB2, "Clock about 1e-20"),
 ("(Hessian rank 0)", CMB2, "the Hessian in the P velocities has rank 0"),
 ("$c_s^2=1/(3(1+R))$ exactly", CMB2, "c_s^2 = 1/(3(1+R)) exactly"),
 ("at most $7\\times10^{-4}$ and follows the source", CMB2, "| at most 7e-4 (\"follows\") |"),
 ("($r$ 0.992--0.997)", CMB2, "r 0.992-0.997"),
 ("still share at most 0.28 / 0.30", CMB2, "k 0.03 at most 0.28 / 0.30"),
 ("H3/H2 1.30 / 1.36 at 100 times, against the dust's 1.447", CMB2, "| law, x 100 | 1.71 [1.99] | 1.30 [1.36] |"),
 ("against the dust's 1.447", CMB2, "| dust R 5.41 | 1.220 | 1.447 |"),
 ("$\\rho_{\\rm DE}$ about 900--$10^4$ times today's", CMB2, "x = 30 needs about 900 times"),
 ("(H3/H2 1.008 vs 1.006)", CMB2, "(H3/H2 1.008 vs 1.006)"),
 ("converges ($-26.65$ / $-94.13$ at $k$ 0.05 / 0.3)", F1A2, "| dust contrast | -8.79 | -26.65 | -48.60 | -76.26 | -94.13 |"),
 ("$Q_{X1}\\le3.7\\times10^{-12}$", F1A2, "Q_X1 <= 3.7e-12"),
 ("G4 REPRODUCED, F1 CONFIRMED unchanged", F1A2, "G4 stays REPRODUCED, and F1 stays CONFIRMED"),
 ("($\\nabla\\ln X=-2A/c^2$)", VR1, "grad ln X = -2 A / c^2"),
 ("gives $\\kappa^2=1/(4q)$", VR1, "kappa^2 = 1/(4q)"),
 ("1.447, 1.772, 0.921, 0.282, 2.507, 0.230", VR1, "1.447 (c/H), 1.772 (Poisson), 0.921 (c t_ff), 0.282 (Jeans, in window), 2.507 (1/sqrt Lambda), 0.230"),
 ("equipartition gives 4.525 / 6.399", VR1, "kappa = 4.525 / 6.399"),
 ("at most $6.9\\times10^{-8}$ of the cluster need", VR1, "That is 6.9e-8 of the X-COP cluster need"),
 ("Lean: 7 theorems, MUTATE twin fails 4/4", VR1, "_MUTATE twin fails 4/4"),
 ("nothing in reach supplies a $\\pi$-free length", VR1, "nothing in reach supplies a pi-free length"),
 ("NO TERM IN ACTION: $\\mathcal K$ depends on $Q$ alone", SA1, "K depends on Q alone"),
 ("carry the largest need in the record", SA1, "they carry the largest need in the record"),
]
REG = "closure_2026_11_07/CLOSURE_REGISTER.json"; CMB3C = "closure_2026_11_07/CMB3_cmb_assumption_audit/FROZEN_CRITERIA.md"
CMB3 = "closure_2026_11_07/CMB3_cmb_assumption_audit/RESULT.md"
L += [
 ("deposited as DOI 10.5281/zenodo.24053083", Z70, '"doi": "10.5281/zenodo.24053083"'),
 ("A1: the frozen line reads BREAKS POSSIBLE", CMB3, "| frozen line | **BREAKS POSSIBLE** | **BREAKS POSSIBLE** |"),
 ("A2 lensing HOLDS (unlensed theory: survival 0.993", CMB3, "+171,685.7, 0.993, 5.511 (+1.9 %)"),
 ("0.877 / 0.862", CMB3, "+151,571.2, 0.877, 5.410 (0.0 %) | +143,585.7, 0.862, 5.412 (0.0 %)"),
 ("$A_\\phi$ 1.00 and baryons alone 9.50 / 9.45", CMB3, "| A_phi at best fit, cold / MB | 1.00 / 9.50 | 1.00 / 9.45 |"),
 ("A3, $N_{\\rm eff}$ and YHe free, HOLDS (0.892 / 0.871)", CMB3, "+154,315.4, 0.892, 5.290 (-2.2 %) | +145,139.3, 0.871, 5.295 (-2.2 %)"),
 ("A4, $n_s$ and running free, HOLDS (0.901 / 0.895)", CMB3, "+155,732.5, 0.901, 5.429 (+0.4 %) | +149,207.6, 0.895, 5.428 (+0.3 %)"),
 ("BREAKS / BREAKS on the record's own data", CMB3, "**BREAKS / BREAKS, by the record's own data"),
 ("bound hosts hold 0.9\\,\\% / 0.8\\,\\%", CMB3, "hold 0.9 % / 0.8 % of the component"),
 ("HOLDS (0.751 / 0.736) but is nuisance-sensitive ($-25$ / $-26$\\,\\%", CMB3, "| nuisance sensitivity | -25 % | -26 % |"),
 ("(0.751 / 0.736)", CMB3, "+129,844.7, 0.751 | +122,711.1, 0.736"),
 ("under any single relaxation is +122,711", CMB3, "The smallest DeltaMB under any single relaxation is +122,711"),
 ("$\\nu-1$ 0.05--0.17", CMB3, "is 0.05 at its total gradient and 0.08-0.17 per band"),
 ("move the amount $R$ by at most 2.2\\,\\%", CMB3, "0.892, 5.290 (-2.2 %)"),
]
X35 = "rebuild_2026_10_22/X35_a0_tracks_ede/README.md"
L += [
 ("UNDECIDED by its frozen rule", X35, "## Verdict (frozen rule 5): **UNDECIDED**"),
 ("1,147--7,565 times today's", X35, "puts a₀(1100) at 1,147–7,565 × today"),
 ("(D1 NULL;", X35, "**The covariant theory gives nothing (D1, NULL).**"),
 ("max$|\\Xi|$ $4.9\\times10^{-29}$", X35, "returns max|Ξ| = 4.9e-29"),
 ("($k_{\\rm J}$ 0.024--0.039\\,Mpc$^{-1}$)", X35, "k < k_J,eff = 0.024–0.039 Mpc⁻¹"),
 ("from 1.00 to 1.49 (a flat-$\\Lambda$ estimate)", X35, "moves the native sqrtX from 1.00 to **1.49 at z 2.33**"),
]
HY1 = "closure_2026_11_08/HY1_hybrid_law_plus_component/RESULT.md"; HYD = "closure_2026_11_08/OWNER_DECISION_2026-11-08_HY1_RULE_LIFT.md"
L += [
 ("the owner lifted the no-cold-component rule for HY1 only", HYD, "Lane HY1 only. Every other lane keeps the standing rules"),
 ("NO VERDICT / NO VERDICT on the frozen M3 rule", HY1, "| **Lane (frozen rule)** | **NO VERDICT** | **NO VERDICT** |"),
 ("so the control cannot bite", HY1, "It **DOES NOT BITE** on either footing"),
 ("Under it, FAIL on both footings", HY1, "both **empty**: **FAIL**"),
 ("about 4.1 times the baryons", HY1, "f_cap R = 4.1113 / 4.1133"),
 ("SPARC rms 0.465--0.658 / 0.464--0.680 against 0.110", HY1, "rms 0.465-0.658, U pinned at the 0.30 floor"),
 ("0.464--0.680 against", HY1, "rms 0.464-0.680, U 0.30"),
 ("over-filled by about 1.1\\,dex", HY1, "The cusp over-fills the core by 1.1 dex"),
 ("($\\kappa$ in [0.05, 0.17] / [0.05, 0.13])", HY1, "| Shared window of the columns with power | [0.05, 0.17] | [0.05, 0.13] |"),
 ("discs shed at least 96\\,\\% of the dust", HY1, "Discs would have to shed at least 96 % of it"),
 ("covered HY1 only", HYD, "the no-cold-component rule is lifted for test lane HY1 only"),
]
KR1 = "closure_2026_11_08/KR1_running_k_mass/RESULT.md"
L += [
 ("deposited as DOI 10.5281/zenodo.24053740", Z70, '"doi": "10.5281/zenodo.24053740"'),
 ("$M(z\\,3)=630.957$", KR1, "lambda** is fixed by M(z = 3) = 630.957 Mpc^-1"),
 ("& FAIL / FAIL. The mass runs the right way", KR1, "**Label, canonical: FAIL. Label, alt: FAIL.**"),
 ("read $\\mu_K(0)$ 1.232--79.65", KR1, "| (iii) mu_K(0) <= 79.43 | PASS | PASS | PASS | **FAIL** | 1.232 / 1.265 / 10.45 / 79.65 |"),
 ("$6.01\\times10^{13}$ at $z$ 1100", KR1, "| **1.232** | 631 | 5.98e4 | 1.29e9 | 6.01e13 |"),
 ("the background density of $z$ 4.31", KR1, "That is the background\ndensity of z = 4.31"),
 ("a Jeans length of 2.8--2.9\\,kpc against the 234\\,kpc", KR1, "Jeans length 2.8-2.9 kpc"),
 ("SPARC rms 0.777 / 0.789 against 0.146 / 0.143", KR1, "| G1 SPARC | Z -0.70, rms 0.777 (line 0.146) | Z -0.71, rms 0.789 (line 0.143) |"),
 ("for any convex $\\mathcal K$ the kernel mass is a function of the sector's own local density", KR1, "is a function of the sector's own local density, everywhere"),
 ("not only its amplitude", KR1, "It holds for every K(Q), not only DBI."),
]
KR2 = "closure_2026_11_08/KR2_today_window/RESULT.md"
L += [
 ("FAIL / FAIL (canonical empty at X-COP; alt empty at SPARC", KR2, "| **Frozen label** | **FAIL (empty at C2)** | **FAIL (empty at C1)** |"),
 ("by the frozen $T=0$ clause", KR2, "C1 is empty only through the frozen T = 0 clause"),
 ("No $\\mu_K(0)$ in 0.1--79.43", KR2, "at any mu_K(0) in 0.1-79.43 Mpc^-1"),
 ("over-filled by 0.89--1.23\\,dex", KR2, "The inner bin over-fills by -0.89 to -1.23 dex"),
 ("best per-bin rms 0.439 / 0.425 against 0.10", KR2, "The best per-bin rms is 0.439 / 0.425 at mu_K 2.5 / 1.6"),
 ("0.225 / 0.231 at the captured amount, KQ1's 0.226 again", KR2, "f_cap R amount 0.225 / 0.231. That is KQ1's 0.226 again"),
 ("Groups need $\\mu_K$ in [1.585, 3.98]", KR2, "| C3 groups (UA1 95 % interval, both f*) | [1.585, 3.98] (edges 1.53, 4.76) |"),
 ("needs at most 0.631: disjoint", KR2, "| C6 hosts inside R500 (NC4) | [0.1, 0.631] (edge 0.84) |"),
 ("SPARC is clean to 6.31 and KiDS to 3.98", KR2, "| C5 KiDS G6 with kSZ gas (KX1, two-sided) | [0.1, 3.98] (edge 5.73) |"),
 ("($\\Delta\\chi^2$ 309--1315, GL1's wall)", KR2, "**empty** (Delta chi^2 309-1315)"),
 ("(SPARC and groups carry $M\\ge2173$)", KR2, "C1's window tops out at 6.31; local M >= 2173."),
]
L += [
 ("(iii) fails for every member", KR1, "so (iii) is FAIL for every member on both"),
 ("the brief's kill fires on both footings", KR1, "it now **FIRES** on both footings"),
 ("the label is unchanged", KR1, "**Label.** Unchanged: FAIL / FAIL."),
]
BG1 = "closure_2026_11_08/BG1_cold_gas_conversion/RESULT.md"; BGD = "closure_2026_11_08/OWNER_DECISION_2026-11-08_BG1_LAUNCH.md"
L += [
 ("deposited as DOI 10.5281/zenodo.24056963", Z70, '"doi": "10.5281/zenodo.24056963"'),
 ("``Launch it anyway''", BGD, 'Owner\'s words: "Launch it anyway"'),
 ("& FAIL / FAIL: no $\\alpha$ in the scan passes G1--G10", BG1, "No alpha in [1e-3, 1e3] passes G1-G10 on either footing"),
 ("SPARC rms 0.0626 (line 0.0660)", BG1, "rms 0.0626 (line 0.0660)"),
 ("(shift $-0.003$\\,dex)", BG1, "-0.003 dex"),
 ("discs retain 0.4\\,\\% of the dust while quenched hosts keep 17--36\\,\\%", BG1, "(retained 0.4 %) while quenched hosts keep 17-36 % of theirs"),
 ("converts 97\\,\\% of the component by $z$ 20", BG1, "the converted fraction by z 20 is 97 %"),
 ("(7\\,$M_\\odot$\\,pc$^{-3}$ at $z$ 1000; its exposure is 1/7 of a disc's)", BG1, "is 1/7 of a SPARC disc's"),
 ("holds only for $\\alpha\\le2.5$", BG1, "G9 needs alpha <= 2.5"),
 ("only for $\\alpha\\le6.3$", BG1, "G8 and G10 need alpha <= 6.3"),
 ("discs need $\\alpha\\ge1000$ (beyond the scan on alt)", BG1, "(alpha >= 1000 canonical, beyond the scan on alt)"),
 ("disjoint by a factor 400", BG1, "Ratio 400 on canonical"),
 ("an exposure $\\times10$ replay moves both alike", BG1, "the x10 replay moves both alike"),
 ("Coma UDGs under-filled by 0.65--0.92\\,dex", BG1, "under-filled by 0.65-0.92 dex"),
 ("gives $b=6.4$ where they need about 80", BG1, "b = 6.4 where the UDGs need about"),
 ("groups at most 7/20", BG1, "(G4, at most 7/20 and 6/20)"),
 ("X-COP over-filled by 0.06--0.10\\,dex at the CMB amount $R=5.41$", BG1, "over-filled by 0.06-0.10 dex at the\n   CMB amount R = 5.41"),
 ("captured share $R=4.11$", BG1, "f_cap R = 4.11, reported"),
 ("clusters keep at least 94\\,\\%", BG1, "Clusters keep >= 94 % of their dust"),
 ("M3 ($10\\times$ the best $\\alpha$) does not bite as frozen", BG1, "**NO BITE**"),
 ("the label does not rest on it", BG1, "The label does not rest on M3"),
]
HX1 = "rebuild_2026_10_22/HX1_hot_ladder/README.md"; HG2 = "rebuild_2026_10_22/HG2_kids_lowg_hot_gas/README.md"
GA1 = "rebuild_2026_10_22/GA1_group_gas_audit/README.md"; GA1O = "rebuild_2026_10_22/GA1_group_gas_audit/ga1_group_gas_audit.out"
L += [
 ("deposited as DOI 10.5281/zenodo.24058756", Z70, '"doi": "10.5281/zenodo.24058756"'),
 ("Coma UDGs (NOT A TEST, UA1)", UA1, "NOT A TEST"),
 ("sub-linear response at the UDGs' internal acceleration on top of a base that already carries Coma's external field (GB1, Disclosed 3)", GB1, "UDG predictions apply the isolated algebraic Delta at the internal x, on top of a base that already includes"),
 ("$+1.121$ / $+1.078$\\,dex", GB1, "FAIL +1.121 (+4.28) / FAIL +1.078 (+4.11)"),
 ("the Lovisari+2015 X-ray masses", UA1, "Lovisari+2015 masses are X-ray hydrostatic"),
 ("median 1.18, $\\log B=+0.07\\pm0.08$ (alt 1.08, $+0.03\\pm0.08$)", HX1, "| Tian groups (144) | 1.18, +0.07 +- 0.08 | 1.08, +0.03 +- 0.08 |"),
 ("$D=-0.294$ [$-0.511$, $-0.076$]\\,dex, UNDERPOWERED", HG2, "| D (primary) | **−0.294 dex, 95% [−0.511, −0.076]**"),
 ("(power 0.45)", HG2, "RESULT: UNDERPOWERED by the frozen rule (power 0.45 < 0.50)"),
 ("$-0.362$ [$-0.605$, $-0.139$] (power 0.36)", GA1O, "measured D -0.3623  95% [-0.6047, -0.1394]  power 0.364"),
 ("all groups on the law would give $+0.173$", GA1, "| **−0.362 [−0.605, −0.139]** | **+0.306 / +0.282** | +0.173 |"),
 ("GA1 re-grades HG2's sample", GA1, "Step 0's random-number order to HG2's"),
 ("KX1's frozen label is NO VERDICT", KX1, "## Label (frozen rule): NO VERDICT on both footings."),
 ("(log $M_\\star$ 9.4, 122--285\\,kpc)", KX1, "| 1 (9.4, 122-285) |"),
 ("frozen extrapolation of the log $M_\\star$ 10.0 kSZ gas row", KX1, "**Bin 1 (log M* 9.4) uses CW6's log M* 10.0 gas row**, a frozen extrapolation."),
 ("without that bin canonical C4 would read SOFTENS", KX1, "C4 canonical would read SOFTENS"),
 ("(Rf $=1.000$ at every $z<1$ bin)", CE2, "Rf = 1.000 at every z < 1 bin"),
]
FS1R = "closure_2026_11_06/FS1_fold_shock_capturing/README.md"; FS2R = "closure_2026_11_06/FS2_fold_viscosity_free/README.md"
AC10R = "action_search_2026_11_05/AC10_nonlinear_clock/README.md"; SV3R = "action_search_2026_11_05/SV3_fold_implicit/README.md"
AS3R = "rebuild_2026_10_22/AS3_ppn_and_khronon_scalar/README.md"; AC11R = "action_search_2026_11_05/AC11_moving_sun/README.md"
MS3R = "closure_2026_11_06/MS3_moving_sun_light/README.md"; X35R = "rebuild_2026_10_22/X35_a0_tracks_ede/README.md"
CT3R = "complete_theory_2026_11_04/CT3_cosmology/CT3_REPORT.md"; C689 = "campaign_fresh_gravity/CFG689_native_ruler_bao/README.md"
CT1R = "complete_theory_2026_11_04/CT1_action/CT1_REPORT.md"; CK3R = "closure_2026_11_07/CK3_groups_kicked_carrier/RESULT.md"
V3XR = "rebuild_2026_10_22/V3X_v3s_close_undecided/README.md"; AZ31 = "astra_goal_2026_11_05/AZ31_w2_graded_radius/README.md"
AZ32 = "astra_goal_2026_11_05/AZ32_solar_spectrum/README.md"
L += [
 ("5.3\\,\\% at $J_{\\rm thr}$ (FS1)", FS2R, "at J_thr, FS1 saw 5.3 %"),
 ("1.2\\,\\% at $J_{\\rm reg}$ (FS2)", FS2R, "That shock reaches J_reg 1.2 % before v3s's dust collapse"),
 ("FS1 and FS2 read the clock-only AC2q folds EARLIER", FS1R, "**DIFF-TIME, EARLIER**"),
 ("at the same time to 0.3\\,\\% (1.0752--1.0782 against 1.0718--1.0773\\,$\\tau_f$)", AC10R, "AC2q's fold time is 1.0752-1.0782 tau_f against v3s's 1.0718-1.0773"),
 ("delays clock-only folds by about 0.1--0.3\\,\\%", SV3R, "AC2q's extra s^2 pressure only delays clock-only folds by about 0.1-0.3 %"),
 ("AS3 finds $\\alpha_1=\\alpha_2=0$ exactly for a source moving through the aether", AS3R, "For a source moving through the aether, the exact solution of v9's linear system is linear GR with G = G~: alpha_1 = alpha_2 = 0"),
 ("AC11 lists the metric response that would give $\\alpha_1$ and $\\alpha_2$ as still open", AC11R, "the metric response that would give alpha_1 and alpha_2"),
 ("no PPN $\\alpha_1$ or $\\alpha_2$ is claimed", MS3R, "No PPN alpha_1 or alpha_2 is claimed."),
 ("CFG689's native band is 0.91 [0.33, 1.21]", C689, "| 2.33 | 0.91 [0.33, 1.21] |"),
 ("moves the native $\\sqrt X$ from 1.00 to 1.49", X35R, "moves the native sqrtX from 1.00 to **1.49 at z 2.33**"),
 ("$a_0(2.33)/a_0(0)\\approx0.85$", CT3R, "a₀(2.33)/a₀(0) ≈ 0.85"),
 ("0.084\\,dex at $z^*$ 2.33 for $3\\sigma$ (CFG689)", C689, "3σ needs a0 to 0.055 / 0.072 / 0.074 / 0.084 dex at z 1.0 / 1.2 / 1.5 / 2.33"),
 ("set at 0.10\\,dex by CT1", CT1R, "a0(z) at z ≈ 2.5 to 0.10 dex"),
 ("L388's masses are in $M_\\odot/h$", CK3R, "L388's masses are in Msun/h"),
 ("FAIL as frozen, NOT ROBUST", CK3R, "FAIL as frozen (slope), both footings, every kick; NOT ROBUST"),
 ("($M\\times0.6736$) reads PASS in every cell", CK3R, "**every cell reads PASS, both footings**"),
 ("from prediction error, not agreement", CK3R, "That PASS comes from **prediction error, not agreement**"),
 ("CK3 reports the record-level fix and does not make it", CK3R, "Correcting it is a record-level fix that this lane reports and does not"),
 ("V3X is UNDECIDED under its frozen rule on W2 and W4c, with a physics reading of PASS", V3XR, "Under the frozen rule the label is UNDECIDED. The physics reading is a PASS."),
 ("AZ31 passes W2 at the graded radius as a new test", AZ31, "This is a new radius-specific test, not an amendment of V3X."),
 ("AZ32 keeps the full W4c UNDECIDED", AZ32, "# UNDECIDED full W4c"),
]
def mutate(lit):
    m = re.search(r"\d", lit)
    return lit if not m else lit[:m.start()] + str((int(m.group()) + 1) % 10) + lit[m.end():]
ok = 0; bad = []
for frag, path, lit in L:
    in_tex = ws(frag) in ws(TEX)
    l2 = mutate(lit) if MUT else lit
    in_src = ws(l2) in src(path)
    if MUT:
        if not re.search(r"\d", lit) or not in_src: ok += 1
        else: bad.append(("mutant survived", frag, path))
    elif in_tex and in_src: ok += 1
    else: bad.append(("tex" if not in_tex else "src", frag, path))
body = TEX.split("\\begin{document}")[1]
rules = [
 ("kappa stated as fitted", "$\\kappa=\\tfrac12$ is fitted" in TEX),
 ("not closed stated", "The theory is not closed" in TEX),
 ("no favouring claim", "Nothing here says the data favour this framework" in TEX),
 ("no local paths", "/Users/" not in TEX),
 ("no 'cold dark matter'", "cold dark matter" not in TEX.lower()),
 ("no pending placeholder", "\\pend{" not in body),
 ("no LCDM input claimed", "No $\\Lambda$CDM inputs were used" in TEX),
 ("version v1.9 stated, no draft marker", "v1.9, 2026-11-08" in TEX and "draft v0" not in TEX),
 ("owner decision carried, nothing pending", "re-stated (owner 2026-11-07)" in TEX and "pending owner" not in TEX and "the frozen RESULT files are not edited" in TEX),
 ("unification quote verbatim", UQ_OK),
 ("seed abstract verbatim", "The next lane must find one covariant quantity that sets that amplitude (not just a switch) in today's hot systems and is non-zero in the early universe, or show the two failures need separate causes." in ws(TEX)),
 ("UDG linear-response f derived", abs(10**1.121-1-12.2)<0.05 and abs(10**1.078-1-11.0)<0.05 and "$f=10^{1.121}-1=12.2$ / $10^{1.078}-1=11.0$" in TEX),
 ("erratum stated", "erratum on PAPER68's printed form only; no number changes" in TEX),
]
if not MUT:
    for name, good in rules:
        if good: ok += 1
        else: bad.append(("rule", name, ""))
for b in bad: print("FAIL", *b)
total = len(L) + (0 if MUT else len(rules))
print(f"{ok} of {total} checks pass" + (" (mutate: each mutated literal must fail)" if MUT else ""))
print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
sys.exit(0 if not bad else 1)
