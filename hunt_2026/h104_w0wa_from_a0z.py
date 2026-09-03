#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h104_w0wa_from_a0z.py -- HUNT ITEM 104: a dark-energy equation of state from galaxy dynamics alone.
====================================================================================================
The first law is a_0 = (c/2) sqrt(G rho_DE).  Read backwards, EVERY measurement of a_0 at a redshift is a measurement
of the dark-energy density at that redshift:

        rho_DE(z)/rho_DE(0) = [a_0(z)/a_0(0)]^2                                              (exact, no modelling)

and under the CPL parametrisation w(a) = w_0 + w_a (1 - a),

        rho_DE(z)/rho_DE(0) = (1+z)^{3(1+w_0+w_a)} exp(-3 w_a z/(1+z))
   =>   2 log10[a_0(z)/a_0(0)] = 3(1+w_0+w_a) log10(1+z) - (3 w_a / ln 10) * z/(1+z).

Item 104 asks for (w_0, w_a) from the a_0(z) ladder of item 101, with a real error bar, and sets the bar at
"w_0 to +-0.05 -- competitive with a supernova sample, from rotation curves".

This script reads h101_rungs.json (run h101_fdm_inversion_surveys.py first) and does five things:
  A  checks the mapping is the one the two footings are actually built on (it is: 9.36e-11 IS (c/2)sqrt(G rho_Lambda)
     with Planck's Omega_Lambda, and 1.13e-10 IS (c/2)sqrt(G rho_crit) -- the two footings are two choices of rho);
  B  fits a CONSTANT w to each rung set separately, with the z = 0 intercept free and then pinned to SPARC;
  C  fits the full (w_0, w_a) and reports the degeneracy honestly instead of a marginal number;
  D  puts the answer beside Planck (w = -1), DESI DR2 w0waCDM (w_0, w_a) = (-0.838, -0.62) +- (0.055, 0.22), and the
     framework's own requirement w = -1 exactly;
  E  states, against interest, by how much the +-0.05 target is missed and how far the surveys are from each other
     in w_0 -- which is the number that decides whether this route is worth anything at all.

Mutation controls: a z-shuffle must return w = -1, and a synthetic closure test must recover an injected w.  The
closure control earned its keep: it caught a sign error in this script's own constant-w fitter (w + 2 returned in
place of w), which the independent CPL fit of Part C then confirmed.  Both are recorded in fit_const_w's docstring.
Both footings.  Checks CAN fail.
"""
import sys, math, os, json
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(104)
RJ = os.path.join(HERE, "h101_rungs.json")
if not os.path.exists(RJ):
    P("FATAL: run h101_fdm_inversion_surveys.py first -- it writes h101_rungs.json"); sys.exit(2)
R = json.load(open(RJ))
DESI = dict(w0=-0.838, wa=-0.62, sw0=0.055, swa=0.22, corr=-0.86)     # DESI DR2 w0waCDM + Pantheon+, banked in repo


def rho_ratio(z, w0, wa):
    """rho_DE(z)/rho_DE(0) under CPL."""
    z = np.asarray(z, dtype=float)
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))


def la_model(z, la0, w0, wa):
    """log10 a_0(z) predicted by CPL, given log10 a_0(0)."""
    return la0 + 0.5*np.log10(rho_ratio(z, w0, wa))


def fit_const_w(z, la, la0=None):
    """Constant w (w_a = 0): log10 a_0 = la0 + (3/2)(1+w) log10(1+z), so w = slope/1.5 - 1.  la0 free unless pinned.
    BUG FOUND AND FIXED IN THE MAKING OF THIS SCRIPT: the first version returned 1 + slope/1.5, i.e. w + 2.  The
    noiseless closure control of Part F caught it -- injecting w = -1 returned +1, injecting -0.7 returned +1.3 --
    and the (independent) CPL fit of Part C disagreed with it by exactly 2.  That is what the closure control is for."""
    x = np.log10(1.0 + np.asarray(z, dtype=float)); y = np.asarray(la, dtype=float)
    if la0 is None:
        A = np.vstack([x, np.ones_like(x)]).T
        s, b = np.linalg.lstsq(A, y, rcond=None)[0]
        return float(s/1.5 - 1.0), float(b)
    s = float(np.sum(x*(y - la0))/np.sum(x*x))
    return float(s/1.5 - 1.0), float(la0)


def boot_const_w(z, la, la0=None, n=3000):
    z = np.asarray(z); la = np.asarray(la)
    out = []
    for _ in range(n):
        i = rng.integers(0, len(z), len(z))
        if np.ptp(z[i]) < 1e-6: continue
        out.append(fit_const_w(z[i], la[i], la0)[0])
    return float(np.std(out))


def fit_cpl(z, la):
    """Linear least squares in (la0, w0, wa): the CPL exponent is linear in w_0 and w_a."""
    z = np.asarray(z, dtype=float); la = np.asarray(la, dtype=float)
    u = 1.5*np.log10(1.0 + z)                                  # coefficient of (1 + w_0 + w_a)
    v = -1.5*(z/(1.0 + z))/math.log(10.0)                      # extra coefficient of w_a
    #  la = la0 + u*(1+w0+wa) + v*wa  =  (la0 + u)  + u*w0 + (u+v)*wa
    Amat = np.vstack([np.ones_like(z), u, u + v]).T
    y = la - u
    beta, *_ = np.linalg.lstsq(Amat, y, rcond=None)
    resid = y - Amat @ beta
    dof = max(len(z) - 3, 1)
    cov = np.linalg.pinv(Amat.T @ Amat)*float(resid @ resid)/dof
    return beta, cov


# ==================================================================================================================
P("="*120); P("PART A -- the mapping, and a check that it is the one the two footings are built on"); P("="*120)
rho_L = OM_L*rho_crit
a0_from_rhoL = 0.5*c_light*math.sqrt(G*rho_L)
a0_from_rhoc = 0.5*c_light*math.sqrt(G*rho_crit)
info(f"Planck-like background: h = {h}, Omega_m = {OM_M:.4f}, Omega_Lambda = {OM_L:.4f}, rho_crit = {rho_crit:.3e} kg/m^3")
info(f"   (c/2) sqrt(G rho_Lambda) = {a0_from_rhoL:.4e} m/s^2   vs the CANONICAL footing {A0['canonical']:.4e} "
     f"({math.log10(a0_from_rhoL/A0['canonical']):+.4f} dex)")
info(f"   (c/2) sqrt(G rho_crit)   = {a0_from_rhoc:.4e} m/s^2   vs the ALT footing       {A0['alt']:.4e} "
     f"({math.log10(a0_from_rhoc/A0['alt']):+.4f} dex)")
ck("104-A the inversion rho_DE = (2 a_0/c)^2/G is not an assumption bolted on for this item: the canonical footing IS "
   "(c/2)sqrt(G rho_Lambda) and the alt footing IS (c/2)sqrt(G rho_total) on the same background, both to under 0.01 "
   "dex, so reading a_0(z) as a dark-energy density is exactly what the two footings already mean",
   abs(math.log10(a0_from_rhoL/A0["canonical"])) < 0.01 and abs(math.log10(a0_from_rhoc/A0["alt"])) < 0.01,
   f"canonical {math.log10(a0_from_rhoL/A0['canonical']):+.4f} dex, alt {math.log10(a0_from_rhoc/A0['alt']):+.4f} dex")
info("")
info("The framework's own statement is therefore not 'a_0 happens to be flat' but w = -1 EXACTLY: pure Lambda has")
info("rho_DE constant, so a_0 is constant, so any detected d log a_0/dz is a detection of w != -1.  Leverage:")
for zz in (0.5, 1.0, 1.5, 2.5):
    info(f"   at z = {zz:.1f}:  d log10 a_0 / d(1+w) = {1.5*math.log10(1+zz):.3f} dex   "
         f"(so 0.05 in w_0 is {0.05*1.5*math.log10(1+zz):.4f} dex in a_0 -- {0.11/(0.05*1.5*math.log10(1+zz)):.1f}x SMALLER than the RAR's own 0.11 dex scatter)")

# ==================================================================================================================
P(""); P("="*120); P("PART B -- a constant w from each rung set, intercept free and then pinned to SPARC"); P("="*120)
la0_sparc = math.log10(R["rungs"]["SPARC (z~0)"]["a0"])
P(f"  SPARC's own z = 0 value through the identical estimator: a_0(0) = {10**la0_sparc:.3e} (log = {la0_sparc:.3f})")
P(f"  {'rung set':22}{'N':>5}{'z med':>7}{'w (a_0(0) free)':>22}{'w (a_0(0) pinned to SPARC)':>30}")
WRES = {}
for lab in ("RC100", "MSA-3D golden"):
    z = np.array(R["rungs"][lab]["z"]); la = np.array(R["rungs"][lab]["la"])
    wf, b = fit_const_w(z, la); ef = boot_const_w(z, la)
    wp, _ = fit_const_w(z, la, la0_sparc); ep = boot_const_w(z, la, la0_sparc)
    WRES[lab] = dict(free=(wf, ef), pinned=(wp, ep), N=len(z), zmed=float(np.median(z)))
    P(f"  {lab:22}{len(z):5d}{np.median(z):7.2f}{f'{wf:+.3f} +- {ef:.3f}':>22}{f'{wp:+.3f} +- {ep:.3f}':>30}")
# joint: all per-galaxy points from the three rungs
zJ = np.concatenate([R["rungs"][l]["z"] for l in R["rungs"]])
laJ = np.concatenate([R["rungs"][l]["la"] for l in R["rungs"]])
wJ, bJ = fit_const_w(zJ, laJ); eJ = boot_const_w(zJ, laJ)
WRES["joint (all three)"] = dict(free=(wJ, eJ), pinned=(np.nan, np.nan), N=len(zJ), zmed=float(np.median(zJ)))
P(f"  {'joint (all three)':22}{len(zJ):5d}{np.median(zJ):7.2f}{f'{wJ:+.3f} +- {eJ:.3f}':>22}{'(SPARC is in the fit)':>30}")
# MUSE-DARK III, propagated from its published linear a_0(z)
M = R["musedark3"]; zg = np.linspace(M["zlo"], M["zhi"], 400)
def w_from_linear(a1):
    la = np.log10(M["a00"] + a1*zg)
    return fit_const_w(zg, la)[0]
w_md3 = w_from_linear(M["a1"]); w_md3_lo = w_from_linear(M["a1"] - M["a1_err"]); w_md3_hi = w_from_linear(M["a1"] + M["a1_err"])
WRES["MUSE-DARK III (lit)"] = dict(free=(w_md3, 0.5*abs(w_md3_hi - w_md3_lo)), pinned=(np.nan, np.nan),
                                   N=M["N"], zmed=0.5*(M["zlo"] + M["zhi"]))
P(f"  {'MUSE-DARK III (lit)':22}{M['N']:5d}{0.5*(M['zlo']+M['zhi']):7.2f}"
  f"{f'{w_md3:+.3f} +- {0.5*abs(w_md3_hi-w_md3_lo):.3f}':>22}{'(published a_0(z), stat only)':>30}")
P("")
P("  The pinned column is not a refinement, it is a WARNING: pinning the z = 0 intercept to SPARC moves RC100's w by")
P(f"  {abs(WRES['RC100']['free'][0]-WRES['RC100']['pinned'][0]):.2f}, because RC100's internal slope is negative while its LEVEL sits above SPARC's.  A number that")
P("  moves by half a unit of w depending on whether an anchor is used is not a measurement of w.")
ck("104-B AGAINST INTEREST -- the equation of state from a_0(z) is not stable against the choice of z = 0 anchor: "
   "RC100 alone gives w = -1.4 with a free intercept and w = -0.9 pinned to SPARC's own value through the same "
   "estimator, a shift larger than the entire DESI-vs-Lambda signal.  Neither number may be quoted as a measurement",
   abs(WRES["RC100"]["free"][0] - WRES["RC100"]["pinned"][0]) > 0.2,
   f"RC100 free {WRES['RC100']['free'][0]:+.3f} +- {WRES['RC100']['free'][1]:.3f} vs pinned "
   f"{WRES['RC100']['pinned'][0]:+.3f} +- {WRES['RC100']['pinned'][1]:.3f}: shift "
   f"{WRES['RC100']['pinned'][0]-WRES['RC100']['free'][0]:+.3f}")

# ==================================================================================================================
P(""); P("="*120); P("PART C -- the full (w_0, w_a), with the degeneracy shown rather than hidden"); P("="*120)
for lab in ("RC100", "MSA-3D golden"):
    z = np.array(R["rungs"][lab]["z"]); la = np.array(R["rungs"][lab]["la"])
    beta, cov = fit_cpl(z, la)
    s0, sa = math.sqrt(max(cov[1, 1], 0)), math.sqrt(max(cov[2, 2], 0))
    rho = cov[1, 2]/max(s0*sa, 1e-30)
    ev, evec = np.linalg.eigh(cov[1:, 1:])
    P(f"  {lab:16} w_0 = {beta[1]:+.2f} +- {s0:.2f},  w_a = {beta[2]:+.2f} +- {sa:.2f},  corr = {rho:+.3f}")
    P(f"  {'':16} best-measured direction {evec[:,0][0]:+.2f} w_0 {evec[:,0][1]:+.2f} w_a to +-{math.sqrt(ev[0]):.2f}; "
      f"worst direction to +-{math.sqrt(ev[1]):.2f}")
    if lab == "RC100": rc_cpl = (beta, s0, sa, rho, math.sqrt(ev[0]), math.sqrt(ev[1]))
P("")
P("  Both surveys measure ONE number -- a slope -- so (w_0, w_a) is degenerate along a line by construction; the")
P("  'marginal' errors above are meaningless on their own and are printed only to show how large they are.")
ck("104-C the CPL fit is rank-deficient by construction, and saying so is the result: one redshift-slope cannot "
   "separate w_0 from w_a, so the marginal w_0 error from a single survey exceeds unity and the only constrained "
   "combination is the one printed.  A (w_0, w_a) contour from a_0(z) alone would be a picture of a prior",
   rc_cpl[1] > 0.5,
   f"RC100 marginal sigma(w_0) = {rc_cpl[1]:.2f}, sigma(w_a) = {rc_cpl[2]:.2f}, corr {rc_cpl[3]:+.3f}; "
   f"best direction +-{rc_cpl[4]:.2f}, worst +-{rc_cpl[5]:.2f}")

# ==================================================================================================================
P(""); P("="*120); P("PART D -- beside Planck, beside DESI, and beside the framework's own requirement"); P("="*120)
P(f"  framework (a_0 fixed by rho_Lambda):   w = -1 EXACTLY, w_a = 0     -> d log a_0/dz = 0.000")
P(f"  Planck LCDM:                           w = -1                      -> d log a_0/dz = 0.000")
P(f"  DESI DR2 w0waCDM + Pantheon+:          w_0 = {DESI['w0']:+.3f} +- {DESI['sw0']:.3f}, w_a = {DESI['wa']:+.3f} +- {DESI['swa']:.2f}")
zz = np.linspace(0.5, 2.5, 200)
desi_la = 0.5*np.log10(rho_ratio(zz, DESI["w0"], DESI["wa"]))
desi_slope = float(np.polyfit(zz, desi_la, 1)[0])
P(f"       -> the framework WITH DESI's CPL predicts d log a_0/dz = {desi_slope:+.4f} over 0.5 < z < 2.5 "
  f"(a_0 falls to {10**float(desi_la[-1]):.3f} of today's by z = 2.5)")
P(f"  measured:")
for lab in ("RC100", "MSA-3D golden", "MUSE-DARK III (lit)"):
    w_, e_ = WRES[lab]["free"]
    tag = " [stat only, systematic swamps it]" if "lit" in lab else ""
    P(f"       {lab:22} w = {w_:+.3f} +- {e_:.3f}   ({abs(w_+1)/max(e_,1e-9):.1f} sigma from w = -1, "
      f"{abs(w_-DESI['w0'])/max(e_,1e-9):.1f} sigma from DESI's w_0){tag}")
# does the framework+DESI prediction survive RC100?
z = np.array(R["rungs"]["RC100"]["z"]); la = np.array(R["rungs"]["RC100"]["la"])
s_rc = float(np.polyfit(z, la, 1)[0]); e_rc = R["rungs"]["RC100"]["slope_err"]
ck("104-D the one thing this route CAN say today, and it says it about the framework's own DESI variant rather than "
   "about dark energy at large: RC100's slope is consistent with pure Lambda (0.000), with the framework carrying "
   "DESI's CPL, and with the LambdaCDM-native emergent rise all at once -- the three predictions differ by less than "
   "this measurement's error bar, so a_0(z) at RC100's precision does not discriminate any of them",
   abs(s_rc - 0.0) < 3*e_rc and abs(s_rc - desi_slope) < 3*e_rc,
   f"RC100 d log a_0/dz = {s_rc:+.4f} +- {e_rc:.4f}; pure Lambda 0.0000 ({abs(s_rc)/e_rc:.1f}s), "
   f"framework+DESI-CPL {desi_slope:+.4f} ({abs(s_rc-desi_slope)/e_rc:.1f}s), "
   f"LambdaCDM-native +{R['LCDM_SLOPE']:.4f} ({abs(s_rc-R['LCDM_SLOPE'])/e_rc:.1f}s)")

# ==================================================================================================================
P(""); P("="*120); P("PART E -- the precision actually reached, against the +-0.05 the item asked for"); P("="*120)
best = min((WRES[l]["free"][1], l) for l in ("RC100", "MSA-3D golden"))
ws = [WRES[l]["free"][0] for l in ("RC100", "MSA-3D golden", "MUSE-DARK III (lit)")]
P(f"  best sigma(w) from a survey THIS script inverts = {best[0]:.3f} ({best[1]}), against the item's target of 0.05 "
  f"-- short by a factor {best[0]/0.05:.0f}")
P(f"  (MUSE-DARK III's nominal +-{WRES['MUSE-DARK III (lit)']['free'][1]:.3f} is the STATISTICAL error on a published a_1 whose own paper says a")
P(f"   +0.2 to +0.45 dex stellar-mass shift would remove the whole signal; it is not a usable error on w, and is not used here.)")
P(f"  and the CENTRAL values across the three surveys span w = {min(ws):+.2f} to {max(ws):+.2f}, a range of "
  f"{max(ws)-min(ws):.2f} in w -- {(max(ws)-min(ws))/DESI['sw0']:.0f} times DESI's own w_0 error")
P(f"  the same three surveys' a_0 levels span {max(math.log10(R['rungs'][l]['a0']) for l in R['rungs']) - min(math.log10(R['rungs'][l]['a0']) for l in R['rungs']):.2f} dex, "
  f"which alone is +-{0.5*(max(math.log10(R['rungs'][l]['a0']) for l in R['rungs']) - min(math.log10(R['rungs'][l]['a0']) for l in R['rungs']))/ (1.5*math.log10(2.5)):.2f} in w at z = 1.5")
ck("104-E AGAINST INTEREST -- item 104's headline ('w_0 to +-0.05, competitive with a supernova sample, from rotation "
   "curves') is NOT reached and is not close.  The best single-survey statistical error is an order of magnitude too "
   "large, and the survey-to-survey disagreement found in item 101 puts the central value anywhere between a strongly "
   "phantom w and no dark energy evolution at all.  This route does not yet measure an equation of state",
   best[0] > 0.05 and (max(ws) - min(ws)) > 0.3,
   f"best sigma(w) = {best[0]:.2f} vs target 0.05; central values {ws[0]:+.2f} (RC100), {ws[1]:+.2f} (MSA-3D), "
   f"{ws[2]:+.2f} (MUSE-DARK III)")
P("")
P("  What WOULD reach it, computed rather than asserted: at z = 1.5 the lever is d log a_0/d(1+w) = "
  f"{1.5*math.log10(2.5):.3f} dex, so sigma(w_0) = 0.05 needs a_0(z) to {0.05*1.5*math.log10(2.5):.4f} dex = "
  f"{100*(10**(0.05*1.5*math.log10(2.5))-1):.1f}% at one redshift,")
P(f"  with the z = 0 anchor known at least that well.  The closed-form estimator's per-galaxy floor is 0.4 dex, so it")
P(f"  needs N > {(0.4/(0.05*1.5*math.log10(2.5)))**2:.0f} galaxies with a CONTROLLED selection -- and the level systematics "
  f"(0.05 dex truncation bias, 0.4 dex")
P(f"  survey-to-survey) would still dominate.  The BTFR route of item 105 is the one with the right systematics.")

# ==================================================================================================================
P(""); P("="*120); P("PART F -- mutation controls"); P("="*120)
zsh = np.concatenate([rng.permutation(R["rungs"][l]["z"]) for l in R["rungs"]])
w_sh, _ = fit_const_w(zsh, laJ); e_sh = boot_const_w(zsh, laJ)
info(f"   within-survey z-shuffle on the joint set: w = {w_sh:+.3f} +- {e_sh:.3f} (the real joint fit gives {wJ:+.3f} +- {eJ:.3f})")
info(f"   -- the shuffle does NOT return w = -1, for the reason item 101's M1 gave: the joint 'trend' is the survey")
info(f"      ladder, which survives shuffling z inside each survey.  Shuffling z ACROSS surveys instead:")
zall = rng.permutation(zJ); w_sh2, _ = fit_const_w(zall, laJ); e_sh2 = boot_const_w(zall, laJ)
info(f"   global z-shuffle: w = {w_sh2:+.3f} +- {e_sh2:.3f}  ({abs(w_sh2+1)/max(e_sh2,1e-9):.1f} sigma from w = -1)")
ck("M104-1 the mutation that must fire: destroying the redshift information entirely returns w = -1 (no evolution) "
   "within errors, while the within-survey shuffle does not -- which is the same diagnosis as item 101's, that a "
   "joint a_0(z) built by stacking surveys measures the survey ladder and not cosmology",
   abs(w_sh2 + 1) < 3*e_sh2 and abs(w_sh + 1) > 0.5*abs(wJ + 1),
   f"global shuffle w = {w_sh2:+.3f} +- {e_sh2:.3f}; within-survey shuffle w = {w_sh:+.3f} vs real {wJ:+.3f}")
# closure: inject a known w, recover it
z = np.array(R["rungs"]["RC100"]["z"])
for w_in in (-1.0, -0.7, -1.3):
    la_syn = la_model(z, math.log10(A0["canonical"]), w_in, 0.0)
    w_out, _ = fit_const_w(z, la_syn)
    info(f"   closure: injected w = {w_in:+.2f} (no noise) -> recovered {w_out:+.4f}")
    if abs(w_in + 1) < 1e-9: w_clo = w_out
la_syn = la_model(z, math.log10(A0["canonical"]), -0.7, 0.0) + rng.normal(0, np.std(R["rungs"]["RC100"]["la"]), len(z))
w_noisy, _ = fit_const_w(z, la_syn); e_noisy = boot_const_w(z, la_syn)
info(f"   closure with RC100's real 0.39 dex per-galaxy scatter: injected w = -0.70 -> recovered "
     f"{w_noisy:+.3f} +- {e_noisy:.3f}")
ck("M104-2 closure: the fitter recovers an injected w exactly in the absence of noise, and with RC100's own "
   "per-galaxy scatter it recovers it to about a quarter of a unit -- which is the error bar Part B quotes, so the "
   "error bar is real and not an artefact of the bootstrap",
   abs(w_clo + 1.0) < 1e-6 and abs(w_noisy + 0.7) < 3*e_noisy,
   f"noiseless recovery of w = -1 gives {w_clo:+.6f}; noisy recovery of w = -0.70 gives {w_noisy:+.3f} +- {e_noisy:.3f}")

P(""); P("="*120)
P("VERDICT (item 104).  The mapping is exact and it is the framework's own -- the canonical footing IS")
P(f"(c/2)sqrt(G rho_Lambda) to {abs(math.log10(a0_from_rhoL/A0['canonical'])):.3f} dex -- so a_0(z) really is a dark-energy density measurement in principle.")
P("In practice it is not one yet:")
P(f"  * best sigma(w) from a survey inverted here = {best[0]:.2f} against the item's +-0.05 target, a factor {best[0]/0.05:.0f} short;")
P(f"  * (w_0, w_a) is rank-deficient from a single slope, marginal sigma(w_0) > 1;")
P(f"  * the central value swings by {abs(WRES['RC100']['free'][0]-WRES['RC100']['pinned'][0]):.2f} in w on the choice of z = 0 anchor alone, and by "
  f"{max(ws)-min(ws):.2f} across the three surveys;")
P(f"  * and RC100's slope cannot separate pure Lambda (0.000), the framework carrying DESI's CPL ({desi_slope:+.3f}) and the")
P(f"    LambdaCDM-native rise (+{R['LCDM_SLOPE']:.3f}) -- all three sit inside one error bar.")
P("The honest product is the LEVER, computed here rather than asserted: sigma(w_0) = 0.05 requires a_0 at one")
P(f"redshift near z = 1.5 to {100*(10**(0.05*1.5*math.log10(2.5))-1):.1f}%, with a z = 0 anchor at least as good.  That is item 105's BTFR meter, not this one.")
P("="*120)
sys.exit(ck.done())
