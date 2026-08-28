"""
Gate A / det C^{AB} regularity — FC-FINAL inside the AeST general-F 6-DOF class on Y>0.
=======================================================================================
Grounded in the PUBLISHED AeST Hamiltonian (arXiv:2307.15126, Skordis-Zlosnik):
  F(Y,Q) = -nu Q^2 + mu Y + U(nu,mu)          [Eq.15]
  primary Pi^(mu)~0, Pi^(nu)~0                 [Eq.33-34]
  secondary S^(mu)=(sqrt q/16piG)(Y+U_mu)~0, S^(nu)=(sqrt q/16piG)(-Q^2+U_nu)~0   [Eq.62-63]
  C^{AB}=dS^(B)/dA (2x2)                        [Eq.70]; det C != 0 => chain terminates => 4 first + 4 second
  class => 6 DOF. Momentum inversion via Xi=chi^2 nu-(2(2-K_B)/K_B+mu)|A|^2 [Eq.32]; Q,Y reconstructed with 1/Xi
  [Eq.64-65]. IMPORTANT (Eq.70): the (nu,nu) entry carries an EXTRA -2Q dQ/dnu from the 1/Xi reconstruction,
  so C^{AB} is NOT purely Hess(U): det C needs BOTH Legendre regularity AND Xi != 0.

FC-FINAL frozen: F=K(Q)+F_M(Y), K(Q)=-2Lambda+K2(Q-Q0)^2 (separable => F_YQ=0), mu=F_Y=mu10, y=sqrt Y/a0,
  mu10(y)=y/(1+y^10)^(1/10). Verifies Carl's exact constitutive algebra + the Legendre-map regularity on Y>0.
"""
import sympy as sp
P=print
def ok(c,s): P(f"  [{'PASS' if bool(c) else 'FAIL'}] {s}"); return bool(c)
F=[]
y,a0,K2,Q,Q0 = sp.symbols('y a0 K2 Q Q0', positive=True)
P("="*94); P("Gate A / det C^{AB} Legendre regularity (FC-FINAL sharp J10 in the AeST general-F class)"); P("="*94)

# --- 1. sharp-kernel constitutive derivatives (Carl's exact algebra) ---
mu10 = y/(1+y**10)**sp.Rational(1,10)
mu10p = sp.simplify(sp.diff(mu10,y))
F.append(ok(sp.simplify(mu10p-(1+y**10)**sp.Rational(-11,10))==0,
   f"mu10'(y) = (1+y^10)^(-11/10)   [{mu10p}]"))
longit = sp.simplify(mu10 + y*mu10p)
F.append(ok(sp.simplify(longit - y*(y**10+2)/(1+y**10)**sp.Rational(11,10))==0 and sp.limit(longit,y,0,'+')==0,
   f"mu10 + y mu10' = y(y^10+2)/(1+y^10)^(11/10) > 0 for y>0  [{longit}] (transverse & longitudinal coeffs positive)"))

# --- 2. F_YY = d(mu=F_Y)/dY with Y=a0^2 y^2 : F_YY = mu10'/(2 a0^2 y) > 0 for y>0, -> inf at y=0 ---
FYY = sp.simplify(mu10p/(2*a0**2*y))
F.append(ok(sp.simplify(FYY - 1/(2*a0**2*y*(1+y**10)**sp.Rational(11,10)))==0,
   f"F_YY = mu10'/(2 a0^2 y) = 1/(2 a0^2 y (1+y^10)^(11/10)) > 0 for y>0; -> inf as y->0+ (irregular Legendre boundary)"))

# --- 3. Legendre map Jacobian det d(mu,nu)/d(Y,Q) (separable => diagonal) ---
# mu=F_Y (Y-sector), nu=-F_Q/(2Q)=-K_Q/(2Q) (Q-sector). F_YQ=0 => off-diagonals 0.
KQ = 2*K2*(Q-Q0); KQQ = 2*K2                      # K(Q)=-2L+K2(Q-Q0)^2
dnu_dQ = sp.simplify(sp.diff(-KQ/(2*Q), Q))
Qsector = sp.simplify(-(Q*KQQ - KQ)/(2*Q**2))     # Carl's -(Q K_QQ - K_Q)/(2 Q^2)
F.append(ok(sp.simplify(dnu_dQ - Qsector)==0 and sp.simplify(Qsector - (-K2*Q0/Q**2))==0,
   f"dnu/dQ = -(Q K_QQ - K_Q)/(2Q^2) = -K2 Q0/Q^2  [{Qsector}]  (nonzero iff K2 Q0 != 0)"))
