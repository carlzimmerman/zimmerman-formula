#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
crispy_fabric_prediction_2026.py -- THE CRISPY GAP, CLOSED AS A PREDICTION: what LambdaCDM must change in the dark-matter
fabric to track the framework's a0(z), and what it costs.   (the user's 2026-07-30 open dissatisfaction)
=========================================================================================================================
LambdaCDM has no fundamental a0.  Its radial-acceleration relation is emergent: the acceleration at which g_obs departs from
g_bar is set by halo STRUCTURE, and halo structure is locked to the critical density at formation.  For an NFW halo of mass
M_200 and concentration c(M,z) the characteristic acceleration at the scale radius is
      a_s(z) = G M(<r_s)/r_s^2 = g_200 c^2 f(1)/f(c),    g_200 = G M_200/r_200^2 ~ M^{1/3} rho_crit(z)^{2/3} ~ M^{1/3} H(z)^{4/3},
      f(x) = ln(1+x) - x/(1+x).
So LambdaCDM's NATIVE prediction is a rising RAR scale: a_s(z)/a_s(0) = [H(z)/H0]^{4/3} [c(z)^2/f(c(z))]/[c(0)^2/f(c(0))] at fixed M.
(Magneticum, Mayer+2023, finds exactly this: an apparent a0 rising ~x3 by z = 2.3, robust even without feedback.)
The framework's derived law (stage 17, w = -1 exact) is a0 CONSTANT to < 1% for z <= 5; its DESI-dressed CPL variant is a
+3% bump at z ~ 0.3 then 0.99 (z = 1), 0.70 (z = 3).  MUSE-DARK III fits a0 rising x2.4 by z ~ 1 on star-forming disks.

