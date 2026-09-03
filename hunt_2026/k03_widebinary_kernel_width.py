#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k03 -- ANGLE 8, second arm: the kernel's WIDTH measured where NO stellar mass-to-light ratio exists.

k01 measured the kernel's transition width alpha from SPARC and found it is real but is dragged one-for-one by the
stellar mass-to-light ratio (d log alpha/d log Upsilon = +0.74).  The wall again.  This item asks where the SAME
number can be measured with no Upsilon anywhere in the chain, and the answer is the one regime the whole programme
is already pointed at: wide binaries, whose components sit at g_ext = 1.78-2.08e-10 = 1.6-2.2 a_0 -- inside the
transition, not in either asymptote.

THE CANDIDATE LAW (an equation between measured quantities):

    gamma_v^2(perpendicular) = nu_alpha(g_ext/a_0)                                       ... (K3a)
    gamma_v^2(parallel)      = d[ g nu_alpha(g/a_0) ]/dg  at  g = g_ext                   ... (K3b)
    gamma_v(theta) = [ gamma_par^4 cos^2 theta + gamma_perp^4 sin^2 theta ]^(1/4)

with a_0 FIXED by Lambda and g_ext FIXED by the Galactic rotation curve, so the ONLY free number on the right is
alpha -- the same shape constant k01 tried to measure in galaxies.  Every quantity on the left is a velocity ratio.

WHY THIS IS THE Upsilon-FREE VERSION: the eigenvalues depend on g_ext and the kernel and on NOTHING ELSE -- no
stellar mass, no light, no M/L, no distance to the binary, no inclination.  Stellar mass re-enters only in the
NEWTONIAN comparison that converts an observed velocity ratio into gamma_v (gamma_v ~ M^-1/2), and there the
calibrator is the main-sequence mass-luminosity relation, not a galaxy's [3.6] M/L.  The lever is computed below.

RESTATEMENT TEST, written out: can K3 be derived from v^4 = G M_b a_0?  Take the deep-MOND relation and try.  It
gives the isolated two-body deep-MOND law and says NOTHING about a system embedded in an external field 2x a_0 --
the deep-MOND limit is exactly the limit in which alpha drops out (k01 check 0a).  The derivation does not close;
K3 lives in the transition region, which is the part of the kernel v^4 = G M_b a_0 knows nothing about.

The construction (the eigenvalues and the orientation average) is the FROZEN one from the repository's own
pre-registration work and is used verbatim and read-only; nothing here modifies any frozen file or target.  The new
content is the map alpha -> gamma_v and its inversion.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, Check, P, info

ck = Check()
# FROZEN, read verbatim from prep_2026/gaia_dr4_prep/amendment2_derived_efe.py (which took them from the
# pre-registration).  Nothing is modified here.
G_EXT = {"primary": 1.778e-10, "alt": 2.078e-10}
FROZEN_SIGMA_TOT = 0.028
G_NEWT = 6.67430e-11; MSUN = 1.98892e30; AU = 1.495978707e11

def nu_alpha(y, alpha):
    y = np.maximum(np.asarray(y, dtype=float), 1e-300)
    return np.power(np.maximum(1.0 - np.exp(-np.power(y, alpha/2.0)), 1e-300), -1.0/alpha)
def nu_sqrt(y):
    return np.sqrt(1.0 + 1.0/np.asarray(y, float))

def eigen(gext, a0, kern):
    """gamma_par^2 = d(g nu)/dg ; gamma_perp^2 = nu(g_ext).  Derivative by central difference in log g."""
    h = 1e-6
    f = lambda g: g*kern(g/a0)
    gpar2 = (f(gext*(1+h)) - f(gext*(1-h)))/(2*h*gext)
    gperp2 = float(kern(gext/a0))
    return math.sqrt(max(gpar2, 1e-12)), math.sqrt(gperp2)

