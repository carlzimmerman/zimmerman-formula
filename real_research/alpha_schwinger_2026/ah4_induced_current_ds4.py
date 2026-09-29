#!/usr/bin/env python3
"""AH4 -- induced current of a charged scalar in dS_4: direct mode sum with adiabatic subtraction vs the published closed form.

Pre-registered in AH4_PREREGISTRATION.md (written before this script was run).  Units H = 1, tau = -1 (a = 1), planar patch.
  lambda = eE/H^2,  mu_phys = m/H,  mu_w = sqrt(9/4 - lambda^2 - mu_phys^2)  (imaginary = i rho for lambda^2 + mu_phys^2 > 9/4)
Mode:     q_k = e^{i kappa pi/2} (2k)^{-1/2} W_{kappa, mu_w}(2 i k tau),  kappa = -i lambda r,  r = k_z/k
Current:  <J_z> = e a H^3/(4 pi^2) f(lambda, mu_phys);   f_direct = -2 Int dk k^2 Int dr (k r - lambda) [ |q_k|^2 - S~(k, r) ]
with the order-T^-2 adiabatic term S~ = 1/(2 Omega) - delta/(2 Omega^2) subtracted inside the integrand.
Comparator: Kobayashi & Afshordi arXiv:1408.4141 eq. (2.58) (transcribed from the PDF; tested here, see V0/V1).

Run:   python3 ah4_induced_current_ds4.py            (real run)
       python3 ah4_induced_current_ds4.py --mutate   (control: delta dropped from the subtraction; must FAIL V1)
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


def check(tag, ok, detail):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


# ------------------------------------------------------------------ adiabatic subtraction, built symbolically
def build_subtraction(with_delta=True):
    t, k, r, lam, mu = sp.symbols("t k r lam mu", real=True)
    Om2 = (k * r + lam / t) ** 2 + k ** 2 * (1 - r ** 2) + mu ** 2 / t ** 2      # Omega^2, with a^2 m^2 = mu^2/t^2
    Om = sp.sqrt(Om2)
    d1 = sp.diff(Om, t)
    d2 = sp.diff(Om, t, 2)
    if with_delta:
        delta = (-2 / t ** 2 + sp.Rational(3, 4) * (d1 / Om) ** 2 - sp.Rational(1, 2) * d2 / Om) / (2 * Om)
    else:
        delta = 0
    S = 1 / (2 * Om) - delta / (2 * Om ** 2)
    return sp.lambdify((t, k, r, lam, mu), S, modules="numpy")


def q2_exact(k, r, lam, mu_phys):
    """|q_k|^2 at tau = -1 from the Whittaker function (mpmath), returned as float."""
    mw = mp.sqrt(mp.mpf(9) / 4 - mp.mpf(lam) ** 2 - mp.mpf(mu_phys) ** 2)
    z = 2j * k * TAU
    w = mp.whitw(-1j * lam * r, mw, z)
    return float(abs(w) ** 2 * mp.e ** (PI * lam * r) / (2 * k))


_S = None


def integrand_k(k, lam, mu_phys, xr, wr, with_delta):
    """g(k) = k^2 Int dr (k r - lam)[|q|^2 - S~]  (Gauss-Legendre in r)."""
    global _S
    if _S is None:
        _S = build_subtraction(with_delta)
    tot = 0.0
    for r, w in zip(xr, wr):
        d = q2_exact(k, r, lam, mu_phys) - float(_S(TAU, k, r, lam, mu_phys))
        tot += w * (k * r - lam) * d
    return k * k * tot


def _segment(args):
    a, b, lam, mu_phys, n_gl, n_r, with_delta = args
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    xr, wr = np.polynomial.legendre.leggauss(n_r)
    s = 0.0
    for x, w in zip(xg, wg):
        k = 0.5 * (b - a) * x + 0.5 * (b + a)
        s += 0.5 * (b - a) * w * integrand_k(k, lam, mu_phys, xr, wr, with_delta)
    return s


def _point(args):
    lam, mu_phys, K, n_seg, n_gl, n_r, with_delta = args
    mp.mp.dps = 22
    k0 = 1e-40
    edges = np.exp(np.linspace(math.log(k0), math.log(K), n_seg + 1))
    total = sum(_segment((a, b, lam, mu_phys, n_gl, n_r, with_delta)) for a, b in zip(edges[:-1], edges[1:]))
    xr, wr = np.polynomial.legendre.leggauss(n_r)
    ks = np.array([0.5 * K, 0.75 * K, K])
    fs = np.array([integrand_k(kk, lam, mu_phys, xr, wr, with_delta) * kk * kk for kk in ks])
    A = np.array([[1.0, 1.0 / kk, 1.0 / (kk * kk)] for kk in ks])
    c2, c3, c4 = np.linalg.solve(A, fs)
    tail = c2 / K + c3 / (2 * K * K) + c4 / (3 * K ** 3)
    return -2.0 * (total + tail), c2


def direct_f(points, K=200.0, n_seg=60, n_gl=12, n_r=24, with_delta=True):
    jobs = [(lam, mu, K, n_seg, n_gl, n_r, with_delta) for lam, mu in points]
    with ProcessPoolExecutor(max_workers=min(len(jobs), 14)) as ex:
        return list(ex.map(_point, jobs))


# ------------------------------------------------------------------ closed form (2.58), as transcribed
def closed_form_f(lam, mu_phys):
    mp.mp.dps = 30
    lam = mp.mpf(lam)
    m = mp.mpf(mu_phys)
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
    return float(-2 * lam ** 3 / 15 + (lam / 3) * mp.log(m) + mp.re(T1) - mp.re(T2) + integ)


if __name__ == "__main__":
    print("=" * 100)
    print("AH4 induced current in dS_4 -- mode: " + ("MUTATE CONTROL (delta dropped)" if MUTATE else "REAL RUN"))
    print("=" * 100, flush=True)

    # ------------------------------------------------------------------ V0: transcription sanity
    print("\n0. TRANSCRIPTION of eq. (2.58): finite and linear as lambda -> 0, odd in lambda")
    v0_ok = True
    for mu_phys in (1.0, 2.0):
        f3 = closed_form_f(1e-3, mu_phys) / 1e-3
        f4 = closed_form_f(1e-4, mu_phys) / 1e-4
        rel = abs(f4 - f3) / abs(f3)
        print(f"     mu = {mu_phys}:  f/lambda at 1e-3: {f3:+.8f}   at 1e-4: {f4:+.8f}   rel diff {rel:.1e}")
        v0_ok = v0_ok and rel < 1e-3
    fp = closed_form_f(0.4, 1.0)
    fm = closed_form_f(-0.4, 1.0)
    odd = abs(fp + fm) / abs(fp)
    print(f"     oddness: f(+0.4) = {fp:+.8f}, f(-0.4) = {fm:+.8f}, |f(+)+f(-)|/|f(+)| = {odd:.1e}")
    v0_ok = v0_ok and odd < 1e-3
    check("V0 transcribed closed form is finite, linear as lambda -> 0 at two masses, and odd in lambda", v0_ok, "")

    # ------------------------------------------------------------------ V1: direct vs closed form
    GRID = [(0.5, 2.0), (1.0, 1.5), (0.3, 1.0), (0.5, 1.2), (1.5, 0.8), (0.4, 1.4), (0.3, 3.0)]
    print("\n1. DIRECT mode sum (order-T^-2 adiabatic subtraction) vs closed form (2.58); f = 4 pi^2 J/(e H^3)")
    t0 = time.time()
    res = direct_f(GRID, with_delta=not MUTATE)
    print(f"     ({time.time() - t0:.0f} s on {min(len(GRID), 14)} processes)")
    print("     lambda   mu_phys   mu_w^2      direct f         closed f         ratio      tail c2")
    ratios = []
    for (lam, mu_phys), (fd, c2) in zip(GRID, res):
        fc = closed_form_f(lam, mu_phys)
        ratios.append(fd / fc)
        mw2 = 2.25 - lam ** 2 - mu_phys ** 2
        print(f"     {lam:5.2f}   {mu_phys:6.2f}   {mw2:+7.3f}   {fd:+.8f}   {fc:+.8f}   {fd / fc:+.6f}   {c2:+.2e}", flush=True)
    worst = max(abs(abs(x) - 1.0) for x in ratios)
    same_sign = all((x > 0) == (ratios[0] > 0) for x in ratios)
    v1_ok = worst <= 2e-3 and same_sign
    sign_note = "+" if np.median(ratios) > 0 else "-"
    check("V1 direct = closed form on the whole grid with one consistent sign", v1_ok,
          f"(worst |ratio| - 1 = {worst:.1e}; sign of direct/closed = {sign_note})")

    if MUTATE:
        print("\nMUTATE CONTROL: the order-T^-2 term delta was dropped from the subtraction (order 0 only).")
        print(f"  V1 {'FAILED as required -- the control works' if not v1_ok else 'DID NOT FAIL -- the check has no power'}")
        sys.exit(0 if not v1_ok else 1)

    # ------------------------------------------------------------------ V2: heavy-field behaviour (closed form, small lambda)
    print("\n2. HEAVY FIELDS from the closed form at small lambda:  F(mu) = |f|/lambda")
    lam_s = 1e-3
    Fm = {}
    print("     mu     F(mu) = |f/lambda|       bare log term (1/3) ln mu")
    for mu_phys in (2.0, 5.0, 10.0, 20.0, 40.0):
        Fm[mu_phys] = abs(closed_form_f(lam_s, mu_phys) / lam_s)
        print(f"     {mu_phys:5.1f}   {Fm[mu_phys]:.6e}        {math.log(mu_phys) / 3:.4f}")
    slope = (math.log(Fm[40.0]) - math.log(Fm[10.0])) / (math.log(40.0) - math.log(10.0))
    print(f"     log-log slope between mu = 10 and 40: {slope:.4f}")
    check("V2 power-law fall ~ 1/mu^2 (slope in [-2.3, -1.7]) and the ln(m) term is cancelled (F(40) < 1/3)",
          -2.3 <= slope <= -1.7 and Fm[40.0] < 1.0 / 3.0, f"(slope {slope:.3f}, F(40) = {Fm[40.0]:.3e})")

    # ------------------------------------------------------------------ V3: running of e
    print("\n3. THE ln(m/H) TERM IS THE ONE-LOOP RUNNING OF e")
    tt, x, y, zc, EE, HH = sp.symbols("tau x y z E H", real=True)
    a = -1 / (HH * tt)
    # F_{tau z} = E a^2 ; F^{tau z} = g^{tt} g^{zz} F_{tz} = -E/a^2 ; sqrt(-g) = a^4 ; nabla_nu F^{nu z} = a^-4 d_tau( a^4 F^{tau z} )
    Ftz_up = -EE / a ** 2
    div = sp.simplify(sp.diff(a ** 4 * Ftz_up, tt) / a ** 4)
    print(f"     nabla_nu F^(nu z) = {div}   (at tau = -1, H = 1, E = 1: {float(div.subs({tt: -1, HH: 1, EE: 1})):+.6f}; = -2 E H / a)")
    coef_log = (1.0 / 3.0) / (4 * PI ** 2)                          # (e H^3/(4 pi^2)) (lambda/3) ln(m/H) = coef_log * e H^3 lambda ln(m/H)
    # in terms of e^2 E H: e H^3 lambda = e^2 E H, so the log term is coef_log * e^2 E H ln(m/H)
    running = (1.0 / (24 * PI ** 2)) * 2.0                          # d(1/e^2)/d ln(mu) = -1/(24 pi^2) times |nabla F| = 2 E H
    print(f"     coefficient of e^2 E H ln(m/H) in the current:  {coef_log:.10e}  (= 1/(12 pi^2) = {1 / (12 * PI ** 2):.10e})")
    print(f"     one-loop scalar-QED running x |nabla F| / (E H):  {running:.10e}  (1/(24 pi^2) x 2)")
    check("V3 the ln(m/H) coefficient equals the scalar-QED one-loop running times |nabla_nu F^(nu z)| (|ratio| = 1 to 1e-12)",
          abs(abs(coef_log / running) - 1) < 1e-12 and abs(abs(float(div.subs({tt: -1, HH: 1, EE: 1}))) - 2.0) < 1e-12, "")

    # ------------------------------------------------------------------ V4: ties
    print("\n4. THE alpha QUESTION:  sigma/H = alpha * G(mu),  G = f_1/pi,  alpha = e^2/(4 pi) (now the 4D constant)")
    MASSES = (0.5, 1.0, 2.0, 5.0)
    G = {}
    print("     mu      |G(mu)| = |f/lambda|/pi")
    for mu_phys in MASSES:
        G[mu_phys] = abs(closed_form_f(lam_s, mu_phys) / lam_s) / PI
        print(f"     {mu_phys:4.1f}    {G[mu_phys]:.6e}")
    CS = {"kappa": KAPPA, "kappa/pi": KAPPA / PI, "1/(2 pi)": 1 / (2 * PI), "1/pi": 1 / PI, "1": 1.0, "2 kappa": 2 * KAPPA}
    print("\n   Tie sigma/H = c: required alpha = c/|G(mu)|")
    print("     c            " + "".join(f"mu={m:<10.1f}" for m in MASSES) + " spread (max/min)")
    any_det = False
    for name, c in CS.items():
        vals = [c / G[m] for m in MASSES]
        spread = max(vals) / min(vals)
        any_det = any_det or spread < 2.0
        print(f"     {name:11s}  " + "".join(f"{v:<13.4e}" for v in vals) + f" {spread:.2e}")
    check("V4 no tie on the conductivity fixes alpha independently of the mass (declared: spread < 2 would count)", not any_det, "")

    Cfit = 0.5 * (Fm[20.0] * 20.0 ** 2 + Fm[40.0] * 40.0 ** 2) / PI
    H0_EV = 67.4e3 / 3.0856775814913673e22 * 6.582119569e-16
    MU_E = 0.51099895e6 / H0_EV
    print(f"\n   Electron-mass reading (EXTRAPOLATION |G| ~ C/mu^2, C = {Cfit:.4f} from mu = 20, 40): mu_e = {MU_E:.3e}")
    for name, c in list(CS.items())[:2]:
        print(f"     tie sigma/H = {name} = {c:.4f}:  required alpha ~ c mu_e^2 / C = {c * MU_E ** 2 / Cfit:.2e}")

    print("\n" + "=" * 100)
    passed = sum(1 for _, ok in CHECKS if ok)
    print(f"CHECKS: {passed}/{len(CHECKS)} passed")
    print("VERDICT (against the declared criteria): see the numbers above; alpha stays an INPUT (flat-space renormalization condition),")
    print("  the dS_4 scalar current is alpha times a mass function G(mu), and no tie on it fixes alpha.")
    print("  Scalar only; fermions, backreaction, other species untested.  kappa = 1/2 stays FITTED.  The SM-mass wall is unchanged.")
    sys.exit(0 if passed == len(CHECKS) else 1)
