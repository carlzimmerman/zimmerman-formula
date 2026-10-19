"""CFG840 -- robustness of CFG829.  Criteria: FROZEN_CRITERIA.md (bb354e8da).  Reuses cfg829.py's loader/amplitude unchanged.
Run: python3 cfg840.py (CFG840_MUTATE=1).  kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, numpy as np, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG840_MUTATE") == "1"
if MUT: os.environ["CFG829_MUTATE"] = "1"                                  # cfg829.load applies g_obs x 2.75
else: os.environ.pop("CFG829_MUTATE", None)
src = open(os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py")).read().split("P(\"CFG829  KiDS")[0]
M = {"__file__": os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py"), "__name__": "cfg829defs"}; exec(compile(src, "cfg829.py", "exec"), M)
load, amp, nu_e, A0, A_DW = M["load"], M["amp"], M["nu_e"], M["A0"], M["A_DW"]
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
BLUE = ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0)
SERS = ("Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0)
ALLK = ("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", None)
GAMA = ("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt", "Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt", None)
W0 = (10 ** -13.3, 10 ** -11.9)
def run(dataset, win, foot="canonical", gshift=0.0):
    gb, go, C = load(*dataset); gbs = gb * 10 ** gshift; gl = gbs * nu_e(gbs / A0[foot]); return amp(gbs, go, C, gl, win)
V = [("primary (CFG829)", BLUE, W0, "canonical", 0.0),
     ("V1 window -0.3 dex", BLUE, (W0[0] / 2, W0[1] / 2), "canonical", 0.0),
     ("V1 window +0.3 dex", BLUE, (W0[0] * 2, W0[1] * 2), "canonical", 0.0),
     ("V1 window widened 1e-14", BLUE, (1e-14, W0[1]), "canonical", 0.0),
     ("V2 M* -0.2 dex", BLUE, W0, "canonical", -0.2),
     ("V2 M* +0.2 dex", BLUE, W0, "canonical", +0.2),
     ("V3 Sersic n<2", SERS, W0, "canonical", 0.0),
     ("V5 alt footing", BLUE, W0, "alt", 0.0)]
P("CFG840  robustness of CFG829 (blue / disc lenses at the dwarfs' g_bar)" + ("  [MUTATE g_obs x2.75]" if MUT else ""))
RES = dict(lane="CFG840", mutate=MUT, variants={}); fails = []
for name, ds, win, foot, gs in V:
    a = run(ds, win, foot, gs)
    if a is None: P(f"  {name:26s} <2 points"); fails.append(name + " (no data)"); continue
    ok = abs(a["A"] - 1) < 2 * a["sA"] and (A_DW - a["A"]) >= 3 * a["sA"]
    if not ok: fails.append(name)
    RES["variants"][name] = dict(A=a["A"], sA=a["sA"], n=a["n"], ok=ok)
    P(f"  {name:26s} A {a['A']:.3f} +- {a['sA']:.3f} ({a['n']} pts)  (A-1)/s {(a['A'] - 1) / a['sA']:+.1f}  (2.75-A)/s {(A_DW - a['A']) / a['sA']:+.1f}  {'ok' if ok else 'FAILS'}")
g, k = run(GAMA, W0), run(ALLK, W0)
z = (g["A"] - k["A"]) / math.hypot(g["sA"], k["sA"]) if g and k else float("nan")
RES["V4"] = dict(gama=g and dict(A=g["A"], sA=g["sA"], n=g["n"]), kids_all=dict(A=k["A"], sA=k["sA"]), z=z)
P(f"  V4 GAMA all-isolated A {g['A']:.3f} +- {g['sA']:.3f} ({g['n']} pts) vs KiDS all-isolated {k['A']:.3f} +- {k['sA']:.3f}: z {z:+.1f} ({'consistent' if abs(z) < 2 else 'differs'})" if g else "  V4 GAMA <2 points")
if not MUT:
    k1 = RES["variants"]["primary (CFG829)"]; P(f"\n  K1 primary A {k1['A']:.3f} +- {k1['sA']:.3f} vs CFG829 1.016 +- 0.086 -> {'PASS' if abs(k1['A'] - 1.016) < 5e-4 and abs(k1['sA'] - 0.086) < 5e-4 else 'FAIL'}")
RES["cls"] = "ROBUST" if not fails else "FRAGILE"; RES["fails"] = fails
P(f"\n  CLASS: {RES['cls']}" + (f"  (failing: {', '.join(fails)})" if fails else ""))
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg840_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg840{sfx}.out"), "w").write("\n".join(OUT) + "\n")