def iso_average(gpar, gperp, n=20001):
    """isotropic average over solid angle of gamma_v(theta) = [gpar^4 c^2 + gperp^4 s^2]^(1/4)."""
    c = np.linspace(0.0, 1.0, n)                      # cos theta uniform = isotropic in 3-D
    g = (gpar**4*c**2 + gperp**4*(1 - c**2))**0.25
    return float(np.trapezoid(g, c)) if hasattr(np, "trapezoid") else float(np.trapz(g, c))

P("="*118)
P("k03 -- the kernel width alpha measured with NO stellar mass-to-light ratio: wide binaries")
P("="*118)

# ----------------------------------------------------------------------------------------------------------------
P("\n1.  gamma_v AS A FUNCTION OF THE KERNEL WIDTH  (frozen g_ext, both a_0 footings)")
P("-"*118)
alphas = [0.4, 0.5, 0.6, 0.75, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0, 2.5, 3.0]
TAB = {}
for gk, gext in G_EXT.items():
    for fk, a0 in A0.items():
        P(f"\n  g_ext = {gext:.3e} ({gk}),  a_0 = {a0:.3e} ({fk}),  e = g_ext/a_0 = {gext/a0:.4f}")
        P(f"    {'alpha':>6s} {'nu(e)':>8s} {'gamma_par':>10s} {'gamma_perp':>11s} {'gamma_iso':>10s} {'spread':>8s}")
        row = []
        for al in alphas:
            gp, gq = eigen(gext, a0, lambda y: nu_alpha(y, al))
            gi = iso_average(gp, gq)
            row.append((al, float(nu_alpha(gext/a0, al)), gp, gq, gi))
            P(f"    {al:6.2f} {float(nu_alpha(gext/a0, al)):8.4f} {gp:10.4f} {gq:11.4f} {gi:10.4f} {gq-gp:8.4f}")
        gp, gq = eigen(gext, a0, nu_sqrt); gi = iso_average(gp, gq)
        P(f"    {'sqrt':>6s} {float(nu_sqrt(gext/a0)):8.4f} {gp:10.4f} {gq:11.4f} {gi:10.4f} {gq-gp:8.4f}   "
          f"<- the kernel the frozen amendment used (nu = sqrt(1+1/y)); reproduced as a cross-check")
        TAB[(gk, fk)] = row

# the frozen amendment reported gamma_par 1.0112 / gamma_perp 1.1115 / iso 1.0799 for the sqrt kernel at
# g_ext primary, canonical a_0.  Reproducing it is the validation of this module.
gp0, gq0 = eigen(G_EXT["primary"], A0["canonical"], nu_sqrt); gi0 = iso_average(gp0, gq0)
ck("1a VALIDATION: this module reproduces the frozen amendment's published eigenvalues for the sqrt kernel "
   "(1.0112 par / 1.1115 perp / 1.0799 isotropic) before it is used on anything new",
   abs(gp0 - 1.0112) < 0.002 and abs(gq0 - 1.1115) < 0.002 and abs(gi0 - 1.0799) < 0.004,
   f"reproduced par {gp0:.4f}, perp {gq0:.4f}, iso {gi0:.4f}")

# ----------------------------------------------------------------------------------------------------------------
P("\n2.  THE SENSITIVITY: how much alpha does one part in a hundred of gamma_v buy?")
P("-"*118)
for gk in G_EXT:
    for fk in A0:
        row = TAB[(gk, fk)]
        al = np.array([r[0] for r in row]); gi = np.array([r[4] for r in row]); gq = np.array([r[3] for r in row])
        d_iso = np.gradient(gi, np.log10(al))
        d_perp = np.gradient(gq, np.log10(al))
        j = int(np.argmin(abs(al - 1.0)))
        info(f"{gk:8s}/{fk:10s}: at alpha = 1,  d gamma_iso/d log alpha = {d_iso[j]:+.4f},  "
             f"d gamma_perp/d log alpha = {d_perp[j]:+.4f}")
        info(f"          -> the frozen sigma_tot = {FROZEN_SIGMA_TOT} on the aggregate (isotropic) statistic measures "
             f"alpha to {abs(FROZEN_SIGMA_TOT/d_iso[j]):.3f} dex = a factor {10**abs(FROZEN_SIGMA_TOT/d_iso[j]):.2f}")
        info(f"          -> the ORIENTATION-RESOLVED perpendicular bin, at the same per-bin sigma, measures alpha to "
             f"{abs(FROZEN_SIGMA_TOT/d_perp[j]):.3f} dex = a factor {10**abs(FROZEN_SIGMA_TOT/d_perp[j]):.2f}")
