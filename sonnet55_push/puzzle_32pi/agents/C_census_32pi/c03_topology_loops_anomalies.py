#!/usr/bin/env python3
"""c03_topology_loops_anomalies.py -- census lane C: the TOPOLOGICAL / loop / anomaly instances of 32 pi^2, 16 pi^2 and neighbours.

  T1  Chern-Gauss-Bonnet: E4 = Riem^2 - 4 Ric^2 + R^2 from the Riemann tensor of S^4(L), S^2 x S^2, de Sitter (sympy);
      int E4 = 32 pi^2 chi;  general 2n:  int E_2n = (4 pi)^n n! chi  (Gamma-function identity, n = 1..6);  the 2-form-norm form 1/(8 pi^2)
      with the 2-form norm differs by 4 = a norm convention
  T2  SU(2) BPST instanton built explicitly: F^a_mu_nu, F^2 = 192 rho^4/(x^2+rho^2)^4, self-duality, int F Ftilde = 32 pi^2, action 8 pi^2/g^2;
      Q = (1/32 pi^2) int F^a Ftilde^a = (1/8 pi^2) int tr F^F ; 32 pi^2 = Vol(S^3) x 16
  T3  Chern-Simons level: (k/12 pi) x 24 pi^2 = 2 pi k
  T4  loop factor 1/(16 pi^2) = Vol(S^3)/(2 pi)^4 x (1/2); 32 pi^2 = 2 (4 pi)^2
  T5  conformal trace anomaly: (1/16 pi^2)(c W^2 - a E4) with hep-th/9308075's a, c reduces to (1/2880 pi^2)(Riem^2 - Ric^2); de Sitter rho = H^4/(960 pi^2);
      integrated anomaly on S^4 = -1/90 = -2 a chi; semiclassical (Starobinsky) self-consistency  G H^2 = 360 pi/N
  T6  2D: Polyakov c/(96 pi) int R box^-1 R = (c/24 pi) int omega lap omega x 4 ; int R sqrt(g) = 4 pi chi
  T7  Vol(S^n) and 32 pi^2 = 12 Vol(S^4) = int_{S^4(1)} R dV
Controls (each MUST be caught): a wrong GB constant, a wrong instanton integral, wrong anomaly coefficient combination, wrong Polyakov factor,
wrong Vol(S^4).
Exit 0 = every check and every control behaves.
"""
import itertools
import sys
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

pi = sp.pi

# ------------------------------------------------------------------ curvature machinery
def christoffel(g, X):
    n = len(X); gi = g.inv()
    return [[[sp.simplify(sum(gi[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(n)) / 2)
              for k in range(n)] for j in range(n)] for i in range(n)]

def curvature_invariants(g, X):
    """returns (Riem^2, Ric^2, R) for a metric g in coordinates X"""
    n = len(X); Gm = christoffel(g, X); gi = g.inv()
    Rup = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]      # R^i_{jkl}
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    e = sp.diff(Gm[i][j][l], X[k]) - sp.diff(Gm[i][j][k], X[l])
                    for m in range(n):
                        e += Gm[i][k][m] * Gm[m][j][l] - Gm[i][l][m] * Gm[m][j][k]
                    Rup[i][j][k][l] = sp.simplify(e)
    Ric = sp.Matrix(n, n, lambda j, l: sp.simplify(sum(Rup[i][j][i][l] for i in range(n))))
    Rs = sp.simplify(sum(gi[j, l] * Ric[j, l] for j in range(n) for l in range(n)))
    # Riem_{ijkl} R^{ijkl}
    Rdown = [[[[sum(g[i, m] * Rup[m][j][k][l] for m in range(n)) for l in range(n)] for k in range(n)] for j in range(n)] for i in range(n)]
    riem2 = 0
    for i, j, k, l in itertools.product(range(n), repeat=4):
        if Rdown[i][j][k][l] == 0: continue
        riem2 += Rdown[i][j][k][l] * sum(gi[i, a] * gi[j, b] * gi[k, c] * gi[l, d] * Rdown[a][b][c][d]
                                         for a in range(n) for b in range(n) for c in range(n) for d in range(n)
                                         if gi[i, a] != 0 and gi[j, b] != 0 and gi[k, c] != 0 and gi[l, d] != 0)
    ric2 = sum(Ric[i, j] * Ric[k, l] * gi[i, k] * gi[j, l] for i, j, k, l in itertools.product(range(n), repeat=4)
               if gi[i, k] != 0 and gi[j, l] != 0)
    return sp.simplify(riem2), sp.simplify(ric2), Rs

