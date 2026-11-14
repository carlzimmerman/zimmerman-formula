#!/usr/bin/env python3
"""BJ1 (FROZEN_CRITERIA.md 9e7ce0dfe6, section 2, G-F at matter level): a copy of XJ1's xj1_matter.py
(closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface) with the case list changed to the budget junction at the
first, second and third caustic (B1, B2, B3, through bj1_lib) and the outputs renamed. XJ1's docstring follows, its
anchor kept (known answer ix). XJ1: the matter-level number in the record's convention for the
exact-junction cases, through JNT2's G1 route. Reported beside the flux-level labels, never a label of this lane.
JNT2's ratios_J (closure_2026_11_13/JNT2_crossing_speed_joint/jnt2_hm.py) is copied with the layout function as an
argument; FRZ1's frz1_forest.py is executed read-only up to the line that reads frz1_hm.json, as JNT2's jnt2_forest.py
does. Anchor (must reproduce, or nothing here is quoted): FZS1's junction at f = 2 and 3 through this script equals
JNT2's stored values (0.0492 / 0.1456 and 1.9898 / 6.4321) within 1 %.
  BJ1_FOOT=canonical|alt nice -n 19 python3 -I -B bj1_matter.py -> bj1_matter_<foot>.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
FOOT = os.environ.get("BJ1_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bj1_lib as BL
BL.install()
X = BL.X; REPO = X.REPO
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
         "B1": lambda z, vs: BL.budget_fn(FOOT, z, vs, 1), "B2": lambda z, vs: BL.budget_fn(FOOT, z, vs, 2), "B3": lambda z, vs: BL.budget_fn(FOOT, z, vs, 3)}
STORED = {"canonical": {"J2": 0.0492, "J3": 1.9898}, "alt": {"J2": 0.1456, "J3": 6.4321}}[FOOT]
RES = dict(lane="BJ1", part="G-F at matter level (JNT2's G1 route, gate 4)", footing=FOOT, criteria="9e7ce0dfe6", gate=4.0,
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.", cases={})
P(f"BJ1 G-F at matter level (JNT2's G1 route, gate 4), footing {FOOT}.")
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
    P(f"[{FOOT}] {name:4s}: Delta chi^2 {r_['dchi2']:10.4f} (1D ratio {r_['r_min']:.5f}-{r_['r_max']:.5f}) -> {'PASS' if r_['dchi2'] <= 4 else 'FAIL'} against the gate 4; R_cold at k 1/3/5/10, z 2.2: "
      + "/".join(f"{x:.5f}" for x in at("2.2")) + "; z 4.4: " + "/".join(f"{x:.5f}" for x in at("4.4")) + extra + f"   [{time.time() - T0:.0f} s]")
RES["anchor_ok"] = bool(all(RES["cases"][k]["anchor_ok"] for k in STORED))
P(f"[{FOOT}] anchor (FZS1's junction at f 2 and 3 reproduces JNT2's stored values within 1 %): {'PASS' if RES['anchor_ok'] else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, f"bj1_matter_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"bj1_matter_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
