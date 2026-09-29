#!/usr/bin/env python3
"""N5-2 -- induced current of a charged Dirac fermion in dS_2 by a DIRECT mode sum, compared with the published closed form; conductivity g_f(mu);
comparison with the scalar g(mu); tie scan.

Pre-registered in N5_PREREGISTRATION.md (with its amendments; written before this script was run).  Units hbar = c = H = 1, tau = -1 (a = 1).
Variables: lambda = eE/H^2, mu = m/H, rho_f = sqrt(mu^2 + lambda^2)  (rho_s = sqrt(mu^2 + lambda^2 - 1/4) for the scalar, AH2).

Modes (validated in n5_1_dirac_modes_and_pairs.py against the far-past ODE, including k<0):
    k>0 positive-frequency mode  Psi = sqrt(a) (W_{kappa-1/2, i rho_f}(z), (i/mu) W_{kappa+1/2, i rho_f}(z)),  z = 2 i k tau,  kappa = -i lambda,
    f(k,lambda) = (|Psi_1|^2 - |Psi_2|^2)/(|Psi_1|^2 + |Psi_2|^2)  (unit norm is conserved, so normalisation is imposed by the ratio),
    k<0 modes: f(-k,lambda) = -f(k,-lambda).
Current:  J/(eH) = -(1/2 pi) [ I_raw - Delta ],  I_raw = Int_0^inf [f(k,lambda) - f(k,-lambda)] dk  (pair (+k,-k) added before integrating),
          Delta = Int dk (-p/omega) = 2 lambda exactly (the zeroth-order adiabatic / heavy-field subtraction, Stahl-Strobel-Xue eq.(95)),
          i.e. J/(eH) = (2 lambda - I_raw)/(2 pi).  Quadrature: log-spaced Gauss-Legendre on (1e-40, K], fitted tail c2/k^2 + c3/k^3 + c4/k^4.
Closed form (comparator, Stahl-Strobel-Xue eq.(96)):  J/(eH) = (1/pi) rho_f sinh(2 pi lambda)/sinh(2 pi rho_f).

Run:     python3 n5_2_induced_current.py            (real run; exit 0 iff every check passes)
         python3 n5_2_induced_current.py --mutate   (control: the subtraction Delta is dropped; V1 must FAIL; the control exits 1 when V1 fails as required)
"""
import sys
import math
import numpy as np
import mpmath as mp
from multiprocessing import Pool
from scipy.integrate import solve_ivp

mp.mp.dps = 25
MUTATE = "--mutate" in sys.argv
PI = math.pi
KAPPA = 0.5
CHECKS = []
K0 = 1e-40


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


# ------------------------------------------------------------------ closed forms
def closed_form(lam, mu):
    rho = math.sqrt(mu * mu + lam * lam)
    if rho == 0.0:
        return lam / PI
    return (rho / PI) * math.sinh(2 * PI * lam) / math.sinh(2 * PI * rho)


def g_f(mu):
    """sigma H/e^2 = lim_{lambda->0} F/lambda = 2 mu/sinh(2 pi mu)."""
    if mu == 0.0:
        return 1.0 / PI
    return 2 * mu / math.sinh(2 * PI * mu)


def g_s(mu):
    """Scalar (AH2): 2 rho_s/sinh(2 pi rho_s), rho_s = sqrt(mu^2 - 1/4); sigma-branch 2 sg/sin(2 pi sg)."""
    v = mu * mu - 0.25
    if abs(v) < 1e-14:
        return 1.0 / PI
    if v > 0:
        r = math.sqrt(v)
        return 2 * r / math.sinh(2 * PI * r)
    sg = math.sqrt(-v)
    return 2 * sg / math.sin(2 * PI * sg)


def ln_g_f_heavy(mu):
    return math.log(2 * mu) - (2 * PI * mu + math.log1p(-math.exp(-4 * PI * mu)) - math.log(2.0))


