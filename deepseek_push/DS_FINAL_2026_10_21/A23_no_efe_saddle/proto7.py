import math, time
import numpy as np
import core as K
import scipy.sparse as sps, scipy.sparse.linalg as spla

DEEP = lambda x: np.maximum(x, 1e-14)
FULLMU = lambda x: x / (1.0 + x)


def aqual_tot(g, m, e, Meff, mufun, alpha=0.6, itmax=800, tol=1e-7, Phi0=None):
    """AQUAL for the TOTAL potential: lap-term = 4 pi rho_b, BC phi=-Meff/r + e z (e>0)."""
    Rb = np.hypot(g.Rf[-1], g.zc); Zb = np.hypot(g.Rc, g.zf[-1])
    def far(R, Z):
        r = np.hypot(R, Z)
        return -Meff / r + e * Z
    pbR, pbZ = far(g.Rf[-1], g.zc), far(g.Rc, g.zf[-1])
    rhs = 4 * math.pi * m.ravel()
    if Phi0 is None:
        rr = np.hypot(g.RR, g.ZZ)
        Phi = -Meff / (rr + 1e-3) + e * g.ZZ
    else:
        Phi = Phi0.copy()
    mu = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
    it = 0
    for it in range(itmax):
        A, b = K.assemble(g, *mu, pbR, pbZ)
        Pn = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        if alpha != 1.0:
            Pn = Phi + alpha * (Pn - Phi)
        d = np.max(np.abs(Pn - Phi)) / (np.max(Pn) - np.min(Pn))
        Phi = Pn
        mu_new = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
        mu = tuple(np.sqrt(a * b) for a, b in zip(mu, mu_new))
        if d < tol and it > 3:
            break
    mu = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
    A, b = K.assemble(g, *mu, pbR, pbZ)
    res = np.max(np.abs(A @ Phi.ravel() - b - rhs)) / np.max(np.abs(rhs))
    C = K.laplacian(g, Phi, pbR, pbZ) / (4 * math.pi) - m / g.V
    return C, Phi, res, it + 1


def qumond_tot(g, m, e, Meff):
    """QUMOND with a Newtonian far field of total mass Meff (e>0)."""
    one = lambda x: np.ones_like(x); zero = np.zeros((g.NR, g.NZ))
    Rb = np.hypot(g.Rf[-1], g.zc); Zb = np.hypot(g.Rc, g.zf[-1])
    pNbR, pNbZ = -2.0 / Rb, -2.0 / Zb
    A, b = K.assemble(g, *K.coeffs(g, zero, pNbR, pNbZ, one, 0.0), pNbR, pNbZ)
    PhiN = spla.spsolve(A.tocsc(), 4 * math.pi * m.ravel() + b).reshape(g.NR, g.NZ)
    (nR, tR, nRo, tRo), (nz, tz, nzo, tzo) = K.face_grads(g, PhiN, pNbR, pNbZ, e)
    vR = K.nu_simple(np.hypot(nR, tR)); vz = K.nu_simple(np.hypot(nz, tz))
    Sflux = K.divflux(g, (vR - 1.0) * nR, (vz - 1.0) * nz)
    ppbR, ppbZ = -(Meff - 2.0) / Rb, -(Meff - 2.0) / Zb
    A2, b2 = K.assemble(g, *K.coeffs(g, zero, ppbR, ppbZ, one, 0.0), ppbR, ppbZ)
    rhs = 4 * math.pi * m.ravel() + Sflux.ravel()
    Phiph = spla.spsolve(A2.tocsc(), rhs + b2).reshape(g.NR, g.NZ)
    res = np.max(np.abs(A2 @ Phiph.ravel() - b2 - rhs)) / np.max(np.abs(rhs))
    C = K.laplacian(g, Phiph, ppbR, ppbZ) / (4 * math.pi)
    return C, res


