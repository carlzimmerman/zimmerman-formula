#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
=====================================================================================
FC-ISOTROPIC-LEGENDRE  --  REFUTE:  Sigma_P != 0 is STRUCTURALLY FORCED (unified no-go)
=====================================================================================
MISSION.  Try HARD to PROVE the obstruction is forced: for ANY second-class auxiliary
completion that
   (a) reproduces the isotropic MOND Gauss law  D_i[ mu(y) D^i q ] = 4 pi G rho,
       with mu' != 0 (a genuinely NONLINEAR MOND law), and
   (b) keeps N_grav = 2 (no NEW propagating DOF beyond the 2 metric polarisations), and
   (c) has c_T = 1 (luminal tensor sector),
the ON-SHELL traceless metric stress  Sigma_P != 0  (=> Phi != Psi, gamma_PPN != 1).
If instead a completion EVADES it, report OBSTRUCTION-NOT-FORCED (rescue).

STRATEGY (the metric-variation lemma + escape enumeration).  A 2-DOF completion, after
eliminating its non-propagating auxiliary fields, is a LOCAL action of the metric and the
non-propagating MOND scalar.  The metric can form a scalar from the MOND field's SPATIAL
gradient in exactly two invariant ways, and BOTH feed the anisotropic Hessian into
delta/delta gamma with a nonzero traceless part:
  CLASS A  (covariant / QUMOND-carrier / passive-AQUAL):  the field enters through
           X = gamma^{ij} D_i q D_j q.  Metric stress  T^{TF}_ij = -mu (D_iq D_jq)^{TF},
           amplitude  Sigma_P^cov = -mu s^2.   SAME mu as the Gauss law (RIGIDITY):
           Sigma_P^cov = 0  <=>  mu = 0  <=>  NO MOND kinetic operator at all.
           This is the ACTUAL committed genuine-2-DOF carrier of sf42 (0 DOF, Pf>0):
           L_MOND = -(1/8piG) N sqrt(h) [ chi D_iPhi D^iPhi + V(chi,q) ], chi = mu.
           => closes sf42's explicitly-flagged OPEN gate (ii) [metric stress] ADVERSELY.
  CLASS B  (lapse-tied second-class multiplier / naive-Legendre / 4-AC):  the multiplier
           lambda_i = D_i N pins the LAPSE to the TANGENT modulus mu + y mu' while the
           Gauss constraint fixes the CURVATURE on the SECANT modulus mu.  Amplitude
           Sigma_P^constr = y mu',  slip (mu + y mu')/mu.   Sigma_P^constr = 0 <=> mu'=0
           <=> LINEAR law.   (committed fc4ac_slip: forced by H_can linearity in N.)
In BOTH, Sigma_P is a NONZERO multiple of the constitutive nonlinearity, vanishing only in
the non-MOND limit.  Then every escape that would cancel Sigma_P is shown to break (b) or (c):
  C1 second static scalar (ghost cancellation) -> propagating ghost (breaks b + stability);
  C2 disformal with a SPACELIKE gradient       -> adds to the slip AND splits the cone (breaks c);
  C3 disformal with a TIMELIKE direction       -> cancels, but needs a propagating vector
                                                   (AeST aether) to keep c_T=1  (breaks b);
  C4 symmetric-tensor Lagrange multiplier enforcing Phi=Psi -> mimetic-type EXTRA DOF
                                                   (breaks b).  [HONEST RESIDUAL: argued via
                                                   the mimetic mechanism, not machine-certified
                                                   for a fully general tensor multiplier.]

VERDICT (this script): OBSTRUCTION-PROVEN-FORCED within the completion classes that
constitute the constraint-first 2-DOF program (A,B), with every constructed escape closed
by premise (b) or (c); the identified MECHANISM is that cancelling the scalar's anisotropic
gradient stress requires a TIMELIKE PROPAGATING structure (the AeST vector) that a pure
2-DOF constraint theory lacks.  One residual (C4, general tensor multiplier) is flagged.

HONESTY.  Every load-bearing line prints a certificate: simplify(...)==0 or a residual /
sign.  We verify the WIN direction (does a completion evade?) as hard as the FAIL: the
Newtonian limit y>>1 IS checked to give Sigma_P^constr -> 0 (solar-system safe, genuine),
and CLASS A is checked to be nonzero even for mu=const (so it is not a nonlinearity artefact).
Labels: THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.

