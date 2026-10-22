import numpy as np, math, time, sys
import _s3 as S

mu = lambda v: np.maximum(v, 1e-30)
Zmax = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0
n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
sig = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05

R = np.linspace(0, Zmax, n)
z = np.linspace(0, Zmax, n)
g = S.Grid(R, z)
rho = S.gauss2(g, sig, zc=0.5, mass=1.0)
phif = lambda r: math.sqrt(2.0) * np.log(np.maximum(r, 1e-9))
t0 = time.time()
Phi, it, dl = S.solve(g, rho, mu, phif, itmax=200, tol=1e-12)
C = S.rho_ph(g, Phi, mu)
Sb, row = S.column(g, C, j=0)
head = "Zmax=%.1f n=%d h=%.4f sig=%.3f" % (Zmax, n, Zmax / n, sig)
print(head)
print("  it=%d  dPhi=%.2e  t=%.1fs" % (it, dl, time.time() - t0))
print("  S       = %+.5f   (A13 -0.22931)" % Sb)
print("  C(0.2d) = %+.4f  (A13 -0.24036)" % np.interp(0.2, R, row))
