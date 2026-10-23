"""P4 solver: v3's static weak-field equations on an axisymmetric (ln r, theta) finite-volume grid.

Units: G = a0 = 1 with a length unit ell (kpc): mass unit M_u = a0 ell^2 / G.  grad(Phi) points OUTWARD for attraction
(the physical acceleration is -grad Phi), so a uniform external field is Phi_e = g_e z.

  L* = 0 (AQUAL, one field):   div[ mu(|grad Phi|) grad Phi ] = 4 pi rho,           mu(x) = x / (1 + x)
  L* > 0 (C4-literal stiffened form, gamma_F = 0; the D10 equations, two fields Phi, chi):
        lap Phi = 4 pi rho + div p(grad chi),   chi = Phi + (L*^2 / 2) div p(grad chi),   p(v) = v / (1 + |v|)
  (at L* = 0, chi = Phi and grad Phi - p = mu(|grad Phi|) grad Phi: AQUAL.)
The solver's unknown is the INTERNAL potential phi = Phi - g_e z (Problem.Phi holds phi); observables are internal fields.

Boundaries: theta in [0, pi] (full) or [0, pi/2] with even symmetry about the equator; zero flux at the poles and at r_in;
Dirichlet ghost at r_out from a boundary function Phi_b(theta) (and chi_b = Phi_b).  Newton with the exact sparse Jacobian
and a backtracking line search.  mutate=True swaps mu for the standard x/sqrt(1+x^2) (the --mutate test only).
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

G_SI, MSUN, KPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e19


def mass_unit(a0_si, ell_kpc=1.0):
    """M_u in Msun for G = a0 = 1 with lengths in units of ell kpc."""
    return a0_si * (ell_kpc * KPC) ** 2 / G_SI / MSUN


def nu1(y):
    """v3's isolated spherical law: g = nu1(gN) gN, mu = x/(1+x)  ->  nu1(y) = 1/2 + sqrt(1/4 + 1/y)."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def g_from_gN(gN):
    """exact inverse of g mu(g) = gN for mu = x/(1+x) (a0 = 1): g = (gN + sqrt(gN^2 + 4 gN)) / 2."""
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN))


