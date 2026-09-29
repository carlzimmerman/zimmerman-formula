#!/usr/bin/env python3
"""Q2/q3 -- induced current of a charged scalar with xi R phi^2 in planar dS_4: direct mode sum with the xi-dependent adiabatic
subtraction, the closed-form-plus-Delta decomposition, and what xi does to the ln(m/H) term and to the heavy/light-field behaviour.

Pre-registered in Q2_PREREGISTRATION.md (before this script was run).  Units H = 1, tau = -1 (a = 1), planar patch.
Conventions exactly as AH4:  f = 4 pi^2 J/(e H^3),  f_direct = -2 Int dk k^2 Int dr (k r - lam)[ |q|^2 - S~ ],
  |q|^2 = |W_{-i lam r, mu_w}(2 i k tau)|^2 e^{pi lam r}/(2k),   mu_w^2 = 9/4 - lam^2 - mu^2 - 12 xi   (derived in q1)
  S~ = 1/(2 Omega) - delta/(2 Omega^2),  delta = [ s/tau^2 + (3/4)(Omega'/Omega)^2 - (1/2) Omega''/Omega ]/(2 Omega),
  Omega^2 = (k_z + lam/tau)^2 + k_perp^2 + mu_sub^2/tau^2,  s = 12 xi - 2  (xi = 0: AH4's -2; xi = 1/6: 0)  [S1 derives this].
Closed form comparator: AH4's transcription of Kobayashi-Afshordi eq. (2.58) for a xi = 0 field of mass mu_eff, mu_eff^2 = mu^2 + 12 xi:
  f = f_0(lam, mu_eff) + Delta,   Delta = Delta_p + Delta_surface,   Delta_p = -2 Int dp p^2 [ I(p; mu_eff) - I(p; mu_sub) ],   I(p; mu, s) = Int dc (p c) S~(p, c; mu, s)
(p = k - lam shifted momentum, exact angular integral, mpmath radial quadrature; I is independent of s), Delta_surface = -lam (mu_eff^2 - 2 - mu_sub^2 - s_sub)/3 is the
radial-k versus spherical-p cutoff-shape term (Amendment 3).  Matched subtraction: s_sub = mu_eff^2 - 2 - mu_sub^2, then Delta = (lam/3) ln(mu_sub/mu_eff).

Run:    python3 q3_current_conformal.py            (real run; exit 0 iff every check passes; about 10-20 minutes on 16 cores)
        python3 q3_current_conformal.py --mutate   (control: AH4's minimal-coupling subtraction constant s = -2 is used for the xi != 0
                                                   modes; the xi != 0 direct sums must FAIL to match; exit 1 = "control fails as
                                                   required", exit 3 = control did NOT fail)
"""
import sys
import math
import time
import numpy as np
import mpmath as mp
import sympy as sp
from concurrent.futures import ProcessPoolExecutor

MUTATE = "--mutate" in sys.argv
PI = math.pi
KAPPA = 0.5
TAU = -1.0
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


# ============================================================ subtraction (sympy) -- used by workers and main
def symbolic_pieces():
    t, kz, kp2, lam, mu, s = sp.symbols("t kz kp2 lam mu s", real=True)
    Q = (kz + lam / t) ** 2 + kp2 + mu ** 2 / t ** 2
    return t, kz, kp2, lam, mu, s, Q


def build_subtraction_kr():
    """S~ as a function of (tau, k, r, lam, mu_sub, s), numpy-lambdified (for the direct k-space sums)."""
    t, kz, kp2, lam, mu, s, Q = symbolic_pieces()
    Om = sp.sqrt(Q)
    d1 = sp.diff(Om, t)
    d2 = sp.diff(Om, t, 2)
    delta = (s / t ** 2 + sp.Rational(3, 4) * (d1 / Om) ** 2 - sp.Rational(1, 2) * d2 / Om) / (2 * Om)
    S = 1 / (2 * Om) - delta / (2 * Om ** 2)
    k, r = sp.symbols("k r", real=True)
    S = S.subs({kz: k * r, kp2: k ** 2 * (1 - r ** 2)})
    return sp.lambdify((t, k, r, lam, mu, s), S, modules="numpy")


