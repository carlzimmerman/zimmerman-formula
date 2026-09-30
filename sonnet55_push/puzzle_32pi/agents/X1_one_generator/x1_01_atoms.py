#!/usr/bin/env python3
"""x1_01_atoms.py -- lane X1 ('one generator?'): independent recomputation of every ATOM that the X1 ledger uses.

Units c = 1, signature (-+++), G restored where it matters.  Nothing is quoted: every atom is recomputed from a metric, an integral or a tensor contraction.
Atoms (a factor that appears in the 4 pi / 8 pi / 16 pi / 32 pi family), each with the SOURCE it is recomputed from:

  S2   4 pi        solid angle of S^2 (angular integral; also the flux of 1/r^2; also the 3-d Fourier transform of 1/q^2 is 1/(4 pi r); also the heat-kernel integral)
  S3   2 pi^2      volume of S^3;   S4   8 pi^2/3   volume of S^4
  BIA  2           weak-field  G_00 = 2 Lap(Phi)  (the trace-reversal 'factor 2' of the Einstein tensor); D-dim value (D-2)/(D-3)
  QEH  1/4         sqrt(-g) R for a TT wave, O(eps^2) coefficient (Euler-operator test); D-independent (spectator directions)
  AVG  1/2         time average of cos^2
  PER  2 pi        Euclidean regularity period 2 pi/kappa of a Killing horizon
  IW   1/(16 pi G) Iyer-Wald Noether potential; horizon value kappa A/(8 pi G) = T S; entropy S = (2 pi/kappa) Q = A/4G (D-independent)
  CW   (4 pi)^n n!  Chern-Gauss-Bonnet constant;  identity (2n)! Vol(S^2n) = 2 (4 pi)^n n!  (n = 1..8)
  INS  32 pi^2      BPST instanton int F F~ (explicit self-dual field)

Also the D-lifts used later:  Poisson  Omega_{D-2},  Newton-vs-Einstein  Omega_{D-2} G_N = 8 pi G_E (D-3)/(D-2),  Wald 1/4 (D-independent),
Tangherlini  kappa r_h = (D-3)/2.

Every check that is a control (a deliberately wrong value that MUST be rejected) is labelled CONTROL.  Exit 0 iff all checks and all controls behave as declared.
Writes x1_atoms.json (read by x1_02_ledger.py).
"""
import sys, json, itertools, time
import numpy as np
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name, flush=True)
def ctl(name, cond_rejected):
    """a control: the wrong value must be rejected"""
    ok.append(bool(cond_rejected)); print(("PASS CONTROL " if cond_rejected else "FAIL CONTROL ") + name, flush=True)

T0 = time.time()
atoms = {}

# ---------------------------------------------------------------- A1 spheres, Gaussian generator of every pi
r = sp.symbols('r', positive=True)
Omega = {}
for n in range(1, 8):
    val = sp.simplify(2 * sp.pi ** sp.Rational(n + 1, 2) / sp.gamma(sp.Rational(n + 1, 2)))
    gauss = sp.integrate(r ** n * sp.exp(-r ** 2), (r, 0, sp.oo))
    chk("A1 Omega_%d = 2 pi^((n+1)/2)/Gamma((n+1)/2) fixed by Omega_n * int r^n e^-r^2 dr = pi^((n+1)/2) (the Gaussian integral): %s" % (n, val),
        sp.simplify(val * gauss - sp.pi ** sp.Rational(n + 1, 2)) == 0)
    Omega[n] = val
th, ph, chi_, psi = sp.symbols('theta phi chi psi', positive=True)
S2 = sp.integrate(sp.sin(th), (th, 0, sp.pi)) * 2 * sp.pi
S3 = sp.integrate(sp.sin(chi_) ** 2, (chi_, 0, sp.pi)) * sp.integrate(sp.sin(th), (th, 0, sp.pi)) * 2 * sp.pi
S4 = (sp.integrate(sp.sin(psi) ** 3, (psi, 0, sp.pi)) * sp.integrate(sp.sin(chi_) ** 2, (chi_, 0, sp.pi))
      * sp.integrate(sp.sin(th), (th, 0, sp.pi)) * 2 * sp.pi)
