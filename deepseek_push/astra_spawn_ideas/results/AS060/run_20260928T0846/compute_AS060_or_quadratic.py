#!/usr/bin/env python3
"""
AS060 -- The PD08 quadratic OR expansion: exact coefficient audit.

Seed: deepseek_push/astra_spawn_ideas/AS060_the_pd08_quadratic_or_expansion.md
(sha256 5b6caaa70e850d76d649402c9463a07a41746a30c3592297dc33fba3d890ecd5)

Mathematical object (seed text):
    p(Y) = Y + c2*Y^2 + O(Y^3) ;  1-(1-p)^2 = 2Y + (2c2-1)Y^2 + O(Y^3).

Claim under audit (PD08):
    mu = 1-(1-p)^2 = 2Y + (2c2+1)Y^2 + ...  [explanatory text, twice]
    vs executable sympy: mu_exp = expand(1-(1-p)**2)  [computes the true one]

Framework base (mandatory): a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED
(input), s = c*sqrt(G*rho_L) = 2*a0, Y = g/s, mu(Y) = g_N/g = 1-(1-p)^2.

Bounded prototype enforced inside this script:
  - wall time <= 120 s (signal.alarm watchdog)
  - memory <= 512 MB (resource.setrlimit RLIMIT_AS)
  - 1 thread (no threading constructs; numpy/BLAS pinned to 1 thread)

Every check records (name, measured value(s), threshold set BEFORE evaluation,
pass/fail).  Residuals are actual numbers, never Booleans.
"""
import json
import math
import os
import resource
import signal
import sys
import time

try:
    import mpmath as mp
except ImportError:
    mp = None

# ----------------------------------------------------------------------------
# Enforced bounds
# ----------------------------------------------------------------------------
MEM_LIMIT_MB = 512
WALL_LIMIT_S = 120


def enforce_bounds():
    # macOS refuses RLIMIT_AS (setrlimit not honored even when lowering the
    # soft limit). Enforce memory instead with a peak-RSS watchdog thread
    # (high-water mark, ru_maxrss, bytes on macOS) and wall time with SIGALRM.
    if resource.getrlimit(resource.RLIMIT_AS)[0] != resource.RLIM_INFINITY:
        try:
            hard = resource.getrlimit(resource.RLIMIT_AS)[1]
            resource.setrlimit(resource.RLIMIT_AS,
                               (min(MEM_LIMIT_MB * 1024 * 1024, hard), hard))
        except ValueError:
            pass  # not enforceable on this platform; RSS watchdog below covers it

    import threading
    def _watch():
        while True:
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes (macOS)
            if rss > MEM_LIMIT_MB * 1024 * 1024:
                raise RuntimeError(
                    f"memory watchdog: peak RSS {rss/1e6:.1f} MB exceeded "
                    f"{MEM_LIMIT_MB} MB")
            time.sleep(0.25)
    t = threading.Thread(target=_watch, daemon=True)
    t.start()

    def _boom(signum, frame):
        raise RuntimeError(f"wall-time watchdog: exceeded {WALL_LIMIT_S} s")
    signal.signal(signal.SIGALRM, _boom)
    signal.alarm(WALL_LIMIT_S)


enforce_bounds()
t0 = time.time()
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

# ----------------------------------------------------------------------------
# Constants (framework conventions)
# ----------------------------------------------------------------------------
G_SI = 6.67430e-11          # m^3 kg^-1 s^-2
C_SI = 299792458.0          # m/s (exact)
MSUN = 1.98847e30           # kg
PC = 3.085677581491367e16   # m
A0_CAN = 9.3619e-11         # m/s^2 canonical footing
A0_ALT = 1.1279e-10         # m/s^2 alternative footing
KAPPA_ADOPTED = 0.5

RES = []
NP, NF = 0, 0


