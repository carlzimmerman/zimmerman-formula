#!/usr/bin/env python3
"""KR1 static consequence (FROZEN_CRITERIA.md 77ebbd6ad2, section 3 row G1-G8): KD1's model P battery with the constant
mu replaced by M_ta, the local K-mass of each member's dust at galaxy turnaround (read from kr1.json).
    python3 kr1_static.py   -> kr1_static.json / kr1_static.out
kd1.py's prefix (KD, grade, GB1 gates) is exec'd read-only; its own KA3/KA4/KA1 run inside it. One thread.
Cold dark energy, never dark matter; no particle. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, resource, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); T0 = time.time(); OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1 << 20)
KR = json.load(open(os.path.join(HERE, "kr1.json")))
KDP = os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.py")
src = open(KDP).read(); cut = src.index("# ------------------------------------------------------------------ per footing")
NS = {"__file__": KDP, "__name__": "kd1_reused"}; a0 = sys.argv; sys.argv = [KDP]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], KDP, "exec"), NS)
sys.argv = a0
KD, grade, flat, GBJ, GB = NS["KD"], NS["grade"], NS["flat"], NS["GBJ"], NS["GB"]
RES = dict(tag="kr1_static", criteria="77ebbd6ad2", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", KA6={}, footings={})
ok6 = True
for k in ("KA3", "KA4", "KA1_canonical", "KA1_alt"):
    RES["KA6"][k] = NS["RES"]["KA"][k]["ok"]; ok6 &= bool(NS["RES"]["KA"][k]["ok"])
P(f"KA6 kd1 prefix own KAs: {RES['KA6']}; RSS {rss():.0f} MB")
F1A = json.load(open(os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit", "f1a.json")))
for f in ("canonical", "alt"):
    b = F1A[f]["best_B2"]; ob, od, h = b["ob"], b["oc"], b["h"]
    row0 = grade(KD(ob, 0.0, h, 1e3), f); dmax = 0.0; okk = True
    for g in row0:
        x, y = flat(row0[g]["num"]), flat(GBJ["cands"]["L0"][f][g]["num"])
        okk &= (x.keys() == y.keys()) and row0[g]["status"] == GBJ["cands"]["L0"][f][g]["status"]
        for k in x:
            if isinstance(x[k], (int, float)) and not isinstance(x[k], bool) and k in y: dmax = max(dmax, abs(x[k] - y[k]))
    RES["KA6"][f"KA2_{f}"] = bool(okk and dmax <= 1e-12); ok6 &= RES["KA6"][f"KA2_{f}"]
    P(f"[{f}] KA6 KD(I0 = 0) vs gb1 L0: max|d| {dmax:.1e} -> {'PASS' if RES['KA6'][f'KA2_{f}'] else 'FAIL'}")
    FO = {}
    for nm, o in KR["footings"][f].items():
        mta = o["GC"]["M_ta"]; stt = dict(n=0, captured=0); row = grade(KD(ob, od, h, mta, stt), f)
        FO[nm] = dict(M_ta=mta, capture=stt, status={g: r["status"] for g, r in row.items()},
                      short={g: (GB["short"](g, r) if r["num"] is not None else r["missing"]) for g, r in row.items()})
        P(f"[{f}] {nm} M_ta {mta:.4g} Mpc^-1 (core pi/M {math.pi/mta*1e3:.3g} kpc): captured {stt['captured']}/{stt['n']}")
        for g, r in row.items(): P(f"[{f}]    {g:17s} {r['status']:10s} {FO[nm]['short'][g]}")
    RES["footings"][f] = FO
RES["KA6_all"] = bool(ok6)
P(f"KA6 all: {'PASS' if ok6 else 'FAIL'}; peak RSS {rss():.0f} MB; {time.time() - T0:.0f} s")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
RES["peak_rss_MB"] = rss()
json.dump(RES, open(os.path.join(HERE, "kr1_static.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "kr1_static.out"), "w").write("\n".join(OUT) + "\n")
