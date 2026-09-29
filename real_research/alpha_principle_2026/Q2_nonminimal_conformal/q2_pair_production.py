#!/usr/bin/env python3
"""Q2/q2 -- per-mode pair-production factor of a charged scalar with xi R phi^2 in planar dS_4, and its dS_2-like closed form.

Pre-registered in Q2_PREREGISTRATION.md (before this script was run).  Units H = 1, k = 1 (the factor is k-independent).
  lam = eE/H^2, mu = m/H, r = cos(theta) = k_z/k
  rho = sqrt(lam^2 + mu^2 + 12 xi - 9/4)      (mu_w = i rho; derived in q1)
  mode  q = e^{i kappa pi/2} (2k)^{-1/2} W_{kappa, i rho}(2 i k tau), kappa = -i lam r
  claim  |beta/alpha|^2 = exp(-2 pi rho) cosh(pi(lam r + rho)) / cosh(pi(lam r - rho))
where beta/alpha is read off the tau -> 0 behaviour chi ~ A (-tau)^{1/2 + i rho} + B (-tau)^{1/2 - i rho}  (B/A = beta/alpha).
This is a PER-MODE factor (comoving), independent of k by the dilatation symmetry; it is not a physical density.

Checks
  P1  closed form = small-|tau| extraction from the Whittaker mode, 12 points (1e-5)
  P2  closed form = independent ODE integration from tau = -2000 with second-order WKB data, 4 points (1e-3)
  P3  r = +-1 reproduces the dS_2 (AH1) formula at the same (lam, mu), 6 points (1e-12)
  P4  lam = 0: N = 1/(exp(2 pi rho) - 1), 3 points (1e-5)
  P5  rho -> 0+: N -> 1/(2 pi rho (1 - tanh(pi lam r))), three cases (1e-3)
  P6  large lam: ratio(r = 1) -> 1/2; oblique Gaussian -ln ratio -> pi lam theta^2 (flat-space Schwinger exp(-pi k_perp^2/eE), recalled)
  P7  e enters only through lam (5 values of alpha, 1e-13)

Run:    python3 q2_pair_production.py            (real run; exit 0 iff every check passes)
        python3 q2_pair_production.py --mutate   (control: sign of lam*r flipped in the cosh ratio; P1 must FAIL;
                                                 exit 1 = "control fails as required", exit 3 = control did NOT fail)
"""
import sys
import math
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp

MUTATE = "--mutate" in sys.argv
mp.mp.dps = 40
PI = math.pi
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def lncosh(x):
    ax = abs(x)
    return ax + math.log1p(math.exp(-2.0 * ax)) - math.log(2.0)


def rho4(lam, mu, xi):
    v = lam * lam + mu * mu + 12.0 * xi - 2.25
    if v <= 0:
        raise ValueError("rho imaginary (mu_w real): no oscillatory out mode")
    return math.sqrt(v)


def ln_ratio(lam, r, rho):
    s = -1.0 if MUTATE else 1.0
    L = s * lam * r
    return -2.0 * PI * rho + lncosh(PI * (L + rho)) - lncosh(PI * (L - rho))


def ratio_closed(lam, r, rho):
    return math.exp(ln_ratio(lam, r, rho))


def ratio_closed_true(lam, r, rho):          # unmutated, for controls' comparators
    return math.exp(-2.0 * PI * rho + lncosh(PI * (lam * r + rho)) - lncosh(PI * (lam * r - rho)))


