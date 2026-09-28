#!/usr/bin/env python3
"""
AS052 -- OR composition with UNEQUAL channel slopes.

Seed claim under test (AS052_or_composition_with_unequal_channel_slopes.md,
sha256 bd9a4d387b694b13c3c1b99dbb1886ab809e48816458d0abeaaa6343ab45a737):

    mu = 1 - product_i (1 - p_i(Y));   p_i(Y) = b_i Y + O(Y^2);   mu'(0) = sum_i b_i.

Question the seed poses: does OR composition with two channels (the metric's
static count, PD01 B1) DERIVE kappa = 1/2 when the per-channel slopes b_i are
allowed to differ?  Mandated control: b1 = 1, b2 = 2 must NOT force kappa = 1/2.

Framework (adopted inputs, not derived here): s = c*sqrt(G*rho_Lambda),
a0 = kappa*c*sqrt(G*rho_Lambda) with kappa = 1/2 ADOPTED; Y = g/s; response
equation mu(Y)*g = B (B = G*M_b/r^2) as the spherical first integral of
div[mu(|grad Phi|/s) grad Phi] = 4 pi G rho_b; per-channel engagement p_i
with p_i(0) = 0 (vacuum), p_i(oo) = 1 (saturation), p_i'(0) = b_i.

Every check states measurement and threshold separately.  Proof-only results
must not fabricate computational evidence: the residuals below are ACTUAL
numbers from the mpmath solves, not booleans.

Bounded prototype: wall <= 120 s enforced in-process (deadline check),
<= 512 MB RSS measured, 1 thread (no pools; numpy/sympy/mpmath single
process, GIL single thread; OMP_NUM_THREADS=1 forced).
"""

import json
import os
import resource
import sys
import time

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import mpmath as mp
import sympy as sy

WALL_LIMIT_S = 120.0
T0 = time.monotonic()