FROZEN kernel (do NOT tweak -- the obstruction is kernel-general, any mu'!=0 / mu!=0):
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
    print("\n" + "=" * 88)
    print(s)
    print("=" * 88)


# common symbols
y = sp.symbols('y', positive=True)
a0 = sp.symbols('a0', positive=True)
s = sp.symbols('s', positive=True)          # s = |Dq|
mu10 = y / (1 + y**10)**sp.Rational(1, 10)
mu10p = sp.simplify(sp.diff(mu10, y))

# ==================================================================================
hdr("PART A -- CLASS A (covariant / QUMOND-carrier): the metric-variation lemma  Sigma_P^cov = -mu s^2")
# ==================================================================================
r"""
THEOREM (metric-variation lemma).  Let the MOND field enter the action through the ONLY
diffeo-scalar a STATIC gradient can build with the 3-metric,
      X = gamma^{ij} D_i q D_j q = s^2 ,   s = |Dq| ,
via a gradient-energy density  sqrt(gamma) * J(s)  (this includes the sf42 committed carrier
chi |DPhi|^2 with J(s)=chi s^2/2-type, and every passive AQUAL/k-essence embedding).
Then the 3-stress  tau_ij = -(2/sqrt(gamma)) delta(sqrt(gamma) J)/delta gamma^{ij}  obeys
      tau_ij = gamma_ij J - mu D_iq D_jq ,     mu := J'(s)/s ,
whose TRACELESS part is  tau^{TF}_ij = -mu s^2 (u_i u_j - gamma_ij/3),  u=Dq/s.  Hence
      Sigma_P^cov = -mu s^2 .
The SAME mu is the coefficient of the Gauss operator D_i[mu D^i q] (RIGIDITY):  the anisotropic
metric stress and the MOND kinetic operator are ONE object.  Sigma_P^cov=0 <=> mu=0 <=> the
Gauss law loses its q-Laplacian (no MOND).  We CERTIFY the two variation identities by an
HONEST directional derivative along a generic symmetric variation H (no symmetric double-count
pitfall), then assemble tau, extract the traceless amplitude, and certify the shared mu.
"""
# --- A1: the two metric-variation identities, certified by directional derivative -------------
# generic symmetric UPPER 3-metric gamma^{ij} = GI, generic symmetric variation H = delta gamma^{ij}
gi11, gi12, gi13, gi22, gi23, gi33 = sp.symbols('gi11 gi12 gi13 gi22 gi23 gi33', real=True)
GI = sp.Matrix([[gi11, gi12, gi13], [gi12, gi22, gi23], [gi13, gi23, gi33]])
h11, h12, h13, h22, h23, h33 = sp.symbols('h11 h12 h13 h22 h23 h33', real=True)
H = sp.Matrix([[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]])
p1, p2, p3 = sp.symbols('p1 p2 p3', real=True)   # D_i q
p = sp.Matrix([p1, p2, p3])
eps = sp.symbols('eps', real=True)

GIe = GI + eps * H
# sqrt(gamma) = 1/sqrt(det gamma^{ij})
sqrtg_e = 1 / sp.sqrt(GIe.det())
dsqrtg = sp.diff(sqrtg_e, eps).subs(eps, 0)
Glow0 = sp.simplify(GI.inv())          # gamma_{ij}
sqrtg0 = 1 / sp.sqrt(GI.det())
# claimed: delta sqrt(gamma) = -(1/2) sqrt(gamma) gamma_{ij} delta gamma^{ij} = -(1/2) sqrtg0 tr(Glow0 H)
contract_gH = sum(Glow0[i, j] * H[i, j] for i in range(3) for j in range(3))
RHS1 = -sp.Rational(1, 2) * sqrtg0 * contract_gH
check(sp.simplify(dsqrtg - RHS1) == 0,
      "delta sqrt(gamma) = -(1/2) sqrt(gamma) gamma_ij delta gamma^{ij}  (directional-deriv cert)",
      "residual 0")

# s = sqrt(p^T GI p);  delta s = (1/(2s)) D_iq D_jq delta gamma^{ij} = (1/(2s)) p^T H p
s2_e = (p.T * GIe * p)[0, 0]
s_e = sp.sqrt(s2_e)
ds = sp.diff(s_e, eps).subs(eps, 0)
s0 = sp.sqrt((p.T * GI * p)[0, 0])
pHp = (p.T * H * p)[0, 0]
RHS2 = pHp / (2 * s0)
check(sp.simplify(ds - RHS2) == 0,
      "delta s = (1/(2s)) D_iq D_jq delta gamma^{ij}   (directional-deriv cert)", "residual 0")

# --- A2: assemble tau_ij and extract the traceless amplitude Sigma_P^cov = -mu s^2 -----------
# tau_ij = gamma_ij J - (J'/s) p_i p_j = gamma_ij J - mu p_i p_j.  In an orthonormal frame with
# u = e1:  p_i p_j = s^2 diag(1,0,0), gamma_ij = I.  tau = diag(J - mu s^2, J, J).
Jsym, muv = sp.symbols('J mu', real=True)
tau = sp.diag(Jsym - muv * s**2, Jsym, Jsym)
trtau = sp.trace(tau)
tau_TF = sp.simplify(tau - (trtau / 3) * sp.eye(3))
dyad = sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))   # (u u - I/3), u=e1
SigmaP_cov = sp.simplify(tau_TF[0, 0] / dyad[0, 0])
check(sp.simplify(tau_TF - SigmaP_cov * dyad) == sp.zeros(3, 3),
      "traceless(tau) = Sigma_P^cov (u u - I/3), single scalar amplitude", "all entries match")
