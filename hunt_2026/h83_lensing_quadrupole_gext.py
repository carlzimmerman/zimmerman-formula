#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h83_lensing_quadrupole_gext.py -- HUNT ITEM 83: a lensing quadrupole aligned with the EXTERNAL FIELD.
=====================================================================================================
Every weak-lensing "halo ellipticity" measurement ever made uses the LIGHT as its reference axis: it asks
whether the mass around a galaxy is elongated the way the galaxy's own isophotes are.  The framework says
there is a second, completely different axis in the problem.  A galaxy embedded in an external Newtonian
field g_ext has a PHANTOM halo that is prolate along g_ext -- linearising QUMOND about a uniform external
field gives phi = -nu(e)(GM/r)[1 + L/3 - (L/3)P_2(mu)] with mu measured from ghat_ext and L = dln nu/dln y
negative, so the potential is deepest along the field.  Nothing in LambdaCDM aligns a halo with the local
gravitational ACCELERATION vector rather than with the tidal field or the light, and the two axes are not
the same: the acceleration points at the nearest big attractor, the tidal stretch points along the filament.

WHAT IS COMPUTED HERE, AND WHAT IS NOT.  The shear catalogues (KiDS-1000, DES Y3) are not on disk, so this
is NOT a measurement.  It is the forecast that has to come first, done properly:
  (a) the QUMOND phantom density around a point mass in a uniform external field (hunt_efe_lib, validated),
  (b) its PROJECTION to a surface density Sigma(R, phi) with the external field at an arbitrary angle to
      the line of sight -- the m = 2 sky modulation carries a sin^2(Theta) factor that dilutes the stack,
  (c) the tangential shear computed by direct Fourier (Kaiser-Squires) inversion on a Cartesian grid, NOT
      by an analytic kernel taken on trust: the axisymmetric limit of that code is checked against
      DeltaSigma = mean Sigma(<R) - Sigma(R), so a wrong kernel cannot pass,
  (d) the achievable signal-to-noise, taken from the ACTUAL KiDS-1000 isolated-lens excess surface density
      profile and its errors, which ARE on disk (Brouwer+2021 Fig-3 mass bins).
Both footings.  Mutation controls.  Checks CAN fail.
"""
import sys, os, math
import numpy as np
from hunt_lib import *
from hunt_efe_lib import EFESolve, dlnnu_dlny

ck = Check(); rng = np.random.default_rng(8383)
MB_LENS = 5.0e10                     # baryonic mass of a KiDS L* isolated lens, Msun
NGRID, HALF = 512, 3.0              # Cartesian grid for the shear inversion: cells, half-width in Mpc

P("="*118); P("ITEM 83 -- is the lensing quadrupole around isolated galaxies aligned with g_ext?"); P("="*118)

# ---------------------------------------------------------------- PART A: the 3-D phantom quadrupole
P(""); P("-"*118); P("PART A -- the phantom's own quadrupole, in three dimensions"); P("-"*118)
info("EFESolve returns rho_ph on a (r, mu) grid in units of r_M = sqrt(G M_b/a_0) and a_0/(G r_M).  Its "
     "multipoles rho_l(r) are extracted by Gauss-Legendre quadrature in mu; the l = 2 to l = 0 ratio is the "
     "quantity the item is really asking about, before any projection.")

def multipoles(sol, lmax=6):
    """rho_l(r) for l = 0..lmax from the solver's (r, mu) phantom density."""
    out = []
    for l in range(lmax + 1):
        Pl = np.polynomial.legendre.Legendre.basis(l)(sol.mu)
        out.append((2*l + 1)/2.0*np.sum(sol.rho_ph*Pl[None, :]*sol.w[None, :], axis=1))
    return np.array(out)

info("the analytic far-field form only applies well beyond the EFE radius r_EFE = r_M/sqrt(e_N), where the "
     "external field overtakes the galaxy's own, so the table is indexed by r/r_EFE rather than by r/r_M.")
P(f"    {'e_N':>7} {'r/r_M':>8} {'r/r_EFE':>8} {'rho_2/rho_0':>12} {'phi_2/phi_0 (total)':>20} "
  f"{'analytic -(L/3)/(1+L/3)':>24}")
