# -*- coding: utf-8 -*-
r"""
cfg292_lib -- symbolic machinery for CFG292 (principal symbols of GR + khronon / Einstein-aether on a frozen background).

Every quantity is built in JET variables on a constant background (gbar, d taubar):
    dH[l][m][n] = d_l h_mn,   ddP[l][s] = d_l d_s pi,   dU[l][m] = d_l du^m   (constant-coefficient linear objects).
A linear expression in the undifferentiated perturbations (h_mn, d_s pi, du^m) is differentiated by substitution
(h_mn -> dH[l][m][n], d_s pi -> ddP[l][s], du^m -> dU[l][m]), which is exact for constant coefficients.
The principal symbol is the Hessian of the quadratic Lagrangian after d_l h -> xi_l H, d_l d_s pi -> xi_l xi_s Pi,
d_l du -> xi_l U.  (A real field redefinition of Pi absorbs the factors of i; null Lagrangians give zero symbol.)
"""
import itertools
import sympy as sp

R4 = range(4)
PAIRS = [(m, n) for m in R4 for n in R4 if m <= n]
NAMES_H = [f"H{m}{n}" for (m, n) in PAIRS]

# undifferentiated perturbation symbols
hS = [[None] * 4 for _ in R4]
for (m, n) in PAIRS:
    hS[m][n] = hS[n][m] = sp.Symbol(f"h{m}{n}")
dpS = [sp.Symbol(f"dp{s}") for s in R4]                  # d_s pi
duS = [sp.Symbol(f"du{m}") for m in R4]                  # du^m (aether control)
# jets
dH = [[[None] * 4 for _ in R4] for _ in R4]
for l in R4:
    for (m, n) in PAIRS:
        dH[l][m][n] = dH[l][n][m] = sp.Symbol(f"dh{l}_{m}{n}")
ddP = [[None] * 4 for _ in R4]
for l in R4:
    for s in R4:
        if l <= s:
            ddP[l][s] = ddP[s][l] = sp.Symbol(f"ddp{l}{s}")
dU = [[sp.Symbol(f"du{l}_{m}") for m in R4] for l in R4]

# Fourier amplitudes
XI = sp.symbols("xi0:4", real=True)
HV = [[None] * 4 for _ in R4]
for (m, n) in PAIRS:
    HV[m][n] = HV[n][m] = sp.Symbol(f"H{m}{n}")
PIV = sp.Symbol("Pi")
UV = [sp.Symbol(f"U{m}") for m in R4]


def D(l, expr):
    """d_l of a constant-coefficient linear expression in (h, d pi, du)."""
    sub = {}
    for (m, n) in PAIRS:
        sub[hS[m][n]] = dH[l][m][n]
    for s in R4:
        sub[dpS[s]] = ddP[l][s]
    for m in R4:
        sub[duS[m]] = dU[l][m]
    return sp.expand(expr.xreplace(sub))


def gamma1(ginv):
    """Gamma^(1) a_{mn} = 1/2 g^{ab}(d_m h_bn + d_n h_bm - d_b h_mn), linear in jets."""
    G = [[[None] * 4 for _ in R4] for _ in R4]
    for a in R4:
        for m in R4:
            for n in R4:
                if n < m:
                    G[a][m][n] = G[a][n][m]
                    continue
                G[a][m][n] = sp.expand(sum(ginv[a, b] * (dH[m][b][n] + dH[n][b][m] - dH[b][m][n]) for b in R4) / 2)
    return G


def L_EH(gbar):
    """quadratic part of sqrt(-g) R in Gamma-Gamma form (differs from it by a total derivative)."""
    ginv = gbar.inv()
    sq = sp.sqrt(-gbar.det())
    G = gamma1(ginv)
    tr = [sp.expand(sum(G[b][a][b] for b in R4)) for a in R4]          # Gamma^b_{ab}
    L = 0
    for m in R4:
        for n in R4:
            if ginv[m, n] == 0:
                continue
            t1 = sum(G[a][b][m] * G[b][a][n] for a in R4 for b in R4)
            t2 = sum(G[a][m][n] * tr[a] for a in R4)
            L += ginv[m, n] * (t1 - t2)
    return sp.expand(sq * L)