chk("A1 S2 area = 4 pi by direct angular integral", sp.simplify(S2 - 4 * sp.pi) == 0 and sp.simplify(Omega[2] - 4 * sp.pi) == 0)
chk("A1 S3 volume = 2 pi^2 by direct angular integral", sp.simplify(S3 - 2 * sp.pi ** 2) == 0 and sp.simplify(Omega[3] - 2 * sp.pi ** 2) == 0)
chk("A1 S4 volume = 8 pi^2/3 by direct angular integral", sp.simplify(S4 - 8 * sp.pi ** 2 / 3) == 0 and sp.simplify(Omega[4] - 8 * sp.pi ** 2 / 3) == 0)
ctl("A1 CONTROL: S4 volume is not 2 pi^2 (rejected)", sp.simplify(S4 - 2 * sp.pi ** 2) != 0)
atoms['S2'] = '4*pi'; atoms['S3'] = '2*pi**2'; atoms['S4'] = '8*pi**2/3'
# Gauss-Bonnet in 2-d: int K dA = 4 pi = 2 pi chi(S^2) for every radius (K = 1/R^2, A = 4 pi R^2)
Rr = sp.symbols('R', positive=True)
chk("A1 2-d Gauss-Bonnet: int_{S^2(R)} K dA = 4 pi = 2 pi chi(S^2), chi = 2, for every R", sp.simplify((1 / Rr ** 2) * 4 * sp.pi * Rr ** 2 - 2 * sp.pi * 2) == 0)

# ---------------------------------------------------------------- A2 Poisson / Fourier / heat kernel: the 4 pi of Gauss's law
R0 = sp.symbols('R0', positive=True)
phi_s = sp.Symbol('phi_s')
flux = sp.integrate(sp.integrate((1 / R0 ** 2) * R0 ** 2 * sp.sin(th), (th, 0, sp.pi)), (phi_s, 0, 2 * sp.pi))
chk("A2 Gauss flux of grad(1/r) through S^2(R0) = 4 pi, independent of R0", sp.simplify(flux - 4 * sp.pi) == 0)
q = sp.symbols('q', positive=True); rr = sp.symbols('rr', positive=True)
Ift = sp.integrate(sp.sin(q * rr) / (q * rr), (q, 0, sp.oo))
FT = sp.simplify(Ift / (2 * sp.pi ** 2))
chk("A2 3-d Fourier transform of 1/q^2 : (1/2 pi^2) int sin(qr)/(qr) dq = 1/(4 pi r)", sp.simplify(FT - 1 / (4 * sp.pi * rr)) == 0)
tt = sp.symbols('tt', positive=True)
hk = sp.integrate((4 * sp.pi * tt) ** sp.Rational(-3, 2) * sp.exp(-rr ** 2 / (4 * tt)), (tt, 0, sp.oo))
chk("A2 heat-kernel route: int_0^oo (4 pi t)^(-3/2) e^(-r^2/4t) dt = 1/(4 pi r)  (the Poisson 4 pi is (4 pi)^(3/2)/(2 sqrt pi))", sp.simplify(hk - 1 / (4 * sp.pi * rr)) == 0)
ctl("A2 CONTROL: Poisson Green function is not 1/(2 pi r)", sp.simplify(hk - 1 / (2 * sp.pi * rr)) != 0)
for d in range(3, 8):
    lhs = sp.simplify(Omega[d - 1] * (d - 2) * sp.gamma(sp.Rational(d, 2) - 1) / (4 * sp.pi ** sp.Rational(d, 2)))
    chk("A2 d = %d: Omega_{d-1} times the d-dim Green-function slope = 1 (Gauss law), so the solid angle IS the Gauss normalisation" % d, lhs == 1)

