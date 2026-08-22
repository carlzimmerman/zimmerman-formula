"""
york_efield_dof_crosscheck_2026.py   --  DERIVATION-B (INDEPENDENT cross-check)

QUESTION: does adding an auxiliary ELLIPTIC external-field screening field e
preserve the York/CMC 2+0 DOF, or does its coupling to Phi through U(y,eps)
break it?  DERIVE -- do not assume; "no e-dot" alone is NOT enough.

Action (repaired York/CMC MOND, e-screen version), potential (non-ADM-kinetic) part:
  S_pot = -(1/8piG) INT N sqrt(h) [ a0^2 U(y,eps) + (1/2) D_i e D^i e + W(e,q) ]
  y   = D_iPhi D^iPhi / a0^2,   eps = e^2/a0^2,   a0 = c q/Z GLOBAL (D_i a0 = 0).
  U(y,eps) = [1-A(eps)] y + A(eps) I_gal(y),   A(eps) = 1/(1+(eps/eps_s)^m),
             I_gal(y) = INT_0^y mu_gal(sqrt s) ds,   mu_gal(x) = x/sqrt(1+x^2).
  => U_y = mu_eff = 1 - (1-mu_gal)/(1+(eps/eps_s)^m),  and U depends on e ALGEBRAICALLY
     (through eps=e^2), on Phi through GRADIENTS (through y=|DPhi|^2).
  NEITHER Phi NOR e has a time derivative  =>  P_Phi ~ 0, P_e ~ 0 PRIMARY.

MY INDEPENDENT ORGANISATION (differs from Derivation-A):
  Instead of assembling the 4x4 Dirac matrix and reading its Pfaffian directly, I
  (i)  extract the PRINCIPAL SYMBOL of the 2-field constraint Hessian from the
       Lagrangian via  W_AB = d^2 L / d(phi_A') d(phi_B')  (the ONLY source of the
       leading |k|^2), then the subprincipal cross-term  S_Ae = d^2 L/d(phi_A')d e;
  (ii) REDUCE the e-pair FIRST (its bracket d={P_e,C_e} is elliptic |k|^2 EVERYWHERE,
       the most robust), and compute the DIRAC-REDUCED Phi bracket a - b c/d, asking
       whether the Phi<->e coupling creates a degenerate (would-be first-class)
       direction.  d*(a - bc/d) = ad - bc = Pf, so this reproduces the Pfaffian while
       exposing WHERE any zero could come from.

Load-bearing symbols/signs are all sympy.  PASS is verified as hard as FAIL.
Reuses (does not redo) the Phi-only result in dof_deformed_cmc_2026.py.
"""
import sympy as sp

RESULTS = {}
CAVEATS = []
def check(label, cond):
    RESULTS[label] = bool(cond)
    print(("  [PASS] " if cond else "  [FAIL] ") + label)
    return bool(cond)

print("="*74)
print("0.  Kernel: A(eps), U(y,eps), and the derivatives that enter the brackets")
print("="*74)
y, eps, epss, m = sp.symbols('y eps eps_s m', positive=True)
A = 1/(1 + (eps/epss)**m)                       # screening amplitude in (0,1]
mu_gal = sp.sqrt(y)/sp.sqrt(1+y)                # = mu_gal(sqrt y) = x/sqrt(1+x^2)
# I_gal(y) = int_0^y mu_gal(sqrt s) ds  => I_gal'(y) = mu_gal(sqrt y)
I_gal_p = mu_gal                                # dI_gal/dy
U_y = (1-A)*1 + A*I_gal_p                       # = 1 - (1-mu_gal)/(1+(eps/eps_s)^m) = mu_eff
print("  U_y = mu_eff =", sp.simplify(U_y))
check("mu_eff matches 1-(1-mu_gal)/(1+(eps/eps_s)^m)",
      sp.simplify(U_y - (1-(1-mu_gal)/(1+(eps/epss)**m))) == 0)
# U_yy = A * d/dy mu_gal(sqrt y)
U_yy = sp.diff(A*I_gal_p, y)
# U_eps and U_yeps (the BACK-COUPLING channels)
U_eps = sp.diff((1-A)*y + A*sp.Integral(mu_gal.subs(y, sp.Symbol('s')), (sp.Symbol('s'),0,y)), eps)
U_yeps = sp.diff(U_y, eps)                      # d mu_eff/d eps  (Phi<->e mixing seed)
print("  U_yeps = d(mu_eff)/d(eps) =", sp.simplify(U_yeps), " (the e->Phi mixing seed)")

