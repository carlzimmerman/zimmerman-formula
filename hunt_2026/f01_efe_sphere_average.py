#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f01_efe_sphere_average.py -- WHICH external-field coupling is the sphere-averaged one?  Checking a factor of 2 by hand.
=======================================================================================================================
An agent derived the exact QUMOND flux theorem -- div g = div S with S = nu(|g_N|/a_0) g_N, so div(g - S) = 0 everywhere
and the divergence theorem gives <g_r>_sphere = <S_r>_sphere EXACTLY, for any geometry, with no linearisation -- and
reported that it implies the correct external-field-dominated effective coupling is nu(x_e)(1 + L_e) with
L_e = dln nu/dln x, i.e. HALF the naive nu(x_e) in the deep limit.  Every external-field liability in the programme,
and the ~5 sigma external-field-slope negative, was then flagged provisional on that factor.

THE FACTOR MATTERS ENOUGH TO CHECK BY HAND, and by hand it comes out differently.  In a dominant uniform external field
the effective coupling is a TENSOR, nu(x_e)[delta_ij + L_e n_i n_j] with n the external-field direction (Milgrom 1986;
Famaey & McGaugh 2012 review, eq. 59-60): PARALLEL to the field it is nu(1 + L_e), PERPENDICULAR it is nu.
  * nu(1 + L_e) is the PARALLEL component -- and in the deep limit L_e = -1/2, so that IS half of nu.
  * but an ISOTROPIC velocity dispersion, and a sphere-averaged enclosed mass, measure the ANGLE AVERAGE, and the
    first-order sphere average of S_r is  -h nu(x_e) [1 + L_e/3]  =>  the coupling is nu(1 + L_e/3) = 0.833 nu deep,
    a 17% correction, NOT a factor 2.
This script does the sphere average NUMERICALLY, with no expansion, and settles which factor applies to which
observable.  Both footings.  Checks CAN fail.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()
def nu_s2(x): x = max(float(x), 1e-14); return 1.0/(1.0 - math.exp(-math.sqrt(x)))
def L_of(x, d=1e-5):
    return (math.log(nu_s2(x*(1+d))) - math.log(nu_s2(x*(1-d))))/(2*d)
P("="*112); P("1. the kernel's log-log slope L = dln nu/dln x, and the three candidate couplings"); P("="*112)
info(f"{'x_e':>10} {'nu(x_e)':>10} {'L_e':>9} {'nu(1+L_e)  [parallel]':>24} {'nu(1+L_e/3) [sphere avg]':>26} {'ratio par/nu':>13}")
for xe in (1e-4, 1e-3, 1e-2, 0.03, 0.1, 0.3, 1.0, 3.0):
    n = nu_s2(xe); L = L_of(xe)
    info(f"{xe:10.4f} {n:10.4f} {L:9.4f} {n*(1+L):24.4f} {n*(1+L/3):26.4f} {1+L:13.4f}")
Ldeep = L_of(1e-6)
ck("A1 the kernel's deep-limit log-log slope is -1/2, so nu(1+L) IS half of nu there (the agent's factor is right for the PARALLEL component)",
   abs(Ldeep + 0.5) < 0.02, f"L(x -> 0) = {Ldeep:.4f}; nu(1+L)/nu = {1+Ldeep:.4f}")
P(""); P("="*112); P("2. the sphere average, done NUMERICALLY with no expansion"); P("="*112)
def sphere_avg_Sr(xe, h_over_a0, n_theta=4001):
    """<S_r> over a sphere, for a uniform external field e = xe*a_0 along z and an internal field -h r_hat.
    Exact quadrature, no expansion.  Returns -<S_r>/h, i.e. the effective coupling in units of G."""
    th = np.linspace(0, math.pi, n_theta); w = np.sin(th)/2.0
    ct = np.cos(th)
    gx = np.zeros_like(th); gz = xe*np.ones_like(th)          # in units of a_0
    # internal field -h r_hat, r_hat = (sin th, 0, cos th) in the plane containing z
    gtx = gx - (h_over_a0)*np.sin(th); gtz = gz - (h_over_a0)*ct
    mag = np.sqrt(gtx**2 + gtz**2)
    nu_v = np.array([nu_s2(m) for m in mag])
    Sr = nu_v*(gtx*np.sin(th) + gtz*ct)                        # S . r_hat, units a_0
    num = np.trapz(Sr*w, th)/np.trapz(w, th)
    return -num/h_over_a0
info(f"{'x_e':>9} {'h/a_0':>9} {'-<S_r>/h  (numerical)':>23} {'nu(1+L/3)':>12} {'nu(1+L)':>10} {'nu':>9}   which it matches")
R2 = {}
for xe in (1e-3, 1e-2, 0.1, 1.0):
    n = nu_s2(xe); L = L_of(xe)
    for hr in (1e-4, 1e-3, 1e-2):
        val = sphere_avg_Sr(xe, hr*xe)
        cands = {"nu(1+L/3)": n*(1+L/3), "nu(1+L)": n*(1+L), "nu": n}
        best = min(cands, key=lambda k: abs(val/cands[k]-1))
        info(f"{xe:9.4f} {hr*xe:9.2e} {val:23.5f} {n*(1+L/3):12.5f} {n*(1+L):10.5f} {n:9.5f}   {best} (to {abs(val/cands[best]-1)*100:.3f}%)")
        if hr == 1e-4: R2[xe] = (val, n*(1+L/3), n*(1+L), n)
