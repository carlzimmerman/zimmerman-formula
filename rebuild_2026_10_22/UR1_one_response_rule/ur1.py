#!/usr/bin/env python3
"""UR1 (FROZEN_CRITERIA.md): one adiabatic response on NF1's grader, read only, through SL1's driver. kappa = 1/2 FITTED, unused here; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); O = os.path.join(HERE, "ur1_results.json"); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
if not os.path.exists(O):
    env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", UR1_DRIVER="1"); d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    pre = """sub('ETA_USE = {\\'v\\': ETA}\\n', "ETA_USE = {'v': ETA}\\nSLMAP = dict(m='EM1', mut=1.0)\\ndef _SL3M(lMb, bg, rc):\\n    if SLMAP['m'] == 'EM1': M = 10 ** (bg['a'] + bg['b'] * (lMb - 10)); return M, (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)\\n    M = SLMAP['mut'] * NAT_RRAT * 10 ** lMb\\n    if SLMAP['m'] == 'FAIR200': return M, (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)\\n    return M, NX['r_ta_com'](10 ** lMb * MSUNE)\\n")
sub('lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)', 'M200, R200 = _SL3M(q["lMb"], bg, rc)')
"""
    d = d.replace('SL1ADD = f"sub(', 'SL1ADD = ' + repr(pre) + ' + f"sub('); d = d.replace('CN1_MODE="off"', 'CN1_MODE="off"'); d = d.replace('os.path.join(HERE, "sl1_tail_harvest.py")', repr(os.path.join(HERE, "ur1_tail.py"))).replace('WD = os.path.join(HERE, "cache")', f'WD = {os.path.join(HERE, "cache")!r}').replace('os.path.join(HERE, "nf1_x74_sl1.py")', repr(os.path.join(HERE, "nf1_x74_sl1.py"))).replace('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'); df = os.path.join(HERE, "ur1_driver.py"); open(df, "w").write(d); os.makedirs(os.path.join(HERE, "cache"), exist_ok=True)
    p = subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(HERE, "ur1_run.log"), "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(O): raise SystemExit("NOT DECIDED: no result, see ur1_run.log")
R = json.load(open(O)); TG = ("A_c2b_refit", "B_cfg886_bg"); P(f"UR1; K1 EM1 off vs NR1 PRIMARY: SPARC |d| {R['K1'][0]:.1e}, preds |d| {R['K1'][1]:.1e}; K2 {R['K2']:.1e}; K4 {R['K4']:.1e}; kappa = 1/2 FITTED, unused; not theory closed")
for k, r in R["runs"].items():
    s = r["sparc"]; z = r["keys"]["Z"]["h0672"]; P(f"\n{k}: U {s[TG[0]]['U']:.2f}/{s[TG[1]]['U']:.2f} rms {s[TG[0]]['rms']:.4f} line {s[TG[0]]['line']}/{s[TG[1]]['line']} tilt {s[TG[0]]['tilt']:+.2f}/{s[TG[1]]['tilt']:+.2f}\n   U by V_flat {[round(v, 2) for v in s[TG[0]]['bins'].values()]}\n   keys {r['keys']['n']}/15 bad {r['keys']['bad']}; alt bad {r['keys_alt']}; G-IN-Mall {z['G-IN-Mall']:+.2f} G-IN-all {z['G-IN-all']:+.2f} G-MID-T3 {z['G-MID-T3']:+.2f} G-OUT-M3 {z['G-OUT-M3']:+.2f}\n   groups Z {r['groups']['Z']:+.2f} {r['groups']['verdict']}; X-COP {r['xcop']['mean']:+.3f}, {r['xcop']['rms']:.3f} {r['xcop']['PASS']} by x {[round(v,3) for v in r['xcop']['by_x'].values()]}; LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f}")
for k in ("response_EM1", "response_FAIRTA"):
    q = R[k]; P(f"\n{k}: cosmic ratio {q['cosmic']:.3f}\n  SPARC M_f/M_0 at r0 (f_local): " + ", ".join(f"{b} {v['Q']:.2f} ({v['fl']:.2f})" for b, v in q["gal"].items()) + "\n  clusters M_f/M_0 by r Mpc, with BCG / gas+stars (f_local): " + ", ".join(f"{b} {v['with_BCG']:.2f}/{v['gas_stars_only']:.2f} ({v['fl']:.3f})" for b, v in q["clusters"].items()))
m = R["MUTATE"]["sparc"][TG[0]]["U"]; P(f"\nMUTATE R_nat x 2 in the map: U {R['runs']['FAIRTA|blum']['sparc'][TG[0]]['U']:.2f} -> {m:.2f}")
open(os.path.join(HERE, "ur1.out"), "w").write("\n".join(OUT) + "\n")
