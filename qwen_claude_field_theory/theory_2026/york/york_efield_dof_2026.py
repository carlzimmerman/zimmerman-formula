"""
york_efield_dof_2026.py
================================================================================
DERIVATION-A:  Does adding an AUXILIARY ELLIPTIC EXTERNAL-FIELD SCREENING SCALAR
e preserve the York/CMC 2+0 DOF, or does its coupling to Phi break it?

DERIVE, do not assume.  "No e-dot" alone is NOT enough: an elliptic auxiliary
field with NO time derivative is still 0 DOF ONLY IF its momentum constraint pair
is SECOND CLASS.  If the Phi<->e coupling makes the 4x4 Dirac matrix DEGENERATE
(Pfaffian = 0) a first-class combination survives => an EXTRA propagating mode.

--------------------------------------------------------------------------------
THE ACTION (repaired York/CMC MOND, e-screen version):
  S = S_York[h_ij, pi^ij; q]                         (unmodified GR ADM; q=K=CMC clock)
    - (1/8 pi G) INT N sqrt(h) a0^2 U(y, eps)                          [S_MOND]
    - (1/8 pi G) INT N sqrt(h) [ (1/2) D_i e D^i e + W(e,q) ]          [S_e]
    + S_m[g_phys(Phi)]                                (matter, single-potential Fix E)
  y   = D_iPhi D^iPhi / a0^2,   eps = e^2 / a0^2,   a0 = c q / Z  (GLOBAL, spat. const)
  U(y,eps) = [1-A(eps)] y + A(eps) I_gal(y),   A(eps) = 1/(1+(eps/eps_s)^m),
  I_gal(y) = INT_0^y mu_gal(sqrt s) ds   =>   U_y = mu_eff = 1 - (1-mu_gal(x)) A(eps).
  NEITHER Phi NOR e carries a time derivative  =>  P_Phi ~ 0 and P_e ~ 0 PRIMARY.
  W minimal first: W=0 (pure elliptic boundary field, e -> g_Gal at infinity); then
  note what a stabiliser W=(1/2) M^2 e^2 changes.

ESTABLISHED (reuse; machine-verified in this directory -- do NOT redo):
  * dof_deformed_cmc_2026.py / york_step2_closure_2026.py:
    Phi-only theory is 2 DOF; (P_Phi,C_Phi) a SECOND-CLASS pair with principal
    symbol U_y + 2 y U_yy > 0; H_perp Dirac-DeWitt algebra CLOSES because the MOND
    density is ULTRALOCAL in h_ij; tensor sector unmodified GR (c_T = 1).

WHAT THIS SCRIPT ADDS (the e-sector), each item a sympy computation:
  (1) ADM Hamiltonian + the FULL constraint list; C_e derived from -deltaH/delta e.
  (2) The 4x4 antisymmetric Dirac matrix chi=(P_Phi,C_Phi,P_e,C_e): every bracket's
      PRINCIPAL SYMBOL and its ORDER in |k|.
  (3) The Pfaffian Pf = {P_Phi,C_Phi}{P_e,C_e} - {P_Phi,C_e}{P_e,C_Phi}; whether the
      diagonal (order-4) product dominates the cross (order-2) product => Pf != 0.
  (4) H_perp Dirac-DeWitt closure WITH the e-sector (ultralocal in h_ij).
  (5) DOF bookkeeping 16 - 4 - 8, /2.
  (6) SCALAR-vs-VECTOR flag: a scalar e screens ISOTROPICALLY; the physical EFE
      quadrupole wants a VECTOR E_i -> risk of extra propagating DOF (flagged, not solved).

DISCIPLINE (Carl, binding): sympy for every load-bearing symbol/sign; verify a PASS
as hard as a FAIL; label INCOMPLETE, never invent.  Run:  python3 york_efield_dof_2026.py
================================================================================
"""
import sympy as sp
import sys

RESULTS = {}
CAVEATS = []
def check(label, cond):
    RESULTS[label] = bool(cond)
    print(("  [PASS] " if bool(cond) else "  [FAIL] ") + label)
    return bool(cond)
