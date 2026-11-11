#!/usr/bin/env python3
"""FRZ2 known answers and summary (KA-P0, KA-P2, MZ1, labels). -> frz2_summary.json / .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S1 = os.path.join(H, "..", "FRZ1_forest_redistribution_at_z")
F1 = json.load(open(os.path.join(S1, "frz1_hm.json")))
OUT = []; R = dict(lane="FRZ2", note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
def P(s): print(s); OUT.append(s)
ka0 = {}
for ft in ("canonical", "alt"):
    J = json.load(open(os.path.join(H, "hm", f"P0_{ft}.json")))["rows"]; ref = F1["cases"][f"primary|{ft}"]
    ka0[ft] = max(float(np.max(np.abs(np.array(J[z]["R_cold"]) / np.array(ref[z]["R_cold"]) - 1))) for z in J)
FO = {ft: json.load(open(os.path.join(H, f"frz2_forest_{ft}.json"))) for ft in ("canonical", "alt")}
d0 = {"canonical": 9916.2, "alt": 9008.7}
okd = all(abs(FO[ft]["cases"]["P0"]["dchi2"] - d0[ft]) <= 0.1 for ft in d0)
R["KA_P0"] = dict(max_rel=ka0, dchi2_ok=okd, pass_=bool(max(ka0.values()) <= 1e-10 and okd))
c = json.load(open(os.path.join(H, "hm", "P2_canonical.json")))["rows"]["3.0"]["R_cold_at"][1]
p = json.load(open(os.path.join(H, "hm", "P0_canonical.json")))["rows"]["3.0"]["R_cold_at"][1]
R["KA_P2"] = dict(change_k3=c - p, frz1=0.5018, pass_=bool(abs(c - p - 0.502) <= 0.01))
mz = {ft: json.load(open(os.path.join(H, f"frz2_forest_{ft}_MUTATE.json")))["MUTATE"]["MZ1"]["dchi2"] for ft in d0}
R["MZ1"] = dict(dchi2=mz, bites=bool(min(mz.values()) > 4))
P(f"KA-P0 max rel {ka0}, dchi2 ok {okd} -> {'PASS' if R['KA_P0']['pass_'] else 'FAIL'}; KA-P2 change {c - p:+.4f} -> {'PASS' if R['KA_P2']['pass_'] else 'FAIL'}; MZ1 {mz} -> {'bites' if R['MZ1']['bites'] else 'DOES NOT BITE'}")
R["table"] = {}
for name in FO["canonical"]["cases"]:
    a, b = FO["canonical"]["cases"][name], FO["alt"]["cases"][name]
    R["table"][name] = dict(f_z3=a["f_z3"], Rk3_5=[a["R_cold_z3_k135"][1:], b["R_cold_z3_k135"][1:]], dchi2=[a["dchi2"], b["dchi2"]], label=[a["label"], b["label"]])
    P(f"{name:7s} f(3) {a['f_z3']:.3f} R(k3,k5) can {a['R_cold_z3_k135'][1]:.3f}/{a['R_cold_z3_k135'][2]:.3f} alt {b['R_cold_z3_k135'][1]:.3f}/{b['R_cold_z3_k135'][2]:.3f} dchi2 {a['dchi2']:.1f} / {b['dchi2']:.1f} {a['label']}/{b['label']}")
fw = [n for n in R["table"] if n[0] in "DQH"]
anyb = [n for n in fw if all(l == "PASSES" for l in R["table"][n]["label"])]
ok = R["KA_P0"]["pass_"] and R["KA_P2"]["pass_"] and R["MZ1"]["bites"]
R["lane_label"] = "NO VERDICT" if not ok else ("A FRAMEWORK a0(z) PASSES" if anyb else "NO FRAMEWORK a0(z) PASSES")
for i, ft in enumerate(("canonical", "alt")):
    pl = {n: R["table"][n]["dchi2"][i] for n in R["table"] if n[0] == "P"}; bn = min(pl, key=pl.get)
    R[f"best_power_{ft}"] = [bn, pl[bn]]; P(f"best power law {ft}: {bn} dchi2 {pl[bn]:.1f} (under gate: {pl[bn] <= 4})")
P(f"LANE: {R['lane_label']}")
json.dump(R, open(os.path.join(H, "frz2_summary.json"), "w"), indent=1); open(os.path.join(H, "frz2_summary.out"), "w").write("\n".join(OUT) + "\n")
