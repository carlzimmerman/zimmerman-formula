"""
MECHANISM 5 VERIFY — independent cross-checks of the S^3 Casimir numbers.

(A) Conformal scalar E_conf*R = (1/2)zeta(-3) = 1/240.
    Cross-check zeta(-3)=1/120 two independent ways (functional eqn + mpmath),
    and confirm the well-known literature value (the S^3 conformal-scalar Casimir
    energy = 1/(240 R); e.g. Elizalde "Ten Physical Applications of Spectral Zeta
    Functions", and the Einstein-static-universe vacuum energy literature).

(B) Numerically reproduce (1/2)sum (l+1)^2 (l+1) = (1/2)sum_{m>=1} m^3 via an
    EXPONENTIAL cutoff e^{-eps*m} and extract the eps->0 finite part: the
    divergent pieces are pure poles in 1/eps, the finite part must be 1/2*(-1/120)...
    wait: cutoff of sum m^3 e^{-eps m} -> 6/eps^4 + ... + zeta(-3). Confirm the
    constant term = zeta(-3) = 1/120.

(C) Check the GATE-(a) question directly: is ANY of {conformal 1/240, minimal
    finite part, the Dirac/ghost variants} equal to 1/2?  And is 1/2 even the
    RIGHT KIND of object (a dimensionless energy COEFFICIENT vs kappa = an action
    NORMALIZATION)?
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 50

print("="*80)
print("(A) zeta(-3) two ways")
print("="*80)
# functional equation: zeta(-3) = -B_4/4 where B_4 = -1/30  => zeta(-3)=1/120
B4 = sp.bernoulli(4)
zeta_m3_fe = -B4/4
print("  via Bernoulli: zeta(-3) = -B_4/4 = -(%s)/4 = %s" % (B4, zeta_m3_fe))
print("  via mpmath:    zeta(-3) =", mp.zeta(-3))
assert sp.nsimplify(zeta_m3_fe) == sp.Rational(1,120)
print("  => E_conf*R = (1/2)*zeta(-3) = 1/240 =", float(sp.Rational(1,240)), " CONFIRMED")

print("\n" + "="*80)
print("(B) exponential-cutoff cross-check of sum_{m>=1} m^3 (conformal energy sum)")
print("="*80)
# sum_{m>=1} m^3 e^{-eps m}. Generating: sum m^3 x^m = x(1+4x+x^2)/(1-x)^4, x=e^{-eps}.
# As eps->0: 6/eps^4 - 1/120 + O(eps^2)?  Actually the Laurent constant term = zeta(-3).
eps = sp.symbols('eps', positive=True)
x = sp.exp(-eps)
S = x*(1+4*x+x**2)/(1-x)**4
ser = sp.series(S, eps, 0, 3).removeO()
print("  sum_{m>=1} m^3 e^{-eps m} = ", ser)
const_term = ser.subs(eps, 0) if not ser.has(1/eps) else None
# extract constant (eps^0) coefficient:
ser_poly = sp.series(S, eps, 0, 1).removeO()
const = sp.simplify(ser_poly - (ser_poly - sp.O(1)))  # messy; do it cleanly:
c0 = sp.limit(S - 6/eps**4, eps, 0)  # subtract leading; but there are 1/eps^2 too
# Cleaner: Laurent-expand and read eps^0
lau = sp.series(S, eps, 0, 1)
print("  Laurent series (to eps^0):", lau)
# The eps^0 coefficient:
coeff0 = lau.removeO().coeff(eps, 0)
print("  constant (eps^0) term =", coeff0, "  [expect zeta(-3)=1/120]")
print("  matches zeta(-3)? ", sp.nsimplify(coeff0) == sp.Rational(1,120))

print("\n" + "="*80)
print("(C) DIRAC / ghost-condensate variants on S^3, and the GATE-(a) table")
print("="*80)
# Dirac on S^3: eigenvalues +-(n+3/2)/R, mult (n+1)(n+2) EACH sign (Camporesi-Higuchi).
# Vacuum energy (1/2) sum |omega| over modes, fermion sign -1:
#   E_D = -(1/2) sum_{n>=0} 2*(n+1)(n+2)*(n+3/2)/R   (factor 2 for both signs)
#       = -(1/R) sum_{n>=0} (n+1)(n+2)(n+3/2).
# Let j=n+1>=1: (j)(j+1)(j+1/2) = j(j+1)(j+1/2). Expand & zeta-regularize.
print("  -- Dirac (massless) on S^3 --")
j = sp.symbols('j', positive=True, integer=True)
nn = sp.symbols('nn', nonnegative=True, integer=True)
expr = (nn+1)*(nn+2)*(nn+sp.Rational(3,2))   # in n
poly = sp.expand(expr.subs(nn, sp.Symbol('n')))
n = sp.Symbol('n')
poly = sp.Poly(sp.expand((n+1)*(n+2)*(n+sp.Rational(3,2))), n)
print("    summand (per sign) (n+1)(n+2)(n+3/2) =", poly.as_expr())
# sum_{n>=0} n^p =reg= zeta(-p, 0+1)? Use Hurwitz: sum_{n>=0}(n+a)^p... easier: shift
# Use sum_{n>=0} P(n) with sum n^p =reg= zeta(-p) but starting n=0 the n=0 term for p>0 is 0,
# for the constant term sum_{n>=0} 1 =reg= zeta(0)+1? Careful. Use Hurwitz zeta on shifted form.
# Write in terms of (n+3/2): not monomial. Just regularize each monomial n^p with
# sum_{n>=0} n^p =reg= zeta(-p) (the n=0 term contributes 0 for p>=1, and for p=0:
# sum_{n>=0} 1 =reg= 1+zeta(0) = 1 - 1/2 = 1/2). Handle p=0 specially.
coeffs = poly.all_coeffs()[::-1]  # c0 + c1 n + c2 n^2 + c3 n^3
E_D_persign = sp.Integer(0)
for p, c in enumerate(coeffs):
    if c == 0: continue
    if p == 0:
        reg = sp.Rational(1,2) + sp.zeta(0)  # sum_{n>=0}1 = 1 + zeta(0); zeta(0)=-1/2 => 1/2
        reg = 1 + sp.zeta(0)
    else:
        reg = sp.zeta(-p)  # sum_{n>=1} n^p ; n=0 adds 0
    E_D_persign += c*reg
    print("    n^%d coeff %s -> reg sum %s = %s" % (p, c, (1+sp.zeta(0)) if p==0 else sp.zeta(-p), sp.nsimplify(c*reg)))
E_D_persign = sp.nsimplify(E_D_persign)
# both signs: factor 2 in the count was per-sign multiplicity; |omega| same for both signs.
# E_D = -(1/2)*[sum over BOTH signs] = -(1/2)*2*E_D_persign... but E_D_persign already is
#       sum over n of mult*(n+3/2). The total mode energy sum over both signs = 2*E_D_persign.
#       Fermion vacuum E = -(1/2)*sum|omega| = -(1/2)*2*E_D_persign = -E_D_persign (times 1/R).
E_D = -E_D_persign
print("    Dirac vacuum E_D * R = -(reg sum) =", E_D, "=", float(E_D))

print("\n  -- GATE (a): does ANY S^3 vacuum-energy coefficient = 1/2? --")
table = {
  "conformal scalar":  sp.Rational(1,240),
  "minimal scalar (finite part, scheme-dep)": sp.nsimplify(sp.Rational(1,2)*(sp.Rational(1,20)
        - sp.zeta(3)/16 - 5*sp.zeta(5)/128 - 7*sp.zeta(7)/256 - 21*sp.zeta(9)/1024)),
  "Dirac (massless)":  E_D,
}
for name, val in table.items():
    isval = sp.nsimplify(val) == sp.Rational(1,2)
    print("    %-42s : E*R = %-22s ~ %+.6f   ==1/2? %s" % (name, val, float(val), isval))
print("\n  None equals 1/2. The conformal scalar (the clean, scheme-independent one) = 1/240.")
print("  (The string -1/12 comes from zeta(-1) on S^1; the S^3 analog is zeta(-3)=1/120,")
print("   and the energy carries an extra 1/2 -> 1/240, NOT 1/2.)")
