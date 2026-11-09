#!/usr/bin/env python3
"""PAPER71 audit: each quoted number appears in the TeX and, as the literal given, in the committed lane file named beside it;
naming rules; no local paths; no pending placeholder. Run: python3 PAPER71_audit.py (exit 0 only if all pass).
--mutate changes one digit of each source literal; exit 0 only if every mutated literal then fails.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, re, subprocess, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEX = open(os.path.join(HERE, "PAPER71_switch_theorems_kids_outer_points_2026.tex"), encoding="utf-8").read()
F = "fable52_push/"
SW = F + "SWT1_switch_theorems/RESULT.md"; EM = F + "EMV1_effective_medium_validation/RESULT.md"
GA = F + "GAL1_growth_lensing_allowance/RESULT.md"; KO = F + "KO1_kids_outer_points/RESULT.md"
KR = F + "KO1R_kids_outer_regrade/RESULT.md"; SN = F + "SNP1_snowplow_clearing/RESULT.md"
P = "qwen_claude_field_theory/papers_2026/"
P69 = P + "PAPER69_closure_by_verdict_2026.zenodo.json"; P70 = P + "PAPER70_field_equations_closure_2026.zenodo.json"
# (fragment in the TeX, source file, literal in that file)
L = [
 ("DOI 10.5281/zenodo.24025170", P69, "10.5281/zenodo.24025170"),
 ("DOI 10.5281/zenodo.24092073", P70, "10.5281/zenodo.24092073"),
 # the class
 ("Lane SWT1 proves (19 theorems)", SW, "19 theorems"),
 ("$-0.43$ to $-0.50$", SW, "-0.43 to -0.50"),
 ("Lane SNP1 adds (28 theorems)", SN, "28 theorems"),
 ("$\\tfrac12a_0M_b\\,\\mu<F_w<a_0M_b\\,\\mu$", SN, "(1/2) a0 M_b mu < F_w < a0 M_b mu"),
 ("$R_{\\rm eq}\\to\\tfrac32\\,m(1+m/2)\\,r_M$", SN, "deep closed form R_eq = (3/2) k r_M"),
 ("Lane KO1 adds (12 theorems)", KO, "12 theorems"),
 ("Lane EMV1 adds 13 theorems", EM, "13 theorems"),
 # filling
 ("CMB-lensing line 0.0354", SW, "0.0354"),
 ("$f\\le0.0231$ (SWT1)", SW, "f <= 0.0231"),
 ("needs a filling of 0.29", SW, "needs a filling of 0.29"),
 ("12.6 times the allowance", SW, "12.6 times the allowance"),
 ("reaches 0.43 of that radius", SW, "0.43 of that radius"),
 ("(0.303/0.361)", SW, "0.303 / 0.361"),
 ("(0.0180/0.0182)", SW, "0.0180 / 0.0182"),
 ("EMV1, T2 HOLDS on both footings", EM, "T2 HOLDS / T2 HOLDS"),
 ("0.0265/0.0259 at the top of that range", EM, "0.0265 (+0.149)"),
 ("0.0265/0.0259 at the top of that range", EM, "0.0259 (+0.123)"),
 ("the readings move by at most 0.001", EM, "at most 0.001"),
 ("GAL1, ALLOWANCE CONFIRMED on both footings", GA, "ALLOWANCE CONFIRMED / ALLOWANCE CONFIRMED"),
 ("$f\\le0.0197$", GA, "f <= 0.0197"),
 ("0.0134 if they exist from $z=6$", GA, "at z 6 it gives 0.0134"),
 ("(0.12 and 0.075)", GA, "f sigma8 allows 0.12, S8 0.075"),
 # KiDS
 ("(181,477 lenses;", KO, "181,477"),
 ("40,667 lenses remain", KO, "40,667"),
 ("$1.098\\pm0.154$/$0.999\\pm0.141$", KO, "1.098 +- 0.154"),
 ("$1.098\\pm0.154$/$0.999\\pm0.141$", KO, "0.999 +- 0.141"),
 ("(line 0.891)", KO, "0.891 line"),
 ("(0.463/0.422)", KO, "0.056 / 0.463"),
 ("(0.463/0.422)", KO, "0.051 / 0.422"),
 ("$1.0822\\pm0.1583$/$0.9847\\pm0.1440$", KR, "1.0822 +- 0.1583"),
 ("$1.0822\\pm0.1583$/$0.9847\\pm0.1440$", KR, "0.9847 +- 0.1440"),
 ("518 lenses have a neighbour exactly 0.3\\,dex heavier", KR, "518 lenses have only tied hosts"),
 ("reproduces the lane to $2\\times10^{-15}$", KR, "2e-15"),
 ("1.6 to 1.8 times above the law at inner radii", KO, "1.6 to 1.8 times above the law at inner radii"),
 ("the law's floor for it is 0.98", KO, "1.04 +- 0.06 | 0.98"),
 ("$0.61\\pm0.09$ at the frozen radius", KO, "0.61 +- 0.09"),
 ("$0.71\\pm0.12$ at 1.3 times it", KO, "0.71 +- 0.12"),
 ("$0.81\\pm0.13$ at 1.6 times it", KO, "0.81 +- 0.13"),
 ("(5.56\\,$M_b$) is excluded at 5.3 to 5.6$\\sigma$", KO, "5.3 to 5.6 sigma"),
 ("33 to 47\\,$M_b$ per galaxy at the wall (2$\\sigma$: at least 23)", KO, "33 to 47 M_b per galaxy at the wall (2 sigma: at least 23)"),
 ("40 to 56 (at least 27) on alt", KO, "40 to 56 (at least 27) on alt"),
 ("they add 0.012/0.011 of the law's level", KO, "0.012 / 0.011 of the law's level"),
 ("the exclusion is 5.2 to 5.4$\\sigma$", KO, "5.2 to 5.4 sigma"),
 ("at least 4.1/4.9 times the record's share", KO, "4.1 / 4.9 times the record's share"),
 ("(0.78/0.66)", KO, "0.78 / 0.66"),
 ("(0.056/0.051 against the amplitude above)", KO, "0.056 / 0.463"),
 ("(0.056/0.051 against the amplitude above)", KO, "0.051 / 0.422"),
 ("1.50 $\\pm$ 0.08", KO, "1.50 +- 0.08"),
 ("0.97 $\\pm$ 0.28", KO, "0.97 +- 0.28"),
 ("$0.47\\pm0.04$", KO, "0.47 +- 0.04"),
 ("($-0.19\\pm0.39$; $0.13\\pm0.68$ with the widest veto)", KO, "-0.19 +- 0.39"),
 ("($-0.19\\pm0.39$; $0.13\\pm0.68$ with the widest veto)", KO, "0.13 +- 0.68"),
 ("early types sit at $1.34\\pm0.18$", KO, "1.34 +- 0.18"),
 # clearing
 ("by 3 to 20 times around galaxies", SW, "3-20x"),
 ("by 4 to 40 times in groups and clusters", SW, "4-40x"),
 ("Clearing fails above 2.8 to 4.0 times the share", SW, "| 2.8 / 3.0 |"),
 ("Clearing fails above 2.8 to 4.0 times the share", SW, "| 3.8 / 4.0 |"),
 ("Dynamics (SNP1): FAILS on both footings", SN, "**SNP1: FAILS / FAILS**"),
 ("7.86 / 7.46 / 7.44 / 7.43", SN, "7.86 / 7.46 / 7.44 / 7.43"),
 ("207 / 236 / 260 / 278 kpc", SN, "207 / 236 / 260 / 278"),
 ("0.43--0.63 of KiDS's outermost radius", SN, "0.43-0.63 of R_K"),
 ("8.6--19.0 $M_b$ stay inside 200\\,kpc", SN, "8.6-19.0 M_b"),
 ("outweighs the wall force by 3.8/4.9", KO, "outweighs the wall force by 3.8 / 4.9"),
 ("at the best-fit shares by 8.0/10.2", KO, "8.0 / 10.2"),
 ("at least 23 baryon masses per galaxy", KO, "at least 23 / 27 M_b per"),
 ("(53.64\\,$M_b$)", KO, "X 53.64"),
 # corrections
 ("falls to $+0.31\\pm0.21$", KO, "+0.31 +- 0.21"),
 ("it wins by 3 to 20 times", SW, "3-20x"),
]
def ws(s): return re.sub(r"\s+", " ", s)
_cache = {}
def src(path):
    """working-tree file; if absent or older, also the copies at HEAD and at origin/main (another session may hold the newer one)."""
    if path not in _cache:
        t = ""
        fp = os.path.join(ROOT, path)
        if os.path.exists(fp): t += open(fp, encoding="utf-8", errors="replace").read()
        for ref in ("HEAD", "origin/main"):
            r = subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{path}"], capture_output=True, text=True)
            if r.returncode == 0: t += "\n" + r.stdout
        _cache[path] = ws(t)
    return _cache[path]
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
    else: bad.append(("tex" if not in_tex else "src", frag, path))
body = TEX.split("\\begin{document}")[1]
rules = [
 ("kappa stated as fitted", "$\\kappa=\\tfrac12$ is fitted" in TEX),
 ("not closed stated", "The theory is not closed" in TEX),
 ("no favouring claim", "Nothing here says the data favour this framework" in TEX),
 ("no completion claimed", "This note does not complete the theory" in TEX),
 ("no local paths", "/Users/" not in TEX),
 ("no 'cold dark matter'", "cold dark matter" not in TEX.lower() and "cdm-like" not in TEX.lower()),
 ("no pending placeholder", "\\pend{" not in body and not any(l.startswith("% PENDING") for l in TEX.splitlines())),
 ("post hoc items are called post hoc or declared", "declared in amendments before they were computed" in TEX and "seen after the freeze" in TEX and "so they are post hoc" in TEX),
 ("the regrade's different label is stated", "NOT SEPARATED on the canonical footing" in TEX),
 ("own wrong estimates are listed", "This note's own estimates" in TEX),
 ("lanes are not registered", "none is registered in the closure record" in TEX),
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
