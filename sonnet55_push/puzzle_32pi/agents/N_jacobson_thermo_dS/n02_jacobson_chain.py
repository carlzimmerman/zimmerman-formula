#!/usr/bin/env python3
"""n02_jacobson_chain.py -- Jacobson's Clausius derivation with every factor tracked; the flat-space limit must give 8 pi G exactly.

Jacobson (arXiv gr-qc/9504004, opened): delta Q = T dS on every local Rindler horizon, T = hbar kappa/(2 pi) (Unruh), S = A/(4 G hbar), gives
R_ab k^a k^b = 8 pi G T_ab k^a k^b for every null k, hence the Einstein equation with Lambda an integration constant.
Here the two numbers 2 pi and 4 are carried as symbols c_T, c_S:  T = hbar kappa / c_T,  S = A/(c_S G hbar).
 B1 Raychaudhuri (linearised, theta(0)=sigma(0)=0):  theta = -lambda R_kk.  Verified on a null congruence of spatially flat FRW (exact identity, sigma = 0).
 B2 Clausius chain with symbols:  R_kk = c_T c_S G T_kk.   8 pi G  <=>  c_T c_S = 8 pi.   Detects a wrong 2 pi or a wrong 4 (but ONLY their product: see B2d).
 B3 Conservation (Bianchi) turns R_kk = chi T_kk (all null k) into R_mn = chi (T_mn - T g_mn/2) + Lambda g_mn, Lambda a free constant;
    Poisson:  R_00 = chi rho/2 = 4 pi G rho  <=> chi = 8 pi G.
 B4 FRW check with the Einstein tensor computed from the metric: R_kk = 8 pi G T_kk holds, 4 pi G and 16 pi G do not.  Lambda drops out of the null-null equation.
 B5 Lambda invisibility: in de Sitter R_kk = 0 for every null k and every H, so the thermodynamic equation cannot fix Lambda (nor tie it to any other constant).
Exit 0 = all pass.
"""
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")
def must_fail(name, cond):
    ok.append(not bool(cond)); print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {name}")

# ---------------------------------------------------------------- generic curvature helper
def curvature(g, X):
    n = len(X); ginv = g.inv()
    Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(n)) / 2
             for k in range(n)] for j in range(n)] for i in range(n)]
    def Riem(i, j, k, l):   # R^i_{jkl}
        return (sp.diff(Gam[i][j][l], X[k]) - sp.diff(Gam[i][j][k], X[l])
                + sum(Gam[i][k][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][k] for m in range(n)))
    Ric = sp.Matrix(n, n, lambda j, l: sp.simplify(sum(Riem(i, j, i, l) for i in range(n))))
    Rs = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    return Gam, Ric, Rs, ginv

print("B1  Raychaudhuri on a null congruence of spatially flat FRW")
t, x, y, z = sp.symbols('t x y z', real=True)
p = sp.symbols('p', positive=True)
A = sp.Function('A')(t)
X = [t, x, y, z]
g = sp.diag(-1, A**2, A**2, A**2)
Gam, Ric, Rs, ginv = curvature(g, X)
k_up = [p / A, p / A**2, 0, 0]                                  # null: -(p/A)^2 + A^2 (p/A^2)^2 = 0
check("B1a k is null", sp.simplify(sum(g[i, i] * k_up[i]**2 for i in range(4))) == 0)
geo = [sp.simplify(sum(k_up[n] * sp.diff(k_up[m], X[n]) for n in range(4)) + sum(Gam[m][n][l] * k_up[n] * k_up[l] for n in range(4) for l in range(4))) for m in range(4)]
check("B1b k is an affinely parametrised geodesic (k^n grad_n k^m = 0)", all(c == 0 for c in geo))
sqrtg = A**3
theta = sp.simplify(sum(sp.diff(sqrtg * k_up[m], X[m]) for m in range(4)) / sqrtg)      # = div k = expansion of an affine null geodesic congruence
k_low = [sum(g[i, j] * k_up[j] for j in range(4)) for i in range(4)]
B = sp.Matrix(4, 4, lambda mu, nu: sp.simplify(sp.diff(k_low[mu], X[nu]) - sum(Gam[l][mu][nu] * k_low[l] for l in range(4))))   # B_{mu nu} = grad_nu k_mu
trans = [2, 3]                                                  # transverse directions y, z (screen orthogonal to k and to the t-x plane)
Btr = sp.Matrix([[B[i, j] for j in trans] for i in trans])
gtr = sp.Matrix([[g[i, j] for j in trans] for i in trans])
mixed = sp.simplify(gtr.inv() * Btr)
check("B1c transverse B is pure trace (shear sigma = 0, twist 0), theta = trace", sp.simplify(mixed[0, 0] - mixed[1, 1]) == 0 and sp.simplify(mixed[0, 1]) == 0 and sp.simplify(mixed.trace() - theta) == 0)
sigma2 = 0
Rkk = sp.simplify(sum(Ric[i, j] * k_up[i] * k_up[j] for i in range(4) for j in range(4)))
dtheta = sp.simplify(sum(k_up[m] * sp.diff(theta, X[m]) for m in range(4)))
check("B1d Raychaudhuri  d theta/d lambda = -theta^2/2 - sigma^2 - R_kk   (exact identity here)", sp.simplify(dtheta + theta**2 / 2 + sigma2 + Rkk) == 0)
must_fail("B1e Raychaudhuri with theta^2 instead of theta^2/2", sp.simplify(dtheta + theta**2 + sigma2 + Rkk) == 0)
lam, lam0, R0 = sp.symbols('lambda lambda_0 R0', real=True)
th_lin = sp.integrate(-R0, (lam, 0, lam))                       # theta(0) = 0, dtheta/dlambda = -R_kk (theta^2 term is 2nd order)
check("B1f linearised: theta(lambda) = -lambda R_kk", sp.simplify(th_lin + lam * R0) == 0)

