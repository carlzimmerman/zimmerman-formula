#!/usr/bin/env python3
"""
DOOR 3 -- CAN BIMOND HOST THE DECLINE?  [PART 1: SYMBOLIC FRW REDUCTION]

Build the ASYMMETRIC bimetric-MOND (BIMOND) cosmology from Milgrom's action
(arXiv:0912.0790, "Bimetric MOND gravity"; structure unchanged in 2512.09353).

ACTION (Milgrom 0912.0790, eq. 14-ish; here in the 'pure C' subclass):
  S = -(c^4 / 16 pi G) * Integral[ beta sqrt(-g) R(g)  +  gamma sqrt(-ghat) Rhat(ghat)
                                    - 2 (g ghat)^{1/4} a0^2 M(Q) ] d^4x
      + S_M[fields, g] + Shat_M[fields, ghat]

  with the scalar built from the DIFFERENCE of the two Levi-Civita connections
      C^a_bc = Gamma^a_bc(g) - Gammahat^a_bc(ghat)            (a true tensor)
  and Q a dimensionless quadratic scalar in C, e.g. Milgrom's
      Q = (c^2/a0)^2 * g^{mu nu}( C^a_{mu b} C^b_{nu a} - C^a_{mu nu} C^b_{ab} )    (Q_2 in 0912.0790)
  [Different index contractions Q_1..Q_5 exist; we take the FRW value of this class.]

  Newtonian/MOND limit: M(Q) ~ Q^{3/2} as Q->0 gives deep-MOND; M -> linear gives Newton.
  KEY THEOREM WE TEST (Milgrom): on FRW the two metrics can have DIFFERENT scale factors
  a(t), ahat(t).  The C-tensor is then built from the difference of Hubble rates.
  Milgrom (0912.0790 sec 6, and 1006.3809) shows Lambda_eff ~ a0^2 * Mtilde, and the
  matter-era enhancement G_e ~ 2 pi G is a DIMENSIONAL estimate.  We test it by integration.

THIS FILE: derive, with sympy, the FRW form of
  (i) the C-tensor / Q on twin flat-FRW metrics,
  (ii) the two modified Friedmann equations,
  (iii) the effective gravitational coupling G_e(z) and a_eff(z) = a0 sqrt(G_e/G).
The numeric integration is in door3_bimond_frw_integrate.py.
"""
import sympy as sp

print("="*92)
print("PART 1  --  SYMBOLIC FRW REDUCTION OF ASYMMETRIC BIMOND")
print("="*92)

t = sp.symbols('t', real=True)
c, a0, G, beta, gam = sp.symbols('c a0 G beta gamma', positive=True)

# Twin spatially-flat FRW metrics (mostly-plus), lapse N=Nhat=1 (cosmic time):
#   ds^2  = -c^2 dt^2 + a(t)^2  delta_ij dx^i dx^j
#   dshat^2 = -c^2 dt^2 + ahat(t)^2 delta_ij dx^i dx^j
a  = sp.Function('a',  positive=True)(t)
ah = sp.Function('ah', positive=True)(t)

H  = sp.diff(a, t)/a
Hh = sp.diff(ah,t)/ah

print("\n[1] Twin flat-FRW metrics share cosmic time t; scale factors a(t) != ahat(t).")
print("    H = a'/a ,  Hhat = ahat'/ahat .")

# ---- Christoffel symbols for a flat FRW metric (standard) ----
# For g = diag(-c^2, a^2, a^2, a^2):
#   Gamma^0_ij = (a a'/c^2) delta_ij ,  Gamma^i_0j = (a'/a) delta^i_j .  (others 0)
# So the only nonzero connection components live in the 0-i-j block.
#
# The DIFFERENCE tensor C^a_bc = Gamma(g) - Gamma(ghat).  Because both metrics are
# diagonal FRW sharing the SAME time slicing and SAME comoving coords, the spatial-time
# mixing pieces are:
#   C^0_ij = (1/c^2)( a a' - ahat ahat' ) delta_ij
#   C^i_0j = ( a'/a - ahat'/ahat ) delta^i_j = (H - Hhat) delta^i_j
# (C^0_00 = C^i_jk(spatial) = 0 for flat FRW.)
print("\n[2] Difference-connection tensor C^a_bc = Gamma(g) - Gamma(ghat) on twin FRW:")
C0ij = (a*sp.diff(a,t) - ah*sp.diff(ah,t))/c**2      # coefficient of delta_ij in C^0_ij
Ci0j = (H - Hh)                                       # coefficient of delta^i_j in C^i_0j
print("    C^0_ij = (a a' - ahat ahat')/c^2  * delta_ij")
print("    C^i_0j = (H - Hhat) * delta^i_j      <-- the relative expansion rate")
sp.pprint(sp.simplify(Ci0j))

