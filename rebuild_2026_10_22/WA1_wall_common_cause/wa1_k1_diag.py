#!/usr/bin/env python3
"""WA1 K1 diagnostic, post-result, no label: the combined injections refit (a) with uninformed nuisances (information < 1) held at their centre, priors off; (b) with priors on. kappa = 1/2 FITTED; not theory closed."""
import json
from wa1_fit import *
o = {}
for f in FEET:
    c = build("LAW", f); r = c["r"]; F = Fit(c); info = np.sum(F.WA ** 2, 0); mk = [j for j in range(len(NN)) if info[j] >= 1]
    for tag in ("all+", "all-"):
        inj = r["inj"][tag]; th = {n: 0.0 for n in NN}; th.update(inj["theta"]); tv = np.array([th[n] for n in NN]); zr = c["z"] + c["a"] @ tv + c["b"] @ (tv * tv)
        for i, l in enumerate(c["lines"]):
            if l in inj["l"]: zr[i] = inj["l"][l] / c["sX"][l] if l in c["sX"] else inj["l"][l]
        e = c["W"] @ (c["z"] - zr); ta, _ = F.solve(e, Pi=1e-10 * np.eye(len(NN)), mask=mk); tb, _ = F.solve(e)
        o[f"{f}|{tag}"] = dict(informed=[NN[j] for j in mk], injected=tv[mk].tolist(), held=ta.tolist(), ok_held=bool(np.abs(ta - tv[mk]).max() <= .25), priors_on=tb.tolist())
json.dump(o, open(os.path.join(HERE, "wa1_k1_diag.json"), "w"), indent=1); print(json.dumps(o, indent=0)[:2500])
