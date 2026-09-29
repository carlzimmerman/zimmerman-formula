#!/usr/bin/env python3
"""AH2 -- induced current of a charged scalar in dS_2, computed by a DIRECT mode sum, compared to the published closed form.

Pre-registered in AH2_PREREGISTRATION.md (written before this script was run).  Units hbar = c = H = 1, tau = -1 (so a = 1).
Variables: lambda = eE/H^2, mu = m/H, rho = sqrt(mu^2 + lambda^2 - 1/4)  (imaginary rho = i*sigma for light fields).

Mode (k>0):  chi_k = e^{+pi lambda/2} (2k)^{-1/2}  W_{-i lambda, i rho}(2 i k tau)        (Bunch-Davies, |chi| -> (2k)^{-1/2})
Mode (k<0):  the same with lambda -> -lambda and |k|.
Current:     J/e = (1/pi) [ Int dk p |chi_k|^2 - Delta ],  p = k + lambda/tau,  Delta = lambda/tau
             (the k integral symmetric in k; Delta = exactly integrated heavy-field WKB subtraction, Frob et al eq. 5.12).
Closed form: J/(eH) = (1/pi) rho sinh(2 pi lambda)/sinh(2 pi rho)     (Frob et al arXiv:1401.4137 eq. 5.14, rho = i sigma).

Run:   python3 ah2_induced_current_ds2.py            (real run)
       python3 ah2_induced_current_ds2.py --mutate   (control: drop the subtraction Delta; must FAIL V1)
"""
import sys
import math
import numpy as np
import mpmath as mp

mp.mp.dps = 25
MUTATE = "--mutate" in sys.argv
PI = math.pi
KAPPA = 0.5
CHECKS = []
TAU = -1.0


def check(tag, ok, detail):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


# ------------------------------------------------------------------ closed form (comparator)
def ln_sinh(x):
    return x + math.log1p(-math.exp(-2 * x)) - math.log(2.0)


def closed_form(lam, mu):
    """J/(eH) = (1/pi) rho sinh(2 pi lam)/sinh(2 pi rho); rho imaginary -> sigma sinh(2 pi lam)/sin(2 pi sigma)."""
    v = mu * mu + lam * lam - 0.25
    if abs(v) < 1e-14:
        return lam / PI                                   # exact linear response at mu^2 = 1/4 (rho = lam)
    if v > 0:
        rho = math.sqrt(v)
        return (rho / PI) * math.sinh(2 * PI * lam) / math.sinh(2 * PI * rho)
    sg = math.sqrt(-v)
    return (sg / PI) * math.sinh(2 * PI * lam) / math.sin(2 * PI * sg)


def g_of_mu(mu):
    """Linear conductivity: sigma H / e^2 = lim_{lam->0} J/(e H lam) = 2 rho/sinh(2 pi rho); sigma-branch 2 sg/sin(2 pi sg)."""
    v = mu * mu - 0.25
    if abs(v) < 1e-14:
        return 1.0 / PI
    if v > 0:
        rho = math.sqrt(v)
        return 2 * rho / math.sinh(2 * PI * rho)
    sg = math.sqrt(-v)
    return 2 * sg / math.sin(2 * PI * sg)


def ln_g_heavy(mu):
    """ln g for mu > 1/2, overflow-safe: ln(2 rho) - ln sinh(2 pi rho)."""
    rho = math.sqrt(mu * mu - 0.25)
    return math.log(2 * rho) - ln_sinh(2 * PI * rho)


# ------------------------------------------------------------------ direct mode sum
def chi2(lam_eff, mu, k, lam_true):
    """|chi_k|^2 for one branch. lam_eff = +lam (k>0) or -lam (k<0); k = |k| > 0."""
    rho2 = mp.mpf(mu) ** 2 + mp.mpf(lam_true) ** 2 - mp.mpf(1) / 4
    m_w = 1j * mp.sqrt(rho2)                              # imaginary index for real rho, real index for light fields
    z = 2j * k * TAU
    w = mp.whitw(-1j * lam_eff, m_w, z)
    return float(abs(w) ** 2 * mp.e ** (PI * lam_eff) / (2 * k))


def paired_integrand(k, lam, mu):
    """f(k) = p_+ |chi_+|^2 + p_- |chi_-|^2 for the pair (+k, -k), tau = -1."""
    p_plus = k + lam / TAU
    p_minus = -k + lam / TAU
    return p_plus * chi2(lam, mu, k, lam) + p_minus * chi2(-lam, mu, k, lam)


