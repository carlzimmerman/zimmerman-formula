#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
v_g06_dsph_shift_decomposition.py -- ADVERSARIAL VERIFICATION of g06's dwarf-spheroidal "against interest" number.
==================================================================================================================
THE CLAIM UNDER TEST (g06_local_volume_groups_lambda_edge.py, section 9 note 3, and check F2):

    "the eight classical dwarf spheroidals move from f09's +0.228 dex to +0.733 dex once the external field is
     treated as QUMOND requires (Newtonian, baryonic) and the ENCLOSED rather than the total mass is used inside
     the half-light radius."

Two things are asserted: the NUMBER (+0.733) and the CAUSE (two named prescription fixes).  This file reproduces
both files' machinery from scratch and turns the shift ON one ingredient at a time, so the cause can be read off
rather than asserted.  Same eight objects, same sigma, same R_half, both footings throughout.

WHAT IT FINDS
  * The number reproduces EXACTLY (+0.733 canonical, and +0.695 on the alt footing g06 never prints).
  * The FIRST named cause runs BACKWARDS.  f09 used g_ext = v_c^2/D with v_c = 200 km/s -- the Milky Way's TOTAL
    dynamical field, 0.182 a_0.  QUMOND requires the BARYONIC Newtonian field, which at 76 kpc is 0.0155 a_0, a
    factor 12 SMALLER.  A smaller external field makes a satellite MORE isolated, so on its own it RAISES the
    prediction and LOWERS the residual: f09's own prescription with only that one fix gives +0.057, not +0.733.
  * The shift is actually produced by an ingredient the claim does not name: replacing f09's combination rule
    g_pred = max(g_iso, g_efe) with g06's interpolation nu(x_int + e)(1 + L*w/3).  f09's "max" rule can only ever
    let the EFE RAISE the prediction; the interpolation always lets it LOWER the prediction.  That single change
    of rule -- not the character of the field -- supplies about two thirds of the +0.505 dex.
  * And it supplies it through a channel that the repository's own bug list forbids: the per-object residual is a
    monotone function of e_N/x_int, the prescription's own external-field parameter.  That is bug pattern #6 (a
    residual whose sign tracks a branch of my own prescription) and it is verbatim f09's own retired check A6,
    reproduced with the opposite sign.  g06 claims A6 is fixed by interpolating.  It is not fixed; it is inverted.

CHECKS CAN FAIL.  Both footings enter every number.  Mutation control included.
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0, nu, nu_s, G, Msun, kpc

ck = Check()

# ---------------------------------------------------------------- the eight objects, verbatim from f09 and g06
# name, M_star/Msun, R_e (PROJECTED half-light radius, kpc), sigma_los (km/s), Galactocentric distance (kpc)
# (the same tuple appears in f09_orbital_coherence_fork.py line 42 and g06 line 606; Wolf et al. 2010, AJ 220, 1220
#  Table 1 lists these as projected R_e, so the (4/3) deprojection to r_1/2 that g06 applies is the right move)
DSPH = [("Draco", 2.9e5, 0.221, 9.1, 76.), ("Sculptor", 2.3e6, 0.283, 9.2, 86.),
        ("Fornax", 4.3e7, 0.710, 11.7, 147.), ("Carina", 3.8e5, 0.250, 6.6, 105.),
        ("Sextans", 4.4e5, 0.695, 7.9, 86.), ("Leo I", 5.5e6, 0.251, 9.2, 254.),
        ("Leo II", 7.4e5, 0.176, 6.6, 233.), ("Ursa Minor", 2.9e5, 0.181, 9.5, 76.)]
MW_VC   = 200e3      # f09's external-field normalisation: the MW's TOTAL circular speed
MW_MB   = 6.0e10     # g06's: baryons only, 5e10 stars (Bland-Hawthorn & Gerhard 2016) + 1e10 gas
GB_LSS  = 6.024e-15  # g06's baryonic large-scale-structure field at the Local Group, from its own E1 printout

# ---------------------------------------------------------------- g06's Jeans machinery, re-implemented
def dlnnu(y):
    y = np.maximum(np.asarray(y, float), 1e-300); s = np.sqrt(y)
    return -0.5*s*np.exp(-s)/(1.0 - np.exp(-s))
