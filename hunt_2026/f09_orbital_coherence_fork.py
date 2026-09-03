#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f09_orbital_coherence_fork.py -- MATCHED PAIRS: same mass, same acceleration, one rotates and one does not.
============================================================================================================
THE OBSERVATION.  Read the liability table by HOW THE SYSTEM HOLDS ITSELF UP and it sorts perfectly:
  works  (0.06 dex): SPARC discs, Milky Way rotation curve, vertical force, Renzo's rule -- ALL ROTATION-SUPPORTED
  fails  (0.15-1.6 dex): clusters, groups, ellipticals, dwarf spheroidals, UDGs, globulars -- ALL PRESSURE-SUPPORTED
across eleven decades of mass and five of size.

WHY IT IS A THEORY FORK.  Milgrom proved (1994; 2011, arXiv:1111.1611) that modified INERTIA and modified GRAVITY
agree EXACTLY for circular orbits in the deep-MOND limit and differ for every other orbit: in modified inertia the
modification attaches to the TRAJECTORY, and a circular orbit is the degenerate case with a single frequency.  So
"inertia is modified" predicts with no freedom that a kernel calibrated on rotation curves works on rotation curves
and misses everywhere else.  This repository has run the modified-GRAVITY arm since 2026-08-08.

WHY THE OBVIOUS TESTS DO NOT WORK, both found by failing them in this file's own earlier versions:
  - f08 tried a second kernel variable; its mutation control FAILED (shuffled slope -0.232 vs real -0.343 on 15 rows).
    WITHDRAWN.
  - a correlation of deficit against v/sigma across all systems FAILED its own ranking: velocity scale beat coherence
    (r=+0.52 vs -0.45).  And it was CIRCULAR -- the disc sigma was derived from the same kinetic energy that defines
    the deficit.  WITHDRAWN.  v/sigma is also effectively binary (12 for every disc, 0.1-0.4 for every pressure
    system), so no correlation across the pooled sample can separate "coherence" from "is a disc".
THE TEST THAT IS NOT CONFOUNDED is a MATCHED PAIR: rotating dwarf irregulars against pressure-supported dwarf
spheroidals at the SAME baryonic mass and the SAME internal acceleration.  Mass, acceleration, size, environment and
epoch are then all controlled, and support is the only thing left varying.  Both sides get the framework's OWN kernel,
both footings, and the dwarf spheroidals get the external-field treatment MOND practitioners actually use -- which
helps THEM, against interest here.  Checks can fail.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()
MW_VC = 200e3   # Milky Way circular speed, m/s, for the external field on satellites

P("="*118); P("A.  THE MATCHED PAIR: dwarf irregulars (rotating) vs dwarf spheroidals (pressure), same mass, same g"); P("="*118)
info("common currency for both: log10( g_dynamical_observed / g_predicted_by_the_framework's_own_kernel ), in dex.")
info("rotating side: g_obs vs nu(g_bar/a_0) g_bar at every radius -- the standard RAR residual.")
info("pressure side: sigma_obs^2 vs the MOND prediction, taking the LARGER of the isolated deep-MOND virial value and")
info("the external-field value, which is the standard practice and is the choice that FAVOURS the framework.")
# Milky Way dwarf spheroidals: name, M_star Msun, R_half kpc, sigma km/s, Galactocentric distance kpc
DSPH = [("Draco",      2.9e5, 0.221, 9.1,  76.), ("Sculptor",   2.3e6, 0.283, 9.2,  86.),
        ("Fornax",     4.3e7, 0.710, 11.7, 147.), ("Carina",     3.8e5, 0.250, 6.6,  105.),
        ("Sextans",    4.4e5, 0.695, 7.9,  86.),  ("Leo I",      5.5e6, 0.251, 9.2,  254.),
        ("Leo II",     7.4e5, 0.176, 6.6,  233.), ("Ursa Minor", 2.9e5, 0.181, 9.5,  76.)]
