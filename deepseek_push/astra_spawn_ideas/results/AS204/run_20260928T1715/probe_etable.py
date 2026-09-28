import json
import numpy as np
import as204_curved_heat_force as m

tbl = {}
for L in (10, 11):
    leaf = m.S3(L)
    e = {}
    for l in range(1, leaf.L + 1):
        ic = leaf._idx(l)
        v = np.zeros(leaf.n); v[ic.start] = 1.0
        He = leaf.hess_field(v)
        e[l] = float(np.sum(np.einsum("ijg,ijg->g", He, He) * leaf.w))
    tbl[L] = e
    print("L", L, json.dumps(e))
json.dump(tbl, open("e2mode_table.json", "w"), indent=1)