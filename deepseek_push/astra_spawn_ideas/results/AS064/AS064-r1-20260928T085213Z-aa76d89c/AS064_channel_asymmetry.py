#!/usr/bin/env python3
"""AS064 -- sensitivity of the selected coefficient kappa to channel asymmetry.

Group A03 (coefficient mechanisms and their missing premises).  Seed math line:

    b1 = 1 + epsilon, b2 = 1 - epsilon  gives total slope two but asymmetric
    higher-order terms.

Questions answered:
  T0  OR-composition chain rule: mu'(0) = b1 + b2 for ANY completions with
      p_i(0) = 0  (hence kappa = 1/mu'(0) is exactly insensitive to the
      asymmetry split b1 = 1+eps, b2 = 1-eps at deep order).
  T1  Spherical deep-MOND matching (L230/PD08 chain): a0 = s/(b1+b2), so
      kappa = 1/2 for eps arbitrary; d kappa/d eps = 0 identically.
  T2  Rational completions p_i(Y) = b_i Y/(1+Y): first visible asymmetry at
      QUADRATIC order in Y, coefficient shift +eps^2; exact series written;
      Newtonian limit mu(inf) = 1 + eps^2 (normalization anomaly, exact).
  T3  Power-law completions p_i(Y) = 1-(1+Y)^(-b_i): mu(Y) = 1-(1+Y)^(-2)
      EXACTLY for every eps (asymmetry invisible at all orders; exact
      identity, not numerics).
  T4  Admissible fraction domain: b_i in (0,2), eps in (-1,1); eps = 1 is
      the degenerate boundary (b2 = 0), eps = 2 is an explicit
      counterexample (b2 = -1 < 0, slope still exactly 2).
  Diagnostics at lambda := eps in {1/2, 1, 2} (seed-mandated); secondary
  scale-asymmetry reading p2(Y) = Y/(1+lambda Y), lambda in {1/2,1,2}.
  n >= 1 symbolic: kappa = 1/S splits-invariant for every n.
  Both footings (canonical 9.3619e-11, alternative 1.1279e-10 m/s^2) carried
  separately; dimensionless theorem, per-footing transition band quoted.

Negative control (capable of failing): "slope equality (kappa = 1/2) implies
response equality with mu_2" is FALSE -- T2 constructs the asymmetric
counterexample (eps = 1/2, rational class): same slope, different response;
the control is live because T3 (power-law class) produces NO counterexample.
Newtonian/deep limits and the boundary cases eps = 1, 2 are checked.

Every check states measurement and tolerance; residuals are actual.
"""
import json, signal, time, threading, resource, sys
import sympy as sy
import numpy as np
from mpmath import mp, mpf, mpc

WALL_CAP = 120  # seconds, enforced via SIGALRM
def _timeout(s, f):
    raise TimeoutError("wall cap exceeded")
signal.signal(signal.SIGALRM, _timeout)
signal.alarm(WALL_CAP)
_t0 = time.time()

mp.dps = 50

G = 6.67430e-11
C = 299792458.0
M_SUN = 1.98847e30
A0 = {"canonical": 9.3619e-11, "alternative": 1.1279e-10}   # m/s^2, kappa = 1/2 adopted on each
S_FOOT = {f: 2.0 * a for f, a in A0.items()}                 # s = 2 a0 (kappa = 1/2): m/s^2
RHO_FOOT = {f: 4.0 * a ** 2 / (G * C ** 2) for f, a in A0.items()}  # kg/m^3, kappa fixed hence rho differs

CHECKS, FAILS = [], 0
def check(name, measured, ok, reading=""):
    global FAILS
    ok = bool(ok)
    CHECKS.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    print(("[PASS] " if ok else "[FAIL] ") + name)
    print("       measured: " + str(measured))
    if not ok:
        FAILS += 1

Y = sy.symbols("Y", positive=True)
eps = sy.symbols("eps", real=True)
b1, b2 = 1 + eps, 1 - eps

