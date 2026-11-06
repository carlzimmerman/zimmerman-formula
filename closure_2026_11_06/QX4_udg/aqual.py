"""QX4 axisymmetric AQUAL solver: div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho, mu(x) = x/(1+x).

Finite volume on cells in (x = ln r, theta), theta in [0, pi/2] (equatorial symmetry, zero flux through the plane and
the axis), Dirichlet Phi = 0 on the sphere r = r_max (any constant: only gradients enter), zero flux at r_min.
Units: kpc, km/s, Msun. G = 4.30091e-6 kpc (km/s)^2/Msun. a0 is passed in (km/s)^2/kpc. mu_one=True gives Newton.
Nonlinear solve: Picard (frozen mu, sparse direct solve) with damping. Kappa = 1/2 FITTED; not theory closed.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

G = 4.30091e-6
CONV = 1e6 / 3.0857e19                      # (km/s)^2/kpc -> m/s^2


def a0_kpc(a0_si): return a0_si / CONV


class Grid:
    def __init__(self, r_min, r_max, nr, nt, p=2.0):
        self.xf = np.linspace(np.log(r_min), np.log(r_max), nr + 1)
        self.xc = 0.5 * (self.xf[1:] + self.xf[:-1]); self.dx = self.xf[1] - self.xf[0]
        s = np.linspace(0, 1, nt + 1)
        self.tf = 0.5 * np.pi * (1 - (1 - s) ** p)                  # faces, clustered at the plane (theta = pi/2)
        self.tc = 0.5 * (self.tf[1:] + self.tf[:-1])
        self.rf = np.exp(self.xf); self.rc = np.exp(self.xc)
        self.nr, self.nt = nr, nt

    def deposit(self, rho_fn, nsub=6):
        """Mass per cell (northern hemisphere) from rho(R, z) by midpoint sub-sampling of 2 pi r^2 sin(t) dr dt."""
        M = np.zeros((self.nr, self.nt))
        u = (np.arange(nsub) + 0.5) / nsub
        for i in range(self.nr):
            x = self.xf[i] + u * self.dx; r = np.exp(x)
            for j in range(self.nt):
                t = self.tf[j] + u * (self.tf[j + 1] - self.tf[j]); dt = (self.tf[j + 1] - self.tf[j]) / nsub
                R = r[:, None] * np.sin(t)[None, :]; z = r[:, None] * np.cos(t)[None, :]
                w = 2 * np.pi * (r ** 3)[:, None] * np.sin(t)[None, :] * (self.dx / nsub) * dt
                M[i, j] = np.sum(rho_fn(R, z) * w)
        return M


def _gradients(g, Phi):
    """Cell-centred gradient components (g_r, g_t) by central differences (one-sided at the ends, Dirichlet 0 outside)."""
    P = np.vstack([Phi, -Phi[-1:, :]])                                   # ghost at r_max: Phi_b = 0 -> ghost = -Phi_last
    xc_ext = np.append(g.xc, g.xc[-1] + g.dx)
    gr = np.gradient(P, xc_ext, axis=0)[:-1] / g.rc[:, None]
    gt = np.gradient(Phi, g.tc, axis=1) / g.rc[:, None]
    gt[:, -1] = 0.5 * (Phi[:, -1] - Phi[:, -2]) / (g.tc[-1] - g.tc[-2]) / g.rc   # symmetric plane: average with 0
    return gr, gt


def mu_fn(x, mu_one):
    return np.ones_like(x) if mu_one else x / (1.0 + x)


def assemble(g, Phi, a0, mu_one):
    nr, nt = g.nr, g.nt
    gr, gt = _gradients(g, Phi)
    idx = lambda i, j: i * nt + j
    rows, cols, vals = [], [], []
    diag = np.zeros(nr * nt); rhs_extra = np.zeros(nr * nt)
    dcos = np.cos(g.tf[:-1]) - np.cos(g.tf[1:])                         # per theta cell
    # r faces i+1/2 for i = 0..nr-1 (last one is the Dirichlet boundary)
    for i in range(nr):
        rf = g.rf[i + 1]
        if i < nr - 1:
            dPhi = Phi[i + 1] - Phi[i]
            gt_f = 0.5 * (gt[i] + gt[i + 1])
        else:
            dPhi = 0.0 - Phi[i]; dPhi = 2 * dPhi                         # boundary half-cell: face value 0
            gt_f = gt[i]
        g_r = dPhi / (rf * g.dx)
        x = np.sqrt(g_r ** 2 + gt_f ** 2) / a0
        m = mu_fn(x, mu_one)
        c = 2 * np.pi * rf * dcos * m / g.dx                             # flux = c * (Phi_{i+1} - Phi_i)
        for j in range(nt):
            k = idx(i, j)
            if i < nr - 1:
                kk = idx(i + 1, j)
                rows += [k, k, kk, kk]; cols += [k, kk, kk, k]; vals += [-c[j], c[j], -c[j], c[j]]
            else:
                diag[k] += -2 * c[j]                                     # Phi_face = 0 at distance dx/2
    # theta faces j+1/2 for j = 0..nt-2 (plane and axis: zero flux)
    area_r = 0.5 * (g.rf[1:] ** 2 - g.rf[:-1] ** 2) / g.rc               # per r cell
    for j in range(nt - 1):
        tf = g.tf[j + 1]; dtc = g.tc[j + 1] - g.tc[j]
        g_t = (Phi[:, j + 1] - Phi[:, j]) / (g.rc * dtc)
        gr_f = 0.5 * (gr[:, j] + gr[:, j + 1])
        x = np.sqrt(g_t ** 2 + gr_f ** 2) / a0
        m = mu_fn(x, mu_one)
        c = 2 * np.pi * np.sin(tf) * area_r * m / dtc
        for i in range(nr):
            k = idx(i, j); kk = idx(i, j + 1)
            rows += [k, k, kk, kk]; cols += [k, kk, kk, k]; vals += [-c[i], c[i], -c[i], c[i]]
    A = sp.csr_matrix((vals, (rows, cols)), shape=(nr * nt, nr * nt)) + sp.diags(diag)
    return A


def solve(g, M, a0, mu_one=False, tol=1e-8, maxit=400, omega=0.7, Phi0=None, verbose=False):
    b = 4 * np.pi * G * M.ravel()
    Phi = np.zeros((g.nr, g.nt)) if Phi0 is None else Phi0.copy()
    if Phi0 is None:                                                     # Newtonian start
        A = assemble(g, Phi, a0, True); Phi = spla.spsolve(A.tocsc(), b).reshape(g.nr, g.nt)
        if mu_one: return Phi, 0.0, 0
    hist = []
    for it in range(maxit):
        A = assemble(g, Phi, a0, mu_one)
        res = np.linalg.norm(A @ Phi.ravel() - b) / np.linalg.norm(b)
        hist.append(res)
        if verbose and it % 10 == 0: print(f"   it {it} res {res:.3e}", flush=True)
        if res < tol: return Phi, res, it
        new = spla.spsolve(A.tocsc(), b).reshape(g.nr, g.nt)
        Phi = Phi + omega * (new - Phi)
    return Phi, hist[-1], maxit


def midplane_vc(g, Phi, R):
    """V_c^2 = R dPhi/dR in the plane: radial derivative of the plane-adjacent row (cell centre at theta ~ pi/2)."""
    row = Phi[:, -1]
    d = np.gradient(row, g.xc)                                           # dPhi/dln r = r dPhi/dr
    v2 = np.interp(np.log(R), g.xc, d)
    return np.sqrt(np.maximum(v2, 0))


def radial_g(g, Phi, r, j):
    d = np.gradient(Phi[:, j], g.xc) / g.rc
    return np.interp(np.log(r), g.xc, d)
