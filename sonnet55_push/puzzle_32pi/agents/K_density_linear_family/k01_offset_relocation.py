"""k01: the AQUAL-offset relocation of the puzzle, reproduced independently of lane G and made precise.

SETTING (c = 1 in the algebra; c is restored only in the H0/a0 numbers).  A Newtonian-normalised MOND action
        L = -(a0^2/(8 pi G)) F(y) - rho phi ,      y = |grad phi|^2/a0^2 ,      F(y) -> y  as y -> infinity
whose field equation is div(mu grad phi) = 4 pi G rho with mu = F'.  The normalisation fixes the additive constant of F:
F(0) = c[mu] := int_0^inf (1 - mu) dy.  READING UNDER TEST ("offset reading"): the vacuum (g = 0) state carries the energy
density  rho_off = a0^2 c[mu] / (8 pi G),  and that IS the dark energy, so   G rho_L / a0^2 = c/(8 pi).   The puzzle
(G rho_L = 4 a0^2) then needs c = 32 pi = 100.53.

WHAT IS CHECKED
 A  Euler-Lagrange derivation (sympy); F(0) = c from the normalisation; the constant piece of L is a cosmological term
    (T_mn = L g_mn = -rho_off g_mn).
 B  Identity c = int (1-mu) d(x^2) = int x^2 dmu (mu is a CDF on x = g/a0 >= 0): c is the SECOND MOMENT of the transition.
 C  Lower bound c >= 1/3 for any mu with mu' <= mu'(0) = 1 (bathtub principle); control: the bound FAILS if mu' may exceed 1.
 D  Finiteness classification: c < inf  <=>  int^inf x (1-mu) dx < inf; tail 1-mu ~ A x^-p is finite iff p > 2
    (p = 2 log-divergent, p < 2 power-divergent).  Partial-sum asymptotics verified.
 E  The values of c for: sharp, exponential, Milgrom mu_n (closed form via Mellin/Beta, verified by two integrations), simple,
    standard, the Milgrom-1999 vacuum-temperature-excess form, McGaugh-RAR (proper AQUAL inverse, two methods; and the
    literal-argument reading, which has the WRONG deep-MOND limit), and the record's OR-channel family mu = 1-(1-p)^N in both
    readings (p = y/(1+y) thermal-geometric; p = min(g/s,1) literal).
 F  What each needs for c = c_req: required c on both a0 footings (c_req = 3 Omega_L (c H0/a0)^2, no G, no pi), the tail
    exponents (n*, s*, N*), the cutoff each marginal family would need, and the self-consistent N* of the record's own family.
 G  Where c accumulates (fraction of c from x < X) and the state-dependence of the offset eps(y) = K int_y^inf (1-mu) dy'.
Every number is recomputed here; 'CONTROL'/'MUTATION' lines must FAIL if the claim they guard were wrong.
"""
import sys
import numpy as np
import mpmath as mp
import sympy as sp
from scipy import integrate, optimize

mp.mp.dps = 30
OK = []


def chk(name, cond):
    OK.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name, flush=True)


PI = mp.pi
C_REQ_FW = 32 * PI                     # the puzzle's requirement

# ------------------------------------------------------------------------------------------------ A
print("== A  Euler-Lagrange derivation and the meaning of F(0)")
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
X = (x1, x2, x3)
G, a0, rho = sp.symbols('G a0 rho', positive=True)
F = sp.Function('F')
phi = sp.Function('phi')(*X)
yv = sum(sp.diff(phi, v) ** 2 for v in X) / a0 ** 2
Lag = -(a0 ** 2 / (8 * sp.pi * G)) * F(yv) - rho * phi
# Euler-Lagrange: dL/dphi - sum_i d_i (dL/d phi_i) = 0
EL = sp.diff(Lag, phi)
for v in X:
    EL -= sp.diff(sp.diff(Lag, sp.diff(phi, v)), v)
# explicit expected form: div( F'(y) grad phi ) / (4 pi G) - rho = 0
yy = sp.Symbol('yy', positive=True)
Fprime_of_y = sp.diff(F(yy), yy).subs(yy, yv)
expected = sum(sp.diff(Fprime_of_y * sp.diff(phi, v), v) for v in X) / (4 * sp.pi * G) - rho
diff_ = sp.simplify((EL - expected).doit())
chk("A1 EL equation of L = -(a0^2/8piG)F(y) - rho*phi is div(F'(y) grad phi) = 4 pi G rho (mu = F')", diff_ == 0)
# mutation: a wrong prefactor (8 pi -> 4 pi) must NOT reproduce the Poisson normalisation
Lag_bad = -(a0 ** 2 / (4 * sp.pi * G)) * F(yv) - rho * phi
EL_bad = sp.diff(Lag_bad, phi)
for v in X:
    EL_bad -= sp.diff(sp.diff(Lag_bad, sp.diff(phi, v)), v)
