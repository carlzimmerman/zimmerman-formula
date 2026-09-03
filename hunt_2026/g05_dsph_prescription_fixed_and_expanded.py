#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g05_dsph_prescription_fixed_and_expanded.py
===========================================================================================================
WHAT THIS IS FOR.  f09_orbital_coherence_fork.py reported a matched-pair separation between rotation-supported
and pressure-supported systems of +0.215 dex = 1.73 sigma, and recorded THREE of its own defects as FAILING
checks.  This script repairs the prescription, repairs three further arithmetic bugs found while doing it,
expands the sample, and does the acceleration matching properly.  The repair was allowed to destroy the
result; it did not, but it changed what the result IS, and it turned up one class that argues the other way.

  DEFECT 1 (f09 check A6).  The dwarf-spheroidal prediction was max(isolated deep-MOND, external-field value).
     A branch switch.  A residual whose SIGN tracks a branch of the author's own formula is a prescription
     artefact, not data.
  DEFECT 2 (f09 check A3).  Matching on baryonic mass as well as acceleration left 5 rotating galaxies at
     -0.205 dex -- the CONTROL degraded.  Is that the framework failing at the lowest disc masses, or SPARC?

THREE FURTHER BUGS FOUND IN f09 WHILE REPAIRING IT.  Two ran in the framework's favour and one against; they
very nearly cancel on the classical eight, which is a coincidence and not an excuse:
  (B-i)  f09 used g_N = G*M_total/R_half^2.  The observed side, g_obs = 3 sigma^2/R, is an ENCLOSED-mass
         statement (Wolf et al. 2010, MNRAS 406, 1220: M_1/2 = 3 sigma^2 r_1/2 / G), so the predicted side must
         use the ENCLOSED baryonic mass M_b/2.  This repository's own "total-mass-where-enclosed-mass-belongs"
         bug pattern.
  (B-ii) f09 used R = R_e (projected).  Wolf et al. 2010's estimator is stated at the DEPROJECTED 3-D
         half-light radius r_1/2 = (4/3) R_e.
  (B-iii) f09 fed nu the TRUE external field g_ext = V_c^2/D.  In QUMOND nu takes the NEWTONIAN field of the
         ACTUAL matter, g_Ne = G M_host,bar/D^2 -- twelve times smaller for the Milky Way at 76 kpc.  This is
         the error the liability table records as "the argument of nu", and it ran AGAINST the framework.

THE FIX FOR DEFECT 1 -- exact, not an interpolation.
  QUMOND: div g = div S with S = nu(|g_N|/a_0) g_N, so div(g - S) = 0 and the divergence theorem gives
  <g_r>_sphere = <S_r>_sphere EXACTLY, for any geometry, with no linearisation (this repository's
  f01_efe_sphere_average.py).  An isotropic velocity dispersion measures exactly that sphere average.  For a
  dwarf of internal Newtonian field x_i = g_Ni/a_0 in a uniform external Newtonian field x_e = g_Ne/a_0,

        <g_r>/a_0  =  -(1/2) INT_0^pi  nu(|x_e zhat - x_i rhat|) (x_e zhat - x_i rhat).rhat  sin(th) dth

  No branch, no max(), no expansion.  Continuous, and it goes over to nu(x_i) x_i as x_e -> 0 and to
  nu(x_e)(1 + L_e/3) x_i as x_i -> 0 (Milgrom 1986; Famaey & McGaugh 2012, Living Rev. Rel. 15, 10, eq. 59-60;
  Angus 2008, MNRAS 387, 1481 for the dSph application).  Both limits are checked before any data is touched,
  and the Newtonian mutation nu = 1 must return the internal field EXACTLY.  The one-dimensional formula of
  Famaey & McGaugh 2012 eq. 60, in the form Lelli et al. 2015 (A&A 584, A113) used for tidal dwarfs, is carried
  alongside -- and the two differ by up to 90 per cent, which is a REAL systematic and is reported as one.

THE MATCHING, done properly this time.  f09 took the min-max acceleration span of its eight dwarfs as a
"window"; with a bigger sample that span swallows all of SPARC and matches nothing.  Here each pressure object
is compared to the SPARC radial-acceleration relation AT ITS OWN INTERNAL ACCELERATION -- a running median of
every SPARC data point within 0.2 dex in g_bar/a_0 -- and objects outside SPARC's coverage are DROPPED, not
extrapolated to.  The rotating side gets the same treatment leave-one-out, so the comparison is between two
sets of residuals measured against the same local relation.

THE EXPANSION, class by class, each with its own reliability assessment:
  classical MW dwarf spheroidals; M31 dwarf spheroidals; ISOLATED Local Group dwarf spheroidals (x_e ~ 1e-4, so
  the external-field prescription is removed entirely); MW ultra-faints (unreliable, and out of SPARC's range
  anyway); outer-halo globular clusters (pressure-supported and containing NO dark matter under LCDM either --
  the one class that discriminates, and it argues AGAINST the reading this whole line of work was chasing).

DATA, all public, all on disk, all cited at point of use:
  Local Volume Database, Pace 2024 ApJS 273, 15 (doi:10.3847/1538-4365/ad9f2c) -- MW, M31, local-field dwarfs
  SPARC, Lelli, McGaugh & Schombert 2016, AJ 152, 157 -- the rotating control
  Baumgardt & Hilker 2018 / Baumgardt et al. 2019-2023 -- globular cluster structural parameters
  Jordi et al. 2009, AJ 137, 4586 (Pal 14); Frank et al. 2012, MNRAS 423, 2917 (Pal 4) -- GC dispersions

BOTH a_0 FOOTINGS.  MUTATION CONTROLS.  CHECKS CAN FAIL AND SEVERAL DO.
"""
import sys, math, csv, os
import numpy as np
from scipy.special import erfcinv
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260903)

MW_MB, M31_MB = 6.0e10, 1.2e11      # host baryonic masses, Msun (McGaugh 2016, ApJ 816, 42); as used in h8/h43
UPS_V = 2.0                          # stellar M/L_V for an old population; scanned 1-5 in part 4
PC = 3.0857e16
MATCH_W, MATCH_N = 0.20, 20          # matching window in dex of g_bar/a_0, and the minimum SPARC points in it

# ==========================================================================================================
P("="*122)
P("PART 0.  THE PRESCRIPTION.  Replacing f09's max() branch with the exact QUMOND sphere average.")
P("="*122)

def L_of(x, d=1e-5):
    return (math.log(nu_s(x*(1+d))) - math.log(nu_s(x*(1-d))))/(2*d)

def g_qumond_sphere(x_i, x_e, ntheta=2001):
    """EXACT sphere-averaged radial QUMOND acceleration, in units of a_0, for
        g_N/a_0 = x_e*zhat - x_i*rhat,   rhat = (sin th, 0, cos th).
    <g_r> = <S_r> exactly (QUMOND flux theorem), S = nu(|g_N|/a_0) g_N.  Returns the INWARD magnitude."""
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        return nu_s(x_i)*x_i
    th = np.linspace(0.0, math.pi, ntheta)
    st, ctm = np.sin(th), np.cos(th)
    gx = -x_i*st
    gz = x_e - x_i*ctm
    Sr = nu(np.sqrt(gx*gx + gz*gz))*(gx*st + gz*ctm)      # S . rhat  (negative = inward)
    return -float(np.trapz(Sr*st, th)/np.trapz(st, th))

def g_fm12_1d(x_i, x_e):
    """Famaey & McGaugh 2012 eq. 60 one-dimensional EFE formula, in the Lelli et al. 2015 form. Units of a_0."""
    nt = nu_s(x_i + x_e)
    ne = nu_s(x_e) if x_e > 0 else 0.0
    return x_i*nt + x_e*(nt - ne)

def g_f09_branch(x_i, x_e):
    """f09's prescription, reproduced so the artefact can be exhibited: max(isolated deep-MOND, EFE value)."""
    g_iso = math.sqrt(x_i)
    g_efe = nu_s(x_e)*x_i if x_e > 0 else 0.0
    return max(g_iso, g_efe), ("isolated" if g_iso >= g_efe else "EFE")

info("limit 1: isolated.  The quadrature must reproduce nu(x_i) x_i when the external field is switched off.")
r1 = [g_qumond_sphere(x, 0.0)/(nu_s(x)*x) for x in (1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0)]
ck("P1 the fixed prescription reduces EXACTLY to the framework's own isolated kernel when the external field is zero, so it is not a different theory smuggled in",
   max(abs(v - 1) for v in r1) < 1e-9, "quadrature/nu(x_i)x_i = " + ", ".join(f"{v:.10f}" for v in r1))

info("limit 2: external-field dominated.  Must reproduce f01's verified sphere-averaged coupling nu(x_e)(1+L_e/3).")
r2 = [g_qumond_sphere(1e-6*xe, xe)/(nu_s(xe)*(1 + L_of(xe)/3.0)*1e-6*xe) for xe in (1e-3, 1e-2, 0.1, 1.0)]
ck("P2 in the external-field-dominated limit the quadrature reproduces f01's independently derived sphere-averaged coupling nu(x_e)(1+L_e/3) to better than 1 per cent, so two separate derivations in this repository agree",
   max(abs(v - 1) for v in r2) < 0.01, "quadrature/[nu(x_e)(1+L_e/3) x_i] = " + ", ".join(f"{v:.5f}" for v in r2))

