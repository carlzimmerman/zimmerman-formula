#!/usr/bin/env python3
r"""H046 -- IS n = 2 FORCED BY THE HEALTH CONDITIONS?  (Agent J)

THE QUESTION.
    The programme's last free integer is n = 2, the DEEP SLOPE
        n = lim_{u -> 0} mu(u)/u ,   mu = f' ,  L = Lambda^4 f(K),  K = u^2,
    with u = g/(2 a_0).  H017/H030 derive it from the dimension,
    n = D(D-3)/2 = 2 at D = 4 -- which still uses the dimension as an input.
    This lane asks whether the HEALTH CONDITIONS alone force it:

      (i)   0 <= c_s^2 <= 1 for all K      (subluminal, no gradient instability)
      (ii)  f' > 0                          (no ghost)
      (iii) stability                       (c_s^2 >= 0, rho > 0)
      (iv)  the deep slope is finite and non-zero

THE MASTER IDENTITY (why the answer is NO).
    With K = u^2 and f'(K) = mu(u),
        2 K f''(K) = 2 u^2 * (mu'(u) / (2u)) = u * mu'(u),
    so the k-essence sound speed is
        c_s^2 = f' / (f' + 2 K f'') = mu / (mu + u mu')
              = 1 / (1 + d ln mu / d ln u).
    Health therefore constrains the LOG-SLOPE of mu and is exactly blind to
    its AMPLITUDE -- and the amplitude is precisely what n is.

THE ANSWER FOUND HERE:  NO.
    * (i)+(ii)+(iii)  <=>  mu > 0 and mu' >= 0                      (Part 1)
    * (iv) forces the deep sound speed to be exactly 1/2 -- for EVERY n,
      so the deep sound speed cannot discriminate n either          (Part 2)
    * an explicit healthy family with deep slope n exists for every n > 0;
      n = 1, 2, 3 are all fully healthy                             (Part 3)
    * even at FIXED n = 2 the functional form is not fixed by health (Part 4)

WHAT IS FOUND INSTEAD (two genuine, forced results).
    * UNIVERSAL DEEP SOUND SPEED.  Health + (iv) force c_s^2 -> 1/2 as
      K -> 0, independently of n.  The programme measures c_s^2 in [1/2, 1)
      (H001/H002); the 1/2 is therefore a PREDICTION, not a fit.
    * SHARP BOUND.  Inside the minimal Pade family mu = u(a+u)/(1+u)^2 --
      the family forced by mu(0)=0, mu(infinity)=1 and a double pole at
      u = -1 -- subluminality gives a <= 2 and positivity a >= 0, so
      0 <= n <= 2 and the observed n = 2 SATURATES the bound.  Scope: the
      family is assumed, so this is a bound, not a derivation of n = 2.

WHAT DOES FIX THE 2 (and it is not health).
    In f = K - c ln(1+sqrt K) - d/(1+sqrt K) + const:
      (alpha) finiteness of f'(0) forces d = c        (the 1/u pole cancels)
      (beta)  mu(0) = f'(0) = 0 (a MOND regime: no Newtonian floor) forces
              c = 2
      (gamma) the deep slope then equals c = 2.
    That is a derivation of the integer from REGULARITY + THE EXISTENCE OF A
    MOND REGIME.  Neither is a health condition, and the family is put in by
    hand.  Reported as the honest positive result, NOT as a health theorem.

HONEST SCOPE.  This lane does NOT claim n = 2 is derived.  It claims the
opposite: (i)-(iv) are proved insufficient, with an explicit counterexample
family, and the residual derivation routes are identified and bounded.

Every check states measurement and threshold separately.  Both footings are
carried throughout.
"""
import json
import sympy as sp

RES, NP_, NF_ = [], 0, 0


