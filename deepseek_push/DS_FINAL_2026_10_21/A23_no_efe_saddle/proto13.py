import math, time
import numpy as np
import scipy.sparse as sps, scipy.sparse.linalg as spla
src = open("a23_checks.py").read()
marker = "# --------------------------------------------------------------------------- S1 symbolic"
exec(src[:src.index(marker)], globals())

t0 = time.time()
hh = 0.006


def aqual_full(e, XM):
    Rf = make_faces(XM, [(0.0, hh), (0.5, hh)])
    zf = make_faces_sym(XM, [(0.0, hh), (0.5, hh)])
    g = Grid(Rf, zf)
    m = plummer(g, BFAC, 2.0, (0.5, -0.5))
    Mb = 2.0

    def far(R, Z):
        if e == 0.0:
            return math.sqrt(Mb) * np.log(np.hypot(R, Z))
        u = np.sqrt(R ** 2 + Z ** 2 / 2.0)
        return e * Z - Mb / (e * u)

    Rb = np.hypot(g.Rf[-1], g.zc)
    Zb = np.hypot(g.Rc, g.zf[-1])
    pbR, pbZ = far(g.Rf[-1], g.zc), far(g.Rc, g.zf[-1])
    rhs = 4 * math.pi * m.ravel()
    Phi = far(g.RR, g.ZZ)
    mu = coeffs(g, Phi, pbR, pbZ, DEEP, 0.0)
    it = 0
    for it in range(800):
        A, b = assemble(g, *mu, pbR, pbZ)
        Pn = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        Pn = Phi + 0.6 * (Pn - Phi)
        d = np.max(np.abs(Pn - Phi)) / (np.max(Pn) - np.min(Pn))
        Phi = Pn
        mu_new = coeffs(g, Phi, pbR, pbZ, DEEP, 0.0)
        mu = tuple(np.sqrt(u * v) for u, v in zip(mu, mu_new))
        if d < 1e-8 and it > 3:
            break
    C = laplacian(g, Phi, pbR, pbZ) / (4 * math.pi) - m / g.V
    S, row = column_S(g, C)
    return S, float(np.interp(0.2, g.Rc, row)), it, g.N


S0 = None
for e in (0.0, 0.1, 0.3, 1.0, 3.0):
    S, C02, it, N = aqual_full(e, 6.0)
    if e == 0.0: S0 = S
    print(f"box6 e={e:4.2f} S={S:+.6f} S/S0={S/S0:.4f} C02={C02:+.4f} it={it} t={time.time()-t0:.1f}")
for e in (0.3, 1.0):
    S, C02, it, N = aqual_full(e, 8.0)
    S00, _, _, _ = aqual_full(0.0, 8.0)
    print(f"box8 e={e:4.2f} S={S:+.6f} S/S0={S/S00:.4f} C02={C02:+.4f} it={it} t={time.time()-t0:.1f}")