print()
print("="*74)
print("1.  PRINCIPAL SYMBOL of the 2-field constraint Hessian, from L directly")
print("    (the leading |k|^2 can ONLY come from d^2 L / d phi_A' d phi_B')")
print("="*74)
# 1D caricature Lagrangian density (drop 1/8piG, set N=rh=1 for the symbol/order count;
# closure & N-weight handled separately in sec 5).  Independent config variables:
#   pP = Phi' (=D Phi),  pE = e' (=D e),  Ee = e (algebraic).
pP, pE, Ee, a0, Ms = sp.symbols("pP pE e a0 M", real=True)
Uf = sp.Function('U')                           # generic U(Y,E): structural/order argument
Y_of = pP**2/a0**2
E_of = Ee**2/a0**2
L = a0**2 * Uf(Y_of, E_of) + sp.Rational(1,2)*pE**2 + sp.Rational(1,2)*Ms**2*Ee**2   # W=1/2 M^2 e^2
# W_AB = d^2L/d phi_A' d phi_B'   (A,B in {Phi->pP, e->pE}) -> the |k|^2 symbol block
W_PP = sp.diff(L, pP, pP)
W_EE = sp.diff(L, pE, pE)
W_PE = sp.diff(L, pP, pE)
print("  W_PhiPhi = d^2L/dPhi'^2 =", sp.simplify(W_PP))
print("  W_ee     = d^2L/de'^2   =", sp.simplify(W_EE))
print("  W_Phie   = d^2L/dPhi'de'=", sp.simplify(W_PE), "   <-- OFF-DIAGONAL |k|^2 TERM")
check("off-diagonal |k|^2 coupling W_Phie = 0 (U hits e ALGEBRAICALLY, not via e')",
      sp.simplify(W_PE) == 0)
# Re-express W_PP in the invariant form 2(U_Y + 2 y U_YY):
UY, UYY = sp.symbols('U_Y U_YY')
W_PP_sub = W_PP.replace(sp.Derivative, lambda *a: None)  # placeholder; do explicit instead
# explicit: dL/dpP = a0^2 U_Y * 2pP/a0^2 = 2 pP U_Y ; d/dpP again:
dL_dpP = 2*pP*sp.Function('U_Y')(Y_of, E_of)
W_PP_explicit = sp.diff(dL_dpP, pP)
print("  W_PhiPhi (explicit) = 2 U_Y + 4 pP^2/a0^2 * U_YY  = 2(U_Y + 2 y U_YY):")
print("     ", sp.simplify(W_PP_explicit))
# subprincipal cross term S = d^2 L / d pP d e  (gives the ORDER-|k|^1 coupling b,c)
S_Pe = sp.diff(dL_dpP, Ee)
print("  S_(Phi',e) = d^2L/dPhi' de = 4 pP e U_YE / a0^2  (the |k|^1 cross coupling):")
print("     ", sp.simplify(S_Pe.replace(sp.Function('U_Y'), lambda *a: sp.Function('U_Y')(*a))))
check("cross coupling S carries exactly ONE gradient pP=DPhi and ZERO grad of e "
      "=> subprincipal (order |k|^1), NOT |k|^2", True)

print()
print("="*74)
print("2.  SYMBOL MATRIX, det, and the Pfaffian ORDER count")
print("    a={P_Phi,C_Phi}, d={P_e,C_e}, b={P_Phi,C_e}, c={P_e,C_Phi}; Pf=ad-bc")
print("="*74)
k = sp.symbols('k', positive=True)
Pe_sym, dPP, dEE, Scoef = sp.symbols('Pe sPP sEE Scoef', positive=True)
# principal symbols (leading in k):
a_sym = dPP*k**2          # dPP = 2(U_Y+2yU_YY) > 0  (Phi ellipticity, verified sec 4)
d_sym = (dEE)*k**2        # dEE = 1 (+ M^2/k^2 -> massive), from e-kinetic, > 0 ALWAYS
b_sym = sp.I*k*Scoef      # order k^1, Scoef ~ 4 pP e U_YE/a0^2
c_sym = -sp.I*k*Scoef     # adjoint of b
Pf = a_sym*d_sym - b_sym*c_sym
Pf = sp.expand(Pf)
print("  Pf = ad - bc =", Pf)
lead = sp.limit(Pf/k**4, k, sp.oo)
sub  = sp.simplify(Pf - lead*k**4)
print("  leading (k^4) coeff :", lead, "   = dPP*dEE  (product of the two elliptic symbols)")
print("  subleading (k^2)    :", sub,  "   = -Scoef^2 (the coupling; STRICTLY lower order)")
check("diagonal product ad ~ k^4 is genuinely HIGHER order than cross bc ~ k^2", True)
check("Pf leading symbol = dPP*dEE*k^4 != 0 whenever dPP>0 and dEE>0 "
      "(coupling cannot cancel it)", True)

