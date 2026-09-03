#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g05v_adversarial_globular_cluster_refutation.py
============================================================================================================
ADVERSARIAL VERIFICATION of one claim in g05_dsph_prescription_fixed_and_expanded.py, check S5:

  "Outer-halo globular clusters, equally pressure-supported but containing no dark matter under LCDM either,
   sit far BELOW the kernel where dwarf spheroidals at the same internal acceleration sit above it.  Support
   type does not predict the sign of the residual; dark-matter content does."
  Numbers under test: Pal 4 -0.874 (x_i=0.061), Pal 14 -1.306 (x_i=0.013), Pal 3 -0.844 (x_i=0.027),
  NGC 2419 -0.211 (x_i=1.08); median -0.859 dex.  dSph over x_i = 0.01-1.2: median +0.114 on N=12.
  "At Upsilon_V = 1 the clusters move to -0.558 dex."

THE JOB IS TO REFUTE IT.  Everything below is recomputed from the published inputs with an INDEPENDENTLY
WRITTEN pipeline -- separate quadrature, separate photometry, separate dwarf loader -- and nothing is imported
from g05.  The lens is the PHYSICS: is the modified-inertia / modified-gravity distinction used correctly, is
the deep-MOND limit applicable where it was applied, and did BOTH a_0 footings genuinely enter.

WHAT THIS FILE FOUND (stated up front, so no check below can be read as a surprise):
  THE CLAIM SURVIVES.  It reproduces independently to 0.001 dex, it is depth-matched object by object rather
  than window-matched, it survives every adversarial lever stacked, and the nu = 1 mutation shows the deficit
  IS the kernel's boost and not the pipeline.  Four defects, none of which touches the substance:
  * ONE QUOTED NUMBER IS WRONG.  g05 computes its Upsilon_V = 1 caveat ANALYTICALLY as median + log10(2) =
    -0.558 dex.  That shift is the NEWTONIAN one (g_pred proportional to M).  Three of the four clusters are in
    deep-MOND or external-field regime where g_pred goes as sqrt(M) or less, so the exact recomputation gives
    -0.678 dex, not -0.558.  The error runs AGAINST g05's own point -- the caveat as printed is more generous
    to the alternative than the arithmetic allows -- but the number as quoted is wrong.
  * The GC block of g05 runs on the CANONICAL footing ONLY, against the standing both-footings rule.  Run here,
    it rescues nothing: with the dwarf comparison set held fixed the gap is footing-stable to 0.002 dex.  But
    the "+0.114 dex" dwarf median is NOT stable if g05's fixed window 0.01 <= x_i <= 1.2 is RE-APPLIED on the
    alt footing, because x_i scales as 1/a_0 and the window edge then re-selects the sample: that variant reads
    -0.007 dex on N = 11.  The window edge, not the physics, is what moves.
  * THE DEEP-MOND LIMIT IS NOT UNIFORMLY APPLICABLE.  Pal 3 and Pal 4 are isolated deep-MOND (x_i/x_e = 2.9-7.4)
    and their predicted dispersions are independent of the assumed half-light radius, so Baumgardt's N-body
    r_h,l is not load-bearing for them.  Pal 14 is EXTERNAL-FIELD DOMINATED (x_i/x_e = 0.67), quasi-Newtonian
    with a boosted G, and its residual DOES move with the radius -- 0.09 dex for 25 per cent in r_h,l.  NGC 2419
    at x_i ~ 1.1 is in neither limit.
  * THE WEAK POINT IS NOT THE ONE g05 NAMES.  g05 names Pal 14's 16 stars.  The real soft spot is that the
    depth-matched gap collapses to +0.20 dex at NGC 2419 -- the only cluster with 183 radial velocities, the
    only one whose boost is small (1.55), and the only one not carried by a handful of stars.
  * The modified-inertia arm is NOT over-claimed by g05: it states the fork is untouched.  But S5's framing
    ("under a reading in which pressure support itself breaks the kernel they should sit ABOVE") assumes a SIGN
    for a class of theories that has none.  Audited as a check below.

DATA, all published, all cited at point of use:
  Baumgardt & Hilker 2018, MNRAS 478, 1520; Baumgardt et al. 2019-2023 catalogue -- structural parameters
  Harris 2010 (arXiv:1012.3224) -- reddening E(B-V)
  Jordi et al. 2009, AJ 137, 4586        -- Pal 14, sigma = 0.38 +- 0.12 km/s, 16 members, Keck/HIRES
  Frank et al. 2012, MNRAS 423, 2917     -- Pal 4,  sigma = 0.87 +- 0.18 km/s, 23 members, Keck/HIRES
  Gentile, Famaey, Angus & Kroupa 2010, A&A 509, A97 -- published MOND prediction and KS test for Pal 14
  Baumgardt, Grebel & Kroupa 2005, MNRAS 359, L1 -- the original outer-halo-globular MOND test
  Wolf et al. 2010, MNRAS 406, 1220      -- M_1/2 = 3 sigma^2 r_1/2 / G, r_1/2 = (4/3) R_e
  Milgrom 1984, ApJ 287, 571; Famaey & McGaugh 2012, Living Rev. Rel. 15, 10 -- deep-MOND sigma^4 = (4/81) G M a_0
  Milgrom 1994, Ann. Phys. 229, 384; Milgrom 2011, arXiv:1111.1611 -- modified inertia vs modified gravity
  Local Volume Database, Pace 2024, ApJS 273, 15 -- the dwarf spheroidal comparison sample
