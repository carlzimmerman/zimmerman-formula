#!/usr/bin/env python3
"""DF3_fluid_next_gates: reads the lane's JSON, applies the frozen labels, writes df3g.out and df3g_summary.json. No new computation. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
def _fx(o):
    if isinstance(o, dict): return {k: _fx(v) for k, v in o.items()}
    if isinstance(o, list): return [_fx(v) for v in o]
    if o in ("inf", "-inf", "nan"): return float(o)
    return o
J = lambda f: _fx(json.load(open(os.path.join(HERE, f))))
OUT = []; P = lambda s="": OUT.append(str(s))
CELLS = [(1.0, 100.0), (5 / 3, 100.0), (1.0, 30.0), (5 / 3, 30.0), (2 / 3, 30.0)]; NAME = {1.0: "1", 5 / 3: "5/3", 2 / 3: "2/3"}
FEET = ("canonical", "alt"); G = 4.30091e-6
ctl = J("df3g_controls.json"); ctm = J("df3g_controls_MUTATE.json"); sc = J("df3g_selfcheck.json"); law = J("df3g_law.json"); bu = J("df3g_bullet.json"); bum = J("df3g_bullet_MUTATE.json"); mu = J("df3g_run_MUTATE.json")
SUM = dict(cells={}, law={}, controls={})
P("DF3_fluid_next_gates, read of the lane's outputs. Criteria FROZEN_CRITERIA.md, A1. kappa = 1/2 FITTED; footings canonical 9.3603e-11, alt 1.1312e-10, never pooled. Not theory closed.")
P(""); P("== Controls")
for k, v in ctl.items():
    if k != "all": P(f"  {k}: {'PASS' if v['passed'] else 'FAIL'} {json.dumps({a: b for a, b in v.items() if a != 'passed'}, default=float)[:240]}")
P(f"  selfcheck vs the other lane's S and law limit: {'PASS' if sc['all'] else 'FAIL'} {json.dumps(sc, default=float)[:300]}")
for k, v in bu["controls"].items(): P(f"  Bullet {k}: {'PASS' if v['passed'] else 'FAIL'} {json.dumps({a: b for a, b in v.items() if a != 'passed'}, default=float)[:300]}")
le = ctl["K_LE_5_3"]["rho_c"]; lem = ctm["K_LE_5_3"]["rho_c"]
mut = dict(LE_fails=not ctm["K_LE_5_3"]["passed"], LE_ratio=lem / le, LE_expect=64.0, LE_ratio_ok=abs(lem / le / 64 - 1) < .05, xcop_bites=mu["bites"], xcop=[mu["mean"], mu["fairx01"]], bullet_control_fails=not bum["controls"]["K_gas_sign"]["passed"])
mut["all_bite"] = all(mut[k] for k in ("LE_fails", "LE_ratio_ok", "xcop_bites", "bullet_control_fails"))
P(f"  MUTATE: {json.dumps(mut, default=float)}")
ok = ctl["all"] and sc["all"] and bu["control_ok"] and mut["all_bite"]; SUM["controls"] = dict(all=ok, mutate=mut); P(f"  ALL CONTROLS {'PASS' if ok else 'FAIL: NO VERDICT'}")
P(""); P("== The a0 law without fluid")
for f in FEET:
    L = law[f]; g = L["G3"]; b = bu["law"][f]; SUM["law"][f] = dict(X=[L["X"]["mean"], L["X"]["rms"]], K=L["K"]["n_pass"], S=[g["rms"], g["Y"], g["tilt"]], lens={c: L["lens"][c]["Z"] for c in L["lens"]}, bullet=b["cls"])
    P(f"  {f}: X-COP {L['X']['mean']:+.3f} {L['X']['rms']:.3f}; keys {L['K']['n_pass']} of 15 {L['K']['failing']}; SPARC {g['rms']:.4f} U {g['Y']:.2f} tilt {g['tilt']:+.2f}; SB Z {g['hs']:+.2f}; LT {g['lt']:+.3f}; groups {g['groups']:+.2f} {g['groups_cls']}; IC Z {g['ic_Z']:+.1f}; dwarfs {[round(v, 2) for v in g['dwarfs'].values()]}; lensing Z blue {L['lens']['blue']['Z']:+.1f} red {L['lens']['red']['Z']:+.1f}; MW X5 line {L['MW']['n_pass']} of {L['MW']['n_cells']}; Bullet {b['cls']} M300 {[round(x / 1e14, 2) for x in b['M300']]} dk {b['main']['dkappa']:+.3f} {b['sub']['dkappa']:+.3f}")
def tov_share(R, f):
    Mt = R.get("M_TOV_Msun");
    if not Mt: return None
    return sum(v["fair"] > Mt for v in R["X"][f]["valid"]) / len(R["X"][f]["valid"])
for g, s in CELLS:
    tag = f"G{g:.3f}_s{s:g}"; R = J(f"df3g_cell_{tag}_N.json"); RS = J(f"df3g_cell_{tag}_S.json"); B = bu["cells"][tag]; cs = {}; SUM["cells"][tag] = cs
    P(""); P(f"== Gamma {NAME[g]}, sigma {s:g} km/s, omega_f/omega_b {R['Rf']:.3f}" + (f", M_TOV {R['M_TOV_Msun']:.2e} Msun" if R.get("M_TOV_Msun") else ""))
    for f in FEET:
        X = R["X"][f]; XC = R["XC"][f]; K = R["K"][f]; w = R["G3"][f]; wc = R["G3C"][f]; D = R["D"][f]; M = R["MW"][f]; Ln = R["lens"][f]; V = X["valid"]; ts = tov_share(R, f)
        bins = [D[k] for k in ("150-200", "200-250")]; ne_d = max(b["noeq"] for b in bins)
        disc = bool(w["S"] and w["Tl"] and all(b["ok"] for b in bins) and ne_d < .10); clus = bool(X["passed"] and K["n_pass"] == 15 and R["X_noeq"][f] < .10 and K["noeq"] < .10)
        rows = B["rows"]; bH = rows[f"N|{f}|4700|H"]; bC = rows[f"N|{f}|4700|C"]; bul = bH["grade"]["cls"] != "FAIL"
        McM = M["mcmillan"]; Mb = 6.6e10; vcC = math.sqrt(McM["vc"] ** 2 + G * max(R["Rf"] * Mb - McM["Mf8"], 0) / 8.122) if McM["noeq"] else McM["vc"]
        cs[f] = dict(disc=disc, clusters=clus, bullet=bul, X=[X["mean"], X["rms"], R["X_noeq"][f]], XC=XC["mean"], K=[K["n_pass"], K["noeq"]], S=[w["rms"], w["Y"], w["tilt"], w["sparc_noeq"]], SC=[wc["rms"], wc["Y"], wc["tilt"]], D2={k: [D[k]["gamma"], D[k].get("Z"), D[k]["noeq"]] for k in ("150-200", "200-250")}, MW=[M["n_vc_kz"], M["n_all"], M["n_noeq"], McM["vc"], McM["K0"], vcC], lens={c: Ln[c]["Z"] for c in Ln}, bullet_H=[bH["label"], bH["grade"]["cls"], bH["grade"]["M300"], bH["grade"]["main"]["dkappa"], bH["grade"]["sub"]["dkappa"]], bullet_C=[bC["label"], bC["grade"]["cls"], bC["grade"]["M300"], bC["grade"]["main"]["dkappa"], bC["grade"]["sub"]["dkappa"]], tov_share=ts)
        P(f"  {f}  N reading")
        P(f"    C1 X-COP held {X['mean']:+.3f} {X['rms']:.3f} {'PASS' if X['passed'] else 'FAIL'}{' (fails past HSE 0.12 too)' if X['hse_clear'] else ''}; NO EQ {R['X_noeq'][f]:.2f}; collapsed {XC['mean']:+.3f} {XC['rms']:.3f}; by x {[round(v, 2) for v in X['by_x'].values()]}; M_f/M_b {[round(v, 3) for v in X['mfmb'].values()]}")
        P(f"       validity: median GM/(R_half c^2) {sorted(v['gm'] for v in V)[len(V) // 2]:.2e}, c_s centre/c {sorted(v['csc'] for v in V)[len(V) // 2]:.2e}, R_half {sorted(v['rhalf_kpc'] for v in V)[len(V) // 2]:.3g} kpc, held/fair {sorted(v['held'] / v['fair'] for v in V)[len(V) // 2]:.2e}" + (f"; fair share above M_TOV in {ts:.2f} of X-COP: NO EQUILIBRIUM (GR)" if ts is not None else ""))
        P(f"    C2 keys {K['n_pass']} of 15, failing {K['failing']}, worst {K['worst']}, NO EQ {K['noeq']:.2f}" + (f"; B=1 {K['B1']['n_pass']}, n(z) {K['nz']['n_pass']}" if "B1" in K else ""))
        P(f"    D1 SPARC held {w['rms']:.4f} U {w['Y']:.2f} tilt {w['tilt']:+.2f} {'PASS' if w['S'] and w['Tl'] else 'FAIL'}, NO EQ {w['sparc_noeq']:.2f}; collapsed {wc['rms']:.4f} U {wc['Y']:.2f} tilt {wc['tilt']:+.2f}")
        for k in ("150-200", "200-250"):
            b = D[k]; P(f"    D2 {k}: M_f/M_b outer third {b['gamma']:.3f}, Z {b['Z']:+.2f} {'PASS' if b['ok'] else 'FAIL'}, NO EQ {b['noeq']:.2f}, retained {b['retained']:.3f}, R_half/R_last {b['rhalf_RL']:.3g}; Jeans lambda/R_d at R_d, 2R_d, R_last {[round(b['lam'][i]['lamJ_over_Rd'], 2) for i in ('0', '1', '2')]}, rho there {[float('%.2g' % b['lam'][i]['rho']) for i in ('0', '1', '2')]} Msun/pc^3, c_s {[round(b['lam'][i]['cs'], 1) for i in ('0', '1', '2')]}")
        P(f"       other bins M_f/M_b, NO EQ: {[(k, round(D[k]['gamma'], 3), round(D[k]['noeq'], 2)) for k in D if k not in ('150-200', '200-250')]}")
        P(f"    D3 SB Z {w['hs']:+.2f}, LT {w['lt']:+.3f} (NO EQ {w['lt_noeq']:.2f}), groups {w['groups']:+.2f} {w['groups_cls']} (NO EQ {w['groups_noeq']:.2f}); IC 1613 Z {w['ic_Z']:+.1f}; dwarfs {[round(v, 2) for v in w['dwarfs'].values()]} (NO EQ {w['dw_noeq']:.2f})")
        P(f"    D4 MW: {M['n_vc_kz']} of {M['n_cells']} cells pass V_c and K_z chi2, {M['n_all']} also K_z(R0); NO EQ {M['n_noeq']}; median V_c {M['med_vc']:.1f}, K_z(R0) {M['med_K0']:.1f}, fluid rho(R0) {M['med_rho0']:.2e} Msun/pc^3; McMillan-like V_c {McM['vc']:.1f} K_z(R0) {McM['K0']:.1f}, collapsed V_c {vcC:.0f}; Ou {M['Ou']}")
        P(f"    Lensing Z blue {Ln['blue']['Z']:+.1f} (law {Ln['blue']['Z_law']:+.1f}), red {Ln['red']['Z']:+.1f} (law {Ln['red']['Z_law']:+.1f}); Gamma at window {Ln['blue']['Gamma']:.3f}, {Ln['red']['Gamma']:.3f}; NO EQ {Ln['blue']['noeq']}, {Ln['red']['noeq']}")
        for mode, bb in (("H", bH), ("C", bC)):
            st = bb["stat"]; gr = bb["grade"]; P(f"    Bullet {mode}, 4700 km/s: {bb['label']}; with galaxies main {st['main']['with_galaxies']:.2f} sub {st['sub']['with_galaxies']:.2f}; Mach centre {st['main']['mach_centre']:.3g}, {st['sub']['mach_centre']:.3g}, at half mass {st['main']['mach_half']:.3g}, {st['sub']['mach_half']:.3g}; ram/P at half mass {st['main']['ram_over_P_half']:.2g}, {st['sub']['ram_over_P_half']:.2g}; subsonic share {st['main']['subsonic_share']:.2f}, {st['sub']['subsonic_share']:.2f}; held {[float('%.3g' % x) for x in bb['held']]} of fair {[float('%.3g' % x) for x in bb['fair']]}; UX6 class {gr['cls']}, M300 {[round(x / 1e14, 2) for x in gr['M300']]} (Z {[round(z, 1) for z in gr['ZO3']]}), peaks from gas/BCG main {gr['main']['d_gas']:.0f}/{gr['main']['d_bcg']:.0f}, sub {gr['sub']['d_gas']:.0f}/{gr['sub']['d_bcg']:.0f} kpc, dkappa {gr['main']['dkappa']:+.3f} {gr['sub']['dkappa']:+.3f}")
        b4 = rows[f"N|{f}|4000|H"]; P(f"    Bullet H at 4000 km/s: {b4['label']}, class {b4['grade']['cls']}, Mach half {b4['stat']['main']['mach_half']:.3g}, {b4['stat']['sub']['mach_half']:.3g}")
        P(f"    labels: discs {'YES' if disc else 'no'}, clusters {'YES' if clus else 'no'}, Bullet {'not FAIL' if bul else 'FAIL'}")
        x = RS["X"][f]; ws = RS["G3"][f]; bs = rows[f"S|{f}|4700|H"]
        P(f"  {f}  S reading: X-COP held {x['mean']:+.3f} {x['rms']:.3f} NO EQ {RS['X_noeq'][f]:.2f}, collapsed {RS['XC'][f]['mean']:+.3f}; SPARC {ws['rms']:.4f} U {ws['Y']:.2f} tilt {ws['tilt']:+.2f} NO EQ {ws['sparc_noeq']:.2f}; groups {ws['groups']:+.2f} {ws['groups_cls']}; Bullet masses held {[float('%.3g' % v) for v in bs['held']]}, {bs['label']}")
    mg = B["mg1"]["canonical"]; P(f"  MG1 pairs, canonical, PROVISIONAL inputs: " + "; ".join(f"{q['system']} {q['sub']}: stays H {q['stays_H']:.2f} C {q['stays_C']:.2f}, M_f(<300)/M_lens H {q['Mf300_over_Mlens_H']:.2f} C {q['Mf300_over_Mlens_C']:.2f}{' NOEQ' if q['noeq'] else ''}{' GR' if q['gr_noeq'] else ''}" for q in mg))
try:
    O = J("../DF3_barotrope_settling/df3_cell_G1.000_s100.json"); P(""); P(f"S keys, READ from DF3_barotrope_settling: (1, 100) {O['K']['canonical']['n_pass']} of 15")
except Exception as e: P(f"S keys READ failed: {e}")
P(""); P("== Lane label, primary (1, 100), reading N, canonical")
c = SUM["cells"]["G1.000_s100"]["canonical"]; lab = ("HOLDS AT DISCS, CLUSTERS AND BULLET" if c["disc"] and c["clusters"] and c["bullet"] else "/".join(n for n, k in (("DISCS ONLY", "disc"), ("CLUSTERS ONLY", "clusters"), ("BULLET ONLY", "bullet")) if c[k]) or "NO GATE")
if not ok: lab = "NO VERDICT (failed control): " + lab
same = sum(1 for t, v in SUM["cells"].items() if t != "G1.000_s100" and (v["canonical"]["disc"], v["canonical"]["clusters"], v["canonical"]["bullet"]) == (c["disc"], c["clusters"], c["bullet"]))
SUM["label"] = lab; SUM["others_same"] = same; P(f"  {lab}; {same} of the other four cells read the same")
P("kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.")
open(os.path.join(HERE, "df3g.out"), "w").write("\n".join(OUT) + "\n"); json.dump(SUM, open(os.path.join(HERE, "df3g_summary.json"), "w"), indent=1, sort_keys=True, default=float); print("\n".join(OUT))
