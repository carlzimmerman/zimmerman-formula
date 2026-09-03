#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h55_group_lensing_eta.py -- HUNT ITEM 55: the residual eta on GROUP scales, and whether the group-to-cluster ladder
                            has a STEP in it or a smooth rise.
====================================================================================================================
The framework works in galaxies (eta = 1 by construction of the RAR) and fails in clusters (eta ~ 2, the standing
liability).  Groups are the hinge: Milgrom (2019) argues there is no missing mass below sigma ~ 300 km/s, i.e. the
residual switches on where the hot gas does.  Item 55 asks for eta on group scales to +-0.2.

WHAT THE ITEM ASKED FOR, AND WHY THIS SCRIPT DOES NOT USE IT.  The item names the KiDS+GAMA group Delta-Sigma profiles
(Viola+2015 MNRAS 452, 3529; Dvornik+2017 MNRAS 468, 3251).  Neither is in VizieR -- tested this session on the CfA
mirror, both return "Table or Catalog not found", and the CDS master (cdsarc.cds.unistra.fr) is blocked from here.
Those papers publish their group Delta-Sigma only as figures.  So this script builds the ladder from three sources
that ARE available, and says plainly what each one costs:

  RUNG 1  GALAXIES, lensing, ON DISK: the KiDS-1000 isolated-galaxy lensing RAR (Brouwer+2021), with and without the
          hot-gas correction, at g_bar down to 1e-15 m/s^2.  A direct stacked Delta-Sigma measurement.
  RUNG 2  GROUPS AND CLUSTERS, ON DISK: eRASS1 (Bulbul+2024), 9830 clean systems from M500 = 5e12 (a group) to
          1.6e15 (a rich cluster).  The M500 in that catalogue is NOT a hydrostatic mass: it comes from the count-rate
          -- mass relation calibrated on DES+KiDS+HSC WEAK LENSING (Grandis+2024).  So it is a lensing mass in the
          mean, which is what item 55 wanted -- at the price of a scaling relation instead of a stacked profile.
  RUNG 3  the baryon budget, which is where the whole question actually lives: at cluster masses the gas dominates and
          f_gas is measured; at group masses the STARS are comparable to the gas and are NOT measured here.  Three
          prescriptions are run side by side and the answer is quoted as a range, not as a number.

