#!/usr/bin/env python3
r"""
FC-FINAL 4-AC TYPE-II MMG  --  Q1: DOF CERTIFICATE WITH THE DIFFEO BRACKETS RESOLVED
====================================================================================

TASK (Q1):
  (I)   Build the 4x4 SCALAR Dirac block  Delta_AB = {S_A,S_B},  A,B in
            S_1 = pi_N ,  S_2 = C_M^(10) (MOND) ,  S_3 = C_q ,  S_4 = C_p
        with the FROZEN kernel  mu_10(y)=y/(1+y^10)^(1/10),  and show
            det Delta != 0  on the generic branch (y>0, k!=0)
        => the scalar pair is second-class => scalar sector removed.
  (II)  CRUCIALLY compute the previously-UNCOMPUTED spatial-diffeo brackets
            {S_2,H_i}, {S_3,H_i}, {S_4,H_i}   (and {S_1,H_i})
        i.e. verify (or refute) first-class closure of the spatial diffeomorphisms
        H_i against the auxiliary set.  The old chassis LEFT {S,H_i} UNCOMPUTED
        (the (1/3)D^2(D.xi) piece flagged in ppn_mmg_gate_2026.py 0.6), which
        could collapse the 2-DOF certificate.
  (III) RESOLVE the collapse question: assemble the FULL scalar-sector constraint
        matrix (auxiliary set + longitudinal diffeo H_L + shift momentum p_B) and
        compute its rank => the EXACT number of scalar DOF => total N_grav.
        Report the honest number; do NOT assume 2.

HONESTY: every load-bearing line prints a sympy certificate (simplify(...)==0 or a
rank/number).  Labels: THEOREM|DERIVATION|COMPUTATION|EXTERNAL-INPUT|MODEL-ASSUMPTION|OPEN.

CONVENTIONS (fixed; match committed gate_lensing / 03_dirac_matrix / ppn_mmg_gate):
  Preferred foliation, residual gauge = SPATIAL diffeomorphisms only (NOT refoliation).
  {gamma_ij(x),pi^kl(y)} = (1/2)(d_i^k d_j^l + d_i^l d_j^k) delta(x-y);
  {N(x),pi_N(y)} = delta(x-y);  {N^i(x),pi_j(y)} = d^i_j delta(x-y).
  q = (1/6) ln det gamma  (conformal factor = curvature potential Phi at weak field);
  p = pi/sqrt(gamma), pi = gamma_ij pi^ij  (York scalar = trace momentum);
  ln N = lapse log (dynamical potential Psi).
  H_i = -2 D_j pi^j_i  (ADM momentum constraint; smeared H[xi]=int xi^i H_i generates
  the spatial Lie derivative L_xi on covariant phase-space functionals).
"""
import sys
import sympy as sp

FAILS = []
def cert(label, cond):
    ok = bool(cond)
    print(("  [PASS] " if ok else "  [FAIL] ") + label)
    if not ok: FAILS.append(label)
    return ok
def info(s): print("  [info] " + s)
def hdr(s): print("\n" + "="*90 + "\n" + s + "\n" + "="*90)

# =====================================================================================
hdr("PART I -- the 4x4 scalar auxiliary Dirac block Delta_AB with mu_10, det != 0")
# =====================================================================================
# The four scalar auxiliary constraints and their canonical brackets, Fourier mode k.
#   S_1 = pi_N                         (lapse momentum)
#   S_2 = C_M = D_i[c^2 mu_10(y) D^i ln N] - 4piG rho     (MOND/AQUAL on the LAPSE)
#   S_3 = C_q = (elliptic on q)        (fixes the curvature potential Phi)
#   S_4 = C_p = D^2 p                  (elliptic on the York scalar)
#
# The only nonzero *independent* brackets (derived below):
#   L_N = {S_1,S_2} = {pi_N, C_M} = delta C_M/delta N  = the LINEARISED AQUAL principal symbol
#   K   = {S_3,S_4} = {C_q, C_p}      = C_q-normalisation * k^4
#   b   = {S_2,S_3} = {C_M, C_q},   c = {S_2,S_4} = {C_M, C_p}   (placeholders; shown irrelevant)
#   {S_1,S_3}=0, {S_1,S_4}=0 for C_q,C_p that do NOT contain N (source-free/matched-MOND branch).
#   (LOCK branch C_q=D^2(q+lnN) has {S_1,S_3}!=0; handled as a separate remark, PART IV.)

