"""CFG330 controls C2 (Gaussian recovery) and C3 (injection) for the K25 local clip; uses cfg330_icgc.py's own functions."""
import math, re, numpy as np, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg330_icgc.py")).read()
g = {"np": np, "math": math, "KCLIP": 2.5, "ONLY_NONCENTRAL": False, "CENTRALS": ()}
for name in ("ml_sigma", "ctrunc", "local_sigma"):
    m = re.search(rf"\ndef {name}\(.*?(?=\n\n\n|\ndef )", src, re.S); exec(m.group(0), g)
rng = np.random.default_rng(330); out = {}
r2 = []; r3 = []; r3raw = []
for _ in range(2000):
    v = rng.normal(0, 200, 40) + rng.normal(0, 15, 40); e = np.full(40, 15.0)
    r2.append(g["local_sigma"](v, e, k=2.5)[1] / 200)
    nc = 10; vc = np.concatenate([rng.normal(0, 200, 30), rng.normal(0, 500, nc)]) + rng.normal(0, 15, 40)
    s0 = g["ml_sigma"](vc, e)[1]; s1 = g["local_sigma"](vc, e, k=2.5)[1]
    r3raw.append(s0 / 200); r3.append(s1 / 200)
m2 = float(np.median(r2)); pull = (np.median(r3raw) - np.median(r3)) / (np.median(r3raw) - 1)
out["C2_median_sigma_ratio"] = m2; out["C2_pass"] = bool(abs(m2 - 1) < 0.03)
out["C3_raw"] = float(np.median(r3raw)); out["C3_clipped"] = float(np.median(r3)); out["C3_pull_fraction"] = float(pull); out["C3_pass"] = bool(pull > 0.5)
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "cfg330_controls_results.json"), "w"), indent=1)