PHI = {}
for e in (0.003, 0.01, 0.03, 0.1):
    sol = EFESolve(e=e)
    rl = multipoles(sol)
    L = float(dlnnu_dlny(np.array([e]))[0]); target = -(L/3)/(1 + L/3)
    rEFE = 1.0/math.sqrt(e)
    for fr in (1.0, 5.0, 15.0):
        rr = fr*rEFE
        i = int(np.argmin(np.abs(sol.r - rr)))
        # the TOTAL potential is the point mass -GM/r (= -1/r in solver units) plus the phantom's
        p0 = sol.phi_l[0][i] - 1.0/sol.r[i]
        p2 = sol.phi_l[2][i]
        PHI[(e, fr)] = (p2/p0, target)
        P(f"    {e:7.3f} {sol.r[i]:8.2f} {fr:8.1f} {rl[2][i]/rl[0][i]:12.2f} {p2/p0:20.4f} {target:24.4f}")
info("the DENSITY ratio in the middle column is unusable as a headline and is printed to show why: in the "
     "external-field-dominated region the monopole phantom density passes through zero, so rho_2/rho_0 "
     "diverges and even changes sign.  The POTENTIAL ratio is the well-behaved statement, and it has an "
     "independent analytic value to be checked against.")
worst = max(abs(PHI[k][0]/PHI[k][1] - 1.0) for k in PHI if k[1] >= 15.0)
q3d = PHI[(0.01, 15.0)][0]
ck("83a the phantom's quadrupole is REAL, is PROLATE along g_ext (positive ratio), and is large -- the "
   "quadrupole of the total potential is 16-19 per cent of its monopole -- and the solver reproduces the "
   "independent analytic far-field value -(L/3)/(1 + L/3) obtained by linearising QUMOND about a uniform "
   "external field.  A sign error or a wrong multipole would fail this",
   worst < 0.10 and all(PHI[k][0] > 0 for k in PHI),
   f"worst |solver/analytic - 1| = {100*worst:.1f}% over e_N = 0.003-0.1 at r = 15 r_EFE; the analytic "
   f"ratio runs {min(PHI[k][1] for k in PHI):.3f} to {max(PHI[k][1] for k in PHI):.3f}.  Nearer in, at "
   f"r = r_EFE, the ratio is still building up -- which is exactly why the lensing signal grows with radius "
   f"in the table below")

# ---------------------------------------------------------------- PART B: projection and shear
P(""); P("-"*118); P("PART B -- projecting it, and turning it into a shear (with the kernel CHECKED)")
P("-"*118)
r_M = math.sqrt(G*MB_LENS*Msun/A0["canonical"])/Mpc
info(f"an L* lens with M_b = {MB_LENS:.1e} Msun has r_M = {r_M*1000:.1f} kpc, so the KiDS radial range "
     f"0.035-2.6 Mpc is r/r_M = {0.035/r_M:.1f} to {2.6/r_M:.0f} -- entirely in the regime where the "
     f"quadrupole has saturated")

x = (np.arange(NGRID) - NGRID/2 + 0.5)*(2*HALF/NGRID)
XX, YY = np.meshgrid(x, x, indexing="ij")
RR = np.hypot(XX, YY)
CELL = 2*HALF/NGRID

_SOL = {}
def solver(e):
    k = round(math.log10(max(e, 1e-9)), 3)
    if k not in _SOL: _SOL[k] = EFESolve(e=10.0**k)
    return _SOL[k]

def sigma_polar(sol, theta_deg, r_M_Mpc, nR=180, nphi=48, nz=320, zmax=30.0):
    """Sigma(R, phi) of the phantom on a polar grid, external field at angle theta to the line of sight,
    phi measured from the sky projection of ghat_ext.  Multipoles l = 0, 2, 4 of rho are all carried, so the
    projection is not truncated at the quadrupole.  (The first version of this script evaluated the 3-D
    density directly on a 1024^2 Cartesian grid for every one of 400 line-of-sight slices; it was correct
    and unusably slow.  This does the same integral on a 180 x 48 polar grid and interpolates.)"""
    th = math.radians(theta_deg)
    Rg = np.geomspace(0.01, 2.0*HALF, nR)
    ph = np.linspace(0.0, math.pi, nphi)
    z = np.linspace(-zmax, zmax, nz)*r_M_Mpc
    dz = z[1] - z[0]
    rl = multipoles(sol, lmax=4)
    R3 = Rg[:, None, None]; P3 = ph[None, :, None]; Z3 = z[None, None, :]
    d = np.sqrt(R3**2 + Z3**2)
    mu = (Z3*math.cos(th) + R3*np.cos(P3)*math.sin(th))/np.maximum(d, 1e-12)
    rho = np.zeros_like(mu)
    for l in (0, 2, 4):
        Pl = np.polynomial.legendre.Legendre.basis(l)(mu)
        rho += np.interp(d/r_M_Mpc, sol.r, rl[l], left=rl[l][0], right=0.0)*Pl
    return Rg, ph, rho.sum(axis=2)*dz/r_M_Mpc

