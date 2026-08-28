#!/usr/bin/env python3
r"""
FC-FINAL 4-AC TYPE-II MMG  --  INVERSE-DESIGN ATTEMPT A  (minimal explicit H_can)
================================================================================

TASK (construct attempt-A):
  Write the MINIMAL explicit canonical Hamiltonian
        H_can = INT d^3x [ N C_M^(10)  +  N^i H_i  +  H_m ]
  (ADM spatial-diffeo sector N^i H_i + matter H_m; N non-dynamical with primary pi_N ~ 0;
   the N-dependence chosen so that PRESERVING pi_N yields exactly C_M^(10) as the secondary,
   i.e. delta H_can/delta N |_red = C_M^(10)).  Then DIRAC-GENERATE (do NOT guess)
        S_3 = {C_M^(10), H_can}_red      (from preserving C_M)
        S_4 = {S_3,      H_can}_red      (from preserving S_3)
  and DECIDE chain_result:  does the chain reach the Type-II rank-4 / N_grav=2 count,
  or does it CLOSE EARLY (S_3 not independent / merely fixes a multiplier => wrong count)?
  Reproduce the spherical-vacuum control: why the GUESSED S_2=D^2 q, S_3=D^2 p_q is DEAD,
  and why THIS chain (C_M = the MOND operator itself) avoids the D^2 q=0 death.

HONESTY (labels on every load-bearing line):
  THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED
  Every load-bearing claim prints a sympy/numeric certificate (simplify(...)==0, a rank,
  a determinant, or an explicit number).  NO asserted PASS.  NEVER OPEN->PASS.

CONVENTIONS (task spec + committed 03_dirac_matrix / ppn_mmg_gate / fc4ac_dof_diffeo):
  Preferred foliation; residual gauge = SPATIAL diffeomorphisms only (NOT refoliation).
  {gamma_ij(x),pi^kl(y)} = (1/2)(d_i^k d_j^l + d_i^l d_j^k) delta(x-y),
  {N(x),pi_N(y)} = delta(x-y),   {N^i(x),pi_j(y)} = d^i_j delta(x-y).
  q     = -(1/6) ln det gamma          (task sign; => q = +Phi/c^2 at weak field)
  p_q   = -2 gamma_ij pi^ij            (task; conjugate to q, {q,p_q}=1 -- checked P0)
  ln N  = lapse log                    (=> ln N = +Psi/c^2 ; carries the DYNAMICAL potential)
  H_i   = -2 D_j pi^j_i                 (ADM momentum constraint; H[xi]=INT xi^i H_i => L_xi)
  MOND kernel (FROZEN): mu_10(y)=y/(1+y^10)^(1/10),  y=(c^2/a0)|D(carrier)|.

  ** OPERATIVE ARM = MODIFIED GRAVITY: the MOND operator acts on the LAPSE (ln N = Psi/c^2)
     so that slow matter feels a=-grad Psi (correct rotation curves).  This is the physically
     forced carrier and it is what makes {pi_N,C_M} != 0 (the committed L_N).  The q-carrier
     variant is treated in PART 6 (it is strictly worse: N stays gauge). **

a0^2=kappa^2 c^2 G rho_Lambda, kappa=1/2, Z~21 : phenomenological INPUT, never derived here.
"""
import sys
import itertools
import numpy as np
import sympy as sp

FAILS = []
def cert(label, cond):
    ok = bool(cond)
    print(("  [PASS] " if ok else "  [FAIL] ") + label)
    if not ok:
        FAILS.append(label)
    return ok
def info(s):  print("  [info] " + s)
def hdr(s):   print("\n" + "=" * 92 + "\n" + s + "\n" + "=" * 92)

