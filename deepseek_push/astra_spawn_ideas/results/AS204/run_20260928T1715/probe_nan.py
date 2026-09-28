import math
import numpy as np
import as204_curved_heat_force as m


def math_safe(x):
    return math.sqrt(float(x))


leaf = m.S3(6)
b = 0.05
rng = np.random.default_rng(204)
csrc = np.zeros(leaf.n)
for l in range(1, leaf.L + 1):
    csrc[leaf._idx(l)] = rng.standard_normal(leaf.dims[l]) / (l + 1) ** 1.5
gu = leaf.grad(csrc)
csrc /= math_safe(np.sum(gu ** 2 * leaf.w[None, :]))
H0 = leaf.grad(leaf.heat(csrc, b))
supH = math_safe(np.max(np.sum(H0 ** 2, axis=0)))
csrc *= 2.3374 / supH
H0 = leaf.grad(leaf.heat(csrc, b))
Hm = np.sqrt(np.sum(H0 ** 2, axis=0))
Fv = (m.h_mono(Hm) / np.where(Hm > 0, Hm, 1.0)) * H0
print("H0 NaN:", np.isnan(H0).any(), "Hm min:", float(np.min(Hm)))
print("F NaN:", np.isnan(Fv).any(), "F max:", float(np.max(np.abs(Fv))))
dFc = np.zeros(leaf.n)
for l in range(1, leaf.L + 1):
    gl = leaf.grad_level(l)
    dFc[leaf._idx(l)] = -np.einsum("jg,jag->a", Fv * leaf.w[None, :], gl)
print("dFc NaN:", np.isnan(dFc).any())
up = leaf.green(dFc)
up[0] = 0.0
print("up NaN:", np.isnan(up).any())
c0 = leaf.coeffs(leaf.values(up))
print("round trip rel:", float(np.max(np.abs(c0 - up))) / float(np.max(np.abs(up)) + 1e-30))
print("up first modes:", np.round(up[:10], 5))