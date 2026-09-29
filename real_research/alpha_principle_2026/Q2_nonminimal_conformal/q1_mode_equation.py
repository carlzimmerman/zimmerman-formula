#!/usr/bin/env python3
"""Q2/q1 -- the mode equation of a charged scalar with xi R phi^2 in planar dS_D, derived from the covariant field equation,
and verified against the Whittaker solution by independent numerical integration.

Pre-registered in Q2_PREREGISTRATION.md (written before this script was run).

Checks
  M1  symbolic: covariant box + metric (Christoffels, Ricci scalar) for D = 2..6 gives, for chi = a^{(D-2)/2} phi,
      chi'' + [(k_z + lam/tau)^2 + k_perp^2 + (mu^2 + xi D(D-1))/tau^2 - D(D-2)/(4 tau^2)] chi = 0  and  R = D(D-1) H^2
  M2  symbolic: chi(tau) = W(2 i k tau) with Whittaker index kappa_W = -i lam r and mu_w^2 = (D-1)^2/4 - lam^2 - mu^2 - xi D(D-1)
      (D = 4: 9/4 - lam^2 - mu^2 - 12 xi) solves it; for xi = 1/6, m = 0 the index is 1/4 - lam^2
  M3  numeric: DOP853 integration of the ODE (rtol 1e-13) from tau = -3 to -0.2 vs the Whittaker function, 8 parameter sets, <= 1e-8
  M4  Wronskian q q*' - q* q' = i (Bunch-Davies normalisation), 1e-10
  M5  |q|^2 -> 1/(2k) at tau = -3000 (5e-3)

Run:    python3 q1_mode_equation.py            (real run; exit 0 iff every check passes)
        python3 q1_mode_equation.py --mutate   (control: the dS_2 index 1/4 - lam^2 - mu^2 is used in place of the dS_4 index;
                                               M3 must FAIL; exit 1 = "control fails as required", exit 3 = control did NOT fail)
"""
import sys
import math
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp

MUTATE = "--mutate" in sys.argv
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


# ---------------------------------------------------------------- M1: covariant derivation, general D
def derive_mode_equation(D):
    t = sp.symbols("t", real=True)
    H, m, xi, e, E, k = sp.symbols("H m xi e E k", positive=True)
    ks = sp.symbols(f"k1:{D}", real=True)          # k1 is the direction of the field (z), k2.. transverse
    xs = sp.symbols(f"x1:{D}", real=True)
    X = [t] + list(xs)
    a = -1 / (H * t)
    g = sp.diag(*([-a ** 2] + [a ** 2] * (D - 1)))
    ginv = g.inv()
    n = D
    # Christoffel symbols and Ricci scalar (R_{mn} = d_l G^l_{mn} - d_n G^l_{ml} + G^l_{ls} G^s_{mn} - G^l_{ns} G^s_{ml})
    Gam = [[[sum(ginv[l, s] * (sp.diff(g[s, mu], X[nu]) + sp.diff(g[s, nu], X[mu]) - sp.diff(g[mu, nu], X[s])) for s in range(n)) / 2
             for nu in range(n)] for mu in range(n)] for l in range(n)]
    Ric = sp.zeros(n, n)
    for mu in range(n):
        for nu in range(n):
            Ric[mu, nu] = sum(sp.diff(Gam[l][mu][nu], X[l]) for l in range(n)) \
                - sum(sp.diff(Gam[l][mu][l], X[nu]) for l in range(n)) \
                + sum(Gam[l][l][s] * Gam[s][mu][nu] for l in range(n) for s in range(n)) \
                - sum(Gam[l][nu][s] * Gam[s][mu][l] for l in range(n) for s in range(n))
    Rs = sp.simplify(sum(ginv[i, i] * Ric[i, i] for i in range(n)))
    # gauge potential: F_{t z} = E a^2, A_z = -E/(H^2 t), covariant derivative D = d - i e A
    Az = -E / (H ** 2 * t)
    chi = sp.Function("chi")
    f = a ** (-sp.Rational(D - 2, 2)) * chi(t)
    phi = f * sp.exp(sp.I * sum(ks[i] * xs[i] for i in range(D - 1)))

    def Dmu(expr, mu):
        return sp.diff(expr, X[mu]) - (sp.I * e * Az * expr if mu == 1 else 0)
    sqrtg = a ** D
    box = 0
    for mu in range(n):
        box += Dmu(sqrtg * ginv[mu, mu] * Dmu(phi, mu), mu)
    box = box / sqrtg
    eq = box - (m ** 2 + xi * Rs) * phi
    eq = sp.simplify(eq / sp.exp(sp.I * sum(ks[i] * xs[i] for i in range(D - 1))) * a ** (sp.Rational(D - 2, 2) + 2))
    # expected:  chi'' + [ (k1 - e A)^2 + kperp^2 + a^2 (m^2 + xi R) - D(D-2)/4 / t^2 ] chi
    kperp2 = sum(ks[i] ** 2 for i in range(1, D - 1))
    expected = sp.diff(chi(t), t, 2) + ((ks[0] - e * Az) ** 2 + kperp2 + a ** 2 * (m ** 2 + xi * D * (D - 1) * H ** 2)
                                         - sp.Rational(D * (D - 2), 4) / t ** 2) * chi(t)
    resid = sp.simplify(sp.expand(eq + expected))          # signature (-,+,..): g^{tt} < 0, so the covariant equation is MINUS the ODE (Amendment 1)
    return Rs, resid