def check(name, measured, ok, threshold="", note=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured : {measured}")
    print(f"         threshold: {threshold}")
    if note:
        for ln in note.split("\n"):
            print(f"         {ln}")
    RES.append({"check": name, "measured": str(measured),
                "threshold": str(threshold), "pass": ok})
    if ok:
        NP_ += 1
    else:
        NF_ += 1
    return ok


u, K, a, c, d, n, A, q = sp.symbols('u K a c d n A q', positive=True)
Lam_meV = 2.2404                 # Lambda, H003/H016
M_Pl_GeV = 1.2209e19             # reduced Planck mass, H016
HBAR = 1.054571817e-34
CLIGHT = 2.99792458e8
EV_J = 1.602176634e-19
FOOT = {"canonical": 9.3619e-11, "alternative": 1.1279e-10}   # both footings

print("=" * 78)
print("H046 -- IS n = 2 FORCED BY HEALTH?   (c_s^2 = mu / (mu + u mu'))")
print("=" * 78)

# =============================================================== PART 0
print("\n" + "=" * 78)
print("PART 0 -- THE FUNCTION AND THE SOUND SPEED")
print("=" * 78)

f = K - 2 * sp.log(1 + sp.sqrt(K)) - 2 / (1 + sp.sqrt(K)) + 1
fp = sp.simplify(sp.diff(f, K))
mu2 = u * (2 + u) / (1 + u) ** 2                       # the kernel mu_2
mu2_alt = 1 - 1 / (1 + u) ** 2                         # identical form
fp_u = sp.simplify(fp.subs(sp.sqrt(K), u))

check("A1 [THE FUNCTION] f'(K) = mu_2(sqrt K) with "
      "mu_2(u) = u(2+u)/(1+u)^2 = 1 - (1+u)^-2, exactly",
      f"f'(u^2) - mu_2(u) = {sp.simplify(fp_u - mu2)}",
      sp.simplify(fp_u - mu2) == 0 and sp.simplify(mu2 - mu2_alt) == 0,
      "symbolic difference == 0",
      "The kernel is a single function; the '2' in u(2+u) and the exponent\n"
      "         in (1+u)^-2 are the SAME parameter.")

fpp = sp.simplify(sp.diff(f, K, 2)).subs(K, u ** 2)
cs2_given = sp.simplify(mu2 / (mu2 + 2 * u ** 2 * fpp))
cs2_target = (u ** 2 + 3 * u + 2) / (u ** 2 + 3 * u + 4)

check("A2 [SOUND SPEED] c_s^2 = f'/(f' + 2K f'') = (u^2+3u+2)/(u^2+3u+4) "
      "= 1 - 2/(u^2+3u+4)",
      f"difference = {sp.simplify(cs2_given - cs2_target)}",
      sp.simplify(cs2_given - cs2_target) == 0,
      "symbolic difference == 0",
      "Reproduces H001/H007 independently. Note the denominator minus the\n"
      "         numerator is the CONSTANT 2 -- the same integer again.")

# =============================================================== PART 1
print("\n" + "=" * 78)
print("PART 1 -- HEALTH <=> mu > 0 AND mu' >= 0  (a condition on the LOG-SLOPE)")
print("=" * 78)

mu_g = sp.Function('mu')
mu_g = sp.symbols('m')
# symbolic: with f'(K)=mu(u), u=sqrt(K):  f'' = mu'(u)/(2u)
mup = sp.Symbol('mup')
# 2 K f'' = 2 u^2 * mup/(2u) = u*mup  -- verified on the concrete f:
twoKfpp = sp.simplify(2 * u ** 2 * fpp)
check("B1 [CHAIN RULE] 2 K f''(K) = u mu'(u)  (verified on the concrete f)",
      f"2K f'' - u mu'(u) = "
      f"{sp.simplify(twoKfpp - u * sp.diff(mu2, u))}",
      sp.simplify(twoKfpp - u * sp.diff(mu2, u)) == 0,
      "symbolic difference == 0",
      "This is the whole reason health cannot see n: c_s^2 depends on\n"
      "         mu'/mu, i.e. on the LOG-SLOPE, never on the normalisation n.")

# the log-slope form, verified symbolically on the concrete f
logslope = sp.simplify(u * sp.diff(mu2, u) / mu2)
cs2_logslope = sp.simplify(1 / (1 + logslope))
check("B2 [MASTER IDENTITY] c_s^2 = 1 / (1 + dln(mu)/dln(u))  -- "
      "health is a statement about the LOG-SLOPE only",
      f"c_s^2 - 1/(1+dlnmu/dlnu) = {sp.simplify(cs2_given - cs2_logslope)}",
      sp.simplify(cs2_given - cs2_logslope) == 0,
      "symbolic difference == 0",
      "CONSEQUENCE: c_s^2 <= 1  <=>  dln mu/dln u >= 0  <=>  mu' >= 0,\n"
      "         with no appearance of the amplitude n anywhere.")

# numeric health scan of the actual f
import math


def cs2_num(uu):
    return (uu * uu + 3 * uu + 2) / (uu * uu + 3 * uu + 4)


def fp_num(uu):
    return uu * (2 + uu) / (1 + uu) ** 2


def fpp_num(uu):
    return 1.0 / (uu * (1 + uu) ** 3)


grid = [10.0 ** e for e in range(-8, 9)]
cs2_vals = [cs2_num(x) for x in grid]
fp_vals = [fp_num(x) for x in grid]
fpp_vals = [fpp_num(x) for x in grid]

check("C1 [NO SUPERLUMINALITY] 0 <= c_s^2 <= 1 for the actual f on "
      "u in [1e-8, 1e8]",
      f"c_s^2 in [{min(cs2_vals):.12f}, {max(cs2_vals):.12f}]",
      min(cs2_vals) >= 0.0 and max(cs2_vals) <= 1.0,
      "0 <= min and max <= 1",
      "The actual f is healthy. That is necessary but NOT sufficient to\n"
      "         single it out -- see Part 3.")
check("C2 [NO GHOST] f'(K) = mu_2 > 0 on the same grid",
      f"min f' = {min(fp_vals):.6e}",
      min(fp_vals) > 0.0, "min f' > 0")
check("C3 [CONVEXITY = SUBLUMINALITY] f''(K) > 0 on the same grid",
      f"min f'' = {min(fpp_vals):.6e}",
      min(fpp_vals) > 0.0, "min f'' > 0",
      "f'' > 0 is the same statement as c_s^2 < 1 (Part 1, B2).")

# =============================================================== PART 2
print("\n" + "=" * 78)
print("PART 2 -- WHAT (iv) DOES FORCE:  THE UNIVERSAL DEEP SOUND SPEED 1/2")
print("=" * 78)

# mu ~ A u^q  =>  c_s^2 = 1/(1+q), independent of A (hence of n)
mu_q = A * u ** q
fp_q = mu_q
fpp_q = sp.simplify(sp.diff(mu_q, u) / (2 * u))
cs2_q = sp.simplify(fp_q / (fp_q + 2 * u ** 2 * fpp_q))
cs2_q = sp.simplify(sp.powsimp(cs2_q))
print(f"      mu ~ A u^q  ->  c_s^2 = {cs2_q}")
for qq in [1, 2, 3]:
    print(f"        q = {qq} : c_s^2 = {sp.simplify(cs2_q.subs(q, qq))}")

check("D1 [UNIVERSALITY] for mu ~ A u^q the sound speed is exactly 1/(1+q), "
      "independent of the amplitude A",
      f"c_s^2(q=1,2,3) = "
      f"{[str(sp.simplify(cs2_q.subs(q, qq))) for qq in (1, 2, 3)]}",
      all(sp.simplify(cs2_q.subs(q, qq) - sp.Rational(1, 1 + qq)) == 0
          for qq in (1, 2, 3)),
      "c_s^2 = 1/(1+q) exactly for q = 1, 2, 3",
      "The amplitude A -- which is what n is -- cancels identically.")

q1 = sp.simplify(cs2_q.subs(q, 1))
check("D2 [THE FORCED VALUE] (iv) (deep slope finite and non-zero) means "
      "q = 1, hence c_s^2(0) = 1/2 for EVERY n",
      f"lim_K->0 c_s^2 = {q1}",
      q1 == sp.Rational(1, 2),
      "c_s^2(0) == 1/2 exactly",
      "THIS IS A GENUINE FORCED PREDICTION: any healthy k-essence with a\n"
      "         linear MOND regime has deep sound speed exactly c/sqrt(2).\n"
      "         The programme's measured range [1/2, 1) (H001 A-checks, H002)\n"
      "         is thus a prediction of health+(iv), not a fitted input --\n"
      "         and it holds for n = 1, 2, 3 alike, so it cannot select n.")

check("D3 [MEASURED] the actual f approaches 1/2 at the deep end "
      "(the approach is linear in u: c_s^2 = 1/2 + 3u/8 + O(u^2))",
      f"c_s^2(1e-8) - 1/2 = {cs2_num(1e-8) - 0.5:.6e} "
      f"(predicted 3u/8 = {3 * 1e-8 / 8:.6e})",
      abs(cs2_num(1e-8) - 0.5) < 1e-8
      and abs((cs2_num(1e-8) - 0.5) - 3 * 1e-8 / 8) < 1e-12,
      "|c_s^2(1e-8) - 1/2| < 1e-8 and the deviation equals 3u/8 to 1e-12")

# =============================================================== PART 3
print("\n" + "=" * 78)
print("PART 3 -- THE COUNTEREXAMPLE FAMILY:  EVERY n > 0 IS HEALTHY")
print("=" * 78)

# mu_n(u) = 1 - (1+u)^(-n): mu(0)=0, mu(inf)=1, deep slope n
mu_n = 1 - 1 / (1 + u) ** n
fp_n = mu_n
fpp_n = sp.simplify(sp.diff(mu_n, u) / (2 * u))
cs2_n = sp.simplify(fp_n / (fp_n + 2 * u ** 2 * fpp_n))
slope_n = sp.limit(mu_n / u, u, 0, '+')

print(f"      mu_n(u) = 1 - (1+u)^-n    deep slope = {slope_n}")
for nn in [1, 2, 3]:
    e = sp.simplify(cs2_n.subs(n, nn))
    print(f"        n = {nn} : c_s^2 = {sp.factor(sp.simplify(e))}")
    print(f"               c_s^2(0) = {sp.limit(e, u, 0, '+')}, "
          f"c_s^2(inf) = {sp.limit(e, u, sp.oo)}")

grid_e = [10.0 ** ee for ee in range(-8, 7)]      # 1e-8 .. 1e6
for nn in (1, 2, 3):
    e = sp.simplify(cs2_n.subs(n, nn))
    vals = [float(e.subs(u, x)) for x in grid_e]
    mpos = min(float(fp_n.subs(n, nn).subs(u, x)) for x in grid_e)
    mder = min(float(fpp_n.subs(n, nn).subs(u, x)) for x in grid_e)
    check(f"E{nn} [HEALTHY AT n = {nn}] mu>0, mu'>0 and "
          f"c_s^2 in [1/2, 1) on u in [1e-8, 1e6]",
          f"min mu = {mpos:.6e}, min f'' = {mder:.6e}, "
          f"c_s^2 in [{min(vals):.12f}, {max(vals):.12f}]",
          mpos > 0 and mder > 0 and min(vals) >= 0.5 - 1e-12
          and max(vals) <= 1.0 and max(vals) > 0.5,
          "min mu > 0, min f'' > 0, 1/2 <= min c_s^2 and max c_s^2 <= 1")

check("E4 [THE NEGATIVE RESULT] three DIFFERENT deep slopes (1, 2, 3) are "
      "all realised by strictly positive, strictly monotone kernels with "
      "0 <= c_s^2 <= 1 -- so (i)+(ii)+(iii)+(iv) do NOT select n = 2",
      f"healthy slopes found: "
      f"{[str(sp.limit(mu_n.subs(n, nn) / u, u, 0, '+')) for nn in (1, 2, 3)]}",
      all(sp.limit(mu_n.subs(n, nn) / u, u, 0, '+') == nn
          for nn in (1, 2, 3)),
      "deep slopes are exactly 1, 2, 3 (each finite and non-zero)",
      "THE ANSWER TO THE LANE QUESTION IS NO.  Health is a condition on the\n"
      "         log-slope of mu; n is its amplitude.  No health condition\n"
      "         can see the amplitude, and Part 3 exhibits healthy members at\n"
      "         three different amplitudes.")

# symbolic proof that health holds for EVERY n > 0 in this family
gap = sp.simplify(1 - cs2_n)
gap_claim = n * u / (u * (1 + u) ** n + (1 + u) ** n - u - 1 + n * u)
check("E5 [FOR ALL n] in this family 1 - c_s^2 = "
      "n u / (u(1+u)^n + (1+u)^n - u - 1 + n u); for n >= 1 every term of "
      "the denominator is >= 0 and the first is > 0, so c_s^2 < 1 -- "
      "health holds for every n, not just 1, 2, 3",
      f"1 - c_s^2 = {gap}",
      sp.simplify(gap - gap_claim) == 0,
      "symbolic identity holds",
      "Subluminality is satisfied identically in n. n is a FREE parameter.")

# =============================================================== PART 4
print("\n" + "=" * 78)
print("PART 4 -- A SECOND DEGENERACY:  HEALTH DOES NOT EVEN FIX THE SHAPE AT n = 2")
print("=" * 78)

alt2 = n * u / (1 + n * u)                    # another family, deep slope n
cs2_alt = sp.simplify(alt2.subs(n, 2) / (alt2.subs(n, 2)
                                          + 2 * u ** 2 * sp.simplify(
    sp.diff(alt2.subs(n, 2), u) / (2 * u))))
print(f"      alternative n = 2 kernel:  mu(u) = 2u/(1+2u),  "
      f"c_s^2 = {sp.simplify(cs2_alt)}")
print(f"      programme  n = 2 kernel:  mu(u) = u(2+u)/(1+u)^2, "
      f"c_s^2 = {cs2_target}")
diff_grid = max(abs(float(cs2_alt.subs(u, x)) - cs2_num(x)) for x in grid)
check("F1 [SHAPE DEGENERACY] two DIFFERENT kernels, both with deep slope 2, "
      "both healthy, with different c_s^2(u)",
      f"max |c_s^2_alt - c_s^2_prog| over grid = {diff_grid:.6f}",
      diff_grid > 1e-3,
      "max difference > 1e-3 (they are genuinely different functions)",
      "So even granting n = 2, health leaves the functional form free.\n"
      "         Health fixes neither the slope nor the shape.")

# =============================================================== PART 5
print("\n" + "=" * 78)
print("PART 5 -- THE SHARP BOUND:  HEALTH GIVES n <= 2 IN THE MINIMAL PADE FAMILY")
print("=" * 78)

# mu = u(a+u)/(1+u)^2 : forced by mu(0)=0, mu(inf)=1, minimal double pole
mu_a = u * (a + u) / (1 + u) ** 2
fp_a = mu_a
fpp_a = sp.simplify(sp.diff(mu_a, u) / (2 * u))
cs2_a = sp.simplify(fp_a / (fp_a + 2 * u ** 2 * fpp_a))
one_minus = sp.simplify(1 - cs2_a)
print(f"      mu_a = u(a+u)/(1+u)^2 ,  c_s^2 = {cs2_a}")
print(f"      1 - c_s^2 = {one_minus}")
print(f"      deep slope = {sp.limit(mu_a / u, u, 0, '+')}")

rows = []
for av in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]:
    vals = [float(cs2_a.subs(a, av).subs(u, x)) for x in
            [10.0 ** e for e in range(-4, 7)]]
    rows.append((av, min(vals), max(vals)))
    print(f"        a = {av:4.1f} : c_s^2 in "
          f"[{min(vals):.9f}, {max(vals):.9f}]"
          f"{'   <-- SUPERLUMINAL' if max(vals) > 1.0 else ''}")