chk("A2 MUTATION: prefactor 1/(4 pi G) does not give div(mu grad phi) = 4 pi G rho", sp.simplify((EL_bad - expected).doit()) != 0)
# Newton: F = y gives Poisson
Nw = sp.simplify((EL.subs(F, sp.Lambda(yy, yy)).doit()) + 0)
chk("A3 F = y reproduces Poisson  lap(phi) = 4 pi G rho", sp.simplify(Nw - (sum(sp.diff(phi, v, 2) for v in X) / (4 * sp.pi * G) - rho)) == 0)
# the additive constant: F -> F + C leaves EL unchanged (repeats lane G D1 independently by direct differentiation)
Cc = sp.Symbol('Cc')
Lag_c = -(a0 ** 2 / (8 * sp.pi * G)) * (F(yv) + Cc) - rho * phi
EL_c = sp.diff(Lag_c, phi)
for v in X:
    EL_c -= sp.diff(sp.diff(Lag_c, sp.diff(phi, v)), v)
chk("A4 additive constant of F is invisible to the field equation (the 'offset' is fixed only by the normalisation choice)", sp.simplify((EL_c - EL).doit()) == 0)
# F(y) = y - int_0^y (1-mu) + F(0); F(inf) - y -> 0  =>  F(0) = c   (checked on an explicit mu)
xs = sp.Symbol('xs', positive=True)
mu_ex = 1 - sp.exp(-xs)                                   # mu(x), x = sqrt(y)
c_ex = sp.integrate((1 - mu_ex) * 2 * xs, (xs, 0, sp.oo))
chk("A5 F(0) = int_0^inf (1-mu) dy evaluated symbolically for mu = 1-e^{-x}: c = 2", sp.simplify(c_ex - 2) == 0)
# constant piece of the Lagrangian is a cosmological term: T_mn = -(2/sqrt(-g)) d(sqrt(-g) L)/d g^mn  (+ nothing else for constant L)
gu = sp.symbols('gu0:4', real=True)                        # diagonal inverse-metric entries g^00, g^11, g^22, g^33
sqrtg = 1 / sp.sqrt(-(gu[0] * gu[1] * gu[2] * gu[3]))      # sqrt(-g) = 1/sqrt(-det g^{mn}) for a diagonal metric
rho_off = sp.Symbol('rho_off', positive=True)
Lc = -rho_off                                              # constant Lagrangian density
at = {gu[0]: -1, gu[1]: 1, gu[2]: 1, gu[3]: 1}
Tdiag = [sp.simplify((-2 / sqrtg * sp.diff(sqrtg * Lc, gu[i])).subs(at)) for i in range(4)]
chk("A6 a constant L = -rho_off has T_00 = +rho_off, T_ii = -rho_off (a cosmological term, w = -1) from the metric variation of sqrt(-g) L (Minkowski point)",
    Tdiag == [rho_off, -rho_off, -rho_off, -rho_off])

# ------------------------------------------------------------------------------------------------ helper: families
mp.mp.dps = 25


def c_quad(one_minus_mu, breaks, weight=lambda x: 2 * x):
    return mp.quad(lambda t: one_minus_mu(t) * weight(t), breaks)


BR = [0, 0.5, 1, 3, 10, 30, 100, 1e3, 1e4, 1e6, 1e9, mp.inf]


# 1 - x(1+x^n)^(-1/n): stable for large x as  -expm1(-log1p(x^-n)/n)
def one_minus_mu_n(t, n):
    t = mp.mpf(t)
    n = mp.mpf(n)
    if t < 1:
        return 1 - t / (1 + t ** n) ** (1 / n)
    return -mp.expm1(-mp.log1p(t ** (-n)) / n)


def c_mun_closed(n):
    n = mp.mpf(n)
    return -(2 / n) * mp.gamma(3 / n) * mp.gamma(-2 / n) / mp.gamma(1 / n)


# ------------------------------------------------------------------------------------------------ B
print("\n== B  c = int (1-mu) dy = int x^2 dmu  (second moment of the transition)")
# second method needs mu'(x): use sympy derivative lambdified to mpmath
xs = sp.Symbol('xs', positive=True)
fams_sym = {
    'exp': 1 - sp.exp(-xs),
    'mu_3': xs / (1 + xs ** 3) ** sp.Rational(1, 3),
    'mu_4': xs / (1 + xs ** 4) ** sp.Rational(1, 4),
    'OR N=3': 1 - (1 + xs / 3) ** (-3),
    'OR N=5': 1 - (1 + xs / 5) ** (-5),
}
vals_B = {}
for nm, mu_s in fams_sym.items():
    f1 = sp.lambdify(xs, 1 - mu_s, 'mpmath')
    if nm.startswith('mu_'):                                  # stable 1 - x(1+x^n)^(-1/n) (naive form cancels catastrophically at large x)
        f1 = (lambda t, n_=int(nm[3:]): one_minus_mu_n(t, n_))
    dmu = sp.simplify(sp.diff(mu_s, xs))
    if nm.startswith('mu_'):                                  # stable form of d/dx[x (1+x^n)^(-1/n)] = (1+x^n)^(-1/n-1)
        n_ = int(nm[3:])
        dmu = (1 + xs ** n_) ** (-sp.Rational(1, n_) - 1)
    f2 = sp.lambdify(xs, dmu * xs ** 2, 'mpmath')
    m1 = c_quad(f1, BR)
    m2 = mp.quad(f2, BR)
    vals_B[nm] = (m1, m2)
    print(f"   {nm:8s}  int(1-mu)dy = {mp.nstr(m1, 12):>16s}   int x^2 dmu = {mp.nstr(m2, 12):>16s}")
