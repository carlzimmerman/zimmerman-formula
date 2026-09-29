#!/usr/bin/env python3
"""AH1 -- does the Schwinger/Unruh pair-production factor in de Sitter space fix alpha?

Pre-registered in AH1_PREREGISTRATION.md (written before this script was run).  Scope: dS_2, minimally
coupled charged scalar, planar patch, k > 0 branch, pair-production (Bogoliubov) factor only.

Units hbar = c = 1, Heaviside-Lorentz: alpha = e^2 / (4 pi).
  lambda = e E / H^2   (field strength in horizon units)
  mu     = m / H       (mass in horizon units)
  rho    = sqrt(mu^2 + lambda^2 - 1/4)

Mode equation (conformal time tau < 0, momentum k):  chi'' + [(k + lambda/tau)^2 + mu^2/tau^2] chi = 0
Solution that is positive-frequency at tau -> -inf:  chi_in = W_{-i lambda, i rho}(2 i k tau)  (Whittaker).
Connection formula gives  r = |beta/alpha|^2 = exp(-2 pi rho) cosh(pi(lambda+rho)) / cosh(pi(lambda-rho)),
and the pair number N = r / (1 - r).  The k < 0 branch is the same with lambda -> -lambda.

Run:   python3 ah1_schwinger_ds2.py            (real run)
       python3 ah1_schwinger_ds2.py --mutate   (control: sign of lambda flipped in the cosh ratio; must FAIL C1)
"""
import sys
import math
import mpmath as mp

mp.mp.dps = 40
MUTATE = "--mutate" in sys.argv
PI = math.pi
KAPPA = 0.5                                   # FITTED in the framework, not derived
ALPHA_TARGET = 1.0 / 137.035999177            # CODATA 2022
CHECKS = []


def check(tag, ok, detail):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


def rho_of(lam, mu):
    v = mu * mu + lam * lam - 0.25
    if v <= 0:
        raise ValueError("rho imaginary: mu^2 + lambda^2 <= 1/4 (no real out-frequency)")
    return math.sqrt(v)


def lncosh(x):
    ax = abs(x)
    return ax + math.log1p(math.exp(-2.0 * ax)) - math.log(2.0)


def ln_r_analytic(lam, mu):
    rh = rho_of(lam, mu)
    L = -lam if MUTATE else lam               # MUTATE control flips the sign inside the cosh ratio
    return -2.0 * PI * rh + lncosh(PI * (L + rh)) - lncosh(PI * (L - rh))


def r_analytic(lam, mu):
    return math.exp(ln_r_analytic(lam, mu))


def whittaker_in(lam, mu, k, tau):
    rh = mp.sqrt(mp.mpf(mu) ** 2 + mp.mpf(lam) ** 2 - mp.mpf(1) / 4)
    return mp.whitw(-1j * lam, 1j * rh, 2j * k * tau)


def r_numeric(lam, mu, k=1):
    """|B/A|^2 read off the small-|tau| asymptotics chi ~ A(-tau)^{1/2+i rho} + B(-tau)^{1/2-i rho}.
    (-tau)^{+i rho} = exp(-i rho H t) is the positive-frequency out mode."""
    lam = mp.mpf(lam)
    mu = mp.mpf(mu)
    rh = mp.sqrt(mu ** 2 + lam ** 2 - mp.mpf(1) / 4)
    t1 = mp.mpf(-1) * mp.mpf(10) ** (-9)
    best = None
    for q in (2, 3, 5):                       # pick the better-conditioned second sample point
        t2 = t1 * q
        M = mp.matrix([[(-t1) ** (0.5 + 1j * rh), (-t1) ** (0.5 - 1j * rh)],
                       [(-t2) ** (0.5 + 1j * rh), (-t2) ** (0.5 - 1j * rh)]])
        d = abs(mp.det(M))
        if best is None or d > best[0]:
            best = (d, t2, M)
    _, t2, M = best
    rhs = mp.matrix([whittaker_in(lam, mu, k, t1), whittaker_in(lam, mu, k, t2)])
    A, B = mp.lu_solve(M, rhs)
    return float(abs(B) ** 2 / abs(A) ** 2)


def pair_number(r):
    return r / (1.0 - r)


def rate_from_physical(e, E, m, H):
    """The pair-production factor from physical inputs: e enters only through eE."""
    return r_analytic(e * E / H ** 2, m / H)


print("=" * 100)
print("AH1 Schwinger/Unruh in de Sitter -- mode: " + ("MUTATE CONTROL (sign of lambda flipped)" if MUTATE else "REAL RUN"))
print("=" * 100)