# ------------------------------------------------------------------ direct mode sum
def f_mp(k, lam, mu):
    """f for the positive-frequency k>0 mode (mpf result)."""
    kappa = -1j * mp.mpf(lam)
    nu = 1j * mp.sqrt(mp.mpf(mu) ** 2 + mp.mpf(lam) ** 2)
    z = 2j * mp.mpf(k) * mp.mpf(-1)
    s1 = mp.whitw(kappa - mp.mpf(1) / 2, nu, z)
    s2 = mp.whitw(kappa + mp.mpf(1) / 2, nu, z) / mp.mpf(mu)
    A, B = abs(s1) ** 2, abs(s2) ** 2
    return (A - B) / (A + B)


def pair_integrand(k, lam, mu):
    """F(k) = f(k,lam) + f(-k,lam) = f(k,lam) - f(k,-lam)."""
    return float(f_mp(k, lam, mu) - f_mp(k, -lam, mu))


def direct_current(args):
    lam, mu, K, n_seg, n_gl, subtract = args
    edges = np.exp(np.linspace(math.log(K0), math.log(K), n_seg + 1))
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    total = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        for x, w in zip(xg, wg):
            k = 0.5 * (b - a) * x + 0.5 * (b + a)
            total += 0.5 * (b - a) * w * pair_integrand(k, lam, mu)
    ks = np.array([0.5 * K, 0.75 * K, 1.0 * K])
    fs = np.array([pair_integrand(k, lam, mu) * k * k for k in ks])
    A = np.array([[1.0, 1.0 / k, 1.0 / (k * k)] for k in ks])
    c2, c3, c4 = np.linalg.solve(A, fs)
    tail = c2 / K + c3 / (2 * K * K) + c4 / (3 * K ** 3)
    i_raw = total + tail
    delta = 2.0 * lam
    return (i_raw - (delta if subtract else 0.0)) / (-2 * PI), (c2, c3, c4, tail, i_raw)


# ------------------------------------------------------------------ massless ODE check
def ode_f_general(k, p_of_tau, tau_end=-1.0, T=4000.0, mu=0.0):
    tau0 = -T / abs(k)

    def rhs(t, y):
        p = p_of_tau(t)
        M = mu * (-1.0 / t)
        return [1j * p * y[0] - 1j * M * y[1], -1j * (M * y[0] + p * y[1])]
    p0 = p_of_tau(tau0)
    M0 = mu * (-1.0 / tau0)
    om = math.hypot(p0, M0)
    u = np.array([M0, om + p0], dtype=complex) if p0 >= 0 else np.array([om - p0, M0], dtype=complex)
    u /= np.linalg.norm(u)
    sol = solve_ivp(rhs, (tau0, tau_end), u, method="DOP853", rtol=1e-12, atol=1e-14)
    y = sol.y[:, -1]
    return abs(y[0]) ** 2, abs(y[1]) ** 2