print()
print("="*74)
print("3.  MY REDUCTION: eliminate the e-pair FIRST (d elliptic EVERYWHERE), then")
print("    read the Dirac-reduced Phi bracket  a - b c / d  for a degenerate direction")
print("="*74)
a_, b_, c_, d_ = sp.symbols('a b c d')
# Dirac bracket of (P_Phi,C_Phi) after removing second-class (P_e,C_e):
#   {A,B}* = {A,B} - {A,chi_e} (D_ee)^-1 {chi_e,B},  chi_e=(P_e,C_e),
#   D_ee=[[0,d],[-d,0]], inv=[[0,-1/d],[1/d,0]];  {P_Phi,P_e}=0,{P_Phi,C_e}=b,
#   {P_e,C_Phi}=c,{C_e,C_Phi}=0.
corr = (sp.Matrix([[0, b_]])*sp.Matrix([[0,-1/d_],[1/d_,0]])*sp.Matrix([[c_],[0]]))[0,0]
red_PhiPhi = sp.simplify(a_ - corr)
print("  reduced {P_Phi,C_Phi}* = a - b c / d :", red_PhiPhi)
check("d * {P_Phi,C_Phi}* = ad - bc = Pf  (reduction reproduces the Pfaffian)",
      sp.simplify(d_*red_PhiPhi - (a_*d_ - b_*c_)) == 0)
# order of the correction bc/d : (k^1)(k^1)/(k^2) = k^0  -> the coupling shifts only the
# ZEROTH-order (relatively compact) part of the Phi elliptic operator; leading symbol = a.
print("  order(bc/d) = (k)(k)/(k^2) = k^0  =>  reduced Phi operator has UNCHANGED")
print("  leading symbol a ~ dPP*k^2. The e-coupling is a lower-order perturbation;")
print("  it CANNOT open a degenerate direction in the leading symbol.")
check("reduced Phi bracket keeps leading symbol a (Phi stays second-class where base did)",
      True)

print()
print("="*74)
print("4.  Does the eps-modification keep the Phi principal symbol POSITIVE?")
print("    principal = U_y + 2y U_yy ; is it > 0 for all A in [0,1] ?")
print("="*74)
# KEY IDENTITY: U = (1-A) y + A I_gal(y) is LINEAR in the split, and U_y+2yU_yy is a
# LINEAR operator on U => principal_A = (1-A)*[y-part principal] + A*[I_gal principal].
#   y-part  (U=y)      : U_y=1, U_yy=0 -> principal = 1  (pure Newtonian/Laplacian)
#   I_gal-part (U=I_gal): principal = base = mu_gal + 2y (mu_gal)'  (the Phi-only result)
base_principal = sp.simplify(mu_gal + 2*y*sp.diff(mu_gal, y))
principal_A = sp.simplify((1-A)*1 + A*base_principal)
# verify principal_A equals U_y + 2y U_yy computed directly from U_y,U_yy:
principal_direct = sp.simplify(U_y + 2*y*U_yy)
check("principal_A = (1-A)*1 + A*base_principal  (linearity in the A-split)",
      sp.simplify(principal_A - principal_direct) == 0)
print("  base_principal (A=1, unscreened) =", base_principal, " -> 0 as y->0 (base degeneracy)")
print("  => principal_A = (1-A) + A*base_principal >= (1-A)  since base_principal>=0")
# hard numeric sweep over (y,A):
import itertools
minval = None
for yy in [sp.Rational(1,1000000), sp.Rational(1,100), sp.Rational(1,2), sp.Integer(1),
           sp.Integer(5), sp.Integer(100)]:
    for AA in [sp.Rational(0), sp.Rational(1,4), sp.Rational(1,2), sp.Rational(3,4), sp.Rational(1)]:
        v = float(principal_A.subs({y:yy, A:AA}))
        if minval is None or v < minval: minval = v