sub_ok = all(mx <= 1.0 + 1e-12 for av, mn, mx in rows if av <= 2.0)
bad_ok = all(mx > 1.0 for av, mn, mx in rows if av > 2.0)
check("G1 [SHARP BOUND] in this family c_s^2 <= 1 for all u >= 0 iff a <= 2: "
      "a <= 2 is subluminal, every a > 2 goes superluminal at large u",
      "; ".join(f"a={av}: max c_s^2={mx:.6f}" for av, mn, mx in rows),
      sub_ok and bad_ok,
      "max c_s^2 <= 1 for a <= 2, and > 1 for every a > 2 tested",
      "n = 2 SATURATES the subluminality bound: it is the LARGEST healthy\n"
      "         deep slope in this family.  SCOPE, STATED: the family is put\n"
      "         in by hand (mu(0)=0, mu(inf)=1, minimal double pole at u=-1).\n"
      "         Health gives the BOUND a <= 2, not the equality a = 2.")

check("G2 [THE BOUND IS NOT A DERIVATION] a is only confined to "
      "0 <= a <= 2, so health leaves a = 1 and a = 1.66 as healthy as a = 2",
      f"healthy interval for the deep slope in this family: "
      f"[0, 2] (subluminality gives a<=2, positivity gives a>=0)",
      sub_ok and bad_ok,
      "the interval has more than one point",
      "To promote the BOUND into the VALUE 2 one needs an extra input --\n"
      "         integrality would give a in {1, 2}, still not unique.")