if __name__ == "__main__":
    print("=" * 110)
    print("N5-2 induced current of a Dirac fermion in dS_2 -- mode: " + ("MUTATE CONTROL (subtraction dropped)" if MUTATE else "REAL RUN"))
    print("=" * 110)
    pool = Pool(processes=8)

    # ---------------------------------------------------------------- 1. grid
    GRID = [(0.30, 0.90), (0.60, 0.60), (1.00, 0.30), (1.50, 1.00), (2.00, 1.50), (0.10, 0.30), (0.20, 0.10), (0.35, 2.00), (0.50, 0.50), (0.40, 0.05)]
    jobs = [(lam, mu, 640.0, 80, 24, not MUTATE) for lam, mu in GRID]
    res = pool.map(direct_current, jobs)
    print("\n1. DIRECT mode sum vs the closed form  J/(eH) = (1/pi) rho_f sinh(2 pi lambda)/sinh(2 pi rho_f)")
    print("     lambda    mu     rho_f     direct J/(eH)     closed form       ratio      tail(c2)")
    ratios = []
    for (lam, mu), (jd, (c2, c3, c4, tail, iraw)) in zip(GRID, res):
        jc = closed_form(lam, mu)
        ratios.append(jd / jc)
        print(f"     {lam:5.2f}  {mu:5.2f}  {math.hypot(lam, mu):7.4f}   {jd:+.9f}    {jc:+.9f}    {jd / jc:+.6f}   {c2:+.2e}")
    worst = max(abs(abs(r) - 1.0) for r in ratios)
    same_sign = all((r > 0) == (ratios[0] > 0) for r in ratios)
    sign = "+" if np.median(ratios) > 0 else "-"
    v1_ok = worst <= 2e-3 and same_sign
    check("V1 direct current equals the closed form on the whole grid, one consistent sign", v1_ok,
          f"(worst |ratio| - 1 = {worst:.1e}; sign of direct/closed = {sign}; + means the paper's orientation convention, in which J and E have the same sign, i.e. sigma > 0)")

    if MUTATE:
        print("\nMUTATE CONTROL: the subtraction Delta = 2 lambda was dropped.")
        print(f"  V1 {'FAILED as required -- the control works' if not v1_ok else 'DID NOT FAIL -- the check has no power'}")
        sys.exit(1 if not v1_ok else 0)

    # ---------------------------------------------------------------- 2. massless
    print("\n2. MASSLESS LIMIT: chirality decouples, no mixing, the whole current is the subtraction (anomaly)")
    worst_nomix = 0.0
    for lam in (0.15, 0.4, 0.8, 1.6):
        for k in (0.3, 1.0, 2.5):
            a1, a2 = ode_f_general(k, lambda t, lam=lam, k=k: k + lam / t)
            b1, b2 = ode_f_general(-k, lambda t, lam=lam, k=k: -k + lam / t)
            worst_nomix = max(worst_nomix, abs(a2 - 1), abs(a1), abs(b1 - 1), abs(b2))
    # non-constant field: same statement for an arbitrary A(tau), here an extra bump 0.7/(1+tau^2) that flips the sign of p for some k
    for k in (0.3, 1.0):
        pb = lambda t, k=k: k + 0.6 / t + 0.7 / (1 + t * t)
        a1, a2 = ode_f_general(k, pb)
        worst_nomix = max(worst_nomix, abs(a2 - 1), abs(a1))
    print(f"     ODE (m = 0): |Psi_2| = 1, Psi_1 = 0 for k>0 and the reverse for k<0, for constant and for time-dependent A: worst deviation {worst_nomix:.1e}")
    print("     => f(k,lambda) = -1 (k>0), +1 (k<0) for both signs of lambda:  I_raw = Int [f(k,lambda) - f(k,-lambda)] dk = 0,  J/(eH) = 2 lambda/(2 pi) = lambda/pi")
    for lam in (0.15, 0.4, 0.8, 1.6):
        print(f"       lambda = {lam:4.2f}:  J/(eH) = {(2 * lam - 0.0) / (2 * PI):.10f}   lambda/pi = {lam / PI:.10f}   closed form (mu -> 0) = {closed_form(lam, 0.0):.10f}")
    check("V2 massless: no mixing verified by ODE (<= 1e-10), so I_raw = 0 and J/(eH) = lambda/pi exactly linear (matches the closed form at mu = 0)",
          worst_nomix <= 1e-10 and all(abs((2 * l) / (2 * PI) - closed_form(l, 0.0)) < 1e-14 for l in (0.15, 0.4, 0.8, 1.6)), f"(worst no-mixing deviation {worst_nomix:.1e})")

    # ---------------------------------------------------------------- 3. oddness
    jobs3 = [(0.6, 0.7, 640.0, 80, 24, True), (-0.6, 0.7, 640.0, 80, 24, True)]
    (jp, _), (jm, _) = pool.map(direct_current, jobs3)
    check("V3 J is odd in lambda (direct computation at +0.6 and -0.6, mu = 0.7)", abs(jp + jm) / abs(jp) <= 2e-3, f"(J(+) = {jp:+.8f}, J(-) = {jm:+.8f})")

    # ---------------------------------------------------------------- 4. heavy
    print("\n4. HEAVY FIELDS: exponentially small current (mu = 3, lambda = 0.3): convergence with the UV cutoff K")
    jc3 = closed_form(0.3, 3.0)
    conv = [(160.0, 60), (320.0, 70), (640.0, 80), (1280.0, 90)]
    resh = pool.map(direct_current, [(0.3, 3.0, KK, ns, 24, True) for KK, ns in conv])
    for (KK, ns), (jk, _) in zip(conv, resh):
        print(f"       K = {KK:6.0f}:  J = {jk:.6e}   closed = {jc3:.6e}   rel diff {abs(jk / jc3 - 1):.2e}")
    jd3 = resh[-1][0]
    ok4a = abs(jd3 / jc3 - 1) <= 2e-3
    print("     small-lambda slope of the closed form over 4 mu e^{-2 pi mu}  (scalar AH2: 1.16, 1.08, 1.04, 1.02 at these mu):")
    ok4b = True
    for mu in (5.0, 10.0, 20.0, 40.0):
        slope = closed_form(1e-4, mu) / 1e-4
        ratio = slope / (4 * mu * math.exp(-2 * PI * mu))
        print(f"       mu = {mu:5.1f}:  ratio = {ratio:.6f}")
        ok4b = ok4b and abs(ratio - 1) <= 0.03
    check("V4 the exponentially small heavy-field current is resolved by the direct sum (mu = 3) and the slope -> 4 mu e^{-2 pi mu}", ok4a and ok4b,
          f"(mu = 3 ratio {jd3 / jc3:.5f}; the fermion slope is 1/(1 - e^{{-4 pi mu}}) times 4 mu e^{{-2 pi mu}}, no 1/mu correction)")

    # ---------------------------------------------------------------- 5. conductivity
    print("\n5. LINEAR CONDUCTIVITY  sigma H/e^2 = g_f(mu) = 2 mu/sinh(2 pi mu)   (scalar: g_s = 2 rho_s/sinh(2 pi rho_s), rho_s = sqrt(mu^2 - 1/4))")
    print("     mu       g_f(mu)        g_s(mu)        g_f/g_s      exp(-pi/(4 mu))")
    ok5a = True
    for mu in (0.0, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0):
        gf = g_f(mu)
        if mu == 0.0:
            print(f"     {mu:5.2f}   {gf:.6e}   (scalar: diverges as 1/(2 pi mu^2))")
            continue
        gs = g_s(mu)
        ok5a = ok5a and gf < gs
        print(f"     {mu:5.2f}   {gf:.6e}   {gs:.6e}   {gf / gs:.5f}      {math.exp(-PI / (4 * mu)):.5f}")
    ok5b = True
    print("     large-mu ratio g_f/g_s against exp(-pi/(4 mu)):")
    for mu in (5.0, 10.0, 20.0):
        r = g_f(mu) / g_s(mu)
        print(f"       mu = {mu:5.1f}:  g_f/g_s = {r:.6f}   exp(-pi/(4 mu)) = {math.exp(-PI / (4 * mu)):.6f}   rel diff {abs(r / math.exp(-PI / (4 * mu)) - 1):.1e}")
        ok5b = ok5b and abs(r / math.exp(-PI / (4 * mu)) - 1) <= 0.05
    print("     small-mu expansion  pi g_f = 1 - (2 pi^2/3) mu^2 + (14 pi^4/45) mu^4 + O(mu^6)  (Amendments 2 and 3):")
    ok5c = True
    for mu in (0.01, 0.05):
        lhs = PI * g_f(mu)
        rhs = 1 - (2 * PI ** 2 / 3) * mu ** 2 + (14 * PI ** 4 / 45) * mu ** 4
        dev = abs((1 - lhs) - (1 - rhs)) / (1 - lhs)
        print(f"       mu = {mu:5.2f}:  pi g_f = {lhs:.8f}   three-term series = {rhs:.8f}   rel diff of the deviation from 1: {dev:.1e}")
        ok5c = ok5c and dev <= 1e-3
    # mass at which the plateau is halved (information only)
    mh = mp.findroot(lambda m: 2 * m / mp.sinh(2 * mp.pi * m) - 0.5 / mp.pi, 0.3)
    print(f"     g_f falls to half its massless value 1/pi at mu = {float(mh):.4f}   (information)")
    check("V5 g_f < g_s at every tabulated mu >= 0.05; g_f/g_s -> exp(-pi/(4 mu)) (5%); g_f = 1/pi at mu = 0 with the three-term small-mu series of Amendments 2-3", ok5a and ok5b and ok5c)

    # ---------------------------------------------------------------- 6. ties
    MASSES = (0.3, 0.5, 1.0, 2.0, 5.0)
    CS = {"kappa": KAPPA, "kappa/pi": KAPPA / PI, "1/(2 pi)": 1 / (2 * PI), "1/pi": 1 / PI, "1": 1.0, "2 kappa": 2 * KAPPA}
    print("\n6. TIES  sigma/H = c:  required e^2/H^2 = c/g_f(mu)   (kappa = 1/2 is FITTED)")
    print("     c            " + "".join(f"mu={m:<10.1f}" for m in MASSES) + " spread(max/min)   massless: e^2/H^2 = pi c")
    any_det = False
    for name, c in CS.items():
        vals = [c / g_f(m) for m in MASSES]
        spread = max(vals) / min(vals)
        any_det = any_det or spread < 2.0
        print(f"     {name:11s}  " + "".join(f"{v:<13.4e}" for v in vals) + f" {spread:.2e}        {PI * c:.5f}")
    check("V6 no tie on the conductivity fixes e^2/H^2 independently of the mass (declared: spread < 2 would count)", not any_det,
          "(the massless value e^2/H^2 = pi c exists only for m = 0 exactly and c supplied from outside)")
    H0_EV = 67.4e3 / 3.0856775814913673e22 * 6.582119569e-16
    mu_e = 0.51099895e6 / H0_EV
    lg = ln_g_f_heavy(mu_e)
    print(f"\n   Electron-mass reading (2D-toy statement): mu_e = m_e/H0 = {mu_e:.3e};  ln g_f(mu_e) = ln(2 mu) - ln sinh(2 pi mu) = {lg:.3e}")
    print(f"     (any tie sigma/H = c would need ln(e^2/H^2) = ln c + {-lg:.3e}: unreachable, as for the scalar)")
    check("V6b heavy fermion: ln g_f = ln(4 mu) - 2 pi mu up to exponentially small terms (mu = 5, 10, 20)",
          all(abs(ln_g_f_heavy(m) - (math.log(4 * m) - 2 * PI * m)) < 1e-9 for m in (5.0, 10.0, 20.0)))

    pool.close()
    print("\n" + "=" * 110)
    passed = sum(1 for _, ok in CHECKS if ok)
    print(f"CHECKS: {passed}/{len(CHECKS)} passed")
    print("VERDICT (against the declared criteria):")
    print("  * The dS_2 fermion induced current is computed by a direct mode sum and matches the published closed form (V1-V4).")
    print("  * It carries e^2: sigma H = (e^2/H^2) g_f(mu), g_f = 2 mu/sinh(2 pi mu), mass dependent; only lambda = eE/H^2 enters the nonlinear function.")
    print("  * Massless limit: J = e^2 E/(pi H) exactly for all lambda (the anomaly); g_f(0) = 1/pi = the coefficient of the Schwinger-model photon mass e^2/pi.")
    print("  * Unlike the scalar: no 1/(2 pi mu^2) divergence at small mu; at large mu g_f/g_s -> exp(-pi/(4 mu)).")
    print("  * A tie sigma/H = c fixes e^2/H^2 = pi c only for an exactly massless fermion with c supplied from outside; for any massive fermion the required coupling")
    print("    varies over many decades (V6).  2D toy: e has mass dimension 1; dS_4 fermions and charge renormalisation are not computed here.")
    print("  * kappa = 1/2 stays FITTED.  The SM-mass wall is unchanged.")
    sys.exit(0 if passed == len(CHECKS) else 1)