# ------------------------------------------------------------------ 1. verification
print("\n1. VERIFY the pair-production factor (do not assume it)")
# C0: the Whittaker function solves the mode equation, and is the Bunch-Davies (positive-frequency) mode
lam0, mu0, k0 = 1.3, 0.9, 1
tau0 = mp.mpf("-0.7")
f = lambda t: whittaker_in(lam0, mu0, k0, t)
chi = f(tau0)
chi2 = mp.diff(f, tau0, 2, h=mp.mpf(10) ** (-8))     # finite-difference truncation error ~ h^2 (checked: 2.5e-8, 2.5e-12, floor)
term = ((k0 + lam0 / tau0) ** 2 + mu0 ** 2 / tau0 ** 2) * chi
res = abs(chi2 + term) / (abs(chi2) + abs(term))
check("C0a Whittaker W_{-i lam, i rho}(2 i k tau) solves the mode equation", res < mp.mpf(10) ** (-12),
      f"(relative residual {float(res):.2e})")
term_wrong = ((k0 - lam0 / tau0) ** 2 + mu0 ** 2 / tau0 ** 2) * chi        # wrong-sign potential: must NOT be solved
res_wrong = abs(chi2 + term_wrong) / (abs(chi2) + abs(term_wrong))
check("C0a' the same function does NOT solve the wrong-sign equation (the check has power)", res_wrong > 0.1,
      f"(relative residual {float(res_wrong):.2e})")
tau_far = mp.mpf(-5000)
z = 2j * k0 * tau_far
ratio = f(tau_far) / (mp.exp(-z / 2) * z ** (-1j * lam0))
check("C0b at tau -> -inf the in-mode is e^{-ik tau} (positive frequency, Bunch-Davies)",
      abs(ratio - 1) < 5e-3, f"(|ratio - 1| = {float(abs(ratio - 1)):.2e} at tau = -5000)")

# C1: analytic r equals the numerically extracted one
grid = [(0.0, 1.5), (0.4, 0.7), (0.9, 0.3), (1.3, 0.9), (2.0, 1.2), (3.0, 2.0), (1.0, 3.0), (2.5, 0.2)]
worst = 0.0
print("     lambda    mu      r_numeric        r_analytic       rel diff")
for lam, mu in grid:
    rn = r_numeric(lam, mu)
    ra = r_analytic(lam, mu)
    d = abs(rn - ra) / rn
    worst = max(worst, d)
    print(f"     {lam:5.2f}  {mu:5.2f}   {rn:.10e}   {ra:.10e}   {d:.1e}")
c1_ok = worst < 1e-5
check("C1 analytic r = numerically extracted |B/A|^2 on the whole grid", c1_ok, f"(worst rel diff {worst:.1e})")

# C2: lambda = 0 is the Gibbons-Hawking Bose-Einstein factor at T = H/2pi
mu_t = 1.5
rh_t = rho_of(0.0, mu_t)
N_num = pair_number(r_numeric(0.0, mu_t))
N_be = 1.0 / (math.exp(2 * PI * rh_t) - 1.0)
check("C2 lambda = 0 gives 1/(e^{2 pi rho} - 1), the Gibbons-Hawking thermal factor",
      abs(N_num - N_be) / N_be < 1e-5, f"(N = {N_num:.6e} vs {N_be:.6e})")

# C3: flat-space Schwinger exponent: -ln r has slope pi in x = mu^2/lambda at large lambda
lamL = 2000.0
xs = (6.0, 8.0)
lnr = [ln_r_analytic(lamL, math.sqrt(x * lamL)) for x in xs]
slope = -(lnr[1] - lnr[0]) / (xs[1] - xs[0])
check("C3 large-lambda limit: d(-ln r)/d(mu^2/lambda) = pi (flat-space Schwinger exp(-pi m^2/eE))",
      abs(slope - PI) / PI < 0.02, f"(slope {slope:.5f} vs pi = {PI:.5f})")

# C4: r < 1; the k < 0 branch (lambda -> -lambda) is suppressed
ok4 = True
for lam, mu in grid:
    if lam > 0:
        # branch comparison uses the unmutated analytic form
        rp = math.exp(-2 * PI * rho_of(lam, mu) + lncosh(PI * (lam + rho_of(lam, mu))) - lncosh(PI * (lam - rho_of(lam, mu))))
        rm = math.exp(-2 * PI * rho_of(lam, mu) + lncosh(PI * (-lam + rho_of(lam, mu))) - lncosh(PI * (-lam - rho_of(lam, mu))))
        ok4 = ok4 and (rp < 1.0) and (rm < rp)
check("C4 r < 1 on the grid, and the k < 0 branch is suppressed relative to k > 0", ok4, "")

if MUTATE:
    print("\nMUTATE CONTROL: sign of lambda flipped inside the cosh ratio.")
    print(f"  C1 {'FAILED as required -- the control works' if not c1_ok else 'DID NOT FAIL -- the check has no power'}")
    sys.exit(0 if not c1_ok else 1)

# ------------------------------------------------------------------ 2. structural fact
print("\n2. STRUCTURAL: the rate sees e only through lambda = eE/H^2")
lam_s, mu_s = 1.3, 0.9
ref = r_analytic(lam_s, mu_s)
dev = 0.0
print("     alpha           alpha^-1    e          E/H^2 needed      r")
for a in (ALPHA_TARGET, 1 / 100.0, 1 / 50.0, 0.5, 1e-4):
    e = math.sqrt(4 * PI * a)
    eps = lam_s / e
    r = rate_from_physical(e, eps, mu_s, 1.0)      # H = 1 units
    dev = max(dev, abs(r - ref) / ref)
    print(f"     {a:.6e}   {1 / a:9.3f}   {e:.5f}   {eps:14.6e}   {r:.12e}")
