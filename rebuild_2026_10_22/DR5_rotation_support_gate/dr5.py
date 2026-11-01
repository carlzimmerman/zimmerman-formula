#!/usr/bin/env python3
"""DR5 (FROZEN_CRITERIA.md): rotation gate on the response, SPARC and LITTLE THINGS only, NR3's path. UR1, SL1, NF1, NR2, NR3 read only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); NR3 = os.path.join(RB, "NR3_ur1_on_nr2"); TG = ("A_c2b_refit", "B_cfg886_bg"); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); r10, r11 = J["r10"], J["r11"]; O = os.path.join(HERE, "dr5_results.json")
if not os.path.exists(O):
    W = os.path.join(HERE, "cache_MEDIAN"); os.makedirs(W, exist_ok=True); PRE = re.search(r'pre = (""".*?""")', open(os.path.join(UR1, "ur1.py")).read(), re.S).group(1); t = open(os.path.join(UR1, "ur1_tail.py")).read(); i = t.index("import time as _tm"); tl = os.path.join(W, "dr5_tail_joined.py"); open(tl, "w").write(t[:i] + open(os.path.join(HERE, "dr5_tail.py")).read())
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(eval(PRE)) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, "NR2_MEDIAN_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "dr5_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", UR1_DRIVER="1")
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(HERE, "dr5_run.log"), "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(O): raise SystemExit("NOT DECIDED: no result, see dr5_run.log")
R = json.load(open(O)); N = json.load(open(os.path.join(NR3, "nr3_MEDIAN_results.json")))["runs"]
def dif(a, b):
    d = []
    for t in TG:
        for k in ("U", "rms", "tilt"): d.append(abs(a["sparc"][t][k] - b["sparc"][t][k]))
        d.append(abs(a["lt"][t] - b["lt"][t]))
    return max(d)
G = json.load(open(os.path.join(HERE, "dr5_g1200.json"))); K1_300 = dif(R["runs"]["f0"], N["EM1|off"]); P(f"K1 at 300 points {K1_300:.1e} (A1: frozen line missed, grid); rows below at 1200 except f1 and MUTATE"); R["runs"].update(G)
K1, K2 = dif(R["runs"]["f0"], N["EM1|off"]), dif(R["runs"]["f1"], N["EM1|blum"]); K3 = R["K3"]; Mv = abs(R["MUTATE"]["sparc"][TG[0]]["U"] - R["runs"]["10"]["sparc"][TG[0]]["U"]); ok = K1 <= 1e-6 and K2 <= 1e-6 and K3 <= 1e-12 and Mv > 0.02
P(f"DR5; K1 {K1:.1e} K2 {K2:.1e} K3 {K3:.1e} MUTATE dU {Mv:.2f}: {'PASS' if ok else 'FAIL'}; kappa = 1/2 FITTED, unused; not theory closed")
for m, r in list(R["runs"].items()) + [("MUTATE swap S at 10", R["MUTATE"])]:
    s = r["sparc"]; P(f"{m}: U {s[TG[0]]['U']:.2f}/{s[TG[1]]['U']:.2f} rms {s[TG[0]]['rms']:.4f}/{s[TG[1]]['rms']:.4f} line {s[TG[0]]['line']}/{s[TG[1]]['line']} tilt {s[TG[0]]['tilt']:+.2f}/{s[TG[1]]['tilt']:+.2f} LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f}\n   U bins {[round(v, 2) for v in s[TG[0]]['bins'].values()]}; 1-S at bin centre {[round(v, 3) for v in r['f_by_bin'].values()]}")
P("\nEnergy, median by V_flat, EM1 smooth core, Upsilon 0.50 (background A)")
for k, v in R["energy"].items(): P(f"{k} n {v['n']}: M_c/M_b {v['McMb']:.1f}; inside 5 R_d {v['Mc5Mb5']:.2f}; T_rot {v['Trot_J']:.2e} J; T_rot/E_undo {v['Trot_Eundo']:.1f}; T_rot/E_bind {v['Trot_Ebind']:.4f}; T_rot/E_in {v['Trot_Ein']:.3f}; centrifugal (v_L/V)^2 {v['cent']:.3f}; m(phi_v=1) {v['m_eV_phi1']:.1e} eV; phi_v at 2e-19 eV {v['phi_v_floor']:.1e}")
o = N["EM1|off"]["sparc"]; g = R["runs"]["10"]["sparc"]; red = all(abs(g[t]["U"] - o[t]["U"]) <= 0.05 and round(abs(g[t]["tilt"] - o[t]["tilt"]), 9) <= 0.05 for t in TG); L = "REDUCES TO EXISTING ROWS" if red else "NEW SPARC ROW, CLUSTERS STILL FAIL"; E = R["energy"].values(); ex = all(v["Trot_Ebind"] < 1 for v in E); un = all(v["Trot_Eundo"] >= 1 for v in E)
V = "NOT DECIDED" if not ok else L; P(f"\nVERDICT: {V}; energy: {'EXPEL SHORT' if ex else 'expel not short in every bin'}, {'UNDO AFFORDABLE IN BOOKKEEPING' if un else 'undo not affordable in every bin'}")
P(f"SIG10 vs off: dU {max(abs(g[t]['U'] - o[t]['U']) for t in TG):.3f}, dtilt {max(abs(g[t]['tilt'] - o[t]['tilt']) for t in TG):.3f}")
json.dump(dict(verdict=V, K1=K1, K2=K2, K3=K3, mutate_dU=Mv), open(os.path.join(HERE, "dr5_verdict.json"), "w"), indent=1); open(os.path.join(HERE, "dr5.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
