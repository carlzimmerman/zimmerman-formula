#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fbD4 -- THE DISTINCTIVE, TESTABLE PREDICTION: a0(z), the deep-MOND BTFR zero point, and MUSE.
=============================================================================================
TASK 4.  Independent recomputation of the repository's registered a0(z) test numbers, and an
honest confrontation with the one measurement that already disagrees.

WHAT IS RE-DERIVED FROM SCRATCH (nothing taken on report):
  1  a0(z)/a0(0) for every law, over the OBSERVABLE range z = 0-3.5.
  2  the LCDM-NATIVE rival law a_s(z)/a_s(0) = E(z)^(4/3) [c^2/f(c)](z)/[c^2/f(c)](0), f(c) =
     ln(1+c) - c/(1+c), with Dutton-Maccio 2014 concentrations -- i.e. what a halo population
     predicts for the emergent RAR scale with NO fundamental a0.  Target: +0.33 dex at z = 2.5.
  3  the required measurement precision for 20:1 odds, from the two-hypothesis Gaussian Bayes
     factor.  Target: 0.134 dex.  And its decomposition into velocity and baryonic-mass budgets.
  4  the MUSE-DARK III confrontation (Ciocan et al., 79 SFGs, 0.33 < z < 1.44,
     a0(z) = a0(0) + a1 z with a0(0) = 1.00 +- 0.04, a1 = +1.59 +- 0.105 in 1e-10 m/s^2 per z):
     the significance against BRANCH A (flat) AND against BRANCH B (a0 propto H), before and after
     folding the LCDM halo-assembly drift, with the double-counting hazard stated.
  5  the framework's OWN prediction is a BAND, not 0.00, once DESI-CPL dark energy is allowed.

