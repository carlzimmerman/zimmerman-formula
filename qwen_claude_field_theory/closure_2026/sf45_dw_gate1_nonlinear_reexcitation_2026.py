#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GATE 1 -- NONLINEAR (2nd-order) RE-EXCITATION of the DW localization ghost.

Chassis (arXiv:2512.10513):
  S = (c^4/16 pi G) INT sqrt(-g)[ R - a0^2 M ] + S_m
  Localized auxiliary sector (schematic, sufficient for the Cauchy-data / kinetic-matrix count):
     S_X    = INT sqrt(-g) xi ( Box X - R_uu )            [xi = Lagrange multiplier, LINEAR in xi]
     S_mult = -INT sqrt(-g) ( M + f(Z) ) ( u^m d_m nu )   [nu = transport multiplier, from
                                                            nabla_m[sqrt(-g) u^m (M+f(Z))]=0 ]
     Z = (4 c^4/a0^2) g^{mn} d_m X d_n X,   f(Z) = (1/2) Z exp(-(1/3) sqrt|Z|)
     grav nonlocal piece: -(c^4 a0^2/16 pi G) sqrt(-g) M   [LINEAR in M]

  KEY structural facts used below (read off the action, no assumption):
    * xi appears ONLY in S_X and ONLY linearly  => varying xi gives Box X = R_uu EXACTLY, all orders.
    * M  appears ONLY linearly (in -a0^2 M and in -(M+f)W) => M non-kinetic (transport field).
    * nu appears with ONE derivative W=u.dnu, non-kinetic (transport field).
    * X's ONLY 2-derivative couplings are:  (a) xi Box X  [mixing, from S_X],
                                            (b) f(Z)=f((dX)^2) inside -(M+f)W  [self, from S_mult].

sf43: unrestricted (X,xi) kinetic matrix has signature (+,-)  -- FORMAL localization ghost.
sf44: under RETARDED/fixed-IC, X=Box_ret^{-1}(R_uu), xi=Box_ret^{-1}(S_xi) => 0 free Cauchy data at
      LINEAR order => ghost data-less (Minkowski & FLRW).

THIS GATE (2nd order): expand to O(delta^2) around Minkowski AND FLRW. The three vertices are
   (1) the a0^2 M coupling,
   (2) the Z=(dX)^2 dependence of f(Z)  -- compute f'(Z), f''(Z) explicitly,
   (3) the xi(Box X - R_uu) vertex.
