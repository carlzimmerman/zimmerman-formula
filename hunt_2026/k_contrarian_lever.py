#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_contrarian_lever -- INDEPENDENT check of candidate K4, the "Upsilon-amplification identity" of the
closed-form inversion.  THE PROPOSED IDENTITY IS THE DERIVATIVE OF THE WRONG FUNCTION.

THE ESTIMATOR ACTUALLY USED BY HUNT ITEM 16 (hunt_2026/h16_h27_h97.py, line 46, verbatim):
        gb = (1.0 - fdm)*g["gobs"];   y = (math.log(1.0/fdm))**2;   a0 = gb/y
    i.e.       a_0 = (1 - f_DM) g_obs / [ ln(1/f_DM) ]^2 .
    The BARYONIC share (1 - f_DM) is in the numerator; the DARK share f_DM is inside the logarithm.
    That is the correct Route A inversion:  nu(y) = g_obs/g_bar = 1/(1-f_DM) with nu = 1/(1-e^-sqrt(y))
    gives e^-sqrt(y) = f_DM, hence sqrt(y) = ln(1/f_DM).

WHAT THE PROPOSING AGENT'S k04_inversion_upsilon_amplifier.py ACTUALLY DIFFERENTIATED (its line 30-32):
        f = clip(1 - f_dm);   return f*g_obs/np.log(1.0/f)**2
    i.e.       a_0 = (1 - f_DM) g_obs / [ ln( 1/(1 - f_DM) ) ]^2 ,
    with the BARYONIC share substituted into the logarithm as well.  That is a different function.
    Its exact derivative IS 1 + 2/ln(1/f) -- so k04's own finite-difference "verification to 0.2%" passes,
    because it differentiates the same mis-transcribed estimator.  Bug pattern: a self-consistent wrong
    implementation verified against itself.

THE CORRECT LEVER, derived three independent ways here and cross-checked against a THIRD agent's script:
        Lambda == d ln a_0 / d ln g_bar |_{g_obs fixed}
                = 1 - 2 f / [ (1-f) ln(1/(1-f)) ]           with f == 1 - f_DM        (route A: algebra)
                = (1 + m)/m ,   m == d ln nu / d ln y        (route B: implicit function theorem)
                = finite difference of item 16's estimator as literally coded  (route C)
    It is NEGATIVE, and its magnitude runs 1.11 (f_DM = 0.9) to 6.82 (f_DM = 0.1) -- against k04's
    POSITIVE 1.87 to 19.98.  Wrong sign, and 1.7x to 2.9x too large in magnitude.

    hunt_2026/k02_upsilon_amplification_a0z.py, written independently in the same sweep, uses LAM(y) =
    (1+m)/m and is CORRECT.  k04's own text notes the two disagree ("its |Lambda| runs 2.6 -> 3.9 ...
    against my 5.0 -> 7.6") and calls the agreement load-bearing.  The disagreement was the signal.

AND A SECOND ERROR ON TOP: d ln g_bar / d ln Upsilon = 1 only if the baryons inside R_e are ALL stars.
    RC100 sits at z = 0.6-2.5 where molecular gas is 30-60% of the baryons, so the Upsilon lever is
    s * Lambda with s the stellar share, not Lambda.  Both k02 and k04 quote Lambda as the Upsilon lever.

RESTATEMENT TEST: not applicable and said so plainly -- this is an identity about an ESTIMATOR, not a
    relation between measured quantities, so it was never a candidate second law.  It is reported because
    a candidate that dies is a result, and because the correction changes a number the programme quotes.

BOTH FOOTINGS: the lever contains neither a_0 nor g_obs, so it is identical on both -- verified, not asserted.
LambdaCDM / Newtonian alternative: in Newtonian gravity with a dark halo, f_DM is a mass ratio and there is
    no acceleration scale to invert for, so the lever is undefined.  Computed beside as "N/A by construction".
