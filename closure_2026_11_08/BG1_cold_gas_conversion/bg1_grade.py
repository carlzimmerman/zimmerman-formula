#!/usr/bin/env python3
"""BG1 grader (FROZEN_CRITERIA.md d5b23bf2d4): assembles parts/expo*.json and parts/cosmic*.json into bg1.json / bg1.out and the
MUTATE twins bg1_MUTATE.json / bg1_MUTATE.out (M1 hot catalyst, M2 alpha -> 0, M3 10 x best alpha, KA replay x10).
Label rule (frozen): PASS on a footing iff one alpha passes G1-G10 (G1 includes its sub-gate G1b); FAIL iff every alpha fails at
least one gate; NO VERDICT only if a gate is NOT EVALUABLE. Both footings separately. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PARTS = os.path.join(HERE, "parts")
CRIT = "d5b23bf2d4"; FOOTS = ("canonical", "alt")
GATES = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"]
NAMES = {"G1": "SPARC rotation curves", "G1b": "SPARC gas-rich low-density discs", "G2": "KiDS isolated lenses", "G3": "X-COP", "G4": "groups",
         "G5": "Coma UDGs", "G6": "dSph (LG field, bright M31)", "G7": "ellipticals (either reading)", "G8": "forest: f_conv(z 2) <= 0.03",
         "G9": "dark ages: f_conv(z 20) <= 0.01", "G10": "growth: CMB lensing + fsigma8"}
OUT = []; MOUT = []
def P(s="", m=False): print(s, flush=True); (MOUT if m else OUT).append(str(s))
def load(name):
    p = os.path.join(PARTS, name)
    return json.load(open(p)) if os.path.exists(p) else None
EX = load("expo.json"); CO = load("cosmic.json"); EXX = load("expo_x10.json"); COX = load("cosmic_x10.json"); EXH = load("expo_hot.json")
assert EX and CO, "run bg1.py expo and bg1.py cosmic first"
ALPHAS = EX["alphas"]; assert [round(a, 9) for a in ALPHAS] == [round(a, 9) for a in CO["alphas"]]

def cells(ex_row, co_row):
    """status per gate; G1 overall = G1 and G1b."""
    c = {g: ex_row[g]["status"] for g in ("G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7")}
    c["G1"] = "PASS" if (ex_row["G1"]["status"] == "PASS" and ex_row["G1b"]["status"] == "PASS") else "FAIL"
    for g in ("G8", "G9", "G10"): c[g] = co_row[g]["status"]
    return c
def miss(ex_row, co_row):
    """normalised distance to the pass line per gate (0 when passing); used only to break ties for the best alpha."""
    m = {}
    g = ex_row["G1"]; m["G1"] = max((g["rms"] - g["rms_line"]) / 0.01, (abs(g["mean"]) - 0.05) / 0.05, 0.0)
    g = ex_row["G1b"]; m["G1b"] = max((g["rms"] - g["rms_line"]) / 0.01, (abs(g["mean"]) - 0.05) / 0.05, 0.0)
    m["G2"] = max((abs(ex_row["G2"]["shift"]) - 0.05) / 0.05, 0.0)
    g = ex_row["G3"]; m["G3"] = max((abs(g["mean"]) - 0.05) / 0.05, (g["rms"] - 0.10) / 0.10, 0.0)
    g = ex_row["G4"]; m["G4"] = max((16 - min(g["fst0"]["n_pass"], g["fst1"]["n_pass"])) / 16.0, 0.0)
    m["G5"] = max((abs(ex_row["G5"]["z"]) - 2.0) / 2.0, 0.0)
    g = ex_row["G6"]; m["G6"] = max((abs(g["LG_field"]["mean_minus_anchor"]) - 0.10) / 0.10, (abs(g["bright_M31"]["stat_subset"]) - g["bright_M31"]["line"]) / g["bright_M31"]["line"], 0.0)
    fr = ex_row["G7"]["f_ret_mean"]; m["G7"] = 0.0 if (fr <= 0.1 or fr >= 0.9) else min(fr - 0.1, 0.9 - fr) / 0.1
    m["G8"] = max((co_row["G8"]["f_conv_z2"] - 0.03) / 0.03, 0.0); m["G9"] = max((co_row["G9"]["f_conv_z20"] - 0.01) / 0.01, 0.0)
    g = co_row["G10"]; fs = max([(abs(r["Rf"] - 0.0) * 0) for r in g["fsigma8"]["rows"]] + [0.0])
    fsm = 0.0
    for r in g["fsigma8"]["rows"]:
        if not (r["in_sf"] and r["in_sfb"] and r["s8dir"]): fsm = max(fsm, 1.0)
    m["G10"] = max((g["lensing_dchi2"] - 4.0) / 4.0, fsm, 0.0)
    return m

RES = dict(criteria=CRIT, note="kappa = 1/2 FITTED; not theory closed; adopts nothing; cold dark energy, never dark matter", alphas=ALPHAS, footings={},
           inputs={f: dict(EX[f]["inputs"], **{k: CO[f]["exposures"][k] for k in ("E_dark_20_1100", "E_dark_20_800_reported", "E_igm_6_20", "E_gal_0_20", "E_gal_2_20", "E_total_z2", "E_total_z0")}) for f in FOOTS})
P(f"BG1 grade. Criteria {CRIT}. alpha grid {len(ALPHAS)} points [{ALPHAS[0]:g}, {ALPHAS[-1]:g}] (M_sun pc^-3 Gyr)^-1. R = {EX['canonical']['inputs']['R']:.6f} / {EX['alt']['inputs']['R']:.6f} (F1A); "
  f"f_cap R {EX['canonical']['inputs']['fcapR']:.4f} / {EX['alt']['inputs']['fcapR']:.4f} reported. kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing.")
best = {}
for f in FOOTS:
    R_ = {}; RES["footings"][f] = R_
    ka = dict(EX[f]["KA"]); ka["KA4_dark_ages"] = CO[f]["KA4_dark_ages"]; ka["KA5_growth_identity"] = CO[f]["KA5_growth_identity"]
    R_["KA"] = ka; ka_ok = all(v["pass_"] for v in ka.values())
    P(f"\n[{f}] known answers: " + "; ".join(f"{k} {'PASS' if v['pass_'] else 'FAIL'}" for k, v in ka.items()) + f" -> {'ALL PASS' if ka_ok else 'KA FAIL'}")
    inp = RES["inputs"][f]
    P(f"[{f}] exposures (M_sun pc^-3 Gyr): SPARC disc mass-weighted median {inp['E_sparc_massweighted_median']:.4f}, at 2.2 h median {inp['E_sparc_median_at_2p2h']:.4f} (<G> median {inp['Gbar_median']:.2f}, "
      f"disc age {inp['t_disc_Gyr']:.2f} Gyr, M_H2/M_HI median {inp['MH2_over_MHI_median']:.3f}); dark ages z 20-1100 {inp['E_dark_20_1100']:.4e} (z 20-800 {inp['E_dark_20_800_reported']:.4e}); "
      f"neutral IGM z 6-20 {inp['E_igm_6_20']:.2e}; galaxy-hosted cosmic z 0-20 {inp['E_gal_0_20']:.3e} (z 2-20 {inp['E_gal_2_20']:.3e})")
    rows = []
    for er, cr in zip(EX[f]["grid"], CO[f]["grid"]):
        assert abs(er["alpha"] - cr["alpha"]) <= 1e-9 * er["alpha"]
        c = cells(er, cr); m = miss(er, cr)
        rows.append(dict(alpha=er["alpha"], cells=c, n_pass=sum(1 for g in GATES if c[g] == "PASS"), miss_sum=float(sum(m.values())), miss=m, expo=er, cosmic=cr))
    R_["rows"] = [dict(alpha=r["alpha"], cells=r["cells"], n_pass=r["n_pass"], miss_sum=r["miss_sum"]) for r in rows]
    # windows
    win = {g: [r["alpha"] for r in rows if r["cells"][g] == "PASS"] for g in GATES}
    R_["windows"] = {g: dict(n=len(w), min=(min(w) if w else None), max=(max(w) if w else None)) for g, w in win.items()}
    allpass = [r["alpha"] for r in rows if all(r["cells"][g] == "PASS" for g in GATES if g != "G1b")]
    every_fail = [g for g in GATES if not win[g]]
    label = "PASS" if allpass else "FAIL"
    R_["label"] = label; R_["alpha_window"] = allpass; R_["gates_failing_at_every_alpha"] = every_fail
    # best alpha: most gates passed, then smallest summed miss
    nb = max(r["n_pass"] for r in rows); cand = [r for r in rows if r["n_pass"] == nb]; b = min(cand, key=lambda r: r["miss_sum"]); best[f] = b
    R_["best_alpha"] = dict(alpha=b["alpha"], n_pass=b["n_pass"], of=len(GATES), cells=b["cells"], miss=b["miss"], tie_n=len(cand), tie_alphas=[r["alpha"] for r in cand])
    # table at best alpha
    e, c = b["expo"], b["cosmic"]
    tab = {
        "G1": f"rms {e['G1']['rms']:.4f} (line {e['G1']['rms_line']:.4f}), mean {e['G1']['mean']:+.4f} (|.| <= 0.05), U_med {e['G1']['U_median']:.2f}; disc-retained median {e['G1']['fdisc_median']:.3f}; max-exposure reading rms {e['G1']['maxexp']['rms']:.4f} {'PASS' if e['G1']['maxexp']['pass_'] else 'FAIL'}",
        "G1b": f"n {e['G1b']['n']}: rms {e['G1b']['rms']:.4f} (line {e['G1b']['rms_line']:.4f}), mean {e['G1b']['mean']:+.4f}; disc-retained median {e['G1b']['fdisc_median']:.3f}",
        "G2": f"shift {e['G2']['shift']:+.4f} dex (|.| <= 0.05); lens-bin retained " + ", ".join(f"{k} {v:.3f}" for k, v in e['G2']['f_lens'].items()),
        "G3": f"c {e['G3']['c_best']:g}: mean {e['G3']['mean']:+.4f} (|.| <= 0.05), rms {e['G3']['rms']:.4f} (<= 0.10); cluster retained {e['G3']['f_cluster_mean']:.3f}; c passing {e['G3']['c_pass']}; at f_cap R (reported) mean {e['G3']['at_fcapR']['mean']:+.4f} rms {e['G3']['at_fcapR']['rms']:.4f}; uniform-b at R mean {e['G3']['uniform_b']['mean']:+.4f} rms {e['G3']['uniform_b']['rms']:.4f}",
        "G4": f"c {e['G4']['c']:g}: {e['G4']['fst0']['n_pass']}/20 (f* 0), {e['G4']['fst1']['n_pass']}/20 (f* 1) (>= 16 both); medians {e['G4']['fst0']['median_res']:+.3f} / {e['G4']['fst1']['median_res']:+.3f}; group retained f*0 {e['G4']['f_group']['0']:.3f}, f*1 {e['G4']['f_group']['1']:.3f}; c passing {e['G4']['c_pass']}",
        "G5": f"mean {e['G5']['mean']:+.4f} = {e['G5']['z']:+.2f} sigma_U (|.| <= 2); UDG retained mean {e['G5']['f_udg_mean']:.3f}",
        "G6": f"LG field mean - anchor {e['G6']['LG_field']['mean_minus_anchor']:+.4f} (|.| <= 0.10; median {e['G6']['LG_field']['median_minus_anchor']:+.4f}, retained {e['G6']['LG_field']['f_ret_mean']:.3f}) {'PASS' if e['G6']['LG_field']['pass_'] else 'FAIL'}; "
               f"bright M31 (equilibrium subset {e['G6']['bright_M31']['N_subset']}) median - anchor {e['G6']['bright_M31']['stat_subset']:+.4f} (|.| <= {e['G6']['bright_M31']['line']:.3f} = 2 sigma of ST1's +{EX[f]['m31_target']['step']:.3f}; retained {e['G6']['bright_M31']['f_ret_mean']:.3f}) {'PASS' if e['G6']['bright_M31']['pass_'] else 'FAIL'}; "
               f"MW classical (reported) {e['G6']['MW_classical_reported']['median_minus_anchor']:+.4f}; anchor {e['G6']['anchor']:+.4f}",
        "G7": f"retained {e['G7']['f_ret_mean']:.3f}: reading {e['G7']['reading']}; GB1 G4 mean plain {e['G7']['gb1_G4_mean_plain']:+.4f}, with IMF {e['G7']['gb1_G4_mean_imf']:+.4f}",
        "G8": f"f_conv(z 2) {c['G8']['f_conv_z2']:.4f} (<= 0.03)",
        "G9": f"f_conv(z 20) {c['G9']['f_conv_z20']:.4f} (<= 0.01)",
        "G10": f"CMB lensing Delta chi^2 {c['G10']['lensing_dchi2']:.2f} (<= 4; chi^2 {c['G10']['lensing_chi2']:.2f}); fsigma8 Rf " + " ".join(f"{r['bin']} {r['Rf']:.3f}" for r in c['G10']['fsigma8']['rows']) + f" -> {'PASS' if c['G10']['fsigma8']['pass_'] else 'FAIL'}",
    }
    R_["table_at_best_alpha"] = tab
    P(f"[{f}] LABEL: {label}. alpha window passing G1-G10: {allpass if allpass else 'EMPTY'}. Gates failing at EVERY alpha: {every_fail}.")
    P(f"[{f}] per-gate windows: " + "; ".join(f"{g} " + (f"[{R_['windows'][g]['min']:g}, {R_['windows'][g]['max']:g}] ({R_['windows'][g]['n']})" if win[g] else "none") for g in GATES))
    P(f"[{f}] best alpha {b['alpha']:g} ({b['n_pass']}/{len(GATES)} cells pass; {len(cand)} alphas tie on count, tie broken by summed miss):")
    for g in GATES: P(f"[{f}]   {g:4s} {b['cells'][g]:4s} {NAMES[g]}: {tab[g]}")
    # expected kills (brief): Coma UDGs, the two dSph samples, gas-rich LSB discs
    g5fail = [r["alpha"] for r in rows if r["cells"]["G5"] == "FAIL"]; g6fail = [r["alpha"] for r in rows if r["cells"]["G6"] == "FAIL"]; g1bfail = [r["alpha"] for r in rows if r["cells"]["G1b"] == "FAIL"]
    g6lg = [r["alpha"] for r in rows if not r["expo"]["G6"]["LG_field"]["pass_"]]; g6m31 = [r["alpha"] for r in rows if not r["expo"]["G6"]["bright_M31"]["pass_"]]
    def span(w): return "every alpha" if len(w) == len(ALPHAS) else ("none" if not w else f"{len(w)}/{len(ALPHAS)} alphas, failing at " + (f"[{min(w):g}, {max(w):g}]" if len(w) > 1 else f"{w[0]:g}"))
    kills = dict(coma_udgs=dict(fires=bool(len(g5fail) == len(ALPHAS)), span=span(g5fail), residual_range=[min(r["expo"]["G5"]["mean"] for r in rows), max(r["expo"]["G5"]["mean"] for r in rows)],
                                 z_range=[min(r["expo"]["G5"]["z"] for r in rows), max(r["expo"]["G5"]["z"] for r in rows)], f_ret_range=[min(r["expo"]["G5"]["f_udg_mean"] for r in rows), max(r["expo"]["G5"]["f_udg_mean"] for r in rows)]),
                 dsph_pair=dict(fires_everywhere=bool(len(g6fail) == len(ALPHAS)), span_G6=span(g6fail), span_LG_field=span(g6lg), span_bright_M31=span(g6m31),
                                LG_field_at_best=e["G6"]["LG_field"], M31_at_best=e["G6"]["bright_M31"]),
                 gas_rich_lsb=dict(fires_everywhere=bool(len(g1bfail) == len(ALPHAS)), span=span(g1bfail), n_lowdens=e["G1b"]["n"]))
    # where does G1 pass while G1b fails (the LSB discs lag)?
    lag = [r["alpha"] for r in rows if r["expo"]["G1"]["status"] == "PASS" and r["expo"]["G1b"]["status"] == "FAIL"]
    kills["gas_rich_lsb"]["alphas_where_G1_passes_but_G1b_fails"] = lag
    R_["expected_kills"] = kills
    P(f"[{f}] expected kills: Coma UDGs {'FIRE' if kills['coma_udgs']['fires'] else 'do not fire'} ({kills['coma_udgs']['span']}; residual {kills['coma_udgs']['residual_range'][0]:+.3f} to {kills['coma_udgs']['residual_range'][1]:+.3f}, "
      f"{kills['coma_udgs']['z_range'][0]:+.2f} to {kills['coma_udgs']['z_range'][1]:+.2f} sigma_U; UDG retained {kills['coma_udgs']['f_ret_range'][0]:.2f}-{kills['coma_udgs']['f_ret_range'][1]:.2f}); "
      f"dSph pair: G6 fails at {kills['dsph_pair']['span_G6']} (LG field {kills['dsph_pair']['span_LG_field']}; bright M31 {kills['dsph_pair']['span_bright_M31']}); "
      f"gas-rich LSB discs (G1b, n {e['G1b']['n']}): fail at {kills['gas_rich_lsb']['span']}; G1 passes while G1b fails at {lag if lag else 'no alpha'}")
    # disjunction: galaxy clearing vs dark ages
    g1w = win["G1"]; g9w = win["G9"]
    R_["disjunction"] = dict(G1_min_alpha=(min(g1w) if g1w else None), G9_max_alpha=(max(g9w) if g9w else None), G8_max_alpha=(max(win["G8"]) if win["G8"] else None), G10_max_alpha=(max(win["G10"]) if win["G10"] else None),
                             ratio_G1min_over_G9max=((min(g1w) / max(g9w)) if (g1w and g9w) else None),
                             E_ratio_disc_over_dark=inp["E_sparc_massweighted_median"] / inp["E_dark_20_1100"])
    d = R_["disjunction"]
    P(f"[{f}] disjunction: G1 (with G1b) passes for alpha >= {d['G1_min_alpha'] if d['G1_min_alpha'] is not None else 'never'}; G9 passes for alpha <= {d['G9_max_alpha']:g}; G8 <= {d['G8_max_alpha']:g}; G10 <= {d['G10_max_alpha'] if d['G10_max_alpha'] is not None else 'never'}; "
      f"ratio {('%.0f' % d['ratio_G1min_over_G9max']) if d['ratio_G1min_over_G9max'] else 'n/a'}; E(disc)/E(dark ages) {d['E_ratio_disc_over_dark']:.1f} (scale-free: the KA x10 replay shifts both windows alike)")

# ================================================================== MUTATE twins
RESM = dict(criteria=CRIT, note=RES["note"], footings={})
P("\n==== MUTATE (separate outputs bg1_MUTATE.*)", True)
# M3 needs 10 x best alpha; run expo on those alphas if not on the grid
m3a = sorted({10 * best[f]["alpha"] for f in FOOTS})
need = [a for a in m3a if not any(abs(a - g) <= 1e-9 * a for g in ALPHAS)]
EXM3 = load("expo_m3.json")
if need and (EXM3 is None or not all(any(abs(a - g) <= 1e-9 * a for g in EXM3["alphas"]) for a in need)):
    env = dict(os.environ, BG1_ALPHAS=",".join(f"{a:.12g}" for a in need))
    subprocess.run([sys.executable, os.path.join(HERE, "bg1.py"), "expo"], env=env, check=True, stdout=open(os.path.join(HERE, "run_expo_m3.txt"), "w"), stderr=subprocess.STDOUT)
    EXM3 = load("expo_m3.json")
def expo_row(f, alpha):
    for src in (EX, EXM3):
        if src is None: continue
        for r in src[f]["grid"]:
            if abs(r["alpha"] - alpha) <= 1e-9 * alpha: return r
    return None
for f in FOOTS:
    M = {}; RESM["footings"][f] = M
    # M1: catalyst swapped to hot gas (T > 1e6 K): must FAIL G3 at every alpha
    g3h = [r["G3"]["status"] for r in EXH[f]["grid"]] if EXH else None
    M["M1_hot_catalyst"] = dict(G3_fail_every_alpha=bool(g3h and all(s == "FAIL" for s in g3h)), G3_pass_alphas=[r["alpha"] for r in EXH[f]["grid"] if r["G3"]["status"] == "PASS"] if EXH else None,
                                E_plasma_T_gt_1e6K=EXH[f]["inputs"].get("E_plasma_T_gt_1e6K") if EXH else None, E_icm_median=EXH[f]["inputs"].get("E_icm_median") if EXH else None,
                                cluster_retained=[r["G3"]["f_cluster_mean"] for r in EXH[f]["grid"]][::10] if EXH else None, G3_mean=[r["G3"]["mean"] for r in EXH[f]["grid"]][::10] if EXH else None)
    M["M1_hot_catalyst"]["bites"] = M["M1_hot_catalyst"]["G3_fail_every_alpha"]
    P(f"[{f}] M1 hot catalyst (T > 1e6 K: ICM, IGrM, primordial plasma z 3.7e5-3.7e8): G3 FAIL at every alpha {M['M1_hot_catalyst']['G3_fail_every_alpha']} (E_plasma {M['M1_hot_catalyst']['E_plasma_T_gt_1e6K']:.0f}, E_ICM median {M['M1_hot_catalyst']['E_icm_median']:.1e}; "
      f"cluster retained {M['M1_hot_catalyst']['cluster_retained'][0]:.3f} at alpha 1e-3, {M['M1_hot_catalyst']['cluster_retained'][-1]:.3f} at 1e3; X-COP mean back to {M['M1_hot_catalyst']['G3_mean'][-1]:+.3f}) -> {'BITES' if M['M1_hot_catalyst']['bites'] else 'NO BITE'}", True)
    # M2: alpha -> 0: must FAIL G1 and G2
    M["M2_alpha0"] = EX[f]["M2_alpha0"]
    P(f"[{f}] M2 alpha -> 0 (full component in galaxies): G1 rms {M['M2_alpha0']['G1']['rms']:.4f} (line {M['M2_alpha0']['G1']['line']:.4f}) mean {M['M2_alpha0']['G1']['mean']:+.3f} FAIL {M['M2_alpha0']['G1']['fail']}; G2 shift {M['M2_alpha0']['G2']['shift']:+.3f} FAIL {M['M2_alpha0']['G2']['fail']} -> {'BITES' if M['M2_alpha0']['bites'] else 'NO BITE'}", True)
    # M3: alpha -> 10 x best alpha must flip G5 or G6
    ab = best[f]["alpha"]; a10 = 10 * ab; r0 = expo_row(f, ab); r1 = expo_row(f, a10)
    flip = dict(G5=(r0["G5"]["status"], r1["G5"]["status"]), G6=(r0["G6"]["status"], r1["G6"]["status"]),
                G6_LG=(r0["G6"]["LG_field"]["pass_"], r1["G6"]["LG_field"]["pass_"]), G6_M31=(r0["G6"]["bright_M31"]["pass_"], r1["G6"]["bright_M31"]["pass_"]))
    bites = bool(flip["G5"][0] != flip["G5"][1] or flip["G6"][0] != flip["G6"][1])
    M["M3_10x_best_alpha"] = dict(best_alpha=ab, alpha_10x=a10, flips=flip, bites=bites,
                                  G5_at=[r0["G5"]["mean"], r1["G5"]["mean"]], G6_LG_at=[r0["G6"]["LG_field"]["mean_minus_anchor"], r1["G6"]["LG_field"]["mean_minus_anchor"]],
                                  G6_M31_at=[r0["G6"]["bright_M31"]["stat_subset"], r1["G6"]["bright_M31"]["stat_subset"]],
                                  f_ret_LG=[r0["G6"]["LG_field"]["f_ret_mean"], r1["G6"]["LG_field"]["f_ret_mean"]], f_ret_M31=[r0["G6"]["bright_M31"]["f_ret_mean"], r1["G6"]["bright_M31"]["f_ret_mean"]], f_ret_udg=[r0["G5"]["f_udg_mean"], r1["G5"]["f_udg_mean"]])
    P(f"[{f}] M3 alpha {ab:g} -> {a10:g}: G5 {flip['G5'][0]} -> {flip['G5'][1]} (mean {M['M3_10x_best_alpha']['G5_at'][0]:+.3f} -> {M['M3_10x_best_alpha']['G5_at'][1]:+.3f}, UDG retained {M['M3_10x_best_alpha']['f_ret_udg'][0]:.2f} -> {M['M3_10x_best_alpha']['f_ret_udg'][1]:.2f}); "
      f"G6 {flip['G6'][0]} -> {flip['G6'][1]} (LG field {M['M3_10x_best_alpha']['G6_LG_at'][0]:+.3f} -> {M['M3_10x_best_alpha']['G6_LG_at'][1]:+.3f}, retained {M['M3_10x_best_alpha']['f_ret_LG'][0]:.2f} -> {M['M3_10x_best_alpha']['f_ret_LG'][1]:.2f}; "
      f"bright M31 {M['M3_10x_best_alpha']['G6_M31_at'][0]:+.3f} -> {M['M3_10x_best_alpha']['G6_M31_at'][1]:+.3f}, retained {M['M3_10x_best_alpha']['f_ret_M31'][0]:.2f} -> {M['M3_10x_best_alpha']['f_ret_M31'][1]:.2f}) -> {'BITES' if bites else 'NO BITE'}", True)
    # M3' (reported only, post-freeze): 10 x the smallest alpha at which G6 passes, to show the dSph row's power to alpha
    g6w = [r["alpha"] for r in EX[f]["grid"] if r["G6"]["status"] == "PASS"]
    if g6w:
        a6 = min(g6w); r6a = expo_row(f, a6); r6b = expo_row(f, 10 * a6)
        if r6b is not None:
            M["M3_reported_10x_first_G6_pass"] = dict(alpha=a6, alpha_10x=10 * a6, G6=(r6a["G6"]["status"], r6b["G6"]["status"]), G5=(r6a["G5"]["status"], r6b["G5"]["status"]),
                                                      LG=(r6a["G6"]["LG_field"]["mean_minus_anchor"], r6b["G6"]["LG_field"]["mean_minus_anchor"]), M31=(r6a["G6"]["bright_M31"]["stat_subset"], r6b["G6"]["bright_M31"]["stat_subset"]),
                                                      flips=bool(r6a["G6"]["status"] != r6b["G6"]["status"]))
            x = M["M3_reported_10x_first_G6_pass"]
            P(f"[{f}] M3' (reported, post-freeze): alpha {a6:g} -> {10 * a6:g}: G6 {x['G6'][0]} -> {x['G6'][1]} (LG field {x['LG'][0]:+.3f} -> {x['LG'][1]:+.3f}; bright M31 {x['M31'][0]:+.3f} -> {x['M31'][1]:+.3f}); G5 {x['G5'][0]} -> {x['G5'][1]} -> {'flips' if x['flips'] else 'no flip'}", True)
    # KA replay: exposure x10 must flip a gate
    flips = []
    if EXX and COX:
        for r, rx, c, cx in zip(EX[f]["grid"], EXX[f]["grid"], CO[f]["grid"], COX[f]["grid"]):
            a, b = cells(r, c), cells(rx, cx)
            for g in GATES:
                if a[g] != b[g]: flips.append((r["alpha"], g, a[g], b[g]))
    M["KA_replay_x10"] = dict(n_flips=len(flips), gates_flipped=sorted({x[1] for x in flips}), examples=flips[:12], bites=bool(flips),
                              x10_label_window=[rx["alpha"] for rx, cx in zip(EXX[f]["grid"], COX[f]["grid"]) if all(cells(rx, cx)[g] == "PASS" for g in GATES if g != "G1b")] if (EXX and COX) else None)
    P(f"[{f}] KA replay (exposure x10, criteria hash {CRIT} in every output): {len(flips)} cell flips over {sorted({x[1] for x in flips})}; x10 label window {M['KA_replay_x10']['x10_label_window'] if M['KA_replay_x10']['x10_label_window'] else 'EMPTY'} -> {'FLIPS' if flips else 'NO FLIP'}", True)
    M["all_bite"] = bool(M["M1_hot_catalyst"]["bites"] and M["M2_alpha0"]["bites"] and M["M3_10x_best_alpha"]["bites"] and M["KA_replay_x10"]["bites"])
    RES["footings"][f]["MUTATE_summary"] = dict(M1=M["M1_hot_catalyst"]["bites"], M2=M["M2_alpha0"]["bites"], M3=M["M3_10x_best_alpha"]["bites"], KA_replay=M["KA_replay_x10"]["bites"])

P("\nSUMMARY: " + "; ".join(f"{f} {RES['footings'][f]['label']} (best alpha {RES['footings'][f]['best_alpha']['alpha']:g}, {RES['footings'][f]['best_alpha']['n_pass']}/{len(GATES)}; every-alpha fails {RES['footings'][f]['gates_failing_at_every_alpha']})" for f in FOOTS))
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
RES["peak_parts"] = dict(expo_rss_GB=EX.get("peak_rss_GB"), cosmic_rss_GB=CO.get("peak_rss_GB"), expo_s=EX.get("seconds"), cosmic_s=CO.get("seconds"))
json.dump(RES, open(os.path.join(HERE, "bg1.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "bg1.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RESM, open(os.path.join(HERE, "bg1_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "bg1_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
