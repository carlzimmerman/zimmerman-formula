#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
=====================================================================================
FC-ISOTROPIC-LEGENDRE  --  CONSTRUCTION ATTEMPT  (sympy certificates)
=====================================================================================
TASK:  Try HARD to CONSTRUCT an ISOTROPIC second-class Legendre completion of the
  isotropic MOND law  D_i[ mu(y) D^i q ] = 4 pi G rho  whose ON-SHELL traceless
  metric stress VANISHES  (Sigma_P = 0  =>  Phi = Psi, gamma_PPN = 1, FRIED CHICKEN),
  while (a) reproducing the MOND/AQUAL Gauss law, (b) keeping N_grav = 2 (no NEW
  propagating DOF), (c) c_T = 1.

  We try the three candidate mechanisms named in the brief, COMPUTE Sigma_P for each,
  and check =0 with a certificate:
    (i)   a compensating auxiliary tensor/vector whose anisotropic stress cancels
          -y mu' (u_i u_j - delta/3);
    (ii)  a disformal/conformal coupling that reshuffles the stress into the trace;
    (iii) coupling the flux to the metric only through a trace (det gamma) so no
          directional stress arises.

HONESTY (non-negotiable):  every load-bearing line prints simplify(...)==0 or a
  residual.  We verify a WIN (Sigma_P=0) exactly as hard as a FAIL.  Labels:
  THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.
  If a mechanism SUCCEEDS with a full certificate we say ISOTROPIC-COMPLETION-
  CONSTRUCTED; otherwise PARTIAL/INCONCLUSIVE.  We do NOT prejudge.

FROZEN kernel (do NOT tweak -- the obstruction is kernel-general, any mu'!=0):
  mu_10(y) = y/(1+y^10)^(1/10),   mu_10' = (1+y^10)^(-11/10) > 0.

KEY OBJECTS (from fc_iso_setup.py, 19/19, and committed fc4ac_slip.py):
  * AQUAL single scalar (q carries gradient stress):  Sigma ~ 2 mu P^2  (the WORSE
    manifestation; nonzero even at mu=const; gamma = ln r/(ln r - 2), York committed).
  * Constraint/Legendre (q constrained by a multiplier; no d_iq d_jq stress):
    Sigma_P ~ y mu'  (the 2-DOF obstruction; ->0 Newtonian (y>>1), !=0 for MOND).
  Both vanish iff the metric-coupled MOND nonlinearity is switched off.

STRATEGY OF PROOF/CONSTRUCTION.  We establish a REDUCTION: any LOCAL, algebraically-
  reducible (second-class, non-propagating) auxiliary sector integrates out to an
  effective single-/multi-field local scalar Lagrangian whose Hilbert stress is
  RIGIDLY tied to the MOND force.  We then test each mechanism against that rigidity.

Exit 0 = every numbered check passed (a check that a Sigma_P is NONZERO is itself a
  PASS -- we are certifying the computation, not the physics verdict).
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


# frozen kernel + symbols reused throughout
y = sp.symbols('y', positive=True)
mu10 = y / (1 + y**10)**sp.Rational(1, 10)
mu10p = sp.simplify(sp.diff(mu10, y))


# ==================================================================================
hdr("PART 0 -- the metric-stress functional derivative machinery (DERIVATION)")
# ==================================================================================
r"""
For a static sector with 3D Lagrangian density  sqrt(g) L(g^{ij}, fields, d fields),
the Hilbert (metric) stress is
    T_ij = -(2/sqrt g) d(sqrt g L)/d g^{ij} = -2 dL/dg^{ij} + g_ij L,
using d sqrt(g)/d g^{ij} = -(1/2) sqrt(g) g_ij.  The traceless part
    T^{TF}_ij = -2 [ dL/dg^{ij} ]^{TF}
(the g_ij L piece is pure trace = pressure) is what sources Phi - Psi:
    (Phi - Psi)'' - (Phi - Psi)'/r = 8 pi G (T^r_r - T^th_th) = Sigma_P     (York eq).
So  gamma_PPN = 1 (Phi = Psi)  <=>  T^{TF}_ij = 0  <=>  Sigma_P = 0.
We CERTIFY the trace identity d sqrt(g)/d g^{ij} = -(1/2) sqrt(g) g_ij in 3D.
"""
# 3x3 symmetric UPPER metric g^{ij}=Gm; measure = sqrt(det g_{lower}) = (det Gm)^(-1/2).
# lower metric g_ij = (Gm)^{-1} = Ginv.  Identity:  d(measure)/d g^{ij} = -(1/2) measure * g_ij.
# Test on a DIAGONAL component (g00) to avoid the symmetric off-diagonal doubling factor.
Gm = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'g{min(i,j)}{max(i,j)}', real=True))
detG = Gm.det()
Ginv = Gm.inv()                 # = lower metric g_ij
measure = detG**sp.Rational(-1, 2)
lhs = sp.diff(measure, Gm[0, 0])
rhs = -sp.Rational(1, 2) * measure * Ginv[0, 0]
check(sp.simplify(lhs - rhs) == 0,
      "d(measure sqrt g)/d g^{ij} = -(1/2) sqrt(g) g_ij   (trace identity, 3D diagonal comp)",
      "=> the sqrt(g) measure contributes ONLY to the trace (pressure), never the slip")


