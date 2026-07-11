#!/usr/bin/env python3
"""
ADVERSARIAL RE-DERIVATION of the anisotropic-stress SLIP scaling.

The reviewed script (lane2_slip.py) modeled the MI stress as scalar-dressed
dust:  T_mn = rho_eff u_m u_n  with rho_eff = rho*D (a SCALAR).  The ONLY
anisotropy such a tensor has is the KINETIC piece u_i u_j ~ v^2  ->  ram
pressure rho v^2  ->  slip ~ (v/c)^2.  That is the standard post-Newtonian
rotating-dust slip.  It is correct AS FAR AS IT GOES.

But the ACTION is  S = -1/2 INT sqrt(-g) rho u^mu K(Box_u/a0^2) u_mu ,  and
Box_u u_mu = (u.nabla)^2 u_mu ~ -a_c^2 u_mu + jerk, so K's argument is
z = a_c^2/a0^2  (a_c = centripetal accel of the ORBITING matter = g_obs).
Varying the metric inside K generates  K'(z) * d(a_c^2)/dg^mn / a0^2 , and
  d(a_c^2)/dg^mn  contains the term  a_mu a_nu  (a_mu = 4-acceleration).
a_mu is SPATIAL, RADIAL, magnitude a_c.  This is the term the review DROPPED.

Question audited here:  what ORDER is that dropped anisotropic stress?
"""
import sympy as sp

print("="*72)
print("RE-DERIVATION: order of the K'-acceleration anisotropic stress")
print("="*72)

# ---- leading normalization: dust action reproduces T ~ rho c^2 u u --------
# S = -1/2 INT rho u.u  ->  (u.u=-1)  ->  T_mn = rho c^2 u_m u_n  (energy dens)
# So a dimensionless K-structure X multiplying the action appears in T as
#   T_mn ~ rho c^2 * X_mn .  Anchor everything to rho c^2.
print("\n[anchor] dust limit K->1 gives T_mn = rho c^2 u_m u_n  (T_00=rho c^2).")
print("         Hence any dimensionless tensor structure X in the action")
print("         appears in the stress as  rho c^2 * X  (energy-density level).")

# ---- the two anisotropic contributions, both as (dimensionless)*rho c^2 ----
eps, z = sp.symbols('epsilon z', positive=True)   # eps=v/c ; z=a_c^2/a0^2
# (A) kinetic/dust ram-pressure anisotropy  (what the review kept):
#     u_i u_j traceless ~ eps^2   ->   X_dust_aniso = O(eps^2)
X_dust = eps**2
# (B) K'-acceleration anisotropy (what the review dropped):
#     from K'(z)*a_i a_j/a0^2, with a_i a_j = a_c^2 n_i n_j, a_c^2/a0^2 = z:
#     X_Kp_aniso = K'(z) * z * (n_i n_j traceless), n_in_j az-averaged != 0.
K  = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
Kp = sp.diff(K, z)
X_Kp = sp.simplify(Kp*z)          # times an O(1) azimuthal-average tensor
print("\n[A] kinetic (dust) anisotropic stress   X_dust = eps^2        (KEPT by review)")
print(f"[B] K'-accel   anisotropic stress   X_Kp   = K'(z)*z * n_in_j (DROPPED by review)")

# evaluate X_Kp on the MOND window z ~ O(1):
print("\n   z (=a_c^2/a0^2)   K'(z)      K'(z)*z   [the O(1) anisotropic amplitude]")
for zz in [sp.Rational(1,4), sp.Rational(1,2), 1, 2, 4]:
    print(f"     {float(zz):5.2f}         {float(Kp.subs(z,zz)):7.4f}   {float(X_Kp.subs(z,zz)):7.4f}")

print("\n   => X_Kp is O(0.1-1) across the whole MOND window.  NOT eps^2-small.")

# ---- azimuthal average of the radial anisotropy over a disk --------------
print("\n[azimuthal average] radial n_i n_j over a disk does NOT vanish:")
phi = sp.symbols('phi')
n = sp.Matrix([sp.cos(phi), sp.sin(phi), 0])
avg = sp.Matrix(3,3, lambda i,j: sp.integrate(n[i]*n[j], (phi,0,2*sp.pi))/(2*sp.pi))
tracefree = sp.simplify(avg - sp.trace(avg)/3*sp.eye(3))
print(f"   <n_i n_j> = diag({[float(avg[k,k]) for k in range(3)]})")
print(f"   traceless part = diag({[float(tracefree[k,k]) for k in range(3)]})  != 0")
print("   => a real O(1) quadrupolar (in-plane vs vertical) anisotropic stress.")

# ---- the decisive ratio: dropped / kept -----------------------------------
print("\n"+"="*72)
print("DECISIVE RATIO  (dropped K'-stress) / (kept dust-stress)")
print("="*72)
c_val = 2.998e8; v_val = 150e3
epsv = v_val/c_val
for zz in [0.25, 1.0]:
    Xkp = float(X_Kp.subs(z, zz))
    ratio = Xkp/epsv**2
    print(f"   z={zz:4.2f}:  X_Kp/X_dust = {Xkp:.3f}/{epsv**2:.2e} = {ratio:.2e}  (~ c^2/v^2)")
print(f"\n   The DROPPED term is ~ c^2/v^2 ~ {1/epsv**2:.1e} times LARGER than the")
print("   kept term -- i.e. exactly the ~1e6 factor the review said was missing.")
print("   The review's '(v/c)^2 suppression, closed by 6 orders' is an ARTIFACT")
print("   of setting T_mn = rho_eff u_m u_n (scalar dust) and dropping K'*a_i a_j.")

# ---- footing check: does a0 footing change the O(1) amplitude? -------------
print("\n[footing] z = a_c^2/a0^2 = (g_obs/a0)^2.  Swapping a0 9.36e-11<->1.13e-10")
for a0v in [9.36e-11, 1.13e-10]:
    g_obs = 1.2e-10   # representative flat-curve accel ~ a0
    zz = (g_obs/a0v)**2
    print(f"   a0={a0v:.2e}: z={zz:.3f}, X_Kp={float(X_Kp.subs(z,zz)):.3f}  (still O(1), NOT eps^2)")

print("\n"+"="*72)
print("VERDICT ON THE REVIEW: the SLIP-CLOSED conclusion is NOT established.")
print("="*72)
print("""
  The load-bearing scaling (Psi-Phi)/Phi = 2 D (v/c)^2 uses ONLY the kinetic
  dust anisotropy.  The K'-acceleration anisotropic stress -- the term the
  TASK explicitly said to KEEP -- is O(1) at the ENERGY-DENSITY level
  (rho c^2 * K'(z) z), because a_c ~ a0 makes z=a_c^2/a0^2 ~ O(1).  It is
  ~ c^2/v^2 ~ 1e6 times the kept term.  You cannot cancel 6 orders; the
  'closed by 1e6' claim cannot survive keeping this term.

  This does NOT by itself prove the channel LENSES correctly (Carl's dream):
  the SAME O(1) K-structure also corrects T_00 (via -1/2 g_mn L and
  d(a_c^2)/dg in the 00 slot), which could ENHANCE the Phi source -> collapse
  toward MG (the double-count horn).  Which of {clean-slip-lens, MG-collapse,
  exact-cancellation} occurs needs the FULL covariant delta/delta g of the
  a_c^2-dependent action -- NOT decidable by the scalar-dust model used.

  STATUS: the review's SLIP-CLOSED (horn C, footing-independent 1e-6) is
  REFUTED as a quantitative closure; true status = OPEN pending the real
  K'-kept variation.
""")
print("exit 0")
