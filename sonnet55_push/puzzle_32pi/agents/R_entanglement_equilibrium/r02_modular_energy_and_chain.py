#!/usr/bin/env python3
"""r02_modular_energy_and_chain.py -- the matter side of Jacobson's equilibrium (arXiv:1505.04753 eqs 9-11, 16-19) and the full chain to 8 pi G, plus the MSS reference (eq 22).

 M1  int_Sigma xi dV = Omega_{d-2} l^d/(d^2-1) with xi = (l^2-r^2)/(2l), symbolic in d and for d = 3..10   (eq 19)
 M2  the conformal Killing vector zeta = [(l^2-r^2-t^2) d_t - 2 r t d_r]/(2l): L_zeta eta = -(2t/l) eta (eq 11); zeta null on the diamond boundary; surface gravity = 1;
     near the boundary zeta^t -> distance to the boundary (Rindler boost with unit rapidity gradient, so K = 2 pi H_zeta)
 M3  full chain (1/4G) dA|_V + 2 pi d<H_zeta> = 0  =>  G_00 = 8 pi G T_00, every d; CONTROLS: xi -> 2 xi gives 16 pi G, T = hbar/pi gives 4 pi G, eta = 1/(2G) gives 4 pi G
 M4  the MSS reference: dS_d has G_ab = -lambda g_ab with lambda = (d-1)(d-2)/(2 L^2); its t=0 slice is S^{d-1}(L) with R_slice = 2 lambda; so the eq (22)
     combination G_00 + lambda g_00 vanishes identically on every MSS, for every L: Lambda is not selected by the small-ball equilibrium (explicit sympy dS_4 metric)
Exit 0 = all pass.
"""
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")
def must_fail(name, cond):
    ok.append(not bool(cond)); print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {name}")

l = sp.symbols('l', positive=True)
r = sp.symbols('r', positive=True)
d = sp.symbols('d', positive=True)
def Om(k):
    return 2 * sp.pi ** sp.Rational(k + 1, 2) / sp.gamma(sp.Rational(k + 1, 2))

# ------------------------------------------------------------------------------------------------ M1
print("M1  int xi dV = Omega_{d-2} l^d/(d^2-1)")
xi = (l**2 - r**2) / (2 * l)
# sympy cannot do the improper endpoint symbolically; use the explicit antiderivative F (F(0) = 0 for d > 1) and check F' = integrand, F(l) = l^d/(d^2-1)
Fanti = (l**2 * r**(d - 1) / (d - 1) - r**(d + 1) / (d + 1)) / (2 * l)
check("symbolic in d: antiderivative F' = xi r^{d-2}", sp.simplify(sp.diff(Fanti, r) - xi * r**(d - 2)) == 0)
check("symbolic in d: F(l) = l^d/(d^2-1)  (and F(0) = 0 for d > 1)", sp.simplify(Fanti.subs(r, l) - l**d / (d**2 - 1)) == 0)
for dd in range(3, 11):
    val = Om(dd - 2) * sp.integrate(xi * r**(dd - 2), (r, 0, l))
    check(f"d={dd}: Omega_{dd-2} int xi r^{dd-2} dr = Omega l^d/(d^2-1)", sp.simplify(val - Om(dd - 2) * l**dd / (dd**2 - 1)) == 0)
must_fail("M1c the weight (l - r) (linear, not the conformal Killing weight) gives the same integral", sp.simplify(
    sp.integrate((l - r) * r**2, (r, 0, l)) - l**4 / 15) == 0)

# ------------------------------------------------------------------------------------------------ M2
print("M2  the conformal Killing vector of the flat diamond (d = 4 coordinates t, r, theta, phi)")
t, th, ph = sp.symbols('t theta phi', real=True)
X = [t, r, th, ph]
g = sp.diag(-1, 1, r**2, r**2 * sp.sin(th)**2)
zeta = [(l**2 - r**2 - t**2) / (2 * l), -r * t / l, 0, 0]
def lie_metric(vec, g, X):
    n = len(X)
    return sp.Matrix(n, n, lambda a, b: sp.simplify(
        sum(vec[c] * sp.diff(g[a, b], X[c]) for c in range(n)) + sum(g[c, b] * sp.diff(vec[c], X[a]) for c in range(n))
        + sum(g[a, c] * sp.diff(vec[c], X[b]) for c in range(n))))