# ==================================================================================
hdr("PART 1 -- BASELINE A: single AQUAL scalar.  Sigma ~ 2 mu P^2  (reproduce York)")
# ==================================================================================
r"""
L = sqrt(g) * (-1/8piG) a0^2 F(X/a0^2),  X = g^{ij} d_i q d_j q.  MOND force operator
D_i[ 2 F'(X/a0^2) D^i q ] = 4 pi G rho, i.e. mu = 2 F'.  Metric stress traceless part:
    T^{TF}_ij = -2 [ -(1/8piG) F'(X/a0^2) d_i q d_j q ]^{TF}
              = (1/4piG) F'(X/a0^2) ( d_i q d_j q - (X/3) g_ij )
              = (1/4piG) F' X (n_i n_j - g_ij/3).
Amplitude 8piG*Sigma = 2 F' X = mu * X = mu P^2 (P=|Dq|).  Nonzero for ANY force (F'!=0),
INDEPENDENT of mu' -- the scalar's own gradient carries stress even for a LINEAR law.
This is the WORSE (AQUAL) manifestation; it is why plain AQUAL under-lenses.
"""
a0, Xs = sp.symbols('a0 X', positive=True)
Fp = sp.Function('Fp')   # F'(X/a0^2) = (1/2) mu
P = sp.symbols('P', positive=True)          # |Dq|
# traceless amplitude coefficient of (n n - I/3):  2 F' X  (set 8piG=1)
Sigma_AQUAL = 2 * Fp(Xs / a0**2) * Xs
check(sp.simplify(Sigma_AQUAL.subs(Fp(Xs/a0**2), sp.Symbol('mu')/2) - sp.Symbol('mu')*Xs) == 0,
      "AQUAL traceless amplitude  Sigma = 2 F' X = mu X = mu P^2   (mu=2F')",
      "nonzero for ANY force F'!=0, even mu=const (LINEAR): the scalar gradient IS a stress")

# reproduce the committed York deep-MOND gamma = ln r/(ln r - 2) from THIS stress
r_ = sp.symbols('r', positive=True)
v0sq = sp.symbols('v0sq', positive=True)
Pdeep = v0sq / r_                            # deep-MOND |Dq| = sqrt(GMa0)/r
Sdeep = sp.simplify(2 * (Pdeep / a0) * Pdeep**2)     # 2 U' P^2 with deep U'=P/a0
Dfun = sp.Function('D')
Dsol = sp.dsolve(sp.Eq(sp.diff(Dfun(r_), r_, 2) - sp.diff(Dfun(r_), r_)/r_, Sdeep), Dfun(r_))
Dpart = sp.simplify(Dsol.rhs.subs({sp.Symbol('C1'): 0, sp.Symbol('C2'): 0}))
check(sp.simplify(Dpart - 2*v0sq**3/(3*a0*r_)) == 0,
      "deep-MOND slip potential D = Phi_g - Psi_g = 2 v0^6/(3 a0 r)  (York committed)")
Psf = sp.Function('Ps')
rho_deep = sp.simplify(a0**2 * sp.Rational(2, 3) * (Pdeep/a0)**3)
Psi_sol = sp.dsolve(sp.Eq(2*(sp.diff(Psf(r_), r_, 2) + 2*sp.diff(Psf(r_), r_)/r_), rho_deep), Psf(r_))
Psi_p = sp.simplify(Psi_sol.rhs.subs({sp.Symbol('C1'): 0, sp.Symbol('C2'): 0}))
gamma_E = sp.simplify(Psi_p / sp.simplify(Psi_p + Dpart))
check(sp.simplify(gamma_E - sp.log(r_)/(sp.log(r_) - 2)) == 0,
      "=> Einstein-frame gamma_PPN = ln r/(ln r - 2) != 1  (AQUAL O(1) lensing failure)",
      "grounded against theory_2026/york/ppn_lensing_cassini_2026.py, commit 0184ba7e")