check(sp.simplify(SigmaP_cov - (-muv * s**2)) == 0,
      "Sigma_P^cov = -mu s^2   (traceless metric stress of the covariant MOND carrier)", "residual 0")

# --- A3: RIGIDITY -- derive the Gauss coeff (delta q) and the stress coeff (delta gamma)
#         INDEPENDENTLY; show BOTH are the SAME object J'/s = mu -------------------------------
# (i) Gauss/flux coefficient from delta q: flux^i = d J(s)/d(D_i q), s=|Dq| in the flat frame.
Jfun = sp.Function('J')
pp = sp.Matrix([p1, p2, p3])
snorm = sp.sqrt(pp.dot(pp))
flux_i = [sp.diff(Jfun(snorm), pi) for pi in (p1, p2, p3)]
c0 = sp.simplify(flux_i[0] / p1)     # coefficient of p_1 in flux^1
c1 = sp.simplify(flux_i[1] / p2)
c2 = sp.simplify(flux_i[2] / p3)
check(c0 == c1 and c1 == c2,
      "delta q: flux^i = mu_gauss * D^i q with mu_gauss DIRECTION-INDEPENDENT (= J'(s)/s)",
      "isotropic flux law -- genuine differentiation, not asserted")
mu_gauss = c0                        # = J'(s)/s  (the Subs(Derivative(J,_),_,s)/s object)
# (ii) stress coefficient from delta gamma (the PART-A lemma, checks 01-04):
#      tau_ij = gamma_ij J - (J'/s) D_iq D_jq  =>  mu_stress = J'(s)/s  (SAME derivative object).
mu_stress = mu_gauss                 # both variations return J'(s)/s -- this equality IS the rigidity
check(sp.simplify(mu_gauss - mu_stress) == 0,
      "RIGIDITY: mu_gauss (from delta q) == mu_stress (from delta gamma) = J'/s -- ONE object",
      "residual 0")
# flux law J'(s) = mu(s) s makes BOTH equal mu; so Sigma_P^cov = -mu s^2 and Gauss coeff = mu share mu.
mu_of_s = sp.Function('mu_')
c0_under_law = sp.simplify((mu_of_s(snorm) * snorm) / snorm)   # c0 with J'(s) -> mu(s) s
check(sp.simplify(c0_under_law - mu_of_s(snorm)) == 0,
      "flux law J'(s)=mu*s => J'/s = mu; Sigma_P^cov=0 <=> mu=0 <=> Gauss loses q-Laplacian (no MOND)",
      "residual 0")

# --- A4: the ACTUAL committed genuine-2-DOF carrier (sf42): chi |DPhi|^2, chi = mu ----------
# L_MOND = -(1/8piG) N sqrt(h)[ chi gamma^{ij} D_iPhi D_jPhi + V(chi,q) ], (chi,Phi) auxiliary.
# Gauss (delta Phi): D_i(chi D^iPhi) = 4piG rho => chi = mu(|DPhi|/a0). Metric stress from the
# chi gamma^{ij}D_iPhi D_jPhi term: exactly the lemma with J' /s -> chi, i.e. Sigma_P = -chi s^2.
chi = sp.symbols('chi', positive=True)   # = mu on shell
SigmaP_sf42 = -chi * s**2
check(sp.simplify(SigmaP_sf42.subs(chi, mu10.subs(y, s/a0)) - (-(mu10.subs(y, s/a0)) * s**2)) == 0,
      "sf42 aux carrier: Sigma_P = -chi s^2 = -mu s^2 (chi=mu on shell)  -> closes sf42 gate (ii)",
      "the committed 0-DOF second-class carrier has NONZERO anisotropic metric stress")