Lg = lie_metric(zeta, g, X)
check("L_zeta g = -(2t/l) g   (eq 11)", sp.simplify(Lg + (2 * t / l) * g) == sp.zeros(4, 4))
must_fail("M2b L_zeta g = -(t/l) g", sp.simplify(Lg + (t / l) * g) == sp.zeros(4, 4))
zsq = sp.simplify(sum(g[a, a] * zeta[a]**2 for a in range(4)))
check("zeta^2 = -(l^2-(t+r)^2)(l^2-(t-r)^2)/(4 l^2)", sp.simplify(zsq + (l**2 - (t + r)**2) * (l**2 - (t - r)**2) / (4 * l**2)) == 0)
# surface gravity on the future boundary t = l - r:  d_a (zeta^2) = -2 kappa zeta_a
zlow = [sum(g[a, b] * zeta[b] for b in range(4)) for a in range(4)]
res = []
for a in range(2):
    lhs = sp.diff(zsq, X[a]).subs(t, l - r)
    zl = sp.simplify(zlow[a].subs(t, l - r))
    res.append(sp.simplify(-lhs / (2 * zl)))
check(f"surface gravity from t-component and r-component agree and equal 1 (got {res})", res[0] == 1 and res[1] == 1)
zeta2 = [2 * c for c in zeta]
zsq2 = sp.simplify(sum(g[a, a] * zeta2[a]**2 for a in range(4)))
zlow2 = [sum(g[a, b] * zeta2[b] for b in range(4)) for a in range(4)]
kap2 = sp.simplify(-sp.diff(zsq2, t).subs(t, l - r) / (2 * sp.simplify(zlow2[0].subs(t, l - r))))
must_fail(f"M2c the doubled vector 2 zeta has surface gravity 1 (it is {kap2}: the normalisation of zeta fixes T = hbar kappa/2 pi)", kap2 == 1)
# near the boundary of the t=0 slice: zeta^t ~ distance to the boundary with unit coefficient (Rindler boost)
lim = sp.limit(xi / (l - r), r, l)
check("zeta^t|_{t=0} -> (l - r) as r -> l: unit boost gradient at the edge, so 2 pi <H_zeta> is the Rindler boost (BW) normalisation", lim == 1)

# ------------------------------------------------------------------------------------------------ M3
print("M3  the full chain, every d, with the modular energy term")
Gn, T00, G00 = sp.symbols('G T00 G00', positive=True)
Omg = sp.symbols('Omega', positive=True)
dA_V = -Omg * l**d * G00 / (d**2 - 1)
dHzeta = Omg * l**d / (d**2 - 1) * T00
sol = sp.solve(sp.Eq(dA_V / (4 * Gn) + 2 * sp.pi * dHzeta, 0), G00)[0]
check("G_00 = 8 pi G T_00 (every d symbolically)", sp.simplify(sol - 8 * sp.pi * Gn * T00) == 0)
sol2 = sp.solve(sp.Eq(dA_V / (4 * Gn) + 2 * sp.pi * 2 * dHzeta, 0), G00)[0]
must_fail("M3b modular weight doubled (kappa = 2) still gives 8 pi G", sp.simplify(sol2 - 8 * sp.pi * Gn * T00) == 0)
print("      (doubled weight gives coefficient /(8 pi G) =", sp.simplify(sol2 / (8 * sp.pi * Gn * T00)), ")")
sol3 = sp.solve(sp.Eq(dA_V / (4 * Gn) + sp.pi * dHzeta, 0), G00)[0]
must_fail("M3c T = hbar/pi (i.e. pi instead of 2 pi) still gives 8 pi G", sp.simplify(sol3 - 8 * sp.pi * Gn * T00) == 0)
sol4 = sp.solve(sp.Eq(dA_V / (2 * Gn) + 2 * sp.pi * dHzeta, 0), G00)[0]
must_fail("M3d entropy density eta = 1/(2G) instead of 1/(4G) still gives 8 pi G", sp.simplify(sol4 - 8 * sp.pi * Gn * T00) == 0)
eta_ = sp.symbols('eta', positive=True)
solg = sp.solve(sp.Eq(dA_V * eta_ + 2 * sp.pi * dHzeta, 0), G00)[0]
check("with a free area-entropy density eta: G_00 = (2 pi/eta) T_00, so G = 1/(4 eta) (paper eq 27) and 1/(4G) IS the Bekenstein-Hawking value",
      sp.simplify(solg - 2 * sp.pi * T00 / eta_) == 0 and sp.simplify((2 * sp.pi / eta_).subs(eta_, 1 / (4 * Gn)) - 8 * sp.pi * Gn) == 0)
print("      (honest limitation: only the product 2 pi x 4 is detected; 2 pi from Bisognano-Wichmann/M2, 4 from eta = 1/4G by definition of G)")

