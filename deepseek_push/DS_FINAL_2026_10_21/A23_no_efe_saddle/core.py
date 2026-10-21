"""Core numerics for A23: axisymmetric two-body saddle in the framework's law.

Units: G = M_lens = a0 = d = 1 for the field solve; the deep-MOND limit is
exact in the sense that the dimensionless equation is parameter-free.

Domain: R in [0, XMAX]; z either [0, XMAX] (half, mirror symmetry at z=0,
used for e=0) or [-XMAX, XMAX] (full, required when an external field along
the pair axis breaks the mirror).
"""
import math
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla

XMAX = 6.0
RATE = 0.05
BFAC = 0.01


def make_faces(xmax, refs):
    xs = [0.0]
    while xs[-1] < xmax:
        x = xs[-1]
        h = min(hk + RATE * abs(x - ck) for ck, hk in refs)
        xs.append(min(x + h, xmax))
    return np.array(xs)


def make_faces_sym(xmax, refs):
    xp = make_faces(xmax, refs)
    return np.concatenate([-xp[::-1][:-1], xp])


class Grid:
    def __init__(self, Rf, zf):
        self.Rf, self.zf = Rf, zf
        self.Rc = 0.5 * (Rf[1:] + Rf[:-1])
        self.zc = 0.5 * (zf[1:] + zf[:-1])
        self.NR, self.NZ = len(self.Rc), len(self.zc)
        self.N = self.NR * self.NZ
        self.RR, self.ZZ = np.meshgrid(self.Rc, self.zc, indexing="ij")
        self.V = np.outer(np.pi * (Rf[1:] ** 2 - Rf[:-1] ** 2), np.diff(zf))
        self.idx = np.arange(self.N).reshape(self.NR, self.NZ)


def plummer(g, b, mtot=1.0, centres=(0.5,)):
    rho = np.zeros((g.NR, g.NZ))
    for zp in centres:
        r2 = g.RR ** 2 + (g.ZZ - zp) ** 2
        rho += (3 / (4 * math.pi * b ** 3)) * (1 + r2 / b ** 2) ** (-2.5)
    m = rho * g.V
    return m * (mtot / m.sum())


def coeffs(g, Phi, pbR, pbZ, mufun, e=0.0):
    """mu (or nu) on faces.  Phi is Psi = Phi_total + e*z, so grad(Phi_tot)=grad(Psi)-e zhat."""
    dR = np.zeros_like(Phi)
    dZ = np.zeros_like(Phi)
    dR[1:-1, :] = (Phi[2:, :] - Phi[:-2, :]) / (g.Rc[2:, None] - g.Rc[:-2, None])
    dR[0, :] = (Phi[1, :] - Phi[0, :]) / (g.Rc[1] + g.Rc[0])
    dR[-1, :] = (pbR - Phi[-2, :]) / (g.Rf[-1] - g.Rc[-2])
    dZ[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) / (g.zc[None, 2:] - g.zc[None, :-2])
    dZ[:, 0] = (Phi[:, 1] - Phi[:, 0]) / (g.zc[1] + g.zc[0])
    dZ[:, -1] = (pbZ - Phi[:, -2]) / (g.zf[-1] - g.zc[-2])
    nR = (Phi[1:, :] - Phi[:-1, :]) / (g.Rc[1:, None] - g.Rc[:-1, None])
    tR = 0.5 * (dZ[1:, :] + dZ[:-1, :]) - e
    muR = mufun(np.hypot(nR, tR))
    nRo = (pbR - Phi[-1, :]) / (g.Rf[-1] - g.Rc[-1])
    muRo = mufun(np.hypot(nRo, dZ[-1, :] - e))
    nz = (Phi[:, 1:] - Phi[:, :-1]) / (g.zc[None, 1:] - g.zc[None, :-1]) - e
    tz = 0.5 * (dR[:, 1:] + dR[:, :-1])
    muz = mufun(np.hypot(nz, tz))
    nzo = (pbZ - Phi[:, -1]) / (g.zf[-1] - g.zc[-1]) - e
    muzo = mufun(np.hypot(nzo, dR[:, -1]))
    return muR, muRo, muz, muzo


