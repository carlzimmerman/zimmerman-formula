import math, time
import numpy as np
import core as K
import scipy.sparse as sps, scipy.sparse.linalg as spla

DEEP = lambda x: np.maximum(x, 1e-14)


def aqual(g, m, e, phif, mufun=DEEP, alpha=0.6, itmax=600, tol=1e-8, Phi0=None):
    Rb = np.hypot(g.Rf[-1], g.zc); Zb = np.hypot(g.Rc, g.zf[-1])
    pbR, pbZ = phif(g.Rf[-1], g.zc), phif(g.Rc, g.zf[-1])
    rhs = 4 * math.pi * m.ravel()
    Phi = phif(g.RR, g.ZZ) if Phi0 is None else Phi0.copy()
    mu = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
    it = 0
    for it in range(itmax):
        A, b = K.assemble(g, *mu, pbR, pbZ)
        Pn = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        if alpha != 1.0: Pn = Phi + alpha * (Pn - Phi)
        d = np.max(np.abs(Pn - Phi)) / (np.max(Pn) - np.min(Pn)); Phi = Pn
        mu_new = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
        mu = tuple(np.sqrt(a * b) for a, b in zip(mu, mu_new))
        if d < tol and it > 3: break
    mu = K.coeffs(g, Phi, pbR, pbZ, mufun, 0.0)
    A, b = K.assemble(g, *mu, pbR, pbZ)
    res = np.max(np.abs(A @ Phi.ravel() - b - rhs)) / np.max(np.abs(rhs))
    C = K.laplacian(g, Phi, pbR, pbZ) / (4 * math.pi) - m / g.V
    return C, Phi, res, it + 1


def qumond(g, m, e, bc_mode="asym"):
    one = lambda x: np.ones_like(x); zero = np.zeros((g.NR, g.NZ))
    Rb = np.hypot(g.Rf[-1], g.zc); Zb = np.hypot(g.Rc, g.zf[-1])
    pNbR, pNbZ = -2.0 / Rb, -2.0 / Zb
    A, b = K.assemble(g, *K.coeffs(g, zero, pNbR, pNbZ, one, 0.0), pNbR, pNbZ)
    PhiN = spla.spsolve(A.tocsc(), 4 * math.pi * m.ravel() + b).reshape(g.NR, g.NZ)
    (nR, tR, nRo, tRo), (nz, tz, nzo, tzo) = K.face_grads(g, PhiN, pNbR, pNbZ, e)
    vR = K.nu_simple(np.hypot(nR, tR)); vz = K.nu_simple(np.hypot(nz, tz))
    Sflux = K.divflux(g, (vR - 1.0) * nR, (vz - 1.0) * nz)
    if e == 0.0:
        ppbR, ppbZ = math.sqrt(2.0) * np.log(Rb) + 2.0 / Rb, math.sqrt(2.0) * np.log(Zb) + 2.0 / Zb
    elif bc_mode == "zero":
        ppbR, ppbZ = np.zeros_like(Rb), np.zeros_like(Zb)
    else:
        c = (K.nu_simple(np.array([e]))[0] - 1.0)
        ppbR, ppbZ = -c * 2.0 / Rb, -c * 2.0 / Zb
    A2, b2 = K.assemble(g, *K.coeffs(g, zero, ppbR, ppbZ, one, 0.0), ppbR, ppbZ)
    rhs = 4 * math.pi * m.ravel() + Sflux.ravel()
    Phiph = spla.spsolve(A2.tocsc(), rhs + b2).reshape(g.NR, g.NZ)
    C = K.laplacian(g, Phiph, ppbR, ppbZ) / (4 * math.pi)
    return C, Phiph


t0 = time.time()
print("=== QUMOND full: BC sensitivity ===")
h = 0.006
Rf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
zff = K.make_faces_sym(K.XMAX, [(0.0, h), (0.5, h)])
gf = K.Grid(Rf, zff); mf = K.plummer(gf, K.BFAC, 2.0, (0.5, -0.5))
for e in (0.3, 1.0, 3.0):
    for bc in ("zero", "asym"):
        C, _ = qumond(gf, mf, e, bc)
        S, row = K.column_S(gf, C)
        print(f" e={e} bc={bc:5s} S={S:+.6f} C02={np.interp(0.2,gf.Rc,row):+.4f}")