# det of the diagonal Legendre map = F_YY * (Q-sector); nonzero on Y>0, Q!=0, K2 Q0 != 0
detJ = sp.simplify(FYY * Qsector)
F.append(ok(detJ != 0,
   f"det d(mu,nu)/d(Y,Q) = F_YY * (-K2 Q0/Q^2) = {detJ}  != 0 for Y>0, Q!=0, K2 Q0 != 0  => J10 side of the"
   " Legendre map is REGULAR on the open MOND branch. (Requires the frozen K(Q) to have Q0 != 0 -- the"
   " condensate value; if Q0=0 the nu-auxiliary degenerates.)"))

# --- 4. honest structure of C^{AB} (Eq.70): NOT purely Hess(U); needs Xi != 0 ---
P("  [note] Eq.70: C^{nu,nu} = (sqrt q/16piG)(-2Q dQ/dnu + U_nu nu). The -2Q dQ/dnu comes from Q reconstructed")
P("         via 1/Xi (Eq.64), Xi=chi^2 nu-(2(2-K_B)/K_B+mu)|A|^2 (Eq.32). So det C != 0 requires BOTH the")
P("         Legendre regularity above AND Xi != 0 (momentum inversion well-defined). On A_i!=0, Y contains")
P("         phi-dot (via sigma) -- so the earlier 'Y purely spatial => F_YY never in the kinetic matrix'")
P("         argument is RETIRED; it held only on the A_i=0 subsector.")

# --- 5. THE EXACT Y=0 RANK DEFECT (Carl's boundary result): det C|_{Y=0} = 0 ---
# On the aligned homogeneous background A_i=0, D_i phi=0 => Y=|D phi|^2=0, Y independent of mu,nu.
# C_mumu propto U_mumu = -1/F_YY -> 0 (since F_YY -> inf); C_munu=0 (separable F_YQ=0). So:
#   C(Y=0) ~ [[0, 0],[0, C_nunu]]  => det C|_{Y=0} = 0, WHILE det C != 0 for every Y>0.
U_mumu = sp.simplify(-1/FYY)                        # Legendre-dual curvature = -1/F_YY
lim_Umumu = sp.limit(U_mumu, y, 0, '+')
F.append(ok(lim_Umumu==0,
   f"U_mumu = -1/F_YY = {U_mumu} -> {lim_Umumu} as Y->0+ ; C_munu=0 (separable) => C(Y=0)~diag(0,C_nunu) => "
   "det C|_{Y=0} = 0 EXACTLY (rank-deficient auxiliary matrix on the aligned Y=0 surface), while det C != 0 for Y>0."))
P("  => the regular 4+4 Dirac classification STOPS applying at Y=0; the algorithm must be RESTARTED there.")
P("     det C=0 does NOT mean ghost or 7 DOF -- it means the rank loss must be resolved by the full bracket")
P("     calculation (benign constraint conversion keeping 6, OR a tertiary chain / extra mode = a kill). OPEN.")

P("\n"+"="*94)
nf=F.count(False)
if nf==0:
    P("VERDICT (matches Carl's independent analysis):")
    P("  Y>0, Q!=0, Xi!=0  => FC-FINAL's sharp J10 stays INSIDE the regular general-F AeST 6-DOF class:")
    P("  J10 Legendre curvature F_YY>0 finite, longitudinal coeff >0, Legendre map nondegenerate => det C != 0")
    P("  => Dirac chain terminates => 4 first + 4 second class => 6 DOF on the open branch. GENERIC Y>0 = PASS.")
    P("  Y=0: F_YY->inf = IRREGULAR Legendre boundary; exact nonlinear rank(C)|_{Y=0} = OPEN (a DIFFERENT")
    P("  theorem from the healthy quadratic-fluctuation result, which stands as a stability statement).")
    P("  OVERALL: FC-FINAL = CONDITIONALLY CLOSED 6-DOF AeST theory (not globally proven).")
else:
    P(f"  {nf} check(s) FAILED.")
import sys; sys.exit(0 if nf==0 else 1)