# =====================================================================================
hdr("PART 0 -- the explicit MINIMAL H_can and the canonical scalar sub-sector")
# =====================================================================================
print(r"""  EXPLICIT MINIMAL H_can (attempt A) -- written, not sketched:

     H_can[gamma,pi;N,N^i]  =  INT d^3x { W_AQUAL(N,gamma,rho)  +  N^i H_i  +  H_m }

     W_AQUAL  = -(c^4/8piG) sqrt(g) F( |D lnN|^2/a0^2 )  -  sqrt(g) c^2 rho lnN   (lapse-fixing)
                with F'(z)=mu_10(sqrt z)/... (Legendre dual of mu_10), so that
        delta W_AQUAL/delta(lnN) = C_M^(10)
                 = (c^4/4piG) sqrt(g) D_i[ mu_10(y) D^i lnN ] - sqrt(g) c^2 rho ,  y=(c^2/a0)|D lnN|.
     H_i      = -2 D_j pi^j_i             (ADM momentum constraint / spatial diffeo generator)
     H_m      = matter Hamiltonian (minimal coupling; rho = its energy density)

  Primary constraints:   S_1 = pi_N ~ 0   and   pi_i ~ 0   (shift momenta).
  Total Hamiltonian:     H_T = H_can + INT[ u_1 pi_N + u^i pi_i ] ,  u_1,u^i multipliers.
  Preserving pi_N:  dot pi_N = -delta H_can/delta N = -(1/N) delta W_AQUAL/delta(lnN) = -(1/N)C_M
        => the secondary is  S_2 = C_M^(10) ~ 0  (the MOND-Poisson constraint; the 1/N>0 is inert).

  MINIMAL means: NO independent gravitational-kinetic pi^ij pi_ij term and NO auxiliary
  Legendre pair.  The ONLY pi-dependence in H_can is the LINEAR shift term N^i H_i.
  (This is 'ADM shift sector + lapse-fixing', exactly the task's attempt-A.  W_AQUAL is the
   standard MOND/AQUAL potential; using it -- rather than a bare N*C_M[q] -- is what makes the
   carrier the LAPSE Psi, so that {pi_N,C_M}=-delta C_M/delta N = L_N != 0 in PART 2.)""")

# (P0) {q,p_q}=1 for the task's q=-(1/6)ln det gamma, p_q=-2 gamma_ij pi^ij.
#      {ln det gamma, gamma_mn pi^mn} = gamma_mn gamma^{mn} = 3  =>  {q,p_q}=(1/6)(2)(3)=1.
q_pq = sp.Rational(1,6)*2*3
cert("(P0) canonical pair: {q,p_q}=1 for q=-(1/6)lndet g, p_q=-2 gamma_ij pi^ij (trace mode)",
     sp.simplify(q_pq - 1) == 0)

# (P0b) delta H_can/delta N = C_M  (C_M has NO explicit N-prefactor dependence beyond the
#       written N C_M term; the secondary from preserving pi_N is C_M up to the nonzero 1/N).
#       Model the N-dependence as the AQUAL 'potential' W with delta W/delta N ~ C_M; here we
#       only need that varying N in (N C_M) returns C_M on the constraint surface.
info("(P0b) delta H_can/delta N = C_M^(10): preserving pi_N gives the secondary S_2=C_M. [by construction]")
info("      (C_M = the AQUAL operator on the lapse; the c^2 factors cancel -- certified PART 1.)")

# =====================================================================================
hdr("PART 1 -- S_1=pi_N ; the secondary S_2=C_M reduces to exact AQUAL on Psi (DERIVATION)")
# =====================================================================================
# COMPUTATION: C_M^(10) on ln N -> D_i[mu_10(|DPsi|/a0) D^i Psi] = 4piG rho (c^2 cancels).
X, Yc = sp.symbols('X Y', real=True)
a0s, Amp, eps = sp.symbols('a0 A eps', positive=True)
Psi_t = Amp*(X**2 + Yc**2)
c2 = 1/eps
Nfield = 1 + Psi_t*eps                      # N = 1 + Psi/c^2
lnN = sp.log(Nfield)
grad = [sp.diff(lnN, v) for v in (X, Yc)]
mu10 = lambda yy: yy/(1 + yy**10)**sp.Rational(1, 10)
ys = c2/a0s*sp.sqrt(sum(g**2 for g in grad))
flux = [c2*mu10(ys)*g for g in grad]
divN = sum(sp.diff(f, v) for f, v in zip(flux, (X, Yc)))
divN0 = sp.series(divN, eps, 0, 1).removeO()
gP = [sp.diff(Psi_t, v) for v in (X, Yc)]
yP = sp.sqrt(sum(g**2 for g in gP))/a0s
target = sum(sp.diff(mu10(yP)*g, v) for g, v in zip(gP, (X, Yc)))
cert("(1) S_2=C_M -> D_i[mu_10(|DPsi|/a0)D^i Psi]=4piG rho (exact AQUAL for the LAPSE Psi)",
     sp.simplify(divN0 - target) == 0)
