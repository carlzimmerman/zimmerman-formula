#!/usr/bin/env python3
"""WD1 grade (FROZEN_CRITERIA.md 0cd6ef1dcb): assemble parts/*.json into wd1.json / wd1.out and wd1_MUTATE.json / wd1_MUTATE.out.
Label per footing by the frozen rule: PASS iff the as-written declared inputs pass G1-G10; FAIL iff they do not; NO VERDICT only
for a NOT EVALUABLE gate. The derived bracket is reported beside every gate it reaches and cannot turn a FAIL into a PASS; the
rebuilt integrator failed KA3, so a bracket PASS is written down as a number only, never credited. Hand estimates graded HIT /
MISS. kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PARTS = os.path.join(HERE, "parts"); CRIT = "0cd6ef1dcb"; NOTE = "kappa = 1/2 FITTED; not theory closed"
FOOTS = ("canonical", "alt"); REQ = ("G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10")
def L(name):
    p = os.path.join(PARTS, name); return json.load(open(p)) if os.path.exists(p) else None
KA, LOC, BUL, WEB = L("ka.json"), L("local.json"), L("bullet.json"), L("web.json")
CMB = {f: L(f"cmb_{f}.json") for f in FOOTS}
MUTS = {m: L(f"local_{m}.json") for m in ("M1", "M2", "M3")}
OUT, MOUT = [], []
def P(s=""): print(s); OUT.append(s)
def M(s=""): print(s); MOUT.append(s)
def st(x): return x["status"] if x else "NOT EVALUABLE"

def footing_table(f, tag="as_written"):
    lo = LOC[f]["sets"][tag]; s = {}; num = {}
    s["G1"] = lo["G1"]["status"]; num["G1"] = dict(rms=lo["G1"]["rms"], rms_line=lo["G1"]["rms_line"], mean=lo["G1"]["mean"], fK_median_last=lo["G1"]["fK_median_last"], fK_max_last=lo["G1"]["fK_max_last"])
    s["G1b"] = lo["G1b"]["status"]; num["G1b"] = dict(rms=lo["G1b"]["rms"], rms_line=lo["G1b"]["rms_line"], mean=lo["G1b"]["mean"], n=lo["G1b"]["n"])
    s["G2"] = lo["G2"]["status"]; num["G2"] = dict(max_abs_shift=lo["G2"]["max_abs_shift"], outer_max=lo["G2"]["outer_max_abs_shift"], outer_mean=lo["G2"]["outer_mean_shift"], mean=lo["G2"]["mean_shift"], n_fail=lo["G2"]["n_fail"], by_r=lo["G2"]["shift_by_r"], ETG_bracket_max=lo["G2_ETG_bracket"]["max_abs_shift"], ETG_bracket_status=lo["G2_ETG_bracket"]["status"])
    s["G3"] = lo["G3"]["status"]; num["G3"] = dict(mean=lo["G3"]["mean"], rms=lo["G3"]["rms"], amount=lo["G3"]["amount_status"], shape=lo["G3"]["shape_status"], bins=[(b["lo"], b["hi"], b["n"], b["mean"]) for b in lo["G3"]["bins"] if b["graded"]], c_comp=lo["G3"]["c_comp_median"], c_gas=lo["G3"]["c_gas_median"], c_need=lo["G3"]["c_need_median"],
                                                   comp_over_Mb_100kpc_median=float(np.median([c["comp_over_Mb_at_100kpc"] for c in lo["G3"]["shape"]])), comp_over_Mb_500kpc_median=float(np.median([c["comp_over_Mb_at_500kpc"] for c in lo["G3"]["shape"]])))
    s["G4"] = lo["G4"]["status"]; num["G4"] = dict(fst0=lo["G4"]["fst0"]["n_pass"], fst1=lo["G4"]["fst1"]["n_pass"], median_res=[lo["G4"]["fst0"]["median_res"], lo["G4"]["fst1"]["median_res"]], code_inputs=[lo["G4_code_inputs_reported"]["fst0"]["n_pass"], lo["G4_code_inputs_reported"]["fst1"]["n_pass"]])
    s["G5"] = lo["G5"]["status"]; num["G5"] = dict(mean=lo["G5"]["mean"], z=lo["G5"]["z"], sigma_U=lo["G5"]["sigma_U"], b_median=lo["G5"]["b_median"], capture_median=lo["G5"]["capture_median"], capture_max=lo["G5"]["capture_max"], mean_without_host=lo["G5"]["mean_without_host_component"], host_field_ratio=lo["G5"]["host_field_ratio_median"], coma_host=lo["G5"]["coma_host"], law_only=lo["G5"]["law_only_mean"])
    g6 = BUL[f]["b_gas_traced_Mach6"] if BUL and f in BUL else None; g6a = BUL[f]["a_asserted_on_galaxies"] if BUL and f in BUL else None
    s["G6"] = (g6["label"] if g6 else "NOT EVALUABLE"); num["G6"] = dict(b=g6, a=g6a)
    c = CMB[f][f] if CMB[f] and f in CMB[f] and "G7" in CMB[f][f] else None
    s["G7"] = (c["G7"]["status"] if c else "NOT EVALUABLE"); num["G7"] = (dict(c["G7"], w=c["w_as_written"], refit=c["refit"]) if c else dict(missing="cmb part missing"))
    w = WEB[f] if WEB and f in WEB and "G8" in WEB[f] else None
    s["G8"] = (w["G8"]["status"] if w else "NOT EVALUABLE"); num["G8"] = (dict(lensing_dchi2=w["G8_lensing"]["dchi2"], lensing_status=w["G8_lensing"]["status"], growth=w["G8_growth"]["status"], footing_background=w["G8_growth"]["footing_background_reported"], nonlinear_baseline=w["G8_lensing"]["nonlinear_baseline_reported"], S1h_z0=w["G8_lensing"]["S1h_z0"]) if w else dict(missing="web part missing"))
    s["G9"] = (("PASS" if w["G9"]["status"] == "PASS" else w["G9"]["status"]) if w else "NOT EVALUABLE"); num["G9"] = (dict(dchi2=w["G9"]["dchi2"], label=w["G9"]["status"], r_min=w["G9"]["r_min"], r_max=w["G9"]["r_max"], readings={k: dict(status=v["status"], dchi2=v["dchi2"]) for k, v in w["G9"]["readings"].items()}) if w else dict(missing="web part missing"))
    s["G10"] = lo["G10"]["status"]; num["G10"] = dict(M_comp_8p2kpc=lo["G10"]["M_comp_inside_8p2kpc_Msun"], rhoK=lo["G10"]["rhoK_Msun_pc3"], cassini_use=lo["G10"]["cassini_use"], worst_planet_use=lo["G10"]["worst_planet_use"], bracket=lo["G10"]["bracket_N1_d35"]["status"], cT=lo["G10"]["cT"])
    s["G9"] = "FAIL" if s["G9"] == "TENSION" else s["G9"]
    return s, num

RES = dict(criteria=CRIT, note=NOTE, footings={}, known_answers={}); MUT = dict(criteria=CRIT, note=NOTE, footings={})
P(f"WD1 grade. Criteria {CRIT}. {NOTE}; footings never pooled; adopts nothing.")
ka_ok = dict(KA1=all(KA[k]["pass_"] for k in KA if k.startswith("KA1")), KA2=KA["KA2_group_proxy"]["pass_"], KA3=KA["KA3_dynamic_integrator"]["pass_"], KA3_tensor=KA["KA3_tensor_finite_difference_check"]["pass_"],
             KA4={f: LOC[f]["KA4"]["pass_"] for f in FOOTS}, KA5={f: (CMB[f][f]["KA"]["pass_"] if CMB[f] and f in CMB[f] else None) for f in FOOTS}, KA_web={f: (WEB[f]["KA_web"]["pass_"] if WEB and f in WEB else None) for f in FOOTS}, KA_bullet=(BUL["KA_ok"] if BUL else None))
RES["known_answers"] = dict(summary=ka_ok, KA1=KA["KA1_canonical"], KA2=KA["KA2_group_proxy"], KA3=KA["KA3_dynamic_integrator"], KA3_tensor=KA["KA3_tensor_finite_difference_check"])
P(f"Known answers: KA1 {ka_ok['KA1']} (0.1168 M_b at 500 kpc; +0.0243 dex with the proposal's nu, +0.0243 with the adopted law), KA2 {ka_ok['KA2']} (R_c {KA['KA2_group_proxy']['Rc_kpc']:.1f} kpc, {KA['KA2_group_proxy']['comp_over_Mb']:.2f} M_b), "
  f"KA3 {ka_ok['KA3']} ({KA['KA3_dynamic_integrator']['mismatch']}); tensor vs finite differences {ka_ok['KA3_tensor']}; KA4 {ka_ok['KA4']}; KA5 {ka_ok['KA5']}; web identities {ka_ok['KA_web']}; Bullet law-alone {ka_ok['KA_bullet']}")
HAND = {}
for f in FOOTS:
    s, num = footing_table(f, "as_written"); sb, numb = footing_table(f, "bracket_dynamic"); sn, numn = footing_table(f, "proposal_nu_reported"); sm, numm = footing_table(f, "monotone_reported")
    ne = [g for g in REQ if s[g] == "NOT EVALUABLE"]; npass = sum(1 for g in REQ if s[g] == "PASS")
    label = "PASS" if all(s[g] == "PASS" for g in REQ) else ("NO VERDICT" if ne and all(s[g] in ("PASS", "NOT EVALUABLE") for g in REQ) else "FAIL")
    g3b = num["G3"]["bins"]; inner = [b for b in g3b if b[0] == 0.0]
    hand = dict(outer_KiDS_0p2_0p4_dex=dict(value=num["G2"]["outer_max"], hit=bool(0.2 <= num["G2"]["outer_max"] <= 0.45 and s["G2"] == "FAIL")),
                XCOP_inner_bin_below_m0p2=dict(value=inner[0][3] if inner else None, hit=bool(inner and inner[0][3] < -0.2)),
                Coma_UDGs_plus_1p1_dex=dict(value=num["G5"]["mean"], hit=bool(abs(num["G5"]["mean"] - 1.1) <= 0.2 and s["G5"] == "FAIL")),
                forest_FAIL=dict(value=num["G9"].get("dchi2"), hit=bool(s["G9"] == "FAIL")))
    kills = dict(KiDS_outer_bins=s["G2"] != "PASS", Coma_UDGs=s["G5"] != "PASS", XCOP_per_bin_shape=num["G3"]["shape"] != "PASS", forest=s["G9"] != "PASS", Bullet_b=s["G6"] != "PASS", primary_CMB_at_4p40=s["G7"] != "PASS")
    RES["footings"][f] = dict(label=label, n_pass=npass, not_evaluable=ne, status=s, num=num, bracket_status={g: sb[g] for g in ("G1", "G1b", "G2", "G3", "G4", "G5", "G10")}, bracket_num={g: numb[g] for g in ("G2", "G3", "G4", "G5", "G10")},
                              proposal_nu_status={g: sn[g] for g in ("G1", "G1b", "G2", "G3", "G4", "G5", "G10")}, proposal_nu_num={g: numn[g] for g in ("G1", "G2", "G3", "G4", "G5")}, monotone_status={g: sm[g] for g in ("G3", "G4")}, monotone_num={g: numm[g] for g in ("G3", "G4")},
                              hand_estimates=hand, expected_kills=kills, baselines=LOC[f]["baselines"], KA4=dict(LOC[f]["KA4"], law_only_set=None), G1c=LOC[f]["sets"]["as_written"]["G1c"], G5b=LOC[f]["sets"]["as_written"]["G5b_dsph_reported"],
                              bracket_runs=LOC[f].get("bracket_runs"))
    P(f"\n== {f}: LABEL {label}. {npass} of {len(REQ)} gates pass as written; not evaluable {ne}")
    P("  as written : " + " ".join(f"{g} {s[g][0]}" for g in REQ))
    P("  bracket    : " + " ".join(f"{g} {sb[g][0]}" for g in ("G1", "G1b", "G2", "G3", "G4", "G5", "G10")) + "   (dynamic integrator, one event, d_sep0 = R500 / 40 kpc, 3:2; KA3 failed, reported only)")
    P("  proposal nu: " + " ".join(f"{g} {sn[g][0]}" for g in ("G1", "G1b", "G2", "G3", "G4", "G5", "G10")) + "   (reported, never graded)")
    n = num
    P(f"  G1 rms {n['G1']['rms']:.4f} (line {n['G1']['rms_line']:.4f}) mean {n['G1']['mean']:+.4f}, component/M_b at the last point median {n['G1']['fK_median_last']:.2e} max {n['G1']['fK_max_last']:.2e}; G1b rms {n['G1b']['rms']:.4f} (line {n['G1b']['rms_line']:.4f}) n {n['G1b']['n']}")
    P(f"  G2 max |shift| {n['G2']['max_abs_shift']:.3f}, outer (>= 0.3 Mpc) max {n['G2']['outer_max']:.3f} mean {n['G2']['outer_mean']:+.3f}, {n['G2']['n_fail']} of 59 over 0.05; by radius " + json.dumps({k: round(v, 3) if v is not None else None for k, v in n['G2']['by_r'].items()}) + f"; ETG bracket max {n['G2']['ETG_bracket_max']:.3f} ({n['G2']['ETG_bracket_status']}); dynamic bracket max {numb['G2']['max_abs_shift']:.3f}")
    P(f"  G3 {n['G3']['mean']:+.3f}/{n['G3']['rms']:.3f} (amount {n['G3']['amount']}, shape {n['G3']['shape']}); bins r/R500 " + " ".join(f"[{b[0]:.2f}-{b[1]:.2f}] n{b[2]} {b[3]:+.3f}" for b in n['G3']['bins']) + f"; concentration M(<0.25)/M(<0.7 R500) component {n['G3']['c_comp']:.2f} gas {n['G3']['c_gas']:.2f} need {n['G3']['c_need']:.2f}; component/M_b inside 100 kpc {n['G3']['comp_over_Mb_100kpc_median']:.2f}, 500 kpc {n['G3']['comp_over_Mb_500kpc_median']:.2f}")
    P(f"     bracket G3 {numb['G3']['mean']:+.3f}/{numb['G3']['rms']:.3f} bins " + " ".join(f"{b[3]:+.3f}" for b in numb['G3']['bins']) + f"; monotone reading {numm['G3']['mean']:+.3f}/{numm['G3']['rms']:.3f} ({sm['G3']}); proposal nu {numn['G3']['mean']:+.3f}/{numn['G3']['rms']:.3f}")
    P(f"  G4 {n['G4']['fst0']}/{n['G4']['fst1']} of 20 (median residual {n['G4']['median_res'][0]:+.3f} / {n['G4']['median_res'][1]:+.3f}); code inputs N 4.5 d 420: {n['G4']['code_inputs']}; bracket {numb['G4']['fst0']}/{numb['G4']['fst1']}; monotone {numm['G4']['fst0']}/{numm['G4']['fst1']}")
    P(f"  G5 {n['G5']['mean']:+.3f} dex ({n['G5']['z']:+.2f} sigma_U, sigma_U {n['G5']['sigma_U']:.3f}); capture median {n['G5']['capture_median']:.1e} max {n['G5']['capture_max']:.1e}, b median {n['G5']['b_median']:.4f}; without Coma's component in the external field {n['G5']['mean_without_host']:+.3f}; host field x {n['G5']['host_field_ratio']:.2f}; Coma R500 {n['G5']['coma_host']['R500_kpc']:.0f} kpc, law-implied M_b {n['G5']['coma_host']['Mb_tot_law_implied']:.2e}; law only {n['G5']['law_only']:+.3f}; bracket {numb['G5']['mean']:+.3f}")
    b6 = n["G6"]["b"]; a6 = n["G6"]["a"]
    if b6: P(f"  G6 (b) gas-traced Mach-6 fluid: {b6['label']} cls {b6['cls']}; M300 {b6['M300'][0]/1e14:.2f}, {b6['M300'][1]/1e14:.2f} e14 (Z {b6['ZM'][0]:+.2f}, {b6['ZM'][1]:+.2f}); dkappa {b6['dkappa'][0]:+.3f}, {b6['dkappa'][1]:+.3f}; peak-to-gal {b6['d_gal'][0]:.0f}, {b6['d_gal'][1]:.0f} kpc, peak-to-gas {b6['d_gas'][0]:.0f}, {b6['d_gas'][1]:.0f} kpc"
             f"\n  G6 (a) asserted on the galaxies: {a6['label']} cls {a6['cls']}; M300 {a6['M300'][0]/1e14:.2f}, {a6['M300'][1]/1e14:.2f} e14 (Z {a6['ZM'][0]:+.2f}, {a6['ZM'][1]:+.2f}); dkappa {a6['dkappa'][0]:+.3f}, {a6['dkappa'][1]:+.3f}; peak-to-gal {a6['d_gal'][0]:.0f}, {a6['d_gal'][1]:.0f} kpc")
    g7 = n["G7"]
    if "status" in g7: P(f"  G7 w {g7['w']:.4f}: dchi2 {g7['dchi2_norefit']:+.1f} no refit, {g7['dchi2_refit']:+.1f} after the 5-parameter refit ({g7['refit']['five_parameter_footing_background']['nfev']} evals), {g7['dchi2_refit_proposal_background']:+.1f} on the proposal's own background (od = 4.40 ob) -> {g7['status']}")
    g8 = n["G8"]; g9 = n["G9"]
    if "lensing_dchi2" in g8: P(f"  G8 growth {g8['growth']} (cold dust before shell-crossing: by construction; footing-background reading lensing dchi2 {g8['footing_background']['lensing_dchi2']:.2f}, fs8 {'PASS' if g8['footing_background']['fs8']['pass_'] else 'FAIL'} Rf {[round(r['Rf'], 3) for r in g8['footing_background']['fs8']['rows']]}); lensing with 1.6 Mpc cores dchi2 {g8['lensing_dchi2']:+.2f} -> {g8['lensing_status']} (nonlinear-baseline reading {g8['nonlinear_baseline']['dchi2']:+.2f}); S_1h(z0) {json.dumps({k: round(v, 3) for k, v in g8['S1h_z0'].items()})}")
    if "dchi2" in g9: P(f"  G9 forest {g9['label']} dchi2 {g9['dchi2']:.1f}, P1D ratio [{g9['r_min']:.3f}, {g9['r_max']:.3f}]; sharper k^4 form {g9['readings']['sharper_k4_reported']['status']} {g9['readings']['sharper_k4_reported']['dchi2']:.1f}")
    P(f"  G10 {s['G10']}: component inside 8.2 kpc {n['G10']['M_comp_8p2kpc']:.3g} Msun, rho {n['G10']['rhoK']:.2e} Msun/pc^3, Cassini use {n['G10']['cassini_use']:.2e}, worst planet {n['G10']['worst_planet_use']:.2e}; N 1 d 35 bracket {n['G10']['bracket']}; c_T {n['G10']['cT']}")
    P("  hand estimates: " + "; ".join(f"{k} {'HIT' if v['hit'] else 'MISS'} ({v['value'] if v['value'] is None else round(v['value'], 3)})" for k, v in hand.items()))
    P("  expected kills: " + "; ".join(f"{k} {'FIRES' if v else 'does not fire'}" for k, v in kills.items()))
    g1c = RES["footings"][f]["G1c"]; P("  G1c (informational): " + "; ".join(f"{k}: law chi2 {v['law_only']:.1f} -> {v['with_component']:.1f} with the component (f_K at the last point {v['fK_last']:.1e})" for k, v in g1c.items()))
    g5b = RES["footings"][f]["G5b"]; P("  G5b (reported): " + "; ".join(f"{k}: n {v['n']}, law residual median {v['median_D_law']:+.3f}, component shift median {v['median_shift']:+.1e} max {v['max_shift']:+.1e}, capture max {v['capture_max']:.1e}" for k, v in g5b.items()))
    # ---------------- MUTATE
    m = {}
    def gate_of(part, g):
        if part is None or f not in part or "sets" not in part[f]: return None
        return part[f]["sets"]["as_written"][g]
    m1 = {g: gate_of(MUTS["M1"], g) for g in ("G1", "G2", "G3")}
    m["M1_Rc0_50kpc"] = dict(G1=st(m1["G1"]), G1_rms=m1["G1"]["rms"] if m1["G1"] else None, G1_fK_median_last=m1["G1"]["fK_median_last"] if m1["G1"] else None, G2=st(m1["G2"]), G2_max=m1["G2"]["max_abs_shift"] if m1["G2"] else None,
                              bites=bool(m1["G1"] and m1["G2"] and m1["G1"]["status"] == "FAIL" and m1["G2"]["status"] == "FAIL"))
    m2 = {g: gate_of(MUTS["M2"], g) for g in ("G3", "G4")}
    m["M2_Wcrit_inf"] = dict(G3=st(m2["G3"]), G3_mean=m2["G3"]["mean"] if m2["G3"] else None, G3_rms=m2["G3"]["rms"] if m2["G3"] else None, G3_as_written_mean=num["G3"]["mean"], G3_law_only_mean=LOC[f]["baselines"]["xcop_law_only"]["mean"],
                             G4=st(m2["G4"]), G4_n=[m2["G4"]["fst0"]["n_pass"], m2["G4"]["fst1"]["n_pass"]] if m2["G4"] else None, comp_over_Mb_500kpc_median=float(np.median([c["comp_over_Mb_at_500kpc"] for c in m2["G3"]["shape"]])) if m2["G3"] else None,
                             bites=bool(m2["G3"] and m2["G4"] and m2["G3"]["status"] == "FAIL" and m2["G4"]["status"] == "FAIL"))
    m3 = MUTS["M3"]; k4 = LOC[f]["KA4"]
    if m3 and f in m3 and "sets" in m3[f]:
        z = m3[f]["sets"]["as_written"]; b_ = LOC[f]["baselines"]
        ok = (abs(z["G1"]["rms"] - b_["sparc_qx8"]["rms"]) <= 1e-6 and z["G2"]["max_abs_shift"] <= 1e-6 and abs(z["G3"]["mean"] - b_["gb1_L0_xcop"][0]) <= 1e-6 and [z["G4"]["fst0"]["n_pass"], z["G4"]["fst1"]["n_pass"]] == b_["groups_gb1_L0"]
              and abs(z["G5"]["mean_without_host_component"] - b_["gb1_L0_udg"]) <= 1e-6 and z["G1"]["status"] == "PASS" and z["G2"]["status"] == "PASS" and z["G10"]["status"] == "PASS" and z["G3"]["status"] == "FAIL" and z["G4"]["status"] == "FAIL" and z["G5"]["status"] == "FAIL")
        m["M3_f_0"] = dict(G1=z["G1"]["status"], G1_rms=z["G1"]["rms"], G2=z["G2"]["status"], G3=z["G3"]["status"], G3_mean=z["G3"]["mean"], G4=z["G4"]["status"], G4_n=[z["G4"]["fst0"]["n_pass"], z["G4"]["fst1"]["n_pass"]], G5=z["G5"]["status"], G5_mean=z["G5"]["mean_without_host_component"], G10=z["G10"]["status"], KA4_in_main_run=k4["pass_"], bites=bool(ok))
    else: m["M3_f_0"] = dict(bites=False, missing="local_M3.json")
    m["criteria_in_outputs"] = bool(all(x and x.get("criteria") == CRIT for x in (KA, LOC, BUL, WEB, CMB["canonical"], CMB["alt"], MUTS["M1"], MUTS["M2"], MUTS["M3"])))
    MUT["footings"][f] = m
    M(f"\n== {f} MUTATE")
    x = m["M1_Rc0_50kpc"]; M(f"  M1 R_c0 -> 50 kpc: G1 {x['G1']} (rms {x['G1_rms']}, component/M_b at the last point median {x['G1_fK_median_last']}), G2 {x['G2']} (max |shift| {x['G2_max']}) -> {'BITES' if x['bites'] else 'NO BITE'}")
    x = m["M2_Wcrit_inf"]; M(f"  M2 W_crit -> inf: G3 {x['G3']} ({x['G3_mean']:+.4f}/{x['G3_rms']:.4f}; as written {x['G3_as_written_mean']:+.4f}, law only {x['G3_law_only_mean']:+.4f}; component/M_b inside 500 kpc median {x['comp_over_Mb_500kpc_median']:.3f}), G4 {x['G4']} {x['G4_n']} -> {'BITES' if x['bites'] else 'NO BITE'}")
    x = m["M3_f_0"]; M(f"  M3 f -> 0 (KA4 replay): " + json.dumps({k: v for k, v in x.items() if k != 'bites'}) + f" -> {'BITES' if x['bites'] else 'NO BITE'}")
    M(f"  criteria hash in every output: {m['criteria_in_outputs']}")
RES["labels"] = {f: RES["footings"][f]["label"] for f in FOOTS}; MUT["bites"] = {f: {k: v["bites"] for k, v in MUT["footings"][f].items() if isinstance(v, dict)} for f in FOOTS}
RES["compute"] = dict(local_s=LOC["seconds"], local_rss_GB=LOC["peak_rss_GB"], mutants_s={m: (MUTS[m]["seconds"] if MUTS[m] else None) for m in MUTS}, web_s=(WEB["seconds"] if WEB else None), web_rss_GB=(WEB["peak_rss_GB"] if WEB else None),
                      cmb_s={f: (CMB[f]["seconds"] if CMB[f] else None) for f in FOOTS}, cmb_rss_GB={f: (CMB[f]["peak_rss_GB"] if CMB[f] else None) for f in FOOTS}, cmb_refit_evals=(CMB["canonical"]["refit_budget_evals"] if CMB["canonical"] else None),
                      bullet_s=(BUL["seconds"] if BUL else None), bullet_child_rss_MB=(BUL["child_peak_rss_MB"] if BUL else None))
RES["declared"] = LOC.get("declared")
P(f"\nLABELS: canonical {RES['labels']['canonical']} / alt {RES['labels']['alt']}. {NOTE}. Adopts nothing.")
P("compute: " + json.dumps(RES["compute"]))
json.dump(RES, open(os.path.join(HERE, "wd1.json"), "w"), indent=1, default=float); json.dump(MUT, open(os.path.join(HERE, "wd1_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "wd1.out"), "w").write("\n".join(OUT) + "\n"); open(os.path.join(HERE, "wd1_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