print("B2  the Clausius chain with symbols c_T (Unruh 2 pi) and c_S (entropy quarter)")
kap, hb, G, Tkk, Rk, cT, cS, Ap = sp.symbols('kappa hbar G T_kk R_kk c_T c_S A_p', positive=True)
lam_min = sp.symbols('lam0', positive=True)
# heat:  delta Q = int T_ab chi^a dSigma^b,  chi^a = -kappa lambda k^a,  dSigma^b = k^b dlambda dA   (constant T_kk on the patch)
dQ = sp.integrate(-kap * lam * Tkk, (lam, -lam_min, 0)) * Ap
# area change from the linearised Raychaudhuri:  delta A = int dA int theta dlambda,  theta = -lambda R_kk
dA_ = sp.integrate(-lam * Rk, (lam, -lam_min, 0)) * Ap
Temp = hb * kap / cT
eta = 1 / (cS * G * hb)
sol = sp.solve(sp.Eq(dQ, Temp * eta * dA_), Rk)[0]
check("B2a R_kk = c_T c_S G T_kk   (kappa, hbar, lambda_0, A_p all cancel)", sp.simplify(sol - cT * cS * G * Tkk) == 0)
chi_ = lambda cTv, cSv: sp.simplify(sol.subs({cT: cTv, cS: cSv}) / Tkk)
check("B2b (c_T, c_S) = (2 pi, 4)  gives exactly 8 pi G", sp.simplify(chi_(2 * sp.pi, 4) - 8 * sp.pi * G) == 0)
must_fail("B2c wrong Unruh factor (pi):  R_kk = 8 pi G T_kk", sp.simplify(chi_(sp.pi, 4) - 8 * sp.pi * G) == 0)
must_fail("B2c' wrong Unruh factor (4 pi)", sp.simplify(chi_(4 * sp.pi, 4) - 8 * sp.pi * G) == 0)
must_fail("B2c'' wrong entropy quarter (S = A/2G)", sp.simplify(chi_(2 * sp.pi, 2) - 8 * sp.pi * G) == 0)
must_fail("B2c''' wrong entropy quarter (S = A/8G)", sp.simplify(chi_(2 * sp.pi, 8) - 8 * sp.pi * G) == 0)
check("B2d honest limitation: only the PRODUCT is detected: (pi, 8) also gives 8 pi G -> the two numbers must be fixed independently "
      "(2 pi: KMS/detector check n01 A4 with H->0; 4: first law dM = T dS in n03 C2)", sp.simplify(chi_(sp.pi, 8) - 8 * sp.pi * G) == 0)

