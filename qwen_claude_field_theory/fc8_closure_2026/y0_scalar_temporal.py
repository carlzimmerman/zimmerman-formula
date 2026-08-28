"""
Y=0 SCALAR TEMPORAL SECTOR — physical kinetic F_QQ vs auxiliary nu (Carl's catch + a convention fix).
=====================================================================================================
Claim (Carl): at the homogeneous aligned background A_i=0, Y=0, Q=Q0 (K-minimum), the auxiliary nu -> 0 but
the PHYSICAL scalar time-kinetic F_QQ != 0, so there is NO kinetic degeneracy. This requires the PUBLISHED
AeST convention K(Q) == -1/2 F(0,Q)  (Skordis-Zlosnik), i.e. F(0,Q) = -2 K(Q). With that convention the
physical Lagrangian term -F(0,Q) = +2 K(Q) gives a HEALTHY (positive) phi-dot kinetic coefficient.

CONVENTION CORRECTION: FROZEN_CANDIDATE.md wrote 'F_Q^star = K(Q)' loosely. Taken literally (F(0,Q)=K), the
action term -F(0,Q)=-K gives d^2/dQ^2 = -2 K2 < 0 => GHOST. The CORRECT AeST convention is F(0,Q)=-2K(Q),
giving +4 K2 > 0. This script verifies Carl's result AND flags the sign fix; FROZEN_CANDIDATE.md is corrected.
"""
import sympy as sp
P=print
def ok(c,s): P(f"  [{'PASS' if bool(c) else 'FAIL'}] {s}"); return bool(c)
F=[]
Q,Q0,K2,Lam = sp.symbols('Q Q0 K2 Lambda', positive=True)
P("="*94); P("Y=0 scalar temporal sector: physical F_QQ vs auxiliary nu"); P("="*94)

# --- AeST convention: cosmological function K(Q)=-1/2 F(0,Q), min at Q0 ---
Kcos = -2*Lam + K2*(Q-Q0)**2                          # cosmological K(Q), K2>0, min at Q0
Fcal0 = sp.simplify(-2*Kcos)                          # F(0,Q) = -2 K(Q)   [AeST]
P(f"  AeST convention: K(Q) = -1/2 F(0,Q) => F(0,Q) = -2K(Q) = {Fcal0}")

# --- auxiliary nu = -F_Q/(2Q) vanishes at Q0 (K-minimum) ---
FQ = sp.diff(Fcal0, Q)
nu = sp.simplify(-FQ/(2*Q))
nu_Q0 = sp.simplify(nu.subs(Q, Q0))
F.append(ok(sp.simplify(FQ.subs(Q,Q0))==0 and nu_Q0==0,
   f"F_Q(Q0)=0 (minimum) => auxiliary nu(Q0) = -F_Q/(2Q)|_Q0 = {nu_Q0}  (nu -> 0)"))

# --- physical F_QQ = -4 K2 != 0 (curvature, NOT the auxiliary) ---
FQQ = sp.simplify(sp.diff(Fcal0, Q, 2))
F.append(ok(sp.simplify(FQQ + 4*K2)==0,
   f"F_QQ = d^2 F(0,Q)/dQ^2 = {FQQ} = -4 K2 != 0 for K2>0  => auxiliary nu=0 does NOT imply physical kinetic degeneracy"))

# --- physical time-kinetic from -F(0,Q) with Q=phi_dot: coefficient of phi_dot^2 ---
Kkin = sp.simplify(sp.diff(-Fcal0, Q, 2))             # d^2[-F(0,Q)]/dQ^2 (Q=phi_dot on aligned bg)
F.append(ok(sp.simplify(Kkin - 4*K2)==0 and Kkin.subs(K2,1) > 0,
   f"physical scalar time-kinetic K_phi,time = d^2[-F(0,Q)]/dQ^2 = {Kkin} = +4 K2 > 0 for K2>0  => HEALTHY (no ghost)"))

# --- the SIGN-ERROR control: the loose 'F(0,Q)=K' convention would give a GHOST ---
Kkin_wrong = sp.simplify(sp.diff(-Kcos, Q, 2))        # if F(0,Q)=K(Q) (WRONG), -F=-K
F.append(ok(sp.simplify(Kkin_wrong + 2*K2)==0,
   f"CONTROL (the fixed error): if F(0,Q)=K (loose), -F=-K gives d^2/dQ^2 = {Kkin_wrong} = -2 K2 < 0 = GHOST. "
   "=> the frozen candidate MUST use F(0,Q)=-2K(Q) (AeST). Corrected in FROZEN_CANDIDATE.md."))

# --- THE TRUE BOUNDARY IS Xi=0, NOT Y=0 (Carl's final result) ---
# Xi = chi^2 nu - (2(2-K_B)/K_B + mu)|A|^2 [2307.15126 Eq.32]. On the aligned background A_i=0, chi=1 => Xi=nu.
nu_full = sp.simplify(-sp.diff(Fcal0,Q)/(2*Q))       # nu = -F_Q/(2Q) = 2K2(Q-Q0)/Q
Xi_aligned = nu_full                                  # Xi = nu at A_i=0
F.append(ok(sp.simplify(nu_full - 2*K2*(Q-Q0)/Q)==0,
   f"aligned A_i=0: Xi = nu = {sp.simplify(nu_full)} = 2K2(Q-Q0)/Q"))
F.append(ok(sp.simplify(Xi_aligned.subs(Q,Q0))==0 and sp.simplify(Xi_aligned.subs(Q, 2*Q0))!=0,
   "=> Xi = 0 ONLY at Q=Q0 (the K-minimum / cosmological condensate); Xi != 0 for Q != Q0. So on the Y=0"))
P("        LOCUS: only the single point Q=Q0 sits on the Xi=0 boundary; all Y=0, Q!=Q0 configs have Xi!=0 and")
P("        are INSIDE the 6-DOF theorem. And even at Q=Q0 the PHYSICAL kinetics (F_QQ=-4K2, spatial 2(2-K_B))")
P("        are finite nonzero => Xi=0 there is an AUXILIARY-chart boundary, not a physical pathology.")
P("        => THE TRUE BOUNDARY OF D_phys IS Xi=0, NOT Y=0. (Both F_YY->inf and Xi->0 at the cosmological")
P("        point are auxiliary-chart degeneracies; the physical velocity Hessian is regular.)")

P("\n"+"="*94)
nf=F.count(False)
if nf==0:
    P("RESULT: at the homogeneous Y=0, Q=Q0 background (AeST convention K=-1/2 F(0,Q)):")
    P("  auxiliary nu(Q0)=0  BUT  physical F_QQ=-4K2 != 0  =>  scalar time-kinetic = +4K2 > 0 (HEALTHY).")
    P("  Combined with the spatial sector H_phys,space = 2(2-K_B)I > 0 (y0_physical_hessian.py), the Y=0")
    P("  physical scalar is NONDEGENERATE in BOTH temporal (4K2) and spatial (2(2-K_B)) sectors.")
    P("  => auxiliary-Legendre rank loss (nu->0, U_mumu->0) is NON-PHYSICAL; the physical kinetic rank is intact.")
    P("  UPGRADE: Y=0 physical kinetic nondegeneracy = CLOSED (both sectors). Still OPEN: the full arbitrary-Y=0")
    P("  operator-valued Dirac rank over the coupled (q_ij,A_i,phi) sector (research-grade).")
else:
    P(f"  {nf} check(s) FAILED.")
import sys; sys.exit(0 if nf==0 else 1)