POLARITY.  This lane is written to be able to report a FALSIFICATION.  If MUSE's rise survives, the
flat law is dead, and that is said in those words.  It is equally written not to manufacture one:
the drift folding that softens it is applied and reported, and so is the reason it may be circular.
Both a0 footings.  Checks CAN fail.
"""
import math, sys, time
import numpy as np
from scipy.integrate import quad

T0 = time.time(); FAILS = []; NC = [0]
def check(name, ok, detail=""):
    NC[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)
def info(s): print("  " + s, flush=True)

h = 0.6736; Om = 0.3153; Or = 9.164e-5; OL = 1 - Om - Or
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4
def E(z): zp = 1 + z; return math.sqrt(Or * zp**4 + Om * zp**3 + OL)
print("=" * 118); print("fbD4 -- a0(z): the prediction, the decisive measurement, and the measurement that disagrees")
print("=" * 118, flush=True)

# ==================================================================================================
sec("PART 1 -- a0(z) over the OBSERVABLE range, every law, both footings")
# ==================================================================================================
def a0r_flat(z): return 1.0
def a0r_stage17(z, nu0=NU0_FLOOR):
    nu = nu0 * (1 + z)**3
    return (math.sqrt(1 + nu0**2) / math.sqrt(1 + nu**2)) ** 0.5
CPL = {"w=-1 (pure Lambda)": (-1.0, 0.0), "DESI DR2 BAO+CMB+SN": (-0.702, -0.72),
       "DESI DR2 BAO+CMB+DESY5": (-0.752, -0.86), "DESI DR1 +PantheonPlus": (-0.827, -0.75)}
def a0r_cpl(z, w0, wa):
    a = 1 / (1 + z)
    return math.sqrt(a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a)))
def a0r_B(z): return E(z)
ZT = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
print(f"    {'law':34s}" + "".join(f"{('z='+str(z)):>9s}" for z in ZT) + "   |  dex at z=2.5")
rows = [("BRANCH A0  a0 locked to Lambda", [a0r_flat(z) for z in ZT])]
for nm, (w0, wa) in CPL.items():
    rows.append((f"BRANCH A1  CPL {nm}"[:34], [a0r_cpl(z, w0, wa) for z in ZT]))
rows.append(("BRANCH A2  stage-17 (floor)", [a0r_stage17(z, NU0_FLOOR) for z in ZT]))
rows.append(("BRANCH A2  stage-17 (ceiling)", [a0r_stage17(z, NU0_CEIL) for z in ZT]))
rows.append(("BRANCH B   a0 propto H(z)", [a0r_B(z) for z in ZT]))
for nm, vals in rows:
    print(f"    {nm:34s}" + "".join(f"{v:9.4f}" for v in vals) + f"   |  {math.log10(vals[5]):+.3f}")
check("D1-a  BRANCH A is FLAT to better than 0.1%% over the entire observable range z <= 3.5 on the locked and "
      "stage-17 laws: |dex| <= %.5f.  That flatness IS the distinctive prediction -- not a rise"
      % max(abs(math.log10(a0r_stage17(z, NU0_CEIL))) for z in ZT),
      max(abs(math.log10(a0r_stage17(z, NU0_CEIL))) for z in ZT) < 1e-3,
      f"max |log10 a0(z)/a0(0)| over z<=3.5 = {max(abs(math.log10(a0r_stage17(z,NU0_CEIL))) for z in ZT):.2e} dex")
cpl_dex = [math.log10(a0r_cpl(2.5, w0, wa)) for (w0, wa) in CPL.values() if (w0, wa) != (-1.0, 0.0)]
check("D1-b  ...but the framework's OWN prediction at z = 2.5 is a BAND, not the single value 0.00, once DESI "
      "evolving dark energy is allowed: %.3f to %.3f dex.  Quoting '0.00 dex' as THE prediction understates "
      "the framework's own spread and would let a genuine confirmation be scored as a refutation"
      % (min(cpl_dex), max(cpl_dex)),
      min(cpl_dex) < -0.02, f"CPL band at z = 2.5: {min(cpl_dex):+.3f} to {max(cpl_dex):+.3f} dex (w=-1 gives 0.000)")
check("D1-c  BRANCH B predicts a LARGE rise, +%.3f dex at z = 2.5, and is separated from branch A by that "
      "amount -- the two branches are trivially distinguishable by any deep-MOND measurement at z ~ 2-3"
      % math.log10(a0r_B(2.5)),
      math.log10(a0r_B(2.5)) > 0.5, f"branch B at z = 2.5: {math.log10(a0r_B(2.5)):+.3f} dex (a factor {a0r_B(2.5):.2f})")

# ==================================================================================================
sec("PART 2 -- the LCDM-NATIVE rival: what a halo population predicts with NO fundamental a0")
# ==================================================================================================
def c_DM14(M, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z**1.21)
    b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M * h / 1e12))
def c_D08(M, z): return 5.71 * (M * h / 2e12) ** (-0.084) * (1 + z) ** (-0.47)
def f_nfw(cc): return math.log(1 + cc) - cc / (1 + cc)
def a_s_ratio(z, M=1e12, cfun=c_DM14):
    num = E(z) ** (4. / 3.) * (cfun(M, z) ** 2 / f_nfw(cfun(M, z)))
    den = 1.0 * (cfun(M, 0.0) ** 2 / f_nfw(cfun(M, 0.0)))
    return num / den
print(f"    {'z':>5s} | {'c_DM14':>8s} {'c^2/f':>9s} {'E^(4/3)':>9s} | {'a_s/a_s(0) DM14':>16s} {'dex':>8s} | "
      f"{'DM14 vs branch A':>17s}")
for z in (0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
    cc = c_DM14(1e12, z); r = a_s_ratio(z)
    print(f"    {z:5.1f} | {cc:8.3f} {cc**2/f_nfw(cc):9.3f} {E(z)**(4./3.):9.3f} | {r:16.4f} {math.log10(r):+8.3f} | "
          f"{math.log10(r):+17.3f}")
dex25 = math.log10(a_s_ratio(2.5))
dex25_d08 = math.log10(a_s_ratio(2.5, cfun=c_D08))
check("D2-a  REGRESSION on the repository's registered number: the LCDM-native rise at z = 2.5 with "
      "Dutton-Maccio 2014 concentrations is %+.3f dex, reproducing the committed +0.33 to 2%%.  Derived here "
      "from the concentration relation and NFW f(c), not copied" % dex25,
      abs(dex25 - 0.33) < 0.02, f"DM14 {dex25:+.4f} dex (committed +0.33); Duffy 2008 {dex25_d08:+.4f} (committed +0.45)")
check("D2-b  the LCDM-native law is the CONSERVATIVE rival: Duffy 2008 gives %+.3f dex, so using DM14's %+.3f "
      "understates the separation.  The framework is being tested against the rival that is HARDEST to beat"
      % (dex25_d08, dex25),
      dex25_d08 > dex25, f"DM14 {dex25:+.3f} < D08 {dex25_d08:+.3f}")
sepAB = abs(math.log10(a0r_B(2.5)) - dex25)
check("D2-c  and BRANCH B is NOT the same as the LCDM-native law even though both rise: branch B gives %+.3f "
      "dex and the halo law %+.3f dex, a separation of %.3f dex.  So a measurement at 0.13 dex separates all "
      "THREE hypotheses, not just two" % (math.log10(a0r_B(2.5)), dex25, sepAB),
      sepAB > 0.13, f"branch B {math.log10(a0r_B(2.5)):+.3f}, LCDM-native {dex25:+.3f}, separation {sepAB:.3f} dex")

# ==================================================================================================
sec("PART 3 -- the decisive measurement: what has to be measured, and how well")
# ==================================================================================================
info("The deep-MOND limit of the framework's own a0-line is v^4 = G M_b a0 EXACTLY, so a rotation-dominated")
info("system with g_bar << a0 measures a0 directly:   a0 = v_flat^4 / (G M_b).")
info("Hence  log10 a0 = 4 log10 v_flat - log10 M_b - log10 G,  and the error budget is FORCED:")
info("       sigma(log10 a0)^2 = (4 sigma_log v)^2 + (sigma_log Mb)^2 .")
def sigma_for_odds(delta, log10B=1.30): return delta / math.sqrt(2 * log10B * math.log(10))
sig_need = sigma_for_odds(dex25)
check("D3-a  REGRESSION: separating FLAT (0.00) from LCDM-native (%+.3f) at 20:1 odds (log10 B = 1.30) needs a "
      "TOTAL uncertainty of %.3f dex on ONE deep-MOND point.  This reproduces the repository's registered "
      "0.13 dex from the Gaussian two-hypothesis Bayes factor, derived not copied" % (dex25, sig_need),
      abs(sig_need - 0.134) < 0.01, f"sigma needed = {sig_need:.4f} dex (registered 0.13-0.134)")
print(f"    {'sigma_v/v':>10s} {'4 sigma_logv':>13s} | {'sigma_logMb':>12s} | {'total dex':>10s} | 20:1 at {sig_need:.3f}?")
for sv in (0.03, 0.05, 0.08, 0.10):
    for sM in (0.05, 0.10, 0.15):
        slv = 4 * sv / math.log(10)
        tot = math.sqrt(slv**2 + sM**2)
        print(f"    {sv:10.2f} {slv:13.4f} | {sM:12.2f} | {tot:10.4f} | {'YES' if tot <= sig_need else 'no'}")
ok_budget = math.sqrt((4 * 0.05 / math.log(10))**2 + 0.10**2) <= sig_need * 1.02
check("D3-b  the budget CLOSES, but only just: 5%% rotation velocities and 0.10 dex baryonic mass give %.3f dex, "
      "at the 20:1 threshold.  The BARYONIC MASS, not the velocity, is the binding constraint -- 4x the "
      "velocity error enters, so 5%% on v is already 0.087 dex and leaves almost nothing for M_b"
      % math.sqrt((4 * 0.05 / math.log(10))**2 + 0.10**2),
      ok_budget, f"5% on v + 0.10 dex on M_b = {math.sqrt((4*0.05/math.log(10))**2+0.10**2):.4f} dex vs {sig_need:.3f} needed")
sig_need_band = sigma_for_odds(dex25 - min(cpl_dex))
check("D3-c  ...and if the framework's own DESI-CPL band (%.3f dex low) is honoured rather than the single "
      "0.00, the separation GROWS to %.3f dex and the requirement RELAXES to %.3f dex.  Reported because it "
      "cuts in the framework's favour and should not be quietly omitted"
      % (min(cpl_dex), dex25 - min(cpl_dex), sig_need_band),
      sig_need_band > sig_need, f"separation {dex25-min(cpl_dex):.3f} dex -> sigma needed {sig_need_band:.3f} dex")
info("")
info("THE MEASUREMENT, stated concretely:  ONE strongly lensed, rotation-dominated galaxy at 2.3 < z < 2.9,")
info("selected to have g_bar(R_out) < 0.3 a0 on BOTH footings (so the deep-MOND limit is actually reached);")
info("rotation from JWST/NIRSpec IFU (G235H/F170LP catches Halpha and [OIII] together over 2.32 < z < 3.83);")
info("an INDEPENDENT gas mass from ALMA CO(3-2) in Band 3 (1.98 < z < 3.12) so M_b does not lean on a")
info("star-formation-rate calibration.  Required: dv/v < 5%, d log10 M_b < 0.10 dex.  N = 1 suffices at 20:1;")
info("this is a targeted observation, not a survey.")

# ==================================================================================================
sec("PART 4 -- THE MEASUREMENT THAT DISAGREES: MUSE-DARK III.  Reported honestly, both ways.")
# ==================================================================================================
A1_M, A1_E = 1.59, 0.105          # 1e-10 m/s^2 per unit z, Ciocan et al. (79 SFGs, 0.33 < z < 1.44)
A00_M, A00_E = 1.00, 0.04
ZLO, ZHI = 0.33, 1.44
A1_DRIFT = 0.80                   # Mayer+2023 Magneticum LCDM assembly drift, apparent a0 rise per unit z
info(f"Ciocan et al. fit a0(z) = a0(0) + a1 z over {ZLO} < z < {ZHI}: a0(0) = {A00_M} +- {A00_E}, "
     f"a1 = +{A1_M} +- {A1_E} (units 1e-10 m/s^2 per z).")
info("To compare a LAW with a LINEAR FIT, each law is projected onto the same linear slope over the same")
info("redshift window by least squares -- the only apples-to-apples comparison available without the data.")
def slope_of(fun, zlo=ZLO, zhi=ZHI, n=200):
    zs = np.linspace(zlo, zhi, n); ys = np.array([fun(z) for z in zs])
    A = np.vstack([np.ones_like(zs), zs]).T
    return float(np.linalg.lstsq(A, ys, rcond=None)[0][1])
sl_A = slope_of(lambda z: a0r_stage17(z, NU0_CEIL))
sl_B = slope_of(a0r_B)
sl_cpl = slope_of(lambda z: a0r_cpl(z, *CPL["DESI DR2 BAO+CMB+SN"]))
print(f"    {'hypothesis':38s} {'effective a1':>13s} | {'sigma vs MUSE (raw)':>20s} | {'after drift folding f=0.5':>26s}")
def sig_raw(sl): return abs(A1_M - sl) / A1_E
def sig_drift(sl, f=0.5): return abs(A1_M - (sl + A1_DRIFT)) / math.sqrt(A1_E**2 + (f * A1_DRIFT)**2)
for nm, sl in (("BRANCH A (flat / stage-17)", sl_A), ("BRANCH A1 (DESI CPL, declining)", sl_cpl),
               ("BRANCH B (a0 propto H)", sl_B), ("LCDM-native halo drift alone", A1_DRIFT)):
    print(f"    {nm:38s} {sl:13.3f} | {sig_raw(sl):20.2f} | {sig_drift(sl):26.2f}")
check("D4-a  REGRESSION on the repository's banked MUSE numbers: BRANCH A (flat) is %.1f sigma from the MUSE "
      "slope at face value, and %.2f-%.2f sigma after folding the LCDM assembly drift at f = 0.5-0.3.  "
      "Reproduces the banked 15.1 sigma raw and 1.9-3.0 sigma folded"
      % (sig_raw(sl_A), sig_drift(sl_A, 0.5), sig_drift(sl_A, 0.3)),
      abs(sig_raw(sl_A) - 15.14) < 0.3 and 1.7 < sig_drift(sl_A, 0.5) < 2.2 and 2.8 < sig_drift(sl_A, 0.3) < 3.3,
      f"raw {sig_raw(sl_A):.2f} sigma (banked 15.14); folded f=0.5 {sig_drift(sl_A,0.5):.2f} (banked 1.91), "
      f"f=0.3 {sig_drift(sl_A,0.3):.2f} (banked 3.02)")
check("D4-b  *** AND THE SAME DATUM DISFAVOURS BRANCH B TOO, WHICH THE RECORD DOES NOT STATE. ***  MUSE's rise "
      "is FASTER than H(z): the effective a1 for a0 propto H over the MUSE window is %.2f against the measured "
      "%.2f +- %.3f, i.e. %.1f sigma.  Ciocan et al. say so in words ('faster than that of H(z)'); it is "
      "quantified here.  MUSE is not a datum that rescues the rising branch"
      % (sl_B, A1_M, A1_E, sig_raw(sl_B)),
      sig_raw(sl_B) > 3.0, f"branch B effective a1 = {sl_B:.3f} vs measured {A1_M} +- {A1_E}  ->  {sig_raw(sl_B):.2f} sigma")
check("D4-c  THE DOUBLE-COUNTING HAZARD, stated rather than exploited: the drift folding that softens branch A "
      "from %.1f to %.1f sigma uses an LCDM halo-assembly drift of +%.2f/z -- which is essentially the SAME "
      "physical effect as branch B's own a0 propto H (effective %.2f/z).  Folding it and then also claiming "
      "branch B as a prediction would count one effect twice.  The folded number is therefore a CEILING on the "
      "relief branch A may claim, not a result" % (sig_raw(sl_A), sig_drift(sl_A, 0.5), A1_DRIFT, sl_B),
      abs(A1_DRIFT - sl_B) / sl_B < 0.5,
      f"assembly drift {A1_DRIFT:.2f}/z vs branch B's own {sl_B:.2f}/z -- the same order, so they are not independent")
check("D4-d  THE FALSIFICATION CONDITION, stated in advance and in the framework's own terms: the stage-17 "
      "derived law predicts an effective a1 of %.2e over the MUSE window -- flat to 5 decimal places.  ANY "
      "robust nonzero a1, EITHER SIGN, at >3 sigma after a homogeneous drift-modelled pipeline kills it.  The "
      "present status is %.1f-%.1f sigma depending on how much of the drift is credited: NOT a falsification "
      "today, and the sharpest live threat the framework has"
      % (sl_A, sig_drift(sl_A, 0.5), sig_drift(sl_A, 0.3)),
      abs(sl_A) < 1e-3 and sig_drift(sl_A, 0.3) > 2.5,
      f"predicted a1 = {sl_A:.2e}; measured {A1_M} +- {A1_E}; folded tension {sig_drift(sl_A,0.5):.2f}-{sig_drift(sl_A,0.3):.2f} sigma")

# ==================================================================================================
sec("PART 5 -- both footings, and the one-line summary of what decides it")
# ==================================================================================================
for foot in ("canonical", "alt"):
    info(f"{foot:10s}: a0(0) = {A0[foot]:.4e};  branch A predicts {A0[foot]:.4e} at EVERY z <= 5;  "
         f"branch B predicts {A0[foot]*E(2.5):.4e} at z = 2.5")
check("D5-a  the a0(z) predictions are footing-independent as RATIOS (the footings differ by a constant 20.5%%, "
      "which is a zero-point not a slope), so every dex number above is unchanged by the choice of footing",
      abs(A0["alt"] / A0["canonical"] - 1.2048) < 0.01,
      f"alt/canonical = {A0['alt']/A0['canonical']:.4f} at all z on both branches -> cancels in every ratio")

sec("VERDICT (fbD4)")
print(f"""
  THE PREDICTION.  On the framework's own derivation (branch A) a0 is FLAT: |log10 a0(z)/a0(0)| < 1e-3 dex
  for all z <= 3.5 on both the locked and the stage-17 laws.  That flatness is the distinctive content --
  LCDM's emergent halo scale instead RISES by {dex25:+.3f} dex by z = 2.5 (Dutton-Maccio 2014; {dex25_d08:+.3f} with Duffy
  2008), and branch B rises by {math.log10(a0r_B(2.5)):+.3f} dex.  One measurement separates all three.
  Honesty amendment: once DESI-CPL dark energy is allowed the framework's own z = 2.5 prediction is a BAND,
  {min(cpl_dex):+.3f} to 0.000 dex, not the single value 0.00 that the registered test uses.

  THE SHARPEST TEST.  a0 = v_flat^4/(G M_b) on ONE strongly lensed, rotation-dominated galaxy at 2.3 < z < 2.9
  selected at g_bar < 0.3 a0, with JWST/NIRSpec rotation and an independent ALMA CO gas mass.  Required total
  uncertainty {sig_need:.3f} dex for 20:1 odds ({sig_need_band:.3f} dex if the framework's own CPL band is honoured).  The budget
  closes only just: 5% on v is already {4*0.05/math.log(10):.3f} dex because the velocity enters to the FOURTH power, leaving
  ~0.10 dex for the baryonic mass.  M_b, not kinematics, is the binding constraint.

  THE MEASUREMENT THAT DISAGREES, AND IT IS REAL.  MUSE-DARK III measures a1 = +{A1_M} +- {A1_E}, i.e. a0 RISING.
  Against branch A's predicted {sl_A:.1e} that is {sig_raw(sl_A):.1f} SIGMA at face value.  Folding the LCDM halo-assembly
  drift (+{A1_DRIFT}/z, Magneticum) at 50-70% credit brings it to {sig_drift(sl_A,0.5):.1f}-{sig_drift(sl_A,0.3):.1f} sigma -- but that folding is close to
  circular, because the drift being folded IS branch B's own effect, so {sig_drift(sl_A,0.5):.1f}-{sig_drift(sl_A,0.3):.1f} sigma is a CEILING on the
  relief, not a resolution.  Status: NOT a falsification today, and the sharpest live threat on the board.
  A homogeneous, drift-modelled re-analysis at >3 sigma either sign KILLS the flat law outright.
  AND THE SAME DATUM DISFAVOURS BRANCH B at {sig_raw(sl_B):.1f} sigma, because the measured rise is FASTER than H(z).
  No branch of this framework is supported by the one direct a0(z) measurement in hand.
""")
print("=" * 118)
if FAILS:
    print(f"fbD4 INCOMPLETE: {len(FAILS)}/{NC[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"fbD4 COMPLETE: {NC[0]}/{NC[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