# ============================================================================= T1 Gauss-Bonnet
print("\nT1  Chern-Gauss-Bonnet")
L = sp.symbols('L', positive=True)
c1, c2, c3, c4 = sp.symbols('chi theta phi psi', positive=True)
gS4 = sp.diag(L**2, L**2 * sp.sin(c1)**2, L**2 * sp.sin(c1)**2 * sp.sin(c2)**2, L**2 * sp.sin(c1)**2 * sp.sin(c2)**2 * sp.sin(c3)**2)
XS4 = [c1, c2, c3, c4]
Riem2, Ric2, Rs = curvature_invariants(gS4, XS4)
E4 = sp.simplify(Riem2 - 4 * Ric2 + Rs**2)
check("S^4(L): Riem^2 = 24/L^4, Ric^2 = 36/L^4, R = 12/L^2", sp.simplify(Riem2 - 24 / L**4) == 0 and sp.simplify(Ric2 - 36 / L**4) == 0 and sp.simplify(Rs - 12 / L**2) == 0)
check("S^4(L): E4 = 24/L^4", sp.simplify(E4 - 24 / L**4) == 0)
sqrtg_S4 = L**4 * sp.sin(c1)**3 * sp.sin(c2)**2 * sp.sin(c3)          # sqrt(det g) on 0<chi,theta,phi<pi (all sines >= 0)
assert sp.simplify(gS4.det() - sqrtg_S4**2) == 0
volS4 = sp.integrate(sqrtg_S4, (c4, 0, 2 * pi), (c3, 0, pi), (c2, 0, pi), (c1, 0, pi))
check("Vol(S^4(L)) = (8 pi^2/3) L^4", sp.simplify(volS4 - sp.Rational(8, 3) * pi**2 * L**4) == 0)
check("int E4 = 64 pi^2 = 32 pi^2 chi with chi(S^4) = 2, for every L", sp.simplify(E4 * volS4 - 64 * pi**2) == 0)
check("CONTROL C-T1a: a wrong constant 30 pi^2 chi is rejected", sp.simplify(E4 * volS4 - 30 * pi**2 * 2) != 0)
# S^2 x S^2
th1, ph1, th2, ph2 = sp.symbols('th1 ph1 th2 ph2', positive=True)
gSS = sp.diag(L**2, L**2 * sp.sin(th1)**2, L**2, L**2 * sp.sin(th2)**2)
riemSS, ricSS, RSS = curvature_invariants(gSS, [th1, ph1, th2, ph2])
E4SS = sp.simplify(riemSS - 4 * ricSS + RSS**2)
volSS = (4 * pi * L**2)**2
check("S^2 x S^2 (Euclidean Nariai): E4 = 8/L^4 = 2 R1 R2, int E4 = 128 pi^2 = 32 pi^2 x 4", sp.simplify(E4SS - 8 / L**4) == 0 and sp.simplify(E4SS * volSS - 128 * pi**2) == 0)
# de Sitter static patch (Lorentzian): Riem^2, Ric^2
tt, rr, thh, phh, H = sp.symbols('t r theta phi H', positive=True)
fdS = 1 - H**2 * rr**2
gdS = sp.diag(-fdS, 1 / fdS, rr**2, rr**2 * sp.sin(thh)**2)
riemdS, ricdS, RdS = curvature_invariants(gdS, [tt, rr, thh, phh])
check("de Sitter: Riem^2 = 24 H^4, Ric^2 = 36 H^4, R = 12 H^2", sp.simplify(riemdS - 24 * H**4) == 0 and sp.simplify(ricdS - 36 * H**4) == 0 and sp.simplify(RdS - 12 * H**2) == 0)
# general dimension 2n: E_2n(S^2n unit) = (2n)!, and (2n)! Vol(S^2n) = 2 (4 pi)^n n!
res = []
for n in range(1, 7):
    vol = 2 * pi**(sp.Rational(2 * n + 1, 2)) / sp.gamma(sp.Rational(2 * n + 1, 2))
    res.append(sp.simplify(sp.factorial(2 * n) * vol - 2 * (4 * pi)**n * sp.factorial(n)) == 0)