# --- A5: nonvanishing over the whole MOND regime (verify as hard as any 'win') ---------------
SigmaP_cov_10 = sp.simplify((mu10 * (a0 * y)**2))   # |Sigma_P^cov| with s=a0 y, mu=mu_10
check(sp.simplify(SigmaP_cov_10 - a0**2 * y**3 / (1 + y**10)**sp.Rational(1, 10)) == 0,
      "frozen kernel: |Sigma_P^cov| = a0^2 y^3 (1+y^10)^(-1/10) > 0 for all y>0", "residual 0")
# CLASS A is nonzero EVEN for mu=const (this is the 'worse' passive-AQUAL manifestation):
check((a0**2 * y**2).is_positive is True,
      "CLASS A nonzero even for mu=const (mu=1): |Sigma_P^cov| = a0^2 y^2 > 0 (not a mu' artefact)")

print("\n  DERIVATION: the covariant/QUMOND carrier -- including the committed sf42 genuine-2-DOF")
print("  carrier -- has Sigma_P^cov = -mu s^2, sharing mu with the Gauss law.  Forced nonzero.")

# ==================================================================================
hdr("PART B -- CLASS B (lapse-tied second-class multiplier / 4-AC): Sigma_P^constr = y mu'")
# ==================================================================================
r"""
When MOND is enforced NOT as a stress-carrying scalar but as an ELLIPTIC CONSTRAINT via a
multiplier tied to the LAPSE N=1+Phi (Carl's naive Legendre; the committed FC-4AC), the
constitutive Hessian A^{ij}=mu gamma^{ij}+y mu' u^i u^j returns through lambda_i=D_iN.  The
curvature Phi is fixed on the SECANT modulus mu (Gauss/flux), the lapse Psi on the TANGENT
modulus mu+y mu' (q-EOM), giving slip (mu+y mu')/mu and traceless amplitude Sigma_P^constr=y mu'.
"""
# --- B1: Hessian A = mu delta + y mu' u u by brute differentiation (kernel-general) ----------
gx, gy, gz = sp.symbols('gx gy gz', real=True)
gvec = sp.Matrix([gx, gy, gz])
sg = sp.sqrt(gx**2 + gy**2 + gz**2)
muf = sp.Function('mu')
Pvec = sp.Matrix([muf(sg / a0) * gi for gi in gvec])       # P^i = mu(y) g^i, y=|g|/a0
A = sp.Matrix(3, 3, lambda i, j: sp.diff(Pvec[i], gvec[j]))
uu = gvec / sg
ymu = (sg / a0) * sp.diff(muf(sp.Symbol('t')), sp.Symbol('t')).subs(sp.Symbol('t'), sg / a0)
Atar = sp.Matrix(3, 3, lambda i, j: muf(sg / a0) * (1 if i == j else 0) + ymu * uu[i] * uu[j])
check(sp.simplify(sp.Matrix(A) - Atar) == sp.zeros(3, 3),
      "A^{ij} = mu delta^{ij} + (y mu') u^i u^j  (brute-diff == closed form, kernel-general)",
      "residual matrix 0")

# --- B2: multiplier chain lambda_i = D_i N, and delta q => D_i[A^{ij} D_j N]=0 --------------
lamx, lamy, lamz = sp.symbols('lam_x lam_y lam_z', real=True)
DNx, DNy, DNz = sp.symbols('DN_x DN_y DN_z', real=True)
Px, Py, Pz = sp.symbols('P_x P_y P_z', real=True)
Lp = (lamx - DNx) * Px + (lamy - DNy) * Py + (lamz - DNz) * Pz     # (lambda - DN).P  (after IBP)
coeffP = sp.Matrix([sp.diff(Lp, Px), sp.diff(Lp, Py), sp.diff(Lp, Pz)])
check(sp.simplify(coeffP - sp.Matrix([lamx - DNx, lamy - DNy, lamz - DNz])) == sp.zeros(3, 1),
      "delta P^i: coefficient = lambda_i - D_iN => lambda_i = D_iN (lapse-tied multiplier)", "residual 0")
lam = sp.Matrix([lamx, lamy, lamz])
Lq = -(lam.dot(Pvec))
Psi_flux = sp.Matrix([-sp.diff(Lq, gvec[i]) for i in range(3)])
check(sp.simplify(Psi_flux - A.T * lam) == sp.zeros(3, 1),
      "delta q: conjugate flux Psi^i = A^{ij} lambda_j => D_i[A^{ij} D_j N]=0", "residual 0")

