#!/usr/bin/env python3
"""
STEP 1 -- Derive the deep-MOND stress tensor from the AQUAL Lagrangian, EXACTLY.
================================================================================
Goal: get T_munu[phi] for L_deepMOND = -(a0^2/8piG) f(Y/a0^2), f(x)->(2/3)x^{3/2},
i.e. L = -|grad phi|^3 / (12 pi G a0).   Y = |grad phi|^2.

We need T_munu k^mu k^nu (the integrand of Jacobson's delta Q flux) for a NULL k.

Every prefactor derived in sympy. No numbers inserted.
"""
import sympy as sp

print("="*78)
print("STEP 1: deep-MOND stress tensor from AQUAL")
print("="*78)

# ---- symbols ----
a0, G, pi, r, M = sp.symbols('a0 G pi r M', positive=True)
# field gradient magnitude and its square
gphi = sp.symbols('gphi', positive=True)   # |grad phi|
Y = gphi**2                                  # Y = |grad phi|^2

# ---- the deep-MOND Lagrangian density ----
# Bekenstein-Milgrom: L = -(a0^2/8 pi G) F(Y/a0^2), F(x)->(2/3) x^{3/2} deep-MOND.
# So L_deep = -(a0^2/8piG)*(2/3)*(Y/a0^2)^{3/2} = -(1/12 pi G a0) Y^{3/2}
L = -(a0**2/(8*pi*G)) * sp.Rational(2,3) * (Y/a0**2)**sp.Rational(3,2)
L = sp.simplify(L)
print("\nL_deepMOND(Y) =", L, "   [should be -gphi^3/(12 pi G a0)]")
L_target = -gphi**3/(12*pi*G*a0)
print("  matches -|grad phi|^3/(12 pi G a0)? ", sp.simplify(L - L_target) == 0)

# ---- the field equation / point-mass solution check ----
# AQUAL EOM: div( mu(|grad phi|/a0) grad phi ) = 4 pi G rho, mu(x)->x deep-MOND.
# For point mass: mu |grad phi| -> |grad phi|^2/a0 = G M / r^2  =>  |grad phi| = sqrt(GMa0)/r
gphi_sol = sp.sqrt(G*M*a0)/r
mu_deep = gphi_sol/a0   # mu = |grad phi|/a0
mond_accel = mu_deep*gphi_sol   # the 'Newtonian-equivalent' field mu|grad phi|
print("\nPoint mass: mu|grad phi| = |grad phi|^2/a0 =", sp.simplify(mond_accel),
      "  [should be GM/r^2]")
print("  equals GM/r^2? ", sp.simplify(mond_accel - G*M/r**2) == 0)

# ---- stress tensor: T_munu = (dL/d(partial^mu phi)) partial_nu phi - g_munu L ----
# For L = L(Y), Y = g^ab partial_a phi partial_b phi:
#   dL/d(partial^mu phi) = 2 L'(Y) partial_mu phi
# => T_munu = 2 L'(Y) partial_mu phi partial_nu phi - g_munu L
# The flux integrand needs T_munu k^mu k^nu with k null (k.k=0), so the g_munu L term
# DROPS (g_munu k^mu k^nu = 0). Thus:
#   T_munu k^mu k^nu = 2 L'(Y) (k.grad phi)^2
Yvar = sp.symbols('Yvar', positive=True)   # clean symbol for Y to differentiate
L_of_Y = -(1/(12*pi*G*a0))*Yvar**sp.Rational(3,2)
Lp_explicit = sp.diff(L_of_Y, Yvar).subs(Yvar, gphi**2)
print("\nL'(Y) = dL/dY =", sp.simplify(Lp_explicit),
      "   [= -(1/8 pi G a0) sqrt(Y) = -|grad phi|/(8 pi G a0)]")
Lp_target = -gphi/(8*pi*G*a0)
print("  equals -|grad phi|/(8 pi G a0)? ",
      sp.simplify(Lp_explicit - Lp_target) == 0)

print("""
=> KEY RESULT for the Jacobson flux (k null, so -g_munu L term vanishes):

     T_munu k^mu k^nu = 2 L'(Y) (k^a partial_a phi)^2
                      = -[ |grad phi| / (4 pi G a0) ] (k.grad phi)^2

NOTE THE SIGN: L'(Y) < 0 for the cubic.  This is the deep-MOND field's
'wrong-sign' kinetic structure (it is the gradient energy of a CONFINING log
potential).  Whether this sign is physical for the flux is examined in Step 3.
""")

# numeric sanity on the prefactor magnitude
print("Prefactor of (k.grad phi)^2 in T_kk:  -|grad phi|/(4 pi G a0)")
print("  (carries 1/(G a0) -- i.e. it is C ~ 1/(G a0), the MOND normalization).")
