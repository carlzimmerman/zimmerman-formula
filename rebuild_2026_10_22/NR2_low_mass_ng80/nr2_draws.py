#!/usr/bin/env python3
"""NR2, POST-RESULT, not in the frozen criteria, cannot change the verdict. The frozen band holds eta(1e12) at 21.53 while its ratios resample eta(1e12) in the denominator. Here all three medians are resampled together and passed as they are: each draw's own eta(1e12) and its own rho. 40 draws, first of the seeded stream.
kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, tempfile
import numpy as np
THIS = os.path.abspath(__file__); HERE0 = os.path.dirname(THIS); RB0 = os.path.dirname(HERE0)
_t = open(os.path.join(RB0, "NR1_native_n_ng80", "nr1.py")).read(); G = dict(__file__=THIS, __name__="nr1_prefix"); exec(compile(_t[:_t.index('P("NR1: version N')], "nr1_prefix", "exec"), G); G["HERE"] = tempfile.mkdtemp(); run = G["run"]; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
E = json.load(open(os.path.join(HERE0, "nr2_results.json")))["eta"]; A, B, C = (np.array(E[f"1e+{m}_ng80"]) for m in (10, 11, 12)); g = np.random.default_rng(20261101); rows = []
med = lambda v: float(np.median(v[g.integers(0, 9, 9)]))
P("NR2 post-result draws: all three medians resampled together; kappa = 1/2 FITTED; not theory closed")
for i in range(40):
    a, b, c = med(A), med(B), med(C); s = run(f"draw{i}", c, a / c, b / c)["footings"]["canonical"]["sparc"]; u = [v["U_median"] for v in s.values()]; ok = all(v["line"] for v in s.values()); rows.append(dict(eta10=a, eta11=b, eta12=c, U=u, rms=[v["rms"] for v in s.values()], line=ok)); P(f"  {i}: eta {a:.1f} {b:.1f} {c:.1f} U {u[0]:.2f} {u[1]:.2f} {'pass' if ok else 'FAIL'}")
n = sum(r["line"] for r in rows); hi = sum(max(r["U"]) > 0.8 for r in rows); lo = sum(min(r["U"]) < 0.5 for r in rows); UA = [r["U"][0] for r in rows]; P(f"line passes {n} of 40; Upsilon high {hi}, low {lo}; Upsilon A p16, p50, p84 {np.percentile(UA, 16):.2f}, {np.percentile(UA, 50):.2f}, {np.percentile(UA, 84):.2f}")
json.dump(rows, open(os.path.join(HERE0, "nr2_draws.json"), "w"), indent=1); open(os.path.join(HERE0, "nr2_draws.out"), "w").write("\n".join(OUT) + "\n")