def rad_grid(rh, lo=1e-3, hi=400.0, n=1400): return np.geomspace(lo*rh, hi*rh, n)
def tracer(r, rh): return (1.0 + (r/(rh/1.3048))**2)**-2.5
def cmf(r, rho):
    N = np.concatenate([[0.], np.cumsum(0.5*(rho[1:]*r[1:]**2 + rho[:-1]*r[:-1]**2)*np.diff(r))]); return N/N[-1]
def jeans_sigma(r, rho, g):
    integ = rho*g
    tail = np.concatenate([np.cumsum((0.5*(integ[1:] + integ[:-1])*np.diff(r))[::-1])[::-1], [0.]])
    w = rho*r**2
    return math.sqrt(float(np.trapz(w*(tail/rho), r)/np.trapz(w, r)))
def g_eff(gN, gext, a0, branch):
    if branch == "isolated": return nu(gN/a0)*gN
    x = (gN + gext)/a0; w = gext/(gN + gext)
    return nu(x)*(1.0 + dlnnu(x)*w/3.0)*gN

def jeans_run(a0, branch="interp", depro=4/3., gext_mode="baryonic", nu_on=True):
    """g06's dwarf-spheroidal block.  gext_mode picks WHICH external field; branch picks the combination rule."""
    out = []
    for nm, Ms, Re, so, Dk in DSPH:
        rh = depro*Re*kpc
        gext = (G*MW_MB*Msun/(Dk*kpc)**2 + GB_LSS) if gext_mode == "baryonic" else MW_VC**2/(Dk*kpc)
        r = rad_grid(rh); rho = tracer(r, rh)
        gN = G*Ms*Msun*cmf(r, rho)/r**2
        gE = g_eff(gN, gext, a0, branch) if nu_on else gN
        out.append((nm, math.log10((so*1e3/jeans_sigma(r, rho, gE))**2), float(gext/a0),
                    float(np.interp(rh, r, gN))/a0))
    return out

def f09_run(a0, gext_mode="total", rule="max"):
    """f09's own prescription: point mass at the PROJECTED radius, g_obs = 3 sigma^2 / R, g_pred = max(iso, efe)."""
    out = []
    for nm, M, Rh, sob, D in DSPH:
        Mk, R, s, d = M*Msun, Rh*kpc, sob*1e3, D*kpc
        g_obs = 3.0*s*s/R; gN = G*Mk/R**2
        g_iso = math.sqrt(gN*a0)
        gext = MW_VC**2/d if gext_mode == "total" else G*MW_MB*Msun/d**2
        g_efe = gN*nu_s(gext/a0)
        g_pred = max(g_iso, g_efe) if rule == "max" else min(g_iso, g_efe)
        out.append((nm, math.log10(g_obs/g_pred)))
    return out

def med(rows, i=1): return float(np.median([r[i] for r in rows]))

# ================================================================================================ SECTION 1
P("="*126); P("1.  BOTH PUBLISHED NUMBERS REPRODUCE FROM SCRATCH -- otherwise nothing below means anything")
P("="*126)
r09 = {f: med(f09_run(a0)) for f, a0 in A0.items()}
r06 = {f: med(jeans_run(a0)) for f, a0 in A0.items()}
info(f"f09 prescription, median residual:  canonical {r09['canonical']:+.3f} dex   alt {r09['alt']:+.3f} dex")
info(f"g06 prescription, median residual:  canonical {r06['canonical']:+.3f} dex   alt {r06['alt']:+.3f} dex")
ck("V1 this file reproduces f09's published +0.228 dex and g06's claimed +0.733 dex to the last digit on the "
   "canonical footing, from the same eight tuples, so the decomposition below is of the real quantity",
   abs(r09["canonical"] - 0.228) < 0.005 and abs(r06["canonical"] - 0.733) < 0.005,
   f"f09 {r09['canonical']:+.4f} against its published +0.228; g06 {r06['canonical']:+.4f} against its claimed "
   f"+0.733; the shift is {r06['canonical'] - r09['canonical']:+.3f} dex")

