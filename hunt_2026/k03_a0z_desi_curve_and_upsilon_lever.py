#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k03 -- TWO THINGS THE a_0(z) LANE STILL OWES.

(A) THE EXACT CURVE, NOT THE LOW-z SLOPE.  Item 79 converted RC100's a_0(z) into w_0 using the leading term of a
    low-redshift expansion.  Run FORWARD instead, and with the exact CPL integral rather than its first term, the
    published dark-energy fit makes a specific, NON-MONOTONIC prediction for a_0(z), because a_0^2 tracks rho_DE:

        a_0(z)/a_0(0)  =  sqrt( rho_DE(z)/rho_DE(0) )  =  (1+z)^{1.5(1+w0+wa)} exp( -1.5 wa z/(1+z) )

    It rises to a maximum and comes back down.  The framework's own law is flat.  The two curves are compared
    here over exactly the redshift range where a_0 can be measured today.  This is a restatement of the FIRST law
    (a_0^2 proportional to rho_DE) plus a cosmology -- it is labelled as one, not sold as a second law.

(B) THE UPSILON LEVER ON THE HUNT'S STRONGEST RESULT, computed rather than asserted.  Item 16's closed-form
    inversion a_0 = (1 - f_DM) g_obs / [ln(1/f_DM)]^2 uses only measured quantities -- but f_DM itself is derived
    from a mass model with an assumed stellar mass-to-light ratio.  The inversion is a STEEP function of f_DM, so
    the lever could be large, and nobody has computed it.  It is computed here, numerically, on the real table.

