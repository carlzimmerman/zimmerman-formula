#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG311 -- STRONG-FIELD NEUTRON-STAR SENSITIVITY s AT alpha_c != 0 IN THE FILTERED C-H/K CHASSIS (closes CFG291's condition).
Criteria frozen and committed first: campaign_fresh_gravity/CFG311_ns_sensitivity/FROZEN_CRITERIA.md (f41011ad5).

Chassis at NS scales (CFG291 N: the heat filter removes the C-H sector, exponent ~ -6e21): the BPS khronon,
  I = (1/16 pi G) Int sqrt(-g) [R + alpha a_mu a^mu - lambda K^2],  alpha = alpha_c,  beta = 0,  lambda = c_2.
Method (FROZEN_CRITERIA sec. 1): first-order (Hellmann-Feynman) perturbation in alpha about Barausse 2019's exact
alpha = beta = 0 solution (static TOV metric in the star frame + the maximal-slicing (K = 0) khronon of a star moving at
v relative to the khronon).  -delta m~(v) = (alpha/16 pi G) Int d^3x sqrt(-g) a^2 = dL_0 + dL_2 v^2;  sigma = 2 dL_2 / M,
s = sigma/(1 + sigma) = alpha (sigma/alpha) + O(alpha^2, alpha^2/lambda).
DERIVED here (sympy): the khronon ODE (E1), a^2 to O(v^2) two ways (E2), the angle-integrated integrand (E3).
ADOPTED: Barausse 2019 (alpha = beta = 0 solutions), Foster 2007 eq. 70 (weak-field target), Read et al. 2009 piecewise
polytropes (RECALLED parameters), CFG291's committed scorer (exec'd read-only, all writes sent to os.devnull).