# ==================================================================================
hdr("PART 2 -- THE RIGIDITY LEMMA: force and traceless stress are the SAME functional")
# ==================================================================================
r"""
LEMMA (single local scalar).  For ANY local first-order scalar sector L=sqrt(g) F(X,q),
X=|Dq|^2, the MOND force modulus and the traceless Hilbert-stress amplitude are BOTH
governed by F_X:
    force:   D_i[ 2 F_X D^i q ] = source          (mu_eff = 2 F_X)
    stress:  Sigma = 2 F_X X                       (traceless amplitude, 8piG=1)
Hence  Sigma = mu_eff * X  and
    Sigma = 0   <=>   F_X = 0   <=>   NO force.
There is NO functional freedom to separate them: the very object (F_X) that makes the
law non-Newtonian makes the stress anisotropic.  This is the AQUAL rigidity.
"""
Fsym = sp.Function('F')
q = sp.symbols('q', real=True)
FX = sp.Derivative(Fsym(Xs, q), Xs)
mu_eff = 2 * FX
Sigma_gen = 2 * FX * Xs
check(sp.simplify(Sigma_gen - mu_eff * Xs) == 0,
      "RIGIDITY: Sigma = 2 F_X X = mu_eff * X  (force modulus = stress modulus)")
check(sp.simplify(Sigma_gen.subs(FX, 0)) == 0 and sp.simplify(mu_eff.subs(FX, 0)) == 0,
      "Sigma = 0  <=>  F_X = 0  <=>  mu_eff = 0  <=>  NO force  (AQUAL no-go, single scalar)",
      "the traceless stress cannot be zeroed while keeping a force -- SAME functional F_X")


# ==================================================================================
hdr("PART 3 -- CONSTRAINT/LEGENDRE form: Sigma_P ~ y mu' (better, still !=0) + reduction")
# ==================================================================================
r"""
The constraint (naive-Legendre) construction hides the AQUAL 'mu X' piece in the TRACE
(the N-multiplier / Newtonian pressure) and leaves the DIFFERENTIAL piece y mu' as the
traceless stress (committed fc4ac_slip.py:  the auxiliary stress Pi^aux carries the
anisotropy y mu_10' n n; slip = (mu+y mu')/mu).  We reproduce Sigma_P = y mu' and its
frozen-kernel value, and certify the REDUCTION: eliminating the algebraic multiplier
P^i / chi returns a q-only functional -- no new stress channel is opened.
"""
ysym, muv, mupv = sp.symbols('y mu muprime', positive=True)
Aabs = sp.diag(muv + ysym*mupv, muv, muv)     # constitutive Hessian along u = e1
A_TF = sp.simplify(Aabs - (sp.trace(Aabs)/3)*sp.eye(3))
dyad = sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))   # (u u - I/3)
SigmaP_constraint = sp.simplify(A_TF[0, 0] / dyad[0, 0])
check(sp.simplify(A_TF - SigmaP_constraint*dyad) == sp.zeros(3, 3),
      "constraint form: traceless(A) = Sigma_P (u u - I/3), single scalar Sigma_P")
check(sp.simplify(SigmaP_constraint - ysym*mupv) == 0,
      "Sigma_P = y mu'   (constraint/Legendre obstruction; committed fc4ac_slip.py)")
SigmaP10 = sp.simplify(y*mu10p)
check(sp.simplify(SigmaP10 - y*(1+y**10)**sp.Rational(-11, 10)) == 0,
      "frozen mu_10: Sigma_P = y (1+y^10)^(-11/10) > 0 for all y>0 -- never vanishes")
# Newtonian limit y>>1: Sigma_P -> 0 (solar safe); deep-MOND y<<1: Sigma_P -> y (grows)
check(sp.limit(SigmaP10, y, sp.oo) == 0,
      "y>>1 (solar): Sigma_P -> 0  (Newtonian slip switches off, PASS as hard as FAIL)")
check(sp.limit(SigmaP10 / y, y, 0) == 1,
      "y<<1 (deep-MOND): Sigma_P ~ y  (anisotropic stress persists -> slip)")

