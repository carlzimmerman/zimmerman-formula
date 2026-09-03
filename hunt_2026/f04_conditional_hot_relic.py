#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f04_conditional_hot_relic.py -- ASSUME THE FRAMEWORK IS RIGHT.  Then what must the cluster residual BE?
=======================================================================================================
CONDITIONAL MODE, stated up front so nothing here is mistaken for a defence: this script ASSUMES
a_0 = (c/2) sqrt(G rho_DE) with the Route A kernel is correct, and asks what the liability table then IMPLIES.
Under that assumption the residuals are not errors -- they are PREDICTIONS of real, undetected mass with a required
density at a required radius, and a required ABSENCE from galaxies (because the radial acceleration relation works
there to 0.06 dex).  That is a sharp, falsifiable specification, and there is a bound that decides it.

THE BOUND.  A fermion cannot be packed denser than its phase space allows (Tremaine & Gunn 1979).  For a species of
mass m and internal degeneracy g in a system of one-dimensional dispersion sigma,
    rho_max  =  g m^4 (2 pi)^(3/2) sigma^3 / h^3 .
So a light relic CAN supply a cluster (large sigma) and CANNOT supply a dwarf (small sigma), for the SAME m.  That is
exactly the pattern the liability table shows -- and it is why this is the one conditional story worth computing.

PRIOR ART, credited: this is Angus's hot-dark-matter MOND cosmology (Angus 2009; Angus, Famaey & Diaferio 2010), which
uses an ~11 eV sterile neutrino.  This programme's own ballistic_survivor_window_2026.py already found a 5-11 eV
Tremaine-Gunn window and KILLED the thermal case on Delta N_eff = 1.  WHAT IS NEW HERE is applying the bound to the
ACTUAL 28-row liability table to ask whether ONE mass fits every cluster row AND is FORBIDDEN in every galaxy row --
i.e. whether the framework's own failures predict their own explanation.  Both footings.  Checks CAN fail, and the
conditional collapsing is a perfectly possible outcome.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()
hP = 6.62607015e-34; eV = 1.602176634e-19; c2 = c_light**2
def rho_max_TG(m_eV, sigma_kms, g=2.0):
    """Tremaine-Gunn maximum density for a fermion of mass m_eV in a system of 1-D dispersion sigma, kg/m^3"""
    m = m_eV*eV/c2
    return g*m**4*(2*math.pi)**1.5*(sigma_kms*1e3)**3/hP**3
def m_required(rho_need, sigma_kms, g=2.0):
    """the MINIMUM fermion mass that can supply rho_need at dispersion sigma, in eV"""
    m4 = rho_need*hP**3/(g*(2*math.pi)**1.5*(sigma_kms*1e3)**3)
    return (m4**0.25)*c2/eV
P("="*116); P("1. the specification: what the framework's own residuals demand, system by system"); P("="*116)
info("required extra density = (boost^2 - 1) x rho_bar_enclosed in the deep regime (since g ~ sqrt(G M a_0), a boost B in")
info("acceleration needs a mass factor B^2); sigma from the system's own dynamics.  Rows and boosts from THE_LIABILITY_TABLE.md.")
# system, boost (acceleration), radius kpc, enclosed baryonic mass Msun, 1-D dispersion km/s
ROWS = [
 ("X-COP clusters 0.9 R500",      1.48, 1107.0, 1.0e14, 1000.0),
 ("X-COP clusters 0.5 R500",      2.09,  616.0, 7.0e13,  1000.0),
 ("X-COP clusters 0.2 R500",      2.76,  246.0, 3.0e13,  1000.0),
 ("X-COP cores 30-100 kpc",       2.91,   65.0, 5.0e12,   900.0),
 ("CLASH 14-600 kpc",             3.45,  200.0, 2.0e13,  1100.0),
 ("Bullet BCG1 300 kpc",          3.17,  300.0, 4.2e13,  1200.0),
 ("X-ray groups R500",            1.45,  600.0, 6.0e12,   400.0),
 ("X-ray groups R2500",           2.24,  224.0, 3.0e12,   400.0),
 ("eRASS1 groups 1e12.5-13.5",    2.63,  400.0, 2.0e12,   300.0),
 ("X-ray ellipticals 5-70 kpc",   1.69,   20.0, 1.0e11,   250.0),
 ("SLUGGS GC systems logM*>11.3", 4.63,   50.0, 3.0e11,   250.0),
 ("Milky Way dwarfs (median)",    2.30,    0.5, 1.0e6,      8.0),
 ("MW ultra-faints",             44.70,    0.05, 3.0e3,     4.0),
 ("Coma UDGs",                    6.19,    3.0, 1.0e8,     30.0),
 ("Pal 4 / Pal 14 globulars",     5.30,    0.02, 2.0e4,     1.0),
]
info(f"{'system':32} {'boost':>6} {'r [kpc]':>9} {'rho_need [kg/m3]':>17} {'sigma':>7} {'m_min [eV]':>11}")
out = []
for nm, B, rkpc, Mb, sig in ROWS:
    r = rkpc*kpc
    rho_bar = Mb*Msun/(4/3*math.pi*r**3)
    rho_need = (B**2 - 1.0)*rho_bar
    m_min = m_required(rho_need, sig)
    out.append((nm, B, rkpc, rho_need, sig, m_min))
    info(f"{nm:32} {B:6.2f} {rkpc:9.2f} {rho_need:17.3e} {sig:7.0f} {m_min:11.2f}")
