#!/usr/bin/env python3
"""SS1 variants B-G grader (AMENDMENT_A2 2b866ef57a, A3 694668618a): parts/ -> ss1v.json / ss1v.out, ss1v_MUTATE.json / .out.
Label per variant and footing: PASS iff gates 1, 2, 3, 5, 5b, 6, 7(b), 8, 9, 10 PASS; else FAIL with the first failing gate.
Gate 4 reported (UA1); 7(b) NO VERDICT (no validated method, A's rule). kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); PA = os.path.join(HERE, "parts"); FOOTS = ("canonical", "alt")
ORDER = ["1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "5b UMa", "6 background", "7b CMB lensing", "8 forest+growth", "9 Bullet", "10 Cassini"]
SUBHALO = {"B": "1 KiDS, 2 groups, 3 X-COP, 5 SPARC (B, C, D, E gates rest on the subhalo bracket)", "C": "same", "D": "same", "E": "same", "F": "f_cen bracket for groups / X-COP", "G": "none"}
CONSTS = {"B": "0.035, 250 kpc, 0.012, Hill 4, 0.72 profile, alpha 3.80", "C": "as B + exponent 3/2, kick 220", "D": "as C, kick 1150", "E": "six added (260, 410, 95, 0.120, 0.008, 3/2)",
          "F": "2 fitted (3.40, 0.75) + baryon key f_cen", "G": "0 fitted; form choices 4 pi, kick factor 4, factor 3, cube-root combination"}
def L(n):
    p = os.path.join(PA, n); return json.load(open(p)) if os.path.exists(p) else None
def table(V, opt=""):
    loc = L(f"local_V{V}{opt}.json"); uma = L(f"uma_V{V}{opt}.json"); bul = L(f"vbullet_{V}.json"); out = {}
    for f in FOOTS:
        s = loc[f]["sets"]["primary_SIS"]; co = L(f"vcosmo_{V}_{f}.json")
        st = {"1 KiDS": s["G1"]["status"], "2 groups": s["G2"]["status"], "3 X-COP": s["G3"]["status"], "5 SPARC": s["G5"]["status"],
              "5b UMa": uma[f]["status"] if uma else "NOT RUN", "6 background": co["G6"]["status"] if co else "NOT RUN", "7b CMB lensing": "NO VERDICT",
              "8 forest+growth": co["G8"]["status"] if co else "NOT RUN", "9 Bullet": bul[f]["status"] if bul else "NOT RUN", "10 Cassini": s["G10"]["status"]}
        first = next((g for g in ORDER if st[g] == "FAIL"), None)
        lab = "PASS" if all(v == "PASS" for v in st.values()) else ("FAIL (first failing gate: " + first + ")" if first else "NO VERDICT")
        num = {"1 KiDS": f"max |shift| {s['G1']['max_abs_shift']:.3f} ({s['G1']['n_fail']}/59 over)",
               "2 groups": f"{s['G2']['fst0']['n_pass']}/20, {s['G2']['fst1']['n_pass']}/20; median residual {s['G2']['fst0']['median_res']:+.2f} / {s['G2']['fst1']['median_res']:+.2f}",
               "3 X-COP": f"mean {s['G3']['mean']:+.3f}, rms {s['G3']['rms']:.3f}; bins " + ", ".join(f"{b['mean']:+.2f}" for b in s['G3']['bins'] if b['graded']),
               "4 Coma UDGs (reported)": f"{s['G4']['mean']:+.3f} ({s['G4']['z']:+.2f} sigma_U)",
               "5 SPARC": f"rms {s['G5']['all']['rms']:.4f} (line {s['G5']['all']['rms_line']:.4f}); tail {s['G5']['massive_tail']['rms']:.4f} ({s['G5']['massive_tail']['rms_line']:.4f}); F2 {s['G5']['F2']['median_retained_inside_last_over_Mb']:.3f}",
               "5b UMa": (f"Delta_pred {uma[f]['Delta_pred']:+.3f} (x_host {uma[f]['x_host_geometry']:.2f}); bound reading {uma[f]['Delta_pred_bound_reading']:+.3f}" if uma else "-"),
               "7b CMB lensing": (f"reading chi2 {co['lensing_reading']['chi2']:.2f}" if co else "-"),
               "8 forest+growth": (f"Rf " + ", ".join(f"{r['bin']} {r['Rf']:.3f}" for r in co['fs8']['rows']) + f"; forest {co['forest']['dchi2']:.3f}; sigma8 {co['sigma8']:.3f} (ref {co['sigma8_ref']:.3f}), S8 {co['S8']:.3f}; converted {co['F_conv_today']:.3f}, lambda {co['lambda_today_Mpc']:.2f} Mpc" if co else "-"),
               "9 Bullet": (f"{bul[f]['row']['label']} (cls {bul[f]['row']['cls']}); M300 {bul[f]['row']['M300'][0]/1e14:.2f}, {bul[f]['row']['M300'][1]/1e14:.2f} e14 (Z {bul[f]['row']['ZM'][0]:+.2f}, {bul[f]['row']['ZM'][1]:+.2f}); dkappa {bul[f]['row']['dkappa'][0]:+.3f}, {bul[f]['row']['dkappa'][1]:+.3f}" if bul else "-"),
               "10 Cassini": f"use {s['G10']['cassini_use']:.3g}"}
        br = {k: {g: v[g]["status"] for g in ("G1", "G2", "G3", "G5", "G10")} for k, v in loc[f]["sets"].items()}
        out[f] = dict(status=st, label=lab, numbers=num, brackets_local=br)
    return out
if __name__ == "__main__":
    ka = L("v_ka.json"); res = dict(amendment2="2b866ef57a", amendment3="694668618a", criteria="b5adc7a90b", known_answers=ka, variants={}, note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
    lines = ["SS1 variants B-G. Criteria b5adc7a90b + A1 9aeeb48503 + A2 2b866ef57a + A3 694668618a. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed."]
    for f in FOOTS:
        F = ka["footings"][f]; lines.append(f"[{f}] F/G constants: z_dec(q=0) {F['z_q0']:.4f}, alpha {F['alpha_G']:.3f}, v_stiff {F['v_stiff']:.1f} km/s, kick {4*F['v_stiff']:.0f} km/s")
    for V in ("G", "B", "C", "D", "E", "F"):
        t = table(V); res["variants"][V] = t
        for f in FOOTS:
            lines.append(f"[{f}] {V} LABEL: {t[f]['label']}   (constants: {CONSTS[V]}; bracket dependence: {SUBHALO[V]})")
            for g, n in t[f]["numbers"].items(): lines.append(f"[{f}]   {V} {g:24s} {t[f]['status'].get(g, 'reported'):10s} {n}")
            for k, v in t[f]["brackets_local"].items(): lines.append(f"[{f}]   {V} bracket {k:15s} " + " ".join(f"{g} {s_}" for g, s_ in v.items()))
            cb = L(f"vcosmo_{V}_{f}_mmin1e10.json")
            if cb: lines.append(f"[{f}]   {V} bracket M_min 1e10: converted {cb['F_conv_today']:.3f}; sigma8 {cb['sigma8']:.3f}, S8 {cb['S8']:.3f}; Rf " + ", ".join(f"{r['bin']} {r['Rf']:.3f}" for r in cb['fs8']['rows']) + f" -> gate 8 {cb['G8']['status']}"); t[f]["cosmo_Mmin1e10"] = dict(G8=cb["G8"]["status"], sigma8=cb["sigma8"], S8=cb["S8"], F_conv=cb["F_conv_today"])
    for opt in ("_obs", "_local"):
        lo = L(f"local_VG{opt}.json")
        if lo:
            for f in FOOTS:
                s = lo[f]["sets"]["primary_SIS"]; lines.append(f"[{f}]   G bracket{opt}: KiDS {s['G1']['status']} {s['G1']['max_abs_shift']:.3f}; groups {s['G2']['status']} {s['G2']['fst0']['n_pass']}/{s['G2']['fst1']['n_pass']} med {s['G2']['fst0']['median_res']:+.2f}/{s['G2']['fst1']['median_res']:+.2f}; X-COP {s['G3']['status']} {s['G3']['mean']:+.3f}/{s['G3']['rms']:.3f} bins " + ", ".join(f"{b['mean']:+.2f}" for b in s['G3']['bins'] if b['graded']) + f"; SPARC {s['G5']['status']}")
            res[f"G_bracket{opt}"] = {f: lo[f]["sets"]["primary_SIS"] for f in FOOTS}
    lf = L("local_VF_fcen0.3.json")
    if lf:
        for f in FOOTS:
            s = lf[f]["sets"]["primary_SIS"]; lines.append(f"[{f}]   F bracket f_cen 0.3: groups {s['G2']['status']} {s['G2']['fst0']['n_pass']}/{s['G2']['fst1']['n_pass']}; X-COP {s['G3']['status']} {s['G3']['mean']:+.3f}; KiDS {s['G1']['status']}; SPARC {s['G5']['status']}")
    json.dump(res, open(os.path.join(HERE, "ss1v.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss1v.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
    ml = ["SS1 variant G MUTATE (A2 section 5)."]; mj = {}; G = res["variants"]["G"]
    for m in ("MG1", "MG2", "MG3", "MG4"):
        t = table(m); mj[m] = t
        for f in FOOTS:
            diff = [g for g in ORDER if t[f]["status"][g] != G[f]["status"][g]]; t[f]["changes_vs_main"] = diff
            ml.append(f"[{f}] {m}: {t[f]['label']}; changes {diff if diff else 'none'}; " + "; ".join(f"{g}: {t[f]['numbers'][g]}" for g in ("1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "8 forest+growth")))
    bite = {}
    for f in FOOTS:
        bite[f"MG1MG2_{f}"] = bool(mj["MG1"][f]["changes_vs_main"] or mj["MG2"][f]["changes_vs_main"])
        bite[f"MG3_{f}"] = bool(mj["MG3"][f]["status"]["1 KiDS"] == "FAIL" or mj["MG3"][f]["status"]["5 SPARC"] == "FAIL")
        bite[f"MG4_{f}"] = bool(mj["MG4"][f]["status"]["2 groups"] == "FAIL" and mj["MG4"][f]["status"]["3 X-COP"] == "FAIL")
    ml.append("BITES: " + ", ".join(f"{k} {'BITES' if v else 'NO BITE'}" for k, v in bite.items()))
    json.dump(dict(mutate=mj, bites=bite), open(os.path.join(HERE, "ss1v_MUTATE.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss1v_MUTATE.out"), "w").write("\n".join(ml) + "\n"); print("\n".join(ml))