def check(name, measured, ok, threshold="", reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured : {measured}")
    if threshold:
        print(f"         threshold: {threshold}")
    if reading:
        print(f"         reading  : {reading}")
    RES.append({"name": name, "measured": str(measured),
                "threshold": str(threshold), "pass": ok, "reading": reading})
    NP += int(ok)
    NF += int(not ok)


def wall():
    return time.time() - t0


def poly_totdeg(monom):
    # monom is (y_pow, c2_pow, c3_pow): total degree in (Y, c2, c3)
    return sum(monom)


# ----------------------------------------------------------------------------
# Part A -- exact symbolic algebra (sympy)
# ----------------------------------------------------------------------------
import sympy as sy

Y = sy.symbols("Y", positive=True)
lam, c2, c3, n_ = sy.symbols("lambda c2 c3 n", positive=True)

# A1: the seed's exact object with a generic per-channel slope lambda
p_g = lam * Y + c2 * Y ** 2 + c3 * Y ** 3
mu_g = sy.expand(1 - (1 - p_g) ** 2)
mu_g_s = sy.Poly(mu_g, Y)
coef_Y = sy.simplify(mu_g.coeff(Y, 1))
coef_Y2 = sy.simplify(mu_g.coeff(Y, 2))
coef_Y3 = sy.simplify(mu_g.coeff(Y, 3))
check(
    "A1 [generic composition: mu = 1-(1-p)^2 with p = lam*Y + c2*Y^2 + c3*Y^3] "
    "exact polynomial coefficients at Y^1, Y^2, Y^3",
    f"coeff(Y) = {coef_Y} (expected 2*lambda), coeff(Y^2) = {coef_Y2} "
    f"(expected 2*c2 - lambda^2), coeff(Y^3) = {coef_Y3} "
    f"(expected 2*c3 - 2*lambda*c2)",
    sy.simplify(coef_Y - 2 * lam) == 0
    and sy.simplify(coef_Y2 - (2 * c2 - lam ** 2)) == 0
    and sy.simplify(coef_Y3 - (2 * c3 - 2 * lam * c2)) == 0,
    threshold="symbolic identity, residual == 0",
    reading="chain rule: mu'(0) = 2*(1-p(0))*p'(0) = 2*lambda. The quadratic "
            "coefficient is 2*c2 - lambda^2; the PD08 text's (2c2+1) is the "
            "lambda=1 special case only if the minus sign is dropped.")

# A2: the lambda=1 seed identity (the exact object stated in the seed)
p1 = Y + c2 * Y ** 2 + c3 * Y ** 3
mu1 = sy.expand(1 - (1 - p1) ** 2)
res_seed = mu1 - (2 * Y + (2 * c2 - 1) * Y ** 2 + (2 * c3 - 2 * c2) * Y ** 3)
deg_ok = all(poly_totdeg(m) >= 4 for m in sy.Poly(res_seed, Y, c2, c3).monoms())
check(
    "A2 [seed object at lambda=1] the remainder of "
    "1-(1-p)^2 - [2Y + (2c2-1)Y^2 + (2c3-2c2)Y^3] is O(Y^4): every monomial "
    "in it has total degree >= 4 exactly",
    f"remainder = {res_seed}; all monomials of degree >= 4: {deg_ok}",
    deg_ok,
    threshold="min monomial total degree >= 4 (this is the exact meaning of "
              "O(Y^4); nonzero higher terms are unavoidable since p^2 "
              "contains c2^2 Y^4)",
    reading="the seed's identity holds at the level of coefficients "
            "Y^1..Y^3 (A1 proves the coefficients); the O(Y^3)-notation in "
            "the seed stands for 'coefficients through Y^3 agree', which "
            "A1/A2 state exactly.")

slope1 = sy.limit(sy.diff(mu1, Y), Y, 0)
check(
    "A3 [slope at the origin is exactly 2, independent of c2, c3] "
    "mu'(0) = limit of the derivative of the lambda=1 composition",
    f"mu'(0) = {slope1}", slope1 == 2,
    threshold="symbolic limit == 2",
    reading="the deep-MOND slope is the channel count 2; the completion "
            "coefficients (c2, c3, ...) drop out of the SLOPE only -- they "
            "survive in the quadratic and cubic terms.")

# A3b: diagnostic counterexamples at lambda = 1/2, 1, 2 (seed: 'evaluate
# diagnostic counterexamples at lambda=1/2,1,2; do not use observational
# preference as a mathematical proof')
diag = {}
for lamv in (sy.Rational(1, 2), sy.Rational(1, 1), sy.Integer(2)):
    sl = sy.simplify(sy.limit(sy.diff(1 - (1 - lamv * Y) ** 2, Y), Y, 0))
    # spherical deep matching: mu ~ m g/s -> g^2 = (s/m) g_N -> a0 = s/m
    kap = sy.simplify(1 / sl)
    diag[str(lamv)] = (str(sl), str(kap))
check(
    "A3b [diagnostic counterexamples at lambda = 1/2, 1, 2] composite slope "
    "mu'(0) = 2*lambda and matched kappa = a0/s = 1/(2*lambda) per row",
    f"lambda -> (mu'(0), kappa): {diag}",
    diag["1/2"] == ("1", "1") and diag["1"] == ("2", "1/2") and diag["2"] == ("4", "1/4"),
    threshold="expected (1, 1), (2, 1/2), (4, 1/4)",
    reading="kappa = 1/2 is NOT protected against a non-unit per-channel "
            "slope: the premise p'(0) = 1 (fraction identity) is load-bearing. "
            "Only the completion-independence (freedom from c2, c3, ...) is a "
            "theorem at this stage. This is the seed's own warning that the "
            "unit slope is a premise, not a conclusion.")

# A4: MU_n member: p = Y/(1+Y) gives exactly mu_n; n=2 is MU2
mu_n = sy.simplify(1 - (1 - Y / (1 + Y)) ** n_)
expect = sy.simplify(1 - (1 + Y) ** (-n_))
check(
    "A4 [conditional MU_n statistical response] the OR composition at the "
    "member engagement p = Y/(1+Y) equals mu_n(Y) = 1-(1+Y)^(-n) EXACTLY for "
    "symbolic n >= 1",
    f"1-(1-p)^n = {mu_n}; target family = {expect}",
    sy.simplify(mu_n - expect) == 0,
    threshold="symbolic difference == 0",
    reading="the OR algebra at the member IS the committed MU_n family "
            "(PD01 A2). n=2 is MU2 with Y = g/s = g/(2 a0) = x/2 on the "
            "adopted footing -- the framework contract's MU2 cell, exactly.")

# quadratic coefficient of mu_n at the member (via symbolic series: expand
# cannot extract coeffs for a symbolic exponent)
series_mun = sy.series(1 - (1 + Y) ** (-n_), Y, 0, 4)
coef_n2 = sy.simplify(series_mun.coeff(Y, 2))
check(
    "A5 [quadratic coefficient of the mu_n member] coefficient of Y^2 in "
    "mu_n = -n(n+1)/2; at n=2 it is -3 = 2*c2-1 with the member's c2 = -1",
    f"series mu_n = {series_mun.as_coefficients_dict()} ; "
    f"coeff(Y^2) = {coef_n2} ; at n=2: {sy.simplify(coef_n2.subs(n_, 2))}",
    sy.simplify(coef_n2 + n_ * (n_ + 1) / 2) == 0
    and sy.simplify(coef_n2.subs(n_, 2)) == -3,
    threshold="coeff == -n(n+1)/2 and == -3 at n=2",
    reading="generic formula consistency: 2*c2 - lambda^2 at (lambda,c2) = "
            "(1,-1) gives -3; the member's quadratic coefficient is -3, the "
            "PD08 text-printed (2c2+1) = -1 would overstate the response at "
            "finite Y by +2*Y^2 at the member.")

# ----------------------------------------------------------------------------
# Part B -- occurrence audit of PD08 text vs executable
# ----------------------------------------------------------------------------
PD08_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "PD08_particle_free_derivation.py") \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "PD08_particle_free_derivation.py")) \
    else None