ck("V2 (a rule g06 breaks) the alt footing must enter the dwarf-spheroidal number, not just be computed and "
   "discarded.  g06 line 612-626 builds dres for BOTH footings and then uses only dres['canonical'] -- the alt "
   "dwarf number is never printed and never checked, while F1, F2, F3 and the quoted 3.50 sigma all run on "
   "canonical alone.  This check supplies the missing number and asks whether the conclusion is footing-stable",
   abs(r06["canonical"] - r06["alt"]) < 0.15,
   f"g06's dwarf median is {r06['canonical']:+.3f} canonical / {r06['alt']:+.3f} alt, a difference of "
   f"{r06['canonical'] - r06['alt']:+.3f} dex.  The conclusion does not flip, but the number was never shown")

# ================================================================================================ SECTION 2
P(""); P("="*126)
P("2.  TURNING THE INGREDIENTS ON ONE AT A TIME -- which of them actually moves the +0.505 dex?")
P("="*126)
info("The claim names TWO causes: (i) the external field treated as QUMOND requires -- Newtonian and baryonic")
info("rather than f09's v_c^2/D; and (ii) enclosed rather than total mass inside the half-light radius.  There is")
info("a THIRD ingredient the claim does not name: f09 combined the isolated and external-field predictions with")
info("g_pred = max(g_iso, g_efe), while g06 replaces that RULE with the interpolation nu(x+e)(1 + L w/3).")
LAD = [
 ("f09 as published (total-matter g_ext, max rule, point mass at projected R)",
  lambda a0: med(f09_run(a0, "total", "max"))),
 ("(i) ALONE: f09 rule, but the QUMOND-required BARYONIC Newtonian g_ext",
  lambda a0: med(f09_run(a0, "baryonic", "max"))),
 ("(ii) ALONE: enclosed-mass Jeans at the deprojected r_1/2, NO external field at all",
  lambda a0: med(jeans_run(a0, branch="isolated"))),
 ("(ii) + (i), but keeping f09's spirit: isolated Jeans (EFE cannot bite on this branch)",
  lambda a0: med(jeans_run(a0, branch="isolated"))),
 ("(iii) THE UNNAMED ONE: (ii) + the max->interpolation change of RULE  == g06 as published",
  lambda a0: med(jeans_run(a0, branch="interp"))),
 ("control: (iii) with f09's TOTAL-matter g_ext instead of the baryonic one",
  lambda a0: med(jeans_run(a0, branch="interp", gext_mode="total"))),
 ("control: (iii) with no deprojection (r_1/2 = R_e), to size the (4/3) on its own",
  lambda a0: med(jeans_run(a0, branch="interp", depro=1.0))),
]
P(f"    {'ingredient':78} {'canonical':>10} {'alt':>8}")
VALS = {}
for lbl, fn in LAD:
    c, a = fn(A0["canonical"]), fn(A0["alt"]); VALS[lbl] = c
    P(f"    {lbl:78} {c:+10.3f} {a:+8.3f}")

base   = VALS["f09 as published (total-matter g_ext, max rule, point mass at projected R)"]
onlyi  = VALS["(i) ALONE: f09 rule, but the QUMOND-required BARYONIC Newtonian g_ext"]
onlyii = VALS["(ii) ALONE: enclosed-mass Jeans at the deprojected r_1/2, NO external field at all"]
full   = VALS["(iii) THE UNNAMED ONE: (ii) + the max->interpolation change of RULE  == g06 as published"]

ck("V3 (THE REFUTATION) the FIRST named cause moves the number in the OPPOSITE direction to the one claimed.  "
   "f09's g_ext = v_c^2/D with v_c = 200 km/s is the Milky Way's TOTAL dynamical field, 0.182 a_0.  The field "
   "QUMOND actually requires in nu's argument is the BARYONIC Newtonian one, 0.0155 a_0 at 76 kpc -- twelve times "
   "SMALLER.  A smaller external field makes a satellite MORE isolated and RAISES its predicted dispersion, so on "
   "its own that fix LOWERS the residual.  This check asserts the claim's own story: that fixing the external "
   "field to the QUMOND-required one raises the dwarf-spheroidal median.  It does not",
   onlyi > base, f"f09 as published {base:+.3f} dex; f09 with ONLY the external field corrected to Newtonian-"
   f"baryonic {onlyi:+.3f} dex.  That single named fix moves the median by {onlyi - base:+.3f} dex -- DOWNWARD, "
   f"and by a third of the size of the shift it is credited with")