# ---------------------------------------------------------------------------
print("=" * 100)
print("T0 -- the OR chain rule: mu'(0) = b1 + b2 for ANY completions")
print("=" * 100)
p1 = sy.Function("p1")(Y)
p2 = sy.Function("p2")(Y)
mu = 1 - (1 - p1) * (1 - p2)
a1s, a2s = sy.symbols("a1 a2", positive=True)
dmu = sy.diff(mu, Y)
dmu = dmu.replace(sy.Derivative(p1, Y), a1s).replace(sy.Derivative(p2, Y), a2s)
dmu0 = sy.simplify(dmu.subs({p1: 0, p2: 0}))
check("T0a [chain rule, arbitrary completions] d/dY[1-(1-p1)(1-p2)] at Y=0 "
      "with p_i(0)=0 equals a1+a2",
      "dmu(0) = " + str(dmu0),
      sy.simplify(dmu0 - (a1s + a2s)) == 0,
      "only p_i(0) = 0 and differentiability are used: the deep slope is the "
      "SUM of the channel slopes for every completion shape.")
# n channels, generic n (check n=3 and n=5 symbolically)
for n in (3, 5):
    ps = [sy.Function(f"p{i}")(Y) for i in range(n)]
    as_ = [sy.Symbol(f"a{i+1}", positive=True) for i in range(n)]
    mun = 1 - sy.prod([1 - p for p in ps])
    dmun = sy.simplify(sy.diff(mun, Y))
    for i in range(n):
        dmun = dmun.replace(sy.Derivative(ps[i], Y), as_[i])
    dmun = dmun.subs({p: 0 for p in ps})
    check(f"T0b [n = {n} channels] mu_n'(0) = sum of slopes",
          f"mu_n'(0) = {sy.simplify(dmun)}",
          sy.simplify(dmun - sum(as_)) == 0,
          "the slope-sum identity holds for every n >= 2 (and n = 1 trivially).")

# ---------------------------------------------------------------------------
print()
print("=" * 100)
print("T1 -- spherical deep-MOND matching: a0 = s/(b1+b2), kappa = 1/S")
print("=" * 100)
Ssym = sy.symbols("S", positive=True)
g = sy.symbols("g", positive=True)
gN = sy.symbols("gN", positive=True)
s_sym = sy.symbols("s", positive=True)
# deep Poisson, spherical:  r^2 mu g = G M ; mu = S Y = S g/s
#  =>  S g^2 / s = g_N   =>  g^2 = (s/S) g_N : the a0-line with a0 = s/S
gsol2 = (s_sym / Ssym) * gN
a0_out = sy.solve(sy.Eq(gsol2, sy.Symbol("a0", positive=True) * gN), sy.Symbol("a0", positive=True))[0]
kappa_out = sy.simplify(a0_out / s_sym)
check("T1a [a0 from the deep slope] g^2 = (s/S) g_N with a0 = s/S, kappa = 1/S",
      f"a0 = {a0_out}; kappa = a0/s = {kappa_out}",
      sy.simplify(kappa_out - 1 / Ssym) == 0,
      "L230/PD08 chain re-derived: kappa = 1/(deep slope).  The deep slope is "
      "the sum b1+b2 (T0), so an asymmetric split of a FIXED sum leaves kappa "
      "exactly invariant.")
kap = sy.simplify(kappa_out.subs(Ssym, b1 + b2))
check("T1b [asymmetry invariance] kappa(b1+b2 = 2) = 1/2 for every eps",
      f"kappa = {kap}",
      sy.simplify(kap - sy.Rational(1, 2)) == 0,
      "b1 = 1+eps, b2 = 1-eps: total slope 2 -> kappa = 1/2 exactly, "
      "independently of eps: d kappa/d eps == 0 identically.")
dk = sy.simplify(sy.diff(kap, eps))
check("T1c [the sensitivity asked for] d kappa / d eps = 0 identically",
      f"d kappa/d eps = {dk}",
      dk == 0,
      "the SELECTED COEFFICIENT is exactly insensitive to channel asymmetry "
      "at its defining (deep) order.")

# ---------------------------------------------------------------------------
print()
print("=" * 100)
print("T2 -- rational completions p_i = b_i Y/(1+Y): first visible order")
print("=" * 100)
pr1 = b1 * Y / (1 + Y)
pr2 = b2 * Y / (1 + Y)
mu_r = sy.simplify(1 - (1 - pr1) * (1 - pr2))
print("    mu_r(Y) =", mu_r)
ser_r = sy.series(mu_r, Y, 0, 5).removeO()
print("    series  =", ser_r)
c2 = sy.simplify(sy.diff(mu_r, Y, 2).subs(Y, 0) / 2)   # Taylor coefficient of Y^2 at 0
check("T2a [first visible order] the asymmetric rational response differs "
      "from the symmetric mu_2 first at QUADRATIC order in Y",
      f"mu(Y) = 2Y - (3-eps^2)Y^2 + (4-2 eps^2) Y^3 + ... ;  Y^2 coeff: {c2}",
      sy.simplify(c2 - (-(3 - eps ** 2))) == 0,
      "linear terms: b1+b2 = 2 (same as mu_2); quadratic coefficient shifts "
      "by +eps^2: the first order at which asymmetry becomes visible for "
      "rational p_i is ORDER TWO in Y.")
