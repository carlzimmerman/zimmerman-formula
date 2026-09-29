#!/usr/bin/env python3
"""d2_spectral_sphere.py -- spectral (heat-kernel / zeta) quantities of a Gaussian filter S_h = exp(b Lap) on the compact leaves S^3, T^3 and on S^4,
with b/L^2 = eps a pure number.  Question (task item 4): does any REGULARISED spectral quantity equal 32 pi^2, 32 pi, 32 pi/3 (or Z = sqrt(32 pi/3))?

PRE-DECLARED (written before running):
  H1  On S^3 the heat trace is T(eps) = sum_{l>=0} (l+1)^2 exp(-eps l(l+2)) = e^{eps} (sqrt(pi)/4) eps^{-3/2} [1 + 2 sum_{m>=1}(1 - 2 pi^2 m^2/eps) e^{-pi^2 m^2/eps}]
      (Poisson dual: this is where pi shows up); its small-eps series has only half-integer powers of eps, so the constant (zeta(0)) term of the heat trace is 0.
  H2  On S^4 every heat-kernel coefficient, normalised with (4 pi)^(-2), is RATIONAL: T(eps) = 1/(6 eps^2) + 1/(3 eps) + 29/90 + O(eps) (minimal scalar), -1/90 for the conformal scalar.
  H3  pi-parity: (4 pi)^(-d/2) Vol(S^d) is rational for even d and (rational) x sqrt(pi) for odd d; on T^d it is (rational) x pi^(-d/2).  The record's filter is SPATIAL
      (d = 3): its single-trace quantities have HALF-integer pi-parity, so they can never equal a target with integer pi-parity (32 pi/3, 32 pi^2, 8 pi/3), up to algebraic factors.
  H4  The only spectral quantity equal to 32 pi^2 is the un-normalised de Rham supertrace of a_2 on S^4, (4 pi)^2 chi(S^4) = 32 pi^2, which is independent of eps (McKean-Singer).
  H5  T(eps) is strictly decreasing from +inf to 1, so ANY target > 1 is hit at exactly one eps*: a hit by solving for b is guaranteed and means nothing; the eps* that
      the targets would need are compared with the ONLY principled values declared below and with the record's xi window.

PRINCIPLED eps (declared before evaluating any target): P1 xi = L (b = xi^2/2, eps = 1/2); P2 b = L^2 (eps = 1); P3 xi = Rindler length c^2/a0 with L = c/H_Lambda,
    i.e. eps = Z^2/2 = 16 pi/3 (uses the puzzle's own relation -- circular, reported only); P4 the record's window xi in [0.0243 pc, 100 pc] (derivation_chain FP14/FP17) with L = c/H_Lambda.
Exit 0 iff all checks (including controls) held.
"""
import sys
import sympy as sp
import mpmath as mp
import numpy as np

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


mp.mp.dps = 50
pi = mp.pi
Z2 = 32 * pi / 3
Z = mp.sqrt(Z2)

# ------------------------------------------------------------------------------------------------------------------
# 0. curvature invariants of the round spheres (from the metric) -> Gilkey a_1, a_2 for the scalar Laplacian
# ------------------------------------------------------------------------------------------------------------------
print("== 0. Seeley-DeWitt data of S^3, S^4 from explicit curvature tensors (Gilkey; Vassilevich arXiv:hep-th/0306138)")


def sphere_invariants(d):
    xs = sp.symbols('x0:%d' % d, real=True)
    # unit sphere: dx0^2 + sin^2(x0)[dx1^2 + sin^2(x1)[dx2^2 + ...]]
    g = sp.zeros(d, d)
    fac = 1
    for i in range(d):
        g[i, i] = fac
        fac = fac * sp.sin(xs[i]) ** 2
    ginv = g.inv()
    Gam = [[[sp.simplify(sum(ginv[i, l] * (sp.diff(g[l, j], xs[k]) + sp.diff(g[l, k], xs[j]) - sp.diff(g[j, k], xs[l])) for l in range(d)) / 2)
             for k in range(d)] for j in range(d)] for i in range(d)]
    def Riem(i, j, k, l):   # R^i_{jkl}
        return sp.simplify(sp.diff(Gam[i][j][l], xs[k]) - sp.diff(Gam[i][j][k], xs[l]) +
                           sum(Gam[i][k][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][k] for m in range(d)))
    Rm = {(i, j, k, l): Riem(i, j, k, l) for i in range(d) for j in range(d) for k in range(d) for l in range(d)}
    Ric = sp.Matrix(d, d, lambda j, l: sp.simplify(sum(Rm[(i, j, i, l)] for i in range(d))))
    Rs = sp.simplify(sum(ginv[j, l] * Ric[j, l] for j in range(d) for l in range(d)))
    Ric2 = sp.simplify(sum(ginv[a, c] * ginv[b, e] * Ric[a, b] * Ric[c, e] for a in range(d) for b in range(d) for c in range(d) for e in range(d)))
    # |Riem|^2 = R_{ijkl}R^{ijkl}: metric is diagonal
    Rd = {}
    for (i, j, k, l), v in Rm.items():
        if v != 0:
            Rd[(i, j, k, l)] = sp.simplify(g[i, i] * v)          # R_{ijkl}
    Riem2 = 0
    for (i, j, k, l), v in Rd.items():
        Riem2 += v * v * ginv[i, i] * ginv[j, j] * ginv[k, k] * ginv[l, l]
    return Rs, Ric2, sp.simplify(Riem2)