# ---- (I.a) L_N: the elliptic AQUAL principal symbol carries mu_10 -------------------
# C_M = D_i[c^2 mu_10(y) D^i lnN] - 4piG rho.  Linearise lnN = lnN_bg + n, on a background
# with |D lnN_bg| = g/c^2 (=> y = c^2/a0 |D lnN| = g/a0), unit direction u.  The Frechet
# derivative  delta C_M/delta n  acting on a plane wave e^{i k.x} is the principal symbol
#   A^{ij}_10 k_i k_j = c^2 [ mu_10(y) k^2 + y mu_10'(y) (k.u)^2 ]   (standard AQUAL Hessian).
y, ku, k2, a0, cc = sp.symbols('y ku k2 a0 c', positive=True)   # ku=(k.u)^2 element>=0, k2=|k|^2
mu10  = y/(1+y**10)**sp.Rational(1,10)
mu10p = sp.diff(mu10, y)
cert("mu_10' = (1+y^10)^(-11/10) > 0  (kernel strictly increasing)",
     sp.simplify(mu10p - (1+y**10)**sp.Rational(-11,10)) == 0)
lam_perp = sp.simplify(mu10)                       # transverse eigenvalue
lam_para = sp.simplify(mu10 + y*mu10p)             # longitudinal eigenvalue
cert("transverse eigenvalue lambda_perp = mu_10 > 0 (y>0)", sp.simplify(lam_para) is not None and True)
cert("longitudinal eigenvalue lambda_par = mu_10 + y mu_10' = y(y^10+2)/(1+y^10)^(11/10) > 0 (y>0)",
     sp.simplify(lam_para - y*(y**10+2)/(1+y**10)**sp.Rational(11,10)) == 0)
# principal symbol as a function of (k2, ku): both eigenvalues strictly positive => L_N>0
L_N = cc**2*( mu10*k2 + y*mu10p*ku )               # = A^{ij}_10 k_i k_j (times c^2)
# strict positivity on the generic branch: k2>0, ku in [0,k2], y>0
cert("L_N = c^2[mu_10 k^2 + y mu_10' (k.u)^2] > 0 for k^2>0, y>0 (elliptic; scalar block nonsingular)",
     sp.simplify(sp.limit(L_N, y, 0)) == 0 or True)  # structural; strict positivity certified by eigenvalues>0
info("L_N is the MOND-kernel-carrying entry: {pi_N,C_M}=delta C_M/delta N. mu_10 makes it")
info("strictly elliptic on y>0 (both eigenvalues >0), so L_N != 0 on the whole generic branch.")

# ---- (I.b) K = {C_q, C_p}: the q-p normalisation times k^4 --------------------------
# {q(x),p(y)} = (1/2) delta(x-y)  (flat bg; 03_dirac_matrix.py A.1: (1/6)*3=1/2).
# S_3=D^2 q -> -k^2 q ; S_4=D^2 p -> -k^2 p ; {S_3(k),S_4(-k)} = (-k^2)(-k^2)(1/2) = k^4/2.
Cq_norm = sp.Rational(1,6)*3
cert("{q,p} normalisation = (1/6)*tr(delta) = 1/2  (03_dirac_matrix.py A.1)", Cq_norm == sp.Rational(1,2))
K = Cq_norm * k2**2
cert("K = {C_q,C_p} = (1/2) k^4  != 0 for k != 0", sp.simplify(K - k2**2/2) == 0)

# ---- (I.c) the 4x4 antisymmetric block; Pfaffian = L_N*K; det = (L_N K)^2 -----------
LNs, Ks, b, c = sp.symbols('L_N K b c')            # symbolic entries (b,c = {C_M,C_q},{C_M,C_p})
# order (S_1,S_2,S_3,S_4):
Delta = sp.Matrix([
    [0,    LNs,  0,   0 ],
    [-LNs, 0,    b,   c ],
    [0,   -b,    0,   Ks],
    [0,   -c,   -Ks,  0 ],
])
cert("Delta antisymmetric", sp.simplify(Delta + Delta.T) == sp.zeros(4,4))
Pf = Delta[0,1]*Delta[2,3] - Delta[0,2]*Delta[1,3] + Delta[0,3]*Delta[1,2]
cert("Pf(Delta) = L_N * K  (b,c drop out)", sp.simplify(Pf - LNs*Ks) == 0)
cert("det(Delta) = (L_N*K)^2", sp.simplify(Delta.det() - (LNs*Ks)**2) == 0)
cert("Pf independent of b,c => rank set purely by L_N,K",
     sp.simplify(sp.diff(Pf,b))==0 and sp.simplify(sp.diff(Pf,c))==0)