check("int_{S^2n} E_2n = (2n)! Vol(S^2n) = (4 pi)^n n! chi  for n = 1..6  (n=1: 4 pi; n=2: 32 pi^2 = 2 (4 pi)^2; n=3: 384 pi^3)", all(res))
check("32 pi^2 = (4 pi)^2 x 2! (the general Pfaffian normalisation (4 pi)^n n!)", 32 * pi**2 == (4 * pi)**2 * sp.factorial(2))
# 2-form-norm form chi = (1/8 pi^2) int (|W|^2 + R^2/24 - |E|^2/2) with 2-form norms (|W|^2_{2-form} = W^2_{tensor}/4)
def euler_2form(riem2, ric2, Rs_, vol):
    W2 = riem2 - 2 * ric2 + Rs_**2 / 3                       # tensor norm of the Weyl tensor (n = 4)
    Ez2 = ric2 - Rs_**2 / 4                                  # tensor norm of the traceless Ricci
    return sp.simplify((W2 / 4 + Rs_**2 / 24 - Ez2 / 2) * vol / (8 * pi**2))
check("2-form-norm form (1/8 pi^2) int (|W|^2 + R^2/24 - |E|^2/2), 2-form norms, gives chi(S^4) = 2 and chi(S^2 x S^2) = 4",
      sp.simplify(euler_2form(Riem2, Ric2, Rs, volS4) - 2) == 0 and sp.simplify(euler_2form(riemSS, ricSS, RSS, volSS) - 4) == 0)
print("      => 8 pi^2 (2-form norm) versus 32 pi^2 (tensor norm): the factor 4 = 2^2 is a NORM CONVENTION, not new physics.")

# ============================================================================= T2 instanton
print("\nT2  the SU(2) BPST instanton, built explicitly")
xs = sp.symbols('x1 x2 x3 x4', real=True); rho = sp.symbols('rho', positive=True)
r2 = sum(v**2 for v in xs)
def eta(a, mu, nu):                                              # 't Hooft symbol (a = 1..3, mu, nu = 1..4)
    if mu <= 3 and nu <= 3: return sp.LeviCivita(a, mu, nu)
    if nu == 4 and mu <= 3: return 1 if a == mu else 0
    if mu == 4 and nu <= 3: return -1 if a == nu else 0
    return 0
A = [[2 * sum(eta(a, mu, nu) * xs[nu - 1] for nu in range(1, 5)) / (r2 + rho**2) for mu in range(1, 5)] for a in range(1, 4)]   # A^a_mu
def Fc(a, mu, nu):                                               # F^a_{mu nu} = d_mu A_nu - d_nu A_mu + eps_{abc} A^b_mu A^c_nu
    e = sp.diff(A[a - 1][nu - 1], xs[mu - 1]) - sp.diff(A[a - 1][mu - 1], xs[nu - 1])
    e += sum(sp.LeviCivita(a, b, c) * A[b - 1][mu - 1] * A[c - 1][nu - 1] for b in range(1, 4) for c in range(1, 4))
    return sp.simplify(e)
F = {(a, mu, nu): Fc(a, mu, nu) for a in range(1, 4) for mu in range(1, 5) for nu in range(1, 5)}
F2 = sp.simplify(sum(F[(a, mu, nu)]**2 for a in range(1, 4) for mu in range(1, 5) for nu in range(1, 5)))
check("F^a_mu_nu F^a_mu_nu = 192 rho^4/(x^2+rho^2)^4", sp.simplify(F2 - 192 * rho**4 / (r2 + rho**2)**4) == 0)
selfdual = all(sp.simplify(F[(a, mu, nu)] - sum(sp.LeviCivita(mu, nu, rh, si) * F[(a, rh, si)] for rh in range(1, 5) for si in range(1, 5)) / 2) == 0
               for a in range(1, 4) for mu in range(1, 5) for nu in range(1, 5))