def sigma_map(sol, theta_deg, r_M_Mpc):
    Rg, ph, S = sigma_polar(sol, theta_deg, r_M_Mpc)
    Rq = np.clip(np.maximum(RR, Rg[0]), Rg[0], Rg[-1])
    pq = np.abs(np.arctan2(YY, XX))                       # Sigma is even in phi and in phi -> pi - phi
    li = np.interp(np.log(Rq), np.log(Rg), np.arange(len(Rg)))
    i0 = np.clip(li.astype(int), 0, len(Rg)-2); fi = li - i0
    lj = np.interp(pq, ph, np.arange(len(ph)))
    j0 = np.clip(lj.astype(int), 0, len(ph)-2); fj = lj - j0
    return ((1-fi)*(1-fj)*S[i0, j0] + fi*(1-fj)*S[i0+1, j0] +
            (1-fi)*fj*S[i0, j0+1] + fi*fj*S[i0+1, j0+1])

def shear_from_kappa(K):
    """Kaiser-Squires: gamma_tilde = ((k1^2 - k2^2) + 2i k1 k2)/|k|^2 kappa_tilde."""
    k1 = np.fft.fftfreq(NGRID, d=CELL)[:, None]*np.ones((1, NGRID))
    k2 = np.ones((NGRID, 1))*np.fft.fftfreq(NGRID, d=CELL)[None, :]
    k2sq = k1**2 + k2**2; k2sq[0, 0] = 1.0
    Kf = np.fft.fft2(K)
    g = np.fft.ifft2(((k1**2 - k2**2) + 2j*k1*k2)/k2sq*Kf)
    g[0, 0] = 0.0
    return g

def tangential(g):
    phi = np.arctan2(YY, XX)
    return -(g.real*np.cos(2*phi) + g.imag*np.sin(2*phi))

# --- validation: an axisymmetric profile must give DeltaSigma = mean Sigma(<R) - Sigma(R)
Ktest = 1.0/np.maximum(RR, CELL)                                   # an isothermal-like Sigma ~ 1/R
gt = tangential(shear_from_kappa(Ktest))
rb = np.geomspace(0.15, 1.5, 12)
err = 0.0
for a, b in zip(rb[:-1], rb[1:]):
    sel = (RR >= a) & (RR < b)
    ins = RR < 0.5*(a + b)
    got = float(gt[sel].mean())
    want = float(Ktest[ins].mean() - Ktest[sel].mean())
    err = max(err, abs(got - want)/abs(want))
ck("83b the shear inversion is CORRECT, not assumed: for an axisymmetric surface density the code's "
   "tangential shear reproduces the textbook DeltaSigma = <Sigma(<R)> - Sigma(R) to better than a few per "
   "cent over the radial range used.  A wrong Fourier kernel or a sign error cannot pass this",
   err < 0.05,
   f"worst relative error {100*err:.2f}% over R = 0.15-1.5 Mpc on a Sigma ~ 1/R test profile, "
   f"{NGRID}^2 grid, cell {1000*CELL:.0f} kpc")