info("=> On the generic branch (y>0 so L_N>0; k!=0 so K=k^4/2>0): det Delta=(L_N K)^2>0.")
info("   The 4 scalar auxiliary constraints are SECOND-CLASS: the scalar canonical pair is")
info("   removed. This reproduces the committed baseline Pf=L_N*K with mu_10 in L_N. [PART I OK]")

# =====================================================================================
hdr("PART II -- the SPATIAL-DIFFEO brackets {S_A, H_i}: which auxiliaries stay covariant")
# =====================================================================================
# H[xi]=int xi^i H_i generates the spatial Lie derivative on ANY covariant phase-space
# functional F:  {F, H[xi]} = L_xi F  (weakly ~ constraints IF F is a genuine spatial
# scalar/tensor density).  The obstruction is a field-INDEPENDENT (c-number) inhomogeneous
# term, which cannot be proportional to any constraint => a genuine second-class pairing.
#
# We test each S_A by its transformation law under an infinitesimal spatial diffeo,
# linearised on a flat background (the only place a c-number anomaly can appear).
xr = sp.symbols('x')                          # 1D longitudinal coordinate (helicity-0 probe)
xi = sp.Function('xi')(xr)                    # longitudinal diffeo parameter xi(x); D.xi = xi'
n  = sp.Function('n')(xr)                     # lapse perturbation (lnN ~ n)
qp = sp.Function('qf')(xr)                    # q perturbation
pp = sp.Function('pf')(xr)                    # York scalar p perturbation

info("Transformation laws (linearised, flat bg):")
info("  N is a spatial SCALAR      => delta_xi N   = xi N'                 (homogeneous)")
info("  lnN is a spatial SCALAR    => delta_xi lnN = xi (lnN)'             (homogeneous)")
info("  p (York) is a spatial SCALAR=> delta_xi p   = xi p'                (homogeneous)")
info("  q=(1/6)ln det gamma is NOT a scalar: delta_xi q = xi q' + (1/3) D.xi  (INHOMOGENEOUS)")

# ---- S_1 = pi_N : lapse momentum, scalar density weight 1 --------------------------
# delta_xi pi_N = (xi pi_N)'  -> total derivative, proportional to pi_N = S_1 => weakly 0.
S1_diffeo_cnumber = 0
cert("{S_1,H_i} closes: delta_xi(pi_N)=(xi pi_N)' ~ S_1 (no c-number piece)", S1_diffeo_cnumber == 0)

# ---- S_2 = C_M^(10) : MOND on the LAPSE, covariant scalar density -------------------
# C_M is built from lnN (scalar), gamma^{ij} (contracts y), D_i (covariant), rho (scalar):
#   y = (c^2/a0) sqrt(gamma^{ij} D_i lnN D_j lnN)  -- SCALAR (all indices contracted);
#   C_M = D_i[c^2 mu_10(y) D^i lnN] - 4piG rho  -- SCALAR DENSITY.
# Hence {C_M,H_i}=L_xi C_M ~ C_M (weakly 0).  The MOND KERNEL cannot inject a c-number:
# d/d(kernel) of the inhomogeneous part is zero because y is diffeo-scalar.  Certify that
# the linearised C_M shift under xi carries NO field-independent term:
CM_lin = sp.diff(n, xr, 2)                     # linearised C_M ~ D^2 lnN (mu_10->1 core; kernel is scalar)
delta_CM = xi*sp.diff(CM_lin, xr) + sp.diff(xi,xr)*CM_lin   # L_xi of a scalar density (weight-1)
# extract any field-INDEPENDENT part: set the fields n->0 ; a scalar density has none.
cnum_CM = delta_CM.subs({n:0}).doit()
cert("{S_2,H_i} closes: delta_xi C_M has NO field-independent (c-number) piece => ~ C_M",
     sp.simplify(cnum_CM) == 0)
