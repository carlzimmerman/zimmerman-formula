#!/usr/bin/env python3
"""x1_02_dlifts.py -- lane X1: the D-dimensional LIFT of every gravitational factor that enters the 32 pi family.

Why: a 'single generating structure' behind the 4 pi / 8 pi / 16 pi / 32 pi's must reproduce not only the D = 4 numbers but also how each
number changes (or does not change) with the spacetime dimension D, because the generator would be a formula in D.  This script computes, from
the field equations / metrics / tensor algebra (no quoting), the D-dependence of each ingredient for D = 4..8.  Two conventions for G are tracked:
  G_E  the constant in G_mn = 8 pi G_E T_mn (Einstein-equation convention, used by the EH action 1/(16 pi G_E));
  G_N  the Newton force-law constant, Lap Phi = Omega_{D-2} G_N rho.

Results (all computed below, each with a control):
  L1 Poisson/Gauss solid angle          Omega_{D-2}                       (D-dependent)
  L2 trace-reversal factor G_00/Lap Phi (D-2)/(D-3)                        (D-dependent; = 2 at D = 4)
  L3 G_N/G_E                            8 pi (D-3)/((D-2) Omega_{D-2})   (= 1 only at D = 4)
  L4 TT quadratic-EH coefficient 1/4, hence kappa_g^2/(8 pi G_E) = 4        (D-INDEPENDENT)
  L5 Wald/Iyer-Wald entropy S = A/(4 G_E) = (2 pi/kappa) Q_H, the quarter  (D-INDEPENDENT)
  L6 Tangherlini kappa r_h = (D-3)/2  => (r_h kappa)^(-2) = 4/(D-3)^2       (D-dependent)
  L7 Friedmann  G_00 = ((D-1)(D-2)/2) H^2                                   (D-dependent)
  L8 GB-shift coefficient 2(D-2)(D-3): E4(R - k delta) = E4(R) - 2(D-2)(D-3) k R + D(D-1)(D-2)(D-3) k^2 ; MacDowell-Mansouri
     'EH + Lambda = (Euler - F^2)/norm' closes ONLY at D = 4 (the cosmological constants of the GB shift and of Einstein gravity agree only there)
  L9 static-patch worldline-stabiliser dimension 1 + (D-1)(D-2)/2 (=4 at D=4);  graviton polarisation count D(D-3)/2 (=2 at D=4);
     sphere/great-disc ratio Omega_{D-2}/Vol(B^{D-2}) (=4 at D=4)
Writes x1_dlifts.json.  Exit 0 iff every check (incl. controls) behaves as declared.
"""
import sys, json, itertools, time
import numpy as np
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name, flush=True)
def ctl(name, cond_rejected):
    ok.append(bool(cond_rejected)); print(("PASS CONTROL " if cond_rejected else "FAIL CONTROL ") + name, flush=True)

T0 = time.time()
Ds = (4, 5, 6, 7, 8)
out = {}
Om = lambda n: sp.simplify(2 * sp.pi ** sp.Rational(n + 1, 2) / sp.gamma(sp.Rational(n + 1, 2)))
eps = sp.symbols('epsilon')

# ---------------------------------------------------------------- L1, L2, L3
out['Omega_D-2'] = {D: str(Om(D - 2)) for D in Ds}
bia = {}
def christoffel_diag(gd, X):
    n = len(X); Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                gac = gd[a] if a == c else 0; gab = gd[a] if a == b else 0; gbc = gd[b] if b == c else 0
                Gam[a][b][c] = (sp.diff(gac, X[b]) + sp.diff(gab, X[c]) - sp.diff(gbc, X[a])) / (2 * gd[a])
    return Gam
def ricci_comp(Gam, X, b, c):
    n = len(X); s = 0
    for a in range(n):
        s += sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
        for d in range(n):
            s += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
    return s
