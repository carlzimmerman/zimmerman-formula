"""
agentOO Route 2 — Block 2: HOSTILE sign audit of the moment rule, and the ACTUAL Gibbons-Hawking
spectral density inserted.

Block 1 baked in a level-repulsion sign via D=1/(W^2-x^2). A hostile verifier will say: "you
CHOSE the bend." So here we DERIVE the sign from the genuine Kramers-Kronig / spectral structure
with NO pre-chosen sign, and then test convergence with the REAL dS spectrum.

THE PROPER SPECTRAL REPRESENTATION (no sign smuggled):
------------------------------------------------------
The retarded self-energy is analytic in the upper-half omega plane and obeys

    Re Sigma(omega,k) = (1/pi) P int dW  Im Sigma(W,k) / (W - omega)

Im Sigma(W,k) is the bath ABSORPTION at frequency W and momentum k. For a PASSIVE bath
Im Sigma(W,k) >= 0 for W>0 (X2's passivity sign). The on-shell correction is
Re Sigma(c k, k), and its k-dependence comes through BOTH the momentum dependence of
Im Sigma(W,k) AND the on-shell argument omega=c k.

The momentum dependence: a DERIVATIVE (gradient) coupling gives Im Sigma(W,k) = k^2 * a(W) at
leading order in k (a(W)>=0 a positive spectral function). Then:

    Re Sigma(c k,k) = (k^2/pi) P int_0^inf dW a(W) [ 1/(W - c k) - 1/(W + c k) ]
                    = (k^2/pi) P int_0^inf dW a(W) * 2 c k /(W^2 - c^2 k^2)        (odd part)

Wait -- 1/(W-ck) - 1/(W+ck) = 2ck/(W^2-c^2k^2). That is ODD in k, giving k^3 not k^2.
The EVEN-in-k piece (the real dispersion sigma_n k^{2n}) comes from the symmetric combination
1/(W-ck) + 1/(W+ck) = 2W/(W^2-c^2k^2). Physically: the dispersion correction (even in k, since
omega^2 is even) is the PRINCIPAL-VALUE symmetric response

    delta(omega^2)(k) = (k^2/pi) P int_0^inf dW a(W) * 2W/(W^2 - c^2 k^2)
                      = (2 k^2/pi) int_0^inf dW a(W) * W/(W^2 - c^2 k^2)

NOW THE SIGN IS NOT CHOSEN -- it is FORCED by a(W)>=0 and the analytic structure. Expand in k:
"""
import sympy as sp

print("="*78)
print("BLOCK 2: hostile sign audit via genuine Kramers-Kronig (no sign pre-chosen)")
print("="*78)

k, c, W = sp.symbols('k c W', positive=True)
x = c*k

# symmetric KK kernel for the even-in-k dispersion correction
Ksym = 2*W/(W**2 - x**2)
Kser = sp.series(Ksym, k, 0, 8).removeO()
print("\nSymmetric KK kernel  2W/(W^2 - c^2 k^2)  expanded in k:")
sp.pprint(sp.simplify(Kser))

# delta(omega^2) = (k^2/pi) int dW a(W) * Ksym  -> multiply expansion by k^2
full = sp.expand(k**2 * Kser)
print("\nk^2 * kernel (the integrand's k-structure, coefficients multiply int dW a(W) W^{-...}):")
sp.pprint(sp.simplify(full))

s2_w = full.coeff(k,4)/1  # WAIT: careful. Let me extract by powers of k directly.
# full = (k^2)*(b0 + b2 k^2 + b4 k^4 + ...) where b0=coeff k^0 of Kser etc.
b0 = Kser.coeff(k,0)
b2 = Kser.coeff(k,2)
b4 = Kser.coeff(k,4)
print("\nKernel coefficients (per bath mode W), Ksym = b0 + b2 k^2 + b4 k^4:")
print("  b0 (->k^2 term, renormalizes c^2):", sp.simplify(b0))
print("  b2 (->k^4 term, = sigma4 weight) :", sp.simplify(b2))
print("  b4 (->k^6 term, = sigma6 weight) :", sp.simplify(b4))

print("""
DECISIVE READING (sign NOT chosen -- forced by a(W)>=0):
  delta(omega^2) = (1/pi)[ k^2 int a(W) b0 dW  +  k^4 int a(W) b2 dW  +  k^6 int a(W) b4 dW + ...]
  with
     b0 = 2/W          (so the k^2 renormalization int a/W  > 0  : speeds up / convex baseline)
     b2 = 2 c^2 / W^3   > 0  for every mode  => sigma4 = +(c^2/pi) int a(W) * 2/W^3 dW  > 0
     b4 = 2 c^4 / W^5   > 0                  => sigma6 = +(c^4/pi) int a(W) * 2/W^5 dW  > 0
""")
print("b0 =", sp.simplify(b0), " b2 =", sp.simplify(b2), " b4 =", sp.simplify(b4))
print("""
*** THE SIGN FLIPPED vs Block 1. ***
Block 1's D=1/(W^2-x^2) gave a NEGATIVE k^4 (bend). The genuine even-in-k Kramers-Kronig
representation with a PASSIVE spectral function a(W)>=0 gives a STRICTLY POSITIVE k^4 (stiffen).

The difference is the physical content of the bath line. The honest, passivity-respecting object
is the SYMMETRIC KK response 2W/(W^2-x^2): every passive bath mode at frequency W, probed
on-shell BELOW it (W > c k in the convergent regime), pushes the dispersion UP (level repulsion
from ABOVE = stiffen). A bend requires bath weight BELOW the on-shell branch (W < c k), i.e. a
peaked/resonant a(W) with most of its weight at LOW frequency relative to the probe -- the He-II
roton structure. A FEATURELESS thermal bath whose weight extends to high W stiffens.

So: the sign is set by WHERE the spectral weight a(W) sits relative to the on-shell frequency
c k. This is exactly the CM dichotomy the task named. Block 3: where does the GH spectrum sit?
""")
