#!/usr/bin/env python3
"""SS3 grader (FROZEN_CRITERIA.md 3a8a5a9fce): parts/ -> ss3.json / ss3.out, ss3_MUTATE.json / .out. Order of gates for the label:
1, 2, 3, 5, 5b, 6, N1, N3, 7b, 8, 9, 10 (N2 enters only if evaluable; it is not). kappa = 1/2 FITTED; not theory closed."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); PA = os.path.join(HERE, "parts"); FOOTS = ("canonical", "alt")
def L(n):
    p = os.path.join(PA, n); return json.load(open(p)) if os.path.exists(p) else None
ORDER = ["1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "5b UMa", "6 BAO+SN", "N1 rho_DE(z)", "N3 covariance", "7b lensing", "8 forest+growth", "9 Bullet", "10 Cassini"]
FORM = "0 fitted; form choices: 50/50 helicity split, (v_stiff/sigma)^2, 200 rho_crit activation, G's cube root / 4 pi"
n3 = L("n3.json"); ka = L("ka_J1.json"); bul = L("vbullet_J.json")
def table(V, cosmoV=None):
    lo = L(f"local_V{V}.json"); uma = L(f"uma_V{V}.json"); out = {}
    for f in FOOTS:
        s = lo[f]["sets"]["primary_SIS"]; co = L(f"vcosmo_{cosmoV or V}_{f}.json")
        st = {"1 KiDS": s["G1"]["status"], "2 groups": s["G2"]["status"], "3 X-COP": s["G3"]["status"], "5 SPARC": s["G5"]["status"], "5b UMa": uma[f]["status"],
              "6 BAO+SN": co["G6"]["status"] if co else "NOT RUN", "N1 rho_DE(z)": co["N1"]["status"] if co else "NOT RUN", "N3 covariance": n3["status"],
              "7b lensing": "NO VERDICT", "8 forest+growth": co["G8"]["status"] if co else "NOT RUN", "9 Bullet": (bul[f]["status"] if (bul and V == "J") else "NOT RUN"), "10 Cassini": s["G10"]["status"]}
        first = next((g for g in ORDER if st[g] == "FAIL"), None)
        lab = "PASS" if all(v == "PASS" for v in st.values()) else ("FAIL (first failing gate: " + first + ")" if first else "NO VERDICT")
        num = {"1 KiDS": f"max |shift| {s['G1']['max_abs_shift']:.3f}", "2 groups": f"{s['G2']['fst0']['n_pass']}/20, {s['G2']['fst1']['n_pass']}/20; median {s['G2']['fst0']['median_res']:+.2f} / {s['G2']['fst1']['median_res']:+.2f}",
               "3 X-COP": f"mean {s['G3']['mean']:+.3f}, rms {s['G3']['rms']:.3f}; bins " + ", ".join(f"{b['mean']:+.2f}" for b in s['G3']['bins'] if b['graded']) + "; retained/M_dyn " + ", ".join(f"{b['retained_over_Mdyn_median']:.2f}" for b in s['G3']['bins'] if b['retained_over_Mdyn_median'] is not None),
               "5 SPARC": f"rms {s['G5']['all']['rms']:.4f} (line {s['G5']['all']['rms_line']:.4f})", "5b UMa": f"{uma[f]['Delta_pred']:+.3f}"}
        if co:
            num.update({"6 BAO+SN": f"Delta chi2 {co['G6']['dchi2']:+.2f}; h {co['h_ref']:.4f} -> {co['h']:.4f}; Omega_DE0 {co['G6']['Omega_DE0']:.3f} (ref {co['G6']['Omega_DE0_ref']:.3f}); D_M/r_d(0.51) {co['G6']['DM_over_rd_051']:.3f} (ref {co['G6']['DM_over_rd_051_ref']:.3f})",
                        "N1 rho_DE(z)": f"rise since z_dec {co['N1']['rho_DE_rise_zdec_to_0']:+.1%}; pulls " + " ".join(f"{x:+.2f}" for x in co['N1']['pulls']) + f"; chi2 {co['N1']['chi2_J']:.2f} vs const {co['N1']['chi2_const_best']:.2f}",
                        "N2 a0(z)": f"NOT EVALUABLE; drift {co['N2']['a0_drift_since_zdec']:+.1%}, a0 today vs footing {co['N2']['a0_today_shift_vs_footing']:+.1%}",
                        "7b lensing": f"reading {co['lensing_reading']['chi2']:.2f}",
                        "8 forest+growth": f"converted {co['F_conv_today']:.3f} of the component; sigma8 {co['sigma8']:.3f}, S8 {co['S8']:.3f}; Rf " + ", ".join(f"{r['bin']} {r['Rf']:.3f}" for r in co['fs8']['rows']) + f"; forest {co['forest']['dchi2']:.3f}"})
        if bul and V == "J": num["9 Bullet"] = f"{bul[f]['row']['label']} (cls {bul[f]['row']['cls']}); M300 Z {bul[f]['row']['ZM'][0]:+.2f}, {bul[f]['row']['ZM'][1]:+.2f}"
        num["N3 covariance"] = "curl of Q = d(Gamma rho_chi)/dr != 0 (no perturbation-free vacuum recipient); uniform case 0 (KA)"
        out[f] = dict(status=st, label=lab, numbers=num)
    return out
res = dict(criteria="3a8a5a9fce", KA_J1=ka, N3=n3, form=FORM); lines = ["SS3 (variant J, vacuum-absorbed conversion). Criteria 3a8a5a9fce. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.",
    f"KA-J1 formula reproduced: {ka['pass_']}; N3 symbolic: {n3['status']} (KA uniform case zero: {n3['KA_uniform_zero']})"]
for V, cv in (("J", None), ("Jsrc", "Jsrc"), ("J_NFW", "J")):
    t = table(V, cv); res[V] = t
    for f in FOOTS:
        lines.append(f"[{f}] {V} LABEL: {t[f]['label']}   ({FORM})" if V == "J" else f"[{f}] bracket {V}: {t[f]['label']}")
        if V == "J":
            for g, n in t[f]["numbers"].items(): lines.append(f"[{f}]   {g:16s} {t[f]['status'].get(g, 'reported'):10s} {n}")
        else: lines.append(f"[{f}]   " + "; ".join(f"{g}: {t[f]['status'][g]} {t[f]['numbers'][g]}" for g in ("2 groups", "3 X-COP")))
for f in FOOTS:
    b = L(f"vcosmo_J_mmin2e11_{f}.json"); res.setdefault("bracket_Mmin2e11", {})[f] = b
    lines.append(f"[{f}] bracket M_min 2e11 (source): converted {b['F_conv_today']:.3f}; rho_DE rise {b['N1']['rho_DE_rise_zdec_to_0']:+.1%}; BAO+SN {b['G6']['dchi2']:+.2f} ({b['G6']['status']}); N1 chi2 {b['N1']['chi2_J']:.2f} vs {b['N1']['chi2_const_best']:.2f} ({b['N1']['status']}); sigma8 {b['sigma8']:.3f}, S8 {b['S8']:.3f}; gate 8 {b['G8']['status']}")
json.dump(res, open(os.path.join(HERE, "ss3.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss3.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
ml = ["SS3 MUTATE (criteria section 5)."]; bite = {}
for f in FOOTS:
    m1 = L(f"vcosmo_J_rad_{f}.json"); j = L(f"vcosmo_J_{f}.json"); m2l = L("local_VMJ2.json")[f]["sets"]["primary_SIS"]; jl = L("local_VJ.json")[f]["sets"]["primary_SIS"]
    bite[f"MJ1_{f}"] = bool(m1["N1"]["status"] != j["N1"]["status"] or abs(m1["G6"]["dchi2"] - j["G6"]["dchi2"]) > 4)
    bite[f"MJ2_{f}"] = bool(abs(m2l["G2"]["fst0"]["median_res"] - jl["G2"]["fst0"]["median_res"]) > 0.05 or abs(m2l["G3"]["mean"] - jl["G3"]["mean"]) > 0.05)
    ml.append(f"[{f}] MJ1 (product -> radiation): BAO+SN {m1['G6']['dchi2']:+.2f} (J {j['G6']['dchi2']:+.2f}); N1 {m1['N1']['status']} (J {j['N1']['status']}); h {m1['h']:.4f}")
    ml.append(f"[{f}] MJ2 (v_stiff -> 0, transverse half only): groups {m2l['G2']['fst0']['n_pass']}/{m2l['G2']['fst1']['n_pass']} median {m2l['G2']['fst0']['median_res']:+.2f} (J {jl['G2']['fst0']['median_res']:+.2f}); X-COP {m2l['G3']['mean']:+.3f} (J {jl['G3']['mean']:+.3f}); KiDS {m2l['G1']['max_abs_shift']:.3f}")
ml.append("BITES: " + ", ".join(f"{k} {'BITES' if v else 'NO BITE'}" for k, v in bite.items()))
json.dump(dict(bites=bite), open(os.path.join(HERE, "ss3_MUTATE.json"), "w"), indent=1); open(os.path.join(HERE, "ss3_MUTATE.out"), "w").write("\n".join(ml) + "\n"); print("\n".join(ml))