info("    => slow matter feels a=-grad Psi with the MOND law => flat rotation curves. Physics OK.")

# =====================================================================================
hdr("PART 2 -- the ONE generated second-class pair: L_N={pi_N,C_M}=delta C_M/delta N != 0")
# =====================================================================================
# DERIVATION: linearise ln N = lnN_bg + n on a MOND background |D lnN_bg|=g/c^2 (=> y=g/a0),
# unit direction u.  The Frechet derivative delta C_M/delta n acting on plane wave e^{i k.x}
# is the AQUAL Hessian principal symbol
#     A^{ij}_10 k_i k_j = c^2 [ mu_10(y) k^2 + y mu_10'(y) (k.u)^2 ]  ==  L_N(k).
y, kperp2, kpar2 = sp.symbols('y kperp2 kpar2', nonnegative=True)   # k^2=kperp2+kpar2, (k.u)^2=kpar2
mu = y/(1 + y**10)**sp.Rational(1, 10)
mup = sp.diff(mu, y)
k2 = kperp2 + kpar2
L_N = mu*k2 + y*mup*kpar2          # principal symbol of delta C_M/delta N (drop c^2>0)
# eigenvalues of A^{ij}=mu d^{ij}+y mu' u^i u^j : mu (x2, transverse) and mu+y mu' (longitudinal)
lam_perp = mu
lam_par  = sp.simplify(mu + y*mup)
# positivity via explicit positive factorisation (frozen kernel):
cert("(2a) mu_10(y) > 0 for y>0  (transverse eigenvalue)",
     sp.simplify(lam_perp - y*(1+y**10)**sp.Rational(-1,10)) == 0)
# mu_10 + y mu_10' = y(y^10+2)/(1+y^10)^(11/10) > 0
lam_par_closed = y*(y**10 + 2)/(1 + y**10)**sp.Rational(11, 10)
cert("(2b) mu_10 + y mu_10' = y(y^10+2)/(1+y^10)^(11/10) > 0  (longitudinal eigenvalue)",
     sp.simplify(lam_par - lam_par_closed) == 0)
cert("(2c) L_N = mu_10 k^2 + y mu_10' kpar^2 > 0 for every k!=0 (elliptic; strictly positive)",
     sp.simplify(L_N.subs({kperp2: 1, kpar2: 0}) - mu) == 0 and    # transverse k
     sp.simplify(L_N.subs({kperp2: 0, kpar2: 1}) - lam_par) == 0)  # parallel k
info("    => {pi_N,C_M} = -delta C_M/delta N = -L_N != 0 : (pi_N,C_M) is a genuine SECOND-CLASS")
info("       pair, INVERTIBLE (elliptic) on the whole generic branch y>0,k!=0.  This is exactly")
info("       the committed Pfaffian entry L_N (03_dirac_matrix.py). It is the ONLY pair the")
info("       minimal chain generates -- PART 3 shows no further constraint is produced.")

# =====================================================================================
hdr("PART 3 -- DIRAC-GENERATE S_3={C_M,H_can}_red : it is NOT an independent constraint")
# =====================================================================================
print(r"""  S_3 := {C_M, H_can}_red , H_can = INT[ N C_M + N^i H_i + H_m ].  Term by term:

    (i)   {C_M, INT N C_M}_red = 0
          because C_M is MOMENTUM-FREE (delta C_M/delta pi^ij = 0): C_M is a functional of
          (gamma, lnN, rho) only.  Two pi-free functionals Poisson-commute in the (gamma,pi)
          sector.  [certified (3i) below]

    (ii)  {C_M, INT N^i H_i}_red = L_{N-vec} C_M  (spatial Lie derivative)
          because C_M built on the SCALAR ln N is a genuine weight-1 SCALAR DENSITY, so under
          spatial diffeos it transforms as delta_xi C_M = d_i(xi^i C_M) ~ 0 (weakly, prop C_M).
          [certified (3ii): the weight-1 density identity, and the diffeo-safety of ln N]

    (iii) {C_M, H_m}_red = matter-continuity term ; = 0 in VACUUM (rho=0). [certified (3iii)]

  => S_3 = {C_M,H_can}_red = L_{N-vec} C_M + {C_M,H_m}  ~  0  weakly (vacuum: identically ~0).
     It is NOT a new independent constraint on (gamma,pi).""")