# ---------------------------------------------------------------- generic Riemann machinery (sympy)
def christoffel(g, ginv, X):
    n = len(X)
    return [[[sum(ginv[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2
              for c in range(n)] for b in range(n)] for a in range(n)]
def ricci(g, ginv, X):
    n = len(X); Gam = christoffel(g, ginv, X)
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

# ---------------------------------------------------------------- A3 BIA: weak-field G_00 = ((D-2)/(D-3)) Lap Phi   (Newtonian limit; D = 4 gives the 'factor 2')
eps = sp.symbols('epsilon')
def christoffel_diag(gd, X):
    n = len(X)
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
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
bia = {}
for D in (4, 5, 6, 7):
    X = sp.symbols('t x1:%d' % D, real=True); xs = X[1:]
    a_ = [sp.Rational(i + 2, 3) for i in range(D - 1)]                    # Phi = sum a_i x_i^2  (Lap Phi = 2 sum a_i), exact EXACT-in-eps Ricci, evaluated at a rational point
    Phi = sum(a_[i] * xs[i] ** 2 for i in range(D - 1))
    gd = [-(1 + 2 * eps * Phi)] + [(1 - 2 * eps * Phi / (D - 3))] * (D - 1)
    Gam = christoffel_diag(gd, X)
    pt = {X[i]: sp.Rational(i + 1, 7) for i in range(D)}
    first = lambda e: sp.diff(e, eps).subs(eps, 0).subs(pt)
    Rcomp = [ricci_comp(Gam, X, i, i) for i in range(D)]
    Rs_exact = sum(Rcomp[i] / gd[i] for i in range(D))                    # R = g^{aa} R_aa (diagonal metric)
    G00 = Rcomp[0] - sp.Rational(1, 2) * gd[0] * Rs_exact
    lap = 2 * sum(a_)
    R00_1 = first(Rcomp[0]); Rii_1 = [first(Rcomp[i]) for i in range(1, D)]
    chk("A3 D=%d Newtonian ansatz g00 = -(1+2Phi), g_ij = (1-2Phi/(D-3)) delta_ij: R_00 = Lap Phi and R_ii = Lap Phi/(D-3) at O(eps) (exact Ricci, then d/deps at 0)" % D,
        sp.nsimplify(R00_1 - lap) == 0 and all(sp.nsimplify(x - lap / (D - 3)) == 0 for x in Rii_1))
    ratio = sp.nsimplify(first(G00) / lap)
    chk("A3 D=%d G_00 = ((D-2)/(D-3)) Lap Phi = %s Lap Phi" % (D, ratio), ratio == sp.Rational(D - 2, D - 3))
    bia[D] = ratio
ctl("A3 CONTROL: D=4 G_00 is not 1 x Lap Phi", bia[4] != 1)
atoms['BIA_D4'] = str(bia[4])
chk("A3 so 8 pi G T_00 = G_00 gives Lap Phi = 4 pi G rho at D=4: Einstein 8 pi = BIA x Poisson 4 pi = 2 x 4 pi", sp.Rational(1, 1) * 8 * sp.pi / bia[4] == 4 * sp.pi)
for D in (4, 5, 6, 7):
    lhs = sp.simplify(Omega[D - 2] * sp.Symbol('GN'))
    rhs = 8 * sp.pi * sp.Symbol('GE') * sp.Rational(D - 3, D - 2)
    GN_over_GE = sp.simplify(rhs / lhs * sp.Symbol('GE') / sp.Symbol('GE')) / sp.Symbol('GN') * sp.Symbol('GN')
    # Omega_{D-2} G_N = 8 pi G_E (D-3)/(D-2):   G_N / G_E
    ratio = sp.simplify(8 * sp.pi * sp.Rational(D - 3, D - 2) / Omega[D - 2])
    atoms['GN_over_GE_D%d' % D] = str(ratio)
chk("A3 Newton force-law constant vs Einstein-equation constant: G_N/G_E = 1 at D=4 (the 8 pi = 2 x 4 pi coincidence), but %s at D=5, %s at D=6"
    % (sp.simplify(8 * sp.pi * sp.Rational(2, 3) / Omega[3]), sp.simplify(8 * sp.pi * sp.Rational(3, 4) / Omega[4])),
    sp.simplify(8 * sp.pi * sp.Rational(1, 2) / Omega[2]) == 1 and sp.simplify(8 * sp.pi * sp.Rational(2, 3) / Omega[3]) != 1)

# ---------------------------------------------------------------- A4 QEH: quadratic Einstein-Hilbert Lagrangian of a TT wave (Euler-operator test), D = 4, 5
def quad_TT(D):
    X = sp.symbols('t x y z', real=True) + (tuple(sp.symbols('w1:%d' % (D - 3), real=True)) if D > 4 else ())
    t_, x_, y_, z_ = X[:4]
    f = sp.Function('f')(t_, z_); gg = sp.Function('g')(t_, z_)
    n = D
    g = sp.eye(n); g[0, 0] = -1
    g[1, 1] = 1 + eps * f; g[2, 2] = 1 - eps * f; g[1, 2] = g[2, 1] = eps * gg
    det2 = 1 - eps ** 2 * (f ** 2 + gg ** 2)                                  # exact inverse of the xy block
    ginv = sp.eye(n); ginv[0, 0] = -1
    ginv[1, 1] = (1 - eps * f) / det2; ginv[2, 2] = (1 + eps * f) / det2; ginv[1, 2] = ginv[2, 1] = -eps * gg / det2
    assert sp.simplify(g * ginv - sp.eye(n)) == sp.zeros(n, n)
    Ric = ricci(g, ginv, X)
    Rs = sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n))
    L = sp.sqrt(det2) * Rs
    L2 = sp.simplify(sp.diff(L, eps, 2).subs(eps, 0) / 2)
    return t_, z_, f, gg, L2
