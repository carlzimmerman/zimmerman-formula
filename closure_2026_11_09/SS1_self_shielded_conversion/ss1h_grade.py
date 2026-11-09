#!/usr/bin/env python3
"""SS1 variant H grader (AMENDMENT_A4 8bcceec033): parts/ -> ss1h.json / ss1h.out, ss1h_MUTATE.json / .out. Gate tables through
ss1v_grade.table. H-core graded; H-full (named added form choices) and H-src (the source's g_pot) labelled beside it.
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json, math
import ss1v_grade as VG
HERE = os.path.dirname(os.path.abspath(__file__)); FOOTS = ("canonical", "alt"); L = VG.L
FORMS = {"H": "0 fitted; form choices: 1/pi, exponential escape law, G's cube root / kick factor 4 / 4 pi",
         "Hfull": "H-core's + resonant window v_vir > v_stiff/2, 180 kpc puff core, kick factor 2 (source's added forms)",
         "Hsrc": "H-core's + the source's fitted g_pot(u) = u/(0.08+u)/(1+2.5 u^1.5)"}
res = dict(amendment4="8bcceec033", criteria="b5adc7a90b", note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
lines = ["SS1 variant H (A4 8bcceec033). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed."]
for V in ("H", "Hfull", "Hsrc"):
    t = VG.table(V); res[V] = t; lo = L(f"local_V{V}.json")
    for f in FOOTS:
        lines.append(f"[{f}] {V} LABEL: {t[f]['label']}   ({FORMS[V]})")
        for g, n in t[f]["numbers"].items(): lines.append(f"[{f}]   {V} {g:24s} {t[f]['status'].get(g, 'reported'):10s} {n}")
        for k, b in t[f]["brackets_local"].items(): lines.append(f"[{f}]   {V} bracket {k:15s} " + " ".join(f"{g} {s_}" for g, s_ in b.items()))
        s = lo[f]["sets"]["primary_SIS"]; g0 = s["G2"]["fst0"]["per"]
        rr = sorted((g["R500_pre"], g["ret_R500"]) for g in g0)
        lines.append(f"[{f}]   {V} group retention inside R500 (by pre-conversion R500, f* 0): " + ", ".join(f"{r:.0f} kpc {x:.2f}" for r, x in rr[::4]) + "  (source: 42-48 % at M500 2.1e13, 79-82 % at 1.4e14; repair band 30-85 %)")
        lines.append(f"[{f}]   {V} X-COP retained/M_dyn by bin: " + ", ".join(f"{b['lo']:.2f}: {b['retained_over_Mdyn_median']:.2f} (TR1 {b['TR1_D_canonical']:.2f})" for b in s["G3"]["bins"] if b["retained_over_Mdyn_median"] is not None) + f"; TR1 shape {s['G3']['TR1_shape_reported']['RMS']:.3f} follows {s['G3']['TR1_shape_reported']['follows']}")
        lines.append(f"[{f}]   {V} KiDS per bin (0.3 / 1 / 1.5 Mpc): " + "; ".join(f"{lm}: " + "/".join(f"{v['nearest'][k]['shift']:+.3f}" for k in ('0.3 Mpc', '1.0 Mpc', '1.5 Mpc')) for lm, v in s["G1"]["per_bin"].items()) + "  (source: < +0.035)")
        cb = L(f"vcosmo_{V}_{f}.json"); lines.append(f"[{f}]   {V} converted (escaped) cosmic share of the component {cb['F_conv_today']:.3f} (of matter {cb['F_conv_today']*5.41/6.41:.3f}; source 16 %); sigma8 {cb['sigma8']:.3f}, S8 {cb['S8']:.3f} (source 0.766-0.771 / 0.78)")
json.dump(res, open(os.path.join(HERE, "ss1h.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss1h.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
ml = ["SS1 variant H MUTATE (A4 section 5)."]; bite = {}
for m in ("MH1", "MH2"):
    t = VG.table(m)
    for f in FOOTS:
        ml.append(f"[{f}] {m}: {t[f]['label']}; " + "; ".join(f"{g}: {t[f]['status'][g]} {t[f]['numbers'][g]}" for g in ("1 KiDS", "5 SPARC", "8 forest+growth")))
    res[m] = t
for f in FOOTS:
    bite[f"MH1_{f}"] = bool(res["MH1"][f]["status"]["1 KiDS"] == "FAIL" or res["MH1"][f]["status"]["5 SPARC"] == "FAIL")
    c0 = L(f"vcosmo_H_{f}.json"); c2 = L(f"vcosmo_MH2_{f}.json")
    bite[f"MH2_{f}"] = bool(c2["G8"]["status"] == "PASS" and c0["G8"]["status"] == "FAIL") or bool(c2["sigma8"] > c0["sigma8"])
ml.append("BITES: " + ", ".join(f"{k} {'BITES' if v else 'NO BITE'}" for k, v in bite.items()))
json.dump(dict(bites=bite, MH1=res["MH1"], MH2=res["MH2"]), open(os.path.join(HERE, "ss1h_MUTATE.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss1h_MUTATE.out"), "w").write("\n".join(ml) + "\n"); print("\n".join(ml))