chk("B1 c = int(1-mu)dy equals the second moment int x^2 mu'(x) dx for 5 families (integration by parts, boundary term x^2(1-mu) -> 0)",
    all(abs(a - b) < 1e-10 * max(1, abs(a)) for a, b in vals_B.values()))
# MUTATION: the first moment is a different number
m_first = mp.quad(sp.lambdify(xs, (1 - fams_sym['exp']), 'mpmath'), BR)
chk("B2 MUTATION: the FIRST moment int(1-mu)dx (= 1 for the exponential) is not c (= 2): the weight 2x matters", abs(m_first - 1) < 1e-12 and abs(vals_B['exp'][0] - 2) < 1e-12)

# ------------------------------------------------------------------------------------------------ C
print("\n== C  lower bound c >= 1/3 when mu' <= mu'(0) = 1 (density of the CDF is bounded by its value at 0)")
rng = np.random.default_rng(20260929)


def c_step_density(widths, heights):
    """density f = heights[i] on [b_i, b_{i+1}); returns (sum f w, c = int x^2 f dx)."""
    b = np.concatenate([[0.0], np.cumsum(widths)])
    mass = float(np.sum(heights * widths))
    c = float(np.sum(heights * (b[1:] ** 3 - b[:-1] ** 3) / 3))
    return mass, c


min_c = 1e9
for _ in range(20000):
    k = rng.integers(1, 12)
    h = np.sort(rng.uniform(0, 1, k))[::-1]
    h[0] = 1.0                                              # f(0) = mu'(0) = 1, f nonincreasing => mu' <= 1
    w = rng.uniform(0.01, 3, k)
    m = np.sum(h * w)
    if m < 1.0:                                             # need total mass 1: rescale by extending the last step
        w[-1] += (1.0 - m) / h[-1] if h[-1] > 1e-9 else 0
    elif m > 1.0:
        continue
    mass, c = c_step_density(w, h)
    if abs(mass - 1) < 1e-9:
        min_c = min(min_c, c)
mass_s, c_sharp = c_step_density(np.array([1.0]), np.array([1.0]))
print(f"   random monotone-density search: min c = {min_c:.6f} (bathtub value 1/3 = {1/3:.6f}); sharp transition c = {c_sharp:.6f}")
chk("C1 for 20000 random nonincreasing densities with f(0)=1: c >= 1/3 (sharp transition attains it)", min_c >= 1 / 3 - 1e-9 and abs(c_sharp - 1 / 3) < 1e-12)
# control: allow the density to exceed f(0) later (non-concave mu): c can drop below 1/3
mass2, c2 = c_step_density(np.array([0.02, 0.2]), np.array([1.0, (1 - 0.02) / 0.2]))    # f=1 on [0,.02], f=4.9 on next 0.2
chk("C2 CONTROL: with mu' > mu'(0) allowed (non-concave mu) c = %.4f < 1/3, so the bound really needs mu' <= 1" % c2, abs(mass2 - 1) < 1e-12 and c2 < 1 / 3)
chk("C3 no upper bound: c[mu] over concave mu is unbounded (mu_n, n -> 2+, has c ~ 1/(n-2)): c(2.001) = %s" % mp.nstr(c_mun_closed(2.001), 6),
    c_mun_closed(2.001) > 900)

# ------------------------------------------------------------------------------------------------ D
print("\n== D  when is c finite?  tail 1-mu ~ A x^-p")
xg = [mp.mpf(10) ** k for k in range(2, 9)]
def partial(one_minus_mu, X):
    pts = sorted(set([mp.mpf(v) for v in [0, 1, 10, 100, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8] if v < X] + [mp.mpf(X)]))
    return mp.quad(lambda t: one_minus_mu(t) * 2 * t, pts)


simple = lambda t: 1 / (1 + t)
standard = lambda t: one_minus_mu_n(t, 2)
tdsx = lambda t: 1 - (mp.sqrt(1 + 4 * t * t) - 1) / (2 * t) if t > 0 else mp.mpf(1)
print("   partial c(X) for X = 1e2..1e8:")
part = {}
for nm, f in [('simple (p=1)', simple), ('standard (p=2)', standard), ('T-excess (p=1)', tdsx)]:
    part[nm] = [partial(f, X) for X in xg]
    print(f"   {nm:16s}" + " ".join(f"{mp.nstr(v, 6):>11s}" for v in part[nm]))