def direct_current(lam, mu, K=640.0, n_seg=80, n_gl=24, subtract=True, k0=1e-40):
    """J/(e H) by direct mode sum with a log-spaced Gauss-Legendre rule on (k0, K] and a fitted large-k tail.
    k0 = 1e-40: light fields have |chi|^2 ~ k^{-2 sigma}, so a cutoff at 1e-9 truncates a visible tail (first-run failure, Amendment 1)."""
    edges = np.exp(np.linspace(math.log(k0), math.log(K), n_seg + 1))
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    total = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        for x, w in zip(xg, wg):
            k = 0.5 * (b - a) * x + 0.5 * (b + a)
            total += 0.5 * (b - a) * w * paired_integrand(k, lam, mu)
    # tail: f(k) k^2 = c2 + c3/k + c4/k^2, fitted on three large-k points
    ks = np.array([0.5 * K, 0.75 * K, 1.0 * K])
    fs = np.array([paired_integrand(k, lam, mu) * k * k for k in ks])
    A = np.array([[1.0, 1.0 / k, 1.0 / (k * k)] for k in ks])
    c2, c3, c4 = np.linalg.solve(A, fs)
    tail = c2 / K + c3 / (2 * K * K) + c4 / (3 * K ** 3)
    integral = total + tail
    delta = lam / TAU
    return (1.0 / PI) * (integral - (delta if subtract else 0.0)), (c2, c3, c4, tail)


print("=" * 100)
print("AH2 induced current in dS_2 -- mode: " + ("MUTATE CONTROL (subtraction dropped)" if MUTATE else "REAL RUN"))
print("=" * 100)

# ------------------------------------------------------------------ 1. direct vs closed form
print("\n1. DIRECT mode sum vs the published closed form  (J/(eH); sign is a convention, found from the data)")
GRID = [(0.30, 0.90), (0.60, 0.60), (1.00, 0.30), (1.50, 1.00), (2.00, 1.50),   # rho real
        (0.10, 0.30), (0.20, 0.40),                                                # rho imaginary (light fields)
        (0.35, 2.00), (0.50, 0.50)]
print("     lambda    mu     rho^2      direct J/(eH)    closed form      ratio    tail(c2)")
ratios = []
worst = 0.0
for lam, mu in GRID:
    jd, (c2, c3, c4, tail) = direct_current(lam, mu, subtract=not MUTATE)
    jc = closed_form(lam, mu)
    r = jd / jc
    ratios.append(r)
    v = mu * mu + lam * lam - 0.25
    print(f"     {lam:5.2f}  {mu:5.2f}  {v:8.4f}   {jd:+.8f}     {jc:+.8f}    {r:+.5f}   {c2:+.3e}")
sign = 1.0 if np.median(ratios) > 0 else -1.0
worst = max(abs(abs(r) - 1.0) for r in ratios)
same_sign = all((r > 0) == (ratios[0] > 0) for r in ratios)
v1_ok = worst <= 2e-3 and same_sign
check("V1 direct current equals the closed form on the whole grid, one consistent sign", v1_ok,
      f"(worst |ratio| - 1 = {worst:.1e}; sign of direct/closed = {'+' if sign > 0 else '-'})")

if MUTATE:
    print("\nMUTATE CONTROL: the heavy-field subtraction Delta = lambda/tau was dropped.")
    print(f"  V1 {'FAILED as required -- the control works' if not v1_ok else 'DID NOT FAIL -- the check has no power'}")
    sys.exit(0 if not v1_ok else 1)

# ------------------------------------------------------------------ 2. linear response at mu^2 = 1/4
print("\n2. EXACT LINEAR RESPONSE at mu^2 = 1/4:  J = e^2 E/(pi H)  <=>  J/(eH) = lambda/pi")
worst2 = 0.0
for lam in (0.15, 0.4, 0.8, 1.6):
    jd, _ = direct_current(lam, 0.5)
    d = abs(abs(jd) - lam / PI) / (lam / PI)
    worst2 = max(worst2, d)
    print(f"     lambda = {lam:4.2f}:  |direct| = {abs(jd):.8f}   lambda/pi = {lam / PI:.8f}   rel diff {d:.1e}")
check("V2 exactly linear at mu^2 = 1/4 for four field strengths", worst2 <= 2e-3, f"(worst {worst2:.1e})")

# ------------------------------------------------------------------ 3. oddness in lambda
jp, _ = direct_current(0.6, 0.7)
jm, _ = direct_current(-0.6, 0.7)
check("V3 J is odd in lambda (direct computation at +0.6 and -0.6)", abs(jp + jm) / abs(jp) <= 2e-3,
      f"(J(+) = {jp:+.8f}, J(-) = {jm:+.8f})")

# ------------------------------------------------------------------ 4. heavy fields
print("\n4. HEAVY FIELDS: exponentially small current")
jc3 = closed_form(0.3, 3.0)
print("     convergence of the mu = 3, lambda = 0.3 point with the UV cutoff K (tail-fit error falls ~ K^-4):")
for KK, ns in ((160.0, 60), (320.0, 70), (640.0, 80), (1280.0, 90)):
    jk, _ = direct_current(0.3, 3.0, K=KK, n_seg=ns)
    print(f"       K = {KK:6.0f}:  |J| = {abs(jk):.6e}   closed = {abs(jc3):.6e}   rel diff {abs(abs(jk) / abs(jc3) - 1):.2e}")