check("C5 the same lambda (hence the same rate) is reached at every alpha by rescaling E/H^2", dev < 1e-13,
      f"(max rel diff {dev:.1e})")
print("     => alpha = lambda^2 / (4 pi eps^2), eps = E/H^2.  The rate fixes lambda, not alpha.")

# ------------------------------------------------------------------ 3. the ties
print("\n3. THE TIES: what alpha is consistent with each, once the only free directions are swept")
eps_grid = [10 ** (x / 4.0) for x in range(-12, 13)]         # 1e-3 .. 1e3
mu_grid = [10 ** (x / 4.0) for x in range(0, 13)]            # 1 .. 1e3
ties = {}


def alpha_span(pairs):
    vals = [lam * lam / (4 * PI * eps * eps) for lam, eps in pairs]
    return min(vals), max(vals)


ties["T1 lambda = kappa*mu   (eE/m = a0)"] = alpha_span([(KAPPA * mu, eps) for mu in mu_grid for eps in eps_grid])
ties["T2 lambda = kappa      (eE = kappa H^2)"] = alpha_span([(KAPPA, eps) for eps in eps_grid])
ties["T3 lambda = 1/2 at mu=0 (massless onset)"] = alpha_span([(0.5, eps) for eps in eps_grid])
print("     tie                                       alpha_min        alpha_max        span (x)")
spans_ok = True
for name, (lo, hi) in ties.items():
    span = hi / lo
    spans_ok = spans_ok and span >= 2.0
    print(f"     {name:42s} {lo:.3e}      {hi:.3e}      {span:.2e}")
check("C6 every tie leaves alpha spanning far more than a factor of 2 (none determines alpha)", spans_ok,
      "(declared criterion: a tie determines alpha only if the span is < 2)")

# ------------------------------------------------------------------ 4. what would be missing
print("\n4. THE MISSING INPUT: the field strength eps = E/H^2 each tie would need to give alpha = 1/137.036")
e_star = math.sqrt(4 * PI * ALPHA_TARGET)
eps_T2 = KAPPA / e_star
print(f"     e = sqrt(4 pi alpha) = {e_star:.6f}")
print(f"     T2 (lambda = kappa):    eps* = kappa/e = {eps_T2:.5f}")
print(f"     T3 (lambda = 1/2):      eps* = 0.5/e   = {0.5 / e_star:.5f}   (same as T2 only because kappa = 1/2 numerically)")
print(f"     T1 (lambda = kappa mu): eps* = kappa mu/e = {KAPPA / e_star:.5f} * mu")
check("C7 the required eps reproduces alpha exactly (self-consistency of the inversion)",
      abs((KAPPA / eps_T2) ** 2 / (4 * PI) - ALPHA_TARGET) / ALPHA_TARGET < 1e-12, "")

print("\n   Natural handles on eps declared in advance, applied to T2 (alpha = kappa^2/(4 pi eps^2)):")
handles = [("1", 1.0), ("kappa", KAPPA), ("1/(2 pi)", 1 / (2 * PI)), ("1/(4 pi)", 1 / (4 * PI)),
           ("sqrt(8 pi/3)", math.sqrt(8 * PI / 3))]
any_hit = False
print("     eps               alpha        alpha^-1     miss (rel)    hit (<1e-3)?")
for name, ev in handles:
    a = KAPPA ** 2 / (4 * PI * ev * ev)
    miss = abs(a - ALPHA_TARGET) / ALPHA_TARGET
    hit = miss < 1e-3
    any_hit = any_hit or hit
    print(f"     {name:14s}  {a:11.5e}  {1 / a:10.3f}   {miss:10.3e}     {'YES' if hit else 'no'}")
check("C8 no pre-declared natural handle hits alpha to 1e-3 (declared expectation)", not any_hit, "")

# ------------------------------------------------------------------ verdict
print("\n" + "=" * 100)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("VERDICT (against the declared criteria):")
print("  * The factor is verified: analytic = numerical (C1), thermal limit (C2), flat-space Schwinger limit (C3).")
print("  * alpha does NOT fix itself from the pair-production factor.  The factor depends on e only through")
print("    lambda = eE/H^2 (C5); alpha needs E/H^2 as a separate input, and none of T1-T3 supplies it (C6).")
print("  * Tying the horizon field to kappa (T2) would need E/H^2 = %.4f to give 1/137.036; the natural handles" % eps_T2)
print("    declared in advance all miss (C8).  The number %.4f is a TARGET the missing input would have to hit," % eps_T2)
print("    not something derived here.")
print("  * Not tested: the induced current / vacuum polarization, dS_4, fermions, running of alpha.")
print("  * kappa = 1/2 stays FITTED.  The SM-mass wall is unchanged.")
sys.exit(0 if passed == len(CHECKS) else 1)