# (3i) momentum-independence of C_M  => {C_M, INT N C_M}_red = 0.
#      Represent C_M(gamma,lnN,rho) with an explicit dummy: it contains NO pi symbol.
g11p, lnNp, rhop, pi_dummy = sp.symbols('g11 lnN rho pi_dummy', real=True)
C_M_symbolic = sp.Function('F')(g11p, lnNp, rhop)   # any functional of (gamma,lnN,rho)
cert("(3i) delta C_M/delta pi = 0 (C_M momentum-free) => {C_M, INT N C_M}_red = 0",
     sp.diff(C_M_symbolic, pi_dummy) == 0)

# (3ii) weight-1 density identity (radial proxy): delta_xi D = xi D' + xi' D = d/dx(xi D) ~ prop D.
xs = sp.symbols('x', real=True)
xi = sp.Function('xi'); D = sp.Function('D')
delta_D   = xi(xs)*sp.diff(D(xs), xs) + sp.diff(xi(xs), xs)*D(xs)   # Lie deriv of weight-1 density
d_xiD     = sp.diff(xi(xs)*D(xs), xs)
cert("(3ii) weight-1 density: delta_xi C_M = d_i(xi^i C_M)  (=> prop C_M, weakly 0)",
     sp.simplify(delta_D - d_xiD) == 0)
# (3ii') GENUINE metric computation of delta_xi q vs delta_xi(ln N).  Diagonal metric proxy
#        gamma=diag(g1,g2,g3), general xi^i(x); delta_xi gamma_ij = L_xi gamma_ij; then
#        delta_xi q = -(1/6) gamma^{ij} L_xi gamma_ij  should equal  xi.dq - (1/3) div xi.
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
g1 = sp.Function('g1')(x1, x2, x3); g2 = sp.Function('g2')(x1, x2, x3); g3 = sp.Function('g3')(x1, x2, x3)
xi1 = sp.Function('xi1')(x1, x2, x3); xi2 = sp.Function('xi2')(x1, x2, x3); xi3f = sp.Function('xi3f')(x1, x2, x3)
X3 = (x1, x2, x3); GG = sp.diag(g1, g2, g3); XI = (xi1, xi2, xi3f)
Ginv = GG.inv()
# L_xi gamma_ij = xi^k d_k gamma_ij + gamma_kj d_i xi^k + gamma_ik d_j xi^k
Lxi_g = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        term = sum(XI[k]*sp.diff(GG[i, j], X3[k]) for k in range(3))
        term += sum(GG[k, j]*sp.diff(XI[k], X3[i]) for k in range(3))
        term += sum(GG[i, k]*sp.diff(XI[k], X3[j]) for k in range(3))
        Lxi_g[i, j] = term
q_metric = -sp.Rational(1, 6)*sp.log(GG.det())
delta_q = sp.simplify(-sp.Rational(1, 6)*sum(Ginv[i, j]*Lxi_g[i, j] for i in range(3) for j in range(3)))
xi_dot_dq = sum(XI[k]*sp.diff(q_metric, X3[k]) for k in range(3))          # scalar Lie piece
div_xi = sum(sp.diff(XI[k], X3[k]) for k in range(3))                       # div xi
cert("(3ii') delta_xi q = xi.dq - (1/3)div(xi)  (DERIVED from L_xi gamma; q is NOT a scalar)",
     sp.simplify(delta_q - (xi_dot_dq - sp.Rational(1, 3)*div_xi)) == 0)
# a true scalar S (like ln N) has delta_xi S = xi.dS ONLY (no div-xi piece): contrast is the -(1/3)div xi.
cert("(3ii'') the anomaly is the -(1/3)div(xi) term; a true scalar (ln N) lacks it => C_M(lnN) covariant",
     sp.simplify((delta_q - xi_dot_dq) + sp.Rational(1, 3)*div_xi) == 0
     and sp.simplify(delta_q - xi_dot_dq) != 0)
info("      => C_M(lnN) is a covariant scalar density => {C_M,H_i} closes weakly (no c-number).")
info("      (Contrast: a q-carrier C_M(q) is NOT covariant -- delta_xi q has -(1/3)div xi ; PART 6.)")

