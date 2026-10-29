#!/usr/bin/env python3
"""GX1 Stage B: the lensing line set (GS1's harness: R4, native, measured-gas budget at s_meas) with GC3's infall shape in place of Burkert.
Frozen criteria 254f01d34a. Machinery: GS1's committed script (01f6dd977d) executed read-only up to its measurement section; one extra
source edit swaps X43's cluster halo line (Burkert, edge r_ta) for the infall profile (edge r_ta PRIMARY; 0.364 r_ta variant).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gx1_stage_b.py      (GX1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib
import numpy as np
from scipy.optimize import brentq, minimize_scalar
MUTB = os.environ.get("GX1_MUTATE", "0") == "1"; TAGB = "_MUTATE" if MUTB else ""
HB = os.path.dirname(os.path.abspath(__file__)); RB_ = os.path.dirname(HB); REPO_ = os.path.dirname(RB_)
GSP = os.path.join(RB_, "GS1_measured_gas_outskirts", "gs1_gas_slope.py")
src = open(GSP).read(); src = src[:src.index("# ============================================================== A. measurement")]
os.environ.pop("MUTATE", None); os.environ.pop("GS1_MUTATE", None)
G1 = {"__file__": os.path.join(HB, "gs1_ro.py"), "__name__": "gs1_ro"}
exec(compile(src, GSP, "exec"), G1)
P = G1["P"]
S_MEAS = json.load(open(os.path.join(RB_, "GS1_measured_gas_outskirts", "gs1_gas_slope_results.json")))["slope"]["s_meas"]
Q = 3.0 if MUTB else 2.25
_xg = np.logspace(-7, 7, 20001); _fx = 1.0 / ((1 + _xg) * (1 + _xg ** 2) ** ((Q - 1) / 2))
_Ix = np.r_[0.0, np.cumsum(0.5 * (_fx[1:] * _xg[1:] ** 3 + _fx[:-1] * _xg[:-1] ** 3) * np.diff(np.log(_xg)))] + _fx[0] * _xg[0] ** 3 / 3
def GX_BK(X): return 4.0 * np.interp(np.log(np.maximum(np.asarray(X, float), 1e-7)), np.log(_xg), _Ix)
def GX_SOLVE(M, R, s):
    g = lambda lr: math.log(math.pi * s * math.exp(2 * lr) * float(GX_BK(R / math.exp(lr)))) - math.log(M)
    lo, hi = math.log(R * 1e-4), math.log(R * 1e4)
    pk = float(minimize_scalar(lambda lr: -g(lr), bounds=(lo, hi), method="bounded", options={"xatol": 1e-10}).x)
    return math.exp(pk) if g(pk) < 0 else math.exp(brentq(g, lo, pk, xtol=1e-12))
OLD = 'r0 = solve_r0(pp["Mfair"], pp["rta"], s); Mh = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)'
EDGE = {"v": None}
_edits0 = G1["edits"]
def edits_gx(*a, **k):
    ed, inj = _edits0(*a, **k)
    if EDGE["v"] is not None:
        ed.append((OLD, 'Redge = GX_EDGE * pp["rta"]; r0 = GX_SOLVE(pp["Mfair"], Redge, s); Mh = math.pi * s * r0 ** 2 * GX_BK(np.minimum(RM, Redge) / r0)'))
        inj.update(GX_EDGE=EDGE["v"], GX_SOLVE=GX_SOLVE, GX_BK=GX_BK)
    return ed, inj
G1["edits"] = edits_gx
P("\n================ GX1 Stage B (criteria 254f01d34a)" + ("  [MUTATE: q = 3]" if MUTB else "") + f"; GS1 R4 native, measured slope s = {S_MEAS:.3f}")
def grade(label, edge, tag):
    EDGE["v"] = edge
    _, r = G1["run"]("R4", True, True, shape="R5", tag=tag, slope=S_MEAS)
    out = {}
    for f in ("canonical", "alt"):
        ft = r["footings"][f]; cells = ft["clusters"]["cells"]
        out[f] = dict(fails=ft["clusters"]["fails"], groups_Z=ft["groups"]["Z"], groups_pass=ft["groups"]["PASS"],
                      sparc=[st["line"] for st in ft["sparc"].values()],
                      Z={k: [cells[hk][k]["Z"] for hk in ("h0672", "h0686")] for k in cells["h0672"]})
    c = out["canonical"]
    P(f"  {label:30s}: canonical fails {c['fails'] or 'none'}; groups Z {c['groups_Z']:+.2f}; worst |Z| {max(abs(z) for v in c['Z'].values() for z in v):.2f}"
      + f" | alt fails {out['alt']['fails'] or 'none'}")
    return out
RES = dict(criteria="254f01d34a", machinery="GS1 01f6dd977d (read-only, one halo-line edit)", mutate=MUTB, s_meas=S_MEAS, runs={})
RES["runs"]["step0_burkert"] = grade("STEP 0 Burkert (GS1 R4)", None, "gx1b_S0_burkert")
k0 = not RES["runs"]["step0_burkert"]["canonical"]["fails"] and not RES["runs"]["step0_burkert"]["alt"]["fails"]
P(f"  K0 GS1 R4 (all 15 keys pass, both footings) reproduced: {'PASS' if k0 else 'FAIL'}")
RES["runs"]["PRIMARY_rta"] = grade("PRIMARY infall, edge r_ta", 1.0, "gx1b_infall_rta" + TAGB)
RES["runs"]["V_splashback"] = grade("V infall, edge 0.364 r_ta", 0.364, "gx1b_infall_rsp" + TAGB)
RES["checks"] = dict(K0=bool(k0), K3=(Q == 2.25))
RES["stageB"] = {k: {f: (not v[f]["fails"]) for f in ("canonical", "alt")} for k, v in RES["runs"].items()}
P(f"=== STAGE B: " + "; ".join(f"{k}: canonical {'PASS' if v['canonical'] else 'FAIL'}, alt {'PASS' if v['alt'] else 'FAIL'}" for k, v in RES["stageB"].items()))
fn = os.path.join(HB, f"gx1_stage_b_results{TAGB}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(RES['checks'].values())}/{len(RES['checks'])}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
# the graded lines are printed to stdout (run log); GS1's P writes to its own file handle, so no separate .out is written here
sys.exit(0 if all(RES["checks"].values()) else 1)
