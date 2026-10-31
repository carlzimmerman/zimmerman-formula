#!/usr/bin/env python3
"""X48 AMENDMENT A4 grade: per mass, nine-seed ng 64 median against the window [3.3, 4.6] and against the ng 48 (A2) median (CONVERGED if
within 20 %); per-seed r_-2 / r_conv at both ng; bootstrap 68 % (10 000, seed 20261026); NFW-fit median. 1e12 repeated from A3's runs."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R64 = json.load(open(os.path.join(HERE, "x48_analyze_results_ng64_A4.json")))
R48 = json.load(open(os.path.join(HERE, "x48_analyze_results_ng48_A2.json")))["runs"]
W = (3.3, 4.6); OUT = ["X48 A4 grade (ng 64 vs ng 48; convergence beyond ng 64 not tested); kappa = 1/2 FITTED; not theory closed"]; RES = {}
rng = np.random.default_rng(20261026)
def rows(R, ng, M): return {o["seed"]: o for o in R.values() if o.get("flag") == "ok" and o.get("ng") == ng and abs(o["M"] / M - 1) < 1e-6}
def stats(d):
    cf = np.array([d[s]["cf"] for s in sorted(d)]); bs = np.median(cf[rng.integers(0, len(cf), (10000, len(cf)))], axis=1)
    return float(np.median(cf)), [float(x) for x in np.percentile(bs, [16, 84])], float(np.median([d[s]["c_nfw_fit"] for s in d]))
for M in (1e12, 1e13, 1e14):
    a, b = rows(R64["runs"], 64, M), rows(R48, 48, M); m64, b64, n64 = stats(a); m48, b48, n48 = stats(b)
    win = "IN WINDOW" if W[0] <= m64 <= W[1] else ("ABOVE WINDOW" if m64 > W[1] else "BELOW WINDOW")
    sh = m64 / m48 - 1; res = "CONVERGED" if abs(sh) <= 0.20 else f"RESOLUTION-DEPENDENT ({'falls' if sh < 0 else 'rises'})"
    OUT.append(f"M {M:.0e}: ng 64 N {len(a)}, median c_f {m64:.2f} (68 % {b64[0]:.2f}-{b64[1]:.2f}), NFW-fit {n64:.2f}; ng 48 N {len(b)}, median {m48:.2f} (68 % {b48[0]:.2f}-{b48[1]:.2f}), NFW-fit {n48:.2f}")
    OUT.append(f"  WINDOW [3.3, 4.6]: {win}; RESOLUTION: shift {100 * sh:+.0f} % -> {res}")
    per = {}
    for s in sorted(set(a) & set(b)):
        per[s] = dict(cf48=b[s]["cf"], cf64=a[s]["cf"], q48=b[s]["rm2"] / b[s]["rconv"], q64=a[s]["rm2"] / a[s]["rconv"], n64=a[s]["n_inside_rm2"])
        OUT.append(f"    seed {s}: c_f {per[s]['cf48']:.2f} -> {per[s]['cf64']:.2f}; r_-2/r_conv {per[s]['q48']:.2f} -> {per[s]['q64']:.2f}; n<r_-2 at ng 64 {per[s]['n64']}")
    pin = [s for s, p in per.items() if p["q48"] <= 2.0]; trk = [s for s in pin if per[s]["q64"] <= 2.0]; pin64 = [s for s, p in per.items() if p["q64"] <= 2.0]
    tr = "no pinned seeds" if not pin else ("TRACKS r_conv" if len(trk) > len(pin) / 2 else "DOES NOT TRACK r_conv")
    OUT.append(f"  r_-2 <= 2 r_conv: ng 48 {pin}, ng 64 {pin64}, both {trk} -> {tr}")
    RES[f"{M:.0e}"] = dict(n64=len(a), median64=m64, boot64=b64, nfw64=n64, median48=m48, boot48=b48, nfw48=n48, window=win, resolution=res, shift=sh, per_seed=per, tracking=tr)
OUT.append("note: the constrained field is drawn on each grid, so per-seed shifts mix resolution and realisation.")
print("\n".join(OUT)); open(os.path.join(HERE, "x48_grade_A4.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "x48_grade_A4.json"), "w"), indent=1)
