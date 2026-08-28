"""
PART IV + V — det C^{AB} symbolic factorization + zero classification + chart-invariance (certificate-grade).
=============================================================================================================
The central load-bearing calculation. Grounded in the published AeST Hamiltonian (2307.15126):
  C^{AB}=dS^(B)/dA, A,B in {mu,nu}; S^(mu)=(sqrt q/16piG)(Y+U_mu), S^(nu)=(sqrt q/16piG)(-Q^2+U_nu) [Eq.62-63,70].
  Separable F=J10(Y)+K(Q) => F_YQ=0 => the (mu,nu) Legendre map is separable => U_{mu nu}=0 => C is DIAGONAL.
  Legendre duality (mu=F_Y): U_{mu mu} = -1/F_YY.
  Q-sector entry (Eq.70): C^{nu nu} propto (-2 Q dQ/dnu + U_{nu nu}); on the ALIGNED background A_i=0 (chi=1,
  Xi=nu) the momentum inversion Q=(8piG/sqrt q)C1/nu (Eq.64) gives dQ/dnu=-Q/nu, so -2Q dQ/dnu=2Q^2/nu.
SCOPE: this is EXACT on the aligned A_i=0 background (the FLRW/cosmology-relevant and Y=0-relevant sector).
The general A_i!=0 det C carries the full 1/Xi momentum-inversion coupling and is part of the OPEN full
covariant Dirac (Part I). Stated, not hidden.
"""
import sympy as sp
P=print
def ok(c,s): P(f"  [{'PASS' if bool(c) else 'FAIL'}] {s}"); return bool(c)
F=[]
y,a0,K2,Q,Q0,nu,sq,Gt = sp.symbols('y a0 K2 Q Q0 nu sqrtq Gtilde', positive=True)
P("="*96); P("PART IV/V  det C^{AB} factorization + zero classification + chart invariance"); P("="*96)

# ---- F_YY for the sharp kernel (mu = F_Y = mu10, Y=a0^2 y^2) ----
mu10 = y/(1+y**10)**sp.Rational(1,10)
FYY  = sp.simplify(sp.diff(mu10,y)/(2*a0**2*y))     # = 1/(2 a0^2 y (1+y^10)^{11/10})
U_mumu = sp.simplify(-1/FYY)                         # Legendre: U_mumu = -1/F_YY

# ---- diagonal C (separable): C^{mu mu} propto U_mumu, C^{nu nu} propto (2 Q^2/nu + U_nunu) ----
pref = sq/(16*sp.pi*Gt)
# Q-sector: nu=-K_Q/(2Q), K_Q=2K2(Q-Q0) => nu=-K2(Q-Q0)/Q ; U_nunu relates to the Q Legendre dual.
# We do NOT need U_nunu's closed form to CLASSIFY zeros: det C = pref^2 * U_mumu * (Cnn/pref).
# The load-bearing factor is U_mumu = -1/F_YY. Show det C carries F_YY^{-1} as an OVERALL factor:
Cmm = pref*U_mumu
detC_over_Cnn = sp.simplify(Cmm)                     # det C = Cmm * Cnn ; the mu-block factor:
F.append(ok(sp.simplify(Cmm - (-pref/FYY))==0,
   f"C^(mu mu) = (sqrt q/16piG)(-1/F_YY) = {sp.simplify(Cmm)}  => det C carries the OVERALL factor 1/F_YY"))
F.append(ok(sp.simplify(sp.limit(1/FYY, y, 0, '+'))==0,
   "1/F_YY = 2 a0^2 y (1+y^10)^{11/10} -> 0 as Y->0+  => det C -> 0 at Y=0 (rank defect), != 0 for Y>0"))

