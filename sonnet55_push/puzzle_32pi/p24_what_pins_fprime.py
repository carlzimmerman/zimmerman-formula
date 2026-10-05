"""p24: what pins f'(1) in BIMOND? Milgrom 2009 (arXiv:0912.0790v2) eqs (84)-(85): with g-hat = lambda g (cosmological C = 0),
   beta G + q a0^2 M(0) g = -8 pi G T,   alpha G + qhat a0^2 M(0) g = -8 pi G That,
   q = (lambda/2)[kappa f]'(kappa = 1/lambda),   qhat = -(lambda^-2/2)[kappa^-1 f]'(kappa = 1/lambda),   f(1) = 1.
Vacuum (T = That = 0) with M(0) != 0 needs q/beta = qhat/alpha (one Einstein tensor, two equations). Lambda = q a0^2 M(0)/beta (sign as in (84): G = -(q/beta) a0^2 M(0) g).
Tests: (1) the alpha + beta = 0 class (Milgrom's main theory, clean QUMOND limit eq 3) at lambda = 1; (2) a ghost-free (dRGT determinant-only) f = A kappa + B/kappa;
(3) the alpha = beta class with g <-> g-hat exchange symmetry f(kappa) = f(1/kappa).
Run: python3 p24_what_pins_fprime.py  |  MUTATE=1: drop the lambda^-2 in qhat (check 2 must fail)
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
k, lam, A, B, fp = sp.symbols("kappa lambda A B fp", real=True)
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
def qs(f, l):
    q = (l / 2) * sp.diff(k * f, k).subs(k, 1 / l)
    qh = -((1 if MUTATE else l**-2) / 2) * sp.diff(f / k, k).subs(k, 1 / l)
    return sp.simplify(q), sp.simplify(qh)

# (1) alpha + beta = 0 (beta = 1, alpha = -1), lambda = 1, general f with f(1) = 1, f'(1) = fp: local Taylor f = 1 + fp (kappa - 1)
f_loc = 1 + fp * (k - 1)
q1, qh1 = qs(f_loc, 1)
cond1 = sp.simplify(q1 / 1 - qh1 / (-1))
print(f"   (1) alpha+beta=0, lambda=1: q = {q1}, qhat = {qh1}; vacuum needs q/beta - qhat/alpha = {cond1} = 0")
check("1 in Milgrom's main class (alpha + beta = 0) a g-hat = g de Sitter vacuum is INCONSISTENT for every f'(1) (needs 1 = 0) unless M(0) = 0: nothing pinned; Lambda from M(0) needs lambda != 1 or twin matter",
      sp.simplify(cond1) != 0 and not sp.solve(sp.Eq(cond1, 0), fp))

# (2) ghost-free determinant-only potential: (g ghat)^(1/4) f = sqrt(g) kappa^-1 f must be a + b kappa^-2 (cosmological constants of g and g-hat) -> f = A kappa + B/kappa
fgf = A * k + B / k
q2, qh2 = qs(fgf, lam)
sol = sp.solve([sp.Eq(q2 / 1, qh2 / (-1)), sp.Eq(A + B, 1)], [A, B], dict=True)[0]
LamCoef = sp.simplify((-q2 / 1).subs(sol))          # Lambda = LamCoef * a0^2 M(0)
print(f"   (2) ghost-free f = A kappa + B/kappa: q = {q2}, qhat = {qh2}; vacuum + f(1) = 1 -> A = {sol[A]}, B = {sol[B]}; f'(1) = {sp.simplify((A - B).subs(sol))}; Lambda = {LamCoef} a0^2 M(0)")
check("2 ghost-freedom restricts f to A kappa + B/kappa, but the vacuum then fixes A, B only in terms of the free scale ratio lambda: f'(1) = (lambda+1)/(lambda-1), Lambda = -lambda/(lambda-1) a0^2 M(0)",
      sp.simplify((A - B).subs(sol) - (lam + 1) / (lam - 1)) == 0 and sp.simplify(LamCoef + lam / (lam - 1)) == 0)

# (3) alpha = beta = 1 with exchange symmetry f(kappa) = f(1/kappa)  ->  f'(1) = 0; vacuum at lambda = 1
fsym = (k + 1 / k) / 2                                  # simplest symmetric f with f(1) = 1 (Milgrom eq 86 with alpha = beta)
q3, qh3 = qs(fsym, 1)
print(f"   (3) alpha=beta=1, f(kappa) = f(1/kappa): f'(1) = {sp.diff(fsym, k).subs(k, 1)}; q = {q3}, qhat = {qh3}; vacuum consistent: {sp.simplify(q3 - qh3) == 0}; Lambda = {-q3} a0^2 M(0)")
check("3 exchange symmetry PINS f'(1) = 0 (any f with f(k) = f(1/k)), and the g-hat = g vacuum is then consistent with Lambda = -(1/2) a0^2 M(0)",
      sp.diff(fsym, k).subs(k, 1) == 0 and sp.simplify(q3 - qh3) == 0 and sp.simplify(q3 - sp.Rational(1, 2)) == 0)
print("   (3) caveat: the alpha = beta class does NOT have Milgrom's clean NR limit (eq 3 is alpha + beta = 0); its nu <-> M' map is not derived here.")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