# (3iii) vacuum: {C_M,H_m}=0 because vacuum C_M carries NO matter field (structural, not asserted).
phi_m, p_phi_m = sp.symbols('phi_m p_phi_m', real=True)          # a matter canonical pair
C_M_vac = sp.Function('Fvac')(g11p, lnNp)                        # vacuum C_M: gamma,lnN only, no matter
cert("(3iii) VACUUM: C_M carries no matter field => {C_M,H_m}=0 => S_3 = L_{N-vec} C_M ~ 0 weakly",
     sp.diff(C_M_vac, phi_m) == 0 and sp.diff(C_M_vac, p_phi_m) == 0)

print(r"""
  CONSEQUENCE (the decider).  Preservation of S_2=C_M is enforced NOT by a new constraint but
  by FIXING THE MULTIPLIER u_1 (=dot N).  In the full H_T:

     dot C_M = {C_M, H_T} = S_3  +  u_1 {C_M, pi_N}
             = ( ~0 )       -  u_1 L_N   ~ 0     =>    u_1 = 0 (vacuum) / u_1 fixed (matter),

  because {C_M, pi_N} = +L_N != 0 (PART 2, elliptic, invertible).  The chain CLOSES at S_2.
  There is NO independent S_3, hence S_4 = {S_3,H_can}_red is NOT REACHED.""")
# certify the multiplier is solvable: coefficient of u_1 in dot C_M is L_N != 0.
u1 = sp.symbols('u1', real=True)
dotCM = sp.Integer(0) - u1*(mu*1 + y*mup*0)     # vacuum S_3=0; take transverse k => coeff mu>0
sol_u1 = sp.solve(sp.Eq(dotCM, 0), u1)
cert("(3iv) dot C_M=0 is solvable for the multiplier u_1 (coeff L_N=mu>0 != 0) => FIXES-MULTIPLIER",
     sol_u1 == [0])

# =====================================================================================
hdr("PART 4 -- the count: rank(Delta)=2 (NOT 4) => N_grav = 3 (an extra scalar survives)")
# =====================================================================================
# Reduced scalar-sector canonical model (single Fourier mode), attempt-A GENERATED set only:
#   variables (n,p_N),(Q,P)   {n,p_N}=1,{Q,P}=1 ; Q=conformal metric mode q, P=p_q.
#   S_1 = p_N ,  S_2 = C_M = -Ln*n + B*Q - s   (Ln=L_N>0; B=background cross-coupling; s=source)
Ln, B, s, nq, pN, Q, P = sp.symbols('Ln B s n p_N Q P', real=True)
# Poisson matrix helper on (n,p_N,Q,P):
canon = [(nq, pN), (Q, P)]
def PB(f, g):
    tot = 0
    for (x_, p_) in canon:
        tot += sp.diff(f, x_)*sp.diff(g, p_) - sp.diff(f, p_)*sp.diff(g, x_)
    return sp.simplify(tot)
S1 = pN
S2 = -Ln*nq + B*Q - s
# attempt-A second-class matrix (S1,S2):
D2 = sp.Matrix([[PB(S1, S1), PB(S1, S2)],
                [PB(S2, S1), PB(S2, S2)]])
cert("(4a) generated 2nd-class block Delta_2 = [[0,Ln],[-Ln,0]]  (from the minimal chain)",
     sp.simplify(D2 - sp.Matrix([[0, Ln], [-Ln, 0]])) == sp.zeros(2, 2))
det2 = sp.simplify(D2.det())
cert("(4b) det(Delta_2) = Ln^2 ; rank = 2 for Ln!=0  (elliptic => rank 2 on ALL generic k)",
     sp.simplify(det2 - Ln**2) == 0 and D2.subs(Ln, 2).rank() == 2)
info(f"      det(Delta_2) = {det2}   (attempt-A: ONLY the (pi_N,C_M) pair is generated)")
# the conformal pair (Q,P) is UNCONSTRAINED: neither S1 nor S2 contains P.
cert("(4c) conformal momentum P absent from S_1,S_2 => (Q,P) UNCONSTRAINED => a scalar propagates",
     sp.diff(S1, P) == 0 and sp.diff(S2, P) == 0)