def ratio_numeric_whittaker(lam, r, rho, k=1):
    kap = -1j * mp.mpf(lam) * mp.mpf(r)
    rh = mp.mpf(rho)
    t1 = mp.mpf(-1) * mp.mpf(10) ** (-15)      # Amendment 2: 1e-9 was too coarse for tiny ratios
    best = None
    for q in (2, 3, 5):
        t2 = t1 * q
        M = mp.matrix([[(-t1) ** (0.5 + 1j * rh), (-t1) ** (0.5 - 1j * rh)],
                       [(-t2) ** (0.5 + 1j * rh), (-t2) ** (0.5 - 1j * rh)]])
        d = abs(mp.det(M))
        if best is None or d > best[0]:
            best = (d, t2, M)
    _, t2, M = best
    rhs = mp.matrix([mp.whitw(kap, 1j * rh, 2j * k * t1), mp.whitw(kap, 1j * rh, 2j * k * t2)])
    A, B = mp.lu_solve(M, rhs)
    return float(abs(B) ** 2 / abs(A) ** 2)


def ratio_numeric_ode(lam, r, mu, xi, rho, t0=-2000.0, t1=-2e-5):
    """Integrate y'' = -[(kr + lam/t)^2 + k^2(1-r^2) + (mu^2 + 12 xi - 2)/t^2] y from tau = t0 with 2nd-order WKB (positive frequency)
    initial data, then project onto (-t)^{1/2 +- i rho} at two small |tau|."""
    def om2(t):
        return (r + lam / t) ** 2 + (1 - r * r) + (mu * mu + 12 * xi - 2) / t ** 2

    def rhs(t, y):
        w2 = om2(t)
        return [y[1], -w2 * y[0], y[3], -w2 * y[2]]
    # WKB: W ~ sqrt(om2) with the leading 2nd-order correction; y = (2W)^{-1/2} exp(-i int W)
    h = 1e-3 * abs(t0)
    Wf = lambda t: math.sqrt(om2(t))
    W0 = Wf(t0)
    dW = (Wf(t0 + h) - Wf(t0 - h)) / (2 * h)
    ddW = (Wf(t0 + h) - 2 * W0 + Wf(t0 - h)) / (h * h)
    W2 = math.sqrt(om2(t0) + 0.75 * (dW / W0) ** 2 - 0.5 * ddW / W0)
    y0 = (2 * W2) ** -0.5
    dy0_over_y0 = -1j * W2 - dW / (2 * W0)
    yc = y0 + 0j
    dyc = dy0_over_y0 * yc
    sol = solve_ivp(rhs, (t0, t1), [yc.real, dyc.real, yc.imag, dyc.imag], method="DOP853", rtol=1e-12, atol=1e-16, dense_output=True)
    ta, tb = t1, 2 * t1
    ya = complex(*(sol.sol(ta)[[0, 2]]))
    yb = complex(*(sol.sol(tb)[[0, 2]]))
    M = np.array([[(-ta) ** (0.5 + 1j * rho), (-ta) ** (0.5 - 1j * rho)],
                  [(-tb) ** (0.5 + 1j * rho), (-tb) ** (0.5 - 1j * rho)]])
    A, B = np.linalg.solve(M, np.array([ya, yb]))
    return abs(B) ** 2 / abs(A) ** 2


print("=" * 100)
print("Q2/q2 pair-production factor, dS_4 charged scalar with xi R phi^2 -- " + ("MUTATE CONTROL (sign of lam r flipped)" if MUTATE else "REAL RUN"))
print("=" * 100, flush=True)

# ---------------------------------------------------------------- P1
GRID1 = [(1.3, -1.0, 0.0, 1 / 6), (1.3, -0.5, 0.0, 1 / 6), (1.3, 0.0, 0.0, 1 / 6), (1.3, 0.5, 0.0, 1 / 6), (1.3, 1.0, 0.0, 1 / 6),
         (0.9, 0.7, 0.0, 1 / 6), (2.5, -0.4, 0.0, 1 / 6), (0.6, 0.3, 0.8, 1 / 6),
         (2.0, 0.5, 0.3, 0.0), (2.5, 1.0, 0.0, 0.0), (1.8, -0.5, 0.0, 0.0), (0.5, 0.6, 1.0, 0.3)]