# =============================================================== PART 6
print("\n" + "=" * 78)
print("PART 6 -- WHAT DOES FIX THE 2:  REGULARITY + NO NEWTONIAN FLOOR")
print("=" * 78)

fs = K - c * sp.log(1 + sp.sqrt(K)) - d / (1 + sp.sqrt(K))
fps = sp.simplify(sp.diff(fs, K)).subs(sp.sqrt(K), u)
resid = sp.simplify(sp.expand(u * (fps - 1)))
print(f"      f'(u^2)  = {fps}")
print(f"      u (f'-1) = {resid}")

check("H1 [RESIDUE] u (f'(K) - 1) = (d - c - c u) / (2 (1+u)^2); "
      "finiteness of f' at K = 0 forces d = c",
      f"u(f'-1) - (d-c-cu)/(2(1+u)^2) = "
      f"{sp.simplify(resid - (d - c - c * u) / (2 * (1 + u) ** 2))}",
      sp.simplify(resid - (d - c - c * u) / (2 * (1 + u) ** 2)) == 0,
      "symbolic difference == 0",
      "The coefficient of ln(1+sqrt K) must equal the coefficient of\n"
      "         1/(1+sqrt K) or f' has a 1/sqrt(K) pole at the vacuum.")

fp_reg = sp.simplify(fps.subs(d, c))
print(f"      with d = c:  f'(K) = {sp.simplify(fp_reg)}")
mu_at_0 = sp.simplify(fp_reg.subs(u, 0))
slope_gen = sp.limit(fp_reg / u, u, 0, '+')
print(f"      mu(0) = {mu_at_0} ,  deep slope = {slope_gen}")

