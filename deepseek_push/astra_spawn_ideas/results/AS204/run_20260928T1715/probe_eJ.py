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
        gA = leaf.grad_ambient(v)
        Hv = leaf.hess_field(v)
        gAx = np.einsum("jg,jg->g", gA, leaf.x.T)
        Hxx = np.einsum("ijg,jg->ig", Hv, leaf.x.T)
        J = -Hv.copy()
        for i in range(4):
            J[:, i, :] += (Hxx[i][None, :] + gA[i][None, :]) * leaf.x.T
            J[i, i, :] += gAx
        e[l] = float(np.sum(np.einsum("ijg,ijg->g", J, J) * leaf.w))
    tbl[L] = e
    print("L", L, json.dumps(e))
json.dump(tbl, open("eJ_table.json", "w"), indent=1)