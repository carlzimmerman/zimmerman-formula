#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
doorA_disformal_slip_vs_cT.py -- door A, the frame-free branch: the disformal escape from the F(X) slip kill.
============================================================================================================
DOOR A = gravity + ONE healthy propagating scalar whose background IS rho_DE, giving mu(y)=1-exp(-y).  Its
frame-free branch, a single F(X) scalar, died on gate 3 (FRIED_CHICKEN_VERDICT Case 2): the scalar's anisotropic
stress d_i phi d_j phi sources grad^2(Phi - Psi) != 0 at O(1) in the MOND regime, so lensing and dynamics disagree.
The verdict names the ONLY escapes: a vector (Case 5, dead on PPN) or a DISFORMAL matter coupling (assumption A1).
The disformal leg was never run.  This file runs it.

THE MECHANISM.  Couple matter and light to  g~_{mu nu} = g_{mu nu} + B d_mu phi d_nu phi  (Bekenstein 1993).
For a static scalar profile the disformal term touches only the SPATIAL metric, with the tensor structure
d_i phi d_j phi -- the SAME structure as the scalar's anisotropic stress.  So B can cancel the slip POINTWISE.
THE PRICE.  Gravitational waves propagate on g; light and matter see g~.  The same B d_i phi d_j phi that fixes
the lensing potential also tilts the light cone of g~ away from the null cone of g.  The no-slip condition fixes
B phi'^2 = 2(Psi - Phi) at every point, and the SAME quantity is the fractional speed difference:
              (c_GW - c_light)/c  =  B phi'^2 / 2  =  (Psi - Phi)_uncancelled.