for D in (4, 5):
    t_, z_, f, gg, L2 = quad_TT(D)
    from sympy.calculus.euler import euler_equations
    eq_c = euler_equations(L2, [f, gg], [t_, z_])
    Ltarget = sp.Rational(1, 2) * ((sp.diff(f, t_)) ** 2 - sp.diff(f, z_) ** 2) + sp.Rational(1, 2) * ((sp.diff(gg, t_)) ** 2 - sp.diff(gg, z_) ** 2)
    eq_t = euler_equations(Ltarget, [f, gg], [t_, z_])
    same = all(sp.simplify(a.lhs - a.rhs - (b.lhs - b.rhs)) == 0 for a, b in zip(eq_c, eq_t))
    chk("A4 D=%d: sqrt(-g)R at O(eps^2) for h_xx=-h_yy=f, h_xy=g equals (1/2)(fdot^2 - f'^2 + gdot^2 - g'^2) up to a total derivative "
        "= -(1/4) d_l h_ij d^l h_ij  (h_ij h_ij = 2f^2+2g^2)" % D, same)
    bad = euler_equations(sp.Rational(1, 3) * ((sp.diff(f, t_)) ** 2 - sp.diff(f, z_) ** 2) + sp.Rational(1, 3) * ((sp.diff(gg, t_)) ** 2 - sp.diff(gg, z_) ** 2), [f, gg], [t_, z_])
    ctl("A4 D=%d CONTROL: a 1/3 instead of 1/2 is rejected" % D,
        not all(sp.simplify(a.lhs - a.rhs - (b.lhs - b.rhs)) == 0 for a, b in zip(eq_c, bad)))