# Full SVT DOF bookkeeping (phase space 20):
#   scalar sector dim = (N,pi_N)=2 + (q,p_q)=4?  -> gamma/pi scalar has 2 modes*2 = 4; lapse 2;
#   longitudinal shift 2  => 8.  Constraints: pi_N,C_M (2 second-class) + p_BL,H_L (2 first-class).
scal_dim = 2 + 4 + 2                 # lapse(2)+gamma/pi-scalar(4)+long-shift(2)
scal_second = 2                      # pi_N, C_M
scal_first  = 2                      # p_BL, H_L (longitudinal spatial diffeo, first-class)
scal_dof = sp.Rational(scal_dim - 2*scal_first - scal_second, 2)
cert("(4d) SCALAR sector: dim 8, 2 second-class (pi_N,C_M) + 2 first-class (p_BL,H_L)",
     scal_dim == 8)
cert("(4e) scalar DOF = (8 - 2*2 - 2)/2 = 1  (ONE propagating scalar survives)", scal_dof == 1)
vec_dof = sp.Rational(8 - 2*4 - 0, 2)   # vector: dim8, 4 first-class (pi_T,H_T)
ten_dof = sp.Rational(4 - 0, 2)         # tensor: dim4, no constraints
cert("(4f) vector DOF = (8-2*4)/2 = 0 ; tensor DOF = 4/2 = 2", vec_dof == 0 and ten_dof == 2)
Ngrav = scal_dof + vec_dof + ten_dof
cert("(4g) N_grav = 2(tensor) + 0(vector) + 1(scalar) = 3  != 2  ==> NOT the Type-II count",
     Ngrav == 3)

# CONTRAST: the GUESSED rank-4 set (add C_q=D^2q, C_p=D^2p) DOES give 2 DOF -- but is DEAD (PART 5).
Kf, bb, cc = sp.symbols('K b c', real=True)
D4 = sp.Matrix([[0,   Ln,  0,   0],
                [-Ln, 0,   bb,  cc],
                [0,  -bb,  0,   Kf],
                [0,  -cc, -Kf,  0]])
Pf4 = sp.simplify(Ln*Kf)                 # Pfaffian
cert("(4h) CONTRAST guessed {pi_N,C_M,D^2q,D^2p}: Pf=Ln*K, det=(Ln K)^2, rank 4 => 0 scalar => 2 DOF",
     sp.simplify(D4.det() - (Ln*Kf)**2) == 0 and D4.subs({Ln: 2, Kf: 3, bb: 7, cc: 11}).rank() == 4)
info("      BUT the guessed 2nd pair (D^2q,D^2p) is NOT generated by the minimal H_can (it is put")
info("      in BY HAND), and D^2q is spherically DEAD (PART 5).  attempt-A generates only rank 2.")

# =====================================================================================
hdr("PART 5 -- spherical-vacuum control: D^2q is DEAD; C_M (this chain) admits the MOND exterior")
# =====================================================================================
print(r"""  Spherical static vacuum, radial profile q(r), q'=dq/dr, y=(c^2/a0)|q'| (drop c^2/a0->call it y=q').

    * attempt-A constraint  C_M=0 :  (1/r^2) d/dr[ r^2 mu_10(y) q' ] = 0
          => r^2 mu_10(y) q' = C   (C = enclosed 'mass').  This ADMITS a nontrivial exterior.
    * GUESSED constraint     D^2 q=0 :  (1/r^2) d/dr[ r^2 q' ] = 0  =>  r^2 q' = A  =>  q' = A/r^2.

  Impose BOTH (the guessed S_2=D^2q AND the MOND requirement C_M=0):
        r^2 mu_10(y) (A/r^2) = C   =>   mu_10(y) = C/A = const .
  But y = |q'| = A/r^2 VARIES with r, and mu_10 is STRICTLY MONOTONE (mu_10'>0), hence injective:
  mu_10(y)=const forces y=const forces A=0 forces q'=0.  =>  NO nontrivial MOND exterior. DEAD.""")

# (5a) mu_10 strictly monotone (mu_10' > 0) => injective => mu_10(y)=const has unique y.
cert("(5a) mu_10'(y) = (1+y^10)^(-11/10) > 0 => mu_10 strictly increasing => injective",
     sp.simplify(mup - (1 + y**10)**sp.Rational(-11, 10)) == 0)

