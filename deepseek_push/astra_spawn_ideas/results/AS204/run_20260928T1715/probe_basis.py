import time
import numpy as np
import as204_curved_heat_force as m

print("y_star", m.Y_STAR, "y_p", m.Y_P, "h_p", m.H_P)
for L in (4, 8, 10):
    t = time.time()
    leaf = m.S3(L)
    dt = time.time() - t
    print("L", L, "n", leaf.n, "grid", leaf.G, "gram_res", leaf.gram_residual, "build_s", round(dt, 1))
    c = np.zeros(leaf.n); c[leaf._idx(1).start] = 1.0
    t = time.time(); H = leaf.hess_field(c)
    h2 = float(np.sum(np.einsum("ijg,ijg->g", H, H) * leaf.w))
    print("  hess l=1 mode: s", round(time.time() - t, 2), "Hess2_int", round(h2, 6), "expected 3")
    c2 = np.zeros(leaf.n); c2[leaf._idx(2).start] = 1.0
    t = time.time(); H2 = leaf.hess_field(c2)
    h22 = float(np.sum(np.einsum("ijg,ijg->g", H2, H2) * leaf.w))
    print("  hess l=2 mode: s", round(time.time() - t, 2), "Hess2_int", round(h22, 6), "expected 8")