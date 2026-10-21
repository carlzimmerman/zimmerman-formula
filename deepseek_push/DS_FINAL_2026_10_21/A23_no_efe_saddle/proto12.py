import math, time
import numpy as np
import core as K
from scipy.integrate import quad
from scipy.interpolate import RegularGridInterpolator

C_LIGHT = 2.99792458e8; G = 6.67430e-11; MSUN = 1.98847e30
PC = 3.0856775814913673e16; MPC = 1.0e6 * PC
SIG_UNIT = MSUN / PC ** 2; A0 = 9.36e-11
DEEP = lambda x: np.maximum(x, 1e-14)
PHIF = lambda r: math.sqrt(2.0) * np.log(r)


def abel(x, col, Rc):
    if x < 1e-9:
        return 2.0 * np.sum(col * np.diff(np.concatenate([[0.0], Rc])))
    umax = math.acosh(max(Rc[-1] / x, 1.0001))
    us = np.linspace(0.0, umax, 2001)
    Rs = x * np.cosh(us)
    fs = np.interp(Rs, Rc, col, left=col[0], right=0.0)
    return 2.0 * x * np.sum(fs * np.cosh(us)) * (us[1] - us[0])


def aeff(g, C):
    xs = np.concatenate([[0.0], np.geomspace(0.01, 1.4, 53)])
    zrows = [j for j in range(g.NZ) if g.zc[j] < 0.16]
    D = np.zeros((len(zrows), len(xs)))
    for a, j in enumerate(zrows):
        col = np.minimum(C[:, j], 0.0)
        D[a, :] = [-abel(x, col, g.Rc) for x in xs]
    D0 = D[0, 0]
    return 4.0 * float(np.trapz(np.trapz((D / D0) ** 2, xs, axis=1), g.zc[zrows])), D0, D, xs, zrows


def orient(g, C):
    zg = np.concatenate([[0.0], g.zc])
    Cg = np.concatenate([np.minimum(C, 0.0)[:, :1], np.minimum(C, 0.0)], axis=1)
    itp = RegularGridInterpolator((g.Rc, zg), Cg, bounds_error=False, fill_value=0.0)
    def d_at(ideg):
        ii = math.radians(ideg); ts = np.linspace(0.0, 1.5, 4001)
        return 2.0 * np.sum(itp(np.column_stack([ts * math.sin(ii), ts * math.cos(ii)]))) * (ts[1] - ts[0])
    cs = np.linspace(0.0, 1.0, 41)
    dv = np.array([d_at(math.degrees(math.acos(max(c, 1e-9)))) for c in cs])
    de = d_at(90.0)
    return float(np.trapz(dv, cs) / de), de, d_at(80.0), d_at(70.0)


t0 = time.time()
for tag in ("QUMOND", "AQUAL"):
    print("===", tag)
    for h in (0.004, 0.002, 0.001, 0.0005):
        Rf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
        zf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
        g = K.Grid(Rf, zf); m = K.plummer(g, K.BFAC, 1.0, (0.5,))
        if tag == "QUMOND":
            C, _, _, _ = K.qumond(g, m, 0.0)
        else:
            Ph, pR, pZ, res, it, d = K.solve_aqual(g, m, DEEP, PHIF, alpha=0.6, itmax=400, tol=1e-9)
            C = K.laplacian(g, Ph, pR, pZ) / (4 * math.pi) - m / g.V
        Ae, D0, D, xs, zr = aeff(g, C)
        eps, de, d80, d70 = orient(g, C)
        print(f" h={h:<7.4f} A_eff={Ae:.5f} D0={D0:.4f} eps={eps:.3f} d80/d0={d80/de:+.3f} d70/d0={d70/de:+.3f}  t={time.time()-t0:.1f}")
