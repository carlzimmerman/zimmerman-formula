import resource
import numpy as np
import as204_curved_heat_force as m


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


print("start rss MB", round(rss_mb(), 1))
leaf = m.S3(10)
print("after leaf build rss MB", round(rss_mb(), 1))
b = 0.05
rng = np.random.default_rng(204)
csrc = np.zeros(leaf.n)
for l in range(1, leaf.L + 1):
    csrc[leaf._idx(l)] = rng.standard_normal(leaf.dims[l]) / (l + 1) ** 1.5
gu = leaf.grad(csrc)
print("after grad rss MB", round(rss_mb(), 1))
H0 = leaf.grad(leaf.heat(csrc, b))
print("after heat/grad rss MB", round(rss_mb(), 1))
supH = float(np.sqrt(np.max(np.sum(H0 ** 2, axis=0))))
csrc *= 2.3374 / supH
H0 = leaf.grad(leaf.heat(csrc, b))
Hm = np.sqrt(np.sum(H0 ** 2, axis=0))
Fv = (m.h_mono(Hm) / np.where(Hm > 0, Hm, 1.0)) * H0
dFc = np.zeros(leaf.n)
for l in range(1, leaf.L + 1):
    gl = leaf.grad_level(l)
    dFc[leaf._idx(l)] = -np.einsum("jg,jag->a", Fv * leaf.w[None, :], gl)
print("after dFc rss MB", round(rss_mb(), 1))
Hv = leaf.hess_field(csrc)
print("after hess_field rss MB", round(rss_mb(), 1))
gA = leaf.grad_ambient(csrc)
print("after grad_ambient rss MB", round(rss_mb(), 1))