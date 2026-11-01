#!/usr/bin/env python3
"""NR3 (FROZEN_CRITERIA.md): UR1's rule on NR2's eta, one driver per input. UR1, SL1, NF1, NR2 read only. kappa = 1/2 FITTED, unused here; not theory closed."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); OUT = []; TG = ("A_c2b_refit", "B_cfg886_bg")
def P(s): print(s, flush=True); OUT.append(s)
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); IN = dict(MEDIAN=(J["r10"], J["r11"]), LOW=(J["r10_68"][0], J["r11_68"][0]), HIGH=(J["r10_68"][1], J["r11_68"][1]))
U1 = open(os.path.join(UR1, "ur1.py")).read(); PRE = re.search(r'pre = (""".*?""")', U1, re.S).group(1)
def go(tag, r10, r11):
    O = os.path.join(HERE, f"nr3_{tag}_results.json")
    if os.path.exists(O): return json.load(open(O))
    W = os.path.join(HERE, f"cache_{tag}"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); a = 'os.path.join(REB, "NR1_native_n_ng80", "NR1_PRIMARY_x74_results_fs0.034_nat_s2.7774.json")'; assert t.count(a) == 1; t = t.replace(a, repr(os.path.join(NR2, f"NR2_{tag}_x74_results_fs0.034_nat_s2.7774.json"))); tl = os.path.join(W, "nr3_tail.py"); open(tl, "w").write(t)
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(eval(PRE)) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, f"NR2_{tag}_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "nr3_driver.py"); open(df, "w").write(d); log = os.path.join(HERE, f"nr3_{tag}_run.log"); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", UR1_DRIVER="1")
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(log, "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(O): raise SystemExit(f"NOT DECIDED: {tag} wrote no result, see {log}")
    return json.load(open(O))
P("NR3: UR1's response rule on NR2's eta; kappa = 1/2 FITTED, unused; not theory closed"); ok = True; A = {}
def Gate(r):
    s = r["sparc"]; line = all(s[t]["line"] for t in TG); tilt = all(abs(s[t]["tilt"]) <= 0.15 for t in TG); lt = all(abs(r["lt"][t]) <= 0.10 for t in TG); return dict(line=line, tilt=tilt, keys=r["keys"]["n"] == 15, groups=r["groups"]["verdict"] == "CONSISTENT", xcop=r["xcop"]["PASS"], lt=lt)
for tag, (a, b) in IN.items():
    R = A[tag] = go(tag, a, b); lg = open(os.path.join(HERE, f"nr3_{tag}_run.log")).read(); e12 = float(re.search(r"eta\(M\) at 1e12/13/14/15: ([\d.]+)", lg).group(1)); k = (max(R["K1"]) <= 1e-6, R["K2"] <= 1e-6, R["K4"] <= 1e-6, abs(R["MUTATE"]["sparc"][TG[0]]["U"] - R["runs"]["FAIRTA|blum"]["sparc"][TG[0]]["U"]) > 0.02, abs(e12 - 21.53) <= 0.01); ok &= all(k)
    P(f"\n=== {tag} rho {a:.3f}, {b:.3f}; K1 {max(R['K1']):.1e} K2 {R['K2']:.1e} K4 {R['K4']:.1e} MUTATE U -> {R['MUTATE']['sparc'][TG[0]]['U']:.2f} K5 eta12 {e12:.3f}: {'PASS' if all(k) else 'FAIL'}")
    for n, r in R["runs"].items():
        s = r["sparc"]; z = r["keys"]["Z"]["h0672"]; P(f"{n}: U {s[TG[0]]['U']:.2f}/{s[TG[1]]['U']:.2f} rms {s[TG[0]]['rms']:.4f}/{s[TG[1]]['rms']:.4f} line {s[TG[0]]['line']}/{s[TG[1]]['line']} tilt {s[TG[0]]['tilt']:+.2f}/{s[TG[1]]['tilt']:+.2f}; bins {[round(v, 2) for v in s[TG[0]]['bins'].values()]}; keys {r['keys']['n']}/15 {r['keys']['bad']} G-IN-Mall {z['G-IN-Mall']:+.2f}; groups {r['groups']['Z']:+.2f} {r['groups']['verdict']}; X-COP {r['xcop']['mean']:+.3f}, {r['xcop']['rms']:.3f}; LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f}")
    q = R["response_EM1"]; P("response EM1, SPARC M_f/M_0 at r0 (f_local): " + ", ".join(f"{b_} {v['Q']:.2f} ({v['fl']:.2f})" for b_, v in q["gal"].items()) + "; clusters gas + stars: " + ", ".join(f"{b_} {v['gas_stars_only']:.2f}" for b_, v in q["clusters"].items()))
def label(R):
    g = Gate(R["runs"]["FAIRTA|blum"]); q = R["response_FAIRTA"]; inw = all(v["Q"] > 1 for v in q["gal"].values()); out = all(q["clusters"][k]["gas_stars_only"] < 1 for k in ("0.15", "0.3", "0.46"))
    if not (inw and out): return "NO SIGN FLIP", g
    return ("ONE RULE CLEARS" if all(g.values()) else "SIGN FLIP YES, AMPLITUDE FAILS"), g
L = {t: label(A[t]) for t in A}; EM = {t: Gate(A[t]["runs"]["EM1|blum"]) for t in A}; nl = any(L[t][0] != L["MEDIAN"][0] or EM[t]["line"] != EM["MEDIAN"]["line"] for t in ("LOW", "HIGH"))
for t in A: P(f"\n{t}: primary {L[t][0]}, gates {L[t][1]}; EM1 + Blumenthal gates {EM[t]}")
V = "NOT DECIDED" if not ok else L["MEDIAN"][0] + (" [NOISE-LIMITED]" if nl else ""); P(f"\nVERDICT: {V}; EM1 line reached at MEDIAN: {'yes' if EM['MEDIAN']['line'] else 'no'}")
json.dump(dict(verdict=V, inputs=IN, label={t: L[t][0] for t in L}, gates={t: L[t][1] for t in L}, EM1_gates=EM), open(os.path.join(HERE, "nr3_results.json"), "w"), indent=1); open(os.path.join(HERE, "nr3.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