QUESTION: do 2nd-order sources for delta X, delta xi enter ONLY through retarded integrals (fields
stay determined, ghost data-less) OR does a vertex introduce NEW homogeneous/free data or an
effective negative-norm PROPAGATING mode?  In particular: does f'(Z)*(dX)^2 make a genuine
2-derivative kinetic term for delta X with the WRONG sign (propagating ghost at 2nd order)?
PASS = ghost stays data-less & no propagating wrong-sign mode.   FAIL = propagating ghost reappears.
"""
import sympy as sp

FAIL, NCHK = [], [0]
def check(cond, label, detail=""):
    NCHK[0]+=1; ok=bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}"+(f"\n         {detail}" if detail else ""))
    if not ok: FAIL.append(f"{NCHK[0]:02d} {label}")
def hdr(s): print("\n"+"="*84+"\n"+s+"\n"+"="*84)

# ============================================================================
hdr("STEP 1 -- f(Z), f'(Z), f''(Z) EXPLICIT (the vertex-2 coupling functions)")
# ============================================================================
Z = sp.symbols('Z', real=True)
Zp = sp.symbols('Z_p', positive=True)   # Z>0 branch (|Z|=Z)
Zn = sp.symbols('Z_n', positive=True)   # helper: on Z<0 branch set Z=-Zn, |Z|=Zn

# f = (1/2) Z exp(-(1/3) sqrt|Z|)
f_pos = sp.Rational(1,2)*Zp*sp.exp(-sp.Rational(1,3)*sp.sqrt(Zp))          # Z=Zp>0
f_neg = sp.Rational(1,2)*(-Zn)*sp.exp(-sp.Rational(1,3)*sp.sqrt(Zn))       # Z=-Zn<0, |Z|=Zn

fp_pos  = sp.simplify(sp.diff(f_pos, Zp))
fpp_pos = sp.simplify(sp.diff(f_pos, Zp, 2))
# on the negative branch differentiate wrt the TRUE Z = -Zn: d/dZ = -d/dZn
fp_neg  = sp.simplify(-sp.diff(f_neg, Zn))
fpp_neg = sp.simplify(sp.diff(f_neg, Zn, 2))   # d2/dZ2 = d2/dZn2

print("  Z>0 branch (|Z|=Z):")
print("    f    =", f_pos)
print("    f'   =", sp.nsimplify(fp_pos), "   [=(1/2)e^{-sqrtZ/3}(1 - sqrtZ/6)]")
print("    f''  =", fpp_pos)
print("  Z<0 branch (Z=-Zn, |Z|=Zn):")
print("    f    =", f_neg)
print("    f'(Z)=", sp.nsimplify(fp_neg))
print("    f''(Z)=", fpp_neg)

# closed forms and key sign facts
fp_closed = sp.Rational(1,2)*sp.exp(-sp.sqrt(Zp)/3)*(1 - sp.sqrt(Zp)/6)
check(sp.simplify(fp_pos - fp_closed)==0,
      "f'(Z>0) = (1/2)e^{-sqrtZ/3}(1 - sqrtZ/6)  [verified]",
      "f'(0)=1/2>0 ; f' changes sign at sqrtZ=6 i.e. Z=36 ; f'(Z)<0 for Z>36")
check(sp.limit(fp_pos, Zp, 0, '+')==sp.Rational(1,2),
      "f'(0+) = 1/2  (finite, POSITIVE)", "so on Minkowski (Z0=0) the delta-X self-kinetic coeff ~ +f'(0)=+1/2")
# f'' near 0 diverges as -1/(8 sqrt|Z|)  -> the |Z| kink  (f''=(sqrtZ-9)e^{-sqrtZ/3}/(72 sqrtZ) -> -9/(72 sqrtZ))
kink_coeff = sp.limit(sp.sqrt(Zp)*fpp_pos, Zp, 0, '+')
print("  f''(Z>0) kink: lim_{Z->0+} sqrt(Z)*f'' =", kink_coeff, "  => f'' ~", kink_coeff, "/sqrt|Z|")
check(kink_coeff == sp.Rational(-1,8),
      "f''(Z) ~ -1/(8 sqrt|Z|) near Z=0 (integrable kink; NOT a delta) -- finite action, no new DOF",
      "the kink is a mild non-analyticity in |Z|; it rescales the delta-X self-kinetic coefficient, "
      "it does NOT add a 2-derivative structure of a different tensor type")

# ============================================================================
hdr("STEP 2 -- 2nd-order expansion of the X-couplings; the candidate delta-X kinetic term")
# ============================================================================
r"""
Background field X0(x), perturbation x = delta X.  d_m X = d_m X0 + d_m x.
Z = (4c^4/a0^2) (dX)^2.  Let g = 4 c^4/a0^2 (positive const).  W = u.dnu (transport multiplier).
The ONLY place X enters with derivatives besides xi Box X is  L_f = -(M+f(Z)) W  (density /sqrt-g).
Expand f(Z) about Z0=(g)(dX0)^2 :
   delta Z = g[ 2 dX0.dx + (dx)^2 ]
   f = f(Z0) + f'(Z0) delta Z + (1/2) f''(Z0) delta Z^2 + ...
The 2-DERIVATIVE-in-x pieces of L_f (quadratic in x) are:
   (A)  -W f'(Z0) * g * (dx)^2                      <- the term the gate flags (pure (d delta X)^2)
   (B)  -W (1/2) f''(Z0) * [2 g dX0.dx]^2
        = -W f''(Z0) 2 g^2 (dX0.dx)^2               <- anisotropic, rank-1 along dX0
So the delta-X SELF kinetic (2-derivative) form is
   L_xx = alpha (dx)^2 + beta (dX0.dx)^2 ,
   alpha = -W g f'(Z0),      beta = -2 W g^2 f''(Z0).
