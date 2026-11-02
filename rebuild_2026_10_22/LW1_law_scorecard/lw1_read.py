#!/usr/bin/env python3
"""LW1 read (FROZEN_CRITERIA.md): assembles parts, checks, scorecard. Reads only this lane's JSON and record JSON. Exit 1 on a failed check. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
import numpy as np
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
J = lambda *p: json.load(open(os.path.join(*p)))
HH = ("h0672", "h0686"); FEET = ("canonical", "alt"); KS = ["G-IN-all", "G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3", "G-OUT-b", "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-IN-Mall"]
K = {t: J(HERE, f"lw1_keys_{t}.json") for t in ("g005_f034", "g005_f0615", "g0_f034", "g0_f0615", "MUTATE_g005_f034")}; D1 = {t: J(RB, "DR1_density_term_law", f"dr1_{t}.json") for t in ("g005_f034", "g005_f0615", "g0_f034")}; M3 = J(RB, "M3A1_outer_key_audit", "m3a1_results.json")["Ztot"]; BA = J(RB, "BA1_joint_shear_statistic", "ba1_results.json")["R_orig"]
X = J(HERE, "lw1_xcop.json"); DW = J(HERE, "lw1_dwarfs.json"); DWM = J(HERE, "lw1_dwarfs_MUTATE.json"); DM = J(HERE, "lw1_dm.json"); MW = J(HERE, "lw1_mw.json"); FG = J(RB, "FG1_final_grade", "fg1_results.json"); FH = J(RB, "FG1_final_grade", "fg1_harness_results.json")
CH = {}
def chk(k, ok, m): CH[k] = bool(ok); P(f"{k} {'PASS' if ok else 'FAIL'}: {m}")
def joint(Z, ks, R):
    z0 = np.array([Z[k] for k in ks]); w, V = np.linalg.eigh(R); ok = w >= 1e-3 * w.max(); z = V[:, ok].T @ z0; c2 = float((z * z / w[ok]).sum()); d = int(ok.sum()); return c2, d, float(chi2.sf(c2, d))
def lab(p): return "JOINT PASS" if p >= 0.05 else "JOINT FAIL" if p < 0.01 else "JOINT MARGINAL"
RES = dict(keys={}); P("LW1_law_scorecard: the a0 law on one table. Law scorecard, not a claim of a theory: kappa fitted, no action, CMB and cluster cores not accounted for. Footings never pooled.")
P("\n--- Part 1, keys on the measured chain (Z stat-only; per h)")
for t, gas, fs in (("g005_f034", "+0.005", "0.034"), ("g005_f0615", "+0.005", "0.0615"), ("g0_f034", "+0", "0.034"), ("g0_f0615", "+0", "0.0615")):
    for f in FEET:
        r = K[t][f"R1|c0|{f}"]; Rr = K[t]["R"][f]; o = dict(n=r["n"], bad=r["bad"], cells={}); wst = []
        for h in HH:
            ks = Rr[h]["keys"]; Rb = np.array(Rr[h]["R_boot"]); Rj = np.array(Rr[h]["R_jack"]); a = joint(r["Z"][h], ks, Rb); b = joint(r["Z"][h], ks, Rj); nm = [k for k in ks if k != "G-OUT-M3"]; ii = [ks.index(k) for k in nm]; c = joint(r["Z"][h], nm, Rb[np.ix_(ii, ii)])
            w = max(KS, key=lambda k: abs(r["Z"][h][k])); s = r["tmpl"][h]["G-OUT-M3"][1]; zm = r["Z"][h]["G-OUT-M3"]; zo = K[t.replace("g005", "g0") if t.startswith("g005") else t.replace("g0", "g005")][f"R1|c0|{f}"]["Z"][h]["G-OUT-M3"]; dd = (zm - zo) / (0.005 if t.startswith("g005") else -0.005); q = M3[f"{fs}|{h}"]; sg = abs(dd) * 0.017 * s; tot = float(np.sqrt(s ** 2 + sg ** 2 + q["slope"] ** 2 + q["m"] ** 2 + q["nz"] ** 2 + q["leak"] ** 2)); zt = zm * s / tot
            o["cells"][h] = dict(M3=zm, worst=[w, r["Z"][h][w]], chi2=a[0], dof=a[1], p=a[2], label=lab(a[2]), jack_p=b[2], noM3_chi2=c[0], noM3_p=c[2], Ztot=zt, s=s, gas_term=sg, tot=tot, Z={k: r["Z"][h][k] for k in KS})
        RES["keys"][f"{f}|{gas}|{fs}"] = o; cc = o["cells"]
        P(f"[{f}] gas {gas} f* {fs}: {15 - len(r['bad'])} of 15, over 2 in either h: {', '.join(r['bad'])}"); P("    " + " | ".join(f"{h}: M3 {cc[h]['M3']:+.2f}, Z_tot {cc[h]['Ztot']:+.2f}, worst {cc[h]['worst'][0]} {cc[h]['worst'][1]:+.2f}, chi2 {cc[h]['chi2']:.1f}/{cc[h]['dof']} p {cc[h]['p']:.1e} {cc[h]['label']}, jack p {cc[h]['jack_p']:.1e}, without M3 p {cc[h]['noM3_p']:.1e}" for h in HH))
d2 = 0.0; g2 = 0.0
for t, f in (("g005_f034", "canonical"), ("g005_f034", "alt"), ("g005_f0615", "canonical"), ("g0_f034", "canonical")):
    a, b = K[t][f"R1|c0|{f}"], D1[t][f"R1|c0|{f}"]; g2 = max(g2, abs(a["groups"]["Z"] - b["groups"]["Z"]))
    for h in HH:
        for k in KS: d2 = max(d2, abs(a["Z"][h][k] - b["Z"][h][k]), abs(a["preds"][h][k] - b["preds"][h][k]))
fgc = max(abs(K["g005_f034"][f"R1|c0|{f}"]["groups"]["Z"] - FH["C4"][f]["groups"]["Z"]) for f in FEET)
P(); chk("K2", d2 <= 1e-6 and g2 <= 1e-6, f"keys Z, preds vs DR1 |d| {d2:.1e}; groups {g2:.1e}; groups vs FG1 C4's harness |d| {fgc:.1e} (FG1 rounds to 2 places; different path)")
rd = max(float(np.abs(np.array(K["g0_f034"]["R"]["canonical"][h]["R_boot"]) - np.array(BA[h]["R_boot"])).max()) for h in HH); P(f"K7 note: R on the law's run at gas +0 f* 0.034 vs BA1's stored R_boot max |d| {rd:.1e}")
z = K["g005_f034"]["R1|c0|canonical"]["Z"]["h0672"]; ci = joint(z, KS, np.eye(15))[0]; chk("K7", abs(ci - sum(z[k] ** 2 for k in KS)) <= 1e-9, "R = I gives sum Z^2"); P("K8 NOT RUN: M3A1 doesn't store its R. Its stored chi^2 can't be reproduced through this function without rerunning its audit.")
P("\n--- Part 2, X-COP; convention log10(M_HSE / M_model), positive = model short, both CS2's and DR1's")
for f in FEET: a = X[f]["cached"]; P(f"[{f}] mean {a['mean']:+.3f}, rms {a['rms']:.3f}, factor {a['factor']:.2f}; deficit at x 0.5 {a['deficit_Msun']['0.5']:.2e} Msun, share missing {a['missing_share']['0.5']:.2f}; x 0.7 {a['deficit_Msun']['0.7']:.2e}, {a['missing_share']['0.7']:.2f}; line {'PASS' if a['PASS'] else 'FAIL'}")
P(f"CS2's -0.151, 0.205 is CS2's Burkert core rule, cold mass normalised to M_HSE - M_b at R500: rebuilt {X['cs2_rule']['mean']:+.4f}, {X['cs2_rule']['rms']:.4f}. FG1's C4 X cell showed another rule's row.")
chk("K3", max(X[f]["K3_d"] for f in FEET) <= 1e-6 and abs(X["cs2_rule"]["mean"] + 0.151) < 5e-4 and abs(X["cs2_rule"]["rms"] - 0.205) < 5e-4, f"cached rows vs DR1 |d| {max(X[f]['K3_d'] for f in FEET):.1e}; CS2 rebuilt; FITS builder vs cached {max(abs(X[f]['cached']['mean'] - X[f]['fits']['mean']) for f in FEET):.1e} (G and Msun constants differ)")
P("\n--- Part 3, Local Group dwarfs; E1 primary"); CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")
for f in FEET:
    for k in ("plain", "E0", "E1", "E1lo", "E1hi", "E2"): v = DW["footings"][f]["rows"][k]; P(f"[{f}] {k:6s}: " + "; ".join(f"{c} {v[c]['median']:+.2f} (Z {v[c]['Z']:+.2f})" for c in CLS))
chk("K1", DW["K1"] <= 1e-6, f"plain vs FG1 C4 Dw |d| {DW['K1']:.1e}"); chk("K4", DW["K4_solver"] <= 1e-6 and DW["K4_xe"] <= 1e-6, f"solver vs Z2's stage {DW['K4_solver']:.1e}; xe {DW['K4_xe']:.1e}")
P("\n--- Part 4, DiskMass")
for f in FEET:
    for fm in ("R", "A"): x = DM[f][f"{fm}|1.5"]; P(f"[{f}] form {fm}: r {x['r']:.3f} [{x['lo']:.3f}, {x['hi']:.3f}], Y_K {x['Y']:.3f}, B {x['B']:.2f}, n {x['n']}: {x['label']}; 2.2 h_R r {DM[f][f'{fm}|2.2']['r']:.3f}")
chk("K5", DM["K5_d"] <= 1e-3, f"UR3's no-extra and CFG576's RM, PD |d| {DM['K5_d']:.1e}")
P("\n--- Part 4, Milky Way")
for f in FEET:
    for fm in ("A", "R"): c = MW[f][f"{fm}|1.0"]; b = c["best"]; bi = c["best_in_prior"]; P(f"[{f}] form {fm}: {c['cls']}; all four {c['n_all']}, V+K {c['n_VK']}, X5's gate {c['n_x5gate']}; counts {c['counts']}; best D {b['D']:.2f} (R_d {b['R_d']:.2f}, V_c {b['vc_R0']:.1f}, K {b['K_R0']:.1f}, chi2_Kz {b['chi2_Kz']:.1f}, chi2_Ou {b['chi2_Ou']:.1f}); in priors D {bi['D']:.2f} (V_c {bi['vc_R0']:.1f}, K {bi['K_R0']:.1f}, chi2_Ou {bi['chi2_Ou']:.1f}): {c['label']}")
chk("K6", MW["K6_rel"] <= 1e-6 and max(MW["K6_newton"]) <= 1e-3, f"AQUAL L* = 0 vs X5's L0, rel {MW['K6_rel']:.1e}; Newton McMillan vs GD3 {max(MW['K6_newton']):.1e}")
P("\n--- MUTATE a0 x 1.5, separate outputs")
mv = {}
for f in FEET:
    a, b = K["g005_f034"][f"R1|c0|{f}"], K["MUTATE_g005_f034"][f"R1|c0|{f}"]; dk = max(abs(a["Z"][h][k] - b["Z"][h][k]) for h in HH for k in KS); dx = abs(X[f]["cached"]["mean"] - X[f]["MUTATE"]["mean"]); dd = max(abs(DW["footings"][f]["rows"]["E1"][c]["median"] - DWM["footings"][f]["rows"]["E1"][c]["median"]) for c in CLS); dR = abs(DM[f]["R|1.5"]["r"] - DM[f]["R|MUTATE"]["r"]); dA = abs(DM[f]["A|1.5"]["r"] - DM[f]["A|MUTATE"]["r"]); dAY = abs(DM[f]["A|1.5"]["Y"] - DM[f]["A|MUTATE"]["Y"]); mwa = MW[f]["A|1.0"]; mwb = MW[f]["A|1.5"]; mra = MW[f]["R|1.0"]; mrb = MW[f]["R|1.5"]
    mv[f] = dict(keys=dk, n=[a["n"], b["n"]], xcop=dx, dwarfs=dd, dm_R=dR, dm_A=dA, dm_A_Y=dAY, mw_A=[mwa["cls"], mwb["cls"], mwa["best"]["D"], mwb["best"]["D"]], mw_R=[mra["cls"], mrb["cls"], mra["best"]["D"], mrb["best"]["D"]])
    P(f"[{f}] keys max |dZ| {dk:.2f}, {a['n']} to {b['n']} of 15, M3 h0672 {a['Z']['h0672']['G-OUT-M3']:+.2f} to {b['Z']['h0672']['G-OUT-M3']:+.2f}; X-COP |d mean| {dx:.3f} to {X[f]['MUTATE']['mean']:+.3f}; dwarfs E1 max |d| {dd:.3f}, E1 line {'PASS' if all(abs(DWM['footings'][f]['rows']['E1'][c]['Z']) < 2 for c in CLS) else 'FAIL'}; DiskMass R |dr| {dR:.3f} to {DM[f]['R|MUTATE']['r']:.3f}, A |dr| {dA:.4f}, A |dY| {dAY:.3f}; MW A {mwa['cls']} to {mwb['cls']}, D {mwa['best']['D']:.2f} to {mwb['best']['D']:.2f}; MW R {mra['cls']} to {mrb['cls']}, D {mra['best']['D']:.2f} to {mrb['best']['D']:.2f}")
mok = all(v["keys"] > 0.05 and v["xcop"] > 0.01 and v["dwarfs"] > 0.01 and v["dm_R"] > 0.01 and abs(v["mw_A"][2] - v["mw_A"][3]) > 0.01 and abs(v["mw_R"][2] - v["mw_R"][3]) > 0.01 for v in mv.values()); chk("MUTATE", mok, "keys, X-COP, dwarfs, DiskMass form R, MW both forms move"); P(f"MUTATE, DiskMass form A: r moves {mv['canonical']['dm_A']:.4f} canonical, {mv['alt']['dm_A']:.4f} alt (alt loses one galaxy), Y_K by {mv['canonical']['dm_A_Y']:.3f}, {mv['alt']['dm_A_Y']:.3f}. r on that form barely bites: as frozen a part that doesn't move has failed its check, so form A's DiskMass gets NO LABEL, number shown.")
# ---------------- scorecard
FAILK = {f: RES["keys"][f"{f}|+0.005|0.034"]["n"] < 15 or RES["keys"][f"{f}|+0.005|0.0615"]["n"] < 15 for f in FEET}
def Kc(f):
    a, b = RES["keys"][f"{f}|+0.005|0.034"], RES["keys"][f"{f}|+0.005|0.0615"]; return ("FAIL" if FAILK[f] else "PASS"), f"{a['n']}, {b['n']} of 15 at f* 0.034, 0.0615; M3 {a['cells']['h0672']['M3']:+.2f}/{a['cells']['h0686']['M3']:+.2f}, Z_tot {a['cells']['h0672']['Ztot']:+.2f}/{a['cells']['h0686']['Ztot']:+.2f}; joint p {a['cells']['h0672']['p']:.0e}/{a['cells']['h0686']['p']:.0e}, {b['cells']['h0672']['p']:.0e}/{b['cells']['h0686']['p']:.0e}"
T = {}; ST = J(HERE, "lw1_mw_stress.json")
for f in FEET:
    F = FG["table"]["C4"][f] if "table" in FG else FG["TABLE"]["C4"][f]; e = DW["footings"][f]["rows"]["E1"]; a = X[f]["cached"]; R_, A_ = DM[f]["R|1.5"], DM[f]["A|1.5"]; mA, mR = MW[f]["A|1.0"], MW[f]["R|1.0"]; tag = " [FORM-DEPENDENT]" if mA["label"] != mR["label"] else ""
    T[f] = {}
    for ln in ("S", "Tl", "LT", "G", "Ln", "IC"): T[f][ln] = (F[ln]["status"], F[ln]["value"] + " [READ FG1]")
    s, n = Kc(f); T[f]["K"] = (s, n); T[f]["X"] = ("PASS" if a["PASS"] else "FAIL", f"mean {a['mean']:+.3f}, rms {a['rms']:.3f}, M_HSE/M_law {a['factor']:.2f}")
    T[f]["Dw"] = ("PASS" if all(abs(e[c]["Z"]) < 2 for c in CLS) else "FAIL", "; ".join(f"{c} {e[c]['median']:+.2f} (Z {e[c]['Z']:+.2f})" for c in CLS) + " [E1]")
    T[f]["MW"] = (f"A {mA['label']}, R {mR['label']}", f"form A {mA['cls']}, {mA['n_all']} cells, X5's gate {mA['n_x5gate']}; form R {mR['cls']}, {mR['n_all']} cells, {ST[f]['n_inprior']} in priors{tag}. No action picks the form")
    T[f]["DM"] = (R_["label"], f"form R r {R_['r']:.3f}, Y_K {R_['Y']:.3f}, n {R_['n']}; form A r {A_['r']:.3f}, NO LABEL (MUTATE doesn't bite on r)")
P("\n=== SCORECARD, the a0 law. Not a theory: kappa fitted, no action, CMB and cluster cores not accounted for"); LINES = ("S", "Tl", "LT", "G", "K", "X", "Ln", "Dw", "MW", "DM", "IC")
for f in FEET:
    P(f"[{f}]")
    for ln in LINES: P(f"  {ln:3s} {T[f][ln][0]:14s} {T[f][ln][1]}")
    P("  FAILED: " + ", ".join(l for l in LINES if T[f][l][0] == "FAIL")); P("  Form dependent: MW. DiskMass form A has no label.")
RES.update(table=T, mutate=mv, checks=CH); json.dump(RES, open(os.path.join(HERE, "lw1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "lw1.out"), "w").write("\n".join(OUT) + "\n"); P(f"\nchecks {sum(CH.values())}/{len(CH)}"); sys.exit(0 if all(CH.values()) else 1)
