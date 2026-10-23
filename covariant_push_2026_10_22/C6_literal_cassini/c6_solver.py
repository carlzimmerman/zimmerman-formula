"""C6 solvers: the C4-literal screened theory (gamma_F = 0) in a uniform Galactic field.

Static, weak-field, O(eps) equations (C4-literal Khronon + P, eta = 0), p = K P, Phi = ln N:
    (L)    lap Phi = K rho + div p
    (P_L)  grad Phi + (L*^2/2) grad div p = a0 p / (a0 - |p|)          (gamma_F = 0: grad-div, no curl stiffness)
General mixing r_F = gamma_F/gamma_L: stiffness = r_F * (vector Laplacian) + (1 - r_F) * (grad div).
r_F = 1 is D7d's equation (P) exactly.

D7d's machinery (Grid, dP, q2_raw, regrid, its build) is imported READ-ONLY from
doors_push_2026_10_22/D7d_screened_q2/d7d_solver.py. This module copies D7d's `build` row layout and adds
the grad-div block, written as the discrete gradient of the discrete divergence (so discrete-divergence-free
fields feel no stiffness: no spurious curl stiffness from the discretisation).
"""
import os, sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "doors_push_2026_10_22", "D7d_screened_q2"))
import d7d_solver as S   # read-only reuse

# ------------------------------------------------------------------ Route F (general r_F)
def chi_gen(kap, c, xe, rF):
    """khat.A^-1.khat, A = (kap^2/2)[rF (I - khat khat) + khat khat] + J - khat khat, J = diag(1+xe, 1+xe, (1+xe)^2).
    In-plane 2x2 (x = perp to the Galactic field, z = along it); khat = (s, c)."""
    kap = np.asarray(kap, float); c = np.asarray(c, float)
    s = np.sqrt(np.maximum(1 - c * c, 0.0))
    jp = 1 + xe; jl = (1 + xe) ** 2
    al = rF * kap ** 2 / 2; be = (1 - rF) * kap ** 2 / 2 - 1
    Axx = al + jp + be * s * s; Azz = al + jl + be * c * c; Axz = be * s * c
    det = Axx * Azz - Axz ** 2
    return (s * s * Azz + c * c * Axx - 2 * s * c * Axz) / det

def chi_stable(kap, c, xe, rF):
    """Kernel used by the Route F integrals: closed form at r_F = 0 (no large-kappa cancellation), D7d's chi at r_F = 1."""
    if rF == 0.0: return chi_C6_closed(kap, c, xe)
    if rF == 1.0: return S.chi(kap, c, xe)
    return chi_gen(kap, c, xe, rF)

def chi_C6_closed(kap, c, xe):
    """r_F = 0 closed form m/(1 - m + kap^2 m/2), m = khat.J^-1.khat."""
    m = (1 - c * c) / (1 + xe) + c * c / (1 + xe) ** 2
    return m / (1 - m + kap ** 2 * m / 2)

def tail_c2(xe, rF, nc=256):
    """P2 coefficient c2 of the 1/kap^4 term: chi = 2/kap^2 - 4 a(c)/kap^4 + ...; c2 = (5/2) int a P2 dc."""
    cg, cw = np.polynomial.legendre.leggauss(nc); P2 = 0.5 * (3 * cg ** 2 - 1)
    jp = 1 + xe; jl = (1 + xe) ** 2
    if rF == 1.0:
        a = jp + (jl - jp) * cg ** 2 - 1
    elif rF == 0.0:
        a = 1 / ((1 - cg ** 2) / jp + cg ** 2 / jl) - 1
    else:
        raise ValueError("tail only for rF in {0,1}")
    return 2.5 * (a * P2 * cw).sum()