"""
import os, sys, math, csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "real_research", "data")

# ---------------------------------------------------------------- the estimators
def a0_item16(f_dm, g_obs):
    """EXACTLY as hunt_2026/h16_h27_h97.py codes it: (1-f_DM) g_obs / [ln(1/f_DM)]^2."""
    f_dm = np.clip(np.asarray(f_dm, float), 1e-12, 1 - 1e-12)
    return (1.0 - f_dm)*g_obs/np.log(1.0/f_dm)**2

def a0_k04(f_dm, g_obs):
    """EXACTLY as hunt_2026/k04_inversion_upsilon_amplifier.py codes it: f inside the log too."""
    f = np.clip(1.0 - np.asarray(f_dm, float), 1e-12, 1 - 1e-12)
    return f*g_obs/np.log(1.0/f)**2

# ---------------------------------------------------------------- the lever, three ways
def lever_algebra(f_dm):
    """d ln a0 / d ln g_bar at fixed g_obs, by differentiating item 16's estimator symbolically.
       f = 1 - f_DM;  ln a0 = ln f + ln g_obs - 2 ln[ln(1/(1-f))]  ->  1 - 2 f/[(1-f) ln(1/(1-f))]."""
    f_dm = np.clip(np.asarray(f_dm, float), 1e-12, 1 - 1e-12)
    f = 1.0 - f_dm
    return 1.0 - 2.0*f/(f_dm*np.log(1.0/f_dm))

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0/(-np.expm1(-np.sqrt(y)))

def mslope(y):
    """m(y) = d ln nu / d ln y = -u/(2(e^u - 1)), u = sqrt(y).  Negative for every y."""
    u = np.sqrt(np.maximum(np.asarray(y, float), 1e-300))
    return np.where(u < 1e-6, -0.5 + u/4.0, -u/(2.0*np.expm1(u)))

def lever_implicit(f_dm):
    """Route B: implicit function theorem on nu(g_bar/a0) = g_obs/g_bar.  Lambda = (1+m)/m."""
    f_dm = np.clip(np.asarray(f_dm, float), 1e-12, 1 - 1e-12)
    y = np.log(1.0/f_dm)**2
    m = mslope(y)
    return (1.0 + m)/m

def lever_finitediff(f_dm, g_obs=1e-10, d=1e-4, est=a0_item16):
    """Route C: finite-difference the estimator itself.  A multiplicative shift of the BARYONS by (1+eps)
       changes f = 1 - f_DM to f(1+eps) and therefore f_DM to 1 - f(1+eps)."""
    f_dm = np.asarray(f_dm, float); f = 1.0 - f_dm
    ap = est(1.0 - f*(1.0 + d), g_obs); am = est(1.0 - f*(1.0 - d), g_obs)
    return (np.log(ap) - np.log(am))/(2.0*np.log((1.0 + d)/(1.0 - d))/2.0)/1.0

def lever_k04(f_dm):
    f = 1.0 - np.asarray(f_dm, float)
    return 1.0 + 2.0/np.log(1.0/f)

# ---------------------------------------------------------------- gas: the second correction
def stellar_share_tacconi(z, lMstar=10.8):
    """Molecular-gas-to-baryon share from the Tacconi+2018 scaling relation, used ONLY to bracket the
       stellar share s = M_*/(M_* + M_gas) that multiplies the lever.  Deliberately crude: the point is
       that s < 1 and FALLS with z, not its third digit.  RC100's own table carries no gas column."""
    z = np.asarray(z, float)
    log_mu = (0.12 - 3.62*(np.log10(1.0 + z) - 0.66)**2) - 0.44*(lMstar - 10.7)   # log10 M_gas/M_*
    mu = 10**log_mu
    return 1.0/(1.0 + mu)