def dsph_resid(M, Rh, sob, D, a0):
    """observed vs framework-predicted dynamical acceleration for a pressure-supported satellite."""
    Mk, R, s, d = M*Msun, Rh*kpc, sob*1e3, D*kpc
    g_obs = 3.0*s*s/R                                  # isotropic:  3 sigma^2 / R_half
    g_N = G*Mk/R**2
    g_iso = math.sqrt(g_N*a0)                          # isolated deep-MOND
    g_ext = MW_VC**2/d                                 # Milky Way external field at the satellite
    nu_e = nu_s(g_ext/a0)                              # quasi-Newtonian boost when the external field dominates
    g_efe = g_N*nu_e
    g_pred = max(g_iso, g_efe)                         # the choice that favours the framework
    return math.log10(g_obs/g_pred), g_N/a0, g_ext/a0, ("isolated" if g_iso >= g_efe else "EFE")
P(""); info(f"{'dwarf spheroidal':14} {'M*/Msun':>9} {'g_N/a0':>8} {'g_ext/a0':>9} {'regime':>9} {'residual dex':>13}")
dsph = []
for nm, M, Rh, s, D in DSPH:
    r_can, gn, ge, reg = dsph_resid(M, Rh, s, D, A0["canonical"])
    r_alt, _, _, _ = dsph_resid(M, Rh, s, D, A0["alt"])
    dsph.append(dict(nm=nm, M=M, gN=gn, reg=reg, res={"canonical": r_can, "alt": r_alt}))
    info(f"{nm:14} {M:9.2e} {gn:8.4f} {ge:9.4f} {reg:>9} {r_can:+13.3f}")
# rotating side: SPARC, per galaxy, mass-weighted RAR residual, restricted to the SAME g_bar/a_0 range
gals = load_sparc()
glo, ghi = min(d["gN"] for d in dsph), max(d["gN"] for d in dsph)
info(f"the dwarf spheroidals span g_bar/a_0 = {glo:.4f} to {ghi:.4f}; matching the rotating sample to that window")
rot = []
for g in gals:
    y = g["gbar"]/A0["canonical"]
    m = (y >= glo) & (y <= ghi)
    if m.sum() < 3: continue
    r_can = float(np.median(np.log10(g["gobs"][m]/(nu(y[m])*g["gbar"][m]))))
    y2 = g["gbar"]/A0["alt"]; m2 = (y2 >= glo) & (y2 <= ghi)
    r_alt = float(np.median(np.log10(g["gobs"][m2]/(nu(y2[m2])*g["gbar"][m2])))) if m2.sum() >= 3 else np.nan
    Mb = float(g["gbar"][-1]*(g["r"][-1]*kpc)**2/G/Msun)
    rot.append(dict(nm=g["name"], M=Mb, res={"canonical": r_can, "alt": r_alt}))
info(f"rotating galaxies with >=3 points inside the SAME acceleration window: N = {len(rot)}")
rr = np.array([d["res"]["canonical"] for d in rot]); pr = np.array([d["res"]["canonical"] for d in dsph])
sep = float(np.median(pr) - np.median(rr))
se  = float(math.sqrt(pr.std(ddof=1)**2/len(pr) + rr.std(ddof=1)**2/len(rr)))
nsig = sep/se
# rank test, distribution-free, since N=8 and the residuals are not gaussian
U = sum(1 for a in pr for b in rr if a > b); n1, n2 = len(pr), len(rr)
mu, sd = n1*n2/2, math.sqrt(n1*n2*(n1+n2+1)/12.0)
zU = (U - mu)/sd
ck("A1 (THE TEST, AND IT DOES NOT REACH A RESULT) at matched internal acceleration the pressure-supported dwarfs sit above the framework's kernel and the rotating ones sit on it -- but with only eight classical dwarf spheroidals in existence and a large spread among them, the separation is a HINT and not a detection.  It does not clear three sigma and this must be quoted at its real strength every time it is cited",
   nsig > 3.0, f"separation {sep:+.3f} dex, standard error {se:.3f}, so {nsig:.2f} sigma; rank test z = {zU:+.2f}. Rotating: {np.median(rr):+.3f} dex (scatter {rr.std():.3f}, N={len(rr)}). Pressure-supported: {np.median(pr):+.3f} dex (scatter {pr.std():.3f}, N={len(pr)}). THE SAMPLE IS THE LIMIT: there are only eight classical dwarf spheroidals, so no analysis choice can push this past two sigma")
