import sympy as sp

# ============================================================
# ZZ1 - Fourier-space anatomy of the spatial-nonlocal key's lapse response
# ============================================================
# The keying theorem (agentDD): the LOCAL key Y_a = a.a c^4/a0^2 with a_i = d_i ln N.
# Its lapse response delta-Y_a/delta-Phi puts a SPATIAL DERIVATIVE on the test function,
# IBP -> unsuppressed geometric piece ~ slip/r^2 = (a0 r/c^2)^-1 x phantom.
#
# A SPATIAL-nonlocal key reads the SMOOTHED field. Two natural realizations:
#   (i) smooth the POTENTIAL:  Phi_L = K_L * Phi,  K_L = Yukawa/Gaussian range L
#       (the resolvent 1/(1 - L^2 nabla^2) acting on Phi).
#   (ii) the key is built from the smoothed acceleration a_L = grad(K_L * ln N).
#
# In Fourier space the convolution is a multiplier.  Local key a_i = i k_i Phi(k);
# smoothed key a_L = i k_i Phi(k) * Khat(k),  Khat(k) = 1/(1 + L^2 k^2)  (resolvent form).
#
# THE TEST. The keying pollution is the lapse response of the key entering eqN.  In Fourier
# space the LOCAL key's lapse response at the constraint is the IBP-enhanced piece ~ k^2 Phi
# (two derivatives on the potential -> the geometric slip/r^2).  The smoothed key replaces
# every factor that carried a spatial derivative of the lapse by k_i * Khat(k).
#
# Decisive comparison:  at the HALO scale the relevant modes are k ~ 1/r_halo.  The kernel
# only suppresses modes with k >> 1/L.  So if L <~ r_halo, the kernel is ~1 at the halo scale
# and does NOT suppress.  If L >> r_halo, the kernel suppresses the halo modes too -> kills
# the slip (the lens) along with the pollution.

k, L, r = sp.symbols('k L r', positive=True)
Khat = 1/(1 + L**2 * k**2)          # resolvent kernel multiplier
print("Khat(k) =", Khat)
print("Khat(k->0)  (long wavelength, k<<1/L) =", sp.limit(Khat, k, 0))
print("Khat(k->oo) (short wavelength, k>>1/L) =", sp.limit(Khat, k, sp.oo))

# The local keying-pollution multiplier vs the smoothed one.  In the keying theorem the
# enhanced eqN feed scales as (the lapse response of the key).  The key is QUADRATIC in the
# acceleration (Y_a = a.a), so the lapse RESPONSE delta-Y_a/delta-Phi is LINEAR in a-bar times
# delta-a.  In Fourier: a-bar(k1) * [i k2 * (kernel)].  The enhancement that made (a0 r/c^2)^-1
# was the SECOND spatial derivative landing geometrically after IBP.
#
# Build the ratio   (smoothed enhanced feed)/(local enhanced feed)  mode by mode.
# Local enhanced feed multiplier ~ k^2 (the slip/r^2 geometric piece).
# Smoothed: the derivative that produced the enhancement now carries Khat -> k^2 * Khat.
ratio = (k**2 * Khat) / (k**2)
ratio = sp.simplify(ratio)
print("\nPer-mode suppression of the keying pollution = Khat(k) =", ratio)

# Numeric: halo scale r ~ 30 kpc -> k_halo; the kernel range L for the lens job.
# The slip (lens) lives at the SAME k as the pollution -- they are the SAME spatial structure
# (the wall-4 identity: r^0-class = alpha^6 (slip/Phi')).  So the suppression of the pollution
# at mode k EQUALS the suppression of the SLIP at mode k.  Quantify the locked ratio.
print("\n--- The locked ratio (pre-registered hostile point, now made exact) ---")
for Lk in [sp.Rational(1,10), sp.Rational(1,2), sp.Integer(1), sp.Integer(3), sp.Integer(10)]:
    # express suppression as function of dimensionless x = L*k
    x = sp.symbols('x', positive=True)
    supp = (1/(1+x**2)).subs(x, Lk)  # at L*k = Lk
    print(f"  L*k = {Lk}:  pollution suppression Khat = {float(supp):.4f}")
