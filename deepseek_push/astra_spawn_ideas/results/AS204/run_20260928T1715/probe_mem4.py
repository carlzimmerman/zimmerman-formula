import resource
import numpy as np
import as204_curved_heat_force as m


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


leaf = m.S3.load_cache("leaf_L8.npz")
print("loaded rss MB", round(rss(), 1))
rng = np.random.default_rng(1)
c = rng.standard_normal(leaf.n)
gA = leaf.grad_ambient(c)
print("grad_ambient rss MB", round(rss(), 1))
Hv = leaf.hess_field(c)
print("hess_field rss MB", round(rss(), 1))
tr = np.einsum("ijg,ijg->g", Hv, Hv)
print("einsum tr rss MB", round(rss(), 1))
gAx = np.einsum("jg,jg->g", gA, leaf.x.T)
Hxx = np.einsum("ijg,jg->ig", Hv, leaf.x.T)
J = -Hv.copy()
print("J build rss MB", round(rss(), 1))
for i in range(4):
    J[:, i, :] += (Hxx[i][None, :] + gA[i][None, :]) * leaf.x.T
    J[i, i, :] += gAx
Jx = np.einsum("ijg,jg->ig", J, leaf.x.T)
JTx = np.einsum("ijg,ig->jg", J, leaf.x.T)
xJx = np.einsum("ijg,ig,jg->g", J, leaf.x.T, leaf.x.T)
print("J reductions rss MB", round(rss(), 1))
daph2 = tr - np.einsum("ig,ig->g", Jx, Jx) - np.einsum("jg,jg->g", JTx, JTx) + xJx
print("final rss MB", round(rss(), 1))