h = 0.006
Rf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
zff = K.make_faces_sym(K.XMAX, [(0.0, h), (0.5, h)])
gf = K.Grid(Rf, zff); mf = K.plummer(gf, K.BFAC, 2.0, (0.5, -0.5))
print("N", gf.N)
t0 = time.time()
for e in (0.0, 0.3, 1.0, 3.0):
    if e == 0.0:
        Rb = np.hypot(gf.Rf[-1], gf.zc); Zb = np.hypot(gf.Rc, gf.zf[-1])
        # deep-MOND BC by using aqual_tot with Meff -> use separate call
        # emulate: phi = sqrt2 log r
        import types
        # simple: call a variant
        def far(r): return math.sqrt(2.0) * np.log(r)
        # inline solve with phi_far
        one = lambda x: np.ones_like(x); zero = np.zeros((gf.NR, gf.NZ))
        pbR, pbZ = far(Rb), far(Zb)
        rhs = 4 * math.pi * mf.ravel()
        Phi = far(np.hypot(gf.RR, gf.ZZ) + 1e-3)
        mu = K.coeffs(gf, Phi, pbR, pbZ, DEEP, 0.0)
        for it in range(800):
            A, b = K.assemble(gf, *mu, pbR, pbZ)
            Pn = spla.spsolve(A.tocsc(), rhs + b).reshape(gf.NR, gf.NZ)
            Pn = Phi + 0.6 * (Pn - Phi)
            d = np.max(np.abs(Pn - Phi)) / (np.max(Pn) - np.min(Pn)); Phi = Pn
            mu_new = K.coeffs(gf, Phi, pbR, pbZ, DEEP, 0.0)
            mu = tuple(np.sqrt(a * b) for a, b in zip(mu, mu_new))
            if d < 1e-7 and it > 3: break
        C = K.laplacian(gf, Phi, pbR, pbZ) / (4 * math.pi) - mf / gf.V
        S, row = K.column_S(gf, C)
        Mph = float(np.sum(C * gf.V))
        print(f"AQUAL e=0 S={S:+.5f} C02={np.interp(0.2,gf.Rc,row):+.4f} Mph={Mph:.2f} it={it} t={time.time()-t0:.1f}")
        continue
    Meff = 2.0
    for k in range(3):
        C, Phi, res, it = aqual_tot(gf, mf, e, Meff, DEEP, Phi0=None if k == 0 else Phi)
        Mph = float(np.sum(C * gf.V))
        print(f"  e={e} pass{k}: Meff={Meff:.2f} -> Mph={Mph:.2f} res={res:.1e} it={it}")
        Meff_new = 2.0 + Mph
        if abs(Meff_new - Meff) < 0.05: break
        Meff = Meff_new
    S, row = K.column_S(gf, C)
    print(f"AQUAL e={e} S={S:+.5f} C02={np.interp(0.2,gf.Rc,row):+.4f} Meff={Meff:.2f} t={time.time()-t0:.1f}")
print("=== QUMOND ===")
for e in (0.0, 0.3, 1.0, 3.0):
    if e == 0.0:
        C, res = K.qumond(gf, mf, 0.0)
        S, row = K.column_S(gf, C); Mph = float(np.sum(C * gf.V))
        print(f"QUMOND e=0 S={S:+.5f} C02={np.interp(0.2,gf.Rc,row):+.4f} Mph={Mph:.2f}")
        continue
    Meff = 2.0
    for k in range(3):
        C, res = qumond_tot(gf, mf, e, Meff)
        Mph = float(np.sum(C * gf.V))
        Meff_new = 2.0 + Mph
        print(f"  e={e} pass{k}: Meff={Meff:.2f} -> Mph={Mph:.2f}")
        if abs(Meff_new - Meff) < 0.05: break
        Meff = Meff_new
    S, row = K.column_S(gf, C)
    print(f"QUMOND e={e} S={S:+.5f} C02={np.interp(0.2,gf.Rc,row):+.4f} Meff={Meff:.2f} t={time.time()-t0:.1f}")
