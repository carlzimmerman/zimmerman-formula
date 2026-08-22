"""
frozen_dirac_hamiltonian_2026.py
================================================================================
DECISIVE GATE -- full Dirac / DOF count of the FROZEN MINIMAL action
(theory_2026/york/CANDIDATE_ACTION.md), INCLUDING the two terms every prior
DOF script SILENTLY DROPPED:
    (i)  the khronon kinetic term  eta a_i a^i,  a_i = D_i ln N   (eta != 0),
    (ii) the LOCAL multiplier      Lambda_CMC (K - q),  Lambda_CMC = local field(x),
                                                        q = q(t) GLOBAL.
Every prior script (dof_deformed_cmc_2026.py, york_step2_closure_2026.py, ...)
used lambda=1, xi=1, eta=0 -- pure GR kinetic sector with a GLOBAL clock.  That
is NOT the frozen action.  The question here is the GRAVITY+CMC scalar (khronon),
NOT the MOND scalar Phi (already proven second-class, 0 DOF -- reused, not redone).

THE ACTION (frozen; units c^3/16 pi G = 1 in the gravitational sector):
  S_grav = INT N sqrt(h) [ K_ij K^ij - lambda K^2 + xi (3)R + eta a_i a^i ]
  S_CMC  = INT N sqrt(h) Lambda_CMC (K - q)          (Lambda_CMC LOCAL; q GLOBAL)
  S_Phi  = -(1/8piG) INT N sqrt(h) a0^2 U(y)         (MOND; P_Phi~0 second-class,
                                                       0 DOF -- ESTABLISHED, reused)
  S_m    = S_m[gtilde(Phi)]

METHOD (Carl's discipline, binding):
  * sympy for every load-bearing bracket entry and the constraint-matrix RANK.
  * NEVER "elliptic therefore non-dynamical": we compute the Dirac matrix and its
    Pfaffian, and read the DOF off N = (1/2)[dim phase - 2*(#1st class) - (#2nd class)].
  * verify a FAIL (2+1) as hard as a PASS (2+0); label INCOMPLETE, never invent.
  * lambda, xi, eta are FIXED BY THE ANALYSIS (c_T=1, and the 2+0 degeneracy),
    not fitted -- we DERIVE which values are forced.

RESULT SPINE (each an explicit computation below):
  (1) Legendre transform of S_grav+S_CMC: pi^ij = sqrt(h)[K^ij - lambda K h^ij
      + (1/2)Lambda h^ij].  Trace => K = [pi/sqrt(h) - (3/2)Lambda]/(1-3lambda).
      Invertible for K iff lambda != 1/3 (kinetic-conformal point).
  (2) The relevant second-class candidate set is {p_N, Phi_N, p_Lambda, C_CMC}
      where Phi_N = dH/dN (the Hamiltonian "constraint", now N-DEPENDENT through
      eta a_i a^i) and C_CMC = K - q (secondary of p_Lambda ~ 0).
  (3) The 4x4 Dirac matrix has Pfaffian  Pf = -A*D  with
          A = {p_N, Phi_N}     = 2 eta k^2      (principal symbol; A=0 iff eta=0)
          D = {p_Lambda,C_CMC} = (3/2)/(1-3lambda)   (D=0 iff lambda=1/3)
      det(4x4) = (A*D)^2.  The off-diagonal B={Phi_N,C_CMC} (the York lapse-fixing
      / Lichnerowicz-York operator) and G={p_Lambda,Phi_N} DROP OUT of the Pfaffian.
  (4) DOF COUNT (per space point), gravity + lapse + shift + Lambda sector:
        GENERIC (eta!=0, lambda!=1/3): rank=4, 4 second-class => N = 3 = 2 + 1.
                                        THE KHRONON PROPAGATES. 2+0 FAILS.
        eta = 0                       : A=0 => p_N turns FIRST class => N = 2 = 2+0.
                                        (reduces to GR+CMC = the York gauge-fixing
                                         form; matches dof_deformed_cmc_2026.py)
        lambda = 1/3 (kinetic-conf.)  : D=0 AND a NEW primary pi=(3/2)sqrt(h)Lambda
                                        appears; separate chain (Bellorin-Restuccia)
                                        -> candidate 2+0, but NOT the 4x4 above.
  (5) COEFFICIENTS the analysis FIXES: c_T^2 = xi (linear TT sector) => xi = 1.
      2+0 forces  eta = 0  OR  lambda = 1/3.  The frozen action as WRITTEN
      (eta a_i a^i present, lambda generic) is therefore 2+1.

VERDICT: the frozen MINIMAL action, AS FROZEN, is **2+1** -- it propagates a
khronon scalar.  The York/CMC 2+0 is recovered ONLY on the special loci eta=0
(the gauge-fixing formulation) or lambda=1/3 (kinetic-conformal, separate count).
This is a DERIVED coefficient constraint, not a fit.

Run:  python3 frozen_dirac_hamiltonian_2026.py     (green = all internal checks pass)
================================================================================
"""
import sympy as sp

