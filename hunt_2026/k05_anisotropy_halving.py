#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k05_anisotropy_halving.py -- ANGLE 4, CANDIDATE K5: THE ANISOTROPY-HALVING LAW.
        d ln g_obs  =  (1 + L(y))  d ln g_bar          with  L = d ln nu / d ln y,  L -> -1/2 deep

DERIVATION.  From g_obs = nu(y) g_bar, y = g_bar/a_0, take the logarithmic differential in ANY direction:
d ln g_obs = (1 + L) d ln g_bar.  Applied radially this is candidate k01.  Applied ANGULARLY it is a statement
nobody has written down: the FRACTIONAL ANGULAR VARIATION of the observed (and lensing) field around a galaxy is
(1 + L(y)) times the fractional angular variation of the baryons' own Newtonian field -- and in the deep-MOND
regime that factor is EXACTLY 1/2, with no free parameter and no dependence on the mass-to-light ratio, because
it is a ratio of two anisotropies and every amplitude cancels.

So: the phantom halo of a disc galaxy is FLATTENED toward the disc, and by a predicted amount.  Nothing in the
BTFR or the RAR says anything at all about angular structure; v^4 = G M_b a_0 is a statement about one number
per galaxy.  This is therefore not a restatement of either -- it is the same kernel read in a direction the
acceleration relation never probes.

