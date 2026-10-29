#!/usr/bin/env python3
"""GX2_infall_corrected_gas: GX1 Stage B (GS1 harness, R4, native, s_meas) with eRASS1 Mgas500 raised by SM1's matched +0.111 dex.
Frozen criteria c6783290b3. Built from GX1 Stage B (9319e09bc2). Machinery: GS1's committed script (01f6dd977d) executed read-only up to its measurement section; one extra
source edit swaps X43's cluster halo line (Burkert, edge r_ta) for the infall profile (edge r_ta PRIMARY; 0.364 r_ta variant).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gx2_corrected_gas.py      (GX2_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib
import numpy as np
from scipy.optimize import brentq, minimize_scalar
MUTB = os.environ.get("GX2_MUTATE", "0") == "1"; TAGB = "_MUTATE" if MUTB else ""
HB = os.path.dirname(os.path.abspath(__file__)); RB_ = os.path.dirname(HB); REPO_ = os.path.dirname(RB_)
GSP = os.path.join(RB_, "GS1_measured_gas_outskirts", "gs1_gas_slope.py")
src = open(GSP).read(); src = src[:src.index("# ============================================================== A. measurement")]
os.environ.pop("MUTATE", None); os.environ.pop("GS1_MUTATE", None)
G1 = {"__file__": os.path.join(HB, "gs1_ro.py"), "__name__": "gs1_ro"}
exec(compile(src, GSP, "exec"), G1)
P = G1["P"]
S_MEAS = json.load(open(os.path.join(RB_, "GS1_measured_gas_outskirts", "gs1_gas_slope_results.json")))["slope"]["s_meas"]
Q = 2.25
FAC0 = 10 ** 0.111; FAC = {"v": 1.0}
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
    if FAC["v"] != 1.0:
        k, new = ed[-1]; assert k.startswith("NX = {")
        app = ('\nassert codeX.count(\'Mg500 = cl["Mgas500"]*qd**2.5;\') == 1'
               '\ncodeX = codeX.replace(\'Mg500 = cl["Mgas500"]*qd**2.5;\', \'Mg500 = cl["Mgas500"]*qd**2.5*%r;\')' % FAC["v"])
        ed[-1] = (k, new + app)
    if EDGE["v"] is not None:
        ed.append((OLD, 'Redge = GX_EDGE * pp["rta"]; r0 = GX_SOLVE(pp["Mfair"], Redge, s); Mh = math.pi * s * r0 ** 2 * GX_BK(np.minimum(RM, Redge) / r0)'))
        inj.update(GX_EDGE=EDGE["v"], GX_SOLVE=GX_SOLVE, GX_BK=GX_BK)
    return ed, inj
G1["edits"] = edits_gx
P("\n================ GX2 corrected gas (criteria c6783290b3)" + ("  [MUTATE: factor applied twice]" if MUTB else "") + f"; GS1 R4 native, measured slope s = {S_MEAS:.3f}")
def grade(label, edge, tag, fac=1.0):
    EDGE["v"] = edge; FAC["v"] = fac
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
RES = dict(criteria="c6783290b3", machinery="GX1 Stage B / GS1 01f6dd977d (read-only + halo and gas-factor edits)", mutate=MUTB, s_meas=S_MEAS, runs={})
RES["runs"]["step0_burkert_nocorr"] = grade("STEP 0 Burkert, no correction", None, "gx2_S0")
k0 = not RES["runs"]["step0_burkert_nocorr"]["canonical"]["fails"] and not RES["runs"]["step0_burkert_nocorr"]["alt"]["fails"]
F = FAC0 ** 2 if MUTB else FAC0
RES["runs"]["PRIMARY_infall_rsp"] = grade("PRIMARY infall 0.364 r_ta, gas +0.111", 0.364, "gx2_rsp" + TAGB, F)
RES["runs"]["V1_infall_rta"] = grade("V1 infall r_ta, gas +0.111", 1.0, "gx2_rta" + TAGB, F)
RES["runs"]["V2_burkert"] = grade("V2 Burkert r_ta, gas +0.111", None, "gx2_bur" + TAGB, F)
SIG = float(np.std([r['dlogMgas500'] for r in json.load(open(os.path.join(RB_, 'SM1_cluster_sample_match', 'sm1_cluster_sample_match_results.json')))['matched']]))   # std of SM1's five offsets
RES["runs"]["PRIMARY_minus1sig"] = grade("PRIMARY, gas +0.111 - 1 sigma", 0.364, "gx2_rsp_m" + TAGB, 10 ** (0.111 - SIG))
RES["runs"]["PRIMARY_plus1sig"] = grade("PRIMARY, gas +0.111 + 1 sigma", 0.364, "gx2_rsp_p" + TAGB, 10 ** (0.111 + SIG))
RES["checks"] = dict(K0=bool(k0), K1=abs(F / 10 ** 0.111 - 1) < 1e-12)
RES["verdict"] = {f: ("INFALL HALO + CORRECTED GAS PASSES CLUSTERS" if not RES["runs"]["PRIMARY_infall_rsp"][f]["fails"]
                      else "LENSING STILL FAILS: " + ", ".join(RES["runs"]["PRIMARY_infall_rsp"][f]["fails"])) for f in ("canonical", "alt")}
P(f"  K0 GS1 R4 reproduced: {'PASS' if k0 else 'FAIL'}; K1 factor 10^0.111: {'PASS' if RES['checks']['K1'] else 'FAIL'}")
P(f"=== VERDICT: canonical {RES['verdict']['canonical']}; alt {RES['verdict']['alt']}")
fn = os.path.join(HB, f"gx2_corrected_gas_results{TAGB}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(RES['checks'].values())}/{len(RES['checks'])}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
# the graded lines are printed to stdout (run log); GS1's P writes to its own file handle, so no separate .out is written here
sys.exit(0 if all(RES["checks"].values()) else 1)
