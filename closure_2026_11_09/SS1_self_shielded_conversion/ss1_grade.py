#!/usr/bin/env python3
"""SS1 grader (FROZEN_CRITERIA.md b5adc7a90b + A1 9aeeb48503): assembles parts/ into ss1.json / ss1.out (main) and
ss1_MUTATE.json / ss1_MUTATE.out. Label per footing: PASS iff gates 1, 2, 3, 5, 6, 7(b), 8, 9, 10 PASS; otherwise FAIL with the
first failing gate in the order 1-10. Gate 4 reported (UA1). Gate 7(b) NO VERDICT if KA4's ratio-method validation fails.
kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); PA = os.path.join(HERE, "parts")
FOOTS = ("canonical", "alt"); ORDER = ["1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "6 background", "7b CMB lensing", "8 forest+growth", "9 Bullet", "10 Cassini"]
def L(n): return json.load(open(os.path.join(PA, n)))
def table(suf=""):
    loc = L(f"local{suf}.json"); bul = L(f"bullet{suf}.json"); out = {}
    for f in FOOTS:
        co = L(f"cosmo_{f}{suf}.json"); s = loc[f]["sets"]["primary_SIS"]
        ka4 = L(f"cosmo_{f}.json").get("KA4", {})
        g7 = co["G7b"]["status"]
        if ka4 and not ka4["ratio_method_validation"]["pass_"]: g7 = "NO VERDICT"
        st = {"1 KiDS": s["G1"]["status"], "2 groups": s["G2"]["status"], "3 X-COP": s["G3"]["status"], "5 SPARC": s["G5"]["status"], "6 background": co["G6"]["status"],
              "7b CMB lensing": g7, "8 forest+growth": co["G8"]["status"], "9 Bullet": bul[f]["status"], "10 Cassini": s["G10"]["status"]}
        first = next((g for g in ORDER if st[g] == "FAIL"), None)
        lab = "PASS" if all(v == "PASS" for v in st.values()) else ("FAIL (first failing gate: " + first + ")" if first else "NO VERDICT")
        num = {"1 KiDS": f"max |shift| {s['G1']['max_abs_shift']:.3f} ({s['G1']['n_fail']}/59 over 0.05)",
               "2 groups": f"{s['G2']['fst0']['n_pass']}/20 (f* 0), {s['G2']['fst1']['n_pass']}/20 (f* 1); median residual {s['G2']['fst0']['median_res']:+.2f} / {s['G2']['fst1']['median_res']:+.2f}",
               "3 X-COP": f"mean {s['G3']['mean']:+.3f}, rms {s['G3']['rms']:.3f}; bins " + ", ".join(f"{b['mean']:+.2f}" for b in s['G3']['bins'] if b['graded']),
               "4 Coma UDGs (reported)": f"{s['G4']['mean']:+.3f} ({s['G4']['z']:+.2f} sigma_U); without host term {s['G4']['mean_without_host_component']:+.3f}",
               "5 SPARC": f"rms {s['G5']['all']['rms']:.4f} (line {s['G5']['all']['rms_line']:.4f}), mean {s['G5']['all']['mean']:+.4f}; tail {s['G5']['massive_tail']['rms']:.4f} (line {s['G5']['massive_tail']['rms_line']:.4f}); F2 median {s['G5']['F2']['median_retained_inside_last_over_Mb']:.4f} (allow {s['G5']['F2']['allowance']:.4f})",
               "6 background": f"Delta chi2 {co['G6']['dchi2']:+.2f} (BAO {co['G6']['dchi2_bao']:+.2f}, SN {co['G6']['dchi2_sn']:+.2f}); h {co['G6']['h_ref']:.4f} -> {co['G6']['h']:.4f}; Omega_dr0 {co['G6']['Omega_dr0']:.3f}",
               "7b CMB lensing": f"chi2 {co['G7b']['chi2']:.2f} (line 18.48) on the ratio method",
               "8 forest+growth": f"forest dchi2 {co['G8_forest']['dchi2']:.3f}; fsigma8 Rf " + ", ".join(f"{r['bin']} {r['Rf']:.3f}" for r in co['G8_growth']['rows']),
               "9 Bullet": f"{bul[f]['row']['label']} (cls {bul[f]['row']['cls']}); M300 {bul[f]['row']['M300'][0]/1e14:.2f}, {bul[f]['row']['M300'][1]/1e14:.2f} e14 (Z {bul[f]['row']['ZM'][0]:+.2f}, {bul[f]['row']['ZM'][1]:+.2f})",
               "10 Cassini": f"use {s['G10']['cassini_use']:.3g}, worst planet {s['G10']['worst_planet_use']:.3g}"}
        out[f] = dict(status=st, label=lab, numbers=num, S0=co["cosmic"]["S0_PS"])
    return out
def brackets():
    loc = L("local.json"); o = {}
    for f in FOOTS:
        o[f] = {k: {g: v[g]["status"] for g in ("G1", "G2", "G3", "G5", "G10")} for k, v in loc[f]["sets"].items()}
    return o
def ka():
    core = L("core.json"); loc = L("local.json"); bul = L("bullet.json"); k = dict(KA1=core["KA1"]["pass_"], KA2=core["KA2"]["pass_"], convergence=core["convergence"]["pass_"], KA6=bul["KA6"]["pass_"])
    for f in FOOTS:
        co = L(f"cosmo_{f}.json"); k[f"KA3_{f}"] = loc[f]["KA3"]["pass_"]; k[f"KA4a_LD1_replay_{f}"] = co["KA4"]["LD1_replay"]["pass_"]
        k[f"KA4b_ratio_validation_{f}"] = co["KA4"]["ratio_method_validation"]["pass_"]; k[f"KA5_{f}"] = co["KA5_baseline"]["pass_"] and co["KA5_forest_R1"]["pass_"]; k[f"KA7_{f}"] = co["KA7"]["pass_"]
    return k, core["sigma_gate"]
if __name__ == "__main__":
    main = table(); kas, sg = ka(); br = brackets()
    lines = ["SS1 (self-shielded late conversion). Criteria b5adc7a90b + AMENDMENT_A1 9aeeb48503. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.",
             "Known answers: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in kas.items()),
             f"Sigma_gate 0.042 g/cm^2 from the stated constants: {'REPRODUCED' if sg['reproduced'] else 'NOT REPRODUCED'} (nearest within 10 %: " + "; ".join(f"{h['expr']} {h['value_gcm2']:.4f}" for h in sg['within_10pct']) + ")"]
    for f in FOOTS:
        lines.append(f"[{f}] LABEL: {main[f]['label']}  (cosmic S0 {main[f]['S0']:.4f})")
        for g, n in main[f]["numbers"].items(): lines.append(f"[{f}]   {g:24s} {main[f]['status'].get(g, 'reported'):10s} {n}")
        for k, v in br[f].items(): lines.append(f"[{f}]   bracket {k:15s} " + " ".join(f"{g} {s}" for g, s in v.items()))
    json.dump(dict(criteria="b5adc7a90b", amendment="9aeeb48503", known_answers=kas, sigma_gate=sg, main=main, brackets_local=br, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"),
              open(os.path.join(HERE, "ss1.json"), "w"), indent=1)
    open(os.path.join(HERE, "ss1.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
    # MUTATE
    ml = ["SS1 MUTATE. Criteria b5adc7a90b + A1 9aeeb48503."]; mj = {}
    for m in ("M1", "M2", "M3", "M4"):
        t = table("_" + m); mj[m] = t
        for f in FOOTS:
            diff = [g for g in ORDER if t[f]["status"][g] != main[f]["status"][g]]
            ml.append(f"[{f}] {m}: label {t[f]['label']}; S0 {t[f]['S0']:.4f}; status changes vs main: {diff if diff else 'none'}; " + "; ".join(f"{g}: {t[f]['numbers'][g]}" for g in ("2 groups", "3 X-COP", "6 background", "7b CMB lensing")))
            mj[m][f]["changes_vs_main"] = diff
    bite = {}
    for f in FOOTS:
        bite[f"M1M2_{f}"] = bool(mj["M1"][f]["changes_vs_main"] or mj["M2"][f]["changes_vs_main"])
        c3 = L(f"cosmo_{f}_M3.json")["G7b"]["chi2"]; bite[f"M3_{f}"] = bool(c3 > 18.48)
        bite[f"M4_{f}"] = bool(mj["M4"][f]["status"]["3 X-COP"] == "FAIL")
    ml.append("BITES: " + ", ".join(f"{k} {'BITES' if v else 'NO BITE'}" for k, v in bite.items()))
    json.dump(dict(mutate=mj, bites=bite, criteria="b5adc7a90b"), open(os.path.join(HERE, "ss1_MUTATE.json"), "w"), indent=1)
    open(os.path.join(HERE, "ss1_MUTATE.out"), "w").write("\n".join(ml) + "\n"); print("\n".join(ml))