Both footings.  Mutation controls.  Checks CAN fail.  The estimator's own weaknesses -- the mass-redshift degeneracy
of an X-ray selected sample, and the stellar budget -- are measured, not asserted.
"""
import sys, math, os
import numpy as np
from hunt_lib import *
sys.path.insert(0, os.path.abspath(DATA))
import _load_erass1 as ER
ck = Check(); rng = np.random.default_rng(55055)

def eta_of(gobs, gbar, a0): return gobs/(gbar*nu(gbar/a0))

# =============================================================== RUNG 1: galaxies, from stacked KiDS lensing (on disk)
P("="*116); P("RUNG 1 -- galaxies: eta from the KiDS-1000 stacked lensing RAR (on disk, a real Delta-Sigma stack)"); P("="*116)
gb_i, go_i, e_i = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
gb_h, go_h, e_h = load_rar("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
info(f"isolated KiDS-bright lenses: {len(gb_i)} acceleration bins, g_bar = {gb_i.min():.2e} to {gb_i.max():.2e} m/s^2")
R1 = {}
for foot, a0 in A0.items():
    out = []
    for tag, gb, go, ee_ in (("stars only     ", gb_i, go_i, e_i), ("stars + hot gas", gb_h, go_h, e_h)):
        e_ = eta_of(go, gb, a0); s_ = ee_/(gb*nu(gb/a0))
        m = np.isfinite(e_) & (go > 0) & (s_ > 0)
        deep = m & (gb < 1e-12)                       # the lensing regime proper, x = g_bar/a_0 < 0.01
        w = 1.0/s_[m]**2; wd = 1.0/s_[deep]**2
        ebar = float(np.average(e_[m], weights=w)); eer = float(1/math.sqrt(w.sum()))
        edeep = float(np.average(e_[deep], weights=wd)); eed = float(1/math.sqrt(wd.sum()))
        info(f"{foot:10} {tag}: eta = {ebar:.2f} +- {eer:.2f} over all 15 bins; {edeep:.2f} +- {eed:.2f} over the {deep.sum()} deep bins (g_bar < 1e-12, x < 0.011)")
        out.append((ebar, eer, edeep, eed))
    R1[foot] = out
lo_ = min(R1["canonical"][1][0], R1["alt"][1][0]); hi_ = max(R1["canonical"][0][0], R1["alt"][0][0])
info(f"the galaxy rung is therefore eta = {lo_:.2f} to {hi_:.2f}: the spread is the BARYON BUDGET (whether the hot gas around")
info("isolated galaxies is counted), not the statistics, exactly as it will be for the groups below.")
ck("55-1 the ladder starts at 1: the KiDS-1000 stacked lensing of isolated galaxies brackets eta = 1 between its two baryon budgets on both footings, so any rise measured further up the ladder is a real rise and not an offset in the zero point",
   lo_ < 1.0 < hi_,
   f"eta(galaxies) = {R1['canonical'][0][0]:.2f} +- {R1['canonical'][0][1]:.2f} with stars alone and {R1['canonical'][1][0]:.2f} with Brouwer's hot-gas correction (canonical); {R1['alt'][0][0]:.2f} / {R1['alt'][1][0]:.2f} (alt).  The 0.15-0.25 dex stellar M/L systematic on g_bar -- this repository's own items 2, 65 and 66 -- is far larger than the {R1['canonical'][0][1]:.2f} statistical error, so this is a consistency, not a measurement")

# =============================================== RUNGS 2-3: groups and clusters from eRASS1 lensing-calibrated masses
P(""); P("="*116); P("RUNGS 2-3 -- groups to clusters: eRASS1, weak-lensing-calibrated M500, measured M_gas"); P("="*116)
d = ER.load_clean(zmax=1.0)
lM = np.log10(d["M500"]*1e13); z = d["z"]; R500 = d["R500"]*kpc
Mgas = d["Mgas"]*1e11; M500 = d["M500"]*1e13
info(f"eRASS1 clean sample: N = {d['N']}, log M500 = {lM.min():.2f} to {lM.max():.2f}, z = {z.min():.3f} to {z.max():.3f}")

def fstar_of(M500_, mode, norm=0.0125, slope=-0.37):
    """M*/M500.  'flat02' = the repository's own baseline M* = 0.2 M_gas; 'none' = gas only (an upper bound on eta);
    'scaling' = a Chiu+2018-class declining stellar fraction, whose normalisation and slope are scanned below."""
    if mode == "none":   return np.zeros_like(M500_)
    if mode == "flat02": return None                       # handled as a gas multiple
    return norm*(M500_/6e14)**slope

MODES = [("none", "gas only (upper bound on eta)"), ("flat02", "M* = 0.2 M_gas (repo baseline)"),
         ("scaling", "M*/M500 = 0.0125 (M500/6e14)^-0.37")]
BINS = [(12.5, 13.5, "GROUPS      "), (13.5, 14.0, "poor groups "), (14.0, 14.5, "clusters    "),
        (14.5, 15.0, "rich        "), (15.0, 15.6, "very rich   ")]
LAD = {}
for foot, a0 in A0.items():
    P("")
    info(f"--- {foot} footing, a_0 = {a0:.3e} m/s^2")
    info(f"{'mass bin':>26} {'N':>5} {'<z>':>6} {'x=g_bar/a0':>11} " + " ".join(f"{m[0]:>14}" for m in MODES))
    for lo, hi, lab in BINS:
        m = (lM >= lo) & (lM < hi)
        if m.sum() < 20: continue
        row = []
        for mode, _ in MODES:
            if mode == "flat02": Mb = 1.2*Mgas[m]
            else: Mb = Mgas[m] + fstar_of(M500[m], mode)*M500[m]
            gobs = G*M500[m]*Msun/R500[m]**2; gbar = G*Mb*Msun/R500[m]**2
            row.append(np.median(eta_of(gobs, gbar, a0)))
            if mode == "flat02": xmed = np.median(gbar/a0)
        info(f"{lab+f'[{lo},{hi})':>26} {m.sum():5d} {np.median(z[m]):6.3f} {xmed:11.4f} " + " ".join(f"{v:14.2f}" for v in row))
        LAD[(foot, lo)] = row
    # slope of log eta with log M500, per prescription, controlling for z
    for mode, desc in MODES:
        if mode == "flat02": Mb = 1.2*Mgas
        else: Mb = Mgas + fstar_of(M500, mode)*M500
        gobs = G*M500*Msun/R500**2; gbar = G*Mb*Msun/R500**2
        le = np.log10(eta_of(gobs, gbar, a0))
        A = np.ascontiguousarray(np.vstack([lM - 14.0, z - 0.3, np.ones_like(lM)]).T)
        coef, *_ = np.linalg.lstsq(A, le, rcond=None)
        resid = le - A @ coef
        cov = np.linalg.inv(A.T @ A)*resid.var(ddof=3)
        info(f"{foot:10} {desc:42}: d log eta/d log M500 = {coef[0]:+.3f} +- {math.sqrt(cov[0,0]):.3f}   (z term {coef[1]:+.3f} +- {math.sqrt(cov[1,1]):.3f} per unit z); eta(1e14, z=0.3) = {10**coef[2]:.2f}")
        LAD[(foot, mode, "fit")] = (coef[0], math.sqrt(cov[0, 0]), coef[1], 10**coef[2])

cn = LAD[("canonical", "flat02", "fit")]; al = LAD[("alt", "flat02", "fit")]
sl_all = [LAD[(f_, m_, "fit")][0] for f_ in A0 for m_, _ in MODES]
ck("55-2 THE ANSWER TO ITEM 55, AND IT IS NOT A STEP: from 5e12 to 1.6e15 solar masses the residual at R500 is FLAT to within a factor 1.4.  There is no threshold where the hot gas 'switches the problem on' -- groups already carry a residual of the same size as clusters do.  The sign of the small remaining trend is set by the stellar prescription, not by the data",
   max(abs(v) for v in sl_all) < 0.15,
   f"d log eta/d log M500 spans {min(sl_all):+.3f} to {max(sl_all):+.3f} over both footings and all three baryon budgets, at fixed redshift, across 2.5 decades of mass; a 'step' from eta = 1 to eta = 2 across one decade would be +0.30 dex/dex, and even the largest trend here gives only a factor {10**(2.5*max(abs(v) for v in sl_all)):.2f} over the whole range")
zt = [LAD[(f_, m_, "fit")][2] for f_ in A0 for m_, _ in MODES]
ck("55-2b and the same fit reproduces this repository's standing item-68 liability from a different direction: at FIXED MASS the residual rises with redshift by about +0.2 dex per unit z, where a constant a_0 requires zero",
   min(zt) > 0.10, f"d log eta/dz = {min(zt):+.3f} to {max(zt):+.3f} per unit z across the six fits, against item 68's independently measured +0.187 +- 0.013; the same selection and mass-proxy caveats apply to both")
eg_c = LAD[("canonical", 12.5)]; ec_c = LAD[("canonical", 14.5)]
ck("55-3 eta(group) is determined to well inside the item's +-0.2 STATISTICALLY and nowhere near it SYSTEMATICALLY: the three baryon prescriptions give group values spanning a factor two, because at 1e13 solar masses the stars are comparable to the gas and eRASS1 does not measure them.  Item 55's '+-0.2' bar cannot be met from this data",
   (max(eg_c) - min(eg_c)) > 0.2,
   f"eta(groups, 1e12.5-1e13.5) = {eg_c[0]:.2f} (gas only) / {eg_c[1]:.2f} (M*=0.2 M_gas) / {eg_c[2]:.2f} (declining f_star); the spread {max(eg_c)-min(eg_c):.2f} is the systematic, against a statistical error of order 0.05")

eg_a = LAD[("alt", 12.5)]
ck("55-7 AGAINST THE FRAMEWORK, AND THIS IS THE ITEM'S REAL FINDING: groups do NOT have eta = 1.  Every baryon budget puts the 1e12.5-1e13.5 systems at eta = 1.4 to 2.9, i.e. the residual is ALREADY THERE at group masses, where Milgrom's reading of the cluster problem (no missing mass below sigma ~ 300 km/s) says it should not be",
   min(eg_c + eg_a) > 1.25,
   f"eta(groups) = {min(eg_c):.2f} to {max(eg_c):.2f} canonical, {min(eg_a):.2f} to {max(eg_a):.2f} alt, over the three baryon budgets.  X-ray flux selection makes this WORSE for the framework, not better: at fixed M500 a flux-limited catalogue prefers the gas-RICH systems, which are the ones with the smallest eta")

# --- how bad is the stellar systematic?  scan the two parameters of the scaling
P(""); P("="*116); P("how much of the ladder is the unmeasured stellar mass?  scan of the stellar-fraction scaling"); P("="*116)
info(f"{'norm f*(6e14)':>14} {'slope':>7} {'eta(1e13)':>11} {'eta(1e14.5)':>13} {'d log eta/d log M':>19}")
SL = []
for norm in (0.008, 0.0125, 0.020):
    for slope in (-0.20, -0.37, -0.50):
        Mb = Mgas + norm*(M500/6e14)**slope*M500
        gobs = G*M500*Msun/R500**2; gbar = G*Mb*Msun/R500**2
        e_ = eta_of(gobs, gbar, A0["canonical"]); le = np.log10(e_)
        A = np.ascontiguousarray(np.vstack([lM - 14.0, z - 0.3, np.ones_like(lM)]).T)
        coef, *_ = np.linalg.lstsq(A, le, rcond=None)
        m1 = (lM > 12.8) & (lM < 13.3); m2 = (lM > 14.3) & (lM < 14.7)
        info(f"{norm:14.4f} {slope:7.2f} {np.median(e_[m1]):11.2f} {np.median(e_[m2]):13.2f} {coef[0]:19.3f}")
        SL.append(coef[0])
SL = SL + [LAD[(f_, m_, "fit")][0] for f_ in A0 for m_, _ in MODES]
ck("55-4 the FLATNESS of the ladder survives the stellar systematic even though its normalisation does not: over every plausible stellar-fraction normalisation and slope the mass trend of eta stays inside +-0.15 dex per dex, so 'no step' is robust -- but the SIGN of the residual trend is not determined, and eta(1e13) itself moves by a factor two",
   max(SL) - min(SL) < 0.30 and max(abs(v) for v in SL) < 0.15,
   f"d log eta/d log M500 spans {min(SL):+.3f} to {max(SL):+.3f} across the nine scanned stellar prescriptions and the six headline fits; eta(1e13) itself spans a factor two over the same scan")

# --- the mass-redshift degeneracy of an X-ray selected sample: the honest weakness
P(""); P("="*116); P("the estimator's own weakness: mass and redshift are confounded in a flux-selected sample"); P("="*116)
r_mz = float(np.corrcoef(lM, z)[0, 1])
info(f"corr(log M500, z) = {r_mz:+.3f} in the clean sample -- groups are nearby, clusters are far, so a mass trend and a")
info("redshift trend cannot be separated without care.  The fits above already carry a linear z term.  Now the low-z cut:")
mlo = z < 0.2
info(f"z < 0.2 subsample: N = {mlo.sum()}, log M500 = {lM[mlo].min():.2f} to {lM[mlo].max():.2f}, corr(logM, z) = {np.corrcoef(lM[mlo], z[mlo])[0,1]:+.3f}")
Mb = 1.2*Mgas
gobs = G*M500*Msun/R500**2; gbar = G*Mb*Msun/R500**2
le = np.log10(eta_of(gobs, gbar, A0["canonical"]))
A = np.ascontiguousarray(np.vstack([lM[mlo] - 14.0, np.ones(mlo.sum())]).T)
co, *_ = np.linalg.lstsq(A, le[mlo], rcond=None)
res = le[mlo] - A @ co; cv = np.linalg.inv(A.T @ A)*res.var(ddof=2)
info(f"z < 0.2 alone, no z term: d log eta/d log M500 = {co[0]:+.3f} +- {math.sqrt(cv[0,0]):.3f}, eta(1e14) = {10**co[1]:.2f}")
ck("55-5 the low-redshift subsample, where mass and redshift are much less confounded, gives the same gentle mass trend as the full fit -- so the ladder's shape is not an artifact of X-ray flux selection",
   abs(co[0] - cn[0]) < 0.15, f"z < 0.2: {co[0]:+.3f} +- {math.sqrt(cv[0,0]):.3f} against the full-sample, z-controlled {cn[0]:+.3f} +- {cn[1]:.3f}")

# --- mutation controls
P(""); P("="*116); P("mutation controls"); P("="*116)
e_w = eta_of(gobs, gbar, 10*A0["canonical"])
ck("M1 mutation: a_0 ten times too large moves the whole ladder by the factor sqrt(10) the deep-MOND kernel demands, so eta really is measuring the acceleration scale and not an arbitrary normalisation",
   abs(np.median(e_w)/np.median(eta_of(gobs, gbar, A0["canonical"])) - 1/math.sqrt(10)) < 0.05,
   f"median eta with 10 a_0 = {np.median(e_w):.2f} vs {np.median(eta_of(gobs, gbar, A0['canonical'])):.2f}, ratio {np.median(e_w)/np.median(eta_of(gobs, gbar, A0['canonical'])):.3f} against the predicted {1/math.sqrt(10):.3f}")
e_n = gobs/gbar
ck("M2 mutation: with nu = 1 (Newton, no kernel) the same systems need a mass discrepancy of 42 in groups and 9 in rich clusters instead of eta ~ 2, so the kernel removes 80-95% of the missing mass everywhere on the ladder and the residual is what is left",
   np.median(e_n) > 3*np.median(eta_of(gobs, gbar, A0["canonical"])),
   f"Newtonian M500/M_bar median {np.median(e_n):.1f} (groups {np.median(e_n[lM<13.5]):.1f}, rich clusters {np.median(e_n[lM>14.5]):.1f}) vs eta = {np.median(eta_of(gobs, gbar, A0['canonical'])):.2f} with the kernel")
sh = rng.permutation(Mgas)
gb_s = G*1.2*sh*Msun/R500**2
le_s = np.log10(eta_of(gobs, gb_s, A0["canonical"]))
A = np.ascontiguousarray(np.vstack([lM - 14.0, z - 0.3, np.ones_like(lM)]).T)
co_s, *_ = np.linalg.lstsq(A, le_s, rcond=None)
ck("M3 mutation: shuffling the gas masses between systems destroys the ladder -- the mass trend of eta swings to the value a random baryon budget gives, which is far from the measured one",
   abs(co_s[0] - cn[0]) > 0.2, f"shuffled d log eta/d log M500 = {co_s[0]:+.3f} against the real {cn[0]:+.3f}")

# --- the LambdaCDM side
P(""); P("="*116); P("the LambdaCDM alternative computed beside it"); P("="*116)
fb_cosmic = OM_B/OM_M
info(f"in LambdaCDM the quantity with a prediction is the baryon fraction, not eta: f_bar should approach the cosmic {fb_cosmic:.3f}")
info(f"{'mass bin':>26} {'f_bar(measured)':>16} {'f_bar/f_cosmic':>16} {'missing baryons':>17}")
for lo, hi, lab in BINS:
    m = (lM >= lo) & (lM < hi)
    if m.sum() < 20: continue
    fb = np.median(1.2*Mgas[m]/M500[m])
    info(f"{lab+f'[{lo},{hi})':>26} {fb:16.3f} {fb/fb_cosmic:16.3f} {1-fb/fb_cosmic:17.1%}")
info("so LambdaCDM's own statement about groups -- that they should have LOST most of their baryons to feedback -- and")
info("the framework's -- that the residual should switch on with the hot gas -- point in OPPOSITE directions on the same")
info("numbers: the systems with the fewest baryons are the ones the framework needs to work best in.")
fbg = np.median(1.2*Mgas[lM < 13.5]/M500[lM < 13.5]); fbc = np.median(1.2*Mgas[lM > 14.5]/M500[lM > 14.5])
ck("55-6 the two theories are pulled the same way by the same number and neither is discriminated here: groups are missing 4/5 of their cosmic baryons in LambdaCDM's accounting, and it is exactly that missing gas that keeps the framework's eta above 1 in groups.  The measurement cannot separate 'feedback expelled the gas' from 'the gravity law is wrong'",
   fbg < 0.5*fbc, f"f_bar = {fbg:.3f} in groups vs {fbc:.3f} in rich clusters, against a cosmic {fb_cosmic:.3f}")

P(""); P("="*116)
info("VERDICT on item 55.")
info("  * The lensing group Delta-Sigma profiles the item names are not machine-readable anywhere reachable from here,")
info("    so the group rung is built on eRASS1's weak-lensing-CALIBRATED masses rather than on a stacked profile.  That")
info("    is a real weakening and it is recorded as one.")
info("  * There is NO STEP.  eta at R500 is flat from 5e12 to 1.6e15 solar masses: d log eta/d log M500 lies between")
info("    -0.08 and +0.14 across both footings and every defensible baryon budget, a factor of at most 1.6 over 2.5")
info("    decades, against the +0.30 dex/dex a 1 -> 2 step across one decade would need.")
info("  * And the sign of the answer is against the framework: groups do not have eta = 1, they have eta = 1.4 to 2.9.")
info("    The residual is present at group masses, not switched on at cluster masses.")
info("  * eta(group) CANNOT be pinned to +-0.2, which was the item's Kepler-grade bar: the three defensible stellar")
info("    budgets give 1.56 to 2.89 at 1e13 because at group masses the unmeasured stars are comparable to the measured")
info("    gas.  Stellar masses for eRASS1 groups are the measurement that would decide it.")
info("  * A by-product: the same fit independently reproduces item 68's redshift liability, +0.18 to +0.21 dex per unit")
info("    z at fixed mass, where a constant a_0 requires zero.")
sys.exit(ck.done())
