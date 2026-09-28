import resource
import numpy as np
from as204_curved_heat_force import sphere_grid


def rss_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


x, w = sphere_grid(8)
G = x.shape[0]
V = [np.ones((1, G))]
Q = [None]
Gr = [np.zeros((4, 1, G))]
print("init rss KB", rss_kb())
for l in range(1, 9):
    vp = V[-1]
    nl = vp.shape[0]
    cand = np.stack([x[:, i, None] * vp.T for i in range(4)], axis=1).reshape(G, 4 * nl)
    print("  cand built l", l, "rss KB", rss_kb())
    Vprev = np.concatenate(V, axis=0)
    proj = Vprev.T @ (Vprev @ (cand * w[:, None]))
    print("  proj l", l, "rss KB", rss_kb())
    R = cand - proj
    del proj, cand
    Gram = R.T @ (R * w[:, None])
    vals, vecs = np.linalg.eigh(Gram)
    print("  eigh l", l, "rss KB", rss_kb())
    keep = vals > 1e-10 * vals[-1]
    Qm = vecs[:, keep] / np.sqrt(vals[keep][None, :])
    V.append(Qm.T @ R.T)
    Q.append(Qm.T)
    del R, Gram, vals, vecs, Vprev
    gp = Gr[l - 1]
    cg = np.zeros((4, 4 * nl, G))
    for i in range(4):
        seg = slice(i * nl, (i + 1) * nl)
        cg[:, seg, :] = np.where(np.arange(4)[:, None, None] == i, vp[None, :, :], 0.0)
        cg[:, seg, :] += x[:, i][None, None, :] * gp
    Gr.append(np.einsum("ab,jbg->jag", Qm.T, cg))
    del cg, Qm
    print("  done l", l, "rss KB", rss_kb(), "live MB",
          round((sum(v.nbytes for v in V) + sum(g.nbytes for g in Gr)) / 1e6, 1))