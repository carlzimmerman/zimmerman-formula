#!/usr/bin/env python3
"""DR9 (FROZEN_CRITERIA.md): galaxy-dependent energy coupling on the response, NR3's path. UR1, SL1, NF1, NR2, NR3 read only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, re, subprocess, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); NR3 = os.path.join(RB, "NR3_ur1_on_nr2"); TG = ("A_c2b_refit", "B_cfg886_bg"); OUT = []
ROWS = ("C0", "CINF", "RET_C1", "RET_CM1", "RET_FIT", "STAR_C1", "STAR_CM1", "STAR_FIT", "RET_FIT_AFTER", "MUTATE", "MUTATE_A1")
def P(s): print(s, flush=True); OUT.append(s)
def rp(n): return os.path.join(HERE, f"dr9_row_{n}.json")
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); r10, r11 = J["r10"], J["r11"]
if not all(os.path.exists(rp(n)) for n in ROWS):
    W = os.path.join(HERE, "cache_MEDIAN"); os.makedirs(W, exist_ok=True); PRE = re.search(r'pre = (""".*?""")', open(os.path.join(UR1, "ur1.py")).read(), re.S).group(1); t = open(os.path.join(UR1, "ur1_tail.py")).read(); i = t.index("import time as _tm"); tl = os.path.join(W, "dr9_tail_joined.py"); open(tl, "w").write(t[:i] + open(os.path.join(HERE, "dr9_tail.py")).read())
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(eval(PRE)) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, "NR2_MEDIAN_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "dr9_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=os.path.join(W, "unused.json"), DR9_HERE=HERE, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", UR1_DRIVER="1")
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(HERE, "dr9_run.log"), "a"), stderr=subprocess.STDOUT)
    if not all(os.path.exists(rp(n)) for n in ROWS): raise SystemExit("NOT DECIDED: rows missing, rerun to resume, see dr9_run.log")
R = {n: json.load(open(rp(n))) for n in ROWS}; E = json.load(open(os.path.join(HERE, "dr9_energy.json"))); CS = json.load(open(os.path.join(HERE, "dr9_constants.json"))); CL = json.load(open(os.path.join(HERE, "dr9_clusters.json"))); N = json.load(open(os.path.join(NR3, "nr3_MEDIAN_results.json")))["runs"]; D5 = json.load(open(os.path.join(RB, "DR5_rotation_support_gate", "dr5_results.json")))["energy"]
def dif(a, b, gr=True):
    d = []
    for t in TG:
        for k in ("U", "rms", "tilt"): d.append(abs(a["sparc"][t][k] - b["sparc"][t][k]))
        d.append(abs(a["lt"][t] - b["lt"][t]))
    if gr: d.append(abs(a["groups"]["Z"] - b["groups"]["Z"]))
    return max(d)
K0 = dif(R["C0"], N["EM1|blum"]); K1 = dif(R["CINF"], N["EM1|off"], gr=False); K1g = abs(R["CINF"]["groups"]["Z"] - N["EM1|off"]["groups"]["Z"]); K2 = abs(E["rrat1"] - 6.271); K3 = all(0 <= R[n]["fmin"] and R[n]["fmax"] <= 1 for n in ROWS); K4 = max(abs(E["bins"][b]["Trot_Eundo"] - D5[b]["Trot_Eundo"]) for b in D5); K5 = abs(CS["eps_CM1"] / (1.15e57 / 4.05695e59) - 1); Mv0 = abs(R["MUTATE"]["sparc"][TG[0]]["U"] - R["RET_FIT"]["sparc"][TG[0]]["U"]); Mv = abs(R["MUTATE_A1"]["sparc"][TG[0]]["U"] - R["RET_FIT"]["sparc"][TG[0]]["U"])
ok = K0 <= 1e-6 and K1 <= 1e-5 and K2 <= 0.001 and K3 and K4 <= 1e-6 and K5 <= 0.01 and Mv > 0.02
P(f"DR9; K0 {K0:.1e} K1 {K1:.1e} (groups, reported {K1g:.1e}) K2 {K2:.1e} K3 {K3} K4 {K4:.1e} K5 {K5:.2e} MUTATE as frozen dU {Mv0:.2f}, missed; MUTATE_A1 dU {Mv:.2f}: {'PASS' if ok else 'FAIL'}; kappa = 1/2 FITTED, unused; not theory closed; G ratio {E['G_ratio']:.6f}, Msun ratio {E['Ms_ratio']:.6f}, GB linearity {E['gb_linearity']:.1e}, f_ret capped {E['n_fret_capped']}/{E['n']}")
P(f"eps_CM1 {CS['eps_CM1']:.5f}; CM1 set n {E['n_cm1']} etaR RET {E['etaR_cm1']['RET']:.4f} STAR {E['etaR_cm1']['STAR']:.4f}; C_CM1 RET {CS['RET_CM1']:.4f} STAR {CS['STAR_CM1']:.4f}; C_FIT RET {CS['RET_FIT']:.4f} STAR {CS['STAR_FIT']:.4f}; C_FIT/C_CM1 RET {CS['RET_FIT'] / CS['RET_CM1']:.1f}")
P("\nEnergy, median by V_flat, Upsilon 0.50, background A, NR3 path")
for b, v in E["bins"].items(): P(f"{b} n {v['n']}: f_local {v['fl']:.2f} (after {v['fa']:.2f}) Q {v['Q']:.2f} M*/Mb {v['sf']:.2f} f_ret {v['fret']:.2f} eta {v['eta']:.3f} (after {v['etaa']:.3f}) etaR {v['cR']:.3f} etaS {v['cS']:.3f} E_SN {v['ESN']:.2e} J E_undo {v['Eu']:.2e} J eps_full {v['efull']:.3f} dW/E C=1 RET {v['dW_ret']:.2f} STAR {v['dW_star']:.2f} AFTER {v['dWa_ret']:.2f}; eta_gas {v['etag']:.2e} gas share at r0 {v['fgr0']:.2f} PG-form/E_undo {v['PG']:.3f} PG-form/E_SN {v['PGsn']:.2e}")
P(f"ratios 150-250 / 20-100: {json.dumps({k: round(v, 3) for k, v in E['order'].items()})}")
P(f"clusters diag (median, ALLI[::4]): {json.dumps({k: float(f'{v:.4g}') for k, v in CL.items()})}")
def clears(r): return all(r["sparc"][t]["line"] and abs(r["sparc"][t]["tilt"]) <= 0.15 and abs(r["lt"][t]) <= 0.10 for t in TG) and abs(r["groups"]["Z"]) <= 2
def gates(r):
    g = []
    for t, s in zip(TG, "AB"):
        q = r["sparc"][t]
        if not 0.5 <= q["U"] <= 0.8: g.append(f"U{s}")
        if q["rms"] > 0.11: g.append(f"rms{s}")
        if abs(q["tilt"]) > 0.15: g.append(f"tilt{s}")
        if abs(r["lt"][t]) > 0.10: g.append(f"LT{s}")
    if abs(r["groups"]["Z"]) > 2: g.append("groups")
    return g
P("")
for n in ROWS:
    r = R[n]; s = r["sparc"]; a, b = TG; P(f"{n} C {r['C']:.4g}: U {s[a]['U']:.2f}/{s[b]['U']:.2f} rms {s[a]['rms']:.4f}/{s[b]['rms']:.4f} tilt {s[a]['tilt']:+.2f}/{s[b]['tilt']:+.2f} LT {r['lt'][a]:+.3f}/{r['lt'][b]:+.3f} groups {r['groups']['Z']:+.2f}\n   U bins {[round(v, 2) for v in s[a]['bins'].values()]}; f at U 0.5 {[None if v is None else round(v, 2) for v in s[a]['f_at_U05'].values()]}; E_undo 0 {r['n_eu0_sparc']}; fails {gates(r)}")
L = "SPARC SIDE CLEARS AT C = 1, CLUSTERS FAIL" if clears(R["RET_C1"]) else "SPARC SIDE CLEARS AT C_CM1, CLUSTERS FAIL" if clears(R["RET_CM1"]) else "SPARC SIDE CLEARS AT C_FIT (FITTED), CLUSTERS FAIL" if clears(R["RET_FIT"]) else "FAILS AT ALL THREE"; V = L if ok else "NOT DECIDED"; O = "ORDER REVERSED" if E["order"]["dW_ret"] > 1 else "NOT REVERSED"; X = CS["RET_FIT"] / CS["RET_CM1"]
P(f"\nVERDICT: {V}; {O} (ratio {E['order']['dW_ret']:.2f}); ten-times claim, etaR ratio {E['order']['cR']:.1f}, etaS {E['order']['cS']:.1f}; {'REDUCES TO CM1, needs x' + format(X, '.0f') if X >= 10 else 'C_FIT/C_CM1 ' + format(X, '.1f')}; STAR clears {[n for n in ('STAR_C1', 'STAR_CM1', 'STAR_FIT') if clears(R[n])]}")
P(f"AFTER vs BEFORE at C_FIT: dU {R['RET_FIT_AFTER']['sparc'][TG[0]]['U'] - R['RET_FIT']['sparc'][TG[0]]['U']:+.3f} dtilt {R['RET_FIT_AFTER']['sparc'][TG[0]]['tilt'] - R['RET_FIT']['sparc'][TG[0]]['tilt']:+.3f} dLT {R['RET_FIT_AFTER']['lt'][TG[0]] - R['RET_FIT']['lt'][TG[0]]:+.3f}")
P(f"clusters read NR3 EM1|blum: keys {N['EM1|blum']['keys']['n']} bad {N['EM1|blum']['keys']['bad']}, X-COP {N['EM1|blum']['xcop']['mean']:+.3f}, {N['EM1|blum']['xcop']['rms']:.3f}")
json.dump(dict(verdict=V, order=O, K0=K0, K1=K1, K2=K2, K3=K3, K4=K4, K5=K5, mutate_frozen_dU=Mv0, mutate_A1_dU=Mv, constants=CS, rows={n: dict(C=R[n]["C"], U=[R[n]["sparc"][t]["U"] for t in TG], rms=[R[n]["sparc"][t]["rms"] for t in TG], tilt=[R[n]["sparc"][t]["tilt"] for t in TG], lt=[R[n]["lt"][t] for t in TG], groups=R[n]["groups"]["Z"], clears=clears(R[n]), fails=gates(R[n])) for n in ROWS}), open(os.path.join(HERE, "dr9_results.json"), "w"), indent=1); open(os.path.join(HERE, "dr9.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