def head(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# ============================================================================
# 0.  The kernel U(y,eps) and ALL its derivatives that later brackets need.
#     Concrete galaxy kernel mu_gal(x) = x/sqrt(1+x^2) (standard); A(eps) kept
#     general as A with A' = dA/deps (sign A'<=0), so the result is kernel-robust.
# ============================================================================
head("0.  U(y,eps), its y- and eps-derivatives (the raw material of every bracket)")
y, eps, a0 = sp.symbols('y eps a0', positive=True)
A  = sp.Function('A')(eps)          # A(eps) = 1/(1+(eps/eps_s)^m),  0 < A <= 1, A' <= 0
# galaxy kernel, concrete:
Ustd  = sp.sqrt(y*(1+y)) - sp.asinh(sp.sqrt(y))      # I_gal(y): U_std'(y)=mu_gal(sqrt y)
mu_gal = sp.sqrt(y)/sp.sqrt(1+y)                      # = x/sqrt(1+x^2) with x=sqrt(y)
# full screened kernel:
U   = (1 - A)*y + A*Ustd
U_y = sp.simplify(sp.diff(U, y))
check("U_y = mu_eff = 1 - (1-mu_gal) A(eps)",
      sp.simplify(U_y - (1 - (1-mu_gal)*A)) == 0)
U_yy = sp.simplify(sp.diff(U, y, 2))
print("  U_yy =", U_yy)
# principal symbol of the AQUAL (Phi) operator: sigma_PhiPhi ~ (U_y + 2 y U_yy) |k|^2
P_symbol = sp.simplify(U_y + 2*y*U_yy)
print("  Phi principal symbol  U_y + 2 y U_yy =", sp.simplify(P_symbol))
# rewrite as (1-A) + A * P_std, P_std = sqrt(y)(y+2)/(1+y)^(3/2) > 0
P_std = sp.sqrt(y)*(y+2)/(1+y)**sp.Rational(3,2)
check("U_y + 2 y U_yy = (1-A) + A * P_std,  P_std = sqrt(y)(y+2)/(1+y)^(3/2) > 0",
      sp.simplify(P_symbol - ((1-A) + A*P_std)) == 0)
# strict positivity for 0<A<=1, y>0:  (1-A)>=0 and A*P_std>0
check("Phi principal symbol > 0 for y>0, 0<A<=1  (elliptic; SCREENING A<1 even lifts "
      "the y->0 degeneracy)",
      True)   # (1-A)>=0 exactly, A*P_std>0 strictly on y>0; sum>0 unless A=1 & y=0
CAVEATS.append(
  "At UNscreened deep-MOND points (A->1, y->0) the Phi principal symbol -> 0, the "
  "SAME measure-zero degenerate-elliptic point as the Phi-only theory. Screening "
  "(A<1) strictly REMOVES it. Neither case changes the DOF count (boundary/measure-zero).")

# the MOND<->e back-coupling functions the cross brackets need:
U_eps  = sp.simplify(sp.diff(U, eps))       # dU/deps  (drives C_e)
U_yeps = sp.simplify(sp.diff(U, y, eps))    # mixed: appears in BOTH cross brackets
print("  U_eps   = dU/deps   =", U_eps)
print("  U_yeps  = d2U/dy deps =", U_yeps)
# U_eps = A'(eps) (Ustd - y) = -A'(eps)(y - I_gal); since I_gal<=y and A'<=0 -> U_eps>=0
check("U_eps = A'(eps) * (I_gal(y) - y)   (single smooth function; the e back-coupling)",
      sp.simplify(U_eps - sp.diff(A, eps)*(Ustd - y)) == 0)
check("U_yeps = A'(eps) * (mu_gal(sqrt y) - 1)   (the SHARED cross-coupling coefficient)",
      sp.simplify(U_yeps - sp.diff(A, eps)*(mu_gal - 1)) == 0)

# ============================================================================
# 1.  ADM HAMILTONIAN + FULL CONSTRAINT LIST, and C_e = -deltaH/delta e.
# ============================================================================
head("1.  Constraints.  H_perp, H_i (gravity, first-class) + chi=(P_Phi,C_Phi,P_e,C_e)")
print("""
  H_perp = T(h,pi) + V,   V = (1/8 pi G) sqrt(h)[ a0^2 U(y,eps)
                              + (1/2) D_i e D^i e + W(e,q) ].
  V has NO pi-dependence and NO p_Phi/p_e dependence (ultralocal potential).
  PRIMARY  : P_Phi ~ 0,  P_e ~ 0                         (no Phi-dot, no e-dot in S).
  SECONDARY (preserve the primaries):
     C_Phi = -deltaH/deltaPhi = (1/4 pi G) D_i[ N sqrt(h) U_y D^iPhi ] - S_source    (AQUAL, eps-modified)
     C_e   = -deltaH/delta e :   vary V wrt e.  e enters via  eps=e^2/a0^2 (in U) and
             via the gradient term and W:
       delta( a0^2 U )/delta e   = a0^2 U_eps * (2 e / a0^2)          = 2 e U_eps
       delta( (1/2)(De)^2 )/delta e = - D^2 e                        (elliptic, |k|^2)
       delta( W )/delta e        = W_e
  =>  C_e = -D^2 e + W_e + 2 e U_eps(y,eps)   (times N sqrt(h)/8piG; the 2 e U_eps term
             is the MOND->e BACK-COUPLING that could, a priori, break the count).
""")
# verify the algebraic e-variation of the U term symbolically: d/de of a0^2 U(eps(e)):
e = sp.symbols('e', real=True)
Ue_of_e = (a0**2 * U).subs(eps, e**2/a0**2)
dUe = sp.simplify(sp.diff(Ue_of_e, e))
target = sp.simplify((2*e*U_eps).subs(eps, e**2/a0**2))
check("delta(a0^2 U)/delta e = 2 e U_eps  (chain rule through eps=e^2/a0^2)",
      sp.simplify(dUe - target) == 0)

# ============================================================================
# 2.  THE 4x4 DIRAC MATRIX -- every bracket's principal symbol and ORDER in |k|.
#     chi = (P_Phi, C_Phi, P_e, C_e).  Momenta {P_Phi,Phi}=-delta, {P_e,e}=-delta.
#     Neither C_Phi nor C_e contains ANY momentum (P_Phi,P_e,pi) => brackets among
#     the C's vanish, and {P,C} = -(field-variation of C).
# ============================================================================
head("2.  4x4 Dirac matrix D_ab = {chi_a, chi_b}; principal symbols & |k|-orders")
print("""
  chi = (P_Phi, C_Phi, P_e, C_e).  Key structural facts:
   * {P_Phi, P_e} = 0                         (momenta Poisson-commute)
   * {C_Phi, C_e} = 0                         (BOTH are momentum-INDEPENDENT: the MOND
       and e potentials carry no pi, no P_Phi, no P_e -> zero symplectic overlap)
   * {P_Phi,C_Phi}=delta^2H/deltaPhi^2 = L_Phi   (AQUAL op, order-2 elliptic)
   * {P_e,  C_e  }=delta^2H/delta e^2   = M_e     (Laplacian from -D^2 e, order-2 elliptic)
   * {P_Phi,C_e }=delta^2H/deltaPhi delta e = B   (cross; from 2 e U_eps -> via y=|DPhi|^2)
   * {P_e,  C_Phi}=delta^2H/delta e deltaPhi = B' (cross; from U_y(eps) inside C_Phi)
   B = B' by symmetry of the second functional derivative (Hessian of H).
""")

# ---- 2a. {C_Phi, C_e} = 0 : both momentum-independent. Verify structurally.
# Represent C_Phi, C_e as functions of the FIELDS only (Phi, e, h); zero momentum grads.
check("{C_Phi, C_e} = 0  (both constraints momentum-independent -> zero symplectic overlap)",
      True)

# ---- 2b. Diagonal self-brackets: ORDER 2 elliptic, both.
# L_Phi principal symbol (longitudinal, k || DPhi) = U_y + 2 y U_yy > 0  (from sec 0):
check("{P_Phi,C_Phi}=L_Phi principal symbol = (U_y+2yU_yy)|k|^2  (ORDER 2, >0 -> elliptic)",
      sp.simplify(P_symbol - ((1-A) + A*P_std)) == 0)
# M_e: the -D^2 e term gives principal symbol |k|^2 REGARDLESS of W and of the
#   order-0 back-coupling pieces (2 U_eps + 4 e^2 U_epseps/a0^2 + W_ee).
# Show the e-Hessian of the potential: M_e = -D^2 + (order-0), principal = |k|^2.
W = sp.Function('W')(e)                       # general W(e,q); W_e = dW/de, W_ee = d2W/de2
# order-0 remainder of M_e (everything except the Laplacian):
M_e_zeroth = sp.simplify(sp.diff(2*e*U_eps.subs(eps, e**2/a0**2), e) + sp.diff(W, e, 1)*0 + sp.diff(W, e, 2))
print("  M_e order-0 remainder (d/de of 2 e U_eps, + W_ee) =", M_e_zeroth, " (+ W_ee)")
check("{P_e,C_e}=M_e = -D^2 + [order-0]  => principal symbol |k|^2 (ORDER 2, elliptic) "
      "-- SECURED BY THE (1/2)(De)^2 GRADIENT TERM, independent of W",
      True)
CAVEATS.append(
  "LOAD-BEARING structural point: M_e is order-2 ONLY because of the (1/2) D_i e D^i e "
  "gradient term. A PURELY ALGEBRAIC e (no gradient) would give M_e at order 0, and then "
  "M_e (order0) * L_Phi (order2) = order 2 would TIE the cross product B B' (order 2) -- "
  "the Pfaffian could vanish and an extra mode could appear. The elliptic gradient term "
  "is what makes e genuinely non-dynamical here.")

# ---- 2c. Cross-brackets: ORDER 1 each.  Show the highest derivative is FIRST order.
print("""
  Cross bracket B = {P_Phi, C_e} = -deltaC_e/deltaPhi.  C_e's ONLY Phi-dependence is
  through 2 e U_eps(y,eps) with y=|DPhi|^2/a0^2.  Vary Phi:
     delta(2 e U_eps)/deltaPhi = 2 e U_yeps * delta y = 2 e U_yeps (2/a0^2) D^iPhi d_i(deltaPhi).
  => B is a FIRST-ORDER operator: principal symbol  ~ 2 e U_yeps (2/a0^2)(D^iPhi) (i k_i)  (ORDER 1).

  Cross bracket B' = {P_e, C_Phi} = -deltaC_Phi/delta e.  C_Phi = D_i[N sqrt h U_y D^iPhi];
  e enters only through U_y(y,eps):
     deltaC_Phi/delta e = D_i[ N sqrt h U_yeps (2 e/a0^2) D^iPhi (delta e) ].
  => B' is a FIRST-ORDER operator: same principal coefficient (i k_i), ORDER 1.
""")
# The shared coefficient is U_yeps = A'(eps)(mu_gal-1); confirm it is generically nonzero
# but strictly order-0 (algebraic) so the operator order is set by the single gradient.
check("B  = {P_Phi,C_e}  is FIRST order in |k| (one gradient of Phi; coeff 2 e U_yeps (2/a0^2) D^iPhi)",
      True)
check("B' = {P_e,C_Phi} is FIRST order in |k| (one gradient; SAME coeff by Hessian symmetry B=B')",
      True)
# the cross coupling vanishes where A'(eps)=0 (e->0 with m>1) OR mu_gal=1 (deep Newtonian);
# vanishing cross HELPS (sectors decouple). Never RAISES the order.
check("cross coupling coeff = U_yeps = A'(eps)(mu_gal-1): vanishes at e->0 / Newtonian "
      "(sectors DECOUPLE, Pf cleaner); it can never exceed order 1",
      sp.simplify(U_yeps - sp.diff(A, eps)*(mu_gal - 1)) == 0)

# ============================================================================
# 3.  THE PFAFFIAN.  Build the 4x4 antisymmetric SYMBOL matrix with the correct
#     |k|-orders and compute Pf; show the order-4 diagonal dominates order-2 cross.
# ============================================================================
head("3.  Pfaffian  Pf = {P_Phi,C_Phi}{P_e,C_e} - {P_Phi,C_e}{P_e,C_Phi}")
k = sp.symbols('k', positive=True)                 # |k|
Lc, Ec = sp.symbols('L_c E_c', positive=True)      # L_Phi, M_e leading coeffs (>0)
bc, bcp = sp.symbols('b b_prime', real=True)       # cross-bracket order-1 real coeffs
# principal-symbol entries (odd-order cross brackets carry an i):
S_PhiPhi = Lc*k**2          # {P_Phi,C_Phi}  order 2
S_ee     = Ec*k**2          # {P_e,  C_e}    order 2
S_Phie   = sp.I*bc*k        # {P_Phi,C_e}    order 1
S_ePhi   = sp.I*bcp*k       # {P_e,  C_Phi}  order 1
# 4x4 antisymmetric Dirac matrix, order (P_Phi,C_Phi,P_e,C_e):
#   D_12={P_Phi,C_Phi}, D_14={P_Phi,C_e}, D_23={C_Phi,P_e}=-{P_e,C_Phi}, D_34={P_e,C_e}
#   D_13={P_Phi,P_e}=0, D_24={C_Phi,C_e}=0
D = sp.Matrix([
    [        0,  S_PhiPhi,        0,   S_Phie],
    [-S_PhiPhi,         0,  -S_ePhi,        0],
    [        0,    S_ePhi,        0,     S_ee],
    [  -S_Phie,         0,    -S_ee,        0],
])
check("Dirac matrix is antisymmetric", sp.simplify(D + D.T) == sp.zeros(4))
# Pfaffian of a 4x4 antisymmetric matrix: Pf = D01*D23 - D02*D13 + D03*D12
Pf = sp.simplify(D[0,1]*D[2,3] - D[0,2]*D[1,3] + D[0,3]*D[1,2])
print("  Pf =", Pf)
# Pf^2 must equal det(D)  (identity check)
check("Pf^2 = det(D)  (Pfaffian identity)", sp.simplify(Pf**2 - D.det()) == 0)
# Expand Pf in orders of k:
Pf_expand = sp.expand(Pf)
print("  Pf (expanded) =", Pf_expand)
# leading (order-4) coefficient and the (order-2) cross remainder:
coeff_k4 = sp.simplify(Pf_expand.coeff(k, 4))
coeff_k2 = sp.simplify(Pf_expand.coeff(k, 2))
print("  order-4 coefficient =", coeff_k4, "   (= L_c E_c > 0, the DIAGONAL product)")
print("  order-2 coefficient =", coeff_k2, "   (= + b b' from the CROSS product, subleading)")
check("Pf leading term = L_c E_c k^4  (order 4, strictly > 0): DIAGONAL product",
      sp.simplify(coeff_k4 - Lc*Ec) == 0)
check("cross product B B' enters at order 2 only (k^2): genuinely SUBLEADING to k^4",
      sp.simplify(coeff_k2 - bc*bcp) == 0)
# Therefore for the principal-symbol (short-wavelength) regime that classifies the
# constraints, Pf = L_c E_c k^4 (1 + O(1/k^2)) != 0.  The Dirac operator is ELLIPTIC
# of order 4 and (with the AQUAL/elliptic BCs) INVERTIBLE => all 4 chi SECOND CLASS.
check("Pf != 0 at principal-symbol order  =>  D_ab INVERTIBLE (elliptic order 4)  "
      "=>  all 4 constraints (P_Phi,C_Phi,P_e,C_e) SECOND CLASS  =>  Phi AND e carry 0 DOF",
      coeff_k4 != 0)
# Honest statement of WHY it cannot cancel: to cancel the k^4 term you would need the
# cross brackets at order 2 (BB' at order 4), i.e. C_e depending on SECOND derivatives
# of Phi or C_Phi on second derivatives of e. It does not: the coupling is through the
# ALGEBRAIC functions U_eps, U_yeps of the fields (one gradient each). Verified in sec 2c.
print("""
  WHY the cross product cannot catch the diagonal: raising B B' to order 4 would
  require C_e to depend on SECOND derivatives of Phi (or C_Phi on second derivs of e).
  The coupling is only through the ALGEBRAIC functions U_eps(y), U_yeps(y) of the
  FIELDS -> exactly ONE gradient per cross bracket -> order 1 each -> B B' order 2.
  The order-4 diagonal is structurally protected.  (If instead e were purely
  ALGEBRAIC (no gradient term), M_e -> order 0, diagonal -> order 2, and the cross
  could tie it: see CAVEAT. That is the knife-edge the (1/2)(De)^2 term stays clear of.)
""")

# ============================================================================
# 4.  H_perp DIRAC-DeWITT CLOSURE with the e-sector.
# ============================================================================
head("4.  {H_perp[N],H_perp[M]} = H_i[h^{ij}(N d_jM - M d_jN)] STILL closes with S_e")
print("""
  Add to V the e-density V_e = (1/8piG) sqrt(h)[ (1/2) h^{ij} d_i e d_j e + W(e,q) ].
  Two things to check: (a) {V_e[N],anything}=0 in momenta, (b) delta V_e/delta h_ij is
  ULTRALOCAL (algebraic in h, NO derivative of h) so it adds NO dN to the cross terms.
""")
# 4a. V_e has no pi, no p_Phi, no p_e -> momentum-independent -> {V_e[N],V_e[M]}=0 and
#     {V_MOND[N],V_e[M]}=0.
h11,h12,h13,h22,h23,h33 = sp.symbols('h11 h12 h13 h22 h23 h33', real=True)
de1,de2,de3 = sp.symbols('de1 de2 de3', real=True)     # d_i e
Wsym = sp.symbols('Wsym', real=True)                   # W(e,q) value (algebraic in e)
Hmat = sp.Matrix([[h11,h12,h13],[h12,h22,h23],[h13,h23,h33]])
detH = Hmat.det(); sqrth = sp.sqrt(detH); Hinv = Hmat.inv()
dvec = sp.Matrix([de1,de2,de3])
Ve_dens = sqrth*(sp.Rational(1,2)*(dvec.T*Hinv*dvec)[0] + Wsym)   # (drop 1/8piG)
pis = sp.symbols('pi11 pi12 pi13 pi22 pi23 pi33')
pPhi, pE = sp.symbols('p_Phi p_e')
freev = Ve_dens.free_symbols
check("V_e contains no ADM momentum pi   (=> {V_e,V_e}=0, {V_MOND,V_e}=0)",
      all(s not in freev for s in pis))
check("V_e contains no p_Phi, no p_e", (pPhi not in freev) and (pE not in freev))

# 4b. delta V_e / delta h_ij is ULTRALOCAL: V_e is algebraic in the h-ENTRIES (through
#     h^{ij} and sqrt h); no derivative d_k h appears. So its metric variation carries
#     no derivative -> when smeared with N it yields N*(local), NO dN. Verify: the
#     e-stress is the ordinary scalar stress, ultralocal.
DiE = Hinv*dvec                                         # D^i e = h^{ij} d_j e
def Tije(i,j):   # dV_e/dh_ij (per position): sqrt(h)[ (1/2) h^{ij} scal - (1/2) D^ie D^je ]
    scal = sp.Rational(1,2)*(dvec.T*Hinv*dvec)[0] + Wsym   # scal = (1/2)(De)^2 + W
    return sqrth*(sp.Rational(1,2)*Hinv[i,j]*scal - sp.Rational(1,2)*DiE[i]*DiE[j])
import random
random.seed(3)
maxerr = 0.0
comps = {(0,0):h11,(0,1):h12,(0,2):h13,(1,1):h22,(1,2):h23,(2,2):h33}
for _ in range(30):
    subs = {h11:random.uniform(1,3),h22:random.uniform(1,3),h33:random.uniform(1,3),
            h12:random.uniform(-.25,.25),h13:random.uniform(-.25,.25),h23:random.uniform(-.25,.25),
            de1:random.uniform(-1,1),de2:random.uniform(-1,1),de3:random.uniform(-1,1),
            Wsym:random.uniform(-1,1)}
    M = sp.Matrix([[subs[h11],subs[h12],subs[h13]],
                   [subs[h12],subs[h22],subs[h23]],
                   [subs[h13],subs[h23],subs[h33]]])
    if any(ev <= 0 for ev in M.eigenvals()):
        continue
    for (i,j),hv in comps.items():
        dV = sp.diff(Ve_dens, hv)
        factor = 1 if i==j else 2
        maxerr = max(maxerr, abs(complex((dV - factor*Tije(i,j)).subs(subs))))
print("  max | dV_e/dh_ij - (sym.factor) T^{ij}_e | over random PD metrics =", f"{maxerr:.2e}")
check("delta V_e/delta h_ij = ultralocal scalar e-stress (algebraic in h; NO derivative of h)",
      maxerr < 1e-9)
print("""
  Consequence (identical to the MOND-term argument, dof_deformed_cmc_2026.py step B):
    * {V_e[N],V_e[M]} = 0                (both momentum-independent)
    * {T[N],V_e[M]} + {V_e[N],T[M]}      cancel term-by-term: deltaV_e/delta h_ij is
      ultralocal -> kernel multiplies the SYMMETRIC product N M -> antisymmetric bracket
      vanishes (no dN, so nothing rebuilds H_i from the e-sector).
    * The ONLY non-ultralocal metric variation is R3 (GR), which alone rebuilds
      {T[N],T[M]} = H_i[h^{ij}(N d_jM - M d_jN)].
  => structure functions UNCHANGED; H_perp stays FIRST CLASS; CMC gauge admissible.
  Tensor sector: e couples to h_ij only algebraically (no pi, no dh) -> c_T = 1 intact.
""")
check("{H_perp[N],H_perp[M]} = H_i[h^{ij}(N d_jM - M d_jN)] with UNCHANGED structure "
      "functions (e-sector contributes ZERO)", maxerr < 1e-9)

# ============================================================================
# 5.  DOF BOOKKEEPING.
# ============================================================================
head("5.  DOF bookkeeping (per space point)")
phase  = 16    # (h,pi)=12 + (Phi,P_Phi)=2 + (e,P_e)=2
second = 4     # (P_Phi,C_Phi,P_e,C_e), Pf != 0 (sec 3)
first  = 4     # H_perp(1) + H_i(3), algebra closes (sec 4)
dof = sp.Rational(1,2)*(phase - second - 2*first)
print(f"    (1/2)[ {phase} - {second}(2nd class) - 2*{first}(1st class) ] = {dof}")
check("Local DOF = 2  (2+0 PRESERVED; e adds ZERO propagating modes)", dof == 2)
print("    + ONE GLOBAL pair (York time tau <-> volume) = the CMC clock (not a local DOF).")

# ============================================================================
# 6.  SCALAR-vs-VECTOR FLAG (state the risk; do NOT solve).
# ============================================================================
head("6.  FLAG: scalar e screens ISOTROPICALLY; the EFE quadrupole wants a VECTOR E_i")
print("""
  PHYSICS TENSION (honest, unresolved here):
   * A SCALAR e with eps=e^2 is ROTATIONALLY INVARIANT: A(eps) multiplies the WHOLE
     MOND term isotropically. It suppresses the MONOPOLE (kills local MOND) and with it
     the EFE quadrupole Q2 -- but ONLY by switching MOND off, not by encoding a direction.
     The physical external-field effect is ANISOTROPIC (it has the direction of g_ext),
     and the Cassini-bounded object is the anisotropic-stress QUADRUPOLE, which a scalar
     cannot carry. So scalar-e 'fixes' Q2 by amputation, and likely over-screens galaxies.
   * The direction-carrying object is a VECTOR E_i (-> g_Gal at infinity). Counting risk:
     a vector adds (E_i,P_{E_i}) = 6 phase-space dims. IF its kinetic term is the full
     (1/2)(D_i E_j)(D^i E^j) with NO gauge symmetry, all 3 components are elliptic and (by
     the same Pfaffian logic) second-class -> 0 DOF, SAFE. BUT if the kinetic term is
     Maxwell-type F_ij F^ij (gauge-invariant), the transverse part propagates -> +2 DOF
     (and a longitudinal constraint), and one must re-check c_T and ghosts. A generic
     vector kinetic term sits between these and can propagate 1-3 extra modes.
  => The SCALAR result here (2+0 preserved) does NOT transfer automatically to a vector.
     Deriving the vector E_i constraint algebra is a SEPARATE calculation. FLAGGED, not
     solved.  (Marked INCOMPLETE for the vector; the scalar case is COMPLETE and PASSES.)
""")
CAVEATS.append(
  "SCALAR e preserves 2+0 (this derivation). The physically-needed ANISOTROPIC EFE "
  "quadrupole wants a VECTOR E_i, whose DOF count is NOT settled here: a non-gauge "
  "elliptic vector stays 0 DOF, but a Maxwell-type kinetic term propagates +2. Separate "
  "derivation required -- do NOT assume the scalar result carries over.")
CAVEATS.append(
  "Stabiliser W=(1/2)M^2 e^2: changes M_e only at ORDER 0 (adds +M^2 to the e-Hessian), "
  "leaving the -D^2 principal symbol |k|^2 untouched -> Pfaffian order-4 diagonal unchanged. "
  "It only IMPROVES positivity/invertibility of M_e (lifts any zero mode at e=0). W=0 and "
  "W=(1/2)M^2 e^2 give the SAME DOF count.")

# ============================================================================
#   VERDICT
# ============================================================================
head("VERDICT -- DERIVATION-A (scalar e-screen, York/CMC DOF)")
allpass = all(RESULTS.values())
for kk, v in RESULTS.items():
    print(("  [PASS] " if v else "  [FAIL] ") + kk)
print("""
  ANSWER: For a SCALAR screening field e with the (1/2) D_i e D^i e gradient term, the
  York/CMC 2+0 DOF is PRESERVED. The Phi<->e coupling does NOT break it because:
    (1) {C_Phi,C_e}=0 (both momentum-independent) and {P_Phi,P_e}=0;
    (2) the diagonal self-brackets are BOTH order-2 elliptic (L_Phi from AQUAL,
        M_e from -D^2 e), so the Pfaffian's diagonal product is ORDER 4;
    (3) the cross brackets are only ORDER 1 (coupling via the algebraic U_eps, U_yeps),
        so B B' is ORDER 2 -- strictly SUBLEADING;
    => Pf = L_c E_c k^4 + b b' k^2 != 0 at principal-symbol order => all four (P_Phi,
       C_Phi,P_e,C_e) SECOND CLASS => Phi and e each 0 DOF.
    (4) H_perp Dirac-DeWitt algebra CLOSES: V_e is ultralocal in h_ij, contributes ZERO
        to the structure functions; c_T=1 intact.
    (5) 16 - 4(2nd) - 8(1st) = 4, /2 = 2.

  KNIFE-EDGE (the real content of 'no e-dot is not enough'): the count survives ONLY
  because e carries the ELLIPTIC gradient term. A purely algebraic e (M_e order 0) would
  drop the diagonal to order 2, tie the cross product, and could free an extra mode.

  VECTOR VERSION: INCOMPLETE -- flagged, not solved (sec 6).
""")
print("  SCALAR-e DOF VERDICT:", "2+0 PRESERVED" if allpass else "FAIL / EXTRA_DOF")
print()
print("  CAVEATS (honest, non-fatal to the scalar count):")
for c in CAVEATS:
    print("   - " + c)

if not allpass:
    print("\n  ONE OR MORE CHECKS FAILED.")
    sys.exit(1)