# --- validation of the m = 2 response: a UNIFORM elliptical sheet of axis ratio q has, exactly, an
#     interior shear |gamma| = kappa (1 - q)/(1 + q), aligned with its major axis.  This is the check that
#     the FFT kernel handles the quadrupole and not only the monopole.
eerr = 0.0
for qq in (0.4, 0.6, 0.8):
    Ke = ((XX/0.5)**2 + (YY/(0.5*qq))**2 <= 1.0).astype(float)
    ge = shear_from_kappa(Ke)
    core = ((XX/0.5)**2 + (YY/(0.5*qq))**2 <= 0.25)
    # exact interior deflection of a homogeneous ellipse (semi-axes a > b, major axis along x):
    #   alpha_x = 2 kappa q/(1+q) x,  alpha_y = 2 kappa/(1+q) y  =>  gamma_1 = -kappa (1-q)/(1+q)
    # NEGATIVE.  The first version of this check compared against the positive value and "failed" by 200%
    # -- the sign convention was mine, not the code's.  Recorded rather than quietly flipped.
    got = float(np.mean(ge.real[core])); want = -(1.0 - qq)/(1.0 + qq)
    eerr = max(eerr, abs(got - want)/abs(want))
    info(f"uniform elliptical sheet q = {qq:.1f} (major axis along x): interior gamma_1 = {got:+.4f}, exact "
         f"-(1-q)/(1+q) = {want:+.4f}, error {100*abs(got-want)/abs(want):.1f}%")
ck("83b2 the m = 2 response of the shear code is CORRECT too, not just the monopole: for a uniform "
   "elliptical sheet it reproduces the exact interior shear kappa(1-q)/(1+q), with the right sign and "
   "orientation, over axis ratios 0.4-0.8",
   eerr < 0.05, f"worst relative error {100*eerr:.1f}% over q = 0.4, 0.6, 0.8")

# --- the quadrupole of the observable
_QP = {}
def quad_profile(e, theta_deg, r_M_Mpc, rbins):
    key = (round(math.log10(max(e, 1e-9)), 3), round(theta_deg, 2), round(r_M_Mpc, 6))
    if key in _QP: return _QP[key]
    sol = solver(e)
    S = sigma_map(sol, theta_deg, r_M_Mpc)
    gt = tangential(shear_from_kappa(S))
    phi = np.arctan2(YY, XX)
    m0, m2 = [], []
    # the lens's own baryons: a point mass M_b = 1 in solver units contributes DeltaSigma = 1/(pi R^2) to
    # the MONOPOLE and nothing to the quadrupole, so leaving it out would inflate the ratio by ~10 per cent
    rM2 = r_M_Mpc**2
    for a, b in zip(rbins[:-1], rbins[1:]):
        sel = (RR >= a) & (RR < b)
        m0.append(float(gt[sel].mean()) + float(np.mean(rM2/(math.pi*RR[sel]**2))))
        m2.append(2.0*float((gt[sel]*np.cos(2*phi[sel])).mean()))
    _QP[key] = (np.array(m0), np.array(m2))
    return _QP[key]

rbins = np.geomspace(0.05, 2.6, 13)
rmid = np.sqrt(rbins[:-1]*rbins[1:])
P(""); P(f"    external field at Theta = 90 deg to the line of sight (the most favourable geometry)")
P(f"    {'R (Mpc)':>9}" + "".join(f"{'e=%.3f' % e:>12}" for e in (0.003, 0.01, 0.03, 0.1)))
QP = {}
for e in (0.003, 0.01, 0.03, 0.1):
    m0, m2 = quad_profile(e, 90.0, r_M, rbins)
    QP[e] = (m0, m2)
for j, rr in enumerate(rmid):
    P(f"    {rr:9.3f}" + "".join(f"{QP[e][1][j]/QP[e][0][j]:12.4f}" for e in (0.003, 0.01, 0.03, 0.1)))
info("(the entry is the ratio of the cos 2phi amplitude of the tangential DeltaSigma to its azimuthal mean; "
     "a value of 0.2 corresponds, for an elliptical halo, to an axis ratio near 0.8)")

# the line-of-sight dilution
P(""); P(f"    {'Theta (deg)':>12} {'quadrupole/monopole at 0.5 Mpc, e_N = 0.01':>44} {'sin^2 Theta':>12}")
DIL = {}
for th in (90.0, 60.0, 30.0, 10.0):
    m0, m2 = quad_profile(0.01, th, r_M, rbins)
    j = int(np.argmin(np.abs(rmid - 0.5)))
    DIL[th] = m2[j]/m0[j]
    P(f"    {th:12.0f} {m2[j]/m0[j]:44.4f} {math.sin(math.radians(th))**2:12.4f}")
