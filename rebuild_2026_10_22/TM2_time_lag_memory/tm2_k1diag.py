#!/usr/bin/env python3
"""TM2 A1.1: K1's failed peak, W3 tau to 0 and to infinity with tm2_map's own functions at UX6's 10 kpc grid. kappa = 1/2 FITTED; not theory closed."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); src = open(os.path.join(HERE, "tm2_map.py")).read(); src = src[:src.index('say("="*90); say("TM2_time_lag_memory Part A"')]
src = src.replace('f"tm2_map{TAG}.out"', '"tm2_k1diag.out"').replace("STEP = 20.0;", "STEP = 10.0;")
ns = dict(__file__=os.path.join(HERE, "tm2_map.py")); exec(src, ns)
S = ns["Sys"](ns["HIST"]["P"]); U = json.load(open(os.path.join(RB, "UX6_gas_term_bullet", "ux6_results.json")))["rows"]; say = ns["say"]; K = ns["KFIT"]
for f in ("canonical", "alt"):
    R = ns["run"](S, {f"W3|tau0|{f}": ("W3", "tau0", f, K[f]), f"W3|inf|{f}": ("W3", "inf", f, K[f])})
    for n, u in ((f"W3|tau0|{f}", f"N1|{f}|fit"), (f"W3|inf|{f}", f"N2|{f}|fit")):
        o = R[n][0]; v = U[u]; say(f"{n}: main {o['main']['peak']} vs {v['main']['peak']}, sub {o['sub']['peak']} lm {o['sub']['local_max']} vs {v['sub']['peak']} lm {v['sub']['local_max']}; M300 {o['M300'][0]/v['M300'][0]-1:+.4f} {o['M300'][1]/v['M300'][1]-1:+.4f}")
ns["OUT"].close()
