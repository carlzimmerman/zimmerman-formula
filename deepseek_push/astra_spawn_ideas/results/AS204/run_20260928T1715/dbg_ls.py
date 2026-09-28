import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(4)
c = np.zeros(leaf.n)
ic = leaf._idx(2)
c[ic.start] = 1.0

# (A) recursion at grid point 0
Hrec = leaf.hess_field(c)[:, :, 0]

def basis_values(pts):
    Gp = pts.shape[0]
    Vs = [np.ones((1, Gp))]
    for l in range(1, leaf.L + 1):
        vp = Vs[-1]
        nl = vp.shape[0]
        cand = np.stack([pts[:, i, None] * vp.T for i in range(4)], axis=1).reshape(Gp, 4 * nl)
        Vs.append(leaf.Q[l] @ cand.T)
    return np.concatenate(Vs, axis=0)

# (C) least-squares quadratic fit around p0: v(p0+q) = c0 + b.q + q.Aq/2
rng = np.random.default_rng(2)
p0 = leaf.x[0]
qs = rng.normal(size=(500, 4)) * 0.03
pts = p0[None, :] + qs
v = basis_values(pts).T @ c
# features: 1, q_i, q_i q_j (i<=j)
feat = [np.ones(len(qs))]
for i in range(4):
    feat.append(qs[:, i])
for i in range(4):
    for j in range(i, 4):
        feat.append(qs[:, i] * qs[:, j])
F = np.stack(feat, axis=1)
wls, *_ = np.linalg.lstsq(F, v, rcond=None)
A = np.zeros((4, 4))
k = 5
for i in range(4):
    for j in range(i, 4):
        A[i, j] = A[j, i] = wls[k] if i == j else 0.5 * wls[k]
        if i < j:
            A[i, j] = A[j, i] = 0.5 * wls[k]
        k += 1
Hls = 2 * A
resid = float(np.max(np.abs(F @ wls - v)))

print("recursion:")
print(np.round(Hrec, 5))
print("least-squares fit (resid", resid, "):")
print(np.round(Hls, 5))
print("max abs diff rec vs ls:", float(np.max(np.abs(Hrec - Hls))))