#!/usr/bin/env python3
"""PAPER69 audit: each quoted number appears in the TeX and, as the literal given, in the committed file named beside it;
naming rules; no local paths; no pending placeholder. Run: python3 PAPER69_audit.py (exit 0 only if all pass).
--mutate changes one digit of each source literal; exit 0 only if every mutated literal then fails.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, re, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEX = open(os.path.join(HERE, "PAPER69_closure_by_verdict_2026.tex"), encoding="utf-8").read()
C = "closure_2026_11_06/"; A = "action_search_2026_11_05/"
QX8 = C + "QX8_sparc_exact_field/README.md"; QX2 = C + "QX2_clusters/README.md"
QX15 = C + "QX15_cmb_primary_likelihood/README.md"; QX18 = C + "QX18_elliptical_gate/README.md"
QX11 = C + "QX11_fg1_tilt_exact/README.md"; QX20 = C + "QX20_failure_ladder/README.md"
QX21 = C + "QX21_step_origin/README.md"; QX25 = C + "QX25_morphology_key/README.md"
QX26 = C + "QX26_imf_variation/README.md"; QX1 = C + "QX1_equation_chain/README.md"
QX17B = C + "QX17B_adm_lean_solutions/RESULT.md"; CH = C + "FRW_RECONCILIATION_CHAIN/CHAIN.md"
AC24 = A + "AC24_moving_sun_powered/README.md"; AC18 = A + "AC18_constraint_causality/README.md"
AC23 = A + "AC23_fresh_slow_roots/README.md"; EB1b = "early_bh_2026_11_06/EB1b_web_efe/README.md"
IDEA = C + "IDEA_EARLY_BH_DARK_BARYONS_CHECK.md"; AC14C = A + "AC14_fold_final/FROZEN_CRITERIA.md"
P68 = "qwen_claude_field_theory/papers_2026/PAPER68_screened_khronon_action_2026.zenodo.json"
VH = "rebuild_2026_10_22/VH1_v3s_health_gates/README.md"
Q27 = C + "QX27_tail_retention_sector/README.md"; Q28 = C + "QX28_superfluid_two_phase/README.md"
Q29 = C + "QX29_dipolar_medium/README.md"; Q30 = C + "QX30_cluster_data_assumptions/README.md"
Q31 = C + "QX31_growth_cmb_data_assumptions/README.md"
# (fragment in the TeX, source file, literal in that file)
L = [
 ("rms 0.0560", QX8, "0.0560"), ("0.0558 at 0.52", QX8, "0.0558"),
 ("$+0.468/+0.435$", QX2, "+0.468"), ("$+0.468/+0.435$", QX2, "+0.435"),
 ("3741.08/3741.15", QX15, "3741.08"), ("3741.08/3741.15", QX15, "3741.15"),
 ("$\\Delta=-64.7$", QX15, "-64.7"), ("$+172{,}848$/$+166{,}612$", QX15, "172,848"),
 ("$+172{,}848$/$+166{,}612$", QX15, "166,612"), ("$h$ 0.674", QX15, "0.674"),
 ("$D=+0.210/+0.189$", QX18, "+0.210"), ("$D=+0.210/+0.189$", QX18, "+0.189"),
 ("FAIL canonical $+0.170$, PASS alt $+0.090$", QX11, "+0.170"), ("PASS alt $+0.090$", QX11, "+0.090"),
 ("$+0.32$--$0.37$\\,dex", QX20, "+0.32 to +0.37"),
 ("$+0.158\\pm0.064$ (2.46$\\sigma$)", QX21, "+0.158 +- 0.064"), ("(2.46$\\sigma$)", QX21, "2.46"),
 ("($+0.078\\pm0.045$)", QX25, "+0.078 +- 0.045"),
 ("$+0.210\\to+0.093$", QX26, "+0.093 / +0.074"), ("56--61\\,\\%", QX26, "56-61%"),
 ("$+0.080$ to $+0.122$", QX26, "+0.080 to +0.122"), ("(4\\,\\% removed)", QX26, "X-COP | +0.467 / +0.435 | +0.448 / +0.415 | 0.04"),
 ("QX1 carries 28 Lean theorems", QX1, "28 theorems, 0 errors, 0 sorry"),
 ("Lean \\texttt{FRW\\_correction} has 11 theorems", CH, "11 theorems, standard axioms, 0 errors"),
 ("max $R$ 2.700110 against 2.700138", CH, "| max R_main at N_obs | 2.700138 | 2.700110 |"),
 ("1.000 to 2.5257 against the stored 1.000 to 2.5253", CH, "1.000 to 2.5257, against the stored 1.000 to 2.5253"),
 ("(12 theorems;", QX17B, "has 12 theorems, standard axioms only"),
 ("(0.496/0.572 against 0.30)", AC24, "0.496"), ("(0.496/0.572 against 0.30)", AC24, "0.572"),
 ("Mars 0.20 of its line, Cassini 0.028", AC24, "| 0.033 | 0.20 | 0.073 | 0.0092 | 0.044 | 0.049 | 0.028 |"),
 ("all 36 graded observer rows nonzero", AC18, "All 36 graded observer rows (6 directions) are nonzero on both footings"),
 ("from $3.6\\times10^{-67}$ (canonical)", AC18, "| canonical | 1 s, 1e9 m | 0.30 | 3.6e-67 to 9.7e-67"),
 ("to $7.8\\times10^{-66}$\\,m/s (alt)", AC18, "| alt | 1 s, 1e9 m | 0.30 | 9.2e-67 to 7.8e-66"),
 ("$R\\le2.70$", AC23, "2.70"),
 ("before $z$ 0.48 (canonical, weakest p05 field)", EB1b, "| p05 (weakest field) | canonical z 0.48"),
 ("at least 15$\\times$", IDEA, "at least 15"),
 ("NO VERDICT if any physical row is UNDECIDED", AC14C, "any physical row is NOT CONVERGED or UNDECIDED"),
 ("10.5281/zenodo.23968171", P68, "10.5281/zenodo.23968171"),
 ("PAPER68 (DOI 10.5281/zenodo.23990944", P68, "10.5281/zenodo.23990944"),
 ("X-COP $-0.024/0.085$ canonical", Q27, "canonical n 4: -0.024 / 0.085"),
 ("($\\Delta\\chi^2$ 231--1059 against 4)", Q27, "Delta chi^2 231-1059 against a line of 4"),
 ("$5.6\\times10^3$--$7.0\\times10^3$ times", Q27, "X-COP 5.6e3-7.0e3"),
 ("X-COP $+0.120$/rms 0.139", Q28, "+0.120 / 0.139"),
 ("($\\Delta\\chi^2$ 140/70 against 4)", Q28, "Delta chi^2 140 / 70 (line 4)"),
 ("(Q2 2.44--4.55$\\times$ the Hees line)", Q29, "Q2 2.44-4.55x / 2.85-5.15x"),
 ("leaves X-COP at $+0.389$", Q29, "+0.389/0.396"),
 ("moves X-COP by $-0.0205$\\,dex (to $+0.447/+0.414$)", Q30, "It moves X-COP by -0.0205 dex"),
 ("(to $+0.447/+0.414$)", Q30, "**+0.447 / +0.414**"),
 ("X-COP at $+0.329/+0.298$", Q30, "+0.329 / +0.298"),
 ("shape $\\chi^2$ at 370--399 against 20.09", Q31, "shape chi^2 at 370-399, against a line of 20.09"),
 ("0.4\\,\\% of the baryons-only", Q31, "all CamSpec nuisance freedom 732 (0.4 %)"),
 ("$a_0=9.3603\\times10^{-11}$", VH, "9.3603e-11"), ("$1.1312\\times10^{-10}$", VH, "1.1312e-10"),
]
ws = lambda t: re.sub(r"\s+", " ", t)
cache = {}
def src(p):
    if p not in cache:
        fp = os.path.join(ROOT, p)
        if os.path.exists(fp):
            cache[p] = ws(open(fp, encoding="utf-8").read())
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
    in_tex = frag in TEX
    l2 = mutate(lit) if MUT else lit
    in_src = ws(l2) in src(path)
    if MUT:
        if not re.search(r"\d", lit) or not in_src: ok += 1
        else: bad.append(("mutant survived", frag, path))
    elif in_tex and in_src: ok += 1
    else: bad.append(("tex" if not in_tex else "src", frag, path))
rules = [
 ("kappa stated as fitted", "$\\kappa=\\tfrac12$ is fitted" in TEX),
 ("not closed stated", "The theory is not closed" in TEX),
 ("no favouring claim", "Nothing here says the data favour this framework" in TEX),
 ("no local paths", "/Users/" not in TEX),
 ("no 'cold dark matter'", "cold dark matter" not in TEX.lower()),
 ("no pending placeholder", "\\pend{" not in TEX.split("\\begin{document}")[1]),
 ("no LCDM input claimed", "No $\\Lambda$CDM inputs were used" in TEX),
]
# AC14 counts read straight from the lane's part files (complete run, 485 rows; the lane commits them with its README)
import glob, json
_c = {}
for f in glob.glob(os.path.join(ROOT, A, "AC14_fold_final", "parts", "*.json")):
    d = json.load(open(f)); r = d.get("row", {})
    k = (r.get("model"), r.get("kind"), d.get("label")); _c[k] = _c.get(k, 0) + 1
und = sum(v for k, v in _c.items() if k[2] == "UNDECIDED"); tot = sum(_c.values())
rules.append(("AC14 296 UNDECIDED of 485 parts", und == 296 and tot == 485 and "296 of the 485 parts" in TEX))
rules.append(("AC14 56 of 80 AC2q soft undecided", _c.get(("AC2q", "soft", "UNDECIDED")) == 56 and _c.get(("AC2q", "soft", "FOLD")) == 24 and "56 of 80 AC2q soft" in TEX))
if not MUT:
    for name, good in rules:
        if good: ok += 1
        else: bad.append(("rule", name, ""))
for b in bad: print("FAIL", *b)
total = len(L) + (0 if MUT else len(rules))
print(f"{ok} of {total} checks pass" + (" (mutate: each mutated literal must fail)" if MUT else ""))
print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
sys.exit(0 if not bad else 1)