def assemble(g, muR, muRo, muz, muzo, pbR, pbZ):
    I = g.idx
    b = np.zeros(g.N)
    diag = np.zeros(g.N)
    rows, cols, vals = [], [], []
    AR = 2 * math.pi * g.Rf[1:-1, None] * np.diff(g.zf)[None, :]
    cR = (muR * AR / (g.Rc[1:, None] - g.Rc[:-1, None])).ravel()
    a, bb = I[:-1, :].ravel(), I[1:, :].ravel()
    rows += [a, bb]
    cols += [bb, a]
    vals += [cR, cR]
    np.add.at(diag, a, -cR)
    np.add.at(diag, bb, -cR)
    ARo = 2 * math.pi * g.Rf[-1] * np.diff(g.zf)
    cRo = (muRo * ARo / (g.Rf[-1] - g.Rc[-1])).ravel()
    ii = I[-1, :].ravel()
    np.add.at(diag, ii, -cRo)
    b[ii] -= cRo * pbR
    Az = np.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)[:, None] * np.ones((1, g.NZ - 1))
    cz = (muz * Az / (g.zc[None, 1:] - g.zc[None, :-1])).ravel()
    a, bb = I[:, :-1].ravel(), I[:, 1:].ravel()
    rows += [a, bb]
    cols += [bb, a]
    vals += [cz, cz]
    np.add.at(diag, a, -cz)
    np.add.at(diag, bb, -cz)
    Azo = np.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)
    czo = (muzo * Azo / (g.zf[-1] - g.zc[-1])).ravel()
    ii = I[:, -1].ravel()
    np.add.at(diag, ii, -czo)
    b[ii] -= czo * pbZ
    rows.append(np.arange(g.N))
    cols.append(np.arange(g.N))
    vals.append(diag)
    A = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                       shape=(g.N, g.N))
    return A, b


def solve_aqual(g, m, mufun, phif, e=0.0, alpha=1.0, itmax=500, tol=1e-10, Phi0=None):
    Rb = np.hypot(g.Rf[-1], g.zc)
    Zb = np.hypot(g.Rc, g.zf[-1])
    pbR, pbZ = phif(Rb), phif(Zb)
    rhs = 4 * math.pi * m.ravel()
    Phi = phif(np.hypot(g.RR, g.ZZ) + 1e-3) if Phi0 is None else Phi0.copy()
    mu = coeffs(g, Phi, pbR, pbZ, mufun, e)
    it = 0
    for it in range(itmax):
        A, b = assemble(g, *mu, pbR, pbZ)
        Pn = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        if alpha != 1.0:
            Pn = Phi + alpha * (Pn - Phi)
        d = np.max(np.abs(Pn - Phi)) / (np.max(Pn) - np.min(Pn))
        Phi = Pn
        mu_new = coeffs(g, Phi, pbR, pbZ, mufun, e)
        mu = tuple(np.sqrt(a * b) for a, b in zip(mu, mu_new))
        if d < tol and it > 3:
            break
    mu = coeffs(g, Phi, pbR, pbZ, mufun, e)
    A, b = assemble(g, *mu, pbR, pbZ)
    res = np.max(np.abs(A @ Phi.ravel() - b - rhs)) / np.max(np.abs(rhs))
    return Phi, pbR, pbZ, res, it + 1, d


def laplacian(g, Phi, pbR, pbZ):
    one = lambda x: np.ones_like(x)
    mu = coeffs(g, Phi, pbR, pbZ, one, 0.0)
    A, b = assemble(g, *mu, pbR, pbZ)
    return (A @ Phi.ravel() - b).reshape(g.NR, g.NZ) / g.V


def face_grads(g, Phi, pbR, pbZ, e=0.0):
    dR = np.zeros_like(Phi)
    dZ = np.zeros_like(Phi)
    dR[1:-1, :] = (Phi[2:, :] - Phi[:-2, :]) / (g.Rc[2:, None] - g.Rc[:-2, None])
    dR[0, :] = (Phi[1, :] - Phi[0, :]) / (g.Rc[1] + g.Rc[0])
    dR[-1, :] = (pbR - Phi[-2, :]) / (g.Rf[-1] - g.Rc[-2])
    dZ[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) / (g.zc[None, 2:] - g.zc[None, :-2])
    dZ[:, 0] = (Phi[:, 1] - Phi[:, 0]) / (g.zc[1] + g.zc[0])
    dZ[:, -1] = (pbZ - Phi[:, -2]) / (g.zf[-1] - g.zc[-2])
    nR = (Phi[1:, :] - Phi[:-1, :]) / (g.Rc[1:, None] - g.Rc[:-1, None])
    tR = 0.5 * (dZ[1:, :] + dZ[:-1, :]) - e
    nz = (Phi[:, 1:] - Phi[:, :-1]) / (g.zc[None, 1:] - g.zc[None, :-1]) - e
    tz = 0.5 * (dR[:, 1:] + dR[:, :-1])
    nRo = (pbR - Phi[-1, :]) / (g.Rf[-1] - g.Rc[-1])
    tRo = dZ[-1, :] - e
    nzo = (pbZ - Phi[:, -1]) / (g.zf[-1] - g.zc[-1]) - e
    tzo = dR[:, -1]
    return (nR, tR, nRo, tRo), (nz, tz, nzo, tzo)


