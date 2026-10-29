#!/usr/bin/env python3
"""X48 AMENDMENT A3 grade (10^12 only): nine-seed ng 64 median against the window [3.3, 4.6] and against the ng 48 (A2) median
(CONVERGED if within 20 %); per-seed r_-2 / r_conv at both ng; bootstrap 68 % (10 000, seed 20261026); NFW-fit median. Writes a
reported-only regrade table (10^12 replaced by the ng 64 median, 10^13 / 10^14 at A2) to x48_A3_regrade_table.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R64 = json.load(open(os.path.join(HERE, "x48_analyze_results_ng64_A3.json")))["runs"]
R48 = json.load(open(os.path.join(HERE, "x48_analyze_results_ng48_A2.json")))
W = (3.3, 4.6); OUT = ["X48 A3 grade (10^12; ng 64 vs ng 48; convergence beyond ng 64 not tested); kappa = 1/2 FITTED; not theory closed"]
def rows(R, ng): return {o["seed"]: o for k, o in R.items() if o.get("flag") == "ok" and o.get("ng") == ng and abs(o["M"] / 1e12 - 1) < 1e-6}
a, b = rows(R64, 64), rows(R48["runs"], 48)
rng = np.random.default_rng(20261026)
def stats(d):
    cf = np.array([d[s]["cf"] for s in sorted(d)]); bs = np.median(cf[rng.integers(0, len(cf), (10000, len(cf)))], axis=1)
    return float(np.median(cf)), [float(x) for x in np.percentile(bs, [16, 84])], float(np.median([d[s]["c_nfw_fit"] for s in d]))
m64, b64, n64 = stats(a); m48, b48, n48 = stats(b)
win = "IN WINDOW" if W[0] <= m64 <= W[1] else ("ABOVE WINDOW" if m64 > W[1] else "BELOW WINDOW")
sh = m64 / m48 - 1; res = "CONVERGED" if abs(sh) <= 0.20 else f"RESOLUTION-DEPENDENT ({'falls' if sh < 0 else 'rises'})"
OUT.append(f"  ng 64: N {len(a)} seeds; median c_f {m64:.2f} (68 % {b64[0]:.2f}-{b64[1]:.2f}); NFW-fit median {n64:.2f}")
OUT.append(f"  ng 48 (A2): N {len(b)} seeds; median c_f {m48:.2f} (68 % {b48[0]:.2f}-{b48[1]:.2f}); NFW-fit median {n48:.2f}")
OUT.append(f"  WINDOW [3.3, 4.6]: {win};  RESOLUTION: median shift {100 * sh:+.0f} % -> {res}")
per = {}
for s in sorted(set(a) | set(b)):
    p = dict(cf48=b[s]["cf"], cf64=a[s]["cf"], q48=b[s]["rm2"] / b[s]["rconv"], q64=a[s]["rm2"] / a[s]["rconv"], rconv48=b[s]["rconv"], rconv64=a[s]["rconv"])
    per[s] = p
    OUT.append(f"    seed {s}: c_f {p['cf48']:.2f} -> {p['cf64']:.2f}; r_-2/r_conv {p['q48']:.2f} -> {p['q64']:.2f}; r_conv {p['rconv48']:.4f} -> {p['rconv64']:.4f} Mpc")
pin = [s for s, p in per.items() if p["q48"] <= 2.0]
trk = [s for s in pin if per[s]["q64"] <= 2.0]
tr = "TRACKS r_conv" if pin and len(trk) > len(pin) / 2 else "DOES NOT TRACK r_conv"
OUT.append(f"  ng 48 seeds with r_-2 <= 2 r_conv: {pin}; still <= 2 r_conv at ng 64: {trk} -> {tr}")
OUT.append(f"  median c_f over those seeds: ng 48 {np.median([per[s]['cf48'] for s in pin]):.2f} -> ng 64 {np.median([per[s]['cf64'] for s in pin]):.2f}; "
           f"over the others: {np.median([per[s]['cf48'] for s in per if s not in pin]):.2f} -> {np.median([per[s]['cf64'] for s in per if s not in pin]):.2f}")
OUT.append("  note: the constrained field is drawn on each grid, so a seed at ng 64 is not the same small-scale realisation as at ng 48; per-seed shifts mix resolution and realisation.")
A2T = json.load(open(os.path.join(HERE, "x48_analyze_results_ng48_A2.json")))["cf_by_mass"]
tab = dict(A2T); tab["1e+12"] = m64
json.dump(dict(cf_by_mass=tab, note="reported-only: 1e12 at ng 64 (A3), 1e13/1e14 at ng 48 (A2)"), open(os.path.join(HERE, "x48_A3_regrade_table.json"), "w"), indent=1)
print("\n".join(OUT)); open(os.path.join(HERE, "x48_grade_A3.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(window=W, ng64=dict(median=m64, boot68=b64, nfw=n64), ng48=dict(median=m48, boot68=b48, nfw=n48), window_label=win, resolution=res,
               shift=sh, per_seed=per, pinned_seeds=pin, tracking=tr), open(os.path.join(HERE, "x48_grade_A3.json"), "w"), indent=1)
