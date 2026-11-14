#!/usr/bin/env python3
"""XJ1 AMENDMENT_A3 cases E0.5 and E0.75 (a copy of xj1_matter.py with the case list changed; outputs xj1_matter2_*). XJ1 (FROZEN_CRITERIA.md ef8ccdde98, section 7, first item): the matter-level number in the record's convention for the
exact-junction cases, through JNT2's G1 route. Reported beside the flux-level labels, never a label of this lane.
JNT2's ratios_J (closure_2026_11_13/JNT2_crossing_speed_joint/jnt2_hm.py) is copied with the layout function as an
argument; FRZ1's frz1_forest.py is executed read-only up to the line that reads frz1_hm.json, as JNT2's jnt2_forest.py
does. Anchor (must reproduce, or nothing here is quoted): FZS1's junction at f = 2 and 3 through this script equals
JNT2's stored values (0.0492 / 0.1456 and 1.9898 / 6.4321) within 1 %.
  XJ1_FOOT=canonical|alt python3 -I -B xj1_matter.py -> xj1_matter_<foot>.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
FOOT = os.environ.get("XJ1_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import xj1_lib as XL
X = XL.X; REPO = X.REPO
Z = X.rec(); F, L = Z["F"], Z["L"]; layout, set_z, CUR, KK, ZB = Z["layout"], Z["set_z"], Z["CUR"], Z["KK"], Z["ZB"]
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRC = os.path.join(FRZ, "frz1_forest.py"); code = open(SRC).read()
cut = code.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC, "__name__": "frz1_forest_lib"}
exec(compile(code[:cut], SRC, "exec"), N)
forest_eval, Rkz_z, perz, FD, BGB = (N[k] for k in ("forest_eval", "Rkz_z", "perz", "FD", "BGB"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
def ratios(fn):
    """JNT2's ratios_J with the layout function as an argument."""
    CUR[0] = 0.0
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, FOOT, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UR, _ = L["U_set"](lambda hb: layout(hb, FOOT, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    US, inf = L["U_set"](fn); PS, _, _ = L["spectra_ta"](US); CUR[0] = 0.0
    Rtot = 1 + (PS - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    return Rtot / Rbar
CASES = {"J2": lambda z, vs: X.split_fn(FOOT, z, 2.0, vs), "J3": lambda z, vs: X.split_fn(FOOT, z, 3.0, vs),
         "E0.5": lambda z, vs: XL.exact_fn(FOOT, z, vs, XL.COL_FOLD, 0.5), "E0.75": lambda z, vs: XL.exact_fn(FOOT, z, vs, XL.COL_FOLD, 0.75)}
STORED = {"canonical": {"J2": 0.0492, "J3": 1.9898}, "alt": {"J2": 0.1456, "J3": 6.4321}}[FOOT]
RES = dict(lane="XJ1", part="matter level, record convention (reported)", footing=FOOT, criteria="ef8ccdde98", gate=4.0,
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", cases={})
P(f"XJ1 matter level, record convention, footing {FOOT}. Reported, not a label.")
for name, mk in CASES.items():
    Rz = {}
    for z in ZB:
        set_z(z); vs = X.vstar(FOOT, z); Rz[str(z)] = ratios(mk(z, vs)).tolist()
    RZ = Rkz_z(Rz); r_ = forest_eval(FD, BGB, RZ)
    at = lambda zz: [float(np.interp(k, KK, Rz[zz])) for k in (1.0, 3.0, 5.0, 10.0)]
    RES["cases"][name] = dict(dchi2=r_["dchi2"], r_min=r_["r_min"], r_max=r_["r_max"], per_z=perz(RZ), R_cold_at_k1_3_5_10={zz: at(zz) for zz in ("2.2", "3.0", "4.4")},
                              word="PASS" if r_["dchi2"] <= 4 else "FAIL")
    extra = ""
    if name in STORED:
        rel = r_["dchi2"] / STORED[name] - 1; RES["cases"][name].update(JNT2_stored=STORED[name], rel=rel, anchor_ok=bool(abs(rel) <= 0.01))
        extra = f"   anchor against JNT2's stored {STORED[name]}: rel {rel:+.2e} -> {'PASS' if abs(rel) <= 0.01 else 'FAIL'}"
    P(f"[{FOOT}] {name:5s}: Delta chi^2 {r_['dchi2']:10.4f} (1D ratio {r_['r_min']:.5f}-{r_['r_max']:.5f}) -> {'PASS' if r_['dchi2'] <= 4 else 'FAIL'} against the gate 4; R_cold at k 1/3/5/10, z 2.2: "
      + "/".join(f"{x:.5f}" for x in at("2.2")) + "; z 4.4: " + "/".join(f"{x:.5f}" for x in at("4.4")) + extra + f"   [{time.time() - T0:.0f} s]")
RES["anchor_ok"] = bool(all(RES["cases"][k]["anchor_ok"] for k in STORED))
P(f"[{FOOT}] anchor (FZS1's junction at f 2 and 3 reproduces JNT2's stored values within 1 %): {'PASS' if RES['anchor_ok'] else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, f"xj1_matter2_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"xj1_matter2_{FOOT}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