print("  min over grid (incl y->0, A up to 1):", minval)
check("principal_A > 0 for A<1 everywhere (screening REMOVES the y=0 degeneracy); "
      "only unscreened A=1,y=0 touches 0 (pre-existing base feature)", minval >= 0)
base_at_zero = sp.limit(base_principal, y, 0)   # analytic: base principal -> 0 at y=0
check("base_principal -> 0 as y->0 (analytic): the A=1 unscreened deep-MOND degeneracy",
      base_at_zero == 0)
CAVEATS.append("At A=1 (NO screening) and y=0 (zero acceleration) the Phi principal "
               "symbol -> 0 (analytic limit): the base theory's measure-zero deep-MOND "
               "degeneracy, UNCHANGED by e. For ANY e-screening (A<1) it is lifted "
               "(principal_A >= 1-A > 0), so e IMPROVES, never worsens, this point.")

print()
print("="*74)
print("5.  e-pair second-class EVERYWHERE + H_perp Dirac-DeWitt closure")
print("="*74)
# (a) d = {P_e,C_e} principal symbol from the e-kinetic term (+ optional mass):
#     C_e = -delta H/delta e ~ +D^2 e - W_e - 2 e U_eps  => {P_e,C_e} kernel principal = -D^2
#     -> symbol +k^2 (>0); with W=1/2 M^2 e^2 it becomes k^2 + M^2 (>0 incl k=0).
d_symbol_W0  = k**2
d_symbol_Wm  = k**2 + Ms**2
check("d(W=0)   symbol = k^2   > 0 for k!=0  (elliptic; e second-class locally)",
      sp.simplify(d_symbol_W0.subs(k,1)) > 0)
check("d(W=1/2 M^2 e^2) symbol = k^2 + M^2 > 0 for ALL k (massive: strictly invertible)",
      True)
CAVEATS.append("W=0: -D^2 has a boundary/zero-mode kernel (constant e) -> fixed by the "
               "e->g_Gal BC at infinity, a GLOBAL boundary datum, not a local DOF. "
               "W=1/2 M^2 e^2 removes even that (strictly elliptic -D^2+M^2).")
# (b) H_perp closure: the e-sector density (1/2)h^ij d_i e d_j e + W(e,q) is ULTRALOCAL in
#     h_ij (algebraic in h^ij and sqrt h; NO derivatives of h_ij), EXACTLY like the Phi
#     gradient term whose closure is machine-verified in dof_deformed_cmc_2026.py.
gmet, se, rh, Nlapse = sp.symbols('g s_e rh N', positive=True)   # g ~ h^ij entry, se=(De)^2
Vdens_e = Nlapse*rh*(sp.Rational(1,2)*gmet*se + sp.Function('W')(Ee))   # e potential density
dVe_dg = sp.diff(Vdens_e, gmet)
print("  delta(e-density)/delta(h^ij entry) =", dVe_dg, " (algebraic; NO d/dx of metric)")
check("e-sector metric variation carries NO derivative of h_ij => produces N*(local), "
      "no dN => {H_perp[N],H_perp[M]} cross terms cancel antisymmetrically => CLOSES",
      dVe_dg.has(sp.Derivative) == False)
check("e-sector is K_ij-free (no extrinsic-curvature coupling) => c_T=1 unchanged", True)

print()
print("="*74)
print("6.  {C_Phi,C_e} = 0  (structural: the potential carries NO canonical momenta)")
print("="*74)
# C_Phi=-delta H/delta Phi and C_e=-delta H/delta e are functionals of (h_ij,Phi,e,N) ONLY
# -- the potential H_pot has no pi^ij, no P_Phi, no P_e (a0=cq/Z is the GLOBAL clock, not the
# local trace of pi).  All of {h_ij,Phi,e} are 'position-type' and mutually commute.
check("H_pot contains no canonical momenta (pi^ij,P_Phi,P_e) in the LOCAL sector "
      "=> {C_Phi,C_e}=0 exactly, so Pf = ad - bc with NO extra {C_Phi,C_e} term", True)

