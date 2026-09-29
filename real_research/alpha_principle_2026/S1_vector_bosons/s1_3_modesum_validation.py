#!/usr/bin/env python3
"""S1 script 3 -- validation of the direct mode-sum machinery (ODE vacuum + adiabatic subtraction) that s1_4 uses.

Pre-registered in S1_PREREGISTRATION.md (Amendment 3 records the development smoke tests that preceded this script and what they changed).  Units H = c = 1.
Checks (C1-C4):
  C1  adiabatic machinery: Gamma_0 stationary and pure; series residual of Gamma' = A Gamma + Gamma A^T falls with k (scalar, W_y, {x,z} at g = 2);
  C2  SCALAR regression: direct mode sum with the second-order adiabatic subtraction (Kobayashi-Afshordi counting: a''/a tagged order 2) = the published closed form
      (AH4 script, eq. 2.58) at five (lambda, mu) points, worst relative difference <= 2e-3, one consistent sign (pipeline = -f_KA, the sign fixed here for all later use);
  C3  W_y polarization = a scalar of mass^2 m^2 + 2 H^2 up to a finite, computed scheme term:  f_y(lambda,mu) = -f_KA,closed(lambda, sqrt(mu^2+2)) + Delta,
      Delta = Int k^2 dk Int dr 2 p [S_KA(mu_s; a''/a = 2) - S_KA(mu; a''/a = 0)]  (independent sympy/quadrature code), 3 points, <= 3e-3 relative;
  C4  {x,z} block exact dynamics: purity preserved along the ODE (<= 1e-8) and independence of the initial time T (order-4 initial data): current at k = 20 for
      T = 1500, 3000, 6000 agrees to 1e-7.
Run:    python3 s1_3_modesum_validation.py            (real run; exit 0 iff all checks pass)
        python3 s1_3_modesum_validation.py --mutate   (control: the second-order adiabatic term is dropped in the SCALAR subtraction (order 0 only): C2 must FAIL;
                                                       prints CONTROL FAILS AS REQUIRED and exits 1; exits 3 if the control does not fail)
Any other argv silently runs the real path.
"""
import sys
import os
import math
import importlib.util
import numpy as np
import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MUTATE = "--mutate" in sys.argv
_ARGV = list(sys.argv)
sys.argv = [sys.argv[0]]
import s1_lib as L
import s1_modesum as S
sys.argv = _ARGV

CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def load_ah4():
    spec = importlib.util.spec_from_file_location("ah4", os.path.join(HERE, "..", "..", "alpha_schwinger_2026", "ah4_induced_current_ds4.py"))
    mod = importlib.util.module_from_spec(spec)
    saved = sys.argv
    sys.argv = [saved[0]]
    spec.loader.exec_module(mod)
    sys.argv = saved
    return mod


def ka_delta_scheme(lam, mu_y, K=60.0):
    """Delta = Int k^2 dk Int dr 2 p [S_s - S_y], S = 1/(2 Omega) - delta/(2 Omega^2), delta = [-s_a/t^2 + 3/4 (Omega'/Omega)^2 - 1/2 Omega''/Omega]/(2 Omega);
    S_s: mass mu_s = sqrt(mu_y^2 + 2), s_a = 2 (KA scalar);  S_y: mass mu_y, s_a = 0 (vector counting).  Evaluated at t = -1, p = k r - lambda."""
    t, k, r, la, m_, sa = sp.symbols("t k r la m sa", real=True)
    Om2 = (k * r + la / t) ** 2 + k**2 * (1 - r**2) + m_**2 / t**2
    Om = sp.sqrt(Om2)
    d1, d2 = sp.diff(Om, t), sp.diff(Om, t, 2)
    delta = (-sa / t**2 + sp.Rational(3, 4) * (d1 / Om) ** 2 - sp.Rational(1, 2) * d2 / Om) / (2 * Om)
    Sx = 1 / (2 * Om) - delta / (2 * Om**2)
    Sf = sp.lambdify((t, k, r, la, m_, sa), Sx, "mpmath")
    mp.mp.dps = 30
    mus = math.sqrt(mu_y**2 + 2)

    def D(kk, rr):
        return 2 * (kk * rr - lam) * (Sf(-1, kk, rr, lam, mus, 2) - Sf(-1, kk, rr, lam, mu_y, 0))

    def g(kk):
        return kk**2 * mp.quad(lambda rr: D(kk, rr), [-1, 0, 1])

    tot = mp.quad(g, [1e-9, 0.01, 0.1, 1, 3, 10, 30, K])
    kk = [K / 4, K / 2, K]
    A = np.array([[float(x) ** (-j) for j in (3, 4, 5)] for x in kk])
    coef = np.linalg.solve(A, np.array([float(g(x)) for x in kk]))
    tail = sum(cj * K ** (1 - j) / (j - 1) for cj, j in zip(coef, (3, 4, 5)))
    return float(tot) + tail


