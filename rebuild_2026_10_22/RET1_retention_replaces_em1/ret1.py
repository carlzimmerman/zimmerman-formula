#!/usr/bin/env python3
"""RET1 (FROZEN_CRITERIA.md): fair share minus SN-lifted gas in place of EM1's line, on UR1's tail and SL1's driver, read only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); OUT = []; TG = ("A_c2b_refit", "B_cfg886_bg"); RES = os.path.join(HERE, "ret1_results.json")
def P(s): print(s, flush=True); OUT.append(s)
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); r10, r11 = J["r10"], J["r11"]
if not os.path.exists(RES):
    W = os.path.join(HERE, "cache"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); t = t[:t.index("import time as _tm")] + f"_NR2J = {os.path.join(NR2, 'NR2_MEDIAN_x74_results_fs0.034_nat_s2.7774.json')!r}\n" + open(os.path.join(HERE, "ret1_tail_add.py")).read(); tl = os.path.join(W, "ret1_tail.py"); open(tl, "w").write(t)
    U1 = open(os.path.join(UR1, "ur1.py")).read(); PRE = eval(re.search(r'pre = (""".*?""")', U1, re.S).group(1)); a = "\\n    M = SLMAP['mut']"; assert PRE.count(a) == 1
    PRE = PRE.replace(a, "\\n    if SLMAP['m'] == 'RET': M = SLMAP['f'](lMb, bg, rc); return M, (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)" + a)
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(PRE) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, "NR2_MEDIAN_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "ret1_driver.py"); open(df, "w").write(d); log = os.path.join(HERE, "ret1_run.log"); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=RES, CN1_FORCE="1", OMP_NUM_THREADS="1", UR1_DRIVER="1")
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(log, "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(RES): raise SystemExit("NOT DECIDED: no result, see ret1_run.log")
R = json.load(open(RES)); Mu = json.load(open(RES.replace("_results.json", "_MUTATE.json"))); lg = open(os.path.join(HERE, "ret1_run.log")).read(); e12 = float(re.search(r"eta\(M\) at 1e12/13/14/15: ([\d.]+)", lg).group(1)); run = R["runs"]
k6 = max(max(abs(run["eps0|off"]["sparc"][t]["U"] - run["FAIR200|off"]["sparc"][t]["U"]), abs(run["eps0|off"]["sparc"][t]["rms"] - run["FAIR200|off"]["sparc"][t]["rms"])) for t in TG)
mut = abs(Mu["E1x4"]["sparc"][TG[0]]["rms"] - run["E1|off"]["sparc"][TG[0]]["rms"]) > 1e-3 and abs(Mu["P1x4"]["sparc"][TG[0]]["rms"] - run["P1|off"]["sparc"][TG[0]]["rms"]) > 1e-3
C = dict(K1=max(R["K1"]) <= 1e-6, K2=R["K2"] <= 1e-6, K4=R["K4"] <= 1e-6, K5=abs(e12 - 21.53) <= 0.01, K6=k6 <= 1e-6, K7=R["K7"][0] <= 1e-4 and R["K7"][1] <= 1e-6, K8=R["K8"] <= 1e-6, K9=R["K9"] <= 1e-6, MUTATE=mut); ok = all(C.values())
P(f"RET1; R_nat {R['RNAT']:.3f}; V_SN {R['VSN']:.0f} km/s, p {R['PSN']:.0f} km/s; lg M* = {R['fs'][0]:.3f} + {R['fs'][1]:.3f} (lg M_b - 10); kappa = 1/2 FITTED, unused; not theory closed")
P(f"checks {C}; K1 {R['K1']} K2 {R['K2']:.1e} K4 {R['K4']:.1e} K6 {k6:.1e} K7 {R['K7']} K8 {R['K8']:.1e} K9 {R['K9']:.1e} eta12 {e12:.3f}")
P(f"FITTED eps (anchor M200(1e10) = EM1): E {R['EPS']['E']} P {R['EPS']['P']}")
def G(r):
    s = r["sparc"]; return dict(line=all(s[t]["line"] for t in TG), tilt=all(abs(s[t]["tilt"]) <= 0.15 for t in TG), groups=r["groups"]["verdict"] == "CONSISTENT", lt=all(abs(r["lt"][t]) <= 0.10 for t in TG))
def row(n, r):
    s = r["sparc"]; z = r["keys"]["Z"]["h0672"]; g = G(r); P(f"{n}: U {s[TG[0]]['U']:.2f}/{s[TG[1]]['U']:.2f} rms {s[TG[0]]['rms']:.4f}/{s[TG[1]]['rms']:.4f} tilt {s[TG[0]]['tilt']:+.2f}/{s[TG[1]]['tilt']:+.2f} bins {[round(v, 2) for v in s[TG[0]]['bins'].values()]}; groups {r['groups']['Z']:+.2f} {r['groups']['verdict']}; LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f}; keys {r['keys']['n']}/15 G-IN-Mall {z['G-IN-Mall']:+.2f} X-COP {r['xcop']['mean']:+.3f},{r['xcop']['rms']:.3f}; fails {[k for k, v in g.items() if not v]}"); return g
GG = {n: row(n, r) for n, r in run.items()}
P("\nMUTATE: " + "; ".join(f"{n}: U {r['sparc'][TG[0]]['U']:.2f} rms {r['sparc'][TG[0]]['rms']:.4f} groups {r['groups']['Z']:+.2f}" for n, r in Mu.items()))
for t in TG:
    L = R["lines"][t]; X = list(L["EM1"]); P(f"\nLINES {t}\n lgMb  EM1  " + "  ".join(f"{n:>11}" for n in ("E1", "P1", "EF", "PF")) + "   eps_req_E eps_req_P Vesc@EM1 lgM* f_ret(EM1)")
    for x in X:
        P(f" {float(x):5.2f} {L['EM1'][x]:6.2f} " + "  ".join(f"{L[n][x]:6.2f}({L[n][x] - L['EM1'][x]:+.2f})" for n in ("E1", "P1", "EF", "PF")) + f"   {L['epsreq_E'][x]:8.3f} {L['epsreq_P'][x]:8.3f} {L['Vesc_EM1'][x]:7.0f} {L['lMs'][x]:5.2f} {10 ** (L['FAIR'][x] - L['EM1'][x]):.2f}")
    for n in ("E1", "P1", "EF", "PF", "EM1"):
        sl = (L[n]["11"] - L[n]["9"]) / 2; bb = {f"{a}-{b}": round((L[n][b] - L[n][a]) / (float(b) - float(a)), 2) for a, b in (("7", "8"), ("8", "9"), ("9", "10"), ("10", "11"), ("11", "12"), ("12", "13"), ("13", "14"))}; am = max(abs(L[n][k] - L["EM1"][k]) for k in ("9", "10", "11")); P(f" {n}: slope(9-11) {sl:.3f} {'SLOPE MATCHES' if abs(sl - 0.9) <= 0.05 else 'SLOPE DIFFERS'}; max|d| at 9,10,11 {am:.3f} {'AMPLITUDE MATCHES' if am <= 0.1 else 'AMPLITUDE DIFFERS'}; by interval {bb}")
    if "var" in L:
        for n, v in L["var"].items(): P(f" var {n}: " + "; ".join(f"{m} " + ",".join(f"{v[m][k] - L[m if m != 'x' else m][k]:+.2f}" for k in ("9", "10", "11")) for m in v))
    P(f" clusters: M200/(R_nat M_b): " + "; ".join(f"lgMb {k}: EM1 {10 ** (L['EM1'][k] - L['FAIR'][k]):.2f} E1 {10 ** (L['E1'][k] - L['FAIR'][k]):.2f} P1 {10 ** (L['P1'][k] - L['FAIR'][k]):.2f} EF {10 ** (L['EF'][k] - L['FAIR'][k]):.2f} PF {10 ** (L['PF'][k] - L['FAIR'][k]):.2f}" for k in ("13", "14")))
    P(" M_ej/M_b on EM1: " + ", ".join(f"{k}: {10 ** (L['EM1'][k] - L['FAIR'][k]) - 1:.1f}" for k in ("8", "9", "10", "11", "12")))
ceil = [n for n in ("E1|off", "E1|blum", "P1|off", "P1|blum") if all(GG[n].values())]; fit = [n for n in ("EF|off", "EF|blum", "PF|off", "PF|blum") if all(GG[n].values())]
V = "NOT DECIDED" if not ok else ("DERIVED LINE CLEARS" if ceil else "DERIVED LINE FAILS") + ", " + ("FITTED eps CLEARS" if fit else "FITTED eps FAILS")
P(f"\nVERDICT: {V}; ceiling cleared {ceil}, fitted cleared {fit}")
json.dump(dict(verdict=V, checks=C, gates=GG), open(os.path.join(HERE, "ret1_verdict.json"), "w"), indent=1); open(os.path.join(HERE, "ret1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