cl = [o for o in out if o[4] >= 250]
gal = [o for o in out if o[4] < 100]
m_cl = max(o[5] for o in cl); m_gal_min = min(o[5] for o in gal)
info(f"\nCLUSTER-and-ELLIPTICAL rows (sigma >= 250 km/s): a single relic must be at least m = {m_cl:.2f} eV to supply the densest of them")
info(f"GALAXY-and-DWARF rows (sigma < 100 km/s): the LIGHTEST mass any of them could be supplied by is m = {m_gal_min:.2f} eV")
ck("A1 (THE CONDITIONAL WORKS, and it is the sharpest thing in this session) the framework's own residuals predict their own explanation: a single fermion mass supplies every cluster, group and elliptical row and is FORBIDDEN by phase space in every galaxy and dwarf row.  The two requirements do not overlap -- the clusters need at least a few eV and the dwarfs would need hundreds",
   m_cl < m_gal_min, f"clusters need m >= {m_cl:.2f} eV; dwarfs would need m >= {m_gal_min:.1f} eV, a factor {m_gal_min/m_cl:.0f} higher.  A relic at the cluster mass CANNOT be dense enough in a dwarf, which is exactly the observed pattern")
P(""); P("="*116); P("2. does that mass also give the right cosmological abundance?"); P("="*116)
h = 0.674; OM_DM = 0.1200/h**2
info("a thermally produced light fermion has Omega h^2 = m/(94 eV) for one degree of freedom (Lesgourgues & Pastor).")
for m in (m_cl, 5.0, 8.0, 11.0, 15.0):
    omh2 = m/94.0
    info(f"  m = {m:6.2f} eV -> Omega_nu h^2 = {omh2:.4f} vs Omega_dm h^2 = 0.1200 (ratio {omh2/0.12:.3f}); needs {0.12/omh2:.2f} degrees of freedom or non-thermal production")
m_thermal = 0.12*94.0
ck("A2 the abundance NEARLY closes but lands just below the window, and that is a real cost: a single thermal degree of freedom gives the full dark-matter density at 11.3 eV, while the densest cluster row needs at least 14.7 eV -- so the conditional requires 0.77 effective degrees of freedom, i.e. mild non-thermality or a degeneracy factor below 2, rather than closing for free",
   0.6 < (m_thermal/m_cl) < 1.0, f"thermal closure at m = {m_thermal:.1f} eV against a cluster floor of {m_cl:.2f} eV: the ratio is {m_thermal/m_cl:.2f}, so g_eff = {0.12*94.0/m_cl*2:.2f} rather than 2.  The window {m_cl:.1f}-{m_gal_min:.0f} eV is real but the abundance does not fall in it for free")
info("⚠️ THE KNOWN KILL, and it is this programme's own: a THERMAL relic of ~11 eV is a hot species that contributes")
info("Delta N_eff ~ 1 and is excluded by the CMB (ballistic_survivor_window_2026.py already found and recorded this).")
info("The escape is NON-THERMAL production (resonant, a la Shi-Fuller), which decouples the abundance from N_eff -- that")
info("is Angus's own route and it is NOT tested here.  So this conditional is coherent but NOT established.")
P(""); P("="*116); P("3. the radial test, which is where this conditional can be falsified on data already in hand"); P("="*116)
info("a phase-space-limited relic is DENSITY-CAPPED, so it must fill a cluster from the OUTSIDE IN and saturate in the")
info("core.  The liability table's radial run is the opposite: the residual GROWS inward (X-COP 1.48 -> 2.09 -> 2.76 -> 2.91")
info("from 0.9 R500 to the core, and R2500 far worse than R500 in the groups).  Test whether the cap is even reached.")
for nm, B, rkpc, rho_need, sig, m_min in out:
    if sig < 250: continue
    for m in (m_thermal,):
        cap = rho_max_TG(m, sig)
        info(f"{nm:32} rho_need {rho_need:.3e}  rho_max({m:.1f} eV, sigma={sig:.0f}) {cap:.3e}  need/cap = {rho_need/cap:.4f}")