class Grid:
    def __init__(s, re, te):
        s.re = np.asarray(re, float); s.te = np.asarray(te, float)
        s.Nr = len(s.re) - 1; s.Nt = len(s.te) - 1; s.n = s.Nr * s.Nt
        s.full = abs(s.te[-1] - math.pi) < 1e-12
        assert s.full or abs(s.te[-1] - math.pi / 2) < 1e-12
        s.rc = np.sqrt(s.re[1:] * s.re[:-1]); s.tc = 0.5 * (s.te[1:] + s.te[:-1])
        s.dcos = np.cos(s.te[:-1]) - np.cos(s.te[1:])
        s.vol = (2 * math.pi / 3) * np.outer(s.re[1:] ** 3 - s.re[:-1] ** 3, s.dcos).ravel()
        s.wt = s.dcos / s.dcos.sum()                                   # solid-angle weights of the theta cells
        s._ops()

    def _ops(s):
        Nr, Nt, n, rc, re, tc, te = s.Nr, s.Nt, s.n, s.rc, s.re, s.tc, s.te
        I = np.arange(Nr)[:, None] * Nt + np.arange(Nt)[None, :]       # cell index (i, j)
        # cell-centred (1/r) d/dtheta with mirror ghosts at 0, pi (or pi/2, even symmetry)
        jm = np.arange(Nt) - 1; jp = np.arange(Nt) + 1
        tm = np.where(jm >= 0, tc[np.clip(jm, 0, Nt - 1)], -tc[0])
        endmirror = (2 * math.pi - tc[-1]) if s.full else (math.pi - tc[-1])
        tp = np.where(jp <= Nt - 1, tc[np.clip(jp, 0, Nt - 1)], endmirror)
        jm_c = np.clip(jm, 0, Nt - 1); jp_c = np.clip(jp, 0, Nt - 1)
        rows = np.concatenate([I.ravel(), I.ravel()])
        cols = np.concatenate([(np.arange(Nr)[:, None] * Nt + jp_c[None, :]).ravel(),
                               (np.arange(Nr)[:, None] * Nt + jm_c[None, :]).ravel()])
        den = (rc[:, None] * (tp - tm)[None, :])
        vals = np.concatenate([(1 / den).ravel(), (-1 / den).ravel()])
        s.Cth = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
        # cell-centred d/dr (central; one-sided at both ends)
        im = np.clip(np.arange(Nr) - 1, 0, Nr - 1); ip = np.clip(np.arange(Nr) + 1, 0, Nr - 1)
        h = rc[ip] - rc[im]
        cols = np.concatenate([(ip[:, None] * Nt + np.arange(Nt)[None, :]).ravel(), (im[:, None] * Nt + np.arange(Nt)[None, :]).ravel()])
        vals = np.concatenate([np.repeat(1 / h, Nt), np.repeat(-1 / h, Nt)])
        s.Crr = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
        # interior r faces f = (i, j), i = 0..Nr-2, between (i, j) and (i+1, j)
        nfr = (Nr - 1) * Nt; s.nfr = nfr
        k1 = I[:-1].ravel(); k2 = I[1:].ravel(); f = np.arange(nfr)
        hr = np.repeat(rc[1:] - rc[:-1], Nt)
        s.Dr = sp.csr_matrix((np.concatenate([1 / hr, -1 / hr]), (np.concatenate([f, f]), np.concatenate([k2, k1]))), shape=(nfr, n))
        A1 = sp.csr_matrix((np.full(2 * nfr, 0.5), (np.concatenate([f, f]), np.concatenate([k1, k2]))), shape=(nfr, n))
        s.Tr = (A1 @ s.Cth).tocsr()
        s.fr_r = np.repeat(re[1:-1], Nt); s.fr_t = np.tile(tc, Nr - 1)
        Ar = 2 * math.pi * np.outer(re[1:-1] ** 2, s.dcos).ravel()
        vol = s.vol
        s.Divr = sp.csr_matrix((np.concatenate([Ar / vol[k1], -Ar / vol[k2]]), (np.concatenate([k1, k2]), np.concatenate([f, f]))), shape=(n, nfr))
        # interior theta faces f = (i, j), j = 0..Nt-2, between (i, j) and (i, j+1)
        nft = Nr * (Nt - 1); s.nft = nft
        if nft > 0:
            k1 = I[:, :-1].ravel(); k2 = I[:, 1:].ravel(); f = np.arange(nft)
            ht = (rc[:, None] * (tc[1:] - tc[:-1])[None, :]).ravel()
            s.Dt = sp.csr_matrix((np.concatenate([1 / ht, -1 / ht]), (np.concatenate([f, f]), np.concatenate([k2, k1]))), shape=(nft, n))
            A2 = sp.csr_matrix((np.full(2 * nft, 0.5), (np.concatenate([f, f]), np.concatenate([k1, k2]))), shape=(nft, n))
            s.Tt = (A2 @ s.Crr).tocsr()
            At = (math.pi * np.outer(re[1:] ** 2 - re[:-1] ** 2, np.sin(te[1:-1]))).ravel()
            s.Divt = sp.csr_matrix((np.concatenate([At / vol[k1], -At / vol[k2]]), (np.concatenate([k1, k2]), np.concatenate([f, f]))), shape=(n, nft))
        else:
            s.Dt = sp.csr_matrix((0, n)); s.Tt = sp.csr_matrix((0, n)); s.Divt = sp.csr_matrix((n, 0))
        # outer faces (Dirichlet ghost on the face r = re[-1])
        ko = I[-1]; s.ho = re[-1] - rc[-1]
        s.Do = sp.csr_matrix((np.full(Nt, -1 / s.ho), (np.arange(Nt), ko)), shape=(Nt, n))
        Ao = 2 * math.pi * re[-1] ** 2 * s.dcos
        s.Divo = sp.csr_matrix((Ao / vol[ko], (ko, np.arange(Nt))), shape=(n, Nt))
        s.Lap = (s.Divr @ s.Dr + s.Divt @ s.Dt + s.Divo @ s.Do).tocsr()
        s.r2d = np.repeat(rc, Nt); s.t2d = np.tile(tc, Nr)

    # ---------------------------------------------------------------- sources
    def rho_spherical(s, Mfun):
        """cell densities (uniform in theta) from an enclosed-mass function M(r) (exact mass per shell; M(<r_in) to ring 0)."""
        Me = np.asarray(Mfun(s.re), float)
        dM = np.diff(Me); dM[0] += Me[0]
        shell = (4 * math.pi / 3) * (s.re[1:] ** 3 - s.re[:-1] ** 3)
        return np.repeat(dM / shell, s.Nt)

    def rho_axisym(s, rhofun, nq=4):
        """cell averages of rho(R, z) by Gauss-Legendre quadrature in (r, cos theta)."""
        x, w = np.polynomial.legendre.leggauss(nq)
        out = np.zeros(s.n); norm = np.zeros(s.n)
        lr0, lr1 = np.log(s.re[:-1]), np.log(s.re[1:])
        c0, c1 = np.cos(s.te[:-1]), np.cos(s.te[1:])
        for a, wa in zip(x, w):
            lr = 0.5 * (lr0 + lr1) + 0.5 * (lr1 - lr0) * a; r = np.exp(lr)
            for b, wb in zip(x, w):
                c = 0.5 * (c0 + c1) + 0.5 * (c1 - c0) * b
                R = np.outer(r, np.sqrt(np.maximum(1 - c * c, 0))); Z = np.outer(r, c)
                ww = wa * wb * np.outer(r ** 3 * (lr1 - lr0), np.abs(c1 - c0)).ravel()
                out += ww * rhofun(R.ravel(), Z.ravel()); norm += ww
        return out / norm

    # ---------------------------------------------------------------- observables
    def face_dr(s, Phi):
        """d Phi / dr on the interior r faces, shape (Nr-1, Nt)."""
        return (s.Dr @ Phi).reshape(s.Nr - 1, s.Nt)

    def radial_profiles(s, Phi):
        """(r_face, sphere average, ring at theta = pi/2, great circle through the axis) of dPhi/dr."""
        d = s.face_dr(Phi)
        mono = np.sum(d * s.wt[None, :], axis=1)                       # explicit sums (macOS Accelerate matmul flags)
        dth = np.diff(s.te); gc = np.sum(d * (dth / dth.sum())[None, :], axis=1)
        if s.full and s.Nt > 1:
            j = s.Nt // 2; ring = 0.5 * (d[:, j - 1] + d[:, j]) if s.Nt % 2 == 0 else d[:, j]
        else:
            ring = d[:, -1]
        return s.re[1:-1], mono, ring, gc

    def at_r(s, r_face, prof, r):
        """interpolation of a radial profile at radii r (linear in ln r)."""
        return np.interp(np.log(r), np.log(r_face), prof)

    def grad_cells(s, Phi):
        """(dPhi/dr, (1/r) dPhi/dtheta) at cell centres."""
        return s.Crr @ Phi, s.Cth @ Phi

    def interp_cells(s, field, R, Z):
        """bilinear interpolation of a cell-centred field in (ln r, theta) at points (R, Z) with Z >= 0 for half grids."""
        r = np.sqrt(R * R + Z * Z); th = np.arctan2(R, Z)
        F = field.reshape(s.Nr, s.Nt)
        lr = np.log(s.rc)
        i = np.clip(np.searchsorted(lr, np.log(r)) - 1, 0, s.Nr - 2)
        j = np.clip(np.searchsorted(s.tc, th) - 1, 0, s.Nt - 2)
        fr = np.clip((np.log(r) - lr[i]) / (lr[i + 1] - lr[i]), 0, 1)
        ft = np.clip((th - s.tc[j]) / (s.tc[j + 1] - s.tc[j]), 0, 1)
        return ((1 - fr) * (1 - ft) * F[i, j] + fr * (1 - ft) * F[i + 1, j] + (1 - fr) * ft * F[i, j + 1] + fr * ft * F[i + 1, j + 1])


