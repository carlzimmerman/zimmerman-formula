"""D7d solvers for the stiffened DSF-21 action in a uniform Galactic field.

Static, weak-field, O(eps) equations (A33 (L) and (P), f = 1), with p = K P and Phi = ln N:
    (L)  lap Phi = K rho + div p            ->  grad Phi = g_N + Pi_L p
    (P)  grad Phi + (L*^2/2) lap p = a0 p / (a0 - |p|)      (vector Laplacian; gamma_F = gamma_L)
Dimensionless units in Route N: lengths in r_M = sqrt(GM/a0), accelerations in a0, Lam = L*/r_M.

Route F: linear response about p_e = u_e zhat, exact Fourier formula (valid for L* >> r_M).
Route N: nonlinear axisymmetric (ln r, theta) grid, Newton, unknowns psi (anomalous potential minus background)
         and w = v - v_e with v = h(p) = p/(1-|p|)  (so p = v/(1+|v|): no cap constraint).
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl
from numpy.polynomial import legendre as Lg

# ------------------------------------------------------------------ Route F
def chi(kap, c, xe):
    """k.A^-1.k for A = (kap^2/2) I + J - khat khat, J = diag(1+xe, 1+xe, (1+xe)^2) (axis = Galactic field)."""
    jp = 1 + xe; jl = (1 + xe) ** 2; a = kap ** 2 / 2 + jp; b = jl - jp
    s2 = 1 - c * c
    A11 = a + b * c * c - 1; A22 = a + b * s2; A12 = b * c * np.sqrt(s2)
    return A22 / (A11 * A22 - A12 ** 2)

def routeF_I2(xe, nk=4000, nc=64, kmin=1e-4, kmax=1e4):
    """I2 = int_0^inf kap^2 chi_2(kap) dkap, chi_2 the P2 projection; analytic tail -(8/3) b / kmax."""
    cg, cw = np.polynomial.legendre.leggauss(nc); P2 = 0.5 * (3 * cg ** 2 - 1)
    lk = np.linspace(np.log(kmin), np.log(kmax), nk); k = np.exp(lk)
    c2 = 2.5 * (chi(k[:, None], cg[None, :], xe) * P2 * cw).sum(1)
    b = (1 + xe) ** 2 - (1 + xe)
    return np.trapz(k ** 3 * c2, lk) - (8.0 / 3.0) * b / kmax

def routeF_Q2_raw(GM, L, xe, **kw):
    """Q2 in the Phi (ordinary potential) convention: 3 Phi_2 / r^2 = (2GM/5 pi L^3) I2."""
    return 2 * GM / (5 * np.pi * L ** 3) * routeF_I2(xe, **kw)

def routeF_radial(GM, L, xe, r, nc=48):
    """Monopole (orientation-averaged) anomalous radial acceleration at r: dPhi_0/dr = (2GM/pi L^2) int kap j1(kap rho) chi_0 dkap."""
    from scipy.integrate import quad
    rho = r / L
    cg, cw = np.polynomial.legendre.leggauss(nc)
    K = 400.0 / rho
    lk = np.linspace(np.log(1e-6), np.log(K), 200000); k = np.exp(lk)
    c0 = 0.5 * (chi(k[:, None], cg[None, :], xe) * cw).sum(1)
    z = k * rho
    j1 = np.where(z < 1e-3, z / 3 - z ** 3 / 30, np.sin(z) / z ** 2 - np.cos(z) / z)
    head = np.trapz(k * k * j1 * c0, lk)
    a = K * rho   # tail with chi_0 -> 2/kap^2: 2 int_a^inf j1(z)/z dz
    t1 = quad(lambda z: 1 / z ** 3, a, np.inf, weight="sin", wvar=1.0)[0]
    t2 = quad(lambda z: 1 / z ** 2, a, np.inf, weight="cos", wvar=1.0)[0]
    return 2 * GM / (np.pi * L ** 2) * (head + 2 * (t1 - t2))

# ------------------------------------------------------------------ Route N
class Grid:
    def __init__(s, rin, rout, nper, Nt):
        s.Nr = int(round(np.log10(rout / rin) * nper)) + 1
        s.x = np.linspace(np.log(rin), np.log(rout), s.Nr); s.dx = s.x[1] - s.x[0]; s.r = np.exp(s.x)
        s.Nt = Nt; dt = np.pi / Nt; s.th = (np.arange(Nt) + 0.5) * dt
        s.st = np.sin(s.th); s.ct = np.cos(s.th)
        sf = np.sin(np.arange(Nt + 1) * dt); sf[0] = 0; sf[-1] = 0
        T = np.zeros((Nt, Nt)); D = np.zeros((Nt, Nt)); C = np.zeros((Nt, Nt))
        for j in range(Nt):
            if j + 1 < Nt:
                T[j, j + 1] += sf[j + 1]; T[j, j] -= sf[j + 1]; D[j, j] += .5 * sf[j + 1]; D[j, j + 1] += .5 * sf[j + 1]
            if j - 1 >= 0:
                T[j, j - 1] += sf[j]; T[j, j] -= sf[j]; D[j, j] -= .5 * sf[j]; D[j, j - 1] -= .5 * sf[j]
            T[j] /= s.st[j] * dt ** 2; D[j] /= s.st[j] * dt
            C[j, min(j + 1, Nt - 1)] += 1 / (2 * dt); C[j, max(j - 1, 0)] -= 1 / (2 * dt)
        s.T, s.D, s.C = T, D, C   # theta-Laplacian (flux form), (1/s) d(s f)/dth, central d/dth (even parity)
        s.Bm = np.stack([Lg.legval(s.ct, np.eye(Nt)[l]) for l in range(Nt)], 1); s.Bi = np.linalg.inv(s.Bm)
        s.N = 3 * s.Nr * Nt
    def idx(s, f, i):
        return (f * s.Nr + i) * s.Nt + np.arange(s.Nt)

def build(g, Lam, isolated, mode, scalar_lap=False):
    """Linear part of the r^2-scaled equations. Unknown blocks: 0 psi, 1 q_r, 2 q_theta (q = p - p_e)."""
    Nr, Nt, dx, r = g.Nr, g.Nt, g.dx, g.r
    I = np.eye(Nt); l = np.arange(Nt)
    Mreg = g.Bm @ np.diag(l * 1.0) @ g.Bi; Mdec = g.Bm @ np.diag(-(l + 1.0)) @ g.Bi
    P0 = g.Bm @ np.diag((l == 0) * 1.0) @ g.Bi
    RR, CC, VV = [], [], []
    def blk(fr, ir, fc, ic, M):
        a, b = np.nonzero(M); RR.append(g.idx(fr, ir)[a]); CC.append(g.idx(fc, ic)[b]); VV.append(M[a, b])
    rhs = np.zeros(g.N); nlmask = np.zeros(Nr, bool)
    alg = (mode == "stiff" and Lam == 0.0); lam2 = 0.5 * Lam ** 2
    fwd = [(0, -1.5 / dx), (1, 2 / dx), (2, -.5 / dx)]; bwd = [(0, 1.5 / dx), (1, -2 / dx), (2, .5 / dx)]
    for i in range(Nr):
        ri = r[i]
        # psi row: r^2 lap psi - r^2 div q = 0
        if 0 < i < Nr - 1:
            blk(0, i, 0, i + 1, I * (1 / dx ** 2 + .5 / dx)); blk(0, i, 0, i - 1, I * (1 / dx ** 2 - .5 / dx))
            blk(0, i, 0, i, -2 / dx ** 2 * I + g.T)
            blk(0, i, 1, i + 1, -ri * I * .5 / dx); blk(0, i, 1, i - 1, ri * I * .5 / dx)
            blk(0, i, 1, i, -2 * ri * I); blk(0, i, 2, i, -ri * g.D)
        elif i == 0:   # monopole flux psi_x = r q_r ; l >= 1 regular (psi_x = l psi)
            for k, cf in fwd: blk(0, 0, 0, k, cf * I)
            blk(0, 0, 0, 0, -Mreg); blk(0, 0, 1, 0, -ri * P0)
        else:
            if isolated: blk(0, i, 0, i, I)
            else:          # decaying per mode
                for k, cf in bwd: blk(0, i, 0, i - k, cf * I)
                blk(0, i, 0, i, -Mdec)
        if mode == "qumond":
            blk(1, i, 1, i, I); blk(2, i, 2, i, I); continue
        pde = alg or (0 < i < Nr - 1)
        if pde:
            if not isolated:   # - r^2 grad psi
                dps = [(i - 1, -.5 / dx), (i + 1, .5 / dx)] if 0 < i < Nr - 1 else (
                    [(k, c) for k, c in fwd] if i == 0 else [(Nr - 1 - k, c) for k, c in bwd])
                for k, cf in dps: blk(1, i, 0, k, -ri * cf * I)
                blk(2, i, 0, i, -ri * g.C)
            if not alg:        # - (L^2/2) r^2 (vector lap q)
                for f in (1, 2):
                    blk(f, i, f, i + 1, -lam2 * I * (1 / dx ** 2 + .5 / dx)); blk(f, i, f, i - 1, -lam2 * I * (1 / dx ** 2 - .5 / dx))
                    blk(f, i, f, i, -lam2 * (-2 / dx ** 2 * I + g.T))
                if not scalar_lap:
                    blk(1, i, 1, i, 2 * lam2 * I); blk(1, i, 2, i, 2 * lam2 * g.D)
                    blk(2, i, 2, i, lam2 * np.diag(1 / g.st ** 2)); blk(2, i, 1, i, -2 * lam2 * g.C)
            rhs[g.idx(1, i)] = 1.0; nlmask[i] = True   # r^2 * GM/r^2 (Sun), radial
        elif i == 0:
            for f in (1, 2):
                for k, cf in fwd: blk(f, 0, f, k, cf * I)
        else:
            if isolated:
                for k, cf in bwd: blk(1, i, 1, i - k, cf * I)
                blk(1, i, 1, i, I); blk(2, i, 2, i, I)
            else:
                blk(1, i, 1, i, I); blk(2, i, 2, i, I)
    A = sp.csr_matrix((np.concatenate(VV), (np.concatenate(RR), np.concatenate(CC))), shape=(g.N, g.N))
    return A, rhs, nlmask

def solve_qumond(g, xe):
    """QUMOND mode (D7b's theory): lap psi = div[(nu-1) g_N - background], nu - 1 = (sqrt(1+4/y)-1)/2."""
    A, rhs, nl = build(g, 0.0, False, "qumond")
    Nr, Nt = g.Nr, g.Nt; n = Nr * Nt
    CT = np.broadcast_to(g.ct, (Nr, Nt)); ST = np.broadcast_to(g.st, (Nr, Nt)); R2 = (g.r ** 2)[:, None]
    gNe = xe ** 2 / (1 + xe)
    gr = gNe * CT + 1 / R2; gt = -gNe * ST; y = np.sqrt(gr ** 2 + gt ** 2)
    nm = lambda y: (np.sqrt(1 + 4 / y) - 1) / 2
    qr = nm(y) * gr - nm(gNe) * gNe * CT; qt = nm(y) * gt + nm(gNe) * gNe * ST
    b = np.zeros(g.N); b[n:2 * n] = qr.ravel(); b[2 * n:] = qt.ravel()
    return spl.spsolve(A.tocsc(), b).reshape(3, Nr, Nt)

def solve_isolated(g, Lam, scalar_lap=False, maxit=60):
    """Isolated (g_e = 0), spherical: Pi_L p = p exactly; h(p) - p = p|p|/(1-|p|) without cancellation."""
    A, rhs, nl = build(g, Lam, True, "stiff", scalar_lap)
    Nr, Nt = g.Nr, g.Nt; n = Nr * Nt; R2 = (g.r ** 2)[:, None]
    nlr = np.repeat(nl, Nt); U = np.zeros(g.N)
    def resid(U):
        qr = U[n:2 * n].reshape(Nr, Nt); qt = U[2 * n:].reshape(Nr, Nt)
        pm = np.sqrt(qr ** 2 + qt ** 2); om = 1 - pm; pmc = np.maximum(pm, 1e-300)
        F = A @ U - rhs
        F[n:2 * n] += np.where(nlr, (R2 * qr * pm / om).ravel(), 0); F[2 * n:] += np.where(nlr, (R2 * qt * pm / om).ravel(), 0)
        f2 = 1 / (pmc * om ** 2)
        J = (pm / om + qr * qr * f2, qr * qt * f2, qt * qr * f2, pm / om + qt * qt * f2)
        return F, J, pm
    ar = np.arange(n)[nlr]
    for it in range(maxit):
        F, J, pm = resid(U)
        rr = np.concatenate([ar + n, ar + n, ar + 2 * n, ar + 2 * n]); cc = np.concatenate([ar + n, ar + 2 * n, ar + n, ar + 2 * n])
        vv = np.concatenate([(R2 * Jk).ravel()[nlr] for Jk in J])
        Jac = (A + sp.csr_matrix((vv, (rr, cc)), shape=A.shape)).tocsr()
        sc = 1 / np.maximum(abs(Jac).max(axis=1).toarray().ravel(), 1e-300)
        f0 = np.linalg.norm(sc * F)
        if f0 < 1e-11: break
        dU = -spl.spsolve((sp.diags(sc) @ Jac).tocsc(), sc * F); alpha = 1.0
        for _ in range(40):
            Fn, _, pmn = resid(U + alpha * dU)
            if np.all(pmn < 1) and np.linalg.norm(sc * Fn) < (1 - 1e-4 * alpha) * f0: break
            alpha *= 0.5
        U = U + alpha * dU
    return U.reshape(3, Nr, Nt)

def dP(xe, CT, ST, wr, wt):
    """Delta p = p(v_e + w) - p(v_e), p(v) = v/(1+|v|), v_e = x_e zhat; and dp/dw (2x2 per node)."""
    ver, vet = xe * CT, -xe * ST
    vr, vt = ver + wr, vet + wt
    vm = np.sqrt(vr ** 2 + vt ** 2)
    dvm = (2 * (ver * wr + vet * wt) + wr ** 2 + wt ** 2) / (vm + xe)
    a = 1 / (1 + vm); ae = 1 / (1 + xe)
    dpr = wr * a - ver * dvm * a * ae; dpt = wt * a - vet * dvm * a * ae
    f2 = a * a / np.maximum(vm, 1e-300)
    return dpr, dpt, (a - vr * vr * f2, -vr * vt * f2, -vt * vr * f2, a - vt * vt * f2)

def solve_v(g, Lam, xe, scalar_lap=False, maxit=60, U0=None):
    """Route N in the Galactic field. Returns U (3,Nr,Nt) = (psi, w_r, w_theta), final scaled residual, iterations."""
    A, rhs, nl = build(g, Lam, False, "stiff", scalar_lap)
    Nr, Nt = g.Nr, g.Nt; n = Nr * Nt
    CT = np.broadcast_to(g.ct, (Nr, Nt)); ST = np.broadcast_to(g.st, (Nr, Nt)); R2 = (g.r ** 2)[:, None]
    A = A.tocsc(); Apsi = A[:, :n]; Aq = A[:, n:]
    nlr = np.repeat(nl, Nt).astype(float)
    Dw = sp.diags(np.concatenate([nlr * np.repeat(g.r ** 2, Nt)] * 2))
    Z = sp.csc_matrix((n, 2 * n))
    U = np.zeros(g.N) if U0 is None else U0.copy()
    def resid(U):
        wr = U[n:2 * n].reshape(Nr, Nt); wt = U[2 * n:].reshape(Nr, Nt)
        pr, pt, J = dP(xe, CT, ST, wr, wt)
        F = Apsi @ U[:n] + Aq @ np.concatenate([pr.ravel(), pt.ravel()]) + np.concatenate([np.zeros(n), Dw @ U[n:]]) - rhs
        return F, J
    fin = np.inf
    for it in range(maxit + 1):
        F, J = resid(U)
        if not np.all(np.isfinite(F)): fin = np.inf; break
        Jb = sp.bmat([[sp.diags(J[0].ravel()), sp.diags(J[1].ravel())], [sp.diags(J[2].ravel()), sp.diags(J[3].ravel())]])
        Jac = sp.hstack([Apsi, Aq @ Jb + sp.vstack([Z, Dw])]).tocsr()
        sc = 1 / np.maximum(abs(Jac).max(axis=1).toarray().ravel(), 1e-300)
        fin = np.linalg.norm(sc * F)
        if fin < 1e-11 or it == maxit: break
        dU = -spl.spsolve((sp.diags(sc) @ Jac).tocsc(), sc * F); alpha = 1.0
        for _ in range(40):
            Fn, _ = resid(U + alpha * dU)
            if np.all(np.isfinite(Fn)) and np.linalg.norm(sc * Fn) < (1 - 1e-4 * alpha) * fin: break
            alpha *= 0.5
        if alpha < 1e-9: break
        U = U + alpha * dU
    return U.reshape(3, Nr, Nt), fin, it

def regrid(Uold, gold, gnew):
    """Initial guess on a new grid: linear interpolation in ln r (zero beyond the old domain), then in theta."""
    Ux = np.zeros((3, gnew.Nr, gold.Nt))
    for f in range(3):
        for j in range(gold.Nt):
            Ux[f, :, j] = np.interp(gnew.x, gold.x, Uold[f, :, j], right=0.0)
    U = np.zeros((3, gnew.Nr, gnew.Nt))
    for f in range(3):
        for i in range(gnew.Nr):
            U[f, i] = np.interp(gnew.th, gold.th, Ux[f, i])
    return U.ravel()

def q2_raw(g, psi, rq, nl=7):
    """3 psi_2(rq)/rq^2 from a least-squares Legendre fit (l = 0..nl-1) per shell (Phi convention, dimensionless)."""
    coef = np.linalg.lstsq(g.Bm[:, :nl], psi.T, rcond=None)[0]
    return 3 * np.interp(np.log(rq), g.x, coef[2]) / rq ** 2