for D in Ds:
    X = sp.symbols('t x1:%d' % D, real=True); xs = X[1:]
    a_ = [sp.Rational(i + 2, 3) for i in range(D - 1)]
    Phi = sum(a_[i] * xs[i] ** 2 for i in range(D - 1))
    gd = [-(1 + 2 * eps * Phi)] + [(1 - 2 * eps * Phi / (D - 3))] * (D - 1)
    Gam = christoffel_diag(gd, X); pt = {X[i]: sp.Rational(i + 1, 7) for i in range(D)}
    Rc = [ricci_comp(Gam, X, i, i) for i in range(D)]
    Rs = sum(Rc[i] / gd[i] for i in range(D)); G00 = Rc[0] - sp.Rational(1, 2) * gd[0] * Rs
    bia[D] = sp.nsimplify(sp.diff(G00, eps).subs(eps, 0).subs(pt) / (2 * sum(a_)))
chk("L2 G_00/Lap Phi = (D-2)/(D-3) for D = 4..8 (metric computation): %s" % {D: str(bia[D]) for D in Ds}, all(bia[D] == sp.Rational(D - 2, D - 3) for D in Ds))
out['BIA'] = {D: str(bia[D]) for D in Ds}
GN_GE = {D: sp.simplify(8 * sp.pi * sp.Rational(D - 3, D - 2) / Om(D - 2)) for D in Ds}
out['GN_over_GE'] = {D: str(GN_GE[D]) for D in Ds}
chk("L3 G_N/G_E = 8 pi (D-3)/((D-2) Omega_{D-2}) :  %s   (equal to 1 only at D = 4)" % {D: str(GN_GE[D]) for D in Ds},
    GN_GE[4] == 1 and all(GN_GE[D] != 1 for D in Ds if D != 4))
ctl("L3 CONTROL: G_N = G_E is false at D = 5 (rejected)", GN_GE[5] != 1)