# closed forms
c_simple = lambda X: 2 * X - 2 * mp.log(1 + X)
c_std = lambda X: mp.asinh(X) + X ** 2 - X * mp.sqrt(1 + X ** 2)
chk("D1 partial c for the simple mu = 2X - 2 ln(1+X) (linear divergence) [closed form vs quadrature at X=1e2..1e8]",
    all(abs(part['simple (p=1)'][i] - c_simple(xg[i])) < 1e-6 * c_simple(xg[i]) for i in range(len(xg))))
chk("D2 partial c for the standard mu = asinh X + X^2 - X sqrt(1+X^2) ~ ln(2X) - 1/2 (log divergence) [closed form vs quadrature]",
    all(abs(part['standard (p=2)'][i] - c_std(xg[i])) < 1e-6 * max(1, c_std(xg[i])) for i in range(len(xg))))
chk("D3 Milgrom-1999 temperature-excess form 1-mu ~ 1/(2x): partial c grows like X (linear divergence): c(1e8)/c(1e6) = %s" % mp.nstr(part['T-excess (p=1)'][6] / part['T-excess (p=1)'][4], 5),
    abs(part['T-excess (p=1)'][6] / part['T-excess (p=1)'][4] - 100) < 1.0)
# a sweep of tail exponents: finite iff p > 2
print("   Milgrom mu_n, c(n) closed form vs quadrature (log-variable x = e^u so that slow tails are resolved):")
def c_quad_log(one_minus_mu, umax=6000):
    pts = [-40, -10, 0, 2, 5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560, umax]
    return mp.quad(lambda u: one_minus_mu(mp.exp(u)) * 2 * mp.exp(2 * u), pts)
rows = []
for n in [2.05, 2.5, 3, 4, 6, 10]:
    cq = c_quad_log(lambda t, n=n: one_minus_mu_n(t, n))
    cc = c_mun_closed(n)
    rows.append((n, cq, cc))
    print(f"   n = {n:5}: quad {mp.nstr(cq, 12):>16s}   closed {mp.nstr(cc, 12):>16s}")
chk("D4 mu_n: c(n) = -(2/n) Gamma(3/n) Gamma(-2/n)/Gamma(1/n) (finite n > 2) matches numerical integration for n = 2.05...10",
    all(abs(a - b) < 1e-7 * max(1, abs(b)) for _, a, b in rows))
chk("D5 c(n) = 1 at n=3 and c(n) ~ 1/(n-2) as n -> 2+ (c(2.001)*(0.001) = %s)" % mp.nstr(c_mun_closed(2.001) * 0.001, 6),
    abs(c_mun_closed(3) - 1) < 1e-15 and abs(c_mun_closed(2.001) * mp.mpf('0.001') - 1) < 5e-3)
# MUTATION: dropping the analytic-continuation sign (using +) would give a negative value
chk("D6 MUTATION: the naive sign (+(2/n)Gamma(3/n)Gamma(-2/n)/Gamma(1/n)) is negative for n>2 and is rejected by the numerics",
    (2 / mp.mpf(3)) * mp.gamma(mp.mpf(1)) * mp.gamma(-mp.mpf(2) / 3) / mp.gamma(mp.mpf(1) / 3) < 0)
# tail-exponent criterion on a synthetic family: 1-mu = (1+x)^-p  (p=1.5, 2, 2.5)
def c_pow(p):
    return mp.quad(lambda t: (1 + t) ** (-p) * 2 * t, [0, 1, 10, 100, 1e3, 1e5, 1e7, 1e9, mp.inf])
c25 = c_pow(mp.mpf('2.5'))
closed25 = 2 / ((mp.mpf('2.5') - 1) * (mp.mpf('2.5') - 2))
chk("D7 synthetic tail (1+x)^-p: p = 2.5 gives finite c = 2/((p-1)(p-2)) = %s (quad %s)" % (mp.nstr(closed25, 8), mp.nstr(c25, 8)), abs(c25 - closed25) < 1e-6)
d15 = [partial(lambda t: (1 + t) ** (-mp.mpf('1.5')), X) for X in (1e4, 1e6, 1e8)]
chk("D8 p = 1.5: partial c grows as X^(1/2) (x10 per two decades): ratios %s" % [mp.nstr(d15[1] / d15[0], 4), mp.nstr(d15[2] / d15[1], 4)],
    abs(d15[1] / d15[0] - 10) < 0.5 and abs(d15[2] / d15[1] - 10) < 0.5)

# ------------------------------------------------------------------------------------------------ E
print("\n== E  c for the standard families")
cv = {}
cv['sharp min(x,1)'] = mp.quad(lambda t: (1 - t) * 2 * t, [0, 1])
cv['exponential 1-e^-x'] = c_quad(lambda t: mp.exp(-t), BR)
for n in [3, 4, 6, 10]:
    cv[f'Milgrom mu_n, n={n}'] = c_mun_closed(n)
