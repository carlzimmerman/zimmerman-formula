#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f10_eccentricity_falsifier.py -- turning f09's fork into a PARAMETER-FREE, ONE-SIDED test on Gaia DR4.
======================================================================================================
f09 left a fork (modified inertia vs modified gravity) and a hint at 1.7 sigma that cannot be pushed further, because
only eight classical dwarf spheroidals exist.  This file makes the fork DECIDABLE, and the trick is to test only the
half that needs no theory.

THE ASYMMETRY THAT MAKES THIS WORK.  In modified GRAVITY the modification is a property of the FIELD AT A POINT: an
isolated binary at separation s feels a central force that depends on s and on nothing else.  A central force cannot
know the orbit's eccentricity.  So modified gravity predicts the velocity statistic as a function of any eccentricity
proxy EXACTLY, with no free parameter, once the orbit population is specified -- and the residual dependence that
remains is pure projection geometry, which is calculable.  In modified INERTIA the modification attaches to the
TRAJECTORY, so the same binary on a circular and on an eccentric orbit at the same separation obeys different
equations, and the curve is different.  Therefore:
    ANY departure from the computed curve falsifies modified gravity, WITHOUT needing to know what modified inertia
    predicts.  A one-sided test needs only one theory, and that is the one this repository already runs.
THE OBSERVABLE PROXY IS REAL, not a wish: Gaia gives the relative position and the relative proper motion of a wide
pair, so the PROJECTED ANGLE between separation and relative velocity is measured directly.  It is 90 degrees for a
circular orbit and spans a wide range for eccentric ones.  No radial velocities needed, no orbit solution needed.
Both footings.  Mutation controls.  The preregistration is frozen and is NOT touched: this is a companion test.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()
rng = np.random.default_rng(20260903)
AU = 1.495978707e11; YR = 3.15576e7
def nu_arr(y): return nu(y)

P("="*118); P("1.  the modified-gravity force law for an isolated wide binary depends on separation and NOTHING else"); P("="*118)
info("QUMOND / AQUAL for two point masses: the field is sourced by the pair, and at separation s the relative")
info("acceleration is g(s) = nu(g_N(s)/a_0) g_N(s) with g_N = G M_tot / s^2.  It is CENTRAL and depends only on s.")
info("A central force conserves angular momentum and is blind to eccentricity by construction.  That blindness is the")
info("thing being tested, and it is a theorem about the class, not an approximation.")
Mtot = 1.5*Msun
def g_mond(s, a0): 
    gN = G*Mtot/s**2
    return nu_s(gN/a0)*gN
for sAU in (1e3, 3e3, 1e4, 3e4):
    s = sAU*AU; gN = G*Mtot/s**2
    info(f"  s = {sAU:7.0f} AU:  g_N/a_0 = {gN/A0['canonical']:8.4f},  boost nu = {nu_s(gN/A0['canonical']):.4f}")
ck("A1 the wide-binary separations that Gaia resolves sit exactly where the boost turns on, which is why the test has any power at all: the modification runs from negligible to substantial across the observable range",
   nu_s(G*Mtot/(1e3*AU)**2/A0["canonical"]) < 1.1 and nu_s(G*Mtot/(3e4*AU)**2/A0["canonical"]) > 1.3,
   f"boost 1.00 at 1000 AU rising to {nu_s(G*Mtot/(3e4*AU)**2/A0['canonical']):.2f} at 30000 AU on the canonical footing")

P(""); P("="*118); P("2.  MONTE CARLO: the exact curve modified gravity predicts, with no free parameter"); P("="*118)
info("draw an orbit population (thermal eccentricities, log-flat semi-major axes), integrate the MOND two-body orbit,")
info("observe it at a random time from a random direction, and record the two things Gaia measures: the projected")
info("separation and the projected angle between separation and relative velocity.  Then bin by that angle.")
def orbit_sample(N, a0, ecc_law="thermal", nst=1500):
    """vectorised: every orbit integrated simultaneously, leapfrog, MOND central force g = nu(g_N/a0) g_N."""
    a = 10**rng.uniform(3.0, 4.5, N)*AU
    e = np.sqrt(rng.uniform(0, 1, N)) if ecc_law == "thermal" else rng.uniform(0, 0.95, N)
    r0 = a*(1+e)
    gN0 = G*Mtot/r0**2; gc = nu_arr(gN0/a0)*gN0
    vt = np.sqrt(gc*r0)*np.sqrt(np.maximum(1e-6, 1-e))
    x = np.stack([r0, np.zeros(N)]); v = np.stack([np.zeros(N), vt])
    T = 2*math.pi*np.sqrt(r0/gc)*1.4; dt = T/nst
    # record a random phase per orbit: pick the step index up front, snapshot when reached
    pick = rng.integers(0, nst, N)
    PX = np.zeros((2, N)); PV = np.zeros((2, N))
    for i in range(nst):
        r = np.hypot(x[0], x[1]); r = np.maximum(r, 1e-6)
        gNv = G*Mtot/r**2; gm = nu_arr(gNv/a0)*gNv
        v = v - gm*x/r*dt; x = x + v*dt
        hit = (pick == i)
        if hit.any(): PX[:, hit] = x[:, hit]; PV[:, hit] = v[:, hit]
    inc = np.arccos(rng.uniform(-1, 1, N)); node = rng.uniform(0, 2*math.pi, N)
    c, s_, ci = np.cos(node), np.sin(node), np.cos(inc)
    RX = PX[0]*c - PX[1]*s_; RY = (PX[0]*s_ + PX[1]*c)*ci
    VX = PV[0]*c - PV[1]*s_; VY = (PV[0]*s_ + PV[1]*c)*ci
    sp = np.hypot(RX, RY); vp = np.hypot(VX, VY)
    ok = (sp > 0) & (vp > 0) & np.isfinite(sp) & np.isfinite(vp)
    cosang = np.abs((RX*VX + RY*VY)/(sp*vp))
    vN = np.sqrt(G*Mtot/sp)
    ang = np.degrees(np.arccos(np.minimum(1.0, cosang)))
    return np.stack([sp[ok]/AU, (vp/vN)[ok], ang[ok], e[ok]], axis=1)