# ------------------------------------------------------------------------------------------------ M4
print("M4  the MSS reference (explicit sympy dS_4 in the static patch)")
Ls = sp.symbols('L', positive=True)
tt, rr, thh, phh = sp.symbols('t r theta phi', real=True)
f = 1 - rr**2 / Ls**2
Xs = [tt, rr, thh, phh]
gs = sp.diag(-f, 1 / f, rr**2, rr**2 * sp.sin(thh)**2)
gi = gs.inv()
n4 = 4
Gam = [[[sum(gi[i, m] * (sp.diff(gs[m, j], Xs[k]) + sp.diff(gs[m, k], Xs[j]) - sp.diff(gs[j, k], Xs[m])) for m in range(n4)) / 2
         for k in range(n4)] for j in range(n4)] for i in range(n4)]
def Riem(i, j, k, m):
    return (sp.diff(Gam[i][j][m], Xs[k]) - sp.diff(Gam[i][j][k], Xs[m])
            + sum(Gam[i][k][q] * Gam[q][j][m] - Gam[i][m][q] * Gam[q][j][k] for q in range(n4)))
Ric = sp.Matrix(n4, n4, lambda j, m: sp.simplify(sum(Riem(i, j, i, m) for i in range(n4))))
Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(n4) for j in range(n4)))
Ein = sp.simplify(Ric - Rs * gs / 2)
Lam = sp.symbols('Lambda_c', positive=True)
check("dS_4: R_ab = (3/L^2) g_ab", sp.simplify(Ric - 3 * gs / Ls**2) == sp.zeros(4, 4))
check("dS_4: G_ab + Lambda g_ab = 0 with Lambda = 3/L^2", sp.simplify(Ein + (3 / Ls**2) * gs) == sp.zeros(4, 4))
# t = 0 slice: static => K_ij = 0; slice metric dr^2/f + r^2 dOmega^2; its scalar curvature
hs = sp.diag(1 / f, rr**2, rr**2 * sp.sin(thh)**2)
Xh = [rr, thh, phh]
hi = hs.inv()
Gh = [[[sum(hi[i, m] * (sp.diff(hs[m, j], Xh[k]) + sp.diff(hs[m, k], Xh[j]) - sp.diff(hs[j, k], Xh[m])) for m in range(3)) / 2
        for k in range(3)] for j in range(3)] for i in range(3)]
def Rh(i, j, k, m):
    return (sp.diff(Gh[i][j][m], Xh[k]) - sp.diff(Gh[i][j][k], Xh[m])
            + sum(Gh[i][k][q] * Gh[q][j][m] - Gh[i][m][q] * Gh[q][j][k] for q in range(3)))
Rich = sp.Matrix(3, 3, lambda j, m: sp.simplify(sum(Rh(i, j, i, m) for i in range(3))))
Rsl = sp.simplify(sum(hi[i, j] * Rich[i, j] for i in range(3) for j in range(3)))
check("t=0 slice of dS_4 is S^3(L): R_slice = 6/L^2 = 2 Lambda = 2 G_00 (G_00 = Lambda, g_00 = -1 at r=0)",
      sp.simplify(Rsl - 6 / Ls**2) == 0 and sp.simplify(Ein[0, 0].subs(rr, 0) - 3 / Ls**2) == 0)
check("eq (22): G_00 + lambda g_00 = 0 on the MSS for EVERY L (lambda = Lambda = 3/L^2, g_00 = -1 at the centre)",
      sp.simplify(Ein[0, 0].subs(rr, 0) + (3 / Ls**2) * gs[0, 0].subs(rr, 0)) == 0)
# general d, constant curvature
dd = sp.symbols('dd', positive=True)
lam_d = (dd - 1) * (dd - 2) / (2 * Ls**2)
Ric_coef = (dd - 1) / Ls**2                    # R_ab = (d-1)/L^2 g_ab
Rscal = dd * Ric_coef
G_coef = Ric_coef - Rscal / 2                  # G_ab = G_coef g_ab
check("dS_d: G_ab = -lambda g_ab with lambda = (d-1)(d-2)/(2 L^2)  (constant-curvature algebra)", sp.simplify(G_coef + lam_d) == 0)
check("dS_d slice S^{d-1}(L): R_slice = (d-1)(d-2)/L^2 = 2 lambda", sp.simplify((dd - 1) * (dd - 2) / Ls**2 - 2 * lam_d) == 0)
must_fail("M4c dS_4 with Lambda = 1/L^2 (wrong)", sp.simplify(Ein + (1 / Ls**2) * gs) == sp.zeros(4, 4))

print(f"\nr02: {sum(ok)}/{len(ok)} checks passed")
sys.exit(0 if all(ok) else 1)