inv = {}
for d in (3, 4):
    inv[d] = sphere_invariants(d)
    print("   S^%d (unit): R = %s, |Ric|^2 = %s, |Riem|^2 = %s" % ((d,) + tuple(inv[d])))
chk("0a curvature invariants of the unit S^d: R = d(d-1), |Ric|^2 = d(d-1)^2, |Riem|^2 = 2d(d-1)  (d = 3, 4, from the metric)",
    all(inv[d] == (d * (d - 1), d * (d - 1)**2, 2 * d * (d - 1)) for d in (3, 4)))
a1 = {d: sp.Rational(inv[d][0]) / 6 for d in (3, 4)}
a2 = {d: (sp.Rational(inv[d][2]) - sp.Rational(inv[d][1])) / 180 + sp.Rational(inv[d][0])**2 / 72 for d in (3, 4)}      # E = 0, Lap R = 0, minimal scalar
print("   Gilkey for -Lap:  S^3: a_1 = %s, a_2 = %s ;  S^4: a_1 = %s, a_2 = %s   (units L^-2, L^-4)" % (a1[3], a2[3], a1[4], a2[4]))
# conformal scalar -Lap + R/6: E = -R/6, a_1 = R/6 + E = 0 ; a_2 = (Riem2 - Ric2)/180 + (R/6+E)^2/2 = (Riem2-Ric2)/180  (Lap R = 0)
a2conf = (sp.Rational(inv[4][2]) - sp.Rational(inv[4][1])) / 180
Vol4 = 8 * sp.pi**2 / 3
Vol3 = 2 * sp.pi**2
B4_min = sp.simplify(Vol4 / (16 * sp.pi**2) * a2[4])
B4_conf = sp.simplify(Vol4 / (16 * sp.pi**2) * a2conf)
print("   integrated (4 pi)^(-2) Vol a_2:  minimal scalar %s ; conformal scalar %s" % (B4_min, B4_conf))
chk("0b Gilkey: S^3 a_1 = 1, a_2 = 1/2 (= 1/n! pattern); S^4 minimal scalar (4 pi)^-2 Vol a_2 = 29/90; conformal scalar = -1/90",
    a1[3] == 1 and a2[3] == sp.Rational(1, 2) and B4_min == sp.Rational(29, 90) and B4_conf == sp.Rational(-1, 90))

# ------------------------------------------------------------------------------------------------------------------
# 1. S^3: exact heat trace, Poisson dual, series, Weyl law, zeta(0)
# ------------------------------------------------------------------------------------------------------------------
print("\n== 1. S^3 (unit radius; eps = b/L^2):  T3(eps) = sum (l+1)^2 exp(-eps l(l+2))")


def T3(eps, lmax=None):
    eps = mp.mpf(eps)
    if lmax is None:
        lmax = int(mp.sqrt(140 / eps)) + 10 if eps > 0 else 10**6
    return mp.fsum((l + 1)**2 * mp.e**(-eps * l * (l + 2)) for l in range(0, lmax + 1))


def T3_dual(eps):
    eps = mp.mpf(eps)
    s = 1 + 2 * mp.fsum((1 - 2 * pi**2 * m**2 / eps) * mp.e**(-pi**2 * m**2 / eps) for m in range(1, 60))
    return mp.e**eps * mp.sqrt(pi) / 4 * eps**mp.mpf(-1.5) * s