QEH = sp.Rational(1, 4)
atoms['QEH'] = '1/4'
G_, h0, wv = sp.symbols('G h0 omega', positive=True)
# canonical stress tensor of L = (1/16 pi G) * (1/2)(fdot^2 - f'^2)  for a plane wave f = h0 cos(w(t-z)); Isaacson (1/32 pi G) <hdot_ij hdot_ij> = (1/16 pi G) <fdot^2>
tv, zv = sp.symbols('tv zv', real=True)
fp = h0 * sp.cos(wv * (tv - zv))
rho_can = (1 / (16 * sp.pi * G_)) * sp.Rational(1, 2) * (sp.diff(fp, tv) ** 2 + sp.diff(fp, zv) ** 2)
avg = lambda e: sp.integrate(e, (tv, 0, 2 * sp.pi / wv)) * wv / (2 * sp.pi)
rho_av = sp.simplify(avg(rho_can))
hdot2 = 2 * sp.diff(fp, tv) ** 2                                      # hdot_ij hdot_ij for h_xx = -h_yy = f
isaac = sp.simplify(avg(hdot2 / (32 * sp.pi * G_)))
chk("A4 energy density of the quadratic action (canonical Hamiltonian) equals Isaacson (1/32 pi G)<hdot_ij hdot_ij> = w^2 h0^2/(32 pi G)", sp.simplify(rho_av - isaac) == 0 and sp.simplify(isaac - wv ** 2 * h0 ** 2 / (32 * sp.pi * G_)) == 0)
ctl("A4 CONTROL: Isaacson with 1/(16 pi G) would be a factor 2 too large (rejected)", sp.simplify(rho_av - 2 * isaac) != 0)
chk("A5 time average <cos^2> = 1/2", sp.simplify(avg(sp.cos(wv * (tv - zv)) ** 2) - sp.Rational(1, 2)) == 0)
atoms['AVG'] = '1/2'

# ---------------------------------------------------------------- A6 Euler characteristic constants
rng = np.random.default_rng(20260929)
def E4_of(Riem, g_inv=None):
    n = Riem.shape[0]
    Ric = np.einsum('acbc->ab', Riem); R = np.trace(Ric)
    return np.sum(Riem * Riem) - 4 * np.sum(Ric * Ric) + R ** 2
def maxsym(n, k):
    d = np.eye(n)
    return k * (np.einsum('ac,bd->abcd', d, d) - np.einsum('ad,bc->abcd', d, d))
kk = 1.0
E4s4 = E4_of(maxsym(4, kk))
chk("A6 E4 = Riem^2 - 4 Ric^2 + R^2 = 24 k^2 on S^4 (k = sectional curvature)", abs(E4s4 - 24) < 1e-12)
chk("A6 int_{S^4(L)} E4 = 24/L^4 x (8 pi^2/3) L^4 = 64 pi^2 = 32 pi^2 chi with chi = 2", sp.simplify(24 * S4 - 64 * sp.pi ** 2) == 0 and sp.simplify(24 * S4 / (32 * sp.pi ** 2)) == 2)
# S2 x S2 with curvatures k1, k2
def prod_riem(k1, k2):
    Rm = np.zeros((4, 4, 4, 4))
    Rm[:2, :2, :2, :2] = maxsym(2, k1); Rm[2:, 2:, 2:, 2:] = maxsym(2, k2)
    return Rm
E4p = E4_of(prod_riem(0.7, 1.3))
chk("A6 S^2 x S^2: E4 = 8 k1 k2 (= 2 R1 R2 with R_i = 2 k_i)", abs(E4p - 8 * 0.7 * 1.3) < 1e-12)
chk("A6 int_{S^2 x S^2} E4 = 8 k1 k2 (4 pi/k1)(4 pi/k2) = 128 pi^2 = 32 pi^2 chi with chi = 4 = chi(S^2)^2", sp.simplify(8 * (4 * sp.pi) ** 2 - 32 * sp.pi ** 2 * 4) == 0)
ctl("A6 CONTROL: 32 pi^2 chi with chi = 2 does not reproduce 128 pi^2 (rejected)", sp.simplify(8 * (4 * sp.pi) ** 2 - 32 * sp.pi ** 2 * 2) != 0)
for n in range(1, 9):
    lhs = sp.factorial(2 * n) * Omega[2 * n] if (2 * n) in Omega else sp.factorial(2 * n) * sp.simplify(2 * sp.pi ** sp.Rational(2 * n + 1, 2) / sp.gamma(sp.Rational(2 * n + 1, 2)))
    rhs = 2 * (4 * sp.pi) ** n * sp.factorial(n)
    chk("A6 Chern-Gauss-Bonnet generator: (2n)! Vol(S^{2n}) = 2 (4 pi)^n n!  (n = %d): %s" % (n, sp.simplify(lhs)), sp.simplify(lhs - rhs) == 0)