slope_c1 = sp.limit(fp_reg.subs(c, 1) / u, u, 0, '+')
slope_c3 = sp.limit(fp_reg.subs(c, 3) / u, u, 0, '+')
check("H2 [NO NEWTONIAN FLOOR] with d = c the deep slope is finite iff c = 2 "
      "(mu(0) = 1 - c/2 = 0); then the deep slope equals c = 2",
      f"mu(0) = {mu_at_0}; slope(c=2) = "
      f"{sp.limit(fp_reg.subs(c, 2) / u, u, 0, '+')}; "
      f"slope(c=1) = {slope_c1}; slope(c=3) = {slope_c3}",
      sp.simplify(mu_at_0 - (1 - c / 2)) == 0
      and sp.limit(fp_reg.subs(c, 2) / u, u, 0, '+') == 2
      and slope_c1 == sp.oo and slope_c3 == -sp.oo,
      "mu(0) = 1 - c/2; slope(c=2) = 2; slope(c=1) = +oo; slope(c=3) = -oo",
      "CHAIN: (alpha) regularity at K=0 => d = c;  (beta) mu(0)=0 (a MOND\n"
      "         REGIME, i.e. no Newtonian floor) => c = 2;  (gamma) the deep\n"
      "         slope is then c = 2.  This DOES fix the 2 -- but (alpha) is a\n"
      "         smoothness input and (beta) is a PHENOMENOLOGICAL input\n"
      "         (deep MOND exists).  Neither is a health condition, and the\n"
      "         family f = K - c ln(1+sqrt K) - d/(1+sqrt K) is assumed.")