eps_list = [mp.mpf('0.05'), mp.mpf('0.18'), mp.mpf('0.5'), mp.mpf(1), mp.mpf(2), 16 * pi / 3]
dev = max(abs(T3(e) / T3_dual(e) - 1) for e in eps_list)
chk("1a Poisson-resummed form equals the l-sum at 50 digits for eps = 0.05, 0.18, 1/2, 1, 2, 16 pi/3 (max rel dev %s): the pi lives in the DUAL representation only" % mp.nstr(dev, 3),
    dev < mp.mpf(10)**-40)
# control: a wrong dual (missing e^eps factor) must fail
dev_bad = abs(T3(mp.mpf('0.5')) / (T3_dual(mp.mpf('0.5')) / mp.e**mp.mpf('0.5')) - 1)
chk("1b CONTROL: the dual form without the curvature factor e^eps differs from the l-sum by %s (test can fail)" % mp.nstr(dev_bad, 3), dev_bad > 0.3)

E = sp.symbols('epsilon', positive=True)
coeffs = sp.series(sp.exp(E), E, 0, 3).removeO()          # T3 = (sqrt(pi)/4) eps^(-3/2) e^eps up to exponentially small terms
chk("1c small-eps series of T3: (sqrt(pi)/4) eps^(-3/2) (1 + eps + eps^2/2 + ...), i.e. a_0 = 1, a_1 = 1, a_2 = 1/2 (Gilkey, 0b); only HALF-integer powers of eps => heat-trace constant term = 0",
    sp.simplify(coeffs - (1 + E + E**2 / 2)) == 0 and a1[3] == 1 and a2[3] == sp.Rational(1, 2))
# (4 pi b)^(-3/2) Vol(S^3) = sqrt(pi)/4 eps^(-3/2)
chk("1d Vol(S^3)/(4 pi b)^(3/2) = (sqrt(pi)/4) (L^2/b)^(3/2): the filter's pi^(-3/2) times the volume's pi^2 leaves pi^(1/2)  (half-integer parity)",
    sp.simplify(Vol3 / (4 * sp.pi * E)**sp.Rational(3, 2) - sp.sqrt(sp.pi) / 4 * E**sp.Rational(-3, 2)) == 0)
# Weyl law: N(lambda) ~ omega_3 Vol lambda^{3/2}/(2 pi)^3 = L^3 lambda^{3/2}/3 : pi cancels
weyl = sp.simplify(sp.Rational(4, 3) * sp.pi * Vol3 / (2 * sp.pi)**3)
Nn = lambda nmax: sum(n**2 for n in range(1, nmax + 1))
ratio = Nn(4000) / (4000**3 / 3.0)
chk("1e Weyl law on S^3: coefficient omega_3 Vol/(2 pi)^3 = %s (no pi); exact count/(n^3/3) at n = 4000 is %.6f -> 1" % (weyl, ratio), weyl == sp.Rational(1, 3) and abs(ratio - 1) < 1e-3)
# zeta(0)
zeta0_S3 = (mp.zeta(-2) - 1)                                            # k = 0 term; k >= 1 terms carry a factor s and no pole -> 0
chk("1f zeta_{S^3}(0) = zeta_R(-2) - 1 = -1 (zero mode removed), so the heat-trace constant term is 0 (H1)", abs(zeta0_S3 + 1) < mp.mpf(10)**-40)

# ------------------------------------------------------------------------------------------------------------------
# 2. S^4: heat trace coefficients (Euler-Maclaurin), zeta(0) by Hurwitz continuation, minimal and conformal scalar
# ------------------------------------------------------------------------------------------------------------------
print("\n== 2. S^4 (unit radius):  eigenvalue l(l+3), degeneracy (2l+3)(l+1)(l+2)/6;  n = l + 3/2")
x = sp.symbols('x')
Es = sp.symbols('e', positive=True)


def heat_series_S4(c, order=6):
    """asymptotic series of e^{c e} sum_{n=3/2,5/2,..} (n^3 - n/4)/3 exp(-e n^2)  (eigenvalue n^2 - c); the n = 1/2 term vanishes so the sum may start there"""
    f = sp.Rational(1, 3) * (x**3 - x / 4) * sum((-Es)**m * x**(2 * m) / sp.factorial(m) for m in range(0, order + 2))
    integral = sp.Rational(1, 3) * (sp.Rational(1, 2) / Es**2 - sp.Rational(1, 4) / (2 * Es))
    corr = 0
    for j in range(2, 2 * order + 2, 2):
        fj = sp.diff(f, x, j - 1).subs(x, 0)
        Bj = (sp.Integer(2)**(1 - j) - 1) * sp.bernoulli(j)                          # B_j(1/2)
        corr += -Bj / sp.factorial(j) * fj
    tot = sp.expand(sp.series(sp.exp(c * Es) * (integral + corr), Es, 0, 3).removeO())
    return tot