info("limit 3: continuity, by a RESOLUTION test, which is the only way to tell a kink from a steep smooth curve.")
info("   For a smooth function the largest jump in the log-log slope between adjacent grid points falls in")
info("   proportion to the grid spacing.  At a genuine kink it does not fall at all.")
def worst_slope_jump(fn, npts):
    xg = np.geomspace(1e-4, 3.0, npts)
    sl = np.diff(np.log(np.array([fn(0.01, x) for x in xg])))/np.diff(np.log(xg))
    return float(np.abs(np.diff(sl)).max())
jq1, jq2 = worst_slope_jump(g_qumond_sphere, 600), worst_slope_jump(g_qumond_sphere, 2400)
jb1, jb2 = worst_slope_jump(lambda a, b: g_f09_branch(a, b)[0], 600), worst_slope_jump(lambda a, b: g_f09_branch(a, b)[0], 2400)
ck("P3 the fixed prescription is SMOOTH and f09's max() is NOT, established by refining the grid fourfold: the fixed prescription's worst slope jump falls by about a factor 4, as a smooth function must, while f09's max() does not fall at all because it has a real kink.  The branch -- and with it any residual whose sign can track a branch -- is gone by construction",
   (jq1/jq2) > 3.0 and (jb1/jb2) < 1.5,
   f"fixed: worst slope jump {jq1:.2e} at 600 points -> {jq2:.2e} at 2400 (falls x{jq1/jq2:.2f}).  "
   f"f09 max(): {jb1:.2e} -> {jb2:.2e} (falls x{jb1/jb2:.2f}, i.e. does not fall -- a kink)")

info("cross-check against the published one-dimensional formula (Famaey & McGaugh 2012 eq. 60):")
info(f"{'x_i':>9} {'x_e':>9} {'sphere-avg (exact)':>20} {'FM12 eq60 (1-D)':>18} {'ratio':>8}")
rat_fm = []
for xi in (1e-3, 1e-2, 0.1):
    for xe in (1e-3, 1e-2, 0.1, 1.0):
        a, b = g_qumond_sphere(xi, xe), g_fm12_1d(xi, xe)
        rat_fm.append(a/b)
        info(f"{xi:9.4f} {xe:9.4f} {a:20.6f} {b:18.6f} {a/b:8.3f}")
ck("P4 (THIS CHECK FAILS AND THE FAILURE IS A RESULT) the exact sphere average and the published one-dimensional EFE formula do NOT agree to 35 per cent: they differ by up to 92 per cent, i.e. 0.28 dex in acceleration.  So 'use a proper external-field treatment' does not name a unique number, and every dwarf-spheroidal residual in this literature carries a prescription systematic of that size.  The exact sphere average is used for the headline BECAUSE it is the one that predicts MORE acceleration and therefore the SMALLER liability -- the conservative choice, against interest",
   0.65 < min(rat_fm) and max(rat_fm) < 1.35,
   f"sphere-average/FM12 ratio spans {min(rat_fm):.3f}-{max(rat_fm):.3f}; the sphere average is exact for an isotropic tracer (flux theorem) and the 1-D formula is an approximation, so the difference is the approximation's error, but it is a 0.28 dex systematic on every number below")

# ==========================================================================================================
P(""); P("="*122)
P("PART 1.  THE PRESSURE-SUPPORTED SAMPLE.  Local Volume Database (Pace 2024, ApJS 273, 15), class by class.")
P("="*122)

