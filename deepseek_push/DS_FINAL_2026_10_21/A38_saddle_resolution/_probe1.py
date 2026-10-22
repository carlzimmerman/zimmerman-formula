import numpy as np, math
import _s3 as S

mu = lambda v: np.maximum(v, 1e-30)
Zmax = 2.0
n = 240
R = np.linspace(0, Zmax, n)
z = np.linspace(-Zmax, Zmax, 2 * n - 1)
g = S.Grid(R, z)
rho = S.gauss2(g, 0.05, zc=0.0, mass=1.0)
phif = lambda r: np.log(np.maximum(r, 1e-9))
Phi, it, dl = S.solve(g, rho, mu, phif, itmax=60, tol=1e-11, zmin_dirichlet=True)
C = S.rho_ph(g, Phi, mu)
j = n - 1
idx = np.searchsorted(R, [0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6])
print("it", it)
for i in idx:
    print("R=%.2f  4pi r^2 rho = %8.4f   C=%+.4e   analytic=%+.4e"
          % (R[i], C[i, j] * 4 * math.pi * R[i] ** 2, C[i, j], 1 / (4 * math.pi * R[i] ** 2)))
