#!/usr/bin/env python3
"""BF3 K4 planted: mock from H = 1 + f sqrt(y)/(1+y), W2, must come back as a joint form. BF3_MUTATE=1 tightens lines to 1e-6 and scales H: nothing recovered, exit 1. kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
from bf3_read import *
from bf3_search import PL_T
a, b, op, w = PL_T; T = f"({a}{op}{b})"; root = "shards_planted"; shutil = __import__("shutil"); shutil.rmtree(os.path.join(LANE, root, f"planted_canonical_A{TAG}"), ignore_errors=True)
r = subprocess.run([sys.executable, os.path.join(LANE, "bf3_search.py"), "planted", "canonical", "A", "1"], env=dict(os.environ, BF3_OUT=root), capture_output=True, text=True); print(r.stdout[-300:], r.stderr[-300:])
Hf0 = lambda y, e, f: 1 + f * eval(T, {"__builtins__": {}}, dict(FN, y=y, ell=e, f=f)); E = Exact("canonical", (Hf0, w)); D = json.load(open(os.path.join(LANE, root, f"planted_canonical_A{TAG}", "000000.json")))
d = json.load(open(os.path.join(CACHE, "pool_canonical_real.json"))); nm = d["names"]; ia, ib = sorted((nm.index(a), nm.index(b))); hit = [q for q in D["rec"] if q[0] == ia and q[1] == "+-*/".index(op) and q[2] == ib and q[3] == w]
print("expressions", D["cnt"]["tried"], "rec", len(D["rec"]), "planted record", hit)
o = E.all(form_fn(T, "A"), w); print("exact on mock:", json.dumps(o, default=float)[:600])
ok = bool(hit) and o["lens"]["sys"] < 1e-3 and abs(o["X"]["mean"]) < 1e-9 and abs(o["G"]["0.6"]["v"]) < 1e-9 and o["S"]["rms"] < 1e-3 and o["S"]["U"] == .65
lines_1e6 = abs(o["X"]["mean"]) <= 1e-6 and o["lens"]["sys"] <= 1e-6
print(f"K4 {'PASS' if ok else 'FAIL'}: planted form recovered at zero distance; at 1e-6 lines recovered: {lines_1e6}")
json.dump(dict(ok=ok, hit=hit, exact=o, tried=D["cnt"]["tried"]), open(os.path.join(LANE, f"bf3_k4{TAG}.json"), "w"), indent=0, sort_keys=True, default=float)
sys.exit(1 if MUT or not ok else 0)
