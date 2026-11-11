#!/usr/bin/env python3
"""HLF1 KA-A3 (FROZEN_CRITERIA 123947b9dc): with the inherited list put back, the copied pipeline reproduces CO1's stored numbers.
  python3 hlf1_ka_a3.py -> hlf1_ka_a3.json / .out     (after the inherited hm / linear / shear / grade runs)
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CO1 = os.path.join(HERE, "..", "..", "closure_2026_11_09", "CO1_form_b_cosmology_computed")
def ld(d, f): return json.load(open(os.path.join(d, f)))
out = []; res = {}
def walk(a, b, path, worst):
    if isinstance(a, dict):
        for k in a:
            if k in b: walk(a[k], b[k], path + "/" + k, worst)
    elif isinstance(a, list) and a and isinstance(a[0], (int, float)) and not isinstance(a[0], bool):
        x, y = np.array(a, float), np.array(b, float)
        if x.shape == y.shape: worst.append((float(np.max(np.abs(x - y) / np.maximum(np.abs(y), 1e-300))), path))
    elif isinstance(a, float) and isinstance(b, float):
        worst.append((abs(a - b) / max(abs(b), 1e-300), path))
A, B = ld(HERE, "hlf1_hm_inherited.json"), ld(CO1, "co1_hm.json"); w = []
for key in ("primary", "brackets", "MUTATE"): walk(A[key], B[key], key, w)
m = max(w); res["hm"] = dict(max_rel=m[0], where=m[1], n=len(w), pass_=bool(m[0] <= 1e-10)); out.append(f"hm arrays: {len(w)} compared, max rel {m[0]:.1e} at {m[1]} -> {'PASS' if res['hm']['pass_'] else 'FAIL'}")
for nm, f1, f2 in (("linear", "hlf1_linear_inherited.json", "co1_linear.json"), ("shear", "hlf1_shear_inherited.json", "co1_shear.json"), ("rows", "hlf1_rows_inherited.json", "co1.json")):
    if not os.path.exists(os.path.join(HERE, f1)): out.append(f"{nm}: not run"); continue
    A, B = ld(HERE, f1), ld(CO1, f2); w = []; walk(A, B, nm, w)
    absd = []
    def walk_abs(a, b, p):
        if isinstance(a, dict):
            for k in a:
                if k in b and k not in ("t",): walk_abs(a[k], b[k], p + "/" + k)
        elif isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)): absd.append((abs(a - b), p))
        elif isinstance(a, str) and isinstance(b, str) and a != b and not p.endswith(("lane", "criteria", "note", "part")): absd.append((float("inf"), p + " (label " + a + " vs " + b + ")"))
    walk_abs(A, B, nm); m = max(absd) if absd else (0.0, "-")
    res[nm] = dict(max_abs=m[0], where=m[1], n=len(absd)); out.append(f"{nm}: {len(absd)} scalars compared, max |diff| {m[0]:.2e} at {m[1]}")
res["note"] = "kappa = 1/2 FITTED; not theory closed; adopts nothing"
json.dump(res, open(os.path.join(HERE, "hlf1_ka_a3.json"), "w"), indent=1); print("\n".join(out)); open(os.path.join(HERE, "hlf1_ka_a3.out"), "w").write("\n".join(out) + "\n")
