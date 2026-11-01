#!/usr/bin/env python3
"""SL1: what the best NATIVE pair does to the halo, by V_flat bin and on clusters; and a tally of why SPEC's exact hits fail the gauntlet. Reported, not graded. kappa = 1/2 FITTED; not theory closed."""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ["SL1_HERE"] = HERE
exec(compile(open(os.path.join(HERE, "discover_law.py")).read().split('if __name__ == "__main__" and "--sweep"')[0], "discover_law", "exec"), globals())
D = Data(); fin = lambda t: float(np.median(t))
for nm, At, Bt in [("best NATIVE", ("inv1p", ("mul", ("sub", ("div", "q", "Rn"), ("sqrt", "q")), "v")), ("add", "1", ("mul", ("sqrt", "fl"), ("sub", ("mul", "Rn", "fl"), "1"))))]:
    o = D.sparc(list(range(len(D.gals))), TAGS[0]); iu = int(np.argmin(abs(D.UPS - 0.5))); fl = o["Mb"][:, iu] / o["M0"]; B = ev(Bt, dict(fl=fl)); Av = ev(At, o["s"].V) * np.ones(len(o["s"].r0)); print(nm, "A and B, SPARC, Upsilon 0.5")
    vf = np.array([D.gals[i]["vf"] for i in o["idx"]]) if "idx" in o else None
    gid = o["gid"]
    for l, h in BINS:
        m = np.array([l <= (vf[g] if vf is not None else D.gals[g]["vf"]) < h for g in gid]); gs = sorted(set(gid[m].tolist())); print(f"  V {l}-{h}: A {fin(Av[gs]):.3f}, B median {fin(B[m]):.3f}, 10-90% {np.percentile(B[m],10):.3f} {np.percentile(B[m],90):.3f}, fl median {fin(fl[m]):.3f}")
    h = HKS[0]; c = D.cl[h]; fc = c["Mb"] / c["M0"]; Bc = ev(Bt, dict(fl=fc)); Ac = ev(At, c["s"].V) * np.ones(len(c["s"].r0)); print(f"  clusters: A median {fin(Ac):.3f}, B by node index (inner to outer): " + " ".join(f"{fin(Bc[:, j]):.2f}" for j in range(0, Bc.shape[1], 4)) + "; fl " + " ".join(f"{fin(fc[:, j]):.2f}" for j in range(0, fc.shape[1], 4)))
R = json.load(open(os.path.join(HERE, "hall_of_fame.json")))["cand"]["SPEC"]; H = [r for r in R if r["gate_exact"] == 0]; C = Counter(); one = []
for r in H:
    F = []
    if not r["holdout"]: F.append("holdout-invalid")
    else:
        if r["holdout"]["g1"] > 0: F.append("holdout G1")
        if r["holdout"]["g2"] > 0: F.append("holdout G2")
    if not (r["groups"] and r["groups"]["PASS"]): F.append("groups")
    if not (r["xcop"] and r["xcop"]["PASS"]): F.append("X-COP")
    if not r["line175"]: F.append("line175")
    if r["alt_keys"]: F.append("alt keys")
    for f in F: C[f] += 1
    C[f"n_fail={len(F)}"] += 1; one.append((len(F), r["nodes"], r["A"], r["B"], F, r["a0_free"], r["q_inert"], r["holdout"] and (r["holdout"]["g1"], r["holdout"]["g2"]), r["xcop"] and (round(r["xcop"]["mean"], 3), round(r["xcop"]["rms"], 3))))
print(len(H), "SPEC exact hits; fail tally", dict(C)); print("a0-free", sum(r["a0_free"] for r in H), "q inert", sum(r["q_inert"] for r in H))
print("A trees distinct", len({r["A"] for r in H}), "B trees distinct", len({r["B"] for r in H}))
for x in sorted(one, key=lambda x: x[:2])[:10]: print(" ", x)
