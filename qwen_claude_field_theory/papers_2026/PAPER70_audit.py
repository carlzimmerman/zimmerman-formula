#!/usr/bin/env python3
"""PAPER70 audit (v1.0): each quoted number appears in the TeX and, as the literal given, in the committed file named
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
 ("$\\sim1.7$ / $1.3$", NOGO, "~1.7 / 1.3"), ("Coma UDGs & $\\sim80$", NOGO, "| Coma UDGs | ~80 |"),
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
 ("($F_{\\rm web,max}$ 0.00481 / 0.00435)", OQ2, "F_web,max = 0.00481"), ("0.00481 / 0.00435", OQ2, "F_web,max = 0.00435"),
 ("SEPARATED NO, as frozen", OQ2, "**NO** (as frozen"),
 ("S1 reading is DEAD on both footings, every start", OQ2, "DEAD, every start, both f*"),
 ("DIFFERS, both footings", FS2, "DIFFERS (frozen)"), ("fold 1.2\\,\\% earlier", FS2, "reaches J_reg 1.2 % before"),
 ("(DIFF-TIME EARLIER, edge-carried)", FS2, "**DIFF-TIME EARLIER**"), ("read SAME-REACH", FS2, "SAME-REACH (r 0.99990-1.00004)"),
 ("no row is REGULAR", FS2, "No row is REGULAR"),
 ("becomes the FINAL moving-Sun label", C7, "MS3 running (~11 h from 08:00), its reading is the FINAL label"),
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
 ("it adopts nothing, owner decision pending", PX1, "It adopts nothing"),
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
 ("(r 75.4 / 78.8)", FA3, "W1 web (r 75.4 / 78.8 at tau_gal)"),
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
 ("version v1.0 stated, no draft marker", "v1.0, 2026-11-07" in TEX and "draft v0" not in TEX),
 ("seed abstract verbatim", "The next lane must find one covariant quantity that sets that amplitude (not just a switch) in today's hot systems and is non-zero in the early universe, or show the two failures need separate causes." in ws(TEX)),
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