def routeF_I2(xe, rF, nk=4000, nc=64, kmin=1e-4, kmax=1e4):
    cg, cw = np.polynomial.legendre.leggauss(nc); P2 = 0.5 * (3 * cg ** 2 - 1)
    lk = np.linspace(np.log(kmin), np.log(kmax), nk); k = np.exp(lk)
    c2 = 2.5 * (chi_stable(k[:, None], cg[None, :], xe, rF) * P2 * cw).sum(1)
    return np.trapz(k ** 3 * c2, lk) - 4.0 * tail_c2(xe, rF) / kmax

def routeF_Q2(GM, L, xe, rF, **kw):
    """BN11/Hees-sign Q2 (s^-2) = -(2GM/5 pi L^3) I2 (D7d's convention)."""
    return -2 * GM / (5 * np.pi * L ** 3) * routeF_I2(xe, rF, **kw)

def routeF_radial(GM, L, xe, r, rF, nc=48):
    """Monopole anomalous radial acceleration at r (D7d's formula with the general kernel; chi_0 -> 2/kap^2 tail)."""
    from scipy.integrate import quad
    rho = r / L
    cg, cw = np.polynomial.legendre.leggauss(nc)
    K = 400.0 / rho
    lk = np.linspace(np.log(1e-6), np.log(K), 200000); k = np.exp(lk)
    c0 = np.concatenate([0.5 * (chi_stable(kk[:, None], cg[None, :], xe, rF) * cw).sum(1) for kk in np.array_split(k, 20)])
    z = k * rho
    j1 = np.where(z < 1e-3, z / 3 - z ** 3 / 30, np.sin(z) / z ** 2 - np.cos(z) / z)
    head = np.trapz(k * k * j1 * c0, lk)
    a = K * rho
    t1 = quad(lambda z: 1 / z ** 3, a, np.inf, weight="sin", wvar=1.0)[0]
    t2 = quad(lambda z: 1 / z ** 2, a, np.inf, weight="cos", wvar=1.0)[0]
    return 2 * GM / (np.pi * L ** 2) * (head + 2 * (t1 - t2))

def dp_vector(kap, c, xe, rF):
    """delta p per unit g_N along khat (in-plane components perp/along khat): returns (longitudinal, transverse)."""
    s = np.sqrt(1 - c * c); jp = 1 + xe; jl = (1 + xe) ** 2
    al = rF * kap ** 2 / 2; be = (1 - rF) * kap ** 2 / 2 - 1
    A = np.array([[al + jp + be * s * s, be * s * c], [be * s * c, al + jl + be * c * c]])
    v = np.linalg.solve(A, np.array([s, c]))
    lon = v[0] * s + v[1] * c; tr = v[0] * c - v[1] * s
    return lon, tr

# ------------------------------------------------------------------ Route N
def graddiv_block(g, mutate=False):
    """r^2 grad div q in the r^2-scaled rows, as G @ Dv (2n x 2n), q = (q_r, q_theta) blocks.
    d = r div q = q_r,x + 2 q_r + Dth q_th (mutate: drop 2 q_r); r-row: d_x - d; theta-row: C d."""
    Nr, Nt, dx = g.Nr, g.Nt, g.dx; n = Nr * Nt
    It = sp.identity(Nt, format="csr")
    # d/dx on shells: central interior, 2nd-order one-sided at the ends
    Dx = sp.lil_matrix((Nr, Nr))
    for i in range(1, Nr - 1): Dx[i, i - 1] = -.5 / dx; Dx[i, i + 1] = .5 / dx
    Dx[0, 0], Dx[0, 1], Dx[0, 2] = -1.5 / dx, 2 / dx, -.5 / dx
    Dx[Nr - 1, Nr - 1], Dx[Nr - 1, Nr - 2], Dx[Nr - 1, Nr - 3] = 1.5 / dx, -2 / dx, .5 / dx
    Dx = sp.kron(Dx.tocsr(), It).tocsr()
    Ir = sp.identity(Nr, format="csr")
    Dth = sp.kron(Ir, sp.csr_matrix(g.D)); Cth = sp.kron(Ir, sp.csr_matrix(g.C))
    In = sp.identity(n, format="csr")
    Dv = sp.hstack([Dx + (0.0 if mutate else 2.0) * In, Dth]).tocsr()          # n x 2n
    G = sp.vstack([Dx - In, Cth]).tocsr()                                         # 2n x n
    return (G @ Dv).tocsr()