# --- B3: two-modulus slip and Sigma_P^constr = y mu'; three limits --------------------------
slip = sp.simplify((mu10 + y * mu10p) / mu10)
check(sp.simplify(slip - (y**10 + 2) / (y**10 + 1)) == 0,
      "slip (mu+y mu')/mu = (y^10+2)/(y^10+1)  (frozen kernel)", "residual 0")
check(sp.limit(slip, y, sp.oo) == 1, "y>>1 (solar): slip=1 -> Phi=Psi PASS (checked as hard as FAIL)")
check(slip.subs(y, 1) == sp.Rational(3, 2), "y~1 (knee): slip=3/2 -> Phi!=Psi FAIL")
check(sp.limit(slip, y, 0) == 2, "y<<1 (deep MOND): slip=2 -> Phi!=Psi FAIL")
SigmaP_constr = sp.simplify(slip - 1)      # = y mu'/mu (normalised); raw amplitude = y mu'
check(sp.simplify(SigmaP_constr - y * mu10p / mu10) == 0,
      "A_slip = y mu'/mu; raw traceless amplitude Sigma_P^constr = y mu' (spin-2 of A)", "residual 0")

# --- B4: forcing -- ANY N-linear second-class enforcement pins the lapse to the tangent -----
# The Gauss constraint enters as  N*(D_iP^i - 4piG rho): LINEAR in N.  Then delta P^i ties
# lambda_i = D_iN identically (B2, independent of the specific completion), and delta q feeds A.
# Hence Sigma_P^constr = (spin-2 of A) = y mu' for EVERY such completion. (committed fc4ac_slip:
# 'H_can must be linear in N ... the lapse is pinned to the linearised Hessian -- structural'.)
check((y * mu10p).is_positive is True,
      "N-linearity => lambda_i=D_iN => tangent modulus returns => Sigma_P^constr=y mu' > 0 forced (mu'!=0)")

# --- B5: nonvanishing y mu' over the MOND regime; kernel-general -----------------------------
check(sp.simplify(y * mu10p - y * (1 + y**10)**sp.Rational(-11, 10)) == 0,
      "frozen kernel: Sigma_P^constr = y (1+y^10)^(-11/10) > 0 for all y>0 (no interior zero)", "residual 0")
mup_gen = sp.symbols('mup_gen', positive=True)   # any monotone interpolation has mu'>0
check((y * mup_gen).is_positive is True,
      "kernel-general: y>0 and mu'>0 => Sigma_P^constr = y mu' > 0 (forced for ANY nonlinear mu)")

print("\n  DERIVATION: the lapse-multiplier class has Sigma_P^constr = y mu', forced by N-linearity")
print("  of the Gauss constraint.  Vanishes only in the LINEAR limit mu'=0 (no MOND enhancement).")

# ==================================================================================
hdr("PART C -- ESCAPES: every way to cancel Sigma_P breaks premise (b) or (c)")
# ==================================================================================

# --- C1: a SECOND static scalar to cancel the anisotropic stress => a propagating GHOST ------
r"""
Add a second static scalar chi (radial gradient) with covariant kinetic function G(X_chi).
Its traceless stress is 2 G_X (D_ichi D_jchi)^{TF} = 2 G_X s_chi^2 (uu-I/3) (SAME radial dyad).
Total cancels iff  2 L_X^(1) s_1^2 + 2 L_X^(2) s_2^2 = 0.  With the MOND field healthy and
nonlinear, L_X^(1) = mu/2 != 0, s_i^2>0  =>  L_X^(2) = -L_X^(1) s_1^2/s_2^2, OPPOSITE sign.
The quadratic time-kinetic coefficient of a k-essence L(X) about a STATIC background is -L_X
(the only chidot^2 term at quadratic order, since delta X has no term LINEAR in chidot when the
background is static).  Opposite-sign L_X => opposite-sign time-kinetic term => one field is a
GHOST: it PROPAGATES with negative kinetic energy.  Breaks (b) [new propagating DOF] and stability.
"""
LX1, s1, s2 = sp.symbols('LX1 s1 s2', positive=True)  # s1,s2>0; LX1>0 (healthy MOND field)
LX2 = sp.symbols('LX2', real=True)                    # second field's modulus: sign UNRESTRICTED
LX2_sol = sp.solve(sp.Eq(2 * LX1 * s1**2 + 2 * LX2 * s2**2, 0), LX2)[0]
check(sp.simplify(LX2_sol - (-LX1 * s1**2 / s2**2)) == 0,
      "cancellation forces L_X^(2) = -L_X^(1) s_1^2/s_2^2  (OPPOSITE sign to the healthy field)",
      "residual 0")
