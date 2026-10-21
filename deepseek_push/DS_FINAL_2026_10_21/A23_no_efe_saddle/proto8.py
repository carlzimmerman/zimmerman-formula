import math, time
import numpy as np
import core as K
import scipy.sparse as sps, scipy.sparse.linalg as spla

DEEP = lambda x: np.maximum(x, 1e-14)
FULLMU = lambda x: x / (1.0 + x)


def aqual(g, m, e, mufun=DEEP, phif=None, alpha=0.6, itmax=600, tol=1e-8, Phi0=None):
    """AQUAL for the total potential with grad(Phi) the true total field (e in the BC)."""
    Rb = np.hypot(g.Rf[-1], g.zc); Zb = np.hypot(g.Rc, g.zf[-1])
    if phif is None:
        if e == 0.0:
            phif = lambda R, Z: math.sqrt(2.0) * np.log(np.hypot(R, Z))
        else:
            phif = lambda R, Z: -2.0 / np.hypot(R, Z) + e * Z
    pbR, pbZ = phif(g.Rf[-1], g.zc), phif(g.Rc, g.zf[-1])
    rhs = 4 * math.pi * m.ravel()
    if Phi0 is None:
        Phi = phif(g.RR, g.ZZ)
    else:
        Phi = Phi0.copy()
    mu = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
    it = 0
    for it in range(itmax):
        A, b = K.assemble(g, *mu, pbR, pbZ)
        Pn = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        if alpha != 1.0:
            Pn = Phi + alpha * (Pn - Phi)
        d = np.max(np.abs(Pn - Phi)) / (np.max(Pn) - np.min(Pn)); Phi = Pn
        mu_new = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
        mu = tuple(np.sqrt(a * b) for a, b in zip(mu, mu_new))
        if d < tol and it > 3: break
    mu = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
    A, b = K.assemble(g, *mu, pbR, pbZ)
    res = np.max(np.abs(A @ Phi.ravel() - b - rhs)) / np.max(np.abs(rhs))
    C = K.laplacian(g, Phi, pbR, pbZ) / (4 * math.pi) - m / g.V
    return C, Phi, res, it + 1


def qumond(g, m, e, phif_ph=None):
    one = lambda x: np.ones_like(x); zero = np.zeros((g.NR, g.NZ))
    Rb = np.hypot(g.Rf[-1], g.zc); Zb = np.hypot(g.Rc, g.zf[-1])
    pNbR, pNbZ = -2.0 / Rb, -2.0 / Zb
    A, b = K.assemble(g, *K.coeffs(g, zero, pNbR, pNbZ, one, 0.0), pNbR, pNbZ)
    PhiN = spla.spsolve(A.tocsc(), 4 * math.pi * m.ravel() + b).reshape(g.NR, g.NZ)
    (nR, tR, nRo, tRo), (nz, tz, nzo, tzo) = K.face_grads(g, PhiN, pNbR, pNbZ, e)
    vR = K.nu_simple(np.hypot(nR, tR)); vz = K.nu_simple(np.hypot(nz, tz))
    Sflux = K.divflux(g, (vR - 1.0) * nR, (vz - 1.0) * nz)
    if phif_ph is None:
        if e == 0.0:
            ppbR, ppbZ = math.sqrt(2.0) * np.log(Rb) + 2.0 / Rb, math.sqrt(2.0) * np.log(Zb) + 2.0 / Zb
        else:
            ppbR, ppbZ = np.zeros_like(Rb), np.zeros_like(Zb)
    else:
        ppbR, ppbZ = phif_ph(Rb), phif_ph(Zb)
    A2, b2 = K.assemble(g, *K.coeffs(g, zero, ppbR, ppbZ, one, 0.0), ppbR, ppbZ)
    rhs = 4 * math.pi * m.ravel() + Sflux.ravel()
    Phiph = spla.spsolve(A2.tocsc(), rhs + b2).reshape(g.NR, g.NZ)
    res = np.max(np.abs(A2 @ Phiph.ravel() - b2 - rhs)) / np.max(np.abs(rhs))
    C = K.laplacian(g, Phiph, ppbR, ppbZ) / (4 * math.pi)
    return C, Phiph, res


h = 0.006
Rf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
zff = K.make_faces_sym(K.XMAX, [(0.0, h), (0.5, h)])
gf = K.Grid(Rf, zff); mf = K.plummer(gf, K.BFAC, 2.0, (0.5, -0.5))
print("N", gf.N)
t0 = time.time()
print("=== AQUAL (BC: deep-MOND at e=0, Newtonian M_b=2 at e>0) ===")
prev = None
for e in (0.0, 0.1, 0.3, 1.0, 3.0):
    C, Phi, res, it = aqual(gf, mf, e, DEEP, Phi0=prev)
    prev = Phi
    S, row = K.column_S(gf, C)
    Mph = float(np.sum(C * gf.V))
    print(f" e={e:4.2f} S={S:+.6f} C02={np.interp(0.2,gf.Rc,row):+.4f} Mph={Mph:+.3f} it={it:3d} res={res:.1e} t={time.time()-t0:.1f}")
print("=== AQUAL full mu ===")
prev = None
for e in (0.0, 1.0):
    C, Phi, res, it = aqual(gf, mf, e, FULLMU, Phi0=prev)
    prev = Phi
    S, row = K.column_S(gf, C)
    print(f" e={e:4.2f} S={S:+.6f} C02={np.interp(0.2,gf.Rc,row):+.4f} it={it:3d} res={res:.1e}")
print("=== QUMOND (BC: phi_ph->0 for e>0) ===")
for e in (0.0, 0.1, 0.3, 1.0, 3.0):
    C, Phiph, res = qumond(gf, mf, e)
    S, row = K.column_S(gf, C)
    Mph = float(np.sum(C * gf.V))
    print(f" e={e:4.2f} S={S:+.6f} C02={np.interp(0.2,gf.Rc,row):+.4f} Mph={Mph:+.3f} res={res:.1e} t={time.time()-t0:.1f}")