check("H3 [OVER-DETERMINATION] the single integer 2 occupies five roles: "
      "the exponent in (1+u)^-2, the additive constant in u(2+u), the "
      "coefficient of ln(1+sqrt K), the coefficient of 1/(1+sqrt K), "
      "and the deep slope",
      f"at c=2: f' = 1 - 1/(1+u)^2 = u(2+u)/(1+u)^2, "
      f"slope = {sp.limit(fp_reg.subs(c, 2) / u, u, 0, '+')}, "
      f"ln-coefficient = c = 2, inverse-coefficient = d = c = 2, "
      f"difference from the kernel = "
      f"{sp.simplify(fp_reg.subs(c, 2) - (1 - 1 / (1 + u) ** 2))}",
      sp.simplify(fp_reg.subs(c, 2) - (1 - 1 / (1 + u) ** 2)) == 0,
      "1 - 1/(1+u)^2 == u(2+u)/(1+u)^2 at c = 2",
      "A consistency check on the framework, not an independent derivation:\n"
      "         the five appearances are forced equal once d = c is imposed,\n"
      "         so they do not independently confirm one another.")

# =============================================================== PART 7
print("\n" + "=" * 78)
print("PART 7 -- BOTH FOOTINGS:  WHAT n THE DATA ACTUALLY SUPPORTS")
print("=" * 78)

