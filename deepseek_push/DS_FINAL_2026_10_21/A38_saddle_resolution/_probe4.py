import numpy as np, math
import _s3 as S

mu = lambda v: np.maximum(v, 1e-30)
Zmax, n = 8.0, 480
R = np.linspace(0, Zmax, n)
z = np.linspace(0, Zmax, n)
g = S.Grid(R, z)
rho = S.gauss2(g, 0.08, zc=0.5, mass=1.0)
phif = lambda r: math.sqrt(2.0) * np.log(np.maximum(r, 1e-9))
Phi, it, dl = S.solve(g, rho, mu, phif, itmax=200, tol=1e-12)
C = S.rho_ph(g, Phi, mu)
row = C[:, 0]
for r in [0.5, 1, 2, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 7.95]:
    print("R=%5.2f  C=%+.5f" % (r, np.interp(r, R, row)))
print("cumulative S(R):")
for L in [1, 2, 3, 4, 5, 6, 7, 8]:
    m = R <= L
    print("  S(<%d) = %+.5f" % (L, 2 * np.trapz(np.minimum(row[m], 0.0), R[m])))