print("\nP1. closed form vs small-|tau| extraction from the Whittaker mode  (xi = 1/6 rows are the conformal scalar)")
print("     lambda     r      mu    xi     rho       numeric          closed form      rel diff")
worst1 = 0.0
for lam, r, mu, xi in GRID1:
    rho = rho4(lam, mu, xi)
    rn = ratio_numeric_whittaker(lam, r, rho)
    rc = ratio_closed(lam, r, rho)
    d = abs(rn - rc) / rn
    worst1 = max(worst1, d)
    print(f"     {lam:5.2f}  {r:+5.2f}  {mu:4.2f}  {xi:5.3f}  {rho:6.3f}   {rn:.10e}   {rc:.10e}   {d:.1e}", flush=True)
p1_ok = worst1 < 1e-5
check("P1 closed form = numerically extracted |B/A|^2 on 12 points", p1_ok, f"(worst {worst1:.1e})")

if MUTATE:
    print("\nMUTATE CONTROL: the sign of lam*r was flipped inside the cosh ratio.")
    if not p1_ok:
        print("  P1 FAILED as required -- CONTROL FAILS AS REQUIRED")
        sys.exit(1)
    print("  P1 did NOT fail -- CONTROL DID NOT FAIL (the check has no power)")
    sys.exit(3)

# ---------------------------------------------------------------- P2
print("\nP2. independent ODE integration from tau = -2000 (second-order WKB initial data) vs closed form")
GRID2 = [(1.3, 0.5, 0.0, 1 / 6), (2.0, 0.5, 0.3, 0.0), (0.6, 0.3, 0.8, 1 / 6), (0.5, 0.6, 1.0, 0.3)]
worst2 = 0.0
print("     lambda     r      mu    xi     ODE r            closed r         rel diff")
for lam, r, mu, xi in GRID2:
    rho = rho4(lam, mu, xi)
    ro = ratio_numeric_ode(lam, r, mu, xi, rho)
    rc = ratio_closed_true(lam, r, rho)
    d = abs(ro - rc) / rc
    worst2 = max(worst2, d)
    print(f"     {lam:5.2f}  {r:+5.2f}  {mu:4.2f}  {xi:5.3f}   {ro:.8e}   {rc:.8e}   {d:.1e}", flush=True)
check("P2 ODE from the far past reproduces the closed form (Bunch-Davies identification and connection formula independent of the Whittaker asymptotics)",
      worst2 < 1e-3, f"(worst {worst2:.1e}; threshold 1e-3)")

# ---------------------------------------------------------------- P3
print("\nP3. r = +-1 is the dS_2 problem: the conformal scalar in dS_4 (xi = 1/6, mass mu) vs the AH1 dS_2 formula at the same (lam, mu)")


def ratio_ds2(lam, mu):                       # AH1 docstring: exp(-2 pi rho) cosh(pi(lam+rho))/cosh(pi(lam-rho)), rho = sqrt(mu^2 + lam^2 - 1/4)
    rho = math.sqrt(mu * mu + lam * lam - 0.25)
    return math.exp(-2 * PI * rho + lncosh(PI * (lam + rho)) - lncosh(PI * (lam - rho)))


worst3 = 0.0
print("     mu     lambda    ratio(dS4 conf, r=+1)    ratio(dS2, +lam)     ratio(dS4 conf, r=-1)   ratio(dS2, -lam)")
for mu, lam in [(0.0, 1.3), (0.0, 0.8), (0.5, 1.0), (0.9, 0.4), (1.2, 2.0), (2.0, 0.3)]:
    rho = rho4(lam, mu, 1 / 6)
    rp, rm = ratio_closed_true(lam, 1.0, rho), ratio_closed_true(lam, -1.0, rho)
    ap, am = ratio_ds2(lam, mu), ratio_ds2(-lam, mu)
    worst3 = max(worst3, abs(rp / ap - 1), abs(rm / am - 1))
    print(f"     {mu:3.1f}   {lam:5.2f}    {rp:.12e}      {ap:.12e}     {rm:.12e}     {am:.12e}")
