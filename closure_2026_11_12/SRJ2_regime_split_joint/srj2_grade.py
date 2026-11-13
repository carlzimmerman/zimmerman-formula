#!/usr/bin/env python3
"""SRJ2 (FROZEN_CRITERIA.md, b8a99499ad): words per footing from the lane's outputs (sections 3, 4, 6, 7 of the criteria).
  python3 srj2_grade.py -> srj2_grade.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(HERE, n)))
HM, RC, LE, CL, LF2 = J("srj2_hm.json"), J("srj2_rc.json"), J("srj2_lens.json"), J("srj2_clusters.json"), J("srj2_lens_MUTATE_F2.json")
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("SRJ2 grade (criteria b8a99499ad). Footings never pooled. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
RES = dict(lane="SRJ2", criteria="b8a99499ad", foot={})
for ft in ("canonical", "alt"):
    FO, TC, TF = J(f"srj2_forest_{ft}.json"), J(f"srj2_forest_{ft}_MUTATE_C.json"), J(f"srj2_forest_{ft}_MUTATE_F2.json")
    rows = {}
    for f in ("0.75", "1.00", "1.25"):
        g1 = FO["cases"][f"on_f{f}"]["dchi2"]; c = CL["foot"][ft][f"joint_f{float(f):.2f}"]["labels"]; lc = LE["cfg"][f"{ft}|on_f{f}"]
        rows[f] = dict(G1=(g1 <= 4, round(g1, 4)), G2=(RC["foot"][ft]["G2"][f"f{f}"]["pass_"], RC["foot"][ft]["G2"][f"f{f}"]["covered"]),
                       G3=(RC["foot"][ft]["G3"][f"f{f}"]["pass_"], RC["foot"][ft]["G3"][f"f{f}"]["by"]),
                       G4=(lc["gate"]["status"] == "PASS", [round(lc["gate"]["lines"][k]["z"], 4) for k in ("G-K1 all", "G-K1 late", "G-K1 early", "G-K3 type difference")] + [round(lc["gate"]["lines"]["G-K2 all profile"]["chi2"], 4)]),
                       clusters=(c["a_last"] == "CONSISTENT" and c["b"] == "CONSISTENT", dict(a=c["a_last"], b=c["b"])),
                       groups=(c["c"] == "CONSISTENT", c["c"]))
    checks = dict(C1_G1=TC["TW_C"]["C1_pass"], C1_G2=RC["foot"][ft]["C1_G2"]["pass_"], C1_G3a=RC["foot"][ft]["C1_G3a"]["pass_"],
                  C1_G4=LE["checks"][f"{ft}|off_f1.00"]["pass_"], C2_G4=LE["checks"][f"{ft}|f0"]["pass_"], C2_G1=FO["KA"]["KA_0_gate"]["pass_"],
                  C3=HM["KA"]["C3"]["pass_"] and LE["C3_lens"] <= 1e-12, C4=HM["KA"]["C4_KA_M"]["pass_"] and HM["KA"]["KA_0_hm"]["pass_"] and FO["KA"]["frz1_KA2"]["pass_"] and FO["KA"]["frz1_KA3"]["pass_"],
                  C1_hm=HM["KA"]["C1_hm"]["pass_"], C5=CL["foot"][ft]["C5"]["pass_"])
    twins = dict(TW_C=TC["TW_C"]["bites"], TW_F2=bool(TF["TW_F2"]["G1_bites"] or LF2[f"TW_F2_canonical"]["G4_bites"]))
    pri = rows["1.00"]; fails = [k for k, v in pri.items() if not v[0]]
    word = "NO VERDICT" if not (all(checks.values()) and all(twins.values())) else ("JOINT HOLDS ON EVERY GRADED ROW (ONE-SIDED)" if not fails else "JOINT FAILS ON " + ", ".join(fails))
    cross = [f"{k} at f {f}" for f in ("0.75", "1.25") for k in pri if rows[f][k][0] != pri[k][0]]
    ref = CL["foot"][ft]["reference"]["labels"]
    if (ref["a_R500"] == "CONSISTENT") != (pri["clusters"][0]): cross.append("clusters, R500 aperture bracket (inherited)")
    triv = []
    if FO["cases"]["on_f1.00"]["dchi2"] < 1: triv.append(f"G1 (Delta chi^2 {FO['cases']['on_f1.00']['dchi2']:.4f} < 1)")
    if LE[f"trivial_{ft}"]["trivial"]: triv.append(f"G4 (max |dz| {LE['trivial_' + ft]['max_z_vs_ref']:.3f}, |dchi2| {LE['trivial_' + ft]['chi2_vs_ref']:.3f} from the reference)")
    if CL["foot"][ft]["n_below"]["xcop"] == 0 and CL["foot"][ft]["n_below"]["groups"] == 0: triv.append("clusters and groups (every system above v_stiff; joint = reference, difference 0)")
    RES["foot"][ft] = dict(word=word, fragile=cross, trivial=triv, rows=rows, checks=checks, twins=twins)
    P(f"[{ft}] WORD: {word}" + (f", FRAGILE ({'; '.join(cross)})" if cross else ""))
    P(f"[{ft}] TRIVIAL beside: {triv if triv else 'none'}")
    for f, r in rows.items(): P(f"[{ft}] f {f}: " + "; ".join(f"{k} {'P' if v[0] else 'F'} {v[1]}" for k, v in r.items()))
    P(f"[{ft}] checks {checks}; twins {twins}")
json.dump(RES, open(os.path.join(HERE, "srj2_grade.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, "srj2_grade.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