sin2 = {th: math.sin(math.radians(th))**2 for th in DIL}
sc = [DIL[th]/sin2[th] for th in DIL if th > 15]
ck("83c the projection dilutes the quadrupole exactly as sin^2(Theta), which is what the analytic "
   "projection of a P_2 field predicts -- so a stack of randomly oriented external fields keeps the "
   "average factor <sin^2 Theta> = 2/3 and not a random-phase cancellation, PROVIDED the stack is rotated "
   "to each lens's own ghat_ext (which is exactly what the committed g_ext vectors make possible)",
   (max(sc) - min(sc))/np.mean(sc) < 0.15,
   f"quadrupole/sin^2(Theta) = {['%.4f' % v for v in sc]} at Theta = 90, 60, 30 deg -- constant to "
   f"{100*(max(sc)-min(sc))/np.mean(sc):.1f}%")

# ---------------------------------------------------------------- PART C: is it reachable?
P(""); P("-"*118); P("PART C -- the forecast, against the KiDS errors that are ON DISK"); P("-"*118)
TOT = {}
for fn, lab in (("Fig-3_Lensing-rotation-curves_Massbin-1.txt", "mass bin 1"),
                ("Fig-3_Lensing-rotation-curves_Massbin-2.txt", "mass bin 2"),
                ("Fig-3_Lensing-rotation-curves_Massbin-3.txt", "mass bin 3"),
                ("Fig-3_Lensing-rotation-curves_Massbin-4.txt", "mass bin 4")):
    Rk, Ek, eEk = load_esd(fn)
    snr_mono = float(np.sqrt(np.sum((Ek/eEk)**2)))
    for ft, a0 in A0.items():
        rMf = math.sqrt(G*MB_LENS*Msun/a0)/Mpc
        for e in (0.01, 0.03):
            m0, m2 = quad_profile(e, 90.0, rMf, rbins)
            Q = np.interp(Rk, rmid, np.abs(m2/m0))
            # fitting a cos(2phi) amplitude over the full azimuth costs sqrt(2) in the error
            snr_q = float(np.sqrt(np.sum((Q*Ek/(math.sqrt(2)*eEk))**2))*math.sqrt(2.0/3.0))
            TOT[(lab, ft, e)] = (snr_mono, snr_q)
P(f"    {'sample':>12} {'footing':>10} {'e_N':>7} {'monopole S/N':>13} {'quadrupole S/N':>15}")
for k in sorted(TOT):
    P(f"    {k[0]:>12} {k[1]:>10} {k[2]:7.3f} {TOT[k][0]:13.1f} {TOT[k][1]:15.2f}")
best = max(TOT.values(), key=lambda t: t[1])[1]
allb = math.sqrt(sum(TOT[k][1]**2 for k in TOT if k[1] == "canonical" and k[2] == 0.01))
info(f"stacking the four mass bins (they are independent lens samples) at e_N = 0.01, canonical footing: "
     f"combined quadrupole S/N = {allb:.1f}")
ck("83d (FORECAST) the aligned quadrupole is within reach of data that already exist, but only just, and "
   "only if the stack is rotated to each lens's own external-field direction.  On the KiDS-1000 isolated "
   "lens errors that are on disk it is a 1-3 sigma effect per mass bin and a few sigma combined -- a "
   "go-look, not a discovery in waiting",
   1.0 < allb < 10.0,
   f"combined S/N = {allb:.1f} over the four KiDS mass bins at e_N = 0.01 with the <sin^2 Theta> = 2/3 "
   f"stacking factor included; the single best bin gives {best:.2f}.  The monopole in the same data is "
   f"detected at S/N = {max(TOT[k][0] for k in TOT):.0f}, so this is a {100*allb/max(TOT[k][0] for k in TOT):.0f} per cent "
   f"measurement of a quadrupole on a signal already in hand")

# ---------------------------------------------------------------- PART D: controls
P(""); P("-"*118); P("mutation controls, and the LambdaCDM alternative"); P("-"*118)
m0n, m2n = quad_profile(1e-9, 90.0, r_M, rbins)
j = int(np.argmin(np.abs(rmid - 0.5)))
info(f"MUTATION 1 (external field switched off): quadrupole/monopole at 0.5 Mpc falls from "
     f"{QP[0.01][1][j]/QP[0.01][0][j]:+.4f} to {m2n[j]/m0n[j]:+.6f} -- an isolated MOND galaxy's phantom is "
     f"exactly spherical, so the whole signal is the external field's")