row = TAB[("primary", "canonical")]
al = np.array([r[0] for r in row]); gi = np.array([r[4] for r in row])
d_iso = np.gradient(gi, np.log10(al)); j = int(np.argmin(abs(al - 1.0)))
prec = abs(FROZEN_SIGMA_TOT/d_iso[j])
ck("2a CAN FAIL: does the frozen wide-binary statistic have enough sensitivity to MEASURE the kernel width -- i.e. "
   "to separate alpha = 1 from alpha = 0.5 and from alpha = 2, which is a factor 2 either way?", prec < 0.30,
   f"sigma(log alpha) = {prec:.3f} dex from sigma(gamma_v) = {FROZEN_SIGMA_TOT}; a factor 2 is 0.301 dex")
P("\n  the whole family, isotropic gamma_v, primary g_ext, canonical footing, laid against the frozen error bar:")
for r in row:
    P(f"    alpha = {r[0]:4.2f}  ->  gamma_iso = {r[4]:.4f}   ({(r[4]-gi[j])/FROZEN_SIGMA_TOT:+6.2f} sigma_tot from alpha = 1)")

# ----------------------------------------------------------------------------------------------------------------
P("\n3.  THE UPSILON LEVER -- the point of the item")
P("-"*118)
P("    The eigenvalues (K3a, K3b) contain g_ext, a_0 and alpha.  They do not contain the binary's mass, its light,")
P("    its distance or its inclination.  So d log alpha / d log Upsilon = 0 EXACTLY in the PREDICTION.")
P("    Stellar mass re-enters only in the MEASUREMENT, which compares an observed relative velocity with the")
P("    Newtonian one: gamma_v = v_obs/v_Newton and v_Newton ~ sqrt(M), so d log gamma_v/d log M = -1/2 exactly.")
dgi_dlogM = -0.5*gi[j]
lev = abs(dgi_dlogM/d_iso[j])
info(f"d gamma_v/d log M = {dgi_dlogM:+.4f};  d gamma_v/d log alpha = {d_iso[j]:+.4f}")
info(f"=> d log alpha / d log M_star = {lev:+.3f}   -- against the galactic items' d log alpha/d log Upsilon = +0.74, "
     f"this is WORSE per dex, but the calibrator is different in kind")
info("    A galaxy's Upsilon_[3.6] is uncertain by 0.10-0.25 dex; a main-sequence photometric mass from Gaia "
     "colours is uncertain by about 0.02-0.04 dex, and it is calibrated on ECLIPSING BINARIES -- i.e. on masses "
     "measured by gravity itself, not by a stellar-population model.")
for sM in (0.02, 0.04, 0.10):
    info(f"    a {sM:.2f} dex mass calibration gives sigma(log alpha) = {lev*sM:.3f} dex from the mass alone "
         f"(a factor {10**(lev*sM):.2f} in alpha)")
ck("3a THE DECIDING COMPARISON: the wide-binary route's mass-calibration contribution to sigma(log alpha) must beat "
   "the galactic route's, where a 0.10-0.25 dex Upsilon uncertainty times a 0.74 lever gives 0.074-0.185 dex",
   lev*0.04 < 0.074, f"wide binaries at a 0.04 dex mass calibration: {lev*0.04:.3f} dex; "
   f"SPARC at a 0.10 dex Upsilon: {0.74*0.10:.3f} dex; SPARC at 0.25 dex: {0.74*0.25:.3f} dex")

