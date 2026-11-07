"""F1A grade: assemble parts/*.json into f1a.json / f1a.out and f1a_MUTATE.json / f1a_MUTATE.out.
Per FROZEN_CRITERIA.md (56879e50da) and AMENDMENT_A1.md (78d0c6f7fa). Footings graded separately, never pooled.
kappa = 1/2 FITTED; not theory closed."""
import json, os
P = lambda n: json.load(open(os.path.join("parts", n)))
cal = P("cal.json")["chi2_cal"]["PA"]; ka = P("ka.json"); g4 = P("g4.json"); m2 = P("mutate_M2.json")["M2"]
QX15_MB = {"canonical": 172848.0, "alt": 166612.0}
b1c, b1m = P("fit_B1_canonical_cold.json"), P("fit_B1_canonical_MB.json")
out, mut, lines, mlines = {}, {}, [], []
ka_ok = ka["KA_A"]["pass_"] and ka["KA_P"]["pass_"] and all(abs(r["KA_dust"] - 1) <= 1e-3 for r in g4["rows"])
g4_ok = all(r["Q_X1"] <= 0.05 and r["Q_X2"] <= 0.05 for r in g4["rows"] if r["k"] >= 0.05)
qx1max = max(r["Q_X1"] for r in g4["rows"])
for foot in ("canonical", "alt"):
    c, m = P(f"fit_B2_{foot}_cold.json"), P(f"fit_B2_{foot}_MB.json")
    dB2 = m["chi2"]["PA"] - c["chi2"]["PA"]; dB1 = b1m["chi2"]["PA"] - b1c["chi2"]["PA"]
    dcal = c["chi2"]["PA"] - cal
    R = c["pars"]["oc"] / c["pars"]["ob"]; R1 = b1c["pars"]["oc"] / b1c["pars"]["ob"]
    G1 = dB1 > 25 and dB2 > 25; G2 = dcal <= 9; G3 = abs(R / 5.562 - 1) <= 0.10
    ratio = dB2 / QX15_MB[foot]; M1 = dB2 > 25; M2 = m2[foot]["pass_"]
    if not (ka_ok and M1 and M2): label = "NO VERDICT"
    elif dB2 <= 25 or dcal > 25 or qx1max >= 0.5: label = "REFUTED"
    elif G1 and G2 and G3 and g4_ok: label = "CONFIRMED"
    else: label = "WEAKENED"
    out[foot] = dict(chi2_cold_B2=c["chi2"]["PA"], chi2_MB_B2=m["chi2"]["PA"], DeltaMB_B2=dB2,
                     chi2_cold_B1=b1c["chi2"]["PA"], chi2_MB_B1=b1m["chi2"]["PA"], DeltaMB_B1=dB1, G1_fails=G1,
                     chi2_cal=cal, Delta_cal=dcal, G2_adequate=G2, R_B2=R, R_over_5562=R / 5.562, G3_match=G3,
                     R_B1=R1, best_B2=c["pars"], best_B1=b1c["pars"], G4_reproduced=g4_ok, Q_X1_max=qx1max,
                     chi2_hmcode=c.get("chi2_hmcode_reported"), class_Pcut_diff_cold=c["class_check_Pcut"]["diff"],
                     class_Pcut_diff_MB=m["class_check_Pcut"]["diff"], MB_best=m["pars"], label=label)
    mut[foot] = dict(M1_DeltaMB=dB2, M1_ratio_to_QX15=ratio, M1_pass=M1, M1_same_order=0.5 <= ratio <= 2, M2=m2[foot])
    lines.append(f"{foot}: B2 cold {c['chi2']['PA']:.2f} MB {m['chi2']['PA']:.2f} DeltaMB {dB2:+.1f}; B1 DeltaMB {dB1:+.1f}; "
                 f"Delta_cal {dcal:+.2f}; R {R:.3f} ({R/5.562:.3f} of 5.562), B1 R {R1:.3f}; G4 {g4_ok} (Q_X1 max {qx1max:.1e}); "
                 f"HMCode {c.get('chi2_hmcode_reported'):.2f}; CLASS Pcut diff cold {c['class_check_Pcut']['diff']:.2f}; LABEL {label}")
    mlines.append(f"{foot}: M1 DeltaMB {dB2:+.1f} ratio to QX15 {ratio:.4f} pass {M1}; M2 dchi2 {m2[foot]['dchi2']:+.1f} "
                  f"peak1 {m2[foot]['peak1_best']}->{m2[foot]['peak1_ob030']} pass {M2}")
out["G4_rows"] = g4["rows"]; out["KA"] = ka; out["KA_ok"] = ka_ok
out["note"] = mut["note"] = "kappa = 1/2 FITTED; not theory closed"
json.dump(out, open("f1a.json", "w"), indent=1); json.dump(mut, open("f1a_MUTATE.json", "w"), indent=1)
open("f1a.out", "w").write("\n".join(lines + [f"KA ok {ka_ok}", out["note"]]) + "\n")
open("f1a_MUTATE.out", "w").write("\n".join(mlines + [mut["note"]]) + "\n")
print(open("f1a.out").read()); print(open("f1a_MUTATE.out").read())