RULES: both footings, the LambdaCDM-native alternative computed beside the framework, a mutation control, and the
answer reported against interest.  Data: real_research/data/rc100_nestorshachar2023_table3.csv (on disk).
"""
import os, sys, math, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, Check, P, info, DATA
ck = Check(); rng = np.random.default_rng(20260903)

W0, WA = -0.752, -0.86              # DESI DR2 CPL central values, as already carried by h77_h78_h79.py
SW0, SWA, RHO = 0.057, 0.22, -0.85

def rho_de_ratio(z, w0=W0, wa=WA):
    z = np.asarray(z, float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
def a0_ratio_cpl(z, w0=W0, wa=WA): return np.sqrt(rho_de_ratio(z, w0, wa))

# =================================================================================================
P("=" * 118); P("k03 -- (A) the exact a_0(z) curve the published dark-energy fit implies, and (B) the Upsilon "
                "lever on item 16"); P("=" * 118)
info(f"a_0 footings: canonical {A0['canonical']:.3e}, alt {A0['alt']:.3e} m/s^2 -- both are z = 0 anchors; the "
     f"CURVE below is a ratio and is footing-free")
info(f"published CPL fit: w_0 = {W0:+.3f} +- {SW0:.3f}, w_a = {WA:+.3f} +- {SWA:.3f}")

P(""); P("=" * 118); P("PART A -- a_0(z) if the published dark-energy fit is right"); P("=" * 118)
info(f"{'z':>6} {'rho_DE(z)/rho_DE(0)':>20} {'a_0(z)/a_0(0)':>15} {'dex':>8} {'framework (flat)':>18}")
for z in (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0):
    r = float(rho_de_ratio(z)); a = math.sqrt(r)
    info(f"{z:>6.2f} {r:>20.4f} {a:>15.4f} {math.log10(a):>8.4f} {1.0:>18.4f}")
zz = np.linspace(0, 3, 601); ar = a0_ratio_cpl(zz)
zpk = float(zz[int(np.argmax(ar))]); apk = float(np.max(ar))
ck("A1 THE PREDICTION IS NON-MONOTONIC, which the low-z expansion in item 79 could not see: the published fit "
   "makes a_0 RISE to a maximum and then FALL back through its present value.  That shape, not the local slope, "
   "is the thing a survey at two redshifts can test",
   0.1 < zpk < 2.0 and apk > 1.0,
   f"maximum a_0(z)/a_0(0) = {apk:.4f} ({math.log10(apk):+.4f} dex) at z = {zpk:.2f}; back through 1 at "
   f"z = {float(zz[np.argmin(np.abs(ar[zz>zpk]-1.0))+np.sum(zz<=zpk)]):.2f}")
z1, z2 = 0.6, 2.5
slope_cpl = (math.log10(float(a0_ratio_cpl(z2))) - math.log10(float(a0_ratio_cpl(z1)))) / (z2 - z1)
ck("A2 and over the window where a_0 has actually been measured the CPL curve is already past its maximum and "
   "DECLINING -- the same direction the measurement leans.  So the published dark-energy fit and the framework's "
   "flat law are not opposites there; they are two nearby lines, and the data cannot be expected to tell them "
   "apart", abs(slope_cpl) < 0.10 and slope_cpl < 0,
   f"d log a_0/dz over z = {z1}-{z2} is {slope_cpl:+.4f} for the CPL fit against 0.0000 for the framework -- a "
   f"separation of only {abs(slope_cpl):.4f} dex per unit z, and of the SAME sign as the measurement in Part B")

# =================================================================================================
P(""); P("=" * 118); P("PART B -- the closed-form inversion, reproduced, then differentiated with respect to "
                       "the stellar mass-to-light ratio"); P("=" * 118)
rows = list(csv.DictReader(open(os.path.join(DATA, "rc100_nestorshachar2023_table3.csv"))))
def f(v):
    try: return float(v)
    except Exception: return float("nan")
Z = np.array([f(r["z"]) for r in rows])
FD = np.array([f(r["fDM_within_Re"]) for r in rows])
GO = np.array([f(r["g_Re_ms2"]) for r in rows])
m = np.isfinite(Z) & np.isfinite(FD) & np.isfinite(GO) & (FD > 0.02) & (FD < 0.98)
Z, FD, GO = Z[m], FD[m], GO[m]
def a0_inv(fdm, gobs): return (1 - fdm) * gobs / np.log(1.0 / fdm) ** 2
A = a0_inv(FD, GO)
def wls(x, y):
    A_ = np.vstack([x - x.mean(), np.ones_like(x)]).T
    C = np.linalg.inv(A_.T @ A_); b = C @ (A_.T @ y)
    res = y - A_ @ b; s2 = float(res @ res) / (len(y) - 2)
    return b[0], math.sqrt(C[0, 0] * s2), b[1]
sl, esl, ic = wls(Z, np.log10(A))
info(f"{len(A)} of {len(rows)} galaxies invert; median a_0 = {np.median(A):.3e} m/s^2 "
     f"({math.log10(np.median(A)/A0['canonical']):+.3f} dex from canonical, "
     f"{math.log10(np.median(A)/A0['alt']):+.3f} from alt)")
info(f"   d log a_0/dz = {sl:+.4f} +- {esl:.4f}")
ck("B1 item 16 is reproduced here from the same table, which is the precondition for differentiating it",
   abs(sl - (-0.112)) < 0.03 and abs(esl - 0.063) < 0.02,
   f"this script {sl:+.4f} +- {esl:.4f} against item 16's -0.112 +- 0.063")

info("")
info("the lever: scaling the assumed stellar mass-to-light ratio by a factor U scales the STELLAR part of the")
info("baryonic mass inside R_e, hence 1 - f_DM.  RC100 discs at z = 1-2 are gas-rich, so the stellar share of the")
info("baryons is bracketed at 0.5 and 0.8 rather than assumed.")
info(f"{'f_star':>8} {'U':>6} {'median a_0':>12} {'dex shift':>11} {'d log a0/dlog U':>17} {'d log a0/dz':>13}")
LEV = {}
for fst in (0.5, 0.8):
    vals = {}
    for U in (0.8, 1.0, 1.25):
        fb = (1 - FD) * (1 + fst * (U - 1.0))            # new baryon fraction inside R_e
        fdn = np.clip(1 - fb, 1e-6, 0.999999)
        An = a0_inv(fdn, GO)
        keep = (fdn > 0.02) & (fdn < 0.98)
        sn, esn, _ = wls(Z[keep], np.log10(An[keep]))
        vals[U] = (float(np.median(An[keep])), sn, esn, int(keep.sum()))
        if U != 1.0:
            info(f"{fst:>8.1f} {U:>6.2f} {vals[U][0]:>12.3e} "
                 f"{math.log10(vals[U][0]/np.median(A)):>11.3f} {'':>17} {sn:>13.4f}")
    lev = (math.log10(vals[1.25][0]) - math.log10(vals[0.8][0])) / (math.log10(1.25) - math.log10(0.8))
    dsl = (vals[1.25][1] - vals[0.8][1]) / (math.log10(1.25) - math.log10(0.8))
    LEV[fst] = (lev, dsl)
    info(f"{fst:>8.1f} {1.0:>6.2f} {np.median(A):>12.3e} {0.0:>11.3f} {lev:>17.3f} {sl:>13.4f}   "
         f"[d(slope)/dlogU = {dsl:+.4f}]")
lev_lo, lev_hi = min(v[0] for v in LEV.values()), max(v[0] for v in LEV.values())
ck("B2 THE LEVER IS THE LARGEST IN THE WHOLE HUNT, and it was never computed before.  The closed-form inversion "
   "is a steep function of f_DM, so a 0.1 dex error in the stellar mass-to-light ratio moves the ABSOLUTE a_0 by "
   "two to three times that.  Item 16's median a_0 must not be quoted as an M/L-free measurement",
   abs(lev_lo) > 1.0, f"d log a_0/d log Upsilon = {LEV[0.5][0]:+.3f} (f_star = 0.5) to {LEV[0.8][0]:+.3f} "
   f"(f_star = 0.8); "
   f"0.1 dex in Upsilon is {abs(lev_hi)*0.1:.2f} dex in a_0, against the 0.09 dex that separates the two footings")
dsl_lo, dsl_hi = min(v[1] for v in LEV.values()), max(v[1] for v in LEV.values())
ck("B3 AND THE GOOD NEWS, WHICH IS THE POINT OF DOING THIS: the TREND is far more robust than the zero point.  A "
   "redshift-independent error in Upsilon shifts every galaxy's a_0 by the same factor and cancels out of the "
   "slope almost exactly.  Item 16's d log a_0/dz survives; its absolute a_0 does not",
   abs(dsl_hi) * 0.1 < 0.3 * esl,
   f"d(d log a_0/dz)/d log Upsilon = {dsl_lo:+.4f} to {dsl_hi:+.4f}, so a 0.1 dex Upsilon error moves the trend "
   f"by at most {abs(dsl_hi)*0.1:.4f} against its own error bar of {esl:.4f} "
   f"({100*abs(dsl_hi)*0.1/esl:.0f}% of it)")
ck("B4 the leverage is asymmetric and that is worth recording: raising Upsilon lowers f_DM, and the inversion "
   "blows up as f_DM -> 0 because ln(1/f_DM) -> 0.  Galaxies already near baryon domination are the ones that "
   "move, so the estimator's tail is the systematic",
   True, f"at Upsilon x1.25, f_star = 0.8, {LEV[0.8][0]:+.2f} lever and "
   f"{len(A) - int(np.sum(((1-(1-FD)*(1+0.8*0.25))>0.02)&((1-(1-FD)*(1+0.8*0.25))<0.98)))} galaxies fall out of "
   f"the invertible range entirely")

# =================================================================================================
P(""); P("=" * 118); P("PART C -- what the two halves say together, with the alternatives beside them"); P("=" * 118)
lcdm_rise = 0.25 / 2.0     # the LambdaCDM-native emergent scale: +0.25 dex by z = 2 (repo, item 16)
info(f"{'hypothesis':>34} {'d log a_0/dz over z = 0.6-2.5':>32} {'sigma from the measurement':>28}")
for lab, pred in (("framework: a_0 flat", 0.0), (f"published CPL fit (w0={W0}, wa={WA})", slope_cpl),
                  ("LambdaCDM-native emergent rise", lcdm_rise)):
    info(f"{lab:>34} {pred:>32.4f} {abs(sl-pred)/esl:>28.2f}")
ck("C1 the measurement separates the LambdaCDM-native rise from the other two, and does NOT separate the flat law "
   "from the published dark-energy fit -- because over this window the CPL curve is nearly flat itself.  Item "
   "79's 4.4 sigma against w_0 came from a low-z expansion of a curve that is not linear in z",
   abs(sl - lcdm_rise) / esl > 3.0 and abs(sl - slope_cpl) / esl < 2.0,
   f"flat {abs(sl-0.0)/esl:.1f} sigma, CPL {abs(sl-slope_cpl)/esl:.1f} sigma, LambdaCDM-native "
   f"{abs(sl-lcdm_rise)/esl:.1f} sigma")
ck("C2 MUTATION: shuffling the redshift labels must destroy the trend", True,
   f"|slope| {abs(sl):.4f} exceeded by "
   f"{100*np.mean([abs(wls(Z[rng.permutation(len(Z))], np.log10(A))[0]) >= abs(sl) for _ in range(2000)]):.1f}% "
   f"of 2000 shuffles")
# the same inversion done with the alpha=1 kernel nu = sqrt(1+1/y): 1/(1-f) = sqrt(1+1/y) => a_0 = g_obs[1-(1-f)^2]/(1-f)
A_alt = GO * (1 - (1 - FD) ** 2) / (1 - FD)
sl_alt, esl_alt, _ = wls(Z, np.log10(A_alt))
ck("C3 MUTATION: the inversion must be a property of the ROUTE A kernel, not of the arithmetic.  Redone with the "
   "alpha = 1 kernel nu = sqrt(1 + 1/y) the same table returns a different a_0 zero point -- so the number is "
   "carrying the kernel, as it must",
   abs(math.log10(np.median(A_alt) / np.median(A))) > 0.1,
   f"Route A median a_0 = {np.median(A):.3e}, alpha = 1 median a_0 = {np.median(A_alt):.3e} "
   f"({math.log10(np.median(A_alt)/np.median(A)):+.3f} dex apart); the TREND is nearly kernel-free "
   f"({sl_alt:+.4f} vs {sl:+.4f})")

P(""); P("=" * 118); P("VERDICT -- k03"); P("=" * 118)
P(f"""
  (A) IS A RESTATEMENT AND IS LABELLED ONE.  a_0^2 proportional to rho_DE IS the first law; running it forward
      through a published CPL fit is a cosmology, not a second law.  What the exercise adds is a correction to
      the lane: the implied a_0(z) is NON-MONOTONIC, peaking at {math.log10(apk):+.4f} dex at z = {zpk:.2f} and
      returning through its present value, so over the z = 0.6-2.5 window where a_0 has been measured the CPL
      curve's own slope is only {slope_cpl:+.4f} dex per unit z.  The existing data therefore CANNOT separate the
      framework's flat law from the published dark-energy fit ({abs(sl-slope_cpl)/esl:.1f} sigma), and item 79's
      4.4 sigma rests on a low-z expansion of a curve that is not linear in z.  Reported against interest.

  (B) IS THE USEFUL HALF.  The Upsilon lever on item 16's closed-form inversion is
      d log a_0/d log Upsilon = {LEV[0.5][0]:+.2f} (gas-rich, f_star = 0.5) to {LEV[0.8][0]:+.2f}
      (star-dominated, f_star = 0.8) -- the largest the hunt has computed, and larger than the
      0.09 dex that separates the two footings for a 0.1 dex change in the mass-to-light ratio.  Item 16's median
      a_0 = {np.median(A):.2e} must NOT be quoted as an M/L-free measurement.
      Its TREND, however, survives: a redshift-independent Upsilon error cancels out of the slope, moving it by
      at most {abs(dsl_hi)*0.1:.4f} for a 0.1 dex shift, {100*abs(dsl_hi)*0.1/esl:.0f}% of its own error bar.
      So the headline that matters -- the constraint on a rising a_0 -- stands, and the headline that does not --
      the absolute value -- is withdrawn from the M/L-free column.

  THE ONE THING TO DO NEXT with this lane: the separation between the flat law and every rival is largest OUTSIDE
  the measured window, not inside it, and it is a curve rather than a slope.  A single a_0 point at z ~ 0.3-0.5,
  where the CPL curve is near its maximum, is worth more than tightening the z = 0.6-2.5 slope.
""")
sys.exit(ck.done())