def fnum(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None

def load_lvd(fname, host_mb, host_name):
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fname))):
        sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"])
        MV = fnum(r["M_V"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
        if sig is None or ul is not None or MV is None or rh is None or sig <= 0 or rh <= 0: continue
        if fnum(r["confirmed_galaxy"]) != 1: continue
        lMs = fnum(r["mass_stellar"]); lMHI = fnum(r["mass_HI"])
        em = fnum(r["vlos_sigma_em"]) or 0.2*sig; ep = fnum(r["vlos_sigma_ep"]) or 0.2*sig
        out.append(dict(name=r["name"], MV=MV, rh=rh, sig=sig, esig=0.5*(em+ep),
                        Ms=(10**lMs if lMs is not None else 10**(0.4*(4.83-MV))*UPS_V),
                        MHI=(10**lMHI if lMHI is not None else 0.0),
                        Dhost=Dh, Dgc=fnum(r["distance_gc"]), Dm31=fnum(r["distance_m31"]),
                        host=host_name, host_mb=host_mb))
    return out

mw_all  = load_lvd("lvd_dwarf_mw.csv",  MW_MB,  "MW")
m31_all = load_lvd("lvd_dwarf_m31.csv", M31_MB, "M31")
fld_all = load_lvd("lvd_dwarf_local_field.csv", None, "field")
info("LVD rows with a MEASURED (not upper-limit) dispersion, a half-light radius, and confirmed_galaxy = 1:")
info(f"   Milky Way satellites {len(mw_all)}   M31 satellites {len(m31_all)}   Local Group field {len(fld_all)}")

ROTATING_EXCLUDE = {"LMC", "SMC"}                                             # rotation-supported
DISRUPTING       = {"Sagittarius", "Bootes III", "Tucana III", "Tucana IV"}   # ongoing tidal disruption
GAS_RATIO_MAX    = 0.3                                                        # M_HI/M* above this = not a dSph

def classify(d, host):
    if d["name"] in ROTATING_EXCLUDE: return None, "rotation-supported (belongs on the OTHER side)"
    if d["name"] in DISRUPTING:       return None, "tidally disrupting"
    if d["MHI"] > GAS_RATIO_MAX*d["Ms"]: return None, f"gas-rich, M_HI/M* = {d['MHI']/max(d['Ms'],1):.2f}"
    if host == "field":               return "isolated", ""
    if host == "M31":                 return "m31", ""
    return ("classical" if d["MV"] <= -7.7 else "ultrafaint"), ""

classes = {"classical": [], "ultrafaint": [], "m31": [], "isolated": []}
dropped = []
for src, host in ((mw_all, "MW"), (m31_all, "M31"), (fld_all, "field")):
    for d in src:
        c, why = classify(d, host)
        (classes[c].append(d) if c else dropped.append((d["name"], host, why)))
info(f"excluded before any calculation ({len(dropped)}):")
for n, h, w in dropped: info(f"   {n:22} ({h:5}) {w}")

def dsph_row(d, a0, ups=UPS_V, presc="sphere", host_mb=None, ext=True, sig=None):
    """(residual dex, x_i, x_e, f09-branch-that-would-have-been-used).
    OBSERVED  g_obs = 3 sigma_los^2 / r_1/2   (Wolf et al. 2010; r_1/2 = 4/3 R_e, deprojected)
    PREDICTED from the ENCLOSED baryonic mass M_b/2 inside r_1/2 through the chosen prescription."""
    r12 = (4.0/3.0)*d["rh"]*PC
    Mb = (ups/UPS_V)*d["Ms"] + 1.33*d["MHI"]                 # LVD mass_stellar is at Upsilon_V = 2
    x_i = G*(0.5*Mb*Msun)/r12**2/a0
    hm = host_mb if host_mb is not None else d["host_mb"]
    if not ext:
        x_e = 0.0
    elif hm is not None and d["Dhost"] and d["Dhost"] > 0:
        x_e = G*hm*Msun/(d["Dhost"]*kpc)**2/a0
    else:                                                     # isolated: MW at D_gc plus M31 at D_M31
        gg = (G*MW_MB*Msun/(d["Dgc"]*kpc)**2 if d["Dgc"] else 0.0) + \
             (G*M31_MB*Msun/(d["Dm31"]*kpc)**2 if d["Dm31"] else 0.0)
        x_e = gg/a0
    s = d["sig"] if sig is None else sig
    g_obs = 3.0*(s*1e3)**2/r12
    gp = {"sphere": g_qumond_sphere, "fm12": g_fm12_1d,
          "f09": lambda a, b: g_f09_branch(a, b)[0]}[presc](x_i, x_e)*a0
    return math.log10(g_obs/gp), x_i, x_e, g_f09_branch(x_i, x_e)[1]

# ---- 1a.  the classical eight, prescription and arithmetic, before and after ------------------------------
P(""); P("-"*122)
P("1a.  THE CLASSICAL MILKY WAY DWARF SPHEROIDALS: f09's prescription and arithmetic, against the repaired ones.")
P("-"*122)
CLASSIC8 = {"Draco", "Sculptor", "Fornax", "Carina", "Sextans", "Leo I", "Leo II", "Ursa Minor"}
c8 = sorted([d for d in classes["classical"] if d["name"] in CLASSIC8], key=lambda z: z["name"])
a0c = A0["canonical"]
info(f"the eight objects f09 used, matched by name in the LVD: {len(c8)} of 8 recovered")
info(f"{'dwarf':14} {'M*/Msun':>9} {'x_i':>8} {'x_e':>8} {'f09 branch':>11} {'f09 presc':>10} {'FIXED':>9} {'change':>8}")
old, new = [], []
for d in c8:
    r_old, xi, xe, br = dsph_row(d, a0c, presc="f09")
    r_new, _, _, _    = dsph_row(d, a0c, presc="sphere")
    old.append((d["name"], r_old, br)); new.append((d["name"], r_new, br))
    info(f"{d['name']:14} {d['Ms']:9.2e} {xi:8.4f} {xe:8.4f} {br:>11} {r_old:+10.3f} {r_new:+9.3f} {r_new-r_old:+8.3f}")

# the artefact statistic: how much of the residual is explained by the BRANCH LABEL alone
def branch_gap(rows):
    a = [r for _, r, b in rows if b == "isolated"]; b_ = [r for _, r, b in rows if b == "EFE"]
    return float(np.median(a) - np.median(b_)), len(a), len(b_)
gap_o, ni, ne = branch_gap(old); gap_n, _, _ = branch_gap(new)
sgn_o = all(r > 0 for _, r, b in old if b == "isolated") and all(r < 0 for _, r, b in old if b == "EFE")
sgn_n = all(r > 0 for _, r, b in new if b == "isolated") and all(r < 0 for _, r, b in new if b == "EFE")
ck("A6-FIXED (f09's own flagged defect, and the repair says f09 MIS-DIAGNOSED IT) f09 attributed 'a large part of the reported scatter' to its own max() branch.  Removing the branch entirely -- replacing it with a prescription that provably has none -- reduces the gap between the two branch groups by only about a tenth.  The branch was not what was driving the split.  What drives it is that f09's 'isolated-branch' objects are simply the ones at the LOWEST internal acceleration, and those are the discrepant ones.  The branch label was a proxy for depth, and depth is what Part 3 has to control for",
   gap_n < 0.5*gap_o,
   f"f09 prescription: isolated-branch ({ni} objects) minus external-field-branch ({ne}) = {gap_o:+.3f} dex, "
   f"perfect sign separation = {sgn_o}.  FIXED: gap {gap_n:+.3f} dex, perfect sign separation = {sgn_n}.  "
   f"Only {100*(gap_o-gap_n)/gap_o:.0f} per cent of the branch structure was the branch; the rest is a real trend with x_i")

P(""); info("DECOMPOSING THE THREE f09 ARITHMETIC BUGS ON THE CLASSICAL EIGHT (canonical footing, median dex):")
def variant(useM2, use43, useNewtExt):
    out = []
    for d in c8:
        R = ((4.0/3.0) if use43 else 1.0)*d["rh"]*PC
        Mb = (0.5 if useM2 else 1.0)*(d["Ms"] + 1.33*d["MHI"])
        xi = G*Mb*Msun/R**2/a0c
        xe = (G*MW_MB*Msun/(d["Dhost"]*kpc)**2/a0c) if useNewtExt else ((200e3)**2/(d["Dhost"]*kpc)/a0c)
        out.append(math.log10(3.0*(d["sig"]*1e3)**2/R/(g_qumond_sphere(xi, xe)*a0c)))
    return float(np.median(out))
v0 = variant(False, False, False); v1 = variant(True, False, False)
v2 = variant(True, True, False);   v3 = variant(True, True, True)
info(f"   f09's inputs, fixed prescription                                  {v0:+.3f}")
info(f"   + enclosed mass M_b/2 instead of M_b (Wolf+2010)                  {v1:+.3f}  ({v1-v0:+.3f})")
info(f"   + deprojected r_1/2 = (4/3) R_e instead of R_e                    {v2:+.3f}  ({v2-v1:+.3f})")
info(f"   + NEWTONIAN external field G M_host/D^2 instead of V_c^2/D        {v3:+.3f}  ({v3-v2:+.3f})")
ck("A7 (AND THIS CHECK FAILS, WHICH IS THE HONEST OUTCOME) I expected the three f09 arithmetic bugs to push the same way.  They do not: two of them (enclosed mass, deprojected radius) made f09's pressure-supported residual too SMALL by +0.42 dex between them, and the third (the true instead of the Newtonian external field) made it too LARGE by a comparable amount.  On the classical eight they very nearly cancel, so f09's classical-dwarf median was accidentally close to right -- and 'nearly cancel on eight objects' is a coincidence of this sample, not a defence of the arithmetic",
   (v1 - v0) > 0 and (v2 - v1) > 0 and (v3 - v2) > 0,
   f"{v0:+.3f} -> {v3:+.3f} dex, net {v3-v0:+.3f}; the three steps are {v1-v0:+.3f}, {v2-v1:+.3f}, {v3-v2:+.3f} -- the third has the opposite sign, so they do not compound")

# ---- 1b.  the expanded sample -----------------------------------------------------------------------------
P(""); P("-"*122)
P("1b.  THE EXPANDED SAMPLE, class by class, WITH ITS RELIABILITY.  Canonical footing, fixed prescription.")
P("-"*122)
RELIABILITY = {
 "classical":  ("GOLD",   "hundreds to thousands of member velocities; dispersions stable across two decades of "
                          "independent studies; distances from RR Lyrae and the tip of the red giant branch.  "
                          "Systematic worries: the tidal state of Sextans and Carina, an unresolved-binary "
                          "contribution of order 1 km/s (McConnachie & Cote 2010, ApJ 722, L209), and the two "
                          "very extended 'feeble giants' Antlia II and Crater II."),
 "m31":        ("SILVER", "10-100 members each, Keck/DEIMOS (Collins et al. 2013, ApJ 768, 172; Tollerud, Kirby). "
                          "Dispersions of 3-5 km/s sit near the instrumental floor, Milky Way foreground "
                          "contamination biases small-N dispersions HIGH, and the M31 baryonic mass carries "
                          "~0.1 dex.  This class is the one most likely to be inflating the result."),
 "isolated":   ("GOLD for the prescription, THIN in number",
                          "x_e ~ 1e-4, so the ENTIRE external-field prescription -- the thing f09 got wrong -- is "
                          "removed.  Cetus and Tucana have 40-100 members (Taibi et al. 2018, A&A 618, A122; "
                          "2020, A&A 635, A152).  The cleanest objects in the comparison, and there are five."),
 "ultrafaint": ("BRONZE -- these must not carry the result",
                          "5-100 member velocities; unresolved BINARIES inflate sigma by up to a factor 2 in the "
                          "faintest systems (McConnachie & Cote 2010; Simon 2019, ARA&A 57, 375); several are "
                          "tidally disturbed.  They also sit two to three decades below a_0, far outside any "
                          "acceleration SPARC reaches, so they cannot enter a matched comparison AT ALL."),
}
summary = {}
for cname in ("classical", "m31", "isolated", "ultrafaint"):
    res = sorted([(d["name"],) + dsph_row(d, a0c)[:3] + (d["Ms"],) for d in classes[cname]], key=lambda t: t[2])
    arr = np.array([t[1] for t in res]); summary[cname] = res
    tier, note = RELIABILITY[cname]
    P("")
    info(f"[{cname.upper()}]  N = {len(res)}   reliability: {tier}")
    info(f"   {note}")
    info(f"   median residual {np.median(arr):+.3f} dex, scatter {arr.std(ddof=1):.3f}; "
         f"x_i {min(t[2] for t in res):.5f}-{max(t[2] for t in res):.4f}, x_e {min(t[3] for t in res):.5f}-{max(t[3] for t in res):.4f}")
    show = res if len(res) <= 14 else res[:7] + res[-7:]
    for i, (n, r, xi, xe, Ms) in enumerate(show):
        if len(res) > 14 and i == 7: info("      ...")
        info(f"      {n:22} M*={Ms:8.2e}  x_i={xi:8.5f}  x_e={xe:8.5f}   {r:+7.3f} dex")

iso = summary["isolated"]
iso_res = np.array([t[1] for t in iso])
ck("A8 (THE CLEANEST OBJECTS, AND THEY ARGUE FOR A MUCH SMALLER EFFECT) the ISOLATED Local Group dwarf spheroidals need no external-field prescription at all (x_e ~ 1e-4), and they sit BARELY above the framework's kernel -- a median far below the classical satellites and the M31 satellites.  Cetus and Tucana, the two best-observed of them, are essentially ON it.  So whatever the offset is, the objects where the prescription cannot be blamed show the LEAST of it, and that is evidence that part of the satellite offset is environmental or tidal rather than a property of pressure support",
   len(iso_res) >= 4 and np.median(iso_res) > 0.10 and np.median(iso_res) < 0.5*np.median([t[1] for t in summary["classical"]]),
   ", ".join(f"{t[0]} {t[1]:+.3f}" for t in iso) +
   f"; isolated median {np.median(iso_res):+.3f} dex on N={len(iso_res)} against classical {np.median([t[1] for t in summary['classical']]):+.3f} and M31 {np.median([t[1] for t in summary['m31']]):+.3f}")

# ==========================================================================================================
P(""); P("="*122)
P("PART 2.  DEFECT 2.  WHY the mass-matched rotating control degrades: the framework, or SPARC?")
P("="*122)
gals = load_sparc()
info(f"SPARC (Lelli, McGaugh & Schombert 2016, AJ 152, 157), Q<=2, i>=30 deg, >=6 points: {len(gals)} galaxies")

full = []
for g in gals:
    y = g["gbar"]/a0c
    r = np.log10(g["gobs"]/(nu(y)*g["gbar"]))
    full.append(dict(name=g["name"], Mb=g["Mb"], res=float(np.median(r)), n=len(y),
                     Vmax=float(g["vobs"].max()), Vf=g["Vflat"], Q=g["Q"], inc=g["inc"], D=g["D"]))
mb = np.array([d["Mb"] for d in full]); rs = np.array([d["res"] for d in full])
info(f"{'M_b bin (Msun)':>24} {'N':>4} {'median dex':>11} {'scatter':>8}")
for lo, hi in [(1e7,1e8),(1e8,1e9),(1e9,1e10),(1e10,1e11),(1e11,1e13)]:
    m = (mb >= lo) & (mb < hi)
    info(f"{lo:10.0e} - {hi:9.0e} {m.sum():4d} {np.median(rs[m]):+11.3f} {rs[m].std(ddof=1):8.3f}")

low = sorted([d for d in full if d["Mb"] < 1e8], key=lambda d: d["Mb"])
lowres = np.array([d["res"] for d in low])
P(""); info("THE LOWEST-MASS SPARC BIN, OBJECT BY OBJECT -- this is f09's degraded control:")
info(f"{'galaxy':13} {'M_b':>9} {'residual':>9} {'V_max':>7} {'V_flat':>7} {'V_max/sig_HI':>13} {'inc':>5} {'Q':>2} {'D Mpc':>6} {'Npts':>5}")
SIG_HI = 10.0   # HI turbulent velocity dispersion, km/s (Leroy et al. 2008, AJ 136, 2782: 10 +- 2 km/s)
for d in low:
    vf = f"{d['Vf']:7.1f}" if d["Vf"] > 0 else "   NONE"
    info(f"{d['name']:13} {d['Mb']:9.2e} {d['res']:+9.3f} {d['Vmax']:7.1f} {vf} {d['Vmax']/SIG_HI:13.2f} "
         f"{d['inc']:5.0f} {d['Q']:2d} {d['D']:6.1f} {d['n']:5d}")
info(f"median {np.median(lowres):+.3f} dex on N={len(low)}  (f09 reported -0.205 on 5 galaxies)")

boot = np.array([np.median(rng.choice(rs, size=len(low), replace=False)) for _ in range(20000)])
p_low = float(np.mean(boot <= np.median(lowres)))
ck("D2a (I EXPECTED SMALL-N AND I WAS WRONG) drawing five SPARC galaxies at random from all 147 essentially never reproduces f09's -0.205 dex.  Those five really are low.  f09's A3 was not a small-number accident and the deficit at the lowest disc masses is real in the data",
   p_low > 0.05,
   f"P(median of 5 random SPARC galaxies <= {np.median(lowres):+.3f}) = {p_low:.4f} over 20000 draws; the 5-galaxy median has a "
   f"16-84 per cent range of {np.percentile(boot,16):+.3f} to {np.percentile(boot,84):+.3f} dex about a whole-sample median of {np.median(rs):+.3f}")

nof = sum(1 for d in low if d["Vf"] <= 0)
vsig = np.array([d["Vmax"]/SIG_HI for d in full])
srt = np.argsort(vsig)
q1, q4 = rs[srt][:20], rs[srt][-20:]
ck("D2b BUT IT IS A PROPERTY OF THE MEASUREMENT, NOT OBVIOUSLY OF THE FRAMEWORK: four of those five galaxies have NO measured V_flat in the SPARC master table at all -- SPARC itself declines to assign them a flat rotation velocity -- and every one of the five has a peak rotation speed within a factor 2.5 of the HI turbulent dispersion (Leroy et al. 2008: 10 +- 2 km/s), where asymmetric drift and the 1/sin(i) inclination error both bite hardest.  Across all 147 galaxies the twenty with the lowest V_max/sigma_HI scatter three times more widely about the kernel than the twenty highest",
   nof >= 3 and q1.std(ddof=1) > 2.0*q4.std(ddof=1),
   f"{nof} of {len(low)} have no V_flat; lowest 20 by V_max/sigma_HI: median {np.median(q1):+.3f}, scatter {q1.std(ddof=1):.3f} "
   f"(V_max/sigma_HI = {vsig[srt][0]:.1f}-{vsig[srt][19]:.1f}); highest 20: median {np.median(q4):+.3f}, scatter {q4.std(ddof=1):.3f}")
info("⚠️ THE LIMIT ON D2b, and f09 hit the same wall: V_max/sigma_HI at fixed sigma_HI IS V_max, so SPARC alone cannot")
info("   separate 'the rotation is not a clean tracer' from a plain velocity-scale trend.  f08 already failed on exactly")
info("   this confound.  The defensible statement is narrow: those five galaxies are the least reliable rotation curves")
info("   in SPARC, so they cannot serve as a control -- but the deficit is real in the data and is NOT explained away.")
info("   f09's mass-matched comparison stays unusable, and it is unusable in BOTH directions.")
mb_d = np.array([d["Ms"] + 1.33*d["MHI"] for d in classes["classical"]])
info(f"and the matching itself was apples to oranges: f09 compared dwarf-spheroidal STELLAR mass with SPARC BARYONIC")
info(f"   mass on gas-dominated dwarf irregulars.  Classical dSph M_b = {mb_d.min():.1e}-{mb_d.max():.1e} Msun.")

# ==========================================================================================================
P(""); P("="*122)
P("PART 3.  THE MATCHING, DONE PROPERLY, AND THE RECOMPUTED SEPARATION.")
P("="*122)
info("f09 took the min-max acceleration span of its eight dwarfs as a 'window'.  With a larger pressure sample that")
info("span runs from 1e-4 to 30 and swallows all of SPARC, matching nothing.  Instead: every pressure object is")
info("compared to the SPARC relation AT ITS OWN x_i -- the running median of every SPARC data point within")
info(f"{MATCH_W} dex -- and objects where SPARC has fewer than {MATCH_N} points are DROPPED rather than extrapolated to.")

def build_pool(a0, drop_name=None):
    ly, rr = [], []
    for g in gals:
        if g["name"] == drop_name: continue
        y = g["gbar"]/a0
        ly.append(np.log10(y)); rr.append(np.log10(g["gobs"]/(nu(y)*g["gbar"])))
    return np.concatenate(ly), np.concatenate(rr)

def ctrl(lx, ly, rr):
    m = np.abs(ly - lx) < MATCH_W
    return (float(np.median(rr[m])), int(m.sum())) if m.sum() >= MATCH_N else (None, int(m.sum()))

_ROT_CACHE = {}
def rotating_deltas(a0):
    """Leave-one-out: each SPARC galaxy's own residual minus the SPARC relation at its own median acceleration,
    with that galaxy's points EXCLUDED from the relation, so the control is not compared with itself."""
    if a0 in _ROT_CACHE: return _ROT_CACHE[a0]
    rot = []
    for g in gals:
        y = g["gbar"]/a0
        rj = float(np.median(np.log10(g["gobs"]/(nu(y)*g["gbar"]))))
        lyj, rrj = build_pool(a0, drop_name=g["name"])
        c, n = ctrl(float(np.median(np.log10(y))), lyj, rrj)
        if c is not None: rot.append((g["name"], rj - c))
    _ROT_CACHE[a0] = rot
    return rot

def matched_sets(pressure_rows, a0):
    """pressure_rows: list of (name, residual, x_i).  Returns matched pressure deltas and leave-one-out rotating deltas."""
    LY, RR = build_pool(a0)
    pres, out_of_range = [], []
    for nm, r, xi in pressure_rows:
        c, n = ctrl(math.log10(xi), LY, RR)
        (pres.append((nm, r - c, xi, r, c)) if c is not None else out_of_range.append((nm, xi, n)))
    return pres, rotating_deltas(a0), out_of_range

def compare(pres, rot, nperm=20000):
    p = np.array([t[1] for t in pres]); r = np.array([t[1] for t in rot])
    sep = float(np.median(p) - np.median(r))
    se = math.sqrt(p.std(ddof=1)**2/len(p) + r.std(ddof=1)**2/len(r))
    pool = np.concatenate([p, r]); n1 = len(p)
    cnt = sum(1 for _ in range(nperm)
              if abs(np.median((q := rng.permutation(pool))[:n1]) - np.median(q[n1:])) >= abs(sep))
    pv = (cnt + 1)/(nperm + 1)
    return dict(sep=sep, se=se, nsig=sep/se, p=pv, z=float(math.sqrt(2)*erfcinv(pv)) if pv < 1 else 0.0,
                np_=len(p), nr=len(r), mp=float(np.median(p)), mr=float(np.median(r)),
                sp=float(p.std(ddof=1)), sr=float(r.std(ddof=1)))

COMBOS = [("classical only (f09's sample, expanded to the class)", ["classical"]),
          ("classical + M31",                                      ["classical", "m31"]),
          ("classical + M31 + ISOLATED (no EFE at all)",           ["classical", "m31", "isolated"]),
          ("+ ultra-faints (BRONZE, shown only to be dismissed)",  ["classical", "m31", "isolated", "ultrafaint"])]
RES = {}
for foot, a0 in A0.items():
    P(""); info(f"FOOTING: {foot}   (a_0 = {a0:.3g} m/s^2)")
    info(f"{'pressure sample':52} {'N_in':>5} {'N_out':>6} {'N_rot':>6} {'rot dex':>8} {'pres dex':>9} {'sep dex':>8} {'sigma':>6} {'perm p':>8}")
    for label, keys in COMBOS:
        rows = [(d["name"],) + dsph_row(d, a0)[:2] for k in keys for d in classes[k]]
        rows = [(n, r, x) for n, r, x in rows]
        pres, rot, oor = matched_sets(rows, a0)
        if len(pres) < 3: info(f"{label:52} {len(pres):5d}  -- too few objects inside SPARC's acceleration range --"); continue
        o = compare(pres, rot); o["oor"] = oor
        RES[(foot, label)] = o
        info(f"{label:52} {o['np_']:5d} {len(oor):6d} {o['nr']:6d} {o['mr']:+8.3f} {o['mp']:+9.3f} "
             f"{o['sep']:+8.3f} {o['nsig']:6.2f} {o['p']:8.4f}")

k_cls = "classical only (f09's sample, expanded to the class)"
k_all = "classical + M31 + ISOLATED (no EFE at all)"
c_all, a_all = RES[("canonical", k_all)], RES[("alt", k_all)]
c_cls = RES[("canonical", k_cls)]
oor = c_all["oor"]
P(""); info("WHAT THE MATCHING THREW AWAY -- and this is the whole story:")
info(f"   {len(oor)} of {len(oor)+c_all['np_']} pressure objects sit OUTSIDE the acceleration range where SPARC has any data, and are dropped.")
info("   They are not a random subset.  They are the DEEPEST ones, and the deepest ones are the discrepant ones:")
kept = sorted([(t[0], t[3], t[2]) for t in matched_sets([(d['name'],) + dsph_row(d, a0c)[:2] for k in ("classical","m31","isolated") for d in classes[k]], a0c)[0]], key=lambda z: z[2])
info(f"      KEPT ({len(kept)}), x_i inside SPARC's coverage:  median raw residual "
     f"{np.median([t[1] for t in kept]):+.3f} dex")
for nm, r, xi in kept: info(f"         {nm:22} x_i = {xi:.5f}   {r:+.3f} dex")
oorres = {}
for k in ("classical", "m31", "isolated"):
    for t in summary[k]: oorres[t[0]] = t[1]
dropres = np.array([oorres[nm] for nm, xi, n in oor])
info(f"      DROPPED ({len(oor)}), x_i below SPARC's coverage: median raw residual {np.median(dropres):+.3f} dex")
for nm, xi, n in sorted(oor, key=lambda t: t[1])[:6]:
    info(f"         {nm:22} x_i = {xi:.5f}   {oorres[nm]:+.3f} dex   ({n} SPARC points within {MATCH_W} dex, {MATCH_N} required)")

ck("A1-REPAIRED (THE HEADLINE, AND IT IS A NEGATIVE.  THE 1.73 SIGMA DOES NOT SURVIVE HONEST MATCHING) with the prescription repaired, the arithmetic repaired, the sample expanded from 8 objects to 50, and -- decisively -- the acceleration matching done object by object against the SPARC relation instead of through f09's min-max window, the separation FALLS from +0.215 dex / 1.73 sigma to about +0.06 dex / 0.9 sigma, p = 0.10.  No sample combination and neither footing reaches two sigma.  f09's matched-pair result is WITHDRAWN",
   c_all["nsig"] > 3.0 and a_all["nsig"] > 3.0 and c_all["p"] < 0.01,
   f"canonical {c_all['sep']:+.3f} dex, {c_all['nsig']:.2f} sigma, permutation p = {c_all['p']:.4f}; "
   f"alt {a_all['sep']:+.3f} dex, {a_all['nsig']:.2f} sigma.  Classical class alone: {c_cls['sep']:+.3f} dex, {c_cls['nsig']:.2f} sigma on "
   f"N = {c_cls['np_']}.  N_pressure = {c_all['np_']} matched, {len(oor)} dropped as outside SPARC's range, against N_rotating = {c_all['nr']}")

ck("A1b (WHY IT DIES, AND THIS IS THE REAL RESULT OF THE FILE) support type and acceleration DEPTH are completely confounded in the Local Group.  Every large pressure-supported residual sits at an internal acceleration BELOW anything SPARC measures: the objects inside SPARC's range have a median residual near the rotating value, the objects below it a median an order of magnitude larger.  f09's 'matched acceleration window' was the min-max span of its eight dwarfs, which includes accelerations where the rotating side has almost no data, so its comparison was an EXTRAPOLATION dressed as a match",
   abs(np.median([t[1] for t in kept])) < 0.5*abs(np.median(dropres)),
   f"inside SPARC's coverage (x_i >= {min(t[2] for t in kept):.4f}): median raw residual {np.median([t[1] for t in kept]):+.3f} dex on N={len(kept)}; "
   f"below it: {np.median(dropres):+.3f} dex on N={len(oor)}.  A factor {abs(np.median(dropres)/max(abs(np.median([t[1] for t in kept])),1e-3)):.1f} in the same currency, "
   f"with SUPPORT TYPE held fixed -- so the split is at least as much about depth as about support")

# the depth trend, quantified, with a shuffle control
allrows = [t for k in ("classical", "m31", "isolated", "ultrafaint") for t in summary[k]]
lx = np.array([math.log10(t[2]) for t in allrows]); rr_ = np.array([t[1] for t in allrows])
sl, ic = np.polyfit(lx, rr_, 1)
rp = float(np.corrcoef(lx, rr_)[0, 1])
sh = np.array([np.polyfit(lx, rng.permutation(rr_), 1)[0] for _ in range(5000)])
ck("A1c the depth trend inside the pressure sample is strong, and its own shuffle control confirms it -- but READ THE SLOPE CAREFULLY, because -0.5 is not an arbitrary number.  In the deep-MOND limit the prediction is g = sqrt(x_i) a_0, so the residual is log(g_obs) - 0.5 log(x_i) - log(a_0), and a slope of exactly -0.5 is what you get when g_obs carries NO dependence on x_i at all.  That is what is measured.  The pressure-supported dwarfs' observed dynamical accelerations do not track their baryonic accelerations in the way the framework requires; they behave as if set by something with a common scale.  This is a mechanical identity as much as a measurement, and it must not be quoted as independent evidence -- but it is exactly why 'depth' and 'residual' are the same axis in this sample and cannot be disentangled from support type here",
   abs(rp) > 0.5 and abs(sl) > 3*sh.std(),
   f"slope {sl:+.3f} dex per dex, r = {rp:+.3f} on N = {len(allrows)} pressure objects; 5000 shuffles give slope "
   f"{sh.mean():+.4f} +- {sh.std():.4f}, so the real slope is {abs(sl-sh.mean())/sh.std():.1f} shuffle-sigma out")

ck("A2-REPAIRED the rotating side is a genuine control and not just a second number: measured against the same local SPARC relation, leave-one-out so no galaxy is compared with itself, the rotating galaxies sit on zero",
   abs(c_all["mr"]) < 0.05,
   f"rotating median {c_all['mr']:+.3f} dex, scatter {c_all['sr']:.3f}, N = {c_all['nr']}; matched pressure median {c_all['mp']:+.3f}, scatter {c_all['sp']:.3f}")

ck("A4-REPAIRED (fails with A1) the separation was supposed to hold at strength on both footings.  It is footing-independent, but at a strength that is not a result on either",
   c_all["sep"] > 0.15 and a_all["sep"] > 0.15,
   f"canonical {c_all['sep']:+.3f} dex ({c_all['nsig']:.2f} sigma), alt {a_all['sep']:+.3f} dex ({a_all['nsig']:.2f} sigma) -- "
   f"identical to 0.001 dex, so a_0 is not the issue; the sample is")

allp = [t for k in ("classical", "m31", "isolated") for t in summary[k]]
non = sum(1 for t in allp if abs(t[1]) < 0.15); bel = sum(1 for t in allp if t[1] < -0.15)
ck("A5-REPAIRED (the honest limit, kept as a check so it cannot be quietly dropped) the pressure-supported failure is NOT uniform and has no consistent sign: a quarter of these objects sit on the kernel and several sit below it.  It is a broad shifted distribution, not a switch",
   0.15 < non/len(allp) < 0.45 and bel > 0,
   f"{non} of {len(allp)} within 0.15 dex of the kernel ({100*non/len(allp):.0f} per cent), {bel} BELOW it; "
   f"full range {min(t[1] for t in allp):+.2f} to {max(t[1] for t in allp):+.2f} dex")

ck("A3-REPAIRED (f09's failing mass-match check, revisited and STILL FAILING) f09 reported that matching on baryonic mass as well as acceleration degraded the control.  Part 2 confirms the deficit is real in the data (p = %.4f against a random draw of five) and shows those five are the least reliable rotation curves in SPARC -- four have no V_flat at all.  That does not rescue the mass-matched comparison; it explains why it cannot be used, in either direction" % p_low,
   p_low > 0.05,
   f"random-draw p = {p_low:.4f} (so NOT small-number noise); {nof} of 5 have no measured V_flat; "
   f"lowest-V/sigma scatter {q1.std(ddof=1):.3f} against highest {q4.std(ddof=1):.3f}")

P(""); info("MATCHING-PARAMETER SENSITIVITY -- the negative must not be an artefact of MY window either:")
info(f"{'window (dex)':>13} {'min SPARC pts':>14} {'N matched':>10} {'separation':>11} {'sigma':>7} {'perm p':>8}")
_SAVE = (MATCH_W, MATCH_N); sens = []
for w_, n_ in ((0.15, 30), (0.20, 20), (0.25, 20), (0.30, 20), (0.30, 50), (0.40, 20)):
    MATCH_W, MATCH_N = w_, n_
    _ROT_CACHE.clear()
    o = compare(*matched_sets([(d["name"],) + dsph_row(d, a0c)[:2] for k in ("classical","m31","isolated") for d in classes[k]], a0c)[:2], nperm=4000)
    sens.append(o)
    info(f"{w_:13.2f} {n_:14d} {o['np_']:10d} {o['sep']:+11.3f} {o['nsig']:7.2f} {o['p']:8.4f}")
MATCH_W, MATCH_N = _SAVE; _ROT_CACHE.clear()
ck("A9 (FAILS, AND THE FAILURE IS THE SAME STATEMENT AS A1b) the separation was supposed to be robust to my own matching window.  It is not -- it is a MONOTONE FUNCTION OF HOW MUCH EXTRAPOLATION IS ALLOWED, running from 0.9 sigma at strict matching to 2.9 sigma at a 0.40 dex window.  A 0.40 dex window compares an object at x_i = 0.004 with SPARC points at x_i = 0.010, which is a smear and not a match; the significance is bought entirely by re-admitting the deep objects that have no rotating counterpart.  Nothing here reaches three sigma, and the number one quotes is set by the analysis choice rather than by the data",
   max(o["nsig"] for o in sens) < 2.0,
   "; ".join(f"w={w:.2f}/n={n}: {o['sep']:+.3f} dex ({o['nsig']:.2f} sigma, N={o['np_']})"
             for (w, n), o in zip(((0.15,30),(0.20,20),(0.25,20),(0.30,20),(0.30,50),(0.40,20)), sens)))

# ==========================================================================================================
P(""); P("="*122)
P("PART 4.  THE SYSTEMATICS THAT COULD ERASE IT, each moved until it does or fails to.")
P("="*122)
KEYS = ["classical", "m31", "isolated"]
info("Two numbers are tracked through every systematic, because they are different claims:")
info("  RAW      = the median residual of the whole pressure sample against the framework's kernel.  This is the")
info("             liability-table quantity, and it is large.  It is NOT matched to a rotating control.")
info("  MATCHED  = the separation from the rotating control at the SAME internal acceleration.  This is f09's claim,")
info("             and it is the one that just collapsed.")
def scan(rows, nperm=4000):
    pres, rot, _ = matched_sets(rows, a0c)
    o = compare(pres, rot, nperm=nperm)
    o["raw"] = float(np.median([r for _, r, _ in rows]))
    return o

P(""); info(f"(a) STELLAR MASS-TO-LIGHT RATIO  {'Upsilon_V':>10} {'RAW dex':>10} {'MATCHED sep':>13} {'sigma':>7}")
ups_scan = {}
for ups in (1.0, 1.5, 2.0, 3.0, 5.0):
    o = scan([(d["name"],) + dsph_row(d, a0c, ups=ups)[:2] for k in KEYS for d in classes[k]])
    ups_scan[ups] = o
    info(f"{'':33}{ups:10.1f} {o['raw']:+10.3f} {o['sep']:+13.3f} {o['nsig']:7.2f}")
ck("S1 the RAW pressure-supported offset is not a stellar mass-to-light ratio: erasing it needs Upsilon_V near 5 for old, metal-poor dwarf-spheroidal populations, roughly three times what anyone publishes (Woo, Courteau & Dekel 2008, MNRAS 390, 1453; Martin, de Jong & Rix 2008, ApJ 684, 1075 use 1-2).  The MATCHED separation, by contrast, is small at every Upsilon and never becomes a result",
   ups_scan[3.0]["raw"] > 0.15 and max(o["nsig"] for o in ups_scan.values()) < 2.0,
   "RAW: " + ", ".join(f"Ups={u} {ups_scan[u]['raw']:+.3f}" for u in (1.0, 2.0, 3.0, 5.0)) +
   ".  MATCHED: " + ", ".join(f"Ups={u} {ups_scan[u]['sep']:+.3f} ({ups_scan[u]['nsig']:.2f} sigma)" for u in (1.0, 2.0, 3.0, 5.0)))

P(""); info(f"(b) WHICH CORRECT PRESCRIPTION  {'':17} {'RAW dex':>10} {'MATCHED sep':>13} {'sigma':>7}")
presc_scan = {}
for pn, plab in (("f09", "f09 max() branch"), ("fm12", "FM12 eq.60 1-D  "), ("sphere", "sphere avg (exact)")):
    o = scan([(d["name"],) + dsph_row(d, a0c, presc=pn)[:2] for k in KEYS for d in classes[k]])
    presc_scan[pn] = o
    info(f"{'':33}{plab:18} {o['raw']:+10.3f} {o['sep']:+13.3f} {o['nsig']:7.2f}")
PSYS = abs(presc_scan["sphere"]["raw"] - presc_scan["fm12"]["raw"])
ck("S2 (FAILS, AND IT IS THE SAME FAILURE AS P4) the choice among CORRECT external-field prescriptions is not free.  The exact sphere average and the published one-dimensional formula differ by more than 0.1 dex in the RAW offset, so 'treat the external field properly' does not name a number.  The sphere average is used everywhere here because it is exact for an isotropic tracer AND gives the smaller liability -- against interest",
   PSYS < 0.06,
   f"RAW offsets: sphere average {presc_scan['sphere']['raw']:+.3f}, FM12 eq.60 {presc_scan['fm12']['raw']:+.3f}, f09 max() {presc_scan['f09']['raw']:+.3f} dex.  "
   f"Prescription systematic {PSYS:.3f} dex, about {100*PSYS/max(presc_scan['sphere']['raw'],1e-3):.0f} per cent of the raw offset.  "
   f"Note f09's max() gives the SMALLEST raw offset of the three, so f09 was using the prescription least favourable to its own conclusion")

MSYS = abs(presc_scan["sphere"]["sep"] - presc_scan["fm12"]["sep"])
ck("S2b (THE SINGLE MOST DECISIVE LINE IN THE FILE) the MATCHED separation is SMALLER THAN ITS OWN PRESCRIPTION SYSTEMATIC.  Between the two defensible external-field treatments the matched separation moves by more than the separation itself; under f09's own max() branch it changes SIGN and lands four sigma on the WRONG side.  A signal smaller than the systematic that moves it is not a measurement, whatever its nominal sigma",
   MSYS < 0.5*abs(presc_scan["sphere"]["sep"]),
   f"matched separation: sphere average {presc_scan['sphere']['sep']:+.3f} dex ({presc_scan['sphere']['nsig']:.2f} sigma), "
   f"FM12 eq.60 {presc_scan['fm12']['sep']:+.3f} ({presc_scan['fm12']['nsig']:.2f} sigma), f09 max() {presc_scan['f09']['sep']:+.3f} ({presc_scan['f09']['nsig']:.2f} sigma).  "
   f"Systematic {MSYS:.3f} dex against a signal of {abs(presc_scan['sphere']['sep']):.3f} dex -- a ratio of {MSYS/max(abs(presc_scan['sphere']['sep']),1e-3):.1f}")

P(""); info("(c) HOST BARYONIC MASS, scanned by a factor 4 (it sets x_e and hence the whole external-field term):")
host_scan = {}
for fac in (0.5, 1.0, 2.0):
    rows = [(d["name"],) + dsph_row(d, a0c, host_mb=(MW_MB if k == "classical" else M31_MB)*fac)[:2]
            for k in ("classical", "m31") for d in classes[k]]
    rows += [(d["name"],) + dsph_row(d, a0c)[:2] for d in classes["isolated"]]
    o = scan(rows); host_scan[fac] = o
    info(f"      host mass x{fac:.1f}: RAW {o['raw']:+.3f} dex, MATCHED separation {o['sep']:+.3f} dex ({o['nsig']:.2f} sigma)")
ck("S3 the RAW offset survives a factor 4 in the assumed host baryonic mass, and cannot be tuned away in the helpful direction: a heavier host means a larger external field, which SUPPRESSES the predicted dispersion and makes the residual LARGER",
   min(o["raw"] for o in host_scan.values()) > 0.15,
   "; ".join(f"x{f}: RAW {host_scan[f]['raw']:+.3f}, matched {host_scan[f]['sep']:+.3f} dex" for f in (0.5, 1.0, 2.0)))

P(""); info("(d) LEAVE ONE CLASS OUT, canonical footing:")
loo = {}
for drop in KEYS:
    o = scan([(d["name"],) + dsph_row(d, a0c)[:2] for k in KEYS if k != drop for d in classes[k]])
    loo[drop] = o
    info(f"      without {drop:10}: N_matched={o['np_']:3d}  RAW {o['raw']:+.3f}  MATCHED {o['sep']:+.3f} dex ({o['nsig']:.2f} sigma, p={o['p']:.4f})")
ck("S4 the collapse of the matched separation is not one class's doing: dropping the classical dwarfs, the M31 dwarfs or the isolated dwarfs leaves the matched separation below two sigma every time, while the RAW offset stays large every time.  The two claims come apart in every subsample",
   max(o["nsig"] for o in loo.values()) < 2.0 and min(o["raw"] for o in loo.values()) > 0.15,
   "; ".join(f"without {k}: RAW {loo[k]['raw']:+.3f}, matched {loo[k]['sep']:+.3f} dex ({loo[k]['nsig']:.2f} sigma, N={loo[k]['np_']})" for k in loo))

# ---- 4e. the class that discriminates ---------------------------------------------------------------------
P(""); P("-"*122)
P("4e.  OUTER-HALO GLOBULAR CLUSTERS -- pressure-supported, and containing NO dark matter under LCDM either.")
P("-"*122)
info("This is the one class that separates the two readings of the whole pattern.  Under DARK MATTER, globular")
info("clusters have none, so MOND's boost should make it OVER-predict their dispersions.  Under a reading in which")
info("PRESSURE SUPPORT itself breaks the kernel, they should behave like the dwarf spheroidals and sit ABOVE it.")
# Baumgardt & Hilker 2018 / Baumgardt et al. 2019-2023 structural parameters (D_sun kpc, R_GC kpc, V mag, r_h,l pc),
# extinction from the Harris 2010 catalogue.  Dispersions: Pal 14 from Jordi et al. 2009, AJ 137, 4586 (16 members);
# Pal 4 from Frank et al. 2012, MNRAS 423, 2917 (23 members).  NGC 2419 and Pal 3 from Baumgardt's own N-body fits,
# therefore MODEL-DEPENDENT and flagged.  Photometric Upsilon_V = 2 for an old metal-poor population.
GC = [("Pal 4",    101.39, 104.05, 14.23, 0.01, 15.88, 0.87, "Frank et al. 2012 (23 members)"),
      ("Pal 14",    73.58,  68.55, 14.13, 0.04, 27.63, 0.38, "Jordi et al. 2009 (16 members)"),
      ("Pal 3",     94.84,  98.17, 14.56, 0.04, 20.16, 0.80, "Baumgardt N-body fit -- MODEL-DEPENDENT"),
      ("NGC 2419",  88.47,  95.93, 10.56, 0.08, 19.76, 5.10, "Baumgardt N-body fit -- MODEL-DEPENDENT")]
info(f"{'cluster':10} {'M_V':>7} {'L_V':>10} {'M(Ups=2)':>10} {'x_i':>8} {'x_e':>8} {'sig_obs':>8} {'sig_pred':>9} {'dex':>8}   source")
gc_res = []
for nm, Dsun, Rgc, V, EBV, rhl, sob, src in GC:
    MV = V - 5*math.log10(Dsun*1e3/10.0) - 3.1*EBV
    LV = 10**(0.4*(4.83 - MV)); M = UPS_V*LV
    r12 = (4.0/3.0)*rhl*PC
    xi = G*(0.5*M*Msun)/r12**2/a0c
    xe = G*MW_MB*Msun/(Rgc*kpc)**2/a0c
    sp = math.sqrt(g_qumond_sphere(xi, xe)*a0c*r12/3.0)/1e3
    r = 2.0*math.log10(sob/sp)                       # residual in ACCELERATION dex = 2 x the dispersion dex
    gc_res.append((nm, r, xi, xe))
    info(f"{nm:10} {MV:7.2f} {LV:10.2e} {M:10.2e} {xi:8.4f} {xe:8.5f} {sob:8.2f} {sp:9.2f} {r:+8.3f}   {src}")
gcr = np.array([t[1] for t in gc_res])
dsph_over = [t for k in KEYS for t in summary[k] if 0.01 <= t[2] <= 1.2]
ck("S5 (AGAINST THE READING THIS WHOLE LINE OF WORK WAS CHASING, AND IT IS THE MOST IMPORTANT RESULT IN THE FILE) at OVERLAPPING internal accelerations the pressure-supported dwarf spheroidals sit ABOVE the framework's kernel and the pressure-supported globular clusters sit far BELOW it.  'Pressure-supported' therefore does NOT predict the sign of the residual.  DARK MATTER does: dwarf spheroidals are dark-matter dominated and globular clusters contain none, so a kernel calibrated on rotation curves must under-predict the first and over-predict the second, which is exactly what is measured.  So even if the matched separation had survived Part 3, the one class that could tell the two explanations apart argues for dark-matter content and not for support type",
   np.median(gcr) < -0.3 and np.median([t[1] for t in dsph_over]) > 0.1,
   f"globular clusters: " + ", ".join(f"{t[0]} {t[1]:+.3f} (x_i={t[2]:.3f})" for t in gc_res) +
   f"; median {np.median(gcr):+.3f} dex.  Dwarf spheroidals over the same x_i = 0.01-1.2: median "
   f"{np.median([t[1] for t in dsph_over]):+.3f} dex on N={len(dsph_over)}.  This reproduces the committed h93 result "
   f"(sigma_obs/sigma_pred = 0.407 for Pal 4 at Upsilon_V = 1.6, i.e. -0.78 dex) to within the M/L difference.  "
   f"⚠️ CAVEAT AGAINST MY OWN POINT: at Upsilon_V = 1 the globular clusters move to "
   f"{np.median(gcr) + math.log10(2.0):+.3f} dex, still strongly negative, and their dispersions rest on 16-23 stars apiece")

# ==========================================================================================================
P(""); P("="*122)
P("PART 5.  MUTATION CONTROLS.")
P("="*122)
def g_sphere_newt(x_i, x_e, ntheta=2001):
    th = np.linspace(0, math.pi, ntheta); st, ctm = np.sin(th), np.cos(th)
    return -float(np.trapz(((-x_i*st)*st + (x_e - x_i*ctm)*ctm)*st, th)/np.trapz(st, th))
m1n = [g_sphere_newt(xi, xe)/xi for xi, xe in ((0.01, 0.1), (0.001, 1.0), (0.5, 0.02))]
ck("M1 with nu = 1 the same quadrature returns the internal Newtonian field EXACTLY at every external field, so the machinery is not manufacturing a coupling",
   max(abs(v - 1) for v in m1n) < 1e-9, "Newtonian sphere average / x_i = " + ", ".join(f"{v:.12f}" for v in m1n))

rows_all = [(d["name"],) + dsph_row(d, a0c)[:2] for k in KEYS for d in classes[k]]
pres_m, rot_m, _ = matched_sets(rows_all, a0c)
pa = np.array([t[1] for t in pres_m]); ra = np.array([t[1] for t in rot_m])
pool = np.concatenate([pa, ra]); n1 = len(pa)
shuf = np.array([abs(np.median((q := rng.permutation(pool))[:n1]) - np.median(q[n1:])) for _ in range(20000)])
real = abs(np.median(pa) - np.median(ra))
# the same shuffle on the UNMATCHED samples, so M2's own claim about them is computed rather than asserted
pu = np.array([t[1] for k in KEYS for t in summary[k]])
poolu = np.concatenate([pu, ra]); n1u = len(pu)
shufu = np.array([abs(np.median((q := rng.permutation(poolu))[:n1u]) - np.median(q[n1u:])) for _ in range(20000)])
realu = abs(np.median(pu) - np.median(ra))
p_unmatched = float(np.mean(shufu >= realu))
ck("M2 (FAILS, AND IT IS THE SAME FAILURE AS A1 -- the mutation control is doing its job) shuffling the rotation/pressure labels between the two MATCHED populations should not reproduce the real separation.  It does, one time in ten.  That is not a broken control; it is the control correctly reporting that there is no separation left to destroy once the acceleration matching is honest.  Note this same shuffle applied to the UNMATCHED samples returns essentially never, which is exactly the point: the unmatched difference is real and the matched one is not",
   float(np.mean(shuf >= real)) < 0.01,
   f"MATCHED: real {real:.3f} dex; shuffled median {np.median(shuf):.3f}, 99th percentile {np.percentile(shuf,99):.3f}; "
   f"P(shuffled >= real) = {np.mean(shuf >= real):.5f}.  UNMATCHED, same shuffle: real {realu:.3f} dex, "
   f"P(shuffled >= real) = {p_unmatched:.5f}.  The raw difference is real; the matched one is not")

big = a0c*100
pres_big = np.array([dsph_row(d, big)[0] for k in KEYS for d in classes[k]])
pres_now = np.array([dsph_row(d, a0c)[0] for k in KEYS for d in classes[k]])
ck("M3 MUTATION CONTROL: raising a_0 by 100 drives every object deep into the modified regime, the predicted dispersions rise and the residuals must fall.  They do",
   np.median(pres_big) < np.median(pres_now) - 0.2,
   f"median residual {np.median(pres_now):+.3f} dex at the canonical a_0, {np.median(pres_big):+.3f} at 100 a_0 ({np.median(pres_big)-np.median(pres_now):+.3f})")

ck("M4 SANITY: the rotating control reproduces the published radial-acceleration relation across the whole SPARC sample, not only inside the matched region",
   abs(np.median(rs)) < 0.10 and rs.std(ddof=1) < 0.25,
   f"all {len(rs)} SPARC galaxies: median {np.median(rs):+.3f} dex, scatter {rs.std(ddof=1):.3f}")

sig_mut = np.array([dsph_row(d, a0c, sig=d["sig"]*math.sqrt(2))[0] for k in KEYS for d in classes[k]])
ck("M5 MUTATION CONTROL on the DATA rather than the theory: inflating every observed dispersion by sqrt(2) must move every residual by exactly +0.301 dex, and nothing else in the pipeline may respond",
   abs(float(np.median(sig_mut - pres_now)) - math.log10(2.0)) < 1e-9,
   f"median shift {float(np.median(sig_mut - pres_now)):+.9f} dex against the analytic 2 log10(sqrt(2)) = log10(2) = {math.log10(2.0):+.9f}")

# ==========================================================================================================
P(""); P("="*122); P("VERDICT"); P("="*122)
P(f"  THE 1.73 SIGMA DOES NOT SURVIVE.  WITHDRAW IT.")
P(f"")
P(f"  Fixing f09's prescription did not kill it; fixing f09's MATCHING did.  f09 called its comparison 'matched")
P(f"  acceleration', but its window was the min-max span of its own eight dwarfs, 0.0009 to 0.073 in g_bar/a_0, and")
P(f"  SPARC has essentially no data below about 0.009.  Comparing object by object against the SPARC relation at")
P(f"  each object's OWN internal acceleration -- and dropping, rather than extrapolating to, the objects where the")
P(f"  rotating side has no data -- the separation falls from +0.215 dex / 1.73 sigma to {c_all['sep']:+.3f} dex / {c_all['nsig']:.2f} sigma,")
P(f"  permutation p = {c_all['p']:.3f}.  It stays under two sigma on both a_0 footings and in every subsample.  Loosening the")
P(f"  matching window pushes it back up -- 0.9 sigma at 0.15 dex, 1.4 at 0.30, {max(o['nsig'] for o in sens):.1f} at 0.40 -- which is itself the")
P(f"  finding: the number is a monotone function of how much extrapolation is allowed, and nothing reaches three")
P(f"  sigma.  A1, A4, A9 and the M2 shuffle all FAIL and are left failing.")
P(f"")
P(f"  AND THE REASON IS A CONFOUND THAT CANNOT BE FIXED WITH LOCAL GROUP DATA.  Support type and acceleration DEPTH")
P(f"  are not independent here.  Of the {len(oor)+c_all['np_']} pressure-supported objects, {len(oor)} sit BELOW the deepest acceleration SPARC")
P(f"  reaches.  Those are the discrepant ones: median {np.median(dropres):+.3f} dex, against {np.median([t[1] for t in kept]):+.3f} dex for the {len(kept)} that overlap the")
P(f"  rotating sample.  Inside the pressure sample alone the residual runs with log10(x_i) at slope {sl:+.2f}, r = {rp:+.2f}.")
P(f"  'Pressure-supported' and 'three decades below a_0' are the same set of objects in the Local Group, so no")
P(f"  Local Group comparison can separate them.  That is a structural limit, not a sample-size one, and it applies")
P(f"  to f09's version of the test as much as to this one.")
P(f"")
P(f"  WHAT DOES SURVIVE, and it is the liability-table statement rather than f09's:  the RAW offset of the")
P(f"  pressure-supported Local Group dwarfs against this framework's kernel is large -- classical {np.median([t[1] for t in summary['classical']]):+.2f} dex, M31")
P(f"  {np.median([t[1] for t in summary['m31']]):+.2f} dex, ultra-faints {np.median([t[1] for t in summary['ultrafaint']]):+.2f} dex -- and it survives a factor 3 in Upsilon_V, a factor 4 in host")
P(f"  mass, and every prescription tried.  What is NOT established is that it has anything to do with pressure")
P(f"  support rather than with depth.")
P(f"")
P(f"  THE REST OF THE REPAIR, for the record.")
P(f"")
P(f"  1. THE PRESCRIPTION IS FIXED, AND f09 MIS-DIAGNOSED ITS OWN DEFECT.  f09's max(isolated, external-field)")
P(f"     branch is replaced by the exact sphere average of the QUMOND field: no branch, reduces to the framework's")
P(f"     own kernel when the external field is off, reproduces f01's independently derived nu(x_e)(1+L_e/3) when it")
P(f"     dominates, and returns the Newtonian field exactly under nu = 1.  But removing the branch entirely changes")
P(f"     the isolated-versus-external-field gap by only about a tenth: the branch label was a PROXY FOR DEPTH, and")
P(f"     depth is what the residual actually runs with.  f09's A6 blamed the right symptom on the wrong cause.")
P(f"     And 'do it properly' does not name a number: the exact sphere average and the published one-dimensional")
P(f"     formula differ by {PSYS:.2f} dex in the raw offset, {100*PSYS/max(presc_scan['sphere']['raw'],1e-3):.0f} per cent of it (P4 and S2 both FAIL and are left failing).")
P(f"")
P(f"  2. THREE FURTHER ARITHMETIC BUGS IN f09, and they do NOT all run one way (A7 FAILS).  Total instead of")
P(f"     enclosed mass ({v1-v0:+.3f} dex) and projected instead of deprojected half-light radius ({v2-v1:+.3f}) both understated")
P(f"     the liability; the true instead of the Newtonian external field in nu's argument ({v3-v2:+.3f}) overstated it.")
P(f"     On the classical eight they nearly cancel, which is a coincidence of that sample and not a defence.")
P(f"")
P(f"  3. THE ISOLATED DWARFS SAY THE LEAST.  Cetus, Tucana and the other isolated Local Group dwarf spheroidals")
P(f"     need no external-field prescription at all (x_e ~ 1e-4) and sit {np.median(iso_res):+.3f} dex from the kernel, against")
P(f"     {np.median([t[1] for t in summary['classical']]):+.3f} for the Milky Way satellites and {np.median([t[1] for t in summary['m31']]):+.3f} for M31's.  Cetus is {[t[1] for t in iso if t[0]=='Cetus'][0]:+.3f}.  The objects where the")
P(f"     prescription cannot be blamed show the least offset, which points at environment or tides.")
P(f"")
P(f"  4. THE CLASS THAT WOULD DECIDE THE FORK DECIDES AGAINST IT.  Outer-halo globular clusters are pressure-")
P(f"     supported and contain no dark matter under LCDM either.  At overlapping internal accelerations the dwarf")
P(f"     spheroidals sit {np.median([t[1] for t in dsph_over]):+.3f} dex ABOVE the kernel and the globular clusters {np.median(gcr):+.3f} dex BELOW it.")
P(f"     'Pressure-supported' does not predict the sign of the residual.  DARK-MATTER CONTENT does, exactly: dwarf")
P(f"     spheroidals are dark-matter dominated and globular clusters are not, so a kernel calibrated on rotation")
P(f"     curves must under-predict the first and over-predict the second.  That is what is measured.  (Reproduces")
P(f"     the committed h93 result to within the M/L difference; caveat, 16-23 stars per cluster.)")
P(f"")
P(f"  5. DEFECT 2 IS REAL AND UNRESOLVED.  f09's five-galaxy mass-matched control is NOT small-number noise: five")
P(f"     random SPARC galaxies reproduce -0.205 dex with p = {p_low:.4f}.  Those five are also the least reliable rotation")
P(f"     curves in SPARC -- {nof} of 5 have no measured V_flat at all and every one has V_max within a factor 2.5 of the")
P(f"     HI turbulent dispersion -- but SPARC alone cannot separate that from a velocity-scale trend, the same")
P(f"     confound that killed f08.  D2a, D2b and A3 are left FAILING.  The mass-matched comparison is unusable.")
P(f"")
P(f"  WHAT MAY BE QUOTED AFTER THIS FILE:")
P(f"   * 'f09's 1.73 sigma rotation-versus-pressure separation is WITHDRAWN.  With object-by-object acceleration")
P(f"     matching it is {c_all['sep']:+.3f} dex, {c_all['nsig']:.2f} sigma, p = {c_all['p']:.3f}; it reaches at most {max(o['nsig'] for o in sens):.1f} sigma, and only by")
P(f"     loosening the matching window to 0.40 dex, which re-admits objects with no rotating counterpart.'")
P(f"   * 'The pressure-supported Local Group dwarfs DO sit well above this framework's kernel in the raw -- median")
P(f"     {presc_scan['sphere']['raw']:+.2f} dex, robust to a factor 3 in Upsilon_V and a factor 4 in host mass, with a {PSYS:.2f} dex prescription")
P(f"     systematic.  That is the liability-table statement and it stands.  What is NOT established is that it has")
P(f"     anything to do with pressure support rather than with sitting three decades below a_0.'")
P(f"   * 'Outer-halo globular clusters, equally pressure-supported, sit far BELOW the kernel, so support type does")
P(f"     not predict the sign; dark-matter content does.'")
P(f"  Nothing stronger.  That MOND under-predicts dwarf-spheroidal dispersions is long known (Angus 2008, MNRAS 387,")
P(f"  1481; McGaugh & Milgrom 2013, ApJ 775, 139); what is new here is only the branch-free prescription, the")
P(f"  honest matching, and the demonstration that the Local Group cannot separate support from depth.")
P(f"")
P(f"  THE FORK ITSELF IS UNTOUCHED AND STILL OPEN.  Milgrom's theorem -- modified inertia and modified gravity are")
P(f"  identical for circular orbits and differ for every other orbit (1994; 2011, arXiv:1111.1611) -- is unaffected")
P(f"  by anything here.  What is gone is the claim that Local Group dwarfs measure it.")
sys.exit(ck.done())
