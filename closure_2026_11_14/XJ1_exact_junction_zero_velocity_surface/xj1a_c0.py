#!/usr/bin/env python3
"""XJ1 build A known answer (c0) and the matter-level reading (FROZEN_CRITERIA.md ef8ccdde98, sections 7 and 8). Built
from FWN2 build A's fwn2a_c0.py / FWN1's fwn1_c0.py (closure_2026_11_14/FWN2_forest_flux_split_f4,
closure_2026_11_13/FWN1_forest_flux_split_f_ceiling).
  table route: this build's tables (xj1a_tables.py, SRH1's prefix) R_cold of each key, interpolated in log k onto FRZ1's
               forest k grid, fed to FRZ1's forest_eval through Rkz_z (JNT2's jnt2_forest.py route: frz1_forest.py prefix,
               executed read-only from its own path).
  chain:       JNT2's jnt2_hm.py executed read-only up to its case loop (FZS1's library, not SRH1's): S5.00 through its own
               ratios_J(foot, z, 5); SE2 / SEzv through a direct halo-model evaluation in ratios_J's style (U_std, U_set,
               spectra_ta on FZS1's namespace) with this build's exact-junction layout (xj1a_tables.lay_E on FZS1's
               namespace, JNT2's above()); graded by the same forest route.
  anchor:      the chain's ratios_J at fac 3 must equal JNT2's stored G1 f3.00 (1.9898 canonical / 6.4321 alt) within 1 %.
Pass: table route = chain within 1 % or 0.002 absolute, and the anchor passes. The matter-level D_rec of SE2 and SEzv is
reported with PASS / FAIL against the gate 4 (reported, never a label).
Usage: nice -n 19 python3 -I -B xj1a_c0.py <footing> -> xj1a_c0_<footing>.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib, warnings, time
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
sys.path.insert(0, HERE); import xj1a_tables as TB
JD = os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint")
T0 = time.time()
# JNT2's halo-model prefix (up to the case loop)
SRC = os.path.join(JD, "jnt2_hm.py"); code = open(SRC).read()
cut = code.index('P(f"JNT2 G1 halo model, mode {MODE}')
J = {"__file__": SRC, "__name__": "jnt2_hm_prefix_xj1a"}; _a = sys.argv; sys.argv = ["jnt2_hm.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), J)
sys.argv = _a
assert J["MODE"] == "main"
Z = J["Z"]; L = J["L"]
# FRZ1's forest prefix, as jnt2_forest.py runs it
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRC2 = os.path.join(FRZ, "frz1_forest.py"); code2 = open(SRC2).read()
cut2 = code2.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC2, "__name__": "frz1_forest_lib_xj1a"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code2[:cut2], SRC2, "exec"), N)
forest_eval, Rkz_z, FD, BGB, KH = (N[k] for k in ("forest_eval", "Rkz_z", "FD", "BGB", "KH"))
JST = json.load(open(os.path.join(JD, f"jnt2_forest_{FOOT}.json")))["cases"]
assert np.allclose(np.asarray(L["KK"]), KH, rtol=1e-12, atol=0)          # the chain's R_cold grid is the forest route's

def ratios_E(foot, z, which):
    """ratios_J's evaluation (JNT2, copied in form) with the exact-junction split layout in place of lay_J."""
    Z["CUR"][0] = 0.0; layout = Z["layout"]
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    US, inf = L["U_set"](TB.lay_E(Z, foot, z, which, lambda hb: J["above"](hb, foot))); PS, _, _ = L["spectra_ta"](US)
    Rtot = 1 + (PS - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    return Rtot, Rbar, Rtot / Rbar, inf

RES = dict(lane="XJ1", build="A", part="known answer c0 and matter-level D_rec (record convention)", footing=FOOT, cases={},
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
TAB = {round(z, 1): TB.tables(z)[FOOT] for z in J["ZB"]}
def table_route(key):
    Rz = {}
    for z in J["ZB"]:
        R = TAB[round(z, 1)]["spec"][key]["Rcold"]
        Rz[str(z)] = np.interp(np.log(KH), np.log(TB.KT[1:]), R[1:]).tolist()
    return float(forest_eval(FD, BGB, Rkz_z(Rz))["dchi2"])
# anchor: the chain at FZS1's junction, fac 3
Rz = {}
for z in J["ZB"]:
    J["setz"](z); Rz[str(z)] = J["ratios_J"](FOOT, z, 3.0)[2].tolist()
anchor = float(forest_eval(FD, BGB, Rkz_z(Rz))["dchi2"]); anc_rel = anchor / JST["f3.00"]["dchi2"] - 1
RES["anchor_J_fac3"] = dict(chain=anchor, jnt2_stored=JST["f3.00"]["dchi2"], rel=anc_rel, pass_=bool(abs(anc_rel) <= 0.01))
P(f"[{FOOT}] anchor: chain at FZS1's junction fac 3 D_rec {anchor:.6g} vs JNT2's stored f3.00 {JST['f3.00']['dchi2']:.6g}: rel {anc_rel:.2e} -> {'PASS' if abs(anc_rel) <= 0.01 else 'FAIL'}  [{time.time() - T0:.0f} s]")
for key in ("S5.00", "SE2", "SEzv"):
    Rz = {}; tinfo = {}
    for z in J["ZB"]:
        J["setz"](z)
        if key == "S5.00": Rt, Rb, Rc, inf = J["ratios_J"](FOOT, z, 5.0)
        else:
            Rt, Rb, Rc, inf = ratios_E(FOOT, z, TB.EWHICH[key])
            ts = [i["t"] for i in inf if i.get("t") is not None]; tinfo[str(z)] = [min(ts), max(ts)] if ts else None
        Rz[str(z)] = Rc.tolist()
    ch = float(forest_eval(FD, BGB, Rkz_z(Rz))["dchi2"]); mine = table_route(key)
    ok = bool(RES["anchor_J_fac3"]["pass_"] and (abs(mine / ch - 1) <= 0.01 or abs(mine - ch) <= 0.002))
    RES["cases"][key] = dict(D_rec_tables=mine, D_rec_chain=ch, rel=mine / ch - 1, abs=mine - ch, pass_=ok, t_min_max_chain=tinfo or None,
                             gate4="PASS" if mine <= 4 else "FAIL")
    P(f"[{FOOT}] {key:5}: D_rec tables route {mine:.6g}, chain {ch:.6g} (rel {mine / ch - 1:.2e}) -> (c0) {'PASS' if ok else 'FAIL'}; "
      f"matter level against the gate 4 (reported, not a label): {'PASS' if mine <= 4 else 'FAIL'}  [{time.time() - T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"xj1a_c0_{FOOT}.json"), "w"), indent=1)
open(os.path.join(HERE, f"xj1a_c0_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
