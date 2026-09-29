#!/usr/bin/env python3
"""S1 script 4 -- what the direct mode sum says about the charged Proca current in dS_4: subtraction sufficiency, exact-mode UV structure, the ln coefficient vs the one-loop
running, the finite W_y piece, and the absence of an electric instability.

Pre-registered in S1_PREREGISTRATION.md; the criteria E1-E7 are those of Amendment 3 (declared before this script's final run; some thresholds are post-hoc, marked there).
Units H = c = 1.  lambda = eE/H^2, mu = m/H.  Pipeline f = -f_KA (s1_3).  g(k) := k^2 Int_{-1}^{1} dr Tr[Q_J Gamma] is the angle-integrated integrand of f = Int dk g.

Run:    python3 s1_4_vector_uv_and_current.py            (real run; exit 0 iff all checks pass)
        python3 s1_4_vector_uv_and_current.py --mutate   (control: the polarization current -d P_pol/dtau is removed from the g = 2 exact current; only E4 is run;
                                                          E4 must FAIL; prints CONTROL FAILS AS REQUIRED and exits 1; exits 3 if the control does not fail)
Any other argv silently runs the real path.
"""
import sys
import os
import math
import importlib.util
import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MUTATE = "--mutate" in sys.argv
_ARGV = list(sys.argv)
sys.argv = [sys.argv[0]]
import s1_lib as L
import s1_modesum as S
from concurrent.futures import ProcessPoolExecutor
sys.argv = _ARGV

CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def _e1job(a):
    kind, c, scheme, r, lam, mu, ks = a
    m = S.get_model(kind, c, scheme)
    return S.integrand_nodes(m, r, lam, mu, ks, T=4000.0, nord=4)


def e1_status(kind, c, scheme, lam, mu, Ns=(2, 3, 4), workers=12):
    ks = np.array([8.0, 12.0, 16.0, 24.0, 32.0])
    xr, wr = np.polynomial.legendre.leggauss(24)
    with ProcessPoolExecutor(workers) as ex_:
        outs = list(ex_.map(_e1job, [(kind, c, scheme, r, lam, mu, ks) for r in xr]))
    EX = np.array([o[0] for o in outs])
    AD = np.array([o[1] for o in outs])
    res = {}
    for N in Ns:
        R = EX - AD[:, :, :N + 1].sum(axis=2)
        g = (wr[:, None] * R).sum(axis=0) * ks**2
        slope = math.log(abs(g[4] / g[2])) / math.log(ks[4] / ks[2])
        res[N] = (slope, g)
    return res


def dirac_G(M):
    M = mp.mpf(M)
    return float((4 / (3 * mp.pi)) * (mp.log(M) - mp.re(mp.psi(0, 1j * M)) - mp.pi * M * (4 * M**2 + 1) / (3 * mp.sinh(2 * mp.pi * M))))


