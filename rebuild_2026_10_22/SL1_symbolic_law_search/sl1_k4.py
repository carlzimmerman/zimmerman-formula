#!/usr/bin/env python3
"""SL1 K4: surrogate against the grader's dvecN at A 0.5, A 2 and radial B. kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ["SL1_HERE"] = HERE
exec(compile(open(os.path.join(HERE, "discover_law.py")).read().split('if __name__ == "__main__" and "--sweep"')[0], "discover_law", "exec"), globals())
PR = [["k", "1"], ["2", "1"], ["1", ["add", "1", ["mul", "xb", ["inv1p", ["mul", "fl", "q"]]]]], [["inv1p", ["log1p", ["mul", "q", "fb"]]], "1"], ["1", ["sqrt", ["add", "1", ["mul", "xb", "2"]]]]]
os.environ.update(SL1_LANE=HERE, SL1_TREES=os.path.join(HERE, "cache", "k4_trees.json"), SL1_OUT=os.path.join(HERE, "cache", "k4_exact.json")); fx = lambda t: t if isinstance(t, str) else tuple(fx(c) if i else c for i, c in enumerate(t)); json.dump([[a, b, ["canonical"]] for a, b in PR], open(os.environ["SL1_TREES"], "w"))
subprocess.run(["nice", "-n", "15", sys.executable, os.path.join(HERE, "sl1_harvest.py"), os.path.join(HERE, "sl1_tail_exact.py")], stdout=open(os.path.join(HERE, "cache", "k4.log"), "w"), stderr=subprocess.STDOUT, check=True)
X = json.load(open(os.environ["SL1_OUT"])); D = Data(); mx = 0.0; OUT = []
for (a, b, _), r in zip([[*p, 0] for p in PR], X["res"]):
    Z = D.cluster_keys(fx(a), fx(b)); d = {h: np.array(r["Z"]["canonical"][h]) - Z[h] for h in HKS}; w = max(float(np.abs(v).max()) for v in d.values()); mx = max(mx, w); k = KEYS[int(np.argmax(np.abs(d[HKS[0]])))]; OUT.append(f"  A {to_s(fx(a))} B {to_s(fx(b))}: max |dZ| {w:.3f} at {k}; exact worst |Z| {max(np.abs(r['Z']['canonical'][h]).max() for h in HKS):.2f}, surrogate {max(np.abs(Z[h]).max() for h in HKS):.2f}")
ok = mx <= 0.05; OUT.append(f"K4 surrogate vs dvecN: max |dZ| {mx:.3f}: {'PASS' if ok else 'FAIL'}"); print("\n".join(OUT)); open(os.path.join(HERE, "sl1_k4.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
