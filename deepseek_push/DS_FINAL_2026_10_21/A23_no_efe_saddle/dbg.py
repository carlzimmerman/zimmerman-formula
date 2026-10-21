import math
import numpy as np
src = open("a23_checks.py").read()
marker = "# --------------------------------------------------------------------------- S2 solver controls"
exec(src[:src.index(marker)], globals())
h = 0.001
Rf = make_faces(6.0, [(0.0, h)]); zf = make_faces(6.0, [(0.0, h)])
gc = Grid(Rf, zf); mc = plummer(gc, BFAC, 0.5, (0.0,))
Phc, pRc, pZc, resc, itc = solve_aqual(gc, mc, DEEP, lambda rr: np.log(rr))
Ca = laplacian(gc, Phc, pRc, pZc) / (4 * math.pi) - mc / gc.V
Cq, PP, resq = qumond(gc, mc, 0.0)
rc = np.hypot(gc.RR, gc.ZZ)
for r in (0.3, 0.4, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0):
    j = np.argmin(abs(gc.Rc - r)); i = 0
    print(f"r={r}: AQUAL C*4pi r^2={Ca[i,j]*4*math.pi*gc.Rc[i]**2:.4f}  QUMOND={Cq[i,j]*4*math.pi*gc.Rc[i]**2:.4f}  h={gc.Rc[i+1]-gc.Rc[i]:.4f}")
print("qumond res", resq)
