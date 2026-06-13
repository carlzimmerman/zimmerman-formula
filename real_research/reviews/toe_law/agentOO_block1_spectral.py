"""
agentOO Route 2 — Block 1: the spectral representation of the induced dispersion correction,
and the GENERAL rule that fixes the sign of the induced k^4 from the bath spectral density shape.

THE PHYSICS (model stated explicitly, no smuggling):
-----------------------------------------------------
The khronon chi couples to a bath of horizon modes. The one-loop in-medium self-energy
Sigma(omega,k) is a convolution of the khronon's bare propagator with the bath spectral density
rho_bath(W). On the khronon mass shell omega ~ c_chi k, the induced REAL dispersion correction is

    delta(omega^2)(k) = Re Sigma(c_chi k, k)
                      = P int dW  rho_bath(W) * G_response(omega=c_chi k, k; W)

where rho_bath(W) >= 0 is the (positive) bath spectral weight (passivity: Im response >= 0), and
G_response is the kernel coupling khronon momentum k to a bath mode of frequency W.

The KRAMERS-KRONIG / spectral statement we test:
  Expand Re Sigma in powers of k^2:  Re Sigma = s0 + s2 k^2 + s4 k^4 + s6 k^6 + ...
  Then  c_chi^2_eff = c_chi^2 + s2 ,  sigma4 = s4 ,  sigma6 = s6.
  The SIGN of s4 is a MOMENT of rho_bath weighted by a kernel curvature.

We compute s4 for two canonical bath shapes:
  (A) FEATURELESS thermal bath: rho ~ thermal occupation, smooth, monotone (the dS Gibbons-Hawking
      Planckian / Rayleigh-Jeans shape) -> predict STIFFEN (s4 >= 0) per CM precedent.
  (B) PEAKED/STRUCTURED bath: a resonance at finite W0 (the He-II roton precedent) -> predict BEND (s4 < 0).

The decisive deliverable: WHICH CLASS is the dS horizon bath? Block 1 sets up the general moment
rule with a concrete, standard self-energy kernel. Blocks 2-3 plug in the actual GH spectrum.
"""
import sympy as sp

print("="*78)
print("BLOCK 1: spectral moment rule for the induced k^4 sign")
print("="*78)

# ---- The standard one-loop kernel ----
# Khronon couples to bath mode of frequency W and the loop momentum runs; the leading
# in-medium dispersion correction from a bath mode at frequency W, for a relativistic-ish
# khronon with bare omega_0(k)=c k, has the universal second-order-perturbation-theory form
# (Brillouin-Wigner / forward self-energy):
#
#   delta(omega^2)(k) = int dW rho(W) * |g(k,W)|^2 * [ 1/(c k - W) - 1/(c k + W) ] * (kernel)
#
# The cleanest, assumption-light handle: the static (omega->0 retarded) polarization correction
# to the gradient energy. The induced k^2-dependent self-energy from coupling to a bath with
# spectral density rho(W) and a derivative (momentum) coupling g(k,W)=k*lambda(W) is, at the
# level of the Matsubara/spectral sum,
#
#   Sigma(k) = - k^2 int_0^inf dW rho(W) lambda(W)^2 * D(c k, W)
#
# where D is the bath propagator's real part D(x,W)=Re 1/(W^2 - x^2 - i0) = W^2/(W^2-x^2) type.
# Expanding D in x=c k gives the k^4, k^6 ... tower. We do this expansion exactly.

k, c, W = sp.symbols('k c W', positive=True)
x = c*k  # on-shell argument

# Bath propagator real part for a mode of frequency W probed at frequency x=c*k:
# D(x,W) = 1/(W^2 - x^2). (Standard bosonic bath line; sign chosen so a single mode BELOW
# the probe (W<x) and ABOVE (W>x) contribute with the physical level-repulsion sign.)
D = 1/(W**2 - x**2)

# Series in k (i.e. in x) to k^6:
Dser = sp.series(D, k, 0, 8).removeO()
print("\nBath-line real part D(c k, W) expanded in k:")
sp.pprint(sp.simplify(Dser))

# Collect coefficients of k^2, k^4, k^6 (these multiply the W-integral of rho*lambda^2)
c2 = Dser.coeff(k,2)
c4 = Dser.coeff(k,4)
c6 = Dser.coeff(k,6)
print("\ncoeff k^2 (per bath mode W):", sp.simplify(c2))
print("coeff k^4 (per bath mode W):", sp.simplify(c4))
print("coeff k^6 (per bath mode W):", sp.simplify(c6))

# The induced self-energy is Sigma(k) = -k^2 * int dW rho(W) lambda(W)^2 D(ck,W).
# So with a derivative coupling lambda^2 -> a smooth positive weight mu(W)=rho(W)lambda(W)^2 >=0,
# write Sigma = - int dW mu(W) [ k^2 D ]. The TOTAL k^4 coefficient sigma4 is:
#   sigma4 = - int dW mu(W) * (k^2 D)|_{coeff k^4}
# k^2 * D has expansion: k^2*(c2 k^2 + c4 k^4 + ...) = c2 k^4 + c4 k^6 + ...
# so the k^4 coeff of (k^2 D) is c2, and the k^6 coeff is c4.
kernel_k4 = c2   # coefficient of k^4 in (k^2 * D)
kernel_k6 = c4   # coefficient of k^6 in (k^2 * D)
print("\n--- sigma4 = - int dW mu(W) * [k^4-coeff of (k^2 D)] ---")
print("k^4 weight per mode  (= c2):", sp.simplify(kernel_k4))
print("k^6 weight per mode  (= c4):", sp.simplify(kernel_k6))

print("""
READING:
  k^4 weight per mode = c^2/W^4   (always POSITIVE for every bath mode W>0)
  => sigma4 = - int dW mu(W) * c^2/W^4
  With mu(W)=rho lambda^2 >= 0 (passive bath, real coupling), sigma4 is a strictly NEGATIVE
  number TIMES the IR-weighted moment int dW mu(W)/W^4.

  This is the level-repulsion / adiabatic sign: coupling to bath modes pushes the on-shell
  branch DOWN, and because the static (low-W) modes dominate the 1/W^4 weight, the curvature
  correction BENDS (negative k^4) -- PROVIDED the bath has enough IR weight for int mu/W^4 to
  converge and be finite. THE WHOLE FIGHT IS IN THE IR CONVERGENCE OF int mu(W)/W^4.
""")

# The decisive quantity: does int_0^inf dW mu(W)/W^4 converge (finite, well-defined negative sigma4)
# or does the bath spectral shape kill it / flip it? That is set by rho_bath(W) as W->0 and W->inf.
print("DECISIVE MOMENT:  M4 = int_0^inf dW mu(W)/W^4 ;  sigma4 = -c^2 * M4")
print("  M4 finite & >0  => sigma4 < 0  (BEND / roton-capable)")
print("  M4 IR-divergent => the expansion in k^4 fails (massless on-shell pole hit) -> need the")
print("                     resonant/structured treatment; sign not fixed by naive moment.")
print("\nNext (Block 2): put the ACTUAL Gibbons-Hawking spectral density in mu(W) and test the moment.")