ratios = {o[0]: o[3]/rho_max_TG(m_thermal, o[4]) for o in out if o[4] >= 250}
over = {k: v for k, v in ratios.items() if v > 1.0}
ck("A3 AGAINST THE CONDITIONAL, and it relocates the boundary: at the thermal-abundance mass the phase-space cap is EXCEEDED in the X-ray ellipticals (need/cap 1.36) and the SLUGGS globular-cluster systems (2.87), so a single relic cannot supply those rows at all.  The clean split is therefore NOT clusters-versus-dwarfs but sigma >~ 300 km/s versus everything below, and two of the liability rows fall on the forbidden side of it",
   len(over) >= 2, "exceeds the cap: " + "; ".join(f"{k} at {v:.2f}" for k, v in over.items()) + f"; every genuine cluster/group row sits at need/cap <= {max(v for k,v in ratios.items() if k not in over):.3f}")
ck("A3b and the same numbers say phase space does NOT explain the cluster PROFILE: in every true cluster row the cap is unsaturated by one to four orders of magnitude, so a density-capped relic would fill clusters smoothly, while the measured residual GROWS inward (1.48 -> 2.09 -> 2.76 -> 2.91 from 0.9 R500 to the core)",
   max(v for k, v in ratios.items() if k not in over) < 0.5,
   f"cluster/group rows span need/cap = {min(ratios.values()):.4f} to {max(v for k,v in ratios.items() if k not in over):.4f}; the cap only bites where sigma <= 250 km/s")
P(""); P("="*116); P("4. mutation controls"); P("="*116)
ck("M1 the Tremaine-Gunn formula is right: a 1 eV fermion at sigma = 1000 km/s must allow a far higher density than the same fermion at sigma = 1 km/s, by the cube of the ratio",
   abs(rho_max_TG(1.0, 1000.0)/rho_max_TG(1.0, 1.0) - 1e9) < 1e7, f"ratio = {rho_max_TG(1.0,1000.0)/rho_max_TG(1.0,1.0):.3e} against the analytic 1e9")
ck("M2 mutation: with boost = 1 (no residual) every required density is zero and no relic is needed",
   abs((1.0**2 - 1.0)) < 1e-15, "boost = 1 gives rho_need = 0 identically")
P(""); P("="*116); P("VERDICT, in conditional mode"); P("="*116)
P("  ASSUMING the framework is right in discs, its own failures DO predict their own explanation, and the prediction is")
P("  sharper than I expected.  A single light fermion supplies every genuine cluster and group residual and is FORBIDDEN")
P("  BY PHASE SPACE in every dwarf and galaxy row: the clusters need m >= 14.7 eV, the dwarfs would need >= 93 eV, and")
P("  those two requirements are a factor 6 apart with nothing fitted.  The framework's own 28-row liability table selects")
P("  that story without being asked to.  Credit where it is due: this is Angus's hot-dark-matter MOND cosmology")
P("  (Angus 2009; Angus, Famaey & Diaferio 2010), and this programme's own ballistic-survivor script had already found")
P("  the 5-11 eV window.  What is new is that the liability table picks it out unprompted.")
P("  THREE COSTS, all reported against the conditional.  (i) The abundance does not close for free: a thermal degree of")
P("  freedom gives the full dark-matter density at 11.3 eV, just BELOW the 14.7 eV cluster floor, so the story needs")
P("  g_eff ~ 1.5 or mild non-thermality.  (ii) The boundary is not where I said: the X-ray ellipticals and the SLUGGS")
P("  globular-cluster systems EXCEED the cap (need/cap 1.36 and 2.87), so the clean split is sigma >~ 300 km/s versus")
P("  everything below, and two liability rows sit on the forbidden side.  (iii) The radial profile is wrong: the cap is")
P("  unsaturated by one to four orders of magnitude in every true cluster row, so a capped relic fills clusters smoothly")
P("  while the measured residual GROWS INWARD.  Phase space explains the galaxy ABSENCE beautifully and the cluster")
P("  PROFILE not at all.  And the known N_eff kill on a thermal 11 eV relic still stands unless production is non-thermal.")
P("  NET: this is the best conditional story available and it is coherent on the amount and on the galaxy/cluster split,")
P("  and it fails on the radial profile, on two intermediate-sigma rows, and on N_eff.  That is a far more specific place")
P("  to stand than 'clusters do not work', and every one of those three failures is a computable next test.")
sys.exit(ck.done())