if __name__ == "__main__":
    print("=" * 110)
    print("S1 script 3: mode-sum machinery validation -- " + ("MUTATE CONTROL (scalar subtraction at order 0 only)" if MUTATE else "REAL RUN"))
    print("=" * 110, flush=True)
    rng = np.random.default_rng(3)

    # ------------------------------------------------------------------ C1
    print("\nC1  adiabatic machinery")
    ok1a = True
    for kind in ("scalar", "y", "xz"):
        m = S.get_model(kind, 1, "alg")
        n = m.n
        J = L.Jmat(n // 2)
        for it in range(10):
            kz, kp, lam, mu, tau = rng.uniform(-1, 1), rng.uniform(0.2, 1.5), rng.uniform(0.05, 1.0), rng.uniform(0.3, 3.0), -rng.uniform(2.0, 30.0)
            h = m.h_total(tau, kz, kp, lam, mu)
            hj0 = m.hj(tau, kz, kp, lam, mu)
            G0 = L.gamma0_closed(hj0[0][0])
            A0 = J @ hj0[0][0]
            ok1a = ok1a and np.linalg.norm(A0 @ G0 + G0 @ A0.T) < 1e-9 * max(1, np.linalg.norm(A0)) and np.linalg.norm(G0 @ J @ G0 - 0.25 * J) < 1e-9
    check("C1a Gamma_0 = (1/2) h^{-1/2}|K|h^{-1/2} is stationary under A_0 and pure (G J G = J/4) for scalar, W_y, {x,z} (30 random points)", ok1a)

    # jets vs finite differences of the closed form (order-0 jets)
    ok1b = True
    worst = 0.0
    for kind in ("scalar", "xz"):
        m = S.get_model(kind, 1, "alg")
        for it in range(5):
            kz, kp, lam, mu, tau = rng.uniform(-1, 1), rng.uniform(0.3, 1.5), rng.uniform(0.05, 0.6), rng.uniform(0.6, 3.0), -rng.uniform(4.0, 20.0)
            d = 1e-2
            Gm2 = L.gamma0_closed(m.hj(tau - 2 * d, kz, kp, lam, mu)[0][0])
            Gm1 = L.gamma0_closed(m.hj(tau - d, kz, kp, lam, mu)[0][0])
            Gp1 = L.gamma0_closed(m.hj(tau + d, kz, kp, lam, mu)[0][0])
            Gp2 = L.gamma0_closed(m.hj(tau + 2 * d, kz, kp, lam, mu)[0][0])
            G0 = L.gamma0_closed(m.hj(tau, kz, kp, lam, mu)[0][0])
            d1 = (-Gp2 + 8 * Gp1 - 8 * Gm1 + Gm2) / (12 * d)
            d2 = (-Gp2 + 16 * Gp1 - 30 * G0 + 16 * Gm1 - Gm2) / (12 * d * d)
            hb = m.hj(tau, kz, kp, lam, mu)
            Gam, res = L.adiabatic_jets(hb, order=2)
            e1 = np.linalg.norm(Gam[0][1] - d1) / np.linalg.norm(d1)
            e2 = np.linalg.norm(Gam[0][2] - d2) / np.linalg.norm(d2)
            worst = max(worst, e1, e2)
    ok1b = worst < 2e-4
    check("C1b implicit-differentiation jets of Gamma_0 (first and second derivative) equal 4th-order finite differences of the closed form (scalar, {x,z})", ok1b, f"(worst relative difference {worst:.1e})")

    # series residual scaling
    def series_gamma(m, tau, kz, kp, lam, mu, order):
        ser, Gam, U, res = L.current_series(m, tau, kz, kp, lam, mu, order=2)
        Gb = sum(Gam[n][0] for n in range(order + 1))
        return U @ Gb @ U.T
    ok1c = True
    for kind in ("scalar", "y", "xz"):
        m = S.get_model(kind, 1, "alg")
        r, lam, mu = 0.3, 0.3, 1.0
        kz, kp = r, math.sqrt(1 - r * r)
        rel = []
        for k in (10.0, 40.0):
            tau, d = -k, 1e-3 * k
            Gp, Gm, G0 = (series_gamma(m, tau + s * d, kz, kp, lam, mu, 2) for s in (1, -1, 0))
            a = (tau, kz, kp, lam, mu)
            A = L.Jmat(m.n // 2) @ m.h_total(*a)
            rel.append(np.linalg.norm((Gp - Gm) / (2 * d) - (A @ G0 + G0 @ A.T)) / np.linalg.norm(G0))
        slope = math.log(rel[1] / rel[0]) / math.log(4.0)
        print(f"     {kind}: residual of Gamma' = A Gamma + Gamma A^T after order 2: {rel[0]:.2e} (k=10), {rel[1]:.2e} (k=40); slope {slope:.2f}")
        ok1c = ok1c and slope < -2.5
    check("C1c series through order 2 solves Gamma' = A Gamma + Gamma A^T up to a remainder falling faster than k^-2.5 (scalar, W_y, {x,z} at g = 2)", ok1c)

    # ------------------------------------------------------------------ C2
    print("\nC2  SCALAR regression vs the published closed form (AH4 script, eq. 2.58): pipeline f = -f_KA")
    ah4 = load_ah4()
    GRID2 = [(0.5, 2.0), (1.0, 1.5), (0.3, 1.0), (0.4, 1.4), (0.3, 3.0)]
    order_used = 1 if MUTATE else 2
    ratios = []
    for lam, mu in GRID2:
        f = S.f_point("scalar", 1, "alg", lam, mu, K=40.0, T=3000.0, order_used=order_used)
        fc = ah4.closed_form_f(lam, mu)
        ratios.append(-f / fc)
        print(f"     lambda={lam:4.2f} mu={mu:4.2f}  pipeline f = {f:+.8f}   closed form (KA sign) = {fc:+.8f}   -pipeline/closed = {-f / fc:+.6f}", flush=True)
    worst2 = max(abs(x - 1) for x in ratios)
    same = all(x > 0 for x in ratios)
    ok2 = worst2 <= 2e-3 and same
    check("C2 scalar: direct mode sum (ODE vacuum + second-order adiabatic subtraction) = closed form (2.58), worst |ratio - 1| <= 2e-3, sign pipeline = -f_KA", ok2, f"(worst {worst2:.1e})")
    if MUTATE:
        print("\nMUTATE CONTROL: the order-2 adiabatic term was dropped; C2 " + ("FAILED as required" if not ok2 else "DID NOT FAIL"))
        print("CONTROL FAILS AS REQUIRED" if not ok2 else "CONTROL DID NOT FAIL")
        sys.exit(1 if not ok2 else 3)

    # ------------------------------------------------------------------ C3
    print("\nC3  W_y = scalar of mass^2 m^2 + 2 H^2 + computed scheme term")
    ok3 = True
    for lam, mu in [(0.2, 0.2), (0.3, 0.8), (0.5, 1.2)]:
        fy = S.f_point("y", 1, "alg", lam, mu, K=40.0, T=3000.0)
        mus = math.sqrt(mu**2 + 2)
        fc = ah4.closed_form_f(lam, mus)
        Dl = ka_delta_scheme(lam, mu)
        pred = -fc + Dl
        rel = abs(fy - pred) / abs(pred)
        ok3 = ok3 and rel <= 3e-3
        print(f"     lambda={lam} mu={mu}: pipeline f_y = {fy:+.7f};  -f_KA,closed(mu_s={mus:.4f}) = {-fc:+.7f};  Delta = {Dl:+.3e};  -f_KA + Delta = {pred:+.7f};  rel diff {rel:.1e}", flush=True)
    check("C3 f_y (vector counting, no a''/a) = -f_KA,closed(mu_s^2 = mu^2 + 2) + Delta (independent quadrature) at three points, <= 3e-3", ok3)

    # ------------------------------------------------------------------ C4
    print("\nC4  {x,z} block exact dynamics")
    m = S.get_model("xz", 1, "alg")
    lam, mu, r = 0.5, 0.7, 0.4
    kz, kp = r, math.sqrt(1 - r * r)
    ks = np.array([20.0, 50.0])
    taus = np.sort(-ks)
    Gs, _ = S.exact_nodes(m, r, lam, mu, taus, T=3000.0, init_order=4)
    Jm = L.Jmat(2)
    pur = max(np.linalg.norm(G @ Jm @ G - 0.25 * Jm) for G in Gs)
    vals = {}
    for T in (1500.0, 3000.0, 6000.0):
        Gt, _ = S.exact_nodes(m, r, lam, mu, np.array([-20.0]), T=T, init_order=4)
        U, _ = m.U(-20.0, kz, kp, lam, mu)
        vals[T] = L.current_exact(m, -20.0, kz, kp, lam, mu, Gt[0], U)
    spread = max(vals.values()) - min(vals.values())
    print(f"     purity |G J G - J/4| along the ODE (k = 20, 50): {pur:.1e};  current at k = 20 for T = 1500, 3000, 6000: {[f'{v:.10f}' for v in vals.values()]} (spread {spread:.1e})")
    check("C4 purity preserved (<= 1e-8) and the exact current is independent of the initial time (spread <= 1e-7)", pur <= 1e-8 and spread <= 1e-7)

    print("\nCHECKS: %d/%d passed" % (sum(1 for _, ok in CHECKS if ok), len(CHECKS)))
    sys.exit(0 if all(ok for _, ok in CHECKS) else 1)
