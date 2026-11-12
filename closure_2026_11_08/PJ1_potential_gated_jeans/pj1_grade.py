#!/usr/bin/env python3
"""PJ1 grade (FROZEN_CRITERIA.md e3c9bc7d3c): assemble parts/*.json into pj1.json / pj1.out and pj1_MUTATE.json / pj1_MUTATE.out.
Label per footing by the frozen rule: PASS iff one grid point (or the as-written point) passes G1-G10; FAIL iff none; NO VERDICT only
for a NOT EVALUABLE gate. M3 (R_J0 -> 10 R_J0 at the best point) and the KA replay (Phi_* x 10 at the best point) are run here as
--points jobs of pj1.py (local and web) when their parts are missing. kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PARTS = os.path.join(HERE, "parts"); CRIT = "e3c9bc7d3c"; NOTE = "kappa = 1/2 FITTED; not theory closed"
FOOTS = ("canonical", "alt"); FORMS = ("T", "C"); ELLS = ("0.0", "1.5", "3.0"); ASW = dict(RJ0=1.4, PHS=1.5e-6, p=2, form=None, ell="1.5")
REQ = ("G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10")
def L(name): return json.load(open(os.path.join(PARTS, name)))
def pkey(pt): return f"{pt['form']}|RJ0 {pt['RJ0']:g}|PHS {pt['PHS']:g}|p {pt['p']:g}"
JOBS = {}
def launch_points(which, pts, tag):
    """one --points job of pj1.py per (which, tag); the M3 and KA-replay jobs of both footings run concurrently (each < 0.4 GB RSS)."""
    fn = os.path.join(PARTS, f"{which}_points_{tag}.json")
    if not os.path.exists(fn) and (which, tag) not in JOBS:
        JOBS[(which, tag)] = subprocess.Popen([sys.executable, os.path.join(HERE, "pj1.py"), which, "--points", json.dumps(pts), "--tag", tag], stdout=open(os.path.join(HERE, f"run_{which}_{tag}.txt"), "w"), stderr=subprocess.STDOUT)
def run_points(which, pts, tag):
    launch_points(which, pts, tag)
    if (which, tag) in JOBS:
        rc = JOBS.pop((which, tag)).wait()
        if rc != 0: raise RuntimeError(f"{which} --points {tag} exited {rc}")
    return L(f"{which}_points_{tag}.json")
LOC, M1L, WEB, BUL = L("local.json"), L("local_M1.json"), L("web.json"), L("bullet.json")
if os.path.exists(os.path.join(PARTS, "cmb.json")): CMB = L("cmb.json")
else:   # one process per footing
    CMB = L("cmb_canonical.json"); CMB.update({k: v for k, v in L("cmb_alt.json").items() if k == "alt"})
OUT, MOUT = [], []
def P(s=""): print(s); OUT.append(s)
def M(s=""): print(s); MOUT.append(s)

def g7_of(f, PHS, p):
    rows = [r for r in CMB[f]["grid"] if abs(r["PHS"] - PHS) < 1e-12 and r["p"] == p]
    if not rows: return dict(status="NOT EVALUABLE", dchi2=None, missing="Phi_* value outside the CMB grid")
    r = rows[0]; d = r["dchi2"]; st = r["status"]; refit = None
    for k, v in CMB[f].get("refit", {}).items():
        if abs(v["PHS"] - PHS) < 1e-12 and v["p"] == p and "dchi2_refit" in v: refit = v; st = v["status"]; d = v["dchi2_refit"]
    return dict(status=st, dchi2=d, dchi2_norefit=r["dchi2"], refit=refit, w_at_k=r["w_at_k"])
def g6_of(f, PHS, p):
    k = f"PHS {PHS:g}|p {p:g}"; m = BUL["grid_map"][f].get(k)
    if m is None: return dict(status="NOT EVALUABLE", missing="Phi_* value outside the Bullet map")
    return dict(status="PASS" if m["label"] == "PASS" else "FAIL", S_over_R=m["S_over_R"], cls=m["cls"], dkappa=m["dkappa"], depth_c2=m["depth_c2"])
def cell(f, lo, we, ell, pt):
    """statuses and misses of every gate at one grid point x ell."""
    g1 = lo["G1_by_ell"][ell]; st = {}; miss = {}; num = {}
    st["G1"] = g1["G1"]["status"]; miss["G1"] = max(g1["G1"]["rms"] / g1["G1"]["rms_line"] - 1, abs(g1["G1"]["mean"]) / 0.05 - 1, 0); num["G1"] = dict(rms=g1["G1"]["rms"], mean=g1["G1"]["mean"], rms_line=g1["G1"]["rms_line"], neg_geff=g1["negative_geff_fraction"])
    st["G1b"] = g1["G1b"]["status"]; miss["G1b"] = max(g1["G1b"]["rms"] / g1["G1b"]["rms_line"] - 1, abs(g1["G1b"]["mean"]) / 0.05 - 1, 0); num["G1b"] = dict(rms=g1["G1b"]["rms"], mean=g1["G1b"]["mean"], rms_line=g1["G1b"]["rms_line"], n=g1["G1b"]["n"])
    st["G2"] = lo["G2"]["status"]; miss["G2"] = max(lo["G2"]["max_abs_shift"] / 0.05 - 1, 0); num["G2"] = dict(max_abs_shift=lo["G2"]["max_abs_shift"], outer_max=lo["G2"]["outer_max_abs_shift"], mean_shift=lo["G2"]["mean_shift"], n_fail=lo["G2"]["n_fail"])
    st["G3"] = lo["G3"]["status"]; miss["G3"] = max(abs(lo["G3"]["mean"]) / 0.05 - 1, lo["G3"]["rms"] / 0.10 - 1, 0); num["G3"] = dict(mean=lo["G3"]["mean"], rms=lo["G3"]["rms"], c_K=lo["G3"]["c_K_median"], c_gas=lo["G3"]["c_gas_median"], c_b=lo["G3"]["c_b_median"], c_need=lo["G3"]["c_need_median"])
    st["G4"] = lo["G4"]["status"]; nmin = min(lo["G4"]["fst0"]["n_pass"], lo["G4"]["fst1"]["n_pass"]); miss["G4"] = max((16 - nmin) / 16, 0); num["G4"] = dict(fst0=lo["G4"]["fst0"]["n_pass"], fst1=lo["G4"]["fst1"]["n_pass"], median_res=lo["G4"]["fst0"]["median_res"])
    st["G5"] = lo["G5"]["status"]; miss["G5"] = max(abs(lo["G5"]["z"]) / 2 - 1, 0); num["G5"] = dict(mean=lo["G5"]["mean"], z=lo["G5"]["z"], b=lo["G5"]["b_median"])
    g6 = g6_of(f, pt["PHS"], pt["p"]); st["G6"] = g6["status"]; miss["G6"] = 0.0 if g6["status"] == "PASS" else 1.0; num["G6"] = g6
    g7 = g7_of(f, pt["PHS"], pt["p"]); st["G7"] = g7["status"]; miss["G7"] = max((g7["dchi2"] or 0) / 10 - 1, 0); num["G7"] = dict(dchi2=g7["dchi2"], dchi2_norefit=g7.get("dchi2_norefit"), refit=bool(g7.get("refit")))
    st["G8"] = we["G8"]["status"]; miss["G8"] = max(we["G8"]["lensing_dchi2"] / 4 - 1, 0) + (0 if we["G8"]["fsigma8"]["pass_"] else 1); num["G8"] = dict(lensing_dchi2=we["G8"]["lensing_dchi2"], fs8_pass=we["G8"]["fsigma8"]["pass_"], Rf=[r["Rf"] for r in we["G8"]["fsigma8"]["rows"]])
    st["G9"] = "PASS" if we["G9"]["status"] == "PASS" else we["G9"]["status"]; miss["G9"] = max(we["G9"]["dchi2"] / 4 - 1, 0); num["G9"] = dict(dchi2=we["G9"]["dchi2"], label=we["G9"]["status"], r_min=we["G9"]["r_min"], r_max=we["G9"]["r_max"])
    st["G10"] = lo["G10"]["status"]; miss["G10"] = 0.0 if st["G10"] == "PASS" else 1.0; num["G10"] = dict(cassini_use=lo["G10"]["cassini_use"], worst_planet_use=lo["G10"]["worst_planet_use"], rhoK_Msun_pc3=lo["G10"]["rhoK_Msun_pc3"], S_over_R_R0=lo["G10"]["S_over_R_R0"])
    npass = sum(1 for g in REQ if st[g] == "PASS"); ne = [g for g in REQ if st[g] == "NOT EVALUABLE"]
    return dict(point=dict(pt, ell=float(ell)), status=st, miss=miss, num=num, n_pass=npass, all_pass=bool(npass == len(REQ)), not_evaluable=ne, miss_sum=float(sum(miss.values())),
                G1c=lo.get("G1c"), fK_median_last=lo.get("fK_median_last"), fK_max_last=lo.get("fK_max_last"))

RES = dict(criteria=CRIT, note=NOTE, footings={}); MUT = dict(criteria=CRIT, note=NOTE, footings={}); BEST = {}; ASW_CELLS = {}
P(f"PJ1 grade. Criteria {CRIT}. {NOTE}; footings never pooled; adopts nothing.")
P(f"Known answers: local {[(f, all(v['pass_'] for v in LOC[f]['KA'].values())) for f in FOOTS]}; web {[(f, WEB[f]['KA5_identity']['pass_']) for f in FOOTS]}; "
  f"cmb {[(f, CMB[f]['KA']['pass_']) for f in FOOTS]}; bullet KA5 {BUL['KA5_ok']}; forest data md5 ok {WEB['forest_data']['md5_ok']}, {WEB['forest_data']['nbins']} bins")
for f in FOOTS:
    locg = {pkey(o["point"]): o for o in LOC[f]["grid"]}; webg = {pkey(o["point"]): o for o in WEB[f]["grid"]}
    cells = []
    for k, lo in locg.items():
        we = webg[k]
        for ell in ELLS: cells.append(cell(f, lo, we, ell, lo["point"]))
    passing = [c for c in cells if c["all_pass"]]; ne_cells = [c for c in cells if c["not_evaluable"]]
    best = max(cells, key=lambda c: (c["n_pass"], -c["miss_sum"]))
    label = "PASS" if passing else ("NO VERDICT" if (not passing and ne_cells and all(c["not_evaluable"] for c in cells)) else "FAIL")
    # the as-written point: both forms, ell 1.5 (the local as_written entries carry the per-point lens tables)
    asw = {}
    for form in FORMS:
        lo = LOC[f]["as_written"][form]; we = WEB[f]["as_written"][form]; pt = dict(ASW, form=form); asw[form] = cell(f, lo, we, ASW["ell"], pt)
        asw[form]["R4.4_reported"] = dict(G3=LOC[f]["as_written"][form + "_R4.4_reported"]["G3"]["status"], G3_mean=LOC[f]["as_written"][form + "_R4.4_reported"]["G3"]["mean"], G3_rms=LOC[f]["as_written"][form + "_R4.4_reported"]["G3"]["rms"],
                                            G2_max=LOC[f]["as_written"][form + "_R4.4_reported"]["G2"]["max_abs_shift"], G4=[LOC[f]["as_written"][form + "_R4.4_reported"]["G4"]["fst0"]["n_pass"], LOC[f]["as_written"][form + "_R4.4_reported"]["G4"]["fst1"]["n_pass"]],
                                            G5_mean=LOC[f]["as_written"][form + "_R4.4_reported"]["G5"]["mean"], G7_dchi2=CMB[f]["as_written_variants_reported"]["R_cmb 4.4 reported (weight x 4.4/R)"]["dchi2"])
        asw[form]["web_total_potential_reading"] = dict(G8=WEB[f]["as_written"][form + "_total_potential_reading"]["G8"]["status"], G8_dchi2=WEB[f]["as_written"][form + "_total_potential_reading"]["G8"]["lensing_dchi2"],
                                                        G9=WEB[f]["as_written"][form + "_total_potential_reading"]["G9"]["status"], G9_dchi2=WEB[f]["as_written"][form + "_total_potential_reading"]["G9"]["dchi2"])
        asw[form]["lens_points"] = lo["G2"]["points"]
    # per-gate windows (grid cells passing)
    win = {g: int(sum(1 for c in cells if c["status"][g] == "PASS")) for g in REQ}
    # the killing gate: at the best point the failing gate with the largest normalised miss; at the as-written, every failing gate
    kill_best = max([g for g in REQ if best["status"][g] != "PASS"], key=lambda g: best["miss"][g], default=None)
    # expected kills
    ek = {}
    for form in FORMS:
        a = asw[form]; g7 = a["num"]["G7"]
        ek[form] = dict(G7_damping_tail=dict(fires=bool(a["status"]["G7"] != "PASS"), dchi2=g7["dchi2"], dchi2_norefit=g7["dchi2_norefit"], w_at_k=CMB[f]["grid"][[i for i, r in enumerate(CMB[f]["grid"]) if abs(r["PHS"] - ASW["PHS"]) < 1e-12 and r["p"] == ASW["p"]][0]]["w_at_k"]),
                        G2_outer_bins=dict(fires=bool(a["status"]["G2"] != "PASS"), outer_max_abs_shift=a["num"]["G2"]["outer_max"], max_abs_shift=a["num"]["G2"]["max_abs_shift"], n_fail=a["num"]["G2"]["n_fail"],
                                           S_over_R_30kpc_by_bin=LOC[f]["as_written"][form]["G2"]["S_over_R_30kpc_by_bin"], depth_c2_30kpc_by_bin=LOC[f]["as_written"][form]["G2"]["depth_c2_30kpc_by_bin"]),
                        G3_G6_gas_shape=dict(G3_fires=bool(a["status"]["G3"] != "PASS"), G3=a["num"]["G3"], G6_fires=bool(a["status"]["G6"] != "PASS"), G6=a["num"]["G6"]))
    F = dict(label=label, n_cells=len(cells), n_pass_all=len(passing), windows=win, best=best, killing_gate_best=kill_best, as_written=asw, expected_kills=ek,
             cmb_refit=CMB[f].get("refit"), cmb_phi_rms=CMB[f]["phi_rms_table"], cmb_variants=CMB[f]["as_written_variants_reported"], bullet=BUL[f], web_phi=WEB[f]["phi_web_table"],
             baselines=LOC[f]["baselines"], KA=dict(local=LOC[f]["KA"], web=WEB[f]["KA5_identity"], cmb=CMB[f]["KA"]))
    RES["footings"][f] = F
    P(f"\n== {f}: LABEL {label}. {len(passing)} of {len(cells)} grid cells pass all gates; per-gate passing cells {win}")
    for form in FORMS:
        a = asw[form]; P(f"  as-written form {form} (ell 1.5, R {LOC[f]['as_written'][form]['R']:.3f}): " + " ".join(f"{g} {a['status'][g][0]}" for g in REQ) + f"; n_pass {a['n_pass']}")
        n = a["num"]; P(f"    G1 rms {n['G1']['rms']:.4f} (line {n['G1']['rms_line']:.4f}) mean {n['G1']['mean']:+.3f} neg-g_eff {n['G1']['neg_geff']:.3f}; G1b rms {n['G1b']['rms']:.4f} (line {n['G1b']['rms_line']:.4f}) n {n['G1b']['n']}; G2 max |shift| {n['G2']['max_abs_shift']:.3f} outer {n['G2']['outer_max']:.3f} mean {n['G2']['mean_shift']:+.3f} ({n['G2']['n_fail']} points over 0.05)")
        P(f"    G3 {n['G3']['mean']:+.3f}/{n['G3']['rms']:.3f}, concentration M(<0.25)/M(<0.7 R500): component {n['G3']['c_K']:.3f}, gas {n['G3']['c_gas']:.3f}, baryons {n['G3']['c_b']:.3f}, need (HSE) {n['G3']['c_need']:.3f}; G4 {n['G4']['fst0']}/{n['G4']['fst1']} of 20; G5 {n['G5']['mean']:+.3f} ({n['G5']['z']:+.2f} sigma_U), b {n['G5']['b']:.2f}")
        P(f"    G6 cls {n['G6'].get('cls')} dkappa {n['G6'].get('dkappa')} S/R {n['G6'].get('S_over_R', float('nan')):.3f}; G7 dchi2 {n['G7']['dchi2']:+.1f} (no refit {n['G7']['dchi2_norefit']:+.1f}, refit {n['G7']['refit']}); G8 lensing dchi2 {n['G8']['lensing_dchi2']:.2f} fs8 {n['G8']['fs8_pass']} Rf {[round(x, 3) for x in n['G8']['Rf']]}; G9 {n['G9']['label']} dchi2 {n['G9']['dchi2']:.1f}; G10 Cassini use {n['G10']['cassini_use']:.2e} rho_K {n['G10']['rhoK_Msun_pc3']:.2e} Msun/pc^3")
        P(f"    reported R 4.4: G3 {a['R4.4_reported']['G3']} {a['R4.4_reported']['G3_mean']:+.3f}/{a['R4.4_reported']['G3_rms']:.3f}, G2 max {a['R4.4_reported']['G2_max']:.3f}, G4 {a['R4.4_reported']['G4']}, G5 {a['R4.4_reported']['G5_mean']:+.3f}, G7 dchi2 {a['R4.4_reported']['G7_dchi2']:+.1f}; "
          f"total-potential web reading: G8 {a['web_total_potential_reading']['G8']} {a['web_total_potential_reading']['G8_dchi2']:.2f}, G9 {a['web_total_potential_reading']['G9']} {a['web_total_potential_reading']['G9_dchi2']:.1f}")
        if a["G1c"]: P(f"    G1c (informational): " + "; ".join(f"{k}: law chi2 {v['law_only']:.1f}, with component+ell " + ", ".join(f"ell {e}: {x:.1f}" for e, x in v['by_ell'].items()) + f", fK {v['fK_last']:.1e}" for k, v in a["G1c"].items()))
    b = best; P(f"  best grid point {pkey(b['point'])} ell {b['point']['ell']:g}: {b['n_pass']} of {len(REQ)} gates pass; " + " ".join(f"{g} {b['status'][g][0]}" for g in REQ) + f"; killing gate {kill_best} (miss {b['miss'][kill_best]:.2f})" if kill_best else "")
    n = b["num"]; P(f"    G1 rms {n['G1']['rms']:.4f}/{n['G1']['rms_line']:.4f} mean {n['G1']['mean']:+.3f}; G1b {n['G1b']['rms']:.4f}/{n['G1b']['rms_line']:.4f}; G2 max {n['G2']['max_abs_shift']:.3f} outer {n['G2']['outer_max']:.3f}; G3 {n['G3']['mean']:+.3f}/{n['G3']['rms']:.3f}; G4 {n['G4']['fst0']}/{n['G4']['fst1']}; G5 {n['G5']['mean']:+.3f} ({n['G5']['z']:+.2f}); "
      f"G6 {n['G6'].get('cls')}; G7 {n['G7']['dchi2']:+.1f}; G8 {n['G8']['lensing_dchi2']:.2f} fs8 {n['G8']['fs8_pass']}; G9 {n['G9']['dchi2']:.1f}; G10 {b['status']['G10']}")
    P(f"  expected kills (as-written): " + "; ".join(f"form {fm}: G7 {'FIRES' if ek[fm]['G7_damping_tail']['fires'] else 'does not fire'} (dchi2 {ek[fm]['G7_damping_tail']['dchi2']:+.0f}), G2 outer {'FIRES' if ek[fm]['G2_outer_bins']['fires'] else 'no'} ({ek[fm]['G2_outer_bins']['outer_max_abs_shift']:.3f} dex), "
                                                       f"G3 {'FIRES' if ek[fm]['G3_G6_gas_shape']['G3_fires'] else 'no'} / G6 {'FIRES' if ek[fm]['G3_G6_gas_shape']['G6_fires'] else 'no'}" for fm in FORMS))
    BEST[f] = b; ASW_CELLS[f] = asw
    bp = dict(RJ0=b["point"]["RJ0"], PHS=b["point"]["PHS"], p=b["point"]["p"], form=b["point"]["form"]); p3 = dict(bp, RJ0=10 * bp["RJ0"]); pk = dict(bp, PHS=10 * bp["PHS"])
    for which in ("local", "web"): launch_points(which, [p3], f"M3_{f}"); launch_points(which, [pk], f"KA_{f}")
for f in FOOTS:
    b = BEST[f]
    # ---------------- MUTATE
    m = {}
    # M1: inverted gate at the as-written point must FAIL G1 or G2
    m1 = M1L[f]["as_written"]; m1c = {form: dict(G1=m1[form]["G1_by_ell"][ASW["ell"]]["G1"]["status"], G1_ell0=m1[form]["G1_by_ell"]["0.0"]["G1"]["status"], G2=m1[form]["G2"]["status"], G2_max=m1[form]["G2"]["max_abs_shift"], G3=m1[form]["G3"]["status"], G3_mean=m1[form]["G3"]["mean"]) for form in FORMS}
    m["M1_inverted_gate"] = dict(cells=m1c, bites=bool(all(c["G1"] == "FAIL" or c["G2"] == "FAIL" for c in m1c.values())))
    m["M2_S_to_0"] = dict(LOC[f]["M2_S0"], bites=LOC[f]["M2_S0"]["bites"])
    # M3: R_J0 -> 10 R_J0 at the best point must flip G2 or G8
    bp = dict(RJ0=b["point"]["RJ0"], PHS=b["point"]["PHS"], p=b["point"]["p"], form=b["point"]["form"]); p3 = dict(bp, RJ0=10 * bp["RJ0"]); pk = dict(bp, PHS=10 * bp["PHS"])
    L3 = run_points("local", [p3], f"M3_{f}"); W3 = run_points("web", [p3], f"M3_{f}"); LK = run_points("local", [pk], f"KA_{f}"); WK = run_points("web", [pk], f"KA_{f}")
    lo3 = L3[f]["grid"][0]; we3 = W3[f]["grid"][0]; c3 = cell(f, lo3, we3, str(b["point"]["ell"]), p3)
    m["M3_RJ0_x10"] = dict(point=p3, G2_best=b["status"]["G2"], G2_x10=c3["status"]["G2"], G2_max_best=b["num"]["G2"]["max_abs_shift"], G2_max_x10=c3["num"]["G2"]["max_abs_shift"], G8_best=b["status"]["G8"], G8_x10=c3["status"]["G8"],
                           G8_dchi2_best=b["num"]["G8"]["lensing_dchi2"], G8_dchi2_x10=c3["num"]["G8"]["lensing_dchi2"], bites=bool(c3["status"]["G2"] != b["status"]["G2"] or c3["status"]["G8"] != b["status"]["G8"]),
                           all_status_x10={g: c3["status"][g] for g in REQ})
    lok = LK[f]["grid"][0]; wek = WK[f]["grid"][0]; ck = cell(f, lok, wek, str(b["point"]["ell"]), pk); flips = [g for g in REQ if ck["status"][g] != b["status"][g]]
    m["KA_replay_PHS_x10"] = dict(point=pk, flips=flips, status_best={g: b["status"][g] for g in REQ}, status_x10={g: ck["status"][g] for g in REQ}, bites=bool(flips), criteria_in_outputs=all(x.get("criteria") == CRIT for x in (LOC, M1L, WEB, CMB, BUL, L3, W3, LK, WK)))
    MUT["footings"][f] = m
    M(f"\n== {f} MUTATE")
    M(f"  M1 gate inverted (as-written): " + "; ".join(f"form {fm}: G1(ell 1.5) {c['G1']}, G1(ell 0) {c['G1_ell0']}, G2 {c['G2']} (max {c['G2_max']:.3f}), G3 {c['G3']} ({c['G3_mean']:+.3f})" for fm, c in m1c.items()) + f" -> {'BITES' if m['M1_inverted_gate']['bites'] else 'NO BITE'}")
    M(f"  M2 S -> 0: X-COP {m['M2_S_to_0']['G3']['mean']:+.4f}/{m['M2_S_to_0']['G3']['rms']:.4f} -> {'BITES' if m['M2_S_to_0']['bites'] else 'NO BITE'}")
    x = m["M3_RJ0_x10"]; M(f"  M3 R_J0 x10 at the best point ({pkey(bp)} -> R_J0 {p3['RJ0']:g}): G2 {x['G2_best']} ({x['G2_max_best']:.3f}) -> {x['G2_x10']} ({x['G2_max_x10']:.3f}); G8 {x['G8_best']} ({x['G8_dchi2_best']:.2f}) -> {x['G8_x10']} ({x['G8_dchi2_x10']:.2f}) -> {'BITES' if x['bites'] else 'NO BITE'}")
    x = m["KA_replay_PHS_x10"]; M(f"  KA replay Phi_* x10 at the best point: flips {x['flips']} -> {'BITES' if x['bites'] else 'NO BITE'}; criteria hash in every output: {x['criteria_in_outputs']}")
RES["labels"] = {f: RES["footings"][f]["label"] for f in FOOTS}; MUT["bites"] = {f: {k: v["bites"] for k, v in MUT["footings"][f].items()} for f in FOOTS}
RES["compute"] = dict(local_s=LOC["seconds"], local_rss_GB=LOC["peak_rss_GB"], web_s=WEB["seconds"], web_rss_GB=WEB["peak_rss_GB"], cmb_s=CMB["seconds"], cmb_rss_GB=max(CMB["peak_rss_GB"], L("cmb_alt.json")["peak_rss_GB"] if os.path.exists(os.path.join(PARTS, "cmb_alt.json")) else 0), cmb_refit_evals=CMB.get("refit_budget_evals"), bullet_s=BUL["seconds"], bullet_child_rss_MB=BUL["child_peak_rss_MB"])
P(f"\nLABELS: canonical {RES['labels']['canonical']} / alt {RES['labels']['alt']}. {NOTE}. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, "pj1.json"), "w"), indent=1, default=float); json.dump(MUT, open(os.path.join(HERE, "pj1_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "pj1.out"), "w").write("\n".join(OUT) + "\n"); open(os.path.join(HERE, "pj1_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