share_rule = (full - onlyii)/(full - base)
ck("V4 the ingredient that actually supplies the shift is the one the claim does not name: the change of "
   "COMBINATION RULE from f09's max(g_iso, g_efe) to g06's interpolation.  f09's 'max' rule can only ever let the "
   "external field RAISE the prediction (it is discarded whenever it is the smaller); the interpolation always "
   "lets it LOWER the prediction.  This check asserts the two NAMED causes account for most of the shift",
   share_rule < 0.5, f"enclosed-mass Jeans alone (both named causes, EFE unable to bite) gives {onlyii:+.3f} dex "
   f"= {onlyii - base:+.3f} of the {full - base:+.3f} dex shift; the unnamed change of rule adds the remaining "
   f"{full - onlyii:+.3f} dex, i.e. {100*share_rule:.0f}% of it")

info("")
info("and the part the named causes DO supply is not what they are described as.  In the isolated deep-MOND limit")
info("the Plummer virial is sigma^4 = (4/81) G M a_0 (Milgrom 1994) -- it depends on the TOTAL mass and on a_0 and")
info("on NOTHING ELSE: not on the radius, not on the deprojection, not on the enclosed-mass profile (that is g06's")
info("own check J3).  f09's estimator sigma^2 = g_pred R/3 gives (1/3) sqrt(G M a_0) against the exact")
info("(2/9) sqrt(G M a_0), a fixed factor 1.5 = 0.176 dex for every isolated-branch object.  So 'enclosed rather")
info("than total mass inside the half-light radius' is a mis-description of a virial-COEFFICIENT correction.")
ana = {f: float(np.median([math.log10((so*1e3/((4/81.)*G*Ms*Msun*a0)**0.25)**2) for _, Ms, _, so, _ in DSPH]))
       for f, a0 in A0.items()}
ck("V5 the isolated-branch part of the shift is exactly the 0.176 dex virial-coefficient factor 1.5, computed "
   "analytically with no radius and no mass profile anywhere in it, which is what shows the 'enclosed vs total "
   "mass' label is wrong for it",
   abs((ana["canonical"] - base) - 0.176) < 0.03,
   f"analytic isolated Plummer virial median {ana['canonical']:+.3f} dex (alt {ana['alt']:+.3f}) against f09's "
   f"{base:+.3f}: a shift of {ana['canonical'] - base:+.3f} dex, against the predicted log10(1.5) = +0.176")

# ================================================================================================ SECTION 3
P(""); P("="*126)
P("3.  BUG PATTERN #6, AND IT IS f09's OWN RETIRED CHECK A6 COMING BACK WITH THE SIGN FLIPPED")
P("="*126)
info("f09's A6 recorded that its dwarf residuals' SIGN tracked which branch of its own external-field rule was")
info("used -- isolated branch all positive, EFE branch all negative -- and concluded the eight objects could not")
info("carry a number until the rule was replaced by a proper interpolation.  g06 does the interpolation and treats")
info("A6 as discharged.  Here is the same diagnostic run on g06's own output.")
rows = jeans_run(A0["canonical"])
order = sorted(range(8), key=lambda i: rows[i][2]/rows[i][3])
P(f"    {'dwarf':12} {'e_N/a0':>9} {'x_int(r_h)':>11} {'e_N/x_int':>10} {'g06 dex':>9} {'isolated dex':>13}")
iso_rows = jeans_run(A0["canonical"], branch="isolated")
for i in order:
    nm, dex, eN, xi = rows[i]
    P(f"    {nm:12} {eN:9.5f} {xi:11.5f} {eN/xi:10.2f} {dex:+9.3f} {iso_rows[i][1]:+13.3f}")
ratio = np.array([rows[i][2]/rows[i][3] for i in range(8)])
dexs  = np.array([rows[i][1] for i in range(8)])
rk = float(np.corrcoef(np.argsort(np.argsort(np.log10(ratio))), np.argsort(np.argsort(dexs)))[0, 1])
rk_iso = float(np.corrcoef(np.argsort(np.argsort(np.log10(ratio))),
                           np.argsort(np.argsort([r[1] for r in iso_rows])))[0, 1])
