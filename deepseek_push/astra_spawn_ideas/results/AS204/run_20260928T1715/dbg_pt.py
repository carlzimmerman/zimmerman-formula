import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(4)
Gp = 1
pts = leaf.x[:1]  # one grid point

def basis_values(pts):
    Gp = pts.shape[0]
    Vs = [np.ones((1, Gp))]
    for l in range(1, leaf.L + 1):
        vp = Vs[-1]
        nl = vp.shape[0]
        cand = np.stack([pts[:, i, None] * vp.T for i in range(4)], axis=1).reshape(Gp, 4 * nl)
        Vs.append(leaf.Q[l] @ cand.T)
    return np.concatenate(Vs, axis=0)

c = np.zeros(leaf.n)
ic = leaf._idx(2)
c[ic.start] = 1.0

Hrec = leaf.hess_field(c)[:, :, :1]

# direct polynomial hessian via exact FD on the polynomial extension (quadratic -> exact)
eps = 1e-4
p0 = pts[0]
Hfd = np.zeros((4, 4))
for i in range(4):
    pp = p0.copy(); pp[i] += eps; pn = p0.copy(); pn[i] -= eps
    Hfd[i, i] = (basis_values(pp[None, :]).T @ c - 2 * (basis_values(p0[None, :]).T @ c)
                 + basis_values(pn[None, :]).T @ c)[0] / eps ** 2
    for j in range(i + 1, 4):
        ppp = p0.copy(); ppp[i] += eps; ppp[j] += eps
        pnm = p0.copy(); pnm[i] -= eps; pnm[j] -= eps
        ppm = p0.copy(); ppm[i] += eps; ppm[j] -= eps
        pmp = p0.copy(); pmp[i] -= eps; pmp[j] += eps
        vpp = basis_values(ppp[None, :]).T @ c; vnm = basis_values(pnm[None, :]).T @ c
        vpm = basis_values(ppm[None, :]).T @ c; vmp = basis_values(pmp[None, :]).T @ c
        Hfd[i, j] = Hfd[j, i] = (vpp + vnm - vpm - vmp)[0] / (4 * eps ** 2)

print("pts", p0)
print("rec:")
print(np.round(Hrec[:, :, 0], 6))
print("fd:")
print(np.round(Hfd, 6))
# direct polynomial coefficients: v = sum Q[2] (i,g) x_i * v1_g ... v1 = 2(R x)
B0 = basis_values(p0[None, :])
print("v(p0) via basis:", float(B0.T @ c), " fd second-deriv central diag check")
# tangent projection consistency: Hessian symmetric?
print("sym residual rec/fd:", float(np.max(np.abs(Hrec[:, :, 0] - Hfd))))