def build_I_of_p():
    """I(p; mu, s) = Int_{-1}^{1} dc (p c) S~(p, c) at tau = -1, exact angular integral. Returns (sympy expr, symbols)."""
    t, kz, kp2, lam, mu, s, Q = symbolic_pieces()
    p, c, O = sp.symbols("p c O", positive=True)
    Qs = sp.Function("Qf")(t)
    Om = sp.sqrt(Qs)
    d1 = sp.diff(Om, t)
    d2 = sp.diff(Om, t, 2)
    delta = (s / t ** 2 + sp.Rational(3, 4) * (d1 / Om) ** 2 - sp.Rational(1, 2) * d2 / Om) / (2 * Om)
    S = 1 / (2 * Om) - delta / (2 * Om ** 2)
    Qp = sp.diff(Q, t)
    Qpp = sp.diff(Q, t, 2)
    pz = sp.symbols("pz", real=True)
    at = {t: -1}
    Qp_v = sp.expand(Qp.subs(at).subs(kz, lam + pz))
    Qpp_v = sp.expand(Qpp.subs(at).subs(kz, lam + pz))
    Sx = S.subs(sp.Derivative(Qs, (t, 2)), Qpp_v).subs(sp.Derivative(Qs, t), Qp_v).subs(Qs, O ** 2).subs(t, -1)
    Sx = Sx.subs(pz, p * c)
    Sx = sp.expand(sp.simplify(Sx))
    integrand = sp.expand(p * c * Sx)
    I = sp.integrate(integrand, (c, -1, 1))
    return I, (p, lam, mu, s, O)


# ============================================================ direct k-space sums (AH4 method, general mode index / subtraction)
_S = None


def q2_exact(k, r, lam, mw2):
    mw = mp.sqrt(mp.mpf(mw2))
    z = 2j * k * TAU
    w = mp.whitw(-1j * lam * r, mw, z)
    return float(abs(w) ** 2 * mp.e ** (PI * lam * r) / (2 * k))


def integrand_k(k, lam, mw2, mu_sub, s_sub, xr, wr):
    global _S
    if _S is None:
        _S = build_subtraction_kr()
    tot = 0.0
    for r, w in zip(xr, wr):
        d = q2_exact(k, r, lam, mw2) - float(_S(TAU, k, r, lam, mu_sub, s_sub))
        tot += w * (k * r - lam) * d
    return k * k * tot


def _segment(args):
    a, b, lam, mw2, mu_sub, s_sub, n_gl, n_r = args
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    xr, wr = np.polynomial.legendre.leggauss(n_r)
    s = 0.0
    for x, w in zip(xg, wg):
        k = 0.5 * (b - a) * x + 0.5 * (b + a)
        s += 0.5 * (b - a) * w * integrand_k(k, lam, mw2, mu_sub, s_sub, xr, wr)
    return s


def _point(args):
    lam, mw2, mu_sub, s_sub, K, n_seg, n_gl, n_r = args
    mp.mp.dps = 22
    k0 = 1e-40
    edges = np.exp(np.linspace(math.log(k0), math.log(K), n_seg + 1))
    total = sum(_segment((a, b, lam, mw2, mu_sub, s_sub, n_gl, n_r)) for a, b in zip(edges[:-1], edges[1:]))
    xr, wr = np.polynomial.legendre.leggauss(n_r)
    ks = np.array([0.5 * K, 0.75 * K, K])
    fs = np.array([integrand_k(kk, lam, mw2, mu_sub, s_sub, xr, wr) * kk * kk for kk in ks])
    A = np.array([[1.0, 1.0 / kk, 1.0 / (kk * kk)] for kk in ks])
    c2, c3, c4 = np.linalg.solve(A, fs)
    tail = c2 / K + c3 / (2 * K * K) + c4 / (3 * K ** 3)
    return -2.0 * (total + tail), c2


def direct_f(specs, K=200.0, n_seg=60, n_gl=12, n_r=24):
    """specs: list of (lam, mu_mode, xi, mu_sub, s_sub)."""
    jobs = [(lam, 2.25 - lam ** 2 - mu ** 2 - 12.0 * xi, mu_sub, s_sub, K, n_seg, n_gl, n_r) for lam, mu, xi, mu_sub, s_sub in specs]
    with ProcessPoolExecutor(max_workers=min(len(jobs), 15)) as ex:
        return list(ex.map(_point, jobs))


# ============================================================ closed form f_0 (AH4 transcription) and Delta
def f0_closed(lam, mueff, dps=40):
    mp.mp.dps = dps
    lam = mp.mpf(lam)
    m = mp.mpf(mueff)
    mw = mp.sqrt(mp.mpf(9) / 4 - lam ** 2 - m ** 2)
    s2 = mp.sin(2 * mp.pi * mw)
    pi = mp.pi
    T1 = (45 + 4 * pi ** 2 * (-2 + 3 * lam ** 2 + 2 * mw ** 2)) * mw * mp.cosh(2 * pi * lam) / (12 * pi ** 3 * lam * s2)
    T2 = (45 + 8 * pi ** 2 * (-1 + 9 * lam ** 2 + mw ** 2)) * mw * mp.sinh(2 * pi * lam) / (24 * pi ** 4 * lam ** 2 * s2)

    def integrand(rr):
        poly = -1 + 4 * mw ** 2 + (7 + 12 * lam ** 2 - 12 * mw ** 2) * rr ** 2 - 20 * lam ** 2 * rr ** 4
        e1 = (mp.e ** (2 * pi * rr * lam) + mp.e ** (2j * pi * mw)) * mp.psi(0, mp.mpf(1) / 2 + mw + 1j * rr * lam)
        e2 = (mp.e ** (2 * pi * rr * lam) + mp.e ** (-2j * pi * mw)) * mp.psi(0, mp.mpf(1) / 2 - mw + 1j * rr * lam)
        return mp.re(1j * lam / (16 * s2) * poly * (e1 - e2))

    integ = mp.quad(integrand, [-1, -0.5, 0, 0.5, 1])
    return -2 * lam ** 3 / 15 + (lam / 3) * mp.log(m) + mp.re(T1) - mp.re(T2) + integ