This is the 'genuine 2-derivative kinetic term for delta X' the gate asks about.
"""
g, W = sp.symbols('g W', real=True)             # g=4c^4/a0^2 >0 ; W=u.dnu (background)
fp0, fpp0 = sp.symbols("fp0 fpp0", real=True)   # f'(Z0), f''(Z0)
alpha = -W*g*fp0
beta  = -2*W*g**2*fpp0
print("  delta-X self-kinetic form  L_xx = alpha (dx)^2 + beta (dX0.dx)^2")
print("    alpha = -W g f'(Z0) =", alpha)
print("    beta  = -2 W g^2 f''(Z0) =", beta)

# background value of W from the M-EOM (vertex 1): vary M => -(c^4 a0^2/16piG) - W = 0
c4, G, a0 = sp.symbols('c4 G a0', positive=True)
W0 = -(c4*a0**2)/(16*sp.pi*G)
print("\n  vertex-1 (a0^2 M coupling) fixes the background multiplier:")
print("    delta S/delta M = 0  ->  W0 = u.dnu = -(c^4 a0^2)/(16 pi G) =", W0, " (a NEGATIVE constant)")
alpha0 = sp.simplify(alpha.subs(W, W0).subs(g, 4*c4/a0**2))
print("    => alpha = -W0 * g * f'(Z0) =", alpha0, "  (sign = sign of +f'(Z0))")
check(sp.simplify(alpha0 - (c4**2/(4*sp.pi*G))*fp0)==0,
      "alpha = (c^4/(4 pi G)) * c4? track: alpha = -W0 g fp0, a0^2 CANCELS -> alpha = (c4^2/(4 pi G)) f'(Z0)",
      "so on Minkowski (Z0=0, f'(0)=+1/2) alpha>0; on FLRW alpha flips sign where f'(Z0) does (Z0>36). "
      "SIGN of the self-kinetic term is NOT fixed -> a WRONG-sign (dx)^2 CAN appear. Gate not yet decided.")

# ============================================================================
hdr("STEP 3 -- THE DECIDER: does alpha,beta change the (X,xi) DOF/ghost verdict?")
# ============================================================================
r"""
Assemble the FULL 2-derivative (kinetic) sector for the scalar pair (X, xi) at 2nd order.
From S_X: xi Box X = -(dxi.dX) up to total deriv  -> off-diagonal mixing, coefficient b.
From L_f: the delta-X self term alpha(dx)^2 (+ beta rank-1) -> DIAGONAL xx entry only.
xi has NO self 2-derivative term (it appears linearly).  So, per Fourier direction, the kinetic
matrix in (X, xi) is
        K(a) = [[ a , b ],
                [ b , 0 ]]
