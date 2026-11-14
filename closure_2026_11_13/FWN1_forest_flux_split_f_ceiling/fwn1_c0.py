#!/usr/bin/env python3
"""FWN1 known answer (c0), the independent chain (FROZEN_CRITERIA.md fab8a8ee0e, section 5): JNT2's jnt2_hm.py
(closure_2026_11_13/JNT2_crossing_speed_joint) executed read-only from its own path up to its case loop (FZS1's library,
not SRH1's), its ratios_J(foot, z, fac) at fac = 3, 5, 10, inf over FRZ1's twelve z bins, graded by JNT2's jnt2_forest.py
route (FRZ1's frz1_forest.py prefix executed read-only; Rkz_z, forest_eval). Nothing is written outside this folder.
Usage: nice -n 19 python3 -I -B fwn1_c0.py <footing> -> fwn1_c0_<footing>.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib, warnings, time
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
JD = os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint")
T0 = time.time()
# JNT2's halo-model prefix (up to the case loop)
SRC = os.path.join(JD, "jnt2_hm.py"); code = open(SRC).read()
cut = code.index('P(f"JNT2 G1 halo model, mode {MODE}')
J = {"__file__": SRC, "__name__": "jnt2_hm_prefix_fwn1"}; _a = sys.argv; sys.argv = ["jnt2_hm.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), J)
sys.argv = _a
assert J["MODE"] == "main"
# FRZ1's forest prefix, as jnt2_forest.py runs it
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRC2 = os.path.join(FRZ, "frz1_forest.py"); code2 = open(SRC2).read()
cut2 = code2.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC2, "__name__": "frz1_forest_lib_fwn1"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code2[:cut2], SRC2, "exec"), N)
forest_eval, Rkz_z, FD, BGB = (N[k] for k in ("forest_eval", "Rkz_z", "FD", "BGB"))
JST = json.load(open(os.path.join(JD, f"jnt2_forest_{FOOT}.json")))["cases"]
RES = dict(lane="FWN1", part="known answer c0, JNT2 chain", footing=FOOT, cases={}, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT = []
for name, fac in (("S3.00", 3.0), ("S5.00", 5.0), ("S10.00", 10.0), ("Sinf", math.inf)):
    Rz = {}; nref = {}
    for z in J["ZB"]:
        J["setz"](z); Rt, Rb, Rc, inf = J["ratios_J"](FOOT, z, fac); Rz[str(z)] = Rc.tolist()
        nref[str(z)] = sum(1 for i in inf if i.get("split_ref"))
    r_ = forest_eval(FD, BGB, Rkz_z(Rz))
    RES["cases"][name] = dict(dchi2=float(r_["dchi2"]), n_reference=nref)
    s = f"[{FOOT}] JNT2 chain {name}: D_rec {r_['dchi2']:.6g}; reference haloes z 2.2 {nref['2.2']}  [{time.time() - T0:.0f} s]"
    print(s, flush=True); OUT.append(s)
RES["jnt2_stored_f3.00"] = JST["f3.00"]["dchi2"]
RES["chain_vs_jnt2_f3"] = RES["cases"]["S3.00"]["dchi2"] / JST["f3.00"]["dchi2"] - 1
OUT.append(f"[{FOOT}] chain S3.00 vs JNT2's stored f3.00 {JST['f3.00']['dchi2']:.6g}: rel {RES['chain_vs_jnt2_f3']:.2e}")
print(OUT[-1])
json.dump(RES, open(os.path.join(HERE, f"fwn1_c0_{FOOT}.json"), "w"), indent=1)
open(os.path.join(HERE, f"fwn1_c0_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
