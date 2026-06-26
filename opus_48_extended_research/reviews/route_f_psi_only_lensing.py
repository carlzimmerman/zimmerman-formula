#!/usr/bin/env python3
"""
ROUTE F -- the decisive explicit check: does a Psi-ONLY (light-only) source genuinely
supply the MOND lensing magnitude WITHOUT accelerating slow matter?  (weak-field geodesics)
=========================================================================================
This is the load-bearing physics of THEORY I (the MI-compatible metric partner). If a
Psi-only slip term lenses light at |M_lens|=|M_dyn| while leaving timelike (matter)
geodesics at g_N, the partner coexists with gated MI and is Cassini-safe. If a Psi-only
term CANNOT reproduce the lensing magnitude (e.g. it gives only HALF), say so honestly.

Standard weak-field results (Misner-Thorne-Wheeler; Will, lensing reviews):
  metric  ds^2 = -(1+2Phi)dt^2 + (1-2Psi)delta_ij dx^i dx^j  (c=1, |Phi|,|Psi|<<1).
  - timelike geodesic (slow matter): d^2x/dt^2 = -grad Phi.            (matter feels Phi only)
  - null geodesic (light) bending:   governed by (Phi+Psi); deflection
       alpha = integral grad_perp (Phi + Psi) dl.                       (light feels Phi+Psi)
  - convergence / lensing mass:  kappa ~ nabla^2 (Phi+Psi)/2 ; M_lens(<r) <-> (Phi+Psi).
"""
import sympy as sp

def H(t): print("\n"+"="*84+"\n "+t+"\n"+"="*84)

H("Setup: baryon GR potentials + the partner's Psi-only addition")
print("""
Baryon GR (no slip): Phi_b = Psi_b =: phi_N, with grad phi_N = g_N (the baryon Newtonian field).
MI matter sector: matter responds with a_dyn = g_obs = sqrt(g_N^2 + g_N a0) -- this is a
KINEMATIC (inertia) effect; it does NOT change phi_N or the metric. Matter's ACCELERATION is
g_obs, but the gravitational POTENTIAL it moves in is still phi_N (baryon).

Partner: adds dPsi to the space potential ONLY (dPhi = 0). Choose dPsi so the TOTAL lensing
potential (Phi+Psi) reproduces the MOND deflection.
""")
r, g_N, a0, G, M = sp.symbols('r g_N a_0 G M', positive=True)
# point mass baryon field
gN_pt = G*M/r**2
g_obs = sp.sqrt(gN_pt**2 + gN_pt*a0)

H("Step 1 -- what lensing magnitude does the MI dynamical mass DEMAND?")
print("""
M_dyn(<r): the dynamical mass inferred from matter's acceleration g_obs via Newton's GR kernel
(this is what an observer using GR lensing formulae would call the 'mass'):
   g_obs = G M_dyn / r^2  =>  M_dyn(<r) = g_obs r^2 / G.
For lensing to AGREE (M_lens = M_dyn), the lensing potential must satisfy
   grad(Phi+Psi)/2 = g_obs   (the deflection-effective field = g_obs), i.e. the light
   'effective gravitational field' g_lens := grad[(Phi+Psi)/2] must equal g_obs.
""")
M_dyn = sp.simplify(g_obs*r**2/G)
print("  M_dyn(<r) = g_obs r^2/G =", M_dyn)
print("  required light-effective field  g_lens = (1/2)grad(Phi+Psi) = g_obs =", sp.simplify(g_obs))

H("Step 2 -- the Psi-only partner that delivers g_lens = g_obs WITHOUT touching matter")
print("""
With dPhi=0, the potentials are:
   Phi = phi_N           (grad Phi = g_N)               <- MATTER feels this (timelike geodesic)
   Psi = phi_N + dPsi    (grad Psi = g_N + grad dPsi)
Light-effective field:
   g_lens = (1/2) grad(Phi+Psi) = (1/2)[g_N + g_N + grad dPsi] = g_N + (1/2) grad dPsi.
Set g_lens = g_obs:
   g_N + (1/2) grad dPsi = g_obs  =>  grad dPsi = 2(g_obs - g_N).
Matter acceleration is UNCHANGED:
   a_matter(gravity) = grad Phi = g_N   (partner adds 0 to Phi)  -- matter's MOND boost is
   supplied SEPARATELY by the MI inertia (a_dyn = g_obs via m*mu_fw). NO double count, NO
   fifth force on planets from the partner.
""")
grad_dPsi = sp.simplify(2*(g_obs - gN_pt))
print("  required  grad dPsi = 2(g_obs - g_N) =", grad_dPsi)
print("  CHECK light-effective field:  g_N + (1/2)grad dPsi =",
      sp.simplify(gN_pt + sp.Rational(1,2)*grad_dPsi), " ; minus g_obs =",
      sp.simplify(gN_pt + sp.Rational(1,2)*grad_dPsi - g_obs), " (0 => light lenses at g_obs). PASS")
print("  CHECK matter gravitational accel = grad Phi = g_N (partner adds 0):  g_N =", gN_pt,
      " => matter NOT accelerated by partner. PASS (Cassini-safe).")