def deDonder(gbar, spatial_trace=False):
    """C_nu = g^{ab}(d_a h_{b nu} - 1/2 d_nu h_ab); spatial_trace replaces the 4-D trace by gamma^{jk} h_jk."""
    ginv = gbar.inv()
    gam_inv = gbar[1:, 1:].inv()
    C = []
    for nu in R4:
        c = sum(ginv[a, b] * dH[a][b][nu] for a in R4 for b in R4)
        if spatial_trace:
            c -= sum(gam_inv[j - 1, k - 1] * dH[nu][j][k] for j in (1, 2, 3) for k in (1, 2, 3)) / 2
        else:
            c -= sum(ginv[a, b] * dH[nu][a][b] for a in R4 for b in R4) / 2
        C.append(sp.expand(c))
    return C


def L_gf(gbar, cgf, mode="full"):
    """-cgf sqrt(-g) g^{mn} C_m C_n (mode 'full'), or the spatial forms -cgf N sqrt(gamma) gamma^{ij} C_i C_j
    ('spatial4' = F2a, 4-D trace; 'spatial3' = F2b, spatial trace)."""
    ginv = gbar.inv()
    sq = sp.sqrt(-gbar.det())
    if mode == "full":
        C = deDonder(gbar)
        return sp.expand(-cgf * sq * sum(ginv[m, n] * C[m] * C[n] for m in R4 for n in R4))
    C = deDonder(gbar, spatial_trace=(mode == "spatial3"))
    gam_inv = gbar[1:, 1:].inv()
    return sp.expand(-cgf * sq * sum(gam_inv[i - 1, j - 1] * C[i] * C[j] for i in (1, 2, 3) for j in (1, 2, 3)))


def khronon_linear(gbar, dtau):
    """linear khronon quantities on a constant background with d taubar = dtau (covector):
    returns dict with dlnN (linear in h, d pi), nbar_dn, nbar_up, Nbar, a1_dn (jets), K1 (jets), K1_dn (jets, mu nu)."""
    ginv = gbar.inv()
    Xb = sp.simplify(-sum(ginv[m, n] * dtau[m] * dtau[n] for m in R4 for n in R4))
    Nb = 1 / sp.sqrt(Xb)
    nb_dn = [sp.simplify(-Nb * dtau[m]) for m in R4]
    nb_up = [sp.simplify(sum(ginv[m, n] * nb_dn[n] for n in R4)) for m in R4]
    h_up = [[sp.expand(sum(ginv[m, a] * ginv[n, b] * hS[a][b] for a in R4 for b in R4)) for n in R4] for m in R4]
    dX = sp.expand(sum(h_up[m][n] * dtau[m] * dtau[n] for m in R4 for n in R4)
                   - 2 * sum(ginv[m, n] * dtau[m] * dpS[n] for m in R4 for n in R4))
    dlnN = sp.expand(-dX / (2 * Xb))
    # delta n_mu = dlnN nbar_mu - Nbar d_mu pi ;  delta n^mu = -h^{mu nu} nbar_nu + g^{mu nu} delta n_nu
    dn_dn = [sp.expand(dlnN * nb_dn[m] - Nb * dpS[m]) for m in R4]
    dn_up = [sp.expand(-sum(h_up[m][n] * nb_dn[n] for n in R4) + sum(ginv[m, n] * dn_dn[n] for n in R4)) for m in R4]
    htr = sp.expand(sum(ginv[a, b] * hS[a][b] for a in R4 for b in R4))
    # projector hbar_mu^nu = delta + n_mu n^nu
    hb_mix = [[(1 if m == n else 0) + nb_dn[m] * nb_up[n] for n in R4] for m in R4]
    a1_dn = [sp.expand(sum(hb_mix[m][n] * D(n, dlnN) for n in R4)) for m in R4]
    K1 = sp.expand(sum(D(m, dn_up[m]) for m in R4) + sum(nb_up[m] * D(m, htr) for m in R4) / 2)
    G = gamma1(ginv)
    nabla_dn = [[sp.expand(D(r, dn_dn[s]) - sum(G[l][r][s] * nb_dn[l] for l in R4)) for s in R4] for r in R4]
    K1_dn = [[sp.expand(sum(hb_mix[m][r] * hb_mix[n][s] * nabla_dn[r][s] for r in R4 for s in R4)) for n in R4] for m in R4]
    return dict(Xb=Xb, Nb=Nb, nb_dn=nb_dn, nb_up=nb_up, dlnN=dlnN, a1_dn=a1_dn, K1=K1, K1_dn=K1_dn, htr=htr)