def build(g, Lam, rF, mutate=False):
    """D7d's `build` (isolated=False, mode='stiff', vector Laplacian scaled by rF) + (1 - rF) grad-div on interior rows."""
    Nr, Nt, dx, r = g.Nr, g.Nt, g.dx, g.r
    I = np.eye(Nt); l = np.arange(Nt)
    Mreg = g.Bm @ np.diag(l * 1.0) @ g.Bi; Mdec = g.Bm @ np.diag(-(l + 1.0)) @ g.Bi
    P0 = g.Bm @ np.diag((l == 0) * 1.0) @ g.Bi
    RR, CC, VV = [], [], []
    def blk(fr, ir, fc, ic, M):
        a, b = np.nonzero(M); RR.append(g.idx(fr, ir)[a]); CC.append(g.idx(fc, ic)[b]); VV.append(M[a, b])
    rhs = np.zeros(g.N); nlmask = np.zeros(Nr, bool)
    alg = (Lam == 0.0); lam2 = 0.5 * Lam ** 2; lamV = rF * lam2
    fwd = [(0, -1.5 / dx), (1, 2 / dx), (2, -.5 / dx)]; bwd = [(0, 1.5 / dx), (1, -2 / dx), (2, .5 / dx)]
    for i in range(Nr):
        ri = r[i]
        if 0 < i < Nr - 1:
            blk(0, i, 0, i + 1, I * (1 / dx ** 2 + .5 / dx)); blk(0, i, 0, i - 1, I * (1 / dx ** 2 - .5 / dx))
            blk(0, i, 0, i, -2 / dx ** 2 * I + g.T)
            blk(0, i, 1, i + 1, -ri * I * .5 / dx); blk(0, i, 1, i - 1, ri * I * .5 / dx)
            blk(0, i, 1, i, -2 * ri * I); blk(0, i, 2, i, -ri * g.D)
        elif i == 0:
            for k, cf in fwd: blk(0, 0, 0, k, cf * I)
            blk(0, 0, 0, 0, -Mreg); blk(0, 0, 1, 0, -ri * P0)
        else:
            for k, cf in bwd: blk(0, i, 0, i - k, cf * I)
            blk(0, i, 0, i, -Mdec)
        pde = alg or (0 < i < Nr - 1)
        if pde:
            dps = [(i - 1, -.5 / dx), (i + 1, .5 / dx)] if 0 < i < Nr - 1 else (
                [(k, c) for k, c in fwd] if i == 0 else [(Nr - 1 - k, c) for k, c in bwd])
            for k, cf in dps: blk(1, i, 0, k, -ri * cf * I)
            blk(2, i, 0, i, -ri * g.C)
            if not alg and lamV != 0.0:
                for f in (1, 2):
                    blk(f, i, f, i + 1, -lamV * I * (1 / dx ** 2 + .5 / dx)); blk(f, i, f, i - 1, -lamV * I * (1 / dx ** 2 - .5 / dx))
                    blk(f, i, f, i, -lamV * (-2 / dx ** 2 * I + g.T))
                blk(1, i, 1, i, 2 * lamV * I); blk(1, i, 2, i, 2 * lamV * g.D)
                blk(2, i, 2, i, lamV * np.diag(1 / g.st ** 2)); blk(2, i, 1, i, -2 * lamV * g.C)
            rhs[g.idx(1, i)] = 1.0; nlmask[i] = True
        elif i == 0:
            for f in (1, 2):
                for k, cf in fwd: blk(f, 0, f, k, cf * I)
        else:
            blk(1, i, 1, i, I); blk(2, i, 2, i, I)
    A = sp.csr_matrix((np.concatenate(VV), (np.concatenate(RR), np.concatenate(CC))), shape=(g.N, g.N))
    if not alg and rF != 1.0:
        n = Nr * Nt
        GD = graddiv_block(g, mutate)
        inner = np.zeros(Nr); inner[1:Nr - 1] = 1.0
        mask = sp.diags(np.concatenate([np.repeat(inner, Nt)] * 2))
        E = -(1.0 - rF) * lam2 * (mask @ GD)
        A = (A + sp.vstack([sp.csr_matrix((n, g.N)), sp.hstack([sp.csr_matrix((2 * n, n)), E])])).tocsr()
    return A, rhs, nlmask

