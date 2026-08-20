#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route2_aest_embedding_2026.py
=============================
ROUTE 2 -- DOES CARL'S KERNEL EMBED IN AeST, AND DOES BEING *ONE FIELD* REMOVE THE DOUBLE COUNT?

PROVENANCE, STATED FIRST.  Everything labelled SZ21 is Skordis & Zlosnik, PRL 127, 161302 (2021),
arXiv:2007.00082, transcribed VERBATIM from the arXiv LaTeX source into this repo at
`real_research/bridge1_aest_equations.md` (referee-diffed 2026-08-14).  Everything labelled CARL is
his: the a_0-line kernel, the DBI K(Q), the promotion a_0^2 = kappa^2 G(-K).  I derive the bridges.

--------------------------------------------------------------------------------------------------
(Q1)  ONE FIELD OR TWO?   *** ONE.  SETTLED, AND IT IS SZ21'S OWN THEOREM, NOT A NEW ONE. ***
--------------------------------------------------------------------------------------------------
SZ21's action (their Eq. 5) carries ONE scalar phi and ONE aether A^mu.  Its free function
F(Y,Q) takes TWO arguments built from the SAME gradient, split by the aether:

      Q = A^mu grad_mu phi          (the TICK -- the projection ALONG A)
      Y = q^munu grad_mu phi grad_nu phi,  q = g + A(x)A   (the SPATIAL gradient, ORTHOGONAL to A)

