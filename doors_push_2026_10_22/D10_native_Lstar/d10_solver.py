"""D10 solvers: the C4-literal stiffened equations (gamma_F = 0) for a Plummer cluster in a uniform external field.

Static, weak field, a0 units for accelerations, lengths in the Plummer scale a (= r_h,l):
    (L)   lap Phi = K rho + div p          (P_L)  grad Phi + (Lam^2/2) grad(div p) = p / (1 - |p|)
Scalar reduction (sympy-checked in K1): p = p(v) = v / (1 + |v|), v = grad chi,
    lap psi = div p(grad chi),      chi = Phi_N + psi + (Lam^2/2) div p(grad chi),      grad Phi = grad Phi_N + grad psi.
Background chi_e = x_e z (total external field x_e = g_e / a0); unknowns are the perturbations dchi, dpsi.
Plummer: Phi_N = -y / sqrt(1 + r^2), y = G M / (a^2 a0).   Gradients are 'outward' (attraction = positive radial field).

Route N2 : 2D axisymmetric finite volume on (ln r, theta), Newton with the exact sparse Jacobian.
Route R1 : 1D isolated radial BVP (independent: scipy solve_bvp on the p-ODE).
Route F  : linear response about the background (C6's frozen kernel), Plummer source, monopole by quadrature.
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl
from scipy.special import k1 as besk1
from scipy.integrate import solve_bvp


# ------------------------------------------------------------------ the law and Plummer
def law_v(gN):
    """isolated spherical AQUAL with mu = x/(1+x): v^2/(1+v) = gN  ->  v = (gN + sqrt(gN^2 + 4 gN))/2."""
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN))


def plummer_gN(r, y):
    return y * r / (1.0 + r * r) ** 1.5


def plummer_phi(r, y):
    return -y / np.sqrt(1.0 + r * r)


# ------------------------------------------------------------------ Route N2
class Grid2D:
    def __init__(s, rin=1e-3, rout=1e4, nper=17, Nt=16):
        nd = math.log10(rout / rin); s.Nr = int(round(nd * nper))
        s.re = np.geomspace(rin, rout, s.Nr + 1); s.rc = np.sqrt(s.re[1:] * s.re[:-1])
        s.Nt = Nt; s.dt = math.pi / Nt; s.te = np.arange(Nt + 1) * s.dt; s.tc = (np.arange(Nt) + 0.5) * s.dt
        s.n = s.Nr * Nt
        s.wt = (np.cos(s.te[:-1]) - np.cos(s.te[1:])) / 2.0          # monopole weights (sum = 1)
        s._ops()

    def k(s, i, j):
        return i * s.Nt + j

    def _ops(s):
        Nr, Nt, rc, re, dt = s.Nr, s.Nt, s.rc, s.re, s.dt
        n = s.n
        # cell-centred theta derivative (1/r) d/dtheta, reflective at the poles
        R, C, V = [], [], []
        for i in range(Nr):
            for j in range(Nt):
                jp_, jm_ = min(j + 1, Nt - 1), max(j - 1, 0)
                kk = s.k(i, j)
                # even reflection: ghost value equals the edge cell
                R += [kk, kk]; C += [s.k(i, jp_), s.k(i, jm_)]; V += [1 / (2 * dt * rc[i]), -1 / (2 * dt * rc[i])]
        s.Cth = sp.csr_matrix((V, (R, C)), shape=(n, n))
        # cell-centred radial derivative (central, one-sided at the ends)
        R, C, V = [], [], []
        for i in range(Nr):
            for j in range(Nt):
                kk = s.k(i, j)
                if 0 < i < Nr - 1:
                    h = rc[i + 1] - rc[i - 1]; R += [kk, kk]; C += [s.k(i + 1, j), s.k(i - 1, j)]; V += [1 / h, -1 / h]
                elif i == 0:
                    h = rc[1] - rc[0]; R += [kk, kk]; C += [s.k(1, j), kk]; V += [1 / h, -1 / h]
                else:
                    h = rc[i] - rc[i - 1]; R += [kk, kk]; C += [kk, s.k(i - 1, j)]; V += [1 / h, -1 / h]
        s.Crr = sp.csr_matrix((V, (R, C)), shape=(n, n))
        # interior r faces f = (i, j) between cells i and i+1, i = 0..Nr-2
        nfr = (Nr - 1) * Nt; s.nfr = nfr
        R, C, V = [], [], []; Ra, Ca, Va = [], [], []
        s.fr_r = np.repeat(re[1:-1], Nt); s.fr_t = np.tile(s.tc, Nr - 1)
        for i in range(Nr - 1):
            h = rc[i + 1] - rc[i]
            for j in range(Nt):
                f = i * Nt + j
                R += [f, f]; C += [s.k(i + 1, j), s.k(i, j)]; V += [1 / h, -1 / h]
                Ra += [f, f]; Ca += [s.k(i, j), s.k(i + 1, j)]; Va += [0.5, 0.5]
        s.Dr = sp.csr_matrix((V, (R, C)), shape=(nfr, n))
        s.Tr = sp.csr_matrix((Va, (Ra, Ca)), shape=(nfr, n)) @ s.Cth
        # interior theta faces (i, j) between j and j+1, j = 0..Nt-2
        nft = Nr * (Nt - 1); s.nft = nft
        R, C, V = [], [], []; Ra, Ca, Va = [], [], []
        s.ft_r = np.repeat(rc, Nt - 1); s.ft_t = np.tile(s.te[1:-1], Nr)
        for i in range(Nr):
            for j in range(Nt - 1):
                f = i * (Nt - 1) + j
                R += [f, f]; C += [s.k(i, j + 1), s.k(i, j)]; V += [1 / (rc[i] * dt), -1 / (rc[i] * dt)]
                Ra += [f, f]; Ca += [s.k(i, j), s.k(i, j + 1)]; Va += [0.5, 0.5]
        s.Dt = sp.csr_matrix((V, (R, C)), shape=(nft, n))
        s.Tt = sp.csr_matrix((Va, (Ra, Ca)), shape=(nft, n)) @ s.Crr
        # outer face (cell Nr-1, j): Robin f ~ 1/r
        s.fo_t = s.tc.copy(); ro, rl = re[-1], rc[-1]
        R = list(range(Nt)); C = [s.k(Nr - 1, j) for j in range(Nt)]
        s.Do = sp.csr_matrix((-rl / ro ** 2 * np.ones(Nt), (R, C)), shape=(Nt, n))
        s.To = sp.csr_matrix((np.ones(Nt) * (rl / ro) ** 2, (R, C)), shape=(Nt, n)) @ s.Cth
        s.Eo = sp.csr_matrix((np.ones(Nt), (R, C)), shape=(Nt, n))  # selector of the outer cells
        # divergence operators (face fluxes -> cell divergence)
        vol = (re[1:] ** 3 - re[:-1] ** 3) / 3.0                      # per unit (cos) solid-angle factor
        R, C, V = [], [], []
        for i in range(Nr - 1):
            for j in range(Nt):
                f = i * Nt + j
                R += [s.k(i, j), s.k(i + 1, j)]; C += [f, f]
                V += [re[i + 1] ** 2 / vol[i], -re[i + 1] ** 2 / vol[i + 1]]
        s.Divr = sp.csr_matrix((V, (R, C)), shape=(n, nfr))
        R = [s.k(Nr - 1, j) for j in range(Nt)]; C = list(range(Nt))
        s.Divo = sp.csr_matrix((re[-1] ** 2 / vol[-1] * np.ones(Nt), (R, C)), shape=(n, Nt))
        R, C, V = [], [], []
        dcos = np.cos(s.te[:-1]) - np.cos(s.te[1:])
        for i in range(Nr):
            ar = (re[i + 1] ** 2 - re[i] ** 2) / 2.0
            for j in range(Nt - 1):
                f = i * (Nt - 1) + j; st = math.sin(s.te[j + 1])
                R += [s.k(i, j), s.k(i, j + 1)]; C += [f, f]
                V += [st * ar / (vol[i] * dcos[j]), -st * ar / (vol[i] * dcos[j + 1])]
        s.Divt = sp.csr_matrix((V, (R, C)), shape=(n, nft))
        # vector Laplacian-free scalar Laplacian (Robin outer)
        s.Lap = (s.Divr @ s.Dr + s.Divt @ s.Dt + s.Divo @ s.Do).tocsr()
        s.r2d = np.repeat(rc, Nt); s.t2d = np.tile(s.tc, Nr)

    def monopole(s, f):
        return (f.reshape(s.Nr, s.Nt) * s.wt).sum(1)


def _pflux(vn, vt, vne, vte):
    """normal flux p_n(v) - p_n(v_e) and its derivatives wrt (vn, vt)."""
    vm = np.sqrt(vn * vn + vt * vt); vme = np.sqrt(vne * vne + vte * vte)
    a = 1.0 / (1.0 + vm)
    F = vn * a - vne / (1.0 + vme)
    vmc = np.maximum(vm, 1e-300)
    dn = a - vn * vn * a * a / vmc
    dt_ = -vn * vt * a * a / vmc
    return F, dn, dt_


class Solver2D:
    def __init__(s, g, y, xe, Lam, isolated=False, mutate=False):
        s.g, s.y, s.xe, s.Lam, s.iso = g, y, xe, Lam, isolated
        s.lam2 = (Lam ** 2) if mutate else 0.5 * Lam ** 2
        s.phiN = plummer_phi(g.r2d, y)
        # background components at faces
        s.ber = xe * np.cos(g.fr_t); s.bet_r = -xe * np.sin(g.fr_t)
        s.btr = xe * np.cos(g.ft_t); s.btt = -xe * np.sin(g.ft_t)
        s.bor = xe * np.cos(g.fo_t); s.bot = -xe * np.sin(g.fo_t)
        if isolated:   # exact outer field from the law (isolated spherical, Lam << r_out)
            ro = g.re[-1]; Mfrac = ro ** 3 / (1 + ro ** 2) ** 1.5
            s.vout = float(law_v(y * Mfrac / ro ** 2))

    def divp(s, chi):
        g = s.g
        vn = g.Dr @ chi + s.ber; vt = g.Tr @ chi + s.bet_r
        Fr, ar, br = _pflux(vn, vt, s.ber, s.bet_r)
        vn2 = g.Dt @ chi + s.btt; vt2 = g.Tt @ chi + s.btr
        Ft, at, bt = _pflux(vn2, vt2, s.btt, s.btr)
        if s.iso:
            # isolated: the outer flux is radial; p_r = v/(1+v) at the prescribed v_out (monopole)
            Fo = np.full(g.Nt, s.vout / (1 + s.vout))
            D = g.Divr @ Fr + g.Divt @ Ft + g.Divo @ Fo
            J = g.Divr @ (sp.diags(ar) @ g.Dr + sp.diags(br) @ g.Tr) + g.Divt @ (sp.diags(at) @ g.Dt + sp.diags(bt) @ g.Tt)
            return D, J, Fo
        vn3 = g.Do @ chi + s.bor; vt3 = g.To @ chi + s.bot
        Fo, ao, bo = _pflux(vn3, vt3, s.bor, s.bot)
        D = g.Divr @ Fr + g.Divt @ Ft + g.Divo @ Fo
        J = (g.Divr @ (sp.diags(ar) @ g.Dr + sp.diags(br) @ g.Tr) + g.Divt @ (sp.diags(at) @ g.Dt + sp.diags(bt) @ g.Tt)
             + g.Divo @ (sp.diags(ao) @ g.Do + sp.diags(bo) @ g.To))
        return D, J, Fo

    def lap_psi(s, psi, Fo):
        g = s.g
        if s.iso:   # outer flux of grad psi equals the outer p flux (Gauss)
            return g.Divr @ (g.Dr @ psi) + g.Divt @ (g.Dt @ psi) + g.Divo @ Fo, (g.Divr @ g.Dr + g.Divt @ g.Dt)
        return g.Lap @ psi, g.Lap

    def resid(s, U):
        n = s.g.n; chi, psi = U[:n], U[n:]
        D, J, Fo = s.divp(chi)
        Lp, Lop = s.lap_psi(psi, Fo)
        R1 = Lp - D
        R2 = chi - s.phiN - psi - s.lam2 * D
        I = sp.identity(n, format="csr")
        Jac = sp.bmat([[-J, Lop], [I - s.lam2 * J, -I]], format="lil")
        if s.iso:   # Neumann at both ends: psi has a free constant; one R1 row is redundant -> gauge psi(outer, 0) = 0
            kk = s.g.k(s.g.Nr - 1, 0); R1[kk] = psi[kk]
            Jac[kk, :] = 0; Jac[kk, n + kk] = 1.0
        return np.concatenate([R1, R2]), Jac.tocsc()

    def solve(s, U0=None, tol=1e-10, maxit=60):
        n = s.g.n
        U = np.concatenate([s.phiN.copy(), np.zeros(n)]) if U0 is None else U0.copy()
        fin = np.inf
        for it in range(maxit + 1):
            F, Jac = s.resid(U)
            sc = 1.0 / np.maximum(abs(Jac).max(axis=1).toarray().ravel(), 1e-300)
            fin = float(np.linalg.norm(sc * F, np.inf))
            if fin < tol or it == maxit: break
            dU = -spl.spsolve(sp.diags(sc) @ Jac, sc * F)
            al = 1.0
            for _ in range(30):
                Fn, _ = s.resid(U + al * dU)
                if np.all(np.isfinite(Fn)) and np.linalg.norm(sc * Fn, np.inf) < (1 - 1e-4 * al) * fin: break
                al *= 0.5
            U = U + al * dU
        s.U, s.res, s.it = U, fin, it
        return U, fin, it

    def field_monopole(s, U=None):
        """(r_face, total monopole radial field) at interior r faces."""
        g = s.g; U = s.U if U is None else U
        psi0 = g.monopole(U[g.n:])
        rf = g.re[1:-1]
        dpsi = np.diff(psi0) / np.diff(g.rc)
        return rf, plummer_gN(rf, s.y) + dpsi


# ------------------------------------------------------------------ Jeans
def jeans(rf, gr, Rlist, rmax=None):
    """isotropic Jeans, Plummer tracer (a = 1).  Returns sigma_p^2(R) for R in Rlist, global virial sigma^2, Wolf sigma^2."""
    lr = np.log(rf)
    r = np.geomspace(rf[0], rf[-1], 6000)
    g = np.interp(np.log(r), lr, gr)
    rho = (3 / (4 * np.pi)) * (1 + r * r) ** -2.5
    # rho sigma_r^2 (r) = int_r^inf rho g dr  (cumulative from outside, trapezoid in r)
    f = rho * g
    seg = 0.5 * (f[1:] + f[:-1]) * np.diff(r)
    P = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    out = []
    t = np.concatenate([[0.0], np.geomspace(1e-5, r[-1], 4000)])
    for R in Rlist:
        rr = np.sqrt(R * R + t * t)
        Pv = np.interp(rr, r, P, right=0.0)
        I = np.trapz(Pv, t) * 2.0
        Sig = (1 / np.pi) * (1 + R * R) ** -2
        out.append(I / Sig)
    vir = np.trapz(rho * r * g * 4 * np.pi * r * r, r) / 3.0
    r12 = 4.0 / 3.0
    wolf = r12 * float(np.interp(np.log(r12), lr, gr)) / 3.0
    return np.array(out), float(vir), float(wolf)


def jeans_lw_check(rf, gr):
    """luminosity-weighted sigma_p^2 over all R (should equal the virial value)."""
    R = np.geomspace(1e-3, 300, 500)
    s2, vir, _ = jeans(rf, gr, R)
    Sig = (1 / np.pi) * (1 + R * R) ** -2
    lw = np.trapz(s2 * Sig * 2 * np.pi * R * R, np.log(R)) / np.trapz(Sig * 2 * np.pi * R * R, np.log(R))
    return lw, vir


# ------------------------------------------------------------------ Route R1 (isolated 1D BVP)
def iso_1d(y, Lam, rin=1e-3, rout=1e3):
    """(Lam^2/2)(p'' + 2p'/r - 2p/r^2) = p^2/(1-p) - gN ;  p ~ r at 0 ; p^2/(1-p) = gN at rout.  Returns (r, g_total)."""
    l2 = 0.5 * Lam ** 2
    def fun2(x, Y):
        r = np.exp(x); p, q = Y
        gN = plummer_gN(r, y)
        r2pp = (p * p / (1 - p) - gN) * r * r / l2 - 2 * q + 2 * p
        return np.vstack([q, r2pp + q])
    def bc(Ya, Yb):
        pb = Yb[0]; gNb = plummer_gN(rout, y)
        return np.array([Ya[1] - Ya[0], pb * pb / (1 - pb) - gNb])
    x = np.linspace(math.log(rin), math.log(rout), 3000); r = np.exp(x)
    v0 = law_v(plummer_gN(r, y)); p0 = v0 / (1 + v0)
    Y0 = np.vstack([p0, np.gradient(p0, x)])
    sol = solve_bvp(fun2, bc, x, Y0, tol=1e-8, max_nodes=400000)
    xs = np.linspace(math.log(rin), math.log(rout), 20000); rs = np.exp(xs)
    p = sol.sol(xs)[0]
    return rs, plummer_gN(rs, y) + p, sol.status


# ------------------------------------------------------------------ Route F (linear about the background)
def routeF_monopole(y, xe, Lam, r, nc=64, nk=6000):
    """linear monopole radial field of psi + Newton at radius r (a = 1): (2y/pi) int k K1(k) chi0(k) j1(kr) dk + gN."""
    c, w = np.polynomial.legendre.leggauss(nc)
    mpar = 1 / (1 + xe) ** 2 if xe > 0 else 1.0; mper = 1 / (1 + xe) if xe > 0 else 1.0
    m = c * c * mpar + (1 - c * c) * mper
    k = np.geomspace(1e-6, 60.0, nk)
    kap = k * Lam
    ker = m[None, :] / (1 - m[None, :] + 0.5 * kap[:, None] ** 2 * m[None, :])
    chi0 = 0.5 * (ker * w[None, :]).sum(1)
    z = k * r
    j1 = np.where(z < 1e-3, z / 3 - z ** 3 / 30, np.sin(z) / z ** 2 - np.cos(z) / z)
    psi_r = (2 * y / np.pi) * np.trapz(k ** 3 * besk1(k) * chi0 * j1, np.log(k))
    newt = (2 * y / np.pi) * np.trapz(k ** 3 * besk1(k) * j1, np.log(k))
    return plummer_gN(r, y) + psi_r, newt