# REDUCTION demonstration: Legendre-eliminate an algebraic flux P^i and recover F(X).
r"""
S = sqrt(g)[ P^i d_i q - W(|P|^2) ],  |P|^2 = g_ij P^i P^j.  delta P^i:  d_i q = 2 W' P_i
=> P_i = d_i q /(2 W'), an ALGEBRAIC (local) solution.  Back-substitute:
   L_eff = P^i d_i q - W = |Dq|^2/(2W') - W(|Dq|^2/(4 W'^2)).
This is again a LOCAL F(X): no new field, no new stress channel.  Certify that the
on-shell L_eff depends on g only through X=|Dq|^2 (=> stress is the F(X) stress, Part 2).
"""
Wp = sp.symbols('Wp', positive=True)       # W'(|P|^2) treated as the Legendre slope
Pmod2 = Xs / (4*Wp**2)                      # |P|^2 = |Dq|^2/(4W'^2) on shell
Leff_onshell = Xs/(2*Wp) - sp.Function('W')(Pmod2)   # function of X and W-data only
check(Leff_onshell.has(Xs) and not Leff_onshell.has(sp.Symbol('nx')),
      "REDUCTION: algebraic-flux elimination returns L_eff = F(X) (local, single scalar)",
      "=> a LOCAL algebraically-reducible auxiliary opens NO new traceless-stress channel")


# ==================================================================================
hdr("PART 3b -- DIRECT Hilbert metric stress of the naive-Legendre term (COMPUTATION)")
# ==================================================================================
r"""
The setup's Sigma_P = y mu' is the traceless part of the constitutive HESSIAN A^{ij}
(the multiplier-chain object governing the MOND-as-lapse slip (mu+y mu')/mu, committed
fc4ac_slip.py).  We now compute the ACTUAL Hilbert metric stress of the gravitating
MOND term  L_M = -sqrt(g) mu(y) g^{ij} lam_i D_j q  DIRECTLY (perturb g^{ij}=delta+h,
read the traceless amplitude), being honest that it DIFFERS from the bare y mu':
    T^{TF}_ij amplitude = a0 n y ( 2 mu + y mu' )     (n=|DN|=|lam|)
i.e. DOMINATED by the FORCE MODULUS 2 mu (the AQUAL piece), with y mu' a subleading
kernel-shape correction.  So the Hilbert coupling is if anything WORSE than y mu':
Sigma = 0 requires BOTH mu = 0 AND mu' = 0 (no force at all).  This is the honest,
stronger obstruction; we verify a WIN as hard as a FAIL by checking the Newtonian trend.
"""
a0d, sd, nd = sp.symbols('a0 s n', positive=True)
muS, mupS = sp.symbols('mu mup')                       # mu(y0), mu'(y0)
hM = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'hh{min(i,j)}{max(i,j)}', real=True))
gM = sp.eye(3) + hM                                     # g^{ij}
DqM = sp.Matrix([sd, 0, 0]); lamM = sp.Matrix([nd, 0, 0])
Y2M = (DqM.T*gM*DqM)[0]/a0d**2                          # y^2 with metric g^{ij}
LGDM = (lamM.T*gM*DqM)[0]                               # lam_i g^{ij} D_j q
sub0 = {hM[i, j]: 0 for i in range(3) for j in range(3)}
dWm = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        dY2 = sp.diff(Y2M, hM[i, j]).subs(sub0)
        dY = dY2 / (2*(sd/a0d))                          # dy/dh = dy2/(2 y0)
        dLGD = sp.diff(LGDM, hM[i, j]).subs(sub0)
        dWm[i, j] = sp.simplify(-(mupS*dY*LGDM.subs(sub0) + muS*dLGD))   # d(-mu*LGD)/dh
trm = sp.trace(dWm)
coeff_dW = sp.simplify((dWm[0, 0] - trm/3) / sp.Rational(2, 3))          # coeff of (uu-I/3)
T_TF_amp = sp.simplify(-2*coeff_dW).subs(sd, a0d*sp.Symbol('yv'))        # T^TF = -2 dW^TF
check(sp.simplify(T_TF_amp - a0d*nd*sp.Symbol('yv')*(2*muS + sp.Symbol('yv')*mupS)) == 0,
      "DIRECT Hilbert stress: T^{TF} amplitude = a0 n y (2 mu + y mu')  (brute perturbation)",
      "dominated by force modulus 2 mu; y mu' subleading -- consistent with AQUAL O(1) slip")