def interleave(g):
    """Permutation to shell-interleaved ordering (block-banded LU, lower memory); new position k holds old index perm[k]."""
    f = np.arange(3)[:, None, None]; i = np.arange(g.Nr)[None, :, None]; j = np.arange(g.Nt)[None, None, :]
    old = (f * g.Nr + i) * g.Nt + j; new = (i * 3 + f) * g.Nt + j
    perm = np.empty(g.N, int); perm[new.ravel()] = old.ravel()
    return perm

def solve_v(g, Lam, xe, rF, maxit=60, U0=None, mutate=False, tol=1e-11):
    """Route N in the Galactic field (D7d's Newton loop with this lane's build)."""
    A, rhs, nl = build(g, Lam, rF, mutate)
    Nr, Nt = g.Nr, g.Nt; n = Nr * Nt
    CT = np.broadcast_to(g.ct, (Nr, Nt)); ST = np.broadcast_to(g.st, (Nr, Nt))
    A = A.tocsc(); Apsi = A[:, :n]; Aq = A[:, n:]
    nlr = np.repeat(nl, Nt).astype(float)
    Dw = sp.diags(np.concatenate([nlr * np.repeat(g.r ** 2, Nt)] * 2))
    Z = sp.csc_matrix((n, 2 * n))
    perm = interleave(g)
    U = np.zeros(g.N) if U0 is None else U0.copy()
    def resid(U):
        wr = U[n:2 * n].reshape(Nr, Nt); wt = U[2 * n:].reshape(Nr, Nt)
        pr, pt, J = S.dP(xe, CT, ST, wr, wt)
        F = Apsi @ U[:n] + Aq @ np.concatenate([pr.ravel(), pt.ravel()]) + np.concatenate([np.zeros(n), Dw @ U[n:]]) - rhs
        return F, J
    fin = np.inf; it = 0
    for it in range(maxit + 1):
        F, J = resid(U)
        if not np.all(np.isfinite(F)): fin = np.inf; break
        Jb = sp.bmat([[sp.diags(J[0].ravel()), sp.diags(J[1].ravel())], [sp.diags(J[2].ravel()), sp.diags(J[3].ravel())]])
        Jac = sp.hstack([Apsi, Aq @ Jb + sp.vstack([Z, Dw])]).tocsr()
        sc = 1 / np.maximum(abs(Jac).max(axis=1).toarray().ravel(), 1e-300)
        fin = np.linalg.norm(sc * F)
        if fin < tol or it == maxit: break
        Jp = (sp.diags(sc) @ Jac).tocsr()[perm][:, perm].tocsc()
        dU = np.empty(g.N); dU[perm] = -spl.splu(Jp, permc_spec="NATURAL").solve((sc * F)[perm]); del Jp
        alpha = 1.0
        for _ in range(40):
            Fn, _ = resid(U + alpha * dU)
            if np.all(np.isfinite(Fn)) and np.linalg.norm(sc * Fn) < (1 - 1e-4 * alpha) * fin: break
            alpha *= 0.5
        if alpha < 1e-9: break
        U = U + alpha * dU
    return U.reshape(3, Nr, Nt), fin, it
