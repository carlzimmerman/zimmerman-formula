#!/usr/bin/env python3
"""
STEP 2 -- The Jacobson balance. First reproduce 8pi (sanity), then feed the MOND flux.
======================================================================================
From Shimada-Okazawa-Iso (arXiv:1206.1154, p.3), Jacobson's two sides are:

  HEAT side :  delta Q / T = -2pi  integral_H  lambda_K  T_munu K^mu K^nu  sqrt(g) d^{n-2}y dlambda_K
  ENTROPY   :  delta(A/4)  = (1/4) integral_H { -R_munu K^mu K^nu |_P  lambda_K + O(lambda^2) } sqrt(g) ...

Set delta Q = T delta S = T delta(A/4) (eta=1/4 in G=hbar=1):
    -2pi T_munu K^muK^nu = (1/4)(-R_munu K^muK^nu)   (integrands, leading order in lambda)
 => R_munu K^muK^nu = 8 pi T_munu K^muK^nu  for all null K  => R_munu - (1/2)Rg_munu = 8 pi T_munu.

The 8pi = 2pi (Unruh) / (1/4) (Bekenstein-Hawking).  This is structural: ANY T_munu
on the RHS sources the SAME Einstein eq with the SAME 8pi.

QUESTION FOR THE MOND ROUTE: if we put the deep-MOND T_munu (Step 1) on the heat side,
does the balance FIX a0 -- or does it merely add phi's stress to the matter that Einstein
gravity already carries (so a0 stays the free normalization of L_phi)?
"""
import sympy as sp

print("="*78)
print("STEP 2: Jacobson factor accounting -- reproduce 8pi, then test MOND")
print("="*78)

pi = sp.pi
# The two universal numbers in Jacobson:
unruh = 2*pi          # T_Unruh = hbar kappa / 2pi  -> the 2pi
bekhawk = sp.Rational(1,4)   # S = A/4 (in lP^2 units) -> the 1/4
coupling = unruh/bekhawk
print(f"\n  Unruh factor (from T = hbar kappa/2pi):      2pi      = {sp.nsimplify(unruh)}")
print(f"  Bekenstein-Hawking factor (from S = A/4):    1/4")
print(f"  Einstein coupling = 2pi / (1/4) =            8pi      = {coupling}")
print("  => R_munu - (1/2)R g_munu = 8 pi G T_munu.  FORCED, matter-independent.")

print("""
--------------------------------------------------------------------------------
THE CRUX -- what role does the deep-MOND T_munu play on the RHS?
--------------------------------------------------------------------------------
In Jacobson, T_munu is the *source*. The deep-MOND scalar's stress (Step 1) is just
ANOTHER contribution to T_munu^total = T_munu^matter + T_munu^phi.  The balance gives:

    G_munu = 8 pi G ( T^matter_munu + T^phi_munu[a0] )

The coefficient 8pi is fixed by Unruh/BH -- a0 does NOT appear in it.  a0 appears ONLY
inside T^phi_munu, as the normalization of L_phi.  So the Jacobson balance treats a0 as
EXTERNAL DATA (the matter Lagrangian's coupling), exactly as it treats the electron
charge or any other matter coupling.  It does not, and cannot, fix a0 -- UNLESS there
is an extra condition that ties a0 to the geometry (Lambda) independently.

That extra condition is the ONE new thing this route tries: the IR cutoff of the
on-shell phi action at the de Sitter horizon R_dS = sqrt(3/Lambda).  Step 4 tests whether
THAT closes a0.  But note already: the cutoff enters the *free energy* (the on-shell
action), NOT the *local* flux T_munu K^muK^nu, which is purely local (no R_dS in it).

So we have two distinct sub-routes to test:
  (2a) PURELY LOCAL Jacobson flux  -> Step 3 (does the local balance see a0? -> expect NO)
  (2b) FREE-ENERGY / on-shell action with R_dS cutoff -> Step 4 (the off-saddle attempt)
""")