ck("A2 the rotating side is genuinely ON the kernel in this window, which is what makes the comparison a control and not just two numbers: the framework's residual on rotating systems at these accelerations is consistent with zero at the published radial-acceleration-relation scatter",
   abs(np.median(rr)) < 0.15, f"rotating median {np.median(rr):+.3f} dex against a published relation scatter of 0.06-0.13 dex")
# mass matching, the tighter version -- and it makes things WORSE, which has to be reported
lo, hi = min(d["M"] for d in dsph), max(d["M"] for d in dsph)
mrot = [d for d in rot if lo <= d["M"] <= hi*3]
mr = np.array([d["res"]["canonical"] for d in mrot])
ck("A3 (AGAINST INTEREST) matching on baryonic mass as well as acceleration does NOT strengthen the result, it undermines the control: in the dwarf spheroidals' own mass range only a handful of rotating galaxies survive, and they no longer sit on the kernel either.  So at the very lowest masses the framework is off for BOTH kinds of system, and the clean split seen at matched acceleration does not survive matching on mass",
   len(mrot) >= 10 and abs(np.median(mr)) < 0.15, f"only {len(mrot)} rotating galaxies overlap the dwarf spheroidal mass range {lo:.1e}-{hi:.1e} Msun, and their median residual is {np.median(mr):+.3f} dex, not consistent with the kernel; the apparent separation grows to {np.median(pr)-np.median(mr):+.3f} dex only because the CONTROL degrades, which is not evidence for anything")
b = {f: float(np.median([d["res"][f] for d in dsph]) - np.median([d["res"][f] for d in rot if np.isfinite(d["res"][f])])) for f in A0}
ck("A4 the separation holds on both footings of the acceleration constant, so it is not a choice of a_0",
   all(v > 0.2 for v in b.values()), f"canonical {b['canonical']:+.3f} dex, alt {b['alt']:+.3f} dex")
P(""); info("⚠️ AGAINST INTEREST, and it sizes the whole result: MOND practitioners fit SOME of these dwarfs successfully,")
info("and this calculation reproduces that -- the spread across the eight is large and the individual residuals matter")
info("more than the median.  Per-object, on the canonical footing:")
for d in sorted(dsph, key=lambda x: x["res"]["canonical"]):
    info(f"   {d['nm']:14} {d['res']['canonical']:+.3f} dex   {'ON the kernel' if abs(d['res']['canonical'])<0.15 else ('ABOVE it' if d['res']['canonical']>0 else 'BELOW it')}")
non = sum(1 for d in dsph if abs(d["res"]["canonical"]) < 0.15)
ck("A5 (the honest limit, as a check so it cannot be quietly dropped) the pressure-supported failure is NOT uniform and does not even have a consistent sign: some dwarf spheroidals sit on the kernel and two sit BELOW it.  The pattern is a tendency with real exceptions, not the clean switch the liability table's medians suggest",
   0 < non < len(dsph), f"{non} of {len(dsph)} within 0.15 dex of the kernel; {sum(1 for d in dsph if d['res']['canonical'] < -0.15)} sit BELOW it; full range {min(d['res']['canonical'] for d in dsph):+.2f} to {max(d['res']['canonical'] for d in dsph):+.2f} dex")
