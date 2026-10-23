"""V1_density_screen solvers.

Record solvers are imported read-only and wrapped; nothing in them is edited:
  D10 (doors_push_2026_10_22/D10_native_Lstar/d10_solver.py): Plummer cluster in a uniform total field (globulars, satellites).
  D7d (doors_push_2026_10_22/D7d_screened_q2/d7d_solver.py): Route N, point-mass Sun in the Galactic field (Cassini Q2).
  P4  (rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_solver.py): axisymmetric AQUAL (MW, thin-slab test).
The screen enters every wrapper the same way: a screening level s multiplies the phantom (P-sector) flux only, so the
static equation is div[mu_S grad Phi] = K rho with mu_S = 1 - s (1 - mu), mu = x/(1+x).
MUTATE (--mutate): s multiplies the whole gravitational response (source and phantom) -- the wrong insertion point.

Own solver: a 1D radial finite-volume Newton solver for the symmetron equation
    (1/r^2)(r^2 psi')' = m^2 psi (psi^2 - 1 + d(r)),   d = rho/rho_*,  lengths in the body radius R.
"""
import os, sys, math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for sub in (("doors_push_2026_10_22", "D10_native_Lstar"), ("doors_push_2026_10_22", "D7d_screened_q2"),
            ("rebuild_2026_10_22", "P4_v3_galaxy_tiles")):
    p = os.path.join(REPO, *sub)
    if p not in sys.path:
        sys.path.insert(0, p)
import d10_solver as S10   # noqa: E402
import d7d_solver as S7    # noqa: E402
import p4_solver as S4     # noqa: E402

np.seterr(all="ignore")    # macOS Accelerate emits spurious matmul warnings inside the record solvers' Legendre setup


# ===================================================================== laws
def g_from_gN_S(gN, s):
    """uniform-s AQUAL in a0 units: g (1 - s/(1+g)) = gN  ->  g = [(gN + s - 1) + sqrt((1 - s - gN)^2 + 4 gN)] / 2."""
    gN = np.asarray(gN, float)
    return 0.5 * ((gN + s - 1.0) + np.sqrt((1.0 - s - gN) ** 2 + 4.0 * gN))


def g_law(gN, s, mutate=False):
    """the screen's spherical law; MUTATE scales the source too."""
    return g_from_gN_S(s * gN if mutate else gN, s)


# ===================================================================== D10 wrapper (globulars, satellites)
class GCSolverS(S10.Solver2D):
    """D10's Solver2D at L* = 0 with the phantom flux multiplied by a uniform s."""

    def __init__(s, g, y, xe, sfac, mutate=False):
        super().__init__(g, y, xe, 0.0)
        s.sfac, s.mut = float(sfac), bool(mutate)
        if s.mut:
            s.phiN = s.sfac * s.phiN          # source scaled as well (wrong insertion)

    def divp(s, chi):
        D, J, Fo = super().divp(chi)
        return s.sfac * D, s.sfac * J, s.sfac * Fo

    def field_monopole(s, U=None):
        g = s.g; U = s.U if U is None else U
        psi0 = g.monopole(U[g.n:])
        rf = g.re[1:-1]
        dpsi = np.diff(psi0) / np.diff(g.rc)
        gN = S10.plummer_gN(rf, s.y) * (s.sfac if s.mut else 1.0)
        return rf, gN + dpsi


def gc_sigma(grid, y, xe, sfac, Rbin, mutate=False, U0=None):
    """(sigma_p^2 at Rbin [E-P], virial sigma^2 [E-V], Wolf sigma^2 [E-W], U, residual) in solver units (a = 1, a0 = 1)."""
    sv = GCSolverS(grid, y, xe, sfac, mutate=mutate)
    U, res, it = sv.solve(U0=U0)
    rf, gr = sv.field_monopole()
    s2, vir, wo = S10.jeans(rf, gr, [Rbin])
    return float(s2[0]), vir, wo, U, res