ser_min = heat_series_S4(sp.Rational(9, 4))
ser_con = heat_series_S4(sp.Rational(1, 4))
print("   minimal scalar   T4(e) ~", ser_min)
print("   conformal scalar Tc(e) ~", ser_con)
chk("2a minimal scalar: T4 = 1/(6 e^2) + 1/(3 e) + 29/90 + O(e)  (a_0 = 1, a_1 = R/6 = 2, a_2 = 29/15 in units of L; (4 pi)^-2 Vol = 1/6)",
    sp.simplify(ser_min.coeff(Es, -2) - sp.Rational(1, 6)) == 0 and sp.simplify(ser_min.coeff(Es, -1) - sp.Rational(1, 3)) == 0 and
    sp.simplify(ser_min.coeff(Es, 0) - sp.Rational(29, 90)) == 0)
chk("2b conformal scalar (-Lap + R/6): Tc = 1/(6 e^2) + 0/e - 1/90 + O(e)  (a_1 = 0)",
    sp.simplify(ser_con.coeff(Es, -2) - sp.Rational(1, 6)) == 0 and sp.simplify(ser_con.coeff(Es, -1)) == 0 and sp.simplify(ser_con.coeff(Es, 0) + sp.Rational(1, 90)) == 0)
chk("2c the same constants equal Gilkey's integrated a_2 from the curvature tensors (0b): 29/90 and -1/90 -- independent routes (spectrum vs curvature) agree",
    sp.simplify(ser_min.coeff(Es, 0) - B4_min) == 0 and sp.simplify(ser_con.coeff(Es, 0) - B4_conf) == 0)


def T4_num(eps, c=mp.mpf(0)):
    eps = mp.mpf(eps)
    lmax = int(mp.sqrt(160 / eps)) + 20
    return mp.fsum((2 * l + 3) * (l + 1) * (l + 2) / mp.mpf(6) * mp.e**(-eps * (l * (l + 3) + c)) for l in range(0, lmax + 1))


e1, e2 = mp.mpf('0.002'), mp.mpf('0.001')
r1 = T4_num(e1) - 1 / (6 * e1**2) - 1 / (3 * e1)
r2 = T4_num(e2) - 1 / (6 * e2**2) - 1 / (3 * e2)
lin = 2 * r2 - r1                                                       # Richardson: constant term
chk("2d direct l-sum of the S^4 heat trace at e = 1e-3, 2e-3 minus the two singular terms, Richardson-extrapolated = %s (29/90 = %s)" % (mp.nstr(lin, 8), mp.nstr(mp.mpf(29) / 90, 8)),
    abs(lin - mp.mpf(29) / 90) < 2e-5)
# zeta(0) by Hurwitz continuation
n = sp.symbols('n')


def zeta0_S4(cc, a_start):
    """zeta(0) of eigenvalue n^2 - cc, degeneracy (n^3 - n/4)/3, n = a_start, a_start+1, ... (pole terms of Hurwitz zeta at 2s+2k-3 = 1, 2s+2k-1 = 1 included)"""
    a_h = sp.nsimplify(a_start)
    zH = lambda m: -sp.bernoulli(m + 1, a_h) / (m + 1)                    # zeta_H(-m, a)
    k0 = sp.Rational(1, 3) * (zH(3) - sp.Rational(1, 4) * zH(1))
    # poles: n^{-1-2s} coefficient of the k-expansion:  (s)_k/k! cc^k c_n ; zeta_H(1+2s,a) ~ 1/(2s)
    pole = sp.Rational(1, 3) * (cc**2 / 2) * sp.Rational(1, 2) - sp.Rational(1, 12) * cc * sp.Rational(1, 2)
    return sp.simplify(k0 + pole)


z0_min = zeta0_S4(sp.Rational(9, 4), sp.Rational(5, 2))
z0_con = zeta0_S4(sp.Rational(1, 4), sp.Rational(3, 2))
chk("2e zeta(0): minimal scalar (zero mode removed) = %s = 29/90 - 1 ; conformal scalar = %s = -1/90  (Hurwitz continuation, exact)" % (z0_min, z0_con),
    z0_min == sp.Rational(29, 90) - 1 and z0_con == sp.Rational(-1, 90))