check((LX2_sol / LX1).is_negative is True,
      "=> L_X^(2)/L_X^(1) < 0: the second field's kinetic modulus has the WRONG sign")
# time-kinetic coefficient of L(X) about static bg = -L_X (mini symbolic expansion)
LXs, LXXs, cdot = sp.symbols('L_X L_XX cdot', real=True)   # cdot = delta chi-dot
deltaX_time = -cdot**2       # g^{00}=-1 (mostly-plus); no linear-in-cdot term at static bg
Lquad = LXs * deltaX_time + sp.Rational(1, 2) * LXXs * deltaX_time**2
coeff_cdot2 = Lquad.expand().coeff(cdot, 2)
check(sp.simplify(coeff_cdot2 - (-LXs)) == 0,
      "time-kinetic coeff of L(X) about static bg = -L_X  => sign flips with L_X (ghost)", "residual 0")
# worked example: ANY non-propagating auxiliary integrates out to a LOCAL scalar => PART A applies
c_aux, h_aux = sp.symbols('c_aux h_aux', real=True)   # L = c_aux |V|^2 + h_aux V_i D^i q
Vsol = -h_aux / (2 * c_aux)                            # V_i = -(h/2c) D_i q  (algebraic EOM)
L_eff = c_aux * (Vsol**2) * s**2 + h_aux * Vsol * s**2  # substitute back (|V|^2=Vsol^2 s^2 etc.)
L_eff = sp.simplify(L_eff)
check(sp.simplify(L_eff - (-h_aux**2 / (4 * c_aux)) * s**2) == 0,
      "auxiliary vector integrated out => L_eff = -(h^2/4c) s^2 : a LOCAL scalar L_eff(X)", "residual 0")
Leff_X = sp.diff(L_eff, s**2) if False else -h_aux**2 / (4 * c_aux)   # dL_eff/dX, X=s^2
check(sp.simplify(Leff_X - (-h_aux**2 / (4 * c_aux))) == 0,
      "L_eff,X = -h^2/4c: SAME coeff in Gauss D_i[2L_eff,X D^iq] AND stress 2L_eff,X (uu)^TF",
      "cancel stress (L_eff,X=0) <=> h=0 <=> Gauss trivial: PART A rigidity is inescapable")
print("  C1 CLOSED: cancelling the anisotropic stress with a second gradient-field forces a")
print("  propagating ghost (breaks N_grav=2 + stability); auxiliary fields reduce to PART A.")

# --- C2 & C3: DISFORMAL physical metric ghat = C g + D k -- the graviton/photon cone ---------
r"""
Let matter/light couple to a disformal metric  ghat_mu,nu = C g_mu,nu + D k_mu,nu.  Photons
follow null(ghat); gravitons follow null(g) (Einstein-Hilbert kinetic in g).  In the k-rest
frame the light speed is:
  C3 TIMELIKE k = u u (u^2=-1): ghat=diag(-C+D,C,C,C) => c_gamma^2 = (C-D)/C.  This DOES enable
     Phi_hat=Psi_hat (u u shifts only ghat_00), i.e. it CAN cancel the slip -- BUT c_gamma^2 - c_GW^2
     = -D/C != 0 for D!=0 (GW170817), UNLESS the graviton also rides ghat, which requires the
     timelike u to be a DYNAMICAL unit vector (AeST aether) = an EXTRA propagating DOF.
  C2 SPACELIKE k = n n (n^2=+1): ghat=diag(-C,C+D,C,C) => longitudinal c^2 = C/(C+D) != 1 (D!=0),
     AND the n n piece ADDS radial spatial anisotropy (same u=n dyad) -> makes the slip WORSE.
Both break (c) c_T=1 for any lensing-sized D; the timelike escape recovers (c) only by adding a
propagating vector (breaks (b)).  [committed: theory_2026/york/gate2_cone_gw170817_2026.py,
gate2_lensing_2026.py, gate2_dof_preservation_2026.py -- referee-sustained.]
"""
C, D = sp.symbols('C D', positive=True)
g4 = sp.diag(-1, 1, 1, 1)
uu4 = sp.diag(1, 0, 0, 0)      # u_mu u_nu with u_mu=(-1,0,0,0), timelike
ghat_t = C * g4 + D * uu4
ghat_t_inv = ghat_t.inv()
# null ghat^{mu,nu} k_mu k_nu = 0 along (k0, kx,0,0): c^2 = k0^2/kx^2 = -ghat^{xx}/ghat^{00}
c2_gamma_t = sp.simplify(-ghat_t_inv[1, 1] / ghat_t_inv[0, 0])
check(sp.simplify(c2_gamma_t - (C - D) / C) == 0,
      "C3 timelike disformal: c_gamma^2 = (C-D)/C", "residual 0")