Lam_eV = Lam_meV * 1e-3
M_Pl_eV = M_Pl_GeV * 1e9
nsee = {}
for k, a0 in FOOT.items():
    a0_eV = a0 * HBAR / CLIGHT / EV_J
    nsee[k] = Lam_eV ** 2 / (a0_eV * M_Pl_eV)
    print(f"      a_0 ({k:11s}) = {a0:.6e} m/s^2 = {a0_eV:.6e} eV")
    print(f"        n = Lambda^2/(a_0 M_Pl) = {nsee[k]:.6f}")

check("I1 [BOTH FOOTINGS] the seesaw n = Lambda^2/(a_0 M_Pl) evaluated at "
      "BOTH footings 9.3619e-11 and 1.1279e-10",
      f"n(canonical 9.3619e-11) = {nsee['canonical']:.6f}; "
      f"n(alternative 1.1279e-10) = {nsee['alternative']:.6f}; "
      f"ratio of footings = "
      f"{FOOT['alternative'] / FOOT['canonical']:.6f}",
      all(1.0 <= v <= 3.0 for v in nsee.values()),
      "both inferred n lie in [1, 3]",
      "The two footings differ by 20.5%, so they infer n = 2.000 and\n"
      "         n = 1.660 respectively.  HEALTH ALLOWS BOTH (Part 3), so the\n"
      "         health conditions cannot adjudicate between the footings\n"
      "         either -- the integer is fixed, if at all, by the data.")

