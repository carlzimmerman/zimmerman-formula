import numpy as np, math, time
import _s3 as S

mu = lambda v: np.maximum(v, 1e-30)
out = {}
for (Zmax, n) in [(4.0, 240), (6.0, 360), (8.0, 480), (12.0, 480)]:
    R = np.linspace(0, Zmax, n)
    z = np.linspace(0, Zmax, n)
    g = S.Grid(R, z)
    rho = S.gauss2(g, 0.08, zc=0.5, mass=1.0)
    phif = lambda r: math.sqrt(2.0) * np.log(np.maximum(r, 1e-9))
    Phi, it, dl = S.solve(g, rho, mu, phif, itmax=200, tol=1e-12)
    C = S.rho_ph(g, Phi, mu)
    out[Zmax] = (R, C[:, 0])
    Sb, _ = S.column(g, C, j=0)
    m = R <= 3.0
    S3 = 2 * np.trapz(np.minimum(C[m, 0], 0.0), R[m])
    print("Zmax=%-5.1f n=%3d  S_tot=%+.5f  S(R<3)=%+.5f" % (Zmax, n, Sb, S3))

ref = np.linspace(0.02, 3.0, 40)
print("\n   R     " + "".join("   L=%-5.1f" % L for L in out))
for r in ref:
    print("%6.2f  " % r + "".join("  %+8.4f" % np.interp(r, v[0], v[1]) for v in out.values()))