# de Rham complex: Str exp(-t Delta) = chi(S^4) = 2 for every t (McKean-Singer), and (4 pi)^2 chi = 32 pi^2
def C_forms(eps, p):
    """coexact p-forms on S^4, l >= 1: eigenvalue (l+p)(l+3-p); p = 0,3 -> deg (2l+3)(l+1)(l+2)/6 ; p = 1,2 -> deg (2l+3) l (l+3)/2"""
    eps = mp.mpf(eps)
    lmax = int(mp.sqrt(160 / eps)) + 20
    tot = mp.mpf(0)
    for l in range(1, lmax + 1):
        lam = (l + p) * (l + 3 - p)
        deg = mp.mpf((2 * l + 3) * (l + 1) * (l + 2)) / 6 if p in (0, 3) else mp.mpf((2 * l + 3) * l * (l + 3)) / 2
        tot += deg * mp.e**(-eps * lam)
    return tot


def Str(eps, drop_b4=False):
    C = [C_forms(eps, p) for p in range(4)]
    b = [1, 0, 0, 0, 0 if drop_b4 else 1]
    Tr = []
    for p in range(5):
        Tr.append(b[p] + (C[p] if p <= 3 else 0) + (C[p - 1] if p >= 1 else 0))
    return sum((-1)**p * Tr[p] for p in range(5)), Tr


vals = [Str(e)[0] for e in (mp.mpf('0.01'), mp.mpf('0.3'), mp.mpf(1), 16 * pi / 3)]
chk("2f de Rham supertrace sum_p (-1)^p Tr e^{-eps Delta_p} = 2 = chi(S^4) at eps = 0.01, 0.3, 1, 16 pi/3 (spread %s): the filter width drops out of the Euler characteristic" % mp.nstr(max(abs(v - 2) for v in vals), 3),
    all(abs(v - 2) < mp.mpf(10)**-30 for v in vals))
chk("2g CONTROL: dropping the harmonic 4-form gives 1, not 2: the supertrace test can fail", abs(Str(mp.mpf('0.3'), drop_b4=True)[0] - 1) < mp.mpf(10)**-30)
Tr1 = Str(mp.mpf('0.002'))[1]
chk("2h leading behaviour Tr_p ~ C(4,p)/(6 e^2) (ranks 1,4,6,4,1): the p-form spectra used are consistent (Tr_1 * 6e^2 = %s at e = 0.002)" % mp.nstr(Tr1[1] * 6 * mp.mpf('0.002')**2, 5),
    abs(Tr1[1] * 6 * mp.mpf('0.002')**2 - 4) < 0.08 and abs(Tr1[2] * 6 * mp.mpf('0.002')**2 - 6) < 0.15)
chk("2i (4 pi)^2 chi(S^4) = 32 pi^2 = 12 Vol(S^4_unit) = 6 x [(1/6) int R dV]: the ONLY spectral quantity equal to 32 pi^2 is this eps-independent integer times (4 pi)^2",
    sp.simplify((4 * sp.pi)**2 * 2 - 32 * sp.pi**2) == 0 and sp.simplify(12 * Vol4 - 32 * sp.pi**2) == 0)

# a regularised spectral SUM (Casimir-type) on S^3: E = (1/2) sum n^2 * n (conformal scalar, omega_n = n/L), exponential cutoff lambda: finite part = zeta_R(-3)/2 = 1/240
def casimir_S3(lam):
    lam = mp.mpf(lam)
    q_ = mp.e**(-lam)
    li = q_ * (1 + 4 * q_ + q_**2) / (1 - q_)**4                       # sum n^3 q^n
    return li / 2
fin = casimir_S3(mp.mpf('1e-3')) - 3 / mp.mpf('1e-3')**4
chk("2j Casimir-type regularised sum on S^3 (conformal scalar, omega_n = n/L): (1/2) sum n^3 e^{-lambda n} = 3/lambda^4 + 1/240 + O(lambda^2); finite part = %s (1/240 = %s): RATIONAL; pi appears only if one divides by Vol(S^3) = 2 pi^2 L^3 to form a density (rho = 1/(480 pi^2 L^4), an hbar-carrying quantity)" % (mp.nstr(fin, 10), mp.nstr(mp.mpf(1) / 240, 10)),
    abs(fin - mp.mpf(1) / 240) < 1e-6)

# ------------------------------------------------------------------------------------------------------------------
# 3. T^3 (flat compact leaf, side l = 1): Tr = theta_3(e^{-4 pi^2 b})^3 = (4 pi b)^(-3/2) theta_3(e^{-1/4b})^3
# ------------------------------------------------------------------------------------------------------------------
print("\n== 3. T^3 (side 1)")
th3 = lambda q, N=200: 1 + 2 * mp.fsum(q**(k * k) for k in range(1, N))
def T_T3(b):
    b = mp.mpf(b)
    return th3(mp.e**(-4 * pi**2 * b))**3