check("P3 the dS_4 conformal per-mode factor at r = +-1 equals the dS_2 minimal-scalar factor (same rho)", worst3 < 1e-12, f"(worst {worst3:.1e})")

# ---------------------------------------------------------------- P4
print("\nP4. lambda = 0: N = 1/(exp(2 pi rho) - 1) (thermal, T = H/2pi) from the numerically extracted ratio")
worst4 = 0.0
for mu, xi in [(1.5, 1 / 6), (2.0, 0.0), (0.9, 0.3)]:
    rho = rho4(0.0, mu, xi)
    rn = ratio_numeric_whittaker(0.0, 0.3, rho)
    Nn = rn / (1 - rn)
    Nb = 1.0 / math.expm1(2 * PI * rho)
    worst4 = max(worst4, abs(Nn / Nb - 1))
    print(f"     mu = {mu}, xi = {xi:.3f}: rho = {rho:.4f}  N numeric = {Nn:.8e}  Bose-Einstein = {Nb:.8e}")
check("P4 lambda = 0 gives the Gibbons-Hawking Bose-Einstein factor", worst4 < 1e-5, f"(worst {worst4:.1e})")

# ---------------------------------------------------------------- P5
print("\nP5. the threshold rho -> 0+:  N rho -> 1/(2 pi (1 - tanh(pi lam r)))")
worst5 = 0.0
cases = [("D=4 conformal massless, lam_c = 1/2", 0.5, 0.5, lambda l: 0.25 + l * l, None),
         ("D=4 minimal massless,   lam_c = 3/2", 0.5, 1.5, lambda l: 2.25 + l * l, None)]
for name, r_, lc, _, _ in cases:
    rho = 1e-4
    lam = math.sqrt(lc * lc + rho * rho)
    rat = ratio_closed_true(lam, r_, rho)
    N = rat / (1 - rat)
    pred = 1.0 / (2 * PI * (1 - math.tanh(PI * lam * r_)))
    worst5 = max(worst5, abs(N * rho / pred - 1))
    print(f"     {name}:  N*rho = {N * rho:.8f}  predicted {pred:.8f}")
rho = 1e-4
lam = math.sqrt(0.25 + rho * rho)                     # dS_2 minimal massless (AH1 form), r = 1
rat = math.exp(-2 * PI * rho + lncosh(PI * (lam + rho)) - lncosh(PI * (lam - rho)))
N = rat / (1 - rat)
pred = 1.0 / (2 * PI * (1 - math.tanh(PI * lam)))
worst5 = max(worst5, abs(N * rho / pred - 1))
print(f"     D=2 minimal massless,   lam_c = 1/2 (r = 1):  N*rho = {N * rho:.8f}  predicted {pred:.8f}")
check("P5 pair number diverges as 1/rho at the threshold in all three cases (a threshold of the out-particle notion)", worst5 < 1e-3, f"(worst {worst5:.1e})")
print("     For lambda < lambda_c (mu_w real) rho is imaginary: the out modes are real powers (-tau)^{1/2 +- mu_w}, no oscillation, no particle number.")