print("=" * 100)
print("Q2/q1 mode equation -- " + ("MUTATE CONTROL (dS_2 index used for dS_4)" if MUTATE else "REAL RUN"))
print("=" * 100, flush=True)

print("\nM1. Covariant derivation, D = 2..6 (metric -> Christoffels -> Ricci scalar -> box with gauge field)")
m1_ok = True
for D in (2, 3, 4, 5, 6):
    Rs, resid = derive_mode_equation(D)
    H = sp.symbols("H", positive=True)
    okR = sp.simplify(Rs - D * (D - 1) * H ** 2) == 0
    okE = resid == 0
    m1_ok = m1_ok and okR and okE
    print(f"     D = {D}:  R = {Rs}   [R - D(D-1)H^2 = 0: {okR}]   mode-equation residual = {resid}")
check("M1 general-D mode equation and R = D(D-1) H^2 (5 dimensions, zero symbolic residual)", m1_ok)

# ---------------------------------------------------------------- M2: Whittaker substitution (symbolic)
print("\nM2. Whittaker substitution chi(tau) = W(2 i k tau), kappa_W = -i lam r, symbolic")
tau = sp.symbols("tau", real=True)
k, r, lam, mu, xi = sp.symbols("k r lam mu xi", positive=True)
z = 2 * sp.I * k * tau
W0 = sp.symbols("W0")


def whittaker_residual(mw2):
    kappaW = -sp.I * lam * r
    # W'' = [1/4 - kappa/z - (1/4 - mu_w^2)/z^2] W  (Whittaker's equation);  chi'' = (2 i k)^2 W''
    chi_pp = (2 * sp.I * k) ** 2 * (sp.Rational(1, 4) - kappaW / z - (sp.Rational(1, 4) - mw2) / z ** 2) * W0
    kz = k * r
    kperp2 = k ** 2 * (1 - r ** 2)
    pot = (kz + lam / tau) ** 2 + kperp2 + (mu ** 2 + 12 * xi - 2) / tau ** 2
    return sp.simplify((chi_pp + pot * W0) / W0)


mw2_gen = sp.Rational(9, 4) - lam ** 2 - mu ** 2 - 12 * xi
res_gen = whittaker_residual(mw2_gen)
res_conf = whittaker_residual(sp.Rational(1, 4) - lam ** 2).subs({mu: 0, xi: sp.Rational(1, 6)})
res_wrong = whittaker_residual(sp.Rational(1, 4) - lam ** 2 - mu ** 2)      # the dS_2 index: must NOT solve the dS_4 xi = 0 equation
res_wrong0 = sp.simplify(res_wrong.subs(xi, 0))
print(f"     general xi, mu_w^2 = 9/4 - lam^2 - mu^2 - 12 xi :  residual = {res_gen}")
print(f"     xi = 1/6, m = 0, mu_w^2 = 1/4 - lam^2            :  residual = {res_conf}")
print(f"     (power test) dS_2 index at xi = 0                :  residual = {res_wrong0}  (must be non-zero)")
check("M2 Whittaker index reproduces the mode equation symbolically (general xi and the conformal massless case)",
      res_gen == 0 and res_conf == 0 and res_wrong0 != 0)

# ---------------------------------------------------------------- M3-M5: numerical
mp.mp.dps = 30
SETS = [(0.8, 0.5, 0.0, 1 / 6), (1.5, -0.3, 0.0, 1 / 6), (0.3, 0.9, 0.0, 1 / 6), (1.2, 0.2, 0.7, 1 / 6),
        (0.5, 0.4, 1.0, 0.0), (1.3, 1.0, 0.5, 0.0), (0.6, -0.6, 0.4, 0.3), (0.4, -1.0, 0.9, 0.05)]
K = 1.0


def mw2_used(lam_, mu_, xi_):
    if MUTATE:
        return 0.25 - lam_ ** 2 - mu_ ** 2
    return 2.25 - lam_ ** 2 - mu_ ** 2 - 12 * xi_


