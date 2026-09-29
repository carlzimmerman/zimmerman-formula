#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG159_compare -- PHASE 2 ONLY: row-by-row comparison of the CFG159 main run (CFG159_sp_riccati_results.json) with CFG119's committed results JSON.
Run after CFG159's own main and MUTATE runs were saved.  The path of the CFG119 JSON comes from the environment variable CFG119_JSON
(default: CFG119_fdm_soliton_results.json in the current directory); only the file's base name is printed.
Reads only.  Output: CFG159_compare.out / CFG159_compare_results.json.  Exit 0 always (a comparison, not a check).
"""
import os, sys, json, math
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
src = os.environ.get("CFG119_JSON", "CFG119_fdm_soliton_results.json")
c119 = json.load(open(src))["numbers"]
mine = json.load(open(os.path.join(HERE, "CFG159_sp_riccati_results.json")))
lines = []
def P(s=""):
    print(s); lines.append(s)
P(f"CFG159 vs {os.path.basename(src)}: rule-(ii) cells, 32 per footing")
theirs = {}
for r in c119["R1"]:
    if r["rule"] == "ii":
        theirs[(r["foot"], r["geom"], r["Mb"], r["m"])] = r
rows = []
for o in mine["cells"]:
    for f in ("canonical", "alt"):
        e = o["opt"][f]; t = theirs[(f, o["geom"], o["M"], o["m"])]
        rows.append(dict(f=f, geom=o["geom"], M=o["M"], m=o["m"], J=(e["J"], t["J"]), s=(e["s"], t["Msol_over_Mb"]),
                         lr01=(e["lr01"], t["L_at"]["0.1"]), lr1=(e["lr1"], t["L_at"]["1"]), lr30=(e["lr30"], t["L_at"]["30"]),
                         sl01=(e["slope01"], t["slopes"]["sp01"]), sl30=(e["slope30"], t["slopes"]["sp30"]), x=(e["xargmax"], t["xJ"])))
def rel(a, b): return abs(a/b - 1) if b != 0 else abs(a)
for f in ("canonical", "alt"):
    R = [r for r in rows if r["f"] == f]
    dJ = [rel(*r["J"]) for r in R]
    dJabs = [abs(r["J"][0] - r["J"][1]) for r in R]
    dlr01 = [rel(*r["lr01"]) for r in R]
    dlr30 = [rel(*r["lr30"]) for r in R]
    ds = [abs(math.log10(r["s"][0]/r["s"][1])) for r in R]
    dsl30 = [rel(*r["sl30"]) for r in R]
    dsl01 = [rel(*r["sl01"]) for r in R]
    P(f"  {f}: J  max relative difference {max(dJ):.3e} (max absolute {max(dJabs):.3e} dex); median relative {np.median(dJ):.2e}")
    P(f"       J  where |dJ| > 1e-3 relative: " + (", ".join(f"{r['geom']} {r['M']:.0e} m={r['m']:.0e}: {r['J'][0]:.6g} vs {r['J'][1]:.6g}" for r in R if rel(*r['J']) > 1e-3) or "none"))
    P(f"       log10 ratio at x=0.1: max relative difference {max(dlr01):.3e};  at x=30: {max(dlr30):.3e}")
    P(f"       optimum M_sol/M_b: max |log10 ratio| {max(ds):.3f} dex; cells beyond 0.05 dex: " + (", ".join(f"{r['geom']} {r['M']:.0e} m={r['m']:.0e}: {r['s'][0]:.4g} vs {r['s'][1]:.4g}" for r in R if abs(math.log10(r['s'][0]/r['s'][1])) > 0.05) or "none"))
    P(f"       slope at x=30 max relative difference {max(dsl30):.3e}; slope at x=0.1 max relative difference {max(dsl01):.3e}")
    P(f"       argmax x equal (both 30): {sum(1 for r in R if abs(r['x'][0]-r['x'][1]) < 1e-3)}/32")
# closest cell rows
for f in ("canonical", "alt"):
    r = [r for r in rows if r["f"] == f and (r["geom"], r["M"], r["m"]) == ("exp", 1e9, 1e-23)][0]
    P(f"  closest cell {f}: J {r['J'][0]:.5f} vs {r['J'][1]:.5f}; M_sol/M_b {r['s'][0]:.5f} vs {r['s'][1]:.5f}; log ratio at 0.1/1/30: {r['lr01'][0]:.4f}/{r['lr1'][0]:.4f}/{r['lr30'][0]:.4f} vs {r['lr01'][1]:.4f}/{r['lr1'][1]:.4f}/{r['lr30'][1]:.4f}")
# single-m aggregation
h1 = c119["H1"]
for f in ("canonical", "alt"):
    P(f"  H1 {f}: CFG119 best m {h1[f]['best_m']:.0e}, worst J {h1[f]['best_worst_J']:.6g}  (mine: see CFG159 P3)")
# their core cells (post-hoc read of their R1 slopes)
flat = [(r["foot"], r["geom"], r["Mb"], r["m"], r["rule"], r["slopes"]["sp01"]) for r in c119["R1"] if r["slopes"]["sp01"] > -0.075]
P(f"  CFG119 R1 cells with slope at 0.1 above -0.075 (both rules, both footings): {len(flat)}; range [{min(x[5] for x in flat):.4f}, {max(x[5] for x in flat):.4f}]; max m {max(x[3] for x in flat):.0e}; max M_b {max(x[2] for x in flat):.0e}")
mine_flat = [(r["f"], r["geom"], r["M"], r["m"], r["sl01"][0]) for r in rows if r["sl01"][0] > -0.075]
P(f"  CFG159 rule-(ii) cells with slope at 0.1 above -0.075: {len(mine_flat)}; range [{min(x[4] for x in mine_flat):.4f}, {max(x[4] for x in mine_flat):.4f}]")
theirs_flat_ii = [x for x in flat if x[4] == "ii"]
P(f"  CFG119 same rule-(ii) subset: {len(theirs_flat_ii)}")
same = set((x[0], x[1], x[2], x[3]) for x in theirs_flat_ii) == set((x[0], x[1], x[2], x[3]) for x in mine_flat)
P(f"  identical rule-(ii) flat-core cell sets: {same}")
env = [r["sl30"] for r in rows]
P(f"  slope at x=30 range: CFG159 [{max(e[0] for e in env):.3g}, {min(e[0] for e in env):.3g}]  CFG119 [{max(e[1] for e in env):.3g}, {min(e[1] for e in env):.3g}] (rule (ii) cells)")
out = dict(rows=rows, n_flat_c119=len(flat), n_flat_mine=len(mine_flat))
with open(os.path.join(HERE, "CFG159_compare.out"), "w") as f: f.write("\n".join(lines) + "\n")
with open(os.path.join(HERE, "CFG159_compare_results.json"), "w") as f: json.dump(out, f, indent=1)