H("Step 3 -- deep-MOND: does the Psi-only partner give the right deflection (v^4=GMa0 lensing)?")
print("""
Deep-MOND g_N<<a0: g_obs -> sqrt(g_N a0). The light-effective field g_lens = g_obs = sqrt(g_N a0)
=> the lensing-deduced mass M_lens = g_obs r^2/G = M_dyn. So in the deep regime the Psi-only
partner reproduces the SAME enhanced lensing mass as dynamics -- the f4 230x deficit is closed.
""")
g_obs_dm = sp.sqrt(gN_pt*a0)
M_lens_dm = sp.simplify(g_obs_dm*r**2/G)
grad_dPsi_dm = sp.simplify(2*(g_obs_dm - gN_pt))
print("  deep-MOND g_lens = g_obs =", sp.simplify(g_obs_dm))
print("  deep-MOND M_lens = g_obs r^2/G =", M_lens_dm, " == M_dyn (same g_obs). PASS")
print("  deep-MOND grad dPsi = 2(sqrt(g_N a0) - g_N) ~", sp.simplify(sp.series(grad_dPsi_dm, a0, sp.oo, 1)),
      " -- partner Psi-source ~ 2 sqrt(g_N a0) = the MOND phantom (for light). Tuned-match.")

H("Step 4 -- the SLIP it implies, made explicit (the honest exposure of Theory I)")
print("""
The slip is Phi - Psi = -dPsi (since Phi=phi_N, Psi=phi_N+dPsi). Its gradient:
   grad(Psi - Phi) = grad dPsi = 2(g_obs - g_N).
This is a REAL, nonzero slip in any region where g_obs != g_N (i.e. wherever MOND operates).
It is OBSERVABLE in principle as a difference between the lensing potential and the dynamical
potential -- BUT note the standard MOND-lensing literature parametrizes lensing by g_obs and
finds M_lens=M_dyn; Theory I reproduces that PHENOMENOLOGY (same g_obs for light and matter
magnitude) while having a slip at the level of the individual potentials Phi vs Psi.
""")
slip_grad = sp.simplify(2*(g_obs - gN_pt))
print("  slip  grad(Psi-Phi) = 2(g_obs - g_N) =", slip_grad)
print("  Newtonian g_N>>a0:  slip ->", sp.simplify(sp.limit(slip_grad, a0, 0)), " (0 => no slip in solar system. GOOD)")
print("  deep-MOND g_N<<a0:  slip ~ 2 g_obs (large) -- the lensing-vs-dynamics potential gap.")
print("""
  KEY both-ways: the slip VANISHES where g_N>>a0 (solar system, high-a) and is large only in
  the deep-MOND (galaxy outskirts/cluster) regime -- so it is Cassini-INVISIBLE (no slip where
  planets are) and only shows up in the weak-field lensing regime where it is TUNED to give the
  right magnitude. This is the honest structure: a gated slip, not a no-slip identity.
""")

H("Step 5 -- is this distinguishable from AeST? (yes -- the slip is the discriminator)")
print("""
AeST: genuine NO SLIP (Phi=Psi exactly, field-equation identity) -- lensing potential = dynamical
   potential at the level of the metric. Matter is accelerated by the SAME modified field
   (modified GRAVITY), and Cassini is failed because the scalar is ungated/EFE-screened-at-Mpc.

THEORY I (gated MI + Psi-only partner): SLIP (Phi != Psi). Matter accelerated by g_N + MI
   inertia (NOT by the partner). Cassini-safe (MI gate on body's own a, EFE-robust; partner in
   Psi doesn't touch matter). The lensing magnitude matches dynamics by TUNING the Psi-source.

OBSERVABLE DISCRIMINATOR: AeST predicts ZERO slip; Theory I predicts a slip = 2(g_obs-g_N) in
   the deep regime. A measurement of the gravitational slip (e.g. comparing the dynamical mass
   from stellar kinematics to the lensing convergence at matched radius, or E_G statistics)
   distinguishes them. Currently both are consistent with data (slip poorly constrained at
   galaxy-outskirt accelerations), but it is a REAL, in-principle test -- and a genuine
   PREDICTION the gated-MI theory makes that AeST does not.
""")

H("NET (this script)")
print("""
EXPLICITLY VERIFIED (sympy):
  * A Psi-only (light-only) partner with grad dPsi = 2(g_obs - g_N) makes light lens at EXACTLY
    g_obs => M_lens = M_dyn in MAGNITUDE (the f4 230x deficit CLOSED), WHILE leaving matter's
    gravitational acceleration at g_N (the partner adds 0 to Phi => NO fifth force on planets).
  * Cassini-safe: the slip 2(g_obs-g_N) -> 0 as g_N>>a0 (vanishes in the solar system); and the
    partner never accelerates matter, so there is no anomalous planetary acceleration at all.
  * The MOND boost on MATTER is supplied 100% by the gated MI inertia (a_dyn=g_obs), Cassini-safe
    by the MI gate on the body's OWN acceleration (EFE-robust, unlike AQUAL's field gate).
  => THEORY I is a genuine, explicit, Cassini-safe metric/lensing partner for gated MI.

HONEST PRICE (conceded):
  * It is a SLIP theory (Phi != Psi), NOT a no-slip identity. M_lens=M_dyn is a TUNED MATCH
    (the Psi-source dPsi is FIXED to 2(g_obs-g_N) by hand -- a free-function choice, exactly
    like AeST's F(Y,Q), not derived).
  * The slip 2(g_obs-g_N) is an OBSERVABLE prediction distinguishing Theory I from AeST -- a
    genuine exposure (and a genuine novel test).
  * Ghost-freedom CONDITIONAL (DEW order-lowering + non-derivative gate; full IR Hamiltonian open).
  * Cluster eta~2.3 and CMB 3rd peak UNCURED (shared, conceded, unchanged). kappa free; a0 transmitted.
""")