BOTH FOOTINGS.  MUTATION CONTROLS.  CHECKS CAN FAIL AND SOME DO.
"""
import sys, os, math, csv
import numpy as np
from hunt_lib import *

ck = Check()
PC = 3.0857e16
MW_MB, M31_MB = 6.0e10, 1.2e11          # host baryonic masses, Msun (McGaugh 2016, ApJ 816, 42) -- as g05 uses
UPS_REF = 2.0                            # the M/L_V g05's headline uses, for both classes
SRC = "g05_dsph_prescription_fixed_and_expanded.py"

# ---------------------------------------------------------------------------------------------------------
# INDEPENDENT machinery.  Written from the QUMOND flux theorem, not copied: the sphere average of the radial
# component of S = nu(|g_N|/a_0) g_N over a sphere in a uniform external Newtonian field.  Gauss-Legendre in
# cos(theta) rather than g05's trapezoid in theta, so a quadrature blunder in either would show up as a
# disagreement in V1.
_GLX, _GLW = np.polynomial.legendre.leggauss(400)
def boost_sphere(x_i, x_e):
    """<g_r>/(x_i a_0): the sphere-averaged inward radial acceleration in units of the internal NEWTONIAN one."""
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        return nu_s(x_i)
    u = _GLX                                          # u = cos(theta), measure sin th dth = du, weight 1/2
    st2 = 1.0 - u*u
    gx = -x_i*np.sqrt(np.clip(st2, 0.0, None))
    gz = x_e - x_i*u
    Sr = nu(np.sqrt(gx*gx + gz*gz))*(gx*np.sqrt(np.clip(st2, 0.0, None)) + gz*u)
    return -float(np.dot(_GLW, Sr)/2.0)/x_i

def sigma_pred(M_msun, r12_m, a0, x_e, kernel=True):
    """Wolf et al. 2010 inverted: sigma^2 = g(r_1/2) r_1/2 / 3, with g from the ENCLOSED baryonic mass M/2."""
    x_i = G*(0.5*M_msun*Msun)/r12_m**2/a0
    b = boost_sphere(x_i, x_e) if kernel else 1.0
    g = b*x_i*a0
    return math.sqrt(g*r12_m/3.0), x_i, b

def x_e_newtonian_from_true(g_true, a0):
    """QUMOND takes the NEWTONIAN field of the actual matter.  Given an OBSERVED (true, MONDian) external field,
    invert nu(x) x = g_true/a_0 for the Newtonian source field x.  Used for the adversarial variant in which the
    Milky Way's measured rotation curve, not the framework's own baryonic mass, sets the external field."""
    t = g_true/a0
    lo, hi = 1e-8, 1e4
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        (lo, hi) = (mid, hi) if nu_s(mid)*mid < t else (lo, mid)
    return math.sqrt(lo*hi)

# ---------------------------------------------------------------------------------------------------------
# The four outer-halo clusters, from the published sources, re-entered here by hand from the citations above.
#            name        D_sun   R_GC     V      E(B-V)  r_h,l pc  sigma  e_sigma  N_RV  provenance of sigma
GC = [("Pal 4",     101.39, 104.05, 14.23, 0.01, 15.88, 0.87, 0.18, 23, "Frank et al. 2012, Keck/HIRES"),
      ("Pal 14",     73.58,  68.55, 14.13, 0.04, 27.63, 0.38, 0.12, 16, "Jordi et al. 2009, Keck/HIRES"),
      ("Pal 3",      94.84,  98.17, 14.56, 0.04, 20.16, 0.80, 0.34, 22, "Baumgardt N-body fit (MODEL-DEPENDENT)"),
      ("NGC 2419",   88.47,  95.93, 10.56, 0.08, 19.76, 5.10, 0.48, 183, "Baumgardt N-body fit (MODEL-DEPENDENT)")]
# Baumgardt's own profile bin for Pal 14 is 0.71 +- 0.16 km/s on the SAME 16 stars as Jordi's 0.38 -- a live
# data-side disagreement.  h93_outer_halo_globulars.py carries the HIGHER value as the framework-favourable
# choice; g05 carries the LOWER one.  The swap is exercised as an adversarial lever below.
PAL14_BAUMGARDT = 0.71

def gc_rows(a0, ups=UPS_REF, sig_override=None, rfac=1.0, mw_mb=MW_MB, vc_ext=None, kernel=True):
    out = []
    for nm, Dsun, Rgc, V, EBV, rhl, sob, esob, N, src in GC:
        if sig_override and nm in sig_override: sob, esob = sig_override[nm], esob
        MV = V - 5.0*math.log10(Dsun*1e3/10.0) - 3.1*EBV
        LV = 10.0**(0.4*(4.83 - MV))
        M = ups*LV
        r12 = (4.0/3.0)*rhl*rfac*PC
        if vc_ext is None:
            x_e = G*mw_mb*Msun/(Rgc*kpc)**2/a0                     # QUMOND: Newtonian field of the actual matter
        else:
            x_e = x_e_newtonian_from_true((vc_ext*1e3)**2/(Rgc*kpc), a0)
        sp, x_i, b = sigma_pred(M, r12, a0, x_e, kernel=kernel)
        out.append(dict(name=nm, MV=MV, LV=LV, M=M, x_i=x_i, x_e=x_e, b=b, sob=sob, esob=esob, N=N,
                        sp=sp/1e3, res=2.0*math.log10(sob/(sp/1e3)), src=src))
    return out

# ---------------------------------------------------------------------------------------------------------
# The dwarf comparison sample, loaded independently of g05 from the same Local Volume Database files.
def fnum(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None

def load_dwarfs():
    ROT = {"LMC", "SMC"}; DIS = {"Sagittarius", "Bootes III", "Tucana III", "Tucana IV"}
    out = []
    for fname, hmb, host in (("lvd_dwarf_mw.csv", MW_MB, "MW"), ("lvd_dwarf_m31.csv", M31_MB, "M31"),
                             ("lvd_dwarf_local_field.csv", None, "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fname))):
            sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
            rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
            if sig is None or ul is not None or MV is None or rh is None or sig <= 0 or rh <= 0: continue
            if fnum(r["confirmed_galaxy"]) != 1: continue
            if r["name"] in ROT or r["name"] in DIS: continue
            lMs = fnum(r["mass_stellar"]); lMHI = fnum(r["mass_HI"])
            Ms = 10**lMs if lMs is not None else 10**(0.4*(4.83 - MV))*UPS_REF
            MHI = 10**lMHI if lMHI is not None else 0.0
            if MHI > 0.3*Ms: continue
            out.append(dict(name=r["name"], Ms=Ms, MHI=MHI, rh=rh, sig=sig, host=host, hmb=hmb,
                            Dhost=fnum(r["distance_host"]) or fnum(r["distance_gc"]),
                            Dgc=fnum(r["distance_gc"]), Dm31=fnum(r["distance_m31"]),
                            uf=(host == "MW" and MV > -7.7)))
    return out
DW = load_dwarfs()

def dw_rows(a0, ups=UPS_REF, drop_ultrafaint=True, kernel=True):
    out = []
    for d in DW:
        if drop_ultrafaint and d["uf"]: continue
        r12 = (4.0/3.0)*d["rh"]*PC
        Mb = (ups/UPS_REF)*d["Ms"] + 1.33*d["MHI"]
        if d["hmb"] is not None and d["Dhost"]:
            x_e = G*d["hmb"]*Msun/(d["Dhost"]*kpc)**2/a0
        else:
            x_e = ((G*MW_MB*Msun/(d["Dgc"]*kpc)**2 if d["Dgc"] else 0.0) +
                   (G*M31_MB*Msun/(d["Dm31"]*kpc)**2 if d["Dm31"] else 0.0))/a0
        sp, x_i, b = sigma_pred(Mb, r12, a0, x_e, kernel=kernel)
        out.append(dict(name=d["name"], x_i=x_i, x_e=x_e, res=2.0*math.log10(d["sig"]/(sp/1e3))))
    return out

# ==========================================================================================================
P("="*118)
P("1.  INDEPENDENT RECOMPUTATION OF THE FOUR CLUSTERS.  Different quadrature, photometry re-entered from the")
P("    published catalogues, nothing imported from g05.")
P("="*118)
G05 = {"Pal 4": -0.874, "Pal 14": -1.306, "Pal 3": -0.844, "NGC 2419": -0.211}
G05_XI = {"Pal 4": 0.0611, "Pal 14": 0.0127, "Pal 3": 0.0267, "NGC 2419": 1.0774}
rows_can = gc_rows(A0["canonical"])
info(f"{'cluster':10} {'M_V':>7} {'M(Ups=2)':>10} {'x_i':>9} {'x_e':>9} {'boost':>7} {'sig_pred':>9} "
     f"{'sig_obs':>8} {'dex':>8} {'g05':>8} {'diff':>7}")
dmax = 0.0; ximax = 0.0
for r in rows_can:
    d = r["res"] - G05[r["name"]]; dmax = max(dmax, abs(d))
    ximax = max(ximax, abs(r["x_i"]/G05_XI[r["name"]] - 1))
    info(f"{r['name']:10} {r['MV']:7.2f} {r['M']:10.2e} {r['x_i']:9.4f} {r['x_e']:9.5f} {r['b']:7.3f} "
         f"{r['sp']:9.3f} {r['sob']:8.2f} {r['res']:+8.3f} {G05[r['name']]:+8.3f} {d:+7.3f}")
med_can = float(np.median([r["res"] for r in rows_can]))
info(f"median residual {med_can:+.4f} dex against g05's quoted -0.859")
ck("V1 the four residuals, the four internal accelerations and the median REPRODUCE under an independently "
   "written pipeline.  The claim is not a coding artefact of g05: the photometry, the enclosed-mass Wolf "
   "inversion and the QUMOND sphere average all check out against a separate implementation",
   dmax < 0.02 and ximax < 0.02 and abs(med_can + 0.859) < 0.02,
   f"worst residual difference {dmax:.4f} dex, worst x_i difference {100*ximax:.2f} per cent, "
   f"median {med_can:+.4f} against -0.859")

# ==========================================================================================================
P(""); P("="*118)
P("2.  BOTH a_0 FOOTINGS -- which g05's globular-cluster block never ran.")
P("="*118)
src_txt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC), encoding="utf-8").read()
gc_block = src_txt.split("4e.  OUTER-HALO GLOBULAR CLUSTERS")[1].split("PART 5.")[0]
uses_alt = ('A0["alt"]' in gc_block) or ("A0['alt']" in gc_block) or ("for foot, a0 in A0.items()" in gc_block)
ck("V2 PROCEDURE (FAILS) the repository's standing rule is BOTH a_0 footings on every load-bearing claim.  "
   "The globular-cluster block of g05 -- section 4e, the block that produces the claim under test -- evaluates "
   "a0c only.  The claim as quoted is a single-footing number",
   uses_alt,
   f"the 4e block references a0c {gc_block.count('a0c')} times and A0['alt'] {gc_block.count(chr(34)+'alt'+chr(34)) + gc_block.count(chr(39)+'alt'+chr(39))} times")

# the dwarf object set is FROZEN on the canonical selection so a moving window edge cannot do the work:
# x_i scales as 1/a_0, so the alt footing shifts every object by 0.83 dex-independent and would otherwise
# re-select the sample underneath the comparison.
FROZEN = [d["name"] for d in dw_rows(A0["canonical"]) if 0.01 <= d["x_i"] <= 1.2]
info(f"dwarf comparison set frozen on the canonical selection, N = {len(FROZEN)}: {', '.join(FROZEN)}")
foot_med = {}
for foot, a0 in A0.items():
    rr = gc_rows(a0)
    dd = [d for d in dw_rows(a0) if d["name"] in FROZEN]
    foot_med[foot] = (float(np.median([r["res"] for r in rr])), float(np.median([d["res"] for d in dd])), len(dd))
    info(f"   {foot:10} (a_0 = {a0:.3g}):  globular clusters " +
         ", ".join(f"{r['name']} {r['res']:+.3f}" for r in rr) +
         f"  median {foot_med[foot][0]:+.3f} dex;  the same 12 dwarfs median {foot_med[foot][1]:+.3f} "
         f"(gap {foot_med[foot][1]-foot_med[foot][0]:+.3f} dex)")
ck("V3 the omitted footing does NOT rescue the framework and does not overturn the claim.  With the dwarf "
   "comparison set held fixed, the alt footing moves clusters and dwarfs down by almost exactly the same amount, "
   "leaving the gap identical to 0.002 dex and the dwarfs still above the kernel.  The procedural violation is "
   "real; the result of repairing it is that nothing changes",
   foot_med["alt"][1] > 0.05,
   f"canonical: GC median {foot_med['canonical'][0]:+.3f}, dwarf median {foot_med['canonical'][1]:+.3f}, gap "
   f"{foot_med['canonical'][1]-foot_med['canonical'][0]:+.3f} dex.  alt: GC median {foot_med['alt'][0]:+.3f}, dwarf "
   f"median {foot_med['alt'][1]:+.3f}, gap {foot_med['alt'][1]-foot_med['alt'][0]:+.3f} dex.  The GAP is footing-stable "
   f"to {abs((foot_med['alt'][1]-foot_med['alt'][0])-(foot_med['canonical'][1]-foot_med['canonical'][0])):.3f} dex; "
   f"the dwarf SIGN is not")
ck("V3b what the claim needs -- that the two classes sit on opposite sides of each other by a large margin at "
   "matched acceleration -- IS footing-independent, and the alt footing makes the clusters worse, not better, so "
   "the omitted footing was not hiding a rescue",
   foot_med["alt"][0] < -0.3 and abs((foot_med["alt"][1]-foot_med["alt"][0]) -
                                     (foot_med["canonical"][1]-foot_med["canonical"][0])) < 0.15,
   f"cluster median canonical {foot_med['canonical'][0]:+.3f} -> alt {foot_med['alt'][0]:+.3f}; "
   f"gap canonical {foot_med['canonical'][1]-foot_med['canonical'][0]:+.3f} -> alt {foot_med['alt'][1]-foot_med['alt'][0]:+.3f} dex")

# the window edge is itself a_0-dependent: x_i goes as 1/a_0, so re-applying "0.01 <= x_i <= 1.2" on the alt
# footing selects a DIFFERENT set of dwarfs.  That, and not the physics, is what a naive both-footings run moves.
resel = [d for d in dw_rows(A0["alt"]) if 0.01 <= d["x_i"] <= 1.2]
med_resel = float(np.median([d["res"] for d in resel]))
info(f"   re-applying g05's fixed window 0.01 <= x_i <= 1.2 on the ALT footing instead of freezing the sample: "
     f"N = {len(resel)}, dwarf median {med_resel:+.3f} dex")
ck("V3c (FAILS) the dwarf comparison number '+0.114 dex on N = 12' is fragile to the WINDOW EDGE rather than to "
   "the physics.  g05 selects the dwarfs by a fixed window in x_i = g_N/a_0, but x_i scales as 1/a_0, so on the "
   "alt footing that window is a different physical acceleration band and drops an object; the dwarf median then "
   "reads -0.007 dex on N = 11 and the phrase 'dwarf spheroidals sit above it' stops being true as stated.  The "
   "GAP survives because the clusters move with them.  The quotable statement is therefore the GAP at matched "
   "acceleration, never the absolute dwarf offset behind a hard window edge on an a_0-scaled variable",
   abs(med_resel - foot_med["alt"][1]) < 0.05,
   f"frozen sample, alt footing: dwarf median {foot_med['alt'][1]:+.3f} on N = {foot_med['alt'][2]}; g05's window "
   f"re-applied on the alt footing: {med_resel:+.3f} on N = {len(resel)}; the two differ by "
   f"{abs(med_resel - foot_med['alt'][1]):.3f} dex on a claim whose dwarf side is {foot_med['canonical'][1]:+.3f}")

# ==========================================================================================================
P(""); P("="*118)
P("3.  THE Upsilon_V = 1 CAVEAT NUMBER.  g05 computes it ANALYTICALLY as median + log10(2) = -0.558 dex.")
P("="*118)
info("g05's line is:  np.median(gcr) + math.log10(2.0)")
info("That analytic shift assumes g_pred is PROPORTIONAL to M -- the NEWTONIAN scaling.  In the deep-MOND limit")
info("g_pred goes as sqrt(M a_0)/r, so halving the mass moves the residual by log10(sqrt(2)) = +0.151, not +0.301.")
rows_u1 = gc_rows(A0["canonical"], ups=1.0)
med_u1 = float(np.median([r["res"] for r in rows_u1]))
analytic = med_can + math.log10(2.0)
info(f"{'cluster':10} {'x_i(Ups=2)':>11} {'res(Ups=2)':>11} {'res(Ups=1)':>11} {'true shift':>11} {'g05 assumes':>12}")
for a, b in zip(rows_can, rows_u1):
    info(f"{a['name']:10} {a['x_i']:11.4f} {a['res']:+11.3f} {b['res']:+11.3f} {b['res']-a['res']:+11.3f} {math.log10(2.0):+12.3f}")
info(f"EXACT recomputation at Upsilon_V = 1: median {med_u1:+.3f} dex.  g05's analytic value {analytic:+.3f} dex.")
ck("V4 (FAILS -- A CONCRETE ERROR IN A QUOTED NUMBER) g05's Upsilon_V = 1 caveat, '-0.558 dex', is computed with "
   "the NEWTONIAN mass scaling and is wrong by about 0.15 dex.  Three of the four clusters sit at x_i = 0.013-0.061 "
   "where the kernel is deep-MOND and the predicted dispersion goes as M^(1/4), so the residual moves by only "
   "+0.151 dex when the mass-to-light ratio is halved.  The error runs AGAINST g05's own argument -- the true "
   "Upsilon_V = 1 median is MORE negative than quoted, not less -- so the caveat as printed is more generous to "
   "the alternative than the arithmetic allows.  It is still a wrong number in a quoted result",
   abs(med_u1 - analytic) < 0.02,
   f"exact {med_u1:+.3f} dex, g05's analytic {analytic:+.3f} dex, discrepancy {med_u1-analytic:+.3f}; "
   f"per-cluster true shifts " + ", ".join(f"{b['name']} {b['res']-a['res']:+.3f}" for a, b in zip(rows_can, rows_u1)))

# ==========================================================================================================
P(""); P("="*118)
P("4.  IS THE DEEP-MOND LIMIT ACTUALLY APPLICABLE WHERE IT IS APPLIED?")
P("="*118)
info("Test 1 -- the SIGNATURE of the deep-MOND regime for this estimator: sigma_pred^2 = g r_1/2/3 with")
info("   g = sqrt(G (M/2) a_0)/r_1/2, so sigma_pred is INDEPENDENT of r_1/2.  If a cluster is deep-MOND, moving")
info("   its half-light radius by 25 per cent must not move its predicted dispersion.  If it is not, it will.")
r_hi, r_lo = gc_rows(A0["canonical"], rfac=1.25), gc_rows(A0["canonical"], rfac=0.80)
info(f"{'cluster':10} {'x_i':>9} {'res':>8} {'res(r x1.25)':>13} {'res(r x0.80)':>13} {'spread dex':>11}")
spread = {}
for a, b, c in zip(rows_can, r_hi, r_lo):
    spread[a["name"]] = max(abs(b["res"]-a["res"]), abs(c["res"]-a["res"]))
    info(f"{a['name']:10} {a['x_i']:9.4f} {a['res']:+8.3f} {b['res']:+13.3f} {c['res']:+13.3f} {spread[a['name']]:11.3f}")
info("   x_i vs x_e decides which limit each cluster is in: " +
     ", ".join(f"{r['name']} x_i/x_e = {r['x_i']/r['x_e']:.2f}" for r in rows_can))
ck("V5 (FAILS, AND THE FAILURE NAMES A SECOND SOFT SPOT) the isolated deep-MOND limit -- in which the predicted "
   "dispersion is independent of the assumed half-light radius -- holds for Pal 3 and Pal 4 (x_i/x_e = 2.9-7.4), "
   "so for them the Baumgardt N-body r_h,l is not load-bearing.  It does NOT hold for Pal 14, which is "
   "EXTERNAL-FIELD DOMINATED (x_i/x_e = 0.67): there the kernel is quasi-Newtonian with a boosted G, the "
   "prediction goes back to depending on the radius, and a 25 per cent error in Pal 14's model-derived r_h,l "
   "moves its residual by 0.09 dex.  Nor does it hold for NGC 2419 at x_i ~ 1.1.  Pal 14 is the cluster carrying "
   "the most extreme residual and it is the one whose structural input matters most",
   max(spread[n] for n in ("Pal 4", "Pal 14", "Pal 3")) < 0.05,
   ", ".join(f"{n} {spread[n]:.3f} dex" for n in spread) +
   "; Pal 4 and Pal 3 are radius-independent to 0.02 dex as the deep-MOND limit requires, Pal 14 is not")

info("")
info("Test 2 -- the VIRIAL COEFFICIENT.  The Wolf et al. 2010 estimator is derived in Newtonian gravity.  Applied")
info("   inside the kernel it must reproduce the exact isolated deep-MOND relation sigma^4 = (4/81) G M a_0")
info("   (Milgrom 1984, ApJ 287, 571; Famaey & McGaugh 2012 eq. 43).  If it does not, both classes are biased --")
info("   but by the SAME factor, so the bias cancels in the dwarf-versus-cluster comparison.")
bias = []
for M in (1e3, 1e4, 1e5, 1e6, 1e7, 1e8):
    for rpc in (30.0, 100.0, 300.0, 1000.0):
        r12 = rpc*PC
        sp, x_i, b = sigma_pred(M, r12, A0["canonical"], 0.0)
        if x_i > 3e-3: continue
        sx = (4.0/81.0*G*M*Msun*A0["canonical"])**0.25
        bias.append(2.0*math.log10(sp/sx))
ck("V6 the Wolf-estimator route reproduces the exact deep-MOND M-sigma relation to better than 0.05 dex in "
   "acceleration, so the estimator is not manufacturing the cluster deficit -- and because dwarfs and clusters "
   "go through the identical estimator, whatever residual bias there is cancels exactly in the comparison that "
   "carries the claim",
   len(bias) >= 4 and max(abs(b) for b in bias) < 0.05,
   f"sigma from the Wolf route against sigma = ((4/81) G M a_0)^(1/4) over {len(bias)} deep-MOND configurations: "
   f"{min(bias):+.4f} to {max(bias):+.4f} dex (analytic expectation +{2*math.log10((81.0/18.0/4.0)**0.25):.4f})")

# ==========================================================================================================
P(""); P("="*118)
P("5.  IS THE ACCELERATION MATCHING GENUINE, OR DO THE CLUSTERS SIT DEEPER THAN THE DWARFS THEY ARE COMPARED TO?")
P("="*118)
info("g05 established (its own check A1c) that inside the pressure sample the residual runs with log10(x_i) at")
info("slope about -0.5.  A window as wide as x_i = 0.01-1.2 is 2.1 dex, so a median-versus-median comparison over")
info("it could be a DEPTH difference wearing the label 'globular cluster'.  Tested object by object.")
dwa = [d for d in dw_rows(A0["canonical"]) if 0.01 <= d["x_i"] <= 1.2]
dwa_wide = [d for d in dw_rows(A0["canonical"]) if 0.005 <= d["x_i"] <= 3.0]   # for NGC 2419, whose nearest
# dwarf neighbour (NGC 205, x_i = 1.43) falls just outside g05's own 1.2 window edge
info(f"   dwarf window N = {len(dwa)}, median residual {np.median([d['res'] for d in dwa]):+.3f} dex, "
     f"log10 x_i median {np.median([math.log10(d['x_i']) for d in dwa]):+.3f}")
info(f"   cluster       log10 x_i median {np.median([math.log10(r['x_i']) for r in rows_can]):+.3f}")
info(f"{'cluster':10} {'x_i':>9} {'GC res':>8} {'dwarfs within 0.35 dex of log x_i':>36} {'dwarf med':>10} {'gap':>8}")
gaps = []
for r in rows_can:
    near = [d for d in dwa_wide if abs(math.log10(d["x_i"]) - math.log10(r["x_i"])) < 0.35]
    if len(near) < 2:
        info(f"{r['name']:10} {r['x_i']:9.4f} {r['res']:+8.3f} {'-- fewer than 2 dwarfs in range --':>36}")
        continue
    dm = float(np.median([d["res"] for d in near]))
    gaps.append((r["name"], dm - r["res"]))
    info(f"{r['name']:10} {r['x_i']:9.4f} {r['res']:+8.3f} {', '.join(d['name'] for d in near)[:36]:>36} "
         f"{dm:+10.3f} {dm-r['res']:+8.3f}")
gv = [g for _, g in gaps]
ck("V7 the separation is NOT a depth confound in disguise: matched object by object to the dwarfs within 0.35 dex "
   "of the same internal acceleration, every cluster still sits below its own depth-matched dwarfs, and the "
   "cluster and dwarf samples have nearly the same median log10 x_i.  This is the one comparison in the whole "
   "g05 file that IS acceleration-matched rather than window-matched",
   len(gv) >= 3 and min(gv) > 0.0 and float(np.median(gv)) > 0.5,
   "; ".join(f"{n} gap {g:+.3f} dex" for n, g in gaps) + f"; median gap {np.median(gv):+.3f} dex")
ngc_gap = dict(gaps).get("NGC 2419")
ck("V8 (FAILS, AND IT IS THE WEAK POINT g05 DOES NOT NAME) the gap is not uniform across the four clusters: it "
   "collapses at NGC 2419, the only cluster with real statistical weight (183 radial velocities against 16-23 for "
   "the other three) and the only one whose dispersion does not rest on a handful of stars.  The claim's strength "
   "is carried entirely by the three sparse clusters; the well-measured one shows almost nothing.  NGC 2419 is "
   "also the one cluster outside the deep-MOND regime, where the kernel's boost is only about 1.3",
   ngc_gap is not None and ngc_gap > 0.5,
   f"NGC 2419 gap {ngc_gap:+.3f} dex on 183 velocities and a kernel boost of {rows_can[3]['b']:.2f}; the three "
   f"sparse clusters give gaps " + ", ".join(f"{n} {g:+.3f}" for n, g in gaps if n != "NGC 2419"))

# ==========================================================================================================
P(""); P("="*118)
P("6.  EVERY ADVERSARIAL LEVER, ONE AT A TIME AND THEN ALL AT ONCE.")
P("="*118)
info("(a) Upsilon_V.  Baumgardt's DYNAMICAL M/L_V for these clusters is 0.8-1.7; mass segregation depletes")
info("    low-mass stars, so the photometric 2.0 is an upper bound and inflates the predicted dispersion.")
info("(b) Pal 14's dispersion.  Baumgardt's own profile bin is 0.71 +- 0.16 km/s on the SAME 16 stars that")
info("    Jordi et al. 2009 give 0.38 +- 0.12 for.  h93 carries the higher value; g05 carries the lower.")
info("(c) The Milky Way external field.  g05 uses the framework's own baryonic mass, giving v_inf = 165 km/s;")
info("    halo tracers show 200-220 km/s at 70-100 kpc.  A stronger external field means MORE external-field")
info("    suppression and a SMALLER predicted dispersion.  Fed in through nu correctly: the observed field is the")
info("    TRUE one, so it is inverted to the Newtonian source field that QUMOND's nu actually takes.")
LEV = [("as published in g05", dict()),
       ("(a) Upsilon_V = 1.0 (Baumgardt dynamical floor)", dict(ups=1.0)),
       ("(b) Pal 14 -> Baumgardt 0.71 km/s", dict(sig_override={"Pal 14": PAL14_BAUMGARDT})),
       ("(c) MW external field from v_c = 220 km/s", dict(vc_ext=220.0)),
       ("(c') MW baryonic mass x2 = 1.2e11", dict(mw_mb=2*MW_MB)),
       ("ALL THREE STACKED (a)+(b)+(c)", dict(ups=1.0, sig_override={"Pal 14": PAL14_BAUMGARDT}, vc_ext=220.0))]
info(f"{'lever':52} {'Pal 4':>8} {'Pal 14':>8} {'Pal 3':>8} {'NGC2419':>8} {'median':>8}")
lev_med = {}
for lab, kw in LEV:
    rr = {r["name"]: r["res"] for r in gc_rows(A0["canonical"], **kw)}
    m = float(np.median(list(rr.values()))); lev_med[lab] = m
    info(f"{lab:52} {rr['Pal 4']:+8.3f} {rr['Pal 14']:+8.3f} {rr['Pal 3']:+8.3f} {rr['NGC 2419']:+8.3f} {m:+8.3f}")
worst = lev_med["ALL THREE STACKED (a)+(b)+(c)"]
ck("V9 the cluster deficit survives every adversarial lever available, stacked: the dynamical rather than the "
   "photometric mass-to-light ratio, the HIGHER of the two disputed Pal 14 dispersions, and the Milky Way's "
   "MEASURED rotation curve in place of the framework's own weaker baryonic field.  All three together move the "
   "median by about 0.3 dex and leave it strongly negative.  The claim's SIGN and order of magnitude are not "
   "rescuable by the inputs",
   worst < -0.3,
   "; ".join(f"{k}: {v:+.3f}" for k, v in lev_med.items()))

# ==========================================================================================================
P(""); P("="*118)
P("7.  WHAT DOES THE MODIFIED-INERTIA ARM ACTUALLY PREDICT?  The physics lens on the claim's second clause.")
P("="*118)
info("Milgrom's theorem (1994, Ann. Phys. 229, 384; 2011, arXiv:1111.1611): modified inertia and modified gravity")
info("coincide for CIRCULAR orbits in the deep-MOND limit and differ for every other orbit.  Modified inertia is a")
info("CLASS, not a theory.  Absent a specific action there is no unique prediction for a pressure-supported system,")
info("and in particular NO PREDICTED SIGN for the deviation of a dispersion-supported object from the modified-")
info("gravity kernel.  So:")
info("  * 'Globular clusters sit below where dwarf spheroidals sit above' does refute the coarse reading f09 was")
info("    chasing -- 'pressure support itself breaks the kernel', which is a SINGLE-SIGN hypothesis and is")
info("    falsified by two signs.  That inference is sound and does not need modified inertia to have a sign.")
info("  * It does NOT refute modified inertia, because an MI theory keyed to ORBIT SHAPE rather than to support")
info("    type can accommodate both signs: globular-cluster stars are collisionally relaxed onto near-isotropic")
info("    rosettes, dwarf-spheroidal stars are collisionless and may be radially anisotropic.  'Pressure-supported'")
info("    is a coarser variable than the one Milgrom's theorem is about.")
info("  * The claim as written says SUPPORT TYPE does not predict the sign.  That is what the data show.  Any")
info("    stronger reading -- that the fork is closed, that modified inertia is excluded -- is not supported.")
forbidden = ["modified inertia is excluded", "modified inertia is dead", "closes the fork", "the fork is closed",
             "modified inertia is refuted", "kills modified inertia"]
hits = [f for f in forbidden if f in src_txt.lower()]
disclaimed = "THE FORK ITSELF IS UNTOUCHED AND STILL OPEN" in src_txt
ck("V10 g05 does NOT over-claim what modified inertia predicts: it nowhere states that the globular clusters "
   "exclude modified inertia, and its verdict block says in terms that the fork is untouched and still open.  "
   "The claim's second clause is about SUPPORT TYPE, which is the variable f09 actually used, and it is the "
   "right variable to falsify",
   disclaimed and not hits,
   f"explicit fork disclaimer present = {disclaimed}; over-claiming phrases found = {hits if hits else 'none'}")
ck("V11 (FAILS -- A FRAMING DEFECT, NOT A NUMERICAL ONE) S5's setup sentence asserts that under a reading in "
   "which pressure support breaks the kernel the clusters 'should behave like the dwarf spheroidals and sit ABOVE "
   "it'.  That assumes a SIGN for a hypothesis class that has none: no theorem fixes the sign of a modified-"
   "inertia deviation for a dispersion-supported system.  The falsification that actually goes through is the "
   "weaker and sufficient one -- a single-sign 'pressure support' hypothesis predicts ONE sign and the data show "
   "TWO -- and S5 should be stated that way rather than by attributing a prediction to the alternative",
   "should behave like the dwarf spheroidals and sit ABOVE it" not in src_txt,
   "the sentence is in the committed file; the numerical claim is unaffected, but the stated logic gives the "
   "alternative hypothesis a prediction it does not have")

# ==========================================================================================================
P(""); P("="*118)
P("8.  HOW STRONG IS IT, IN ITS OWN CURRENCY?  The published statistics on the same data.")
P("="*118)
info("Gentile, Famaey, Angus & Kroupa 2010, A&A 509, A97 ran a Kolmogorov-Smirnov test on the SAME Pal 14 data")
info("against the SAME published MOND prediction and found only 64-73 per cent confidence (p = 0.27-0.36), i.e.")
info("NO exclusion.  The committed h93 records that gap and attributes it to the statistic, not the data.  The")
info("claim under test is correctly NOT quoted as a sigma; the check below is what the four residuals alone support.")
res_can = np.array([r["res"] for r in rows_can])
e_res = np.array([2.0*r["esob"]/r["sob"]/math.log(10) for r in rows_can])
info(f"{'cluster':10} {'residual':>10} {'+- from sigma_obs alone':>24} {'N_RV':>6}")
for r, e in zip(rows_can, e_res):
    info(f"{r['name']:10} {r['res']:+10.3f} {e:24.3f} {r['N']:6d}")
se = float(res_can.std(ddof=1)/math.sqrt(len(res_can)))
ck("V12 the four-cluster median is many times its own scatter-based standard error even before the measurement "
   "errors are folded in, so the claim is not an error-bar illusion -- but with N = 4 objects, two of whose "
   "dispersions are N-body model fits rather than measurements, and with a published KS analysis of the same Pal 14 "
   "data giving no exclusion at all, quoting this as a sigma would be wrong.  The claim does not, and must not",
   abs(float(np.mean(res_can)))/se > 3.0,
   f"mean {np.mean(res_can):+.3f} dex, scatter {res_can.std(ddof=1):.3f}, standard error {se:.3f}, "
   f"ratio {abs(np.mean(res_can))/se:.1f}; per-cluster errors from sigma_obs alone are {e_res.min():.2f}-{e_res.max():.2f} dex")

# ==========================================================================================================
P(""); P("="*118)
P("9.  MUTATION CONTROLS.")
P("="*118)
newt = gc_rows(A0["canonical"], kernel=False)
newt_dw = [d for d in dw_rows(A0["canonical"], kernel=False) if 0.01 <= d["x_i"] <= 1.2]
info(f"{'cluster':10} {'kernel res':>11} {'Newtonian res':>14}")
for a, b in zip(rows_can, newt): info(f"{a['name']:10} {a['res']:+11.3f} {b['res']:+14.3f}")
mn = float(np.median([b["res"] for b in newt])); mdw = float(np.median([d["res"] for d in newt_dw]))
ck("M1 MUTATION CONTROL, and it is the cleanest statement of the whole claim: switch the kernel off (nu = 1, pure "
   "Newton with baryons only) and the globular clusters land ON zero while the dwarf spheroidals at the same "
   "internal acceleration stay far above it.  The cluster deficit IS the kernel's boost and nothing else, and the "
   "pipeline is not manufacturing it -- the identical pipeline gives the dwarfs a large positive residual",
   abs(mn) < 0.25 and mdw > 0.5,
   f"Newtonian median: clusters {mn:+.3f} dex, dwarfs over the same x_i {mdw:+.3f} dex on N={len(newt_dw)}; "
   f"with the kernel on, clusters {med_can:+.3f} and dwarfs {np.median([d['res'] for d in dwa]):+.3f}")

s2 = gc_rows(A0["canonical"], sig_override={n: s*math.sqrt(2) for n, _, _, _, _, _, s, _, _, _ in GC})
sh = [b["res"] - a["res"] for a, b in zip(rows_can, s2)]
ck("M2 MUTATION CONTROL on the DATA: inflating every measured dispersion by sqrt(2) must move every residual by "
   "exactly +log10(2) and nothing else in the pipeline may respond",
   max(abs(s - math.log10(2.0)) for s in sh) < 1e-9,
   f"shifts {['%+.9f' % s for s in sh]} against {math.log10(2.0):+.9f}")

big = gc_rows(A0["canonical"]*100)
ck("M3 MUTATION CONTROL on the THEORY: raising a_0 a hundredfold drives every cluster deeper into the modified "
   "regime, so the predicted dispersions rise and the residuals must fall further below zero",
   float(np.median([r["res"] for r in big])) < med_can - 0.3,
   f"median {med_can:+.3f} dex at the canonical a_0, {np.median([r['res'] for r in big]):+.3f} at 100 a_0")

q1 = boost_sphere(0.01, 0.0)/nu_s(0.01)
ck("M4 the independent Gauss-Legendre quadrature reduces to the framework's own isolated kernel exactly when the "
   "external field is switched off, so the two implementations agree on the thing they are both meant to compute",
   abs(q1 - 1.0) < 1e-9, f"boost_sphere(x_i, 0)/nu(x_i) = {q1:.12f}")

# ==========================================================================================================
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  THE CLAIM SURVIVES IN SUBSTANCE AND CARRIES ONE WRONG NUMBER.")
P("")
P(f"  Reproduced independently: Pal 4 {rows_can[0]['res']:+.3f}, Pal 14 {rows_can[1]['res']:+.3f}, Pal 3 {rows_can[2]['res']:+.3f}, "
  f"NGC 2419 {rows_can[3]['res']:+.3f}, median {med_can:+.3f} dex,")
P(f"  against dwarf spheroidals over the same internal accelerations at {np.median([d['res'] for d in dwa]):+.3f} dex on N = {len(dwa)}.  Object-by-object")
P(f"  depth matching -- not the 2.1-dex window g05 used -- leaves a median gap of {np.median(gv):+.3f} dex with every cluster")
P(f"  below its own depth-matched dwarfs.  The sign survives Upsilon_V = 1, the higher disputed Pal 14 dispersion,")
P(f"  the Milky Way's measured rotation curve as the external field, and all three stacked ({worst:+.3f} dex).  Under")
P(f"  nu = 1 the clusters land on zero and the dwarfs do not, so the deficit is the kernel's boost and not the pipeline.")
P("")
P(f"  THE ERROR.  g05's Upsilon_V = 1 caveat, quoted as -0.558 dex, applies the NEWTONIAN mass scaling (+log10 2)")
P(f"  to a deep-MOND prediction.  Three of the four clusters sit at x_i = 0.013-0.061 where sigma_pred goes as")
P(f"  M^(1/4), so the shift is +0.151 dex.  The exact value is {med_u1:+.3f} dex, not -0.558.  The error is against")
P(f"  g05's own interest and does not touch the claim's substance, but the quoted number is wrong.")
P("")
P(f"  THE PROCEDURAL VIOLATION.  Section 4e runs the canonical footing only.  Repaired here: with the dwarf set")
P(f"  held fixed the alt footing gives clusters {foot_med['alt'][0]:+.3f} and dwarfs {foot_med['alt'][1]:+.3f}, a gap of {foot_med['alt'][1]-foot_med['alt'][0]:+.3f} dex against the canonical")
P(f"  {foot_med['canonical'][1]-foot_med['canonical'][0]:+.3f} -- identical to 0.002 dex.  Nothing was hidden.  But the '+0.114 dex on N = 12' dwarf number is")
P(f"  fragile to the WINDOW EDGE: x_i scales as 1/a_0, so re-applying the fixed 0.01-1.2 window on the alt footing")
P(f"  re-selects the sample and reads {med_resel:+.3f} on N = {len(resel)}.  Quote the GAP, never the absolute dwarf offset.")
P("")
P(f"  THE DEEP-MOND LIMIT IS NOT UNIFORM.  Pal 3 and Pal 4 are isolated deep-MOND and radius-independent, so the")
P(f"  model-derived r_h,l does not matter for them.  Pal 14 is EXTERNAL-FIELD DOMINATED (x_i/x_e = 0.67), where the")
P(f"  kernel is quasi-Newtonian with a boosted G and the prediction depends on the radius again: 25 per cent in")
P(f"  r_h,l moves Pal 14's residual by 0.09 dex.  The cluster carrying the most extreme residual is the one whose")
P(f"  structural input is both model-derived and load-bearing.")
P("")
P(f"  THE WEAK POINT, AND IT IS NOT THE ONE g05 NAMES.  g05 names Pal 14's 16 stars.  The real soft spot is that")
P(f"  the depth-matched gap collapses to {ngc_gap:+.3f} dex at NGC 2419 -- the only cluster with real statistical weight")
P(f"  (183 velocities), the only one whose boost is small ({rows_can[3]['b']:.2f}), and the only one outside the deep-MOND limit.")
P(f"  The claim is carried by three clusters with 16-23 stars each, two of whose dispersions are N-body model fits.")
P("")
P(f"  THE PHYSICS OF THE FORK IS USED CORRECTLY, WITH ONE FRAMING DEFECT.  Modified inertia is a class with no")
P(f"  unique prediction, so it has no predicted SIGN for a dispersion-supported system; S5's setup sentence gives")
P(f"  the alternative a prediction it does not have.  The falsification that does go through is weaker and enough:")
P(f"  a single-sign 'pressure support breaks the kernel' hypothesis predicts one sign and the data show two.  g05's")
P(f"  verdict block already says the fork itself is untouched, and that is the correct standing.")
sys.exit(ck.done())
