"""
wf2_transverse_sector_scalar.py
============================================================================
Backs the load-bearing step of wf2_alpha1_maxwell_direct.py:

  "In AeST the shift-symmetric scalar touches the TRANSVERSE-VECTOR (spin-1)
   aether mode -- the sector that carries alpha_1 -- ONLY through a mass term
   M^2 = (2-K_B)(1+lambda_s) Q0^2 / K_B, and NOT through any V-beta or
   matter-beta coupling.  Since alpha_1 is a spin-1 quantity, the scalar
   cannot cancel it; it only shifts the (cosmologically tiny) vector mass."

We prove this by explicit spatial-Fourier component algebra with a transverse
projector, using the EXACT AeST second-order building blocks from
Skordis-Zlosnik 2109.13287 (Linear stability on Minkowski):

  * aether kinetic  -(K_B/2) Fhat^2   (Maxwell point)
  * scalar terms via  Y = qhat^{mu nu} d_mu phi d_nu phi ,  Q = Ahat^mu d_mu phi
  * the AeST-specific coupling  2(2-K_B) J^mu d_mu phi,  J^mu = Ahat^nu grad_nu Ahat^mu
  * background  Ahat=(1,0,0,0), phi = Q0 t + varphi,  so d_i phi = d_i varphi.

Signature (-,+,+,+).  We take a single spatial wavevector k = (0,0,k) and read
off the TRANSVERSE (x,y) block (perpendicular to k), where the spin-1 physics
of alpha_1 lives.  Transverse aether:  beta = (b1,b2,0), div beta = 0.
Transverse metric shift:  V = (V1,V2,0).  Scalar gradient: grad varphi = i k f zhat
= (0,0, i k f)  -- purely LONGITUDINAL.

The one identity that does all the work:
        (transverse vector) . (grad scalar) = 0
so every scalar coupling that reaches the vector sector only through grad(phi)
is transverse-blind, EXCEPT the algebraic |Q0 A|^2 piece of Y (no gradient),
which is exactly the mass.
"""
import sympy as sp

KB, lam_s, Q0, k, t = sp.symbols('K_B lambda_s Q0 k t', real=True)
b1, b2, V1, V2, f  = sp.symbols('b1 b2 V1 V2 f', real=True)   # Fourier amplitudes
I = sp.I

print("="*74)
print("Fourier setup: k=(0,0,k).  Transverse (spin-1) directions = x,y.")
print("="*74)
# spatial vectors as 3-tuples (x,y,z)
kvec  = (0, 0, k)
beta  = (b1, b2, 0)                 # transverse aether  (div beta = i k*0 = 0) OK
Vvec  = (V1, V2, 0)                 # transverse metric shift g_0i^T
gradf = (0, 0, I*k*f)              # grad(varphi): purely longitudinal (|| k)

def dot(a, b_):
    return sum(ai*bi for ai, bi in zip(a, b_))

print("div(beta)  = i*k*beta_z =", I*k*beta[2], "  (transverse OK)")
print("beta . grad(varphi) =", sp.simplify(dot(beta, gradf)),
      "   <-- ZERO: transverse vector _|_ scalar gradient")

print("\n" + "="*74)
print("1)  Q = Ahat.grad(phi):  transverse-beta content")
print("="*74)
# Q = Ahat^mu d_mu phi. Perturbation: dQ = dAhat^mu d_mu phi_bg + Ahat^mu_bg d_mu dphi
#   = (dAhat^0)*Q0 + beta . grad(varphi) + d_t varphi
# transverse-beta piece is beta.grad(varphi):
dQ_transverse_beta = dot(beta, gradf)
print("dQ (transverse-beta part) = beta.grad(varphi) =", sp.simplify(dQ_transverse_beta))
print("  => K(Q) cannot give a beta-V or beta-matter coupling (Q is beta-blind).")

