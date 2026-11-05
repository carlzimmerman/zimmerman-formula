#!/usr/bin/env python3
"""PAPER68 audit: each quoted number appears in the TeX and in the committed file named beside it; naming rules; no local paths.
Run: python3 PAPER68_audit.py (exit 0 only if all pass). --mutate changes one digit of each source literal; exit 0 only if every mutated literal then fails.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, re, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEX = open(os.path.join(HERE, "PAPER68_screened_khronon_action_2026.tex"), encoding="utf-8").read()
Q = "rebuild_2026_10_22/"
V3 = "covariant_push_2026_10_22/V3_FULL_PICTURE.md"
AD = "finish_2026_11_04/FN1_action_call/OWNER_DECISION_2026-11-04_ADOPT_V3S_SCOPED.md"
SI = "action_scale_investigation_2026_11_05/joint_phase/SELECTION_IMPASSE.md"
PR = "astra_goal_2026_11_05/PROGRAM.md"
BR = "ASTRA_GOAL_2026-11-05_HANDOFF_LANES.md"
VH = Q + "VH1_v3s_health_gates/README.md"; X3 = Q + "X3_switched_stiffness/README.md"; AX = Q + "AX1_action_for_law/README.md"
# (fragment in the TeX, source file, literal in that file)
L = [
 ("4.8e7 (canonical), 5.7e7 (alt)", AD, "4.8e7 (canonical; 4.849e7 in c6p_cassini_hp.out), 5.7e7 (alt)"),
 ("$\\le0.17$ of bound", AD, "planets <= 0.17 of bound"),
 ("9.8e-14 ($\\gamma$) and 1.1e-12 ($\\beta$)", AD, "9.8e-14 (gamma) and 1.1e-12 (beta)"),
 ("1.13 $\\pm$ 0.21 / 1.04 $\\pm$ 0.19", AD, "1.13 +- 0.21 / 1.04 +- 0.19"),
 ("6e-32", AD, "6e-32"),
 ("$-0.7$\\,\\% against a 2\\,\\% line", AD, "-0.7 % against the 2 % line"),
 ("14.6\\,\\% against 5\\,\\%", AD, "14.6 % against 5 %"),
 ("1.1e-10 below $c$", AD, "1.1e-10 below c"),
 ("1.69--5.18 times", AX, "1.69–5.18×"),
 ("2.44--5.19 times", V3, "fails Cassini 2.44–5.19×"),
 ("rms 0.054\\,dex", V3, "rms 0.054 / 0.054 dex"),
 ("EFE solved for 109", V3, "EFE solved for 109"),
 ("63--64\\,\\% acceptable", V3, "63–64 % acceptable"),
 ("+0.032\\,dex from SPARC", V3, "+0.032 dex from SPARC"),
 ("3.2e-14", V3, "at most 3.2e-14 of the double pulsar"),
 ("2.9e-11", V3, "shifts ≤ 2.9e-11"),
 ("$L_\\star\\ge21.7/22.9$", V3, "L★ ≥ 21.7 / 22.9 pc"),
 ("$\\mu_K\\le14.8\\,h$/Mpc", V3, "μ_K ≤ 14.8 h/Mpc"),
 ("$<0.1$\\,Mpc", V3, "μ_K < 0.1 Mpc⁻¹"),
 ("$c^2\\approx-0.058\\,\\epsilon\\gamma_L<0$", V3, "c² ≈ −0.058 εγ_L < 0"),
 ("$\\Gamma\\to1.22474$ against the localised 1.224745", V3, "Γ → 1.22474 against the localised 1.224745"),
 ("margin $\\ge1.8\\times10^4$", V3, "margin ≥ 1.8e4"),
 ("11,250 solves, 0 unconverged", V3, "11,250 solves, 0 unconverged"),
 ("$+0.006$\\,\\%", V3, "(+0.006 %)"),
 ("$N\\le0.048$ (globulars) and $\\le0.013$ (satellites)", V3, "N ≤ 0.048 (globulars), ≤ 0.013 (satellites)"),
 ("13/13 checks", X3, "13/13 PASS"),
 ("fails 6 of 12", V3, "switch removed, fails 6 of 12"),
 ("3 degrees of freedom, 8 second-class constraints and rank 4", V3, "3 DOF: no tertiary constraint, 8 second-class constraints, rank 4"),
 ("0.003--0.005", V3, "it is 0.003–0.005"),
 ("0 of 1,804 cells pass", V3, "0 of 1,804 cells pass"),
 ("disagree at $\\ge5\\sigma$", V3, "disagree at ≥ 5σ"),
 ("9.3603\\times10^{-11}", VH, "9.3603e-11 / 1.1312e-10"),
 ("$1.1312\\times10^{-10}$", VH, "9.3603e-11 / 1.1312e-10"),
 ("PASS on both footings & VH1", VH, "PASSES Codex's three KT40/KT42 health gates on both footings"),
 ("C_3^2\\rho_{\\rm vac}=128\\pi F^3", SI, "C3^2 rho_vac=128pi F^3"),
 ("\\frac{32\\pi F^3}{C_3^2\\rho_{\\rm vac}}", SI, "32pi F^3/(C3^2 rho_vac)"),
 ("a_{\\rm MOND}=2F/C_3", SI, "a_MOND=1/(K C3)=2F/C3"),
 ("AZ35--AZ39", PR, "AZ35 complete to NO VERDICT on full nonlinear"),
 ("post-Newtonian sign", PR, "AZ36 complete to NO VERDICT on full nonspherical"),
 ("a Sun moving through the khronon frame", PR, "AZ37 complete to NO VERDICT on the selected moving"),
 ("not evaluable without an external model", PR, "AZ38 NOT EVALUABLE for a realistic interior"),
 ("charged-background causality", PR, "AZ39 NO VERDICT for full charged-background"),
 ("\\texttt{8aeba82a87}", V3, "8aeba82a87"),
 ("\\texttt{8c5703da06}", AD, "C6P, 8c5703da06"),
 ("\\texttt{17d7b7ecdc}", AD, "V3W W1, 17d7b7ecdc"),
 ("\\texttt{ee4210e959}", AD, "V3X, ee4210e959"),
 ("\\texttt{9c11102bf3}", AD, "AX1, 9c11102bf3"),
 ("\\texttt{7ac515f958}", BR, "v3s stays adopted, scoped (7ac515f958)"),
 ("10.5281/zenodo.23968171", BR, "10.5281/zenodo.23968171"),
]
ws = lambda t: re.sub(r"\s+", " ", t)
cache = {}
def src(p):
    if p not in cache:
        cache[p] = ws(open(os.path.join(ROOT, p), encoding="utf-8").read())
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
        if re.search(r"\d", lit) and not in_src: ok += 1
        elif not re.search(r"\d", lit): ok += 1   # no digit to mutate
        else: bad.append(("mutant survived", frag, path))
    elif in_tex and in_src: ok += 1
    else: bad.append(("tex" if not in_tex else "src", frag, path))
rules = [
 ("kappa stated as fitted", "$\\kappa=\\tfrac12$ is fitted" in TEX),
 ("not closed stated", "The theory is not closed" in TEX),
 ("no favouring claim", "Nothing here says the data favour this framework" in TEX),
 ("no local paths", "/Users/" not in TEX),
 ("no 'cold dark matter'", "cold dark matter" not in TEX.lower()),
 ("credit section present", "\\section{Credit}" in TEX),
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