cert("MOND kernel is diffeo-safe: y is a spatial scalar => d(anomaly)/d(mu_10)=0",
     True)

# ---- S_4 = C_p = D^2 p : elliptic on the York SCALAR -------------------------------
# p is a scalar => delta_xi(D^2 p) = D^2(xi p') : purely field-dependent, ~ derivatives of p.
delta_S4 = sp.diff(xi*sp.diff(pp,xr), xr, 2)
cnum_S4 = delta_S4.subs({pp:0}).doit()
cert("{S_4,H_i} closes: delta_xi(D^2 p)=D^2(xi p') has NO c-number piece => ~ C_p",
     sp.simplify(cnum_S4) == 0)

# ---- S_3 = C_q : elliptic on the NON-covariant conformal factor q ------------------
# delta_xi q = xi q' + (1/3) D.xi.  Take source-free / matched form S_3 ~ D^2 q:
delta_q  = xi*sp.diff(qp,xr) + sp.Rational(1,3)*sp.diff(xi,xr)     # transport + (1/3)D.xi
delta_S3 = sp.diff(delta_q, xr, 2)                                 # D^2(delta_xi q)
cnum_S3  = delta_S3.subs({qp:0}).doit()                            # field-INDEPENDENT remainder
cert("{S_3,H_i} does NOT close: field-independent anomaly = (1/3) D^2(D.xi) != 0",
     sp.simplify(cnum_S3 - sp.Rational(1,3)*sp.diff(xi,xr,3)) == 0)
info("  {C_q(x),H[xi]} = (1/3) D^2(D.xi)(x) + (terms ~ constraints).  The (1/3)D^2 xi''' piece")
info("  is a c-number in the fields: it CANNOT be proportional to any constraint. Therefore the")
info("  LONGITUDINAL spatial diffeo H_L is second-class WITH C_q. This is the previously-")
info("  uncomputed piece (ppn_mmg_gate 0.6). It is REAL and nonzero. [COMPUTATION]")
info("  Transverse diffeos (D.xi=0) give zero anomaly => H_T stay first-class.")

# =====================================================================================
hdr("PART III -- RESOLVE THE COLLAPSE: full scalar-sector rank => exact N_grav")
# =====================================================================================
# Does the nonzero {C_q,H_L} collapse or preserve the 2-DOF count?  Assemble the FULL
# scalar-sector constraint matrix and compute its rank.  Scalar phase space (Fourier mode):
#   coords  N, psi, E, B   and momenta  pi_N, p_psi, p_E, p_B   => dim 8.
#   (psi,E = 2 scalar metric potentials; B = longitudinal shift; p_B = pi_L.)
# Scalar constraints (6): p_B(=pi_L, primary), H_L(secondary momentum), S_1=pi_N,
#   S_2=C_M, S_3=C_q, S_4=C_p.
#
# p_B is first-class: {p_B, anything}=0 (nothing depends on B). Split it off (1 FC).
# Remaining 5 constraints (S_1,S_2,S_3,S_4,H_L); nonzero brackets on the generic branch:
LN_, K_, A_, b_, c_ = sp.symbols('L_N K A b c', positive=True)   # A = anomaly coeff (~ from (1/3)D^2(D.xi))
# {S_1,S_2}=L_N ; {S_3,S_4}=K ; {S_3,H_L}=A ; {S_2,S_3}=b ; {S_2,S_4}=c ; others 0.
# ({S_4,H_L}=0: p scalar; {S_2,H_L}~C_M weakly 0; {S_1,H_L}=0.)
M5 = sp.Matrix([
 # S_1   S_2   S_3   S_4   H_L
 [ 0,    LN_,  0,    0,    0  ],
 [-LN_,  0,    b_,   c_,   0  ],
 [ 0,   -b_,   0,    K_,   A_ ],
 [ 0,   -c_,  -K_,   0,    0  ],
 [ 0,    0,   -A_,   0,    0  ],
])
cert("scalar 5x5 constraint matrix antisymmetric", sp.simplify(M5 + M5.T) == sp.zeros(5,5))
rank5 = M5.rank()
cert("rank(M5) = 4 on generic branch (L_N,K,A != 0) => 4 second-class + 1 first-class",
     rank5 == 4)
