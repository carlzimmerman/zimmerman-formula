"""
MECHANISM 5 — ZETA-FUNCTION CASIMIR ENERGY on S^3 (the dS horizon 3-sphere).

GOAL: compute the EXACT zeta-regularized vacuum (Casimir) energy
   E = (1/2) sum_n omega_n
for (i) a CONFORMALLY-COUPLED scalar and (ii) a MINIMALLY-coupled scalar / the
K(Q) ghost-condensate mode, on the round S^3 of radius R (the round dS horizon).

S^3 scalar Laplacian:  -Delta phi = l(l+2)/R^2 phi,  degeneracy d_l = (l+1)^2,
l = 0,1,2,...

  Conformal scalar (xi = 1/8 in 3D, mass term = R_scalar/8 = (6/R^2)/8... actually
  the conformal frequency on S^3 is omega_l = (l+1)/R  [eigenvalues (l+1)^2/R^2]):
        omega_l^2 = [ l(l+2) + 1 ] / R^2 = (l+1)^2 / R^2  =>  omega_l = (l+1)/R
  Minimal scalar:
        omega_l^2 = l(l+2)/R^2  =>  omega_l = sqrt(l(l+2))/R

  E = (1/2) sum_{l>=0} d_l omega_l ,  zeta-regularized.

We regularize E(s) = (1/2) sum_l d_l omega_l^{-s} R^{-1}... i.e. define the spectral
zeta and analytically continue to the physical point. Standard convention: the
Casimir energy is  E = (1/2) mu^{2s} sum d_l omega_l^{1-2s}|_{s->0}, equivalently
the value of the "energy zeta" zeta_E(s)=sum d_l omega_l^{-s} continued to s=-1,
times 1/2.

We get the EXACT number and then run the TWO GATES.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
print("="*80)
print("MECHANISM 5: zeta-regularized Casimir energy on the round S^3 (dS horizon)")
print("="*80)

# ----------------------------------------------------------------------------
# (i) CONFORMAL SCALAR: omega_l = (l+1)/R, d_l = (l+1)^2.
#     E_conf = (1/2R) sum_{l>=0} (l+1)^2 (l+1) = (1/2R) sum_{l>=0}(l+1)^3
#            = (1/2R) sum_{m>=1} m^3  = (1/2R) zeta(-3).
#     zeta(-3) = 1/120  (exact).
# ----------------------------------------------------------------------------
print("\n--- (i) CONFORMAL scalar: omega_l=(l+1)/R, d_l=(l+1)^2 ---")
m = sp.symbols('m', positive=True, integer=True)
# energy zeta: sum_{l>=0} d_l omega_l^{-s} = sum_{m>=1} m^2 * m^{-s} = zeta(s-2)
# E = (1/2) zeta_E(s=-1)/R = (1/2) zeta(-1-2) /R = (1/2) zeta(-3)/R
z_m3 = sp.zeta(-3)
print("  zeta_E(s) = sum_{m>=1} m^2 * (m/R)^{-s} ; continue to s=-1 (the energy sum (1/2)sum d_l omega_l)")
print("  => E_conf = (1/(2R)) sum_{m>=1} m^3 =reg= (1/(2R)) * zeta(-3)")
print("  zeta(-3) =", z_m3, "=", sp.nsimplify(z_m3), "=", float(z_m3))
E_conf_coeff = sp.Rational(1,2)*z_m3
print("  => E_conf * R =", E_conf_coeff, "=", float(E_conf_coeff), "   (i.e. E_conf = %s / R)" % E_conf_coeff)

# ----------------------------------------------------------------------------
# (ii) MINIMAL scalar: omega_l = sqrt(l(l+2))/R = sqrt((l+1)^2 - 1)/R, d_l=(l+1)^2.
#      Let n = l+1 >= 1.  omega = sqrt(n^2 - 1)/R, degeneracy n^2.
#      E_min = (1/2R) sum_{n>=1} n^2 sqrt(n^2 - 1).
#      Need zeta_E(s) = sum_{n>=1} n^2 (n^2-1)^{-s/2}, continued to s=-1:
#         zeta_E(-1) = sum_{n>=1} n^2 (n^2-1)^{1/2}.
#      Expand (n^2-1)^{1/2} = n (1 - 1/n^2)^{1/2} = n sum_k C(1/2,k)(-1)^k n^{-2k}
#      => n^2*sqrt(n^2-1) = sum_k C(1/2,k)(-1)^k n^{3-2k}
#      => zeta_E(-1) =reg= sum_k C(1/2,k)(-1)^k zeta(2k-3).
#      Only finitely many zeta(neg even)=0; the surviving terms are k=0,1,2 (zeta(-3),
#      zeta(-1), zeta(1)-pole) plus zeta(2k-3) for k>=... Let's do it exactly + check
#      against the literature (Elizalde/Bordag) and a direct numerical Abel-Plana / cutoff.
# ----------------------------------------------------------------------------
print("\n--- (ii) MINIMAL scalar: omega_l=sqrt(l(l+2))/R=sqrt(n^2-1)/R, n=l+1, d=n^2 ---")
print("  E_min = (1/2R) sum_{n>=1} n^2 sqrt(n^2-1) ; regularize the asymptotic series.")

# Binomial expansion of n^2 sqrt(n^2-1) in powers of n:
k = sp.symbols('k', nonnegative=True, integer=True)
n = sp.symbols('n', positive=True)
# (n^2-1)^{1/2} = n*(1-1/n^2)^{1/2}
binom_terms = []
print("\n  Binomial: n^2*sqrt(n^2-1) = sum_k binom(1/2,k)(-1)^k n^{3-2k}")
for kk in range(0, 7):
    coeff = sp.binomial(sp.Rational(1,2), kk)*(-1)**kk
    power = 3 - 2*kk      # exponent of n
    # zeta of (-(power)) = zeta(2k-3); contributes coeff * zeta(-power)
    zarg = -power         # = 2k-3
    binom_terms.append((kk, coeff, power, zarg))
    print("    k=%d: coeff=%s, n^%d -> zeta(%d)" % (kk, coeff, power, zarg))

# zeta-regularized sum: sum_n n^{power} =reg= zeta(-power) = zeta(2k-3)
# k=0: zeta(-3)=1/120 ; k=1: -1/2*zeta(-1) ; k=2: -1/8*zeta(1) POLE!
# The k=2 term has zeta(1) (harmonic) -> a genuine log divergence / pole.
print("\n  Regularized term-by-term (sum_n n^p =reg= zeta(-p)):")
E_min_reg = sp.Integer(0)
pole = None
for (kk, coeff, power, zarg) in binom_terms:
    if zarg == 1:
        pole = (kk, coeff)
        print("    k=%d: coeff=%s * zeta(1)  <-- POLE (log divergence) coeff = %s" % (kk, coeff, coeff))
        continue
    term = coeff*sp.zeta(zarg)
    E_min_reg += term
    print("    k=%d: %s * zeta(%d) = %s" % (kk, coeff, zarg, sp.nsimplify(term)))
E_min_reg = sp.nsimplify(E_min_reg)
print("  Finite part (excluding the zeta(1) pole) sum =", E_min_reg, "=", float(E_min_reg))
print("  => E_min*R (finite part) = (1/2)*[finite] =", sp.Rational(1,2)*E_min_reg, "=", float(sp.Rational(1,2)*E_min_reg))
if pole is not None:
    print("  NOTE: minimal scalar has a zeta(1) POLE (k=2 term, coeff=%s) -> the bare" % pole[1])
    print("        Casimir energy is NOT finite without a counterterm; the finite part is")
    print("        SCHEME-DEPENDENT (depends on the renormalization scale mu). The conformal")
    print("        scalar (i) is the clean, scheme-independent one.")

print("\n" + "="*80)
print("THE NUMBERS (exact):")
print("="*80)
print("  Conformal scalar:  E_conf = (1/2) zeta(-3) / R = (1/240) / R   [zeta(-3)=1/120]")
print("    => coefficient = 1/240 = %s" % float(sp.Rational(1,240)))
print("  Minimal scalar:    has a zeta(1) pole -> scheme-dependent finite part (NOT clean)")
print("  Neither equals 1/2.")
