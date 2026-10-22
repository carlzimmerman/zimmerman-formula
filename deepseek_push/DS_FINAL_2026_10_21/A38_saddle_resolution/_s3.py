"""A38 solver 3 core: node-centred flux-form FD in (R,z), deep-mu AQUAL.
Equation (G=M_lens=d=1, a0 absorbed):   div( |grad Phi| grad Phi ) = 4 pi rho_b
Half domain z in [0,Zmax] (mirror symmetry at z=0, valid at zero external field).
"""
import math
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla


def graded(xmax, n, a=7.0):
    u = np.linspace(0.0, 1.0, n)
    return xmax * (np.exp(a * u) - 1.0) / (math.exp(a) - 1.0)


class Grid:
    def __init__(self, R, z):
        self.R, self.z = R, z
        self.NR, self.NZ = len(R), len(z)
        self.RR, self.ZZ = np.meshgrid(R, z, indexing="ij")
        dR = np.zeros(self.NR)
        dR[1:-1] = 0.5 * (R[2:] - R[:-2])
        dR[0] = 0.5 * (R[1] - R[0])
        dR[-1] = 0.5 * (R[-1] - R[-2])
        dz = np.zeros(self.NZ)
        dz[1:-1] = 0.5 * (z[2:] - z[:-2])
        dz[0] = 0.5 * (z[1] - z[0])
        dz[-1] = 0.5 * (z[-1] - z[-2])
        self.dR, self.dz = dR, dz
        self.vol = 2 * math.pi * R[:, None] * dR[:, None] * dz[None, :]
        self.Rf = 0.5 * (R[1:] + R[:-1])
        self.zf = 0.5 * (z[1:] + z[:-1])
        self.hR = np.diff(R)
        self.hz = np.diff(z)
        self.AR = 2 * math.pi * self.Rf[:, None] * dz[None, :]
        self.Az = 2 * math.pi * R[:, None] * dR[:, None] * np.ones((1, self.NZ - 1))
        self.idx = np.arange(self.NR * self.NZ).reshape(self.NR, self.NZ)
        self.invDz = np.zeros(self.NZ)
        self.invDz[1:-1] = 1.0 / (z[2:] - z[:-2])
        self.invDz[0] = 1.0 / (z[1] - z[0])
        self.invDz[-1] = 1.0 / (z[-1] - z[-2])
        self.invDR = np.zeros(self.NR)
        self.invDR[1:-1] = 1.0 / (R[2:] - R[:-2])
        self.invDR[0] = 1.0 / (R[1] - R[0])
        self.invDR[-1] = 1.0 / (R[-1] - R[-2])


def node_grads(g, Phi):
    dR = np.zeros_like(Phi)
    dZ = np.zeros_like(Phi)
    dR[1:-1, :] = (Phi[2:, :] - Phi[:-2, :]) * g.invDR[1:-1, None]
    dR[0, :] = (Phi[1, :] - Phi[0, :]) * g.invDR[0]
    dR[-1, :] = (Phi[-1, :] - Phi[-2, :]) * g.invDR[-1]
    dZ[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) * g.invDz[None, 1:-1]
    dZ[:, 0] = (Phi[:, 1] - Phi[:, 0]) * g.invDz[0]
    dZ[:, -1] = (Phi[:, -1] - Phi[:, -2]) * g.invDz[-1]
    return dR, dZ


def faces(g, Phi, e=0.0):
    dR, dZ = node_grads(g, Phi)
    nR = (Phi[1:, :] - Phi[:-1, :]) / g.hR[:, None]
    tR = 0.5 * (dZ[1:, :] + dZ[:-1, :]) - e
    nz = (Phi[:, 1:] - Phi[:, :-1]) / g.hz[None, :] - e
    tz = 0.5 * (dR[:, 1:] + dR[:, :-1])
    return (nR, tR), (nz, tz)


def residual(g, Phi, rho, mufun, e=0.0, with_mu=False):
    (nR, tR), (nz, tz) = faces(g, Phi, e)
    muR = mufun(np.hypot(nR, tR))
    muz = mufun(np.hypot(nz, tz))
    FR = g.AR * muR * nR
    Fz = g.Az * muz * nz
    R = np.zeros_like(Phi)
    R[:-1, :] += FR
    R[1:, :] -= FR
    R[:, :-1] += Fz
    R[:, 1:] -= Fz
    out = R - 4 * math.pi * rho * g.vol
    return (out, muR, muz) if with_mu else out