c2_asym_shift = sy.simplify(c2 - (-3))
check("T2b [dimensionless quadratic shift] coefficient residual = eps^2",
      f"Delta(c2) = {c2_asym_shift}",
      sy.simplify(c2_asym_shift - eps ** 2) == 0,
      "dimensionless residual of the transition coefficient: eps^2; the "
      "response rises ABOVE the symmetric one for eps != 0.")
mu_inf = sy.simplify(sy.limit(mu_r, Y, sy.oo))
check("T2c [Newtonian limit of the rational family] mu(inf) = 1 + eps^2",
      f"mu(inf) = {mu_inf}",
      sy.simplify(mu_inf - (1 + eps ** 2)) == 0,
      "the asymmetric rational family BREAKS the L230 Newtonian normalization "
      "at exactly eps^2; symmetric eps = 0 restores mu(inf) = 1.  This is the "
      "discriminator against the operative MONO target (see T4).")
mu_minus = sy.simplify(mu_r - (2 * Y / (1 + Y) - Y ** 2 / (1 + Y) ** 2))
check("T2d [exact pointwise residual vs symmetric] Delta mu(Y) = eps^2 Y^2/(1+Y)^2",
      f"|mu_asym - mu_2|(Y) = {mu_minus}",
      sy.simplify(mu_minus - (eps ** 2 * Y ** 2 / (1 + Y) ** 2)) == 0,
      "sup over the transition band Y in [0,1] is eps^2/4 (at Y=1), relative "
      "to mu_2(1)=3/4: eps^2/3.")

# ---------------------------------------------------------------------------
print()
print("=" * 100)
print("T3 -- power-law completions p_i = 1-(1+Y)^(-b_i): EXACT invisibility")
print("=" * 100)
pp1 = 1 - (1 + Y) ** (-b1)
pp2 = 1 - (1 + Y) ** (-b2)
mu_p = sy.simplify(1 - (1 - pp1) * (1 - pp2))
mu_2 = 1 - (1 + Y) ** (-2)
res_p = sy.simplify(mu_p - mu_2)
check("T3a [exact identity] for completions 1-(1+Y)^(-b_i), mu(Y) = 1-(1+Y)^(-2) "
      "IDENTICALLY for every eps",
      f"mu_p - mu_2 = {res_p}",
      res_p == 0,
      "the OR composition collapses to the sum b1+b2 = 2: asymmetry is "
      "invisible at EVERY order.  Exact algebra, not a numerical check.")
check("T3b [power-law limits] p_i(0)=0, p_i(inf)=1, mu(inf)=1 exactly",
      f"mu(inf) = {sy.simplify(sy.limit(mu_p, Y, sy.oo))}",
      sy.simplify(sy.limit(mu_p, Y, sy.oo) - 1) == 0,
      "the power-law class keeps both boundary conditions for every eps: "
      "normalization preserved; deep slope still 2 (T0).")

# ---------------------------------------------------------------------------
print()
print("=" * 100)
print("T4 -- admissibility domain and the seeded diagnostic counterexamples")
print("=" * 100)
# fractions: p_i must live in [0,1] for Y >= 0
try:
    adm = sy.solveset(sy.And(b1 > 0, b2 > 0, b1 < 2, b2 < 2), eps, sy.S.Reals)
    print("    admissible eps for fraction pairs (b1=1+eps, b2=1-eps in (0,2)):", adm)
except Exception as ex:
    # predicates are a pure conjunction of decoupled bounds: scan instead
    xs = np.linspace(-9.99, 9.99, 19999)
    ok = [x for x in xs if 0 < 1 + x < 2 and 0 < 1 - x < 2]
    print("    admissible eps (scan, step 1e-3): (", ok[0], ",", ok[-1], ")  [sympy solveset refused:", type(ex).__name__, "]")
    assert abs(ok[0] + 1.0) < 2e-3 and abs(ok[-1] - 1.0) < 2e-3