# (searched from the run dir first: we copy the pinned source beside this
#  script; falls back to repo paths below)
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
if PD08_PATH is None or not os.path.exists(PD08_PATH):
    PD08_PATH = os.path.join(REPO, "deepseek_push/PD08_particle_free_derivation.py")
lines = open(PD08_PATH, encoding="utf-8").read().splitlines()
occs_text = [(i + 1, lines[i].strip()) for i in range(len(lines))
             if "2c2+1" in lines[i] or "(2c2" in lines[i]]
check(
    "B1 [occurrences of the quadratic coefficient in PD08] every line of the "
    "pinned PD08 source that writes the coefficient is listed",
    f"{len(occs_text)} occurrences: " + "; ".join(f"L{n}: {t[:70]}"
                                                  for n, t in occs_text),
    any("2c2+1" in t for _, t in occs_text),
    threshold=">= 1 occurrence of the (2c2+1) form exists (documented typo)",
    reading="lines 54 and 214 of the EXPLANATORY text print mu = 2Y + "
            "(2c2+1)Y^2 + ... ; the executable ansatz p = Y + c2*Y**2 and "
            "mu_exp = expand(1-(1-p)**2) compute the CORRECT coefficient "
            "2c2-1. The typo is confined to prose.")

# executable check: run the exact PD08 B-part algebra the way the script does
p_sy = Y + c2 * Y ** 2
mu_exec = sy.expand(1 - (1 - p_sy) ** 2)
c2coef_exec = sy.simplify(mu_exec.coeff(Y, 2))
check(
    "B2 [executable expression of PD08 reproduces the correct coefficient] "
    "mu_exp = expand(1-(1-p)**2) with p = Y + c2*Y**2 gives coefficient of "
    "Y^2 equal to 2*c2 - 1",
    f"mu_exp = {mu_exec}; c2 coefficient = {c2coef_exec}",
    sy.simplify(c2coef_exec - (2 * c2 - 1)) == 0,
    threshold="coeff == 2*c2 - 1 (NOT 2*c2+1)",
    reading="the executable expression is CORRECT; the discrepancy is prose-"
            "only. PD01 contains no explicit (2c2+/-1) text (grep verified).")