def T_T3_dual(b):
    b = mp.mpf(b)
    return (4 * pi * b)**mp.mpf(-1.5) * th3(mp.e**(-1 / (4 * b)))**3


devT = max(abs(T_T3(b) / T_T3_dual(b) - 1) for b in ('0.001', '0.01', '0.05', '0.3', '1'))
chk("3a T^3 heat trace: sum_n e^{-4 pi^2 b |n|^2} = (4 pi b)^(-3/2) theta_3(e^{-1/(4b)})^3 at 50 digits (max rel dev %s): pi^(-3/2) prefactor, no pi in the volume" % mp.nstr(devT, 3), devT < mp.mpf(10)**-40)

# ------------------------------------------------------------------------------------------------------------------
# 4. pi-parity theorem
# ------------------------------------------------------------------------------------------------------------------
print("\n== 4. pi-parity of the normalised volume  Vol(S^d)/(4 pi)^{d/2}")
par_ok = True
par = {}
for d in range(1, 10):
    val = 2 * sp.pi**sp.Rational(d + 1, 2) / (sp.gamma(sp.Rational(d + 1, 2)) * (4 * sp.pi)**sp.Rational(d, 2))
    val = sp.simplify(sp.gammasimp(val))
    q = sp.simplify(val / (1 if d % 2 == 0 else sp.sqrt(sp.pi)))
    par[d] = (q, 'rational' if d % 2 == 0 else 'rational x sqrt(pi)')
    par_ok = par_ok and q.is_rational
print("   d: value  ", {d: (sp.simplify(par[d][0]), par[d][1]) for d in (2, 3, 4, 5)})
chk("4a Vol(S^d)/(4 pi)^{d/2} is rational for even d and rational x sqrt(pi) for odd d, d = 1..9 (so heat-trace quantities have integer parity on S^4, half-integer parity on S^3)", par_ok)
# Lindemann-type consequence: rational x sqrt(pi) cannot equal a rational x pi^k with k integer
def alg_ratio(target_fn, base_fn, deg=4, maxc=10**4, dps=150):
    """True iff target/base has a minimal polynomial of degree <= deg with integer coeffs <= maxc (searched at `dps` digits: 5*4 = 20 digits of freedom << dps, no spurious hits)"""
    with mp.workdps(dps):
        v = target_fn() / base_fn()
        try:
            return mp.findpoly(v, deg, maxcoeff=maxc, maxsteps=500000, tol=mp.mpf(10)**(-dps + 20)) is not None
        except Exception:
            return False


tgf = {"Z=sqrt(32pi/3)": lambda: mp.sqrt(32 * mp.pi / 3), "sqrt(8pi/3)": lambda: mp.sqrt(8 * mp.pi / 3), "Z^2=32pi/3": lambda: 32 * mp.pi / 3,
       "32 pi": lambda: 32 * mp.pi, "32 pi^2": lambda: 32 * mp.pi**2, "8pi/3": lambda: 8 * mp.pi / 3}
base_S3 = lambda: mp.sqrt(mp.pi) / 4                                        # S^3 Weyl coefficient (Vol/(4 pi)^{3/2} at L = b = 1)
base_T3 = lambda: (4 * mp.pi)**mp.mpf(-1.5)                                 # T^3 (side 1)
base_S4 = lambda: mp.mpf(1) / 6                                             # S^4
alg_S3 = {k: alg_ratio(f, base_S3) for k, f in tgf.items()}
alg_T3 = {k: alg_ratio(f, base_T3) for k, f in tgf.items()}
alg_S4 = {k: alg_ratio(f, base_S4) for k, f in tgf.items()}
print("   target / (S^3 single-trace coefficient sqrt(pi)/4) has degree<=4 minimal polynomial?", alg_S3)
print("   target / (T^3 coefficient (4 pi)^(-3/2))?                                            ", alg_T3)
print("   target / (S^4 coefficient 1/6)?                                                       ", alg_S4)
with mp.workdps(150):
    ctrl_alg = (mp.findpoly(3 * mp.sqrt(2) + 1, 4, maxcoeff=10**4, maxsteps=500000, tol=mp.mpf(10)**-130) is not None
                and mp.findpoly(mp.pi, 4, maxcoeff=10**4, maxsteps=500000, tol=mp.mpf(10)**-130) is None
                and mp.findpoly(mp.sqrt(mp.pi), 4, maxcoeff=10**4, maxsteps=500000, tol=mp.mpf(10)**-130) is None)