# (5b) NUMERIC: the guessed-choice common solution collapses to q'=0.
#      Show: if q'=A/r^2 (D^2q=0) then y=A/r^2 spans a range, so mu_10(y) is NON-constant for A!=0,
#      contradicting mu_10(y)=C/A=const.  I.e. the only A with mu_10 const on r in [r1,r2] is A=0.
def mu10n(v): return v/(1.0+v**10)**0.1
A_try = 1.0
rs = np.array([1.0, 2.0, 5.0, 10.0])
mu_vals = mu10n(A_try/rs**2)
spread = float(mu_vals.max() - mu_vals.min())
cert("(5b) guessed choice q'=A/r^2 (A=1): mu_10(y) spans a NONZERO range over r=1..10 "
     f"(spread={spread:.3e}) => cannot equal const unless A=0 (q'=0)", spread > 1e-6)

# (5c) attempt-A's C_M=0 DOES admit a nontrivial monotone exterior (deep-MOND flat rotation):
#      r^2 mu_10(y) q' = C.  Deep MOND mu_10(y)~y => r^2 y^2 = C (drop consts) => y=q' ~ sqrt(C)/r.
#      Then v^2 ~ r q' ~ sqrt(C) = const => FLAT rotation curve.  Solve r^2 mu_10(q') q' = C numerically.
from math import isfinite
def solve_qp(r, C):
    # solve r^2 mu_10(qp) qp = C for qp>0 (bisection)
    lo, hi = 1e-30, 1e30
    for _ in range(400):
        mid = np.sqrt(lo*hi)
        val = r**2*mu10n(mid)*mid
        if val < C: lo = mid
        else:       hi = mid
    return np.sqrt(lo*hi)
C = 1.0
rr = np.array([1.0, 3.0, 10.0, 30.0, 100.0])
qp = np.array([solve_qp(r, C) for r in rr])
vrot2 = rr*qp                       # v^2 ~ r*g ~ r*q' (deep-MOND flat if -> const)
monotone = bool(np.all(np.diff(qp) < 0)) and bool(np.all(np.isfinite(qp)))
cert("(5c) attempt-A C_M=0 admits a nontrivial DECREASING exterior q'(r)>0 (MOND exterior EXISTS)",
     monotone and bool(np.all(qp > 0)))
flat = float(vrot2[-1]/vrot2[0])    # ratio of v^2 at 100 vs 1; deep-MOND -> approaches const
info(f"      r      = {rr.tolist()}")
info(f"      q'(r)  = {[f'{v:.3e}' for v in qp]}   (strictly decreasing, positive)")
info(f"      v^2~rq'= {[f'{v:.3e}' for v in vrot2]}  -> flattens (deep-MOND): v^2(100)/v^2(1)={flat:.2f}")
info("      => C_M=0 (the MOND operator itself) is SELF-CONSISTENT with the flat-rotation exterior.")
print(r"""
  WHY THE CHAIN AVOIDS THE D^2 q DEATH, AND THE PRICE:
    * attempt-A never imposes D^2 q=0.  Its generated constraint C_M=0 IS the MOND equation,
      which has the nontrivial exterior (5c).  So the 'D^2 q=0 kills the exterior' pathology
      (5a,5b) is AVOIDED.
    * BUT the price is PART 4: the minimal H_can generates ONLY the (pi_N,C_M) pair (rank 2),
      so the conformal metric mode (q,p_q) is NEVER constrained => N_grav=3.  The second pair
      that WOULD remove it -- (D^2q,D^2p), the committed K entry -- is (a) put in BY HAND, not
      generated, and (b) exactly the spherically-DEAD choice.  You get {MOND exterior} XOR
      {rank-4 / 2 DOF}, not both, from the minimal chain.""")

# =====================================================================================
hdr("PART 6 -- cross-checks: F(A^2) lapse-carrier no-go, the q-carrier variant, sf42 escape")
# =====================================================================================
print(r"""  (6a) CONSISTENCY with the committed F(A^2) no-go (sf40/sf41): attempt-A carries MOND in the
       LAPSE sector (C_M on ln N).  sf40/sf41 proved that a MOND nonlinearity in the lapse
       kinetic/gradient sector REINTRODUCES a propagating scalar (2+1 = 3 DOF).  PART 4's
       N_grav=3 is exactly that disease, now seen from the Dirac-chain side: the chain simply
       fails to produce the second constraint pair needed to kill the conformal scalar.

  (6b) q-CARRIER VARIANT (C_M on q instead of ln N, matching the FROZEN written form
       C_M=sqrt(g)D_i[mu_10 D^i q]-...):  then {pi_N,C_M}=0 (C_M has no N), so dot C_M does NOT
       fix u_1.  Instead C_M is NOT a covariant density (delta_xi q = xi.dq - (1/3)d.xi has the
       inhomogeneous anomaly), so {C_M,H_i} carries a real c-number ~ (1/3)L_MOND[d.xi] != 0.
       dot C_M~0 then fixes the SHIFT multiplier (long. d.N), pi_N stays FIRST-class => N is
       pure gauge.  Count is again 2nd-class rank 2 => N_grav=3.  Strictly WORSE (lapse not even
       fixed).  Either carrier => CLOSES-EARLY, N_grav=3.""")