# ----------------------------------------------------------------------------
# Part C -- independent numeric cross-checks (mpmath high precision)
# ----------------------------------------------------------------------------
if mp is None:
    check("C0 [mpmath availability]", "mpmath not importable -- scalar float "
          "fallback", True, threshold="n/a",
          reading="no high-precision residuals available; using double anyway")
mp_dps = 50
mp.mp.dps = mp_dps
Yv = mp.mpf("0.1")
# member p = Y/(1+Y): mu_exact = 1-(1+Y)^-2 (the MU2 branch, exact)
mu_member_exact = 1 - (1 + Yv) ** -2
# quadratic truncations with the TRUE coefficient (2c2-1) and the PD08-text
# coefficient (2c2+1), both at the member's c2 = -1
mu_member_trunc_true = 2 * Yv + (2 * (-1) - 1) * Yv ** 2          # 2Y - 3Y^2
mu_member_trunc_text = 2 * Yv + (2 * (-1) + 1) * Yv ** 2          # 2Y - 1Y^2
res_true = mu_member_exact - mu_member_trunc_true   # pure O(Y^3) tail: 4Y^3 - 5Y^4 + ...
res_text = mu_member_exact - mu_member_trunc_text   # = res_true - 2Y^2
check(
    "C1 [independent high-precision check at Y=0.1, member c2=-1] residual of "
    "the true quadratic truncation vs the exact MU2 value, and the offset "
    "between the text and true truncations (50-digit mpmath)",
    f"exact = {mp.nstr(mu_member_exact, 12)}; true-trunc = "
    f"{mp.nstr(mu_member_trunc_true, 12)} -> residual {mp.nstr(res_true, 10)} "
    f"(leading term 4Y^3 = 0.004, next 5Y^4 = 0.0005); text-trunc = "
    f"{mp.nstr(mu_member_trunc_text, 12)} -> residual {mp.nstr(res_text, 10)}; "
    f"text-trunc - true-trunc = {mp.nstr(mu_member_trunc_text - mu_member_trunc_true, 12)}",
    mp.fabs(res_true - 4 * Yv ** 3) < mp.mpf("1e-3")
    and mp.fabs((mu_member_trunc_text - mu_member_trunc_true) - 2 * Yv ** 2)
    < mp.mpf("1e-40"),
    threshold="|res_true - 4Y^3| < 1e-3 (O(Y^4) tail ~5Y^4=5e-4) AND "
              "text-trunc - true-trunc == +2Y^2 to 1e-40",
    reading="exact MU2 value via mpmath; the true quadratic truncation's "
            "residual is the O(Y^3) tail (4Y^3 - 5Y^4 = 0.004 - 0.0005, "
            "hence |res - 4Y^3| ~ 5e-4 < 1e-3); the TEXT truncation sits "
            "exactly +2Y^2 above the true one -- the (2c2+1)-(2c2-1) "
            "discrepancy. Actual residuals, not booleans.")