ctl("A6 CONTROL: (2n)! Vol(S^2n) != (4 pi)^n n! (missing chi = 2), n=2", sp.simplify(sp.factorial(4) * Omega[4] - (4 * sp.pi) ** 2 * 2) != 0)
atoms['CW_n2'] = '32*pi**2'
chk("A6 in D = 4: 32 pi^2 = 2 (4pi)^2 = 12 Vol(S^4) = 16 Vol(S^3) = 4 x 8 pi^2 (all equal exactly; one number, several decompositions)",
    all(sp.simplify(v - 32 * sp.pi ** 2) == 0 for v in (2 * (4 * sp.pi) ** 2, 12 * S4, 16 * S3, 4 * 8 * sp.pi ** 2)))

# ---------------------------------------------------------------- A7 BPST instanton (explicit self-dual field)
xs4 = sp.symbols('x1:5', real=True); rho = sp.symbols('rho', positive=True)
def eta(a, mu, nu):
    if mu < 3 and nu < 3:
        return sp.LeviCivita(a, mu, nu)
    if mu < 3 and nu == 3:
        return 1 if a == mu else 0
    if mu == 3 and nu < 3:
        return -1 if a == nu else 0
    return 0
x2 = sum(v ** 2 for v in xs4)
Aa = [[None] * 4 for _ in range(3)]
for a in range(3):
    for mu in range(4):
        Aa[a][mu] = 2 * sum(eta(a, mu, nu) * xs4[nu] for nu in range(4)) / (x2 + rho ** 2)
F = [[[None] * 4 for _ in range(4)] for _ in range(3)]
for a in range(3):
    for mu in range(4):
        for nu in range(4):
            comm = sum(sp.LeviCivita(a, b, c) * Aa[b][mu] * Aa[c][nu] for b in range(3) for c in range(3))
            F[a][mu][nu] = sp.simplify(sp.diff(Aa[a][nu], xs4[mu]) - sp.diff(Aa[a][mu], xs4[nu]) + comm)
FF = sp.simplify(sum(F[a][m][n] ** 2 for a in range(3) for m in range(4) for n in range(4)))
chk("A7 BPST: F^a_mn F^a_mn = 192 rho^4/(x^2+rho^2)^4", sp.simplify(FF - 192 * rho ** 4 / (x2 + rho ** 2) ** 4) == 0)
selfdual = all(sp.simplify(F[a][m][n] - sp.Rational(1, 2) * sum(sp.LeviCivita(m, n, p, s) * F[a][p][s] for p in range(4) for s in range(4))) == 0
               for a in range(3) for m in range(4) for n in range(m + 1, 4))
chk("A7 BPST field is self-dual (F = F~), so F F~ = F F", selfdual)
rs = sp.symbols('rs', positive=True)
Iins = sp.integrate(2 * sp.pi ** 2 * rs ** 3 * 192 * rho ** 4 / (rs ** 2 + rho ** 2) ** 4, (rs, 0, sp.oo))
chk("A7 int d^4x F^a F~^a = Vol(S^3) x int r^3 (192 rho^4/(r^2+rho^2)^4) dr = 2 pi^2 x 16 = 32 pi^2, independent of rho", sp.simplify(Iins - 32 * sp.pi ** 2) == 0)
ctl("A7 CONTROL: instanton integral is not 16 pi^2 (rejected)", sp.simplify(Iins - 16 * sp.pi ** 2) != 0)
atoms['INS'] = '32*pi**2'