# RAR: nu(y) = 1/(1-e^{-sqrt y}), g_obs = g_bar nu, x = y nu, mu = 1/nu = 1 - e^{-sqrt y}  (y = g_bar/a0, x = g_obs/a0)
xr = lambda y: y / (-mp.expm1(-mp.sqrt(y)))
rar1 = mp.quad(lambda y: xr(y) ** 2 * mp.exp(-mp.sqrt(y)) / (2 * mp.sqrt(y)), [mp.mpf('1e-30'), 1, 10, 100, 1e3, 1e4, 1e5, 1e6])
# method 2: integrate over x with the inverse solved numerically (scipy, independent code path)
def y_of_x(xv):
    if xv < 1e-12:
        return xv ** 2
    return optimize.brentq(lambda y: y / (-np.expm1(-np.sqrt(y))) - xv, 1e-30, max(4 * xv, 4.0), xtol=1e-14, rtol=1e-13)
def omm_rar(xv):
    return np.exp(-np.sqrt(y_of_x(xv)))
rar2 = 0.0
edges = [0, 1, 3, 10, 30, 100, 300, 1000]
for a, b in zip(edges[:-1], edges[1:]):
    rar2 += integrate.quad(lambda t: 2 * t * omm_rar(t), a, b, epsabs=1e-13, epsrel=1e-12, limit=200)[0]
cv['RAR-nu (proper AQUAL inverse)'] = rar1
lit_rar = c_quad(lambda t: mp.exp(-mp.sqrt(t)), BR)
cv['RAR mu=1-e^-sqrt(x) at g_obs (wrong deep-MOND limit)'] = lit_rar
# record's OR-channel family, thermal-geometric p = y/(1+y):  mu = 1-(1+x/N)^-N
def c_or(N):
    N = mp.mpf(N)
    return 2 * N ** 2 / ((N - 1) * (N - 2))
def c_or_compact(N):
    N = mp.mpf(N)
    return 2 * N ** 2 / ((N + 1) * (N + 2))
for N in [3, 5]:
    cv[f"record OR family (1+x/N)^-N, N={N}"] = c_or(N)
for nm, v in cv.items():
    print(f"   {nm:56s} c = {mp.nstr(v, 10):>14s}   G rho/a0^2 = c/(8 pi) = {mp.nstr(v / (8 * PI), 6)}")
print(f"   (RAR-nu second method (scipy, inverse by brentq): {rar2:.9f})")
chk("E1 sharp transition c = 1/3 exactly, exponential c = 2 exactly", abs(cv['sharp min(x,1)'] - mp.mpf(1) / 3) < 1e-12 and abs(cv['exponential 1-e^-x'] - 2) < 1e-10)
chk("E2 RAR-nu (proper inverse): two independent integrations agree: %.7f vs %.7f (lane G: 25.976)" % (float(rar1), rar2), abs(float(rar1) - rar2) < 2e-6 and abs(float(rar1) - 25.976) < 2e-3)
chk("E3 the literal-argument reading mu(x) = 1 - e^{-sqrt x} gives exactly c = 24 (but its deep limit mu ~ sqrt(x) is NOT deep-MOND: excluded as a MOND mu)", abs(lit_rar - 24) < 1e-9)
# the deep limit check of the literal reading: mu(x)*x = y -> x^{3/2} = y (g_obs ~ g_bar^{2/3}, not g_bar^{1/2})
xs_ = sp.Symbol('x', positive=True)
lim_ratio = sp.limit((1 - sp.exp(-sp.sqrt(xs_))) / xs_, xs_, 0)
chk("E4 literal reading: mu/x -> infinity as x -> 0 (mu ~ sqrt(x)); a MOND mu must have mu/x -> 1", lim_ratio == sp.oo)
chk("E5 OR family closed forms: c(N) = 2N^2/((N-1)(N-2)) [(1+x/N)^-N] verified vs quadrature at N = 3, 5", all(abs(c_quad(lambda t, N=N: (1 + t / N) ** (-N), BR) - c_or(N)) < 1e-7 * c_or(N) for N in (3, 5)))
chk("E6 OR family literal-compact reading (p = min(g/s,1), mu = 1-(1-g/s)^N on g<s): c = 2N^2/((N+1)(N+2)) < 2 for every N (verified at N=2: %s vs quad %s)" %
    (mp.nstr(c_or_compact(2), 8), mp.nstr(mp.quad(lambda t: (1 - t / 2) ** 2 * 2 * t, [0, 2]), 8)),
    abs(c_or_compact(2) - mp.quad(lambda t: (1 - t / 2) ** 2 * 2 * t, [0, 2])) < 1e-12 and all(c_or_compact(N) < 2 for N in (1, 2, 5, 50, 500)))
# exact marginal case N = 2 of the record's own shape: mu = 1 - (1+x/2)^-2
def c_or2_partial(Xv):
    Xv = mp.mpf(Xv)
    return 8 * (mp.log((2 + Xv) / 2) + 2 / (2 + Xv) - 1)