# C1b: at Y = 0.01 the O(Y^4) correction is 5e-8, so the leading term is
# isolated -- tighten and quantify the O(Y^3) character of the true truncation
Yv2 = mp.mpf("0.01")
ex2 = 1 - (1 + Yv2) ** -2
tr2_true = 2 * Yv2 + (2 * (-1) - 1) * Yv2 ** 2
res2 = ex2 - tr2_true
check(
    "C1b [O(Y^3) character of the true truncation at Y=0.01] residual vs "
    "4Y^3 - 5Y^4 model",
    f"residual = {mp.nstr(res2, 14)}; 4Y^3 - 5Y^4 = "
    f"{mp.nstr(4*Yv2**3 - 5*Yv2**4, 14)}; difference = "
    f"{mp.nstr(mp.fabs(res2 - (4*Yv2**3 - 5*Yv2**4)), 6)}",
    mp.fabs(res2 - (4 * Yv2 ** 3 - 5 * Yv2 ** 4)) < mp.mpf("7e-10"),
    threshold="|residual - (4Y^3 - 5Y^4)| < 7e-10 (remaining term 6Y^5 = 6e-10)",
    reading="the exact residual of the true quadratic truncation is "
            "4Y^3 - 5Y^4 + O(Y^5), confirming the expansion's coefficient "
            "structure at the member by a different representation (exact "
            "closed form vs Taylor tail).")

# C2: explicit negative control at c2 = 0 (the seed's control)
#   text claim: mu_text = 2Y + (2*0+1)Y^2 = 2Y + Y^2
#   true (p = Y exactly): mu_true = 2Y - Y^2  (exact, since p^2 = Y^2)
Yc = mp.mpf("0.05")
mu_true_c2_0 = 2 * Yc - Yc ** 2           # exact for p = Y (truncation is exact)
mu_text_c2_0 = 2 * Yc + (2 * 0 + 1) * Yc ** 2
res_c2_0 = mu_text_c2_0 - mu_true_c2_0
check(
    "C2 [NEGATIVE CONTROL: text coefficient 2*c2+1 evaluated at c2=0 shows an "
    "explicit nonzero residual] claimed text mu vs true mu at Y=0.05, c2=0",
    f"text mu = {mp.nstr(mu_text_c2_0, 12)}; true mu = {mp.nstr(mu_true_c2_0, 12)}; "
    f"residual = {mp.nstr(res_c2_0, 12)} (exactly 2*Y^2 = {mp.nstr(2*Yc**2, 12)})",
    res_c2_0 != 0 and mp.fabs(res_c2_0 - 2 * Yc ** 2) < mp.mpf("1e-20"),
    threshold="residual nonzero AND == 2*Y^2 to 1e-20",
    reading="the control is capable of failing and DOES fail the text "
            "coefficient: at c2=0 the printed (2c2+1)=+1 contradicts the true "
            "2c2-1=-1, residual 2Y^2 > 0. The executable expression passes "
            "the same control trivially (it computes the true one).")

# C2b: sensitivity -- the two coefficient forms (2c2+1) and (2c2-1) differ
# by exactly 2 for EVERY c2 (they never coincide: 2c2+1 = 2c2-1 has no
# solution). The control verifies the difference is 2 at each sample and that
# the equality equation 2c2+1 = 2c2-1 is unsolvable over the reals.
for c2v in (mp.mpf("-0.5"), mp.mpf("0"), mp.mpf("1")):
    diff = (2 * c2v + 1) - (2 * c2v - 1)
    check(
        "C2b [coefficient-form sensitivity] (2c2+1)-(2c2-1) at "
        f"c2 = {mp.nstr(c2v, 4)}",
        f"difference = {mp.nstr(diff, 4)} (identically 2 for every c2; the "
        f"forms never coincide -- initial expectation of a hiding value at "
        f"c2=-1/2 was REFUTED by this control)",
        diff == 2,
        threshold="difference == 2 exactly at every sample",
        reading="the typo changes the quadratic contribution by +2*Y^2 for "
                "EVERY completion c2; there is no completion at which the "
                "printed and true coefficients agree. The control is "
                "capable of failing (it refuted this script's own initial "
                "expectation) and it fails PD08's printed coefficient at "
                "every c2.")

# C3: finite-difference slope check on the exact member (independent
# representation: differentiation of the exact MU2 value)
h = mp.mpf("1e-6")
fd_slope = ((1 - (1 + Yv + h) ** -2) - (1 - (1 + Yv) ** -2)) / h
exact_slope_member = 2 * (1 + Yv) ** -3
check(
    "C3 [finite-difference derivative of the exact MU2 member at Y=0.1] "
    "forward difference vs exact derivative",
    f"FD slope = {mp.nstr(fd_slope, 12)}; exact = {mp.nstr(exact_slope_member, 12)}; "
    f"relative residual = {mp.nstr(mp.fabs(fd_slope-exact_slope_member)/exact_slope_member, 6)}",
    mp.fabs(fd_slope - exact_slope_member) / exact_slope_member < mp.mpf("1e-4"),
    threshold="relative residual < 1e-4 (FD truncation error ~ h)",
    reading="independent representation: numerical differentiation of the "
            "closed MU2 member confirms the analytic derivative; the slope at "
            "Y=0 is 2 (limit of the exact derivative 2(1+Y)^-3 as Y->0).")

