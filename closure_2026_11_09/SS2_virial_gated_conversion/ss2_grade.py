#!/usr/bin/env python3
"""SS2 grader (FROZEN_CRITERIA.md 390a1dc5ff): parts/ -> ss2.json / ss2.out and ss2_MUTATE.json / .out. Gate tables through SS1's
ss1v_grade.table (read-only) pointed at this lane's parts/. Label per footing: PASS iff 1, 2, 3, 5, 5b, 6, 7(b), 8, 9, 10 PASS;
else FAIL with the first failing gate. 7(b) graded only if the CMB-lensing validation passed (it did not: NO VERDICT).
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); SS1 = os.path.join(HERE, "..", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1)
import ss1v_grade as VG
VG.PA = os.path.join(HERE, "parts"); FOOTS = ("canonical", "alt"); L = VG.L
FORM = "fitted constants 0; form choices: cube root (a0 c L*)^(1/3), kick factor 4, 4 pi in Gamma0, factor 3 in x0"
valid = {f: L(f"valid_{f}.json") for f in FOOTS}; ka = L("v_ka.json"); pred = L("predict.json")
res = dict(criteria="390a1dc5ff", known_answers=ka, lensing_validation=valid, prediction=pred, form_choices=FORM, note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
lines = ["SS2 (variant G, virial-gated late conversion). Criteria 390a1dc5ff. Not blind: SS1 A2 graded G first (f3186ce8e7). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.",
         f"Known answers: K0 {'PASS' if ka['K0_closed_form_vs_ODE']['pass_'] else 'FAIL'}; K-G {'PASS' if ka['K_G']['pass_'] else 'FAIL (threshold point M500 1e13: f 0.148 vs 0.161)'}; Lovisari min f {ka['K_G']['lovisari_min_f']:.4f}; x_crit 4.39 {ka['x_crit_4p39']:.4f}, footing " + ", ".join(f"{f} {v:.4f}" for f, v in ka['x_crit_footing'].items())]
for f in FOOTS:
    v = valid[f]; F = ka["footings"][f]
    lines.append(f"[{f}] constants: z_dec {F['z_q0']:.4f}, alpha {F['alpha_G']:.3f}, v_stiff {F['v_stiff']:.1f} km/s, kick {4*F['v_stiff']:.0f} km/s (source: 0.642, 4.39, 286)")
    lines.append(f"[{f}] lensing validation: CLASS {v['chi2_CLASS']:.2f} vs method {v['chi2_method']:.2f} (baseline {v['baseline']:.2f}, tol {v['tolerance']:.2f}) -> {'PASS' if v['pass_'] else 'FAIL: 7(b) NO VERDICT'}")
for V in ("G", "Gsrc"):
    t = VG.table(V); res[V] = t
    for f in FOOTS:
        lines.append(f"[{f}] {V} LABEL: {t[f]['label']}   ({FORM})")
        for g, n in t[f]["numbers"].items(): lines.append(f"[{f}]   {V} {g:24s} {t[f]['status'].get(g, 'reported'):10s} {n}")
        for k, b in t[f]["brackets_local"].items(): lines.append(f"[{f}]   {V} bracket {k:15s} " + " ".join(f"{g} {s_}" for g, s_ in b.items()))
for opt in ("_obs", "_local"):
    lo = L(f"local_VG{opt}.json")
    for f in FOOTS:
        s = lo[f]["sets"]["primary_SIS"]; lines.append(f"[{f}]   G bracket{opt}: groups {s['G2']['status']} {s['G2']['fst0']['n_pass']}/{s['G2']['fst1']['n_pass']} med {s['G2']['fst0']['median_res']:+.2f}/{s['G2']['fst1']['median_res']:+.2f}; X-COP {s['G3']['status']} {s['G3']['mean']:+.3f}; KiDS {s['G1']['status']}; SPARC {s['G5']['status']}")
for f in FOOTS:
    cb = L(f"vcosmo_G_{f}_mmin1e10.json"); lines.append(f"[{f}]   G bracket M_min 1e10: converted {cb['F_conv_today']:.3f}; sigma8 {cb['sigma8']:.3f}, S8 {cb['S8']:.3f}; Rf " + ", ".join(f"{r['bin']} {r['Rf']:.3f}" for r in cb['fs8']['rows']) + f" -> gate 8 {cb['G8']['status']}")
# amount table (per group, per radial point) and TR1 fraction, primary G
lo = L("local_VG.json"); amt = {}
for f in FOOTS:
    s = lo[f]["sets"]["primary_SIS"]; amt[f] = {fst: [dict(name=g["name"], x0=g["x0"], retained_over_Mb=g["retained_over_Mb"], dlog=g["dlog"]) for g in s["G2"][fst]["per"]] for fst in ("fst0", "fst1")}
    tr = [(b["lo"], b["retained_over_Mdyn_median"], b["TR1_D_canonical"]) for b in s["G3"]["bins"] if b["retained_over_Mdyn_median"] is not None]
    lines.append(f"[{f}]   X-COP retained / M_dyn by bin (TR1 D canonical beside): " + ", ".join(f"{lo_:.2f}: {r:.2f} ({t:.2f})" for lo_, r, t in tr) + f"; TR1 shape with the retained component: {s['G3']['TR1_shape_reported']}")
    g0 = amt[f]["fst0"]; lines.append(f"[{f}]   groups f* 0: retained 4.1 M_b in {sum(1 for g in g0 if g['retained_over_Mb'] > 3.9)}/20; per-point residuals median {sorted(d for g in g0 for d in g['dlog'])[len([d for g in g0 for d in g['dlog']])//2]:+.2f}")
res["amount_table"] = amt
for f in FOOTS:
    lines.append(f"[{f}]   lens-z prediction (frozen; no split on disk): source +0.245/+0.205/+0.078/+0.020; lane primary " + ", ".join(f"{q['excess_dex']:+.3f}" for q in pred["lane"][f]["primary_KD1P3"]["rows"]) + "; lane Moster " + ", ".join(f"{q['excess_dex']:+.3f}" for q in pred["lane"][f]["Moster13"]["rows"]))
json.dump(res, open(os.path.join(HERE, "ss2.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss2.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
# MUTATE
G = res["G"]; ml = ["SS2 MUTATE (criteria 390a1dc5ff section 6)."]; mj = {}; bite = {}
for m in ("MG1", "MG2", "MG3", "MG4"):
    t = VG.table(m); mj[m] = t
    for f in FOOTS:
        diff = [g for g in VG.ORDER if t[f]["status"][g] != "NOT RUN" and t[f]["status"][g] != G[f]["status"][g]]; t[f]["changes_vs_main"] = diff   # gates not run in a MUTATE pass are not changes
        ml.append(f"[{f}] {m}: {t[f]['label']}; changes {diff if diff else 'none'}; " + "; ".join(f"{g}: {t[f]['numbers'][g]}" for g in ("1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "8 forest+growth")))
for f in FOOTS:
    z2 = L(f"vcosmo_Gz2_{f}.json"); g0 = L(f"vcosmo_G_{f}.json")
    bite[f"M5_{f}"] = bool(z2["lensing_reading"]["chi2"] > g0["lensing_reading"]["chi2"])
    ml.append(f"[{f}] M5 onset z 2: lensing reading {z2['lensing_reading']['chi2']:.2f} vs main {g0['lensing_reading']['chi2']:.2f}; converted {z2['F_conv_today']:.3f}; sigma8 {z2['sigma8']:.3f}")
    bite[f"M1M2_{f}"] = bool(mj["MG1"][f]["changes_vs_main"] or mj["MG2"][f]["changes_vs_main"])
    bite[f"M3_{f}"] = bool(mj["MG3"][f]["status"]["1 KiDS"] == "FAIL" or mj["MG3"][f]["status"]["5 SPARC"] == "FAIL")
    bite[f"M4_{f}"] = bool(mj["MG4"][f]["status"]["2 groups"] == "FAIL" and mj["MG4"][f]["status"]["3 X-COP"] == "FAIL")
ml.append("BITES: " + ", ".join(f"{k} {'BITES' if v else 'NO BITE'}" for k, v in bite.items()))
json.dump(dict(mutate=mj, bites=bite), open(os.path.join(HERE, "ss2_MUTATE.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss2_MUTATE.out"), "w").write("\n".join(ml) + "\n"); print("\n".join(ml))
