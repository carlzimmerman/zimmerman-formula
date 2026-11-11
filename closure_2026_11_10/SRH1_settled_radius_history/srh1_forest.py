#!/usr/bin/env python3
"""SRH1 (FROZEN_CRITERIA.md, 5ed8a37ec6): G1 forest gate, a copy of FZS1's fzs1_forest.py (73defd766f) fed with srh1_hm.json.
FRZ1's frz1_forest.py is executed unchanged, from its own path (read-only), up to the line that reads frz1_hm.json; nothing
is written in FRZ1's or FZS1's folders. KA-T / KA-0 on the gate; KA-G1 against FZS1's f = 1 and 0.5; every grid f; tilts;
MUTATE MU1 (f 10), MU3a (z reversed at f 0.6).
  SRH1_FOOT=canonical|alt nice -n 10 python3 srh1_forest.py -> srh1_forest_<foot>.json / .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json
FOOT = os.environ.get("SRH1_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
FZD = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
SRC = os.path.join(FRZ, "frz1_forest.py"); code = open(SRC).read()
cut = code.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
N = {"__file__": SRC, "__name__": "frz1_forest_lib"}
exec(compile(code[:cut], SRC, "exec"), N)
import numpy as np
forest_eval, Rkz_z, perz, FD, BGB = (N[k] for k in ("forest_eval", "Rkz_z", "perz", "FD", "BGB"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = dict(lane="SRH1", part="G1 forest gate", footing=FOOT, criteria="5ed8a37ec6", note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           data=N["RES"]["data"], KA=dict(frz1_KA2=N["RES"]["KA"]["KA2"], frz1_KA3=N["RES"]["KA"]["KA3"]), cases={})
HM = json.load(open(os.path.join(HERE, "srh1_hm.json"))); MU = json.load(open(os.path.join(HERE, "srh1_hm_MUTATE.json")))
FZF = json.load(open(os.path.join(FRZ, f"frz1_forest_{FOOT}.json"))); FZS = json.load(open(os.path.join(FZD, f"fzs1_forest_{FOOT}.json")))
def run(name, rows, store=RES["cases"]):
    Rz = {z: v["R_cold"] for z, v in rows.items()}; RZ = Rkz_z(Rz); r_ = forest_eval(FD, BGB, RZ)
    store[name] = dict(dchi2=r_["dchi2"], r_min=r_["r_min"], r_max=r_["r_max"], status=r_["status"], per_z=perz(RZ),
                       s_min_max={z: v["s_min_max"] for z, v in rows.items()})
    P(f"[{FOOT}] {name:22s}: dchi2 {r_['dchi2']:10.3f} (1D ratio {r_['r_min']:.5f}-{r_['r_max']:.5f}) -> {'PASS' if r_['dchi2'] <= 4 else 'FAIL'}")
names = [k.split("|")[0] for k in HM["cases"] if k.endswith("|" + FOOT)]
for name in names: run(name, HM["cases"][f"{name}|{FOOT}"])
kt = RES["cases"]["KA_T"]; f0 = FZF["cases"]["primary"]
dper = max(abs(kt["per_z"][z] - f0["per_z"][z]) for z in f0["per_z"])
RES["KA"]["KA_T_gate"] = dict(dchi2=kt["dchi2"], frz1=f0["dchi2"], max_per_bin_diff=dper, pass_=bool(abs(kt["dchi2"] - f0["dchi2"]) <= 0.01 and dper <= 0.01))
RES["KA"]["KA_0_gate"] = dict(dchi2=RES["cases"]["KA_0"]["dchi2"], pass_=bool(abs(RES["cases"]["KA_0"]["dchi2"]) <= 1e-10))
kg = {fn: (RES["cases"][fn]["dchi2"], FZS["cases"][fz]["dchi2"]) for fn, fz in (("f1.00", "primary"), ("f0.50", "x0.5"))}
RES["KA"]["KA_G1"] = dict(rows=kg, pass_=bool(all(abs(a - b) <= 0.01 for a, b in kg.values())))
P(f"[{FOOT}] KA-T gate: {kt['dchi2']:.3f} vs FRZ1 {f0['dchi2']:.3f} (per-bin {dper:.1e}) -> {'PASS' if RES['KA']['KA_T_gate']['pass_'] else 'FAIL'}; "
  f"KA-0: {RES['cases']['KA_0']['dchi2']:.1e} -> {'PASS' if RES['KA']['KA_0_gate']['pass_'] else 'FAIL'}; KA-G1 (f 1, 0.5 vs FZS1): "
  + ", ".join(f"{k} {a:.3f} vs {b:.3f}" for k, (a, b) in kg.items()) + f" -> {'PASS' if RES['KA']['KA_G1']['pass_'] else 'FAIL'}")
MR = {}
for name in ("MU1_f10", "MU3a_zrev_f0.60"):
    run(name, MU["MUTATE"]["cases"][f"{name}|{FOOT}"], MR)
MR["MU1"] = dict(bites=bool(MR["MU1_f10"]["dchi2"] > 4)); MR["MU3a_hm"] = MU["MUTATE"]["MU3a"]
P(f"[{FOOT}] MU1 (f 10) {'bites' if MR['MU1']['bites'] else 'DOES NOT BITE'}; MU3a (halo model, canonical) {'bites' if MR['MU3a_hm']['bites'] else 'DOES NOT BITE'}")
RES["MUTATE"] = MR
grid = HM["f_grid"]; G1 = {f"{f:.2f}": RES["cases"][f"f{f:.2f}"]["dchi2"] <= 4 for f in grid}
RES["G1_pass"] = G1; ok = [f for f in grid if G1[f"{f:.2f}"]]
RES["G1_upper"] = max(ok) if ok else None
P(f"[{FOOT}] G1 passes at f = {ok}")
RES["KA_ok"] = bool(all(v.get("pass_", True) for k, v in HM["KA"].items() if isinstance(v, dict)) and RES["KA"]["KA_T_gate"]["pass_"] and RES["KA"]["KA_0_gate"]["pass_"]
                    and RES["KA"]["KA_G1"]["pass_"] and RES["KA"]["frz1_KA2"]["pass_"] and RES["KA"]["frz1_KA3"]["pass_"])
RES["MUTATE_ok"] = bool(MR["MU1"]["bites"] and MR["MU3a_hm"]["bites"])
P(f"[{FOOT}] KA all pass: {RES['KA_ok']}; MUTATE bite: {RES['MUTATE_ok']}")
json.dump(RES, open(os.path.join(HERE, f"srh1_forest_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"srh1_forest_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