_IFUN = None


def I_fun():
    global _IFUN
    if _IFUN is None:
        I, (p, lam, mu, s, O) = build_I_of_p()
        _IFUN = sp.lambdify((p, lam, mu, s), I.subs(O, sp.sqrt(p ** 2 + mu ** 2)), modules="mpmath")
    return _IFUN


def Delta_p(lam, mueff, mu_sub, dps=40, extra_breaks=()):
    """spherical (kinetic-momentum) integral of the difference of subtractions; independent of s (the s-term is odd in the angle)."""
    mp.mp.dps = dps
    If = I_fun()
    lam = mp.mpf(lam)
    me, ms = mp.mpf(mueff), mp.mpf(mu_sub)
    g = lambda pp: pp ** 2 * (If(pp, lam, me, 0) - If(pp, lam, ms, 0))
    lo = min(me, ms)
    br = sorted(set([mp.mpf(0), lo / 10, lo, 10 * lo, mp.mpf(1), mp.mpf(10), mp.mpf(100), mp.mpf(1000), mp.mpf(10) ** 4, mp.mpf(10) ** 5] + [mp.mpf(x) for x in extra_breaks]))
    return -2 * mp.quad(g, br + [mp.inf])


def Delta(lam, mueff, mu_sub, s_sub, dps=40, extra_breaks=(), surface=True):
    d = Delta_p(lam, mueff, mu_sub, dps, extra_breaks)
    if surface:
        d += -mp.mpf(lam) * (mp.mpf(mueff) ** 2 - 2 - mp.mpf(mu_sub) ** 2 - mp.mpf(s_sub)) / 3
    return d


def Delta_analytic(lam, mueff, mu_sub, s_sub):
    lam, mueff, mu_sub, s_sub = mp.mpf(lam), mp.mpf(mueff), mp.mpf(mu_sub), mp.mpf(s_sub)
    return lam / 3 * (mp.log(mu_sub / mueff) - (mueff ** 2 - 2 - mu_sub ** 2 - s_sub))


def f_formula(lam, mu_mode, xi, mu_sub, s_sub, dps=40):
    mueff = math.sqrt(mu_mode ** 2 + 12.0 * xi)
    return f0_closed(lam, mueff, dps) + Delta(lam, mueff, mu_sub, s_sub, dps)


def f_massless(lam, mu_sub, s_sub=None, dps=40):
    """exactly massless conformal modes (mu_w^2 = 1/4 - lam^2 <=> mu_eff = sqrt 2), subtraction reference mass mu_sub, matched s = -mu_sub^2 by default."""
    if s_sub is None:
        s_sub = -mu_sub ** 2
    return f0_closed(lam, math.sqrt(2.0), dps) + Delta(lam, math.sqrt(2.0), mu_sub, s_sub, dps)


