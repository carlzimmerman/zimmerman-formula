import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(4)
p0 = leaf.x[0]

# level-1 basis values at arbitrary points (polynomials)
def bv_1(pts):
    return leaf.Q[1] @ pts.T  # (4, Gp): candidate x_i -> Q combination

# candidate C = x_0 * Y_{1,0}  (Y_{1,0} = first level-1 basis func)
# true ambient hessian of C at p0 (least squares quadratic fit)
rng = np.random.default_rng(7)
qs = rng.normal(size=(800, 4)) * 0.02
pts = p0[None, :] + qs
Y1 = bv_1(pts)[0]            # Y_{1,0} at pts
C = pts[:, 0] * Y1           # x_0 * Y
feat = [np.ones(len(qs))]
for i in range(4):
    feat.append(qs[:, i])
for i in range(4):
    for j in range(i, 4):
        feat.append(qs[:, i] * qs[:, j])
F = np.stack(feat, axis=1)
wls, *_ = np.linalg.lstsq(F, C, rcond=None)
A = np.zeros((4, 4))
k = 5
for i in range(4):
    for j in range(i, 4):
        if i == j:
            A[i, i] = wls[k]
        else:
            A[i, j] = A[j, i] = 0.5 * wls[k]
        k += 1
Htrue = 2 * A
print("true hessian of x0*Y10 at p0:")
print(np.round(Htrue, 5))
print("Y10(p0) =", float(Y1[0]), " dY10 at p0 (via level-1 grad)")
Gl1 = leaf.grad_level(1)[:, :, 0]   # (j, gamma)
print("Gl1[:,0] =", np.round(Gl1[:, 0], 5))
# recursion terms at l=2, i=0, candidate gamma=0:
# term1(k-slot): delta[k,0]*G[j]; term2: delta[j,0]*G[k]; term3: x0 * Hess(Y10) [=0 at level1]
for j in range(4):
    for k in range(4):
        t1 = (k == 0) * Gl1[j, 0]
        t2 = (j == 0) * Gl1[k, 0]
        val = t1 + t2
        if abs(Htrue[j, k] - val) > 1e-6:
            print("MISMATCH jk", j, k, "true", round(Htrue[j, k], 5), "terms", round(val, 5))