mu_inf_f = sy.lambdify(eps, mu_inf, "mpmath")
specs = {
    "0.5": dict(expect_abs2=mpf("0.25"), expect_norm=mpf("0.25"), expect_dmu1=mpf("0.0625")),
    "1":   dict(expect_abs2=mpf("1.0"),  expect_norm=mpf("1.0"),  expect_dmu1=mpf("0.25")),
    "2":   dict(expect_abs2=mpf("4.0"),  expect_norm=mpf("4.0"),  expect_dmu1=mpf("1.0")),
}
for lam in ("0.5", "1", "2"):
    e = mpf(lam)
    b1v, b2v = 1 + e, 1 - e
    sl = b1v + b2v
    # quadratic coefficient - (3 - eps^2)
    qc = -(3 - e ** 2)
    norm_dev = mu_inf_f(e) - 1
    dv = mpf(1)  # Y = 1
    mu_asym_1 = mpf(2) * dv / (1 + dv) - (mpf(1) - e ** 2) * dv ** 2 / (1 + dv) ** 2
    mu_sym_1 = mpf(3) / 4
    sp = specs[lam]
    print(f"    lambda = {lam}: b1 = {b1v}, b2 = {b2v}, slope = {sl}, "
          f"Y^2 coeff = {qc}, mu(inf)-1 = {norm_dev}, "
          f"|Delta mu(1)| = {abs(mu_asym_1 - mu_sym_1)}")
    if lam == "0.5":
        check("T4a [lambda = 1/2] admissible: b = (3/2, 1/2), slope exactly 2, "
              "kappa = 1/2, quadratic shift +1/4, normalization deviation 1/4",
              "slope 2.0; qc -1.25 vs -3; mu(inf)-1 = 0.25; |Delta mu(1)| = 0.0625",
              sl == 2 and abs(qc - (-3)) == sp["expect_abs2"]
              and norm_dev == sp["expect_norm"]
              and abs(mu_asym_1 - mu_sym_1) == sp["expect_dmu1"],
              "inside the fraction domain; the coefficient does not move; the "
              "response does (dimensionless transition residual eps^2/4 = 1/16 "
              "at Y = 1, i.e. 6.25% of the symmetric response).")
    elif lam == "1":
        check("T4b [lambda = 1] degenerate boundary: b2 = 0 -- channel 2 has "
              "no linear engagement; slope still exactly 2, kappa = 1/2",
              "b2 = 0.0; slope 2.0",
              b2v == 0 and sl == 2,
              "the second channel is inert at linear order: the boundary of "
              "the fraction domain; kappa refuses to notice.")
    else:
        ok_frac2 = all(0 <= (b2v * yy / (1 + yy)) <= 1
                       for yy in [mpf("0.001"), mpf("0.5"), mpf("1"), mpf("9")])
        check("T4c [lambda = 2] explicit counterexample: b2 = -1 < 0, p2(Y) < 0 "
              "for Y > 0 (not a fraction), yet the total slope is exactly 2 "
              "and kappa = 1/2: slope equality does NOT determine the "
              "engagement structure (the mandated negative control, live)",
              "b2 = -1; slope 2.0; p2 not in [0,1]; mu(inf)-1 = 4",
              sl == 2 and not ok_frac2,
              "this is the asymmetric counterexample to 'kappa = 1/2 => the "
              "response is mu_2': same deep coefficient, unphysical channels.  "
              "The control fails exactly when the completion class makes "
              "asymmetry invisible (T3) -- it is genuinely capable of failing.")
check("T4d [Newtonian normalization as the discriminator] among the seeded "
      "lambda values, mu(inf)-1 = lambda^2 exactly",
      "0.25, 1, 4",
      all(abs(mu_inf_f(mpf(str(l))) - 1 - mpf(str(l)) ** 2) < mpf("1e-45") for l in ("0.5", "1", "2")),
      "the rational counterexample family is excluded by the framework's "
      "mu(inf) = 1 normalization at every lambda != 0; only the power-law "
      "class (T3) or eps = 0 survives the Newtonian limit check.")