# ---------------------------------------------------------------- A8 Noether potential / Komar / Smarr / entropy / temperature, from the metric
Rsym, Msym, Gs, Lsym = sp.symbols('r M G L', positive=True)
tc, thc, phc = sp.symbols('t theta phi', real=True)
def noether_Q(fr):
    Xc = (tc, Rsym, thc, phc)
    g = sp.diag(-fr, 1 / fr, Rsym ** 2, Rsym ** 2 * sp.sin(thc) ** 2); gi = g.inv()
    Gam = christoffel(g, gi, Xc)
    xi_low = [g[i, 0] for i in range(4)]                                # xi = d_t
    nab = sp.Matrix(4, 4, lambda m, n: sp.diff(xi_low[n], Xc[m]) - sum(Gam[l][m][n] * xi_low[l] for l in range(4)))  # nab_m xi_n
    up = gi * nab * gi                                                    # nabla^m xi^n
    sqrtg = Rsym ** 2 * sp.sin(thc)
    # eps_{trth ph} = sqrtg ; Q_{th ph} = -(1/16 pi G) eps_{th ph a b} nabla^a xi^b = -(1/16 pi G) sqrtg (nabla^t xi^r - nabla^r xi^t)
    Qthph = -(1 / (16 * sp.pi * Gs)) * sqrtg * (up[0, 1] - up[1, 0])
    return sp.simplify(sp.integrate(sp.integrate(Qthph, (thc, 0, sp.pi)), (phc, 0, 2 * sp.pi)))
fgen = sp.Function('f')(Rsym)
Qgen = noether_Q(fgen)
chk("A8 Iyer-Wald Noether charge of xi = d_t through a coordinate sphere of any static metric: Q(r) = r^2 f'(r)/(4G)", sp.simplify(Qgen - Rsym ** 2 * sp.diff(fgen, Rsym) / (4 * Gs)) == 0)
Qsch = noether_Q(1 - 2 * Gs * Msym / Rsym)
chk("A8 Schwarzschild: Q = M/2 at every radius (so Komar M = 2 Q and Q integrates the 1/(16 pi G) potential)", sp.simplify(Qsch - Msym / 2) == 0)
Qds = noether_Q(1 - Rsym ** 2 / Lsym ** 2)
chk("A8 de Sitter static patch: Q(r) = -r^3/(2 G L^2)", sp.simplify(Qds + Rsym ** 3 / (2 * Gs * Lsym ** 2)) == 0)
# horizon values: Q_H = kappa A/(8 pi G), S = 2 pi Q_H/kappa = A/4G
rh = 2 * Gs * Msym; kap = sp.simplify(sp.diff(1 - 2 * Gs * Msym / Rsym, Rsym).subs(Rsym, rh) / 2); Ah = 4 * sp.pi * rh ** 2
chk("A8 Schwarzschild horizon: kappa = f'(r_h)/2 = 1/(4 G M); Q_H = M/2 = kappa A/(8 pi G) = T S", sp.simplify(kap - 1 / (4 * Gs * Msym)) == 0 and sp.simplify(Qsch - kap * Ah / (8 * sp.pi * Gs)) == 0)
chk("A8 S = (2 pi/kappa) Q_H = A/(4G): the 1/4 = (2 pi)/(8 pi)  [thermal period over Einstein coupling]", sp.simplify(2 * sp.pi / kap * Qsch - Ah / (4 * Gs)) == 0)
chk("A8 Smarr: M = kappa A/(4 pi G) = 2 T S (Komar 1/(4 pi) = solid-angle normalisation)", sp.simplify(kap * Ah / (4 * sp.pi * Gs) - Msym) == 0)
ctl("A8 CONTROL: S = (2 pi/kappa) Q_H with the Komar normalisation (2Q) would give A/2G (rejected)", sp.simplify(2 * sp.pi / kap * 2 * Qsch - Ah / (4 * Gs)) != 0)
# Euclidean regularity period: near-horizon of  f dtau^2 + dr^2/f  (genuine expansion, not a restated identity)
uu, up_, fp1 = sp.symbols('u up fp1', positive=True)
frh = 1 - 2 * Gs * Msym / Rsym
fprime_h = sp.simplify(sp.diff(frh, Rsym).subs(Rsym, rh))                    # f'(r_h) = 2 kappa
f_series = sp.series(frh.subs(Rsym, rh + uu), uu, 0, 2).removeO()             # f ~ f'(r_h) u
chk("A8 near-horizon expansion: f = f'(r_h) (r - r_h) + O(u^2)", sp.simplify(f_series - fprime_h * uu) == 0)
s_of_u = sp.integrate(1 / sp.sqrt(fp1 * up_), (up_, 0, uu))                    # proper radial distance s(u)
u_of_s = sp.solve(sp.Eq(sp.Symbol('s', positive=True), s_of_u), uu)[0]
fs = sp.simplify((fp1 * uu).subs(uu, u_of_s))
kap_sym = fp1 / 2
chk("A8 temperature: proper distance s = 2 sqrt(u/f'), so f = (f'/2)^2 s^2 = kappa^2 s^2 and  kappa^2 s^2 dtau^2 + ds^2 is the plane in polar coordinates iff tau ~ tau + 2 pi/kappa  (T = kappa/2 pi)",
    sp.simplify(fs - kap_sym ** 2 * sp.Symbol('s', positive=True) ** 2) == 0 and sp.simplify(fprime_h / 2 - kap) == 0)