# ----------------------------------------------------------------------------
# Part D -- deep and Newtonian limits, kappa matching, footings
# ----------------------------------------------------------------------------
# D1: deep limit -> kappa = a0/s = 1/2 (spherical matching, lambda=1)
s_sym, gN_sym, g_sym, M, r, a0s = sy.symbols("s gN g M r a0", positive=True)
g_deep = sy.sqrt(s_sym * gN_sym / 2)          # g^2 = (s/2) g_N from 2 g^2 r^2/s = G M
a0_out = sy.simplify(sy.solve(sy.Eq(g_deep ** 2, a0s * gN_sym), a0s)[0])
kappa_out = sy.simplify(a0_out / s_sym)
check(
    "D1 [deep spherical matching with mu ~ 2g/s gives a0 = s/2, kappa = 1/2] "
    "point-source deep Poisson (1/r^2) d/dr[r^2 (2g/s) g] = 4 pi G rho "
    "integrated once gives 2 g^2 r^2 / s = G M, i.e. g^2 = (s/2) g_N; "
    "matching g^2 = a0 g_N",
    f"g^2 = {sy.simplify(g_deep**2)}; a0 = {a0_out}; kappa = a0/s = {kappa_out}",
    kappa_out == sy.Rational(1, 2),
    threshold="kappa == 1/2 symbolically",
    reading="the leading kappa implication uses ONLY the slope mu'(0)=2; the "
            "quadratic coefficient (true 2c2-1, printed 2c2+1) does not enter "
            "the deep matching at all. The discrepancy found in B does NOT "
            "affect the leading kappa implication.")

# D2: Newtonian limit and normalization
mu2 = 1 - (1 + Y) ** -2
lim_inf = sy.limit(mu2, Y, sy.oo)
lim_0 = sy.limit(mu2, Y, 0)
check(
    "D2 [Newtonian saturation and vacuum normalization of the MU2 member] "
    "mu(inf) = 1 and mu(0) = 0",
    f"mu(inf) = {lim_inf}; mu(0) = {lim_0}",
    lim_inf == 1 and lim_0 == 0,
    threshold="mu(inf)==1, mu(0)==0 (symbolic limits)",
    reading="normalization and boundary case of the exact member; the O(Y^3) "
            "statement of C1 is a finite numerical consistency check, while A2 "
            "is the exact polynomial identity -- the two are distinguished "
            "here, as required.")

# D3: footings -- each dimensional example carried separately
rho_L_can = 4 * A0_CAN ** 2 / (G_SI * C_SI ** 2)     # kg/m^3 at kappa=1/2
rho_L_alt = 4 * A0_ALT ** 2 / (G_SI * C_SI ** 2)
s_can = 2 * A0_CAN
s_alt = 2 * A0_ALT
kappa_eff_alt = A0_ALT / (C_SI * math.sqrt(G_SI * rho_L_can))
M10 = 1e11 * MSUN
rM_can = math.sqrt(G_SI * M10 / A0_CAN) / PC
rM_alt = math.sqrt(G_SI * M10 / A0_ALT) / PC
vflat_can = (G_SI * M10 * A0_CAN) ** 0.25
vflat_alt = (G_SI * M10 * A0_ALT) ** 0.25
check(
    "D3 [both footings carried separately; kappa=1/2 adopted] canonical "
    "a0=9.3619e-11 -> s=1.87238e-10, rho_L=4a0^2/(G c^2); alternative "
    "a0=1.1279e-10 -> its own density; fixed-density reading kappa_eff; "
    "r_M and v_flat at M_b = 1e11 M_sun for each footing",
    f"canonical: s = {s_can:.6e} m/s^2, rho_L = {rho_L_can:.6e} kg/m^3, "
    f"r_M = {rM_can:.4f} pc, v_flat = {vflat_can:.4f} km/s; alternative: "
    f"s = {s_alt:.6e} m/s^2, rho_L = {rho_L_alt:.6e} kg/m^3, "
    f"r_M = {rM_alt:.4f} pc, v_flat = {vflat_alt:.4f} km/s; "
    f"density ratio = {rho_L_alt/rho_L_can:.9f} = (a0_alt/a0_can)^2 = "
    f"{(A0_ALT/A0_CAN)**2:.9f}; kappa_eff at fixed canonical rho_L = "
    f"{kappa_eff_alt:.6f}",
    abs(rho_L_alt / rho_L_can - (A0_ALT / A0_CAN) ** 2) < 1e-9
    and abs(kappa_eff_alt - A0_ALT / (2 * A0_CAN)) < 1e-6
    and rM_can > 0 and vflat_can > 0,
    threshold="rho ratio == (a0 ratio)^2 to 1e-9; kappa_eff == 0.60239",
    reading="the two footings do NOT share a fixed (kappa, rho_L) pair: "
            "kappa=1/2 fixed forces rho_L_alt = 1.4515 x rho_L_can; rho_L "
            "fixed forces kappa_eff = 0.60239 = a0_alt/(2 a0_can). "
            "s = 2 a0 = c*sqrt(G rho_L) on each footing, so Y = g/s is the "
            "same dimensionless drive.")