def log_edges(r_in, r_out, nper, align=None):
    """log-spaced radial edges, nper per decade; with align = r, one edge sits exactly at r (AMENDMENT A4)."""
    if align is None:
        nd = math.log10(r_out / r_in); N = max(int(round(nd * nper)), 4)
        return np.geomspace(r_in, r_out, N + 1)
    nlo = max(int(math.ceil(math.log10(align / r_in) * nper)), 2); nhi = max(int(math.ceil(math.log10(r_out / align) * nper)), 2)
    return align * 10.0 ** (np.arange(-nlo, nhi + 1) / nper)


def theta_edges(Nt, full=True, stretch_min=None):
    """uniform edges; or (half grid) geometric cells refined towards the equator with smallest cell stretch_min (rad)."""
    if stretch_min is None:
        return np.linspace(0, math.pi if full else math.pi / 2, Nt + 1)
    L = math.pi / 2
    lo, hi = 1.0 + 1e-9, 2.0
    for _ in range(200):
        q = 0.5 * (lo + hi)
        if stretch_min * (q ** Nt - 1) / (q - 1) > L: hi = q
        else: lo = q
    q = 0.5 * (lo + hi)
    d = stretch_min * q ** np.arange(Nt); d *= L / d.sum()
    half = np.concatenate([[0.0], np.cumsum(d[::-1])])               # from the pole (big cells) to the equator (small)
    half[-1] = L
    if not full:
        return half
    return np.concatenate([half, math.pi - half[-2::-1]])


