import math, time
import numpy as np
import core as K

DEEP = lambda x: np.maximum(x, 1e-14)
PHIF = lambda r: math.sqrt(2.0) * np.log(r)
h = 0.005
Rf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
zfh = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
zff = K.make_faces_sym(K.XMAX, [(0.0, h), (0.5, h)])
gh = K.Grid(Rf, zfh); mh = K.plummer(gh, K.BFAC, 1.0, (0.5,))
gf = K.Grid(Rf, zff); mf = K.plummer(gf, K.BFAC, 2.0, (0.5, -0.5))
print("N half", gh.N, "N full", gf.N)

t0 = time.time()
print("=== AQUAL ===")
for tag, g, m in (("half", gh, mh), ("full", gf, mf)):
    prev = None
    for e in (0.0, 0.3, 1.0, 3.0):
        Ph, pR, pZ, res, it, d = K.solve_aqual(g, m, DEEP, PHIF, e=e, alpha=0.3,
                                               itmax=800, tol=1e-7, Phi0=prev)
        prev = Ph
        C = K.laplacian(g, Ph, pR, pZ) / (4 * math.pi) - m / g.V
        S, row = K.column_S(g, C)
        print(f" {tag:4s} e={e:4.1f} S={S:+.5f} C02={np.interp(0.2,g.Rc,row):+.4f} it={it:3d} res={res:.1e} t={time.time()-t0:.1f}")
print("=== QUMOND ===")
for tag, g, m in (("half", gh, mh), ("full", gf, mf)):
    for e in (0.0, 0.3, 1.0, 3.0):
        C, _, _, res = K.qumond(g, m, e=e)
        S, row = K.column_S(g, C)
        print(f" {tag:4s} e={e:4.1f} S={S:+.5f} C02={np.interp(0.2,g.Rc,row):+.4f} res={res:.1e} t={time.time()-t0:.1f}")
    for e in (1.0,):
        C, _, _, res = K.qumond(g, m, e=e, include_ext=False)
        S, row = K.column_S(g, C)
        print(f" {tag:4s} own-source e={e}: S={S:+.5f} C02={np.interp(0.2,g.Rc,row):+.4f}")