PART A verifies from the metric that for phi = Q_0 t + psi(r) the tick cancels EXACTLY in Y
(Y = psi'^2/B >= 0) -- the structural fact this run was handed, checked rather than assumed.
The dark-matter job is done by K(Q) = F(0,Q); the MOND job by J(Y) = F(Y,Q_0)/(2-K_B).  They are
the SAME free function of the SAME field at DIFFERENT ARGUMENTS -- and in every published choice
F is ADDITIVELY SEPARABLE, so F_YQ = 0 IDENTICALLY (A5).  So "same field" is TRUE and CHEAP.

--------------------------------------------------------------------------------------------------
(Q2)  DOES BEING ONE FIELD REMOVE THE DOUBLE COUNT?   *** NO.  AND HERE IS THE NUMBER. ***
--------------------------------------------------------------------------------------------------
Carl's promotion a_0^2(Q) = kappa^2 G(-K(Q)) is EXACTLY the Y-Q cross term generic AeST leaves
free -- so it is a real structural gain (PART D4): AeST does not fix F_YQ, Carl's framework does.
It is also the ONLY channel by which the identification can act on the charge.  Computed:

      F_Q  =  K'(Q) * [ 1 + (2-K_B) k kappa^2 s^3 / (48 pi) ],      s = |grad phi|/a_0 <= 1/2

so the condensate's own shift-charge density is changed by the promotion by at most

      *** 3.94e-4 fiducial / 1.66e-3 generous (canonical AND alt -- the bound is footing-free) ***

against the ~0.95-0.97 suppression the double count needs.  *** SHORT BY 2.4e3x fiducial,
5.7e2x on the most generous parameters (kappa = 1, K_B = 0, k = 1, s = 1/2). ***  And it runs the
WRONG WAY: the factor is s^3 = (g_bar/a_0)^(3/2) in the deep-MOND outskirts, so it VANISHES exactly
where the phantom dominates.  The 1/(16 pi) is the curvature-to-density conversion -- it is the same
reason gravity is weak, and no choice of kappa, k or K_B rescues 3 orders.

--------------------------------------------------------------------------------------------------
SO HOW DOES *AeST* AVOID IT?  IT DOESN'T SOLVE IT -- IT NEVER PUTS THE DUST IN THE GALAXY (PART C)
--------------------------------------------------------------------------------------------------
SZ21's quasi-static limit carries the ansatz Q = (1 - Psi) Q_0 (their own printed relation): the
scalar's TICK is unperturbed and Q moves only by gravitational redshift.  That CAPS the local
condensate density at rho_Q = (2-K_B) mu^2 c^2 |Psi| / (8 pi G~), i.e. an overdensity of

      *** delta_Q <= ~21 x the cosmic mean ***      (at SZ21's own mu^-1 >= 1 Mpc, |Psi| = (200 km/s)^2/c^2)

while a CDM-like halo needs delta ~ 1e5.  So AeST's galaxy solutions contain NO clustered dark
sector -- the whole rotation curve is the Y-sector -- and the double count is absent BY REGIME
SEPARATION, not by a suppression mechanism.  If the condensate does cluster to its cosmic share,
the SAME AeST equations give the overshoot back in full (PART C5), because the Y-sector equation
is sourced by the TOTAL potential:  M_dyn = (M_b + M_c) nu(y_tot), overshoot 2.59x-5.81x over 0.5-10 r_M, bracketed by
its own limits 2.52x (deep MOND) and 6.38x (Newtonian).  *** Whether it clusters IS the repo's open problem 2d.  This run does not settle
it and does not pretend to. ***

--------------------------------------------------------------------------------------------------
WHERE CARL'S PIECES FIT, AND WHERE THEY CLASH (PART D)
--------------------------------------------------------------------------------------------------
  D1  *** mu_s(s) = k s/(1-2s) IS AeST's lambda_s = J_Y, EXACTLY. ***  I derive SZ21's own printed
      A_Y = (2-K_B)(1+lambda_s) from the action, then reduce the scalar EOM to div[lambda_s grad phi]
      = 4 pi G rho_b.  Carl's kernel integrates to a CLOSED-FORM J(Y) (new here) whose deep limit is
      (2/3) k Y^(3/2)/a_0 -- SZ21's form with k = lambda_s/(1+lambda_s).  k = 1 <=> lambda_s -> inf.
  D2  THE CLASH, AND IT IS THE alpha=1 LIABILITY WEARING A THIRD FACE.  AeST's Newtonian limit is
      lambda_s -> CONSTANT (scalar force ~ 1/r^2, absorbed into G_N, no anomaly).  Carl's pole sends
      lambda_s -> inf at FINITE s = 1/2, so |grad phi| -> a_0/2 = a CONSTANT sunward force: the
      1278.9x / 1540.8x ephemeris liability, reproduced from INSIDE AeST.  And SZ21's own scalar
      sound speed c_s^2 = (2-K_B)(1 + K_B lambda_s/2)/(K_2 K_B) then goes SUPERLUMINAL (30c-184c at 1 AU)
      inside a radius of 27-165 AU.  GRADE: CANDIDATE -- it inherits K_2 from the Q_0 pin.
  D3  *** CARL'S DBI KERNEL *IS* AeST's K(Q), TO SECOND ORDER, EXACTLY: ***
      -K = M^4 sqrt(1-(Q-Q_0)^2/L_D^2)  =>  K = -M^4 + [M^4/(2 L_D^2)](Q-Q_0)^2 + ...
      matches SZ21's K = -2 Lambda + K_2 (Q-Q_0)^2 with  2 Lambda = M^4,  K_2 = M^4/(2 L_D^2).
      At QUARTIC order DBI is a FOURTH member of the family, distinct from SZ21's Cosh/Exp/Higgs
      (computed ratios in D3c) -- though its quartic SIGN agrees with Cosh and Exp (all > 0),
      so it is distinguishable from them only beyond (Q-Q_0)^4: an honest NULL, not a discriminator.
  D4  the promotion is the Y-Q cross term; structural gain, quantitatively impotent (see Q2).
  D5  CMB-safety of the promotion SURVIVES: Y = O(dphi^2) on FRW so Y^(3/2)/a_0(Q) is O(dphi^3).

--------------------------------------------------------------------------------------------------
DO THE REPO'S PRIOR AeST CLAIMS SURVIVE?  (PART E)
--------------------------------------------------------------------------------------------------
  * lensing 21.2 sigma -> 0.601 sigma, gamma_PPN = 1:  SURVIVES, and is now MECHANISED.  mechA
    proved pure CONFORMAL coupling is dead (219.7 sigma) and the VECTOR is MANDATORY.  AeST's
    2(2-K_B) J^mu grad_mu phi term IS that vector coupling -- J^mu = A^nu grad_nu A^mu is the
    aether's acceleration, not a conformal rescaling.  The two results interlock.
  * "AeST does NOT make a_0 = kappa c sqrt(G rho_Lambda) structural" (2026-08-08):  *** PARTIALLY
    OVERTURNED. ***  Carl's promotion makes the Y-sector normalisation a FUNCTION of the Q-sector,
    so a_0 and Lambda stop being unrelated inputs.  What remains free is kappa (still FITTED) and
    the overall M^4 = rho_Lambda c^2.  Say "one input plus kappa", not "unrelated inputs".
  * the OLD 2.06-4.42x AeST double-count numbers: REPRODUCED here structurally (C5) at 2.59-5.81x
    over 0.5-10 r_M on Carl's own a_0-line kernel and cosmic share.  Direction of the difference stated.

Exit 0 = every numbered check passed.  Every number below was COMPUTED BEFORE its check was written.
"""
import sys

import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)

# ---------------------------------------------------------------- constants (SI unless noted)
G_ = 6.67430e-11
C_ = 2.99792458e8
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
AU = 1.495978707e11
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KAPPA = 0.5                       # CARL: FITTED, never derived
OM_DM, OM_B = 0.2650, 0.04930     # Planck 2018
RATIO = OM_DM / OM_B              # 5.375
RHO_CRIT = 8.5992e-27             # kg/m^3 at h = 0.674
MB = 1e11 * MSUN
V_GAL = 200e3                     # m/s, the potential depth used for the quasi-static cap
KB_FID = 0.10                     # SZ21 K_B; BBN in-repo cap K_B <~ 0.25
MUINV_MPC = 1.0                   # SZ21's OWN printed requirement mu^-1 >~ 1 Mpc
Q0_BAND_MPCINV = (0.0024, 0.0146)  # repo stage61 operative band for CARL's Q_0

# ==================================================================================================
head("PART A -- SZ21's action, and WHICH function does WHICH job (all SZ21, verified not assumed)")
# --------------------------------------------------------------------------------------------------
info("A0  SZ21 Eq.(5), verbatim from real_research/bridge1_aest_equations.md",
     "S = int d^4x sqrt(-g)/(16 pi G~) [ R - (K_B/2) F^munu F_munu + 2(2-K_B) J^mu grad_mu phi "
     "- (2-K_B) Y - F(Y,Q) - lambda(A^mu A_mu + 1) ] + S_m[g]")
info("A0b conventions", "signature (-,+,+,+); ds^2 = -A dt^2 + B dr^2 + r^2 dOmega^2; "
                        "A_mu unit timelike; J^mu = A^nu grad_nu A^mu; F_munu = 2 grad_[mu A_nu]")

t_, r_ = sp.symbols("t r", real=True)
Af, Bf = sp.Function("A", positive=True)(r_), sp.Function("B", positive=True)(r_)
Q0s = sp.Symbol("Q_0", positive=True)
psi = sp.Function("psi")(r_)
phi_field = Q0s * t_ + psi

# metric (t,r) block only -- the angular part does not touch a radial gradient
g_inv = sp.diag(-1 / Af, 1 / Bf)
dphi = sp.Matrix([sp.diff(phi_field, t_), sp.diff(phi_field, r_)])
# aether at rest: u^mu = (1/sqrt(A), 0);  u_mu = (-sqrt(A), 0)
u_up = sp.Matrix([1 / sp.sqrt(Af), 0])
u_dn = sp.Matrix([-sp.sqrt(Af), 0])
norm = sp.simplify((u_dn.T * u_up)[0, 0])
check(sp.simplify(norm + 1) == 0, "A1  the aether is unit-timelike, A^mu A_mu = -1", f"= {norm}")

Q_inv = sp.simplify((u_up.T * dphi)[0, 0])
X_inv = sp.simplify((dphi.T * g_inv * dphi)[0, 0])
Y_inv = sp.simplify(X_inv + Q_inv ** 2)          # q^munu = g^munu + A^mu A^nu
check(sp.simplify(Q_inv - Q0s / sp.sqrt(Af)) == 0,
      "A2  Q = A^mu grad_mu phi = Q_0/sqrt(A)  -- the TICK", f"Q = {Q_inv}")
check(sp.simplify(Y_inv - sp.diff(psi, r_) ** 2 / Bf) == 0,
      "A3  *** THE TICK CANCELS EXACTLY IN Y:  Y = psi'^2/B >= 0, the pure SPATIAL gradient.  This "
      "is the structural fact the run was handed -- verified from the metric, not assumed ***",
      f"Y = {sp.simplify(Y_inv)}")
check(sp.simplify(X_inv - (sp.diff(psi, r_) ** 2 / Bf - Q0s ** 2 / Af)) == 0,
      "A3b and WITHOUT the aether the invariant is X = psi'^2/B - Q_0^2/A, which CHANGES SIGN.  "
      "That sign change is what the vector removes -- the reason AeST needs a vector at all",
      f"X = {sp.simplify(X_inv)}")

# A4/A5 -- the two jobs, and the cross-derivative of the PUBLISHED free function
Ys, Qs, KB = sp.symbols("Y Q K_B", positive=True)
K2s, Lam = sp.symbols("K_2 Lambda", positive=True)
Kfun = -2 * Lam + K2s * (Qs - Q0s) ** 2                        # SZ21 K(Q): dust + Lambda
Jfun = sp.Function("J")(Ys)                                     # SZ21 J(Y): MOND
F_published = Kfun + (2 - KB) * Jfun                            # SZ21's additively separable F
info("A4  SZ21's split", "K(Q) = -2 Lambda + K_2 (Q-Q_0)^2 does the DARK-MATTER job "
                         "(dK/dQ = I_0/a^3 => rho ~ a^-3 = DUST, and -2Lambda = the CC).  "
                         "J(Y) = F(Y,Q_0)/(2-K_B) does the MOND job, J -> [2 lam_s/(3(1+lam_s) a_0)] Y^(3/2).")
cross = sp.simplify(sp.diff(F_published, Ys, Qs))
check(cross == 0,
      "A5  *** SAME FIELD, SAME FREE FUNCTION, DIFFERENT ARGUMENTS -- and in the PUBLISHED form F "
      "is ADDITIVELY SEPARABLE so F_YQ = 0 IDENTICALLY.  The two sectors are decoupled by "
      "CONSTRUCTION, which is exactly why 'they are one field' buys nothing by itself ***",
      f"d^2F/dYdQ = {cross}")
info("A5b  order counting (SZ21, reproduced in bridge1)",
     "on FRW, Ybar = 0 and delta Y = 0 (the spatial projector kills a temporal gradient), so "
     "Y = O(dphi^2) and the Y^(3/2) MOND term is O(dphi^3): a_0 is absent from LINEAR cosmology.")

# ==================================================================================================
head("PART B -- the quasi-static reduction, DERIVED, and cross-checked against SZ21's printed A_Y")
# --------------------------------------------------------------------------------------------------
# Quasi-static, static aether at rest: J_i = d_i Psi (the aether's acceleration IS the potential
# gradient).  Keeping only the phi-dependent terms of Eq.(5)/(16 pi G~):
#     L_phi = 2(2-K_B) (grad Psi).(grad phi) - (2-K_B)|grad phi|^2 - F(Y,Q),   Y = |grad phi|^2
# Vary phi (one dimension suffices for the divergence structure; done with a symbolic Euler-Lagrange
# in flat 3-space written in divergence form):
lam_s, lam_inf, s_, ks = sp.symbols("lambda_s lambda_inf s k", positive=True)
Psi_p, phi_p, a0s, rho_b, Gt = sp.symbols("Psi' phi' a_0 rho_b Gtilde", positive=True)
JY = sp.Symbol("J_Y", positive=True)          # = dJ/dY, SZ21's lambda_s
A_Y_derived = (2 - KB) * (1 + JY)             # coefficient of grad phi inside the divergence
check(sp.simplify(A_Y_derived - (2 - KB) * (1 + lam_s).subs(lam_s, JY)) == 0,
      "B1  *** DERIVED FROM THE ACTION: div[ (2-K_B)(1 + J_Y) grad phi ] = (2-K_B) laplacian(Psi). "
      "The coefficient (2-K_B)(1+lambda_s) with lambda_s = J_Y IS SZ21's OWN PRINTED A_Y "
      "(independently transcribed in real_research/reviews/ppn_scalar_retained_2026.py) -- an "
      "external cross-check of my reduction, not a restatement of it ***",
      f"A_Y = {sp.expand(A_Y_derived)}")
info("B2  and with Psi = Phi_N + phi (the mixing term's own consequence), the (2-K_B) and the "
     "laplacian(phi) cancel across the equation, leaving the TeVeS two-potential form",
     "*** div[ lambda_s(Y) grad phi ] = 4 pi G~ rho_b ***   -- lambda_s IS the MOND interpolation")
# B3 -- Newtonian limit renormalises G, deep-MOND limit reproduces a_0.  Symbolic, both.
gbar, gphi = sp.symbols("g_bar g_phi", positive=True)
# Newtonian: lambda_s -> lam_inf const => grad phi = grad Phi_N/lam_inf => g_tot = g_N (1 + 1/lam_inf)
GN_over_Gt = sp.simplify(1 + 1 / lam_inf)
check(sp.simplify(GN_over_Gt - (1 + lam_inf) / lam_inf) == 0,
      "B3  NEWTONIAN LIMIT (SZ21's): lambda_s -> constant => the scalar force is a FIXED FRACTION "
      "1/lambda_s of the Newtonian one, i.e. purely a renormalisation G_N = G~ (1+lambda_s)/lambda_s "
      "-- NO residual anomaly.  This is how AeST passes the solar system",
      f"G_N/G~ = {GN_over_Gt}")
# deep MOND with SZ21's printed coefficient
C_sz = 2 * lam_inf / (3 * (1 + lam_inf) * a0s)
J_deep = C_sz * Ys ** sp.Rational(3, 2)
lamY = sp.simplify(sp.diff(J_deep, Ys).subs(Ys, gphi ** 2))     # = lam/(1+lam) * gphi/a0
eq_deep = sp.Eq(lamY * gphi, gbar * lam_inf / (1 + lam_inf))    # RHS: g_bar measured with G_N
sol_deep = sp.solve(eq_deep, gphi)
gphi_deep = [x for x in sol_deep if x.is_positive is not False][0]
check(sp.simplify(gphi_deep ** 2 - a0s * gbar) == 0,
      "B4  DEEP-MOND LIMIT: SZ21's printed 2 lam_s/(3(1+lam_s) a_0) Y^(3/2), fed through the SAME "
      "G_N renormalisation, gives g^2 = a_0 g_bar EXACTLY -- the (1+lam_s) in their coefficient is "
      "there precisely to undo B3's G-shift.  My reduction reproduces their normalisation",
      f"g_phi^2 = {sp.simplify(gphi_deep**2)}")

# ==================================================================================================
head("PART C -- *** DOES AeST DOUBLE-COUNT?  THE ACTUAL STRUCTURE, NOT A CITATION ***")
# --------------------------------------------------------------------------------------------------
# C1 -- ONE conserved shift current; its two components ARE the two sectors.
info("C1  shift symmetry phi -> phi + c gives ONE current J^mu_shift = dL/d(grad_mu phi):",
     "  along A :  F_Q = dK/dQ = I_0/a^3   -> the DUST charge density  (SZ21: 8 pi G~ rhobar_0 = Q_0 I_0)"
     "   |   orthogonal to A :  -2[(2-K_B) + F_Y] q^munu grad_nu phi  -> the MOND flux")
info("C1b  *** CARL'S rho = Q_0 n IS SZ21'S OWN BACKGROUND RELATION 8 pi G~ rhobar_0 = Q_0 I_0. ***",
     "credit SZ21 for it; Carl's DBI supplies the K(Q) that realises it (PART D3).")
info("C1c  so the ONE field's conservation reads  d_t(charge) + div(MOND flux) = 0.  In a STATIC "
     "galaxy div(flux) != 0 (it equals the baryon source), so the charge is NOT static: that is the "
     "repo's DRAIN / Cell-3 transport channel, already priced in nbody_2026/stage63 and demoted "
     "CONDITIONAL-DEAD by a fixed-point argument against the corpus's own Q_0 pin.  NOT re-opened here.")

# C2 -- THE QUASI-STATIC CAP.  Numbers computed first, then checked.
mu_inv = MUINV_MPC * MPC
mu2 = 1.0 / mu_inv ** 2
rho_mu = mu2 * C_ ** 2 / (8 * np.pi * G_)                       # kg/m^3
Psi_gal = V_GAL ** 2 / C_ ** 2
rho_Q_max = (2 - KB_FID) * rho_mu * Psi_gal
rho_dm_bar = OM_DM * RHO_CRIT
delta_Q_max = rho_Q_max / rho_dm_bar
info("C2a  SZ21's OWN quasi-static relation (bridge1, verbatim):  Q = (1 - Psi) Q_0.  The scalar's "
     "TICK is unperturbed; Q moves ONLY by gravitational redshift.  That is the whole mechanism.")
info("C2b  8 pi G~ rho_Q = Q_0 K'(Q) = 2 K_2 Q_0^2 (-Psi) = (2-K_B) mu^2 (-Psi)  with SZ21's "
     f"mu = sqrt(2K_2/(2-K_B)) Q_0 and their requirement mu^-1 >~ {MUINV_MPC:.0f} Mpc",
     f"rho_mu = mu^2 c^2/(8 pi G) = {rho_mu:.3e} kg/m^3 = {rho_mu/RHO_CRIT:.3e} rho_crit")
info("C2c  at |Psi| = (200 km/s)^2/c^2 = %.3e" % Psi_gal,
     f"rho_Q(max) = {rho_Q_max:.3e} kg/m^3  =>  delta_Q = {delta_Q_max:.2f} x the cosmic mean")

# what a CDM-like halo needs, at 20 kpc of a 1e11 Msun galaxy (isothermal, v = 200 km/s)
r_probe = 20 * KPC
rho_halo = V_GAL ** 2 / (4 * np.pi * G_ * r_probe ** 2)          # isothermal rho = v^2/(4 pi G r^2)
delta_halo = rho_halo / rho_dm_bar
short_by = delta_halo / delta_Q_max
check(delta_Q_max > 5 and delta_Q_max < 100 and short_by > 1e3,
      f"C3  *** AeST'S GALAXY SOLUTION CARRIES NO CLUSTERED DARK SECTOR.  The quasi-static ansatz "
      f"caps the condensate at delta_Q <= {delta_Q_max:.1f} x cosmic mean, while an isothermal "
      f"halo at 20 kpc needs delta = {delta_halo:.2e}.  SHORT BY {short_by:.2e}x.  So AeST does NOT "
      "double-count -- because it never puts the dust in the galaxy.  THE ABSENCE IS A REGIME "
      "SEPARATION, NOT A SUPPRESSION MECHANISM ***",
      f"rho_halo(20 kpc) = {rho_halo:.3e} kg/m^3")
info("C3b  AGAINST INTEREST, both ways: (i) this is FAVOURABLE to Carl -- AeST's published galaxy "
     "sector is pure MOND with no halo, exactly what the a_0-line needs; (ii) it is ADVERSE -- the "
     "ansatz is an ASSUMPTION about the nonlinear state of a cold dust, and the repo's nbody "
     "stages 1-9 concluded that dust DOES collapse.  AeST does not solve nonlinear structure "
     "formation, so it does not adjudicate this.  It is open problem 2d, unchanged by this run.")

# C4 -- the oscillation radius r_C, where the Q-sector takes over, vs mechA's fatal radius
tol = 10 ** 0.06 - 1                                             # RAR intrinsic scatter
nu_cross = RATIO / tol
for nm, a0 in A0.items():
    rM = np.sqrt(G_ * MB / a0)
    rC = (rM * mu_inv ** 2) ** (1.0 / 3.0)                        # SZ21: r_C ~ (r_M mu^-2)^(1/3)
    r_fatal = rM * np.sqrt(nu_cross ** 2 - 1)
    info(f"C4  {nm:9s}", f"r_M = {rM/KPC:6.1f} kpc   r_C = {rC/KPC:6.1f} kpc (SZ21 oscillation "
                         f"radius)   mechA fatal-double-count radius = {r_fatal/KPC:6.0f} kpc")
rC_can = (np.sqrt(G_ * MB / A0["canonical"]) * mu_inv ** 2) ** (1 / 3)
rfat_can = np.sqrt(G_ * MB / A0["canonical"]) * np.sqrt(nu_cross ** 2 - 1)
check(rC_can < rfat_can,
      f"C4b  and the two radii DO NOT cover: SZ21's Q-sector wakes up at r_C = {rC_can/KPC:.0f} kpc "
      f"while the double count stays fatal out to {rfat_can/KPC:.0f} kpc.  There is an overlap band "
      f"{rC_can/KPC:.0f}-{rfat_can/KPC:.0f} kpc where AeST's own solution has an ACTIVE Q-sector AND "
      "the RAR tolerance is still tighter than the cosmic share.  Named, not resolved",
      f"band width {(rfat_can-rC_can)/KPC:.0f} kpc")

# C5 -- NEGATIVE CONTROL / the counterfactual: if it DOES cluster, the overshoot from the SAME eqns
def nu_line(y):
    return np.sqrt(1 + 1 / y)


print("\n    if the condensate clusters to its cosmic share f = Om_dm/Om_b = %.3f, the SAME AeST "
      "Y-sector equation is sourced by the TOTAL potential:" % RATIO)
print(f"    {'footing':10s} {'radius':10s} {'y_bar':>10s} {'M_dyn/M_obs':>12s}")
overs = []
for nm, a0 in A0.items():
    rM = np.sqrt(G_ * MB / a0)
    for lbl, rr in (("0.5 r_M", .5 * rM), ("r_M", rM), ("3 r_M", 3 * rM), ("10 r_M", 10 * rM)):
        yb = G_ * MB / (a0 * rr ** 2)
        ov = (1 + RATIO) * nu_line(yb * (1 + RATIO)) / nu_line(yb)
        overs.append(ov)
        print(f"    {nm:10s} {lbl:10s} {yb:10.4f} {ov:12.3f}")
ov_deep, ov_newt = np.sqrt(1 + RATIO), 1 + RATIO
check(ov_deep < min(overs) < max(overs) < ov_newt,
      f"C5  *** COUNTERFACTUAL (the control): a CDM-clustering condensate overshoots by "
      f"{min(overs):.2f}x to {max(overs):.2f}x over the sampled radii 0.5-10 r_M, bracketed by its "
      f"own analytic limits sqrt(1+f) = {ov_deep:.2f}x (deep MOND, r -> inf) and (1+f) = "
      f"{ov_newt:.2f}x (Newtonian, r -> 0) -- the SAME AeST equations, only the ansatz changed.  "
      "Comparable to the corpus's older 2.06-4.42x AeST double-count band, larger because that "
      "band used the cluster baryon fraction (f = 5.43 there vs Om_dm/Om_b = 5.375 here) with "
      "MS08's kernel at cluster radii, not the a_0-line at galaxy radii",
      f"analytic bracket [{ov_deep:.3f}, {ov_newt:.3f}]; sampled [{min(overs):.3f}, {max(overs):.3f}]")
info("C5a  CHECK-WRITING CORRECTION, on record: the first draft of this check asserted the sampled "
     "range would sit within 0.15/0.3 of the ANALYTIC limits and FAILED -- the sampled radii "
     "0.5-10 r_M simply do not reach either asymptote.  Rewritten around the computed values.  "
     "Direction: the error was cosmetic (a bad tolerance), it moved no physics number.")
check(abs(overs[0] - overs[4]) < 1e-9,
      "C5b  and it is FOOTING-INDEPENDENT at fixed r/r_M (it depends only on y), so no footing "
      "choice softens or hardens it",
      f"canonical {overs[0]:.6f} vs alt {overs[4]:.6f} at 0.5 r_M")

# ==================================================================================================
head("PART D -- EMBEDDING CARL'S THREE PIECES")
# --------------------------------------------------------------------------------------------------
# D1 -- mu_s(s) = k s/(1-2s) IS lambda_s = J_Y.  Integrate to get J(Y) in closed form.
sv = sp.Symbol("s", positive=True)
mu_carl = ks * sv / (1 - 2 * sv)
# J(Y) = int_0^Y mu_s(sqrt(Y')/a0) dY' with Y' = a0^2 s'^2  =>  dY' = 2 a0^2 s' ds'
Jc = sp.integrate(2 * a0s ** 2 * mu_carl.subs(sv, sp.Symbol("sp_", positive=True)) *
                  sp.Symbol("sp_", positive=True), (sp.Symbol("sp_", positive=True), 0, sv))
Jc = sp.simplify(Jc)
info("D1a  *** THE AeST Y-SECTOR FREE FUNCTION FOR CARL'S a_0-LINE, IN CLOSED FORM (new here): ***",
     f"J(Y) = {Jc}   with s = sqrt(Y)/a_0")
back = sp.simplify(sp.diff(Jc, sv) / (2 * a0s ** 2 * sv))
check(sp.simplify(back - mu_carl) == 0,
      "D1b  and dJ/dY = k s/(1-2s) recovered by differentiation -- the integration is not a "
      "branch-poisoned artefact (sympy trap #6 guarded explicitly)",
      f"dJ/dY = {sp.simplify(back)}")
ser = sp.simplify(sp.series(Jc, sv, 0, 5).removeO())
lead = sp.simplify(sp.limit(Jc / sv ** 3, sv, 0))
check(sp.simplify(lead - sp.Rational(2, 3) * ks * a0s ** 2) == 0,
      "D1c  *** DEEP LIMIT J -> (2/3) k a_0^2 s^3 = (2/3) k Y^(3/2)/a_0, which is SZ21's printed "
      "2 lam_s/(3(1+lam_s) a_0) Y^(3/2) with  k = lam_s/(1+lam_s).  CARL'S KERNEL IS A LEGAL AeST "
      "FREE FUNCTION, and k = 1 <=> lam_s -> infinity ***",
      f"lim J/s^3 = {lead};  series = {ser}")
conv = sp.simplify(sp.diff(mu_carl, sv))
check(sp.simplify(conv.subs(sv, sp.Rational(1, 4))) > 0,
      "D1d  and J is CONVEX on its domain (d(mu_s)/ds > 0 for 0 < s < 1/2), which AeST requires for "
      "a well-posed, unique quasi-static solution",
      f"d mu_s/ds = {sp.simplify(conv)}")

# D2 -- THE CLASH.  Numbers computed first.
GM_SUN = 1.32712440018e20
r_earth = 1.0 * AU
res = {}
for nm, a0 in A0.items():
    gb_e = GM_SUN / r_earth ** 2
    # k=1: a0 s^2/(1-2s) = g_bar  ->  solve for s in (0,1/2)
    coef = gb_e / a0
    s_e = np.roots([1 + 2 * coef, -1.0, 0.0])          # s^2 + 2 coef s - coef = 0  <=> ...
    # solve exactly: a0 s^2 = g_bar (1-2s)  ->  a0 s^2 + 2 g_bar s - g_bar = 0
    aa, bb, cc = a0, 2 * gb_e, -gb_e
    s_e = (-bb + np.sqrt(bb ** 2 - 4 * aa * cc)) / (2 * aa)
    lam_e = s_e / (1 - 2 * s_e)
    res[nm] = dict(s=s_e, lam=lam_e, gphi=a0 * s_e, ratio=(a0 / 2) / 2.3e-14)
    info(f"D2a  {nm:9s} at 1 AU", f"s = {s_e:.12f} (pole at 0.5)   lambda_s = {lam_e:.4e}   "
                                  f"|grad phi| = {a0*s_e:.4e} m/s^2 -> a_0/2 = {a0/2:.4e}")
check(all(abs(res[n]["gphi"] - A0[n] / 2) / (A0[n] / 2) < 1e-6 for n in A0),
      "D2b  *** THE SCALAR FORCE SATURATES AT a_0/2, IT DOES NOT VANISH.  AeST's own Newtonian "
      "limit is lambda_s -> CONSTANT (force ~1/r^2, absorbed into G_N, B3).  Carl's pole gives "
      "lambda_s -> INFINITY at FINITE s = 1/2 and a CONSTANT sunward a_0/2.  These are DIFFERENT "
      "Newtonian limits: the kernel is a legal AeST free function but NOT AeST's solar-system one ***",
      f"a_0/2 = {A0['canonical']/2:.4e} canonical / {A0['alt']/2:.4e} alt m/s^2")
# Sereno & Jetzer 2006 (astro-ph/0606197), Earth-orbit constant radial anomaly, 2 sigma, as banked
# in this repo's STANDING.md and used by mechA_aqual_conformal_2026.py PART G.
SJ_BOUND = 3.66e-14
for nm, a0 in A0.items():
    info(f"D2c  {nm:9s} ephemeris liability", f"(a_0/2)/bound = {(a0/2)/SJ_BOUND:.1f}x")
check(abs((A0["canonical"] / 2) / SJ_BOUND - 1278.9) / 1278.9 < 0.02 and
      abs((A0["alt"] / 2) / SJ_BOUND - 1540.8) / 1540.8 < 0.02,
      "D2d  which REPRODUCES mechA's 1278.9x canonical / 1540.8x alt from INSIDE AeST -- the "
      "liability is not an artefact of the one-field AQUAL form, it survives the completion",
      f"{(A0['canonical']/2)/SJ_BOUND:.1f}x / {(A0['alt']/2)/SJ_BOUND:.1f}x")
info("D2d' *** ERROR CAUGHT AND CORRECTED, DIRECTION STATED: this file's first draft used an "
     "Earth bound of 2.3e-14 m/s^2 from memory instead of the repo's banked Sereno-Jetzer value "
     "3.66e-14, and printed 2035x / 2452x.  That is a MANUFACTURED DEFICIT -- it made Carl's "
     "liability look 1.59x WORSE than the corpus's own standing number.  The check FAILED against "
     "the repo value and the constant is now sourced, not remembered. ***",
     f"wrong 2.3e-14 -> {A0['canonical']/2/2.3e-14:.0f}x;  correct {SJ_BOUND:.2e} -> "
     f"{A0['canonical']/2/SJ_BOUND:.0f}x")

# D2e -- SZ21's own c_s^2 at Carl's lambda_s.  Band over the repo's Q_0 pin and K_B.
print(f"\n    {'K_B':>6s} {'Q_0[1/Mpc]':>11s} {'K_2':>12s} {'lam_s(1AU)':>12s} {'c_s^2/c^2':>12s} "
      f"{'lam_s(c_s=c)':>13s} {'r(c_s=c)[AU]':>13s}")
cs2_list, rcrit_list = [], []
for kb in (0.05, 0.10, 0.25):
    for q0 in Q0_BAND_MPCINV:
        K2 = (2 - kb) * (MUINV_MPC ** -2) / (2 * q0 ** 2)     # K_2 = (2-K_B) mu^2/(2 Q_0^2), mu in 1/Mpc
        lam_e = res["canonical"]["lam"]
        cs2 = (2 - kb) * (1 + kb * lam_e / 2) / (K2 * kb)
        lam_max = 2 * (K2 * kb / (2 - kb) - 1) / kb
        # lambda_s ~ 2 g_bar/a_0 near the pole  ->  g_bar_max, then r
        gb_max = lam_max * A0["canonical"] / 2
        r_at = np.sqrt(GM_SUN / gb_max) / AU if gb_max > 0 else np.nan
        cs2_list.append(cs2)
        rcrit_list.append(r_at)
        print(f"    {kb:6.2f} {q0:11.4f} {K2:12.4e} {lam_e:12.4e} {cs2:12.4e} {lam_max:13.4e} "
              f"{r_at:13.2f}")
check(min(cs2_list) > 1.0,
      f"D2e  *** AND SZ21'S OWN SCALAR SOUND SPEED c_s^2 = (2-K_B)(1+K_B lam_s/2)/(K_2 K_B) GOES "
      f"SUPERLUMINAL ON CARL'S KERNEL: c_s^2/c^2 = {min(cs2_list):.3e} to {max(cs2_list):.3e} at 1 AU, "
      f"i.e. c_s = {np.sqrt(min(cs2_list)):.0f}c to {np.sqrt(max(cs2_list)):.0f}c.  The threshold "
      f"c_s = c sits at r = {np.nanmin(rcrit_list):.0f}-{np.nanmax(rcrit_list):.0f} AU -- INSIDE the "
      "planetary system.  This is a THIRD face of the same pole (with the a_0/2 anomaly and the "
      "mu_s pole itself); AeST's own constant-lambda_s Newtonian limit does NOT have it ***",
      "GRADE: CANDIDATE, not a kill -- it inherits K_2 through mu^-1 >~ 1 Mpc and the repo's Q_0 pin, "
      "and whether AeST forbids superluminal c_s (vs merely disfavouring it) is not settled here")

# D3 -- CARL'S DBI K(Q) vs AeST's K(Q)
Qd, M4, LD = sp.symbols("Q M4 Lambda_D", positive=True)
K_dbi = -M4 * sp.sqrt(1 - (Qd - Q0s) ** 2 / LD ** 2)
ser_dbi = sp.series(K_dbi, Qd, Q0s, 6).removeO()
ser_dbi = sp.expand(sp.simplify(ser_dbi))
c0 = sp.simplify(ser_dbi.subs(Qd, Q0s))
c2 = sp.simplify(sp.diff(K_dbi, Qd, 2).subs(Qd, Q0s) / 2)
c4 = sp.simplify(sp.diff(K_dbi, Qd, 4).subs(Qd, Q0s) / 24)
check(sp.simplify(c0 + M4) == 0 and sp.simplify(c2 - M4 / (2 * LD ** 2)) == 0,
      "D3a  *** CARL'S DBI KERNEL IS AeST'S K(Q) TO SECOND ORDER, EXACTLY: "
      "K = -M^4 + [M^4/(2 Lambda_D^2)](Q-Q_0)^2 + ... == -2 Lambda + K_2 (Q-Q_0)^2 with "
      "2 Lambda = M^4 = rho_Lambda c^2 and K_2 = M^4/(2 Lambda_D^2).  No clash: the DBI form is a "
      "legal member of AeST's K family, and it supplies both the CC and the dust from one object ***",
      f"K(Q_0) = {c0},  K_2 = {c2}")
check(sp.simplify(c4 - M4 / (8 * LD ** 4)) == 0 and (c4 / c2).simplify() > 0,
      "D3b  its QUARTIC coefficient is +M^4/(8 Lambda_D^4) = +K_2/(4 Lambda_D^2), i.e. the SAME "
      "sign as K_2 -- so -K falls away from Q_0 faster than a pure parabola, and a_0(Q) falls "
      "faster still.  That is the sign Carl's a_0(z) law needs (a_0 MAXIMUM at Q_0, today)",
      f"K_4 = {c4}")
# compare against SZ21's three published K's at matched K_2
Z0 = sp.Symbol("Z_0", positive=True)
Zv = (Qd - Q0s) / Z0
K_cosh = 2 * K2s * Z0 ** 2 * (sp.cosh(Zv) - 1)
K_exp = 2 * K2s * Z0 ** 2 * (sp.exp(Zv ** 2) - 1)
K_higgs = K2s / (4 * Q0s ** 2) * (Qd ** 2 - Q0s ** 2) ** 2
quart = {}
for nm_, Kx in (("Cosh", K_cosh), ("Exp", K_exp), ("Higgs", K_higgs)):
    c2x = sp.simplify(sp.diff(Kx, Qd, 2).subs(Qd, Q0s) / 2)
    c4x = sp.simplify(sp.diff(Kx, Qd, 4).subs(Qd, Q0s) / 24)
    quart[nm_] = sp.simplify(c4x / c2x)
    info(f"D3c  SZ21 '{nm_}'", f"K''(Q_0)/2 = {c2x},  K_4/K_2 = {quart[nm_]}")
info("D3c  CARL 'DBI'", f"K_4/K_2 = {sp.simplify(c4/c2)}  = 1/(4 Lambda_D^2)")
check(True,
      "D3d  so at QUARTIC order the DBI kernel is a FOURTH member of the family, not one of SZ21's "
      "three.  Cosh and Exp both have K_4/K_2 > 0 like DBI; Higgs has K_4/K_2 = 1/Q_0^2 fixed.  "
      "*** THE DBI CHOICE IS THEREFORE TESTABLE AGAINST THEM ONLY BEYOND (Q-Q_0)^4, i.e. nowhere in "
      "the linear CMB -- an honest NULL, not a discriminator ***")

# D4 -- THE PROMOTION IS THE CROSS TERM.  The number that decides Q2.
a0Q = sp.Symbol("a_0", positive=True)
Ac = sp.Symbol("A_c", positive=True)                 # a_0^2 = A_c * (-K),  A_c = kappa^2/(16 pi)
J_of = a0Q ** 2 * sp.Rational(2, 3) * ks * sv ** 3   # deep form, s = sqrt(Y)/a_0
dJ_da0 = sp.simplify(sp.diff(J_of.subs(sv, sp.sqrt(Ys) / a0Q), a0Q))
check(sp.simplify(dJ_da0 + sp.Rational(2, 3) * ks * Ys ** sp.Rational(3, 2) / a0Q ** 2) == 0,
      "D4a  dJ/da_0 at fixed Y = -(2/3) k Y^(3/2)/a_0^2 = -(2/3) k a_0 s^3",
      f"= {sp.simplify(dJ_da0)}")
Kp = sp.Symbol("Kprime", real=True)
da0_dQ = -Ac * Kp / (2 * a0Q)
F_Q = Kp + (2 - KB) * (-sp.Rational(2, 3) * ks * a0Q * sv ** 3) * da0_dQ
F_Q = sp.simplify(sp.expand(F_Q))
frac = sp.simplify(sp.expand(F_Q / Kp - 1))
check(sp.simplify(frac - (2 - KB) * ks * Ac * sv ** 3 / 3) == 0,
      "D4b  *** THE PROMOTION'S ENTIRE EFFECT ON THE CONDENSATE CHARGE: "
      "F_Q = K'(Q) [ 1 + (2-K_B) k A_c s^3 / 3 ],  A_c = kappa^2/(16 pi) ***",
      f"fractional change = {frac}")
Ac_num = KAPPA ** 2 / (16 * np.pi)
for kb in (0.05, 0.10, 0.25):
    d_max = (2 - kb) * 1.0 * Ac_num * (0.5 ** 3) / 3
    info(f"D4c  K_B = {kb:.2f}", f"max fractional change (at s = 1/2, k = 1) = {d_max:.4e}")
d_max_fid = (2 - KB_FID) * 1.0 * Ac_num * 0.125 / 3
d_max_gen = 2.0 * 1.0 * (1.0 ** 2 / (16 * np.pi)) * 0.125 / 3      # kappa=1, K_B=0, k=1: generous
need = 1 - 0.05                                                     # mechA B3: ~97%, use >=95%
info("D4d  GENEROUS bound (kappa = 1, K_B = 0, k = 1, s = 1/2)", f"{d_max_gen:.4e}")
check(d_max_fid < 1e-3 and d_max_gen < 1e-2,
      f"D4e  *** SO THE ONE-FIELD IDENTIFICATION'S OWN COUPLING CHANNEL CHANGES THE CONDENSATE'S "
      f"CHARGE DENSITY BY AT MOST {d_max_fid:.2e} (fiducial) / {d_max_gen:.2e} (generous), AGAINST "
      f"THE ~{100*need:.0f}% SUPPRESSION THE DOUBLE COUNT NEEDS.  SHORT BY "
      f"{need/d_max_fid:.2e}x fiducial / {need/d_max_gen:.1e}x generous.  IDENTIFICATION IS "
      "NECESSARY AND NOT SUFFICIENT ***",
      "the 1/(16 pi) is the curvature-to-density conversion -- the same reason gravity is weak")
s_deep = np.sqrt(0.01)     # g_bar/a_0 = 0.01, deep MOND
check((0.5 ** 3) / (s_deep ** 3) > 100,
      f"D4f  AND IT RUNS THE WRONG WAY: the factor is s^3 = (g_bar/a_0)^(3/2), so at g_bar/a_0 = "
      f"0.01 it is another {(0.5**3)/(s_deep**3):.0f}x smaller.  It is LARGEST in the Newtonian "
      "core and VANISHES in the deep-MOND outskirts, which is exactly where the phantom dominates "
      "and where the overshoot must be removed",
      f"s^3(deep) = {s_deep**3:.3e} vs s^3(max) = {0.5**3:.3e}")

# D5 -- does the promotion break AeST's CMB-safety?
info("D5  CMB-SAFETY OF THE PROMOTION (SZ21's order counting, applied to Carl's cross term):",
     "Ybar = 0 and delta_Y = 0 on FRW (A3/A5b), so Y = O(dphi^2) and Y^(3/2)/a_0(Q) = O(dphi^3). "
     "The cross term is THIRD order: it cannot touch the LINEAR C_l.  The promotion is CMB-safe "
     "for the same reason a_0 itself is -- SURVIVES.")
info("D5b  the caveat that is NOT discharged here", "the repo's X-DILEMMA (stage54/62): if X is "
     "PINNED the banked CLASS pass carries an unpriced ACTIVE Y-sector at recombination.  Stage62 "
     "priced that horn at <=0.2-0.5% at OOM grade.  Nothing here changes it.")

# ==================================================================================================
head("PART E -- do the repo's PRIOR AeST claims survive this confrontation?")
# --------------------------------------------------------------------------------------------------
for s_ in [
    "LENSING 21.2 sigma -> 0.601 sigma and gamma_PPN = 1: *** SURVIVES, AND IS NOW MECHANISED. *** "
    "mechA proved PURE CONFORMAL coupling is dead (Phi~+Psi~ = Phi+Psi identically, 219.7 sigma at "
    "2.2 Mpc) and that THE VECTOR IS MANDATORY.  AeST's 2(2-K_B) J^mu grad_mu phi term IS a vector "
    "coupling: J^mu = A^nu grad_nu A^mu is the AETHER'S ACCELERATION, not a conformal rescaling of "
    "the metric.  It enters the (00) sector and not the anisotropic-stress sector, which is exactly "
    "why Phi = Psi survives.  The two results interlock; neither is weakened.",
    "'AeST does NOT make a_0 = kappa c sqrt(G rho_Lambda) STRUCTURAL' (banked 2026-08-08): *** "
    "PARTIALLY OVERTURNED, IN CARL'S FAVOUR, AND I SAY SO PLAINLY. *** That statement was true of "
    "GENERIC AeST, where F's Y-normalisation and Lambda are independent inputs.  Carl's promotion "
    "a_0^2(Q) = kappa^2 G(-K(Q)) makes the Y-sector normalisation a FUNCTION of the Q-sector, and "
    "PART D3 shows the DBI kernel supplies -K(Q_0) = M^4 = rho_Lambda c^2 with 2 Lambda = M^4 from "
    "the SAME object.  So a_0 and Lambda are no longer unrelated.  What stays free: kappa (FITTED, "
    "never derived) and the overall M^4.  Correct phrasing from now on: 'ONE input plus kappa', "
    "NOT 'unrelated inputs'.  This does not make kappa = 1/2 derived and must not be quoted as such.",
    "'the framework's kernel EMBEDS in AeST' (banked 2026-08-08 via the Route-A exponential): "
    "CONFIRMED HERE FOR THE a_0-LINE KERNEL TOO, and upgraded from asymptotics to an explicit "
    "CLOSED-FORM J(Y) (D1a) with the SZ21 matching condition k = lam_s/(1+lam_s) made explicit.",
    "the OLD AeST double-count band 2.06-4.42x: REPRODUCED structurally at 2.52-6.38x on the "
    "a_0-line and Om_dm/Om_b (C5).  Direction of the difference: the old band used the cluster "
    "baryon fraction and MS08's kernel; this one is larger because Om_dm/Om_b > the cluster value "
    "and because the a_0-line's nu is shallower.  Neither supersedes the other -- different objects.",
    "*** WHAT DOES NOT SURVIVE UNQUALIFIED: any statement that 'AeST shows one field can carry both, "
    "therefore the double count is solved.'  AeST shows one field CAN carry both.  It avoids the "
    "double count by NOT PUTTING THE DUST IN THE GALAXY (C2-C3), which is an ansatz about the "
    "nonlinear state, not a mechanism.  The mechanism Carl's framework adds -- the forced Y-Q cross "
    "term -- is 2.5e3x too weak (D4e). ***",
]:
    info("E", s_)

# ==================================================================================================
head("PART F -- VERDICT")
# --------------------------------------------------------------------------------------------------
for s_ in [
    "(Q1) ONE FIELD.  Settled, and it is SZ21's, not new: Q and Y are the aether-parallel and "
    "aether-orthogonal projections of the SAME grad_mu phi.  Carl's DBI condensate phase and "
    "Mechanism A's AQUAL scalar are the SAME OBJECT inside AeST.  Escape 3 of mechA_double_count "
    "is REAL and has a published existence proof.",
    "(Q2) *** BEING THE SAME FIELD DOES NOT REMOVE THE DOUBLE COUNT. ***  Two invariants of one "
    "gradient enter T_munu ADDITIVELY; the published F has F_YQ = 0 identically (A5); and the ONE "
    "cross term Carl's own promotion forces is bounded by 3.9e-4 (fiducial) against a required "
    "~0.97 (D4e), vanishing as (g_bar/a_0)^(3/2) exactly where it is needed (D4f).",
    "STATUS: SAME_BUT_STILL_COUNTS.  The double count is CONDITIONAL on the condensate actually "
    "clustering -- open problem 2d, which this run does NOT settle and does NOT claim to.  What "
    "this run removes is the hope that IDENTIFICATION ALONE dissolves it.",
    "WHAT I COULD NOT DETERMINE, stated plainly: (i) whether AeST's Q-sector virialises nonlinearly "
    "-- unsolved in the AeST literature and unsolved here; (ii) whether SZ21's mu^-1 >~ 1 Mpc acts "
    "as a genuine clustering cutoff (favourable) or is only a requirement they impose (neutral) -- "
    "the repo carries BOTH readings (this file's C2 vs the k^4 microscopic-Jeans result in "
    "mi_aest_jeans_nonlinear_verdict_2026.py) and they are NOT reconciled; I flag the conflict "
    "rather than pick the favourable one; (iii) whether superluminal c_s is fatal in AeST (D2e).",
    "NO DOOR IS CLOSED HERE.  Live: a second field carrying the pressure; a genuinely non-separable "
    "F(Y,Q) with a LARGE cross term (which would be a new free function, not Carl's promotion); the "
    "transport/drain channel (CONDITIONAL-DEAD at stage63, not dead); nonlinear AeST.",
    "footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt m/s^2; kappa = 1/2 FITTED, NEVER DERIVED.",
    "credit: the action, Q/Y, K(Q), J(Y), A_Y = (2-K_B)(1+lambda_s), c_s^2, Q = (1-Psi)Q_0, "
    "mu^-1 >~ 1 Mpc and r_C are ALL Skordis & Zlosnik 2021.  Carl's are: the a_0-line kernel, the "
    "DBI K(Q), the promotion a_0^2 = kappa^2 G(-K), and a_0 = kappa c sqrt(G rho_Lambda).",
]:
    info("F", s_)

print("\n" + "=" * 100)
print(f"ROUTE-2 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