def divflux(g, fR, fz):
    out = np.zeros((g.NR, g.NZ))
    AR = 2 * math.pi * g.Rf[1:-1, None] * np.diff(g.zf)[None, :]
    out[:-1, :] += fR * AR
    out[1:, :] -= fR * AR
    Az = np.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)[:, None] * np.ones((1, g.NZ - 1))
    out[:, :-1] += fz * Az
    out[:, 1:] -= fz * Az
    return out


def nu_simple(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-30))


def qumond(g, m, e=0.0, include_ext=True, nu=nu_simple, phif=None):
    """QUMOND-type law: lap(phi) = div( nu(|grad phi_N,tot|) grad phi_N,tot ).

    include_ext=False is the framework's own-source rule (A5): nu is evaluated on
    the system's own baryonic field only, so e never enters.
    """
    if phif is None:
        phif = lambda r: math.sqrt(2.0) * np.log(r)
    one = lambda x: np.ones_like(x)
    zero = np.zeros((g.NR, g.NZ))
    Rb = np.hypot(g.Rf[-1], g.zc)
    Zb = np.hypot(g.Rc, g.zf[-1])
    pNbR, pNbZ = -2.0 / Rb, -2.0 / Zb
    A, b = assemble(g, *coeffs(g, zero, pNbR, pNbZ, one, 0.0), pNbR, pNbZ)
    PhiN = spla.spsolve(A.tocsc(), 4 * math.pi * m.ravel() + b).reshape(g.NR, g.NZ)
    ee = e if include_ext else 0.0
    (nR, tR, nRo, tRo), (nz, tz, nzo, tzo) = face_grads(g, PhiN, pNbR, pNbZ, ee)
    vR = nu(np.hypot(nR, tR))
    vz = nu(np.hypot(nz, tz))
    Sflux = divflux(g, (vR - 1.0) * nR, (vz - 1.0) * nz)
    ph = lambda r: phif(r) + 2.0 / r
    ppbR, ppbZ = ph(Rb), ph(Zb)
    A2, b2 = assemble(g, *coeffs(g, zero, ppbR, ppbZ, one, 0.0), ppbR, ppbZ)
    rhs = 4 * math.pi * m.ravel() + Sflux.ravel()
    Phiph = spla.spsolve(A2.tocsc(), rhs + b2).reshape(g.NR, g.NZ)
    res = np.max(np.abs(A2 @ Phiph.ravel() - b2 - rhs)) / np.max(np.abs(rhs))
    C = laplacian(g, Phiph, ppbR, ppbZ) / (4 * math.pi)
    return C, PhiN, Phiph, res


def midplane(g, C):
    """C on the midplane z=0, interpolated between the two adjacent cells."""
    j = int(np.searchsorted(g.zc, 0.0))
    if j <= 0:
        return C[:, 0]
    if j >= g.NZ:
        return C[:, -1]
    t = (0.0 - g.zc[j - 1]) / (g.zc[j] - g.zc[j - 1])
    return (1 - t) * C[:, j - 1] + t * C[:, j]


def column_S(g, C):
    row = midplane(g, C)
    return float(2 * np.sum(np.minimum(row, 0.0) * np.diff(g.Rf))), row


def richardson(S_vals, h_vals):
    """S(h) = S_inf + a h^p; p from the last two increments."""
    inc = [S_vals[i + 1] - S_vals[i] for i in range(len(S_vals) - 1)]
    ratios = [inc[i + 1] / inc[i] if abs(inc[i]) > 1e-15 else 0.5 for i in range(len(inc) - 1)]
    r = ratios[-1]
    if not np.isfinite(r) or r <= 0 or r >= 1:
        r = 0.5
    p = math.log2(1.0 / r)
    S_inf = S_vals[-1] + inc[-1] * r / (1.0 - r)
    return float(S_inf), float(p), ratios, inc