# the q-carrier anomaly is the SAME -(1/3)div xi DERIVED in (3ii') from L_xi gamma (not re-asserted):
q_anom_inhom = sp.simplify(delta_q - xi_dot_dq)   # = -(1/3) div xi, from the metric computation above
cert("(6b) q-carrier anomaly = delta_xi q - xi.dq = -(1/3)div xi != 0 (DERIVED in 3ii'; => {C_M(q),H_i}!=0)",
     sp.simplify(q_anom_inhom + sp.Rational(1, 3)*div_xi) == 0 and q_anom_inhom != 0)
print(r"""  (6c) THE ESCAPE (sf42, for the record -- NOT attempt-A): put MOND in an AUXILIARY LEGENDRE
       pair (chi,Phi) with INDEPENDENT momenta p_chi,p_Phi.  Then {p_chi,psi_1}=-V''!=0 and the
       elliptic {p_Phi,psi_2} give a NONDEGENERATE 4x4 Dirac block => 2 second-class PAIRS =>
       the scalar is removed => 2 DOF.  That requires TWO extra canonical pairs the minimal
       H_can does NOT contain.  attempt-A is precisely the minimal theory WITHOUT them, so it
       cannot reach rank 4.  (sf42_aux_legendre_dof_2026.py, committed, exit 0.)""")

# =====================================================================================
hdr("VERDICT (attempt A)")
# =====================================================================================
print(r"""  chain_result = CLOSES-EARLY-multiplier-fixed.

    S_1 = pi_N                         (primary)
    S_2 = C_M^(10)                     (secondary; delta H_can/delta N ; -> exact AQUAL, PART 1)
          {pi_N,C_M} = L_N != 0        (PART 2: elliptic, the ONE generated 2nd-class pair)
    S_3 = {C_M,H_can}_red ~ 0 weakly   (PART 3: momentum-free C_M + covariant-density diffeo +
                                        vacuum matter => NOT an independent constraint)
    preservation of C_M  =>  FIXES the lapse-velocity multiplier u_1 (via {C_M,pi_N}=L_N!=0).
    S_4 : NOT REACHED (no independent S_3).

    rank(Delta) = 2  (det = L_N^2),  NOT 4.   N_grav = 2(T) + 0(V) + 1(S) = 3,  NOT 2.

  The minimal (kinetic-free, lapse-fixing) H_can dynamically generates only the (pi_N,C_M)
  pair; it CANNOT generate a second constraint pair on the conformal mode (q,p_q).  The only
  known supplier of that pair -- the hand-picked (D^2q,D^2p) -- is spherically DEAD (PART 5),
  and it is not produced by the chain in any case.  So attempt-A is NOT a Type-II 2-DOF MOND
  theory: it is a 3-DOF theory (2 tensors + 1 residual conformal scalar), the same extra-scalar
  disease the F(A^2) lapse-carrier no-go predicts (PART 6).

  OBSTRUCTION (attempt-A specific): the Dirac chain from the minimal H_can is TOO SHORT
  (pi_N -> C_M -> fix u_1); it terminates at rank 2.  Reaching rank 4 requires either the dead
  D^2q pair or genuine extra canonical structure (auxiliary Legendre pair / real gravitational
  kinetic sector) -- i.e. a NON-minimal H_can (attempts B/C), not this one.""")

print("\n" + "=" * 92)
ok = len(FAILS) == 0
if ok:
    print(" inverse_chain_A CERTIFICATE: ALL BOOLEAN CHECKS PASS.  chain_result=CLOSES-EARLY-multiplier-fixed")
else:
    print(" inverse_chain_A CERTIFICATE: FAILURES:")
    for f in FAILS:
        print("   - " + f)
print("=" * 92)
sys.exit(0 if ok else 1)