def assemble(g, muR, muz):
    NR, NZ = g.NR, g.NZ
    diag = np.zeros(NR * NZ)
    rows, cols, vals = [], [], []
    cR = (muR * g.AR / g.hR[:, None]).ravel()
    a, b = g.idx[:-1, :].ravel(), g.idx[1:, :].ravel()
    rows += [a, b]; cols += [b, a]; vals += [cR, cR]
    np.add.at(diag, a, -cR); np.add.at(diag, b, -cR)
    cz = (muz * g.Az / g.hz[None, :]).ravel()
    a, b = g.idx[:, :-1].ravel(), g.idx[:, 1:].ravel()
    rows += [a, b]; cols += [b, a]; vals += [cz, cz]
    np.add.at(diag, a, -cz); np.add.at(diag, b, -cz)
    rows.append(np.arange(NR * NZ)); cols.append(np.arange(NR * NZ)); vals.append(diag)
    return sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(NR * NZ, NR * NZ))


def solve(g, rho, mufun, phi_far, itmax=120, tol=1e-11, omega=1.0, Phi0=None, verbose=False,
          zmin_dirichlet=False):
    NR, NZ = g.NR, g.NZ
    fixed = np.zeros((NR, NZ), dtype=bool)
    fixed[-1, :] = True
    fixed[:, -1] = True
    if zmin_dirichlet:
        fixed[:, 0] = True
    fidx = g.idx[fixed]
    free = g.idx[~fixed]
    phif = phi_far(np.hypot(g.RR, g.ZZ))
    pf = phif[fixed]
    rhs0 = (4 * math.pi * rho * g.vol).ravel()
    Phi = phif.copy() if Phi0 is None else Phi0.copy()
    muR = np.ones((NR - 1, NZ)); muz = np.ones((NR, NZ - 1))
    delta = 1.0
    it = 0
    for it in range(itmax):
        A = assemble(g, muR, muz).tocsr()
        rhs = rhs0 - A[:, fidx] @ pf
        Aff = A[free][:, free].tocsc()
        Pn = np.empty(NR * NZ); Pn[fidx] = pf
        Pn[free] = spla.spsolve(Aff, rhs[free])
        Pn = Pn.reshape(NR, NZ)
        if omega != 1.0:
            Pn = Phi + omega * (Pn - Phi)
        delta = np.max(np.abs(Pn - Phi)) / max(np.max(np.abs(Pn)), 1e-30)
        _, muRn, muzn = residual(g, Pn, rho, mufun, with_mu=True)
        if it == 0:
            muR, muz = muRn, muzn
        else:
            muR = np.sqrt(muRn * muR); muz = np.sqrt(muzn * muz)
        Phi = Pn
        if verbose and (it % 10 == 0):
            print("      it %3d  dPhi %.2e" % (it, delta))
        if delta < tol and it > 2:
            break
    return Phi, it + 1, delta


def laplacian(g, Phi):
    one = lambda x: np.ones_like(x)
    return residual(g, Phi, np.zeros_like(Phi), one) / g.vol


def rho_ph(g, Phi, mufun):
    """rho_ph = div( (1-mu) grad Phi ) / 4 pi  with the same discrete flux operator."""
    (nR, tR), (nz, tz) = faces(g, Phi)
    muR = mufun(np.hypot(nR, tR)); muz = mufun(np.hypot(nz, tz))
    FR = g.AR * (1.0 - muR) * nR
    Fz = g.Az * (1.0 - muz) * nz
    d = np.zeros_like(Phi)
    d[:-1, :] += FR; d[1:, :] -= FR
    d[:, :-1] += Fz; d[:, 1:] -= Fz
    out = np.zeros_like(Phi)
    nz_ = g.vol > 0
    out[nz_] = d[nz_] / g.vol[nz_] / (4 * math.pi)
    return out


def column(g, C, j=0):
    row = C[:, j]
    return float(2 * np.sum(np.minimum(row, 0.0) * g.dR)), row


def gauss2(g, sigma, zc=0.5, mass=1.0):
    """two lenses (one explicit, one mirrored at z=-zc) in the half domain"""
    r2 = g.RR ** 2 + (g.ZZ - zc) ** 2
    return mass * np.exp(-0.5 * r2 / sigma ** 2) / (2 * math.pi * sigma ** 2) ** 1.5