# ---------------------------------------------------------------- P6
print("\nP6. large lambda")
lamL = 200.0
rho = rho4(lamL, 0.0, 1 / 6)
rr = ratio_closed_true(lamL, 1.0, rho)
ok6a = abs(rr / 0.5 - 1) < 5e-3
print(f"     conformal massless, lam = 200, r = +1: ratio = {rr:.6f}  (-> 1/2, i.e. N -> 1 per mode along the field)")
th = 0.1
lamL2 = 2000.0                                    # Amendment 2: regime pi(rho - lam r) >> 1 (lambda = 200, theta = 0.05 was not)
rho2 = rho4(lamL2, 0.0, 1 / 6)
lnr = -(-2 * PI * rho2 + lncosh(PI * (lamL2 * math.cos(th) + rho2)) - lncosh(PI * (lamL2 * math.cos(th) - rho2)))
gauss = PI * lamL2 * th * th
ok6b = abs(lnr / gauss - 1) < 0.02
print(f"     oblique (lam = {lamL2:.0f}, theta = {th}; pi(rho - lam r) = {PI * (rho2 - lamL2 * math.cos(th)):.2f}): -ln ratio = {lnr:.6f} vs pi lam theta^2 = {gauss:.6f}  (flat-space Schwinger Gaussian exp(-pi k_perp^2/eE) at k = eE/H, k_perp = k sin(theta))")
check("P6 large-lambda limits: ratio(r=1) -> 1/2 and the flat-space transverse Gaussian", ok6a and ok6b)

# ---------------------------------------------------------------- P7
print("\nP7. the per-mode factor depends on e only through lambda = eE/H^2")
lam_s, mu_s_, xi_s, r_s = 1.3, 0.0, 1 / 6, 0.4
ref = ratio_closed_true(lam_s, r_s, rho4(lam_s, mu_s_, xi_s))
dev = 0.0
print("     alpha           1/alpha     e          E/H^2 needed      ratio")
for a in (1 / 137.035999177, 1 / 100.0, 1 / 50.0, 0.5, 1e-4):
    e = math.sqrt(4 * PI * a)
    eps = lam_s / e
    lam_phys = e * eps                              # lambda rebuilt from the physical inputs
    val = ratio_closed_true(lam_phys, r_s, rho4(lam_phys, mu_s_, xi_s))
    dev = max(dev, abs(val - ref) / ref)
    print(f"     {a:.6e}   {1 / a:9.3f}   {e:.5f}   {eps:14.6e}   {val:.12e}")
check("P7 the same lambda (hence the same per-mode factor) is reached at every alpha by rescaling E/H^2", dev < 1e-13, f"(max rel diff {dev:.1e})")
print("     => alpha = lambda^2/(4 pi eps^2), eps = E/H^2: the factor fixes lambda, not alpha (structural, as in AH1 C5).")

# ---------------------------------------------------------------- unscored table
print("\nReference table (unscored): conformal massless scalar, per-mode N(lambda, r) = ratio/(1 - ratio) and its angular average <N> = (1/2) Int dr N")
print("     lambda    rho      N(r=-1)      N(r=0)       N(r=+1)      <N>")
for lam in (0.55, 0.75, 1.0, 2.0, 5.0):
    rho = rho4(lam, 0.0, 1 / 6)
    Ns = lambda rr_: (lambda x: x / (1 - x))(ratio_closed_true(lam, rr_, rho))
    avg = 0.5 * float(mp.quad(lambda rr_: Ns(float(rr_)), [-1, 0, 1]))
    print(f"     {lam:5.2f}   {rho:6.3f}   {Ns(-1.0):.5e}   {Ns(0.0):.5e}   {Ns(1.0):.5e}   {avg:.5e}")

print("\n" + "=" * 100)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("VERDICT: for the charged scalar in dS_4 the per-mode Bogoliubov factor is exp(-2 pi rho) cosh(pi(lam r + rho))/cosh(pi(lam r - rho)),")
print("  rho^2 = lam^2 + mu^2 + 12 xi - 9/4.  At xi = 1/6, m = 0: rho^2 = lam^2 - 1/4 and the r = +-1 modes are exactly the dS_2 problem;")
print("  off-axis r shifts lam -> lam r inside the cosh ratio only.  It depends on e only through lam (alpha free).  The pair number is")
print("  singular as 1/rho at lam = lam_c (a threshold of the particle notion, not of the physics).  Scalar only; no claim about alpha.")
sys.exit(0 if passed == len(CHECKS) else 1)