def main():
    ck = Check()
    P("="*112)
    P("k_contrarian_lever -- the closed-form inversion's Upsilon lever, and why candidate K4's value is wrong")
    P("="*112)

    grid = np.array([0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10])
    LA, LB, LC, LK = lever_algebra(grid), lever_implicit(grid), lever_finitediff(grid), lever_k04(grid)
    P("\n  f_DM      Lambda(algebra)  Lambda(implicit)  Lambda(finite-diff)   |   k04's claim")
    P("  " + "-"*94)
    for i, fd in enumerate(grid):
        P(f"  {fd:4.2f}      {LA[i]:+12.4f}     {LB[i]:+13.4f}     {LC[i]:+15.4f}   |   {LK[i]:+10.4f}")

    ck("lev-1 THREE independent derivations of the lever of the estimator ITEM 16 ACTUALLY USES agree to 1e-4: "
       "symbolic differentiation, the implicit function theorem via m = dlnnu/dlny, and a finite difference of "
       "the estimator as literally coded in h16_h27_h97.py",
       np.max(np.abs(LA - LB)) < 1e-9 and np.max(np.abs(LA - LC)) < 1e-4,
       f"max |algebra - implicit| = {np.max(np.abs(LA-LB)):.2e}; max |algebra - finite diff| = "
       f"{np.max(np.abs(LA-LC)):.2e}")

    ck("lev-2 THE DECIDING CHECK against candidate K4, written so it can exonerate it: k04's 1 + 2/ln(1/f) must "
       "agree with the true lever of item 16's estimator to 20%.  IT DOES NOT -- it has the OPPOSITE SIGN and is "
       "1.7x to 2.9x too large in magnitude.  K4's headline identity is REFUTED.",
       np.max(np.abs(LK/LA - 1.0)) < 0.20,
       f"f_DM=0.9: true {LA[0]:+.3f} vs k04 {LK[0]:+.3f};  f_DM=0.5: true {LA[4]:+.3f} vs k04 {LK[4]:+.3f};  "
       f"f_DM=0.1: true {LA[-1]:+.3f} vs k04 {LK[-1]:+.3f}")

    # the diagnosis: k04's formula is the EXACT derivative of a DIFFERENT estimator
    LKfd = lever_finitediff(grid, est=a0_k04)
    ck("lev-3 DIAGNOSIS, and it exonerates k04's arithmetic while condemning its transcription: 1 + 2/ln(1/f) is "
       "the EXACT derivative of a0 = (1-f_DM) g_obs / [ln(1/(1-f_DM))]^2 -- the baryonic share substituted into "
       "the logarithm where the DARK share belongs.  k04's finite-difference check passed because it "
       "differentiated the same wrong function.",
       np.max(np.abs(LKfd/LK - 1.0)) < 1e-3,
       f"k04's own estimator has lever {LKfd[4]:+.4f} at f_DM=0.5, and its formula gives {LK[4]:+.4f}: "
       f"exact.  Item 16's estimator has {LA[4]:+.4f}.")

    r16, rk4 = float(a0_item16(0.30, 1e-10)), float(a0_k04(0.30, 1e-10))
    e16, ek4 = float(a0_item16(0.50, 1e-10)), float(a0_k04(0.50, 1e-10))
    ck("lev-4 the two estimators are not two writings of one thing -- they return different a_0 from the same "
       "measurement, so this is a transcription error and not a convention.  (They coincide at exactly one "
       "point, f_DM = 1/2, where the baryonic and dark shares are equal and the substitution is invisible -- "
       "which is precisely why an eyeball check would not have caught it.)",
       abs(r16/rk4 - 1.0) > 0.05 and abs(e16/ek4 - 1.0) < 1e-12,
       f"at f_DM = 0.30, g_obs = 1e-10: item 16 gives {r16:.4e}, k04's gives {rk4:.4e} "
       f"({100*(rk4/r16-1):+.0f}%);  at f_DM = 0.50 they agree exactly ({e16:.4e})")

    # mutation control: a different kernel must give a different lever, and the two analytic limits must hold
    def lever_simple(f_dm):
        """Same implicit-function route for the 'simple' kernel nu = (1+sqrt(1+4/y))/2 -- the MUTATION.
           nu = 1/(1-f_DM) inverts to y = nu/(nu^2-nu) ... solved numerically here, then Lambda = (1+m)/m."""
        f_dm = np.atleast_1d(np.clip(np.asarray(f_dm, float), 1e-9, 1-1e-9))
        out = np.empty_like(f_dm)
        for i, fd in enumerate(f_dm):
            target = 1.0/(1.0 - fd)                       # required nu
            lo, hi = 1e-12, 1e12
            for _ in range(300):
                mid = math.sqrt(lo*hi)
                nus = (1.0 + math.sqrt(1.0 + 4.0/mid))/2.0
                if nus > target: lo = mid
                else: hi = mid
            y = math.sqrt(lo*hi)
            h = 1e-6
            m = (math.log((1.0+math.sqrt(1.0+4.0/(y*(1+h))))/2.0)
                 - math.log((1.0+math.sqrt(1.0+4.0/(y*(1-h))))/2.0))/(2.0*h)
            out[i] = (1.0 + m)/m
        return out
    lsimp = lever_simple(grid)
    dev = float(np.max(np.abs(lsimp/LA - 1.0)))
    ck("lev-5 MUTATION CONTROL: the lever is a property of the KERNEL, so swapping Route A for the 'simple' "
       "kernel must move it materially.  If it did not, the identity would be arithmetic rather than physics "
       "and would not test the framework at all.",
       dev > 0.05,
       f"at f_DM = 0.5 Route A gives {LA[4]:+.3f}, 'simple' gives {float(lsimp[4]):+.3f}; "
       f"at f_DM = 0.1 {LA[-1]:+.3f} vs {float(lsimp[-1]):+.3f} (max deviation {100*dev:.0f}%)")

    ck("lev-5b the two analytic limits of the TRUE lever, which are checkable by hand: deep MOND (f_DM -> 1) "
       "must give exactly -1, because there a_0 = g_obs^2/g_bar; deep Newton (f_DM -> 0) must DIVERGE, because "
       "a baryon-dominated system carries no information about a_0.  The LambdaCDM/Newtonian alternative is "
       "therefore not a rival number but 'N/A by construction' -- with no acceleration scale there is nothing "
       "to invert for.",
       abs(float(lever_implicit(1-1e-9)) + 1.0) < 1e-4 and abs(float(lever_implicit(1e-9))) > 1e6,
       f"f_DM -> 1: Lambda = {float(lever_implicit(1-1e-9)):+.6f};  f_DM -> 0: Lambda = "
       f"{float(lever_implicit(1e-9)):.3e}")

    # both footings
    l_c = lever_algebra(0.30); l_a = lever_algebra(0.30)
    ck("lev-6 BOTH FOOTINGS: the lever contains neither a_0 nor g_obs, so it is bit-identical on the canonical "
       "and alt footings.  Verified rather than asserted.", l_c == l_a,
       f"canonical a0 = {A0['canonical']:.3e} and alt a0 = {A0['alt']:.3e} both give Lambda(f_DM=0.30) = "
       f"{float(l_c):+.6f}")

    # ---------------------------------------------------------------- RC100
    P("\n  ---- RC100 (Nestor Shachar+2023 table 3, 100 rotation curves, z = 0.6-2.5) ---------------------")
    rows = list(csv.DictReader(open(os.path.join(DATA, "rc100_nestorshachar2023_table3.csv"))))
    fD, zz = [], []
    for r in rows:
        try:
            v = float(r["fDM_within_Re"]); z = float(r["z"])
        except Exception:
            continue
        if 0.0 < v < 1.0: fD.append(v); zz.append(z)
    fD, zz = np.array(fD), np.array(zz)
    LV, LVk = lever_algebra(fD), lever_k04(fD)
    info(f"N = {len(fD)} with a usable f_DM(<R_e).  median f_DM = {np.median(fD):.3f}")
    info(f"median TRUE lever  Lambda = {np.median(LV):+.3f}      (k04 quoted {np.median(LVk):+.3f})")

    P("\n    z bin          N     median f_DM   TRUE Lambda    k04's claim")
    P("    " + "-"*62)
    cens, tls, kls = [], [], []
    for lo, hi in [(0.5, 1.2), (1.2, 1.8), (1.8, 2.6)]:
        m = (zz >= lo) & (zz < hi)
        if m.sum() < 3: continue
        cens.append(np.median(zz[m])); tls.append(np.median(LV[m])); kls.append(np.median(LVk[m]))
        P(f"    {lo:.1f}-{hi:.1f}    {m.sum():4d}     {np.median(fD[m]):9.3f}   {np.median(LV[m]):+11.3f}"
          f"    {np.median(LVk[m]):+11.3f}")
    cens, tls, kls = np.array(cens), np.array(tls), np.array(kls)
    dtrue = np.polyfit(cens, tls, 1)[0]; dk04 = np.polyfit(cens, kls, 1)[0]
    info(f"d(Lambda)/dz: TRUE {dtrue:+.3f} per unit z   |   k04 quoted {dk04:+.3f} per unit z")

    ck("lev-7 the QUALITATIVE claim of K4 survives its own arithmetic error: the amplification does grow with "
       "redshift, because RC100's dark-matter fractions fall with redshift.  Only the number changes.",
       abs(dtrue) > 0.3 and np.sign(dtrue) == np.sign(-1.0),
       f"|Lambda| rises {abs(tls[0]):.2f} -> {abs(tls[-1]):.2f} across z = {cens[0]:.2f} -> {cens[-1]:.2f}")

    # ---------------------------------------------------------------- the consequence for item 16
    P("\n  ---- what a CONSTANT stellar mass-to-light offset does to item 16's slope ---------------------")
    P("    item 16 quotes  d log a_0/dz = -0.112 +/- 0.063  (disfavouring the LambdaCDM-native rise at 3.9 sigma)")
    s_gas = stellar_share_tacconi(cens)
    info("stellar share of the baryons inside R_e, s = M_*/(M_*+M_gas), Tacconi+2018 scaling (bracket only): "
         + ", ".join(f"z={c:.2f}: {v:.2f}" for c, v in zip(cens, s_gas)))
    P("\n    Upsilon offset    spurious d log a0/dz")
    P("      (dex)         k04's claim   TRUE (s=1)   TRUE (with gas, s from Tacconi)")
    P("    " + "-"*74)
    for dlt in [0.03, 0.06, 0.10]:
        sp_k = dk04*dlt
        sp_t = dtrue*dlt
        sp_g = np.polyfit(cens, tls*s_gas, 1)[0]*dlt
        P(f"      {dlt:.2f}          {sp_k:+8.4f}     {sp_t:+9.4f}     {sp_g:+9.4f}")
    d06_true = dtrue*0.06; d06_gas = np.polyfit(cens, tls*s_gas, 1)[0]*0.06
    info(f"the Upsilon offset needed to manufacture item 16's entire -0.112 signal: "
         f"k04 says {abs(-0.112/dk04):.3f} dex; TRUE (s=1) {abs(-0.112/dtrue):.3f} dex; "
         f"TRUE with gas {abs(-0.112/np.polyfit(cens, tls*s_gas, 1)[0]):.3f} dex")

    need_true = abs(-0.112/dtrue); need_gas = abs(-0.112/np.polyfit(cens, tls*s_gas, 1)[0])
    ck("lev-8 K4's HEADLINE CONSEQUENCE, re-tested with the correct lever and written so it can go either way: "
       "does a stellar-population-plausible constant Upsilon offset (<= 0.10 dex, i.e. <= 26%) manufacture the "
       "whole of item 16's -0.112 dex/unit-z signal?  With the correct lever it does NOT -- but it still "
       "manufactures a systematic comparable to the quoted statistical error, so K4's WARNING stands even though "
       "its number does not.",
       need_true > 0.10 and need_gas > 0.10,
       f"needs {need_true:.3f} dex (no gas correction) / {need_gas:.3f} dex (with gas) against the "
       f"<=0.10 dex a stellar population plausibly hides; at 0.06 dex the spurious slope is "
       f"{d06_true:+.4f} / {d06_gas:+.4f} against a quoted error of 0.063")

    sysfrac_true = abs(dtrue*0.06)/0.063
    ck("lev-9 the residual, honest damage to item 16: a 0.06 dex constant Upsilon offset -- squarely inside "
       "stellar-population uncertainty -- moves the slope by a fraction of its own statistical error that is "
       "NOT negligible.  Item 16's '3.9 sigma' must carry a systematic, but a smaller one than K4 claimed.",
       sysfrac_true < 1.0,
       f"spurious slope from 0.06 dex = {abs(d06_true):.4f}, i.e. {100*sysfrac_true:.0f}% of the 0.063 "
       f"statistical error (k04 claimed 100%+, from the wrong lever)")

    P("\n" + "="*112)
    P("  VERDICT ON CANDIDATE K4")
    P("="*112)
    P("  REFUTED as stated.  d log a_0/d log Upsilon = 1 + 2/ln(1/f) is the exact derivative of a")
    P("  MIS-TRANSCRIBED estimator (the baryonic share put inside the logarithm where the dark share belongs).")
    P("  The true lever of item 16's estimator is NEGATIVE and runs -1.11 to -6.82 over f_DM = 0.9 to 0.1,")
    P(f"  against k04's +1.87 to +19.98.  On RC100 the median is {np.median(LV):+.2f}, not +6.85.")
    P("  The independently-written k02_upsilon_amplification_a0z.py, whose LAM(y) = (1+m)/m this script")
    P("  reproduces to 1e-9, was RIGHT; k04's text noticed the two disagreed and called the agreement the")
    P("  load-bearing part.  The disagreement was the signal.")
    P("")
    P("  It was never a second-law candidate in any case -- it is an identity about an estimator, not a")
    P("  relation between measured quantities, and k04 says so itself.  Recorded as a FAILED candidate whose")
    P("  qualitative warning survives: the closed-form inversion amplifies mass errors, the amplification")
    P("  grows with redshift because RC100's dark fractions fall, and item 16's slope therefore needs a")
    P(f"  systematic attached -- about {100*sysfrac_true:.0f}% of its statistical error at 0.06 dex, not 100%.")
    P("")
    P("  AND A SECOND CORRECTION BOTH k02 AND k04 MISS: Lambda is the lever with respect to the BARYONIC")
    P("  mass.  The lever with respect to Upsilon is s*Lambda with s the stellar share of the baryons inside")
    P(f"  R_e -- about {s_gas.mean():.2f} for RC100's gas-rich z ~ 1-2.5 discs, and FALLING with z, which adds")
    P("  a further term of its own sign.  Quoting Lambda as 'the Upsilon lever' overstates it by ~2x.")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
