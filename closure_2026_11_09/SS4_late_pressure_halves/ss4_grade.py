#!/usr/bin/env python3
"""SS4 grader (FROZEN_CRITERIA.md f3effad98c): parts/ -> ss4.json / ss4.out, ss4_MUTATE.json / .out. Order for the label: 1, 2, 3, 5,
5b, 6, 7b, 8, CS, 9, 10. Item (4) dynamics computed here (core reachability at each half's sound speed). kappa = 1/2 FITTED."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); PA = os.path.join(HERE, "parts"); FOOTS = ("canonical", "alt"); sys.path.insert(0, HERE)
def L(n):
    p = os.path.join(PA, n); return json.load(open(p)) if os.path.exists(p) else None
ORDER = ["1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "5b UMa", "6 background", "7b lensing", "8 forest+growth", "CS cosmic shear", "9 Bullet", "10 Cassini"]
FORM = "0 fitted; form choices: 50/50 split, 4/3 polytrope, R_c1 = 2.60 Mpc (its formula gives 0.31 / 0.34 Mpc), the cube power, c_s2's form"
def table(V):
    lo = L(f"local_V{V}.json"); uma = L(f"uma_V{V}.json"); bul = L(f"vbullet_{V}.json"); out = {}
    for f in FOOTS:
        s = lo[f]["sets"]["primary_SIS"]; co = L(f"vcosmo_{V}_{f}.json")
        st = {"1 KiDS": s["G1"]["status"], "2 groups": s["G2"]["status"], "3 X-COP": s["G3"]["status"], "5 SPARC": s["G5"]["status"], "5b UMa": uma[f]["status"],
              "6 background": "PASS", "7b lensing": "NO VERDICT", "8 forest+growth": co["G8"]["status"] if co else "NOT RUN", "CS cosmic shear": co["CS"]["status"] if co else "NOT RUN",
              "9 Bullet": bul[f]["status"] if bul else "NOT RUN", "10 Cassini": s["G10"]["status"]}
        first = next((g for g in ORDER if st[g] == "FAIL"), None)
        lab = "PASS" if all(v == "PASS" for v in st.values()) else ("FAIL (first failing gate: " + first + ")" if first else "NO VERDICT")
        num = {"1 KiDS": f"max |shift| {s['G1']['max_abs_shift']:.3f} ({s['G1']['n_fail']}/59 over); per bin 0.3/1/1.5 Mpc " + "; ".join(f"{lm}: " + "/".join(f"{v['nearest'][k]['shift']:+.3f}" for k in ('0.3 Mpc', '1.0 Mpc', '1.5 Mpc')) for lm, v in s['G1']['per_bin'].items()),
               "2 groups": f"{s['G2']['fst0']['n_pass']}/20, {s['G2']['fst1']['n_pass']}/20; median {s['G2']['fst0']['median_res']:+.2f} / {s['G2']['fst1']['median_res']:+.2f}",
               "3 X-COP": f"mean {s['G3']['mean']:+.3f}, rms {s['G3']['rms']:.3f}; bins " + ", ".join(f"{b['mean']:+.2f}" for b in s['G3']['bins'] if b['graded']) + "; retained/M_dyn " + ", ".join(f"{b['retained_over_Mdyn_median']:.2f}" for b in s['G3']['bins'] if b['retained_over_Mdyn_median'] is not None),
               "5 SPARC": f"rms {s['G5']['all']['rms']:.4f} (line {s['G5']['all']['rms_line']:.4f})", "5b UMa": f"{uma[f]['Delta_pred']:+.3f}"}
        if co: num.update({"8 forest+growth": "Rf " + ", ".join(f"{r['bin']} {r['Rf']:.3f}" for r in co['fs8']['rows']) + f"; forest {co['forest']['dchi2']:.3f}",
                           "CS cosmic shear": f"sigma8 {co['sigma8']:.3f} (ratio {co['sigma8_ratio_z0']:.3f}); S8 {co['S8']:.3f} vs ref {co['S8_ref']:.3f}: change {co['CS']['S8_change']:+.1%} (line +-{co['CS']['line']:.1%}); P ratio " + ", ".join(f"{k} {v:.2f}" for k, v in co['CS']['Pk_ratio'].items()),
                           "7b lensing": f"reading {co['lensing_reading']['chi2']:.2f}"})
        if bul: num["9 Bullet"] = f"gas-traced {bul[f]['row']['label']} (cls {bul[f]['row']['cls']}; M300 Z {bul[f]['row']['ZM'][0]:+.2f}, {bul[f]['row']['ZM'][1]:+.2f}); galaxy-traced {bul[f]['galaxy_traced_reported']['label']} ({bul[f]['galaxy_traced_reported']['cls']})"
        num["10 Cassini"] = f"use {s['G10']['cassini_use']:.3g}"
        out[f] = dict(status=st, label=lab, numbers=num)
    return out
res = dict(criteria="f3effad98c", form=FORM, KA=L("ka.json"), option_c=L("optc.json")); lines = ["SS4 (variant K, late pressure halves; option (c) table). Criteria f3effad98c. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed."]
oc = res["option_c"]
for f in FOOTS:
    lines.append(f"[{f}] option (c): R_c (Mpc) -> f_gal max (all 59 KiDS points / 0.3-1.5 Mpc subset) vs source: " + "; ".join(f"{k}: {v['f_gal_max']:.3f} / {v['f_max_0p3_1p5Mpc']:.3f} (src {oc['source_claim'][k]:.2f})" for k, v in oc["footings"][f].items()))
for V in ("K", "Kp2", "Kform"):
    t = table(V); res[V] = t
    for f in FOOTS:
        if V == "K":
            lines.append(f"[{f}] K LABEL: {t[f]['label']}   ({FORM})")
            for g, n in t[f]["numbers"].items(): lines.append(f"[{f}]   {g:16s} {t[f]['status'].get(g, 'reported'):10s} {n}")
        else: lines.append(f"[{f}] bracket {V}: {t[f]['label']}; " + "; ".join(f"{g}: {t[f]['status'][g]} {t[f]['numbers'].get(g, '')}" for g in ("1 KiDS", "2 groups", "3 X-COP", "CS cosmic shear") if g in t[f]['numbers']))
# item (4): reachability of each core at each half's sound speed (6.0 Gyr since onset), on primary halos
sys.argv = ["ss4.py", "none", "K"]
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import ss4 as S4
dyn = {}
for f in FOOTS:
    p = S4.vparK("K", f); F = p["F"]; co = L(f"vcosmo_K_{f}.json"); cs1 = co["cs1_today_kms"] if co else None; rows = []
    for Mb in (1e10, 1e11, 1e13, 1e14):
        H = S4.C.halo(Mb, F["R"], F["h"], F["Om"], z=p["z_dec"]); H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]; v = math.sqrt(S4.SV.G_KPC * H["M500"] / H["R500"])
        rc2 = H["R500"] * (p["v_stiff"] / v) ** 3; t_age = F["t_q0"]
        t1 = (p["rc1"] - H["R200"]) / (cs1 * 1.0227e-3) / 1e3 if cs1 else None          # Gyr (kpc / (km/s) -> Myr x 1e-3)
        t2 = max(rc2 - H["R200"], 0.0) / (p["v_stiff"] * 1.0227e-3) / 1e3
        rows.append(dict(M_b=Mb, v_vir=v, R200=H["R200"], R_c2=rc2, cs1=cs1, t_reach_Rc1_Gyr=t1, t_reach_Rc2_Gyr=t2, t_available_Gyr=t_age, half1_can_expand=bool(cs1 and cs1 >= v), half2_can_expand=bool(p["v_stiff"] >= v)))
    dyn[f] = rows
    lines.append(f"[{f}] item (4) dynamics (t available {F['t_q0']:.2f} Gyr): " + "; ".join(f"M_b {r['M_b']:.0e}: v_vir {r['v_vir']:.0f}, c_s1 {r['cs1']:.0f}, R_c1 2.6 Mpc reached in {r['t_reach_Rc1_Gyr']:.0f} Gyr; R_c2 {r['R_c2']:.0f} kpc in {r['t_reach_Rc2_Gyr']:.1f} Gyr" for r in rows))
res["dynamics"] = dyn
json.dump(res, open(os.path.join(HERE, "ss4.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss4.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
ml = ["SS4 MUTATE (criteria section 5)."]; bite = {}
for m in ("MK1", "MK2"):
    t = table(m); res[m] = t
    for f in FOOTS: ml.append(f"[{f}] {m}: {t[f]['label']}; " + "; ".join(f"{g}: {t[f]['status'][g]} {t[f]['numbers'].get(g, '')}" for g in ("1 KiDS", "2 groups", "3 X-COP", "CS cosmic shear")))
for f in FOOTS:
    bite[f"MK1_{f}"] = bool(res["MK1"][f]["status"]["1 KiDS"] == "FAIL")
    k = res["K"][f]["status"]; m2 = res["MK2"][f]["status"]; bite[f"MK2_{f}"] = bool(any(k[g] != m2[g] for g in ("2 groups", "3 X-COP", "CS cosmic shear") if m2[g] != "NOT RUN"))
ml.append("BITES: " + ", ".join(f"{k} {'BITES' if v else 'NO BITE'}" for k, v in bite.items()))
json.dump(dict(bites=bite), open(os.path.join(HERE, "ss4_MUTATE.json"), "w"), indent=1); open(os.path.join(HERE, "ss4_MUTATE.out"), "w").write("\n".join(ml) + "\n"); print("\n".join(ml))