check("I2 [HEALTH IS INDIFFERENT TO THE FOOTINGS] both inferred values of n "
      "are admissible under (i)-(iv), since the healthy family of Part 3 "
      "covers every n > 0",
      f"n values {[round(v, 6) for v in nsee.values()]} all in (0, infinity)",
      all(v > 0 for v in nsee.values()),
      "every inferred n > 0",
      "The 20% footing split is a DATA question, not a health question.")

# =============================================================== VERDICT
print("\n" + "=" * 78)
print(f"H046 READING:  {NP_} PASS / {NF_} FAIL")
print("=" * 78)
print("""
VERDICT --  n = 2 IS **NOT** FORCED BY THE HEALTH CONDITIONS.

  WHY.  With K = u^2 and f'(K) = mu(u),

        c_s^2 = f'/(f' + 2K f'') = mu/(mu + u mu') = 1/(1 + dln mu/dln u).

  Health ((i) 0 <= c_s^2 <= 1, (ii) f' > 0, (iii) stability) is therefore
  EXACTLY the statement  mu > 0 and mu' >= 0 -- a condition on the LOG-SLOPE
  of mu.  The deep slope n is the AMPLITUDE of mu, and it cancels out of
  every health condition identically.  Condition (iv) (finite, non-zero deep
  slope) fixes the deep LOG-SLOPE to 1, and hence fixes

        c_s^2(0) = 1/2       for EVERY value of n,

  which is a real forced prediction -- and simultaneously the proof that the
  deep sound speed cannot discriminate n.  Part 3 exhibits a healthy kernel
  with deep slope n for every n > 0 (checked explicitly at n = 1, 2, 3);
  Part 4 shows health does not even fix the shape at fixed n = 2.

  WHAT IS GENUINELY FORCED (new, n-independent):
    * c_s^2 -> 1/2 at the deep end for any healthy k-essence with a linear
      MOND regime.  The programme's measured [1/2, 1) is a prediction.
    * Inside the minimal Pade family, subluminality gives the SHARP bound
      n <= 2 and the observed n = 2 saturates it (a > 2 is superluminal at
      large u).  This is a bound, not a derivation: the family is assumed.

  WHAT DOES FIX THE 2 (not health):
    Regularity of f' at K = 0 forces the two coefficients in
    f = K - c ln(1+sqrt K) - d/(1+sqrt K) to be equal (d = c); the absence of
    a Newtonian floor, mu(0) = 0, then forces c = 2; the deep slope equals c
    and is therefore 2.  Both inputs -- smoothness at the vacuum and the
    EXISTENCE of a MOND regime -- are outside (i)-(iv), and the family is
    assumed.  Reported as the honest positive result.

  WHAT THIS LANE DOES NOT DO:
    * It does not claim n = 2 is derived.  It proves (i)-(iv) insufficient.
    * It does not revisit H017/H030's dimensional route, which stands.
    * It does not adjudicate between the two a_0 footings (Part 7):
      they infer n = 2.000 and n = 1.660, and health permits both.
""")

json.dump({
    "lane": "H046",
    "pass": NP_, "fail": NF_, "results": RES,
    "verdict": "n = 2 is NOT forced by health conditions (i)-(iv)",
    "master_identity": "c_s^2 = mu/(mu + u mu') = 1/(1 + dln mu/dln u)",
    "forced": {"deep_cs2": 0.5,
               "sharp_bound_in_pade_family": "0 <= n <= 2, saturated at n = 2"},
    "not_forced": {"healthy_slopes_exhibited": [1, 2, 3],
                   "shape_degeneracy_at_n2": True},
    "what_fixes_two": "regularity at K=0 (d=c) + no Newtonian floor (c=2)",
    "footings": FOOT,
    "n_from_seesaw": nsee,
}, open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/"
        "H046_results.json", "w"), indent=2)
print(json.dumps({"pass": NP_, "fail": NF_}))
