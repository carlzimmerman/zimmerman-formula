"""
COMPUTE-A part (2): the APS INDEX on the 4D Euclidean de Sitter region with S^3
boundary. Index = INT_M A-hat(R) - (eta(0)+h)/2.  The boundary eta/2 term is the
natural home of a 1/2.  Does the framework's a0 = (c/2) coefficient = this eta/2?

We keep kappa SYMBOLIC and ask whether the GEOMETRY outputs 1/2 non-circularly.
"""
import sympy as sp
from sympy import Rational, sqrt, pi, S, nsimplify

print("="*70)
print("(2) APS INDEX ON THE EUCLIDEAN dS REGION, boundary = S^3")
print("="*70)
print("""
The Euclidean de Sitter instanton is the round 4-sphere S^4 (radius l, Lambda=3/l^2).
The de Sitter STATIC PATCH analytically continues to a HEMISPHERE of S^4; its
boundary 3-surface (the horizon's Euclidean section, the 'equator' bolt) is a
round S^3.  This is the framework's OWN forced saddle (the t=0 de Sitter
nucleation 4-sphere named in the SO(4,1) paper, N=3 parity-obstruction note).

APS (Atiyah-Patodi-Singer I, 1975) for the Dirac operator on a 4-manifold M with
boundary dM, under the global APS boundary condition:

    index(D) = INT_M  A-hat(R)  -  (eta_{dM}(0) + h)/2

where A-hat(R) = -1/(192 pi^2) tr(R ^ R) at leading (4-dim) order, h=dim ker(D_{dM}).
""")

# --- (2a) The bulk A-hat integral on the hemisphere/full S^4 ----------------
# For a CLOSED S^4 the Dirac index is 0 (A-hat genus of S^4 = 0; no harmonic
# spinors; positive scalar curvature => Lichnerowicz => ker=0). So on the FULL
# closed S^4: index=0, INT_{S^4} A-hat = 0.
#
# On a HEMISPHERE H (half of S^4) with boundary the equatorial S^3:
#   INT_H A-hat = (1/2) INT_{S^4} A-hat = 0   (A-hat density integrates to 0 even
#   over the hemisphere because the Euler/Pontryagin densities of the round S^4
#   are such that the Pontryagin number p_1=0; A-hat ~ p_1 vanishes pointwise-
#   integrated to the same 0 by symmetry).
#
# Let us verify the round-S^4 Pontryagin/A-hat content symbolically.
print("(2a) Bulk A-hat on round S^4 / hemisphere")
# Round S^n of radius l: Riemann R_{abcd} = (1/l^2)(g_ac g_bd - g_ad g_bc).
# Pontryagin density p_1 ~ tr(R^R). For a CONSTANT-curvature (maximally symmetric)
# 4-manifold, the Weyl tensor vanishes, R is pure 'scalar' part. The first
# Pontryagin form p_1 = (1/8pi^2) tr(R ^ R) for constant curvature:
#   tr(R^R) is built from the Weyl part; for conformally flat (round sphere) the
#   SIGNATURE/Pontryagin number p_1[S^4]=0.  A-hat_4 = -p_1/24.
l = sp.symbols('l', positive=True)
# Pontryagin number of S^4:
p1_S4 = 0      # H^4(S^4) has the Euler class (chi=2) but p_1=0 (signature(S^4)=0)
Ahat_bulk_S4 = -Rational(1,24)*p1_S4
print("   p_1[S^4] = 0  (signature(S^4)=0, Weyl=0 round) ;  A-hat[S^4] =", Ahat_bulk_S4)
print("   => INT_{S^4} A-hat = 0 ; INT_{hemisphere} A-hat = 0 (round, symmetric).")

# --- (2b) The boundary eta term on the bounding S^3 -------------------------
# The bounding S^3 carries the round metric INDUCED from S^4 plus the SECOND
# FUNDAMENTAL FORM of the equator. For the GEODESIC equator (totally geodesic
# S^3 in S^4) the extrinsic curvature vanishes, the boundary is the round S^3,
# and from part (1): eta(0)=0, h=0  => boundary term (eta+h)/2 = 0.
print("\n(2b) Boundary eta on the equatorial S^3 (totally geodesic)")
print("   round S^3, eta(0)=0, h=0  =>  (eta+h)/2 = 0.")

index_geodesic = Ahat_bulk_S4 - S(0)
print("   => index(D) on the geodesic-boundary hemisphere =", index_geodesic)
print("""
   HONEST: with the TOTALLY-GEODESIC equatorial boundary the entire APS formula
   reads 0 = 0 - 0.  There is NO 1/2 anywhere.  The eta/2 boundary slot is
   present but EMPTY for the round, symmetric configuration.
""")

# --- (2c) Does the STATIC-PATCH (horizon) boundary differ? ------------------
# The de Sitter HORIZON in the static patch is NOT the geodesic equator: in
# Euclidean signature the static-patch boundary is the bolt where the Killing
# vector degenerates. But geometrically the Euclidean static patch IS the round
# hemisphere and its boundary IS the round S^3 equator (the cosmological horizon
# bifurcation surface continues to the S^2 bolt, while the t=const slice is the
# S^3).  Either way the induced 3-geometry is the round S^3 with eta=0.
print("(2c) Static-patch boundary = round S^3 (induced) => same eta=0 result.")
print("     The boundary 3-geometry of the Euclidean dS saddle is round S^3.")
print("     No extrinsic-curvature anomaly breaks the +/- spectral symmetry.")
print()
print("VERDICT of the NAIVE geometric APS: eta-boundary-term = 0, NOT 1/2.")
print("A 1/2 does NOT fall out of the round-S^3 / S^4 Dirac APS index.")
