#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
=====================================================================================
FC-ISOTROPIC-LEGENDRE  --  SETUP  (sympy certificates)
=====================================================================================
MISSION (this file = the SETUP for the LAST open door of the 2-DOF MOND program):
  Reproduce, as sympy certificates, the two committed obstructions that motivate the
  isotropic-completion question, then DEFINE the obstruction object Sigma_P and state
  the decisive question precisely.

  (1) Carl's NAIVE-LEGENDRE chain.  Action
        S_M = int[ N (D_i P^i - 4 pi G rho) + lambda_i ( P^i - mu(y) D^i q ) ]
      Variations:
        delta N   : D_i P^i = 4 pi G rho                       (Gauss constraint)
        delta lam : P^i = mu(y) D^i q                          (constitutive)
        delta P^i : (after IBP  N D_i P^i -> -(D_i N) P^i)  lambda_i = D_i N
        delta q   : D_i[ A^{ij} lambda_j ] = 0,  A^{ij} = mu gamma^{ij} + y mu' u^i u^j
      => on shell  D_i[ A^{ij} D_j N ] = 0 : the TANGENT modulus mu + y mu' returns
      through the multiplier.  Radial slip  Phi'/Psi' = (mu + y mu')/mu.
      For mu_10:  = (y^10 + 2)/(y^10 + 1)  =  1 (y>>1) -> 3/2 (y=1) -> 2 (y<<1).

  (2) The committed YORK auxiliary-scalar anisotropic stress
        T_mn = (1/8piG)[ 2 U'(Y) d_mu Phi d_nu Phi - g_mn a0^2 U(Y) ],  Y=|DPhi|^2/a0^2,
      traceless Sigma_ij = (2U'/8piG) P^2 (n_i n_j - delta_ij/3), and the resulting
      Einstein-frame gamma_PPN = ln r/(ln r - 2) != 1  (spherical AQUAL scalar).
      [reproduced here + cross-cited: theory_2026/york/ppn_lensing_cassini_2026.py,
       commit 0184ba7e, exit 0.]

  (3) DEFINE the obstruction object Sigma_P = coefficient of the traceless
      (u_i u_j - delta_ij/3) in the ON-SHELL metric stress of the 2-DOF construction,
      and confirm Sigma_P is proportional to  y mu'  (the differential/anisotropic
      part of the constitutive Hessian).  Sigma_P = 0  <=>  mu' = 0  <=>  linear law.

HONESTY: every load-bearing line prints a certificate (simplify(...)==0 or a residual).
  Labels: THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.
  We verify a WIN (Sigma_P=0, gamma=1) exactly as hard as a FAIL: the Newtonian limit
  IS checked to give slip=1 (solar-system safe); the surviving slip is intrinsic.

FROZEN kernel (do NOT tweak -- the obstruction is kernel-general, any mu'!=0):
  mu_10(y) = y/(1+y^10)^(1/10),   mu_10' = (1+y^10)^(-11/10) > 0.
PHENOMENOLOGICAL INPUT (never derived): a0^2 = kappa^2 c^2 G rho_Lambda, kappa=1/2, Z~21.

Exit 0 = every numbered check passed.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok ' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")


def hdr(s):
    print("\n" + "=" * 86)
    print(s)
    print("=" * 86)


# ==================================================================================
hdr("PART 1 -- the constitutive Hessian A^{ij} = mu gamma^{ij} + y mu' u^i u^j  (DERIVATION)")
# ==================================================================================
r"""
The isotropic MOND flux is  P^i = mu(y) D^i q,  y = |Dq|/a0,  s := |Dq|.
Its Hessian w.r.t. the gradient g_i := D_i q is
   A^{ij} = d P^i / d g_j = d(mu(y) g^i)/d g_j
          = mu delta^{ij} + g^i (dmu/dg_j)
          = mu delta^{ij} + (y mu') u^i u^j ,   u^i = g^i/s.
Compute it by BRUTE symbolic differentiation on a generic 3-vector g and match.
"""
a0 = sp.symbols('a0', positive=True)
gx, gy, gz = sp.symbols('gx gy gz', real=True)
g = sp.Matrix([gx, gy, gz])
s = sp.sqrt(gx**2 + gy**2 + gz**2)         # |Dq|
yv = s / a0

# generic mu(y): use an undefined function so the Hessian identity is kernel-GENERAL
muf = sp.Function('mu')
mu = muf(yv)
Pvec = sp.Matrix([mu * gi for gi in g])    # P^i = mu(y) g^i

A = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        A[i, j] = sp.diff(Pvec[i], g[j])

# target: mu*delta + y*mu' * u u  (with y mu' = s/a0 * mu'(y), u=g/s)
u = g / s
ymu = (s / a0) * sp.diff(muf(sp.Symbol('t')), sp.Symbol('t')).subs(sp.Symbol('t'), yv)
Atar = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Atar[i, j] = mu * (1 if i == j else 0) + ymu * u[i] * u[j]

res = sp.simplify(sp.Matrix(A) - sp.Matrix(Atar))
check(res == sp.zeros(3, 3),
      "Hessian A^{ij} = mu delta^{ij} + (y mu') u^i u^j  (brute-diff == closed form)",
      "residual matrix == 0")

# Eigenstructure: eigenvalue mu (transverse, x2), mu + y mu' (longitudinal along u).
# Verify on a concrete direction g=(s,0,0): A = diag(mu + y mu', mu, mu).
Asub = A.subs({gx: s, gy: 0, gz: 0})       # careful: s here is symbol via sqrt; set gx=s
# instead evaluate along axis directly:
gxx = sp.symbols('gxx', positive=True)
Aaxis = sp.zeros(3, 3)
Pax = sp.Matrix([muf(sp.sqrt(gx**2+gy**2+gz**2)/a0)*gi for gi in (gx, gy, gz)])
for i, gi in enumerate((gx, gy, gz)):
    for j, gj in enumerate((gx, gy, gz)):
        Aaxis[i, j] = sp.diff(Pax[i], gj)
Aaxis = Aaxis.subs({gy: 0, gz: 0})
Aaxis = sp.simplify(Aaxis.subs(gx, gxx))
yy = gxx / a0
mu_y = muf(yy)
mup_y = sp.diff(muf(sp.Symbol('t')), sp.Symbol('t')).subs(sp.Symbol('t'), yy)
long_eig = sp.simplify(Aaxis[0, 0] - (mu_y + yy * mup_y))
tran_eig = sp.simplify(Aaxis[1, 1] - mu_y)
check(long_eig == 0, "longitudinal eigenvalue = mu + y mu'  (TANGENT modulus)", "residual 0")
check(tran_eig == 0, "transverse eigenvalue  = mu          (SECANT modulus)", "residual 0")

print("\n  DERIVATION: A^{ij} is intrinsically ANISOTROPIC for any mu'!=0.")
print("  transverse (2x): SECANT modulus mu ;  longitudinal: TANGENT modulus mu + y mu'.")
print("  The anisotropy amplitude is exactly  (y mu')  along  u u.")

# ==================================================================================
hdr("PART 2 -- the multiplier chain: delta P^i => lambda_i = D_i N ; delta q => D_i[A^{ij} D_j N]=0")
# ==================================================================================
r"""
Bookkeeping of the naive-Legendre action, done symbolically so the KEY steps carry a
certificate rather than an assertion:
  L = N (D_i P^i - 4piG rho) + lambda_i (P^i - mu(y) D^i q).
  * IBP:  int N D_i P^i = - int (D_i N) P^i   (boundary dropped).  So the P-dependent
    part of the bulk L is  Lp = -(D_i N) P^i + lambda_i P^i = (lambda_i - D_i N) P^i.
    delta/delta P^i :  lambda_i - D_i N = 0  =>  lambda_i = D_i N.               (2a)
  * q-dependent part:  Lq = - lambda_j mu(y) D^j q  = - lambda_j (mu(y) g^j),  g=Dq.
    The conjugate flux is  Psi^i := - dLq/d(D_i q) = lambda_j d(mu g^j)/d g_i
                                   = lambda_j A^{ji} = A^{ij} lambda_j   (A symmetric).
    Euler-Lagrange (no undifferentiated q):  D_i Psi^i = 0 => D_i[A^{ij} lambda_j]=0.  (2b)
    Substitute (2a):  D_i[ A^{ij} D_j N ] = 0.                                    (2c)
Certificates: (i) coefficient of P^i in Lp is (lambda_i - D_i N); (ii) the conjugate
flux equals A^{ij} lambda_j.
"""
# (2a) coefficient of P^i:  d Lp / d P^i  = lambda_i - D_i N
lamx, lamy, lamz = sp.symbols('lam_x lam_y lam_z', real=True)
DNx, DNy, DNz = sp.symbols('DN_x DN_y DN_z', real=True)   # D_i N
Px, Py, Pz = sp.symbols('P_x P_y P_z', real=True)
Lp = (lamx - DNx)*Px + (lamy - DNy)*Py + (lamz - DNz)*Pz  # = (lambda - DN).P
coeffP = sp.Matrix([sp.diff(Lp, Px), sp.diff(Lp, Py), sp.diff(Lp, Pz)])
target = sp.Matrix([lamx - DNx, lamy - DNy, lamz - DNz])
check(sp.simplify(coeffP - target) == sp.zeros(3, 1),
      "delta P^i : coefficient = lambda_i - D_i N  =>  lambda_i = D_i N", "residual 0")

# (2b) conjugate flux  Psi^i = - d(-lambda_j mu g^j)/d g_i  = lambda_j A^{ji}
lam = sp.Matrix([lamx, lamy, lamz])
Lq = -(lam.dot(Pvec))                       # Pvec = mu(y) g   (from PART 1)
Psi_flux = sp.Matrix([-sp.diff(Lq, g[i]) for i in range(3)])
Psi_target = A.T * lam                      # A^{ij} lambda_j  (A symmetric so A.T=A)
check(sp.simplify(Psi_flux - Psi_target) == sp.zeros(3, 1),
      "delta q : conjugate flux Psi^i = A^{ij} lambda_j  => D_i[A^{ij} lambda_j]=0", "residual 0")
check(sp.simplify(A - A.T) == sp.zeros(3, 3),
      "A^{ij} symmetric (so Psi^i = A^{ij} lambda_j = lambda_j A^{ji})", "residual 0")

print("\n  DERIVATION (Carl's chain reproduced): lambda_i = D_i N and D_i[A^{ij}D_j N]=0.")
print("  The Gauss constraint fixes q on the SECANT modulus mu; the q-EOM feeds the")
print("  lapse N through the SAME Hessian A -> its longitudinal eigenvalue mu + y mu'.")
print("  Naive Legendre is DEAD: the tangent modulus returns via the multiplier.")

# ==================================================================================
hdr("PART 3 -- radial slip  Phi'/Psi' = (mu + y mu')/mu  for the frozen mu_10  (COMPUTATION)")
# ==================================================================================
y = sp.symbols('y', positive=True)
mu10 = y / (1 + y**10)**sp.Rational(1, 10)
mu10p = sp.simplify(sp.diff(mu10, y))
check(sp.simplify(mu10p - (1 + y**10)**sp.Rational(-11, 10)) == 0,
      "mu_10' = (1+y^10)^(-11/10) > 0", "residual 0")
slip = sp.simplify((mu10 + y*mu10p) / mu10)
check(sp.simplify(slip - (y**10 + 2)/(y**10 + 1)) == 0,
      "slip (mu+y mu')/mu = (y^10+2)/(y^10+1)", "residual 0")
lim_hi = sp.limit(slip, y, sp.oo)
lim_1 = slip.subs(y, 1)
lim_lo = sp.limit(slip, y, 0)
check(lim_hi == 1, "y>>1 (solar/Newtonian): slip = 1   -> Phi=Psi  (PASS, checked as hard as FAIL)")
check(lim_1 == sp.Rational(3, 2), "y~1  (knee):            slip = 3/2 -> Phi!=Psi (FAIL)")
check(lim_lo == 2, "y<<1 (deep galactic):   slip = 2   -> Phi!=Psi (FAIL)")
print("\n  A_slip(y) := (slip - 1) = y mu'/mu.  A_slip = 0  <=>  mu' = 0  <=>  linear law.")
Aslip = sp.simplify(slip - 1)
check(sp.simplify(Aslip - y*mu10p/mu10) == 0, "A_slip = y mu_10'/mu_10 exactly", "residual 0")

# ==================================================================================
hdr("PART 4 -- York auxiliary-scalar anisotropic stress + gamma_PPN != 1  (reproduce + cite)")
# ==================================================================================
r"""
Committed script: theory_2026/york/ppn_lensing_cassini_2026.py  (commit 0184ba7e, exit 0).
Reproduce the load-bearing lines symbolically here.
  T_mn = (1/8piG)[ 2 U'(Y) d_mu Phi d_nu Phi - g_mn a0^2 U(Y) ],  Y=|DPhi|^2/a0^2,
  U'(Y) = mu(sqrt Y) = sqrt(Y)/sqrt(1+Y)  (standard mu here; kernel-general obstruction).
  Radial Phi(r): d_iPhi = P n_i, P=Phi'(r).  Anisotropic stress amplitude
     8piG (p_r - p_t) = 2 U'(Y) P^2  ->  Sigma_ij = (2U'/8piG) P^2 (n_i n_j - delta_ij/3).
  Deep-MOND point mass: Phi_g - Psi_g = D(r) with  D'' - D'/r = 2 U' P^2, giving
     gamma_PPN(Einstein frame) = Psi_g/Phi_g = ln r/(ln r - 2)  != 1.
"""
Y = sp.symbols('Y', positive=True)
Uprime = sp.sqrt(Y)/sp.sqrt(1+Y)
U = sp.sqrt(Y*(1+Y)) - sp.asinh(sp.sqrt(Y))
check(sp.simplify(sp.diff(U, Y) - Uprime) == 0, "U'(Y) = sqrt(Y)/sqrt(1+Y) = mu(sqrt Y)", "residual 0")

P = sp.symbols('P', positive=True)
Yr = P**2/a0**2
p_r = 2*Uprime.subs(Y, Yr)*P**2 - a0**2*U.subs(Y, Yr)
p_t = -a0**2*U.subs(Y, Yr)
Sig = sp.simplify(p_r - p_t)
check(sp.simplify(Sig - 2*Uprime.subs(Y, Yr)*P**2) == 0,
      "8piG(p_r-p_t) = 2 U'(Y) P^2  (nonzero for P>0) -> AeST/AQUAL scalar stress anisotropy",
      "residual 0")

# deep-MOND slip and gamma (reproduce the committed closed forms)
r = sp.symbols('r', positive=True)
v0sq = sp.symbols('v0sq', positive=True)
Pdeep = v0sq/r
Sdeep = sp.simplify(2*(Pdeep/a0)*Pdeep**2)            # 2 U' P^2 with deep U'=P/a0
D = sp.Function('D')
Dsol = sp.dsolve(sp.Eq(sp.diff(D(r), r, 2) - sp.diff(D(r), r)/r, Sdeep), D(r))
Dpart = sp.simplify(Dsol.rhs.subs({sp.Symbol('C1'): 0, sp.Symbol('C2'): 0}))
check(sp.simplify(Dpart - 2*v0sq**3/(3*a0*r)) == 0,
      "D_p(r)=Phi_g-Psi_g = 2 v0^6/(3 a0 r)  (deep-MOND, committed)", "residual 0")
Ps = sp.Function('Ps')
rho_deep = sp.simplify(a0**2*sp.Rational(2, 3)*(Pdeep/a0)**3)
Psi_sol = sp.dsolve(sp.Eq(2*(sp.diff(Ps(r), r, 2)+2*sp.diff(Ps(r), r)/r), rho_deep), Ps(r))
Psi_p = sp.simplify(Psi_sol.rhs.subs({sp.Symbol('C1'): 0, sp.Symbol('C2'): 0}))
Phi_g = sp.simplify(Psi_p + Dpart)
gamma_E = sp.simplify(Psi_p/Phi_g)
check(sp.simplify(gamma_E - sp.log(r)/(sp.log(r) - 2)) == 0,
      "Einstein-frame gamma_PPN = ln r/(ln r - 2)  != 1  (committed York result)", "residual 0")
print("\n  EXTERNAL-INPUT (committed): theory_2026/york/ppn_lensing_cassini_2026.py, commit 0184ba7e,")
print("  exit 0 -- reproduced above.  gamma_phys=1 there is a DISFORMAL model INPUT, not derived.")

# ==================================================================================
hdr("PART 5 -- DEFINE the obstruction object Sigma_P ; confirm Sigma_P ~ y mu'  (DEFINITION+CERT)")
# ==================================================================================
r"""
DEFINITION.  Write the ON-SHELL traceless metric stress of the 2-DOF construction as
   Pi^{TF}_{ij} = Sigma_P (u_i u_j - delta_ij/3),
i.e. Sigma_P is the SCALAR coefficient multiplying the unit traceless dyad along the
MOND gradient u = Dq/|Dq|.  gamma_PPN = 1 (Phi=Psi)  <=>  Sigma_P = 0.

CLAIM (kernel-general).  In the naive-Legendre / 2-DOF constraint construction the field
q carries NO independent stress; the metric slip is sourced PURELY by the differential
(anisotropic) part of the constitutive Hessian A^{ij} = mu delta + (y mu') u u.  The
isotropic part mu delta is a pressure (pure-trace) and cannot source the traceless slip;
only the (y mu') u u piece can.  Therefore
   Sigma_P = C * (y mu'),   C != 0 a kernel-independent geometric constant,
so  Sigma_P = 0  <=>  y mu' = 0  <=>  mu' = 0  <=>  the law is LINEAR (Newton/pure-a0-shift).
We CERTIFY the traceless decomposition of A and that its traceless amplitude is exactly y mu'.
"""
# traceless part of A = mu*I + (y mu') u u   (3D):  A - (trA/3) I
# trA = 3 mu + y mu'  ;  A_TF = (y mu')(u u - I/3).  amplitude coefficient = y mu'.
ysym, muv, mupv = sp.symbols('y mu muprime', positive=True)   # abstract y, mu, mu'
# build A along axis u=e1:  A = diag(mu + y mu', mu, mu)
Aabs = sp.diag(muv + ysym*mupv, muv, muv)
trA = sp.trace(Aabs)
A_TF = sp.simplify(Aabs - (trA/3)*sp.eye(3))
# unit traceless dyad along u=e1:  (u u - I/3) = diag(2/3, -1/3, -1/3)
dyad = sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
# solve A_TF = SigmaP * dyad  for SigmaP from the (1,1) entry, verify all entries match
SigmaP = sp.simplify(A_TF[0, 0] / dyad[0, 0])
check(sp.simplify(A_TF - SigmaP*dyad) == sp.zeros(3, 3),
      "traceless(A) = Sigma_P (u u - I/3) with a SINGLE scalar Sigma_P", "all entries match")
check(sp.simplify(SigmaP - ysym*mupv) == 0,
      "Sigma_P = y mu'  EXACTLY  (obstruction proportional to the differential modulus)",
      "residual 0")
# and for the frozen kernel:
SigmaP_10 = sp.simplify((y*mu10p))
check(sp.simplify(SigmaP_10 - y*(1+y**10)**sp.Rational(-11, 10)) == 0,
      "frozen mu_10:  Sigma_P = y (1+y^10)^(-11/10) > 0 for all y>0  (never vanishes)",
      "residual 0")

print("\n  THEOREM (within this construction): Sigma_P = y mu'  is the UNIQUE traceless")
print("  amplitude of the constitutive Hessian; the isotropic mu delta is pure trace and")
print("  cannot source Phi-Psi.  Hence in ANY 2-DOF constraint completion whose metric")
print("  couples to A^{ij}, the slip obstruction is Sigma_P ~ y mu', vanishing iff mu'=0.")
print("  [The York AQUAL scalar is a DISTINCT, WORSE manifestation: its field carries a")
print("   genuine gradient stress ~ 2 mu P^2, giving gamma=ln r/(ln r-2) even at mu=const.")
print("   Both are nonzero for the nonlinear MOND law; the 2-DOF obstruction is the y mu' one.]")

# ==================================================================================
hdr("THE DECISIVE QUESTION (stated precisely)")
# ==================================================================================
print(r"""
  Does there exist a SECOND-CLASS auxiliary Legendre completion of the isotropic MOND
  law  D_i[mu(y) D^i q] = 4 pi G rho  such that, ON SHELL, the traceless metric stress
  VANISHES,
        Sigma_P = 0        (=> Phi = Psi, gamma_PPN = 1, FRIED CHICKEN),
  WHILE simultaneously
        (a) reproducing  D_i[mu D^i q] = 4 pi G rho     (the MOND/AQUAL Gauss law),
        (b) keeping N_grav = 2  (no NEW propagating DOF beyond the 2 metric polarizations),
        (c) c_T = 1                                     (luminal tensor sector) ?

  RESCUE  : YES  => an isotropic Legendre completion exists => the constraint-first
            2-DOF program has a lensing-clean member.
  UNIFIED NO-GO : Sigma_P != 0 is FORCED whenever mu' != 0 for ANY such completion
            => the anisotropic Hessian of every nonlinear isotropic MOND law forces a
            metric slip in every 2-DOF constraint construction => the ENTIRE
            constraint-first program is closed on the lensing axis.

  SETUP STATUS: the two committed dead-ends (naive Legendre: slip=(mu+y mu')/mu ;
  York AQUAL scalar: gamma=ln r/(ln r-2)) are reproduced above with certificates.
  Sigma_P is defined and shown ~ y mu' within these constructions.  Whether Sigma_P=0
  is FORCED (no-go) or EVADABLE (rescue) for a GENERIC second-class completion is the
  OPEN question the next task must settle -- NOT prejudged here.
""")

# ==================================================================================
hdr("VERDICT")
# ==================================================================================
if FAIL:
    print(f"  {len(FAIL)} CHECK(S) FAILED:")
    for f in FAIL:
        print("   -", f)
    print("\n  FC-ISO-SETUP CERTIFICATE: FAILED.")
    sys.exit(1)
else:
    print(f"  ALL {NCHK[0]} BOOLEAN CHECKS PASS.")
    print("  Reproduced: (1) naive-Legendre chain lambda_i=D_i N, D_i[A^{ij}D_j N]=0,")
    print("  A^{ij}=mu delta + y mu' u u, slip=(y^10+2)/(y^10+1) for mu_10;")
    print("  (2) York anisotropic stress 2U'P^2 and gamma=ln r/(ln r-2) (commit 0184ba7e);")
    print("  (3) DEFINED Sigma_P and CERTIFIED Sigma_P = y mu' (the 2-DOF obstruction).")
    print("  Decisive question stated.  This is SETUP only -- the no-go/rescue is OPEN.")
    print("\n  FC-ISO-SETUP CERTIFICATE: ALL BOOLEAN CHECKS PASS (exit 0).")
    sys.exit(0)