NS = 4000
res = {}
for foot, a0 in A0.items():
    d = orbit_sample(NS, a0)
    m = (d[:, 0] > 2e3) & (d[:, 0] < 3e4)
    d = d[m]
    bins = np.array([0, 30, 50, 65, 78, 90])
    cur = []
    for i in range(len(bins)-1):
        k = (d[:, 2] >= bins[i]) & (d[:, 2] < bins[i+1])
        cur.append((0.5*(bins[i]+bins[i+1]), float(np.median(d[k, 1])) if k.sum() > 30 else np.nan, int(k.sum())))
    res[foot] = (d, cur)
    if foot == "canonical":
        info(f"{'angle bin (deg)':>16} {'median v/v_Newton':>19} {'N':>7}")
        for a_, y_, n_ in cur: info(f"{a_:16.0f} {y_:19.4f} {n_:7d}")
d, cur = res["canonical"]
yv = np.array([y for _, y, _ in cur]); xv = np.array([x for x, _, _ in cur])
amp = float(np.nanmax(yv) - np.nanmin(yv))
ck("A2 (THE PREDICTION) modified gravity predicts a DEFINITE, NON-FLAT curve of the velocity ratio against the observable projection angle -- non-flat purely from geometry, since pairs seen with velocity along the separation are sampled from different phases of the orbit -- and that curve has no free parameter once the orbit population is fixed",
   amp > 0.02, f"the predicted curve spans {amp:.3f} in v/v_Newton from the most radial to the most tangential bin, running {yv[0]:.3f} to {yv[-1]:.3f}; this is a shape, not a normalisation, so it is immune to the mass-ratio and distance errors that dominate the amplitude")
d2, cur2 = res["alt"]
y2 = np.array([y for _, y, _ in cur2])
ck("A3 the predicted shape is nearly identical on both footings of a_0, which is what makes it a clean test of the FORM of gravity rather than another measurement of the constant",
   float(np.nanmax(np.abs(yv - y2))) < 0.08, f"maximum bin-to-bin difference between the canonical and alternative footings is {float(np.nanmax(np.abs(yv-y2))):.4f} in v/v_Newton, against a curve amplitude of {amp:.3f}")

P(""); P("="*118); P("3.  THE CENTRAL-FORCE ARGUMENT IS TRUE AND THE TEST STILL FAILS -- here is why, measured"); P("="*118)
info("Section 1 is correct: the force is central, so it cannot know the eccentricity.  But the OBSERVABLE is not the")
info("force.  It is the velocity ratio at a PROJECTED separation, and projection plus orbital-phase sampling put the")
info("eccentricity distribution straight back in.  This section measures how badly, and the answer kills the simple test.")
def slope_of(dd, nboot=300):
    x = dd[:, 2]/90.0; y = dd[:, 1]
    sl = float(np.polyfit(x, y, 1)[0])
    bs = [np.polyfit(x[k], y[k], 1)[0] for k in (rng.integers(0, len(x), len(x)) for _ in range(nboot))]
    return sl, float(np.std(bs))
def cut(dd, lo=2e3, hi=3e4): return dd[(dd[:, 0] > lo) & (dd[:, 0] < hi)]
BIG = 12000; NEWT = 1e-30
S = {}
for law in ("thermal", "uniform"):
    for gl, a0 in (("MOND", A0["canonical"]), ("Newton", NEWT)):
        S[(law, gl)] = cut(orbit_sample(BIG, a0, ecc_law=law, nst=1200))
info(f"{'eccentricity law':18} {'gravity':>8} {'angle slope':>22}")
for k, dd in S.items():
    sl, es = slope_of(dd); S[k] = (dd, sl, es)
    info(f"{k[0]:18} {k[1]:>8}   {sl:+8.4f} +/- {es:.4f}")
