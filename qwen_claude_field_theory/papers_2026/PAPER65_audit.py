#!/usr/bin/env python3
"""PAPER65 (DRAFT) audit: every quoted number must match the committed lane outputs (rebuild_2026_10_22/ X66, X68, X69,
X70_smooth_core_shape, X71); naming rules (cold dark energy; CDM only inside LambdaCDM); no local path; draft banner present.
Run: python3 PAPER65_audit.py (exit 0 only if all pass).
     python3 PAPER65_audit.py --mutate (perturbs every JSON-derived number; exit 0 only if every number check then FAILS)."""
import json, math, os, re, sys

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.normpath(os.path.join(HERE, "..", "..", "rebuild_2026_10_22"))
TEX = open(os.path.join(HERE, "PAPER65_DRAFT_smooth_core_closed_routes_2026.tex")).read()
F = N = 0; NUMF = NUMN = 0
def check(name, ok, msg=""):
    global F, N
    N += 1; F += (not ok)
    if not MUT: print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))
def J(rel): return json.load(open(os.path.join(RB, rel)))
def bump(t):
    for i in range(len(t) - 1, -1, -1):
        if t[i].isdigit(): return t[:i] + str((int(t[i]) + 1) % 10) + t[i + 1:]
    return t + "1"
def num(name, value, fmt, tpl):
    """tpl holds '{}' where the number sits; the whole context string must appear in the TeX."""
    global NUMF, NUMN
    s = format(value, fmt)
    if MUT: s = bump(s)
    s = tpl.replace("{}", s)
    ok = s in TEX
    NUMN += 1; NUMF += (not ok)
    if not MUT: check(name, ok, f"'{s}'")

# X70 smooth core
x70 = J("X70_smooth_core_shape/x70_smooth_core_results.json")["footings"]
BS1 = 4 * (math.asinh(1) - 1 / math.sqrt(2)); B1 = 3 * math.log(2) - math.pi / 2
num("X70 B_S(1)", BS1, ".5f", "B_S(1)={}"); num("X70 eta_S", 14.8286 * B1 / BS1, ".2f", "\\eta_S={}")
num("X70 SPARC rms canonical A", x70["canonical"]["sparc"]["A_c2b_refit"]["rms"], ".4f", "rms {}")
num("X70 SPARC Upsilon canonical A", x70["canonical"]["sparc"]["A_c2b_refit"]["U_median"], ".2f", "$\\Upsilon$ {})")
num("X70 SPARC Upsilon alt A", x70["alt"]["sparc"]["A_c2b_refit"]["U_median"], ".2f", "\\Upsilon={}<0.50")
num("X70 groups Z canonical", x70["canonical"]["groups"]["Z"], "+.2f", "groups $Z={}$")
num("X70 max |Z| cluster keys canonical", max(abs(c["Z"]) for hk in x70["canonical"]["clusters"]["cells"].values() for c in hk.values()), ".2f", "|Z|\\le{}$")
# X71 measured f*
TPL71 = {("0.0615", "S"): "$Z={}$ ($f_\\star=0.0615$)", ("0.034", "S"): "${}$ ($f_\\star=0.034$)",
         ("0.0615", "B"): "same $f_\\star$: ${}$ and", ("0.034", "B"): "and ${}$, and the groups"}
for fs, label in (("0.0615", "X-COP"), ("0.034", "A1")):
    for sh in ("S", "B"):
        z = J(f"X71_smooth_core_measured_fstar/x71_results_fs{fs}_{sh}.json")["footings"]["canonical"]["clusters"]["cells"]["h0672"]["G-OUT-M3"]["Z"]
        num(f"X71 G-OUT-M3 Z f*={fs} shape {sh}", z, "+.2f", TPL71[(fs, sh)])
# X69 soft floor
x69 = J("X69_soft_floor_sparc/x69_soft_floor_results.json")["footings"]
num("X69 n LOW canonical", x69["canonical"]["per_bg"]["A_c2b_refit"]["nlow"], "d", "{} of 175")
num("X69 LOW worsening canonical (%)", 100 * x69["canonical"]["per_bg"]["A_c2b_refit"]["low"][2], ".1f", "{}\\% (canonical)")
num("X69 LOW worsening alt (%)", 100 * x69["alt"]["per_bg"]["A_c2b_refit"]["low"][2], ".1f", "{}\\% (alt)")
# X66 core gate
rows = J("X66_core_gated_quarter_a0/x66_results.json")["rows"]
pick = lambda **kw: [r for r in rows if all(r[k] == v for k, v in kw.items())][0]
num("X66 R_N 1e9", pick(M=1e9, mode="N", j=0.1, N=2000)["R"], ".2f", "$R$ {}$\\to$")
num("X66 R_G 1e9 canonical", pick(M=1e9, mode="G", footing="canonical", j=0.1, N=2000)["R"], ".2f", "$\\to${})")
# X68 split scale (post-hoc diagnostic medians, canonical)
s68 = J("X68_split_scale_halo/x68_split_scale_results.json")["footings"]["canonical"]["reported"]["S_log"]
num("X68 heaviest-to-target median (groups)", s68["groups"]["Mlim_over_M_median"], ".1f", "{}--5.5$\\times$")
num("X68 heaviest-to-target median (SPARC)", s68["sparc"]["Mlim_over_M_median"], ".1f", "2.5--{}$\\times$")

# naming / hygiene
body = re.sub(r"\\Lambda\s*\{?\\rm\s*CDM\}?|\$\\Lambda\$CDM|\\LambdaCDM", "", TEX)
check("no bare CDM outside LambdaCDM", "CDM" not in body.replace("$\\Lambda$CDM", ""))
check("no 'cold dark matter'", "cold dark matter" not in TEX.lower())
check("names 'cold dark energy'", "cold dark energy" in TEX)
check("no local path", "/Users/" not in TEX and "carlzimmerman" not in TEX)
check("standing line (kappa fitted, not closed)", "fitted" in TEX and "not closed" in TEX)
check("DRAFT banner", "DRAFT" in TEX and "not deposited" in TEX)

if MUT:
    print(f"MUTATE: {NUMF}/{NUMN} number checks fail (all must fail)")
    sys.exit(0 if NUMF == NUMN else 1)
print(f"\nchecks {N - F}/{N}")
sys.exit(0 if F == 0 else 1)