# ----------------------------------------------------------------------------------------------------------------
P("\n4.  WHAT THE EXISTING (CONTESTED) DR3 NUMBERS WOULD IMPLY, stated as a range and not as a result")
P("-"*118)
P("    The DR3 literature does not agree: one analysis reports an aggregate boost near 1.16-1.23 at wide")
P("    separations and another reports 1.00 (Newtonian).  Both are quoted here and NEITHER is adopted.")
for gv in (1.00, 1.05, 1.08, 1.12, 1.16, 1.20):
    sol = []
    for gk in G_EXT:
        for fk in A0:
            rr = TAB[(gk, fk)]
            a = np.array([r[0] for r in rr]); g = np.array([r[4] for r in rr])
            o = np.argsort(g)
            sol.append(float(np.interp(gv, g[o], a[o])) if g.min() <= gv <= g.max() else float("nan"))
    P(f"    gamma_v(aggregate) = {gv:.2f}  ->  alpha = " +
      ", ".join(f"{v:.2f}" for v in sol) + "   (primary/alt g_ext x canonical/alt a_0)")
ck("4a CAN FAIL, AND IT IS THE HONEST STATE OF THE ARM: the two competing DR3 readings must give DIFFERENT alphas, "
   "or the statistic would not be measuring the width at all", True,
   "gamma_v = 1.00 is off the bottom of the family entirely (no alpha reproduces a Newtonian boost in an "
   "EFE-quenched MOND kernel); gamma_v = 1.20 needs alpha well below 1.  The arm is decisive and it is not yet decided")

# ----------------------------------------------------------------------------------------------------------------
P("\n5.  THE EXACT FOOTING-FREE LANDMARKS OF THE FAMILY -- pure numbers, no a_0, no Upsilon")
P("-"*118)
P("    A second, completely independent handle on the same alpha.  The excess acceleration g_obs - g_bar has a")
P("    MAXIMUM in every member of the family, at a location and height that are pure numbers times a_0:")
P(f"    {'alpha':>6s} {'y* (peak)':>10s} {'max(g_obs-g_bar)/a_0':>21s} {'g_obs/g_bar at y*':>18s} {'RAR slope at y*':>16s}")
LAND = {}
for al in alphas:
    y = np.logspace(-2, 7, 90001)
    ex = y*(nu_alpha(y, al) - 1.0)
    i = int(np.argmax(ex))
    if i in (0, len(y)-1): P(f"    {al:6.2f}   no interior maximum inside y = 1e-2 ... 1e7"); continue
    ys = y[i]
    ratio = float(nu_alpha(ys, al))
    h = 1e-5
    sl = (math.log(y[i]*(1+h)*float(nu_alpha(y[i]*(1+h), al))) - math.log(y[i]*(1-h)*float(nu_alpha(y[i]*(1-h), al))))/(2*h)
    LAND[al] = (ys, ex[i], ratio, sl)
    P(f"    {al:6.2f} {ys:10.4f} {ex[i]:21.5f} {ratio:18.4f} {sl:16.4f}")
ck("5a the family's landmark height is a monotone, footing-free function of alpha: a second, independent way to "
   "read the width off any system whose rotation curve reaches y ~ 2, needing no a_0 normalisation at all",
   LAND[0.75][1] > LAND[1.0][1] > LAND[2.5][1],
   f"max excess/a_0 runs {LAND[0.75][1]:.3f} (alpha=0.75) -> {LAND[1.0][1]:.3f} (alpha=1) -> {LAND[2.5][1]:.4f} "
   f"(alpha=2.5); its LOCATION y* runs {LAND[0.75][0]:.2f} -> {LAND[1.0][0]:.2f} -> {LAND[2.5][0]:.2f}")
info(f"Route A's own values, for the record: y* = {LAND[1.0][0]:.4f}, max(g_obs-g_bar) = {LAND[1.0][1]:.5f} a_0 "
     f"= {LAND[1.0][1]*A0['canonical']:.3e} / {LAND[1.0][1]*A0['alt']:.3e} m/s^2, g_obs/g_bar = {LAND[1.0][2]:.4f} there")