atoms['PER'] = '2*pi'; atoms['IW'] = '1/(16*pi*G)'

# ---------------------------------------------------------------- A9 free fall, Friedmann, dS/Schwarzschild dimensionless products
r0, Mm, rr2 = sp.symbols('r0 M rr2', positive=True)
tff = sp.integrate(1 / sp.sqrt(2 * Gs * Mm * (1 / rr2 - 1 / r0)), (rr2, 0, r0))
rho_ball = Mm / (4 * sp.pi * r0 ** 3 / 3)
chk("A9 free fall: G rho t_ff^2 = 3 pi/32 (exact integral)", sp.simplify(Gs * rho_ball * tff ** 2 - 3 * sp.pi / 32) == 0)
tsym, a0c = sp.symbols('t'), sp.Function('a')
Xf = sp.symbols('t x y z', real=True); af = sp.Function('a')(Xf[0])
gF = sp.diag(-1, af ** 2, af ** 2, af ** 2); RicF = ricci(gF, gF.inv(), Xf)
RsF = sum(gF.inv()[i, i] * RicF[i, i] for i in range(4)); G00F = sp.simplify(RicF[0, 0] - sp.Rational(1, 2) * gF[0, 0] * RsF)
Hh = sp.diff(af, Xf[0]) / af
chk("A9 FRW: G_00 = 3 H^2, so H^2 = (8 pi/3) G rho: 8 pi/3 = 8 pi x (1/3) with 3 = dim SO(3)", sp.simplify(G00F - 3 * Hh ** 2) == 0)
chk("A9 de Sitter: A Lambda = 4 pi L^2 x 3/L^2 = 12 pi ;  Schwarzschild: A kappa^2 = pi", sp.simplify(4 * sp.pi * Lsym ** 2 * 3 / Lsym ** 2 - 12 * sp.pi) == 0 and sp.simplify(Ah * kap ** 2 - sp.pi) == 0)

print("\n%d/%d checks and controls behave as declared  (%.1f s)" % (sum(ok), len(ok), time.time() - T0))
json.dump(atoms, open(__file__.replace('x1_01_atoms.py', 'x1_atoms.json'), 'w'), indent=1)
sys.exit(0 if all(ok) else 1)