check("field strength is self-dual: F = Ftilde", selfdual)
rad = sp.symbols('r', positive=True)
Ir = sp.integrate(rad**3 * rho**4 / (rad**2 + rho**2)**4, (rad, 0, sp.oo))
check("int_0^oo r^3 rho^4/(r^2+rho^2)^4 dr = 1/12", sp.simplify(Ir - sp.Rational(1, 12)) == 0)
volS3 = 2 * pi**2
FF = sp.simplify(volS3 * 192 * Ir)
check("int F^a Ftilde^a d^4x = Vol(S^3) x 192 x (1/12) = 32 pi^2", sp.simplify(FF - 32 * pi**2) == 0)
g = sp.symbols('g', positive=True)
check("action S = (1/(4 g^2)) int F^2 = 8 pi^2/g^2   [0802.1862 eq.(1.1): exp(-8 pi^2/g^2)]", sp.simplify(FF / (4 * g**2) - 8 * pi**2 / g**2) == 0)
check("winding number Q = (1/(32 pi^2)) int F^a Ftilde^a = 1  [0802.1862 eq.(10.3), (12.7) as read]", sp.simplify(FF / (32 * pi**2) - 1) == 0)
check("CONTROL C-T2a: a wrong normalisation Q = (1/(16 pi^2)) int F^a Ftilde^a is rejected (gives 2)", sp.simplify(FF / (16 * pi**2) - 1) != 0)
# tr F^F = (1/4) F^a Ftilde^a d^4x with tr T^a T^b = delta/2 : numeric check of the epsilon contraction on random antisymmetric F
rng = np.random.default_rng(7)
Fm = rng.normal(size=(4, 4)); Fm = Fm - Fm.T
eps4 = np.zeros((4, 4, 4, 4))
for p in itertools.permutations(range(4)):
    eps4[p] = np.linalg.det(np.eye(4)[list(p)])
coef_wedge = 0.25 * np.einsum('mnrs,mn,rs->', eps4, Fm, Fm)      # coefficient of d^4x in F^F, F = (1/2) F_mn dx^m dx^n
Ft = 0.5 * np.einsum('mnrs,rs->mn', eps4, Fm)
check("F^F = (1/4) eps F F d^4x = (1/2) F_mn Ftilde_mn d^4x (random antisymmetric F, exact to 1e-12)", abs(coef_wedge - 0.5 * np.einsum('mn,mn->', Fm, Ft)) < 1e-12)
check("so (1/8 pi^2) int tr F^F = (1/8 pi^2)(1/2)(1/2) int F^a Ftilde^a = (1/32 pi^2) int F^a Ftilde^a: 32 pi^2 = 8 pi^2 x 2 x 2 (tr T^aT^b = delta/2; F^F = (1/2) F Ftilde)",
      sp.Rational(1, 8) / pi**2 * sp.Rational(1, 2) * sp.Rational(1, 2) == 1 / (32 * pi**2))
check("32 pi^2 = Vol(S^3) x 16 = 2 pi^2 x 16", 32 * pi**2 == 2 * pi**2 * 16)

# ============================================================================= T3 Chern-Simons level
print("\nT3  Chern-Simons level")
k = sp.symbols('k', positive=True, integer=True)
dCS = (k / (12 * pi)) * 24 * pi**2          # (k/4pi) x (1/3) int tr (g^-1 dg)^3 with int = 24 pi^2 n
check("Delta S_CS = (k/4 pi)(1/3)(24 pi^2) = 2 pi k for a unit-winding gauge transformation (needs (1/24 pi^2) int tr(g^-1 dg)^3 = 1)", sp.simplify(dCS - 2 * pi * k) == 0)
check("consistent with the instanton: dCS = tr F^F, (1/8 pi^2) int tr F^F = 1  =>  int tr F^F = 8 pi^2 = 4 pi x 2 pi", 8 * pi**2 == 4 * pi * 2 * pi)