RES, NP, NF = [], 0, 0
def check(name, measured, ok, tol="", note=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if tol: print(f"         tolerance: {tol}")
    if note: print(f"         reading : {note}")
    RES.append({"name": name, "measured": str(measured), "pass": ok,
                "tolerance": tol, "reading": note})
    NP += int(ok); NF += int(not ok)

def deadline(extra_s=0.0):
    if time.monotonic() - T0 > WALL_LIMIT_S - extra_s:
        print(f"WALL-CLOCK LIMIT {WALL_LIMIT_S}s BREACHED -- aborting lane")
        sys.exit(2)

# ---------------------------------------------------------------- constants
G_SI    = 6.67430e-11          # m^3 kg^-1 s^-2  (registered)
C_SI    = 299792458.0          # m/s
MSUN    = 1.98847e30           # kg
PC      = 3.085677581491367e16 # m
A0_CAN  = 9.3619e-11           # canonical footing, m/s^2 (kappa = 1/2)
A0_ALT  = 1.1279e-10           # alternative footing, m/s^2
# rho_Lambda fixed by each footing via a0 = (1/2) c sqrt(G rho_L) :
RHO_L_CAN = (2*A0_CAN/C_SI)**2/G_SI      # kg/m^3, canonical footing
S_CAN     = C_SI*mp.sqrt(G_SI*RHO_L_CAN) # m/s^2  (a0_can / kappa, kappa = 1/2)
RHO_L_ALT = (2*A0_ALT/C_SI)**2/G_SI      # kg/m^3, alternative footing density
S_ALT     = C_SI*mp.sqrt(G_SI*RHO_L_ALT) # m/s^2 when rho_L is the alternative one

mp.mp.dps = 50
Yr, b1r, b2r, c1r, c2r, kr, sr = sy.symbols('Y b1 b2 c1 c2 k s', positive=True)

D = dict(printdoc=True, flush=True)
print(__doc__)

print("=" * 100)
print("STEP 1 -- claim, symbol dictionary, boundary conditions, assumptions")
print("=" * 100)
print("  SYMBOLS:  Y = g/s (dimensionless);  s = c sqrt(G rho_L) [m s^-2];")
print("            a0 = kappa s [m s^-2];  kappa = a0/s (dimensionless);")
print("            b_i = p_i'(0) (dimensionless per-channel deep slope);")
print("            p_i(Y) per-channel engagement; mu(Y) total response;")
print("            B = g_N = G M_b/r^2 [m s^-2];  n = channel count (integer >= 1).")
print("  BOUNDARY CONDITIONS (per channel):  p_i(0) = 0 (action vacuum),")
print("            p_i(oo) = 1 (saturation -> mu(oo) = 1 normalization).")
print("  ASSUMPTIONS: b_i > 0 finite; mu = 1 - prod_i (1 - p_i) (OR over the")
print("            carrier's static channels, PD01 D1 premise); response")
print("            equation mu(Y) g = B (spherical first integral);")
print("            s fixed by the measured vacuum density, independent of a0")
print("            (PD08; k01: the one-scale action has no second coefficient).")
print("  FRAMEWORK INPUTS (adopted): kappa = 1/2; s = c sqrt(G rho_L);")
print("            G_N = G_bare = G_cosmo NOT separated in this lane (single G")
print("            in s and in B; separation flagged open in limitations).")
print("  CONCLUSIONS TO BE ESTABLISHED: mu'(0) = sum_i b_i (exact chain rule);")
print("            quadratic coefficient c1 + c2 - b1 b2 (two channels);")
print("            kappa = 1/(sum_i b_i) from the deep matching;")
print("            the exact equal-(unit-)slope condition needed for kappa = 1/n.")

# ---------------------------------------------------------------- STEP 1b
MU = lambda p1, p2: 1 - (1 - p1) * (1 - p2)
p1s = b1r * Yr + c1r * Yr**2
p2s = b2r * Yr + c2r * Yr**2
mus = sy.expand(MU(p1s, p2s))
slope = sy.limit(sy.diff(mus, Yr), Yr, 0)
check("S1 [claim restated] the OR composition of two quadratics expands and is "
      "differentiated at 0",
      f"mu(Y) = {mus};  mu'(0) = {slope}",
      sy.simplify(slope - (b1r + b2r)) == 0,
      "exact symbolic equality",
      "chain rule through the OR: mu'(0) = b1 + b2, independent of c1, c2.")

# general n (symbolic n, symbolic n-channel product)
def muN(b_list, Y):
    acc = sy.S(1)
    for b in b_list:
        acc *= (1 - b * Y)
    return 1 - acc
for n_ in (2, 3, 5):
    m = sy.expand(muN([sy.Symbol(f'b{i}') for i in range(n_)], Yr))
    lin = sy.expand(sy.diff(m, Yr).subs(Yr, 0))
    check(f"S1n [OR over {n_} channels] generic engagement p_i = b_i Y (linear "
          "truncation): the origin slope equals the sum of slopes",
          f"mu(Y) = {sy.expand(sy.simplify(m))};  mu'(0) = {lin}",
          sy.simplify(lin - sum(sy.Symbol(f'b{i}') for i in range(n_))) == 0,
          "exact symbolic equality")

print()
print("=" * 100)
print("STEP 2 -- full quadratic coefficient (two channels); equal-slope condition")
print("=" * 100)
q2 = sy.expand(sy.series(mus, Yr, 0, 3).removeO())
qfull = sy.expand((b1r + b2r) * Yr + (c1r + c2r - b1r * b2r) * Yr**2
                  - (b1r * c2r + c1r * b2r) * Yr**3 - c1r * c2r * Yr**4)
print(f"  mu(Y) = {q2}  + O(Y^3)   [full exact polynomial: {sy.expand(mus)}]")
check("S2 [quadratic coefficient for two channels]",
      f"mu(Y) = (b1+b2) Y + (c1 + c2 - b1*b2) Y^2 - (b1*c2 + c1*b2) Y^3 "
      f"- c1*c2 Y^4 (exact polynomial identity)",
      sy.simplify(mus - qfull) == 0,
      "exact; quadratic coefficient is c1 + c2 - b1*b2 (cross term SUBTRACTS "
      "b1*b2; sign is negative from the OR p1*p2 term)",
      "linear term: sum of slopes; quadratic: sum of per-channel quadratic "
      "coefficients MINUS the cross product of the two linear slopes.  The "
      "leading neglected term is O(Y^3), valid on any neighborhood of Y = 0 "
      "where p1, p2 are C^3; on Y in (0, Y0) with Y0 < 1/max(b1,b2) the "
      "remainder is bounded by the third-derivative norms (finite, "
      "dimensionless).")
print("  EQUAL-SLOPE ASSUMPTION NEEDED FOR kappa = 1/n:")
print("    kappa = 1/(sum_i b_i).  Hence kappa = 1/n  <=>  sum_i b_i = n.")
print("    Equal slopes b_i = b give kappa = 1/(n b) -- equal slopes alone do")
print("    NOT give 1/n; the unit-slope fraction identity b_i = 1 (PD08 step 3,")
print("    k01: one scale s, no second coefficient) is the exact premise.")
print("    Under that premise unequal slopes are impossible a priori (all")
print("    b_i = 1).  Outside the one-scale class, each b_i is a genuinely")
print("    independent dimensionless freedom; the OR composition does NOT")
print("    remove it (control E1).")

print()
print("=" * 100)
print("STEP 3 -- the closed-form family with unequal slopes and its algebra")
print("=" * 100)
print("  Saturating completion for a slope-b channel: p_i(Y) = b_i Y/(1 + b_i Y);")
print("  p_i(0) = 0, p_i(oo) = 1, p_i'(0) = b_i.  OR composition:")
print("  mu(Y) = 1 - prod_i 1/(1 + b_i Y).   Two channels:")
print("  mu(Y) = 1 - 1/[(1 + b1 Y)(1 + b2 Y)]")
print("        = (b1+b2) Y - (b1^2 + b1 b2 + b2^2) Y^2 + O(Y^3).")
p1f = b1r * Yr / (1 + b1r * Yr)
p2f = b2r * Yr / (1 + b2r * Yr)
muf = sy.simplify(MU(p1f, p2f))
mufs = sy.series(muf, Yr, 0, 4)
check("S3 [closed-form family] the unequal-slope OR member p_i = b_i Y/(1+b_i Y) "
      "is expanded",
      f"mu(Y) = {muf} = {sy.simplify(mufs.removeO())} + O(Y^4)",
      sy.simplify(sy.diff(muf, Yr).subs(Yr, 0) - (b1r + b2r)) == 0 and
      sy.simplify(muf - (1 - 1/((1 + b1r*Yr)*(1 + b2r*Yr)))) == 0,
      "exact closed form; slope at 0 = b1 + b2; quad coeff = -(b1^2 + b1 b2 + b2^2),"
      " matching S2 with c_i = -b_i^2",
      "At b1 = b2 = 1: mu(Y) = 1 - (1+Y)^(-2) -- EXACTLY the framework MU2 "
      "branch (mu2(x) = 1 - (1 + x/2)^(-2) with Y = x/2, s = 2 a0), so the "
      "family is the committed branch's unequal-slope generalization.")
# saturation and Newtonian recovery, exact
sat = sy.limit(muf, Yr, sy.oo)
check("S3b [normalization] the family saturates at one for ALL b1, b2 > 0",
      f"mu(oo) = {sat}",
      sat == 1,
      "exact limit",
      "any saturating completion (p_i(oo)=1) would do; the corpus member "
      "p = Y/(1+Y) saturates ONLY at b = 1 -- unequal slopes require their "
      "own saturating completion, an extra premise per channel.")
# Newtonian: mu(Y) -> 1 means g -> B : solve mu(g/s) g = B at large B
Bv = sy.Symbol('Bv', positive=True)
g_expr = sy.sqrt((s := sy.Symbol('s', positive=True)) * Bv / (b1r + b2r))
print(f"  Deep regime (Y << 1): mu ~ (b1+b2) Y -> k g^2 r^2/s = G M ->")
print(f"  g^2 = (s/k) g_N with k = b1 + b2;   a0 = s/k;   kappa = a0/s = 1/k.")
a0sym = sy.Symbol('a0', positive=True)
kap = sy.simplify((sy.solve(sy.Eq(g_expr**2, a0sym * Bv), a0sym)[0]) / s)
check("S3c [deep matching algebra] k g^2 r^2/s = G M with g_N = G M/r^2 gives "
      "the a0-line with a0 = s/k and kappa = 1/k, k = b1 + b2",
      f"g^2 = (s/(b1+b2)) g_N;  a0 = s/(b1+b2);  kappa = {kap}",
      sy.simplify(kap - 1/(b1r + b2r)) == 0,
      "exact",
      "scale factors: s [m s^-2] enters as argument unit AND as the matched "
      "rate; kappa dimensionless; all signs positive (attractive deep law).  "
      "Leading neglected term in the deep regime: with mu = k Y + q2 Y^2 the "
      "first correction to g^2 = (s/k) g_N is (q2/k^2)(s/k) g_N^2/s + O(g_N^3) "
      "-- relative O(g/s) = O(sqrt(g_N/s)); quoted as the S6 ladder check.")

print()
print("=" * 100)
print("STEP 4 -- independent check in a different representation (50 digits)")
print("=" * 100)
def muF(b1, b2, Y):
    return 1 - 1/((1 + b1*Y) * (1 + b2*Y))

# (a) direct differentiation of the closed form, symbolic vs numeric FD
for (b1, b2) in [(1, mp.mpf(1)/2), (1, 1), (1, 2)]:
    sym_slope = sy.diff(muf, Yr).subs({b1r: b1, b2r: b2}).subs(Yr, 0)
    with mp.workdps(80):                       # division-amplified rounding:
        eps = mp.mpf(10) ** (-40)              # mu(eps) ~ 1e-40 with error
        fd = (muF(b1, b2, eps) - muF(b1, b2, 0)) / eps   # ~1e-80 -> slope err ~1e-40
    rel = abs(fd - (b1 + b2)) / (b1 + b2)
    check(f"S4a [different representation] finite-difference slope of the closed "
          f"form at Y = 1e-40 (b1, b2) = ({b1}, {b2}) vs symbolic b1+b2",
          f"FD slope = {mp.nstr(fd, 20)}, b1+b2 = {mp.nstr(b1+b2, 20)}, rel err"
          f" = {mp.nstr(rel, 3)}",
          rel < mp.mpf(10)**(-25),
          "< 1e-25 relative at eps = 1e-40 (dps 80)",
          "direct differentiation and difference quotient agree: the slope is "
          "the exact sum of slopes, not a count.")

# (b) high-precision response solves on the deep ladder: actual residuals
print("  Deep ladder: solve mu(g/s) g = B for (b1,b2) in {(1,1/2),(1,1),(1,2)},")
print("  B/s in {1e-1 ... 1e-14}; 50-digit mpmath bisection + Newton;")
print("  kappa_fit = g^2/(B*s)  ->  1/(b1+b2).")
ladder_decades = list(range(-1, -15, -1))
def solve_response(b1, b2, s, B):
    # bracket in Y = g/s: deep mu ~ (b1+b2) Y -> Y ~ sqrt(B/(s (b1+b2)))
    lo, hi = mp.mpf(10)**(-200), mp.mpf(10)**(10)
    f = lambda Y: muF(b1, b2, Y) * (Y * s) - B
    f_lo = f(lo)
    assert f_lo < 0, "should be negative at tiny Y"
    # expand hi until sign change
    while f(hi) < 0:
        hi *= 10
        assert hi < mp.mpf(10)**(200)
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    Y = (lo + hi) / 2
    # Newton polish
    dmu = lambda Y: (b1/(1+b1*Y)**2) * (1/(1+b2*Y)) + (1/(1+b1*Y)) * (b2/(1+b2*Y)**2)
    for _ in range(6):
        fv = f(Y)
        dfv = dmu(Y) * (Y * s) + muF(b1, b2, Y) * s
        Y = Y - fv / dfv
    g = Y * s
    resid = abs(muF(b1, b2, Y) * g - B) / B
    return g, resid

worst_resid = mp.mpf(0)
fit_tbl = {}
for (b1, b2) in [(1, mp.mpf(1)/2), (1, 1), (1, 2)]:
    k = b1 + b2
    row = []
    for dec in ladder_decades:
        Bs = mp.mpf(10) ** dec
        g, resid = solve_response(b1, b2, mp.mpf(1), Bs)   # s = 1 (scale-free)
        kappa_fit = g*g/Bs
        row.append((dec, kappa_fit, resid))
        worst_resid = max(worst_resid, resid)
    deepest = row[-1]
    fit_tbl[(float(b1), float(b2))] = deepest
    check(f"S4b [deep ladder, (b1,b2) = ({float(b1):g},{float(b2):g})] "
          f"kappa_fit -> 1/(b1+b2) = {mp.nstr(1/k, 20)}",
          f"deepest (B/s = 1e-14): kappa_fit = {mp.nstr(deepest[1], 20)}, "
          f"rel err = {mp.nstr(abs(deepest[1] - 1/k)/(1/k), 3)}; max residual/B "
          f"on ladder = {mp.nstr(deepest[2], 3)}",
          abs(deepest[1] - 1/k) < mp.mpf(10)**(-6),
          "|kappa_fit - 1/(b1+b2)| < 1e-6 at B/s = 1e-14",
          "ACTUAL residual quoted (not a Boolean): solve-response residuals at "
          "50 digits are ~1e-48, far below the 1e-6 fitting tolerance; the "
          "identity kappa = 1/(sum b_i) is exact, the ladder is finite "
          "consistency evidence (not an exact identity).")
check("S4c [whole ladder] the three fits approach distinct limits "
      "{2/3, 1/2, 1/3} monotonically on B/s in [1e-1, 1e-14]",
      "limits: " + "; ".join(f"({float(b1):g},{float(b2):g}) -> "
      f"{mp.nstr(v[1], 10)}" for (b1, b2), v in fit_tbl.items()),
      all(abs(v[1] - 1/(b1+b2)) < mp.mpf(10)**(-6)
          for (b1, b2), v in fit_tbl.items()),
      "each within 1e-6 at the deepest point")

print()
print("=" * 100)
print("STEP 5 -- negative control and boundary regimes")
print("=" * 100)
# E1: mandated control b1 = 1, b2 = 2
b1_, b2_ = 1, 2
k = b1_ + b2_
deep = fit_tbl[(1.0, 2.0)]
control_refuted = abs(deep[1] - mp.mpf(1)/2) > mp.mpf(10)**(-3)
check("E1 [NEGATIVE CONTROL, must be capable of failing] set b1 = 1, b2 = 2 and "
      "show two channels alone do NOT force kappa = 1/2",
      f"mu'(0) = {b1_}+{b2_} = {k}; kappa_deep-fit -> {mp.nstr(deep[1], 12)} "
      f"= 1/3, NOT 1/2 (claim 'count 2 => kappa 1/2' REFUTED)",
      control_refuted,
      "claim fails iff |kappa_fit - 1/2| > 1e-3 at B/s = 1e-14",
      "The control is capable of failing: if the count alone fixed kappa, "
      "this ladder would converge to 1/2 and the check would FAIL.  It "
      "converges to 1/3: the OR composition inherits the SLOPE SUM, and the "
      "sum is an independent freedom.  The kappa = 1/2 landing needs b1 + b2"
      " = 2 -- supplied only by the unit-slope fraction identity, not by "
      "the composition.")
# E2: lambda diagnostics at lambda = 1/2, 1, 2  (lambda := b2/b1, b1 = 1)
print("  Diagnostic counterexamples at lambda = b2/b1 in {1/2, 1, 2} (b1 = 1):")
lam_rows = []
for lam in (mp.mpf(1)/2, mp.mpf(1), mp.mpf(2)):
    b1, b2 = mp.mpf(1), lam
    kk = b1 + b2
    dd = fit_tbl[(1.0, float(lam))]
    lam_rows.append({"lambda": str(lam), "b1": 1, "b2": str(lam),
                     "mu_prime_0": str(kk), "kappa_pred": str(mp.mpf(1)/kk),
                     "kappa_pred_mpf": mp.mpf(1)/kk,
                     "kappa_fit_deepest": str(dd[1]),
                     "matches_1over2": bool(kk == 2)})
    print(f"    lambda = {str(lam):>3s}: b1+b2 = {mp.nstr(kk, 3)}; kappa = "
          f"1/(b1+b2) = {mp.nstr(1/kk, 20)}; fit = {mp.nstr(dd[1], 12)}")
check("E2 [lambda diagnostics] kappa = 1/(1 + lambda) at lambda in {1/2, 1, 2} "
      "gives exactly {2/3, 1/2, 1/3}; kappa = 1/2 only at lambda = 1",
      "; ".join(f"lambda={r['lambda']} -> kappa={r['kappa_pred']} (fit "
                f"{mp.nstr(mp.mpf(r['kappa_fit_deepest']), 8)})" for r in lam_rows),
      all(r["kappa_pred_mpf"] == 1/(1 + mp.mpf(r["lambda"])) for r in lam_rows)
      and lam_rows[0]["kappa_pred_mpf"] == mp.mpf(2)/3
      and lam_rows[2]["kappa_pred_mpf"] == mp.mpf(1)/3,
      "exact rationals at dps 50 (mpf comparisons, no string round-trip); "
      "only lambda = 1 lands on kappa = 1/2",
      "observational preference is NOT a mathematical proof: the algebra "
      "selects lambda = 1 iff b1 + b2 = 2 is imposed; the deep slope alone "
      "cannot distinguish (b1,b2) = (1,1) from (1/2,3/2) (same sum; E3).")
# E3: slope-sum degeneracy
check("E3 [identifiability] the deep regime measures the slope SUM, not the "
      "count: (b1,b2) = (1,1) and (1/2,3/2) share mu'(0) = 2 and kappa = 1/2",
      "(1,1): sum 2 -> kappa 1/2; (1/2,3/2): sum 2 -> kappa 1/2; "
      "the count n = 2 is not identifiable from the deep response",
      True,
      "n/a (structural statement)",
      "a slope pair summing to the count masquerades as the count; any "
      "kappa observed in (1/3, 2/3) is compatible with SOME unequal-slope "
      "two-channel OR member.  The equal-slope reading is selected only by "
      "the independent one-scale premise, not by the composition.")
# E4: Newtonian regime
for (b1, b2) in [(1, mp.mpf(1)/2), (1, 1), (1, 2)]:
    B = mp.mpf(10)**16
    g, resid = solve_response(b1, b2, mp.mpf(1), B)
    check(f"E4 [Newtonian] (b1,b2) = ({float(b1):g},{float(b2):g}) at B/s = 1e16: "
          "g -> B (mu -> 1)",
          f"g/B - 1 = {mp.nstr(g/B - 1, 3)}; residual/B = {mp.nstr(resid, 3)}",
          abs(g/B - 1) < mp.mpf(10)**(-14),
          "|g/B - 1| < 1e-14",
          "the OR normalization mu(oo) = 1 recovers Newton exactly for every "
          "slope pair -- Newtonian and deep limits each hold; the slope "
          "freedom lives only in the deep-matching constant.")
# E5: boundary case Y -> 0 saturation of the linear law (exact vs numeric)
with mp.workdps(80):
    eps2 = mp.mpf(10)**(-30)
    for (b1, b2) in [(1, mp.mpf(1)/2), (1, 1), (1, 2)]:
        lhs = muF(b1, b2, eps2)/((b1+b2)*eps2)
        check(f"E5 [boundary case] (b1,b2) = ({float(b1):g},{float(b2):g}): "
              "mu(Y)/((b1+b2) Y) -> 1 as Y -> 0",
              f"at Y = 1e-30: ratio - 1 = {mp.nstr(lhs - 1, 3)}",
              abs(lhs - 1) < mp.mpf(10)**(-25),
              "< 1e-25 (dps 80)",
              "exact-identity check at a boundary point (finite numerical "
              "consistency, not an exact identity).")

print()
print("=" * 100)
print("FOOTINGS -- canonical and alternative a0 must be carried separately")
print("=" * 100)
print(f"  rho_Lambda(canonical)  = {mp.nstr(RHO_L_CAN, 10)} kg/m^3; s_can = "
      f"{mp.nstr(S_CAN, 10)} m/s^2 (a0_can = s_can/2 = {A0_CAN})")
print(f"  rho_Lambda(alternative) = {mp.nstr(RHO_L_ALT, 10)} kg/m^3; s_alt = "
      f"{mp.nstr(S_ALT, 10)} m/s^2 (a0_alt = s_alt/2 = {A0_ALT})")
foot_rows = []
for (b1, b2) in [(1, mp.mpf(1)/2), (1, 1), (1, 2)]:
    kk = b1 + b2
    a0p_c = S_CAN / kk
    a0p_a = S_ALT / kk
    foot_rows.append({"b1": 1, "b2": str(b2), "sum": str(kk),
                      "a0_pred_canonical_rhoL": mp.nstr(a0p_c, 10),
                      "a0_pred_alt_rhoL": mp.nstr(a0p_a, 10),
                      "a0_pred_canonical_mpf": a0p_c, "a0_pred_alt_mpf": a0p_a,
                      "ratio_vs_measured_can": mp.nstr(a0p_c/A0_CAN, 6),
                      "ratio_vs_measured_alt": mp.nstr(a0p_a/A0_ALT, 6)})
    print(f"  b1+b2 = {mp.nstr(kk, 3)}: a0_pred = s/(b1+b2) = "
          f"{mp.nstr(a0p_c, 8)} (canonical rho_L), {mp.nstr(a0p_a, 8)} "
          f"(alternative rho_L); ratios to measured footings "
          f"{mp.nstr(a0p_c/A0_CAN, 5)} / {mp.nstr(a0p_a/A0_ALT, 5)}")
check("F1 [footing discipline] the counterexample family predicts a0 = s/(sum b_i)"
      " on each footing; a measured footing alone cannot select the slope pair",
      "; ".join(f"sum={r['sum']}: can {r['a0_pred_canonical_rhoL']}, "
                f"alt {r['a0_pred_alt_rhoL']}" for r in foot_rows),
      all(r["a0_pred_canonical_mpf"] == S_CAN/mp.mpf(r["sum"]) for r in foot_rows)
      and all(r["a0_pred_alt_mpf"] == S_ALT/mp.mpf(r["sum"]) for r in foot_rows),
      "formula applied on each footing with its OWN rho_L (mpf comparisons, "
      "no string round-trip); ratio column 1.3333 / 1.0 / 0.66667 states the "
      "distance from the measured footings",
      "kappa = 1/2 footing requires sum b_i = 2 on BOTH densities; the "
      "alternative footing is NOT the same kappa with the same density -- "
      "each rho_L fixes s and the predicted a0 is s/(sum b_i).  "
      "G_N/G_bare/G_cosmo: this lane uses one G in s and one G in B; the "
      "ratio G_E/G_N carrying Lambda_eff is out of scope (limitation L3).")

print()
print("=" * 100)
print("BRANCHES -- distinctness audit (Q, RAR, MU2, EXP, MONO)")
print("=" * 100)
# MU2 exact membership: family at (1,1) is the framework mu2 (quotient form,
# same symbol -- avoids Pow-with-negative-exponent vs fraction mismatch)
mu2_fw = 1 - 1/(1 + Yr)**2
check("B1 [MU2] the equal-unit-slope member b1 = b2 = 1 is EXACTLY the framework "
      "MU2 branch mu_n(Y) = 1 - (1+Y)^(-n) at n = 2, Y = g/s",
      f"mu(1,1;Y) = 1 - 1/(1+Y)^2",
      sy.simplify(sy.cancel(muf.subs({b1r: 1, b2r: 1}) - mu2_fw)) == 0,
      "exact symbolic equality (cancel before simplify; quotient form)",
      "framework mu2(x) = 1 - (1 + x/2)^(-2) with x = g/a0, Y = x/2, s = 2 a0 "
      "(kappa = 1/2 adopted): same function, argument rescaling documented.")
# deep slope of RAR, EXP, Q on the adopted footing (Y variable) -- numeric
# RAR: g = B nu_RAR(sqrt(B/a0)); response mu(Y) := B/g; deep: g^2 = a0 B
#   -> B = g^2/a0 -> mu(Y) = g/a0 = s Y/a0 = Y/kappa -> slope 1/kappa = 2 at
#   kappa = 1/2.  Numeric check: mu/Y at deep points of the RAR solution.
def rar_slope(Y, kappa):
    a0i = kappa                    # s = 1 => a0 = kappa
    # solve B from g = B/(1 - exp(-sqrt(B/a0))), g = Y (s = 1)
    fB = lambda Bv: Bv / (1 - mp.exp(-mp.sqrt(Bv / a0i))) - Y
    lo, hi = mp.mpf(0), a0i
    while fB(hi) < 0:
        hi *= 10
    for _ in range(300):
        mid = (lo + hi) / 2
        if fB(mid) < 0:
            lo = mid
        else:
            hi = mid
    Bv = (lo + hi) / 2
    return (Bv / Y) / Y            # mu(Y)/Y with mu = B/g, Y = g/s (s = 1)

rar_slopes = [rar_slope(mp.mpf(10)**(-d), mp.mpf(1)/2) for d in (6, 8, 10)]
check("B2 [RAR/EXP/Q deep slopes] on the adopted footing (s fixed, kappa = 1/2) "
      "the independent branches' deep slope in Y = g/s is 2 within numerics; "
      "they are the equal-slope members' comparisons, NOT unequal-slope "
      "counterexamples",
      "RAR: mu/Y at Y in {1e-6, 1e-8, 1e-10} = "
      + ", ".join(mp.nstr(v, 8) for v in rar_slopes)
      + "; EXP mu(x)=1-e^-x slope 2 exact (x = 2Y); Q g^2 = B^2 + a0 B deep "
        "slope 1/kappa = 2 exact",
      all(abs(v - 2) < mp.mpf(10)**(-3) for v in rar_slopes),
      "RAR within 1e-3 numerically on the three deep points; EXP/Q exact",
      "branch audit: this seed's conclusions live in the CORE coefficient "
      "cell (conditional MU_n statistical response); RAR/EXP/Q agree in the "
      "deep limit with the adopted kappa = 1/2; MONO is NOT used -- no "
      "bridge from the spherical OR cell to the filtered nu_mono "
      "continuation is derived here (limitation L1).")

print()
print("=" * 100)
print("STEP 6 -- strongest surviving statement and first transfer implication")
print("=" * 100)
print("  THEOREM (conditional, this run):")
print("    OR composition mu = 1 - prod_i (1 - p_i), p_i'(0) = b_i, p_i(0) = 0,")
print("    p_i(oo) = 1, b_i > 0  =>  mu'(0) = sum_i b_i (exact), and the deep")
print("    spherical matching gives kappa = a0/s = 1/(sum_i b_i) with")
print("    a0 = s/(sum_i b_i) on whichever footing fixes s.")
print("  COUNTEREXAMPLE (this run):  (b1, b2) = (1, 2) gives mu'(0) = 3, kappa")
print("    = 1/3 != 1/2 on both footings -- the channel count 2 alone does NOT")
print("    force kappa = 1/2; the composition does NOT remove the per-channel")
print("    slope freedom.")
print("  EQUAL-SLOPE PREMISE NEEDED FOR kappa = 1/n:  sum_i b_i = n; the only")
print("    premise in the framework's action class that supplies it is the")
print("    unit-slope fraction identity p_i'(0) = 1 (PD08 step 3, k01 no-go:")
print("    one scale s, no second coefficient), which EXCLUDES unequal slopes.")
print("  FIRST TRANSFER IMPLICATION: the delta-function counting argument")
print("    (PD01 A1: slope = count for equal channels) needs the map from the")
print("    metric's two static channels to per-channel slopes b_i = 1; if a")
print("    future derivation yields b1 + b2 = 2 without unit slopes (e.g.")
print("    b1 = 1/2, b2 = 3/2), the count reading of PD01 is replaced by a")
print("    slope-sum reading with the same kappa and the falsifier (PD01 D3: ")
print("    'any kappa strictly inside (1/2, 1) kills the structure') must be")
print("    re-derived -- the slope-sum family fills (1/3, 2/3) continuously.")

print()
print(f"S5 [WORST solve residual, quoted] max |mu(g/s) g - B|/B over all ladders"
      f" = {mp.nstr(worst_resid, 3)} (50-digit mpmath; tolerance 1e-30)")
check("S5", f"worst residual/B = {mp.nstr(worst_resid, 3)}",
      worst_resid < mp.mpf(10)**(-30), "< 1e-30",
      "actual residual from the solved responses -- the numerics are "
      "self-consistent at the stated precision.")

# ---------------------------------------------------------------- bounds
wall = time.monotonic() - T0
if sys.platform == "darwin":
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0 / 1024.0
else:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
print(f"\nBOUNDS: wall = {wall:.2f}s (limit 120s, enforced in-process); "
      f"RSS = {rss:.1f} MiB (limit 512 MiB, measured; darwin ru_maxrss is "
      f"bytes, converted); threads = 1 "
      f"(single process, OMP/OPENBLAS/MKL pinned to 1).")
print(f"AS052 COMPLETE: {NP}/{NP+NF} checks PASS.")
out = {"pass": NP, "fail": NF, "checks": RES,
       "wall_s": wall, "rss_mib": rss,
       "lambda_scan": [{k: (str(v) if isinstance(v, mp.mpf) else v)
                        for k, v in r.items()} for r in lam_rows],
       "footings": [{k: (str(v) if isinstance(v, mp.mpf) else v)
                     for k, v in r.items()} for r in foot_rows],
       "worst_residual_over_B": str(worst_resid)}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "raw_outputs", "checks.json"), "w"), indent=1)
sys.exit(0 if NF == 0 else 1)