if __name__ == "__main__":
    t_start = time.time()
    print("=" * 100)
    print("Q2/q3 induced current, dS_4 charged scalar with xi R phi^2 -- " + ("MUTATE CONTROL (minimal-coupling subtraction constant used)" if MUTATE else "REAL RUN"))
    print("=" * 100, flush=True)

    # ------------------------------------------------------------ S1: adiabatic terms with xi, derived
    print("\nS1. Adiabatic expansion with xi (derived; not copied from AH4)")
    t, w = sp.symbols("t w", real=True)
    Wf = sp.Function("W")(t)
    Iw = sp.Function("Iw")(t)
    om2 = sp.Function("om2")(t)
    chi = (2 * Wf) ** sp.Rational(-1, 2) * sp.exp(-sp.I * Iw)
    ode = sp.diff(chi, t, 2) + om2 * chi
    ode = ode.subs(sp.Derivative(Iw, (t, 2)), sp.Derivative(Wf, t)).subs(sp.Derivative(Iw, t), Wf)
    lhs = sp.simplify(ode / chi)                          # = om2 - W^2 - (1/2)(W''/W - (3/2)(W'/W)^2) (up to arrangement)
    wkb = om2 - Wf ** 2 - sp.Rational(1, 2) * (sp.diff(Wf, t, 2) / Wf - sp.Rational(3, 2) * (sp.diff(Wf, t) / Wf) ** 2)
    print(f"     chi = (2W)^(-1/2) exp(-i Int W) solves chi'' + om2 chi = 0  <=>  W^2 = om2 - (1/2)(W''/W - (3/2)(W'/W)^2):  residual = {sp.simplify(lhs - wkb)}")
    s1a = sp.simplify(lhs - wkb) == 0
    tt = sp.symbols("tt", real=True)
    eps, xi_ = sp.symbols("eps xi", real=True)
    Om = sp.Function("Om")(tt)                                   # the order-0 frequency, left as an undetermined positive function of tau (Om^2 = Q)
    w2 = sp.symbols("w2")
    Wser = Om + eps ** 2 * w2
    # field-equation frequency^2 = Om^2 + eps^2 (12 xi - 2)/tau^2: the (12 xi - 2)/tau^2 counted at adiabatic order 2 (q1); each tau-derivative carries eps
    om2_eps = Om ** 2 + eps ** 2 * (12 * xi_ - 2) / tt ** 2
    rhs = om2_eps - sp.Rational(1, 2) * eps ** 2 * (sp.diff(Om, tt, 2) / Om - sp.Rational(3, 2) * (sp.diff(Om, tt) / Om) ** 2)
    order2 = sp.expand(sp.series(sp.expand(Wser ** 2 - rhs), eps, 0, 3).removeO()).coeff(eps, 2)
    w2sol = sp.solve(order2, w2)[0]
    delta_ah4 = (-2 / tt ** 2 + sp.Rational(3, 4) * (sp.diff(Om, tt) / Om) ** 2 - sp.Rational(1, 2) * sp.diff(Om, tt, 2) / Om) / (2 * Om)
    d_xi0 = sp.simplify(w2sol.subs(xi_, 0) - delta_ah4)
    d_xi16 = sp.simplify(w2sol.subs(xi_, sp.Rational(1, 6)) - (sp.Rational(3, 4) * (sp.diff(Om, tt) / Om) ** 2 - sp.Rational(1, 2) * sp.diff(Om, tt, 2) / Om) / (2 * Om))
    d_diff = sp.simplify(w2sol - delta_ah4 - 12 * xi_ / (2 * Om * tt ** 2))
    print(f"     second-order term W2(xi) = {w2sol}")
    print(f"     W2(xi) - AH4 delta at xi = 0                                  = {d_xi0}")
    print(f"     W2(1/6) - [(3/4)(Om'/Om)^2 - (1/2) Om''/Om]/(2 Om)   (no a''/a term)            = {d_xi16}")
    print(f"     W2(xi) - AH4 delta - 12 xi/(2 Om tau^2)                                        = {d_diff}")
    check("S1 the xi-dependent second-order adiabatic term is s/tau^2 with s = 12 xi - 2 (AH4 at xi = 0; the a''/a term vanishes at xi = 1/6)",
          s1a and d_xi0 == 0 and d_xi16 == 0 and d_diff == 0)

    # ------------------------------------------------------------ S2: the log coefficient, symbolic
    print("\nS2. Coefficient of the logarithmic divergence of the subtraction, from the large-p expansion of p^2 I(p; mu, s)")
    I_expr, (p_, lam_s, mu_s, s_s, O_s) = build_I_of_p()
    u = sp.symbols("u", positive=True)
    expr = (p_ ** 2 * I_expr).subs({O_s: sp.sqrt(1 + mu_s ** 2 * u ** 2) / u}).subs(p_, 1 / u)
    ser = sp.series(sp.simplify(expr), u, 0, 3).removeO()
    Lcoef = sp.simplify(ser.coeff(u, 1))
    print(f"     coefficient of 1/p in p^2 I(p; mu, s) at large p:  L(lam, mu, s) = {Lcoef}")
    lam_sym = lam_s
    Lmag = sp.simplify(2 * Lcoef)
    print(f"     2 L = {Lmag}  ->  the coefficient of ln(mu_sub) in f is -2L; compare +lam/3 (AH4 V3)")
    for mv, sv in [(1.0, -2.0), (2.0, 0.0), (0.7, 3.5)]:
        print(f"        (mu, s) = ({mv}, {sv}):  -2 L / lam = {float((-Lmag).subs({mu_s: mv, s_s: sv, lam_sym: 1}))}")
    indep = sp.simplify(sp.diff(Lcoef, mu_s)) == 0 and sp.simplify(sp.diff(Lcoef, s_s)) == 0
    mag_ok = sp.simplify(-Lmag - lam_sym / 3) == 0
    check("S2 the ln(m/H) coefficient is lam/3, independent of the subtraction mass and of s (hence of xi)", indep and mag_ok,
          f"(independent of mu and s: {indep}; equals lam/3: {mag_ok})")

    # ------------------------------------------------------------ S3: Delta sanity
    print("\nS3. Delta: numerical p-space integral vs the elementary result (lam/3) ln(mu_sub/mu_eff); identity; breakpoint stability")
    d_id = Delta_p(0.5, 1.3, 1.3)
    worst_an = 0.0
    for lam_t, me_t, ms_t in [(0.5, 1.3, 0.8), (0.3, 2 ** 0.5, 1.0), (1.2, 0.4, 3.0), (0.1, 5.0, 0.05)]:
        num = Delta_p(lam_t, me_t, ms_t)
        an = mp.mpf(lam_t) / 3 * mp.log(mp.mpf(ms_t) / me_t)
        worst_an = max(worst_an, abs(num - an) / abs(an))
        print(f"     lam = {lam_t}, mu_eff = {me_t:.4f}, mu_sub = {ms_t}:  Delta_p numeric = {mp.nstr(num, 15)}   (lam/3) ln(mu_sub/mu_eff) = {mp.nstr(an, 15)}")
    b1 = Delta_p(0.5, 1.3, 0.8)
    b2 = Delta_p(0.5, 1.3, 0.8, extra_breaks=(0.3, 3.0, 30.0))
    check("S3 Delta_p = (lam/3) ln(mu_sub/mu_eff) numerically (4 cases), Delta_p(mu, mu) = 0, stable under breakpoints",
          worst_an < 1e-12 and abs(d_id) < 1e-25 and abs(b1 - b2) / abs(b1) < 1e-12, f"(worst rel diff {float(worst_an):.1e})")

    # ------------------------------------------------------------ direct sums
    XI = 1 / 6
    SPEC_A = [(0.5, 2.0, 0.0), (0.3, 1.0, 0.0), (0.4, 1.4, 0.0)]
    SPEC_B = [(0.3, 1.0, XI), (0.8, 1.0, XI), (0.5, 0.5, XI), (1.2, 0.7, XI), (0.4, 2.0, XI), (0.9, 0.6, XI),
              (0.5, 1.5, 0.1), (0.3, 0.8, 0.1), (0.6, 1.0, 0.3)]
    SPEC_C = [(0.3, 1.0), (0.5, 1.0), (0.8, 1.0), (0.3, 2.0), (0.8, 2.0)]                # matched: s = -mu_s^2
    SPEC_CM = [(0.3, 1.0), (0.8, 2.0)]                                                      # pre-registered mismatched variant: s = 0 (Amendment 3)
    specs, truth = [], []             # specs: (lam, mu_mode, xi, mu_sub, s_used); truth: (lam, mu_mode, xi, mu_sub, s_true, tag)
    for lam, mu, xi in SPEC_A:
        specs.append((lam, mu, xi, mu, -2.0))
        truth.append((lam, mu, xi, mu, -2.0, "A"))
    for lam, mu, xi in SPEC_B:
        s_true = 12 * xi - 2
        specs.append((lam, mu, xi, mu, -2.0 if MUTATE else s_true))
        truth.append((lam, mu, xi, mu, s_true, "B"))
    for lam, mus in SPEC_C:
        specs.append((lam, 0.0, XI, mus, -2.0 if MUTATE else -mus ** 2))
        truth.append((lam, 0.0, XI, mus, -mus ** 2, "C"))
    if not MUTATE:
        for lam, mus in SPEC_CM:
            specs.append((lam, 0.0, XI, mus, 0.0))
            truth.append((lam, 0.0, XI, mus, 0.0, "Cm"))
    print(f"\nDIRECT mode sums ({len(specs)} points: A xi = 0 regression x{len(SPEC_A)}, B xi != 0 massive x{len(SPEC_B)}, C exactly massless conformal, matched x{len(SPEC_C)}"
          + ("" if MUTATE else f", Cm mismatched-s variant x{len(SPEC_CM)}") + "); running ...", flush=True)
    t0 = time.time()
    res = direct_f(specs)
    print(f"     ({time.time() - t0:.0f} s)")
    print("     set  lambda  mu_mode  xi     mu_sub  s_true    direct f          f_0+Delta (with surface)  ratio      | f_0+Delta_p only  ratio       tail c2")
    ratios = {"A": [], "B": [], "C": [], "Cm": []}
    ratios_p = {"A": [], "B": [], "C": [], "Cm": []}
    for (lam, mu, xi, musub, strue, tag), (fd, c2) in zip(truth, res):
        mueff = math.sqrt(mu ** 2 + 12.0 * xi)
        if tag in ("C", "Cm") and abs(lam - 0.5) < 1e-12:
            # the closed form has a removable 0/0 at mu_w = 0 (lam = 1/2); f is smooth, so average two points 1e-5 either side
            f0v = 0.5 * (f0_closed(lam * (1 + 1e-5), mueff) + f0_closed(lam * (1 - 1e-5), mueff))
        else:
            f0v = f0_closed(lam, mueff)
        fc = float(f0v + Delta(lam, mueff, musub, strue))
        fp = float(f0v + Delta_p(lam, mueff, musub))
        ratios[tag].append(fd / fc)
        ratios_p[tag].append(fd / fp)
        print(f"     {tag:2s}  {lam:5.2f}  {mu:6.2f}  {xi:5.3f}  {musub:6.2f}  {strue:+6.2f}  {fd:+.8f}   {fc:+.8f}          {fd / fc:+.6f}  | {fp:+.8f}   {fd / fp:+.6f}   {c2:+.1e}", flush=True)
    worst = {k: (max(abs(x - 1.0) for x in v) if v else float('nan')) for k, v in ratios.items()}
    worst_p = {k: (max(abs(x - 1.0) for x in v) if v else float('nan')) for k, v in ratios_p.items()}
    same = {k: all(x > 0 for x in v) for k, v in ratios.items()}
    okA = worst["A"] <= 2e-3 and same["A"]
    okB = worst["B"] <= 2e-3 and same["B"]
    okC = worst["C"] <= 2e-3 and same["C"]
    print(f"     worst |ratio - 1| (with surface term):  A {worst['A']:.1e}   B {worst['B']:.1e}   C {worst['C']:.1e}   Cm {worst['Cm']:.1e}")
    print(f"     worst |ratio - 1| (p-space only, H4 as literally pre-registered):  A {worst_p['A']:.1e}   B {worst_p['B']:.1e}   C {worst_p['C']:.1e}   Cm {worst_p['Cm']:.1e}")

    if MUTATE:
        print("\nMUTATE CONTROL: the minimal-coupling subtraction constant s = -2 was used for the xi != 0 modes and for the massless-conformal matched set.")
        print(f"  A (xi = 0, unaffected): {'pass' if okA else 'FAIL'};  B: {'pass' if okB else 'FAIL'};  C: {'pass' if okC else 'FAIL'}")
        if (not okB) and (not okC):
            print("  B and C FAILED as required -- CONTROL FAILS AS REQUIRED")
            sys.exit(1)
        print("  B or C did NOT fail -- CONTROL DID NOT FAIL (the check has no power)")
        sys.exit(3)

    check("A direct mode sum reproduces AH4's closed form at xi = 0 (regression of the code, 3 points)", okA, f"(worst {worst['A']:.1e})")
    check("B direct mode sum = f_0(mu_eff) + (lam/3) ln(mu/mu_eff) for xi != 0 massive fields (9 points)", okB, f"(worst {worst['B']:.1e})")
    check("C direct mode sum for the exactly massless conformal scalar = f_0(sqrt 2) + (lam/3) ln(mu_s/sqrt 2) (5 matched points, includes lam = 1/2)", okC, f"(worst {worst['C']:.1e})")
    okCm = worst["Cm"] <= 2e-3
    check("Cm the mismatched-s variant agrees with the surface-term formula (tests Delta_surface; 2 points)", okCm, f"(worst {worst['Cm']:.1e}; p-space-only version misses by {worst_p['Cm']:.1e})")
    print(f"     H4 as literally pre-registered (no surface term): {'REFUTED' if worst_p['Cm'] > 2e-3 else 'not refuted'} at the mismatched points; amended in Amendment 3.")

    # convergence: doubled quadrature at one B and one C point
    print("\nConvergence test: one B point (0.3, 1.0, 1/6) and one C point (0.8, mu_s = 1) with n_seg = 90, n_gl = 16")
    conv_specs = [(0.3, 1.0, XI, 1.0, 12 * XI - 2), (0.8, 0.0, XI, 1.0, -1.0)]
    resc = direct_f(conv_specs, n_seg=90, n_gl=16)
    base = [res[len(SPEC_A)], res[len(SPEC_A) + len(SPEC_B) + 2]]
    dconv = max(abs(a_[0] / b_[0] - 1) for a_, b_ in zip(resc, base))
    print(f"     direct f (fine) = {resc[0][0]:+.8f}, {resc[1][0]:+.8f};  (coarse) = {base[0][0]:+.8f}, {base[1][0]:+.8f}")
    check("convergence: doubled quadrature changes the direct sums by < 1e-4", dconv < 1e-4, f"(max rel change {dconv:.1e})")

    # ------------------------------------------------------------ H5: log slope with the modes held fixed
    print("\nH5. (1/lam) d f / d ln(mu_sub) at FIXED modes, matched subtraction s = mu_eff^2 - 2 - mu_sub^2, four mode indices (mu_eff^2 = 1 + 12 xi)")
    lam_l = 1e-3
    print("     xi       mu_eff     range of mu_sub    slope        (expect 1/3)")
    ok5 = True
    for xi in (0.0, 0.1, 1 / 6, 0.3):
        me = math.sqrt(1.0 + 12 * xi)
        f0v = f0_closed(lam_l, me)
        for a_, b_ in ((0.01, 0.02), (20.0, 40.0)):
            fa = f0v + Delta(lam_l, me, a_, me ** 2 - 2 - a_ ** 2)
            fb = f0v + Delta(lam_l, me, b_, me ** 2 - 2 - b_ ** 2)
            sl = float((fb - fa) / lam_l / math.log(b_ / a_))
            ok5 = ok5 and abs(sl - 1 / 3) < 2e-2
            print(f"     {xi:5.3f}   {me:7.4f}    ({a_}, {b_})        {sl:.6f}")
    fa = f0_closed(lam_l, math.sqrt(2.0)) + Delta(lam_l, math.sqrt(2.0), 20.0, 0.0)
    fb = f0_closed(lam_l, math.sqrt(2.0)) + Delta(lam_l, math.sqrt(2.0), 40.0, 0.0)
    print(f"     (for contrast, MISMATCHED s = 0 at mu_eff = sqrt 2, mu_sub 20 -> 40: slope {float((fb - fa) / lam_l / math.log(2.0)):.3f}; the extra lam mu_sub^2/3 is a gauge-non-invariant term, not a running)")
    check("H5 the coefficient of ln(reference scale) is 1/3 per lam at small and large scale for every xi (matched subtraction)", ok5)

    # ------------------------------------------------------------ H6: heavy fields
    print("\nH6. Heavy fields, F_xi(mu) = f/lam at lam = 1e-3 with mu_sub = mu, s = 12 xi - 2, mu_eff^2 = mu^2 + 12 xi")
    XIS = (0.0, 0.1, 1 / 6, 0.3)
    MUS = (5.0, 10.0, 20.0, 40.0)
    Fh = {}
    print("     xi       " + "".join(f"mu={m:<12.0f}" for m in MUS) + " slope(10->40)   C(20)      C(40)      C_inf (Richardson)")
    Cinf = {}
    ok6 = True
    for xi in XIS:
        row = []
        for mu in MUS:
            Fh[(xi, mu)] = float(f_formula(lam_l, mu, xi, mu, 12 * xi - 2)) / lam_l
            row.append(Fh[(xi, mu)])
        sl = (math.log(abs(Fh[(xi, 40.0)])) - math.log(abs(Fh[(xi, 10.0)]))) / math.log(4.0)
        c20, c40 = Fh[(xi, 20.0)] * 400.0, Fh[(xi, 40.0)] * 1600.0
        Cinf[xi] = (4 * c40 - c20) / 3
        ok6 = ok6 and (-2.3 <= sl <= -1.7)
        print(f"     {xi:5.3f}    " + "".join(f"{v:<14.6e}" for v in row) + f" {sl:8.4f}    {c20:.6f}   {c40:.6f}   {Cinf[xi]:.6f}", flush=True)
    C0, C3 = Cinf[0.0], Cinf[0.3]
    dev = max(abs(Cinf[x] - (C0 + (C3 - C0) * x / 0.3)) for x in (0.1, 1 / 6))
    c1 = (C3 - C0) / 0.3
    print(f"     C(xi) = C0 + c1 xi with C0 = {C0:.6f} (AH4: |f/lam| ~ 0.389/mu^2), c1 = {c1:+.6f};  max deviation of xi = 0.1, 1/6 from the line: {dev:.2e}")
    check("H6a heavy-field power law is ~1/mu^2 for every xi tested (slope in [-2.3, -1.7])", ok6)
    check("H6b the 1/mu^2 coefficient is affine in xi (deviation <= 2e-3)", dev <= 2e-3, f"(deviation {dev:.1e})")
    check("H6c the slope c1 = dC/dxi equals -2 (derived in Amendment 3 before this run; tolerance 5e-3)", abs(c1 + 2.0) < 5e-3, f"(c1 = {c1:+.5f})")
    print(f"     C(xi = 1/6) = {Cinf[1 / 6]:.6f}  (conformal coupling reduces the heavy-field coefficient from {C0:.4f} to {Cinf[1 / 6]:.4f}; the fraction C(1/6)/C0 = {Cinf[1 / 6] / C0:.4f})")

    # ------------------------------------------------------------ H7: light fields
    print("\nH7. Light fields at lam = 1e-3")
    F0 = {}
    for mu in (0.05, 0.1, 0.2):
        F0[mu] = float(f0_closed(lam_l, mu)) / lam_l
        print(f"     xi = 0     mu = {mu:5.2f}   F = {F0[mu]:+.6e}")
    sl0 = (math.log(abs(F0[0.1])) - math.log(abs(F0[0.05]))) / math.log(2.0)
    print(f"     xi = 0: log-log slope of |F| between mu = 0.05 and 0.1: {sl0:.4f}  (IR hyperconductivity, mu_w -> 3/2)")
    G = {}
    for mu in (0.01, 0.02):
        G[mu] = float(f_formula(lam_l, mu, XI, mu, 0.0)) / lam_l
        print(f"     xi = 1/6   mu = {mu:5.2f}   F = {G[mu]:+.8f}   F - (1/3) ln mu = {G[mu] - math.log(mu) / 3:+.8f}")
    dG = abs((G[0.02] - math.log(0.02) / 3) - (G[0.01] - math.log(0.01) / 3))
    check("H7a minimal scalar: |F| ~ mu^-2 as mu -> 0 (slope in [-2.4, -1.6])", -2.4 <= sl0 <= -1.6, f"(slope {sl0:.3f})")
    check("H7b conformal scalar: F - (1/3) ln mu converges as mu -> 0 (no power-law blow-up)", dG <= 5e-3, f"(difference {dG:.1e})")

    # ------------------------------------------------------------ H8: analyticity at lam_c
    print("\nH8. Smoothness of the exactly massless conformal current (subtraction reference mu_s = 1) through lam = 1/2")
    def fm(l):
        return float(f_massless(l, 1.0))
    print("     lam         f_massless(lam)")
    eps_list = (1e-3, 2e-3)
    vals = {}
    for e_ in eps_list:
        for k_ in (1, 2):
            for sg in (+1, -1):
                l = 0.5 + sg * k_ * e_
                vals[(e_, k_, sg)] = fm(l)
    Q = {}
    for e_ in eps_list:
        Dr = (vals[(e_, 2, +1)] - vals[(e_, 1, +1)]) / e_
        Dl = (vals[(e_, 1, -1)] - vals[(e_, 2, -1)]) / e_
        Q[e_] = (Dr - Dl) / e_
        print(f"     eps = {e_:.0e}:  right slope {Dr:+.8f}  left slope {Dl:+.8f}  (Dr - Dl)/eps = {Q[e_]:+.6f}   (a kink would make Dr - Dl -> const, i.e. this ratio ~ 1/eps)")
    lin = abs(Q[eps_list[0]] / Q[eps_list[1]] - 1)
    check("H8 no kink at lam = 1/2: (Dr - Dl)/eps is the same at eps = 1e-3 and 2e-3 (a smooth function; a kink would double it)", lin < 5e-2,
          f"(ratio - 1 = {lin:.1e})")

    # ------------------------------------------------------------ H9: ties
    print("\nH9. Ties for the conformal scalar (xi = 1/6): sigma/H = alpha G_c(mu), G_c = |F|/pi at lam = 1e-3")
    MASSES = (0.5, 1.0, 2.0, 5.0)
    Gc = {}
    for mu in MASSES:
        Gc[mu] = abs(float(f_formula(lam_l, mu, XI, mu, 0.0)) / lam_l) / PI
        print(f"     mu = {mu:4.1f}   |G_c| = {Gc[mu]:.6e}")
    CS = {"kappa": KAPPA, "kappa/pi": KAPPA / PI, "1/(2 pi)": 1 / (2 * PI), "1/pi": 1 / PI, "1": 1.0, "2 kappa": 2 * KAPPA}
    any_det = False
    print("     c            " + "".join(f"mu={m:<10.1f}" for m in MASSES) + " spread (max/min)")
    for name, cval in CS.items():
        vs = [cval / Gc[m] for m in MASSES]
        spread = max(vs) / min(vs)
        any_det = any_det or spread < 2.0
        print(f"     {name:11s}  " + "".join(f"{v:<13.4e}" for v in vs) + f" {spread:.2e}")
    check("H9a no tie on the conformal-scalar conductivity fixes alpha independently of the mass (spread < 2 would count)", not any_det)
    Fm1 = float(f_massless(lam_l, 1.0)) / lam_l
    print(f"     exactly massless, subtraction scale mu_s = 1 (a scale CHOICE, unscored): F = {Fm1:+.8f}, |G| = {abs(Fm1) / PI:.6f}")
    ALPHA = 1 / 137.035999177
    for name, cval in CS.items():
        a_req = cval / (abs(Fm1) / PI)
        print(f"        tie {name:9s}: required alpha_H = {a_req:.5e}  (miss vs 1/137.036: {abs(a_req / ALPHA - 1):.2e})")
    H0_EV = 67.4e3 / 3.0856775814913673e22 * 6.582119569e-16
    MU_E = 0.51099895e6 / H0_EV
    print(f"     Electron-mass reading (EXTRAPOLATION, F ~ C/mu^2 with C(1/6) = {Cinf[1 / 6]:.4f}): mu_e = {MU_E:.3e}; required alpha ~ c mu_e^2/(pi-normalised C):")
    for name in ("kappa", "kappa/pi"):
        print(f"        tie sigma/H = {name}: alpha ~ {CS[name] * MU_E ** 2 / (Cinf[1 / 6] / PI):.2e}")

    print("\n" + "=" * 100)
    passed = sum(1 for _, ok in CHECKS if ok)
    print(f"CHECKS: {passed}/{len(CHECKS)} passed   (elapsed {time.time() - t_start:.0f} s)")
    print("VERDICT (against the declared criteria): see the numbers above.  xi changes the finite part and the 1/mu^2 coefficient, not the ln(m/H)")
    print("  coefficient (lam/3, the flat-space running) and not the power law.  The exactly massless conformal current is alpha x (a log of the")
    print("  scale at which alpha is defined) + a finite function of lam; no tie on it fixes alpha.  Scalar only; kappa = 1/2 stays FITTED.")
    sys.exit(0 if passed == len(CHECKS) else 1)
