#!/usr/bin/env python3
"""JC1 read, per FROZEN_CRITERIA.md. JC1_MUTATE=1 reads the twin, exit 1. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = ("A_c2b_refit", "B_cfg886_bg"); MUT = os.environ.get("JC1_MUTATE") == "1"; OUT = []
def P(s): print(s); OUT.append(s)
N = json.load(open(os.path.join(H, "..", "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")))["runs"]["EM1|blum"]
R = json.load(open(os.path.join(H, "jc1_MUTATE_results.json" if MUT else "jc1_RUN_results.json")))
d = max(abs(R["rows"]["k|+0.00"]["sparc"][t][q] - N["sparc"][t][q]) for t in T for q in ("U", "rms")); k1 = d <= 1e-3; P(f"K1 M_s = M0 vs NR3 EM1|blum |d| {d:.2e}: {k1}")
if MUT: open(os.path.join(H, "jc1_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k1 else 1)
def gates(r):
    s = r["sparc"]; return dict(U=all(0.5 <= s[t]["U"] <= 0.8 and s[t]["rms"] <= 0.110 for t in T), tilt=all(abs(s[t]["tilt"]) <= 0.15 for t in T), groups=r["groups"].get("verdict") == "CONSISTENT", lt=all(abs(r["lt"][t]) <= 0.10 for t in T), mass=-0.10 - 1e-9 <= r["delta"] <= 0.14)
cl = {}
for m in ("lit", "norm"):
    c = R["clusters"][m]; e = R["edge"][m]; P(f"\n{m}: keys {c['n']} bad {c['bad']} X-COP {c['xcop']['mean']:+.3f}, {c['xcop']['rms']:.3f}; M_s/M_0 at outer edge min {e['min']:.2f} median {e['median']:.2f} max {e['max']:.2f}")
    for dl in (-0.10, -0.05, 0.0, 0.05, 0.10):
        r = R["rows"][f"{m}|{dl:+.2f}"]; s = r["sparc"]; bad = [k for k, v in gates(r).items() if not v]; b = s[T[0]]["bins"]
        P(f"  {dl:+.2f} U {s[T[0]]['U']:.2f}/{s[T[1]]['U']:.2f} rms {s[T[0]]['rms']:.4f} tilt {s[T[0]]['tilt']:+.2f}/{s[T[1]]['tilt']:+.2f} Z {r['groups'].get('Z', float('nan')):+.2f} {r['groups'].get('verdict')} LT {r['lt'][T[0]]:+.3f}/{r['lt'][T[1]]:+.3f} bins {' '.join(f'{v:.2f}' for v in b.values())} {','.join(bad) or 'ALL CLEAR'}")
        if not bad: cl.setdefault(m, []).append(dl)
P(f"\n=== LABEL: {'CLEARS ' + str(cl) if cl else 'FAILS'} [NOISE-LIMITED]")
open(os.path.join(H, "jc1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k1 else 1)
