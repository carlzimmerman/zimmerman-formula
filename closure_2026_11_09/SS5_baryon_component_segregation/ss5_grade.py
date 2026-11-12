#!/usr/bin/env python3
"""SS5 grader (FROZEN_CRITERIA.md 12c42eef04): parts/ss5_<footing>.json -> ss5.json / ss5.out, ss5_MUTATE.json / .out.
The frozen label is the one ss5.py computes (section 2 label rule + section 3 known answers + ML1 power). A reading at z 0 only
(the offset line was frozen without a redshift; ss5.py applies it at z 3, 1.2 and 0) is printed beside it, marked post hoc.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); FOOTS = ("canonical", "alt")
FORM = "0 fitted; form choices (the source's): the 1/sqrt(3) cap, the u^4 (1 + u^2) capture law, R_seg = v_stiff / H(z_turn), z_turn = 1.2"
R = {f: json.load(open(os.path.join(HERE, "parts", f"ss5_{f}.json"))) for f in FOOTS}
res = dict(criteria="12c42eef04", form=FORM, footings={}); L = ["SS5 (variant L, baryon-component segregation). Criteria 12c42eef04. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed."]
ml = ["SS5 MUTATE (criteria section 4)."]; bites = {}
for f in FOOTS:
    r = R[f]; m = r["mechanism"]; a = r["D2a"]; b = r["D2b"]
    z0 = b["main"]["z 0.0"]["offset_Mpc"]; post = "no segregation (r = 1; baryons more concentrated; z 0 offset < 0.35)" if (m["r_ge_099"] and m["baryons_at_least_as_concentrated"] and z0 < 0.35) else "separation"
    res["footings"][f] = dict(label=m["label"], mechanism=m, post_hoc_z0_reading=post, KA_L2=r["KA_L2"], KA_L3=r["KA_L3"], ML1_bites=r["ML1_bites"])
    L.append(f"[{f}] LABEL (frozen): {m['label']}   ({FORM})")
    L.append(f"[{f}]   D1: " + "; ".join(f"{k}: " + ", ".join(f"{z} b/chi {v['delta_b_over_delta_chi']:.2f} (nu {v['nu']:.1f}) r {v['r']:.3f}" for z, v in kv.items()) for k, kv in r["D1"].items()))
    L.append(f"[{f}]   D2(a) collapse z (half-mass shell / qM shell): chi {a['setup']['z_coll_chi_half_shell']:.2f} / {a['setup']['z_coll_chi_qM_shell']:.2f}, baryons {a['setup']['z_coll_b_half_shell']:.2f} / {a['setup']['z_coll_b_qM_shell']:.2f}; 2x steps: chi {a['setup_2x']['z_coll_chi_half_shell']:.2f} / {a['setup_2x']['z_coll_chi_qM_shell']:.2f}, b {a['setup_2x']['z_coll_b_half_shell']:.2f} / {a['setup_2x']['z_coll_b_qM_shell']:.2f}; KA-L2 {r['KA_L2']['z_coll_newton_qM_shell']:.3f} {'PASS' if r['KA_L2']['pass_'] else 'FAIL'}")
    L.append(f"[{f}]   D2(a) R_half (kpc) chi / b: " + "; ".join(f"{z} {v['R_half_chi_kpc']:.0f} / {v['R_half_b_kpc']:.0f}" for z, v in a["main"].items()) + "; 2x steps " + "; ".join(f"{z} {v['R_half_chi_kpc']:.0f} / {v['R_half_b_kpc']:.0f}" for z, v in a["convergence_2x_steps"].items()) + " (z 0 radii not step-converged: post-collapse radial bounce)")
    L.append(f"[{f}]   D2(b) offsets (Mpc) z 3 / 1.2 / 0: main " + " / ".join(f"{v['offset_Mpc']:.3f}" for v in b["main"].values()) + "; 4x steps " + " / ".join(f"{v['offset_Mpc']:.3f}" for v in b["convergence_4x_steps"].values()) + f"; claimed R_seg {dict(canonical=3.45, alt=3.74)[f]} Mpc; line 0.35")
    L.append(f"[{f}]   reading at z 0 (post hoc, reported): {post}")
    ml.append(f"[{f}] ML1 planted v_stiff at z 1.2 (law baryons): offsets " + " / ".join(f"{v['offset_Mpc']:.3f}" for v in b["ML1_planted"].values()) + f" -> {'BITES' if r['ML1_bites'] else 'NO BITE'}; power check (planted, Newtonian baryons, reported): " + " / ".join(f"{v['offset_Mpc']:.3f}" for v in b["power_check_planted_newton_reported"].values()))
    ml.append(f"[{f}] ML2 Newtonian baryons: offsets " + " / ".join(f"{v['offset_Mpc']:.3f}" for v in b["ML2_newton"].values()) + f" -> KA-L3 {'PASS' if r['KA_L3'] else 'FAIL'}")
    bites[f"ML1_{f}"] = r["ML1_bites"]; bites[f"ML2_{f}"] = r["KA_L3"]
json.dump(res, open(os.path.join(HERE, "ss5.json"), "w"), indent=1); open(os.path.join(HERE, "ss5.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
json.dump(dict(bites=bites), open(os.path.join(HERE, "ss5_MUTATE.json"), "w"), indent=1); open(os.path.join(HERE, "ss5_MUTATE.out"), "w").write("\n".join(ml) + "\n"); print("\n".join(ml))
