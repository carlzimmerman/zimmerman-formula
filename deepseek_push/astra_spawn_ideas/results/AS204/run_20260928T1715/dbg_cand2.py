import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(4)
p0 = leaf.x[0]

def fit_hess(fvals, qs):
    """quadratic least-squares hessian from values at p0+qs"""
    feat = [np.ones(len(qs))]
    for i in range(4):
        feat.append(qs[:, i])
    for i in range(4):
        for j in range(i, 4):
            feat.append(qs[:, i] * qs[:, j])
    F = np.stack(feat, axis=1)
    wls, *_ = np.linalg.lstsq(F, fvals, rcond=None)
    A = np.zeros((4, 4))
    k = 5
    for i in range(4):
        for j in range(i, 4):
            if i == j:
                A[i, i] = wls[k]
            else:
                A[i, j] = A[j, i] = 0.5 * wls[k]
            k += 1
    return 2 * A

rng = np.random.default_rng(7)
qs = rng.normal(size=(800, 4)) * 0.02
pts = p0[None, :] + qs

# all level-2 candidates c_b = x_i * Y10gamma: values at pts
vp1 = leaf.Q[1] @ pts.T          # (4, Gp) level-1 values
nl1 = 4
cand = np.zeros((16, len(qs)))
for i in range(4):
    for g in range(nl1):
        cand[i * nl1 + g] = pts[:, i] * vp1[g]
# true hessians
Htrue_cand = np.zeros((4, 4, 16))
for b in range(16):
    Htrue_cand[:, :, b] = fit_hess(cand[b], qs)
# mode = beta of level 2: Q2 (9,16): hessian of mode beta:
for beta in (0, 1):
    Hm = np.einsum("jkb,b->jk", Htrue_cand, leaf.Q[2][beta])
    c = np.zeros(leaf.n)
    ic = leaf._idx(2)
    c[ic.start + beta] = 1.0
    Hrec = leaf.hess_field(c)[:, :, 0]
    print("beta", beta, "true-from-candidates:")
    print(np.round(Hm, 5))
    print("recursion:")
    print(np.round(Hrec, 5))
    print("max abs diff:", float(np.max(np.abs(Hm - Hrec))))