chk("E7 the record's own N = 2 shape (kappa = 1/2) is the MARGINAL member: 1-mu = 4/(2+x)^2 ~ 4/x^2, c(X) = 8[ln(1+X/2) + 2/(2+X) - 1] -> infinity (closed form vs quadrature at X = 1e3, 1e6)",
    all(abs(c_or2_partial(Xv) - mp.quad(lambda t: (1 + t / 2) ** (-2) * 2 * t, sorted(set([mp.mpf(v) for v in [0, 1, 10, 100, 1e3, 1e4, 1e5, 1e6] if v < Xv] + [mp.mpf(Xv)])))) < 1e-8 * c_or2_partial(Xv) for Xv in (1e3, 1e6)))
# bookkeeping: heavy tails 8x the standard function's amplitude
chk("E8 tail amplitudes: standard 1-mu -> 1/(2x^2); record N=2 -> 4/x^2 (8x heavier); simple -> 1/x; T-excess -> 1/(2x)",
    abs(sp.limit(xs_ ** 2 * (1 - xs_ / sp.sqrt(1 + xs_ ** 2)), xs_, sp.oo) - sp.Rational(1, 2)) == 0 and
    abs(sp.limit(xs_ ** 2 * (1 + xs_ / 2) ** (-2), xs_, sp.oo) - 4) == 0 and
    abs(sp.limit(xs_ * (1 - (sp.sqrt(1 + 4 * xs_ ** 2) - 1) / (2 * xs_)), xs_, sp.oo) - sp.Rational(1, 2)) == 0)

# ------------------------------------------------------------------------------------------------ F
print("\n== F  what each family needs")
c_light = 2.99792458e8
Mpc = 3.0856775814913673e22
H0 = 67.4e3 / Mpc
OmL = 0.685
Z2 = 32 * PI / 3
a0_fw = c_light * H0 * mp.sqrt(OmL) / mp.sqrt(Z2)           # cH_L/Z, the framework's own a0
a0_sparc = 1.1279e-10                                        # the record's second footing (SPARC-fitted)
a0_alt2 = 1.2e-10
def c_req(a0v):
    return 3 * OmL * (c_light * H0 / a0v) ** 2
print(f"   framework a0 = cH_L/Z = {float(a0_fw):.4e} ; SPARC-fitted a0 = {a0_sparc:.4e} ; cH0 = {c_light*H0:.4e} m/s^2")
creq = {'a0 = cH_L/Z (framework)': c_req(a0_fw), 'a0 = 1.1279e-10 (SPARC fit)': c_req(a0_sparc), 'a0 = 1.2e-10 (rounded literature)': c_req(a0_alt2)}
for k_, v_ in creq.items():
    print(f"   c_req = 3 Omega_L (c H0/a0)^2 = {mp.nstr(v_, 6):>10s}   [{k_}]   G rho_L/a0^2 = {mp.nstr(v_ / (8 * PI), 5)}")
chk("F1 CONTROL: with a0 = c H_L / Z the requirement is c_req = 3 Z^2 = 32 pi exactly, independent of H0 and Omega_L", abs(creq['a0 = cH_L/Z (framework)'] - 32 * PI) < 1e-9)
chk("F2 on the SPARC-fitted a0 the requirement is c_req = %.1f (not 32 pi): the offset reading needs 61-100 depending on the a0 footing; G rho_L/a0^2 = c_req/(8 pi) = 2.7-4" % float(creq['a0 = 1.1279e-10 (SPARC fit)']),
    60 < creq['a0 = 1.1279e-10 (SPARC fit)'] < 72 and 55 < creq['a0 = 1.2e-10 (rounded literature)'] < 66)

# tail parameters needed
def solve_n(target):
    return mp.findroot(lambda n: c_mun_closed(n) - target, (mp.mpf('2.002'), mp.mpf('2.5')), solver='illinois', tol=1e-25, maxsteps=200)
def solve_s(target):
    return mp.findroot(lambda s: (2 / s) * mp.gamma(2 / s) - target, (mp.mpf('0.3'), mp.mpf('0.5')), solver='anderson', tol=1e-25, maxsteps=200)
def solve_N(target):
    return mp.findroot(lambda N: c_or(N) - target, (mp.mpf('2.001'), mp.mpf('3')), solver='illinois', tol=1e-25, maxsteps=200)
print("   family parameter that makes c = c_req:")
sol = {}
for nm, cr in [('32 pi', 32 * PI), ('SPARC-a0', creq['a0 = 1.1279e-10 (SPARC fit)'])]:
    sol[nm] = (solve_n(cr), solve_s(cr), solve_N(cr))
    print(f"   c_req = {mp.nstr(cr, 6):>9s} ({nm:8s}):  Milgrom n* = {mp.nstr(sol[nm][0], 8)},  stretched-exp s* = {mp.nstr(sol[nm][1], 8)},  record-OR N* = {mp.nstr(sol[nm][2], 8)}")
