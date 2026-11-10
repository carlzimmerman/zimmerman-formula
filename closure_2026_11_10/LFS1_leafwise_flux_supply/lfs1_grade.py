"""LFS1 grader: applies FROZEN_CRITERIA section 4 to lfs1_sym.json and lfs1_num.json (or a MUTATE twin's files).

Usage: python3 lfs1_grade.py [suffix]   (suffix '' | _MUTATE_MU1 | _MUTATE_MU2 | _MUTATE_MU3)
Writes lfs1_grade<suffix>.json / .out. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
suf = sys.argv[1] if len(sys.argv) > 1 else ""
sym = json.load(open(os.path.join(here, f"lfs1_sym{suf if suf == '_MUTATE_MU1' else ''}.json")))
num = json.load(open(os.path.join(here, f"lfs1_num{suf}.json")))
base = json.load(open(os.path.join(here, "lfs1_num.json")))   # KA6 needs the unmutated S2 pair
lines = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); lines.append(s)

ka6 = num["KA6"]["pass_"] if num["KA6"]["pass_"] is not None else base["KA6"]["pass_"]
KA = dict(KA1=sym["KA1"], KA2=sym["KA2"], KA3=sym["KA3"], KA4=num["KA4"]["pass_"], KA5=num["KA5"]["pass_"],
          KA6=ka6, S1=sym["S1_pass"])
say("Known answers:", KA)
out = {"suffix": suf, "KA": KA, "labels": {}}
for foot, rows in num["A"].items():
    a1 = all(r["A1"]["pass_"] for r in rows.values())
    a2 = all(r["A2"]["pass_"] for r in rows.values())
    a4 = [r["A4"] for r in rows.values()]
    a4_bad = any(x in ("WALL", "FOLD") for x in a4)
    short = any(r["A3"]["short_of_cap"] for r in rows.values())
    fails = []
    if not a1: fails.append("A1 (lambda not the normal equation's; worst |rho_lambda - 1| = %.6f)"
                            % max(r["A1"]["worst"][0] for r in rows.values()))
    if not a2: fails.append("A2 (negative clock charge at the edge: %s M_b)"
                            % ", ".join("%.1f" % r["edge"]["R_ta"]["q_edge_over_Mb"] for r in rows.values()))
    if a4_bad: fails.append("A4 (%s)" % ", ".join(sorted(set(a4))))
    if not all(KA.values()):
        lab = "NO VERDICT"
    elif fails:
        lab = "ILL-POSED"
    elif short:
        lab = "SUPPLIES-SHORT"
    else:
        lab = "SUPPLIES"
    out["labels"][foot] = dict(label=lab, A1=a1, A2=a2, A4=a4, short_of_cap=short, fails=fails)
    say(f"{foot}: {lab}; A1 {'PASS' if a1 else 'FAIL'}, A2 {'PASS' if a2 else 'FAIL'}, A4 {a4}, reach short of cap {short}")
    for f in fails: say("   fails:", f)
say("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
json.dump(out, open(os.path.join(here, f"lfs1_grade{suf}.json"), "w"), indent=1)
open(os.path.join(here, f"lfs1_grade{suf}.out"), "w").write("\n".join(lines) + "\n")

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
