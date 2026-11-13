#!/usr/bin/env python3
"""JNT2 (FROZEN_CRITERIA.md, e186b314ef): G1 halo-model part. SRJ2's srj2_hm.py content copied (cited), with the boundary
replaced: a halo keeps the reference layout (FRZ1 mode "Rb") at every radius when FRZ1's v_vir(hb) (its v200c, the lemma's
convention with M = M200c) exceeds v*(z) of the mode; otherwise FZS1's settled layout at R_set = f R_fold.
FZS1's fzs1_hm.py is executed read-only from its own path up to its "checkpointed run" marker.
  python3 jnt2_hm.py [--mode main|S|0|H|D] -> jnt2_hm.json (main) or jnt2_hm_MUTATE_<mode>.json
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2_common as C
MODE = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "main"; assert MODE in C.MODES
FZD = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
SRC = os.path.join(FZD, "fzs1_hm.py"); code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
Z = {"__file__": SRC, "__name__": "fzs1_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), Z)
F, L = Z["F"], Z["L"]; layout, set_z, Bar, rset_com, CUR = (Z[k] for k in ("layout", "set_z", "Bar", "rset_com", "CUR"))
KK, ZB, FOOTS, VST, at = Z["KK"], Z["ZB"], Z["FOOTS"], Z["VST"], Z["at"]
assert VST == C.VSTIFF
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
ZNOW = [0.0]
def above(hb, foot):
    return F["v_vir"](hb) > C.vstar_kms(foot, ZNOW[0], MODE)
def setz(z): ZNOW[0] = z; set_z(z)

# the split layout (SRJ2's lay_J, copied; the switch is the JNT2 boundary)
def lay_J(foot, z, fac=1.0):
    def fn(hb):
        if above(hb, foot):
            CUR[0] = 0.0; rR, MR, inf = layout(hb, foot, mode="Rb"); return rR, MR, dict(inf, R_set=0.0, split_ref=True)
        R = rset_com(hb, foot, z, fac); CUR[0] = R
        rB, MB, inf = layout(hb, foot, mode="B"); rR, MR, _ = layout(hb, foot, mode="Rb"); CUR[0] = 0.0
        if R <= 0 or inf["regime"] == "L": return rR, MR, dict(inf, R_set=R)
        assert len(rB) == len(rR) and np.array_equal(rB, rR)
        bar = Bar(hb, foot, rB); CB, CR = MB - bar, MR - bar
        i = int(np.argmin(abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
        s = CR[i] / CB[i]
        return rB, np.where(rB <= rB[i], bar + s * CB, bar + CR), dict(inf, R_set=R, s=float(s))
    return fn
def ratios_J(foot, z, fac=1.0):
    CUR[0] = 0.0
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    US, inf = L["U_set"](lay_J(foot, z, fac)); PS, _, _ = L["spectra_ta"](US)
    Rtot = 1 + (PS - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    return Rtot, Rbar, Rtot / Rbar, inf

P(f"JNT2 G1 halo model, mode {MODE}. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
CASES = {"main": [("KA_0", 0.0)] + [(f"f{f:.2f}", f) for f in (0.75, 1.0, 1.25, 1.5, 2.0, 3.0)],
         "S": [("f1.00", 1.0)], "0": [("f1.00", 1.0)], "H": [("f1.25", 1.25), ("f2.00", 2.0)], "D": [("f1.25", 1.25), ("f2.00", 2.0)]}[MODE]
RES = dict(lane="JNT2", part="G1 halo model", mode=MODE, criteria="e186b314ef", cases={}, membership={})
# membership of the forest grid (per z bin): haloes above the boundary and the lightest such M200c
for ft in FOOTS:
    m = {}
    for z in ZB:
        setz(z); ab = [hb for hb in L["HB"] if above(hb, ft)]
        m[str(z)] = dict(vstar=C.vstar_kms(ft, z, MODE), n_above=len(ab), n=len(L["HB"]),
                         lightest_above_M200c=(min(hb["M200c"] for hb in ab) if ab else None),
                         check_vh_vs_vvir=max(abs(C.vh_kms(hb["M200c"] / F["h"], z) / F["v_vir"](hb) - 1) for hb in L["HB"][::40]))
    RES["membership"][ft] = m
    P(f"[{ft}] forest grid above v*(z) ({MODE}): " + "; ".join(f"z {z}: {m[str(z)]['n_above']}/{m[str(z)]['n']} (v* {m[str(z)]['vstar']:.0f}, lightest M200c {m[str(z)]['lightest_above_M200c'] or float('nan'):.2e} Msun/h)" for z in (ZB[0], ZB[4], ZB[-1]))
      + f"; |v_lemma / v_vir - 1| max {max(v['check_vh_vs_vvir'] for v in m.values()):.1e}")
for name, fac in CASES:
    for ft in FOOTS:
        rows = {}
        for z in ZB:
            setz(z); Rt, Rb, Rc, inf = ratios_J(ft, z, fac)
            ss = [i.get("s") for i in inf if i.get("s") is not None]
            rows[str(z)] = dict(R_cold=Rc.tolist(), R_cold_at=at(Rc), s_min_max=[min(ss), max(ss)] if ss else None,
                                n_reference=sum(1 for i in inf if i.get("split_ref")), n_haloes=len(inf))
        RES["cases"][f"{name}|{ft}"] = rows
        P(f"  {name:6s} {ft:9s} R_cold at k 1/3/5/10: z 2.2 " + "/".join(f"{x:.5f}" for x in rows["2.2"]["R_cold_at"]) + "; z 4.4 "
          + "/".join(f"{x:.5f}" for x in rows["4.4"]["R_cold_at"]) + f"; reference haloes z 2.2 / 4.4: {rows['2.2']['n_reference']} / {rows['4.4']['n_reference']} of {rows['2.2']['n_haloes']}   [{time.time() - T0:.0f} s]")
RES.update(k=KK.tolist(), z_bins=ZB, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
tag = "" if MODE == "main" else f"_MUTATE_{MODE}"
json.dump(RES, open(os.path.join(HERE, f"jnt2_hm{tag}.json"), "w"), indent=1)
open(os.path.join(HERE, f"jnt2_hm{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
P(f"done ({time.time() - T0:.0f} s)")