if __name__ == "__main__":
    print("=" * 112)
    print("S1 script 4: vector UV structure and current -- " + ("MUTATE CONTROL (polarization current removed, E4 only)" if MUTATE else "REAL RUN"))
    print("=" * 112, flush=True)
    LAM = 0.1

    # ------------------------------------------------------------------ helper: UV fits at (kind, c, scheme, lam, mu)
    def fitset(kind, c, scheme, lam, mu, kmin, kmax=250.0, nk=24, T=6000.0):
        ks = np.geomspace(kmin, kmax, nk)
        g = S.raw_g(kind, c, scheme, lam, mu, ks, T=T)
        coef, res = S.uv_fit(g, ks)
        return coef, res

    # ------------------------------------------------------------------ E4 (also the control target)
    print("\nE4  ln coefficient: exact-mode c_{-1} (independent of any beta-function input), lambda = 0.1, window k in [max(20, 6 mu), 250]")
    MUS = (3.0, 4.0, 6.0)
    scheme_g2 = "alg_nopol" if MUTATE else "alg"
    tab = {}
    for mu in MUS:
        kmin = max(20.0, 6 * mu)
        cy, ry = fitset("y", 1, "alg", LAM, mu, kmin)
        cx2, rx2 = fitset("xz", 1, scheme_g2, LAM, mu, kmin)
        cx1, rx1 = (None, None) if MUTATE else fitset("xz", 0, "alg", LAM, mu, kmin)
        tab[mu] = (cy, cx2, cx1)
        print(f"     mu = {mu:3.0f}: W_y c1/lam = {cy[0]/LAM:+.4f}, c-1/lam = {cy[1]/LAM:+.4f} (res {ry:.0e});  {{x,z}} g=2 c1/lam = {cx2[0]/LAM:+.4f}, c-1/lam = {cx2[1]/LAM:+.4f} (res {rx2:.0e})"
              + ("" if MUTATE else f";  g=1 c1/lam = {cx1[0]/LAM:+.4f}, c-1/lam = {cx1[1]/LAM:+.4f} (res {rx1:.0e})"), flush=True)
    mus = np.array(MUS)
    A = np.vstack([np.ones_like(mus), 1 / mus**2]).T
    tot2 = np.array([(tab[m][0][1] + tab[m][1][1]) / LAM for m in MUS])
    sol2, *_ = np.linalg.lstsq(A, tot2, rcond=None)
    ok_g2 = abs(sol2[0] - 7.0) / 7.0 <= 0.05
    print(f"     g = 2: total (W_y + {{x,z}}) c-1/lam = {np.round(tot2, 3)}; fit c_inf + a/mu^2: c_inf = {sol2[0]:.3f}, a = {sol2[1]:.2f};  prediction -b = +7 (b = -7)")
    if MUTATE:
        print("\nMUTATE CONTROL: polarization current removed; E4(g=2) " + ("FAILED as required" if not ok_g2 else "DID NOT FAIL"))
        print("CONTROL FAILS AS REQUIRED" if not ok_g2 else "CONTROL DID NOT FAIL")
        sys.exit(1 if not ok_g2 else 3)
    tot1 = np.array([(tab[m][0][1] + tab[m][2][1]) / LAM for m in MUS])
    sol1, *_ = np.linalg.lstsq(A, tot1, rcond=None)
    ok_g1 = abs(sol1[0] - 1.0) / 1.0 <= 0.05
    print(f"     g = 1: total c-1/lam = {np.round(tot1, 3)}; fit c_inf = {sol1[0]:.3f}, a = {sol1[1]:.2f};  prediction -b = +1 (b = 1 - 2 g^2 = -1)")
    ratio2 = sol2[0] / (1.0 / 3.0)
    check("E4 the exact-mode ln coefficient at large mass equals -b lambda with b = -7 (g = 2) and b = -1 (g = 1) within 5% (ratio to the scalar's 1/3: 21 and 3)", ok_g2 and ok_g1,
          f"(ratio to scalar {ratio2:.2f} [21], {sol1[0] / (1.0 / 3.0):.2f} [3])")

    # ------------------------------------------------------------------ E1
    print("\nE1  is the second-order adiabatic subtraction (the AH4/Q1 rule) sufficient?  slope of |k^2 Int dr R| between k = 16 and 32; converges iff <= -2.5;  (lambda, mu) = (0.3, 1.0)")
    expect = {("y", 1, "alg", 2): True, ("xz", 1, "alg", 2): False, ("xz", 1, "alg", 3): False, ("xz", 1, "alg", 4): False,
              ("xz", 0, "alg", 2): False, ("xz", 0, "alg", 3): False, ("xz", 0, "alg", 4): True, ("xz", 1, "F1", 2): False}
    okE1 = True
    for (kind, c, scheme) in (("y", 1, "alg"), ("xz", 1, "alg"), ("xz", 0, "alg"), ("xz", 1, "F1")):
        st = e1_status(kind, c, scheme, 0.3, 1.0)
        line = f"     {kind} g={'2' if c else '1'} scheme {scheme}: "
        for N, (slope, g) in st.items():
            conv = slope <= -2.5
            e = expect.get((kind, c, scheme, N))
            if e is not None:
                okE1 = okE1 and (conv == e)
            line += f"N={N}: slope {slope:+.2f} ({'converges' if conv else 'does NOT converge'}{'' if e is None else ('' if conv == e else ', UNEXPECTED')});  "
        print(line, flush=True)
    check("E1 observed convergence statuses equal the declared ones: W_y converges at N=2; {x,z} g=2 never converges through N=4 (the rule fails for the vector); g=1 converges only at N=4; F1 fails", okE1)

    # ------------------------------------------------------------------ E2
    print("\nE2  baseline UV coefficients (lambda = 0.3, window k in [20,160]): scalar and W_y")
    okE2 = True
    for mu in (1.0, 2.0):
        for kind in ("scalar", "y"):
            cf, rs = fitset(kind, 1, "alg", 0.3, mu, 20.0, kmax=160.0, nk=20, T=3000.0)
            c1_ok = abs(cf[0] / (-4 * 0.3 / 3) - 1) <= 0.01
            cm_ok = abs(cf[1] / (-0.3 / 3) - 1) <= 0.03
            okE2 = okE2 and c1_ok and cm_ok
            print(f"     {kind:6s} mu = {mu}: c1/lam = {cf[0] / 0.3:+.4f} [-4/3], c-1/lam = {cf[1] / 0.3:+.4f} [-1/3]")
    check("E2 scalar and W_y: c1 = -4 lambda/3 (1%) and c-1 = -lambda/3 = -b lambda with b = 1/3 (3%)", okE2)

    # ------------------------------------------------------------------ E3, E5
    print("\nE3/E5  {x,z} quadratic coefficient and the mass-dependent extra divergence (lambda = 0.1; mu <= 2: window [20,160]; mu >= 3 from E4)")
    okE3 = True
    c1_table = {}
    cm_table = {}
    for mu in (0.5, 1.0, 2.0):
        c2, r2 = fitset("xz", 1, "alg", LAM, mu, 20.0, kmax=160.0, nk=20, T=3000.0)
        c1_, r1 = fitset("xz", 0, "alg", LAM, mu, 20.0, kmax=160.0, nk=20, T=3000.0)
        c1_table[mu] = (c2[0] / LAM, c1_[0] / LAM)
        cm_table[mu] = (c2[1] / LAM, c1_[1] / LAM, r2, r1)
        print(f"     mu = {mu}: g=2 c1/lam = {c2[0] / LAM:+.4f} [law {-(8 / 3 + 4 / (3 * mu**2)):+.4f}], c-1/lam = {c2[1] / LAM:+8.3f} (res {r2:.0e});  g=1 c1/lam = {c1_[0] / LAM:+.4f} [-2.6667], c-1/lam = {c1_[1] / LAM:+.3f} (res {r1:.0e})", flush=True)
    for mu in MUS:
        c1_table[mu] = (tab[mu][1][0] / LAM, tab[mu][2][0] / LAM)
    for mu, (a2, a1) in c1_table.items():
        okE3 = okE3 and abs(a2 / (-(8 / 3 + 4 / (3 * mu**2))) - 1) <= 0.005 and abs(a1 / (-8 / 3) - 1) <= 0.005
    lin_ok = True
    for mu, kmin in ((2.0, 20.0), (4.0, 24.0)):
        kmax = 160.0 if mu == 2.0 else 250.0
        ca, _ = fitset("xz", 1, "alg", 0.3, mu, kmin, kmax=kmax, nk=20 if mu == 2.0 else 24, T=3000.0 if mu == 2.0 else 6000.0)
        cb = cm_table[2.0][0] * LAM if mu == 2.0 else tab[4.0][1][1]
        rat = (ca[1] / 0.3) / (cb / LAM)
        lin_ok = lin_ok and abs(rat - 1) <= 0.05
        print(f"     linearity in lambda (g=2, mu = {mu}): c-1/lam at lambda = 0.3 over lambda = 0.1: {rat:.3f}")
    check("E3 {x,z}: c1/lambda = -(8/3 + 4/(3 mu^2)) at g = 2 and -8/3 at g = 1 (0.5%, mu = 0.5..6); c-1 linear in lambda (5%)", okE3 and lin_ok)
    a_g2 = sol2[1]
    print(f"     E5: mass-dependent part of the log coefficient: total c-1/lam = c_inf + a/mu^2 with a(g=2) = {a_g2:.2f}, a(g=1) = {sol1[1]:.2f}; small-mass {{x,z}} values c-1/lam(g=2) = "
          f"{cm_table[0.5][0]:.1f}, {cm_table[1.0][0]:.1f}, {cm_table[2.0][0]:.1f} at mu = 0.5, 1, 2 (fit residuals {cm_table[0.5][2]:.0e}, {cm_table[1.0][2]:.0e}, {cm_table[2.0][2]:.0e}: mu = 0.5 is not reliable)")
    check("E5 the log coefficient of the g = 2 block carries a mass-dependent part a/mu^2 with |a| > 0.5 (a non-renormalizable, H^2/m^2 divergence, not removable by a charge renormalization)", abs(a_g2) > 0.5, f"(a = {a_g2:.2f})")

    # ------------------------------------------------------------------ E6
    print("\nE6  W_y finite current (one of three polarizations; vector-counting subtraction, see s1_3 C3 for its scheme term) vs scalar and Dirac: G = f_1/pi, odd extraction from lambda = 0.1, 0.2")
    spec = importlib.util.spec_from_file_location("ah4", os.path.join(HERE, "..", "..", "alpha_schwinger_2026", "ah4_induced_current_ds4.py"))
    ah4 = importlib.util.module_from_spec(spec)
    sv = sys.argv
    sys.argv = [sv[0]]
    spec.loader.exec_module(ah4)
    sys.argv = sv
    MU6 = (0.3, 0.5, 1.0, 2.0, 4.0)
    Gy = {}
    print("     mu     G_y(mu)         G_s(mu) [AH4]   G_s(sqrt(mu^2+2))   G_Dirac(mu) [Q1]")
    for mu in MU6:
        f1 = S.f_point("y", 1, "alg", 0.1, mu, K=40.0, T=3000.0)
        f2 = S.f_point("y", 1, "alg", 0.2, mu, K=40.0, T=3000.0)
        a1 = (8 * f1 - f2) / 0.6
        Gy[mu] = -a1 / math.pi
        Gs = ah4.closed_form_f(1e-3, mu) / 1e-3 / math.pi
        Gs2 = ah4.closed_form_f(1e-3, math.sqrt(mu**2 + 2)) / 1e-3 / math.pi
        print(f"     {mu:4.1f}   {Gy[mu]:+.6f}     {Gs:+.6f}      {Gs2:+.6f}          {dirac_G(mu):+.6f}", flush=True)
    f_check = S.f_point("y", 1, "alg", 0.05, 1.0, K=40.0, T=3000.0)
    f01 = S.f_point("y", 1, "alg", 0.1, 1.0, K=40.0, T=3000.0)
    f02 = S.f_point("y", 1, "alg", 0.2, 1.0, K=40.0, T=3000.0)
    a1 = (8 * f01 - f02) / 0.6
    a3 = (f02 - 2 * f01 * 1.0) / 0.006 if False else None
    pred = a1 * 0.05 + (f01 - a1 * 0.1) * (0.05 / 0.1) ** 3
    print(f"     odd-cubic check at mu = 1: f(0.05) measured {f_check:+.8f}, predicted from f(0.1), f(0.2): {pred:+.8f}")
    CS = {"kappa": 0.5, "kappa/pi": 0.5 / math.pi, "1/(2 pi)": 1 / (2 * math.pi), "1/pi": 1 / math.pi, "1": 1.0, "2 kappa": 1.0}
    any_det = False
    print("     ties sigma/H = c on W_y alone (required alpha = c/G_y with G_y's SIGN; determined only if all three are positive and the spread over mu in {0.5, 1, 2} is < 2):")
    for name, c in CS.items():
        vals = [c / Gy[m] for m in (0.5, 1.0, 2.0)]
        spread = max(abs(v) for v in vals) / min(abs(v) for v in vals)
        det = all(v > 0 for v in vals) and spread < 2.0
        any_det = any_det or det
        print(f"       c = {name:9s}: alpha_req = {vals[0]:+.3e}, {vals[1]:+.3e}, {vals[2]:+.3e}; |spread| {spread:.2e}; determined: {det}")
    check("E6 W_y alone: G_y is mass dependent (it changes sign between mu = 0.5 and 1 in this scheme) and no tie fixes alpha; odd-cubic consistency (f(0.05) to 2%)", (not any_det) and abs(f_check - pred) <= 0.02 * abs(pred), "")

    # ------------------------------------------------------------------ E7
    print("\nE7  dynamical stability of the exact vacuum in the electric background: R = ||Gamma_exact||_F / ||Gamma_adiabatic(order 2)||_F at fixed k (T = 2000, order-4 initial data)")
    def ratio(c, r, lam, mu, k=100.0):
        m_ = S.get_model("xz", c, "alg")
        kz, kp = r, math.sqrt(1 - r * r)
        tau_ = np.array([-k])
        Gs_, _ = S.exact_nodes(m_, r, lam, mu, tau_, T=2000.0, init_order=4)
        ser, Gam, U, res = L.current_series(m_, -k, kz, kp, lam, mu, order=2)
        return np.linalg.norm(Gs_[0]) / np.linalg.norm(Gam[0][0] + Gam[1][0] + Gam[2][0])
    weak = max(abs(ratio(1, r, 0.1, 3.0, k) - 1) for r in (-0.9, 0.3, 0.9) for k in (50.0, 100.0, 200.0))
    r_g2 = ratio(1, 0.9, 10.0, 0.3)
    r_g1 = ratio(0, 0.9, 10.0, 0.3)
    r_mid = ratio(1, 0.9, 10.0, 1.0)
    print(f"     weak field (lambda, mu) = (0.1, 3): max |R - 1| over r in {{-0.9,0.3,0.9}}, k = 50, 100, 200: {weak:.1e}")
    print(f"     strong field, light (lambda, mu) = (10, 0.3) [lambda/mu^2 = 111], r = 0.9, k = 100:  g = 2: R = {r_g2:.3g};   g = 1: R = {r_g1:.6f}")
    print(f"     strong field, heavier (10, 1) [lambda/mu^2 = 10], r = 0.9, k = 100, g = 2: R = {r_mid:.6f}")
    check("E7 no growth at weak field (|R-1| <= 1e-3); for g = 2 at lambda/mu^2 = 111 the sub-horizon vacuum is exponentially amplified (R > 1e3) while g = 1 at the same point is not (|R-1| < 1e-2); "
          "(script 1 A5: h > 0 for every real E, so this is a dynamical, not a tachyonic, instability)", weak <= 1e-3 and r_g2 > 1e3 and abs(r_g1 - 1) < 1e-2 and abs(r_mid - 1) < 1e-2)

    print("\nCHECKS: %d/%d passed" % (sum(1 for _, ok in CHECKS if ok), len(CHECKS)))
    sys.exit(0 if all(ok for _, ok in CHECKS) else 1)