ok13 = all(abs(v[0]/v[1] - 1) < 0.01 for v in R2.values())
ok1L = all(abs(v[0]/v[2] - 1) < 0.01 for v in R2.values())
ck("A2 (THE CORRECTION TO THE CORRECTION) the sphere-averaged coupling is nu(1 + L/3), NOT nu(1 + L): the numerical quadrature matches nu(1+L/3) to better than 1% at every external field, and does NOT match nu(1+L)",
   ok13 and not ok1L, "; ".join(f"x_e={k}: numerical {v[0]:.5f} vs nu(1+L/3) {v[1]:.5f} ({100*(v[0]/v[1]-1):+.2f}%) vs nu(1+L) {v[2]:.5f} ({100*(v[0]/v[2]-1):+.1f}%)" for k, v in R2.items()))
deep = R2[1e-3]
ck("A3 so the deep-limit correction to an ISOTROPIC, sphere-averaged measurement is 0.83x, a 17% reduction -- NOT the factor 2 that was flagged.  The factor 2 applies to the PARALLEL component only",
   abs(deep[1]/deep[3] - 0.8333) < 0.02, f"nu(1+L/3)/nu = {deep[1]/deep[3]:.4f} (sphere-averaged, 17% down) vs nu(1+L)/nu = {deep[2]/deep[3]:.4f} (parallel, 50% down)")
P(""); P("="*112); P("3. mutation control"); P("="*112)
flat = sphere_avg_Sr(1e-3, 1e-7)
ck("M1 the quadrature reproduces the isolated-limit identity: as the internal field vanishes the coupling tends to a constant, not to zero or infinity",
   0.1 < flat/nu_s2(1e-3) < 10, f"-<S_r>/h -> {flat:.4f} = {flat/nu_s2(1e-3):.4f} nu(x_e)")
def sphere_avg_newton(xe, hr, n_theta=2001):
    th = np.linspace(0, math.pi, n_theta); w = np.sin(th)/2.0; ct = np.cos(th)
    gtx = -hr*np.sin(th); gtz = xe - hr*ct
    Sr = 1.0*(gtx*np.sin(th) + gtz*ct)
    return -np.trapz(Sr*w, th)/np.trapz(w, th)/hr
newt = sphere_avg_newton(1e-3, 1e-7)
ck("M2 mutation: with nu = 1 (Newton) the sphere-averaged coupling is exactly 1, so the machinery is not manufacturing a factor",
   abs(newt - 1.0) < 1e-6, f"Newtonian sphere average = {newt:.8f}")
P(""); P("="*112); P("4. what this does to the numbers that were flagged provisional"); P("="*112)
info("the ~5 sigma external-field-SLOPE negative (cluster-infall BTFR, Local Volume dwarfs) was computed with the naive")
info("nu(x_e) coupling.  A slope is d/dln(x_e) of the log of the coupling, so what matters is not the coupling's VALUE but")
info("how its LOGARITHM runs with x_e.  Compute both:")
info(f"{'x_e':>9} {'dln[nu]/dln x':>15} {'dln[nu(1+L/3)]/dln x':>22} {'dln[nu(1+L)]/dln x':>20}")
def dln(f, x, d=1e-4): return (math.log(f(x*(1+d))) - math.log(f(x*(1-d))))/(2*d)
S3 = {}
for xe in (1e-3, 1e-2, 0.1, 0.3, 1.0):
    a = dln(lambda z: nu_s2(z), xe)
    b = dln(lambda z: nu_s2(z)*(1 + L_of(z)/3), xe)
    c = dln(lambda z: nu_s2(z)*(1 + L_of(z)), xe)
    S3[xe] = (a, b, c); info(f"{xe:9.4f} {a:15.4f} {b:22.4f} {c:20.4f}")
worst = max(abs(S3[x][1]/S3[x][0] - 1) for x in S3 if abs(S3[x][0]) > 1e-6)
ck("A4 (AGAINST THE FRAMEWORK'S INTEREST) the sphere-averaged correction barely changes the predicted SLOPE, which is the quantity the ~5 sigma negative measures: dln(coupling)/dln(x_e) moves by under 25% across the whole range, so the negative does NOT dissolve into it",
   worst < 0.25, f"worst fractional change in the predicted slope = {100*worst:.1f}%; e.g. at x_e = 0.1 the naive slope is {S3[0.1][0]:+.4f} and the sphere-averaged one {S3[0.1][1]:+.4f}")
P(""); P("="*112); P("VERDICT"); P("="*112)
P("  The flux theorem is right and the factor it implies is real, but it was attached to the wrong observable, and this")
P("  script corrects the correction.  nu(1 + L) is the coupling PARALLEL to the external field, and in the deep limit")
P("  that is indeed half of nu.  An isotropic velocity dispersion, and any sphere-averaged enclosed mass, measure the")
P("  ANGLE AVERAGE instead, and the numerical quadrature says that is nu(1 + L/3) = 0.83 nu deep -- a 17% reduction, not")
P("  a factor 2.  So the pressure-supported liabilities shrink by about 0.08 dex, not by 0.3, and the external-field")
P("  SLOPE negative shrinks hardly at all, because a slope depends on how the coupling's logarithm runs and not on its")
P("  value.  REPORTED AGAINST INTEREST: I flagged that ~5 sigma negative as provisional on a factor 2, and by this")
P("  calculation the factor that applies to it is not 2.  The negative stands until the correction run says otherwise")
P("  on the measurement side, and the caveat I attached to the liability table is too generous to the framework.")
sys.exit(ck.done())
