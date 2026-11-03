#!/usr/bin/env python3
"""K1, keys part: lambda 0 (arm Z) key Z's against RQ3's cached law keys, all three cells, both footings, both h. Line 1e-6. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); RQ3 = os.path.join(os.path.dirname(H), "RQ3_acceptance_v2", "cache_keys"); mx = 0.0
for t in ("g005_f034", "g005_f0615", "g0_f034"):
    a = json.load(open(os.path.join(H, "cache_keys", f"db1_Z_{t}", "keys.json"))); b = json.load(open(os.path.join(RQ3, f"law_{t}", "keys.json")))
    for f in ("canonical", "alt"):
        rk = f"R1|c0|{f}"
        for h, zz in a[rk]["Z"].items():
            for k, v in zz.items(): mx = max(mx, abs(v - b[rk]["Z"][h][k]))
ok = mx < 1e-6; s = f"K1-keys {'PASS' if ok else 'FAIL'} lambda 0 against RQ3's law keys, max |dZ| {mx:.1e}"; print(s); open(os.path.join(H, "db1_k1keys.out"), "w").write(s + "\n"); sys.exit(0 if ok else 1)