# ===================================================================== D7d wrapper (Cassini Q2)
def solve_q2_S(g, xe, sfac, mutate=False, maxit=12, U0=None):
    """D7d Route N at L* = 0 (AQUAL) with the psi-row phantom columns multiplied by s.  Returns (U, final scaled residual, its)."""
    A, rhs, nl = S7.build(g, 0.0, False, "stiff")
    Nr, Nt = g.Nr, g.Nt; n = Nr * Nt
    CT = np.broadcast_to(g.ct, (Nr, Nt)); ST = np.broadcast_to(g.st, (Nr, Nt))
    A = A.tocsc(); Apsi = A[:, :n]; Aq = A[:, n:]
    Aq = (sp.diags(np.concatenate([np.full(n, sfac), np.ones(2 * n)])) @ Aq).tocsc()
    if mutate:
        rhs = sfac * rhs
    nlr = np.repeat(nl, Nt).astype(float)
    Dw = sp.diags(np.concatenate([nlr * np.repeat(g.r ** 2, Nt)] * 2))
    Z = sp.csc_matrix((n, 2 * n))
    U = np.zeros(g.N) if U0 is None else U0.copy()

    def resid(U):
        wr = U[n:2 * n].reshape(Nr, Nt); wt = U[2 * n:].reshape(Nr, Nt)
        pr, pt, J = S7.dP(xe, CT, ST, wr, wt)
        F = Apsi @ U[:n] + Aq @ np.concatenate([pr.ravel(), pt.ravel()]) + np.concatenate([np.zeros(n), Dw @ U[n:]]) - rhs
        return F, J
    fin = np.inf; it = 0
    for it in range(maxit + 1):
        F, J = resid(U)
        if not np.all(np.isfinite(F)):
            fin = np.inf; break
        Jb = sp.bmat([[sp.diags(J[0].ravel()), sp.diags(J[1].ravel())], [sp.diags(J[2].ravel()), sp.diags(J[3].ravel())]])
        Jac = sp.hstack([Apsi, Aq @ Jb + sp.vstack([Z, Dw])]).tocsr()
        sc = 1 / np.maximum(abs(Jac).max(axis=1).toarray().ravel(), 1e-300)
        fin = float(np.linalg.norm(sc * F))
        if fin < 1e-11 or it == maxit:
            break
        dU = -spl.spsolve((sp.diags(sc) @ Jac).tocsc(), sc * F); alpha = 1.0
        for _ in range(40):
            Fn, _ = resid(U + alpha * dU)
            if np.all(np.isfinite(Fn)) and np.linalg.norm(sc * Fn) < (1 - 1e-4 * alpha) * fin:
                break
            alpha *= 0.5
        if alpha < 1e-9:
            break
        U = U + alpha * dU
    return U.reshape(3, Nr, Nt), fin, it


# ===================================================================== P4 wrapper (axisymmetric AQUAL with s(R, z))
class ProblemS(S4.Problem):
    """P4's Problem (AQUAL, L* = 0) with face-dependent screening s: mu_S = 1 - s (1 - mu).
    sfun(R, z) -> s; uniform s if sfun is a number.  MUTATE (uniform only): the source is scaled by s too."""

    def __init__(s, grid, rho, M, ge=0.0, sfun=1.0, mutate=False):
        super().__init__(grid, rho, M, ge=ge, Lam=0.0)
        g = grid
        if callable(sfun):
            rr = g.fr_r; tt = g.fr_t
            s.Sr = sfun(rr * np.sin(tt), rr * np.cos(tt))
            if g.Nt > 1:
                rt = np.repeat(g.rc, g.Nt - 1); tht = np.tile(g.te[1:-1], g.Nr)
                s.St = sfun(rt * np.sin(tht), rt * np.cos(tht))
            else:
                s.St = np.zeros(0)
            s.So = sfun(g.re[-1] * np.sin(g.tc), g.re[-1] * np.cos(g.tc))
        else:
            s.Sr = np.full(g.nfr, float(sfun)); s.St = np.full(g.nft, float(sfun)); s.So = np.full(g.Nt, float(sfun))
            if mutate:
                s.src = float(sfun) * s.src
        s.inflow = s.inflow * 0.0 if ge == 0 else s.inflow     # isolated use only below

    @staticmethod
    def _wrap(fluxf, Sx):
        def f(vn, vc, vt):
            F, a, b = fluxf(vn, vc, vt)
            return (1 - Sx) * vn + Sx * F, (1 - Sx) + Sx * a, Sx * b
        return f

    def _div(s, fluxf, U):
        if fluxf != s.aq_flux:
            return super()._div(fluxf, U)
        g = s.g
        fr = s._wrap(s.aq_flux, s.Sr); ft = s._wrap(s.aq_flux, s.St); fo = s._wrap(s.aq_flux, s.So)
        dU = g.Dr @ U
        Fr, ar, br = fr(dU + s.er_n, dU + s.er_nc, g.Tr @ U + s.er_t)
        dU2 = g.Dt @ U
        Ft, at, bt = ft(dU2 + s.et_n, dU2 + s.et_n, g.Tt @ U + s.et_t)
        dU3 = g.Do @ U + s.bo
        Fo, ao, bo_ = fo(dU3 + s.eo_n, dU3 + s.eo_nc, s.tb)
        D = g.Divr @ Fr + g.Divt @ Ft + g.Divo @ Fo + s.inflow
        J = (g.Divr @ (sp.diags(ar) @ g.Dr + sp.diags(br) @ g.Tr) + g.Divt @ (sp.diags(at) @ g.Dt + sp.diags(bt) @ g.Tt)
             + g.Divo @ (sp.diags(ao) @ g.Do))
        return D, J