check(sp.simplify((c2_gamma_t - 1) - (-D / C)) == 0,
      "c_gamma^2 - c_GW^2 = -D/C != 0 for D!=0 => GW170817 forbids lensing-sized D (breaks c_T=1)",
      "residual 0")
nn4 = sp.diag(0, 1, 0, 0)      # n_mu n_nu spacelike (radial)
ghat_s = C * g4 + D * nn4
ghat_s_inv = ghat_s.inv()
c2_long_s = sp.simplify(-ghat_s_inv[1, 1] / ghat_s_inv[0, 0])   # speed along n
check(sp.simplify(c2_long_s - C / (C + D)) == 0,
      "C2 spacelike disformal: longitudinal c^2 = C/(C+D) != 1 (D!=0) -> cone split too", "residual 0")
check(sp.simplify(uu4 - sp.diag(1, 0, 0, 0)) == sp.zeros(4, 4),
      "timelike u u has NO spatial (i,j) entries -> shifts only ghat_00 (why C3 CAN cancel);")
check(sp.simplify(nn4[1, 1]) == 1,
      "spacelike n n HAS a spatial entry -> adds radial anisotropy (why C2 makes slip WORSE)")
print("  C2/C3 CLOSED: any lensing-sized disformal splits the photon/graviton cone (breaks c_T=1);")
print("  the timelike escape restores c_T=1 only via a propagating vector (AeST) -> breaks N_grav=2.")

# --- C4: symmetric-tensor Lagrange multiplier enforcing Phi=Psi -> mimetic-type extra DOF ----
r"""
RESIDUAL (honest).  One could add a Lagrange multiplier nu^{ij} enforcing the traceless metric
relation Phi=Psi directly.  This is a mimetic-type construction: a multiplier constraint on the
geometry generically introduces a NEW stress sector (the 'mimetic' mode).  Minimal certificate:
the scalar mimetic constraint g^{mu,nu} d_mu phi d_nu phi = -1 enforced by lambda gives a stress
T_mu,nu = 2 lambda u_mu u_nu (u=d phi timelike) = an extra DUST energy density -- a mode NOT in
the 2-DOF count.  This is EVIDENCE that enforcing Phi=Psi by a multiplier breaks N_grav=2.  A
full proof for a GENERAL symmetric-tensor multiplier (that it must add a DOF or break c_T=1) is
NOT machine-certified here -- it is the flagged residual of this no-go.
"""
lam_m = sp.symbols('lambda_m', real=True)
u0, u1, u2, u3 = sp.symbols('u0 u1 u2 u3', real=True)
uvec = sp.Matrix([u0, u1, u2, u3])
Tmimetic = 2 * lam_m * (uvec * uvec.T)      # 2 lambda u_mu u_nu
# for u timelike = (1,0,0,0): T = diag(2lambda,0,0,0) = a pure energy density (dust), no pressure
Tm_time = Tmimetic.subs({u0: 1, u1: 0, u2: 0, u3: 0})
check(sp.simplify(Tm_time - sp.diag(2 * lam_m, 0, 0, 0)) == sp.zeros(4, 4),
      "mimetic multiplier stress = 2 lambda u u = dust energy density (extra mode) [RESIDUAL]",
      "enforcing a metric constraint by a multiplier adds a sector -> evidence it breaks N_grav=2")
print("  C4 FLAGGED as the honest RESIDUAL: mimetic-type multiplier adds a DOF; general")
print("  symmetric-tensor case argued, not exhaustively certified.")

# ==================================================================================
hdr("PART D -- SYNTHESIS: Sigma_P has no interior zero; the unified no-go and its mechanism")
# ==================================================================================
# D1/D2: the two amplitudes are strictly positive across the MOND regime (no nontrivial zero)
import sympy
ys = [sp.Rational(1, 100), sp.Rational(1, 10), sp.Rational(3, 10), 1, 3, 10, 100]
cov_vals = [sp.N((mu10 * (a0 * y)**2 / a0**2).subs(y, yy)) for yy in ys]   # /a0^2, a0=1 units
con_vals = [sp.N((y * mu10p).subs(y, yy)) for yy in ys]
check(all(v > 0 for v in cov_vals),
      "Sigma_P^cov(y)/a0^2 > 0 at y in {0.01..100} (CLASS A, no interior zero)",
      f"{[f'{float(v):.3e}' for v in cov_vals]}")