chk("F3 32 pi needs Milgrom n* = 2.0100 (a tail 0.010 above the marginal exponent 2), stretched-exponential s* = 0.4085 (lane G), record-OR N* = 2.0796",
    abs(sol['32 pi'][0] - mp.mpf('2.0099')) < 2e-4 and abs(sol['32 pi'][1] - mp.mpf('0.40853')) < 1e-4 and abs(sol['32 pi'][2] - mp.mpf('2.0796')) < 2e-4)
chk("F4 each solution verifies: c(n*) = c(N*) = c(s*) = 32 pi", abs(c_mun_closed(sol['32 pi'][0]) - 32 * PI) < 1e-12 and abs(c_or(sol['32 pi'][2]) - 32 * PI) < 1e-12 and abs((2 / sol['32 pi'][1]) * mp.gamma(2 / sol['32 pi'][1]) - 32 * PI) < 1e-12)
# cutoffs for the marginal / divergent families (X_c: c(X_c) = 32 pi)
Xc_simple = mp.findroot(lambda X: c_simple(X) - 32 * PI, 60)
Xc_std = mp.exp(32 * PI - mp.log(2) + mp.mpf(1) / 2)      # asymptotic c_std(X) = ln(2X) - 1/2
Xc_or2 = mp.findroot(lambda X: c_or2_partial(X) - 32 * PI, 1e6)
print(f"   cutoff X_c (units of a0) at which the partial c reaches 32 pi:  simple {mp.nstr(Xc_simple, 5)};  record N=2 {mp.nstr(Xc_or2, 5)};  standard {mp.nstr(Xc_std, 5)}")
with mp.workdps(200):
    c_std_at_cut = c_std(mp.mpf(Xc_std))
asym_err = abs(c_std(mp.mpf(10) ** 6) - (mp.log(2 * mp.mpf(10) ** 6) - mp.mpf(1) / 2))
chk("F5 the cutoffs that would make a marginal/divergent family hit 32 pi: simple X_c = 54.3 a0; record N=2 X_c = 1.56e6 a0; standard X_c = 3.8e43 a0 (exact closed forms; no scale identified; bookkeeping, not results)",
    abs(Xc_simple - 54.278) < 0.01 and 1.55e6 < Xc_or2 < 1.57e6 and 3.7e43 < Xc_std < 3.9e43 and abs(c_std_at_cut - 32 * PI) < 1e-6 and asym_err < 1e-9)

# self-consistent N of the record's own OR family: a0 = s/N (unit response per channel) => G rho_L / a0^2 = N^2 ; offset reading => c(N)/(8 pi)
Nsc = (3 + mp.sqrt(1 + 1 / PI)) / 2
Nsc_num = mp.findroot(lambda N: c_or(N) - 8 * PI * N ** 2, (mp.mpf('2.001'), mp.mpf('3')), solver='illinois', tol=1e-25, maxsteps=200)
print(f"   record OR family, unit response p'(0)=1 (a0 = s/N): offset reading G rho/a0^2 = N^2 = c(N)/(8 pi)  =>  (N-1)(N-2) = 1/(4 pi):")
print(f"      N* = (3 + sqrt(1 + 1/pi))/2 = {mp.nstr(Nsc, 12)}  (numeric root {mp.nstr(Nsc_num, 12)});  kappa* = 1/N* = {mp.nstr(1 / Nsc, 8)};  G rho/a0^2 = {mp.nstr(Nsc ** 2, 8)}")
chk("F6 self-consistency in the record's OR family (mu = 1-(1+g/s)^-N, a0 = s/N): the offset reading is (N-1)(N-2) = 1/(4 pi), N* = %s, NOT N = 2 (at N=2 the offset is infinite)" % mp.nstr(Nsc, 8),
    abs(Nsc - Nsc_num) < 1e-15 and abs(Nsc - mp.mpf('2.07409')) < 2e-5 and abs((Nsc - 1) * (Nsc - 2) - 1 / (4 * PI)) < 1e-25)
chk("F7 the compact reading (p = min(g/s,1)) has NO solution: c(N) = 2N^2/((N+1)(N+2)) < 8 pi N^2 for every N > 0", all(c_or_compact(N) < 8 * PI * N ** 2 for N in [mp.mpf(v) for v in (0.01, 0.1, 1, 2, 10, 1e3)]))
# coincidence disclosure (NOT a result): kappa* against Verlinde's kappa = sqrt(2 pi/27)
kV = mp.sqrt(2 * PI / 27)
print(f"   disclosure: kappa* = {mp.nstr(1 / Nsc, 6)} lies {mp.nstr(abs(1 / Nsc - kV) / kV * 100, 3)}% from Verlinde's sqrt(2 pi/27) = {mp.nstr(kV, 6)}; different chains, I attribute no meaning to it.")
chk("F8 disclosure check (numerology guard): kappa* is within 0.1% of Verlinde's 0.4824 -- a numerical coincidence of two unrelated chains; nothing is claimed", abs(1 / Nsc - kV) / kV < 1e-3)

