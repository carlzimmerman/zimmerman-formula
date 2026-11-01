#!/usr/bin/env python3
"""RM2 read, per FROZEN_CRITERIA.md. RM2_MUTATE=1 reads the twin, exit 1. All numbers FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = ("A_c2b_refit", "B_cfg886_bg"); MUT = os.environ.get("RM2_MUTATE") == "1"; OUT = []
def P(s): print(s); OUT.append(s)
N = json.load(open(os.path.join(H, "..", "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")))["runs"]["EM1|blum"]
def k1f(r): return max(abs(r["sparc"][t][q] - N["sparc"][t][q]) for t in T for q in ("U", "rms")) <= 1e-6
if MUT:
    R = json.load(open(os.path.join(H, "rm2_MUTATE_results.json"))); k = k1f(R["rows"]["K|10.0|1.0|+0.00"]); P(f"MUTATE K1: {'PASS' if k else 'FAIL'}"); open(os.path.join(H, "rm2_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k else 1)
R = json.load(open(os.path.join(H, "rm2_RUN_results.json"))); rows = R["rows"]; clu = R["clusters"]
def gates(r):
    s = r["sparc"]; return dict(U=all(0.5 <= s[t]["U"] <= 0.8 and s[t]["rms"] <= 0.110 for t in T), tilt=all(abs(s[t]["tilt"]) <= 0.15 for t in T), groups=r["groups"].get("verdict") == "CONSISTENT", lt=all(abs(r["lt"][t]) <= 0.10 for t in T), mass=-0.10 - 1e-9 <= r["delta"] <= 0.14)
pas = []; best = None
for key in clu:
    c = clu[key]; P(f"\nlgMc|f_hi {key}: keys {c['n']} bad {c['bad']} X-COP {c['xcop']['mean']:+.3f}, {c['xcop']['rms']:.3f}")
    for d in (-0.10, -0.05, 0.0, 0.05, 0.10):
        r = rows[f"{key}|{d:+.2f}"]; G = gates(r); s = r["sparc"]; bad = [k for k, v in G.items() if not v]; b = s[T[0]]["bins"]
        P(f"  {d:+.2f} U {s[T[0]]['U']:.2f}/{s[T[1]]['U']:.2f} rms {s[T[0]]['rms']:.4f} tilt {s[T[0]]['tilt']:+.2f}/{s[T[1]]['tilt']:+.2f} Z {r['groups'].get('Z', float('nan')):+.2f} {r['groups'].get('verdict')} LT {r['lt'][T[0]]:+.3f}/{r['lt'][T[1]]:+.3f} bins {' '.join(f'{v:.2f}' for v in b.values())} {','.join(bad) or 'ALL CLEAR'}")
        if not bad: pas.append((f"{key}|{d:+.2f}", c["n"]))
        if best is None or len(bad) < best[0]: best = (len(bad), key, d, bad)
P(f"\nCells clearing all five: {[p[0] + ' keys ' + str(p[1]) for p in pas]}\nFewest gates failed: {best}")
c0 = rows["10.0|0.4|+0.00"]["sparc"][T[0]]["U"]; k1 = k1f(rows["K|10.0|1.0|+0.00"]); k2 = 6 <= R["mb"][0] and R["mb"][1] <= 16; k3 = c0 != rows["K|10.0|1.0|+0.00"]["sparc"][T[0]]["U"]
P(f"M_b range seen, lg, galaxies and clusters: {R['mb']}\n\n=== LABEL: {'CELLS CLEAR' if pas else 'NO CELL'} [NOISE-LIMITED]\nK1 {k1}; K2 {k2}; K3 {k3}")
open(os.path.join(H, "rm2.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k1 and k2 and k3 else 1)
