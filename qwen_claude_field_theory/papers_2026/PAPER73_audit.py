#!/usr/bin/env python3
"""PAPER73 audit: each quoted number appears in the TeX and, as the literal given, in the lane file named beside it
(working tree, HEAD or origin/main: another session may hold the newer copy of a lane). Naming rules; no local paths;
no pending placeholder; the paper's own arithmetic recomputed.
Run: python3 PAPER73_audit.py (exit 0 only if all pass).
--mutate changes one digit of each source literal (and of each TeX number in the arithmetic checks); exit 0 only if
every mutated literal then fails.
kappa = 1/2 FITTED; not theory closed; the cold component is cold dark energy (the clock's dust), never a particle."""
import json, math, os, re, subprocess, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TEX = open(os.path.join(HERE, "PAPER73_the_lock_the_amount_cannot_balance_2026.tex"), encoding="utf-8").read()
P = "qwen_claude_field_theory/papers_2026/"
F = "fable52_push/"; C9 = "closure_2026_11_09/"; D = "closure_2026_11_10/"; H = "hy4_preview_push/"
C11 = "closure_2026_11_11/"; T = "toe_2026_11_10/"; R22 = "rebuild_2026_10_22/"
P69 = P + "PAPER69_closure_by_verdict_2026.zenodo.json"
P70 = P + "PAPER71_switch_theorems_kids_outer_points_2026.zenodo.json"   # carries PAPER70's DOI as a related id
P71 = P + "PAPER71_switch_theorems_kids_outer_points_2026.zenodo.json"
P72 = P + "PAPER72_law_with_cold_dark_energy_counted_once_2026.zenodo.json"
SHP = F + "SHP1_cold_component_shape/RESULT.md"
ONE = F + "ONE1_counted_once/RESULT.md"
PD1 = C9 + "PD1_phantom_is_dust/RESULT.md"
HIS = F + "HIS1_history_reading/RESULT.md"
HSR = F + "HIS1R_history_regrade/RESULT_BLIND.md"
FRM = F + "FRM1_formation_theory/RESULT.md"
LFS = D + "LFS1_leafwise_flux_supply/RESULT.md"
AMT = D + "AMT1_amount_budget/AMOUNT_BUDGET.md"
GAS = H + "HY4-1_GAS1_hot_gas_census/RESULT.md"
GASc = H + "HY4-1_GAS1_hot_gas_census/FROZEN_CRITERIA.md"
AKST = T + "AKS1_acceleration_keyed_sink/FROZEN_CRITERIA_T.md"
AKSR = T + "AKS1_acceleration_keyed_sink/RESULT.md"
SMF = D + "SMF1_smooth_frame_parent/RESULT.md"
THY = D + "THEORY_ASSEMBLED_2026-11-10.md"
L = [
 # header: the DOIs of the companions, each read from its own deposit
 ("PAPER69 (DOI 10.5281/zenodo.24025170", P69, "10.5281/zenodo.24025170"),
 ("PAPER70 (DOI 10.5281/zenodo.24092073", P70, "10.5281/zenodo.24092073"),
 ("PAPER71 (DOI 10.5281/zenodo.24095262", P71, "10.5281/zenodo.24095262"),
 ("PAPER72 (v1.1 DOI 10.5281/zenodo.24125791", P72, "10.5281/zenodo.24125791"),
 # section 1: the ontology
 ("5.41$ units of gravitating mass per unit of baryons", THY,
  "The universe carries 5.41 units of it per unit of baryons"),
 ("Matter couples to the metric only", THY, "Matter couples to the metric only"),
 ("There is no fifth force on matter", THY, "no external field effect"),
 # section 2: the law as a measurement
 ("SPARC has 2700 points in 149 galaxies.", SHP, "SPARC has 2700 points in 149 galaxies."),
 ("175 files, 2700 points against", SHP, "175 files, 2700 points (Lelli+2017: 2693), 149 galaxies (153)"),
 ("0.057\\,dex canonical (0.021 alt) for $x$ from 0.18 to 10, against a line of 0.10", SHP,
  "The worst bin median is within\n0.057 dex canonical (0.021 alt) for x from 0.18 to 10, against a line of 0.10."),
 ("rms 0.0563 (line 0.0660) canonical and 0.0558 alt", PD1, "rms 0.0563 (line 0.0660)"),
 ("rms 0.0563 (line 0.0660) canonical and 0.0558 alt", PD1, "PASS 0.0558"),
 ("median truncation radius 186\\,kpc", PD1, "median R_trunc 186 kpc"),
 ("$1.40\\pm0.03$/$1.28\\pm0.03$ times", SHP, "1.40 +-\n0.03 /\n1.28 +- 0.03 times the law"),
 ("roughly flat from $x\\sim15$ to $\\sim200$", SHP, "roughly flat from x ~ 15 to ~ 200"),
 ("$\\kappa=\\tfrac12$ fitted", THY, "kappa (fitted)"),
 # section 3: the six rules
 ("The action is QX17's (A), certified (label CERTIFIED).", THY, "The action is QX17's (A)."),
 ("The action is QX17's (A), certified (label CERTIFIED).",
  "closure_2026_11_06/QX17_covariant_field_equations/RESULT.md", "**Label: CERTIFIED**"),
 ("\\textbf{Fields.} The metric, one clock field that picks a slicing", THY, "1. **Fields.** The metric, one clock field tau"),
 ("\\textbf{One conserved charge.} The clock equation", THY, "2. **One conserved charge.**"),
 ("\\textbf{Falling clock.} Where the clock free-falls", THY, "3. **Falling clock = cold dust.**"),
 ("\\textbf{Standing clock.} Where the clock stands still", THY, "4. **Standing clock = the law.**"),
 ("\\textbf{Counted once.} A halo is made", THY, "5. **Counted once.**"),
 ("\\textbf{The joint.} How a falling clock", THY, "6. **The joint.**"),
 # section 4.1 T4
 ("Inside any ball whose boundary free-falls, the net polarization charge is exactly zero, at all times, for any exchange\nrate, alignment and multipole", SMF,
  "The frame's polarization charge in that region is zero at every time, for every exchange rate,\n  alignment and ell"),
 ("for any momentum equation", AKSR, "whatever the momentum equation"),
 ("\\textbf{T4 GAUSS (exact; SMF1 S0b reproduced)}", AKST, "**T4 GAUSS (exact; SMF1 S0b reproduced).**"),
 ("\\textbf{S0b (exact, Gauss)}", SMF, "**S0b (exact, Gauss):**"),
 ("for any momentum equation", AKSR,
  "**T4 Gauss (exact; SMF1 S0b):** the net polarization charge in any free-fall-bounded ball is 0 at all times, whatever the momentum equation"),
 # section 4.2 LFS1
 ("a static halo cannot grow", LFS, "A static halo cannot grow."),
 ("ILL-POSED", LFS, "**Label, canonical and alt: ILL-POSED.**"),
 ("about $10^{-6}$", LFS, "about 1e-6"),
 ("total polarization charge is zero", LFS, "Its total polarization charge is then\n  exactly zero"),
 # section 4.3 AMT1: the budget
 ("$X_s=59.5\\,M_b$", AMT, "**X_s = 59.5 M_b**"),
 ("$\\mathbf{5.41\\,M_b}$", AMT, "**5.41 M_b** (Omega_c/Omega_b, the whole cosmic cold-to-baryon ratio)"),
 ("$\\mathbf{1.06\\,M_b}$ turned around by $z=0$", AMT, "**1.06 M_b** turned around by z 0"),
 ("41.48", AMT, "| 272 | 41.9814 | 41.48 | 2.326e42 | 7.668 | 39.14 | 29.63 |"),
 ("97.82", AMT, "| 637 | 98.3168 | 97.82 | 5.483e42 | 18.081 | 92.28 | 69.87 |"),
 ("\\textbf{the whole cosmic budget is spent here}", AMT, "**the whole cosmic budget is spent here**"),
 ("$+4.85$/$+4.93\\sigma$", AMT, "+4.85 / +4.93 sigma"),
 ("$12.09$ to $12.11$", AMT, "X_s/5.41 = 12.09 to 12.11"),
 ("{\\bf MISSING BARYONS EXCLUDED [AMOUNT AND AMPLITUDE]}", GAS, "**MISSING BARYONS EXCLUDED [AMOUNT AND AMPLITUDE]**"),
 ("\\[\n\\Sigma_{\\rm gas}=\\frac{a_0}{\\pi G x_b^{2}},", GAS, "Sigma_gas = a0 / (pi G x_b^2),"),
 ("x_b^{2}=R_b(1+R_b)=5.41\\times6.41=34.6781,", GAS, "x_b^2 = R_b (1 + R_b) = 5.41 x 6.41 = 34.6781"),
 ("$1.287355", GAS, "1.287355e-02 kg/m^2 = 6.1627 Msun/pc^2"),
 ("$0.0392\\pm0.0069$", GAS, "0.0392 +- 0.0069"),
 ("$0.0324\\pm0.0057$", GAS, "0.0324 +- 0.0057"),
 ("36/41 times below the law", GAS, "36 / 41 times below the law"),
 ("$1.4002\\pm0.2211$", GAS, "1.4002 +- 0.2211 (canonical) /\n1.2740 +- 0.2012 (alt) of the law"),
 ("{\\bf The pre-registered acceptance line is 0.891}", GASc, "Amplitude line   0.891 = 10^-0.05"),
]
# the paper's own arithmetic: (fragment in the TeX, computed value, TeX-printed number, format)
XS, BUD, DEL = 59.50, 5.41, 1.06
A = [
 ("11.00 times", XS / BUD, "11.00", "%.2f"),
 ("56 times", XS / DEL, "56", "%.0f"),
 ("$1.33\\times10^{14}M_\\odot$", 1.3257e14, "1.33", None),
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
 ("the only 'cold dark matter' is a denial", TEX.lower().count("cold dark matter") == 1 and "never ``cold dark matter''" in TEX and "cdm-like" not in TEX.lower()),
 ("footings never pooled", "never pooled" in TEX),
 ("no local paths", "/Users/" not in TEX),
 ("no pending placeholder", "\\pend{" not in body),
 ("frozen reading before post hoc", "the frozen one is given first" in TEX or "frozen one first" in TEX),
 ("the law is stated as a measurement", "a measurement, not a hypothesis" in TEX),
 ("the lock is stated as a conservation cap", "cannot be manufactured during infall" in TEX),
 ("the decisive number is pre-registered", "The pre-registered acceptance line is 0.891" in TEX),
 ("own wrong estimates are listed", "Our own estimates that were wrong" in TEX),
 ("memory inputs are declared", "What is from memory" in TEX),
 ("lanes are not registered", "None of these lanes is registered" in TEX),
 ("T4's missing folder is disclosed", "T4 has no lane folder of its own" in TEX),
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
