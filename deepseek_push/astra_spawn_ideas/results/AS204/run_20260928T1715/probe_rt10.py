import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(10)
rng = np.random.default_rng(7)
v = np.zeros(leaf.n)
for l in range(1, leaf.L + 1):
    v[leaf._idx(l)] = rng.standard_normal(leaf.dims[l]) / (l + 1.0)
fv = leaf.values(v)
v2 = leaf.coeffs(fv)
rel = float(np.max(np.abs(v2 - v))) / float(np.max(np.abs(v)))
print("round trip rel err:", rel)
g1 = leaf.grad(v)
g2 = leaf.grad(v2)
d = np.abs(g1 - g2)
print("grad diff max", float(np.max(d)), "grad scale", float(np.sqrt(np.mean(g1 ** 2))))
print("g1 NaN", np.isnan(g1).any(), "g2 NaN", np.isnan(g2).any())
print("v2 NaN", np.isnan(v2).any(), "fv NaN", np.isnan(fv).any())