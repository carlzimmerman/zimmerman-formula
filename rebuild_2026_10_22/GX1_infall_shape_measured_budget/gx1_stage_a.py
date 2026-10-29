#!/usr/bin/env python3
"""GX1 Stage A: X-COP (HO1(a)'s rule and machinery) with GC3's self-similar infall shape on GS1's measured-gas budget.
Frozen criteria 254f01d34a (committed alone). Machinery: HO1's committed script (91cc5c3bd4) executed read-only up to its grade block;
the halo's cumulative profile and root solver are swapped (Burkert -> infall) in that namespace only.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gx1_stage_a.py      (GX1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib, resource
import numpy as np
from scipy.optimize import brentq, minimize_scalar

MUT = os.environ.get("GX1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
HO1 = os.path.join(REB, "HO1_xcop_hotgas_heldout", "ho1_heldout.py")
src = open(HO1).read(); src = src[:src.index("# ------------------------------------------------------------------ 6. grade per footing")]
src = src.replace('"ho1_heldout.out"', '"gx1a_ho1_step0_STOPPED.out"').replace('"ho1_heldout_results.json"', '"gx1a_ho1_step0_STOPPED.json"')
os.environ.pop("HO1_MUTATE", None)
HO = {"__file__": os.path.join(HERE, "ho1_ro.py"), "__name__": "ho1_ro"}
exec(compile(src, HO1, "exec"), HO)
P, FEET = HO["P"], HO["FEET"]
P("\n================ GX1 Stage A (criteria 254f01d34a)" + ("  [MUTATE: outer slope q = 3]" if MUT else ""))
checks = {}
BK0, SR0, BUD0 = HO["Bk"], HO["solve_r0"], HO["budget"]

# GC3's infall profile (q = 2.25; MUTATE q = 3)
Q = 3.0 if MUT else 2.25
_xg = np.logspace(-7, 7, 20001); _fx = 1.0 / ((1 + _xg) * (1 + _xg ** 2) ** ((Q - 1) / 2))
_Ix = np.r_[0.0, np.cumsum(0.5 * (_fx[1:] * _xg[1:] ** 3 + _fx[:-1] * _xg[:-1] ** 3) * np.diff(np.log(_xg)))] + _fx[0] * _xg[0] ** 3 / 3
def I_inf(X): return np.interp(np.log(np.maximum(np.asarray(X, float), 1e-7)), np.log(_xg), _Ix)
def Bk_inf(X): return 4.0 * I_inf(X)                                   # pi s r0^2 Bk_inf = 4 pi s r0^2 I
K1 = []
def solve_r0_inf(M, R, s):
    g = lambda lr: math.log(math.pi * s * math.exp(2 * lr) * float(Bk_inf(R / math.exp(lr)))) - math.log(M)
    lo, hi = math.log(R * 1e-4), math.log(R * 1e4)
    pk = float(minimize_scalar(lambda lr: -g(lr), bounds=(lo, hi), method="bounded", options={"xatol": 1e-10}).x)
    if g(pk) < 0: HO["SAT"]["n"] += 1; return math.exp(pk)
    r0 = math.exp(brentq(g, lo, pk, xtol=1e-12))
    K1.append(abs(math.pi * s * r0 ** 2 * float(Bk_inf(R / r0)) / M - 1)); return r0

def grade(lab, shape, rsp=False):
    HO["Bk"], HO["solve_r0"] = (BK0, SR0) if shape == "burkert" else (Bk_inf, solve_r0_inf)
    HO["budget"] = (lambda name, f=1.0: (lambda b: (b[0], 0.364 * b[1], b[2]))(BUD0(name, f))) if rsp else BUD0
    out = {}
    for f in FEET:
        g = HO["xcop_cl2"](f)
        out[f] = dict(mean=g["mean"], rms=g["rms"], by_x=g["by_x"], verdict=g["verdict"], per_cluster=g["per_cluster"])
    o = out["canonical"]
    P(f"  {lab:34s}: mean {o['mean']:+.3f} rms {o['rms']:.3f} | by x " + ", ".join(f"{k}:{v:+.3f}" for k, v in o["by_x"].items()) + f" -> {o['verdict']}"
      + f"   [alt mean {out['alt']['mean']:+.3f} rms {out['alt']['rms']:.3f}]")
    return out
RES = dict(criteria="254f01d34a", machinery="HO1 91cc5c3bd4 (read-only; halo profile swapped)", mutate=MUT, runs={})
R0 = grade("STEP 0 Burkert (HO1(a))", "burkert")
checks["K0"] = all(abs(R0[f]["mean"] - (-0.002)) < 0.0015 and abs(R0[f]["rms"] - 0.126) < 0.0015 for f in FEET)
P(f"  K0 reproduces HO1(a): {'PASS' if checks['K0'] else 'FAIL'}")
RES["runs"]["step0"] = R0
K1.clear(); sat0 = HO["SAT"]["n"]
RES["runs"]["PRIMARY"] = grade("PRIMARY infall, truncated at r_ta", "infall")
nsat = HO["SAT"]["n"] - sat0
RES["runs"]["V_splashback"] = grade("V infall, truncated at 0.364 r_ta", "infall", rsp=True)
checks["K1"] = (max(K1) < 1e-8) if K1 else True
checks["K3"] = (Q == 2.25)
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K2"] = peak < 1.0
def cls(o): return "PASS" if (abs(o["mean"]) <= 0.05 and o["rms"] <= 0.10) else "FAIL"
RES["stageA"] = {f: cls(RES["runs"]["PRIMARY"][f]) for f in FEET}; RES["checks"] = checks; RES["saturated_primary"] = nsat
P(f"\n  K1 budget root to 1e-8: {'PASS' if checks['K1'] else 'FAIL'} (saturated {nsat}); K3 q = 2.25: {'PASS' if checks['K3'] else 'FAIL'}; K2 peak RSS {peak:.2f} GB")
P(f"=== STAGE A (X-COP, PRIMARY): canonical {RES['stageA']['canonical']}; alt {RES['stageA']['alt']}")
fn = os.path.join(HERE, f"gx1_stage_a_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"gx1_stage_a{TAG}.out"), "w").write("\n".join(HO["OUT"]).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(checks.values()) else 1)
