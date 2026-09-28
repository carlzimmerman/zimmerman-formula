"""Independent finite-difference verification of the AS204 derivative machinery (S3 leaf)."""
import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(6)

def basis_values(pts):
    Gp = pts.shape[0]
    Vs = [np.ones((1, Gp))]
    for l in range(1, leaf.L + 1):
        vp = Vs[-1]
        nl = vp.shape[0]
        cand = np.stack([pts[:, i, None] * vp.T for i in range(4)], axis=1).reshape(Gp, 4 * nl)
        Vs.append(leaf.Q[l] @ cand.T)
    return np.concatenate(Vs, axis=0)

def grad_ambient_at(cv, pts):
    pts = np.atleast_2d(pts)
    Gp = pts.shape[0]
    gl = [np.zeros((4, 1, Gp))]
    off = 0
    for l in range(1, leaf.L + 1):
        vp_all = basis_values(pts)
        vp = vp_all[off:off + leaf.dims[l - 1]]
        off += leaf.dims[l - 1]
        nl = vp.shape[0]
        cgc = np.zeros((4, 4 * nl, Gp))
        for i in range(4):
            seg = slice(i * nl, (i + 1) * nl)
            cgc[:, seg, :] = np.where(np.arange(4)[:, None, None] == i, vp[None, :, :], 0.0)
            cgc[:, seg, :] += pts[:, i][None, None, :] * gl[-1]
        gl.append(np.einsum("ab,jbg->jag", leaf.Q[l], cgc))
    g = np.zeros((4, Gp))
    for l in range(1, leaf.L + 1):
        cc = cv[leaf._idx(l)]
        if np.any(cc):
            g += np.einsum("a,jag->jg", cc, gl[l])
    return g

def Aext(cv, p):
    gp_ = grad_ambient_at(cv, p)[:, 0]
    return -(gp_ - (gp_ @ p) * p)

def formula_norm(Jmat, pts):
    out = []
    for g0 in range(pts.shape[0]):
        xx = pts[g0]
        Jx = Jmat[:, :, g0] @ xx
        JTx = Jmat[:, :, g0].T @ xx
        out.append(float(np.sum(Jmat[:, :, g0] ** 2)) - float(np.sum(Jx * Jx))
                   - float(np.sum(JTx * JTx)) + float((Jx @ xx) ** 2))
    return np.array(out)

def direct_norm(cv, pts, eps=1e-5):
    out = []
    for g0 in range(pts.shape[0]):
        xx = pts[g0]
        Tb = np.eye(4) - np.outer(xx, xx)
        uu, _ = np.linalg.qr(Tb)
        uu = uu[:, :3]
        val = 0.0
        for a in range(3):
            u = uu[:, a]
            xpp = xx + eps * u; xpm = xx - eps * u
            xpp /= np.linalg.norm(xpp); xpm /= np.linalg.norm(xpm)
            duA = (Aext(cv, xpp) - Aext(cv, xpm)) / (2 * eps)
            duA = duA - np.dot(duA, xx) * xx
            val += float(np.sum(duA * duA))
        out.append(val)
    return np.array(out)

pts = leaf.x[:40]
for l in (2, 3, 4):
    ic = leaf._idx(l)
    c = np.zeros(leaf.n); c[ic.start] = 1.0
    gA = leaf.grad_ambient(c)
    Hv = leaf.hess_field(c)
    gAx = np.einsum("jg,jg->g", gA, leaf.x.T)
    Hxx = np.einsum("ijg,jg->ig", Hv, leaf.x.T)
    J = -Hv.copy()
    for i in range(4):
        J[:, i, :] += (Hxx[i][None, :] + gA[i][None, :]) * leaf.x.T
        J[i, i, :] += gAx
    f = formula_norm(J[:, :, :40], pts)
    d = direct_norm(c, pts)
    rel = np.abs(f - d) / (np.abs(f) + 1e-30)
    print("l", l, "max rel err (formula vs FD):", float(np.max(rel)),
          "median:", float(np.median(rel)))
print("FD verification complete")