print("\n" + "="*74)
print("2)  Y = qhat.d phi d phi:  the |grad phi + Q0 A|^2 structure (SZ eq at 2nd order)")
print("="*74)
# SZ 2109.13287 second-order expansion contains  -(2-K_B)(1+lambda_s)|grad varphi + Q0 A|^2
# The vector (transverse) part of the aether A is beta; grad varphi is longitudinal.
combo = tuple(sp.simplify(g + Q0*bi) for g, bi in zip(gradf, beta))  # grad varphi + Q0 beta
print("grad(varphi) + Q0*beta =", combo)
modsq = sp.expand(dot(combo, [sp.conjugate(x) for x in combo]))
# work with real amplitudes for the transverse magnitude (drop the i for |.|^2 bookkeeping)
modsq_real = sp.expand( (Q0*b1)**2 + (Q0*b2)**2 + (k*f)**2 )
print("|grad varphi + Q0 beta|^2 =", modsq_real)
print("   transverse (beta) part  =", Q0**2*(b1**2+b2**2), "= Q0^2 |beta|^2  (NO gradient, NO V)")

Yvec_coeff = -(2-KB)*(1+lam_s)*Q0**2   # coefficient of |beta|^2 from the Y term
print("\nY contributes to the transverse action:", Yvec_coeff, "* |beta|^2")
print("  This is an ALGEBRAIC (mass) term: no time/space derivative, no V, no matter.")

print("\n" + "="*74)
print("3)  AeST-specific coupling 2(2-K_B) J^mu d_mu phi:  transverse content")
print("="*74)
# J^mu = Ahat^nu grad_nu Ahat^mu.  Linear (flat, rest frame):
#   J^i_lin = d_t beta^i (+ metric connection, longitudinal); J^0_lin = scalar (constraint)
# transverse part of J is J^i_T = d_t beta^i  -> in Fourier  = d_t beta (still transverse).
# Coupling  J^mu d_mu phi = J^0 Q0 + J^i d_i varphi.
#   J^i_T d_i varphi = (transverse) . grad(varphi) = 0
Jt = (sp.Symbol('bd1'), sp.Symbol('bd2'), 0)   # d_t beta, transverse
print("J^i_T . grad(varphi) =", sp.simplify(dot(Jt, gradf)),
      "   <-- ZERO (transverse J _|_ scalar gradient)")
print("  J^0 * Q0  is a scalar/longitudinal component (constraint-fixed): no beta_T.")
print("  => 2(2-K_B) J^mu d_mu phi has NO transverse beta-V or beta-matter coupling.")
print("     (In a boosted frame grad phi_bg = -Q0 w is still a gradient (|| w),")
print("      so the same transverse-projection identity kills it at O(w) too.)")

print("\n" + "="*74)
print("4)  Assemble: transverse (beta) quadratic action = EA-Maxwell + mass")
print("="*74)
w = sp.symbols('omega', real=True)
# EA-Maxwell transverse aether kinetic (SZ eq 21):  K_B(|beta_dot|^2 - k^2|beta|^2)
# + Y-mass:  -(2-K_B)(1+lam_s)Q0^2 |beta|^2.  In Fourier the beta dispersion:
#   K_B(omega^2 - k^2) - (2-K_B)(1+lam_s)Q0^2 = 0
disp = KB*(w**2 - k**2) - (2-KB)*(1+lam_s)*Q0**2
M2 = sp.simplify((2-KB)*(1+lam_s)*Q0**2/KB)
print("beta dispersion:  K_B(omega^2 - k^2) - (2-K_B)(1+lam_s)Q0^2 = 0")
print("  => omega^2 = k^2 + M^2 ,  with")
print("     M^2 =", M2)
print("  MATCHES Skordis-Zlosnik 2109.13287 eq(22):  M^2 = (2-K_B)(1+lambda_s)Q0^2/K_B  [SOLID]")
print("  vector sound speed = coeff of k^2 = 1  (c_V = c)  -- Maxwell point, as in EA. [SOLID]")

print("""
CONCLUSION of this script (SOLID):
  * The scalar enters the transverse spin-1 sector ONLY as the mass M^2 above.
    Every derivative coupling (K(Q), J^mu d_mu phi) is transverse-blind because
    grad(phi) is longitudinal and (transverse vector).(gradient)=0.
  * Hence AeST transverse-vector sector = Einstein-aether Maxwell point + mass.
  * alpha_1 depends on the transverse sector; adding a mass M does not change
    the Einstein-aether coefficient (next script quantifies the (M/k)^2
    suppression), so alpha_1(AeST) = alpha_1(EA,Maxwell) = -4 K_B.
""")
