#!/usr/bin/env python3
"""
STEP 3 -- The on-shell MOND free energy with the R_dS IR cutoff, and its first-law match.
=========================================================================================
This is THE calculable object the prior verdict flagged as 'the one bounded thing that
could still close it': the O(eps^3) on-shell free energy of the C(Q) Y^{3/2} vertex with
the de Sitter horizon as IR cutoff, matched to delta Q = T delta S.

We compute:
  (A) I_phi = integral L_deepMOND d^3x for the point-mass field, IR-cut at R_dS.
  (B) the de Sitter first law delta Q = T delta S for a mass M (Gibbons-Hawking).
  (C) match them and see what is forced.

EVERYTHING in sympy. The radicand sqrt(pi) and the rational prefactor are tracked
separately, per the hard constraint (sqrt(32pi/3) not in Q(pi)).
"""
import sympy as sp

print("="*78)
print("STEP 3: on-shell MOND free energy, IR-cut at R_dS, vs de Sitter first law")
print("="*78)

# symbols
a0, G, M, r, Lam, c, hbar = sp.symbols('a0 G M r Lambda c hbar', positive=True)
pi = sp.pi
Rds = sp.sqrt(3/Lam)        # de Sitter horizon radius (c=1 here; restore c later)

# ---------------------------------------------------------------------------
# (A) on-shell action of the deep-MOND field around a point mass
# ---------------------------------------------------------------------------
# |grad phi| = sqrt(G M a0)/r ; L = -|grad phi|^3/(12 pi G a0)
gphi = sp.sqrt(G*M*a0)/r
Ldens = -gphi**3/(12*pi*G*a0)
Ldens = sp.simplify(Ldens)
print("\nL(r) =", Ldens)

# integral over 3-space: 4 pi r^2 dr, from inner cutoff r_in to R_dS
r_in = sp.symbols('r_in', positive=True)
integrand = Ldens*4*pi*r**2
I_phi = sp.integrate(integrand, (r, r_in, Rds))
I_phi = sp.simplify(I_phi)
print("\nI_phi = integral L 4pi r^2 dr (r_in..R_dS) =", I_phi)
print("  (LOG divergent: ~ log(R_dS/r_in). The IR end R_dS is the horizon link.)")

# The IR-DOMINANT, physically meaningful piece is the log times the coefficient.
# Coefficient of the logarithm:
coef = sp.simplify(integrand*r)   # integrand ~ coef/r, so integral = coef*log(...)
print("\nCoefficient of dr/r in the integrand (the log coefficient):")
print("   integrand * r =", coef)
log_coef = coef
print("   => I_phi = (", log_coef, ") * log(R_dS / r_in)")

# So I_phi = -(GMa0)^{3/2}/(3 G a0) * log(R_dS/r_in)
#          = -(1/3) M^{3/2} (G a0)^{1/2} ... let's simplify the coefficient cleanly
log_coef_simpl = sp.simplify(-(G*M*a0)**sp.Rational(3,2)/(3*G*a0))
print("\n   log coefficient simplified =", log_coef_simpl,
      "  =? -(1/3) M sqrt(G M a0)")
check = sp.simplify(log_coef_simpl - (-sp.Rational(1,3)*M*sp.sqrt(G*M*a0)))
print("   equals -(1/3) M sqrt(GMa0)? ", check == 0)

print("""
--------------------------------------------------------------------------------
OBSERVATION 1: the free energy is M^{3/2}, NOT linear in M.
--------------------------------------------------------------------------------
I_phi ~ -(1/3) M sqrt(G M a0) log(R_dS/r_in)  ~  M^{3/2}.

The de Sitter first-law heat delta Q = T delta S for adding mass M is LINEAR in M
(delta S = delta A/4, delta A linear in M to leading order; T fixed).  A function ~M^{3/2}
CANNOT be matched term-by-term to a function ~M^1 by any choice of the CONSTANT a0:
the M-dependences differ.  This is the first obstruction and it is structural, not
numerical.  We quantify it precisely in Step 4.
""")
