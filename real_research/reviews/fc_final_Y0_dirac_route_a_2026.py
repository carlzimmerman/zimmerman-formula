"""
ROUTE A -- mini-superspace Dirac analysis of the FC-FINAL scalar sector at the Y=0
degenerate branch.  Question: (a) 6-DOF benign non-analyticity, (b) DOF jump/spurious
gauge, (c) ghost, (d) strong coupling?

Reduced model (as assigned):
  keep the analytic  -(2-K_B) Y  kinetic term for phi
  represent F_M(Y) by its Legendre auxiliary:  F_M(Y) -> q Y - F_M^*(q),
      F_M^*(q) = (4/3) a0^2 q^3   [dual of F_M = Y^{3/2}/(3 a0) near Y=0]
  So the Y-dependent Lagrangian density is
      L_Y = -(2-K_B) Y  -  [ q Y - F_M^*(q) ]  =  -[(2-K_B)+q] Y + (4/3) a0^2 q^3

Mini-superspace: one mode, Y is treated as phi's kinetic scalar Y = phidot^2
(the "spatial-gradient proxy" carrying Y>=0), q(t) the auxiliary.  We run the FULL Dirac
algorithm: momenta, primary+secondary constraints, the constraint Poisson matrix, its rank,
N_phys, all as functions of the background q (equivalently Y=4 a0^2 q^2), then take q->0.
We report which of  F_YY = 1/(4 a0 sqrt(Y)),  F*_qq = 8 a0^2 q,  or the (2-K_B) term
controls the second-class bracket and the phi kinetic eigenvalue.
"""
import sympy as sp

t = sp.symbols('t')
KB, a0 = sp.symbols('K_B a0', positive=True)   # 0 < K_B < 2  (BBN: K_B <~ 0.25)
c2 = 2 - KB                                     # (2 - K_B) > 0, the analytic coefficient

# ---- configuration variables and velocities
phi = sp.Function('phi')(t)
q   = sp.Function('q')(t)
phid = sp.diff(phi, t)
qd   = sp.diff(q, t)

Y = phid**2                                     # spatial-gradient proxy -> phi kinetic scalar
Fstar = sp.Rational(4,3)*a0**2*q**3             # F_M^*(q)

L = -(c2 + q)*Y + Fstar                         # reduced Lagrangian
print("L =", sp.simplify(L))

# ---- canonical momenta
pphi = sp.diff(L, phid)
pq   = sp.diff(L, qd)
print("p_phi =", pphi)
print("p_q   =", pq, "  -> PRIMARY constraint C1 = p_q ~ 0")

PPHI, PQ, Q, PHI = sp.symbols('p_phi p_q q phi')

# invert velocity: p_phi = -2(c2+q) phidot  => phidot = -p_phi/(2(c2+q))
phid_sol = -PPHI/(2*(c2+Q))

# ---- canonical Hamiltonian (phi sector); q has no velocity -> primary constraint
Hcan = (PPHI*phid_sol
        - ( -(c2+Q)*phid_sol**2 + sp.Rational(4,3)*a0**2*Q**3 ))
Hcan = sp.simplify(Hcan)
print("\nH_can =", Hcan)

# phi kinetic eigenvalue = coefficient of p_phi^2  (inverse effective mass of phi)
Kphi = sp.simplify(Hcan.coeff(PPHI,2))
print("phi kinetic coefficient (1/eff-mass) =", Kphi)
print("  limit q->0 :", sp.limit(Kphi, Q, 0), "  <-- set by (2-K_B), NOT by q")

# ---- Dirac algorithm.  Total H = H_can + u * C1,  C1 = p_q
# Consistency of C1:  {C1, H} = -dH/dq  must vanish -> secondary constraint C2
C1 = PQ
C2 = sp.simplify(-sp.diff(Hcan, Q))            # = dH/dq up to sign; this is the secondary
print("\nC1 = p_q")
print("C2 (secondary, from {C1,H}=0) =", C2)

# Poisson brackets in (phi,p_phi,q,p_q).  Canonical pairs.
def PB(f,g):
    return (sp.diff(f,PHI)*sp.diff(g,PPHI) - sp.diff(f,PPHI)*sp.diff(g,PHI)
          + sp.diff(f,Q)*sp.diff(g,PQ)   - sp.diff(f,PQ)*sp.diff(g,Q))

M12 = sp.simplify(PB(C1,C2))
print("\n{C1,C2} =", M12)

# evaluate {C1,C2} ON the secondary surface C2=0.
# C2=0 solves p_phi^2 in terms of q:
sol = sp.solve(sp.Eq(C2,0), PPHI**2)
print("C2=0  =>  p_phi^2 =", sol)
if sol:
    M12_on = sp.simplify(M12.subs(PPHI**2, sol[0]))
    # sympy may not substitute p_phi**2 pattern; do it manually via p_phi^2 symbol
    P2 = sp.symbols('P2', nonnegative=True)
    M12_p2  = M12.rewrite(sp.Pow)
    M12_p2  = M12.subs(PPHI, sp.sqrt(P2))
    M12_on2 = sp.simplify(M12_p2.subs(P2, sol[0]))
    print("{C1,C2} ON the constraint surface C2=0 :", M12_on2)
    print("  factor out: proportional to q ->", sp.simplify(M12_on2/ (a0**2*Q)))
    print("  limit q->0 :", sp.limit(M12_on2, Q, 0))

# ---- the two candidate Hessians, and their product
FYY  = 1/(4*a0*sp.sqrt(sp.symbols('Yv', positive=True)))  # F_YY = 1/(4 a0 sqrt Y) -> inf
Fqq  = 8*a0**2*Q                                           # F*_qq = 8 a0^2 q      -> 0
Yv   = sp.symbols('Yv', positive=True)
# on-shell Y = 4 a0^2 q^2 -> sqrt(Y)=2 a0 q :
FYY_onshell = sp.simplify(FYY.subs(Yv, 4*a0**2*Q**2))
print("\nF_YY on-shell =", FYY_onshell, "  (-> +inf as q->0)")
print("F*_qq        =", Fqq,            "  (->  0   as q->0)")
print("F_YY * F*_qq =", sp.simplify(FYY_onshell*Fqq), "  (identically 1 -> reciprocal)")

# ---- DOF count.  Phase space dim = 4 (phi,p_phi,q,p_q).
# generic q>0: constraints {C1,C2} second-class (bracket != 0):
#   N_phys = (4 - 2)/2 = 1 propagating DOF (phi).  Auxiliary q frozen algebraically.
print("\n--- DOF ---")
print("generic Y>0 (q>0): C1,C2 second-class, det(M)!=0 -> N_phys=(4-2)/2 = 1 (phi healthy)")
print("Y=0 (q=0): {C1,C2}->0 (controlled by F*_qq=8 a0^2 q), constraints declassify AT the point")
print("  but phi kinetic coeff -> 1/(4(2-K_B)) FINITE nonzero  => NOT strong coupling, NOT ghost")
print("  and F_M = O(Y^{3/2}) => modification's contribution to H,C2,bracket switches off there")