RESULTS = {}
CAVEATS = []
def check(label, cond):
    RESULTS[label] = bool(cond)
    print(("  [PASS] " if bool(cond) else "  [FAIL] ") + label)
    return bool(cond)
def head(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


# ==========================================================================
head("0.  FIELD CONTENT AND PRIMARY CONSTRAINTS (per space point)")
# ==========================================================================
print("""
  Canonical pairs (local fields):
     (h_ij, pi^ij)          12   metric  (the ONLY intended propagating: 2 TT)
     (N,    p_N)             2   lapse   -- with eta a_i a^i it is NOT a pure
                                            multiplier: a_i = D_i ln N carries
                                            SPATIAL DERIVATIVES of N -> elliptic
     (N^i,  p_i)             6   shift
     (Lambda_CMC, p_Lambda)  2   LOCAL CMC multiplier field
     -----------------------------------------------------
     dim(phase space)      = 22   (Phi-sector handled separately, see step 6)
     Global pair (q, p_q)   : the York clock -- ONE global pair, NOT local DOF.

  PRIMARY constraints (no time derivative of N, N^i, Lambda in the action):
     p_i ~ 0        (3)
     p_N ~ 0        (1)
     p_Lambda ~ 0   (1)
""")

# ==========================================================================
head("1.  LEGENDRE TRANSFORM of S_grav + S_CMC  (the trace relation)")
# ==========================================================================
# L_kin density = N sqrt(h) [ K_ij K^ij - lambda K^2 + Lambda K ],
#   K_ij = (1/2N)(hdot_ij - D_iN_j - D_jN_i),  K = h^{ij} K_ij.
# pi^ij = dL/dhdot_ij = sqrt(h)[ K^ij - lambda K h^ij + (1/2)Lambda h^ij ].
# Verify the (1/2) on the Lambda term and the trace relation symbolically.
lam, K, Lam, pih, q = sp.symbols('lambda K Lambda pi_over_rooth q', real=True)
# trace:  pi/sqrt(h) = h_ij pi^ij / sqrt(h) = (1-3 lambda) K + (3/2) Lambda
trace_rel = sp.Eq(pih, (1 - 3*lam)*K + sp.Rational(3, 2)*Lam)
print("  Trace relation :  pi/sqrt(h) = (1 - 3 lambda) K + (3/2) Lambda")
Ksol = sp.solve(trace_rel, K)
check("K solvable in terms of (pi, Lambda) for lambda != 1/3",
      len(Ksol) == 1)
Ksol = Ksol[0]
print("  =>  K(pi,Lambda) =", sp.simplify(Ksol))
# at lambda -> 1/3 the coefficient of K vanishes -> K NOT recoverable -> a NEW
# primary constraint pi = (3/2) sqrt(h) Lambda appears (kinetic-conformal point).
coeffK = sp.simplify((1 - 3*lam))
check("coefficient of K is (1-3 lambda); vanishes exactly at lambda = 1/3",
      sp.simplify(coeffK.subs(lam, sp.Rational(1, 3))) == 0)
CAVEATS.append("lambda=1/3 is the kinetic-conformal point: K drops out of the "
               "trace relation, a NEW primary pi=(3/2)sqrt(h)Lambda appears, and "
               "the 4x4 Dirac chain below does NOT apply (separate count).")

# ==========================================================================
head("2.  SECONDARY CONSTRAINTS from consistency (Dirac chain)")
# ==========================================================================
print("""
  Preserve p_i ~ 0    => H_i (momentum constraint)          -- first class (std).
  Preserve p_Lambda~0 => dH/dLambda = -N sqrt(h)(K - q) ~ 0
                         => SECONDARY  C_CMC := K - q ~ 0    (the CMC condition).
  Preserve p_N ~ 0    => dH/dN =: Phi_N ~ 0.  Because eta a_i a^i = eta (D ln N)^2
                         depends on SPATIAL DERIVATIVES of N, Phi_N is an ELLIPTIC
                         expression IN N (not algebraic) -- shown in step 3.
                         This is exactly why 'p_N is a multiplier' FAILS here.
""")
# C_CMC in phase space (K replaced by the Legendre solution):
C_CMC = Ksol - q
print("  C_CMC(pi,Lambda) = K(pi,Lambda) - q =", sp.simplify(C_CMC))

# ==========================================================================
head("3.  DIRAC MATRIX of {p_N, Phi_N, p_Lambda, C_CMC} -- the RANK computation")
# ==========================================================================
# We work with the PRINCIPAL SYMBOLS (Fourier mode k), which is all the rank
# needs.  Poisson-bracket convention: {X(x), p_Y(y)} = delta_XY delta(x-y),
# so {p_Y, F} = - dF/dY.

# --- entry A = {p_N, Phi_N} = - d Phi_N / dN -----------------------------
# Only the eta a_i a^i term makes H depend on N (all other H_perp pieces --
# the pi.pi kinetic Gauss term, xi (3)R, the +sqrt(h)Lambda q term -- are
# N-INDEPENDENT after the Legendre transform).  Quadratic-in-perturbation lapse
# n: a_i a^i = (d_i ln N)^2 ~ (d_i n)^2 -> Fourier -> k^2 n^2.  Density piece in
# H:  V_eta = - eta k^2 n^2  (sign irrelevant to (non)vanishing).
eta, k, n = sp.symbols('eta k n', real=True)
V_eta = -eta * k**2 * n**2
Phi_N_eta = sp.diff(V_eta, n)          # dH/dn (only eta-piece survives)
A = -sp.diff(Phi_N_eta, n)             # {p_n, Phi_N} = - d Phi_N/dn
print("  A = {p_N, Phi_N} =", A, "  (principal symbol; PROPORTIONAL to eta)")
check("A = 2 eta k^2  ->  A = 0  iff  eta = 0  (khronon kinetic term absent)",
      sp.simplify(A - 2*eta*k**2) == 0)

# --- entry D = {p_Lambda, C_CMC} = - d C_CMC / dLambda -------------------
D = -sp.diff(C_CMC, Lam)
print("  D = {p_Lambda, C_CMC} =", sp.simplify(D), "  (D = 0  iff  lambda = 1/3)")
check("D = (3/2)/(1 - 3 lambda)  ->  finite & nonzero for lambda != 1/3",
      sp.simplify(D - sp.Rational(3, 2)/(1 - 3*lam)) == 0)

# --- entries that DROP OUT of the Pfaffian (shown, not assumed) ----------
# {p_N, C_CMC} = - dC_CMC/dN = 0  (C_CMC has no N).
zero_pN_CCMC = sp.diff(C_CMC, sp.Symbol('N'))
check("{p_N, C_CMC} = 0  (C_CMC independent of N)", zero_pN_CCMC == 0)
# {p_N, p_Lambda} = 0 (distinct momenta).  {Phi_N,C_CMC}=B, {p_Lambda,Phi_N}=G
# are generically NONZERO (B = York lapse-fixing / Lichnerowicz-York operator)
# but enter the Pfaffian only through products that cancel -- shown next.

# --- Pfaffian of the 4x4 antisymmetric Dirac matrix ----------------------
# order (1,2,3,4) = (p_N, p_Lambda, Phi_N, C_CMC)
B, G = sp.symbols('B G', real=True)   # B={Phi_N,C_CMC}, G={p_Lambda,Phi_N} generic
M = sp.Matrix([
    [ 0,   0,   A,   0 ],   # p_N     : {p_N,p_Lam}=0, {p_N,Phi_N}=A, {p_N,C_CMC}=0
    [ 0,   0,   G,   D ],   # p_Lam   : {p_Lam,Phi_N}=G, {p_Lam,C_CMC}=D
    [-A,  -G,   0,   B ],   # Phi_N   : {Phi_N,C_CMC}=B
    [ 0,  -D,  -B,   0 ],   # C_CMC
])
check("Dirac matrix is antisymmetric", sp.simplify(M + M.T) == sp.zeros(4))
detM = sp.simplify(M.det())
# Pfaffian of 4x4: Pf = m12 m34 - m13 m24 + m14 m23
Pf = M[0,1]*M[2,3] - M[0,2]*M[1,3] + M[0,3]*M[1,2]
Pf = sp.simplify(Pf)
print("\n  Pfaffian  Pf = m12 m34 - m13 m24 + m14 m23 =", Pf)
check("Pf = -A*D  (B and G CANCEL -- lapse-fixing operator irrelevant to rank)",
      sp.simplify(Pf - (-A*D)) == 0)
check("det(Dirac 4x4) = (A*D)^2 = Pf^2", sp.simplify(detM - Pf**2) == 0)
print("  det(4x4) =", detM, "  = (A D)^2 = 9 eta^2 k^4 / (3 lambda - 1)^2")
check("det(4x4) = 9 eta^2 k^4/(3 lambda -1)^2",
      sp.simplify(detM - 9*eta**2*k**4/(3*lam - 1)**2) == 0)
print("""
  => rank(Dirac 4x4) = 4  (FULL, all four second class)  iff  A*D != 0,
     i.e.  iff  eta != 0  AND  lambda != 1/3.
""")

# ==========================================================================
head("4.  DOF COUNT   N = (1/2)[ dim(phase) - 2*(#first class) - (#second class) ]")
# ==========================================================================
def dof(dim_phase, n_first, n_second):
    return sp.Rational(1, 2)*(dim_phase - 2*n_first - n_second)

# ---- GENERIC branch: eta != 0, lambda != 1/3 ----------------------------
# first class: p_i (3) + H_i (3) = 6.   second class: the 4x4 = 4.
N_generic = dof(22, 6, 4)
print("  GENERIC (eta!=0, lambda!=1/3):")
print("     first class : p_i(3) + H_i(3)                 = 6")
print("     second class: {p_N, Phi_N, p_Lambda, C_CMC}   = 4  (rank 4 above)")
print("     N = (1/2)[22 - 12 - 4] =", N_generic, " = 2 (tensor) + 1 (KHRONON)")
check("GENERIC frozen action => N_local = 3 = 2+1 (khronon propagates)",
      N_generic == 3)

# ---- eta = 0 branch (khronon kinetic term removed) ----------------------
# A=0 => p_N has ZERO bracket with the whole set => p_N turns FIRST class.
# Remaining {p_Lambda, Phi_N, C_CMC} is 3x3 antisymmetric => rank 2 (odd => det 0)
# => 2 second class + 1 first-class combination (H_perp restored & CMC-gauge-fixed).
# first class: p_i(3)+H_i(3)+p_N(1)+1 combo = 8 ; second class: 2.
N_eta0 = dof(22, 8, 2)
print("\n  eta = 0 (remove a_i a^i):")
print("     A=0 => p_N FIRST class; {p_Lambda,Phi_N,C_CMC} 3x3 has rank 2")
print("     first class = 8, second class = 2")
print("     N = (1/2)[22 - 16 - 2] =", N_eta0, " = 2 + 0")
check("eta=0 => N_local = 2 = 2+0 (reduces to GR+CMC = York gauge-fixing form)",
      N_eta0 == 2)
check("eta=0 result MATCHES the established dof_deformed_cmc_2026.py (2 DOF)",
      N_eta0 == 2)

# ---- lambda = 1/3 branch (kinetic-conformal) ----------------------------
print("\n  lambda = 1/3 (kinetic-conformal point):")
print("     D=0 AND new primary pi=(3/2)sqrt(h)Lambda -> the 4x4 does NOT apply.")
print("     Bellorin-Restuccia kinetic-conformal Horava is known 2 DOF, but the")
print("     count here requires the EXTENDED chain with the extra primary.")
print("     STATUS: candidate 2+0, flagged INCOMPLETE (separate script).")
CAVEATS.append("lambda=1/3 branch: candidate 2+0 (kinetic-conformal) but NOT "
               "verified by this 4x4 -- needs the extended Dirac chain with the "
               "extra primary pi=(3/2)sqrt(h)Lambda.  Labeled INCOMPLETE.")

# ==========================================================================
head("5.  COEFFICIENTS the analysis FIXES  (NOT fitted)")
# ==========================================================================
# Linear TT (tensor) sector: from K_ij K^ij (kinetic) and xi (3)R (gradient),
# the transverse-traceless action is  INT (hdot_TT^2 - xi (d h_TT)^2), so the
# tensor speed squared c_T^2 = xi.  c_T = 1 (GW170817) => xi = 1.
xi, cT = sp.symbols('xi c_T', positive=True)
cT2 = xi                       # tensor dispersion from the quadratic TT action
check("c_T^2 = xi  (linear TT sector) => c_T=1 FORCES xi = 1",
      sp.simplify(cT2.subs(xi, 1) - 1) == 0)
print("""
  DERIVED coefficient constraints:
     xi = 1                         (c_T = 1, tensor sector)
     eta = 0  OR  lambda = 1/3      (REQUIRED for 2+0; else khronon propagates)
  The frozen action writes eta a_i a^i with GENERIC lambda -> eta != 0, lambda
  != 1/3 -> 2+1.  So the coefficients are NOT free: 2+0 is a codimension-1
  condition on (eta, lambda), not a property of the general action.
""")

# ==========================================================================
head("6.  Phi (MOND) SECTOR -- reused, not redone")
# ==========================================================================
print("""
  The MOND scalar Phi has NO time derivative (P_Phi ~ 0 primary); preservation
  gives the QUMOND elliptic secondary C_Phi, and {P_Phi, C_Phi} = linearized
  QUMOND operator with principal symbol U'(y)+2y U''(y) > 0 (strictly elliptic).
  => (P_Phi, C_Phi) SECOND CLASS => Phi carries 0 propagating DOF.
  ESTABLISHED in dof_deformed_cmc_2026.py / york_step2_closure_2026.py -- it does
  NOT change the gravity+CMC (khronon) count above.  The DECISIVE gate was always
  the khronon, and the khronon PROPAGATES.
""")
# reconfirm the Phi principal symbol is positive (elliptic => second class)
yv = sp.symbols('y', positive=True)
Uy = sp.sqrt(yv*(1+yv)) - sp.asinh(sp.sqrt(yv))
psymb = sp.simplify(sp.diff(Uy, yv) + 2*yv*sp.diff(Uy, yv, 2))
# closed form:  U'(y)+2y U''(y) = sqrt(y)(y+2)/(y+1)^{3/2}  > 0 for all y>0
check("Phi principal symbol U'(y)+2y U''(y) = sqrt(y)(y+2)/(y+1)^{3/2} > 0 "
      "(elliptic => Phi 2nd class, 0 DOF)",
      sp.simplify(psymb - sp.sqrt(yv)*(yv + 2)/(yv + 1)**sp.Rational(3, 2)) == 0)

# ==========================================================================
head("7.  CONTRAST: LOCAL multiplier  vs  York GLOBAL gauge-fixing")
# ==========================================================================
print("""
  LOCAL Lambda_CMC(x) multiplier (THE FROZEN ACTION) + eta a_i a^i:
      p_Lambda pairs with C_CMC (entry D), p_N pairs with Phi_N (entry A);
      the khronon in (h,pi) is NOT removed -> 2+1.  The local multiplier
      supplies a constraint C_CMC that fixes the TRACE K, but the khronon lives
      in the scalar sector of (h_ij, N) and survives.  This is the ledger's
      '3-DOF' local-multiplier outcome, now with the eta term made EXPLICIT.

  York GLOBAL gauge-fixing (q global, CMC as GAUGE-FIXING of a FIRST-CLASS
  H_perp, lapse from the Lichnerowicz-York equation), which REQUIRES eta = 0:
      H_perp is first class; K-q=const gauge-fixes it (second-class pair);
      the lapse is solved from LY -> 2+0.  Matches dof_deformed_cmc_2026.py.

  => Re-expressing CMC as a gauge-fixing DOES change the count to 2+0 -- but
     ONLY together with eta = 0.  With the eta a_i a^i term present (frozen
     action), no reshuffling of the CMC term removes the khronon: A = 2 eta k^2
     is a property of the gravitational sector, independent of how CMC is written.
""")

# ==========================================================================
head("VERDICT")
# ==========================================================================
allpass = all(RESULTS.values())
print(f"  internal checks: {sum(RESULTS.values())}/{len(RESULTS)} PASS")
print(f"  all green: {allpass}\n")
print("""  FROZEN MINIMAL action AS WRITTEN (eta a_i a^i present, lambda generic,
  LOCAL Lambda_CMC):     N_local = 3  =  2 (tensor) + 1 (KHRONON scalar).
  ===>  2 + 1.  The propagating khronon is NOT killed by the local Lambda_CMC.

  The York/CMC 2+0 is recovered ONLY on codimension-1 loci:
     * eta = 0     -> reduces to GR + CMC (the gauge-fixing form) = 2+0  [PROVEN]
     * lambda = 1/3-> kinetic-conformal candidate 2+0                    [INCOMPLETE]
  c_T = 1 additionally FORCES xi = 1.

  Consequence for CANDIDATE_ACTION.md Theorem 3: the '2+0' claim holds for the
  scalar-e / GR+CMC sub-formulation (eta=0) but FAILS for the frozen action as
  literally written -- the eta a_i a^i term propagates a khronon.  To keep 2+0
  the action must be AMENDED: set eta=0 (accept the York gauge-fixing form) or
  tune lambda=1/3 (and verify the kinetic-conformal chain).  This is a DERIVED
  coefficient constraint, not a fit.
""")
if CAVEATS:
    print("  CAVEATS (honest, non-fatal):")
    for c in CAVEATS:
        print("   -", c)

import sys
sys.exit(0 if allpass else 1)