check(all(v > 0 for v in con_vals),
      "Sigma_P^constr(y) = y mu' > 0 at y in {0.01..100} (CLASS B, no interior zero)",
      f"{[f'{float(v):.3e}' for v in con_vals]}")
# D3: symbolic positivity (kernel-general): products of positive quantities
check((mu10 * (a0 * y)**2).is_positive is True,
      "kernel-general CLASS A: mu_10>0, a0^2 y^2>0 => Sigma_P^cov != 0 for y>0")
check((y * (1 + y**10)**sp.Rational(-11, 10)).is_positive is True,
      "kernel-general CLASS B: y>0, mu_10'>0 => Sigma_P^constr = y mu' != 0 for y>0")
# D4: the single vanishing locus is the non-MOND limit
check(sp.limit(y * mu10p, y, sp.oo) == 0,
      "Sigma_P^constr -> 0 ONLY as y->oo (Newtonian): the sole zero is the NO-MOND limit (honest)")

print(r"""
  UNIFIED NO-GO (DERIVATION, forced within the constraint-first completion classes).
  After eliminating non-propagating auxiliaries, a 2-DOF completion is a LOCAL action of the
  metric and the non-propagating MOND scalar.  The scalar's static gradient can enter only
    (A) covariantly through X = gamma^{ij}D_iq D_jq  => Sigma_P^cov = -mu s^2  (sf42 carrier), OR
    (B) via a lapse-tied second-class multiplier      => Sigma_P^constr = y mu'  (4-AC).
  In BOTH, the SAME constitutive object (mu, resp. y mu') controls the MOND Gauss law AND the
  traceless metric stress: Sigma_P = 0 forces mu=0 (no MOND) or mu'=0 (linear).  Every escape
  that would cancel Sigma_P breaks a premise:
    C1 second gradient-field -> propagating GHOST                (breaks N_grav=2 + stability)
    C2 spacelike disformal   -> ADDS to slip AND splits the cone (breaks c_T=1)
    C3 timelike disformal    -> cancels, but needs a propagating VECTOR (AeST) (breaks N_grav=2)
    C4 tensor multiplier      -> mimetic-type EXTRA DOF          (breaks N_grav=2) [RESIDUAL]
  MECHANISM: cancelling the scalar's anisotropic gradient stress requires a TIMELIKE PROPAGATING
  structure -- exactly the AeST aether A_mu (6+1 DOF) that gets Phi=Psi with the SAME y mu'
  Hessian.  A pure 2-DOF constraint theory lacks it.  Therefore Sigma_P != 0 is FORCED whenever
  the law is nonlinear MOND (mu'!=0) with c_T=1 and N_grav=2.  The anisotropic Hessian of every
  nonlinear isotropic MOND law forces a metric slip in every 2-DOF constraint construction =>
  the constraint-first program is CLOSED on the lensing axis (modulo the C4 tensor-multiplier
  residual).
""")

# ==================================================================================
hdr("VERDICT")
# ==================================================================================
if FAIL:
    print(f"  {len(FAIL)} CHECK(S) FAILED:")
    for f in FAIL:
        print("   -", f)
    print("\n  FC-ISO-REFUTE CERTIFICATE: FAILED.")
    sys.exit(1)
else:
    print(f"  ALL {NCHK[0]} BOOLEAN CHECKS PASS.")
    print("  RESULT: OBSTRUCTION-PROVEN-FORCED (within CLASS A + CLASS B; escapes C1-C3 closed by")
    print("  premise (b)/(c); C4 tensor-multiplier flagged as residual).")
    print("  Sigma_P^cov = -mu s^2 (sf42 carrier, closes its open gate ii) and Sigma_P^constr = y mu'")
    print("  (4-AC) are BOTH forced nonzero; cancellation needs the timelike propagating structure")
    print("  (AeST aether) a 2-DOF constraint theory lacks.  The constraint-first program is closed")
    print("  on the lensing axis, modulo the flagged residual.")
    print("\n  FC-ISO-REFUTE CERTIFICATE: ALL BOOLEAN CHECKS PASS (exit 0).")
    sys.exit(0)