ck("V6 (THE SAME DISEASE, NOT THE CURE) g06's per-object dwarf residual must not be a monotone function of "
   "e_N/x_int, the external-field ratio that its own prescription computes.  If it is, the +0.733 dex is a "
   "property of the branch and not of the data -- which is exactly the verdict f09 reached about its own numbers "
   "in check A6, and exactly the repository's bug pattern #6.  This check asserts the rank correlation is not "
   "extreme; it fails, and it fails harder than f09's version did because five of the eight objects are now "
   "external-field dominated where in f09 six of eight were isolated",
   abs(rk) < 0.75, f"Spearman rank correlation of g06's dwarf residual against e_N/x_int = {rk:+.3f} over the "
   f"eight objects (the isolated branch, where the EFE cannot act, gives {rk_iso:+.3f}); "
   f"{int((ratio > 1).sum())} of 8 are external-field dominated on g06's own numbers, up to e_N/x_int = "
   f"{ratio.max():.0f} for Sextans, whose residual is the largest in the file at {dexs[int(np.argmax(ratio))]:+.3f}")

spread = full - onlyii
ck("V7 so the replacement number is not stable enough to replace anything.  The claim's operative conclusion -- "
   "'f09's dwarf spheroidal number should not be quoted at its published value' -- is right about f09 and wrong "
   "to imply +0.733 is the value to quote instead: the same eight objects give anywhere from the isolated-branch "
   "value to the interpolated one depending on a prescription choice that no check in g06 tests on the dwarfs "
   "(g06's R4 branch-sensitivity check is groups-only, and the groups sit at e_N/x_int ~ 0.06 where the branch "
   "cannot matter).  This check asserts the branch does not matter for the dwarfs either",
   abs(spread) < 0.10, f"isolated branch {onlyii:+.3f} dex, interpolated branch {full:+.3f} dex, a prescription "
   f"spread of {spread:+.3f} dex on the same eight objects -- {abs(spread)/0.505*100:.0f}% of the entire shift "
   f"the claim is built on, and larger than f09's published number itself")

# ================================================================================================ SECTION 4
P(""); P("="*126); P("4.  MUTATION CONTROLS"); P("="*126)
mn = {f: med(jeans_run(a0, nu_on=False)) for f, a0 in A0.items()}
ck("M1 mutation -- switch the kernel off (nu = 1, Newtonian gravity on the same stellar masses).  The dwarf "
   "residuals must explode to the famous dark-matter-to-baryon ratios of the classical dwarf spheroidals; if they "
   "did not, this re-implementation would not be computing gravity at all",
   mn["canonical"] > 1.5 and mn["alt"] > 1.5, f"Newtonian median residual {mn['canonical']:+.3f} dex canonical / "
   f"{mn['alt']:+.3f} alt, i.e. a factor {10**mn['canonical']:.0f} in mass, against the kernel's "
   f"{r06['canonical']:+.3f} dex")
sw = {f: med(f09_run(a0, "total", "min")) for f, a0 in A0.items()}
ck("M2 mutation -- flip f09's combination rule from max to min while changing nothing else.  This isolates the "
   "rule from the field and must reproduce most of the gap on its own, confirming that the rule and not the field "
   "is the lever",
   sw["canonical"] > base + 0.15, f"f09 with max {base:+.3f} dex, f09 with min {sw['canonical']:+.3f} dex "
   f"(alt {sw['alt']:+.3f}): the rule alone moves the median by {sw['canonical'] - base:+.3f} dex without a "
   f"single number in the external field changing")

P(""); P("="*126); P("VERDICT"); P("="*126)
P("  The NUMBER is right: g06's +0.733 dex reproduces exactly, and its alt-footing companion is +0.695.")
P("  The CAUSE as stated is not.  Of the two causes the claim names, the first -- 'the external field treated as")
P("  QUMOND requires (Newtonian, baryonic)' -- moves the median DOWN by 0.17 dex when applied on its own, because")
P("  the QUMOND-required baryonic field is TWELVE TIMES SMALLER than the total-matter field f09 used, and a")
P("  smaller external field makes a dwarf more isolated.  The second -- 'enclosed rather than total mass' -- is a")
P("  mis-description of a fixed virial-coefficient correction that the isolated deep-MOND limit shows depends on")
P("  neither radius nor mass profile.  Roughly two thirds of the shift comes from an ingredient the claim does not")
P("  mention at all: replacing max(g_iso, g_efe) with an interpolation, which changes the SIGN of what the")
P("  external field does to the prediction.  And that ingredient delivers its shift through a residual that ranks")
P("  monotonically with the prescription's own e_N/x_int -- f09's retired check A6, inverted, not cured.")
sys.exit(ck.done())