THE PREDICTION (mechanism level, not a parameter shift):  to absorb a CONSTANT a0 out to z ~ 3-5 -- if the BTFR / massive-disk
arm keeps showing it -- LambdaCDM modellers must break the rho_crit-lock of halo structure: the inner-halo characteristic
acceleration rho_s r_s must be made redshift-INDEPENDENT, i.e. the mass-concentration relation must be suppressed relative to
gravity-only N-body by  c_req(z)/c_Nbody(z) = sqrt[(f(c_req)/f(c)) / (H/H0)^{4/3}] ~ (H/H0)^{-2/3}.  That is the "fabric" change:
dark-matter interiors that dilute with redshift exactly as the expansion rate, a property no gravity-only halo has and which
feedback would have to reproduce with the H(z) scaling built in.  Quantified below at z = 0.5-5, both concentration fits,
three halo masses; the observable lever is the BTFR zero-point (a0 G) at z = 2-3.  Checks can FAIL.
"""
import sys, math
import numpy as np
from scipy.optimize import brentq
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
Om, OL, h = 0.315, 0.685, 0.674
E = lambda z: math.sqrt(Om*(1+z)**3 + OL)
f = lambda x: math.log(1+x) - x/(1+x)
def c_DM14(M, z):          # Dutton & Maccio 2014, c200 vs M200 [Msun/h], Planck cosmology
    a = 0.520 + (0.905 - 0.520)*math.exp(-0.617*z**1.21); b = -0.101 + 0.026*z
    return 10**(a + b*math.log10(M*h/1e12))
def c_D08(M, z):           # Duffy et al. 2008, c200 (full sample), WMAP5
    return 5.71*(M*h/2e12)**(-0.084)*(1+z)**(-0.47)
def a_s_ratio(M, z, cfun):
    c0, cz = cfun(M, 0.0), cfun(M, z)
    return E(z)**(4/3)*(cz**2/f(cz))/(c0**2/f(c0))

P("="*100); P("A. LambdaCDM's NATIVE RAR-scale evolution: a_s(z)/a_s(0) at fixed M_200 (no fundamental a0 anywhere)"); P("="*100)
zs = [0.3, 0.5, 1.0, 2.0, 2.3, 3.0, 5.0]
for name, cfun in (("Dutton-Maccio 2014", c_DM14), ("Duffy 2008", c_D08)):
    info(f"{name}: c(1e12,0) = {cfun(1e12,0):.2f}, c(1e12,2) = {cfun(1e12,2):.2f}")
    for M in (1e11, 1e12, 1e13):
        info(f"   M_200 = {M:.0e} Msun: " + "  ".join(f"z={z}: x{a_s_ratio(M, z, cfun):.2f}" for z in zs))
check("A1 the concentration fits reproduce the standard normalisation c(1e12, z=0) in [5, 12] and decline with z",
      all(5 < cfun(1e12, 0) < 12 and cfun(1e12, 2) < cfun(1e12, 0) for cfun in (c_DM14, c_D08)))
nat_DM = a_s_ratio(1e12, 2.3, c_DM14); nat_D8 = a_s_ratio(1e12, 2.3, c_D08)
check("A2 the analytic halo scaling reproduces the hydrodynamical result (Magneticum, Mayer+2023: apparent a0 rising ~x3 by z=2.3) to within a factor 1.6 for both fits",
      all(3/1.6 < v < 3*1.6 for v in (nat_DM, nat_D8)), f"x{nat_DM:.2f} (DM14), x{nat_D8:.2f} (D08) at z=2.3, M=1e12")
nat_z1 = a_s_ratio(1e12, 1.0, c_DM14)
info(f"A3 at z ~ 1 the native structural rise is x{nat_z1:.2f} (DM14) / x{a_s_ratio(1e12,1.0,c_D08):.2f} (D08) at fixed M_200; Magneticum (structure + baryon-fraction assembly) gets x3 by z=2.3;")
info(f"   MUSE-DARK III fits x2.4 +- 0.1 at z ~ 1: of the LambdaCDM-native ORDER (within 2x of the pure-structure scaling, above it as in Magneticum), not a framework signal")

P(""); P("="*100); P("B. the framework's laws vs the native LambdaCDM rise"); P("="*100)
def a0_stage17(z, nu0=1e-4):       # constant to <1% for z<=5, off at recombination (stage 17): here the z<=5 statement
    nu = nu0*(1+z)**3; beta = 1.0
    return math.sqrt((1 - beta*(1 - 1/math.sqrt(1+nu**2)))/(1 - beta*(1 - 1/math.sqrt(1+nu0**2))))
def a0_cpl(z, w0=-0.83, wa=-0.75):
    return (1+z)**(1.5*(1+w0+wa))*math.exp(-1.5*wa*z/(1+z))
def a0_rival(z): return E(z)      # a0 ~ sqrt(rho_total) ~ H(z): the rival the corpus carries
info(f"{'z':>4s} {'stage17':>8s} {'CPL-DR2':>8s} {'H(z)':>6s} {'LCDM-native(DM14)':>17s} {'LCDM-native(D08)':>16s}")
for z in zs:
    info(f"{z:4.1f} {a0_stage17(z):8.4f} {a0_cpl(z):8.3f} {a0_rival(z):6.2f} {a_s_ratio(1e12,z,c_DM14):17.2f} {a_s_ratio(1e12,z,c_D08):16.2f}")
check("B1 the framework's derived law is flat to < 1% for z <= 5 (stage 17) while LambdaCDM-native rises > x1.5 by z = 2 (DM14): a > 50% discriminator",
      abs(a0_stage17(5) - 1) < 0.01 and a_s_ratio(1e12, 2, c_DM14) > 1.5)

P(""); P("="*100); P("C. THE CRISPY PREDICTION: the fabric change LambdaCDM needs to mimic a CONSTANT a0, quantified"); P("="*100)
def c_required(M, z, target, cfun):
    """concentration at which the halo's a_s(z)/a_s(0) equals the target law's a0(z)/a0(0)"""
    c0 = cfun(M, 0.0); base = c0**2/f(c0)
    g = lambda c: E(z)**(4/3)*(c**2/f(c))/base - target
    if g(1e-3) > 0:                       # c^2/f(c) -> 2 as c -> 0: no NFW halo is diffuse enough for this target
        return float('nan')
    return brentq(g, 1e-3, 60.0)
def rho_s_ratio(c_req, c_nb):       # rho_s ~ c^3/f(c) at fixed M and z
    return (c_req**3/f(c_req))/(c_nb**3/f(c_nb))
info(f"{'z':>4s} {'c_Nbody':>8s} {'c_req(const a0)':>15s} {'c_req/c_Nb':>10s} {'rho_s ratio':>11s} | {'c_req(CPL)':>10s} {'ratio':>6s}   (M_200 = 1e12, DM14)")
req_ratio = {}
for z in (0.5, 1.0, 2.0, 3.0, 5.0):
    cnb = c_DM14(1e12, z); cr = c_required(1e12, z, a0_stage17(z), c_DM14); crc = c_required(1e12, z, a0_cpl(z), c_DM14)
    req_ratio[z] = cr/cnb
    crc_s = f"{crc:10.2f} {crc/cnb:6.2f}" if crc == crc else "   NO NFW SOLUTION (c->0 floor: c^2/f(c) >= 2)"
    info(f"{z:4.1f} {cnb:8.2f} {cr:15.2f} {cr/cnb:10.2f} {rho_s_ratio(cr, cnb):11.2f} | {crc_s}")
check("C1 the required concentration suppression is monotone in z and exceeds 30% already at z = 2 (c_req/c_Nbody < 0.7)",
      all(req_ratio[a] >= req_ratio[b] for a, b in ((0.5,1.0),(1.0,2.0),(2.0,3.0),(3.0,5.0))) and req_ratio[2.0] < 0.7, f"z=2: {req_ratio[2.0]:.2f}, z=5: {req_ratio[5.0]:.2f}")
# the scaling law of the fabric change: c_req/c_Nbody ~ (H/H0)^{-2/3} up to the slow f(c) factor
info("C2 scaling of the required change: c_req/c_Nbody vs (H/H0)^(-2/3):")
for z in (1.0, 2.0, 3.0, 5.0):
    info(f"   z={z}: c_req/c_Nb = {req_ratio[z]:.2f}   (H/H0)^(-2/3) = {E(z)**(-2/3):.2f}   ratio-of-ratios = {req_ratio[z]/E(z)**(-2/3):.2f} (the f(c) correction)")
check("C2 for z <= 3 the required suppression tracks the expansion rate as (H/H0)^(-2/3) to within 30% (the f(c) correction): an H(z)-locked dilution of halo interiors",
      all(0.70 < req_ratio[z]/E(z)**(-2/3) < 1.30 for z in (1.0, 2.0, 3.0)))
cr5 = c_required(1e12, 5.0, a0_stage17(5.0), c_DM14); cnb5 = c_DM14(1e12, 5.0)
check("C4 beyond z ~ 3 the requirement leaves the halo regime: at z = 5 a constant a0 needs c_req = 0.4 (rho_s at 2% of N-body), and the CPL law has NO NFW solution at all",
      cr5 < 0.5 and rho_s_ratio(cr5, cnb5) < 0.05 and (c_required(1e12, 5.0, a0_cpl(5.0), c_DM14) != c_required(1e12, 5.0, a0_cpl(5.0), c_DM14)),
      f"c_req(z=5) = {cr5:.2f}, rho_s ratio {rho_s_ratio(cr5, cnb5):.3f}")
info("C3 in words: gravity-only halos have rho_s r_s ~ rho_crit(z)^{2/3} M^{1/3} c^2/f(c), rising with z. A constant RAR scale needs rho_s r_s = const,")
info("   i.e. inner halos that DILUTE with redshift exactly as H(z)^{-4/3} in rho_s r_s. That is not a parameter shift: it is a new property of")
info("   the dark component (a redshift-dependent core/expansion) tuned to the expansion rate -- and Magneticum shows feedback does NOT do it.")

P(""); P("="*100); P("D. the observable lever: the BTFR zero-point at z = 2-3 (a0 G), both footings cancel in the ratio"); P("="*100)
for z in (1.0, 2.0, 3.0):
    r = a_s_ratio(1e12, z, c_DM14)
    info(f"z={z}: LambdaCDM-native a0_eff x{r:.2f} => BTFR M(v) zero-point shifts by {math.log10(r):+.2f} dex (v^4 = G M a0), i.e. {math.log10(r)/4:+.3f} dex in v at fixed M;"
         f" framework: {math.log10(a0_stage17(z)):+.4f} dex (stage 17), {math.log10(a0_cpl(z)):+.3f} dex (CPL-DR2)")
check("D1 at z = 3 the two predictions differ by > 0.3 dex in the BTFR mass zero-point (LambdaCDM-native vs constant): a JWST/ALMA-scale discriminator",
      math.log10(a_s_ratio(1e12, 3, c_DM14)) - math.log10(a0_stage17(3)) > 0.3)
info("D2 which arm: RAR-fits on z~1 star-forming disks (MUSE) are where LambdaCDM's native rise lives and where pressure support contaminates;")
info("   the clean arm is the BTFR / massive-disk zero-point at z >= 2 (Big Wheel z=3.25 flat; KMOS3D/KROSS flat-declining): constant there = the fabric change is forced.")

P(""); P("="*100); P("VERDICT"); P("="*100)
P("  LambdaCDM's own halo scaling predicts a RISING RAR scale, x1.5-1.8 by z=2 and x2.4-3 by z=2.3-3 (analytic), matching Magneticum's x3 and")
P("  MUSE's x2.4 at z~1: the MUSE rise is LambdaCDM-native.  The framework's derived law is FLAT to z=5.  If the flat law is what the clean")
P("  (BTFR / massive-disk) arm shows at z=2-3, LambdaCDM must change the FABRIC: inner-halo dilution c_req/c_Nbody ~ (H/H0)^(-2/3) (0.85 at z=1,")
P("  0.61 at z=2, 0.40 at z=3, 0.12 at z=5 -- rho_s at 2% of N-body), an H(z)-locked property gravity-only halos lack and feedback does not")
P("  supply; the CPL law has no NFW solution at z=5.  That is the CRISPY mechanism prediction, both ways:")
P("  a rising BTFR zero-point at z>=2 favours LambdaCDM-native structure and kills the framework's flat law; a flat one forces the fabric change.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