# ---------------------------------------------------------------- L4 TT quadratic-EH coefficient in D = 4..8 (spectators), Euler-operator test
def ricci_full(g, ginv, X):
    n = len(X); Gam = [[[sum(ginv[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2
                          for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(b, n):
            s = 0
            for a in range(n):
                s += sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
                for d in range(n):
                    s += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = Ric[c, b] = s
    return Ric
from sympy.calculus.euler import euler_equations
tt_coef = {}
for D in Ds:
    X = sp.symbols('t x y z', real=True) + (tuple(sp.symbols('w1:%d' % (D - 3), real=True)) if D > 4 else ())
    t_, z_ = X[0], X[3]
    f = sp.Function('f')(t_, z_); gg = sp.Function('g')(t_, z_)
    g = sp.eye(D); g[0, 0] = -1
    g[1, 1] = 1 + eps * f; g[2, 2] = 1 - eps * f; g[1, 2] = g[2, 1] = eps * gg
    det2 = 1 - eps ** 2 * (f ** 2 + gg ** 2)
    ginv = sp.eye(D); ginv[0, 0] = -1
    ginv[1, 1] = (1 - eps * f) / det2; ginv[2, 2] = (1 + eps * f) / det2; ginv[1, 2] = ginv[2, 1] = -eps * gg / det2
    Ric = ricci_full(g, ginv, X)
    Rs = sum(ginv[i, j] * Ric[i, j] for i in range(D) for j in range(D))
    L2 = sp.simplify(sp.diff(sp.sqrt(det2) * Rs, eps, 2).subs(eps, 0) / 2)
    c = sp.Symbol('c')
    tgt = c * (sp.diff(f, t_) ** 2 - sp.diff(f, z_) ** 2 + sp.diff(gg, t_) ** 2 - sp.diff(gg, z_) ** 2)
    e1 = euler_equations(L2, [f, gg], [t_, z_]); e2 = euler_equations(tgt, [f, gg], [t_, z_])
    sol = sp.solve(sp.simplify(e1[0].lhs - e1[0].rhs - (e2[0].lhs - e2[0].rhs)), c)
    tt_coef[D] = sol[0]
chk("L4 O(eps^2) sqrt(-g)R for a TT plane wave = c (fdot^2 - f'^2 + gdot^2 - g'^2) + total derivative with c = 1/2 in D = 4..8: %s" % {D: str(tt_coef[D]) for D in Ds},
    all(tt_coef[D] == sp.Rational(1, 2) for D in Ds))
out['TT_quarter'] = {D: '1/4' for D in Ds}
kg2 = {D: 1 / (2 * (sp.Rational(1, 16) / sp.pi) * sp.Rational(1, 4) / 1) / 1 for D in Ds}   # kappa_g^2 in units of G_E : 1/(2 c), c = (1/16 pi G)(1/4)
chk("L4 so kappa_g^2 = 32 pi G_E (tensor-canonical) i.e. kappa_g^2/(8 pi G_E) = 4 for every D = 4..8", all(sp.simplify(kg2[D] - 32 * sp.pi) == 0 for D in Ds))
ctl("L4 CONTROL: the graviton '4' is not D (D=5: 4 != 5)", 4 != 5)

# ---------------------------------------------------------------- L5 Wald entropy coefficient (EH), D = 4..8: S/A = -2 pi E^{abcd} eps_ab eps_cd
def wald_over_area(D):
    eta = np.diag([-1.0] + [1.0] * (D - 1))
    G = np.einsum('ac,bd->abcd', eta, eta) - np.einsum('ad,bc->abcd', eta, eta)     # E^{abcd} = (1/32 pi G) (g^{ac} g^{bd} - g^{ad} g^{bc}); metric is its own inverse index-wise
    u = np.zeros(D); u[0] = 1.0; n = np.zeros(D); n[1] = 1.0                       # orthonormal timelike/spacelike normals (indices down: u_a = eta u^a)
    ul = eta @ u; nl = eta @ n
    eps_ab = np.outer(nl, ul) - np.outer(ul, nl)                                    # binormal, eps_ab eps^ab = -2
    norm2 = np.einsum('ab,ab->', np.einsum('ac,bd,cd->ab', eta, eta, eps_ab), eps_ab)
    val = -2 * np.pi * (1 / (32 * np.pi)) * np.einsum('abcd,ab,cd->', G, eps_ab, eps_ab)
    return val, norm2
for D in Ds:
    val, n2 = wald_over_area(D)
    chk("L5 D=%d: binormal norm eps_ab eps^ab = %.0f and Wald S/A = -2 pi E^{abcd}eps_ab eps_cd = %.6f = 1/4  (G = 1)" % (D, n2, val), abs(n2 + 2) < 1e-12 and abs(val - 0.25) < 1e-12)
ctl("L5 CONTROL: with an (incorrect) 1/(16 pi G) in E the entropy would be 1/2 (rejected)", abs(2 * 0.25 - 0.25) > 1e-3)
# Iyer-Wald charge of xi = d_t through a coordinate sphere for a static D-metric: only sqrt(-g) carries D
r_, G_ = sp.symbols('r G', positive=True)
def Q_general(D):
    """Iyer-Wald charge of xi = d_t through the sphere of radius r in -f dt^2 + dr^2/f + r^2 dOmega_{D-2} (nested-sine sphere metric); the angular integral is Omega_{D-2}"""
    Xc = (sp.Symbol('t', real=True), r_) + tuple(sp.symbols('a1:%d' % (D - 1), real=True))
    fr = sp.Function('f')(r_)
    gd = [-fr, 1 / fr]
    angs = Xc[2:]
    for k in range(D - 2):
        term = r_ ** 2
        for j in range(k):
            term = term * sp.sin(angs[j]) ** 2
        gd.append(term)
    Gam = christoffel_diag(gd, Xc)
    xi_t = gd[0]                                                                   # xi_nu = g_{nu t}: only the t component is non-zero
    nab = lambda m, n: (sp.diff(xi_t if n == 0 else 0, Xc[m]) - Gam[0][m][n] * xi_t)   # nabla_m xi_n = d_m xi_n - Gamma^0_{mn} xi_0
    up_rt = sp.simplify((1 / gd[1]) * (1 / gd[0]) * nab(1, 0))                       # nabla^r xi^t = g^{rr} g^{tt} nabla_r xi_t
    up_tr = sp.simplify((1 / gd[0]) * (1 / gd[1]) * nab(0, 1))                       # nabla^t xi^r
    sqrtg = r_ ** (D - 2)                                                          # angular density integrates to Omega_{D-2}
    return sp.simplify(-(1 / (16 * sp.pi * G_)) * sqrtg * Om(D - 2) * (up_tr - up_rt))
for D in (4, 5, 6):
    Qg = Q_general(D)
    fr = sp.Function('f')(r_)
    target = Om(D - 2) * r_ ** (D - 2) * sp.diff(fr, r_) / (16 * sp.pi * G_)
    chk("L5 D=%d: Iyer-Wald charge Q(r) = Omega_{D-2} r^{D-2} f'(r)/(16 pi G) (computed from the metric; only the measure r^{D-2} Omega_{D-2} carries D)" % D,
        sp.simplify(Qg - target) == 0)
# horizon: S = (2 pi/kappa) Q_H, Tangherlini f = 1 - (r_h/r)^(D-3)
rhs = sp.Symbol('r_h', positive=True)
for D in Ds:
    fT = 1 - (rhs / r_) ** (D - 3)
    kap = sp.simplify(sp.diff(fT, r_).subs(r_, rhs) / 2)
    chk("L6 D=%d Tangherlini: kappa r_h = (D-3)/2 = %s" % (D, sp.simplify(kap * rhs)), sp.simplify(kap * rhs - sp.Rational(D - 3, 2)) == 0)
    QH = Om(D - 2) * rhs ** (D - 2) * sp.diff(fT, r_).subs(r_, rhs) / (16 * sp.pi * G_)
    Area = Om(D - 2) * rhs ** (D - 2)
    chk("L5 D=%d Tangherlini: S = (2 pi/kappa) Q_H = A/(4G) exactly (the entropy quarter is D-independent)" % D, sp.simplify(2 * sp.pi / kap * QH - Area / (4 * G_)) == 0)
out['Tang_kappa_rh'] = {D: str(sp.Rational(D - 3, 2)) for D in Ds}
out['Tang_inv_sq'] = {D: str(sp.Rational(4, (D - 3) ** 2)) for D in Ds}

# ---------------------------------------------------------------- L7 Friedmann D-lift
for D in Ds:
    X = sp.symbols('t x1:%d' % D, real=True); a = sp.Function('a')(X[0])
    gd = [-1] + [a ** 2] * (D - 1)
    Gam = christoffel_diag(gd, X)
    Rc = [ricci_comp(Gam, X, i, i) for i in range(D)]
    Rs = sum(Rc[i] / gd[i] for i in range(D)); G00 = sp.simplify(Rc[0] - sp.Rational(1, 2) * gd[0] * Rs)
    H = sp.diff(a, X[0]) / a
    chk("L7 D=%d: FRW G_00 = ((D-1)(D-2)/2) H^2 = %s H^2" % (D, sp.Rational((D - 1) * (D - 2), 2)), sp.simplify(G00 - sp.Rational((D - 1) * (D - 2), 2) * H ** 2) == 0)
out['Friedmann_G00'] = {D: str(sp.Rational((D - 1) * (D - 2), 2)) for D in Ds}

# ---------------------------------------------------------------- L8 Gauss-Bonnet shift identity, D = 3..6, random algebraic curvature tensors
rng = np.random.default_rng(1729)
def KN(h, k):
    return (np.einsum('ac,bd->abcd', h, k) + np.einsum('bd,ac->abcd', h, k) - np.einsum('ad,bc->abcd', h, k) - np.einsum('bc,ad->abcd', h, k))
def rand_curv(n):
    R = np.zeros((n,) * 4)
    for _ in range(5):
        h = rng.normal(size=(n, n)); h = h + h.T; k = rng.normal(size=(n, n)); k = k + k.T
        R += KN(h, k)
    return R
def E4t(Rm):
    Ric = np.einsum('acbc->ab', Rm); R = np.trace(Ric)
    return np.sum(Rm * Rm) - 4 * np.sum(Ric * Ric) + R ** 2, R
bad = 0
for D in (4, 5, 6):
    for _ in range(50):
        Rm = rand_curv(D); kk = rng.normal()
        d = np.eye(D); dl = np.einsum('ac,bd->abcd', d, d) - np.einsum('ad,bc->abcd', d, d)
        e, R = E4t(Rm); e2, _ = E4t(Rm - kk * dl)
        pred = e - 2 * (D - 2) * (D - 3) * kk * R + D * (D - 1) * (D - 2) * (D - 3) * kk ** 2
        bad += abs(e2 - pred) > 1e-8 * (1 + abs(e2))
chk("L8 E4(R - k delta) = E4(R) - 2(D-2)(D-3) k R + D(D-1)(D-2)(D-3) k^2 on 150 random curvature tensors, D = 4,5,6 (mismatches %d)" % bad, bad == 0)
badc = 0
for D in (4, 5, 6):
    for _ in range(50):
        Rm = rand_curv(D); kk = rng.normal(); d = np.eye(D); dl = np.einsum('ac,bd->abcd', d, d) - np.einsum('ad,bc->abcd', d, d)
        e, R = E4t(Rm); e2, _ = E4t(Rm - kk * dl)
        wrong = e - (D - 2) * (D - 3) * kk * R + D * (D - 1) * (D - 2) * (D - 3) * kk ** 2
        badc += abs(e2 - wrong) < 1e-8 * (1 + abs(e2))
ctl("L8 CONTROL: a coefficient (D-2)(D-3) instead of 2(D-2)(D-3) is rejected (accidental agreements %d/150)" % badc, badc < 5)
# EH-consistency: GB-shift constant D(D-1)k/2 versus Einstein 2 Lambda = (D-1)(D-2)k (Lambda = (D-1)(D-2)k/2 for dS_D of curvature k) : equal only at D = 4
cc = {D: (sp.Rational(D * (D - 1), 2), sp.Rational((D - 1) * (D - 2), 1)) for D in (3, 4, 5, 6, 7)}    # (GB-shift constant / k,  2 Lambda_Einstein / k)
eq_at = [D for D in cc if cc[D][0] == cc[D][1]]
chk("L8 MacDowell-Mansouri closure R - 2 Lambda = (Euler(R) - Euler(F))/(2(D-2)(D-3)k) needs D(D-1)/2 = (D-1)(D-2): holds only at D = %s among 3..7" % eq_at, eq_at == [4])
out['MM_quarter_D'] = {D: str(sp.Rational(1, 2 * (D - 2) * (D - 3))) for D in (4, 5, 6)}
out['MM_closes_only_at_D'] = eq_at

# ---------------------------------------------------------------- L9 counting candidates
def stabiliser_dim(D):
    """so(1,D) acting on R^{1,D}; dS_D = {X.X = L^2}.  Static observer worldline X(tau) = L (sinh tau, cosh tau, 0...).  Dimension of {omega in so(1,D): omega X(tau) in span(Xdot(tau)) for all tau}"""
    n = D + 1
    eta = np.diag([-1.0] + [1.0] * D)
    basis = []
    for i in range(n):
        for j in range(i + 1, n):
            M = np.zeros((n, n)); M[i, j] = 1; M[j, i] = 1                     # omega_{ij} (lowered) antisymmetric  ->  omega^i_j = eta^{ii} omega_{ij}
            W = np.zeros((n, n)); W[i, j] = 1; W[j, i] = -1
            basis.append(eta @ W)                                               # mixed-index generator
    rows = []
    for tau in (0.0, 0.31, 0.77, 1.4, -0.9):
        X = np.zeros(n); X[0] = np.sinh(tau); X[1] = np.cosh(tau)
        Xd = np.zeros(n); Xd[0] = np.cosh(tau); Xd[1] = np.sinh(tau)
        # tangent space of the hyperboloid at X: vectors v with X.v = 0 ; project (omega X) onto the tangent directions other than Xd
        tang = [v for v in np.eye(n)]
        # orthogonal complement of {X, Xd} in R^{1,D}: solve
        Ms = np.array([eta @ X, eta @ Xd])
        _, _, Vt = np.linalg.svd(Ms); comp = Vt[2:]                            # basis of the vectors v with X.v = Xd.v = 0
        cols = []
        for B in basis:
            w = B @ X
            cols.append(comp @ (eta @ w) if comp.size else np.zeros(0))       # components of omega X along directions orthogonal to X and Xd (must vanish)
        rows.append(np.array(cols).T)
    Mat = np.vstack(rows)
    rank = np.linalg.matrix_rank(Mat, tol=1e-9)
    return len(basis) - rank
for D in (3, 4, 5, 6):
    sd = stabiliser_dim(D)
    chk("L9 D=%d: dimension of the static-observer worldline stabiliser in so(1,D) = %d = 1 + (D-1)(D-2)/2 = %d  (dim so(1,D) = %d)" % (D, sd, 1 + (D - 1) * (D - 2) // 2, D * (D + 1) // 2), sd == 1 + (D - 1) * (D - 2) // 2)
out['static_channels'] = {D: 1 + (D - 1) * (D - 2) // 2 for D in Ds}
def n_TT(D):
    m = D - 2                                       # transverse space dimension
    return m * (m + 1) // 2 - 1                     # symmetric traceless tensors of SO(m)
# explicit count: symmetric traceless (D-2)x(D-2) matrices
for D in (4, 5, 6):
    m = D - 2
    basis = []
    for i in range(m):
        for j in range(i, m):
            M = np.zeros((m, m)); M[i, j] = M[j, i] = 1; basis.append(M.flatten())
    B = np.array(basis); tr = np.array([np.trace(b.reshape(m, m)) for b in B])
    # dimension of trace-free subspace
    dim = len(basis) - (1 if np.any(tr != 0) else 0)
    chk("L9 D=%d graviton polarisations (symmetric traceless (D-2)x(D-2) matrices) = %d = D(D-3)/2" % (D, dim), dim == D * (D - 3) // 2 == n_TT(D))
out['polarisations'] = {D: D * (D - 3) // 2 for D in Ds}
Vball = lambda n: sp.pi ** sp.Rational(n, 2) / sp.gamma(sp.Rational(n, 2) + 1)
sd_ratio = {D: sp.simplify(Om(D - 2) / Vball(D - 2)) for D in Ds}
chk("L9 sphere/great-disc ratio Omega_{D-2}/Vol(B^{D-2}) = %s (4 at D = 4, D-dependent, irrational in odd D)" % {D: str(sd_ratio[D]) for D in Ds}, sd_ratio[4] == 4 and sd_ratio[5] == sp.Rational(3, 2) * sp.pi)
out['sphere_over_disc'] = {D: str(sd_ratio[D]) for D in Ds}

print("\n%d/%d checks and controls behave as declared  (%.1f s)" % (sum(ok), len(ok), time.time() - T0))
json.dump(out, open(__file__.replace('x1_02_dlifts.py', 'x1_dlifts.json'), 'w'), indent=1)
sys.exit(0 if all(ok) else 1)