def L_khronon(gbar, dtau, al, be, c2):
    """sqrt(-g)[alpha a.a - c2 K^2 - beta K_mn K^mn] at quadratic order (background a = K = 0)."""
    ginv = gbar.inv()
    sq = sp.sqrt(-gbar.det())
    q = khronon_linear(gbar, dtau)
    aa = sum(ginv[m, n] * q["a1_dn"][m] * q["a1_dn"][n] for m in R4 for n in R4)
    KK = sum(ginv[m, r] * ginv[n, s] * q["K1_dn"][m][n] * q["K1_dn"][r][s] for m in R4 for n in R4 for r in R4 for s in R4)
    return sp.expand(sq * (al * aa - c2 * q["K1"]**2 - be * KK)), q


def L_aether(c1, c2, c3, c4):
    """Einstein-aether quadratic Lagrangian on flat space, aligned aether ubar = d_t, unit constraint solved
    (du^0 = h_00/2):  -c1 D_a^m D^a_m - c2 (D_m^m)^2 - c3 D_a^m D_m^a + c4 eta_mn D_0^m D_0^n,
    D_a^m = d_a du^m + Gamma^(1) m_{a0}."""
    eta = sp.diag(-1, 1, 1, 1)
    G = gamma1(eta)
    du_full = [hS[0][0] / 2, duS[1], duS[2], duS[3]]
    Dm = [[sp.expand(D(a, du_full[m]) + G[m][a][0]) for m in R4] for a in R4]          # Dm[a][m] = D_a^m
    t1 = sum(eta[a, a] * eta[m, m] * Dm[a][m]**2 for a in R4 for m in R4)
    t2 = sum(Dm[m][m] for m in R4)**2
    t3 = sum(Dm[a][m] * Dm[m][a] for a in R4 for m in R4)
    t4 = sum(eta[m, m] * Dm[0][m]**2 for m in R4)
    return sp.expand(-c1 * t1 - c2 * t2 - c3 * t3 + c4 * t4)


def fourier_sub(xi):
    sub = {}
    for l in R4:
        for (m, n) in PAIRS:
            sub[dH[l][m][n]] = xi[l] * HV[m][n]
        for s in R4:
            if l <= s:
                sub[ddP[l][s]] = xi[l] * xi[s] * PIV
        for m in R4:
            sub[dU[l][m]] = xi[l] * UV[m]
    return sub


VARS_H = [HV[m][n] for (m, n) in PAIRS]


def symbol_matrix(L, variables, xi=XI):
    """P(xi) = Hessian of the Fourier-substituted quadratic Lagrangian."""
    Q = sp.expand(L.xreplace(fourier_sub(xi)))
    return sp.Matrix(len(variables), len(variables), lambda i, j: sp.expand(sp.diff(Q, variables[i], variables[j])))


def pencil(P, lam, xi_spatial, xi=XI):
    """substitute xi = (lam, xi_spatial) and return A, B, C with P = A lam^2 + B lam + C."""
    sub = {xi[0]: lam, xi[1]: xi_spatial[0], xi[2]: xi_spatial[1], xi[3]: xi_spatial[2]}
    Pl = P.xreplace(sub).applyfunc(sp.expand)
    A = Pl.applyfunc(lambda e: sp.Poly(e, lam).coeff_monomial(lam**2))
    B = Pl.applyfunc(lambda e: sp.Poly(e, lam).coeff_monomial(lam))
    C = Pl.applyfunc(lambda e: sp.Poly(e, lam).coeff_monomial(1))
    deg_ok = all(sp.Poly(e, lam).degree() <= 2 for e in Pl if e != 0)
    return A, B, C, Pl, deg_ok