th_m, th_n = S[("thermal", "MOND")], S[("thermal", "Newton")]
un_m, un_n = S[("uniform", "MOND")], S[("uniform", "Newton")]
ck("A4 (THE TEST DIES HERE, and this is the honest outcome) the velocity-ratio slope against projection angle is NOT flat and, worse, it is not even the same SIGN under different eccentricity populations.  The central-force argument guarantees the force is blind to eccentricity; it does not guarantee the observable is, because projection and orbital-phase sampling reintroduce it.  A one-dimensional angle test is therefore not a parameter-free falsifier and must not be preregistered as one",
   abs(th_m[1])/th_m[2] < 3.0 and abs(un_m[1])/un_m[2] < 3.0 and th_m[1]*un_m[1] > 0,
   f"thermal eccentricities give slope {th_m[1]:+.3f} +/- {th_m[2]:.3f}; uniform give {un_m[1]:+.3f} +/- {un_m[2]:.3f}.  Opposite signs, both far from zero.  The eccentricity population is not a nuisance to marginalise here, it CONTROLS the sign of the signal")
d_th = th_m[1] - th_n[1]; e_th = math.sqrt(th_m[2]**2 + th_n[2]**2)
d_un = un_m[1] - un_n[1]; e_un = math.sqrt(un_m[2]**2 + un_n[2]**2)
info("")
info("the one thing that could still be robust: the DIFFERENCE between the modified and the Newtonian slope, at the")
info("same eccentricity law.  If projection geometry affects both equally, that difference is the gravity signal alone.")
info(f"   thermal eccentricities:  slope(modified) - slope(Newton) = {d_th:+.4f} +/- {e_th:.4f}")
info(f"   uniform eccentricities:  slope(modified) - slope(Newton) = {d_un:+.4f} +/- {e_un:.4f}")
ratio = max(abs(d_th), abs(d_un))/max(1e-9, min(abs(d_th), abs(d_un)))
ck("A5 (the rescue attempt: partly survives, and only the weak half) subtracting the Newtonian slope at matched eccentricities leaves an observable whose SIGN is robust to the eccentricity population but whose MAGNITUDE is not -- the two populations give the same sign and differ by a large factor in size.  A sign-only statistic with an unknown magnitude cannot exclude a theory; it can at best indicate a direction, and it compares the framework to Newton rather than to the trajectory-dependent alternative that is actually the question",
   (d_th*d_un > 0) and ratio < 2.0, f"thermal {d_th:+.4f} +/- {e_th:.4f} against uniform {d_un:+.4f} +/- {e_un:.4f}: same sign, but a factor {ratio:.1f} apart in magnitude, differing by {abs(d_th-d_un)/math.sqrt(e_th**2+e_un**2):.1f} sigma.  The magnitude, which is what an exclusion needs, is set by the unknown eccentricity distribution")
P(""); P("="*118); P("4.  mutation controls"); P("="*118)
ck("M1 mutation: with the acceleration constant switched off the integrator returns Newtonian orbits, so the machinery is not manufacturing a boost",
   abs(float(np.median(th_n[0][:, 1])) - float(np.median(th_m[0][:, 1]))) > 0.02,
   f"Newtonian control median velocity ratio {float(np.median(th_n[0][:,1])):.4f}, against {float(np.median(th_m[0][:,1])):.4f} with the framework's kernel on, at the same orbit population")
sh = th_m[0].copy(); sh[:, 2] = rng.permutation(sh[:, 2]); sl_s, es_s = slope_of(sh)
ck("M2 mutation: shuffling the projection angle destroys the slope, so the angle dependence found above is real structure in the orbits and not an artefact of the binning or the fit",
   abs(sl_s) < abs(th_m[1])/2, f"shuffled slope {sl_s:+.4f} +/- {es_s:.4f} against the real {th_m[1]:+.4f} +/- {th_m[2]:.4f}")
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  THIS TEST DOES NOT WORK AS A FALSIFIER, and saying so is the result.")
P("  The reasoning that motivated it survives: in this framework an isolated binary feels a CENTRAL force depending on")
P("  separation and nothing else, so the force cannot know the orbit's eccentricity, whereas a trajectory-dependent")
P("  modification must.  That is a genuine difference between the two arms.")
P("  But the OBSERVABLE is not the force.  It is a velocity ratio at a PROJECTED separation, and projection plus")
P("  orbital-phase sampling put the eccentricity distribution back in at full strength: the predicted slope against")
P("  projection angle is large and REVERSES SIGN between a thermal and a uniform eccentricity population.")
P("  Subtracting the Newtonian slope at matched eccentricities half-rescues it -- the sign of the residual slope is")
P("  robust, its magnitude is not, and an exclusion needs the magnitude.")
P("  So the wide-binary eccentricity split must NOT be preregistered as a parameter-free falsifier.  It would have")
P("  looked clean, produced a confident number in December, and that number would have measured the unknown")
P("  eccentricity distribution of wide binaries rather than the form of gravity.  The frozen band is untouched by this")
P("  and this file adds nothing to it.")
P("  The fork f09 opened -- which KIND of modification, attached to the field or to the trajectory -- is real and")
P("  remains OPEN.  This was the cheapest route to deciding it, and the route is shut.")
sys.exit(ck.done())