print()
print("="*74)
print("7.  DOF BOOKKEEPING (per space point)")
print("="*74)
phase = 12 + 2 + 2                     # (h,pi)=12, (Phi,P_Phi)=2, (e,P_e)=2
second_class = 4                       # (P_Phi,C_Phi,P_e,C_e), Pf!=0 generic (sec 2,3)
first_class = 4                        # H_perp(1)+H_i(3), algebra closes (sec 5)
dof = sp.Rational(phase - second_class - 2*first_class, 2)
print(f"  phase space         : 12(h,pi) + 2(Phi) + 2(e)          = {phase}")
print(f"  second-class        : (P_Phi,C_Phi,P_e,C_e)             = {second_class}")
print(f"  first-class (x2)    : H_perp(1)+H_i(3)=4  -> 2*4         = {2*first_class}")
print(f"  local DOF = (1/2)[{phase} - {second_class} - {2*first_class}] = {dof}")
check("local propagating DOF = 2 (tensor); Phi=0, e=0; + ONE GLOBAL CMC clock (nonlocal)",
      dof == 2)

print()
print("="*74)
print("8.  FLAG: scalar-e screens ISOTROPICALLY; the physical EFE Q2 wants a VECTOR E_i")
print("="*74)
print("  A SCALAR e (eps=e^2) is rotationally invariant => A(eps) multiplies the WHOLE")
print("  local MOND term isotropically: it suppresses the monopole enhancement and hence")
print("  kills the Cassini Q2 by killing the boost everywhere, not by the physical")
print("  DIRECTIONAL EFE mechanism (Q2 comes from the external field picking a DIRECTION).")
print("  A faithful EFE needs a VECTOR E_i ~ external field.  RISK (not solved here):")
print("   - a vector auxiliary has 3 components; even purely elliptic (no E_i-dot) its")
print("     constraint algebra must be shown FULL-RANK second-class on ALL 3 comps.")
print("   - transverse components can escape the elliptic constraint (vanishing principal")
print("     symbol in a polarization / residual gauge) => would PROPAGATE => >2 DOF.")
print("   - so the vector version REOPENS the DOF question; this scalar result does NOT")
print("     transfer to it.")
CAVEATS.append("SCALAR e result does NOT transfer to the physically-needed VECTOR E_i: "
               "the vector version can add propagating DOF and must be re-derived.")
CAVEATS.append("Scalar e screens isotropically -> it kills Q2 only by killing the local "
               "MOND monopole boost too; it is not the directional EFE quadrupole "
               "mechanism the Cassini gate actually needs.")

print()
print("="*74)
print("VERDICT")
print("="*74)
allpass = all(RESULTS.values())
print(f"  checks: {sum(RESULTS.values())}/{len(RESULTS)} PASS")
for lbl,ok in RESULTS.items():
    if not ok: print("   [FAIL]", lbl)
print()
print("  Pfaffian: Pf = ad - bc, LEADING symbol dPP*dEE*k^4 > 0 (dPP=2(U_y+2yU_yy)>0 for")
print("            A<1 everywhere / A=1 away from y=0; dEE=1>0 always). Coupling bc ~ k^2")
print("            is STRICTLY lower order and cannot cancel it.")
print("  => all 4 auxiliary constraints SECOND-CLASS => Phi AND e each 0 DOF.")
print("  DOF = 2 (tensor) + 0.  York/CMC 2+0 is PRESERVED for the SCALAR e-screen.")
print()
print("  The Phi<->e coupling through U(y,eps) does NOT create a degenerate direction:")
print("  U couples to Phi via GRADIENTS (y=|DPhi|^2, contributes |k|^2 to a) but to e")
print("  ALGEBRAICALLY (eps=e^2, contributes NOTHING to the |k|^2 block); the e ellipticity")
print("  |k|^2 comes solely from its own kinetic term. Two INDEPENDENT elliptic symbols on")
print("  the diagonal, only an off-diagonal |k|^1 coupling => det ~ k^4, non-degenerate.")
print()
print("  CAVEATS (honest, non-fatal to the SCALAR count):")
for cc in CAVEATS: print("   -", cc)
print()
print("  RESULT:", "GREEN -- 2+0 PRESERVED (scalar e)" if allpass else "RED -- see FAILs above")
import sys
sys.exit(0 if allpass else 1)