# ===================================================================== own symmetron BVP (1D radial)
def symmetron_radial(m, d_body, d_amb, R=1.0, rmax=None, n_in=300, n_out=500, h0=1e-5, tol=1e-12, maxit=200):
    """Uniform sphere (radius R, d = rho/rho_* = d_body) in an ambient d_amb < 1.  Returns (r_nodes, psi, psi_amb, info).
    Finite volume on cells; Neumann at r = 0; Dirichlet psi = psi_amb at rmax; Newton with a tridiagonal Jacobian."""
    psi_a = math.sqrt(1.0 - d_amb); ma = m * math.sqrt(2.0) * psi_a
    if rmax is None:
        rmax = R + 60.0 / ma
    # faces: inside, geometric clustering towards R from the centre; outside, geometric from R outwards
    q_in = np.geomspace(h0, R, n_in)                                   # distances from the surface, inward
    f_in = np.sort(np.concatenate([[0.0], R - q_in[::-1][:-1], [R]]))
    f_in = np.unique(np.clip(f_in, 0.0, R))
    f_out = R + np.geomspace(h0, rmax - R, n_out)
    faces = np.concatenate([f_in, f_out])
    rc = 0.5 * (faces[1:] + faces[:-1])
    vol = (faces[1:] ** 3 - faces[:-1] ** 3) / 3.0
    dvec = np.where(rc < R, d_body, d_amb)
    N = len(rc)
    fa = faces[1:-1] ** 2 / (rc[1:] - rc[:-1])                         # interior face conductances
    gb = faces[-1] ** 2 / (faces[-1] - rc[-1])                          # Dirichlet ghost at rmax
    psi = np.where(rc < R, math.sqrt(max(0.0, 1.0 - d_body)) + 1e-3, psi_a)

    def resid(p):
        flux = fa * (p[1:] - p[:-1])
        div = np.zeros(N); div[:-1] += flux; div[1:] -= flux
        div[-1] += gb * (psi_a - p[-1])
        return div - vol * m * m * p * (p * p - 1.0 + dvec)
    w = 1.0 / np.sqrt(vol)                                              # residual weights for the line search
    it = 0; fn = np.inf
    for it in range(maxit):
        F = resid(psi)
        dmain = np.zeros(N); dmain[:-1] -= fa; dmain[1:] -= fa; dmain[-1] -= gb
        dmain -= vol * m * m * (3 * psi * psi - 1.0 + dvec)
        sc = 1.0 / np.maximum(np.abs(dmain), 1e-300)                    # row scaling (|diagonal| dominates the row)
        fn = float(np.max(np.abs(sc * F)))
        if fn < tol:
            break
        Jm = sp.diags([dmain, fa, fa], [0, 1, -1], format="csc")
        dp = spl.spsolve(Jm, -F)
        f2 = float(np.linalg.norm(w * F)); al = 1.0
        for _ in range(50):
            pn = psi + al * dp
            if np.linalg.norm(w * resid(pn)) < (1 - 1e-4 * al) * f2:
                break
            al *= 0.5
        psi = pn
    return rc, psi, psi_a, dict(iters=it, res=fn, ma=ma, rmax=rmax, N=N)


def form_factor(z):
    """3 (z cosh z - sinh z) / z^3 (uniform sphere, Yukawa), -> 1 as z -> 0."""
    if z < 1e-4:
        return 1.0 + z * z / 10.0
    return 3.0 * (z * math.cosh(z) - math.sinh(z)) / z ** 3
