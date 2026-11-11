#!/usr/bin/env python3
"""WV1 grading: S3 items from runs/*.json, plus S0 (wv1_sym.json), S1 and S2 (wv1_s1s2.json), the known answers
(wv1_ka.json) and Lean (compile*.txt); MUTATE M3 and M4 applied here; labels per variant and footing, as frozen and
under AMENDMENT_A1.

Run:  python3 wv1_s3_grade.py -> wv1_grade.out, wv1_grade.json
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, json, math, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LINES, RES = [], {}


def P_(s=""):
    LINES.append(s); print(s, flush=True)


SYM = json.load(open(os.path.join(HERE, "wv1_sym.json")))
SYM_M1 = json.load(open(os.path.join(HERE, "wv1_sym_MUTATE_M1.json")))
S12 = json.load(open(os.path.join(HERE, "wv1_s1s2.json")))
KA = json.load(open(os.path.join(HERE, "wv1_ka.json")))
LEAN_OK = "exit 0" in open(os.path.join(HERE, "compile.txt")).read()
LEAN_TWIN_FAILS = "exit 1" in open(os.path.join(HERE, "compile_MUTATE.txt")).read()
RUNS = {}
for f in glob.glob(os.path.join(HERE, "runs", "*.json")):
    j = json.load(open(f)); RUNS[j["tag"]] = j

KIDS_INNER = {10.7: 362.0, 9.4: 81.0}      # FLD1 table: ONE1's inner window edge (kpc)
SPARC_RLAST = {10.7: 71.0, 9.4: 23.0}      # FLD1 table: SPARC's largest R_last within 0.25 dex (kpc)
FACS = [1, 4, 16, 64, 256, 1024, 4096]
MASSES = [10.7, 9.4]


def tag(fo, m, fac, law, extra=""):
    return f"{fo}_M{m}_f{fac}_{'law' if law else 'off'}{extra}"


P_("WV1 grading. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P_("")
# ------------------------------------------------------------------ known answers and twins
ka_sym = all(v["ok"] for v in SYM["checks"].values())
ka = {
    "KA1_C5": SYM["checks"]["KA1_C5_dispersion"]["ok"],
    "KA2_QX17_static": SYM["checks"]["KA2_constitutive"]["ok"] and SYM["checks"]["S0_law"]["ok"],
    "KA3_QG1": S12["known_answers"]["KA3_QG1_machinery"]["ok"],
    "KA4i_COL1_focus": all(v["ok"] for v in KA["KA4i"].values()),
    "KA4ii_as_frozen": KA["KA4ii_as_frozen"]["ok"],
    "KA4ii_prime_A1": all(v["ok"] for v in KA["KA4ii_prime_A1"].values()),
    "KA5_soliton": KA["KA5"]["ok"],
    "KA6_LFS1_COL1_charge": SYM["checks"]["KA6_LFS1_COL1_charge"]["ok"],
    "KA7_QX28_SPARC": "not run (S4 not graded)",
}
mut = {"M1": SYM_M1.get("bites", False), "M2": S12["M2"]["bites"], "M5": KA["M5"]["bites"],
       "Lean": LEAN_OK and LEAN_TWIN_FAILS}
P_("=== Known answers ===")
for k_, v in ka.items():
    P_(f"  {k_}: {v}")
P_(f"  (all symbolic checks pass: {ka_sym}; Lean compiles: {LEAN_OK}; Lean twin fails: {LEAN_TWIN_FAILS})")

S0_ok = all(SYM["checks"][k_]["ok"] for k_ in SYM["checks"] if k_.startswith("S0")) and ka["KA2_QX17_static"]
P_("")
P_(f"=== S0 static reduction: {'PASS' if S0_ok else 'FAIL'} (both variants, both footings; sympy residual 0) ===")

labels = {}
for fo in ("canonical", "alt"):
    P_("")
    P_(f"================ footing {fo} ================")
    nu_max = S12["S2"][fo]["nu_max_kpc_kms"]
    P_(f"S2: nu_max = {nu_max:.4g} kpc km/s (m c^2 >= {S12['S2'][fo]['m_c2_min_eV']:.3e} eV)")
    s1 = S12["S1"]
    P_(f"S1: V1 {s1['V1'][fo]}, V2 {s1['V2'][fo]}")
    # ---------------- S3 scan table
    P_("")
    P_("S3 scan (law off | law bracket): R_s = static-frame radius, min over the last-Gyr set (kpc); r_ta, r_c at z 0 (kpc);")
    P_("S3(c) = max over the last-Gyr set of Psi's mass fraction inside r_ta(z 0) with D.P > m n; M4 = same with A -> dPhi/dr")
    rows = []
    for m in MASSES:
        for fac in FACS:
            for law in (False, True):
                t_ = tag(fo, m, fac, law)
                if t_ not in RUNS:
                    rows.append((m, fac, law, None)); continue
                rows.append((m, fac, law, RUNS[t_]))
    missing = [f"{m}/{fac}/{'law' if law else 'off'}" for m, fac, law, r in rows if r is None]
    for m in MASSES:
        P_(f"  log M_b {m} (KiDS inner edge {KIDS_INNER[m]:g} kpc, SPARC R_last {SPARC_RLAST[m]:g} kpc):")
        for fac in FACS:
            ro = RUNS.get(tag(fo, m, fac, False)); rl = RUNS.get(tag(fo, m, fac, True))
            def fmt(r):
                if r is None:
                    return "missing"
                return (f"R_s {r['R_s_lastGyr_min']:.3g}, r_ta {r['r_ta_z0']:.4g}, r_c {r['r_c_lastGyr']:.3g}, "
                        f"S3(c) {r['S3c_bad_mass_frac_max']:.3f}, M4 {r['M4_bad_mass_frac_max']:.3f}, narrow {r['narrow_maxima_total']}")
            nu = ro["nu_kpc_kms"] if ro else float("nan")
            P_(f"    nu {nu:9.4g}: off [{fmt(ro)}] | law [{fmt(rl)}]")
    # ---------------- V1 items
    v1 = {}
    # S3(a)
    narrow, narrow_br = {}, {}
    for m in MASSES:      # S3(a) is graded on the primary (law-off) runs; the bracket's count is reported
        r = RUNS.get(tag(fo, m, 1, False)); narrow[str(m)] = None if r is None else r["narrow_maxima_total"]
        r = RUNS.get(tag(fo, m, 1, True)); narrow_br[str(m)] = None if r is None else r["narrow_maxima_total"]
    conv = None
    full = RUNS.get(tag(fo, 10.7, 1, False)); half = RUNS.get(tag(fo, 10.7, 1, False, "_dx0.5_z2"))
    if full is not None and half is not None:
        npz = np.load(os.path.join(HERE, "runs", tag(fo, 10.7, 1, False) + ".npz"))
        if "hist_t_Gyr" in npz.files:
            th, rc = npz["hist_t_Gyr"], npz["hist_central_over_bar"]
            t2 = full["outputs"]["z2"]["t_Gyr"]
            sel = th <= t2 + 1e-9
            peak_full = float(rc[sel].max()); c2_full = float(full["outputs"]["z2"]["central_over_bar"])
            peak_half = half["central_peak_over_bar"]; c2_half = float(half["outputs"]["z2"]["central_over_bar"]) \
                if "central_over_bar" in half["outputs"]["z2"] else half["central_end_over_bar"]
            conv = {"peak_full": peak_full, "peak_half": peak_half, "z2_full": c2_full, "z2_half": c2_half,
                    "peak_rel": abs(peak_half / peak_full - 1), "z2_rel": abs(c2_half / c2_full - 1)}
            conv["ok"] = conv["peak_rel"] <= 0.2 and conv["z2_rel"] <= 0.2
    s3a_ok = all(v == 0 for v in narrow.values() if v is not None) and None not in narrow.values() and bool(conv and conv["ok"])
    s3a_fail = any(v for v in narrow.values() if v is not None) or bool(conv is not None and not conv["ok"])
    s3a_pending = None in narrow.values() or conv is None
    v1["S3a"] = {"narrow_maxima_at_nu_max_lawoff": narrow, "narrow_maxima_bracket_reported": narrow_br, "convergence": conv,
                 "pass": s3a_ok, "pending": s3a_pending}
    P_("")
    P_(f"V1 S3(a) fold-free: narrow maxima at nu_max (law off) {narrow} [bracket, reported: {narrow_br}]; convergence "
       f"(dx/2 to z 2) {conv} -> {'PENDING' if s3a_pending and not any(v for v in narrow.values() if v) else ('PASS' if s3a_ok else 'FAIL')}")
    # S3(b) and the window, under A1 (frozen grading of the bracket) and under A1 + A2 (bracket at nu_max graded on the
    # outputs it reached, runs/<tag>_partial.json)
    XMAX_SETUP = {10.7: 4000.0, 9.4: 2500.0}

    def s3b_window(use_partial):
        def reach_ok(m, fac, force_static=False):
            ro = RUNS.get(tag(fo, m, fac, False)); rl = RUNS.get(tag(fo, m, fac, True))
            rlp = RUNS.get(tag(fo, m, fac, True) + "_partial") if (use_partial and fac == 1) else None
            if force_static:                                     # a = 1 at z 0: the run's outer physical radius
                return XMAX_SETUP[m] >= KIDS_INNER[m] and XMAX_SETUP[m] >= SPARC_RLAST[m], XMAX_SETUP[m]
            if ro is None or (rl is None and rlp is None):
                return None, None
            Rl = rl["R_s_lastGyr_min"] if rl is not None else rlp["R_s_reached_min"]
            Rs = max(ro["R_s_lastGyr_min"], Rl)
            return Rs >= KIDS_INNER[m] and Rs >= SPARC_RLAST[m], Rs
        b_at_max = {m: reach_ok(m, 1) for m in MASSES}
        fail_known = any(v[0] is False for v in b_at_max.values())        # one mass failing decides FAIL
        ok = all(v[0] is True for v in b_at_max.values())
        nu_min, dead = None, True                                          # dead: every scanned nu fails at a mass
        for fac in FACS:
            res_ = [reach_ok(m, fac) for m in MASSES]
            if all(r_[0] is True for r_ in res_):
                nu_min = (S12["S2"]["canonical"]["nu_max_kpc_kms"] * fac if fac != 1 else nu_max); dead = False; break
            if not any(r_[0] is False for r_ in res_):
                dead = False
        window = nu_min is not None and nu_min <= nu_max * (1 + 1e-12)
        status = "non-empty" if window else ("EMPTY" if (dead or fail_known) else "pending")
        m3 = {m: reach_ok(m, 1, force_static=True) for m in MASSES}
        m3_pass = all(v[0] for v in m3.values())
        return {"b_at_max": b_at_max, "fail_known": fail_known, "ok": ok, "nu_min": nu_min, "dead": dead,
                "window": window, "status": status, "M3_pass": m3_pass, "M3_bites": (not ok) and m3_pass}
    fmtR = lambda v: "pending" if v is None else f"{v:.3g} kpc"
    W = {"A1": s3b_window(False), "A1A2": s3b_window(True)}
    for rd, w_ in W.items():
        v1[f"S3b_{rd}"] = {"R_s_graded_at_nu_max": {str(m): w_["b_at_max"][m][1] for m in MASSES}, "pass": w_["ok"],
                           "fail_known": w_["fail_known"], "nu_min_kpc_kms": w_["nu_min"], "every_scanned_nu_fails": w_["dead"],
                           "window_status": w_["status"], "M3_pass": w_["M3_pass"], "M3_bites": w_["M3_bites"]}
        P_(f"V1 S3(b) [{rd}] static-frame reach at nu_max: R_s = {', '.join(f'{m}: {fmtR(w_['b_at_max'][m][1])}' for m in MASSES)} "
           f"(needs >= KiDS inner edge and SPARC R_last at both masses) -> {'PASS' if w_['ok'] else ('FAIL' if w_['fail_known'] else 'PENDING')}; "
           f"nu_min over the scan: {'none' if w_['nu_min'] is None else f'{w_['nu_min']:.4g}'}"
           f"{' (every scanned nu fails at a mass)' if w_['dead'] else ''}; window [nu_min, nu_max] {w_['status']}; "
           f"M3 (static forced everywhere) {'PASS -> BITES' if w_['M3_bites'] else 'does not bite'}")
    # S3(c)
    c_rows = {m: RUNS.get(tag(fo, m, 1, False)) for m in MASSES}
    cfr = {m: (None if r is None else r["S3c_bad_mass_frac_max"]) for m, r in c_rows.items()}
    m4fr = {m: (None if r is None else r["M4_bad_mass_frac_max"]) for m, r in c_rows.items()}
    s3c_ok = all(v is not None and v <= 0.01 for v in cfr.values())
    s3c_fail = any(v is not None and v > 0.01 for v in cfr.values())
    m4_pass = all(v is None or v <= 0.01 for v in m4fr.values()) and any(v is not None for v in m4fr.values())
    m4_bites = (not s3c_ok) and m4_pass
    med = {m: (None if r is None else r["outputs"]["g8"].get("median_absA_over_a0_inside_rta")) for m, r in c_rows.items()}
    medg = {m: (None if r is None else r["outputs"]["g8"].get("median_absA_over_g_inside_rta")) for m, r in c_rows.items()}
    v1["S3c"] = {"bad_mass_frac_max": cfr, "pass": s3c_ok, "M4_bad_mass_frac_max": m4fr, "M4_pass": m4_pass,
                 "M4_bites": m4_bites, "median_absA_over_a0_z0": med, "median_absA_over_g_z0": medg}
    P_(f"V1 S3(c) wave multi-streaming in V1: bad mass fraction {cfr} (line 0.01) -> {'PASS' if s3c_ok else 'FAIL'}; "
       f"median |A|/a0 inside r_ta at z 0 {med}, |A|/g {medg}; M4 (A -> dPhi/dr): {m4fr} -> "
       f"{'BITES' if m4_bites else 'does NOT bite (the smooth law phantom also exceeds the local Psi density)'}")
    # S3(d)
    d_rows = {m: (None if c_rows[m] is None else {"r_c": c_rows[m]["r_c_lastGyr"], "r_ta": c_rows[m]["r_ta_z0"],
                                                  "r_c_over_r_ta": c_rows[m]["r_c_over_r_ta"]}) for m in MASSES}
    v1["S3d"] = d_rows
    P_(f"S3(d) reported at nu_max (law off): {d_rows} (QX28's diffuse core: r_c/r_ta 0.15-0.26)")
    # ---------------- labels V1
    solver_ok_A1 = ka["KA4ii_prime_A1"] and ka["KA5_soliton"] and ka["KA4i_COL1_focus"] and mut["M5"]
    solver_ok_frozen = solver_ok_A1 and ka["KA4ii_as_frozen"]
    batch_done = all(RUNS.get(tag(fo, m, fac, law)) is not None for m in MASSES for fac in FACS for law in (False, True)
                     if not (fac == 1 and law))

    def v1_label(solver_ok, w_, rd):
        fails, pending = [], []
        if not S0_ok: fails.append("S0")
        if s1["V1"][fo] != "PASS": fails.append("S1")
        if s3a_fail: fails.append("S3(a)")
        elif not s3a_ok: pending.append("S3(a)")
        if w_["fail_known"]: fails.append("S3(b)")
        elif not w_["ok"]: pending.append("S3(b)")
        if s3c_fail: fails.append("S3(c)")
        elif not s3c_ok: pending.append("S3(c)")
        if w_["status"] == "EMPTY": fails.append("window")
        elif w_["status"] == "pending": pending.append("window")
        decisive = [f_ for f_ in fails if (f_ in ("S3(b)", "window") and w_["M3_bites"]) or f_ == "S3(a)"
                    or (f_ == "S3(c)" and m4_bites) or f_ in ("S0", "S1")]
        nd = [f_ for f_ in fails if f_ not in decisive]
        if not solver_ok:
            lab = "NO VERDICT (known answer KA4(ii) fails as frozen)"
        elif not decisive:
            if rd == "A1" and "S3(b)" in pending and any(RUNS.get(tag(fo, m, 1, True) + "_partial") for m in MASSES):
                lab = "NO VERDICT (S3(b): the law-bracket runs at nu_max do not finish)"
            else:
                lab = "PENDING" if pending else "NO VERDICT"
        else:
            lab = "STRUCTURE FAILS (" + ", ".join(decisive) + ")"
        if nd: lab += f"; also failing, not decisive (its MUTATE did not bite): {', '.join(nd)}"
        stopped = rd == "A1" and any(RUNS.get(tag(fo, m, 1, True) + "_partial") for m in MASSES)
        if pending and lab.startswith("STRUCTURE"):
            lab += (f"; not graded under A1 (the nu_max law brackets did not finish): {', '.join(pending)}" if stopped
                    else f"; still running: {', '.join(pending)}")
        return lab, fails, pending, decisive
    lf = v1_label(solver_ok_frozen, W["A1"], "frozen")
    la = v1_label(solver_ok_A1, W["A1"], "A1")
    lb = v1_label(solver_ok_A1, W["A1A2"], "A1A2")
    labels[("V1", fo)] = {"as_frozen": lf[0], "under_A1": la[0], "under_A1_A2": lb[0],
                          "failing_parts_A1_A2": lb[1], "pending_A1_A2": lb[2], "decisive_A1_A2": lb[3]}
    # ---------------- V2 items and label
    v2 = {"S1": s1["V2"][fo],
          "S3a": "FAIL: the frame at zero charge is mimetic dust (test shells) and focuses at COL1's time "
                 f"({KA['KA4i'][f'{fo}_10.7']['t_focus_Gyr']:.4f} / {KA['KA4i'][f'{fo}_9.4']['t_focus_Gyr']:.4f} Gyr after z 10 at log M_b 10.7 / 9.4)",
          "S3b": "FAIL: the frame's charge div P is carried with the frame (wv1_sym S1b_V2_charge, exact) and is 0 on FRW; "
                 "a regular frame that starts at P = 0 never polarizes (Lean advected_zero, regular_centre_zero): reach 0"}
    v2_fails = []
    if s1["V2"][fo] != "PASS": v2_fails.append("S1(c) FRW")
    v2_fails += ["S3(a) frame focuses", "S3(b) law never appears"]
    v2_ok_support = ka["KA3_QG1"] and mut["M2"] and ka["KA6_LFS1_COL1_charge"] and ka["KA4i_COL1_focus"] and mut["Lean"]
    lab2 = ("STRUCTURE FAILS (" + ", ".join(v2_fails) + ")") if v2_ok_support else "NO VERDICT"
    labels[("V2", fo)] = {"as_frozen": lab2, "under_A1": lab2, "failing_parts": v2_fails}
    RES[fo] = {"nu_max": nu_max, "V1": v1, "V2": v2, "missing_runs": missing}
    P_("")
    P_(f"LABEL V1 / {fo}: as frozen {labels[('V1', fo)]['as_frozen']}")
    P_(f"                 under A1 {labels[('V1', fo)]['under_A1']}")
    P_(f"                 under A1 + A2 {labels[('V1', fo)]['under_A1_A2']}")
    P_(f"LABEL V2 / {fo}: {lab2}")
    if missing:
        P_(f"  (missing runs: {missing})")

P_("")
P_("S4: NOT GRADED for either variant (S0-S3 do not all pass).")
P_(f"MUTATE: M1 {mut['M1']}, M2 {mut['M2']}, M3 per footing {[RES[f]['V1']['S3b_A1A2']['M3_bites'] for f in ('canonical', 'alt')]}, "
   f"M4 per footing {[RES[f]['V1']['S3c']['M4_bites'] for f in ('canonical', 'alt')]}, M5 {mut['M5']}, Lean twin {mut['Lean']}")
RES["labels"] = {f"{k[0]}_{k[1]}": v for k, v in labels.items()}
RES["known_answers"] = ka; RES["mutate"] = mut; RES["S0"] = S0_ok
P_("")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "wv1_grade.out"), "w").write("\n".join(LINES) + "\n")
json.dump(RES, open(os.path.join(HERE, "wv1_grade.json"), "w"), indent=1, default=str)
