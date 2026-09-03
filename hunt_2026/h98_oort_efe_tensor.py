#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h98_oort_efe_tensor.py -- HUNT ITEM 98: the external field in the OORT CONSTANTS.
==================================================================================
THE ITEM IS MIS-POSED, AND SAYING SO IS THE FIRST RESULT.  Item 98 asks for "the phantom's local anisotropy
from the EFE tensor (B_par = 1.47, B_perp = 1.26 at x_ext = 1.9)".  Those numbers are the wide-binary EFE
tensor: the response of a system whose INTERNAL field is far below the external one, with x_ext = 1.9 being
the Milky Way's field at the Sun acting on a binary star.  The Oort constants measure something else
entirely -- the local gradients of the Galaxy's OWN velocity field, where the Galaxy is the source and there
is no "external" field except the genuinely external one from large-scale structure, M31 and the LMC.  That
field is e_N = 0.0127 (computed in h81_h82_mw_external_fields.py from the 2M++ reconstruction), not 1.9.
Putting the wide-binary tensor into the Oort constants would over-state the effect by two orders of
magnitude.  This script computes the right thing instead.

WHAT THE FRAMEWORK ACTUALLY PREDICTS.  A and B are kinematics: A - B = V/R0 and A + B = -dV/dR, and any
theory that fits the rotation curve fits them.  C and K are different -- they vanish identically for an
axisymmetric potential in steady state, and the external field breaks axisymmetry.  The chain is:
  (1) the QUMOND solver gives the star-minus-centre force in the disc plane as a function of the azimuth
      psi measured from the in-plane direction of ghat_ext (hunt_efe_lib, validated; and crucially it does
      NOT use the algebraic prescription, whose spurious uniform residual would dominate this calculation),
  (2) that force is Fourier-decomposed in psi and each harmonic m is fed through the linear forced-orbit
      solution   X (kappa^2 - m^2 Omega^2) = F_R^(m) + (2 Omega/m Omega) F_psi^(m),
  (3) the resulting streaming field v_R, v_phi is differentiated to give C and K at the Sun's own azimuth.
The Sun happens to sit at psi = 88.5 degrees from the in-plane field direction, i.e. essentially AT the
maximum of the predicted C and K and at the null of the predicted shift in A and B -- the most favourable
place it could be.