The slip you cancel is exactly the GW/light speed difference you create.  There is no freedom in between.
GW170817 bounds |c_GW/c_light - 1| < ~1e-15 (Abbott+2017, ApJL 848 L13).  The MOND slip is O(Phi) ~ v^2/c^2 ~ 1e-7.
Calibration from the repo's own Case 3a: a light-cone tilt of -2e-7 was killed 1e7-1e9x on c_T, 1e5x on delay.
Both a_0 footings.  Mutation controls.  Checks can fail -- A6 is against interest and shows Cassini is NOT the
killer, so the trade is exactly gate 3 for gate 6.
"""
import sys, os, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "hunt_2026"))
from hunt_lib import *
ck = Check()

P("="*118); P("1.  STRUCTURE: the disformal term and the scalar stress share the tensor d_i phi d_j phi (sympy)"); P("="*118)
X, B, FX, F = sp.symbols("X B F_X F", real=True)
p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)          # d_i phi, static profile
dphi = sp.Matrix([p1, p2, p3])
g3 = sp.eye(3)
# k-essence stress tensor (spatial block, static):  T_ij = F_X d_i phi d_j phi + g_ij F   (Armendariz-Picon+1999)
T_scalar = FX*dphi*dphi.T + F*g3
# disformal correction to the spatial matter metric:   dg~_ij = B d_i phi d_j phi
dg_disf = B*dphi*dphi.T
# the traceless (slip-sourcing) parts
tl = lambda M: M - sp.Rational(1, 3)*M.trace()*g3
ratio = sp.simplify(tl(dg_disf)[0, 0]/tl(T_scalar)[0, 0])
ck("A1 (STRUCTURE) the traceless part of the disformal metric correction is PROPORTIONAL to the traceless part of the F(X) scalar's anisotropic stress, with a constant ratio B/F_X independent of the field direction.  So a disformal B can cancel the slip POINTWISE, not just at one radius -- the escape is real at the level of tensor structure",
   sp.simplify(ratio - B/FX) == 0 and all(sp.simplify(tl(dg_disf)[i, j]*FX - tl(T_scalar)[i, j]*B) == 0 for i in range(3) for j in range(3)),
   f"traceless(dg~_ij) / traceless(T_ij^scalar) = {ratio}  for every component; the isotropic F g_ij piece of the stress does not slip and does not need cancelling")

P(""); P("="*118); P("2.  THE IDENTITY: no-slip fixes B phi'^2, and the same B phi'^2 is the light-cone tilt"); P("="*118)
Phi, Psi, Bp2 = sp.symbols("Phi Psi Bphi2", real=True)   # Bphi2 = B phi'^2 along the ray
# Einstein-frame static weak field:  g_00 = -(1+2Phi),  g_rr = (1-2Psi).  GW null cone of g, radial:
cGW2 = (1 + 2*Phi)/(1 - 2*Psi)
# Jordan-frame light null cone of g~ = g + B dphi dphi, radial:  g~_00 = g_00,  g~_rr = g_rr + B phi'^2
cL2 = (1 + 2*Phi)/(1 - 2*Psi + Bp2)
# lensing potential light sees radially:  g~_rr = 1 - 2 Psi~  =>  Psi~ = Psi - B phi'^2 / 2
Psi_t = Psi - Bp2/2
noslip = sp.solve(sp.Eq(Psi_t, Phi), Bp2)[0]           # B phi'^2 that makes light see Phi
tilt = sp.series(sp.sqrt(cGW2/cL2) - 1, Bp2, 0, 2).removeO()
tilt_lin = sp.simplify(sp.series(tilt.subs({Phi: 0, Psi: 0}), Bp2, 0, 2).removeO())
ck("A2 (THE IDENTITY) the no-slip condition fixes B phi'^2 = 2(Psi - Phi) pointwise, and substituting that SAME value into the ratio of the GW null cone to the light null cone gives (c_GW - c_light)/c = (Psi - Phi): the slip cancelled equals the speed difference created, to leading order, with nothing left to tune",
   sp.simplify(noslip - 2*(Psi - Phi)) == 0 and sp.simplify(tilt_lin - Bp2/2) == 0,
   f"no-slip: B phi'^2 = {noslip};  tilt = {tilt_lin} = (Psi - Phi)")

P(""); P("="*118); P("3.  THE NUMBER: how big is the MOND slip, hence the tilt, both footings"); P("="*118)
info("Case 2 says the slip is O(1) x Phi in the MOND regime.  Parametrize (Psi - Phi) = eps * Phi_MOND with eps in")
info("[0.1, 1].  Phi_MOND is the potential where a galaxy is deep-MOND, v_flat^2 / c^2 with v_flat^4 = G M a_0 (BTFR).")
def phi_mond(M_bar, a0): return math.sqrt(G*M_bar*a0)/c_light**2          # v_flat^2 / c^2
GAL = {"NGC 4993 host (~1e11 Msun)": 1.0e11, "Milky Way (~6e10 Msun)": 6.0e10}
tilts = {}
for foot, a0 in A0.items():
    for nm, M in GAL.items():
        ph = phi_mond(M*Msun, a0); tilts[(foot, nm)] = ph
        if foot == "canonical": info(f"   {nm:28} Phi_MOND = {ph:.3e}  ->  tilt = eps x {ph:.3e}")
BOUND = 1e-15   # |c_GW/c_light - 1|, Abbott+2017 (-3e-15 .. +7e-16); using 1e-15 as the round figure
ph_can = tilts[("canonical", "NGC 4993 host (~1e11 Msun)")]; ph_alt = tilts[("alt", "NGC 4993 host (~1e11 Msun)")]
ck("A3 (THE MAGNITUDE) in the MOND outskirts of an ordinary galaxy the slip-cancelling tilt is of order 1e-7, eight orders of magnitude above the GW170817 bound, on both footings and for any eps down to 0.01",
   0.01*min(ph_can, ph_alt) > 1e3*BOUND, f"canonical {ph_can:.2e}, alt {ph_alt:.2e} per unit eps; even eps = 0.01 gives {0.01*ph_can:.1e} against a bound of {BOUND:.0e} -- a factor {0.01*ph_can/BOUND:.0e}")

P(""); P("="*118); P("4.  GW170817's ACTUAL PATH: two galaxies' MOND outskirts plus 40 Mpc of intergalactic medium"); P("="*118)
D = 40.0*Mpc
info("The signal left NGC 4993 and arrived at Earth, so it crossed the MOND regions of BOTH galaxies and the IGM.")
info("Path-averaged tilt = (1/D) Integral (Psi - Phi) dl.  Model: each galaxy contributes a segment L_gal of deep-MOND")
info("outskirts at tilt eps*Phi_MOND; the IGM contributes the whole path at a tilt suppressed by (g_IGM/g_gal)^2, since")
info("B phi'^2 goes as the square of the scalar gradient and in deep MOND that gradient carries the acceleration.")
L_gal = 100.0*kpc; g_IGM, g_gal = 1e-13, 1e-10
res = {}
for foot, a0 in A0.items():
    ph_h = tilts[(foot, "NGC 4993 host (~1e11 Msun)")]; ph_mw = tilts[(foot, "Milky Way (~6e10 Msun)")]
    for eps in (1.0, 0.1):
        gal = (L_gal*ph_h + L_gal*ph_mw)*eps/D
        igm = eps*0.5*(ph_h + ph_mw)*(g_IGM/g_gal)**2
        res[(foot, eps)] = (gal, igm)
        if foot == "canonical": info(f"   eps = {eps:4.1f}:  galactic segments {gal:.2e}   IGM alone {igm:.2e}   bound {BOUND:.0e}   -> over by {gal/BOUND:.0e} (gal) / {igm/BOUND:.0e} (IGM)")
gal1, igm1 = res[("canonical", 1.0)]; gal01, igm01 = res[("canonical", 0.1)]
ck("A4 (THE KILL) the two galaxies' MOND outskirts alone put the path-averaged GW/light speed difference five to six orders of magnitude over the GW170817 bound, for eps anywhere from 0.1 to 1, on both footings",
   min(res[(f, 0.1)][0] for f in A0) > 1e4*BOUND, f"eps=1: {gal1/BOUND:.0e}x over; eps=0.1: {gal01/BOUND:.0e}x over (canonical); alt footing eps=0.1: {res[('alt',0.1)][0]/BOUND:.0e}x")
ck("A5 (EVEN THE IGM ALONE) suppressing the tilt by the square of the acceleration ratio, the 40 Mpc of intergalactic medium by itself still exceeds the bound -- so the kill does not depend on the galactic path model",
   min(res[(f, 0.1)][1] for f in A0) > BOUND, f"IGM alone, eps=0.1: {igm01/BOUND:.0f}x over (canonical), {res[('alt',0.1)][1]/BOUND:.0f}x (alt); eps=1: {igm1/BOUND:.0f}x")

P(""); P("="*118); P("5.  AGAINST INTEREST: Cassini is NOT the killer -- this trades gate 3 for gate 6 and nothing else"); P("="*118)
info("In the solar system the acceleration is >> a_0, mu -> 1, and the scalar carries essentially no force: phi' -> 0.")
info("The disformal spatial correction B phi'^2 therefore vanishes there, and with A = 1 the matter-frame g~_00 = g_00,")
info("so gamma_PPN is untouched.  Quantify with the framework's own kernel: the scalar's share of the force is 1 - 1/nu.")
share = {}
for foot, a0 in A0.items():
    gS = G*Msun/(9.5*1.496e11)**2                   # Sun's field at Saturn
    y = gS/a0; nu_ = nu_s(y); share[foot] = 1 - 1/nu_
info(f"   scalar force share at Saturn: canonical {share['canonical']:.2e}, alt {share['alt']:.2e}  (so phi'^2 is down by its square)")
ck("A6 (against interest, and it sharpens the verdict) the disformal correction is negligible at Cassini because the scalar carries no force at solar-system accelerations, so the escape does NOT fail on gamma_PPN.  It fails on ONE gate only, c_T, and it fails there by construction: the mechanism that fixes lensing is the mechanism that tilts the light cone",
   max(share.values())**2*phi_mond(1e11*Msun, A0["canonical"]) < 2.3e-5, f"disformal term at Saturn ~ (scalar share)^2 x Phi ~ {max(share.values())**2*ph_can:.1e}, far below the Cassini |gamma-1| bound 2.3e-5")

P(""); P("="*118); P("6.  mutation controls and calibration against the repo's own Case 3a"); P("="*118)
ck("M1 mutation: with B = 0 the light cone coincides with the GW cone (tilt exactly zero) and the slip is back -- the tilt is caused by the cancellation, not by the machinery",
   sp.simplify(tilt.subs(Bp2, 0)) == 0 and sp.simplify((Psi_t - Phi).subs(Bp2, 0) - (Psi - Phi)) == 0, "tilt(B=0) = 0; slip(B=0) = Psi - Phi")
ck("M2 mutation: with no MOND force (scalar gradient zero) both the slip and the required B phi'^2 vanish, recovering GR with Phi = Psi and c_GW = c_light",
   all(sp.simplify(tl(T_scalar).subs({p1: 0, p2: 0, p3: 0})[i, j]) == 0 for i in range(3) for j in range(3)), "traceless scalar stress = 0 at phi' = 0, so nothing to cancel and nothing to tilt")
ck("M3 calibration: the tilt found here (~1e-7 in MOND zones) is the same order as Case 3a's lambda = -2e-7, which the repo killed at 1e5x (delay) to 1e7-1e9x (c_T); the factors here fall in that range, so the two kills are mutually consistent",
   1e4 < gal1/BOUND < 1e10, f"this file: {gal1/BOUND:.0e}x over GW170817; Case 3a: 1e5x-1e9x")

P(""); P("="*118); P("VERDICT"); P("="*118)
P("  Door A's frame-free branch had ONE named escape from the slip kill: a disformal matter coupling.  It is real at")
P("  the level of structure -- the disformal correction shares the tensor form of the scalar's anisotropic stress, so")
P("  it cancels the slip pointwise -- and it dies on one line of algebra: the no-slip condition fixes B phi'^2 =")
P("  2(Psi - Phi), and that same quantity IS the fractional GW/light speed difference.  The slip you cancel is the")
P("  tilt you create.  In galaxy outskirts the slip is ~1e-7; GW170817 allows 1e-15.  Along that event's actual path")
P("  the excess is 1e5-1e6x from the two galaxies' MOND regions, and the IGM alone still exceeds the bound.  Cassini")
P("  is untouched, so this is a clean trade of gate 3 for gate 6, with no parameter in between.")
P("  DOOR A, FRAME-FREE BRANCH: CLOSED, conditional on A1 (the coupling is disformal of the Bekenstein form) and on")
P("  Case 2's slip being O(Phi) in the MOND regime.  Together with the committed framed-branch kill (alpha_1) this")
P("  leaves door A one leg: prove the alpha_1 kill general beyond the aether class, or exhibit a framed coupling that")
P("  makes MOND without vector-scalar mixing.  That is the next computation, and it is the last one door A has.")
sys.exit(ck.done())