# ============================================================================= T4 loop factors
print("\nT4  loop factors")
Lam, m, kk = sp.symbols('Lambda m k', positive=True)
Iloop = (2 * pi**2 / (2 * pi)**4) * sp.integrate(kk**3 / (kk**2 + m**2)**2, (kk, 0, Lam))
lead = sp.simplify(sp.limit(Iloop / sp.log(Lam**2), Lam, sp.oo))
check("int d^4k/(2 pi)^4 (k^2+m^2)^-2 ~ (1/(16 pi^2)) ln(Lambda^2/m^2): coefficient of ln Lambda^2 is 1/(16 pi^2)", sp.simplify(lead - 1 / (16 * pi**2)) == 0)
check("1/(16 pi^2) = Vol(S^3)/(2 pi)^4 x (1/2) [(1/2) from int k^3 dk/k^4 = (1/2) ln Lambda^2];  Vol(S^3)/(2 pi)^4 = 1/(8 pi^2)", 2 * pi**2 / (2 * pi)**4 == 1 / (8 * pi**2) and 1 / (8 * pi**2) / 2 == 1 / (16 * pi**2))
check("32 pi^2 = 2 (4 pi)^2 = 2 x 16 pi^2: the SAME Vol(S^3) = 2 pi^2 sits in the loop measure and in the instanton integral", 32 * pi**2 == 2 * (4 * pi)**2 and 32 * pi**2 == 2 * pi**2 * 16)

# ============================================================================= T5 anomaly
print("\nT5  conformal trace anomaly and the de Sitter stress")
Rm2, Rc2, R2 = sp.symbols('Riem2 Ric2 R2')
a_s, c_s = sp.Rational(1, 360), sp.Rational(1, 120)             # per real conformal scalar, hep-th/9308075 eqs.(30),(31) as read (N_S = 1)
W2 = Rm2 - 2 * Rc2 + R2 / 3; E4s = Rm2 - 4 * Rc2 + R2
anom = sp.expand((c_s * W2 - a_s * E4s) / (16 * pi**2))
check("(1/16 pi^2)[c W^2 - a E4] with a = 1/360, c = 1/120 = (1/2880 pi^2)(Riem^2 - Ric^2): the R^2 terms cancel",
      sp.simplify(anom - (Rm2 - Rc2) / (2880 * pi**2)) == 0)
check("[bookkeeping] 2880 pi^2 = 180 x 16 pi^2 = 90 x 32 pi^2 ; 5760 pi^2 = 180 x 32 pi^2  (a_scalar/(16 pi^2) = 1/(5760 pi^2) = 1/(180 . 32 pi^2))",
      2880 * pi**2 == 180 * 16 * pi**2 == 90 * 32 * pi**2 and 5760 * pi**2 == 180 * 32 * pi**2 and a_s / (16 * pi**2) == 1 / (5760 * pi**2))
Tdesitter = anom.subs({Rm2: riemdS, Rc2: ricdS})
rho_dS = sp.simplify(-Tdesitter / 4)
check("de Sitter (conformal scalar): rho = -<T>/4 = H^4/(960 pi^2)   [Bunch-Davies vacuum value, from memory: 1/(960 pi^2)]", sp.simplify(rho_dS - H**4 / (960 * pi**2)) == 0)
integ = sp.simplify(anom.subs({Rm2: Riem2, Rc2: Ric2}) * volS4)
check("integrated anomaly on S^4: int <T> = -1/90 (any radius) = -2 a chi with a = 1/360, chi = 2  (32 pi^2 x a/(16 pi^2) x chi)", sp.simplify(integ + sp.Rational(1, 90)) == 0
      and sp.simplify(-2 * a_s * 2 + sp.Rational(1, 90)) == 0)
check("CONTROL C-T5a: a wrong a-coefficient (1/180) breaks the R^2 cancellation", sp.simplify(sp.expand((c_s * W2 - sp.Rational(1, 180) * E4s) / (16 * pi**2)).coeff(R2)) != 0)
Gs, Hs, N = sp.symbols('G H N', positive=True)
solH = sp.solve(sp.Eq(3 * Hs**2 / (8 * pi * Gs), N * Hs**4 / (960 * pi**2)), Hs)
check("semiclassical self-consistent de Sitter (N conformal scalars): 3H^2/(8 pi G) = N H^4/(960 pi^2)  =>  G H^2 = 360 pi/N  (a Planckian pure number, unrelated to a0)",
      len(solH) == 1 and sp.simplify(Gs * solH[0]**2 - 360 * pi / N) == 0)