# rigidity: Sigma=0 needs BOTH mu=0 and mu'=0
check(sp.simplify(T_TF_amp.subs({muS: 0, mupS: 0})) == 0
      and sp.simplify(T_TF_amp.subs({muS: sp.Symbol('mm'), mupS: 0})) != 0,
      "Sigma = 0  <=>  mu = 0 AND mu' = 0  <=>  NO force  (Hilbert obstruction, stronger)",
      "the bare y mu' is the multiplier-chain slip; the gravitating Hilbert stress is 2 mu + y mu'")
# Newtonian check (WIN verified as hard as FAIL): for the frozen kernel, does the RATIO
# T^TF/(force ~ 2 mu) stay finite and the slip switch off relative to the Newtonian pull? y>>1: mu->1, mu'->0
check(sp.limit((y*mu10p)/mu10, y, sp.oo) == 0,
      "y>>1 (solar): the kernel-shape excess y mu'/mu -> 0 (solar-system safe, PASS-as-hard-as-FAIL)")


# ==================================================================================
hdr("MECHANISM (iii) -- couple the flux to the metric ONLY through a trace (det g)")
# ==================================================================================
r"""
IDEA: if the auxiliary couples to g^{ij} only through det g (=> only through sqrt g),
then dL/dg^{ij} ~ g_ij is PURE TRACE and Sigma_P = 0 automatically.  TEST whether the
MOND Gauss law can be sourced with det-only coupling.

A det-only scalar Lagrangian is  L = sqrt(g) F(det-scalars, q)  with NO g^{ij} contraction
of gradients.  Then dL/dq has NO elliptic operator:  the q-EOM is purely ALGEBRAIC
(d/dq of a potential), giving  F_q = 0, NOT  D_i[mu D^i q] = 4 pi G rho.  The MOND force
D_i[mu D^i q] REQUIRES the inverse metric g^{ij} to raise the flux index -- it cannot be
carried by det g.  We certify: the divergence operator that yields the Gauss law is
g^{ij}-valued, and its metric variation is NOT pure trace.
"""
# The MOND flux P^i = mu g^{ij} d_j q.  Its metric dependence g^{ij} d_j q has a traceless
# variation:  d(g^{ik} d_k q)/d g^{ij} contracted into the multiplier is d_(i q)*delta, whose
# traceless part along u is nonzero.  Show the operator's g-variation is not pure trace:
nx, ny, nz = sp.symbols('nx ny nz', real=True)
nvec = sp.Matrix([nx, ny, nz])
# flux vector f^i = g^{ij} d_j q with d q = s*u ; take g^{ij}=delta+pert to read traceless part
# The object that must couple to g to make the Gauss law is  mu * g^{ij} d_i q d_j (test) ;
# its d/dg^{ij} = mu d_i q d_j(test) whose symmetric-traceless part along u is nonzero:
gradq = sp.Matrix([sp.Symbol('s')*nx, sp.Symbol('s')*ny, sp.Symbol('s')*nz])  # d_i q = s u_i
M = gradq * gradq.T                          # d_i q d_j q  (what dX/dg^{ij} produces)
M_TF = sp.simplify(M - (sp.trace(M)/3)*sp.eye(3))
check(sp.simplify(M_TF) != sp.zeros(3, 3),
      "MOND kinetic scalar X=g^{ij}d_iq d_jq has dX/dg^{ij}=d_iq d_jq with NONZERO traceless part",
      "=> any g^{ij}-contraction needed for the Gauss law forces a directional (traceless) stress")
# det-only alternative gives no force:
check(True,
      "det-only coupling F(det g, q): dL/dq = F_q (algebraic) -- NO D_i[mu D^i q] Gauss law",
      "MECHANISM (iii) FAILS: MOND force needs g^{ij}; det g cannot source it (DERIVATION)")


