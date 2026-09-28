import numpy as np
import as204_curved_heat_force as m

x, w = m.sphere_grid(4)
print("sum w", w.sum(), "int x0^2", float(np.sum(x[:, 0] ** 2 * w)), "expect 0.25")
print("int x0^2 x1^2", float(np.sum(x[:, 0] ** 2 * x[:, 1] ** 2 * w)), "expect 1/12")

leaf = m.S3(4)
print("n", leaf.n, "gram", leaf.gram_residual)
# intrinsic grad gram for level 1, diagonal only
ics = leaf._idx(1)
e = np.zeros(leaf.n); e[ics.start] = 1.0
g = leaf.grad(e)
n2 = float(np.sum(g * g * w[None, :]))
print("||grad_S Y_1||^2 integrated:", n2, "expect 3")
print("|g.x|^2:", float(np.sum(np.einsum("jg,jg->g", g, leaf.x.T) ** 2 * w)))
# direct check: ambient grad squared
ga = np.zeros((4, leaf.G))
for l in range(1, leaf.L + 1):
    icc = leaf._idx(l)
    cc = e[icc]
    if np.any(cc):
        ga += np.einsum("a,jag->jg", cc, leaf.grad_level(l))
print("||grad_amb Y_1||^2 integrated:", float(np.sum(ga * ga * w[None, :])))
gx = np.einsum("jg,jg->g", ga, leaf.x.T)
print("||grad_amb||^2 - (g.x)^2:", float(np.sum((ga * ga - (gx[None, :] * leaf.x.T) ** 2) * w[None, :])))
# what is the actual direction of the mode?  check norm of Y itself
yv = leaf.values(e)
print("||Y_1||^2:", float(np.sum(yv * yv * w)))
# projection check at one point: is (g - (g.x)x) tangent?
gxpt = np.einsum("jg,jg->g", g, leaf.x.T)
print("tangency (g . x) max:", float(np.max(np.abs(gxpt))), "expect ~0")