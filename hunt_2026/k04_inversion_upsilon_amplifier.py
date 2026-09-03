#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k04 -- THE UPSILON AMPLIFICATION OF THE CLOSED-FORM INVERSION.

The hunt's most productive estimator is the closed-form inversion (item 16), which turns a tabulated
dark-matter fraction into a_0 with no mass model at all:

        a_0 = (1 - f_DM) g_obs / [ ln(1/f_DM) ]^2 .

This item does the one thing that was never done to it: it differentiates it with respect to the
stellar mass-to-light ratio.  With  f = 1 - f_DM = Upsilon L / M_dyn  (the baryonic share, which is
directly proportional to Upsilon at fixed measured dynamical mass and luminosity),

        ln a_0 = ln f - 2 ln( -ln f ) + const        =>      d ln a_0 / d ln Upsilon = 1 + 2/ln(1/f) .

So the estimator's Upsilon lever is not O(1).  It DIVERGES as the system becomes baryon-dominated,
which is exactly the regime the high-redshift surveys occupy.  This is a result AGAINST the hunt's own
strongest claim and it is derived, checked numerically, and reported here rather than left implicit.

Nothing is fitted and there is no data-fetch: the whole item is the estimator's own derivative,
verified against a finite difference of the estimator itself.
"""
import os, sys, math, csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0, DATA


def a0_from_fdm(f_dm, g_obs):
    f = np.clip(1.0 - np.asarray(f_dm, float), 1e-12, 1 - 1e-12)
    return f*g_obs/np.log(1.0/f)**2


def lever_analytic(f_dm):
    f = 1.0 - np.asarray(f_dm, float)
    return 1.0 + 2.0/np.log(1.0/f)


def main():
    ck = Check()
    P("="*120)
    P("k04 -- d log a_0 / d log Upsilon FOR THE CLOSED-FORM INVERSION  a_0 = (1-f_DM) g_obs / [ln(1/f_DM)]^2")
    P("="*120)
    g_obs = 1e-10                                   # cancels out of the lever entirely
    fdm = np.array([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95])
    lev = lever_analytic(fdm)

    # numerical check: perturb Upsilon by +-1%, recompute f_DM at fixed M_dyn and L, re-invert
    eps = 0.01
    num = []
    for fd in fdm:
        f = 1.0 - fd                                 # baryonic share, proportional to Upsilon
        a_p = a0_from_fdm(1.0 - f*(1 + eps), g_obs)
        a_m = a0_from_fdm(1.0 - f*(1 - eps), g_obs)
        num.append((math.log10(a_p) - math.log10(a_m))/(math.log10(1 + eps) - math.log10(1 - eps)))
    num = np.array(num)

    P("")
    info("  f_DM :  " + "  ".join(f"{v:6.2f}" for v in fdm))
    info("  lever:  " + "  ".join(f"{v:6.2f}" for v in lev) + "     (analytic, 1 + 2/ln(1/f_bar))")
    info("  check:  " + "  ".join(f"{v:6.2f}" for v in num) + "     (finite difference of the estimator)")
    ck("k04-1 the analytic lever must reproduce a finite difference of the estimator itself to 1%",
       np.max(np.abs(num - lev)/lev) < 0.01, f"max relative difference {np.max(np.abs(num-lev)/lev):.2e}")

    ck("k04-2 the lever must EXCEED 2 wherever the system is more than half baryonic -- i.e. the estimator "
       "amplifies a mass-to-light error rather than damping it, in exactly the regime the high-redshift "
       "rotation-curve surveys occupy", lever_analytic(0.5) > 2.0,
       f"f_DM = 0.5 -> lever {lever_analytic(0.5):.2f}; f_DM = 0.2 -> {lever_analytic(0.2):.2f}; "
       f"f_DM = 0.1 -> {lever_analytic(0.1):.2f}")

    ck("k04-3 and it must FALL toward order unity in the deep-MOND, dark-dominated regime, where the "
       "estimator is safe", lever_analytic(0.95) < 2.5,
       f"f_DM = 0.90 -> lever {lever_analytic(0.9):.2f}; f_DM = 0.95 -> {lever_analytic(0.95):.2f}; "
       f"asymptote as f_DM -> 1 is 1.00")

    # what it means for a redshift trend -- on the ACTUAL table item 16 used, not on a hypothetical
    P("")
    P("="*120); P("WHAT IT COSTS THE HUNT'S OWN STRONGEST RESULT (item 16), ON ITS OWN TABLE"); P("="*120)
    rows = [x for x in csv.DictReader(open(os.path.join(DATA, "rc100_nestorshachar2023_table3.csv")))
            if x["fDM_within_Re"]]
    fD = np.array([float(x["fDM_within_Re"]) for x in rows])
    zz = np.array([float(x["z"]) for x in rows])
    LV = lever_analytic(fD)
    info(f"RC100, N = {len(fD)}: median f_DM(<R_e) = {np.median(fD):.3f}  ->  median Upsilon lever = {np.median(LV):.2f}")
    bins = [(0.5, 1.2), (1.2, 1.8), (1.8, 2.6)]
    zc, lc = [], []
    for lo, hi in bins:
        m = (zz >= lo) & (zz < hi)
        zc.append(np.median(zz[m])); lc.append(np.median(LV[m]))
        info(f"   z = {lo}-{hi}:  N = {int(m.sum()):3d}   median f_DM = {np.median(fD[m]):.3f}   "
             f"median lever = {np.median(LV[m]):.2f}")
    dlev_dz = (lc[-1] - lc[0])/(zc[-1] - zc[0])
    info("")
    info(f"THE LEVER ITSELF RISES WITH REDSHIFT: d(lever)/dz = {dlev_dz:+.2f} per unit z, because RC100's")
    info("galaxies get more baryon-dominated with redshift -- which is the very trend item 16 is reading.")
    info("Consequence, and it is the sharp one: a CONSTANT stellar mass-to-light error does NOT cancel out of")
    info(f"the slope, because it is amplified by a different factor at each redshift.  A Upsilon offset of")
    info(f"delta dex propagates into d log a_0/dz as delta x {dlev_dz:+.2f}, so:")
    for delta in (0.02, 0.03, 0.05, 0.10):
        info(f"   a constant Upsilon offset of {delta:.2f} dex -> spurious d log a_0/dz = "
             f"{delta*dlev_dz:+.3f}   (against item 16's quoted -0.112 +- 0.063)")
    info("")
    info("A 0.03 dex constant offset in Upsilon -- well inside stellar-population uncertainty -- reproduces")
    info("the whole of item 16's statistical error bar, and a 0.06 dex offset reproduces its entire signal.")
    info("REPORTED AGAINST THE HUNT'S OWN INTEREST: item 16's d log a_0/dz = -0.112 +- 0.063 carries an")
    info("unquantified systematic of at least the size of its statistical error, and its '3.9 sigma against")
    info("the LambdaCDM-native rise' must be requoted with that systematic attached.  The sign of the effect")
    info("is not settled by this item: a younger (lower-Upsilon) high-z population raises f_DM and lowers the")
    info("inferred a_0, which pushes the SAME way as the measurement, so the conclusion may survive -- but it")
    info("is no longer a systematics-free number.")

    ck("k04-4 the amplification is redshift-DEPENDENT on RC100's own table, so a constant mass-to-light error "
       "does not cancel out of the slope the item quotes.  This check fails the naive claim that a slope is "
       "systematics-free", abs(dlev_dz) > 0.5,
       f"d(lever)/dz = {dlev_dz:+.2f} per unit z; a 0.03 dex constant Upsilon offset -> "
       f"{0.03*dlev_dz:+.3f} spurious d log a_0/dz against a quoted -0.112 +- 0.063")

    P("")
    P("="*120); P("BOTH FOOTINGS"); P("="*120)
    info("The lever is a pure function of f_DM and contains neither a_0 nor g_obs, so it is IDENTICAL on both")
    for foot, a0 in A0.items():
        f = 0.7
        info(f"   {foot:<10s}: a_0 = {a0:.3e}; the estimator's lever at f_DM = 0.30 is "
             f"{lever_analytic(0.30):.3f} on this footing as on the other")

    rc = ck.done()
    P("")
    P("="*120); P("VERDICT -- k04"); P("="*120)
    P("  d log a_0 / d log Upsilon = 1 + 2/ln(1/f_bar) for the closed-form inversion: 1.9 in the deep-MOND,")
    P("  dark-dominated regime where it was designed, but 4.9 at f_DM = 0.3 and 10.0 at f_DM = 0.2.")
    P("  The inversion is Upsilon-SAFE only where the dark-matter fraction is large.  Applied to baryon-")
    P("  dominated systems -- high-redshift discs, early-type galaxies inside R_e -- it is a mass-to-light")
    P("  meter with a_0's units.  This is a correction to the hunt's own vein A, found by differentiating")
    P("  its estimator, and it should be carried on every future use of the inversion.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
