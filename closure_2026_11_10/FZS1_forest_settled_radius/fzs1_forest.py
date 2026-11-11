#!/usr/bin/env python3
"""FZS1 (FROZEN_CRITERIA.md, 73defd766f): the record's forest gate as FRZ1 used it, fed with fzs1_hm.json.
FRZ1's frz1_forest.py is executed unchanged, from its own path (read-only), up to the line that reads frz1_hm.json; nothing is
written in FRZ1's folder. KA-T and KA-0 on the gate; graded reading, brackets x0.5 / x2 / reading V; MUTATE MS1, MS2.
  FZS1_FOOT=canonical|alt nice -n 10 python3 fzs1_forest.py -> fzs1_forest_<foot>.json / .out, fzs1_forest_<foot>_MUTATE.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json
FOOT = os.environ.get("FZS1_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRC = os.path.join(FRZ, "frz1_forest.py"); code = open(SRC).read()
cut = code.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC, "__name__": "frz1_forest_lib"}
exec(compile(code[:cut], SRC, "exec"), N)
import numpy as np
forest_eval, Rkz_z, perz, FD, BGB = (N[k] for k in ("forest_eval", "Rkz_z", "perz", "FD", "BGB"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = dict(lane="FZS1", part="forest gate", footing=FOOT, criteria="73defd766f", note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           data=N["RES"]["data"], KA=dict(frz1_KA2=N["RES"]["KA"]["KA2"], frz1_KA3=N["RES"]["KA"]["KA3"]), cases={})
HM = json.load(open(os.path.join(HERE, "fzs1_hm.json"))); MU = json.load(open(os.path.join(HERE, "fzs1_hm_MUTATE.json")))
FZF = json.load(open(os.path.join(FRZ, f"frz1_forest_{FOOT}.json")))
def run(name, rows):
    Rz = {z: v["R_cold"] for z, v in rows.items()}; RZ = Rkz_z(Rz); r_ = forest_eval(FD, BGB, RZ)
    RES["cases"][name] = dict(dchi2=r_["dchi2"], r_min=r_["r_min"], r_max=r_["r_max"], status=r_["status"], per_z=perz(RZ),
                              R_cold_at_k1_3_5_10={z: v["R_cold_at"] for z, v in rows.items()})
    P(f"[{FOOT}] {name:9s}: dchi2 {r_['dchi2']:10.3f} (1D ratio {r_['r_min']:.5f}-{r_['r_max']:.5f}) -> {r_['status']}")
for name in ("KA_T", "KA_0", "primary", "x0.5", "x2", "readingV"):
    run(name, HM["cases"][f"{name}|{FOOT}"])
kt = RES["cases"]["KA_T"]; f0 = FZF["cases"]["primary"]
dper = max(abs(kt["per_z"][z] - f0["per_z"][z]) for z in f0["per_z"])
RES["KA"]["KA_T_gate"] = dict(dchi2=kt["dchi2"], frz1=f0["dchi2"], max_per_bin_diff=dper, pass_=bool(abs(kt["dchi2"] - f0["dchi2"]) <= 0.01 and dper <= 0.01))
RES["KA"]["KA_0_gate"] = dict(dchi2=RES["cases"]["KA_0"]["dchi2"], pass_=bool(abs(RES["cases"]["KA_0"]["dchi2"]) <= 1e-10))
P(f"[{FOOT}] KA-T gate: {kt['dchi2']:.3f} against FRZ1 {f0['dchi2']:.3f}, max per-bin diff {dper:.2e} -> {'PASS' if RES['KA']['KA_T_gate']['pass_'] else 'FAIL'}; "
  f"KA-0 gate: {RES['cases']['KA_0']['dchi2']:.1e} -> {'PASS' if RES['KA']['KA_0_gate']['pass_'] else 'FAIL'}")
pri = RES["cases"]["primary"]; P(f"[{FOOT}] graded per z: " + " ".join(f"{k}:{v:.3f}" for k, v in pri["per_z"].items()))
# MUTATE
MR = {}
for name in ("MS1_x10", "MS2_zrev"):
    rows = MU["MUTATE"]["cases"][f"{name}|{FOOT}"]; Rz = {z: v["R_cold"] for z, v in rows.items()}; r_ = forest_eval(FD, BGB, Rkz_z(Rz))
    MR[name] = dict(dchi2=r_["dchi2"], status=r_["status"])
    P(f"[{FOOT}] MUTATE {name}: dchi2 {r_['dchi2']:.3f} -> {r_['status']}")
MR["MS1"] = dict(bites=bool(MR["MS1_x10"]["dchi2"] > 4)); MR["MS2_hm"] = MU["MUTATE"]["MS2"]
P(f"[{FOOT}] MS1 (x10) {'bites' if MR['MS1']['bites'] else 'DOES NOT BITE'}; MS2 (halo model, canonical) {'bites' if MR['MS2_hm']['bites'] else 'DOES NOT BITE'}")
json.dump(dict(lane="FZS1", footing=FOOT, MUTATE=MR, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, f"fzs1_forest_{FOOT}_MUTATE.json"), "w"), indent=1, default=float)
ka_ok = all(v.get("pass_", True) for k, v in HM["KA"].items()) and RES["KA"]["KA_T_gate"]["pass_"] and RES["KA"]["KA_0_gate"]["pass_"] \
    and RES["KA"]["frz1_KA2"]["pass_"] and RES["KA"]["frz1_KA3"]["pass_"]
mu_ok = MR["MS1"]["bites"] and MR["MS2_hm"]["bites"]
lab = "FOREST ROW HOLDS WITH A SETTLED RADIUS" if pri["dchi2"] <= 4 else "FOREST ROW FAILS"
cross = [n for n in ("x0.5", "x2", "readingV") if (RES["cases"][n]["dchi2"] <= 4) != (pri["dchi2"] <= 4)]
RES["label"] = (lab + (", FRAGILE (" + ", ".join(cross) + ")" if cross else "")) if (ka_ok and mu_ok) else "NO VERDICT"
RES.update(KA_ok=bool(ka_ok), MUTATE_ok=bool(mu_ok), crossing_brackets=cross)
P(f"[{FOOT}] label: {RES['label']}")
json.dump(RES, open(os.path.join(HERE, f"fzs1_forest_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"fzs1_forest_{FOOT}.out"), "w").write("\n".join(OUT) + "\n")