class Problem:
    """one solve: grid, cell densities rho (M_u / ell^3), external field ge (a0), stiffness Lam (ell), total mass M (M_u)."""

    def __init__(s, grid, rho, M, ge=0.0, Lam=0.0, mutate=False):
        """Unknown: the INTERNAL potential phi = Phi - ge z.  The uniform external field enters every face flux through its exact
        face average (so its discrete divergence is exactly zero); phi's outer value is the linearised far field."""
        s.g, s.rho, s.M, s.ge, s.Lam, s.mut = grid, rho, M, float(ge), float(Lam), mutate
        g = grid; ro = g.re[-1]
        th = g.tc
        te = g.te; dc = g.dcos
        s2 = np.sin(te) ** 2
        avc = (s2[1:] - s2[:-1]) / (2 * dc)                                  # face average of cos(theta) over a radial face
        avs = ((te[1:] - te[:-1]) / 2 - (np.sin(2 * te[1:]) - np.sin(2 * te[:-1])) / 4) / dc   # face average of sin(theta)
        # radial faces: flux uses the exact face average of the normal component; |v| uses the face-centre components
        s.er_n = np.tile(s.ge * avc, g.Nr - 1); s.er_nc = np.tile(s.ge * np.cos(th), g.Nr - 1); s.er_t = np.tile(-s.ge * np.sin(th), g.Nr - 1)
        # theta faces (cones): the external components are constant on the face
        s.et_n = (np.zeros(g.Nr)[:, None] - s.ge * np.sin(te[1:-1])[None, :]).ravel() if g.Nt > 1 else np.zeros(0)
        s.et_t = (np.zeros(g.Nr)[:, None] + s.ge * np.cos(te[1:-1])[None, :]).ravel() if g.Nt > 1 else np.zeros(0)
        s.eo_n = s.ge * avc; s.eo_nc = s.ge * np.cos(th)
        # inner sphere r_in: the uniform field's own flux enters the innermost ring (internal flux ~ 0 there)
        mu_e0 = (s.ge / math.sqrt(1 + s.ge * s.ge)) if mutate else (s.ge / (1 + s.ge))
        Ain = 2 * math.pi * g.re[0] ** 2 * dc
        s.inflow = np.zeros(g.n); s.inflow[:g.Nt] = -mu_e0 * s.ge * avc * Ain / g.vol[:g.Nt]
        pe0 = s.ge / (1 + s.ge)                                              # p of the uniform field (stiffened form)
        s.inflow_p = np.zeros(g.n); s.inflow_p[:g.Nt] = -pe0 * avc * Ain / g.vol[:g.Nt]
        s.inflow_lap = np.zeros(g.n); s.inflow_lap[:g.Nt] = -s.ge * avc * Ain / g.vol[:g.Nt]
        if s.ge > 0:
            xe = s.ge; mue = xe / (1 + xe); Le = 1.0 / (1 + xe)
            if mutate:
                mue = xe / math.sqrt(1 + xe * xe); Le = 1.0 / (1 + xe * xe)
            s.mue, s.Le = mue, Le
            def phib(t):
                return -s.M / (mue * math.sqrt(1 + Le)) / np.sqrt((ro * np.sin(t)) ** 2 + (ro * np.cos(t)) ** 2 / (1 + Le))
        else:
            def phib(t):
                return np.zeros_like(np.asarray(t, float))
        s.phib = phib(th)
        dt = 1e-6
        s.tb = (phib(th + dt) - phib(th - dt)) / (2 * dt) / ro - s.ge * np.sin(th)   # tangential component on the outer face (total)
        s.bo = s.phib / g.ho
        s.src = 4 * math.pi * rho

    # ---- face flux laws
    def _mu(s, x):
        if s.mut:
            return x / np.sqrt(1 + x * x), 1.0 / (1 + x * x) ** 1.5
        return x / (1 + x), 1.0 / (1 + x) ** 2

    def aq_flux(s, vn, vc, vt):
        """F = mu(|w|) vn, |w| = sqrt(vc^2 + vt^2) (vn: flux normal, vc: face-centre normal); derivatives wrt the common internal
        increments of vn = vc (normal) and vt."""
        v = np.sqrt(vc * vc + vt * vt); vs = np.maximum(v, 1e-300)
        mu, dmu = s._mu(v)
        F = mu * vn
        a = mu + dmu * vn * vc / vs
        b = dmu * vn * vt / vs
        return F, np.maximum(a, 1e-14), b

    def p_flux(s, vn, vc, vt):
        """p_n = vn / (1 + |w|) and its derivatives (the stiffened form; mu = x/(1+x) only)."""
        v = np.sqrt(vc * vc + vt * vt); vs = np.maximum(v, 1e-300)
        a = 1.0 / (1.0 + v)
        F = vn * a
        dn = a - vn * vc * a * a / vs
        dt = -vn * vt * a * a / vs
        return F, dn, dt

    def _div(s, fluxf, U):
        g = s.g
        dU = g.Dr @ U
        Fr, ar, br = fluxf(dU + s.er_n, dU + s.er_nc, g.Tr @ U + s.er_t)
        dU2 = g.Dt @ U
        Ft, at, bt = fluxf(dU2 + s.et_n, dU2 + s.et_n, g.Tt @ U + s.et_t)
        dU3 = g.Do @ U + s.bo
        Fo, ao, bo_ = fluxf(dU3 + s.eo_n, dU3 + s.eo_nc, s.tb)
        D = g.Divr @ Fr + g.Divt @ Ft + g.Divo @ Fo + (s.inflow if fluxf == s.aq_flux else s.inflow_p)
        J = (g.Divr @ (sp.diags(ar) @ g.Dr + sp.diags(br) @ g.Tr) + g.Divt @ (sp.diags(at) @ g.Dt + sp.diags(bt) @ g.Tt)
             + g.Divo @ (sp.diags(ao) @ g.Do))
        return D, J

    def initial(s):
        """quasi-Newtonian start for phi: monopole field g0 = gN / mu(max(g_iso, ge))."""
        g = s.g
        Me = np.cumsum(np.bincount(np.repeat(np.arange(g.Nr), g.Nt), weights=s.rho * g.vol, minlength=g.Nr))
        gN = Me / g.re[1:] ** 2
        giso = g_from_gN(np.abs(gN))                                       # a negative enclosed mass (SPARC's negative gas) points outward
        geff = np.maximum(giso, s.ge)
        g0 = gN * (1 + geff) / np.maximum(geff, 1e-300)
        # potential from r_out inwards, zero at r_out plus the boundary monopole
        dr = np.diff(np.concatenate([g.rc, [g.re[-1]]]))
        phi = -np.cumsum((g0 * dr)[::-1])[::-1]
        U = np.repeat(phi, g.Nt) + float(np.mean(s.phib))
        return U

    def solve_aqual(s, U0=None, tol=1e-10, maxit=80):
        g = s.g
        U = s.initial() if U0 is None else U0.copy()
        it, fin = 0, np.inf
        for it in range(maxit + 1):
            D, J = s._div(s.aq_flux, U)
            R = D - s.src
            sc = 1.0 / np.maximum(abs(J).max(axis=1).toarray().ravel(), 1e-300)
            fin = float(np.max(np.abs(sc * R)))
            if fin < tol or it == maxit:
                break
            dU = -spl.spsolve((sp.diags(sc) @ J).tocsc(), sc * R)
            al = 1.0
            for _ in range(40):
                Dn, _ = s._div(s.aq_flux, U + al * dU)
                Fn = float(np.max(np.abs(sc * (Dn - s.src))))
                if np.isfinite(Fn) and Fn < (1 - 1e-4 * al) * fin:
                    break
                al *= 0.5
            U = U + al * dU
        s.Phi, s.res, s.it = U, fin, it
        return U, fin, it

    def solve_newton(s):
        """Newtonian potential (mu = 1) with the isolated point-mass boundary value -M/r_out (no external field)."""
        g = s.g
        bo = np.full(g.Nt, -s.M / g.re[-1]) / g.ho
        s.PhiN = spl.spsolve(g.Lap.tocsc(), s.src - g.Divo @ bo)
        return s.PhiN

    def solve(s, U0=None, tol=1e-10, maxit=80):
        """L* = 0: AQUAL.  L* > 0: the two-field stiffened system, started from the AQUAL solution."""
        Phi0, res0, it0 = s.solve_aqual(U0=U0, tol=tol, maxit=maxit)
        if s.Lam <= 0:
            return s.Phi
        assert not s.mut
        g = s.g; n = g.n; lam2 = 0.5 * s.Lam ** 2
        I = sp.identity(n, format="csr")
        L = g.Lap; Lb = g.Divo @ s.bo
        U = np.concatenate([Phi0, Phi0])
        fin = np.inf
        for it in range(maxit + 1):
            Phi, chi = U[:n], U[n:]
            D, J = s._div(s.p_flux, chi)
            R1 = L @ Phi + Lb - D - s.src
            R2 = chi - Phi - lam2 * D
            Jac = sp.bmat([[L, -J], [-I, I - lam2 * J]], format="csr")
            sc = 1.0 / np.maximum(abs(Jac).max(axis=1).toarray().ravel(), 1e-300)
            F = np.concatenate([R1, R2])
            fin = float(np.max(np.abs(sc * F)))
            if fin < tol or it == maxit:
                break
            dU = -spl.spsolve((sp.diags(sc) @ Jac).tocsc(), sc * F)
            al = 1.0
            for _ in range(40):
                Un = U + al * dU
                Dn, _ = s._div(s.p_flux, Un[n:])
                Fn = np.concatenate([L @ Un[:n] + Lb - Dn - s.src, Un[n:] - Un[:n] - lam2 * Dn])
                fn = float(np.max(np.abs(sc * Fn)))
                if np.isfinite(fn) and fn < (1 - 1e-4 * al) * fin:
                    break
                al *= 0.5
            U = U + al * dU
        s.Phi, s.chi, s.res, s.it = U[:n], U[n:], fin, it
        return s.Phi


def plummer_M(M, a):
    return lambda r: M * np.asarray(r, float) ** 3 / (np.asarray(r, float) ** 2 + a * a) ** 1.5


def uniform_M(M, R):
    return lambda r: M * np.minimum(np.asarray(r, float) / R, 1.0) ** 3


def hernquist_M(M, a):
    return lambda r: M * np.asarray(r, float) ** 2 / (np.asarray(r, float) + a) ** 2


def sphere_grid(r_in, r_out, nper=20, Nt=16):
    return Grid(log_edges(r_in, r_out, nper), theta_edges(Nt, full=True))


def r_out_for(M, ge, rmax, fac=300.0):
    """outer radius: fac x max(rmax, r_e), r_e = sqrt(M)/ge (deep) or sqrt(M/ge) (strong field), G = a0 = 1."""
    re_ = 0.0
    if ge > 0:
        re_ = max(math.sqrt(max(M, 0)) / ge, math.sqrt(max(M, 0) / ge))
    else:
        re_ = math.sqrt(max(M, 0))
    return fac * max(rmax, re_)
