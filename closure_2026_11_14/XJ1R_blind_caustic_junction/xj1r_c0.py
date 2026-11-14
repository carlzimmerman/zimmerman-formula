#!/usr/bin/env python3
"""XJ1R known answer (c0), the independent chain (FROZEN_CRITERIA.md section 5): a copy of FWN1's fwn1_c0.py route. JNT2's
jnt2_hm.py (closure_2026_11_13/JNT2_crossing_speed_joint) executed read-only from its own path up to its case loop (FZS1's
library, not SRH1's); on that namespace the exact junction is written a second time (not imported from xj1r_tables) with
R_set = R_k from xj1r_rk.rk_kpc, FZS1's Mb_fold, x 1e-3 (1 + z) h, capped at r_ta; JNT2's own above() is the boundary.
D_rec of SEc2, SEc3 (this chain) and of S5.00 (JNT2's ratios_J at fac 5, which must equal FWN1's stored c0 S5.00) over
FRZ1's twelve z bins, graded by FRZ1's frz1_forest.py route (prefix executed read-only; Rkz_z, forest_eval). This is also
the record's older matter-level number for the two cases (reported, never a label). Nothing is written outside this folder.
Usage: nice -n 19 python3 -I -B xj1r_c0.py <footing> -> xj1r_c0_<footing>.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib, warnings, time
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
sys.path.insert(0, HERE); import xj1r_rk as RK
JD = os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint")
FWN1 = os.path.join(REPO, "closure_2026_11_13", "FWN1_forest_flux_split_f_ceiling")
T0 = time.time()
SRC = os.path.join(JD, "jnt2_hm.py"); code = open(SRC).read()
cut = code.index('P(f"JNT2 G1 halo model, mode {MODE}')
J = {"__file__": SRC, "__name__": "jnt2_hm_prefix_xj1r"}; _a = sys.argv; sys.argv = ["jnt2_hm.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), J)
sys.argv = _a
assert J["MODE"] == "main"
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRC2 = os.path.join(FRZ, "frz1_forest.py"); code2 = open(SRC2).read()
cut2 = code2.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC2, "__name__": "frz1_forest_lib_xj1r"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code2[:cut2], SRC2, "exec"), N)
forest_eval, Rkz_z, FD, BGB = (N[k] for k in ("forest_eval", "Rkz_z", "FD", "BGB"))
Z = J["Z"]; L = J["L"]; layout, Bar, CUR = J["layout"], J["Bar"], J["CUR"]


def lay_Xc(foot, z, k, tl):
    """second writing of the exact junction on FZS1's library (criteria section 2)."""
    def fn(hb):
        if J["above"](hb, foot):
            CUR[0] = 0.0; rR, MR, inf = layout(hb, foot, mode="Rb"); return rR, MR, dict(inf, split_ref=True)
        h = Z["h"]; R = min(RK.rk_kpc(foot, z, math.log10(Z["Mb_fold"](hb, foot) / h), k) * 1e-3 * (1 + z) * h, hb["rta"])
        CUR[0] = R if R > 0 else 0.0
        rB, MB, inf = layout(hb, foot, mode="B"); rR, MR, _ = layout(hb, foot, mode="Rb"); CUR[0] = 0.0
        if R <= 0 or inf["regime"] == "L": return rR, MR, inf
        if R >= rB[-1]: return rB, MB, inf
        bar = Bar(hb, foot, rB); j = int(np.flatnonzero(np.isclose(rB, R, rtol=1e-12, atol=0))[0])
        cb, cr, ctot = MB[j] - bar[j], MR[j] - bar[j], MR[-1] - bar[-1]; t = (ctot - cb) / (ctot - cr); tl.append(t)
        out = MB.copy(); o = np.arange(len(rB)) > j
        out[o] = bar[o] + cb + t * ((MR[o] - bar[o]) - cr)
        return rB, out, inf
    return fn


def ratios_X(foot, z, k, tl):
    CUR[0] = 0.0
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    US, inf = L["U_set"](lay_Xc(foot, z, k, tl)); PS, _, _ = L["spectra_ta"](US)
    Rtot = 1 + (PS - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    return Rtot, Rbar, Rtot / Rbar, inf


RES = dict(lane="XJ1R", part="known answer c0, independent chain", footing=FOOT, cases={}, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT = []
for name, k in (("S5.00", None), ("SEc2", 2), ("SEc3", 3)):
    Rz = {}; tz = {}
    for z in J["ZB"]:
        J["setz"](z)
        if k is None: Rt, Rb, Rc, inf = J["ratios_J"](FOOT, z, 5.0)
        else:
            tl = []; Rt, Rb, Rc, inf = ratios_X(FOOT, z, k, tl); tz[str(z)] = [float(min(tl)), float(np.median(tl)), float(max(tl))] if tl else None
        Rz[str(z)] = Rc.tolist()
    r_ = forest_eval(FD, BGB, Rkz_z(Rz))
    RES["cases"][name] = dict(dchi2=float(r_["dchi2"]), t_min_median_max_by_z=tz)
    s = f"[{FOOT}] chain {name}: D_rec {r_['dchi2']:.6g}  [{time.time() - T0:.0f} s]"; print(s, flush=True); OUT.append(s)
ST = json.load(open(os.path.join(FWN1, f"fwn1_c0_{FOOT}.json")))["cases"]["S5.00"]["dchi2"]
RES["fwn1_stored_c0_S5.00"] = ST; RES["chain_S5_vs_fwn1_rel"] = RES["cases"]["S5.00"]["dchi2"] / ST - 1
OUT.append(f"[{FOOT}] chain S5.00 vs FWN1's stored c0 S5.00 {ST:.10g}: rel {RES['chain_S5_vs_fwn1_rel']:.2e}"); print(OUT[-1])
json.dump(RES, open(os.path.join(HERE, f"xj1r_c0_{FOOT}.json"), "w"), indent=1)
open(os.path.join(HERE, f"xj1r_c0_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