CFG311_MUTATE=1 flips alpha -> -alpha_c (outputs carry _MUTATE; the window gate must flag it, rc = 1).
Run from anywhere:  python3 campaign_fresh_gravity/CFG311_ns_sensitivity/cfg311_ns_sensitivity.py
"""
import os, sys, io, json, math, time, builtins, contextlib, subprocess
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad, simpson
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG311_MUTATE", "0") == "1"
SLUG = "cfg311_ns_sensitivity"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "CFG311", "mutate": MUTATE, "frozen_criteria_commit": "f41011ad5", "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reading)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 112); P(t); P("=" * 112)


P(__doc__.strip())
if MUTATE:
    P("\n  *** CFG311_MUTATE=1: alpha -> -alpha_c; the window gate must FAIL (rc = 1) ***")

# ================================================================================================ S1 symbolic derivation
banner("S1  SYMBOLIC DERIVATION (sympy): khronon ODE E1, a^2 to O(v^2) two ways E2, angle-integrated integrand E3")
t, r, th, ph, v = sp.symbols("t r theta phi v", real=True)
Phi = sp.Function("Phi")(r); Lam = sp.Function("Lam")(r); F = sp.Function("F")(r)
X = [t, r, th, ph]
g = sp.diag(-sp.exp(2 * Phi), sp.exp(2 * Lam), r**2, r**2 * sp.sin(th)**2); gi = g.inv()
T = t + v * F * sp.cos(th)                     # khronon of a star moving at v relative to the khronon frame (star frame)
dT = [sp.diff(T, x) for x in X]
N = 1 / sp.sqrt(-sum(gi[a, b] * dT[a] * dT[b] for a in range(4) for b in range(4)))   # lapse of the foliation
ul = [-N * d for d in dT]; uu = [sum(gi[a, b] * ul[b] for b in range(4)) for a in range(4)]
sqg = sp.exp(Phi + Lam) * r**2 * sp.sin(th)
Kexpr = sum(sp.diff(sqg * uu[a], X[a]) for a in range(4)) / sqg
K1 = sp.simplify(sp.diff(Kexpr, v).subs(v, 0))
# E1: K1 = 0 <=> (r^2 e^{2Phi - Lam} F')' = 2 e^{2Phi + Lam} F ; verify the expected form symbolically
E1_expected = sp.diff(r**2 * sp.exp(2 * Phi - Lam) * F.diff(r), r) - 2 * sp.exp(2 * Phi + Lam) * F
ratioE1 = sp.simplify(K1 / E1_expected)
E1_ok = (not ratioE1.has(F)) and (not ratioE1.has(sp.Derivative)) and ratioE1 != 0
P(f"    K at O(v) = {sp.factor(K1)}")
P(f"    K1 / [(r^2 e^(2Phi-Lam) F')' - 2 e^(2Phi+Lam) F] = {sp.simplify(ratioE1)}  (no F dependence: {not ratioE1.has(F)})")
flat = sp.dsolve(sp.Eq(sp.diff(r**2 * sp.Function('f')(r).diff(r), r) - 2 * sp.Function('f')(r), 0)).rhs
P(f"    flat limit (r^2 F')' = 2F: F = {flat}")
# E2 (i) lapse formula; (ii) a_mu = u^nu nabla_nu u_mu
lnN = sp.log(N)
hmn = [[gi[a, b] + uu[a] * uu[b] for b in range(4)] for a in range(4)]
a2_i = sum(hmn[a][b] * sp.diff(lnN, X[a]) * sp.diff(lnN, X[b]) for a in range(4) for b in range(4))
Gam = [[[sum(gi[l, s_] * (sp.diff(g[s_, m], X[n]) + sp.diff(g[s_, n], X[m]) - sp.diff(g[m, n], X[s_])) for s_ in range(4)) / 2
         for n in range(4)] for m in range(4)] for l in range(4)]
acc = [sum(uu[n] * (sp.diff(ul[m], X[n]) - sum(Gam[l][n][m] * ul[l] for l in range(4))) for n in range(4)) for m in range(4)]
a2_ii = sum(gi[a, b] * acc[a] * acc[b] for a in range(4) for b in range(4))
a2i_0 = sp.simplify(a2_i.subs(v, 0)); a2ii_0 = sp.simplify(a2_ii.subs(v, 0))
a2i_2 = sp.simplify(sp.diff(a2_i, v, 2).subs(v, 0) / 2); a2ii_2 = sp.simplify(sp.diff(a2_ii, v, 2).subs(v, 0) / 2)
a2i_1 = sp.simplify(sp.diff(a2_i, v).subs(v, 0))
E2_ok = sp.simplify(a2i_2 - a2ii_2) == 0 and sp.simplify(a2i_0 - a2ii_0) == 0 and a2i_1 == 0
P(f"    a^2 at O(v^0) = {a2i_0}   (both routes agree: {sp.simplify(a2i_0 - a2ii_0) == 0}); O(v^1) = {a2i_1}")
P(f"    a^2 at O(v^2): lapse route - Christoffel route = {sp.simplify(a2i_2 - a2ii_2)}")
# E3: angle integral of sqrt(-g) a^2_(2) / (r^2 sin th) -> I2(r) with dL2 = (alpha/16 pi) Int dr r^2 e^{Phi+Lam} I2
I2 = sp.simplify(sp.integrate(sp.integrate(sp.expand(a2i_2 * sp.sin(th)), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi)))
# eliminate F'' with E1
Fpp = sp.solve(sp.Eq(E1_expected, 0), F.diff(r, 2))[0]
I2 = sp.simplify(I2.subs(F.diff(r, 2), Fpp))
P(f"    E3 I2(r) (angle-integrated a^2 at O(v^2), F'' eliminated) = {I2}")
# TOV substitutions (G = c = 1): Lam = -1/2 ln(1 - 2m/r), Phi' = (m + 4 pi r^3 p)/(r (r - 2m)), m' = 4 pi r^2 e
m_, p_, e_, Ph_, F_, Fp_ = sp.symbols("m p e Phi_v F_v Fp_v", real=True)
mf, pf = sp.Function("m")(r), sp.Function("p")(r)
Lam_tov = -sp.log(1 - 2 * mf / r) / 2
Php_tov = (mf + 4 * sp.pi * r**3 * pf) / (r * (r - 2 * mf))
subsd = {}
I2s = I2
for k in (3, 2, 1):
    I2s = I2s.subs(Lam.diff(r, k), sp.diff(Lam_tov, r, k)).subs(Phi.diff(r, k), sp.diff(Php_tov, r, k - 1))
I2s = I2s.subs(Lam, Lam_tov)
I2s = I2s.subs(mf.diff(r), 4 * sp.pi * r**2 * e_).subs(pf.diff(r), -(e_ + pf) * Php_tov)
I2s = I2s.subs({mf: m_, pf: p_, Phi: Ph_}).subs({F.diff(r): Fp_}).subs({F: F_})
I2s = sp.simplify(I2s)
assert not I2s.has(sp.Derivative), I2s
P(f"    I2 in TOV variables (r, m, p, e, Phi, F, F') = {I2s}")
f_I2 = sp.lambdify((r, m_, p_, e_, Ph_, F_, Fp_), I2s, "numpy")
check("S1 symbolic consistency: E1 is K at O(v) (expected form, flat solutions r and r^-2); a^2 at O(v^2) from the lapse "
      "formula equals u^nu nabla_nu u_mu squared; a^2 has no O(v) term",
      f"K1/E1 = {sp.simplify(ratioE1)}; flat F = {flat}; a2 routes differ by {sp.simplify(a2i_2 - a2ii_2)}",
      E1_ok and E2_ok and str(flat).replace(" ", "") in ("C1/r**2+C2*r", "C1*r+C2/r**2"))
OUT["numbers"]["symbolic"] = {"K1": str(K1), "a2_v0": str(a2i_0), "a2_v2": str(a2i_2), "I2": str(I2), "I2_tov": str(I2s)}

# ================================================================================================ W1(a),(b) weak field
banner("W1(a,b)  WEAK-FIELD LIMIT: leading order in G of sigma vs Foster 2007's (11/3) alpha |Omega_N| / M")
eps = sp.Symbol("epsilon", positive=True)
U = sp.Function("U")(r); mu = sp.Function("mu")(r); f = sp.Function("f")(r)
wf_sub = {Phi: -eps * U, Lam: eps * mu, F: r + eps * f}
def wf(expr, order):
    ex = expr.subs({Phi.diff(r, 2): -eps * U.diff(r, 2), Phi.diff(r): -eps * U.diff(r), Lam.diff(r, 2): eps * mu.diff(r, 2), Lam.diff(r): eps * mu.diff(r),
                    F.diff(r, 2): eps * f.diff(r, 2), F.diff(r): 1 + eps * f.diff(r)}).subs(wf_sub)
    return sp.simplify(sp.diff(ex, eps, order).subs(eps, 0) / sp.factorial(order))
I2raw = sp.simplify(sp.integrate(sp.integrate(sp.expand(a2i_2 * sp.sin(th)), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi)))
I2_wf = wf(I2raw, 2)                                   # O(G^2) integrand (sqrt(-g) -> r^2 at this order)
E1_wf = wf(E1_expected, 1)                             # O(G) khronon equation for f
P(f"    O(G) khronon equation: {sp.simplify(E1_wf)} = 0")
P(f"    O(G^2) angle-integrated a^2_(2): {I2_wf}")
# uniform sphere, exact (G = 1): m = M r^3/R^3 inside; U, mu = m/r
Rs, Ms = sp.symbols("R M", positive=True)
min_ = Ms * r**3 / Rs**3; Uin = Ms * (3 * Rs**2 - r**2) / (2 * Rs**3); Uout = Ms / r
fsym = sp.Function("f")
def solve_f(mm, UU):
    eq = E1_wf.subs({U: UU, mu: mm / r}).doit()
    return sp.dsolve(sp.Eq(eq.subs(f, fsym(r)), 0), fsym(r)).rhs
fin_g, fout_g = solve_f(min_, Uin), solve_f(Ms, Uout)
C1s, C2s = sp.symbols("C1 C2")
# regular at 0 (no r^-2), no growing r-term outside (F/r -> 1)
fin_c = sp.expand(fin_g); fout_c = sp.expand(fout_g)
A_, B_ = sp.symbols("A_ B_")
fin = sp.expand(fin_c).subs(sp.Symbol("C1"), 0).subs(sp.Symbol("C2"), A_)
fout = sp.expand(fout_c).subs(sp.Symbol("C2"), 0).subs(sp.Symbol("C1"), B_)
solAB = sp.solve([sp.Eq(fin.subs(r, Rs), fout.subs(r, Rs)), sp.Eq(fin.diff(r).subs(r, Rs), fout.diff(r).subs(r, Rs))], [A_, B_])
fin, fout = fin.subs(solAB), fout.subs(solAB)
def integ(UU, mm, ff, lo, hi):
    ex = I2_wf.subs({U: UU, mu: mm / r, f: ff}).doit()
    return sp.integrate(sp.expand(ex * r**2), (r, lo, hi))
Itot = sp.simplify(integ(Uin, min_, fin, 0, Rs) + integ(Uout, Ms, fout, Rs, sp.oo))
Omega_u = -sp.Rational(3, 5) * Ms**2 / Rs
ratio_u = sp.simplify((2 * Itot / (16 * sp.pi * Ms)) / (sp.Rational(11, 3) * (-Omega_u) / Ms))
P(f"    uniform sphere: f_in = {fin}, f_out = {fout};  Int r^2 I2 dr = {Itot};  sigma/alpha / [(11/3)|Omega_N|/M] = {ratio_u}")
W1a = ratio_u == 1
# n = 1 polytrope, Newtonian, numerical
P(f"    (I2_wf contains f'': {I2_wf.has(f.diff(r, 2))}; U'': {I2_wf.has(U.diff(r, 2))})")
f_rhs = sp.solve(sp.Eq(E1_wf, 0), f.diff(r, 2))[0]
I2_wf_e = I2_wf.subs(f.diff(r, 2), f_rhs)
f_I2wf = sp.lambdify((r, U, U.diff(r), mu, mu.diff(r), f, f.diff(r)), I2_wf_e, "numpy")
f_fpp = sp.lambdify((r, U, U.diff(r), U.diff(r, 2), mu, mu.diff(r), mu.diff(r, 2), f, f.diff(r)), f_rhs, "numpy")
P(f"    f'' from the O(G) equation: {f_rhs}  (contains U'' or mu'': {f_rhs.has(U.diff(r, 2)) or f_rhs.has(mu.diff(r, 2))})")
assert not (f_rhs.has(U.diff(r, 2)) or f_rhs.has(mu.diff(r, 2)))
def newton_poly1():
    Rr = math.pi                                       # rho = sin(x)/x (rho_c = 1), 4 pi G rho_c/(K..) scaled so R = pi
    mfun = lambda x: 4 * math.pi * (math.sin(x) - x * math.cos(x)) if x <= Rr else 4 * math.pi * math.pi
    rho = lambda x: math.sin(x) / x if 0 < x < Rr else (1.0 if x == 0 else 0.0)
    Mt = 4 * math.pi**2
    # U' = -m/r^2, U(inf) = 0; U inside = U(R) + int_r^R m/r^2
    Up = lambda x: -mfun(x) / x**2 if x > 0 else 0.0
    UR = Mt / Rr
    Uin_ = lambda x: UR + quad(lambda y: mfun(y) / y**2, x, Rr, epsabs=1e-13, epsrel=1e-12)[0] if x < Rr else Mt / x
    mu_ = lambda x: mfun(x) / x
    mup = lambda x: 4 * math.pi * x * rho(x) - mfun(x) / x**2
    Upp = lambda x: -4 * math.pi * rho(x) + 2 * mfun(x) / x**3
    mupp = lambda x: 0.0                          # absent from f'' (checked: f_rhs has no U'', mu'')
    def rhs(x, y):
        ff, ffp = y
        return [ffp, f_fpp(x, Uin_(x), Up(x), Upp(x), mu_(x), mup(x), mupp(x), ff, ffp)]
    x0 = 1e-4
    # particular + homogeneous: integrate two solutions from the centre (regular: f ~ a x + O(x^3))
    solp = solve_ivp(rhs, [x0, Rr], [0.0, 0.0], rtol=1e-12, atol=1e-14, dense_output=True)
    solh = solve_ivp(lambda x, y: [y[1], (2 * y[0] - 2 * x * y[1]) / x**2], [x0, Rr], [x0, 1.0], rtol=1e-12, atol=1e-14, dense_output=True)
    # outside: f = -M/2 + B/r^2 (O(G) eq. with m = M); match f, f' at R
    fp_, fpp_ = solp.y[:, -1]; fh_, fhp_ = solh.y[:, -1]
    # c fh + fp = -Mt/2 + B/R^2 ; c fhp + fpp = -2B/R^3
    Amat = np.array([[fh_, -1 / Rr**2], [fhp_, 2 / Rr**3]]); bvec = np.array([-Mt / 2 - fp_, -fpp_])
    cc, BB = np.linalg.solve(Amat, bvec)
    fin_n = lambda x: cc * solh.sol(x) + solp.sol(x)
    Iin = quad(lambda x: f_I2wf(x, Uin_(x), Up(x), mu_(x), mup(x), *fin_n(x)) * x**2, x0, Rr, limit=400, epsabs=1e-12, epsrel=1e-11)[0]
    fo = lambda x: (-Mt / 2 + BB / x**2, -2 * BB / x**3)
    Iout = quad(lambda x: f_I2wf(x, Mt / x, -Mt / x**2, Mt / x, -Mt / x**2, *fo(x)) * x**2, Rr, np.inf, limit=400, epsabs=1e-12, epsrel=1e-11)[0]
    Om = -quad(lambda x: mfun(x) * 4 * math.pi * x**2 * rho(x) / x, x0, Rr, epsabs=1e-13, epsrel=1e-12)[0]
    return (2 * (Iin + Iout) / (16 * math.pi * Mt)) / (11 / 3 * abs(Om) / Mt), Om, -3 * Mt**2 / (4 * Rr)
ratio_p1, Om_p1, Om_p1_an = newton_poly1()
P(f"    Newtonian n = 1 polytrope: Omega_N = {Om_p1:.10g} (analytic -3GM^2/4R = {Om_p1_an:.10g}); ratio = {ratio_p1:.8f}")
W1b = abs(ratio_p1 - 1) < 1e-4 and abs(Om_p1 / Om_p1_an - 1) < 1e-8
OUT["numbers"]["W1ab"] = {"uniform_ratio": str(ratio_u), "uniform_f_in": str(fin), "uniform_f_out": str(fout),
                          "poly1_ratio": ratio_p1}

# ================================================================================================ EOS and TOV
banner("EOS + TOV  Read et al. 2009 piecewise polytropes (RECALLED parameters) and the strong-field integral")
KAPPA = 7.42591549e-29 * 1e10                  # G/c^2 [cm/g] -> rho [g/cm^3] to km^-2
MSUN_KM = 1.4766250614                          # G Msun / c^2 [km]
CRUST = [(6.80110e-9, 1.58425, 0.0), (1.06186e-6, 1.28733, 2.44034e7), (5.32697e1, 0.62223, 3.78358e11), (3.99874e-8, 1.35692, 2.62780e12)]
CORE = {"SLy": (34.384, 3.005, 2.988, 2.851), "APR4": (34.269, 2.830, 3.445, 3.348), "MPA1": (34.495, 3.446, 3.572, 2.887)}
READ_RECALLED = {"SLy": (2.049, 11.736), "APR4": (2.213, 11.428), "MPA1": (2.461, 12.466)}
C_CGS = 2.99792458e10


class PWP:
    """piecewise polytrope in g/cm^3 units: p/c^2 = K rho^Gamma, e/c^2 = (1 + a) rho + K rho^Gamma/(Gamma - 1)."""
    def __init__(self, name, core=None, poly1_K=None):
        self.name = name
        if poly1_K is not None:                 # Gamma = 2 polytrope in geometric units (control)
            self.pieces = [(poly1_K * KAPPA, 2.0, 0.0)]     # p_geo = K rho_geo^2 -> K_cgs = K KAPPA (first run had / KAPPA: disclosed)
        else:
            lp1, g1, g2, g3 = core
            rho1, rho2 = 10**14.7, 10**15.0
            K1 = 10**lp1 / C_CGS**2 / rho1**g1
            K2 = K1 * rho1**(g1 - g2); K3 = K2 * rho2**(g2 - g3)
            Kc, gc = CRUST[-1][0], CRUST[-1][1]
            rho0 = (Kc / K1)**(1 / (g1 - gc))
            self.pieces = CRUST + [(K1, g1, rho0), (K2, g2, rho1), (K3, g3, rho2)]
        a = [0.0]
        for i in range(1, len(self.pieces)):
            Kp, gp, _ = self.pieces[i - 1]; K, gg, rb = self.pieces[i]
            a.append(a[-1] + Kp * rb**(gp - 1) / (gp - 1) - K * rb**(gg - 1) / (gg - 1))
        self.a = a
        self.pb = [K * rb**gg for (K, gg, rb) in self.pieces]
    def from_p(self, p):                        # p in geometric km^-2 -> (rho, e) in km^-2
        pc = p / KAPPA
        i = max(j for j in range(len(self.pieces)) if self.pb[j] <= pc)
        K, gg, _ = self.pieces[i]
        rho = (pc / K)**(1 / gg)
        e = (1 + self.a[i]) * rho + K * rho**gg / (gg - 1)
        return rho * KAPPA, e * KAPPA
    def p_of_rho(self, rho_cgs):
        i = max(j for j in range(len(self.pieces)) if self.pieces[j][2] <= rho_cgs)
        K, gg, _ = self.pieces[i]
        return K * rho_cgs**gg * KAPPA


def tov_star(eos, rho_c_cgs, N=4000, rtol=1e-10, rout_fac=2000.0, want_sigma=True, rho_stop=1e4):
    """returns dict with M, R (km), C, sigma/alpha, Omega_N/M, tail fraction, K residual."""
    pc = eos.p_of_rho(rho_c_cgs)
    p_stop = eos.p_of_rho(rho_stop) if eos.name != "poly1" else pc * 1e-16
    _, ec = eos.from_p(pc)
    def rhs(rr, y):
        m, p, phi, Fv, Gv = y
        if p <= p_stop:
            p = p_stop
        _, e = eos.from_p(p)
        php = (m + 4 * math.pi * rr**3 * p) / (rr * (rr - 2 * m))
        lam = -0.5 * math.log(1 - 2 * m / rr)
        Fp = Gv * math.exp(-2 * phi + lam) / rr**2
        return [4 * math.pi * rr**2 * e, -(e + p) * php, php, Fp, 2 * math.exp(2 * phi + lam) * Fv]
    r0 = 1e-6 * (1.0 / math.sqrt(ec))           # tiny compared with the star
    m0 = 4 / 3 * math.pi * r0**3 * ec
    y0 = [m0, pc, 0.0, r0, r0**2]
    ev = lambda rr, y: y[1] - p_stop; ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, [r0, 1e7], y0, method="DOP853", rtol=rtol, atol=1e-30, events=ev, dense_output=True)
    R = sol.t[-1]; M = sol.y[0, -1]
    out = {"M_msun": M / MSUN_KM, "R_km": R, "C": M / R, "rho_c": rho_c_cgs}
    if not want_sigma:
        return out
    shift = 0.5 * math.log(1 - 2 * M / R) - sol.y[2, -1]
    rg = np.concatenate([np.geomspace(r0, R * 1e-3, N // 8, endpoint=False), np.linspace(R * 1e-3, R, N)])
    Y = sol.sol(rg)
    m, p, phi, Fv, Gv = Y; phi = phi + shift
    p = np.maximum(p, 0.0)
    e = np.array([eos.from_p(max(pp, p_stop))[1] for pp in p])
    lam = -0.5 * np.log(1 - 2 * m / rg)
    Fp = Gv * np.exp(-2 * (phi - shift) + lam) / rg**2
    Iin = simpson(rg**2 * np.exp(phi + lam) * f_I2(rg, m, p, e, phi, Fv, Fp), x=rg)
    # K residual in the interior: K1 bracket from the ODE with F'' by differentiating the dense F' (relative, v = 1)
    Fpp_num = np.gradient(Fp, rg)
    php = (m + 4 * math.pi * rg**3 * p) / (rg * (rg - 2 * m))
    lamp = (4 * math.pi * rg**2 * e * rg - m) / (rg * (rg - 2 * m))
    Kbr = rg**2 * Fpp_num + 2 * rg * Fp + rg**2 * Fp * (2 * php - lamp) - 2 * Fv * np.exp(2 * lam)
    sl = slice(N // 8 + 5, -5)
    scale = np.abs(rg**2 * Fpp_num) + np.abs(2 * rg * Fp) + np.abs(rg**2 * Fp * (2 * php - lamp)) + np.abs(2 * Fv * np.exp(2 * lam))
    Kres_g2 = float(np.max(np.abs(Kbr[sl]) / scale[sl]))   # FIRST-RUN measure (np.gradient, 2nd order): kept, reported
    Kloc_g2 = float(rg[sl][np.argmax(np.abs(Kbr[sl]) / scale[sl])] / R)
    # RECODED measure (after the first run; disclosed): F'' by a 4th-order central difference of the dense F' with step
    # h = 1e-4 R, at points whose stencil crosses no EOS piece boundary and stays inside r < R - 3h (F''' jumps there)
    h = 1e-4 * R
    def Fp_at(rr):
        yy = sol.sol(rr); lm = -0.5 * np.log(1 - 2 * yy[0] / rr)
        return yy[4] * np.exp(-2 * yy[2] + lm) / rr**2
    rk = np.linspace(1e-2 * R, R - 3 * h, 2000)
    rho_b = [pc_[2] for pc_ in eos.pieces[1:]]
    def rho_at(rr):
        return np.array([eos.from_p(max(pp, p_stop))[0] / KAPPA for pp in sol.sol(rr)[1]])
    ok_pts = np.ones(rk.size, bool)
    r_lo, r_hi = rho_at(rk + 2 * h), rho_at(rk - 2 * h)
    for rb in rho_b:
        ok_pts &= ~((r_lo <= rb) & (rb <= r_hi))
    rk = rk[ok_pts]
    Fpp4 = (-Fp_at(rk + 2 * h) + 8 * Fp_at(rk + h) - 8 * Fp_at(rk - h) + Fp_at(rk - 2 * h)) / (12 * h)
    yk = sol.sol(rk); mk, pk, Fk = yk[0], np.maximum(yk[1], 0), yk[3]
    ek = np.array([eos.from_p(max(pp, p_stop))[1] for pp in pk]); Fpk = Fp_at(rk)
    lk = -0.5 * np.log(1 - 2 * mk / rk)
    phpk = (mk + 4 * math.pi * rk**3 * pk) / (rk * (rk - 2 * mk)); lampk = (4 * math.pi * rk**2 * ek * rk - mk) / (rk * (rk - 2 * mk))
    Kb4 = rk**2 * Fpp4 + 2 * rk * Fpk + rk**2 * Fpk * (2 * phpk - lampk) - 2 * Fk * np.exp(2 * lk)
    sc4 = np.abs(rk**2 * Fpp4) + np.abs(2 * rk * Fpk) + np.abs(rk**2 * Fpk * (2 * phpk - lampk)) + np.abs(2 * Fk * np.exp(2 * lk))
    Kres = float(np.max(np.abs(Kb4) / sc4)); Kloc = float(rk[np.argmax(np.abs(Kb4) / sc4)] / R)
    # exterior: exact Schwarzschild; F1 = r - M/2 exact; integrate the ODE outwards to r_out, normalise by A
    FR, FpR = Fv[-1], Fp[-1]
    def rhs_ext(rr, y):
        x = 1 - 2 * M / rr
        Fv_, Gv_ = y
        return [Gv_ / (rr**2 * x**1.5), 2 * math.sqrt(x) * Fv_]
    rout = rout_fac * R
    se = solve_ivp(rhs_ext, [R, rout], [FR, R**2 * (1 - 2 * M / R)**1.5 * FpR], method="DOP853", rtol=rtol, atol=1e-30, dense_output=True)
    F1 = lambda rr: rr - M / 2
    J = lambda rr: quad(lambda u: u**2 / ((1 - 2 * M * u)**1.5 * (1 - M * u / 2)**2), 0.0, 1.0 / rr, epsabs=0, epsrel=1e-13, limit=200)[0]   # u = 1/q
    F2 = lambda rr: F1(rr) * J(rr)
    F2p = lambda rr: J(rr) - 1 / (rr**2 * (1 - 2 * M / rr)**1.5 * (rr - M / 2))
    Fo, Go = se.y[:, -1]; Fpo = Go / (rout**2 * (1 - 2 * M / rout)**1.5)
    A_, B_ = np.linalg.solve(np.array([[F1(rout), F2(rout)], [1.0, F2p(rout)]]), np.array([Fo, Fpo]))
    re = np.geomspace(R, rout, 6 * N)
    Fe, Ge = se.sol(re); xe = 1 - 2 * M / re
    Fpe = Ge / (re**2 * xe**1.5)
    phe = 0.5 * np.log(xe); lame = -0.5 * np.log(xe)
    inte = re**2 * np.exp(phe + lame) * f_I2(re, M + 0 * re, 0 * re, 0 * re, phe, Fe, Fpe)
    Iex = simpson(inte, x=re)
    tail = inte[-1] * re[-1]                       # integrand ~ k/r^2 asymptotically
    Itot = (Iin + Iex + tail) / A_**2
    sig_over_alpha = 2 * Itot / (16 * math.pi * M)
    # Newtonian binding energy of the same profile (weak-field target): Omega_N = -Int m dm / r (e as density)
    Om = -simpson(m * 4 * math.pi * rg**2 * e / rg, x=rg)
    # check the exterior solution: B/A small and F1 exact (residual of F1 in the exterior ODE)
    out.update({"sigma_over_alpha": sig_over_alpha, "OmegaN_over_M": Om / M, "foster_sigma_over_alpha": 11 / 3 * abs(Om) / M,
                "strong_over_weak": sig_over_alpha / (11 / 3 * abs(Om) / M), "tail_frac": tail / (Iin + Iex + tail),
                "K_residual": Kres, "K_residual_at_r_over_R": Kloc, "K_residual_firstrun_grad2": Kres_g2, "K_residual_firstrun_at_r_over_R": Kloc_g2, "K_points_used": int(rk.size), "A_norm": A_, "B_over_A_over_R3": B_ / A_ / R**3, "I_in_frac": Iin / (Iin + Iex + tail)})
    return out


def rho_for_mass(eos, Mtarget, lo=14.3, hi=None, **kw):
    hi = hi if hi is not None else eos.lrho_max
    fm = lambda lr: tov_star(eos, 10**lr, want_sigma=False, **kw)["M_msun"] - Mtarget
    return 10**brentq(fm, lo, hi, xtol=1e-10)


EOSS = {nm: PWP(nm, CORE[nm]) for nm in CORE}
# exterior Schwarzschild: F = r - M/2 is an exact solution (symbolic check)
Mx = sp.Symbol("M", positive=True)
xS = 1 - 2 * Mx / r
ext_res = sp.simplify(sp.diff(r**2 * xS**sp.Rational(3, 2) * sp.diff(r - Mx / 2, r), r) - 2 * sp.sqrt(xS) * (r - Mx / 2))
P(f"    exterior Schwarzschild: residual of F = r - M/2 in E1 = {ext_res}  (exact solution; the decaying one by reduction of order)")
T1rows = {}
okT1 = ext_res == 0
for nm, eos in EOSS.items():
    res = minimize_scalar(lambda lr: -tov_star(eos, 10**lr, want_sigma=False)["M_msun"], bounds=(14.8, 15.8), method="bounded",
                          options={"xatol": 1e-6})
    eos.lrho_max = res.x; Mmax = -res.fun
    r14 = tov_star(eos, rho_for_mass(eos, 1.4), want_sigma=False)["R_km"]
    Mr, Rr_ = READ_RECALLED[nm]
    T1rows[nm] = {"M_max": Mmax, "log10_rho_c_max": res.x, "R_1.4_km": r14, "recalled": READ_RECALLED[nm],
                  "dM": Mmax / Mr - 1, "dR": r14 / Rr_ - 1}
    okT1 &= abs(Mmax / Mr - 1) < 0.02 and abs(r14 / Rr_ - 1) < 0.02 and Mmax > 2.01
    P(f"    {nm:5s}: M_max = {Mmax:.4f} Msun (recalled {Mr}; {100 * (Mmax / Mr - 1):+.2f}%), R_1.4 = {r14:.3f} km "
      f"(recalled {Rr_}; {100 * (r14 / Rr_ - 1):+.2f}%)")
OUT["numbers"]["T1"] = T1rows
check("T1 TOV with the recalled Read et al. 2009 parameters reproduces the recalled M_max and R_1.4 within 2% for SLy, APR4, "
      "MPA1; 2.01 Msun < M_max for each; F = r - M/2 solves E1 exactly in Schwarzschild",
      "; ".join(f"{k_}: M_max {v_['M_max']:.3f} ({100 * v_['dM']:+.2f}%), R1.4 {v_['R_1.4_km']:.2f} ({100 * v_['dR']:+.2f}%)" for k_, v_ in T1rows.items()),
      okT1, "a self-consistency test of recalled numbers (section 0 of FROZEN_CRITERIA), not an independent read")

# ================================================================================================ W1(c) weak field, full code
banner("W1(c)  THE FULL STRONG-FIELD CODE ON LOW-COMPACTNESS STARS vs Foster's (11/3) |Omega_N| / M")
POLY = PWP("poly1", poly1_K=100.0)            # Gamma = 2, K = 100 km^2
W1c = {}
for lab, eos, rc_list in (("poly1", POLY, (5e-6 / KAPPA, 5e-7 / KAPPA)), ("SLy", EOSS["SLy"], (1e10, 1e8))):
    for rc in rc_list:
        st = tov_star(eos, rc)
        W1c[f"{lab} rho_c={rc:.3e}"] = st
        P(f"    {lab:5s} rho_c = {rc:.3e} g/cm^3: M = {st['M_msun']:.4e} Msun, C = {st['C']:.3e}, sigma/alpha = {st['sigma_over_alpha']:.6e}, "
          f"(11/3)|Omega_N|/M = {st['foster_sigma_over_alpha']:.6e}, ratio = {st['strong_over_weak']:.6f}")
devs = {k_: abs(v_["strong_over_weak"] - 1) for k_, v_ in W1c.items()}
okW1c = True
for lab in ("poly1", "SLy"):
    ks = [k_ for k_ in W1c if k_.startswith(lab)]
    hiC, loC = sorted(ks, key=lambda k_: -W1c[k_]["C"])
    okW1c &= W1c[hiC]["C"] <= 1.5e-3 and devs[hiC] < 0.01 and devs[loC] < devs[hiC]
OUT["numbers"]["W1c"] = W1c
check("W1 weak-field limit (Foster 2007 eq. 70 at beta = 0): (a) uniform sphere exactly 11/3; (b) Newtonian n = 1 polytrope "
      "within 1e-4; (c) full code on low-C stars within 1%, deviation shrinking with C",
      f"(a) {ratio_u}; (b) {ratio_p1:.8f}; (c) " + ", ".join(f"{k_} C={W1c[k_]['C']:.1e} dev {d_:.2e}" for k_, d_ in devs.items()),
      W1a and W1b and okW1c, "this also tests the Hellmann-Feynman step (no boundary term): a boundary piece would add an O(G) term not equal to 11/3")

# ================================================================================================ the pulsar stars
banner("NS  sigma/alpha AT THE PULSAR MASSES (SLy, APR4, MPA1), with convergence N1 and the alpha = 0 residual Z1")
MASSES = {"J1738+0333": 1.46, "J0348+0432": 2.01, "J0737-3039A": 1.338185, "J0737-3039B": 1.248868}
TAB = {}
for nm, eos in EOSS.items():
    for lab, Mt in MASSES.items():
        rc = rho_for_mass(eos, Mt)
        st = tov_star(eos, rc)
        TAB[(nm, lab)] = st
        P(f"    {nm:5s} {lab:12s} M = {st['M_msun']:.6f}: R = {st['R_km']:.3f} km, C = {st['C']:.4f}, sigma/alpha = {st['sigma_over_alpha']:.6f}, "
          f"Foster (11/3)|Omega_N|/M = {st['foster_sigma_over_alpha']:.5f}, strong/weak = {st['strong_over_weak']:.4f}, tail {st['tail_frac']:.1e}, "
          f"interior share {st['I_in_frac']:.3f}, K residual {st['K_residual']:.1e} at r/R {st['K_residual_at_r_over_R']:.3f} (first-run grad2 measure {st['K_residual_firstrun_grad2']:.1e} at r/R {st['K_residual_firstrun_at_r_over_R']:.4f})")
# N1 convergence on the most compact star (MPA1/APR4 at 2.01) and one typical
conv = {}
okN1 = True
for key in (("SLy", "J0348+0432"), ("APR4", "J0737-3039A")):
    eos = EOSS[key[0]]; rc = TAB[key]["rho_c"]
    base = tov_star(eos, rc, N=4000)["sigma_over_alpha"]
    n2 = tov_star(eos, rc, N=8000)["sigma_over_alpha"]; n4 = tov_star(eos, rc, N=16000)["sigma_over_alpha"]
    tol = tov_star(eos, rc, N=8000, rtol=1e-12)["sigma_over_alpha"]
    ro = tov_star(eos, rc, N=8000, rout_fac=4000.0)["sigma_over_alpha"]
    conv[f"{key[0]} {key[1]}"] = {"N": base, "2N": n2, "4N": n4, "2N_rtol1e-12": tol, "2N_rout_x2": ro,
                                  "d_2N_4N": abs(n4 / n2 - 1), "d_rtol": abs(tol / n2 - 1), "d_rout": abs(ro / n2 - 1)}
    c_ = conv[f"{key[0]} {key[1]}"]
    okN1 &= c_["d_2N_4N"] < 1e-4 and c_["d_rtol"] < 1e-5 and c_["d_rout"] < 1e-5
    P(f"    N1 {key}: N {base:.8f}, 2N {n2:.8f}, 4N {n4:.8f}; rtol 1e-12 {tol:.8f}; r_out x2 {ro:.8f}")
OUT["numbers"]["N1"] = conv
check("N1 convergence: sigma/alpha changes < 1e-4 between 2N and 4N, < 1e-5 under rtol x 1e-2, < 1e-5 when r_out doubles",
      "; ".join(f"{k_}: {v_['d_2N_4N']:.1e}/{v_['d_rtol']:.1e}/{v_['d_rout']:.1e}" for k_, v_ in conv.items()), okN1)
Kmax = max(st["K_residual"] for st in TAB.values())
# lambda-independence (reading) via the PPN combination at the window: alpha1 - 2 alpha2/3 vs -11 alpha/3 handled after the scorer
OUT["numbers"]["NS"] = {f"{k_[0]} {k_[1]}": v_ for k_, v_ in TAB.items()}

# compactness sweep (reading)
sweep = {}
for nm, eos in EOSS.items():
    rows = []
    Mmax = T1rows[nm]["M_max"]
    for Mt in (0.2, 0.5, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 0.98 * Mmax):
        if Mt >= 0.999 * Mmax:
            continue
        try:
            st = tov_star(eos, rho_for_mass(eos, Mt, lo=14.3))
        except ValueError:
            P(f"    sweep {nm}: M = {Mt} not bracketed on log10 rho_c in [14.3, max]; skipped"); continue
        rows.append({k_: st[k_] for k_ in ("M_msun", "R_km", "C", "sigma_over_alpha", "foster_sigma_over_alpha", "strong_over_weak", "OmegaN_over_M")})
    sweep[nm] = rows
    P(f"    sweep {nm}: " + "; ".join(f"C={rw['C']:.3f}: s/a={rw['sigma_over_alpha']:.4f} (x{rw['strong_over_weak']:.3f} Foster)" for rw in rows))
OUT["numbers"]["compactness_sweep"] = sweep

# s/alpha table and the scored maxima
SA = {lab: max(TAB[(nm, lab)]["sigma_over_alpha"] for nm in EOSS) for lab in MASSES}
SA_min = {lab: min(TAB[(nm, lab)]["sigma_over_alpha"] for nm in EOSS) for lab in MASSES}
for lab in MASSES:
    P(f"    s/alpha_c at {lab:12s} ({MASSES[lab]} Msun): {SA_min[lab]:.4f} .. {SA[lab]:.4f} over the three EOS (scored: max)")
OUT["numbers"]["s_over_alpha"] = {"max_over_EOS": SA, "min_over_EOS": SA_min}

# ================================================================================================ R1 CFG291 scorer, read-only
banner("R1  CFG291's committed scorer, exec'd read-only (every write -> os.devnull), reproduced, then re-scored with computed s")
CFG291_PY = os.path.join(REPO, "campaign_fresh_gravity", "CFG291_khronon_binary_pulsar", "cfg291_khronon_binary_pulsar.py")
CFG291_JS = os.path.join(REPO, "campaign_fresh_gravity", "CFG291_khronon_binary_pulsar", "cfg291_khronon_binary_pulsar_results.json")
committed = json.load(open(CFG291_JS))
_real_open = builtins.open
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        return _real_open(os.devnull, "w")
    return _real_open(file, mode, *a, **k)
ns = {"__file__": CFG291_PY, "__name__": "cfg291_readonly", "open": _ro_open}
_old_mut = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
buf = io.StringIO(); rc291 = None
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(_real_open(CFG291_PY).read(), CFG291_PY, "exec"), ns)
except SystemExit as ex_:
    rc291 = ex_.code
finally:
    if _old_mut is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = _old_mut
cm = committed["numbers"]["W1"]
repro = {b: ns["summary1"][b]["n_pass"] == cm["summary"][b]["n_pass"] for b in ("B0/computed", "B1/computed", "B2/computed", "B1/universal", "B2/universal", "B3/computed")}
marg_ok = abs(float(ns["marg1"].min()) / cm["min_scrit_over_sB2"] - 1) < 5e-4
gs = subprocess.run(["git", "status", "--porcelain", "--", os.path.dirname(CFG291_PY)], cwd=REPO, capture_output=True, text=True).stdout.strip()
P(f"    CFG291 exec rc = {rc291}; pass counts reproduced: {repro}; min s_crit/s_B2 = {float(ns['marg1'].min()):.6e} "
  f"(committed {cm['min_scrit_over_sB2']:.6e}); CFG291 dir git status: '{gs or 'clean'}'")
okR1 = all(repro.values()) and marg_ok and gs == "" and rc291 == 0
check("R1 CFG291's committed scorer reproduces its committed W1 pass counts and min s_crit/s_B2 (5.25e4) before the computed "
      "s replaces the bracket; CFG291's directory is untouched", f"{repro}; margin {float(ns['marg1'].min()):.4e}; git '{gs or 'clean'}'", okR1)

SYS = ns["SYSTEMS"]; score_point = ns["score_point"]; Rpair = ns["Rpair"]; coeffs = ns["coeffs"]; in_window = ns["in_window"]
AC_GRID = ns["AC_GRID"]; C2_W1 = ns["C2_GRID_W1"]
SYS_MASS = {"J1738+0333": "J1738+0333", "J0348+0432": "J0348+0432", "J0737-3039A/B": "J0737-3039A"}
SIGN = -1.0 if MUTATE else 1.0

def s_comp(alpha_c, sysname):
    return SIGN * alpha_c * SA[SYS_MASS[sysname]]

def rescore(ac_grid, c2_grid, nsdiff=False):
    res = {r_: np.ones((len(ac_grid), len(c2_grid)), bool) for r_ in ("computed", "universal")}
    persys = {r_: {k_: 0 for k_ in SYS} for r_ in ("computed", "universal")}
    margin = np.inf; worst = (0, None); maxdip = 0.0
    for i, acv in enumerate(ac_grid):
        for j, c2v in enumerate(c2_grid):
            for nmS, s_sys in SYS.items():
                sNS = s_comp(acv, nmS)
                ns["sens"] = lambda bracket, alpha, lam, _s=sNS: _s
                Rc = Rpair(acv, c2v, s_sys)
                for rmode in ("computed", "universal"):
                    if nsdiff and s_sys["kind"] == "NS-NS":
                        ds = abs(acv * (SA["J0737-3039A"] - SA["J0737-3039B"]))
                        out_ = score_point(acv, c2v, s_sys, "B1", rmode, Rcache=Rc if rmode == "computed" else None, ds_override=ds)
                        s_eff = ds
                    else:
                        out_ = score_point(acv, c2v, s_sys, "B1", rmode, Rcache=Rc if rmode == "computed" else None)
                        s_eff = sNS
                    dmin, dmax, ddip, dq, scrit, ok = out_
                    res[rmode][i, j] &= ok
                    persys[rmode][nmS] += int(ok)
                    if rmode == "computed":
                        margin = min(margin, scrit / abs(s_eff))
                        tns = max(dmax / s_sys["hi"], dmin / s_sys["lo"])
                        if tns > worst[0]:
                            worst = (tns, (acv, c2v, nmS, ddip, dq))
                        maxdip = max(maxdip, ddip)
    return res, persys, margin, worst, maxdip

if not MUTATE:
    resW1, persW1, margW1, worstW1, maxdipW1 = rescore(AC_GRID, C2_W1)
    n1 = {r_: int(resW1[r_].sum()) for r_ in resW1}
    P(f"    W1 with the computed s (max over EOS): computed R {n1['computed']}/{resW1['computed'].size}, universal R {n1['universal']}/{resW1['universal'].size}")
    P(f"    per system (computed R): {persW1['computed']}; per system (universal R): {persW1['universal']}")
    P(f"    min s_crit / s_computed over W1 and systems = {margW1:.4e};  largest dipole delta = {maxdipW1:.3e}; "
      f"max delta/limit = {worstW1[0]:.3e} at alpha_c {worstW1[1][0]:.2e}, c_2 {worstW1[1][1]:.3e}, {worstW1[1][2]}")
    resD, persD, margD, worstD, maxdipD = rescore(AC_GRID, C2_W1, nsdiff=True)
    P(f"    reading, J0737 with the computed |s(1.338) - s(1.249)| = {SA['J0737-3039A'] - SA['J0737-3039B']:.4f} alpha_c: "
      f"{int(resD['computed'].sum())}/{resD['computed'].size} pass; min margin s_crit/|s_eff| {margD:.3e} (the NS-WD systems set it unless the J0737 margin is lower)")
    # s on the window, per system
    s_win = {lab: [AC_GRID[0] * SA[lab], AC_GRID[-1] * SA[lab]] for lab in MASSES}
    for lab, (lo_, hi_) in s_win.items():
        P(f"    s on the window, {lab:12s}: {lo_:.3e} .. {hi_:.3e}")
    # W3 record window
    C2_W3 = np.logspace(-12, -1, 49)
    res3, pers3, marg3, worst3, maxdip3 = rescore(AC_GRID, C2_W3)
    cover = np.array([[acv / c2v <= 1e-3 for c2v in C2_W3] for acv in AC_GRID])
    def edge(mask):
        colok = mask.all(axis=0)
        if colok.all():
            return float(C2_W3[0])
        bad = np.where(~colok)[0]
        return float(C2_W3[bad.max() + 1]) if bad.max() + 1 < len(C2_W3) else float("nan")
    W3 = {"computed_edge": edge(res3["computed"]), "universal_edge": edge(res3["universal"]), "coverage_edge": edge(cover),
          "n_pass_computed": int(res3["computed"].sum()), "n_pass_universal": int(res3["universal"].sum()), "n": int(res3["computed"].size),
          "n_covered": int(cover.sum()), "n_covered_pass_computed": int((res3["computed"] & cover).sum()),
          "n_covered_pass_universal": int((res3["universal"] & cover).sum())}
    P(f"    W3: radiation passes at every alpha_c for c_2 >= {W3['computed_edge']:.3e} (computed R), >= {W3['universal_edge']:.3e} (universal); "
      f"first-order validity alpha/lambda <= 1e-3 at every alpha_c for c_2 >= {W3['coverage_edge']:.3e}; covered points passing "
      f"{W3['n_covered_pass_computed']}/{W3['n_covered']} (computed), {W3['n_covered_pass_universal']}/{W3['n_covered']} (universal)")
    # PPN reading: the weak-field combination over W1 equals -11 alpha/3 (lambda-independence at this order)
    ppn_dev = max(abs((coeffs(a_, c_)["a1"] - 2 * coeffs(a_, c_)["a2"] / 3) / (-11 * a_ / 3) - 1) for a_ in AC_GRID for c_ in C2_W1)
    P(f"    reading: max |(alpha1 - 2 alpha2/3)/(-11 alpha_c/3) - 1| over W1 = {ppn_dev:.2e} (lambda enters only at O(alpha/lambda))")
    OUT["numbers"]["rescore"] = {"W1_pass": n1, "W1_n": int(resW1["computed"].size), "per_system": persW1, "min_scrit_over_s": margW1,
                                 "max_delta_dip": maxdipW1, "worst": [worstW1[0], [float(x) if not isinstance(x, str) else x for x in worstW1[1]]],
                                 "J0737_actual_diff": {"n_pass": int(resD["computed"].sum()), "min_margin": margD}, "s_window": s_win, "W3": W3,
                                 "ppn_combination_dev": ppn_dev}
    Z1_ok = Kmax < 1e-6 and ppn_dev < 1e-5
    check("Z1 alpha -> 0: s = alpha (sigma/alpha) vanishes identically at alpha = 0 (Barausse 2019); the alpha = 0 khronon satisfies "
          "K = 0 (residual < 1e-6); lambda enters only at O(alpha/lambda) (PPN combination = -11 alpha/3 within 1e-5 over W1)",
          f"K residual max {Kmax:.2e}; PPN dev {ppn_dev:.1e}", Z1_ok)
    sw = [TAB[k_]["strong_over_weak"] for k_ in TAB]
    check("READING strong-field s over Foster's weak-field estimate at the pulsar masses (Yagi et al. 2014: realistic stars can "
          "exceed it by up to 200%)", f"{min(sw):.3f} .. {max(sw):.3f}", max(sw) <= 3.0, load_bearing=False)
    check("READING L3 literature-tabulated s point (Yagi et al. 2014): NOT AVAILABLE (no table returned from the HTML read); not run, "
          "not counted as passed", "not run", False, load_bearing=False)
else:
    # MUTATE: alpha -> -alpha_c.  s flips sign; CFG291's scorer cannot evaluate alpha < 0 (c0^2 < 0) and the window gate flags it
    s_m = {lab: -AC_GRID[-1] * SA[lab] for lab in MASSES}
    P(f"    MUTATE s at alpha = -alpha_c,max: " + ", ".join(f"{k_}: {v_:+.3e}" for k_, v_ in s_m.items()))
    flip_ok = all(v_ < 0 for v_ in s_m.values())
    gate = [in_window(-a_, c_)[0] for a_ in AC_GRID for c_ in C2_W1]
    try:
        coeffs(-AC_GRID[-1], C2_W1[0]); scorer_msg = "scorer evaluated alpha < 0 (unexpected)"
    except (ValueError, ZeroDivisionError) as ex_:
        scorer_msg = f"scorer refuses alpha < 0: {type(ex_).__name__} ({ex_}) -- c0^2 = lambda(2 - alpha)/(alpha(2 + 3 lambda)) < 0"
    # sign-blindness of the dipole: score |alpha| with negative s
    ns["sens"] = lambda bracket, alpha, lam: -alpha * SA["J1738+0333"]
    sb = score_point(AC_GRID[-1], C2_W1[0], SYS["J1738+0333"], "B1", "computed")
    ns["sens"] = lambda bracket, alpha, lam: alpha * SA["J1738+0333"]
    sp_ = score_point(AC_GRID[-1], C2_W1[0], SYS["J1738+0333"], "B1", "computed")
    P(f"    {scorer_msg}")
    P(f"    dipole sign-blindness (alpha_c max, c_2 min, J1738): delta_dip with s<0 {sb[2]:.6e}, with s>0 {sp_[2]:.6e}")
    P(f"    window gate (CFG291 in_window) at alpha = -alpha_c: {sum(gate)}/{len(gate)} points inside")
    check("MUTATE s flips sign with alpha (sigma/alpha unchanged, s < 0)", s_m, flip_ok)
    check("MUTATE the radiation score alone cannot see the sign (dipole quadratic in s1 - s2): disclosed", f"{sb[2]:.3e} vs {sp_[2]:.3e}",
          abs(sb[2] / sp_[2] - 1) < 1e-12, load_bearing=False)
    check("WINDOW the scored alpha lies in the frozen chassis window (alpha_c > 0, L340 P1); MUTATE must fail this row",
          f"{sum(gate)}/{len(gate)} inside; {scorer_msg}", all(gate))

# ================================================================================================ VERDICT
banner("VERDICT (frozen rule, FROZEN_CRITERIA sec. 5)")
lb_failed = [n for n, ok, lb in CH if lb and not ok]
if MUTATE:
    verdict = "MUTATE (alpha -> -alpha_c; window gate test; no chassis verdict)"
elif lb_failed:
    verdict = "OPEN"
else:
    nC, nU, nT = n1["computed"], n1["universal"], resW1["computed"].size
    if nC == 0:
        verdict = "KILL"
    elif nC < nT:
        verdict = "CONDITIONAL (sub-window survives; KILL outside it)"
    elif nU < nT:
        verdict = "CONDITIONAL"
    else:
        verdict = "PASS (at the stated scope)"
OUT["verdict"] = verdict
P(f"  failed load-bearing checks: {lb_failed or 'none'}")
if not MUTATE:
    P(f"  W1 with computed s: {n1['computed']}/{resW1['computed'].size} (computed R), {n1['universal']}/{resW1['universal'].size} (universal R); "
      f"min sensitivity margin s_crit/s = {margW1:.3e}")
P(f"  VERDICT: {verdict}")
P(f"  Time {time.time() - T0:.0f} s.")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_pass"], OUT["n_fail_load_bearing"] = len(CH), sum(1 for _, ok, _ in CH if ok), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, _real_open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