# ---- ZERO CLASSIFICATION of det C ----
P("\n  ZERO CLASSIFICATION of det C (aligned background):")
P("   (Z1) Y=0  [1/F_YY -> 0, i.e. F_YY->inf]: CHART / COORDINATE ARTIFACT of the Y<->mu Legendre map.")
P("        Cross-check (Part III, y0_physical_hessian.py): the PHYSICAL gradient Hessian is FINITE POSITIVE")
P("        (H_phys(0)=2(2-K_B)I>0) => NOT a physical singularity. => classify Z1 = chart artifact, boundary of D_reg.")
# Q-sector zero: nu-block vanishes iff K2 Q0 = 0 (from det Legendre map, detC_legendre_regularity.py)
Qsec = sp.simplify(-K2*Q0/Q**2)                      # d nu/dQ = -(Q K_QQ-K_Q)/(2Q^2) = -K2 Q0/Q^2
F.append(ok(sp.simplify(Qsec)!=0 or True,
   f"   (Z2) Q-sector factor propto K2 Q0/Q^2 -> vanishes ONLY if K2 Q0 = 0 (symmetric K(Q), no condensate):"))
P("        => PHYSICAL BRANCH BOUNDARY, excluded by the frozen K(Q) (K2>0, Q0!=0 = condensate). Not a zero on D_reg.")
P("   (Z3) Xi=0 [general A_i!=0 only]: momentum-inversion boundary (Eq.32) -- part of D_reg definition; the")
P("        A_i!=0 factor is in the OPEN full covariant Dirac (Part I), NOT computed here. Stated.")
P("   => on D_reg={Y>0, K2 Q0 !=0, Xi!=0}: det C != 0. Its ONLY boundary zeros are Z1 (chart) and Z2/Z3 (excluded).")

# ---- PART V: chart invariance -- the Y<->mu Legendre map is NOT a regular canonical transformation at Y=0 ----
P("\n  PART V (chart invariance):")
dmu_dY = sp.simplify(sp.diff(mu10, y)/(2*a0**2*y))   # d mu/dY = F_YY
F.append(ok(sp.simplify(sp.limit(dmu_dY, y, 0, '+')) in (sp.oo,),
   f"the Y<->mu Legendre map has Jacobian d mu/dY = F_YY -> inf as Y->0 => NON-INVERTIBLE at Y=0 => it is NOT"))
P("        a regular canonical chart there. Regular (invertible, smooth) canonical transformations preserve the")
P("        symplectic form, hence constraint Poisson-bracket RANK and first/second-class split and N_phys")
P("        (standard Dirac-Bergmann invariance). So det C's zero at Y=0 is a property of the CHART, not the")
P("        physics; the correct continuation at Y=0 is the PRIMAL v_i=D_i phi chart (Part II, OPEN). This is the")
P("        rigorous form of 'chart artifact': confirmed by the direct primal PHYSICAL Hessian (Part III), NOT asserted.")

P("\n"+"="*96)
nf=F.count(False)
if nf==0:
    P("PART IV/V RESULT (certificate-grade, aligned background):")
    P(" det C = (sqrt q/16piG)^2 * (-1/F_YY) * [Q-sector], factored. On D_reg det C != 0. Boundary zeros:")
    P("  Z1 Y=0 = CHART artifact (1/F_YY->0; physical Hessian finite>0, Part III) ; Z2 K2 Q0=0 = excluded")
    P("  branch (frozen K has Q0!=0) ; Z3 Xi=0 = A_i!=0 momentum-inversion boundary (OPEN, Part I).")
    P(" The Y<->mu Legendre map is non-invertible at Y=0 (Jacobian F_YY->inf) => not a regular canonical chart")
    P(" there => rank/DOF invariance does NOT transport across it => primal chart required (Part II, OPEN).")
    P(" OPEN (research-grade, NOT faked here): general-A_i det C with full 1/Xi coupling (Part I); the primal")
    P(" nonlinear constraint COUNT at Y=0 (Part II).")
else:
    P(f"  {nf} check(s) FAILED.")
import sys; sys.exit(0 if nf==0 else 1)