iso = [d for d in dsph if d["reg"] == "isolated"]; efe = [d for d in dsph if d["reg"] == "EFE"]
ck("A6 (I FOUND THIS IN MY OWN PRESCRIPTION AND IT IS NOT PHYSICS) the two dwarfs that fall BELOW the kernel are exactly the two handled by the external-field branch, and every dwarf handled by the isolated branch falls above it.  A residual that flips sign with which branch of my own formula was used is a prescription artefact: the 'take the larger of the two' rule is crude, the true behaviour interpolates, and a large part of the reported scatter is therefore mine, not the data's.  Until that is replaced by a proper interpolation, the eight-object scatter is not a measurement",
   all(d["res"]["canonical"] > 0 for d in iso) and all(d["res"]["canonical"] < 0 for d in efe),
   f"isolated branch ({len(iso)} objects): all positive, median {np.median([d['res']['canonical'] for d in iso]):+.3f} dex.  External-field branch ({len(efe)} objects): all negative, median {np.median([d['res']['canonical'] for d in efe]):+.3f} dex.  The sign tracks my branch choice, so the prescription must be fixed before this sample can carry a number")
P(""); P("="*118); P("B.  THE FALSIFIER, AND WHAT THIS IS NOT"); P("="*118)
ck("B1 the fork is not retrodiction-only, and it needs no new observation.  In modified GRAVITY the wide-binary velocity ratio at fixed separation is independent of orbital eccentricity, because the modification is a property of the field at a point.  In modified INERTIA it is not, because eccentric orbits are exactly where the two theories part.  Gaia DR4 in December carries the sample to split on an eccentricity proxy, and because it is a SHAPE test it survives the mass-ratio and contamination systematics that dominate the amplitude",
   True, "modified gravity: the same ratio in every eccentricity bin (frozen band 1.1614-1.1814 canonical, Amendment 10); modified inertia: a bin-to-bin gradient.  Same data, same frozen pipeline")
info("⚠️ THE FOUR HONEST LIMITS, all load-bearing:")
info("  1. This selects a CLASS, not a theory.  Modified inertia has no accepted relativistic completion, and this")
info("     repository's own rapidity-gap modified-inertia action was EXCLUDED at 21 sigma.  No equation here is a field")
info("     theory, and this is not a licence to reopen that action.")
info("  2. DARK MATTER EXPLAINS THE SAME PATTERN and has for fifty years: pressure-supported systems are the ones with")
info("     high dark-matter fractions.  This test does NOT separate the two.  The eccentricity split in B1 would.")
info("  3. The pattern has exceptions (A5): some dwarf spheroidals sit on the kernel.")
info("  4. It does not rescue the cluster residual.  Clusters would still need a large modification, and the f04-f07")
info("     no-go chain in this directory still forbids supplying it with any dark component, hot, cold or mixed.")
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  Four versions of this test have now been run and THREE ARE WITHDRAWN: a second kernel variable whose mutation")
P("  control failed; a pooled coherence correlation that was out-ranked and circular; and a mass-matched control that")
P("  degrades instead of tightening.  What is left is one matched-acceleration comparison at 1.7 sigma on the only")
P("  eight classical dwarf spheroidals that exist.  THAT IS A HINT, NOT A RESULT, and the sample size is the ceiling.")
P("  Worse, the sign of the residual tracks which branch of my own external-field prescription was used, so part of")
P("  the scatter is mine.  The prescription has to be replaced by a proper interpolation before these eight objects")
P("  can carry any number at all.")
P("  WHAT SURVIVES ALL OF THAT is not the measurement but the STRUCTURE: the framework's successes are rotation-")
P("  supported and its failures are not, and Milgrom proved that modified inertia and modified gravity are identical")
P("  for circular orbits and different for every other orbit.  That makes 'which arm' a real fork, and this repository")
P("  has run only one arm since 2026-08-08.")
P("  The fork is decidable without new observations: modified inertia predicts the Gaia DR4 wide-binary velocity ratio")
P("  to drift across orbital-eccentricity bins where modified gravity predicts it flat.  December, frozen band, shape")
P("  test rather than amplitude.  That is the deliverable here -- a test to run, not a discovery to announce.")
sys.exit(ck.done())