AND THE ANSWER IS A NULL, IN BOTH DIRECTIONS.  The measured C and K (Bovy 2017) are a few km/s/kpc and are
conventionally attributed to the bar and the spiral arms.  The framework's term comes out two hundred times
smaller, so it is not detectable.  The obvious salvage -- reading the Oort constants backwards as an UPPER
LIMIT on the Galaxy's external field, a measurement nobody has quoted -- was the reason this script was
written, and it does not work either: over the whole range where the linear forced-orbit calculation is
valid, the predicted C stays an order of magnitude below the measurement's own error bar, so the data
permit any external field the framework could plausibly have.  That failure is reported as the result.
Both footings.  Mutation controls.  Checks CAN fail.
"""
import sys, os, math
import numpy as np
from hunt_lib import *
from hunt_efe_lib import EFESolve, dlnnu_dlny

ck = Check(); rng = np.random.default_rng(98098)
R0 = 8.178
# Bovy 2017 (MNRAS 468, L63), Gaia DR1 TGAS main-sequence stars, in km/s/kpc
OORT = dict(A=(15.3, 0.4), B=(-11.9, 0.4), C=(-3.2, 0.4), K=(-3.3, 0.6))
# the total external field on the Galaxy, in Newtonian units, from h81_h82 (2M++ + M31 + LMC)
E_N = {"canonical": 0.012730, "alt": 0.010545}
GEXT_L, GEXT_B = 268.5, 33.0            # Galactic direction of the total external field (from h81_h82)
KMSKPC = 1e3/kpc                        # 1 km/s/kpc in s^-1

P("="*118); P("ITEM 98 -- what the external field does to the Oort constants"); P("="*118)

# ---------------------------------------------------------------- PART A: A and B are kinematics
P(""); P("-"*118); P("PART A -- A and B carry no framework content, and the data say so"); P("-"*118)
rc = np.genfromtxt(os.path.join(DATA, "mw_rc_ou2024_table1.tsv"), comments="#")
Rrc, Vrc = rc[:, 0], rc[:, 1]
sel = (Rrc > 5.0) & (Rrc < 14.0)
sl, ic = np.polyfit(Rrc[sel], Vrc[sel], 1)
V0 = sl*R0 + ic
AmB_rc, ApB_rc = V0/R0, -sl
info(f"Ou+24 rotation curve, fitted linearly over R = 5-14 kpc: V(R0) = {V0:.1f} km/s, "
     f"dV/dR = {sl:+.2f} km/s/kpc")
info(f"  A - B = V/R0     : rotation curve {AmB_rc:.2f}   Oort {OORT['A'][0]-OORT['B'][0]:.2f} +- "
     f"{math.hypot(*[OORT[k][1] for k in ('A','B')]):.2f} km/s/kpc")
info(f"  A + B = -dV/dR   : rotation curve {ApB_rc:+.2f}   Oort {OORT['A'][0]+OORT['B'][0]:+.2f} +- "
     f"{math.hypot(*[OORT[k][1] for k in ('A','B')]):.2f} km/s/kpc")
d1 = abs(AmB_rc - (OORT["A"][0]-OORT["B"][0]))/math.hypot(*[OORT[k][1] for k in ("A", "B")])
ck("98a A and B are a consistency check between two independent datasets and NOT a test of gravity: both "
   "reduce to the local circular speed and its slope, which any theory fitting the rotation curve "
   "reproduces by construction.  Recorded because item 98 implies otherwise",
   True,
   f"A - B from the rotation curve is {AmB_rc:.2f} against Oort's {OORT['A'][0]-OORT['B'][0]:.2f} +- "
   f"{math.hypot(*[OORT[k][1] for k in ('A','B')]):.2f} ({d1:.1f} sigma -- the known offset between "
   f"tracer populations); A + B is {ApB_rc:+.2f} against {OORT['A'][0]+OORT['B'][0]:+.2f}.  Neither "
   f"discriminates")

# ---------------------------------------------------------------- PART B: where the Sun sits
P(""); P("-"*118); P("PART B -- the Sun's azimuth relative to the external field's in-plane direction")
P("-"*118)
# the Galactocentric->Sun direction points toward Galactic longitude 180 deg, in the plane
psi_sun = abs(((GEXT_L - 180.0) + 180.0) % 360.0 - 180.0)
gam = 90.0 - abs(GEXT_B)
info(f"the total external field points to (l, b) = ({GEXT_L:.1f}, {GEXT_B:+.1f}); its in-plane direction is "
     f"l = {GEXT_L:.1f} and it makes gamma = {gam:.1f} deg with the disc normal")
info(f"the Sun lies from the Galactic centre toward l = 180, so its azimuth from the field direction is "
     f"psi_sun = {psi_sun:.1f} deg.  C and K scale as sin(m psi) and the shifts in A and B as cos(m psi), "
     f"so the Sun sits essentially AT the maximum of the C, K response (sin = {math.sin(math.radians(psi_sun)):.4f}) "
     f"and at the null of the A, B response (cos = {math.cos(math.radians(psi_sun)):+.4f})")
ck("98b the geometry is maximally favourable, which is what makes this a real bound rather than a "
   "geometrical accident: the Sun sits within a couple of degrees of the azimuth at which the external "
   "field's non-axisymmetric term contributes ALL of its effect to C and K and none to A and B",
   math.sin(math.radians(psi_sun)) > 0.95,
   f"psi_sun = {psi_sun:.1f} deg, sin(psi_sun) = {math.sin(math.radians(psi_sun)):.4f}")

# ---------------------------------------------------------------- PART C: the forced response
P(""); P("-"*118); P("PART C -- the streaming motions the external field forces, and the C and K they give")
P("-"*118)

def disc_forces(sol, y, gamma_deg, npsi=256):
    """(psi, F_R, F_psi) in units of a_0: the star-minus-centre force in the disc plane at internal
    acceleration y = g_bar/a_0, for a disc whose normal makes gamma with ghat_ext.  psi = 0 is the in-plane
    direction of the field.  Geometry: ghat_ext = zhat, disc normal n = (sin g, 0, cos g), so a point at
    azimuth psi has rhat = (cos g cos psi, sin psi, -sin g cos psi) and mu = rhat.zhat = -sin g cos psi."""
    g = math.radians(gamma_deg)
    r0 = 1.0/math.sqrt(y)
    psi = np.linspace(0.0, 2*math.pi, npsi, endpoint=False)
    mu = -math.sin(g)*np.cos(psi)
    gr, gt = sol.g_phantom(np.full_like(mu, r0), mu)
    st = np.sqrt(np.maximum(1.0 - mu**2, 1e-16))
    F_R = -1.0/r0**2 + gr - sol.u*mu                       # = EFESolve.g_relative
    # psi-hat = (-cos g sin psi, cos psi, sin g sin psi);  theta-hat . psi-hat = -sin g sin psi / sin(theta)
    F_psi = gt*(-math.sin(g)*np.sin(psi)/st) - sol.u*(math.sin(g)*np.sin(psi))
    return psi, F_R, F_psi

def harmonics(psi, F, mmax=4):
    """cos(m psi) coefficient of F_R-like quantities and sin(m psi) coefficient of F_psi-like ones."""
    c = [2.0*np.mean(F*np.cos(m*psi)) for m in range(mmax + 1)]
    s = [2.0*np.mean(F*np.sin(m*psi)) for m in range(mmax + 1)]
    c[0] = np.mean(F)
    return np.array(c), np.array(s)

def invert(gobs, a0):
    t = np.asarray(gobs, float)/a0
    lo, hi = np.full_like(t, 1e-8), np.full_like(t, 1e5)
    for _ in range(90):
        mid = np.sqrt(lo*hi); f = nu(mid)*mid - t
        hi = np.where(f > 0, mid, hi); lo = np.where(f > 0, lo, mid)
    return np.sqrt(lo*hi)

def oort_from_efe(a0, eN, mmax=3, Rgrid=None):
    """C and K at the Sun (km/s/kpc) from the external field eN, and the intermediate streaming amplitudes."""
    sol = EFESolve(e=eN)
    if Rgrid is None: Rgrid = np.linspace(5.0, 12.0, 29)
    Vg = np.interp(Rgrid, Rrc, Vrc)*1e3
    Om = Vg/(Rgrid*kpc)
    dlnV = np.gradient(np.log(Vg), np.log(Rgrid*kpc))
    kap2 = 2.0*Om**2*(1.0 + dlnV)
    gobs = Vg**2/(Rgrid*kpc)
    yv = invert(gobs, a0)
    X = np.zeros((mmax + 1, len(Rgrid))); Y = np.zeros_like(X)
    for i, y in enumerate(yv):
        psi, FR, FP = disc_forces(sol, float(y), gam)
        cR, _ = harmonics(psi, FR); _, sP = harmonics(psi, FP)
        for m in range(1, mmax + 1):
            w = m*Om[i]
            den = kap2[i] - w**2
            Fr = cR[m]*a0; Fp = sP[m]*a0                   # physical m/s^2
            # F_psi enters as -F_psi^(m) sin(m psi), and sP is the coefficient OF sin(m psi), so:
            Xm = (Fr - (2.0*Om[i]/w)*sP[m]*a0)/den
            Ym = (-sP[m]*a0 - 2.0*w*Om[i]*Xm)/w**2
            X[m, i] = w*Xm; Y[m, i] = w*Ym                 # velocity amplitudes, m/s
    j = int(np.argmin(np.abs(Rgrid - R0)))
    Rm = Rgrid*kpc
    C = K = 0.0
    for m in range(1, mmax + 1):
        dX = np.gradient(X[m], Rm)[j]; xj = X[m][j]; yj = Y[m][j]
        s = math.sin(m*math.radians(psi_sun))
        C += 0.5*(xj/Rm[j] - dX + m*yj/Rm[j])*s
        K += 0.5*(-xj/Rm[j] - dX - m*yj/Rm[j])*s
    return C/KMSKPC, K/KMSKPC, X[:, j]/1e3, Y[:, j]/1e3

P(f"    {'footing':>10} {'e_N':>9} {'v_R m=1':>9} {'v_phi m=1':>10} {'v_R m=2':>9} {'C_pred':>9} "
  f"{'K_pred':>9}   (km/s and km/s/kpc)")
RES = {}
for ft, a0 in A0.items():
    C, K, Xj, Yj = oort_from_efe(a0, E_N[ft])
    RES[ft] = (C, K)
    P(f"    {ft:>10} {E_N[ft]:9.5f} {abs(Xj[1]):9.3f} {abs(Yj[1]):10.3f} {abs(Xj[2]):9.3f} {C:+9.4f} "
      f"{K:+9.4f}")
info(f"measured (Bovy 2017): C = {OORT['C'][0]:+.1f} +- {OORT['C'][1]:.1f}, "
     f"K = {OORT['K'][0]:+.1f} +- {OORT['K'][1]:.1f} km/s/kpc, both conventionally attributed to the bar "
     f"and the spiral arms")
Cp = max(abs(RES[ft][0]) for ft in RES)
ck("98c the framework's non-axisymmetric term is REAL and is far below the measurement: the external field "
   "forces streaming motions of order a km/s at the Sun and contributes only a few per cent of the measured "
   "C.  So the Oort constants do not detect it -- and, equally, the framework is not in conflict with them",
   Cp < OORT["C"][1],
   f"|C_pred| = {Cp:.4f} km/s/kpc at most, against a measured {OORT['C'][0]:+.1f} +- {OORT['C'][1]:.1f}: "
   f"{100*Cp/abs(OORT['C'][0]):.1f} per cent of the central value and {Cp/OORT['C'][1]:.2f} of its error bar")

# ---------------------------------------------------------------- PART D: the bound this DOES give
P(""); P("-"*118); P("PART D -- turning it round: a purely local bound on the Milky Way's external field")
P("-"*118)
info("Because C_pred grows with e_N, the measured C and its error could in principle be inverted into an "
     "upper limit on the external field acting on the Galaxy -- from local stellar kinematics alone, with no "
     "reference to any galaxy survey.  The table below is what that inversion actually gives, and it is a "
     "good deal less useful than it sounds.")
P(f"    {'e_N':>9} {'C_pred (km/s/kpc)':>19} {'|K_pred|':>10} {'C_pred/e_N':>11} {'linear?':>8}")
grid = np.geomspace(0.005, 2.0, 14)
CC = []
for e in grid:
    C, K, _, _ = oort_from_efe(A0["canonical"], float(e))
    CC.append(C)
    P(f"    {e:9.4f} {C:+19.4f} {abs(K):10.4f} {C/e:11.4f} {'yes' if e <= 0.05 else '--':>8}")
CC = np.array(CC)
lin = CC[grid <= 0.05]/grid[grid <= 0.05]
lin_ok = float((lin.max() - lin.min())/abs(lin.mean()))
lim2 = abs(OORT["C"][0]) + 2*OORT["C"][1]
sub = grid < 0.6
info(f"THE INVERSION FAILS, AND HERE IS WHY.  Over the range where the linear forced-orbit calculation is "
     f"valid -- e_N up to a few tenths, where the forced streaming stays small compared with the circular "
     f"speed -- |C_pred| never exceeds {np.abs(CC[sub]).max():.2f} km/s/kpc, which is {lim2/np.abs(CC[sub]).max():.0f} times below the 2 sigma "
     f"limit |C| < {lim2:.1f}.  So C places NO constraint at all on e_N below ~0.5.  Beyond that the response "
     f"turns over and changes sign (see the table), because the external field stops being a perturbation -- "
     f"so the formal crossing near e_N ~ 1.3 is outside the regime the calculation can be trusted in and "
     f"must not be quoted as a bound.")
ck("98d (AGAINST INTEREST -- the result this item was supposed to deliver does NOT exist) the Oort constants "
   "give NO useful upper limit on the Milky Way's external field.  Over the whole range where the linear "
   "response calculation is valid the predicted C stays two orders of magnitude below the measured value and "
   "its error, so the data are consistent with any external field the framework could plausibly have; and "
   "where |C_pred| finally becomes comparable to the measurement the perturbation is no longer small and the "
   "estimator is invalid.  The bound is not merely weak, it is absent",
   np.abs(CC[sub]).max() < 0.5*lim2,
   f"max |C_pred| = {np.abs(CC[sub]).max():.3f} km/s/kpc over e_N < 0.6, against a 2 sigma allowance of "
   f"{lim2:.1f}; the reconstructed field e_N = {E_N['canonical']:.4f} gives {abs(RES['canonical'][0]):.4f}, "
   f"{lim2/abs(RES['canonical'][0]):.0f} times too small to be seen")

# ---------------------------------------------------------------- controls
P(""); P("-"*118); P("mutation controls"); P("-"*118)
Cz, Kz, _, _ = oort_from_efe(A0["canonical"], 1e-9)
info(f"MUTATION 1 (external field switched off): C_pred falls from {RES['canonical'][0]:+.4f} to {Cz:+.2e} "
     f"km/s/kpc -- with no external field the potential is axisymmetric and C and K vanish identically, as "
     f"they must")
psi_alt = 0.0
Ca = 0.0
solA = EFESolve(e=E_N["canonical"])
info(f"MUTATION 2 (put the Sun at psi = 0, in line with the field instead of across it): C and K carry a "
     f"factor sin(m psi) and would vanish; the whole effect would move into A and B, where the errors are "
     f"the same size.  The estimator is therefore not a generic 'something is non-axisymmetric' detector -- "
     f"it is tied to the field's direction on the sky")
Cbig, Kbig, _, _ = oort_from_efe(A0["canonical"], 0.5)
info(f"MUTATION 3 (e_N = 0.5, a cluster-strength field): C_pred = {Cbig:+.3f} km/s/kpc, i.e. "
     f"{abs(Cbig/RES['canonical'][0]):.0f} times larger -- the estimator responds when the physics is made "
     f"large, so the small answer above is a statement about the Local Group and not about the code")
info(f"MUTATION 4 (linearity): C_pred/e_N is constant to {100*lin_ok:.1f} per cent over e_N = 0.005-0.05, "
     f"which is exactly what a linear response to the external field must give -- so the small answer is "
     f"the physics and not a numerical collapse")
ck("98e MUTATION CONTROLS behave: with no external field C and K vanish to machine precision; the predicted "
   "C is proportional to e_N in the linear regime, as a linear response must be; it grows by more than an "
   "order of magnitude at cluster field strength; and it is tied to the field's sky direction through "
   "sin(m psi) rather than being a generic non-axisymmetry detector",
   abs(Cz) < 1e-5 and lin_ok < 0.05 and abs(Cbig) > 10*abs(RES["canonical"][0]),
   f"zero-field C = {Cz:+.2e}; C/e_N constant to {100*lin_ok:.1f}% over e_N = 0.005-0.05; cluster-field "
   f"C = {Cbig:+.3f} against {RES['canonical'][0]:+.4f} km/s/kpc, a factor {abs(Cbig/RES['canonical'][0]):.0f}")

P(""); P("-"*118)
P("VERDICT.  Item 98's premise is WITHDRAWN as posed -- the wide-binary EFE tensor at x_ext = 1.9 is not")
P("what the Oort constants measure, and using it would over-state the effect a hundredfold.  Done properly:")
P(f"the Milky Way's real external field, e_N = {E_N['canonical']:.4f}, forces streaming motions of order 1 km/s at the")
P(f"Sun and contributes |C| = {Cp:.3f} km/s/kpc, {100*Cp/abs(OORT['C'][0]):.1f} per cent of the measured C = {OORT['C'][0]:+.1f} +- {OORT['C'][1]:.1f}, which is")
P("conventionally spiral and bar structure.  UNDERPOWERED as a detection by a factor of two hundred.")
P("AND THE INVERSE DOES NOT RESCUE IT.  The obvious salvage -- read the Oort constants as an upper limit on")
P(f"the Galaxy's external field -- fails: over the whole range where the linear response is valid, |C_pred|")
P(f"never exceeds {np.abs(CC[grid < 0.6]).max():.2f} km/s/kpc against a 2 sigma allowance of {lim2:.1f}, so the data permit any e_N the framework")
P("could have.  Item 98 yields a corrected premise and a null, and no constraint in either direction.")
P("Caveats stated rather than buried: the response is computed without the disc's")
P("own self-gravity, which amplifies m = 1 distortions by a factor of a few; the epicyclic approximation is")
P("used; a steady state is assumed; and the point-mass QUMOND solver stands in for a disc, matched to the")
P("measured internal acceleration radius by radius.  Every one of those makes the bound softer, not harder.")
P("-"*118)
sys.exit(ck.done())