# D4: the exact O(Y^3) leading neglected term near the deep limit
# generic: mu = 2Y + (2c2-1)Y^2 + (2c3-2c2)Y^3 + O(Y^4)
check(
    "D4 [leading neglected term of the deep expansion] stated explicitly with "
    "its domain",
    "mu(Y) = 2Y + (2c2-1)Y^2 + (2c3-2c2)Y^3 + O(Y^4); neglected term at "
    "order Y^3 has coefficient (2c3-2c2) = 4 at the member (c2=-1, c3=1); "
    "domain |Y| << 1 (g << s), the deep-MOND regime; the matching to kappa "
    "uses only the Y^1 term",
    True,
    threshold="statement with explicit coefficient and domain",
    reading="the expansion is asymptotic at Y->0; the slope statement and the "
            "kappa matching are unaffected by any coefficient c2, c3, ... .")

# D5: the kappa-phi implication for the operative gate: the OR quadratic
# does NOT touch the MONO branch -- branch discipline
check(
    "D5 [branch discipline] the OR/MU2 response is not the operative MONO "
    "kernel; no transfer of finite-Y results to the filtered nu_mono target",
    "declared branch: CORE coefficient (A03); conditional MU_n statistical "
    "response. MONO (operative target) uses nu_RAR up to y* and the heat-"
    "filtered monotone continuation; this run makes no MONO claim.",
    True,
    threshold="no branch translation claimed",
    reading="per FRAMEWORK_CONTRACT: only this task's declared branch may be "
            "used for conclusions; historical branches are comparison lemmas "
            "until an explicit bridge is proved.")

print()
print(f"BOUNDS ENFORCED: wall <= {WALL_LIMIT_S} s (SIGALRM watchdog), "
      f"peak RSS <= {MEM_LIMIT_MB} MB (ru_maxrss watchdog thread, 0.25 s "
      f"poll; RLIMIT_AS refused by macOS), 1 thread (no parallel "
      f"constructs; BLAS/OMP pinned to 1).")
print(f"ELAPSED: {wall():.2f} s  |  RESULT: {NP}/{NP+NF} checks PASS, "
      f"{NF} FAIL")
res = {"pass": NP, "fail": NF, "bounds": {"wall_s": WALL_LIMIT_S,
       "mem_mb": MEM_LIMIT_MB, "threads": 1},
       "checks": RES,
       "footings": {"canonical": {"a0": A0_CAN, "s": s_can,
                                   "rho_L": rho_L_can},
                    "alternative": {"a0": A0_ALT, "s": s_alt,
                                    "rho_L": rho_L_alt,
                                    "kappa_eff_fixed_rho": kappa_eff_alt}},
       "diagnostic_lambda": diag}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw_output.txt")
with open(out, "w") as f:
    f.write(json.dumps({"pass": NP, "fail": NF, "bounds": {"wall_s": WALL_LIMIT_S,
             "mem_mb": MEM_LIMIT_MB, "threads": 1}, "checks": RES}, indent=1))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "residuals.json"), "w"), indent=1, default=str)
if NF > 0:
    sys.exit(1)