print("B3  conservation: R_kk = chi T_kk (all null k) => R_mn = chi (T_mn - T g_mn/2) + Lambda g_mn; Poisson coefficient")
chi, phi_, Lam = sp.symbols('chi phi Lambda')
# R_mn = chi T_mn + phi g_mn (null-null equation allows a trace term);  contracted Bianchi + conservation of T fix  d_n(phi + chi T/2) = 0
Tt = sp.symbols('T')                                            # trace of T_mn
phi_sol = -chi * Tt / 2 + Lam                                   # the general solution: phi + chi T/2 = Lambda = const
Rtrace = chi * Tt + 4 * phi_sol
Gmn_coeff_of_g = phi_sol - Rtrace / 2                           # G_mn = chi T_mn + (phi - R/2) g_mn ; must have vanishing divergence => coefficient of g_mn is -Lambda + ... constant + chi T terms cancel
check("B3a  G_mn = chi T_mn - Lambda g_mn with Lambda an arbitrary constant (the T-dependent pieces cancel)", sp.simplify(Gmn_coeff_of_g + Lam) == 0)
rho = sp.symbols('rho', positive=True)
T_dust = -rho                                                   # trace of dust, T = -rho
R00 = chi * rho + phi_sol.subs(Tt, T_dust) * (-1)               # R_00 = chi T_00 + phi g_00, T_00 = rho, g_00 = -1
R00 = sp.simplify(R00.subs(Lam, 0))
check("B3b R_00 = chi rho/2 for dust (Lambda = 0): Newtonian limit  R_00 = laplacian(Phi)", sp.simplify(R00 - chi * rho / 2) == 0)
check("B3c chi = 8 pi G  <=>  laplacian Phi = 4 pi G rho", sp.simplify((R00.subs(chi, 8 * sp.pi * G)) - 4 * sp.pi * G * rho) == 0)
must_fail("B3d chi = 4 pi G would give laplacian Phi = 4 pi G rho", sp.simplify((R00.subs(chi, 4 * sp.pi * G)) - 4 * sp.pi * G * rho) == 0)

print("B4  FRW with Lambda: Einstein tensor from the metric; the null-null equation holds with 8 pi G only")
Einstein = sp.simplify(Ric - Rs * g / 2)
rho_t, p_t, Lm, G4 = sp.symbols('rho_t p_t Lambda_c G4')
u = sp.Matrix([1, 0, 0, 0]); ulow = g * u
Tmn = sp.Matrix(4, 4, lambda i, j: (rho_t + p_t) * ulow[i] * ulow[j] + p_t * g[i, j])
eqs = [sp.Eq(Einstein[0, 0] + Lm * g[0, 0], 8 * sp.pi * G4 * Tmn[0, 0]), sp.Eq(Einstein[1, 1] + Lm * g[1, 1], 8 * sp.pi * G4 * Tmn[1, 1])]
sol_fr = sp.solve(eqs, [rho_t, p_t], dict=True)[0]
Tkk_frw = sp.simplify(sum(Tmn[i, j] * k_up[i] * k_up[j] for i in range(4) for j in range(4)))
resid = sp.simplify((Rkk - 8 * sp.pi * G4 * Tkk_frw).subs(sol_fr))
check("B4a R_kk = 8 pi G T_kk on the FRW solution of G_mn + Lambda g_mn = 8 pi G T_mn  (any a(t), any Lambda)", resid == 0)
check("B4b Lambda_c does not appear in R_kk - 8 pi G T_kk", not resid.has(Lm))
for cc, nm in [(4 * sp.pi, "4 pi G"), (16 * sp.pi, "16 pi G")]:
    res_w = sp.simplify((Rkk - cc * G4 * Tkk_frw).subs(sol_fr))
    must_fail(f"B4c null-null equation with coefficient {nm}", res_w == 0)

print("B5  Lambda is invisible to the null-null equation (de Sitter static patch, generic H)")
Hh = sp.symbols('H', positive=True)
tt, rr, th_, ph_ = sp.symbols('t r theta phi', real=True)
fH = 1 - Hh**2 * rr**2
Xs = [tt, rr, th_, ph_]
gs = sp.diag(-fH, 1 / fH, rr**2, rr**2 * sp.sin(th_)**2)
Gs, Rics, Rss, _ = curvature(gs, Xs)
check("B5a de Sitter: R_mn = 3 H^2 g_mn", sp.simplify(Rics - 3 * Hh**2 * gs) == sp.zeros(4, 4))
ks = [1 / fH, 1, 0, 0]
check("B5b k = (1/f, 1, 0, 0) is null", sp.simplify(sum(gs[i, i] * ks[i]**2 for i in range(4))) == 0)
check("B5c R_kk = 0 for every H: T_kk = 0 in vacuum, and the equation is satisfied by ANY Lambda", sp.simplify(sum(Rics[i, j] * ks[i] * ks[j] for i in range(4) for j in range(4))) == 0)

n, npass = len(ok), sum(ok)
print(f"\nn02: {npass}/{n} checks passed")
sys.exit(0 if npass == n else 1)
