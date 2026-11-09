#!/usr/bin/env python3
"""SS1 variant I grader (AMENDMENT_A5 0499ce563c): parts/ -> ss1i.json / ss1i.out, ss1i_MUTATE.json / .out. Gate tables through
ss1v_grade.table. I-core graded; I-src (the source's g_vir) and I-nob (the source's accounting: bound daughters dropped) beside it.
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math
import ss1v_grade as VG
HERE = os.path.dirname(os.path.abspath(__file__)); FOOTS = ("canonical", "alt"); L = VG.L
FORMS = {"I": "1 fitted (ceiling 1/sqrt3, chosen after SS2's over-fill); form choices: factor 3, exponential law, kick factor 1, G's cube root / 4 pi",
         "Isrc": "3 fitted (1/sqrt3 + g_vir's 0.07, 0.45); same form choices",
         "Inob": "I-core's + the source's accounting (bound daughters dropped from their system)"}
res = dict(amendment5="0499ce563c", criteria="b5adc7a90b", note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
lines = ["SS1 variant I (A5 0499ce563c). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed."]
for V in ("I", "Isrc", "Inob"):
    t = VG.table(V); res[V] = t; lo = L(f"local_V{V}.json")
    for f in FOOTS:
        lines.append(f"[{f}] {V} LABEL: {t[f]['label']}   ({FORMS[V]})")
        for g, n in t[f]["numbers"].items(): lines.append(f"[{f}]   {V} {g:24s} {t[f]['status'].get(g, 'reported'):10s} {n}")
        for k, b in t[f]["brackets_local"].items(): lines.append(f"[{f}]   {V} bracket {k:15s} " + " ".join(f"{g} {s_}" for g, s_ in b.items()))
        s = lo[f]["sets"]["primary_SIS"]; g0 = s["G2"]["fst0"]["per"]; rr = sorted((g["R500_pre"], g["ret_R500"]) for g in g0)
        lines.append(f"[{f}]   {V} group retention inside R500 (f* 0): " + ", ".join(f"{r:.0f} kpc {x:.2f}" for r, x in rr[::4]) + "  (source: 22 / 32 / 45 % at M500 2e13 / 4.5e13 / 1.4e14)")
        lines.append(f"[{f}]   {V} X-COP retained/M_dyn by bin: " + ", ".join(f"{b['lo']:.2f}: {b['retained_over_Mdyn_median']:.2f} (TR1 {b['TR1_D_canonical']:.2f})" for b in s["G3"]["bins"] if b["retained_over_Mdyn_median"] is not None) + f"; TR1 shape RMS {s['G3']['TR1_shape_reported']['RMS']:.3f} follows {s['G3']['TR1_shape_reported']['follows']}  (source: 0.71 / 0.65 / 0.46)")
        lines.append(f"[{f}]   {V} KiDS per bin (0.3 / 1 / 1.5 Mpc): " + "; ".join(f"{lm}: " + "/".join(f"{v['nearest'][k]['shift']:+.3f}" for k in ('0.3 Mpc', '1.0 Mpc', '1.5 Mpc')) for lm, v in s["G1"]["per_bin"].items()))
        cb = L(f"vcosmo_{V}_{f}.json")
        lines.append(f"[{f}]   {V} escaped share of the component {cb['F_conv_today']:.3f}; lambda {cb['lambda_today_Mpc']:.2f} Mpc; sigma8 {cb['sigma8']:.3f} (ratio {cb['sigma8_ratio_z0']:.3f}; source 0.95), S8 {cb['S8']:.3f} (source 0.769)")
sys.argv = ["x"]
import ss1v as SV, ss1_core as C
for f in FOOTS:
    p = SV.vpar("I", f); F = p["F"]; G_ = 6.6743e-11; MS = 1.98892e30; KPC = 3.0857e19; a0 = SV.A0H[f]; glaw = lambda g: 0.5 * g + math.sqrt(0.25 * g * g + a0 * g); row = []
    for lm in (11.0, 11.3, 11.5):
        Ms = 10 ** lm; out_ = {}
        for tag, am in (("primary", False), ("Moster13", True)):
            if am:
                M200 = C.moster_halo(Ms, p["z_dec"]); H = C.halo(Ms, F["R"], F["h"], F["Om"], M200=M200, Mchi=M200 * F["R"] / (1 + F["R"]), z=p["z_dec"])
            else: H = C.halo(Ms, F["R"], F["h"], F["Om"], z=p["z_dec"])
            H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]; inside = float(SV.h_enc(p, H, H["R200"] * 1.0001)) / H["Mchi0"]; sh = {}
            for Rk in (300.0, 1000.0, 1500.0):
                gN = G_ * Ms * MS / (Rk * KPC) ** 2; m = float(SV.h_enc(p, H, Rk)); sh[f"{Rk/1000:g} Mpc"] = math.log10(glaw(gN + G_ * m * MS / (Rk * KPC) ** 2) / glaw(gN))
            out_[tag] = dict(M200=H["M200"], one_halo_retained=inside, shift=sh)
        row.append((lm, out_))
    res.setdefault("kids_claims", {})[f] = row
    lines.append(f"[{f}]   I KiDS claims (1-halo retained in R200 / pointwise shift 0.3, 1, 1.5 Mpc): " + "; ".join(
        f"M* 10^{lm}: primary {o['primary']['one_halo_retained']:.3f} / " + "/".join(f"{v:+.3f}" for v in o['primary']['shift'].values())
        + f", Moster (M200 {o['Moster13']['M200']:.2g}) {o['Moster13']['one_halo_retained']:.3f} / " + "/".join(f"{v:+.3f}" for v in o['Moster13']['shift'].values()) for lm, o in row)
        + "  (source: 1.3 / 2.1 / 4.0 %; +0.038 at 1.5 Mpc)")
    lines.append(f"[{f}]   KA-I3 R_FS {p['R_FS']:.3f} Mpc (source 1.68 / 1.82)")
json.dump(res, open(os.path.join(HERE, "ss1i.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss1i.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
ml = ["SS1 variant I MUTATE (A5 section 6)."]; bite = {}
for m in ("MI1", "MI2"):
    t = VG.table(m); res[m] = t
    for f in FOOTS: ml.append(f"[{f}] {m}: {t[f]['label']}; " + "; ".join(f"{g}: {t[f]['status'][g]} {t[f]['numbers'][g]}" for g in ("1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "8 forest+growth")))
for f in FOOTS:
    s0 = L("local_VI.json")[f]["sets"]["primary_SIS"]; s1 = L("local_VMI1.json")[f]["sets"]["primary_SIS"]
    bite[f"MI1_{f}"] = bool(abs(s1["G2"]["fst0"]["median_res"] - s0["G2"]["fst0"]["median_res"]) > 0.05 or abs(s1["G3"]["mean"] - s0["G3"]["mean"]) > 0.05)
    bite[f"MI2_{f}"] = bool(res["MI2"][f]["status"]["1 KiDS"] == "FAIL" or res["MI2"][f]["status"]["5 SPARC"] == "FAIL")
ml.append("BITES: " + ", ".join(f"{k} {'BITES' if v else 'NO BITE'}" for k, v in bite.items()))
json.dump(dict(bites=bite, MI1=res["MI1"], MI2=res["MI2"]), open(os.path.join(HERE, "ss1i_MUTATE.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ss1i_MUTATE.out"), "w").write("\n".join(ml) + "\n"); print("\n".join(ml))