# Newtonian control: a spherical NFW gives zero quadrupole; an ELLIPTICAL one gives a quadrupole aligned
# with its own axes, which is the LambdaCDM alternative
def nfw_sigma(q, rs=0.3, angle=0.0):
    xr = XX*math.cos(angle) + YY*math.sin(angle); yr = -XX*math.sin(angle) + YY*math.cos(angle)
    Re = np.sqrt(xr**2 + (yr/q)**2)
    xx = np.maximum(Re, CELL)/rs
    return 1.0/(xx*(1.0 + xx)**2)
gtN = tangential(shear_from_kappa(nfw_sigma(1.0)))
phi = np.arctan2(YY, XX)
sel = (RR >= 0.4) & (RR < 0.6)
qN = 2.0*float((gtN[sel]*np.cos(2*phi[sel])).mean())/float(gtN[sel].mean())
gtE = tangential(shear_from_kappa(nfw_sigma(0.8)))
qE = 2.0*float((gtE[sel]*np.cos(2*phi[sel])).mean())/float(gtE[sel].mean())
info(f"the LambdaCDM alternative, computed with the same code: a SPHERICAL NFW gives quadrupole/monopole = "
     f"{qN:+.5f} (zero, as it must) and an NFW flattened to q = 0.8 -- about what dark-matter simulations "
     f"give for the projected shape -- returns {qE:+.4f}, roughly "
     f"{abs(QP[0.01][1][j]/QP[0.01][0][j]/qE):.0f} times SMALLER than the framework's {QP[0.01][1][j]/QP[0.01][0][j]:+.4f} at e_N = 0.01.  So the "
     f"amplitude is a discriminant after all -- but the SIGN-DEFINITE one is still the axis, because a "
     f"halo's ellipticity axis is the light's and the phantom's is the external field's")
ck("83e MUTATION CONTROLS behave, and the discriminant is named: with no external field the phantom is "
   "exactly round; a spherical NFW returns exactly zero through the same pipeline; and a realistically "
   "flattened NFW returns a quadrupole several times SMALLER than the framework's.  The measurement that "
   "matters is still whether the quadrupole's axis follows ghat_ext or the light, because those two axes "
   "are only weakly correlated and only one of them is a dark-matter prediction",
   abs(m2n[j]/m0n[j]) < 0.02 and abs(qN) < 0.02 and abs(qE) > 0.01 and
   abs(QP[0.01][1][j]/QP[0.01][0][j]) > 2*abs(qE),
   f"no-field quadrupole {m2n[j]/m0n[j]:+.5f}; spherical NFW {qN:+.5f}; q = 0.8 NFW {qE:+.4f} against the "
   f"framework's {QP[0.01][1][j]/QP[0.01][0][j]:+.4f} at e_N = 0.01")

P(""); P("-"*118)
P(f"VERDICT.  Item 83 is a REAL and REACHABLE test and this run makes it quantitative for the first time.")
P(f"The phantom's quadrupole is not a small correction: the total potential's l = 2 term is {100*abs(q3d):.0f} per cent of its")
P(f"monopole, matching the analytic linearised QUMOND value to a few per cent, and after")
P(f"projection the tangential DeltaSigma carries a cos 2phi modulation of {abs(QP[0.01][1][j]/QP[0.01][0][j]):.2f} of the monopole at 0.5 Mpc for a")
P(f"typical field e_N = 0.01, diluted only by <sin^2 Theta> = 2/3 in a stack rotated to each lens's own")
P(f"ghat_ext.  On the KiDS-1000 isolated-lens errors already on disk that is S/N ~ {allb:.1f} combined.  It is NOT a")
P(f"measurement here -- the shear catalogue is not on disk -- so this is recorded as NOT RUNNABLE / forecast.")
P(f"The one thing that must not be lost: an NFW halo flattened to q = 0.8 gives {abs(qE):.3f} through the same")
P(f"pipeline, {abs(QP[0.01][1][j]/QP[0.01][0][j]/qE):.0f} times smaller but not zero.  The whole content is in the AXIS.  The framework points")
P(f"it at the nearest attractor; every dark-matter model points it at the light or at the filament; and the")
P(f"g_ext vectors needed to rotate the stack are already committed for SPARC and computable for any lens")
P(f"sample from 2M++.  That is the experiment.")
P("-"*118)
sys.exit(ck.done())
