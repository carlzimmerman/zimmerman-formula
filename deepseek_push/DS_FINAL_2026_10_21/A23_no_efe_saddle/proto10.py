import math, time
import numpy as np
import core as K

DEEP = lambda x: np.maximum(x, 1e-14)
PHIF = lambda r: math.sqrt(2.0) * np.log(r)
H = [0.004, 0.002, 0.001, 0.0005]
t0 = time.time()
print("h        N      QUMOND S      C02      AQUAL S      C02     itA")
lq, la = [], []
for h in H:
    Rf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
    zf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
    g = K.Grid(Rf, zf); m = K.plummer(g, K.BFAC, 1.0, (0.5,))
    Cq, _, _, resq = K.qumond(g, m, 0.0)
    Sq, rowq = K.column_S(g, Cq)
    Ph, pR, pZ, resa, ita, d = K.solve_aqual(g, m, DEEP, PHIF, alpha=0.6, itmax=400, tol=1e-9)
    Ca = K.laplacian(g, Ph, pR, pZ) / (4 * math.pi) - m / g.V
    Sa, rowa = K.column_S(g, Ca)
    lq.append(Sq); la.append(Sa)
    print(f"{h:<8.4f} {g.N:6d} {Sq:+.6f} {np.interp(0.2,g.Rc,rowq):+.4f}  {Sa:+.6f} {np.interp(0.2,g.Rc,rowa):+.4f}  {ita}")
    if h == H[-1]:
        np.save("Cq_fine.npy", Cq); np.save("Ca_fine.npy", Ca)
        np.save("Rc_fine.npy", g.Rc); np.save("zc_fine.npy", g.zc); np.save("Rf_fine.npy", g.Rf)
for tag, vals in (("QUMOND", lq), ("AQUAL", la)):
    Sinf, p, ratios, inc = K.richardson(vals, H)
    print(f"{tag}: S_inf={Sinf:+.6f} p={p:.2f} ratios={['%.3f'%r for r in ratios]} inc={['%+.5f'%i for i in inc]}")
print("t", time.time() - t0)
