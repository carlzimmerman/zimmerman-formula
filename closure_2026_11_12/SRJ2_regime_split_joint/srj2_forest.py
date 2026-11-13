#!/usr/bin/env python3
"""SRJ2 (FROZEN_CRITERIA.md, b8a99499ad): G1 forest gate at matter level, FZS1's fzs1_forest.py machinery fed with srj2_hm.json.
FRZ1's frz1_forest.py is executed unchanged, from its own path (read-only), up to the line that reads frz1_hm.json.
KA-0 on the gate, FRZ1's KA2 / KA3, C1 (split off f 1 = FZS1's 38.741 / 36.658), the graded joint and its fixed points.
  SRJ2_FOOT=canonical|alt python3 srj2_forest.py          -> srj2_forest_<foot>.json / .out
  SRJ2_FOOT=canonical|alt python3 srj2_forest.py --twin C  -> srj2_forest_<foot>_MUTATE_C.json / .out   (TW-C; exits 1)
  SRJ2_FOOT=canonical|alt python3 srj2_forest.py --twin F2 -> srj2_forest_<foot>_MUTATE_F2.json / .out  (TW-F2; exits 1)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
FOOT = os.environ.get("SRJ2_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
TWIN = sys.argv[sys.argv.index("--twin") + 1] if "--twin" in sys.argv else None; assert TWIN in (None, "C", "F2")
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
FZD = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
SRC = os.path.join(FRZ, "frz1_forest.py"); code = open(SRC).read()
cut = code.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC, "__name__": "frz1_forest_lib"}
exec(compile(code[:cut], SRC, "exec"), N)
forest_eval, Rkz_z, perz, FD, BGB = (N[k] for k in ("forest_eval", "Rkz_z", "perz", "FD", "BGB"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
HM = json.load(open(os.path.join(HERE, "srj2_hm.json"))); FZS = json.load(open(os.path.join(FZD, f"fzs1_forest_{FOOT}.json")))
RES = dict(lane="SRJ2", part="G1 forest gate" + (f" TWIN {TWIN} (deliberately wrong)" if TWIN else ""), footing=FOOT, criteria="b8a99499ad",
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", data=N["RES"]["data"],
           KA=dict(frz1_KA2=N["RES"]["KA"]["KA2"], frz1_KA3=N["RES"]["KA"]["KA3"]), cases={})
def run(name):
    rows = HM["cases"][f"{name}|{FOOT}"]; Rz = {z: v["R_cold"] for z, v in rows.items()}; RZ = Rkz_z(Rz); r_ = forest_eval(FD, BGB, RZ)
    RES["cases"][name] = dict(dchi2=r_["dchi2"], r_min=r_["r_min"], r_max=r_["r_max"], status=r_["status"], per_z=perz(RZ),
                              n_cluster_regime={z: v["n_cluster_regime"] for z, v in rows.items()})
    P(f"[{FOOT}] {name:10s}: dchi2 {r_['dchi2']:10.4f} (1D ratio {r_['r_min']:.5f}-{r_['r_max']:.5f}) -> {'PASS' if r_['dchi2'] <= 4 else 'FAIL'}")
    return RES["cases"][name]
if TWIN is None:
    for name in ("KA_0", "on_f1.00", "on_f0.75", "on_f1.25"): run(name)
    RES["KA"]["KA_0_gate"] = dict(dchi2=RES["cases"]["KA_0"]["dchi2"], pass_=bool(abs(RES["cases"]["KA_0"]["dchi2"]) <= 1e-10))
    pri = RES["cases"]["on_f1.00"]
    P(f"[{FOOT}] graded (on, f 1) per z: " + " ".join(f"{k}:{v:.4f}" for k, v in pri["per_z"].items()))
    P(f"[{FOOT}] KA-0 gate {RES['cases']['KA_0']['dchi2']:.1e} -> {'PASS' if RES['KA']['KA_0_gate']['pass_'] else 'FAIL'}; FRZ1 KA2 {RES['KA']['frz1_KA2']['pass_']}, KA3 {RES['KA']['frz1_KA3']['pass_']}")
    tag = ""
else:
    name = "off_f1.00" if TWIN == "C" else "on_f2.00"; tw = run(name)
    gr = json.load(open(os.path.join(HERE, f"srj2_forest_{FOOT}.json")))["cases"]["on_f1.00"]["dchi2"]
    if TWIN == "C":
        fz = FZS["cases"]["primary"]["dchi2"]
        RES["TW_C"] = dict(dchi2=tw["dchi2"], FZS1=fz, graded=gr, C1_pass=bool(abs(tw["dchi2"] - fz) <= 0.01), bites=bool(abs(tw["dchi2"] - fz) <= 0.01 and abs(tw["dchi2"] - gr) > 1))
        P(f"[{FOOT}] TW-C / C1 (law's layout restored in cluster-regime haloes = FZS1's rule): {tw['dchi2']:.3f} vs FZS1 {fz:.3f} (C1 {'PASS' if RES['TW_C']['C1_pass'] else 'FAIL'}); graded {gr:.4f} -> {'bites' if RES['TW_C']['bites'] else 'DOES NOT BITE'}")
    else:
        RES["TW_F2"] = dict(dchi2=tw["dchi2"], graded=gr, G1_bites=bool(tw["dchi2"] - gr > 1))
        P(f"[{FOOT}] TW-F2 (joint at f 2): {tw['dchi2']:.4f} vs graded f 1 {gr:.4f} -> G1 part {'bites' if RES['TW_F2']['G1_bites'] else 'does not bite (G4 part in srj2_lens)'}")
    tag = f"_MUTATE_{TWIN}"
json.dump(RES, open(os.path.join(HERE, f"srj2_forest_{FOOT}{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"srj2_forest_{FOOT}{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
sys.exit(1 if TWIN else 0)