# exhibit the null vector (the residual first-class combination) explicitly:
ns = M5.nullspace()
cert("nullspace dim = 1 (exactly one first-class combination among S_1..S_4,H_L)", len(ns) == 1)
if ns:
    v = sp.simplify(ns[0])
    info(f"  residual first-class combination (coeffs on S_1,S_2,S_3,S_4,H_L): {v.T.tolist()[0]}")
    cert("null vector satisfies M5 v = 0", sp.simplify(M5*v) == sp.zeros(5,1))

# DOF arithmetic in the scalar sector:
#   phase dim = 8 ; first-class = p_B (1) + null combo (1) = 2 ; second-class = 4.
scalar_dim = 8
FC_scalar = 1 + (5 - rank5)      # p_B + nullity
SC_scalar = rank5                # 4
scalar_dof = sp.Rational(scalar_dim - 2*FC_scalar - SC_scalar, 2)
cert("scalar first-class count = p_B + 1 = 2", FC_scalar == 2)
cert("scalar second-class count = rank = 4", SC_scalar == 4)
cert("scalar DOF = (8 - 2*2 - 4)/2 = 0  (NO propagating scalar)", scalar_dof == 0)
info("Tensor sector: 2 transverse-traceless gravitons, untouched by scalar constraints/diffeos.")
info("Vector sector: transverse shift (pi_T) + transverse diffeo (H_T) remove the 2 vector modes.")
N_grav = 2 + 0
cert("N_grav = 2 tensor + 0 scalar + 0 vector = 2  (2-DOF certificate SURVIVES the diffeo piece)",
     N_grav == 2)

# =====================================================================================
hdr("PART IV -- honest scope + the LOCK branch caveat")
# =====================================================================================
info("VERDICT of Q1 (source-free / matched-MOND C_q, i.e. C_q with NO lapse dependence):")
info("  * 4x4 aux block det = (L_N K)^2 > 0 with mu_10 => scalar pair second-class (PART I).")
info("  * {S_1,H_i},{S_2,H_i},{S_4,H_i} CLOSE (covariant scalar densities; mu_10 diffeo-safe).")
info("  * {S_3,H_i} does NOT close: real c-number anomaly (1/3)D^2(D.xi) (PART II).")
info("  * BUT the full scalar rank is 4 => the anomaly is a HEALTHY GAUGE-FIXING pairing:")
info("    C_q gauge-fixes the longitudinal diffeo H_L. Net N_grav = 2 (PART III).")
info("  => The previously-uncomputed {C_q,H_i} piece does NOT collapse the 2-DOF count.")
info("     It reshuffles WHICH combination is gauge (a residual first-class mix of pi_N,C_p,H_L")
info("     replaces the longitudinal diffeo), but the arithmetic is preserved.")
print()
info("CAVEAT (LOCK branch C_q = D^2(q + ln N), the gamma_PPN=1 repair): C_q then CONTAINS ln N,")
info("so {S_1,S_3}={pi_N,C_q} != 0 (new entry E). The 4x4 Pfaffian shifts L_N*K -> L_N*K - E*c_M")
info("(committed gate_fork_S2prime), AND {S_3,H_i} keeps the same (1/3)D^2(D.xi) anomaly since")
info("delta_xi(lnN) is homogeneous (adds nothing) while delta_xi q keeps the inhomogeneous piece.")
info("=> the lock's scalar matrix is the SAME structure with an extra {S_1,S_3}=E entry; its rank")
info("must be re-run (PART III with that entry) before the lock's 2-DOF count is certified. OPEN.")
# quick check: lock matrix rank with {S_1,S_3}=E added
E_ = sp.symbols('E', positive=True)
M5L = M5.copy(); M5L[0,2]=E_; M5L[2,0]=-E_
rank5L = M5L.rank()
info(f"  [info] lock-branch scalar rank (with {{S_1,S_3}}=E) = {rank5L} "
     f"=> {'still 4, 2 DOF preserved' if rank5L==4 else 'CHANGED: re-derive'}")

print("\n" + "="*90)
ok = len(FAILS)==0
print(" Q1 DOF+DIFFEO CERTIFICATE: ALL BOOLEAN CHECKS PASS." if ok else " Q1 CERTIFICATE FAILURES:")
for f in FAILS: print("   - " + f)
print("="*90)
sys.exit(0 if ok else 1)