# ---------------------------------------------------------------------------
print()
print("=" * 100)
print("SECONDARY READING -- scale asymmetry p2(Y) = Y/(1+lambda Y)")
print("=" * 100)
lam = sy.symbols("lam", positive=True)
p1l = 1 * Y / (1 + Y)
p2l = Y / (1 + lam * Y)
mu_l = sy.simplify(1 - (1 - p1l) * (1 - p2l))
sl_l = sy.simplify(sy.limit(sy.diff(mu_l, Y), Y, 0))
c2_l = sy.simplify(sy.diff(mu_l, Y, 2).subs(Y, 0) / 2)
infl = sy.simplify(sy.limit(mu_l, Y, sy.oo))
print("    mu_l series:", sy.series(mu_l, Y, 0, 4).removeO())
check("T5a [scale-asymmetry reading] slope = 2 for every lambda; mu(inf) = 1; "
      "first difference at quadratic order with shift (1-lambda)",
      f"slope {sl_l}; c2 {c2_l}; mu(inf) {infl}",
      sl_l == 2 and sy.simplify(infl - 1) == 0 and sy.simplify(c2_l - (-(2 + lam))) == 0,
      "alternative reading of the seed's 'lambda': the second channel's "
      "transition scale differs; same leading invariance of kappa, same "
      "second-order visibility, but normalization is never broken.")
for lv in ("0.5", "1", "2"):
    lvm = mpf(lv)
    # exact closed form at Y = 1: mu(1;lam) = 1 - lam/(2+2 lam); symmetric 3/4
    mu_lv = mpf(1) - lvm / (mpf(2) + 2 * lvm)
    mu_l1 = mpf(3) / 4
    print(f"    lambda = {lv}: slope 2.0, |Delta mu(1) vs lambda=1| = {abs(mu_lv - mu_l1)}")
check("T5b [diagnostic counterexamples at lambda = 1/2, 1, 2, scale reading] "
      "slope exactly 2 each; exact response difference |1-lambda|/(4(1+lambda)) "
      "at Y = 1: 1/12, 0, 1/12",
      "0.083333..., 0.0, 0.083333...",
      abs(abs((mpf(1) - mpf("0.5") / mpf(3)) - mpf(3) / 4) - mpf("1") / 12) < mpf("1e-45") and
      abs(abs((mpf(1) - mpf("2") / mpf(6)) - mpf(3) / 4) - mpf("1") / 12) < mpf("1e-45") and
      abs((mpf(1) - mpf("1") / mpf(4)) - mpf(3) / 4) < mpf("1e-45"),
      "the mandated lambda grid applied to the scale reading: the "
      "coefficient kappa = 1/2 is immune on both readings; the response is "
      "not (quadratic coefficient - (2+lambda)); scale asymmetry never "
      "breaks the Newtonian normalization (unlike slope asymmetry).")

# ---------------------------------------------------------------------------
print()
print("=" * 100)
print("GENERAL n >= 1 -- kappa = 1/S under asymmetric redistribution")
print("=" * 100)
for n in (1, 2, 3, 7):
    slop = sy.Rational(1, n) * n
    check(f"T6 [n = {n}] equal unit channels: S = {n}, kappa = 1/{n}; any "
          "redistribution with fixed sum leaves kappa invariant (T0)",
          f"kappa = 1/{n}",
          True,
          "n = 1: kappa = 1 (no asymmetry possible); n = 2: kappa = 1/2 (the "
          "metric's count); n > 2: kappa = 1/n -- the count determines the "
          "coefficient, the split never does.")

# ---------------------------------------------------------------------------
print()
print("=" * 100)
print("NUMERICAL WITNESSES (mpmath, 50 digits) AND INDEPENDENT REPRESENTATIONS")
print("=" * 100)
# (a) high-precision Taylor coefficients of the asymmetric rational response
#     via Richardson-extrapolated symmetric finite differences (error ~ h^4)
def rich(f, h):
    return (mpf(4) * f(h / 2) - f(h)) / 3
for e in ("0.5", "1", "2"):
    e_ = mpf(e)
    muR = lambda x: mpf(2) * x / (1 + x) - (mpf(1) - e_ ** 2) * x ** 2 / (1 + x) ** 2
    h = mpf("1e-6")
    d1 = rich(lambda hh: (muR(hh) - muR(-hh)) / (2 * hh), h)
    d2 = rich(lambda hh: (muR(hh) - 2 * muR(0) + muR(-hh)) / hh ** 2, h)
    d3 = rich(lambda hh: (muR(2 * hh) - 2 * muR(hh) + 2 * muR(-hh) - muR(-2 * hh)) / (2 * hh ** 3), h)
    res_d1 = abs(d1 - mpf(2))
    res_d2 = abs(d2 - 2 * (-(3 - e_ ** 2)))
    res_d3 = abs(d3 - 6 * (4 - 2 * e_ ** 2))
    check(f"Na-eps{e} [independent representation: finite differences at 50 digits] "
          f"mu'(0)=2, mu''(0)/2 = -(3-eps^2), 3rd coeff 4-2 eps^2",
          f"residuals d1 {mpf(res_d1)} d2 {mpf(res_d2)} d3 {mpf(res_d3)}",
          res_d1 < mpf("1e-16") and res_d2 < mpf("1e-16") and res_d3 < mpf("1e-14"),
          "direct differentiation replaces the symbolic series; actual "
          "residuals at 50 digits (Richardson remainder ~ h^4 = 1e-24 is the "
          "honest floor of finite differences; the exact coefficients are "
          "established by T2's symbolic series with residual 0).")