# ------------------------------------------------------------------------------------------------ G
print("\n== G  where c accumulates, and the state dependence of the offset")
def cum_fraction(kind):
    out = []
    for Xv in (3, 10, 30, 100, 1e3, 1e6):
        if kind == 'rar':
            # c(<X) = int_{x<X} x^2 dmu ; parametrise by y with x(y) < X
            ymax = optimize.brentq(lambda y: y / (-np.expm1(-np.sqrt(y))) - Xv, 1e-9, 4 * Xv + 10)
            part_ = mp.quad(lambda y: xr(y) ** 2 * mp.exp(-mp.sqrt(y)) / (2 * mp.sqrt(y)), [mp.mpf('1e-30'), min(1, ymax), ymax] if ymax > 1 else [mp.mpf('1e-30'), ymax])
            out.append(part_ / cv['RAR-nu (proper AQUAL inverse)'])
    return out
fr_rar = cum_fraction('rar')
print("   fraction of c from x < X, X = 3, 10, 30, 100, 1e3, 1e6")
print("   RAR-nu (c = 25.98):        " + " ".join(f"{float(v):.3f}" for v in fr_rar))
# for a standard-like tail 1-mu = x^-n/n with n = 2.01: c(<X) = c - int_X^inf ~ c - 2 X^(2-n)/(n (n-2))  (asymptotic)
n201 = mp.mpf('2.01')
fr_n = [1 - (2 * Xv ** (2 - n201) / (n201 * (n201 - 2))) / c_mun_closed(n201) for Xv in (3, 10, 30, 100, 1e3, 1e6)]
print("   mu_n, n = 2.01 (c = 99.5): " + " ".join(f"{float(v):.3f}" for v in fr_n) + "   (asymptotic tail formula, valid x >> 1)")
chk("G1 for the RAR-nu (c = 25.98): only %.0f%% of c comes from x < 10, %.0f%% from x < 30, %.0f%% from x < 100: c is a moment of the 10-100 a0 range that SPARC covers by a few hundred points at most (k02), not of the transition x ~ 1" % (100 * float(fr_rar[1]), 100 * float(fr_rar[2]), 100 * float(fr_rar[3])),
    fr_rar[1] < 0.30 and 0.6 < fr_rar[2] < 0.72 and fr_rar[3] > 0.95)
chk("G2 for the mu_n tail with n = 2.01 (c = 99.5) only %.0f%% of c comes from x < 1e3 and %.0f%% from x < 1e6: >85%% of c sits at g > 1e6 a0 = 1e-4 m/s^2, far beyond any galaxy" % (100 * float(fr_n[4]), 100 * float(fr_n[5])),
    fr_n[5] < 0.15 and fr_n[4] < 0.1)
# offset is state dependent: eps(y)/eps(0) = int_y^inf (1-mu) dy' / c
def eps_ratio_rar(x_at):                                    # fraction of the offset remaining at field g = x_at*a0
    ymax = optimize.brentq(lambda y: y / (-np.expm1(-np.sqrt(y))) - x_at, 1e-12, 4 * x_at + 10)
    lower = mp.quad(lambda y: xr(y) ** 2 * mp.exp(-mp.sqrt(y)) / (2 * mp.sqrt(y)), [mp.mpf('1e-30'), min(1, ymax), ymax] if ymax > 1 else [mp.mpf('1e-30'), ymax])
    # eps(y_field) = int_{x_at^2}^{inf} (1-mu) d(x^2) = c - int_0^{x_at^2}(1-mu) d(x^2); int_0^{X}(1-mu)2x dx = X^2 (1-mu(X)) + int_0^X x^2 dmu
    return (cv['RAR-nu (proper AQUAL inverse)'] - (x_at ** 2 * mp.exp(-mp.sqrt(ymax)) + lower)) / cv['RAR-nu (proper AQUAL inverse)']
er = {xx: eps_ratio_rar(xx) for xx in (0.01, 1, 3, 10, 30)}
print("   RAR-nu offset remaining at field g = X a0 (eps(g)/eps(0)): " + "  ".join(f"X={k}: {float(v):.3f}" for k, v in er.items()))
chk("G3 the offset is STATE-DEPENDENT: eps(g)/eps(0) = 1.00 (g<<a0), %.2f at g = a0, %.2f at 10 a0, %.2f at 30 a0: inside high-g systems the 'vacuum energy' is suppressed, so the reading needs the cosmic vacuum to sit at g << a0" % (float(er[1]), float(er[10]), float(er[30])),
    er[0.01] > 0.999 and er[1] < 0.99 and er[3] < er[1] and er[10] < er[3] and er[10] < 0.65 and er[30] < 0.25)

print(f"\n{sum(OK)}/{len(OK)} checks passed")
sys.exit(0 if all(OK) else 1)