# ---- The MOND scalar Q.  Milgrom builds Q from the scalar
#   Upsilon = g^{mu nu}( C^a_{mu b} C^b_{nu a} - C^a_{mu nu} C^b_{a b} ) * (c^2/a0)^2
# Evaluate this contraction on the FRW C-tensor.  We do the index sums explicitly.
print("\n[3] The dimensionless MOND scalar Q on FRW (Milgrom's Q_2 contraction):")
print("    Q = (c^2/a0)^2 * g^{mu nu}( C^a_{mu b} C^b_{nu a} - C^a_{mu nu} C^b_{ab} ).")

# Build the C tensor as an explicit 4x4x4 array on a flat FRW background metric.
# coords (0=ct-like time index with g_00=-c^2, 1,2,3 spatial with g_ii=a^2)
g  = sp.diag(-c**2, a**2,  a**2,  a**2)
gi = g.inv()
# C[upper a][lower b][lower c]
C = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
delta = lambda i,j: 1 if i==j else 0
for i in range(1,4):
    for j in range(1,4):
        C[0][i][j] = C0ij*delta(i,j)     # C^0_ij
for i in range(1,4):
    for j in range(1,4):
        C[i][0][j] = Ci0j*delta(i,j)     # C^i_0j
        C[i][j][0] = Ci0j*delta(i,j)     # C^i_j0  (symmetric lower pair)

# term1 = g^{mu nu} C^a_{mu b} C^b_{nu a}  (sum a,b,mu,nu)
term1 = sp.Integer(0)
for mu in range(4):
    for nu in range(4):
        gmn = gi[mu,nu]
        if gmn == 0: continue
        for aidx in range(4):
            for b in range(4):
                term1 += gmn * C[aidx][mu][b] * C[b][nu][aidx]
# term2 = g^{mu nu} C^a_{mu nu} C^b_{a b}
term2 = sp.Integer(0)
for mu in range(4):
    for nu in range(4):
        gmn = gi[mu,nu]
        if gmn == 0: continue
        for aidx in range(4):
            Cb_ab = sum(C[b][aidx][b] for b in range(4))   # contract C^b_{a b}
            term2 += gmn * C[aidx][mu][nu] * Cb_ab

Ups = sp.simplify(term1 - term2)
Q = sp.simplify((c**2/a0)**2 * Ups)
print("\n    Upsilon = term1 - term2 =")
sp.pprint(sp.simplify(Ups))
print("\n    => Q (dimensionless) =")
Q = sp.simplify(Q)
sp.pprint(Q)

# Express Q in terms of (H - Hhat):
dH = sp.symbols('DeltaH', real=True)   # = H - Hhat
Q_dH = Q.subs(sp.diff(a,t), H*a).subs(sp.diff(ah,t), Hh*ah)
Q_dH = sp.simplify(Q_dH)
print("\n    Q as a function of the relative expansion rate (H - Hhat):")
sp.pprint(Q_dH)
# Show leading behavior: Q ~ (c^2/a0)^2 * #*(H-Hhat)^2   -> dimensionless 'relative-acceleration' scalar
print("\n    => Q is QUADRATIC in (H - Hhat), scaled by (c^2/a0)^2.")
print("       Define the relative-expansion acceleration  A_rel = c*(H - Hhat).")
print("       Then Q ~ (A_rel/a0)^2 * O(1).  This is the cosmological 'relative-acceleration scalar'.")

print("""
[4] PHYSICAL READING (the crux):
    * In Milgrom's BIMOND the interaction term  (g ghat)^{1/4} a0^2 M(Q)  acts as an
      effective Lambda whose VALUE is set by a0^2 * M(Q_FRW).
    * Q_FRW is controlled by the dimensionless ratio  x = c(H - Hhat)/a0  (relative
      expansion of the twin metrics).  When the two metrics co-move (Hhat=H), Q=0:
      then the interaction is a PURE CONSTANT  Lambda = -(a0^2/c^4) M(0) Mtilde0/2  (eq.87)
      -> exactly GR + constant Lambda  (the SYMMETRIC-FRW theorem).
    * To get ANY time-evolution of Lambda_eff you must DRIVE Hhat != H.  The twin
      matter sector (rho_hat) sources ahat; if the visible and twin matter differ, the
      metrics separate, Q(z) runs, and Lambda_eff(z)=a0^2 M(Q(z)) evolves.
    * The deep-MOND choice M(Q)~Q^{3/2} (-> Q->0) makes the interaction a function that
      GROWS with |H-Hhat|; the matter-era estimate G_e~2 pi G is the claim we now TEST.

    a_eff(z) is read off the EFFECTIVE Newton constant in the Friedmann constraint:
        a_eff(z) = a0 * sqrt( G_e(z)/G ).
    The integration file builds the two coupled Friedmann equations and computes G_e(z).
""")
print("Symbolic reduction complete. Q is quadratic in (H-Hhat)/(a0/c) as Milgrom states.")
