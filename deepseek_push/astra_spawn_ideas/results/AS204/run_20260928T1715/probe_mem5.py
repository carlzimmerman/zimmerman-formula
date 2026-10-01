import resource
import numpy as np
import as204_curved_heat_force as m


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


leaf = m.S3.load_cache("leaf_L8.npz")
print("loaded rss MB", round(rss(), 1))
rng = np.random.default_rng(1)
c = rng.standard_normal(leaf.n)
H = np.zeros((4, 4, leaf.G))
x = leaf.x
block = 640
for b0 in range(0, leaf.G, block):
    b1 = min(b0 + block, leaf.G)
    sl = slice(b0, b1)
    blk = b1 - b0
    Hprev = np.zeros((4, 4, 1, blk))
    for l in range(1, leaf.L + 1):
        ic = leaf._idx(l)
        cc = c[ic]
        nl1 = leaf.V[l - 1].shape[0]
        Gp = leaf.grad_level(l - 1)
        Gpb = Gp[:, :, sl]
        ch = np.zeros((4, 4, 4 * nl1, blk))
        for i in range(4):
            seg = slice(i * nl1, (i + 1) * nl1)
            for j in range(4):
                ch[j, :, seg, :] += (np.arange(4)[:, None, None] == i) * Gpb[j][None, :, :]
            ch[:, :, seg, :] += (np.arange(4)[:, None, None, None] == i) * Gpb[None, :, :, :]
            ch[:, :, seg, :] += x[sl, i][None, None, None, :] * Hprev
        print("  block", b0, "l", l, "rss MB", round(rss(), 1), "ch MB",
              round(ch.nbytes / 1e6, 1))
        Hl = np.einsum("ab,jkbg->jkag", leaf.Q[l], ch)
        print("    after einsum rss MB", round(rss(), 1))
        Hprev = Hl
        if np.any(cc):
            H[:, :, sl] += np.einsum("a,jkag->jkg", cc, Hl)
print("hess_field done rss MB", round(rss(), 1))