chk("4b integer-relation test of parity (150 digits): Z and sqrt(8 pi/3) (parity 1/2) are ALGEBRAIC multiples of the S^3 single-trace coefficient sqrt(pi)/4, while Z^2, 32 pi, 32 pi^2, 8 pi/3 (integer parity) are not; on T^3 (coefficient pi^(-3/2)) no target matches and on S^4 (rational coefficient) no target matches; control: the search finds 3 sqrt2 + 1 and rejects pi, sqrt(pi)",
    alg_S3["Z=sqrt(32pi/3)"] and alg_S3["sqrt(8pi/3)"] and not any(alg_S3[k] for k in ("Z^2=32pi/3", "32 pi", "32 pi^2", "8pi/3")) and
    not any(alg_T3.values()) and not any(alg_S4.values()) and ctrl_alg)
# a control: the parity test can fail -- an S^4 (even-d) 'quantity' 8 pi^2/3 x (4 pi)^-2 = 1/6 rational parity 0; the un-normalised Vol(S^4) has parity 2
chk("4c CONTROL: the un-normalised volume Vol(S^4) = 8 pi^2/3 has parity 2 and 32 pi^2 = 12 Vol(S^4) (the puzzle's number), whereas Vol(S^4)/(4 pi)^2 = %s has parity 0: the normalisation of the filter removes exactly the pi that the puzzle needs" % sp.simplify(Vol4 / (16 * sp.pi**2)),
    sp.simplify(Vol4 / (16 * sp.pi**2)) == sp.Rational(1, 6))

# ------------------------------------------------------------------------------------------------------------------
# 5. principled eps values, targets, and the guaranteed-hit (IVT) demonstration
# ------------------------------------------------------------------------------------------------------------------
print("\n== 5. targets vs principled eps  (targets and eps list were declared in the docstring)")
targets = {"Z = sqrt(32pi/3)": Z, "Z^2 = 32pi/3": Z2, "32 pi": 32 * pi, "32 pi^2": 32 * pi**2, "8pi/3": 8 * pi / 3, "sqrt(8pi/3)": mp.sqrt(8 * pi / 3)}
princ = {"P1 xi=L (eps=1/2)": mp.mpf(1) / 2, "P2 b=L^2 (eps=1)": mp.mpf(1), "P3 xi=1/a0,L=1/H (eps=Z^2/2)": Z2 / 2}
print("   %-30s %14s %14s %14s" % ("principled eps", "T3(eps) S^3", "T4(eps) S^4", "T^3 (b=eps)"))
rows = {}
for nm, e in princ.items():
    rows[nm] = (T3(e), T4_num(e), T_T3(e))
    print("   %-30s %14s %14s %14s" % (nm, mp.nstr(rows[nm][0], 10), mp.nstr(rows[nm][1], 10), mp.nstr(rows[nm][2], 10)))
minrel = min(abs(v / tv - 1) for v in [x_ for r_ in rows.values() for x_ in r_] for tv in targets.values())
chk("5a at the three principled eps none of T3, T4, T^3 is within 5%% of any of the six targets (closest relative deviation %s)" % mp.nstr(minrel, 3), minrel > 0.05)
print("   P3: T3(16 pi/3) - 1 = %s = 4 e^{-3 eps} + 9 e^{-8 eps}+...: at the framework's own ratio only the zero mode survives" % mp.nstr(T3(Z2 / 2) - 1, 5))
chk("5b at P3 (xi = Rindler length = Z L/... i.e. filter longer than the leaf) T3 = 1 + %s: no information beyond the constant mode" % mp.nstr(T3(Z2 / 2) - 1, 3), T3(Z2 / 2) - 1 < mp.mpf(10)**-20)

# P4: the record's window
pc = mp.mpf('3.0856775814913673e16')                                      # m per pc
H0, OL = mp.mpf('67.4'), mp.mpf('0.685')                                   # km/s/Mpc, Planck-like: only the ORDER of magnitude enters
cH = mp.mpf('299792.458') / (H0 * mp.sqrt(OL))                             # c/H_Lambda in Mpc
L_pc = cH * 10**6
xi_lo, xi_hi = mp.mpf('0.0243'), mp.mpf(100)
eps_lo, eps_hi = (xi_lo / L_pc)**2 / 2, (xi_hi / L_pc)**2 / 2
N_lo = mp.sqrt(pi) / 4 * eps_hi**mp.mpf(-1.5)
N_hi = mp.sqrt(pi) / 4 * eps_lo**mp.mpf(-1.5)
print("   P4: c/H_Lambda = %s pc;  eps in [%s, %s];  Weyl count Tr S_h = (sqrt(pi)/4) eps^(-3/2) in [%s, %s]" % (mp.nstr(L_pc, 4), mp.nstr(eps_lo, 3), mp.nstr(eps_hi, 3), mp.nstr(N_lo, 3), mp.nstr(N_hi, 3)))
chk("5c P4: with the record's own xi window the closed-leaf eps is <= 2e-16 (radius >= c/H_Lambda), deep in the Weyl regime: Tr S_h >= 1e23, corrections e^eps - 1 <= 2e-16; no O(1) transcendental content", eps_hi < 3e-16 and N_lo > 1e23)