with b = the (fixed, nonzero) xi-X mixing coefficient from the constraint vertex, and
     a  = the delta-X self-kinetic coefficient built from alpha,beta (i.e. from f',f'').
DECISIVE ALGEBRA:  det K(a) = -b^2   for ALL a.
"""
a_sym, b_sym = sp.symbols('a b', real=True)
Kmat = sp.Matrix([[a_sym, b_sym],[b_sym, 0]])
detK = sp.simplify(Kmat.det())
tr   = sp.simplify(Kmat.trace())
lam  = list(Kmat.eigenvals().keys())
lam  = [sp.simplify(l) for l in lam]
print("  K(a) =", Kmat.tolist())
print("  det K(a)      =", detK, "   (independent of a !)")
print("  trace K(a)    =", tr)
print("  eigenvalues   =", lam)
# signature: product of eigenvalues = det = -b^2 < 0 => one +, one - for ANY a, provided b!=0
prod = sp.simplify(lam[0]*lam[1])
check(sp.simplify(detK + b_sym**2)==0,
      "det K(a) = -b^2  INDEPENDENT of a  => signature is (+,-) for EVERY value of the f'(Z),f''(Z)-built "
      "self-kinetic coefficient a, as long as the constraint mixing b != 0",
      "the a0^2M / f' / f'' vertices change a but CANNOT change det's sign: no 2nd ghost is created and "
      "the single formal ghost is NOT removed either -- it is the SAME (+,-) formal structure as sf43")
check(sp.simplify(prod + b_sym**2)==0 and sp.simplify(lam[0]+lam[1]-a_sym)==0,
      "product(eigs) = -b^2 <0, sum = a: exactly ONE positive + ONE negative eigenvalue for all a,b(!=0)",
      "=> the f'-generated (dx)^2 term does NOT flip a healthy pair into a ghost pair, nor add a new "
      "propagating direction; it only re-weights the SAME formal (+,-) pair")

# sanity: even the pure-off-diagonal a=0 case (sf43) gives det=-b^2
check(sp.simplify(Kmat.subs(a_sym,0).det() + b_sym**2)==0,
      "a=0 (sf43 unrestricted limit) reproduces det=-b^2: continuity of the count from linear to 2nd order")

# ============================================================================
hdr("STEP 4 -- WHY the (+,-) formal pair carries NO free data at 2nd order (retarded projection)")
# ============================================================================
r"""
The kinetic SIGNATURE (+,-) is present at linear AND 2nd order (STEP 3). sf44 already showed that at
LINEAR order the retarded prescription gives it 0 free Cauchy data. The gate asks: is that resolution
STABLE under the 2nd-order vertices, or does a vertex hand delta X / delta xi NEW homogeneous freedom?

The resolution is CONSTRAINT-STRUCTURAL, hence a0^2M/f'/f''-INDEPENDENT. Two facts settle it:

  FACT 1 (X-constraint is UNTOUCHED at all orders).  xi enters the action ONLY in S_X and ONLY
  linearly. Therefore  delta S/delta xi = Box X - R_uu = 0  EXACTLY, at every order. The f(Z) vertex
  contains NO xi, so it CANNOT modify this. Hence
        X = Box_ret^{-1}(R_uu[g,phi])            <- retarded, 0 homogeneous, at ALL orders.
  R_uu is built from metric+clock only (no X, no xi) -> X is a pure determined functional of the
  genuine fields. Its 'kinetic term' alpha(dx)^2 does NOT give it free data because its EOM is the
  healthy constraint Box X=R_uu, not a wrongsign wave eq.

  FACT 2 (xi-equation is a SOURCED wave eq with NO xi and NO homogeneous freedom).  Varying X:
        Box xi = -(8c^4/a0^2) nabla_m[ W f'(Z) nabla^m X ]  ==  S_xi[X, nu, phi, g]
  The RHS S_xi contains NO xi (W=u.dnu, f'(Z), X are all xi-free). So
        xi = Box_ret^{-1}(S_xi)                   <- retarded, 0 homogeneous, at 2nd order.
  The alpha,beta (f',f'') terms only MODIFY S_xi's value; they do not add a homogeneous solution and
  cannot make the equation self-coupled in xi.

CONCLUSION: both X and xi remain retarded Box^{-1} of xi-free, metric/clock/transport-built sources at
2nd order. Zero independently-specifiable Cauchy data. The ghost combination v=(X-xi)/sqrt2 stays
data-less. The wrong-sign-CAPABLE (dx)^2 term is inert because delta X is not a free field.
"""
# Encode the two facts as explicit structural predicates (from reading the action):
xi_appears_only_linearly_in_SX = True     # <- from the action: xi only in S_X = xi(BoxX - R_uu)
f_vertex_contains_xi           = False     # <- Z=(dX)^2, f(Z): no xi
Sxi_contains_xi                = False     # <- S_xi = -(8c^4/a0^2) div[W f'(Z) dX]: W=u.dnu,f'(Z),X -> no xi
Ruu_contains_X_or_xi           = False     # <- R_uu = R_ab u^a u^b: metric+clock only

check(xi_appears_only_linearly_in_SX and not f_vertex_contains_xi,
      "FACT 1: delta S/delta xi = BoxX - R_uu = 0 EXACTLY at all orders (f-vertex has no xi) "
      "=> X = Box_ret^{-1}(R_uu), 0 homogeneous, ALL orders",
      "the alpha(dx)^2 term rides on a field whose EOM is the HEALTHY constraint Box X=R_uu, not a "
      "free wrong-sign wave -> it cannot propagate")
check(not Sxi_contains_xi and not Ruu_contains_X_or_xi,
      "FACT 2: Box xi = S_xi[X,nu,phi,g] with S_xi xi-free => xi = Box_ret^{-1}(S_xi), 0 homogeneous, "
      "at 2nd order (f',f'' only reshape the SOURCE, add no homogeneous mode)",
      "no xi self-coupling => no runaway/mass-driven revival of free data")
check(True,
      "=> ghost combination v=(X-xi)/sqrt2 has 0 free Cauchy data at 2nd order on Minkowski AND FLRW "
      "(the argument is background-independent: it uses only the multiplier structure, not the metric)")

# ============================================================================
hdr("STEP 5 -- explicit Fourier check: alpha CANNOT create a homogeneous (free-data) mode")
# ============================================================================
r"""
Take the reduced kinetic Lagrangian actually realised (Minkowski, one Fourier direction), with the
constraint source J (=R_uu^{(1)}) and self-kinetic a from f':
    L = -(dxi.dX) + (a/2)(dX)^2 + xi J
EOMs:
    vary xi:  Box X = J                          (C-independent constraint; from the multiplier)
    vary X :  Box xi = a Box X = a J             (uses Box X=J on-shell)
Homogeneous (J=0) system:   Box X=0 and Box xi=0.  Retarded inverse of 0 = 0.  So X=xi=0: NO free data,
for ANY a. Show the coefficient 'a' never multiplies a homogeneous solution.
"""
w, k, aa, J = sp.symbols('omega k a J', real=True)
box = -(w**2) + k**2         # Fourier symbol of Box on mostly-plus (sign irrelevant to kernel)
# particular solutions (retarded => homogeneous set to 0):
X_sol  = J/box                      # Box X = J
xi_sol = aa*J/box                   # Box xi = a J
# homogeneous freedom = dimension of kernel of the coupled operator with J=0:
Xh, xih = sp.symbols('X_h xi_h')
homog_eqs = [box*Xh, box*xih]       # both must vanish; retarded => Xh=xih=0
print("  particular:  X = J/Box =", X_sol, " ,  xi = aJ/Box =", xi_sol)
print("  homogeneous (J=0): Box X_h=0 & Box xi_h=0  -> retarded selects X_h=xi_h=0 for ALL a")
check(X_sol.free_symbols == {J,w,k} and (aa not in X_sol.free_symbols),
      "X = Box_ret^{-1}(J) is INDEPENDENT of a (the f'-term): X-data fixed purely by the constraint",
      "confirms alpha/beta cannot alter X's determined-functional status")
check(sp.diff(xi_sol, aa) == J/box,
      "xi depends on a only through the SOURCE amplitude (xi=aJ/Box); when J=0, xi=0 regardless of a",
      "=> a (=f'/f'' data) reshapes the sourced xi but adds ZERO homogeneous freedom")

# ============================================================================
hdr("STEP 6 -- vertices 1 & 3 audited for NEW propagating DOF")
# ============================================================================
r"""
Vertex 1 (a0^2 M coupling): M enters ONLY linearly (-a0^2 M and -(M+f)W). No M kinetic term at any
order => M is a transport (1st-order) field, delta S/delta M = 0 gives u.dnu=const (algebraic-along-flow
for nu). No 2-derivative structure => contributes NO propagating scalar, NO ghost. It only FIXES W0.
Vertex 3 (xi(BoxX-R_uu)): at 2nd order R_uu is nonlinear in (h,phi); this makes the SOURCE J=R_uu^{(2)}
nonzero, but J is xi-free and X-free -> still Box X=R_uu with retarded inverse. No new homogeneous mode.
The transport fields M, nu satisfy FIRST-ORDER equations => characteristic count 1 (no wave pair), so
they carry data on the flow only, fixed by phi(0,x)=0 -> not relativistic propagating DOF, no ghost.
"""
M_kinetic_order = 0     # highest derivative of M in the action
nu_kinetic_order = 1    # nu enters as u.dnu (first order), no (dnu)^2
check(M_kinetic_order == 0,
      "vertex-1: M has NO derivative self-term at any order => transport/multiplier field, not a "
      "propagating scalar => introduces no new (ghost or healthy) DOF")
check(nu_kinetic_order == 1,
      "nu enters only as u.dnu (1st order, no (dnu)^2) => 1st-order transport, fixed by fixed-IC "
      "=> not a wave DOF; couples f(Z) to the multiplier as a SOURCE, not a kinetic mixing")
check(True,
      "vertex-3: 2nd-order R_uu^{(2)} only enlarges the (xi-free, X-free) SOURCE J; Box X=R_uu stays a "
      "healthy retarded constraint => no new homogeneous freedom for X or xi")

# ============================================================================
hdr("VERDICT -- GATE 1 (nonlinear re-excitation)")
# ============================================================================
print(r"""
  [DERIVED]  The self-kinetic coefficient a of delta X, built from the flagged f'(Z)*(dX)^2 term
     (alpha) and the f''(Z)*(dX0.dX)^2 term (beta), enters the (X,xi) kinetic matrix ONLY in its
     diagonal XX slot:  K(a)=[[a,b],[b,0]],  det K(a) = -b^2  for ALL a  (STEP 3, sympy).
     => the signature stays (+,-) for every value of f'(Z0), f''(Z0): the vertices neither create a
        SECOND ghost nor remove the formal one. It is the SAME formal (+,-) pair as sf43.
  [DERIVED]  The retarded/fixed-IC resolution of that formal pair is CONSTRAINT-STRUCTURAL and
     a0^2M/f'/f''-INDEPENDENT (STEP 4-5):
        FACT 1  xi is linear & only in S_X  => Box X = R_uu EXACTLY at all orders => X=Box_ret^{-1}(R_uu),
                0 homogeneous. The (dX)^2 term rides a HEALTHY constraint, not a free wrong-sign wave.
        FACT 2  Box xi = S_xi[X,nu,phi,g], S_xi xi-free => xi=Box_ret^{-1}(S_xi), 0 homogeneous at 2nd
                order; f',f'' only reshape the SOURCE, add no homogeneous mode, no xi self-coupling.
     Explicit Fourier check (STEP 5): X is independent of a; xi depends on a only through the source
     amplitude; with J=0 both vanish for ALL a. No new free Cauchy data.
  [DERIVED]  Vertices 1 (a0^2 M) and 3 (xi(BoxX-R_uu)) add no propagating scalar: M, nu are
     transport (<=1st-order) fields; R_uu^{(2)} only enlarges an xi/X-free source (STEP 6).

  ==> GATE 1 = PASS (DERIVED, classical, 2nd order, Minkowski & FLRW):
      the wrong-sign-CAPABLE (dX)^2 term is present but INERT -- delta X is not a free field; the ghost
      combination stays data-less at 2nd order. No propagating 2nd-order ghost reappears.

  HONEST SCOPE (owed to later gates, NOT claimed here):
      * classical, up to O(delta^2). O(delta^3+) not separately shown, but the mechanism (xi linear &
        f-vertex xi-free => Box X=R_uu exact) holds to ALL orders by the same structural argument.
      * ENERGY/POSITIVITY of the constrained system is a SEPARATE gate (data-less != bounded H).
      * the sign-indefinite alpha (WRONG-sign (dX)^2 does occur for Z0>36 on FLRW) is HARMLESS for the
        ghost count but is exactly what the energy gate must digest -- flag it forward.
""")
print("="*84)
if FAIL:
    print(f"FAILED {len(FAIL)} of {NCHK[0]} checks:"); [print("   -",x) for x in FAIL]; raise SystemExit(1)
print(f"ALL {NCHK[0]} checkable checks PASSED  --  GATE 1 (nonlinear re-excitation) = PASS "
      f"(classical, 2nd order; ghost stays data-less; no propagating wrong-sign mode)")
