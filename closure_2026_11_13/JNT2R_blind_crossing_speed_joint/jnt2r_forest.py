#!/usr/bin/env python3
"""JNT2R (READING.md, 5abea0324b): G1 forest gate at matter level (Delta chi^2 <= 4), SRJ2's / FZS1's machinery fed with
jnt2r_hm.json. FRZ1's frz1_forest.py is executed unchanged, from its own path (read-only), up to the line that reads
frz1_hm.json.
  JNT2R_FOOT=canonical|alt python3 jnt2r_forest.py              -> jnt2r_forest_<foot>.json / .out (f 0, primary and B-halo grid)
  JNT2R_FOOT=canonical|alt python3 jnt2r_forest.py --twin V|N|H|D -> jnt2r_forest_<foot>_MUTATE_<T>.json / .out (exits 1)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
FOOT = os.environ.get("JNT2R_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
TWIN = sys.argv[sys.argv.index("--twin") + 1] if "--twin" in sys.argv else None; assert TWIN in (None, "V", "N", "H", "D")
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRJ2 = os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint")
FZD = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
SRC = os.path.join(FRZ, "frz1_forest.py"); code = open(SRC).read()
cut = code.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC, "__name__": "frz1_forest_lib"}
exec(compile(code[:cut], SRC, "exec"), N)
forest_eval, Rkz_z, perz, FD, BGB = (N[k] for k in ("forest_eval", "Rkz_z", "perz", "FD", "BGB"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
HM = json.load(open(os.path.join(HERE, "jnt2r_hm.json")))
RES = dict(lane="JNT2R", part="G1 forest gate" + (f" TWIN {TWIN} (deliberately wrong)" if TWIN else ""), footing=FOOT, reading="5abea0324b",
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", KA=dict(frz1_KA2=N["RES"]["KA"]["KA2"], frz1_KA3=N["RES"]["KA"]["KA3"]), cases={})
def run(name):
    rows = HM["cases"][f"{name}|{FOOT}"]; Rz = {z: v["R_cold"] for z, v in rows.items() if z != "_same_as"}; RZ = Rkz_z(Rz); r_ = forest_eval(FD, BGB, RZ)
    RES["cases"][name] = dict(dchi2=r_["dchi2"], status="PASS" if r_["dchi2"] <= 4 else "FAIL", per_z=perz(RZ),
                              n_above={z: v["n_above"] for z, v in rows.items() if z != "_same_as"})
    P(f"[{FOOT}] {name:10s}: dchi2 {r_['dchi2']:10.4f} -> {RES['cases'][name]['status']}")
    return RES["cases"][name]
FG = ("0.75", "1.00", "1.25", "1.50", "2.00", "3.00")
if TWIN is None:
    for name in ["KA_0"] + [f"P_f{f}" for f in FG] + [f"B_f{f}" for f in FG]: run(name)
    RES["KA"]["KA_0_gate"] = dict(dchi2=RES["cases"]["KA_0"]["dchi2"], pass_=bool(abs(RES["cases"]["KA_0"]["dchi2"]) <= 1e-10))
    P(f"[{FOOT}] KA4 f 0 gate {RES['cases']['KA_0']['dchi2']:.1e} -> {'PASS' if RES['KA']['KA_0_gate']['pass_'] else 'FAIL'}; FRZ1 KA2 {RES['KA']['frz1_KA2']['pass_']}, KA3 {RES['KA']['frz1_KA3']['pass_']}")
    tag = ""
else:
    tw = run(f"TW{TWIN}_f1.00"); gr = json.load(open(os.path.join(HERE, f"jnt2r_forest_{FOOT}.json")))["cases"]["P_f1.00"]["dchi2"]
    o = dict(dchi2=tw["dchi2"], primary_f1=gr)
    if TWIN == "V":
        ref = json.load(open(os.path.join(SRJ2, f"srj2_forest_{FOOT}.json")))["cases"]["on_f1.00"]["dchi2"]; o.update(SRJ2=ref, reproduces=bool(abs(tw["dchi2"] - ref) <= 0.01))
    if TWIN == "N":
        ref = json.load(open(os.path.join(FZD, f"fzs1_forest_{FOOT}.json")))["cases"]["primary"]["dchi2"]; o.update(FZS1=ref, reproduces=bool(abs(tw["dchi2"] - ref) <= 0.01))
    o["moves"] = bool(abs(tw["dchi2"] - gr) > 1.0); o["mark_differs"] = bool((tw["dchi2"] <= 4) != (gr <= 4))
    RES["TW"] = o
    P(f"[{FOOT}] TW-{TWIN} G1: {tw['dchi2']:.4f} against primary f 1 {gr:.4f}; " + ", ".join(f"{k} {v}" for k, v in o.items() if k not in ("dchi2", "primary_f1")))
    tag = f"_MUTATE_{TWIN}"
json.dump(RES, open(os.path.join(HERE, f"jnt2r_forest_{FOOT}{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"jnt2r_forest_{FOOT}{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
sys.exit(1 if TWIN else 0)