C0, _ = qumond(gf, mf, 0.0)
S0, row0 = K.column_S(gf, C0)
print(f" e=0 S={S0:+.6f} C02={np.interp(0.2,gf.Rc,row0):+.4f}")
print("profile e=0:", [(round(x,3),round(float(np.interp(x,gf.Rc,row0)),4)) for x in (0.01,0.02,0.05,0.1,0.2,0.3,0.5,1.0,1.5)])
for e in (0.3,1.0,3.0):
    C,_=qumond(gf,mf,e,"asym"); S,row=K.column_S(gf,C)
    print(f"profile e={e}:", [(round(x,3),round(float(np.interp(x,gf.Rc,row)),4)) for x in (0.01,0.02,0.05,0.1,0.2,0.3,0.5,1.0)])
print("t",time.time()-t0)
print("=== AQUAL full: box sensitivity at e=0.3 ===")
for XM in (6.0, 8.0):
    K.XMAX = XM
    Rf = K.make_faces(XM, [(0.0, h), (0.5, h)])
    zff = K.make_faces_sym(XM, [(0.0, h), (0.5, h)])
    g = K.Grid(Rf, zff); m = K.plummer(g, K.BFAC, 2.0, (0.5, -0.5))
    phif = lambda R, Z: -2.0 / np.hypot(R, Z) + 0.3 * Z
    C, Phi, res, it = aqual(g, m, 0.3, phif)
    S, row = K.column_S(g, C)
    print(f" XMAX={XM} N={g.N} e=0.3 S={S:+.6f} C02={np.interp(0.2,g.Rc,row):+.4f} it={it} res={res:.1e}")
K.XMAX = 6.0
print("=== AQUAL half (A13 config) vs full at e=0.3 ===")
Rf = K.make_faces(6.0, [(0.0, h), (0.5, h)])
zfh = K.make_faces(6.0, [(0.0, h), (0.5, h)])
gh = K.Grid(Rf, zfh); mh = K.plummer(gh, K.BFAC, 1.0, (0.5,))
phif0 = lambda R, Z: math.sqrt(2.0) * np.log(np.hypot(R, Z))
C, Phi, res, it = aqual(gh, mh, 0.0, phif0)
S0h, row0h = K.column_S(gh, C)
print(f" half e=0 S={S0h:+.6f} C02={np.interp(0.2,gh.Rc,row0h):+.4f}")
# half with e: A13's Psi=Phi+ez convention -> mu argument is grad(Psi)-e zhat; BC Psi=sqrt2 log r
def aqual_half_e(g, m, e, alpha=0.6, itmax=600, tol=1e-8):
    Rb = np.hypot(g.Rf[-1], g.zc); Zb = np.hypot(g.Rc, g.zf[-1])
    phif = lambda r: math.sqrt(2.0) * np.log(r)
    pbR, pbZ = phif(Rb), phif(Zb)
    rhs = 4 * math.pi * m.ravel()
    Phi = phif(np.hypot(g.RR, g.ZZ) + 1e-3)
    mu = K.coeffs(g, Phi, pbR, pbZ, DEEP, e)
    for it in range(itmax):
        A, b = K.assemble(g, *mu, pbR, pbZ)
        Pn = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        Pn = Phi + alpha * (Pn - Phi)
        d = np.max(np.abs(Pn - Phi)) / (np.max(Pn) - np.min(Pn)); Phi = Pn
        mu_new = K.coeffs(g, Phi, pbR, pbZ, DEEP, e)
        mu = tuple(np.sqrt(a * b) for a, b in zip(mu, mu_new))
        if d < tol and it > 3: break
    mu = K.coeffs(g, Phi, pbR, pbZ, DEEP, e)
    A, b = K.assemble(g, *mu, pbR, pbZ)
    res = np.max(np.abs(A @ Phi.ravel() - b - rhs)) / np.max(np.abs(rhs))
    C = K.laplacian(g, Phi, pbR, pbZ) / (4 * math.pi) - m / g.V
    return C, res, it + 1
for e in (0.3, 1.0):
    C, res, it = aqual_half_e(gh, mh, e)
    S, row = K.column_S(gh, C)
    print(f" half e={e} S={S:+.6f} ratio={S/S0h:.3f} C02={np.interp(0.2,gh.Rc,row):+.4f} it={it} res={res:.1e}")
print("t",time.time()-t0)