jd3, _ = direct_current(0.3, 3.0, K=1280.0, n_seg=90)
print(f"     mu = 3, lambda = 0.3:  |direct| = {abs(jd3):.6e}   closed form = {abs(jc3):.6e}   ratio {abs(jd3) / abs(jc3):.5f}")
ok4a = abs(abs(jd3) / abs(jc3) - 1) <= 2e-3
print("     small-lambda slope J/(eH lambda) over the published heavy-field form 4 mu e^{-2 pi mu}:")
for mu in (5.0, 10.0, 20.0, 40.0):
    lam = 1e-4
    slope = closed_form(lam, mu) / lam
    ref = 4 * mu * math.exp(-2 * PI * mu)
    print(f"       mu = {mu:5.1f}:  ratio = {slope / ref:.5f}")
mu40 = 40.0
ok4b = abs(closed_form(1e-4, mu40) / 1e-4 / (4 * mu40 * math.exp(-2 * PI * mu40)) - 1) <= 0.03
check("V4 the exponentially small heavy-field current is resolved by the direct sum (mu = 3) and tends to 4 mu e^{-2 pi mu}",
      ok4a and ok4b, "")

# ------------------------------------------------------------------ 5. linear conductivity and the ties
print("\n5. LINEAR CONDUCTIVITY  sigma H / e^2 = g(mu) = 2 rho / sinh(2 pi rho):")
print("     mu       g(mu)")
for mu in (0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0):
    print(f"     {mu:5.2f}   {g_of_mu(mu):.6e}")
print(f"     limits: g(1/2) = 1/pi = {1 / PI:.6f};  mu -> 0: g -> 1/(2 pi mu^2), e.g. mu = 0.05: {1 / (2 * PI * 0.05 ** 2):.4f} vs {g_of_mu(0.05):.4f}")

MASSES = (0.3, 0.5, 1.0, 2.0, 5.0)
CS = {"kappa": KAPPA, "kappa/pi": KAPPA / PI, "1/(2 pi)": 1 / (2 * PI), "1/pi": 1 / PI, "1": 1.0, "2 kappa": 2 * KAPPA}
print("\n   Tie sigma/H = c: required e^2/H^2 = c / g(mu)")
print("     c            " + "".join(f"mu={m:<9.1f}" for m in MASSES) + "  spread (max/min)")
any_det = False
for name, c in CS.items():
    vals = [c / g_of_mu(m) for m in MASSES]
    spread = max(vals) / min(vals)
    any_det = any_det or spread < 2.0
    print(f"     {name:11s}  " + "".join(f"{v:<12.4e}" for v in vals) + f"  {spread:.2e}")
check("V5 no tie on the conductivity fixes e^2/H^2 independently of the mass (declared: spread < 2 would count)", not any_det, "")

H0_INV_S = 67.4 * 1e3 / 3.0856775814913673e22             # H0 in 1/s
HBAR_EV_S = 6.582119569e-16
H0_EV = H0_INV_S * HBAR_EV_S
MU_E = 0.51099895e6 / H0_EV
print(f"\n   Electron-mass reading (2D-toy statement): mu_e = m_e/H0 = {MU_E:.3e}")
print(f"     ln g(mu_e) = ln(4 mu) - 2 pi mu = {math.log(4 * MU_E) - 2 * PI * MU_E:.3e}")
print(f"     so any tie sigma/H = c needs ln(e^2/H^2) = ln c + {-(math.log(4 * MU_E) - 2 * PI * MU_E):.3e}  (e^2/H^2 ~ e^(2 pi m/H)): unreachable")
check("V6 heavy charged field: ln g = ln(4 mu) - 2 pi mu up to O(1/mu) (checked at mu = 5, 10, 20)",
      all(abs(ln_g_heavy(m) - (math.log(4 * m) - 2 * PI * m)) < 0.25 for m in (5.0, 10.0, 20.0)), "")

# ------------------------------------------------------------------ verdict
print("\n" + "=" * 100)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("VERDICT (against the declared criteria):")
print("  * The dS_2 induced current is computed directly and matches the published closed form (V1-V4).")
print("  * The current does carry e^2: sigma H = e^2/H^2 * g(mu).  But g depends steeply on the mass, so a tie on the conductivity")
print("    fixes only the combination (e^2/H^2) g(mu), one equation for two unknowns.  No tie fixes the coupling (V5).")
print("  * For a heavy charged field the response is Boltzmann-suppressed, g ~ 4 mu e^{-2 pi mu}; at the electron mass over H0")
print("    the required coupling is exponentially large in 10^39.  No O(1) horizon-conductivity tie can hold for a known charged particle (V6).")
print("  * This is a 2D toy: e has mass dimension there, so e^2/H^2 is not the 4D alpha.  dS_4, fermions, and charge renormalization untested.")
print("  * kappa = 1/2 stays FITTED.  The SM-mass wall is unchanged.")
sys.exit(0 if passed == len(CHECKS) else 1)