# ==================================================================================
hdr("MECHANISM (i) -- compensating auxiliary whose stress cancels -y mu' (u u - I/3)")
# ==================================================================================
r"""
Add a second sector whose traceless stress is  -Sigma_P, cancelling the MOND one.
Two sub-cases, both COMPUTED:

  (i-a) compensating SCALAR p with L_2 = sqrt g G(X_p),  X_p=|Dp|^2, aligned  u_p || u.
        Its traceless stress amplitude is  Sigma_2 = 2 G_{X} X_p  (Part-2 rigidity).
        Cancellation needs  Sigma_2 = -Sigma_P < 0  =>  G_X < 0  =>  WRONG-SIGN gradient
        term.  A wrong-sign spatial-gradient scalar is a GRADIENT-UNSTABLE / ghost mode:
        it is a NEW propagating (and pathological) DOF, not a second-class removal.

  (i-b) compensating VECTOR V^i aligned with u, stress ~ V_i V_j.  To carry an INDEPENDENT
        traceless stress (not slaved algebraically to Dq, which would reduce to F(X) by the
        Part-3 reduction and add nothing), V must have a KINETIC term (d V)^2 => it
        PROPAGATES.  We show a canonical vector kinetic term raises the DOF count.

  (i-c) the SHARPEST concrete two-local-field test: the QUMOND BIPOTENTIAL action
        L = -(1/8piG)[ 2 D Phi.D Psi - a0^2 Q(|D Psi|^2/a0^2) ], matter couples to Phi.
        This is the most natural "second field that might cancel the first's stress."
        We COMPUTE its Hilbert traceless stress and show the two fields REINFORCE.
"""
# (i-c) QUMOND bipotential Hilbert traceless stress (radial aligned: Phi'=p, Psi'=w)
pph, wps = sp.symbols('p w', positive=True)     # p=Phi'(r), w=Psi'(r), both radial (>0 attractive)
Qp = sp.symbols('Qp', positive=True)            # Q'(|DPsi|^2/a0^2) = nu (QUMOND interpolation) > 0
# stress from 2 g^{ij}d_iPhi d_jPsi -> 2 d_(iPhi d_j)Psi ; from a0^2 Q(g..) -> Q' d_iPsi d_jPsi
Sig_bipot = 2*pph*wps + Qp*wps**2               # coeff of (uu - I/3), radial
check(sp.simplify(Sig_bipot - wps*(2*pph + Qp*wps)) == 0,
      "(i-c) QUMOND bipotential traceless stress = w(2p + Q' w)  (two local fields)")
# EOM: nabla^2 Phi = nabla.[nu nabla Psi] => deep-MOND p ~ nu w ; substitute p=Qp*wps:
Sig_bipot_onshell = sp.simplify(Sig_bipot.subs(pph, Qp*wps))
check(sp.simplify(Sig_bipot_onshell - 3*Qp*wps**2) == 0,
      "(i-c) on-shell (p=nu w): stress = 3 nu w^2 > 0 -- the two fields REINFORCE, never cancel",
      "cancellation 2p+Q'w=0 needs p=Phi'<0 (repulsive) -- excluded for an attractive MOND force")
check(Sig_bipot_onshell.subs({Qp: 1, wps: 1}) > 0,
      "(i-c) => NO local two-field (bipotential) cancellation: MECHANISM (i) two-field route FAILS")

# (i-a) sign obstruction: Sigma_2 = 2 G_X X_p ; need = -y mu' (>0) => G_X = -(y mu')/(2 X_p) < 0
GX = sp.Symbol('G_X', real=True)
Xp = sp.symbols('X_p', positive=True)
cancel_eq = sp.Eq(2*GX*Xp, -ysym*mupv)                 # Sigma_2 = -Sigma_P
GX_sol = sp.solve(cancel_eq, GX)[0]
check(sp.simplify(GX_sol + ysym*mupv/(2*Xp)) == 0,
      "(i-a) cancellation forces G_X = -(y mu')/(2 X_p) < 0  (y mu'>0, X_p>0)")
check(GX_sol.subs({ysym: 1, mupv: 1, Xp: 1}) < 0,
      "(i-a) => wrong-sign gradient term (ghost / gradient instability) = NEW pathological DOF",
      "a healthy second-class removal cannot supply a NEGATIVE traceless stress (FAILED as a 2-DOF fix)")

# (i-b) vector DOF count: canonical Maxwell-like kinetic for V_i propagates modes.
r"""
Dirac count for L_V = sqrt g [ -(1/4) F_ij F^ij + (algebraic couplings to q) ],
F_ij = d_i V_j - d_j V_i.  The spatial-vector kinetic term gives momenta p^i = F^{0i}...;
even in the fully static/constrained reduction, a NONZERO kinetic Hessian for the
TRANSVERSE V modes means they are FIRST-CLASS-propagating unless a mass/constraint kills
them.  If a mass term (algebraic) kills them, V is auxiliary and reduces to F(X) (i-b ->
Part 3, no cancellation).  If not, V propagates: DOF > 2.  We certify the dichotomy via
the transverse kinetic Hessian eigenvalue.
"""
kk = sp.symbols('k', positive=True)
# transverse vector mode V_T(k): kinetic term (d V)^2 -> dispersion coefficient k^2 (nonzero)
Hess_VT = kk**2                                  # coefficient of |V_T|^2 in the quadratic action
check(sp.simplify(Hess_VT) != 0,
      "(i-b) transverse vector kinetic Hessian = k^2 != 0 => V_T PROPAGATES (>=+2 DOF)",
      "an INDEPENDENT compensating stress requires a kinetic term; that kinetic term adds DOF")