# IVT: guaranteed hit
def solve_eps(target):
    f = lambda le: T3(mp.e**le) - target
    return mp.e**mp.findroot(f, (mp.log(mp.mpf('1e-3')), mp.log(mp.mpf(30))), solver='illinois', tol=mp.mpf(10)**-40, maxsteps=200)


print("   eps* such that T3(eps*) = target (b tuned to the answer; the solution exists for ANY target > 1):")
eps_star = {}
for nm, tv in targets.items():
    if tv > 1.01:
        eps_star[nm] = solve_eps(tv)
        print("     %-20s eps* = %-14s  xi*/L = sqrt(2 eps*) = %-10s  (xi* = %s pc if L = c/H_Lambda; record's max xi = 100 pc)" %
              (nm, mp.nstr(eps_star[nm], 8), mp.nstr(mp.sqrt(2 * eps_star[nm]), 6), mp.nstr(mp.sqrt(2 * eps_star[nm]) * L_pc, 4)))
mono = all(T3(mp.mpf(a_)) > T3(mp.mpf(b_)) for a_, b_ in ((0.02, 0.05), (0.05, 0.2), (0.2, 1), (1, 3)))
chk("5d T3 is strictly decreasing (samples) from +inf to 1: a root eps* exists for every target > 1 (H5)", mono and all(abs(T3(eps_star[k]) - targets[k]) < mp.mpf(10)**-30 for k in eps_star))
rng = np.random.default_rng(7)
decoys = rng.uniform(4, 700, 20)
dec_ok = 0
for tv in decoys:
    try:
        e_ = solve_eps(mp.mpf(float(tv)))
        dec_ok += abs(T3(e_) - tv) < 1e-20
    except Exception:
        pass
chk("5e CONTROL: 20/20 random decoy targets in [4, 700] are ALSO hit by some eps* (%d/20): a solved-for b reproduces anything, so a hit only counts if b is fixed first" % dec_ok, dec_ok == 20)
ratio_star = {k: mp.sqrt(2 * v) * L_pc / xi_hi for k, v in eps_star.items()}
chk("5f the tuned eps* for the puzzle's own targets need xi* >= %s x the record's maximum xi = 100 pc (xi* of order the Hubble radius)" % mp.nstr(min(ratio_star.values()), 3),
    min(ratio_star.values()) > 1e6)

# parity-compatible reading: Z (parity 1/2) as an effective mode count of the S^3 leaf
eps_weyl_Z = (sp.Integer(3)**sp.Rational(1, 3) / 8)                         # sqrt(pi)/4 eps^{-3/2} = Z = 4 sqrt(2 pi/3)  =>  eps = 3^{1/3}/8
lhs = sp.sqrt(sp.pi) / 4 * eps_weyl_Z**sp.Rational(-3, 2)
chk("5g parity-compatible reading: the Weyl term (sqrt(pi)/4) eps^(-3/2) equals Z = 4 sqrt(2 pi/3) iff eps = 3^(1/3)/8 = %.5f (algebraic, a cube root of 3), and Z^2 = 32 pi/3 would need eps ~ pi^(-1/3): parity forbids it" % float(eps_weyl_Z),
    sp.simplify(lhs - 4 * sp.sqrt(2 * sp.pi / 3)) == 0)
eZ = solve_eps(Z)
print("   with the curvature factor e^eps kept, T3(eps) = Z needs eps = %s (no longer algebraic; T3 - Weyl = %s)" % (mp.nstr(eZ, 8), mp.nstr(T3(eZ) - mp.sqrt(pi) / 4 * eZ**mp.mpf(-1.5), 4)))
chk("5h that eps is not any of P1-P3, and 3^(1/3)/8 has no derivation in the record (xi is a declared knob: FP17 theorem, xi not buildable from (a0, Lambda, G, c)): parity compatibility is a necessary condition, not evidence",
    all(abs(eZ / v - 1) > 0.05 for v in princ.values()))

print("\n%d/%d checks held" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
