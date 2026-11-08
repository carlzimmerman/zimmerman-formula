#!/usr/bin/env python3
"""CMB1 grade (FROZEN_CRITERIA.md a66f9d1254 / origin 0b04506ce2): parts/base.json + parts/post.json ->
cmb1.json / cmb1.out and cmb1_MUTATE.json / cmb1_MUTATE.out. Footings separate, never pooled.
kappa = 1/2 FITTED; not theory closed."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); P = lambda n: json.load(open(os.path.join(H, "parts", n)))
b, p = P("base.json"), P("post.json")
scan = P("ob_scan.json") if os.path.exists(os.path.join(H, "parts", "ob_scan.json")) else None
NOTE = "kappa = 1/2 FITTED; not theory closed"
out, mut, L, ML = dict(note=NOTE), dict(note=NOTE), [], []
for foot in ("canonical", "alt"):
    r = b[foot]; c = r["cold"]["chi2_F1A"]; dMB = r["DeltaMB"]
    E, B = p[f"E_{foot}"], p[f"B_{foot}"]; dE, dB = E["chi2"] - c, B["chi2"] - c; O = r["KA_E"]["offset_O"]
    E_graded = dE > 10 * O
    if not E_graded: blk = "NO VERDICT (E)"
    elif dE <= 9: blk = "EQUALITY SUFFICES"
    elif dB <= 9: blk = "BARYONS SUFFICE"
    elif dE > 25 and dB > 25: blk = "CLUSTERING PINNED"
    else: blk = "PARTIAL"
    gates = dict(KA1=r["KA1_pass"], M2=r["M2_pass"], M1=r["M1"]["pass_"], KA_E_bg=r["KA_E"]["bg_pass"])
    lane = blk if all(gates.values()) else "NO VERDICT"
    top = {k: v for k, v in r["A_delta"].items() if not k.startswith("  ")}
    big = max(top, key=lambda k: top[k])
    zMB = {k: v["z"] for k, v in r["MB"]["B"].items() if k.startswith("F_")}; zE = {k: v["z"] for k, v in E["B"].items() if k.startswith("F_")}
    fMB = max(zMB, key=lambda k: abs(zMB[k])); fE = max(zE, key=lambda k: abs(zE[k]))
    third = abs(zE["F_32"]) > 5 and abs(zE["F_pos1"]) <= 3 and abs(zE["F_sp"]) <= 3
    out[foot] = dict(DeltaMB=dMB, Delta_E=dE, Delta_B=dB, f_E=(dMB - dE) / dMB, f_B=(dMB - dB) / dMB, offset_O=O, E_graded=E_graded,
                     block_C_label=blk, gates=gates, lane_label=lane, A_delta=top, A_share={k: v / dMB for k, v in top.items()},
                     largest_piece=big, z_MB=zMB, z_E=zE, z_B=dict((k, v["z"]) for k, v in B["B"].items() if k.startswith("F_")),
                     z_cold=dict((k, v["z"]) for k, v in r["cold"]["B"].items() if k.startswith("F_")),
                     largest_feature_MB=fMB, largest_feature_E=fE, third_peak_rule=third, E_pars=E["pars"], B_pars=B["pars"],
                     ob_scan=scan[foot] if scan else None)
    mut[foot] = dict(M1=r["M1"], M2=dict(sum=r["M2_sum"], total=dMB, pass_=r["M2_pass"]), KA1=dict(rebuilt=dMB, F1A=r["DeltaMB_F1A"], pass_=r["KA1_pass"]), KA_E=r["KA_E"])
    L.append(f"{foot}: DeltaMB {dMB:+.1f}; Delta_E {dE:+.1f} (f_E {(dMB - dE) / dMB:.3f}, 10 O = {10 * O:.0f}); Delta_B {dB:+.1f} (f_B {(dMB - dB) / dMB:.4f}); "
             f"block C {blk}; largest piece {big} {top[big] / dMB:.1%}; largest feature MB {fMB} z {zMB[fMB]:+.1f}, E {fE} z {zE[fE]:+.1f}; "
             f"third-peak rule {third}; LANE {lane}")
    ML.append(f"{foot}: M1 dF_oe {r['M1']['dF_oe_sigma']:+.1f} sigma, dF_32 {r['M1']['dF_32_sigma']:+.1f} sigma, ratio {r['M1']['ratio']:.3f} PASS {r['M1']['pass_']}; "
              f"M2 sum {r['M2_sum']:.4f} vs {dMB:.4f} PASS {r['M2_pass']}; KA1 {dMB:.2f} vs {r['DeltaMB_F1A']:.2f} PASS {r['KA1_pass']}; "
              f"KA-E dH {r['KA_E']['max_dH']:.1e} dtheta {r['KA_E']['dtheta']:.1e} O {O:.1f}")
json.dump(out, open(os.path.join(H, "cmb1.json"), "w"), indent=1); json.dump(mut, open(os.path.join(H, "cmb1_MUTATE.json"), "w"), indent=1)
open(os.path.join(H, "cmb1.out"), "w").write("\n".join(L + [NOTE]) + "\n"); open(os.path.join(H, "cmb1_MUTATE.out"), "w").write("\n".join(ML + [NOTE]) + "\n")
print("\n".join(L)); print("\n".join(ML))