# ============================================================================= T6 2D
print("\nT6  two dimensions (Liouville / Polyakov)")
xx, yy, cc = sp.symbols('xx yy c')
om = sp.Function('omega')(xx, yy)
g2 = sp.exp(2 * om) * sp.eye(2)
_, R2d = None, None
Gm2 = christoffel(g2, [xx, yy])
def ricci_scalar_2d(g, X):
    n = len(X); Gm = christoffel(g, X); gi = g.inv(); Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(n):
            e = 0
            for i in range(n):
                e += sp.diff(Gm[i][j][k], X[i]) - sp.diff(Gm[i][j][i], X[k])
                for l in range(n):
                    e += Gm[i][i][l] * Gm[l][j][k] - Gm[i][k][l] * Gm[l][j][i]
            Ric[j, k] = e
    return sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
R2d = ricci_scalar_2d(g2, [xx, yy])
lap = sp.diff(om, xx, 2) + sp.diff(om, yy, 2)
check("conformal gauge g = e^(2 omega) delta: R = -2 e^(-2 omega) lap(omega)", sp.simplify(R2d + 2 * sp.exp(-2 * om) * lap) == 0)
# box^-1 R = -2 omega  (box = e^-2w lap) ; sqrt(g) R box^-1 R = 4 omega lap omega
sqrtgR_boxinvR = sp.exp(2 * om) * R2d * (-2 * om)
check("sqrt(g) R box^-1 R = 4 omega lap(omega); so (c/96 pi) int R box^-1 R = (c/24 pi) int omega lap(omega)  [string-theory textbook form as quoted in hep-th/0402009 App. B: c/(24 pi)]",
      sp.simplify(sqrtgR_boxinvR - 4 * om * lap) == 0 and sp.Rational(1, 96) * 4 == sp.Rational(1, 24))
check("CONTROL C-T6a: c/(48 pi) in front of int R box^-1 R would give (c/12 pi) omega lap omega and is rejected", sp.Rational(1, 48) * 4 != sp.Rational(1, 24))
check("96 pi = 24 pi x 4 with 4 = (-2)^2 from R = -2 lap(omega); 24 pi = 12 x 2 pi.  Also int R sqrt(g) = 4 pi chi = 8 pi on S^2 (Gauss-Bonnet in 2D, cf. T1 n=1)", 96 * pi == 24 * pi * 4)

# ============================================================================= T7 spheres
print("\nT7  sphere volumes")
V = lambda n: 2 * pi**sp.Rational(n + 1, 2) / sp.gamma(sp.Rational(n + 1, 2))
check("Vol(S^1)=2 pi, Vol(S^2)=4 pi, Vol(S^3)=2 pi^2, Vol(S^4)=8 pi^2/3, Vol(S^5)=pi^3, Vol(S^6)=16 pi^3/15",
      sp.simplify(V(1) - 2 * pi) == 0 and sp.simplify(V(2) - 4 * pi) == 0 and sp.simplify(V(3) - 2 * pi**2) == 0 and sp.simplify(V(4) - 8 * pi**2 / 3) == 0
      and sp.simplify(V(5) - pi**3) == 0 and sp.simplify(V(6) - 16 * pi**3 / 15) == 0)
check("32 pi^2 = 12 Vol(S^4) = int_{S^4(1)} R dV (R = 12)", sp.simplify(12 * V(4) - 32 * pi**2) == 0)
check("CONTROL C-T7a: Vol(S^4) = 4 pi^2/3 (wrong) is rejected", sp.simplify(V(4) - 4 * pi**2 / 3) != 0)
check("32 pi^2 = (8 pi)(4 pi) = Einstein 8 pi x Vol(S^2) and 32 pi^2 = 2 (4 pi)^2 = 2 Vol(S^2)^2 = 16 Vol(S^3): four equal numbers, four different origins",
      32 * pi**2 == 8 * pi * 4 * pi == 2 * (4 * pi)**2 == 16 * V(3))

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
