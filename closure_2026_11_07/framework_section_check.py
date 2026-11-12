#!/usr/bin/env python3
"""Check PAPER70_v1_1_FRAMEWORK_SECTION_DRAFT.md: every quoted literal appears in the draft and, as given, in the committed
source named beside it (read from origin/main if absent locally). --mutate changes one digit of each source literal;
exit 0 only if every mutated literal then fails. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, re, subprocess, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DOC = open(os.path.join(HERE, "PAPER70_v1_1_FRAMEWORK_SECTION_DRAFT.md"), encoding="utf-8").read()
C6 = "closure_2026_11_06/"; C7 = "closure_2026_11_07/"; RR = "real_research/"
NOGO = C6 + "ALL_GATES_NOGO_2026_11_06.md"; QX15 = C6 + "QX15_cmb_primary_likelihood/README.md"
QX12 = C6 + "QX12_triangle/README.md"; SE2 = C6 + "SE2_step_as_systematics/RESULT.md"
UA1 = C7 + "UA1_fragile_rows/RESULT.md"; KX1 = C7 + "KX1_kids_joint_budget/RESULT.md"
CE2 = C7 + "CE2_late_heated_window/RESULT.md"; NA2 = C7 + "NA2_compact_baryon_remnant/RESULT.md"
FC = C7 + "FRAMEWORK_CANDIDATE_2026_11_07.md"; Q17D = C7 + "QX17D_blend_field_equations/RESULT.md"
XR13 = RR + "cross_thread_review_2026_09_26/XR13_README.md"; XR16 = RR + "cross_thread_review_2026_09_26/XR16_README.md"
L388o = RR + "dark_sector_2026/L388_linear_gate_pooled.out"; L388p = RR + "dark_sector_2026/L388_linear_gate_pooled.py"
L377 = RR + "dark_sector_2026/L377_full_construction_pm.py"; L362 = RR + "g03_audit_2026/L362_forest_pincer_convergence.py"
L370 = RR + "merger_infall_2026/L370_boosted_infall_mergers.out"; L370M = RR + "merger_infall_2026/L370_boosted_infall_mergers_MUTATE.out"
# (literal in the doc, source file, literal in that source)
L = [
 ("L1 PASS 3741.08 /\n  3741.15", QX15, "| 3741.08, Delta -64.72 | 3741.15, Delta -64.65 |"),
 ("+172,848 / +166,612", QX15, "| +172,848 | +166,612 |"),
 ("omega_b 0.02236, omega_d 0.1209", QX15, "omega_b 0.02236, omega_d 0.1209"),
 ("R = omega_d/omega_b = 5.562", QX12, "R = omega_d/omega_b = 5.562"),
 ("near 546 km/s", XR13, "The top bin would reach 0.868 near 546 km s⁻¹."),
 ("v_esc 107-421 km/s", XR16, "v_esc(r_F) was 107–421 km/s"),
 ("| SPARC discs | <= 0.33 / 0.19 |", NOGO, "| SPARC discs | <= 0.33 / 0.19 |"),
 ("| X-COP clusters | ~4.2 / 3.8 |", NOGO, "| X-COP clusters | ~4.2 / 3.8 |"),
 ("| groups | 1.2-3.5 / 0.9-2.9 |", NOGO, "| groups | 1.2-3.5 / 0.9-2.9 |"),
 ("| dSph satellites | ~1.7 / 1.3 |", NOGO, "| dSph satellites | ~1.7 / 1.3 |"),
 ("| Coma UDGs | ~80 |", NOGO, "| Coma UDGs | ~80 |"),
 ("X-COP +0.440 / +0.408", SE2, "**+0.440**"), ("X-COP +0.440 / +0.408", SE2, "**+0.408**"),
 ("groups +0.259 / +0.221", UA1, "+0.232 -> +0.259 canonical, +0.194 -> +0.221 alt"),
 ("NOT A TEST (2 of 9 admissible)", UA1, "2 of 9 admissible -> NOT A TEST"),
 ("f_cap 4.1 vs <= 0.33", NOGO, "(f_cap 4.1 vs <= 0.33)"),
 ("Retention exp(depth/c_s^2) is too sharp", NOGO, "Retention exp(depth/c_s^2) is too sharp"),
 ("chi^2 166-194", NOGO, "fails CMB lensing (chi^2 166-194)"),
 ("0.34 -> 0.50 -> 0.68 -> 0.85 at\n  575 km/s", L388o, "v575: 6.0e+13-1.0e+14: 0.34 (n=47), 1.0e+14-1.5e+14: 0.50 (n=38), 1.5e+14-2.5e+14: 0.68 (n=26), 2.5e+14-1.0e+17: 0.85 (n=7)"),
 ("X-COP (+0.324 / +0.287)", CE2, "GX (+0.324 / +0.287,"), ("(0-1 of 20)", CE2, "GG (0-1 of 20)"),
 ("Mach 1.7-1.9", CE2, "Mach is 1.7-1.9"), ("ram pressure strips the subcluster's sector", CE2, "ram pressure strips the subcluster's sector"),
 ("eps = M_c,model / M_c,LCDM", RR + "dark_sector_2026/L366_triggered_carrier_cluster_retention.py", "eps = M_c,model / M_c,LCDM"),
 ('"omega_cdm": 0.12', L362, '"omega_cdm": 0.12'),
 ('A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}', L377, 'A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}'),
 ("n=7 halos", L388o, "2.5e+14-1.0e+17: 0.79 (n=7)"),
 ("0.374-0.607", XR13 .replace("XR13_README.md", "XR13_door_cosmology.out"), "L388 pooled 0.374-0.607"),
 ('"Without the phantom"', XR13, "Without the phantom, the two-sided 20% rule"),
 ('"with the\n     cluster phantoms on"', XR13, "measured in boxes with the cluster phantoms on"),
 ('"-0.000 to -0.000"', L370M, "measured: beta -0.000 to -0.000"),
 ('"beta +0.001 to +0.072"', L370, "beta +0.001 to +0.072"),
 ("VK = (575.0, 600.0, 625.0, 650.0)", L388p, "VK = (575.0, 600.0, 625.0, 650.0)"),
 ('"the trigger posited (no action)"', L388o, "the trigger posited (no action)"),
 ("NO VERDICT on both footings", KX1, "NO VERDICT on both footings"),
 ('"between the gas and the stars"', NA2, "between the gas and the stars"),
 ("(5.5-6e5 m/s)^2", FC, "(5.5-6e5 m/s)^2"),
 ("2F h_mn -> Pi F'(Pi) h_mn", Q17D, "2 F h_mn replaced by Pi F'(Pi) h_mn"),
]
ws = lambda t: re.sub(r"\s+", " ", t)
cache = {}
def src(p):
    if p not in cache:
        fp = os.path.join(ROOT, p)
        if os.path.exists(fp):
            cache[p] = ws(open(fp, encoding="utf-8").read())
        else:
            r = subprocess.run(["git", "-C", ROOT, "show", "origin/main:" + p], capture_output=True, text=True)
            cache[p] = ws(r.stdout) if r.returncode == 0 else ""
    return cache[p]
def mutate(lit):
    m = re.search(r"\d", lit)
    return lit if not m else lit[:m.start()] + str((int(m.group()) + 1) % 10) + lit[m.end():]
D = ws(DOC); ok = 0; bad = []
for frag, path, lit in L:
    if MUT:
        if not re.search(r"\d", lit) or ws(mutate(lit)) not in src(path): ok += 1
        else: bad.append(("mutant survived", frag, path))
    elif ws(frag) in D and ws(lit) in src(path): ok += 1
    else: bad.append(("doc" if ws(frag) not in D else "src", frag, path))
rules = [("kappa fitted", "Kappa = 1/2 FITTED" in DOC), ("not closed", "not theory closed" in DOC),
         ("no favouring", "Nothing here says the data favour the framework" in D),
         ("never pooled", "never pooled" in DOC), 
         ("no local paths", "/Users/" not in DOC), ("no 'cold dark matter'", "cold dark matter" not in DOC.lower()),
         ("CONDITIONAL in title", DOC.splitlines()[0].endswith("(CONDITIONAL)")), ("fold only if CK pass", "only if CK1-CK4 pass" in DOC), ("not a particle", "not a particle species" in DOC)]
if not MUT:
    for n, g in rules:
        if g: ok += 1
        else: bad.append(("rule", n, ""))
for b in bad: print("FAIL", *b)
print(f"{ok} of {len(L) + (0 if MUT else len(rules))} checks pass" + (" (mutate)" if MUT else ""))
print("kappa = 1/2 FITTED; not theory closed.")
sys.exit(0 if not bad else 1)
