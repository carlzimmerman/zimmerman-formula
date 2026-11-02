#!/usr/bin/env python3
"""BF2 step 6 read: arms on identical jobs, bootstrap over jobs, K6. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
import numpy as np
R = os.path.dirname(os.path.abspath(__file__)); N = sys.argv[1]; TAG = "_MUTATE" if os.environ.get("BF2_MUTATE") == "1" else ""; A = {a: json.load(open(os.path.join(R, f"control_{a}_N{N}{TAG}.json"))) for a in ("real", "control", "perm1", "perm2") if os.path.exists(os.path.join(R, f"control_{a}_N{N}{TAG}.json"))}
snap = json.load(open(os.path.join(R, "snapshot.json"))); rg = np.random.default_rng(20261102); ja = sorted(snap["done"]); idx = rg.permutation(len(ja))[:int(N)]; jobs = {ja[i] for i in idx}; ref = sorted(tuple(h) for h in snap["hits"] if f"{h[0]}{h[1]}" in jobs); got = sorted((h["i"], h["op"], h["j"], h["w"]) for h in A["real"]["hits"]); ok = ref == got
print(f"K6 real arm reproduces snapshot on sampled jobs: {ok}; {len(got)} vs {len(ref)}")
for a, d in A.items():
    H = d["hits"]; n = len(H); print(f"{a:8s} jobs {d['n_jobs']} expressions {d['expressions']:.4g} hits {n}; jobs with a hit {sum(x > 0 for x in d['per_job'])}; fixed rms <= .20: {sum(h['rms'] <= .20 for h in H)}; X-COP unseen |m| <= .05, rms <= .10: {sum(abs(h['xh']) <= .05 and h['xhr'] <= .10 for h in H)}; both {sum(h['rms'] <= .20 and abs(h['xh']) <= .05 and h['xhr'] <= .10 for h in H)}; lowest rms {min([h['rms'] for h in H], default=float('nan')):.3f}; on train X {np.mean([abs(h['x']) for h in H]) if H else float('nan'):.3f}")
ctl = [a for a in A if a != "real"]
if ctl:
    r = np.array(A["real"]["per_job"]); c = np.mean([A[a]["per_job"] for a in ctl], axis=0); b = rg.integers(0, len(r), (20000, len(r))); ra = r[b].sum(1) / np.maximum(c[b].sum(1), 1e-9); print(f"ratio real/mean control {r.sum() / max(c.sum(), 1e-9):.2f}; bootstrap 95 % {np.percentile(ra, 2.5):.2f}-{np.percentile(ra, 97.5):.2f}; rule: above 3 with lower bound above 1: {r.sum() >= 3 * c.sum() and np.percentile(ra, 2.5) > 1}")
sys.exit(0 if ok else 1)