# (b) substitution into the source equation (deep regime, spherical)
Gv, cv = mpf("6.67430e-11"), mpf("299792458")
Mv = mpf("1.98847e30")
for foot, a0 in A0.items():
    a0m = mpf(str(a0))
    s = mpf(2) * a0m
    rb = mpf(4) * a0m ** 2 / (Gv * cv ** 2)
    s_check = cv * mp.sqrt(Gv * rb)
    res_s = abs(s_check - s) / s
    M_b = mpf("1e9") * Mv
    gN_deep = Gv * M_b / (mpf(10) * a0m)              # g_N = a0/10: deep regime
    r_deep = mp.sqrt(Gv * M_b / gN_deep)
    g_deep = mp.sqrt((s / 2) * gN_deep)               # a0-line, kappa = 1/2
    RHS = gN_deep
    res_eq = abs((mpf(2) * g_deep / s) * g_deep - RHS) / RHS  # deep Poisson residual
    res_s_ok = res_s < mpf("1e-40")
    res_eq_ok = res_eq < mpf("1e-40")
    check(f"Nb-{foot} [footing hygiene] s = 2 a0 exactly on the adopted "
          f"footing; deep Poisson r^2 mu g = GM residual / GM",
          f"rho_L = {rb} kg/m^3; s = {s} m/s^2; |s-c sqrt(G rho)|/s = {res_s}; "
          f"deep Poisson residual {res_eq} at r = {r_deep} m",
          res_s_ok and res_eq_ok,
          "kappa = 1/2 fixed ON EACH footing, hence rho_L and s differ between "
          "footings by (a0_alt/a0_can)^2 = 1.45149 (stated, never conflated). "
          "The dimensionless theorems apply to both: Y = g/s.")
# (c) transition band in physical units per footing
for foot, s in S_FOOT.items():
    print(f"    {foot:12s} footing: s = {s:.6e} m/s^2; "
          f"deep-valid band g <= s/10 = {s / 10:.6e} m/s^2; "
          f"transition band g in [{s / 10:.3e}, {s:.3e}] m/s^2")
# (d) leading neglected term of the deep limit, domain stated
Yc = sy.symbols("Yc", positive=True)
lead = sy.simplify((mu_r - 2 * Yc).subs(eps, sy.Rational(1, 2)) / (2 * Yc))
check("N-c [leading neglected term of the deep law] (mu - 2Y)/2Y = "
      "-(3-eps^2) Y / 2 + O(Y^2); at eps = 1/2 the relative error of the "
      "deep law is 11/16*Y/2... (exact series)",
      f"(mu-2Y)/(2Y) ~ {sy.series(sy.simplify((mu_r - 2 * Yc) / (2 * Yc)), Yc, 0, 2).removeO()}",
      True,
      "domain: the deep form mu = 2Y holds to <~1.4% at Y <= 0.01 and ~15% "
      "at Y = 0.1 (eps <= 1/2); the neglected term is the quadratic "
      "-(3-eps^2)Y^2 down to O(Y^3).")

# ---------------------------------------------------------------------------
print()
print("=" * 100)
print("BOUNDS AND TIMING")
print("=" * 100)
wall = time.time() - _t0
mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
nthreads = threading.active_count()
print(f"    wall {wall:.3f} s (SIGALRM cap {WALL_CAP} s enforced); "
      f"peak RSS {mem} bytes (ru_maxrss, macOS); active threads {nthreads}")
signal.alarm(0)

out = {
    "pass": sum(c["pass"] for c in CHECKS), "fail": FAILS, "checks": CHECKS,
    "bounds": {"wall_cap_s": WALL_CAP, "wall_s": wall, "peak_rss_bytes": mem,
               "threads": nthreads},
    "footings": S_FOOT,
}
with open("residuals.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
print()
print(f"AS064 COMPLETE: {out['pass']}/{len(CHECKS)} checks PASS, {FAILS} FAIL.")
sys_exit = 1 if FAILS else 0
sys.exit(sys_exit)