WHAT IS COMPUTED HERE.  (1) the identity, verified numerically against the kernel; (2) the exterior field of a
razor-thin exponential disc, Newtonian and modified, and the measured ratio of their pole-to-equator
anisotropies, which must equal 1 + L; (3) the phantom's own isodensity axis ratio, which is what a
galaxy-galaxy lensing halo-ellipticity measurement (KiDS, DES, Euclid) reports as f_h; (4) both footings;
(5) the Upsilon lever; (6) the LambdaCDM alternative quoted beside it.
"""
import os, math, sys
import numpy as np
from scipy.special import j0, j1
from hunt_lib import *

ck = Check()
P("="*118); P("CANDIDATE K5 -- the anisotropy-halving law: d ln g_obs = (1 + L(y)) d ln g_bar in EVERY direction"); P("="*118)

def nu_of(g, a0):  return 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(g/a0, 1e-300))))
def L_of_y(y):
    s = np.sqrt(np.maximum(y, 1e-300))
    return np.where(s < 1e-8, -0.5, -(s/2.0)/np.expm1(np.minimum(s, 700.0)))

P("  (1) the identity, verified against the kernel by finite differences (checks that CAN fail):")
for y in [0.01, 0.1, 1.0, 10.0]:
    e = 1e-6
    lg1 = math.log(y*(1+e)/(1 - math.exp(-math.sqrt(y*(1+e)))))
    lg0 = math.log(y*(1-e)/(1 - math.exp(-math.sqrt(y*(1-e)))))
    num = (lg1 - lg0)/(math.log(y*(1+e)) - math.log(y*(1-e)))
    ck(f"d ln g_obs/d ln g_bar = 1 + L at y={y}", abs(num - (1 + float(L_of_y(y)))) < 1e-6,
       f"numeric {num:.9f} vs 1+L = {1+float(L_of_y(y)):.9f}")
P(f"  deep limit: 1 + L = 1/2 exactly.  Tabulated:")
P(f"    {'y = g_bar/a_0':>14} {'1 + L':>8}     {'y = g_bar/a_0':>14} {'1 + L':>8}")
ys = [0.01, 0.1, 0.3, 1.0, 3.0, 10.0]
for i in range(0, len(ys), 2):
    P(f"    {ys[i]:14.2f} {1+float(L_of_y(ys[i])):8.4f}     {ys[i+1]:14.2f} {1+float(L_of_y(ys[i+1])):8.4f}")
P("")

# ---------------------------------------------------------------- exterior field of a razor-thin exponential disc
Rd = 1.0
KG = np.concatenate([np.linspace(1e-6, 5, 4000), np.linspace(5.0001, 60, 3000), np.linspace(60.001, 2000, 4000)])
def gN_cyl(R, z):
    R = np.atleast_1d(np.asarray(R, float)); z = np.atleast_1d(np.asarray(z, float))
    kk = KG[None, :]; S = (1.0 + (kk*Rd)**2)**-1.5*kk*np.exp(-kk*np.abs(z)[:, None])
    gR = -np.trapz(S*j1(kk*R[:, None]), KG, axis=1)
    gz = -np.sign(z)*np.trapz(S*j0(kk*R[:, None]), KG, axis=1)
    return gR, gz                                        # units of 2 pi G Sigma0

P("  (2) EXTERIOR FIELD OF AN EXPONENTIAL DISC.  Compare the pole-to-equator contrast of |g_N| with that of")
P("      |g_obs| = nu |g_N|.  The law says contrast(obs)/contrast(bar) = 1 + L, evaluated at that radius.")
P(f"  {'r/R_d':>7} {'y_eq = g_bar/a_0':>17} {'Newtonian contrast':>19} {'modified contrast':>18} {'ratio':>8} {'1 + L':>8}")
for y_eq_target in [0.3]:
    for rr in [4.0, 8.0, 16.0, 32.0]:
        # equator (theta = 90 deg) and pole (theta = 0)
        gRe, gze = gN_cyl(np.array([rr]), np.array([1e-9])); ge = math.hypot(gRe[0], gze[0])
        gRp, gzp = gN_cyl(np.array([1e-7]), np.array([rr])); gp = math.hypot(gRp[0], gzp[0])
        # scale so that the equatorial baryonic acceleration at r = 4 R_d has the chosen y
        gR4, _ = gN_cyl(np.array([4.0]), np.array([1e-9])); sc = y_eq_target/abs(gR4[0])
        gee, gpp = ge*sc, gp*sc               # in units of a_0
        con_N = (gee - gpp)/(0.5*(gee + gpp))
        oe, op = gee*float(nu_of(gee, 1.0)), gpp*float(nu_of(gpp, 1.0))
        con_M = (oe - op)/(0.5*(oe + op))
        ymid = 0.5*(gee + gpp)
        P(f"  {rr:7.1f} {gee:17.4f} {con_N:19.5f} {con_M:18.5f} {con_M/con_N:8.4f} {1+float(L_of_y(ymid)):8.4f}")
        ck(f"anisotropy ratio equals 1+L at r={rr} R_d", abs(con_M/con_N - (1+float(L_of_y(ymid)))) < 0.04,
           f"{con_M/con_N:.4f} vs {1+float(L_of_y(ymid)):.4f}")
P("")

# ---------------------------------------------------------------- the phantom's own shape (the lensing observable)
P("  (3) THE PHANTOM'S OWN SHAPE.  rho_ph = div[(nu-1) g_N]/(4 pi G).  Its isodensity axis ratio is what a")
P("      galaxy-galaxy lensing halo-ellipticity measurement reports.  Computed on an (R,z) grid:")
def phantom_axis_ratio(y_scale, a0=1.0):
    Rg = np.exp(np.linspace(math.log(0.05), math.log(80.0), 300))
    zg = np.concatenate([-np.exp(np.linspace(math.log(60.0), math.log(0.01), 150)),
                          np.exp(np.linspace(math.log(0.01), math.log(60.0), 150))])
    RR, ZZ = np.meshgrid(Rg, zg, indexing="ij")
    gR, gz = gN_cyl(RR.ravel(), ZZ.ravel())
    gR = gR.reshape(RR.shape)*y_scale; gz = gz.reshape(RR.shape)*y_scale
    gm = np.hypot(gR, gz)
    F = (nu_of(gm, a0) - 1.0)
    FR, FZ = F*gR, F*gz
    div = (np.gradient(RR*FR, Rg, axis=0)/np.maximum(RR, 1e-12)) + np.gradient(FZ, zg, axis=1)
    rho = -div/(4*np.pi)   # SIGN: g_N = -grad Phi_N, so div[(nu-1) g_N] = -4 pi G rho_ph
    # axis ratio of the isodensity contour through (R = r0, z = 0): find z on the polar axis with the same rho
    iz0 = int(np.argmin(np.abs(zg)))
    zpos = zg[zg > 0]
    out = []
    for r0 in [4.0, 8.0, 16.0]:
        iR = int(np.argmin(np.abs(Rg - r0)))
        target = rho[iR, iz0]
        col = rho[0, zg > 0]                      # polar axis (smallest R on the grid)
        ok = np.isfinite(col) & (col > 0)
        zz_, cc_ = zpos[ok], col[ok]
        if target <= 0 or len(zz_) < 5: out.append((r0, float("nan"))); continue
        # cc_ decreases with z: interpolate log rho -> z on the decreasing branch
        j = int(np.argmax(cc_))
        zz_, cc_ = zz_[j:], cc_[j:]
        if not (cc_.min() < target < cc_.max()): out.append((r0, float("nan"))); continue
        zi = float(np.interp(math.log(target), np.log(cc_[::-1]), zz_[::-1]))
        out.append((r0, zi/r0))
    return out
for lab, ys_ in [("bright spiral y(4Rd) ~ 1", 1.0), ("dwarf  y(4Rd) ~ 0.1", 0.1)]:
    gR4, _ = gN_cyl(np.array([4.0]), np.array([1e-9])); sc = ys_/abs(gR4[0])
    P(f"    {lab:28}: " + "  ".join(f"q(r={r0:.0f}R_d) = {q:.3f}" for r0, q in phantom_axis_ratio(sc)))
P("    (q < 1 means the phantom is OBLATE -- flattened toward the disc, as the halving law requires.)")
P("    CAVEAT, recorded against interest: for a RAZOR-THIN disc part of the phantom is a delta-function sheet of")
P("    surface density (nu-1) Sigma_b, so the innermost axis ratios above are dominated by that sheet and are an")
P("    artefact of the idealisation, not a halo shape.  The honest, sheet-free statement is the FIELD contrast in")
P("    part (2): the phantom's angular structure is 1+L times the baryons' and both DIE OFF outward, because a")
P("    point mass's phantom is spherical.  At r = 16 R_d the modified field's pole-to-equator contrast is only")
P("    2.8% (Newtonian 5.2%), i.e. a halo ellipticity of ~1.4% -- one to two orders of magnitude below what")
P("    galaxy-galaxy lensing halo-ellipticity measurements can currently resolve.  That is this candidate's")
P("    limiting number and it is what caps its promise.")
P("    LambdaCDM alternative: N-body haloes are triaxial with q = 0.7-0.9 but their orientation is set by the")
P("    tidal field, not by the disc, and lensing measurements report f_h = e_halo/e_light with no predicted value.")
P("")
P("  (4) THE UPSILON LEVER.  The ratio contrast(obs)/contrast(bar) = 1 + L(y) is a RATIO of two anisotropies, so")
P("      every amplitude -- Upsilon, distance, the disc's mass -- cancels from it exactly.  Upsilon survives only")
P("      inside y:")
for u in [0.3, 0.5, 0.7]:
    yv = 0.3*(u/0.5)
    P(f"      Upsilon = {u:.1f}  ->  y scales to {yv:.3f}  ->  1 + L = {1+float(L_of_y(yv)):.4f}")
l1 = math.log10(1+float(L_of_y(0.3*0.6))); l2 = math.log10(1+float(L_of_y(0.3*1.4)))
lev = (l2 - l1)/(math.log10(1.4) - math.log10(0.6))
P(f"      d log(1+L) / d log Upsilon = {lev:+.4f}   (compare: deep-tail a_0 rung -0.647, KiDS dwarf stack -1.046)")
ck("Upsilon lever on the halving law |d log(1+L)/d log Upsilon| < 0.15", abs(lev) < 0.15, f"{lev:+.4f}")
P("")
P("  (5) BOTH FOOTINGS.  1 + L depends on a_0 only through y = g_bar/a_0:")
for foot, a0 in A0.items():
    P(f"      {foot:10} a_0 = {a0:.3e}: at g_bar = 1e-11 m/s^2, 1 + L = {1+float(L_of_y(1e-11/a0)):.4f}; "
      f"at 1e-10, {1+float(L_of_y(1e-10/a0)):.4f}")
P("")
sys.exit(ck.done())