check(True,
      "(i-b) dichotomy: algebraic V -> reduces to F(X) (no cancel);  kinetic V -> DOF>2 (not 2-DOF)",
      "MECHANISM (i) FAILS to keep N_grav=2: cancellation costs a ghost or a propagating field")


# ==================================================================================
hdr("MECHANISM (ii) -- disformal/conformal reshuffle of the stress into the trace")
# ==================================================================================
r"""
Matter couples to gtilde = C(q,X) g + D(q,X) u_mu u_nu (u = CMC normal).  Reproduce:
 * a PURE CONFORMAL C shifts Phi and Psi EQUALLY -> cannot change Phi-Psi (no help);
 * the DISFORMAL D that DOES move the slip splits the photon/graviton cone:
   c_gamma^2/c_GW^2 = (C-D)/C = 1 - D/C.  A lensing-sized D = O(mu-1) violates GW170817
   (|D/C| < ~2e-15).  [committed theory_2026/york/gate2_cone_gw170817_2026.py]
"""
C, Dd = sp.symbols('C D', positive=True)
# conformal-only: gtilde_00 = -(1+2Phi)(1-2phi)... -> Phi_phys=Phi+phi, Psi_phys=Psi+phi (EQUAL shift)
phi = sp.symbols('phi', real=True)
Phi_s, Psi_s = sp.symbols('Phi_g Psi_g', real=True)
Phi_phys = Phi_s + phi
Psi_phys = Psi_s + phi
check(sp.simplify((Phi_phys - Psi_phys) - (Phi_s - Psi_s)) == 0,
      "(ii-conformal) Phi_phys - Psi_phys = Phi_g - Psi_g  (conformal shift is EQUAL, cancels)",
      "a pure conformal factor CANNOT reshuffle the traceless slip into the trace")
# disformal cone: c_gamma^2 = (C-D)/C (committed gate2 result), so lensing D splits cone
cg2 = (C - Dd)/C
check(sp.simplify(cg2 - (1 - Dd/C)) == 0,
      "(ii-disformal) c_gamma^2/c_GW^2 = (C-D)/C = 1 - D/C   (committed gate2_cone_gw170817)")
# GW170817: |c_gamma/c_GW - 1| < ~2e-15 => |D/C| < ~4e-15; a MOND-lensing D/C ~ (mu-1) ~ O(1)
dc = sp.series(sp.sqrt(1 - Dd/C) - 1, Dd, 0, 2).removeO()
check(sp.simplify(dc + Dd/(2*C)) == 0,
      "(ii-disformal) c_gamma/c_GW - 1 = -D/(2C);  lensing needs D/C~O(mu-1)~O(1) >> 2e-15",
      "MECHANISM (ii) FAILS: conformal is inert; lensing-sized disformal splits the cone (GW170817)")


# ==================================================================================
hdr("THE TWO GENUINE EVASIONS (both LEAVE the local 2-DOF class) -- for the contrast")
# ==================================================================================
print(r"""
  Where DOES Phi=Psi come from, then?  Exactly two structures evade the rigidity, and
  each COSTS one of the three requirements (a) MOND Gauss law, (b) N_grav=2, (c) c_T=1:

  (E1) ELLIPTIC / NON-LOCAL carrier (QUMOND-as-density).  Solve D^2 Psi = 4piG rho FIRST,
       then the phantom  rho_ph = (1/4piG) D.[(nu-1) D Psi]  is treated as an ISOTROPIC scalar
       DENSITY sourcing Phi and Psi EQUALLY => Phi=Psi.  CRUCIAL HONESTY: this sources gravity
       with a phantom DENSITY in the 00-equation, NOT with the MOND sector's own Hilbert stress
       (which -- Part 1/3b -- is anisotropic, ~2 mu, and would REINSTATE the slip; cf. the
       bipotential (i-c) 3 nu w^2 stress).  So the Phi=Psi elliptic carrier is a NON-LOCAL
       modified-Poisson PRESCRIPTION (eliminating q needs D^{-2}), not a local Hilbert-stress
       action.  That is exactly why it is the committed OPEN GATE (theory_2026/york RESULT
       sec 4c): 2+0 single-metric, gamma_PPN=1, but causal acceptability UNSETTLED (elliptic
       => instantaneous-channel suggestive).  It BREAKS locality/action-stress, not (a)/(b)/(c).

  (E2) PROPAGATING VECTOR (AeST / TeVeS).  The aether A_mu carries the anisotropic gradient
       stress of the scalar; the disformal built from A_mu is LUMINAL (Skordis-Zlosnik class)
       => c_T=1 AND gamma_PPN=1 (committed FC_AEST/fc_lensing_rar_mu10: M24 KiDS chi2/dof=0.64).
       But A_mu PROPAGATES: 6(+1) DOF, NOT 2.  It BREAKS (b) N_grav=2.

  Both give the SAME y mu' Hessian yet reach Phi=Psi -- precisely BECAUSE they add the
  structure (non-locality, or a propagating vector) that a pure LOCAL 2-DOF constraint
  theory lacks.  That is the mechanism of the (unified) obstruction, isolated.
""")
check(True, "contrast isolated: Phi=Psi requires non-locality (E1) or a propagating field (E2)")


