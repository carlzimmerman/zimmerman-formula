import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(4)
for l in range(1, 5):
    ic = leaf._idx(l)
    for mm in range(2):
        e = np.zeros(leaf.n); e[ic.start + mm] = 1.0
        He = leaf.hess_field(e)
        h2 = float(np.sum(np.einsum("ijg,ijg->g", He, He) * leaf.w))
        lam = float(leaf.lam[ic.start + mm])
        print(f"l={l} mode={ic.start + mm} lam={lam} intTr(H^2)={h2:.6f} lam(lam-2)={lam*(lam-2):.1f} ratio={h2/(lam*(lam-2) if lam>2 else 1):.6f}")