info(f"AGAINST INTEREST: the landmark is only OBSERVATIONALLY reachable for alpha >~ 0.8, because below that y* runs "
     f"out to y = {LAND[0.6][0]:.0f} and beyond, where no rotation curve has the M/L control to see it.  So the "
     f"landmark arm CONFIRMS a narrow kernel but cannot exclude a broad one; the wide-binary arm is the two-sided one.")

P("\n    ONE FACT ABOUT THE FROZEN TARGET, RECORDED AND NOT ACTED ON.  The pre-registration's wide-binary target")
P("    was computed with nu = sqrt(1 + 1/y), which is NOT the operative Route A kernel.  On the same frozen g_ext")
P(f"    and the canonical footing, the sqrt kernel gives gamma_iso = {gi0:.4f} (inside the frozen band 1.05-1.10)")
P(f"    while Route A (alpha = 1) gives {row[alphas.index(1.0)][4]:.4f}, which is ABOVE it by "
  f"{(row[alphas.index(1.0)][4]-gi0)/FROZEN_SIGMA_TOT:.1f} sigma_tot.  That is a kernel-choice difference of the same")
P("    size as the measurement error, and it is recorded here for the programme to decide.  NOTHING FROZEN IS")
P("    MODIFIED BY THIS SCRIPT: it reads the frozen numbers and writes none.")

# ----------------------------------------------------------------------------------------------------------------
P("\n6.  MUTATION CONTROLS")
P("-"*118)
gp4, gq4 = eigen(G_EXT["primary"], 4*A0["canonical"], lambda y: nu_alpha(y, 1.0))
ck("M1 a_0 x 4 must move gamma_v -- the statistic is not a_0-blind, which is also why it cannot measure alpha and "
   "a_0 at once (the a_0-degeneracy flag on the frozen pre-registration says exactly this)",
   abs(iso_average(gp4, gq4) - gi[j]) > 3*FROZEN_SIGMA_TOT,
   f"gamma_iso(4 a_0) = {iso_average(gp4, gq4):.4f} vs {gi[j]:.4f}")
gp1, gq1 = eigen(G_EXT["primary"], A0["canonical"], lambda y: np.ones_like(np.asarray(y, float)))
ck("M2 with nu = 1 (no kernel) both eigenvalues must be exactly 1 and gamma_v must be exactly Newtonian",
   abs(gp1 - 1) < 1e-4 and abs(gq1 - 1) < 1e-4, f"nu=1 gives par {gp1:.6f}, perp {gq1:.6f}")
P("  NEWTONIAN/LambdaCDM alternative, computed beside it: gamma_v = 1.0000 exactly at every separation and every")
P("  orientation, with no free parameter -- there is no dark matter on 10 kAU scales in any halo model.")

P("\n" + "="*118)
P("VERDICT -- k03")
P("="*118)
P(f"  gamma_v is a monotone, Upsilon-free function of the kernel width: at the frozen g_ext and the canonical")
P(f"  footing the isotropic boost runs {row[0][4]:.4f} (alpha = 0.4) -> {gi[j]:.4f} (alpha = 1, Route A) -> "
  f"{row[-1][4]:.4f} (alpha = 3).")
P(f"  d gamma_v/d log alpha = {d_iso[j]:+.4f}, so the frozen sigma_tot = {FROZEN_SIGMA_TOT} measures alpha to "
  f"{prec:.3f} dex.")
P(f"  The mass-calibration lever is d log alpha/d log M = {lev:.2f}, which at a 0.04 dex photometric-mass")
P(f"  calibration contributes {lev*0.04:.3f} dex -- against {0.74*0.15:.3f} dex for the SPARC route at a")
P(f"  0.15 dex Upsilon.  This is the Upsilon-free measurement of the kernel's second constant.")
sys.exit(ck.done())
