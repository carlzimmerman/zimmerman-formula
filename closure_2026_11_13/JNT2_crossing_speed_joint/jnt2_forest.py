#!/usr/bin/env python3
"""JNT2 (FROZEN_CRITERIA.md, e186b314ef): G1 forest gate at matter level. SRJ2's srj2_forest.py content copied (cited): FRZ1's
frz1_forest.py is executed unchanged from its own path (read-only) up to the line that reads frz1_hm.json, then fed with
jnt2_hm[_MUTATE_<mode>].json. Every case of the mode is evaluated (Delta chi^2 <= 4).
  JNT2_FOOT=canonical|alt python3 jnt2_forest.py [--mode main|S|0|H|D] -> jnt2_forest_<foot>[_MUTATE_<mode>].json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
FOOT = os.environ.get("JNT2_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
MODE = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "main"; assert MODE in ("main", "S", "0", "H", "D")
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRC = os.path.join(FRZ, "frz1_forest.py"); code = open(SRC).read()
cut = code.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC, "__name__": "frz1_forest_lib"}
exec(compile(code[:cut], SRC, "exec"), N)
forest_eval, Rkz_z, perz, FD, BGB = (N[k] for k in ("forest_eval", "Rkz_z", "perz", "FD", "BGB"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
tag = "" if MODE == "main" else f"_MUTATE_{MODE}"
HM = json.load(open(os.path.join(HERE, f"jnt2_hm{tag}.json")))
RES = dict(lane="JNT2", part="G1 forest gate", mode=MODE, footing=FOOT, criteria="e186b314ef",
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", cases={})
for key in HM["cases"]:
    name, ft = key.split("|")
    if ft != FOOT: continue
    rows = HM["cases"][key]; Rz = {z: v["R_cold"] for z, v in rows.items()}; RZ = Rkz_z(Rz); r_ = forest_eval(FD, BGB, RZ)
    RES["cases"][name] = dict(dchi2=r_["dchi2"], r_min=r_["r_min"], r_max=r_["r_max"], status=r_["status"], per_z=perz(RZ),
                              n_reference={z: v["n_reference"] for z, v in rows.items()})
    P(f"[{FOOT}] {MODE} {name:6s}: dchi2 {r_['dchi2']:10.4f} (1D ratio {r_['r_min']:.5f}-{r_['r_max']:.5f}) -> {'PASS' if r_['dchi2'] <= 4 else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, f"jnt2_forest_{FOOT}{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"jnt2_forest_{FOOT}{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
