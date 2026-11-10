"""TK1 grade: reads tk1_a1.json, tk1_k4.json, tk1_frw.json, tk1_a3.json, tk1_a45.json, tk1_ka3.json and the MUTATE
outputs; prints the known answers, the per-footing A1-A5 table and the lane label (frozen, then under AMENDMENT A1).
Criteria 98f2ab2b6e, AMENDMENT A1 813946cec9. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, json
H = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(H, f)))
a1, k4, frw, a3, a45, ka3 = J("tk1_a1.json"), J("tk1_k4.json"), J("tk1_frw.json"), J("tk1_a3.json"), J("tk1_a45.json"), J("tk1_ka3.json")
a1m, k4m, a3m2 = J("tk1_a1_MUTATE_MU1.json"), J("tk1_k4_MUTATE_MU3.json"), J("tk1_a3_MUTATE_MU2.json")
out = {}
ka = {
    "KA1 covariant current (max rel residual)": (max(a1["K1_residuals"]), max(a1["K1_residuals"]) < 1e-30),
    "KA2 charge identity / Friedmann form": ((a1["KA2_identity_residual"], a1["KA2_friedmann_residual"]),
                                            a1["KA2_identity_residual"] == "0" and a1["KA2_friedmann_residual"] == "0"),
    "KA3 rho_K form (symbolic)": (a1["KA3_residual"], a1["KA3_residual"] == "0"),
    "KA3 mu_B1a -> w(3400) = 0.01 (canonical, alt rel)": ((ka3["canonical"]["rel"], ka3["alt"]["rel"]),
                                                          ka3["canonical"]["pass_"] and ka3["alt"]["pass_"]),
    "KA4 lambda-term G_cosmo": (a1["KA4_residual"], a1["KA4_residual"] == "0"),
    "KA5 K4 key off: c_s^2 = (Q-1)/Q (max |rel|, tk1_ka5.json)": (max(abs(v["rel"]) for k_, v in J("tk1_ka5.json").items() if k_.startswith("key_off")), J("tk1_ka5.json")["KA5_pass"]),
    "KA6 EdS delta_lin at collapse": (a3["KA6"]["delta_lin_coll"], a3["KA6"]["pass_"]),
    "KA7 sqrt(Msun a0/G) per kpc": (a45["KA7"]["canonical"], a45["KA7"]["pass_"]),
    "KA-K4 A_z numerator proportional to the Hessian trace (factor a^5)": (k4["KA_K4_ratio"], k4["KA_K4_ratio"] == "a(t)**5"),
}
allka = all(v[1] for v in ka.values())
print("Known answers:")
for k, v in ka.items():
    print("  %-70s %s  %s" % (k, v[0], "PASS" if v[1] else "FAIL"))
out["known_answers_pass"] = allka
mut = {
    "MU1 KA2 Friedmann form residual": (a1m["KA2_friedmann_residual"] != "0"),
    "MU1 A3 a-equation residual (see tk1_a3_MUTATE_MU1)": None,
    "MU3 KA-K4 ratio": (k4m["KA_K4_ratio"] != "a(t)**5"),
}
print("MUTATE:")
print("  MU1 KA2 Friedmann-form residual nonzero:", mut["MU1 KA2 Friedmann form residual"])
print("  MU3 KA-K4 ratio no longer a^5:", mut["MU3 KA-K4 ratio"], "(", k4m["KA_K4_ratio"], ")")
for foot in ("canonical", "alt"):
    for zt in ("5", "2", "1", "0.5"):
        r = a3m2[foot]["A3"]["MU2_key_off_zta%s" % zt]
        tc, tg = r.get("t_coll_Gyr"), r["t_coll_GR_Gyr"]
        print("  MU2 %s z_ta %s: %s, t_coll %.4f vs GR %.4f (rel %.1e)%s" % (
            foot, zt, r["label_frozen"], tc, tg, tc / tg - 1, " [GR itself after t0 = %.2f]" % r["t0_Gyr"] if tg > r["t0_Gyr"] else ""))
print()
for foot in ("canonical", "alt"):
    print("=== %s" % foot)
    f = frw[foot]["primary"]
    wp = (max(a1["K1_residuals"]) < 1e-30 and a1["K2c_residual"] == "0" and not f["z_with_Az_le_0"]
          and not f["z_with_g4_over_Az_lt_0"])
    gmax = max(abs(r["G_cosmo_over_G_minus_1"]) for r in f["rows"].values())
    print("A1 around FRW (primary): %s; max |G_cosmo/G_N - 1| %.2e; lambda_eff(z 0) %.2e" % (
        "WELL-POSED" if wp else "NOT WELL-DEFINED", gmax, f["rows"]["0"]["lambda_eff"]))
    for nm in ("theta0_9H0", "p4", "floor_off"):
        fb = frw[foot][nm]
        print("    bracket %-10s A_z <= 0 at z %s; g4/A_z < 0 at z %s" % (
            nm, ("none" if not fb["z_with_Az_le_0"] else "%.2g-%.2g" % (min(fb["z_with_Az_le_0"]), max(fb["z_with_Az_le_0"]))),
            ("none" if not fb["z_with_g4_over_Az_lt_0"] else "0-%.2g" % max(fb["z_with_g4_over_Az_lt_0"]))))
    a2 = a3[foot]["A2"]["primary"]
    print("A2: w(3400) %.2e (line 0.01); mu_eff min %.4g per Mpc at z %.2g vs mu_J %.4g (ratio %.3f): %s" % (
        a2["rows"]["3400"]["w"], a2["mu_eff_min"]["mu"], a2["mu_eff_min"]["z"], a2["mu_eff_min"]["mu_J"], a2["mu_eff_min"]["ratio"],
        "PASS" if a2["w3400_pass"] and a2["jeans_dominance_pass"] else "FAIL/NOT EVALUABLE"))
    labs_f, labs_a = [], []
    for zt in ("5", "2", "1", "0.5"):
        for nm in ("primary", "theta0_9H0", "p4", "floor_off"):
            r = a3[foot]["A3"]["%s_zta%s" % (nm, zt)]
            E = r["events"]
            def ev(n):
                e = E.get(n)
                return "-" if not e else "%+.3g Myr (theta %.3g H0, wl %.3g kpc)" % (
                    e["minus_t_ta_GR_Myr"], e["theta"], (e.get("unstable_wavelength_pc") or 0) / 1e3)
            if nm == "primary":
                labs_f.append(r["label_frozen"]); labs_a.append(r["label_A1"])
            t0s = r.get("at_t0") or {}
            print("A3 z_ta %-3s %-10s frozen %-22s A1 %-22s | lam<0 %s | s2 %s | fold %s | at t0: a/a_ta %.6f H %.2e H0 Q-1 %.1e | if s3 set aside: frozen %s, A1 %s" % (
                zt, nm, r["label_frozen"], r["label_A1"], ev("lam_zero"), ev("s2"),
                ("after %.3g Gyr" % r["t_fold_Gyr"]) if r.get("t_fold_Gyr") else "none",
                t0s.get("a_over_aGR", float("nan")), t0s.get("H", float("nan")), t0s.get("Qm1", float("nan")),
                "SINGULAR (s2)" if E.get("s2") and E["s2"]["before_t0"] else "STALLS",
                "SINGULAR (fold)" if (r.get("t_fold_Gyr") or 1e99) < r["t0_Gyr"] else "STALLS"))
    a3lab = "SINGULAR" if any(l.startswith("SINGULAR") for l in labs_f) else ("STALLS" if any(l == "STALLS" for l in labs_f) else "REGULAR")
    a3labA = "SINGULAR" if any(l.startswith("SINGULAR") for l in labs_a) else ("STALLS" if any(l == "STALLS" for l in labs_a) else "REGULAR")
    rows5 = a45["A5"][foot]
    fails5 = [k for k, v in rows5.items() if not v["passes"]]
    print("A4 (reported): short of 5.41 M_b at %d of 8; cap holds at %d of 8" % (
        sum(1 for r in a45["A4"][foot] if not r["holds_5p41"]), sum(1 for r in a45["A4"][foot] if r["holds_cap"])))
    print("A5 (reported): failing rows %s" % fails5)
    if not allka:
        lab = "NO VERDICT"
    elif not wp:
        lab = "NOT WELL-DEFINED"
    elif a3lab == "SINGULAR":
        lab = "BREAKS AT TURNAROUND"
    elif a3lab == "STALLS":
        lab = "STALLS AT TURNAROUND"
    else:
        lab = "ROWS FAIL" if fails5 else "CLOSES MK1's GAP"
    labA = ("BREAKS AT TURNAROUND" if a3labA == "SINGULAR" else "STALLS AT TURNAROUND" if a3labA == "STALLS" else lab) if (allka and wp) else lab
    print("LANE LABEL %s: frozen %s | under A1 %s" % (foot, lab, labA))
    out[foot] = dict(label_frozen=lab, label_A1=labA, A1_FRW=wp, G_ratio_max=gmax, A5_fails=fails5)
json.dump(out, open(os.path.join(H, "tk1_grade.json"), "w"), indent=1)