def q_mode(t, lam_, r_, mu_, xi_):
    mw = mp.sqrt(mp.mpf(mw2_used(lam_, mu_, xi_)))
    kap = -1j * lam_ * r_
    return mp.e ** (1j * kap * mp.pi / 2) * (2 * K) ** (-0.5) * mp.whitw(kap, mw, 2j * K * t)


def rhs(t, y, lam_, r_, mu_, xi_):
    pot = (K * r_ + lam_ / t) ** 2 + K ** 2 * (1 - r_ ** 2) + (mu_ ** 2 + 12 * xi_ - 2) / t ** 2
    return [y[1], -pot * y[0], y[3], -pot * y[2]]                 # (Re, Re', Im, Im')


print("\nM3. Numerical ODE (DOP853, rtol 1e-13) from tau = -3 to -0.2 vs the Whittaker mode; M4 Wronskian; M5 BD normalisation")
print("     lambda    r      mu    xi      |ODE - Whittaker| (rel)     |Wronskian - i|     |2k|q|^2 - 1| at tau=-3000")
worst3 = worst4 = worst5 = 0.0
for lam_, r_, mu_, xi_ in SETS:
    t0, t1 = -3.0, -0.2
    q0 = q_mode(mp.mpf(t0), lam_, r_, mu_, xi_)
    dq0 = mp.diff(lambda tt: q_mode(tt, lam_, r_, mu_, xi_), mp.mpf(t0))
    y0 = [float(q0.real), float(dq0.real), float(q0.imag), float(dq0.imag)]
    sol = solve_ivp(rhs, (t0, t1), y0, method="DOP853", rtol=1e-13, atol=1e-16, args=(lam_, r_, mu_, xi_))
    q1 = q_mode(mp.mpf(t1), lam_, r_, mu_, xi_)
    dq1 = mp.diff(lambda tt: q_mode(tt, lam_, r_, mu_, xi_), mp.mpf(t1))
    yn = sol.y[:, -1]
    num = math.sqrt((yn[0] - float(q1.real)) ** 2 + (yn[2] - float(q1.imag)) ** 2 + (yn[1] - float(dq1.real)) ** 2 + (yn[3] - float(dq1.imag)) ** 2)
    den = math.sqrt(float(abs(q1)) ** 2 + float(abs(dq1)) ** 2)
    d3 = num / den
    tw = mp.mpf(-0.5)
    qw = q_mode(tw, lam_, r_, mu_, xi_)
    dqw = mp.diff(lambda tt: q_mode(tt, lam_, r_, mu_, xi_), tw)
    wr = qw * mp.conj(dqw) - mp.conj(qw) * dqw
    d4 = float(abs(wr - 1j))
    qf = q_mode(mp.mpf(-3000), lam_, r_, mu_, xi_)
    d5 = float(abs(2 * K * abs(qf) ** 2 - 1))
    worst3, worst4, worst5 = max(worst3, d3), max(worst4, d4), max(worst5, d5)
    print(f"     {lam_:5.2f}  {r_:+5.2f}  {mu_:4.2f}  {xi_:5.3f}   {d3:.3e}                {d4:.3e}           {d5:.3e}", flush=True)
m3_ok = worst3 <= 1e-8
check("M3 numerical ODE = Whittaker mode on 8 parameter sets", m3_ok, f"(worst {worst3:.2e}; threshold 1e-8)")

if MUTATE:
    print("\nMUTATE CONTROL: the dS_2 index 1/4 - lam^2 - mu^2 was used for the dS_4 modes (identical for xi = 1/6, wrong for the xi != 1/6 sets).")
    if not m3_ok:
        print("  M3 FAILED as required -- CONTROL FAILS AS REQUIRED")
        sys.exit(1)
    print("  M3 did NOT fail -- CONTROL DID NOT FAIL (the check has no power)")
    sys.exit(3)

check("M4 Wronskian q q*' - q* q' = i (Bunch-Davies normalisation) on 8 sets", worst4 <= 1e-10, f"(worst {worst4:.2e}; threshold 1e-10)")
check("M5 |q|^2 -> 1/(2k) in the far past on 8 sets", worst5 <= 5e-3, f"(worst {worst5:.2e}; threshold 5e-3)")

print("\n" + "=" * 100)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("VERDICT: the covariant derivation gives mu_w^2 = (D-1)^2/4 - lam^2 - mu^2 - xi D(D-1); for D = 4 this is 9/4 - lam^2 - mu^2 - 12 xi,")
print("  and for the conformally coupled massless scalar (xi = 1/6, m = 0) it is 1/4 - lam^2 (in every D); the Whittaker mode is the")
print("  Wronskian-normalised Bunch-Davies solution.  Scalar only; no claim about alpha.  kappa = 1/2 stays FITTED.")
sys.exit(0 if passed == len(CHECKS) else 1)
