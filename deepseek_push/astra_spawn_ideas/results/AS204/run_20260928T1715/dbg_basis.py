import numpy as np
import as204_curved_heat_force as m

print("Y_STAR", m.Y_STAR, "Y_P", m.Y_P, "H_P", m.H_P)
x, w = m.sphere_grid(4)
G = x.shape[0]
leaf = m.S3.__new__(m.S3)
leaf.L = 4
leaf.x, leaf.w, leaf.G = x, w, G
leaf.V = [np.ones((1, G))]
leaf.Q = [None]
for l in range(1, 5):
    vp = leaf.V[-1]
    nl = vp.shape[0]
    cand = np.stack([x[:, i, None] * vp.T for i in range(4)], axis=1).reshape(G, 4 * nl)
    Vprev = np.concatenate(leaf.V, axis=0)
    proj = Vprev.T @ (Vprev @ (cand * w[:, None]))
    R = cand - proj
    Gram = R.T @ (R * w[:, None])
    vals, vecs = np.linalg.eigh(Gram)
    keep = vals > 1e-10 * vals[-1]
    nk = int(np.count_nonzero(keep))
    print("level", l, "cand", cand.shape, "kept", nk, "expected", (l + 1) ** 2,
          "eigsum", float(vals.sum()), "eigs", np.round(vals, 4))
    assert nk == (l + 1) ** 2
    Q = vecs[:, keep] / np.sqrt(vals[keep][None, :])
    leaf.V.append(Q.T @ R.T)
    leaf.Q.append(Q.T)
for l in (1, 2, 3, 4):
    Gr = (leaf.V[l] * w[None, :]) @ leaf.V[l].T
    print("level", l, "gram-id residual", float(np.max(np.abs(Gr - np.eye(Gr.shape[0])))))
# gradient / hessian via the public intrinsic grad() and the 4-term derivative formula
leaf.n = sum(v.shape[0] for v in leaf.V)
leaf.dims = [v.shape[0] for v in leaf.V]
for l in (1, 2, 3):
    ids = np.zeros((leaf.dims[l], leaf.dims[l]))
    ic = leaf._idx(l)
    for a in range(leaf.dims[l]):
        e = np.zeros(leaf.n); e[ic.start + a] = 1.0
        ga = leaf.grad(e)
        for bb in range(a, leaf.dims[l]):
            eb = np.zeros(leaf.n); eb[ic.start + bb] = 1.0
            ids[a, bb] = float(np.sum(ga * leaf.grad(eb) * w[None, :]))
    lam = l * (l + 2)
    err = float(np.max(np.abs(ids - lam * np.eye(ids.shape[0]))))
    print("level", l, "intrinsic grad gram residual", err)
for l in (1, 2, 3):
    ic = leaf._idx(l)
    e = np.zeros(leaf.n); e[ic.start] = 1.0
    Hv = leaf.hess_field(e)
    tr = np.einsum("ijg,ijg->g", Hv, Hv)
    Hx = np.einsum("ijg,jg->ig", Hv, leaf.x.T)
    xxJx = np.einsum("ijg,ig,jg->g", Hv, leaf.x.T, leaf.x.T)
    d2 = tr - 2.0 * np.einsum("ig,ig->g", Hx, Hx) + xxJx
    int_d2 = float(np.sum(np.maximum(d2, 0.0) * w))
    lam = l * (l + 2)
    print("mode", l, "||grad(-grad_S Y)||^2 integrated", round(int_d2, 6),
          "expected lam(lam-2)", lam * (lam - 2.0))