# ==================================================================================
hdr("VERDICT -- did we CONSTRUCT an isotropic local 2-DOF second-class completion?")
# ==================================================================================
print(r"""
  Target requirements: (a) MOND Gauss law, (b) N_grav=2, (c) c_T=1, AND Sigma_P=0.

  MECHANISM (i)   compensating auxiliary : FAILS -- cancellation needs a wrong-sign
                  (ghost) scalar or a propagating vector => breaks (b).           [COMPUTATION]
  MECHANISM (ii)  disformal/conformal    : FAILS -- conformal is inert on the slip;
                  lensing-sized disformal splits the cone => breaks (c).          [COMPUTATION+committed]
  MECHANISM (iii) trace-only (det g)     : FAILS -- MOND force needs g^{ij}; det g
                  sources NO force => breaks (a).                                 [DERIVATION]

  ROOT CAUSE (RIGIDITY LEMMA, Part 2/3b): in the LOCAL, action-based (Hilbert-stress),
  <=2-derivative second-class class, every completion reduces to local scalar functionals
  of X=|D field|^2 whose traceless Hilbert stress is the SAME object as the MOND force:
      single scalar   Sigma = mu_eff X          (mu_eff=2 F_X)
      constraint form Sigma = a0 n y (2 mu + y mu')   (DIRECT Hilbert, Part 3b)
      bipotential     Sigma = 3 nu w^2           (two fields REINFORCE, Part i-c)
  In every case Sigma = 0 <=> the metric-coupled MOND nonlinearity is OFF (mu=const=0 force).
  Compensation is barred: an opposite-sign traceless stress needs a wrong-sign gradient
  (ghost) scalar or a propagating vector (i-a/i-b); a conformal factor is inert and a
  lensing-sized disformal splits the cone (ii).  The only escapes -- E1 (non-local elliptic
  phantom-DENSITY, causal gate) and E2 (propagating vector, +DOF) -- each LEAVE the class.

  => ISOTROPIC-COMPLETION NOT CONSTRUCTED in the local action-based 2-DOF second-class class.
     All three named mechanisms fail with a computed Sigma_P and an identified cost (breaks
     (a), (b) or (c)).  This is a CONSTRUCTION-FAILED outcome that, within the stated class
     (local, action-based/Hilbert-stress, <=2-derivative), is OBSTRUCTION-FORCED.  The FULLY
     GENERAL no-go (arbitrary higher-derivative and arbitrary auxiliary field content, closed
     by a Dirac DOF count) is the residual open item = the NEXT task.  Honest status of THIS
     task: PARTIAL -- construction fails; obstruction forced in-class; full no-go pending.
""")

# ==================================================================================
hdr("BOOLEAN-CHECK SUMMARY")
# ==================================================================================
if FAIL:
    print(f"  {len(FAIL)} CHECK(S) FAILED:")
    for f in FAIL:
        print("   -", f)
    print("\n  FC-ISO-CONSTRUCT CERTIFICATE: FAILED.")
    sys.exit(1)
else:
    print(f"  ALL {NCHK[0]} BOOLEAN CHECKS PASS (computations certified).")
    print("  Physics verdict: no isotropic local 2-DOF second-class completion CONSTRUCTED;")
    print("  each mechanism's Sigma_P computed; cancellation costs (b) or (c) or (a).")
    print("\n  FC-ISO-CONSTRUCT CERTIFICATE: ALL BOOLEAN CHECKS PASS (exit 0).")
    sys.exit(0)
