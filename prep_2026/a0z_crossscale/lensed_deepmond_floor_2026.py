#!/usr/bin/env python3
"""
lensed_deepmond_floor_2026.py -- THE z~2 a0(z) ERROR BUDGET *RECOMPUTED* FOR LENSED,
DEEP-MOND-SELECTED SYSTEMS, AND THE GO/NO-GO AGAINST THE TWO DEC-vs-RISE BARS.
=====================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework (a0 = c H_Lambda / Z,
Z = sqrt(32 pi/3); canonical a0(0) = 9.355e-11 m/s^2; its OWN interpolation
g_obs = sqrt(g_bar^2 + g_bar a0), i.e. the EXACT a0-line  g_obs^2 - g_bar^2 = a0 g_bar).

ROLE (D-3 of the DEC-vs-RISE design): the committed highz_systematics_floor.py computed a
~0.30 dex COHERENT z=2 floor for MASSIVE HSB DISKS and returned NO-GO.  That number must NOT
be inherited: the target population here is different in three ways that all matter, two
favourable and one hostile.  This file RECOMPUTES the budget from scratch for
    LENSED (mu ~ 3-25), DEEP-MOND-SELECTED (g_bar < 0.3 a0), LOW-MASS z ~ 1.5-2.5 rotators
and renders GO/NO-GO separately against BOTH bars.

THE TWO BARS (they are NOT the same test -- rule 3):
  BAR-3S   ~37% on a0  ==  0.1367 dex.  A 3-sigma MECHANISM call, DEC vs RISE.
           Source: committed desitter_unruh_horizon_fork_2026.py, f = gap/(3*mid) at z=2
           with DEC = 0.874 and RISE = 3.005 -> f = 0.366.  (The looser pure-dex reading of
           "3 sigma" is 0.5364/3 = 0.1788 dex = 51%; BOTH are reported, the TIGHTER one is
           used as the headline bar so that a GO cannot be manufactured by convention.)
  BAR-20   ~10.9% on a0 == 0.0450 dex.  A PRIOR-ROBUST 20:1 Bayes factor for DEC over RISE,
           i.e. B>20 under EVERY A_drift prior in the committed ladder.
           Source: committed a0z_fork_likelihood_2026.py section 6(B), truth=M-DEC,
           pair DEC-vs-RISE, z=2 -> sigma = 0.0450 dex.
  A design that reaches BAR-3S but not BAR-20 is a REAL RESULT and is reported as such.

WHAT CHANGES vs THE MASSIVE-HSB FLOOR (all three recomputed, none inherited):
  (+) THE DILUTION LEVER.  The framework's own kernel gives  d log M / d log a0 = -1/(1+2y),
      y = g_bar/a0, so L = 1/(1+2y) and 1/L = 2y+1 is EXACTLY the g_bar-channel error
      amplification.  Deep-MOND selection (y ~ 0.1-0.3) has 1/L = 1.2-1.6 against
      1/L = 7.9 (Ubler z=2.3, y=3.46) and 12.8 (Amvrosiadis, y=5.92).  REAL gain -- but
      computed, not asserted: the honest factor is 5-9x on the mass channel and 3.7-5.8x on
      the velocity channel at y=0.2, NOT the 8-13x that only holds in the y->0 limit.
  (+) LENSING vs BEAM SMEARING.  Magnification buys effective source-plane resolution.
      Conservative fiducial: sqrt(mu) (geometric mean; the disc major axis has random
      orientation w.r.t. the shear direction).  Optimistic sensitivity: mu_t ~ mu.
      Also DERIVED here: g_bar is magnification-INVARIANT (surface density is conserved by
      lensing: M ~ 1/mu and area ~ 1/mu) while g_obs ~ sqrt(mu) through R, so the lens-model
      error enters a0 with only a HALF power: d ln a0 / d ln mu = (y+1).
  (-) PRESSURE SUPPORT IS WORSE, AND LENSING DOES NOT FIX IT.  Asymmetric drift is a
      DYNAMICAL property.  REAL anchors for exactly this population:
        Jones+2010 (MNRAS 404,1247; 6 LENSED z=1.7-3.1, mu~8 linear, ~100 pc source-plane):
            V/sigma = 0.5-1.3, M_dyn = 10^9.7-10.3.
        Simons+2016 (ApJ 830,14, "Kinematic Downsizing at z~2", N=49): below
            log M* ~ 10.2 dispersion-dominated / marginally rotation-supported (V/sig <~ 1)
            is COMMON; low-mass trails high-mass by a few Gyr.
        Leethochawalit+2016 (arXiv:1509.01279; 15 LENSED z~2, log M* ~ 9.5): most do NOT
            match a simple rotating disc.
        Ubler+2019 (ApJ 880,48, KMOS3D): sigma_0 ~ 45 km/s at z~2.3, ~30 km/s at z~0.9
            (MASSIVE discs -- the low-mass V is smaller at similar sigma_0, so V/sigma is
            worse, which is the downsizing statement above).
        KLASS (Mason+2017 ApJ 838,14; Girard+2020 MNRAS 497,173): lensed 7.8<logM*<10.5,
            0.7<z<2.3, majority rotation-supported but at LOWER V/sigma than local.
      => the deep-MOND cut (low mass, low Sigma, large R) and the rotation-support cut
         (V/sigma >= 1.5) are ANTI-CORRELATED at z~2.  That joint-selection cost is the
         deepest finding here and it is a NO-GO pressure, not a GO.
  (-) GAS-MASS CALIBRATION IS HARDER, NOT EASIER.  No HI at z~2.  alpha_CO at the LOW
      metallicity of log M* ~ 9 systems is uncertain by 1-2 ORDERS of magnitude in the worst
      case (Bolatto+2013 review; low-Z dwarf modelling, e.g. A&A 2024 aa47280-23);
      [CII] (Zanella+2018) has ~0.30 dex scatter about alpha_[CII] ~ 31 M_sun/L_sun with a
      zero-point that recent high-z work finds systematically offset.  This is the COHERENT
      wall and it does NOT average down.

HARD CALIBRATION RAILS (a manufactured GO and a manufactured NO-GO are penalized equally)
  R1  Pressure support is NOT assumed away.  Its residual is f_res * C/(1+C) with
      C = 2(R/Rd) sigma_0^2 / V_rot^2 computed from REAL V/sigma anchors above, and f_res is
      SWEPT 0.15/0.25/0.35/0.50.  Its COHERENT fraction is set to 0.60 -- HIGHER than the
      parent's 0.50 -- precisely because lensing removes the per-galaxy sigma NOISE and
      therefore leaves a LARGER share of the residual in the common prescription. That is an
      anti-GO adjustment made deliberately.
  R2  The dilution lever is RECOMPUTED, not inherited, and the honest gain (5-9x, not 8-13x
      at the realistic y=0.2) is reported.
  R3  BOTH bars reported separately, in both currencies.
  R4  PRE-REGISTERED ESTIMATOR = MEDIAN-LIKE (committed estimator_bias_mocks.py /
      estimator_bias_verdict.json: gls_origin bias +10.34 pp FAIL, theilsen +7.93 pp FAIL;
      median_a0pt +0.84, ivw_median +0.66, galaxy_median_then_median +0.31 pp PASS).
      GLS IS FORBIDDEN.  The 1/sqrt(N) averaging therefore carries the median's efficiency
      penalty sqrt(pi/2) = 1.2533 -- a real COST of the pre-registration, applied here.
  R5  Bottom-up budget CROSS-CHECKED against the only real lensed low-mass near-a0 a0(z)
      point in hand (Jeanneau+2026, 95 lensed low-mass z~0.9: +/-0.27 dex on Delta_b, which
      de-dilutes at its own y=0.55 to 0.566 dex on a0).  If my bottom-up sits BELOW that, I
      say so and label the design a FORECAST, not a demonstrated capability.
  R6  Both footings noted; the RATIO a0(z)/a0(0) is footing-independent so every number here
      is.  a0's VALUE and the HORIZON CHOICE remain POSITS.  nu = sqrt(1+1/y) is
      Milgrom 1999 (PLA 253:273 Eq.9) -- the framework's distinctive content is the
      cH_Lambda/Z coefficient and the modified-inertia completion.  McCulloch (MiHsC)
      credited for the rising/Hubble-horizon branch.  No TOE.  No "theory closed".
      Exit 0 = budget computed + GO/NO-GO rendered, NOT a verdict.
"""
import numpy as np
import sympy as sp
import json
import os

np.seterr(all="ignore")
TRAPZ = getattr(np, "trapezoid", None) or np.trapz     # numpy>=2 renamed trapz -> trapezoid
HERE = os.path.dirname(os.path.abspath(__file__))
DEX = np.log(10.0)
BAR = "=" * 100

# ---------------------------------------------------------------- framework constants
Z_CONST = np.sqrt(32 * np.pi / 3)
A0_CAN, A0_ALT = 9.355e-11, 1.1305e-10      # canonical cH_Lambda/Z ; alt cH0/Z
G_NEWT = 6.67430e-11
MSUN, PC, KPC = 1.98892e30, 3.0857e16, 3.0857e19
W0, WA, OM, OL = -0.838, -0.62, 0.3150, 0.6850    # DESI DR2 + Pantheon+ (committed fork head)


def rho_de_ratio(z):
    return (1.0 + z) ** (3.0 * (1.0 + W0 + WA)) * np.exp(-3.0 * WA * z / (1.0 + z))


def R_dec(z):
    return np.sqrt(rho_de_ratio(z))                      # de Sitter / future-event horizon


def R_rise(z):
    return np.sqrt(OM * (1.0 + z) ** 3 + OL * rho_de_ratio(z))   # Hubble horizon (McCulloch)


print(BAR)
print("LENSED DEEP-MOND z~2 a0 ERROR BUDGET -- recomputed, NOT inherited from massive HSB")
print(BAR)
print(f"  a0 = c H_Lambda / Z, Z = {Z_CONST:.5f}; canonical a0(0) = {A0_CAN:.4e} m/s^2, "
      f"alt = {A0_ALT:.4e}.")
print("  Everything below lives in the RATIO a0(z)/a0(0) -> FOOTING-INDEPENDENT (both "
      "footings identical).")

# =====================================================================================
# S0 -- THE TWO BARS, in three currencies, tied to the committed parents
# =====================================================================================
ZT = 2.0
DECz, RISEz = float(R_dec(ZT)), float(R_rise(ZT))
GAP_DEX = np.log10(RISEz / DECz)
MID = 0.5 * (DECz + RISEz)
BAR3S_FRAC = abs(RISEz - DECz) / (3.0 * MID)        # the fork script's own 3-sigma statement
BAR3S_LN = np.log(1.0 + BAR3S_FRAC)
BAR3S_DEX = BAR3S_LN / DEX
BAR3S_DEX_LOOSE = GAP_DEX / 3.0                      # the looser pure-dex reading
BAR20_DEX = 0.0450                                   # committed likelihood section 6(B)
BAR20_LN = BAR20_DEX * DEX
BAR20_FRAC = np.exp(BAR20_LN) - 1.0

print("\n" + BAR)
print("S0 -- THE TWO BARS (they are different tests; rule 3)")
print(BAR)
print(f"  z = {ZT:.1f}:  DEC (de Sitter) = {DECz:.3f}   RISE (Hubble/McCulloch) = {RISEz:.3f}"
      f"   ratio = {RISEz/DECz:.2f}x   gap = {GAP_DEX:.4f} dex")
print(f"  {'bar':10} {'sigma(a0) frac':>15} {'sigma ln a0':>12} {'sigma dex':>10}   meaning")
print("  " + "-" * 92)
print(f"  {'BAR-3S':10} {100*BAR3S_FRAC:>14.1f}% {BAR3S_LN:>12.4f} {BAR3S_DEX:>10.4f}   "
      f"3-sigma MECHANISM call DEC vs RISE (fork script, mid-referenced)")
print(f"  {'(loose 3S)':10} {100*(10**BAR3S_DEX_LOOSE-1):>14.1f}% "
      f"{BAR3S_DEX_LOOSE*DEX:>12.4f} {BAR3S_DEX_LOOSE:>10.4f}   same 3 sigma read in pure "
      f"dex (gap/3) -- LOOSER, reported not used")
print(f"  {'BAR-20':10} {100*BAR20_FRAC:>14.1f}% {BAR20_LN:>12.4f} {BAR20_DEX:>10.4f}   "
      f"PRIOR-ROBUST 20:1 B(DEC/RISE) under EVERY A_drift prior")
print("  HEADLINE BARS USED BELOW: BAR-3S = 0.1367 dex (tighter of the two 3-sigma "
      "conventions), BAR-20 = 0.0450 dex.")

# =====================================================================================
# S1 -- FRAMEWORK-NATIVE AMPLIFICATIONS + the lever identity 1/L = 2y+1 + the mu law
# =====================================================================================
print("\n" + BAR)
print("S1 -- THE FRAMEWORK'S OWN ERROR AMPLIFICATIONS (sympy; and 1/L = 2y+1 proved)")
print(BAR)
a0s, yv, mus = sp.symbols("a0 y mu", positive=True)
go, gb = sp.symbols("g_obs g_bar", positive=True)
a0_read = (go**2 - gb**2) / gb
onshell = {go: sp.sqrt(a0s**2 * yv * (yv + 1)), gb: a0s * yv}
assert sp.simplify(a0_read.subs(onshell) - a0s) == 0
amp_gobs = sp.simplify((sp.diff(sp.log(a0_read), go) * go).subs(onshell))
amp_gbar = sp.simplify((sp.diff(sp.log(a0_read), gb) * gb).subs(onshell))
assert sp.simplify(amp_gobs - 2 * (yv + 1)) == 0
assert sp.simplify(amp_gbar + (2 * yv + 1)) == 0
# the DILUTION LEVER from the framework's own kernel, INDEPENDENTLY: at fixed V and r,
# g_bar = (-a0 + sqrt(a0^2 + 4 V^4/r^2))/2  =>  d log M / d log a0 = -1/(1+2y)
Wv = sp.symbols("W", positive=True)                 # W = V^4/r^2 = g_obs^2, held FIXED
gb_of_a0 = (-a0s + sp.sqrt(a0s**2 + 4 * Wv)) / 2    # framework kernel inverted for g_bar
dlogM_dloga0 = sp.simplify(sp.diff(sp.log(gb_of_a0), a0s) * a0s)
lever_expr = sp.simplify(dlogM_dloga0.subs(Wv, a0s**2 * yv * (yv + 1)))   # put on-shell in y
# sympy leaves -1/sqrt(4y^2+4y+1); 4y^2+4y+1 = (2y+1)^2 exactly and both sides are negative
assert sp.factor(4 * yv * (yv + 1) + 1) == (2 * yv + 1) ** 2
assert sp.simplify(lever_expr**2 - (1 / (1 + 2 * yv))**2) == 0, "lever^2 must be 1/(1+2y)^2"
assert all(float(lever_expr.subs(yv, t)) < 0 for t in (0.1, 0.2, 1.0, 6.0)), "lever sign"
assert max(abs(float(lever_expr.subs(yv, t)) + 1.0 / (1 + 2 * t))
           for t in (0.05, 0.2, 0.55, 3.46, 5.92)) < 1e-14, "lever must be -1/(1+2y)"
# the magnification law: g_bar mu-INVARIANT (Sigma conserved), g_obs ~ sqrt(mu) through R
amp_mu = sp.simplify(sp.Rational(1, 2) * amp_gobs)
assert sp.simplify(amp_mu - (yv + 1)) == 0
print("  d ln a0 / d ln V      =  4(y+1)      (velocity channel)")
print("  d ln a0 / d ln g_obs  =  2(y+1)      (pressure / g_obs channel)  <- the deep-MOND")
print("                                        '2x scatter amplification' at y->0")
print("  d ln a0 / d ln g_bar  = -(2y+1) = -1/L   <- the g_bar / mass / gas channel")
print(f"  PROVED (sympy): d log M/d log a0 = {sp.simplify(lever_expr)}  =>  L = 1/(1+2y) and")
print("     1/L = 2y+1 is EXACTLY the g_bar-channel amplification. The 'dilution lever' and")
print("     the 'mass-side error amplification' are THE SAME OBJECT -- so applying the lever")
print("     gain is not double-counting, it IS the amplification.")
print("  PROVED (sympy): d ln a0 / d ln mu = (y+1).  Reason: lensing conserves surface")
print("     brightness, so M ~ 1/mu and area ~ 1/mu leave Sigma -- hence g_bar = G M/R^2 --")
print("     magnification-INVARIANT, while V is invariant and R ~ mu^-1/2, so g_obs ~ mu^1/2.")
print("     The lens-model error therefore enters a0 with only a HALF power of mu.")


def AMP_V(y):    return 4.0 * (y + 1.0)
def AMP_GOBS(y): return 2.0 * (y + 1.0)
def AMP_GBAR(y): return 2.0 * y + 1.0
def LEVER(y):    return 1.0 / (1.0 + 2.0 * y)
def AMP_MU(y):   return y + 1.0


Y_SAMPLES = {"deep-MOND target (g_bar=0.2a0)": 0.20, "deep-MOND edge (0.3a0)": 0.30,
             "very deep (0.1a0)": 0.10, "Jeanneau lensed z~0.9": 0.55,
             "Ubler KMOS3D z=2.3": 3.46, "Amvrosiadis ALMA z=2.4": 5.92}
print(f"\n  {'sample / selection':32} {'y':>6} {'L':>7} {'1/L=AMP_gbar':>13} "
      f"{'AMP_gobs':>9} {'AMP_V':>7} {'AMP_mu':>7}")
print("  " + "-" * 92)
for lab, y in Y_SAMPLES.items():
    print(f"  {lab:32} {y:>6.2f} {LEVER(y):>7.3f} {AMP_GBAR(y):>13.2f} "
          f"{AMP_GOBS(y):>9.2f} {AMP_V(y):>7.2f} {AMP_MU(y):>7.2f}")
GAIN_MASS = (AMP_GBAR(3.46) / AMP_GBAR(0.20), AMP_GBAR(5.92) / AMP_GBAR(0.20))
GAIN_VEL = (AMP_GOBS(3.46) / AMP_GOBS(0.20), AMP_GOBS(5.92) / AMP_GOBS(0.20))
print(f"\n  HONEST LEVER GAIN at the realistic y = 0.20 (NOT the y->0 limit):")
print(f"    mass / gas / g_bar channel : {GAIN_MASS[0]:.1f}x - {GAIN_MASS[1]:.1f}x  "
      f"(vs Ubler y=3.46 / Amvrosiadis y=5.92)")
print(f"    velocity / pressure channel: {GAIN_VEL[0]:.1f}x - {GAIN_VEL[1]:.1f}x")
print(f"    The quoted '8-13x' is the y->0 limit (1/L = 7.9-12.8 vs 1.0). At the actual cut")
print(f"    g_bar<0.3a0 the realized gain is {GAIN_MASS[0]:.1f}-{GAIN_MASS[1]:.1f}x on the "
      f"mass side and {GAIN_VEL[0]:.1f}-{GAIN_VEL[1]:.1f}x on the velocity side. Both are")
print("    REAL and both are smaller than 8-13x. Stated, not rounded up.")

# =====================================================================================
# S2 -- WHAT g_bar < 0.3 a0 MEANS PHYSICALLY AT z=2, AND THE OBSERVABLE FORK SIGNATURE
# =====================================================================================
print("\n" + BAR)
print("S2 -- THE DEEP-MOND SELECTION AT z=2: surface density, radius, and the FORK in V")
print(BAR)
SIG_A0 = A0_CAN / (2 * np.pi * G_NEWT) / (MSUN / PC**2)     # M_sun/pc^2 at g_bar = a0
print(f"  Sigma at g_bar = a0 (=a0/2piG): {SIG_A0:.1f} M_sun/pc^2   "
      f"-> the cut g_bar<0.3a0 needs Sigma_bar < {0.3*SIG_A0:.1f} M_sun/pc^2.")


def R_of_y(Mbar_msun, y, a0=A0_CAN):
    """radius (kpc) at which the ENCLOSED baryonic mass gives g_bar = y*a0."""
    return np.sqrt(G_NEWT * Mbar_msun * MSUN / (y * a0)) / KPC


def d_A(z, Om=0.3, H0=70.0):
    c = 299792.458
    zz = np.linspace(0.0, z, 4000)
    return (c / H0) * TRAPZ(1.0 / np.sqrt(Om*(1+zz)**3 + (1-Om)), zz) / (1 + z)


KPC_PER_AS = d_A(ZT) * 1e3 / 206265.0
print(f"  z={ZT:.1f} angular scale: {KPC_PER_AS:.2f} kpc/arcsec (flat LCDM Om=0.3 H0=70).")
print(f"\n  {'log M_bar':>10} {'R(g=0.3a0)':>11} {'R(g=0.2a0)':>11} {'theta(0.2a0)':>13} "
      f"{'Sigma_enc(0.2a0)':>17}")
print("  " + "-" * 68)
DEEP_R = {}
for lm in (8.5, 9.0, 9.5, 10.0):
    M = 10.0 ** lm
    r3, r2 = R_of_y(M, 0.3), R_of_y(M, 0.2)
    DEEP_R[lm] = (r3, r2)
    sig_enc = M / (np.pi * (r2 * 1e3) ** 2)
    print(f"  {lm:>10.1f} {r3:>10.2f}k {r2:>10.2f}k {r2/KPC_PER_AS:>12.3f}\" "
          f"{sig_enc:>14.1f} M/pc^2")
print("  READING: the cut is reachable at R ~ 2-7 kpc for log M_bar = 9-10, i.e. R ~ 2-4 R_e")
print("  for a z=2 low-mass disc -- the FAINT OUTSKIRTS. It is NOT a central measurement, and")
print("  the source-plane angular scale is 0.25-0.85 arcsec: unlensed that is 2-6 JWST PSFs")
print("  across the WHOLE probe radius, which is exactly why lensing is not optional here.")

# --- the fork as a DIRECT observable: V at fixed (g_bar, R) under DEC vs RISE -----------
print("\n  THE FORK AS A VELOCITY, not an abstraction (framework kernel, y set at z=0):")
print(f"  {'g_bar/a0(0)':>12} {'g_obs DEC':>11} {'g_obs RISE':>11} {'V_RISE/V_DEC':>13} "
      f"{'req sig(V) 3s':>14} {'req sig(V) 20:1':>16}")
print("  " + "-" * 82)
VGAP = {}
for yy0 in (0.1, 0.2, 0.3):
    gbar = yy0 * A0_CAN
    goD = np.sqrt(gbar**2 + gbar * A0_CAN * DECz)
    goR = np.sqrt(gbar**2 + gbar * A0_CAN * RISEz)
    vr = np.sqrt(goR / goD)                      # V ~ sqrt(g R) at fixed R
    y_eff = gbar / (A0_CAN * DECz)               # y measured against the TRUE a0(z) (DEC)
    sv3 = BAR3S_LN / AMP_V(y_eff)
    sv20 = BAR20_LN / AMP_V(y_eff)
    VGAP[yy0] = (vr, sv3, sv20, y_eff)
    print(f"  {yy0:>12.2f} {goD:>11.3e} {goR:>11.3e} {vr:>12.3f}x "
          f"{100*sv3:>13.2f}% {100*sv20:>15.2f}%")
print("  => at g_bar = 0.2 a0(0) the two horizon readings predict rotation velocities that")
print(f"     differ by {100*(VGAP[0.2][0]-1):.0f}% at the SAME radius. That is a large, honest, directly")
print(f"     measurable signal. The 3-sigma bar needs {100*VGAP[0.2][1]:.1f}% COHERENT velocity accuracy;")
print(f"     the 20:1 bar needs {100*VGAP[0.2][2]:.1f}% -- and the mass side must match "
      f"(see S5).")
GAS_NEED_3S = BAR3S_LN / (AMP_GBAR(0.2) * 0.85) / DEX
GAS_NEED_20 = BAR20_LN / (AMP_GBAR(0.2) * 0.85) / DEX
print(f"     MASS-SIDE requirement (gas share 0.85, y=0.2): M_gas known COHERENTLY to "
      f"{GAS_NEED_3S:.3f} dex (3s) / {GAS_NEED_20:.3f} dex (20:1).")

# =====================================================================================
# S3 -- PRESSURE SUPPORT / ASYMMETRIC DRIFT for LENSED LOW-MASS z~2 (the hostile term)
# =====================================================================================
print("\n" + BAR)
print("S3 -- PRESSURE SUPPORT: dynamical, WORSE at low mass, and lensing does NOT fix it")
print(BAR)
R_OVER_RD = 2.2
K_AD = 2.0 * R_OVER_RD
VSIG_ANCHORS = [
    ("Jones+2010 lensed z=1.7-3.1 (N=6, mu~8, 100pc)", 0.5, 1.3,
     "MNRAS 404,1247 -- THE most on-target real sample: V/sigma = 0.5-1.3, M_dyn 1e9.7-10.3"),
    ("Simons+2016 z~2 log M*<10.2 (N=49)", 0.6, 1.2,
     "ApJ 830,14 kinematic downsizing: dispersion-dominated / V/sig<~1 COMMON below 10.2"),
    ("Leethochawalit+2016 lensed z~2 (N=15)", 0.6, 1.5,
     "arXiv:1509.01279 log M*~9.5 lensed: most do NOT fit a simple rotating disc"),
    ("KLASS lensed 0.7<z<2.3 (N=25/44)", 1.0, 2.5,
     "Mason+2017 ApJ 838,14 / Girard+2020 MNRAS 497,173: majority rotation-supported but "
     "LOWER V/sig than local"),
    ("massive HSB z~2.3 (for contrast)", 3.0, 5.0,
     "Ubler+2019 ApJ 880,48 KMOS3D sigma_0~45 km/s with V~150-250 km/s"),
]
print("  REAL V/sigma anchors for the target population (nothing invented):")
for lab, lo, hi, cite in VSIG_ANCHORS:
    print(f"    {lab:46} V/sig = {lo:.1f}-{hi:.1f}")
    print(f"    {'':46} {cite}")


def C_AD(vsig):
    """asymmetric-drift correction as a FRACTION of V_rot^2: V_c^2 = V_rot^2 + K sigma^2."""
    return K_AD / vsig**2


def press_term(y, vsig, f_res):
    """sigma(ln a0) from the RESIDUAL of the asymmetric-drift correction."""
    C = C_AD(vsig)
    return AMP_GOBS(y) * f_res * C / (1.0 + C), C


print(f"\n  V_c^2 = V_rot^2 + {K_AD:.1f} sigma_0^2 (exp. disc at R=2.2 Rd). Residual on g_obs")
print("  = f_res * C/(1+C); f_res is the fractional uncertainty of the CORRECTION TERM.")
print("  In the dispersion-dominated limit C>>1 this becomes f_res itself -- i.e. f_res IS the")
print("  uncertainty of the dynamical-mass coefficient. Lensing sharpens sigma_0 (removing the")
print("  beam-inflation part of f_res) but CANNOT touch the prescription/anisotropy part.")
print(f"\n  {'V/sigma':>8} {'C_AD':>7} {'C/(1+C)':>8} | " +
      " | ".join(f"f_res={f:.2f}" for f in (0.15, 0.25, 0.35, 0.50)))
print("  " + "-" * 76)
PRESS = {}
for vsig in (0.5, 0.8, 1.0, 1.5, 2.0, 3.0):
    C = C_AD(vsig)
    cells = []
    for f in (0.15, 0.25, 0.35, 0.50):
        s, _ = press_term(0.20, vsig, f)
        PRESS[(vsig, f)] = s
        cells.append(f"{100*(np.exp(s)-1):>8.0f}%")
    print(f"  {vsig:>8.1f} {C:>7.2f} {C/(1+C):>8.3f} | " + " | ".join(cells))
print("  (cells are sigma on a0 in %, at y=0.20; f_res=0.50 is the committed massive-HSB value)")
print("  READING, stated against my own interest: at the V/sigma the REAL lensed low-mass")
print("  z~2 samples actually have (Jones 0.5-1.3), the pressure residual ALONE is")
print(f"  {100*(np.exp(PRESS[(1.0,0.25)])-1):.0f}% on a0 even at an optimistic f_res=0.25 -- already "
      f"{(np.exp(PRESS[(1.0,0.25)])-1)/BAR3S_FRAC:.1f}x the 3-sigma bar")
print(f"  and {(np.exp(PRESS[(1.0,0.25)])-1)/BAR20_FRAC:.1f}x the 20:1 bar. Lensing does not "
      f"help this term at all.")

# =====================================================================================
# S4 -- BEAM SMEARING: the term lensing GENUINELY attacks (quantified, both gain modes)
# =====================================================================================
print("\n" + BAR)
print("S4 -- BEAM SMEARING vs MAGNIFICATION: the one term lensing really does fix")
print(BAR)
RD_LOWMASS = 1.10        # kpc; R_e ~ 1.85 kpc at log M*~9.2, z=2 (van der Wel+2014) -> Rd=Re/1.68
THETA_RD = RD_LOWMASS / KPC_PER_AS
BEAMS = {
    "JWST NIRSpec IFU (0.15\", Halpha 1.97um)": 0.15,
    "JWST NIRCam/NIRISS grism (0.13\")": 0.13,
    "ALMA 0.10\" (CO/[CII] cold tracer)": 0.10,
    "ALMA 0.05\" (long baselines)": 0.05,
}


def dV_beam(ratio):
    """residual dV/V after 3D forward modelling (Di Teodoro&Fraternali15, Ubler+18 calib.)."""
    return 0.02 + 0.05 * ratio


def res_gain(mu, mode):
    """effective source-plane resolution gain. 'sqrt' = geometric mean (CONSERVATIVE, the
    disc major axis has random orientation w.r.t. the shear); 'tan' = full mu_t (optimistic,
    only if the major axis happens to lie along the stretch)."""
    return np.sqrt(mu) if mode == "sqrt" else mu


print(f"  target source: R_d = {RD_LOWMASS:.2f} kpc (van der Wel+2014 size-mass, log M*~9.2, "
      f"z=2) -> theta_Rd = {THETA_RD:.3f}\"")
print("  residual dV/V after 3D forward-modelling = 2% + 5%*(R_beam/R_d_effective).")
print(f"\n  {'instrument':40} " + " ".join(f"{'mu='+str(m):>13}" for m in (1, 3, 8, 15, 25)))
print("  " + "-" * 110)
BEAMTAB = {}
for blab, bfw in BEAMS.items():
    cells = []
    for mu in (1, 3, 8, 15, 25):
        ratio = bfw / (THETA_RD * res_gain(mu, "sqrt"))
        s = AMP_V(0.20) * dV_beam(ratio)
        BEAMTAB[(blab, mu)] = (ratio, s)
        cells.append(f"r={ratio:>4.2f} {100*(np.exp(s)-1):>4.0f}%")
    print(f"  {blab:40} " + " ".join(f"{c:>13}" for c in cells))
print("  (cells: R_beam/R_d_eff and the resulting sigma on a0, at y=0.20, gain = sqrt(mu))")
_r1 = BEAMTAB[("JWST NIRSpec IFU (0.15\", Halpha 1.97um)", 1)]
_r8 = BEAMTAB[("JWST NIRSpec IFU (0.15\", Halpha 1.97um)", 8)]
_r25 = BEAMTAB[("JWST NIRSpec IFU (0.15\", Halpha 1.97um)", 25)]
print(f"\n  THE LENSING GAIN, quantified: JWST NIRSpec-IFU on this source goes from "
      f"{100*(np.exp(_r1[1])-1):.0f}% (mu=1)")
print(f"  to {100*(np.exp(_r8[1])-1):.0f}% (mu=8) to {100*(np.exp(_r25[1])-1):.0f}% (mu=25) "
      f"on a0 -- a real, large gain, and the ONLY term")
print("  in this budget that magnification improves. BUT the 2% floor in the residual formula")
print(f"  imposes an IRREDUCIBLE beam term = 4(y+1)*0.02 = "
      f"{100*(np.exp(AMP_V(0.20)*0.02)-1):.1f}% on a0 no matter how large mu is:")
print(f"  that alone is {(np.exp(AMP_V(0.20)*0.02)-1)/BAR20_FRAC:.1f}x the 20:1 bar. "
      f"Lensing cannot beat the modelling floor.")
_opt = AMP_V(0.20) * dV_beam(0.15 / (THETA_RD * res_gain(8, "tan")))
print(f"  OPTIMISTIC MODE (major axis along the stretch, gain = mu_t = mu): mu=8 gives "
      f"{100*(np.exp(_opt)-1):.0f}% instead of {100*(np.exp(_r8[1])-1):.0f}%.")
print("  Both modes are carried; sqrt(mu) is the fiducial because orientation is random.")

# =====================================================================================
# S5 -- GAS-MASS CALIBRATION: the COHERENT wall (and the phi optimum)
# =====================================================================================
print("\n" + BAR)
print("S5 -- GAS-MASS CALIBRATION at z~2 without HI: the coherent wall")
print(BAR)
GASCAL = {
    "[CII] Zanella+2018 alpha_[CII]~31": dict(rand=0.30, coh=0.15,
        cite="A&A/MNRAS: ~0.30 dex scatter over 4 dex in L; zero-point systematically "
             "offset in recent high-z work -> 0.15 dex coherent is the OPTIMISTIC read"),
    "CO + metallicity alpha_CO (log M*~9)": dict(rand=0.35, coh=0.30,
        cite="Bolatto+2013 review; low-Z dwarfs span 1-2 ORDERS in alpha_CO (SMC ~70x MW) "
             "-> 0.30 dex coherent is generous for a log M*~9, low-Z z=2 system"),
    "dust continuum + GDR(Z)": dict(rand=0.30, coh=0.25,
        cite="gas-to-dust ratio is itself metallicity-dependent; inherits the same low-Z "
             "problem plus a dust-temperature systematic"),
    "DIRECT HI 21cm (SKA2/ngVLA, ~2035+)": dict(rand=0.10, coh=0.05,
        cite="no alpha_CO at all -- the only route that breaks the wall (committed parent's "
             "same conclusion, reached independently here)"),
}
print("  tracer options and their per-object RANDOM / COHERENT calibration errors (dex on M_gas):")
print(f"  {'tracer':38} {'rand':>6} {'coh':>6} {'sig(a0) coh @ y=0.2, gas share 0.85':>38}")
print("  " + "-" * 92)
for lab, d in GASCAL.items():
    s_coh = AMP_GBAR(0.20) * 0.85 * d["coh"] * DEX
    d["s_coh_a0"] = s_coh
    print(f"  {lab:38} {d['rand']:>6.2f} {d['coh']:>6.2f} "
          f"{100*(np.exp(s_coh)-1):>36.0f}%")
for lab, d in GASCAL.items():
    print(f"    {lab:38} {d['cite']}")
print(f"\n  REQUIREMENT (from S2): M_gas coherent to {GAS_NEED_3S:.3f} dex for the 3-sigma bar,")
print(f"  {GAS_NEED_20:.3f} dex for the 20:1 bar. ONLY direct HI (0.05 dex) clears BOTH.")
print(f"  [CII] at an optimistic 0.15 dex coherent gives "
      f"{100*(np.exp(GASCAL['[CII] Zanella+2018 alpha_[CII]~31']['s_coh_a0'])-1):.0f}% on a0 "
      f"-- it MISSES the 3-sigma bar by "
      f"{(np.exp(GASCAL['[CII] Zanella+2018 alpha_[CII]~31']['s_coh_a0'])-1)/BAR3S_FRAC:.1f}x.")

# --- the phi (stellar share) OPTIMUM: maximum gas dominance is NOT optimal --------------
print("\n  THE phi OPTIMUM (a genuine design finding, not an assumption): the mass side is")
print("  AMP_gbar(y) * sqrt[ ((1-phi) sig_gascal)^2 + (phi sig_lnUpsilon)^2 ], so the best")
print("  baryon mix TRADES the gas-calibration error against the stellar M/L error.")
UPS_LN_HIGHZ = 0.40      # ~0.17 dex; z~2 stellar pops: young+dusty+bursty, IMF+SFH priors
print(f"  sig_lnUpsilon at z~2 taken as {UPS_LN_HIGHZ:.2f} in ln (= {UPS_LN_HIGHZ/DEX:.3f} dex);"
      f" parent used 0.35 TODAY / 0.23 FUTURE.")
print(f"  {'phi (stellar share of g_bar)':30} " +
      " ".join(f"{'gascal='+f'{g:.2f}':>14}" for g in (0.05, 0.15, 0.30)))
print("  " + "-" * 78)
PHI_GRID = np.array([0.05, 0.15, 0.30, 0.50, 0.70, 0.85])
MASS_SIDE = {}
for phi in PHI_GRID:
    cells = []
    for g in (0.05, 0.15, 0.30):
        s = AMP_GBAR(0.20) * np.hypot((1 - phi) * g * DEX, phi * UPS_LN_HIGHZ)
        MASS_SIDE[(round(float(phi), 2), g)] = s
        cells.append(f"{100*(np.exp(s)-1):>13.0f}%")
    print(f"  {phi:>30.2f} " + " ".join(cells))
for g in (0.05, 0.15, 0.30):
    best = min(PHI_GRID, key=lambda p: MASS_SIDE[(round(float(p), 2), g)])
    print(f"    gascal={g:.2f} dex -> optimum phi = {best:.2f}  "
          f"(sigma_a0 = {100*(np.exp(MASS_SIDE[(round(float(best),2), g)])-1):.0f}%)")
print("  READING: with [CII]/CO-level calibration the optimum is a MIXED baryon budget")
print("  (phi ~ 0.3-0.5), NOT maximum gas dominance -- chasing extreme gas fractions buys")
print("  nothing once sig_gascal > sig_Upsilon. Only if direct HI arrives (gascal 0.05 dex)")
print("  does full gas dominance become the right target. This flips the usual z=0 intuition.")

# =====================================================================================
# S6 -- LENS-MODEL SYSTEMATIC ON THE MAGNIFICATION
# =====================================================================================
print("\n" + BAR)
print("S6 -- LENS-MODEL SYSTEMATIC: d ln a0 / d ln mu = (y+1) (half-power, S1-proved)")
print(BAR)
MU_CASES = {
    "well-modelled bright arc, multiply imaged (stat)": dict(dmu=0.10, coh=0.03,
        cite="e.g. RCSGA 032727-132609 source-plane reconstruction: 'uncertainty on the "
             "magnification is typically 10%' (MCMC over one model family)"),
    "cluster field, CROSS-MODEL systematic at mu~3": dict(dmu=0.40, coh=0.06,
        cite="Priewe+2017 MNRAS 465,1030 / Raney+2020 MNRAS 494,4771 (HFF): scatter ~40% "
             "and bias -6% at mu=3, method-to-method"),
    "cluster field, CROSS-MODEL at mu~10": dict(dmu=0.65, coh=0.17,
        cite="same: scatter ~65%, bias -17% at mu=10; up to ~70% at mu~40"),
    "galaxy-scale lens (SLACS/BELLS-like)": dict(dmu=0.15, coh=0.05,
        cite="ESTIMATE-CODED: single deflector, simple mass model, far fewer model "
             "degeneracies than a cluster; flagged as an estimate, not a published number"),
}
print(f"  {'lens configuration':50} {'d mu/mu':>8} {'coh':>6} {'sig(a0)':>9} {'coh a0':>8}")
print("  " + "-" * 86)
for lab, d in MU_CASES.items():
    d["s"] = AMP_MU(0.20) * d["dmu"]
    d["s_coh"] = AMP_MU(0.20) * d["coh"]
    print(f"  {lab:50} {d['dmu']:>8.2f} {d['coh']:>6.2f} "
          f"{100*(np.exp(d['s'])-1):>8.0f}% {100*(np.exp(d['s_coh'])-1):>7.0f}%")
for lab, d in MU_CASES.items():
    print(f"    {lab:50} {d['cite']}")
DIFFMAG_COH = 0.06       # differential magnification across the resolved arc, breaks Sigma-invariance
print(f"\n  PLUS a DIFFERENTIAL-MAGNIFICATION term: the mu-invariance of g_bar holds only if the")
print(f"  SAME mu delenses flux and area. Across a real giant arc mu varies from ~4 to >100")
print(f"  (RCSGA 032727 is the textbook case), so the invariance is only approximate. Coded as")
print(f"  a COHERENT {DIFFMAG_COH:.2f} in ln mu -> {100*(np.exp(AMP_MU(0.20)*DIFFMAG_COH)-1):.0f}% "
      f"on a0. ESTIMATE-CODED, flagged.")
print("  READING: the half-power law is a REAL gain (a 40% mu error becomes a 48% not a 96%")
print("  a0 error), and g_bar's mu-invariance is a genuine structural protection. But the")
print("  COHERENT part (method bias 6-17% + differential magnification) already sits at")
print(f"  {100*(np.exp(np.hypot(AMP_MU(0.2)*0.06, AMP_MU(0.2)*DIFFMAG_COH))-1):.0f}%-"
      f"{100*(np.exp(np.hypot(AMP_MU(0.2)*0.17, AMP_MU(0.2)*DIFFMAG_COH))-1):.0f}% on a0, "
      f"i.e. {(np.exp(AMP_MU(0.2)*0.17)-1)/BAR20_FRAC:.1f}x the 20:1 bar on its own.")

# =====================================================================================
# S7 -- ASSEMBLE: per-object sigma(a0), COHERENT vs RANDOM split, and N = 15/25/40
# =====================================================================================
print("\n" + BAR)
print("S7 -- THE ASSEMBLED BUDGET: per object, and averaged to N = 15 / 25 / 40")
print(BAR)
MEDIAN_PENALTY = np.sqrt(np.pi / 2)      # sqrt(pi/2)=1.2533: the COST of pre-registering median-like
COH_FRAC = dict(beam=0.30, press=0.60, ups=0.70, diffmag=1.00)
print(f"  Coherent fractions: beam {COH_FRAC['beam']:.2f} (PSF/3D-model), pressure "
      f"{COH_FRAC['press']:.2f} (prescription/anisotropy;")
print("  the parent used 0.50 -- RAISED here because lensing removes the per-galaxy sigma NOISE")
print(f"  and so leaves MORE of the residual in the common recipe), Upsilon {COH_FRAC['ups']:.2f} "
      f"(SPS/IMF/SFH),")
print("  gas + lens-model split explicitly per scenario, differential magnification 1.00.")
print(f"  MEDIAN-LIKE ESTIMATOR PENALTY applied to all random terms: sqrt(pi/2) = "
      f"{MEDIAN_PENALTY:.4f} (rule 4 -- GLS is FORBIDDEN, bias +10.34 pp).")


def budget(y=0.20, mu=10.0, gain_mode="sqrt", vsig=1.5, f_res=0.25, beam=0.10,
           phi=0.50, ups_ln=0.40, gas_coh=0.15, gas_rand=0.30, dmu=0.15, dmu_coh=0.05,
           diffmag=0.06, rar_dex=0.15, fv=0.04, Rd=RD_LOWMASS):
    """Full sigma(ln a0) budget for ONE lensed deep-MOND-selected object at z=2."""
    th = Rd / KPC_PER_AS
    ratio = beam / (th * res_gain(mu, gain_mode))
    T = {}
    T["beam"] = (AMP_V(y) * dV_beam(ratio), COH_FRAC["beam"])
    C = C_AD(vsig)
    T["press"] = (AMP_GOBS(y) * f_res * C / (1.0 + C), COH_FRAC["press"])
    s_gas_tot = AMP_GBAR(y) * (1 - phi) * np.hypot(gas_coh, gas_rand) * DEX
    s_gas_coh = AMP_GBAR(y) * (1 - phi) * gas_coh * DEX
    T["gas"] = (s_gas_tot, s_gas_coh / s_gas_tot if s_gas_tot > 0 else 0.0)
    T["ups"] = (AMP_GBAR(y) * phi * ups_ln, COH_FRAC["ups"])
    T["lens_mu"] = (AMP_MU(y) * dmu, dmu_coh / dmu if dmu > 0 else 0.0)
    T["diffmag"] = (AMP_MU(y) * diffmag, COH_FRAC["diffmag"])
    T["rar_intrinsic"] = (2.0 * rar_dex * DEX, 0.0)        # a0 scatter = 2x RAR dex; RANDOM
    T["vel_noise"] = (AMP_V(y) * fv, 0.0)                  # RANDOM (S/N-limited)
    tot = np.sqrt(sum(v[0] ** 2 for v in T.values()))
    coh = np.sqrt(sum((v[0] * v[1]) ** 2 for v in T.values()))
    rnd = np.sqrt(max(tot**2 - coh**2, 0.0))
    T["_C_AD"] = C
    T["_beam_ratio"] = ratio
    return T, tot, coh, rnd


def sig_N(coh, rnd, N):
    return np.sqrt(coh**2 + (MEDIAN_PENALTY * rnd / np.sqrt(N)) ** 2)


def pct(sln):
    return 100.0 * (np.exp(sln) - 1.0)


SCEN = {
 "A TODAY / ARCHIVAL (JWST+ALMA in hand)": dict(
    mu=8, vsig=1.0, f_res=0.35, beam=0.15, phi=0.50, ups_ln=0.45, gas_coh=0.30,
    gas_rand=0.35, dmu=0.40, dmu_coh=0.08, diffmag=0.08, rar_dex=0.18, fv=0.06),
 "B PURPOSE-BUILT JWST+ALMA (~2028-31)": dict(
    mu=10, vsig=1.5, f_res=0.25, beam=0.10, phi=0.50, ups_ln=0.40, gas_coh=0.15,
    gas_rand=0.30, dmu=0.15, dmu_coh=0.05, diffmag=0.06, rar_dex=0.15, fv=0.04),
 "C OPTIMISTIC, still NO direct HI": dict(
    mu=15, vsig=2.0, f_res=0.15, beam=0.05, phi=0.50, ups_ln=0.35, gas_coh=0.10,
    gas_rand=0.25, dmu=0.10, dmu_coh=0.03, diffmag=0.04, rar_dex=0.12, fv=0.03),
 "D HI ERA: SKA2/ngVLA + ELT (~2035+)": dict(
    mu=15, vsig=2.5, f_res=0.15, beam=0.05, phi=0.15, ups_ln=0.35, gas_coh=0.05,
    gas_rand=0.10, dmu=0.10, dmu_coh=0.03, diffmag=0.04, rar_dex=0.11, fv=0.03),
}
TERMS = ["beam", "press", "gas", "ups", "lens_mu", "diffmag", "rar_intrinsic", "vel_noise"]
RES = {}
print(f"\n  per-term sigma on a0 (%), y = 0.20 throughout:")
print(f"  {'scenario':38} " + " ".join(f"{t[:9]:>10}" for t in TERMS) +
      f" | {'PER-OBJ':>8} {'COHERENT':>9} {'RANDOM':>8}")
print("  " + "-" * 152)
for lab, kw in SCEN.items():
    T, tot, coh, rnd = budget(**kw)
    RES[lab] = dict(T={k: (float(T[k][0]), float(T[k][1])) for k in TERMS},
                    tot=float(tot), coh=float(coh), rnd=float(rnd),
                    C_AD=float(T["_C_AD"]), beam_ratio=float(T["_beam_ratio"]), kw=kw)
    print(f"  {lab:38} " + " ".join(f"{pct(T[t][0]):>9.0f}%" for t in TERMS) +
          f" | {pct(tot):>7.0f}% {pct(coh):>8.0f}% {pct(rnd):>7.0f}%")
print("\n  aggregate sigma(a0) after averaging (COHERENT part does NOT average down):")
print(f"  {'scenario':38} {'N=1':>9} {'N=15':>9} {'N=25':>9} {'N=40':>9} {'N=inf':>9} "
      f"| {'3S bar':>8} {'20:1 bar':>9}")
print("  " + "-" * 118)
for lab in SCEN:
    r = RES[lab]
    row = [r["tot"]] + [sig_N(r["coh"], r["rnd"], n) for n in (15, 25, 40)] + [r["coh"]]
    r["sigN"] = {k: float(v) for k, v in zip(("N1", "N15", "N25", "N40", "Ninf"), row)}
    print(f"  {lab:38} " + " ".join(f"{pct(v):>8.0f}%" for v in row) +
          f" | {100*BAR3S_FRAC:>7.0f}% {100*BAR20_FRAC:>8.1f}%")

# --- the SAME term list applied to a MASSIVE HSB disc: proves recomputation, not inheritance
print("\n  RECOMPUTATION CHECK (rule 2): the SAME term list at MASSIVE-HSB acceleration")
print("  (y = 3.46, Ubler KMOS3D z=2.3) with scenario-B instrument settings:")
Tm, totm, cohm, rndm = budget(y=3.46, phi=0.70, Rd=2.0, vsig=3.5, **{k: v for k, v in
                              SCEN["B PURPOSE-BUILT JWST+ALMA (~2028-31)"].items()
                              if k not in ("phi", "vsig")})
print(f"    massive HSB : per-obj {pct(totm):>6.0f}%  coherent {pct(cohm):>6.0f}% "
      f"({cohm/DEX:.2f} dex)   N=25 {pct(sig_N(cohm, rndm, 25)):>6.0f}%")
rb = RES["B PURPOSE-BUILT JWST+ALMA (~2028-31)"]
print(f"    lensed deep-MOND (B): per-obj {pct(rb['tot']):>6.0f}%  coherent "
      f"{pct(rb['coh']):>6.0f}% ({rb['coh']/DEX:.2f} dex)   N=25 "
      f"{pct(sig_N(rb['coh'], rb['rnd'], 25)):>6.0f}%")
print(f"    => the deep-MOND selection improves the COHERENT floor by "
      f"{cohm/rb['coh']:.1f}x ({cohm/DEX:.2f} -> {rb['coh']/DEX:.2f} dex).")
print(f"    PROVENANCE, stated exactly: {cohm/DEX:.2f} dex sits INSIDE the parent's own PHYSICS")
print("    bottom-up massive-HSB range (0.6-1.0 dex), and ~2.6x ABOVE the parent's")
print("    DATA-ANCHORED ledger floor (0.30 dex, the number most favourable to the test).")
print("    That is the SAME ~2x reconciliation gap the parent documented and did not hide.")
print("    So this file reproduces the parent's massive-HSB physics and the deep-MOND gain is")
print("    EARNED by the selection, not manufactured by re-labelling. Against the parent's")
print(f"    DATA-ANCHORED 0.30 dex the gain is only {0.30/(rb['coh']/DEX):.1f}x, not "
      f"{cohm/rb['coh']:.1f}x -- both are reported.")

# =====================================================================================
# S8 -- GO / NO-GO against BOTH bars, with the REQUIRED per-object precision and N
# =====================================================================================
print("\n" + BAR)
print("S8 -- GO / NO-GO, bar by bar (rule 3: they are separate results)")
print(BAR)


def verdict_for(coh, rnd, bar_ln, Ns=(15, 25, 40)):
    """(verdict, smallest N in Ns that clears the bar or None, N needed if unbounded)."""
    if coh >= bar_ln:
        return "NO-GO (coherent floor exceeds the bar; N is irrelevant)", None, None
    hit = next((n for n in Ns if sig_N(coh, rnd, n) <= bar_ln), None)
    need = (MEDIAN_PENALTY * rnd / np.sqrt(bar_ln**2 - coh**2)) ** 2
    if hit is not None:
        return f"GO at N={hit}", hit, need
    return f"NO-GO at N<=40 (needs N~{need:.0f})", None, need


GONOGO = {}
for barlab, bar_ln, barfrac in (("BAR-3S  (3-sigma DEC-vs-RISE mechanism call)", BAR3S_LN,
                                 BAR3S_FRAC),
                                ("BAR-20  (prior-robust 20:1 Bayes factor)", BAR20_LN,
                                 BAR20_FRAC)):
    print(f"\n  --- {barlab}: sigma(a0) <= {100*barfrac:.1f}% = {bar_ln/DEX:.4f} dex " +
          "-" * 12)
    print(f"    {'scenario':38} {'coh floor':>10} {'N=25':>8} {'N req':>8}   verdict")
    print("    " + "-" * 106)
    for lab in SCEN:
        r = RES[lab]
        v, hit, need = verdict_for(r["coh"], r["rnd"], bar_ln)
        GONOGO[(barlab, lab)] = dict(verdict=v, N_hit=hit,
                                     N_required=(float(need) if need is not None else None),
                                     coh_dex=r["coh"] / DEX)
        nreq = f"{need:>8.0f}" if need is not None else f"{'--':>8}"
        print(f"    {lab:38} {r['coh']/DEX:>9.3f}d {pct(r['sigN']['N25']):>7.0f}% {nreq}   {v}")

print("\n  " + "#" * 96)
print("  THE ANSWER, in one block (both bars, no hedging):")
print("  " + "#" * 96)
_C = RES["C OPTIMISTIC, still NO direct HI"]
_D = RES["D HI ERA: SKA2/ngVLA + ELT (~2035+)"]
_B = RES["B PURPOSE-BUILT JWST+ALMA (~2028-31)"]
_A = RES["A TODAY / ARCHIVAL (JWST+ALMA in hand)"]
print(f"""
  BAR-3S  (~37% on a0 = 0.1355 dex; a 3-sigma DECLINING-vs-RISING MECHANISM call)
    * TODAY / ARCHIVAL lensed sample: NO-GO. Coherent floor {_A['coh']/DEX:.2f} dex, i.e.
      {_A['coh']/BAR3S_LN:.1f}x the bar, and it does not average down. N is irrelevant.
    * PURPOSE-BUILT JWST NIRSpec-IFU + ALMA campaign (scenario B): NO-GO. Coherent floor
      {_B['coh']/DEX:.2f} dex = {_B['coh']/BAR3S_LN:.1f}x the bar. Still N-irrelevant.
    * OPTIMISTIC no-HI corner (scenario C: V/sigma>=2 SELECTED, f_res<=0.15, ALMA 0.05",
      [CII] zero-point pinned to 0.10 dex, mu>=15 well-modelled arcs): MARGINAL GO, and only
      at N ~ {GONOGO[('BAR-3S  (3-sigma DEC-vs-RISE mechanism call)','C OPTIMISTIC, still NO direct HI')]['N_required']:.0f}
      ({pct(_C['sigN']['N40']):.0f}% at N=40 vs the 37% bar -- a {100*(BAR3S_FRAC-(np.exp(_C['sigN']['N40'])-1))/BAR3S_FRAC:.0f}%
      margin). This is a KNIFE-EDGE result and must be quoted as such.
    * HI ERA (scenario D, SKA2/ngVLA gas masses + ELT/ALMA cold tracers): GO at N = {GONOGO[('BAR-3S  (3-sigma DEC-vs-RISE mechanism call)','D HI ERA: SKA2/ngVLA + ELT (~2035+)')]['N_hit']}
      ({pct(_D['sigN']['N25']):.0f}% at N=25). Comfortable, not marginal.

  BAR-20  (~10.9% on a0 = 0.0450 dex; a PRIOR-ROBUST 20:1 Bayes factor for DEC over RISE)
    * NO-GO IN EVERY SCENARIO, INCLUDING THE HI ERA AND INCLUDING N -> infinity.
      Coherent floors: A {_A['coh']/DEX:.2f}, B {_B['coh']/DEX:.2f}, C {_C['coh']/DEX:.2f},
      D {_D['coh']/DEX:.2f} dex against a 0.0450 dex bar -- {_D['coh']/BAR20_LN:.1f}x short even at
      the best. Coherent terms do not average down, so no N and no telescope in this design
      clears it. Reaching BAR-20 at z=2 would require the FULL coherent budget below
      0.045 dex, i.e. simultaneously: gas mass coherent to <{GAS_NEED_20:.3f} dex,
      pressure prescription to f_res < {BAR20_LN/(AMP_GOBS(0.2)*0.5)*1.0:.3f} at V/sigma=2,
      beam residual below {BAR20_LN/AMP_V(0.2):.3f} in dV/V (BELOW the 2% modelling floor --
      already impossible), and lens-model coherent mu to <{BAR20_LN/AMP_MU(0.2):.3f}.
      The beam requirement alone is inside the 2% floor, so BAR-20 is CLOSED at z=2 for this
      observable class. Said plainly: the prior-robust 20:1 target is NOT reachable this way.

  NET GO/NO-GO: **GO for the 3-sigma MECHANISM call, NO-GO for the prior-robust 20:1** --
  and the GO is conditional (knife-edge without direct HI, comfortable with it).""")

# =====================================================================================
# S9 -- SENSITIVITY, THE JOINT-SELECTION COST, AND THE EMPIRICAL CROSS-CHECK
# =====================================================================================
print("\n" + BAR)
print("S9 -- SENSITIVITY (both directions), the JOINT-SELECTION cost, and the reality check")
print(BAR)
print("  (a) ONE-AT-A-TIME sensitivity around scenario B: which knob actually moves the answer?")
base_kw = dict(SCEN["B PURPOSE-BUILT JWST+ALMA (~2028-31)"])
_, tb, cb, rb2 = budget(**base_kw)
print(f"    {'knob change':44} {'coh dex':>9} {'N=25':>8} {'d(coh) vs base':>15}")
print("    " + "-" * 80)
KNOBS = [
    ("BASE (scenario B)", {}),
    ("V/sigma 1.5 -> 1.0 (real Jones+2010 value)", dict(vsig=1.0)),
    ("V/sigma 1.5 -> 2.5 (aggressive selection)", dict(vsig=2.5)),
    ("f_res 0.25 -> 0.50 (parent's massive value)", dict(f_res=0.50)),
    ("f_res 0.25 -> 0.15 (best conceivable)", dict(f_res=0.15)),
    ("gas_coh 0.15 -> 0.30 dex (alpha_CO low-Z)", dict(gas_coh=0.30)),
    ("gas_coh 0.15 -> 0.05 dex (direct HI only)", dict(gas_coh=0.05)),
    ("mu 10 -> 25 (highest-mag arcs)", dict(mu=25)),
    ("mu 10 -> 3 (modest magnification)", dict(mu=3)),
    ("gain sqrt(mu) -> mu_t (major axis aligned)", dict(gain_mode="tan")),
    ("dmu 0.15 -> 0.40 (cross-model cluster)", dict(dmu=0.40, dmu_coh=0.08)),
    ("y 0.20 -> 0.30 (looser deep-MOND cut)", dict(y=0.30)),
    ("y 0.20 -> 0.10 (tighter cut, fainter)", dict(y=0.10)),
    ("phi 0.50 -> 0.85 (max gas dominance)", dict(phi=0.85)),
    ("rar_dex 0.15 -> 0.25 (clumpy high-z RAR)", dict(rar_dex=0.25)),
]
SENS = {}
for lab, ch in KNOBS:
    kw = dict(base_kw); kw.update(ch)
    _, t, c, r = budget(**kw)
    SENS[lab] = dict(coh_dex=float(c / DEX), N25=float(sig_N(c, r, 25)))
    print(f"    {lab:44} {c/DEX:>9.3f} {pct(sig_N(c, r, 25)):>7.0f}% "
          f"{(c-cb)/DEX:>+15.3f}")
worst = max(SENS, key=lambda k: SENS[k]["coh_dex"])
best = min(SENS, key=lambda k: SENS[k]["coh_dex"])
print(f"    DOMINANT knobs: worst = '{worst}' ({SENS[worst]['coh_dex']:.3f} dex), "
      f"best = '{best}' ({SENS[best]['coh_dex']:.3f} dex).")
print("    Note both directions are present: 'gas_coh -> 0.05 (HI)' is the single biggest")
print("    IMPROVEMENT and 'f_res -> 0.50' / 'V/sigma -> 1.0' are the biggest DEGRADATIONS.")

print("\n  (b) THE JOINT-SELECTION COST (the finding that constrains N, and it is hostile):")
FROT = dict(lo=0.20, hi=0.40)     # ESTIMATE-CODED from the V/sigma anchors in S3
print(f"    The design needs BOTH (i) g_bar < 0.3 a0 -- low mass, low Sigma, LARGE radius, and")
print(f"    (ii) V/sigma >= 1.5 so that a rotation curve means anything. At z~2 these are")
print(f"    ANTI-CORRELATED: Jones+2010 finds V/sigma = 0.5-1.3 for exactly this population")
print(f"    (0 of 6 above 1.5) and Simons+2016 finds V/sigma <~ 1 COMMON below log M* = 10.2.")
print(f"    ESTIMATE-CODED yield of the V/sigma >= 1.5 sub-population at low mass, z~2:")
print(f"    f_rot = {FROT['lo']:.0%}-{FROT['hi']:.0%} (flagged as an ESTIMATE from those V/sigma")
print(f"    distributions, NOT a published fraction).")
print(f"    {'target N':>9} {'lensed low-mass z~2 systems that must be surveyed':>52}")
for N in (15, 25, 40):
    print(f"    {N:>9} {int(np.ceil(N/FROT['hi'])):>26} - {int(np.ceil(N/FROT['lo'])):<24}")
print("    => a scenario-C/D sample of N=40 needs 100-200 lensed low-mass z~2 systems with")
print("    resolved kinematics AND cold-gas masses. That is a LARGE multi-cycle program, and")
print("    it is the binding practical constraint on the marginal BAR-3S GO.")

print("\n  (c) EMPIRICAL REALITY CHECK (rule 5) -- against the best real lensed low-mass point:")
JEAN_DB, JEAN_Y = 0.27, 0.55
JEAN_A0_DEX = JEAN_DB / LEVER(JEAN_Y)
print(f"    Jeanneau+2026 (A&A, arXiv:2603.28856; 95 LENSED low-mass, z~0.9, g_bar~0.3-1 a0)")
print(f"    carries an honest systematics-inclusive +/-{JEAN_DB:.2f} dex on Delta_b, which at its")
print(f"    own y = {JEAN_Y:.2f} (L = {LEVER(JEAN_Y):.3f}) de-dilutes to "
      f"{JEAN_A0_DEX:.3f} dex = {100*(10**JEAN_A0_DEX-1):.0f}% on a0.")
print(f"    My scenario-B per-object forecast is {_B['tot']/DEX:.2f} dex and its N=25 aggregate is")
print(f"    {sig_N(_B['coh'], _B['rnd'], 25)/DEX:.2f} dex -- i.e. "
      f"{JEAN_A0_DEX/(sig_N(_B['coh'], _B['rnd'], 25)/DEX):.1f}x better than the best measurement")
print("    of this class that exists, at a HIGHER redshift. Stated plainly: this budget is a")
print("    FORECAST that assumes a purpose-built campaign beats the best in-hand lensed")
print("    low-mass a0(z) constraint by a factor of a few. It is NOT a demonstrated capability,")
print("    and if the real campaign lands at Jeanneau-like systematics BOTH bars are NO-GO.")

print("\n  (d) THE NON-OBVIOUS RESULT worth flagging: magnification is NOT the binding term.")
print(f"    mu = 3 -> 25 moves the scenario-B COHERENT floor by only "
      f"{abs(SENS['mu 10 -> 25 (highest-mag arcs)']['coh_dex'] - SENS['mu 10 -> 3 (modest magnification)']['coh_dex']):.3f} dex, and")
print("    switching to the optimistic mu_t gain mode moves it by ~0.001 dex. Lensing is")
print("    NECESSARY (without it these objects are unresolvable and the per-object RANDOM error")
print("    is ~2x worse) but it is NOT SUFFICIENT: the coherent floor is set by GAS-MASS")
print("    CALIBRATION and the PRESSURE PRESCRIPTION, neither of which magnification touches.")
print("    Any proposal claiming 'high magnification solves the systematics' is wrong, and this")
print("    is the number that shows it.")

# =====================================================================================
# S10 -- PRE-REGISTRATION, JSON, SELF-CHECK
# =====================================================================================
print("\n" + "#" * 100)
print("# PRE-REGISTRATION -- lensed deep-MOND z~2 a0(z) floor + GO/NO-GO, frozen with this commit")
print("#" * 100)
PREREG = [
    "ESTIMATOR (rule 4, NON-NEGOTIABLE): the a0 aggregate MUST be a MEDIAN-LIKE estimator -- "
    "median_a0pt, ivw_median_a0pt, galaxy_median_then_median, log_median_a0pt or "
    "trimmed_mean_a0pt (all |bias| <= 1.41 pp in the committed estimator_bias_verdict.json). "
    "GLS (gls_origin / gls_lowy, bias +10.34 pp) and Theil-Sen (+7.93 pp) are FORBIDDEN. The "
    "sqrt(pi/2) = 1.2533 efficiency penalty on the random terms is applied throughout as the "
    "honest COST of that choice; a design that only clears a bar without the penalty does not "
    "clear it.",
    "TARGET SELECTION, frozen: z in [1.5, 2.5]; g_bar(R_meas) < 0.3 a0(0) with y = 0.1-0.3 "
    "(equivalently Sigma_bar < 32 M_sun/pc^2 enclosed); V/sigma >= 1.5 measured from a "
    "source-plane-resolved velocity field (NOT from an integrated line width); mu >= 5 with a "
    "lens model constrained by at least one spectroscopically confirmed counter-image.",
    "THE V/sigma CUT IS THE HARD ONE AND IT IS PRE-REGISTERED AS A CUT, NOT A CORRECTION. "
    "Jones+2010 (the most on-target real lensed sample, N=6 at z=1.7-3.1) has V/sigma = "
    "0.5-1.3, i.e. ZERO objects passing. If the real campaign cannot assemble N >= 15 objects "
    "at V/sigma >= 1.5, the measurement MUST NOT be attempted by relaxing the cut and applying "
    "a bigger asymmetric-drift correction: that is exactly the channel that manufactures an "
    "apparent a0 rise (the A_drift nuisance of the committed likelihood, sign-locked positive).",
    "THE COHERENT/RANDOM SPLIT IS THE LOAD-BEARING MODELLING CHOICE. Pressure is coded 60% "
    "coherent (HIGHER than the parent's 50%, deliberately, because lensing removes the "
    "per-galaxy sigma noise and therefore leaves MORE of the residual in the common "
    "prescription); gas calibration 100% coherent in its zero-point; beam 30%; Upsilon 70%. If "
    "any of these is optimistic the verdicts move toward NO-GO, not toward GO.",
    "GAS MASS IS THE WALL AND THE REQUIREMENT IS NUMERICAL: M_gas must be known COHERENTLY to "
    f"{GAS_NEED_3S:.3f} dex for BAR-3S and {GAS_NEED_20:.3f} dex for BAR-20 (at y=0.2, gas "
    "share 0.85). [CII] (Zanella+2018, 0.30 dex scatter) at an optimistic 0.15 dex zero-point "
    "MISSES BAR-3S by 1.4x on that term alone; metallicity-dependent alpha_CO at log M* ~ 9 is "
    "worse. Only DIRECT HI 21cm (<0.05 dex, SKA2/ngVLA) clears it -- the same conclusion the "
    "committed parent reached for massive discs, re-derived here independently for the lensed "
    "deep-MOND case.",
    "phi OPTIMUM (a design instruction, not an assumption): with [CII]/CO-level calibration the "
    "mass side is MINIMIZED at a MIXED baryon budget phi ~ 0.3-0.5, NOT at maximum gas "
    "dominance. Chasing extreme gas fractions is counter-productive once sig_gascal > "
    "sig_Upsilon. Full gas dominance only becomes optimal in the direct-HI era.",
    "MAGNIFICATION IS NOT THE BINDING TERM. mu = 3 -> 25 moves the coherent floor by <0.002 "
    "dex. Lensing is necessary for detectability and for the per-object random error, and "
    "g_bar is magnification-INVARIANT (surface-density conservation, S1-proved) so the lens "
    "model enters a0 only at half power (y+1) d ln mu -- a real structural protection. But the "
    "campaign must NOT be justified on magnification: it must be justified on gas calibration "
    "and on the V/sigma >= 1.5 yield.",
    "FORECAST STATUS (rule 5): the scenario-B N=25 aggregate (0.21 dex) is ~2.8x better than "
    "the best existing measurement of this class (Jeanneau+2026, 0.567 dex on a0 after "
    "de-dilution, at the EASIER redshift z~0.9). This budget is therefore a FORECAST, not a "
    "demonstrated capability. If the real campaign lands at Jeanneau-like systematics, BOTH "
    "bars are NO-GO and that must be reported as the outcome.",
    "THE SIGN ASYMMETRY IS THE ONE FREE GIFT AND IT IS NOT OVERSOLD: the committed likelihood "
    "showed A_drift is sign-locked POSITIVE, so a measured a0(2)/a0(0) BELOW 1 is drift-proof. "
    "That is why BAR-3S (a mechanism call against a 3.44x RISE) is reachable while BAR-20 "
    "(which must also out-argue Ciocan under every prior) is not. It does NOT make the "
    "framework's DECLINE detected -- distinguishing DEC from FLAT at z=2 needs 0.010 dex and is "
    "not on this table at all.",
    "CONDITIONALITY: the whole test is void if DESI DR3 relaxes to w = -1, because M-DEC then "
    "becomes EXACTLY M-FLAT and there is nothing to measure (untestable, NOT falsified). The "
    "GO below is conditional on DESI's w0wa evolution being real.",
    "BOTH FOOTINGS: every number lives in the ratio a0(z)/a0(0), which is footing-independent, "
    f"so canonical a0(0) = {A0_CAN:.4e} and alt {A0_ALT:.4e} give identical budgets and "
    "identical verdicts. Only an absolute-a0 anchor separates the footings, and this design "
    "does not attempt one.",
    "a0's VALUE and the HORIZON CHOICE remain POSITS. nu = sqrt(1+1/y) is Milgrom 1999 (PLA "
    "253:273 Eq.9) -- the framework's distinctive content is the cH_Lambda/Z coefficient and "
    "the modified-inertia completion. McCulloch (MiHsC) is credited for the rising/Hubble "
    "branch that this design tries to exclude. No TOE. No 'theory closed'. Doors remain open. "
    "Exit 0 = budget computed, NOT a verdict.",
]
for i, c in enumerate(PREREG, 1):
    print(f"#  {i}. {c}")
print("#" * 100)

out = dict(
    role="D-3 systematic floor + GO/NO-GO for the LENSED DEEP-MOND-SELECTED z~2 a0(z) fork",
    bars=dict(BAR3S=dict(frac=float(BAR3S_FRAC), ln=float(BAR3S_LN), dex=float(BAR3S_DEX),
                         loose_dex=float(BAR3S_DEX_LOOSE),
                         meaning="3-sigma DEC-vs-RISE mechanism call"),
              BAR20=dict(frac=float(BAR20_FRAC), ln=float(BAR20_LN), dex=float(BAR20_DEX),
                         meaning="prior-robust 20:1 Bayes factor DEC over RISE")),
    fork_at_z2=dict(DEC=DECz, RISE=RISEz, ratio=float(RISEz / DECz), gap_dex=float(GAP_DEX),
                    V_ratio_at_y0p2=float(VGAP[0.2][0]),
                    req_sigV_3s=float(VGAP[0.2][1]), req_sigV_20=float(VGAP[0.2][2])),
    amplifications=dict(dlnA0_dlnV="4(y+1)", dlnA0_dlnGobs="2(y+1)", dlnA0_dlnGbar="-(2y+1)",
                        dlnA0_dlnMu="(y+1)", lever="L = 1/(1+2y) == 1/AMP_gbar (sympy-proved)"),
    lever_gain_at_y0p2=dict(mass_channel=[float(x) for x in GAIN_MASS],
                            velocity_channel=[float(x) for x in GAIN_VEL],
                            note="the quoted 8-13x is the y->0 limit; realized gain is smaller"),
    deep_mond_selection=dict(Sigma_a0_Msun_pc2=float(SIG_A0),
                             Sigma_cut_0p3a0=float(0.3 * SIG_A0),
                             R_kpc_at_0p2a0={str(k): float(v[1]) for k, v in DEEP_R.items()},
                             kpc_per_arcsec_z2=float(KPC_PER_AS)),
    gas_requirement_dex=dict(BAR3S=float(GAS_NEED_3S), BAR20=float(GAS_NEED_20),
                             tracers={k: dict(rand=v["rand"], coh=v["coh"],
                                              sig_a0_coh_frac=float(np.exp(v["s_coh_a0"]) - 1))
                                      for k, v in GASCAL.items()}),
    scenarios={k: dict(settings=v["kw"], per_term_frac={t: float(np.exp(v["T"][t][0]) - 1)
                                                        for t in TERMS},
                       per_object_frac=float(np.exp(v["tot"]) - 1),
                       coherent_frac=float(np.exp(v["coh"]) - 1),
                       coherent_dex=float(v["coh"] / DEX),
                       sigma_at_N={n: float(np.exp(s) - 1) for n, s in v["sigN"].items()})
               for k, v in RES.items()},
    go_no_go={f"{b} || {s}": g for (b, s), g in GONOGO.items()},
    sensitivity=SENS,
    joint_selection=dict(f_rot_estimate=[FROT["lo"], FROT["hi"]],
                         survey_size_for_N={str(n): [int(np.ceil(n / FROT["hi"])),
                                                     int(np.ceil(n / FROT["lo"]))]
                                           for n in (15, 25, 40)},
                         note="ESTIMATE-CODED from the Jones+2010 / Simons+2016 V/sigma "
                              "distributions; not a published fraction"),
    empirical_crosscheck=dict(jeanneau_deltab_dex=JEAN_DB, jeanneau_y=JEAN_Y,
                              jeanneau_a0_dex=float(JEAN_A0_DEX),
                              forecast_improvement_factor=float(
                                  JEAN_A0_DEX / (sig_N(RES["B PURPOSE-BUILT JWST+ALMA (~2028-31)"]["coh"],
                                                       RES["B PURPOSE-BUILT JWST+ALMA (~2028-31)"]["rnd"],
                                                       25) / DEX)),
                              status="FORECAST, not demonstrated capability"),
    estimator=dict(prereg="MEDIAN-LIKE ONLY; GLS and Theil-Sen FORBIDDEN",
                   gls_bias_pp=10.34, theilsen_bias_pp=7.93,
                   allowed_max_bias_pp=1.41, median_efficiency_penalty=float(MEDIAN_PENALTY)),
    footings=dict(canonical=A0_CAN, alt=A0_ALT, ratio_footing_independent=True),
    verdict=("GO for BAR-3S (the ~37%, 3-sigma DECLINING-vs-RISING MECHANISM call) but ONLY in "
             "the optimistic no-HI corner at N>=~40 (knife-edge, 1% margin) or comfortably at "
             "N>=15 once DIRECT HI 21cm gas masses exist (SKA2/ngVLA + ELT/ALMA, ~2035+); "
             "NO-GO for BAR-20 (the ~10.9% prior-robust 20:1 Bayes factor) in EVERY scenario "
             "and at N->infinity, because the coherent floor (0.080-0.299 dex) exceeds the "
             "0.045 dex bar by 1.8-6.6x and the beam-modelling requirement alone falls inside "
             "the irreducible 2% dV/V floor. Today's/archival lensed samples are NO-GO on both. "
             "The binding terms are GAS-MASS CALIBRATION and the PRESSURE PRESCRIPTION, not "
             "magnification; and the binding practical constraint is the V/sigma>=1.5 yield at "
             "low mass and z~2, which the real lensed samples (Jones+2010: V/sigma=0.5-1.3) do "
             "not currently supply."),
)
JP = os.path.join(HERE, "lensed_deepmond_floor_2026_results.json")
with open(JP, "w") as f:
    json.dump(out, f, indent=1, default=float)
print(f"\nwrote {JP}")

print("\n" + BAR)
print("SELF-CHECK (frozen invariants)")
print(BAR)
assert abs(DECz - 0.874) < 0.002 and abs(RISEz - 3.005) < 0.005, "fork must match the parents"
assert abs(RISEz / DECz - 3.44) < 0.02, "z=2 divergence must be 3.44x"
assert abs(BAR20_DEX - 0.0450) < 1e-9, "BAR-20 must be the committed 0.0450 dex"
assert 0.36 < BAR3S_FRAC < 0.37, "BAR-3S must reproduce the fork script's 37%"
assert BAR3S_DEX < BAR3S_DEX_LOOSE, "the headline 3-sigma bar must be the TIGHTER convention"
assert abs(LEVER(0.0) - 1.0) < 1e-12 and abs(LEVER(3.46) - 0.126) < 1e-3
assert abs(1.0 / LEVER(0.2) - AMP_GBAR(0.2)) < 1e-12, "1/L must equal AMP_gbar exactly"
assert abs(SIG_A0 - 106.8) < 1.0, "Sigma at a0 must be ~107 M_sun/pc^2"
assert 5.0 < GAIN_MASS[0] < 6.5 and 8.5 < GAIN_MASS[1] < 10.0, \
    "the honest lever gain must be 5-9x at y=0.2, NOT 8-13x"
assert RES["A TODAY / ARCHIVAL (JWST+ALMA in hand)"]["coh"] > BAR3S_LN, \
    "today's archival lensed sample must be NO-GO on BAR-3S (not spun into a GO)"
assert all(RES[s]["coh"] > BAR20_LN for s in SCEN), \
    "BAR-20 must be NO-GO in EVERY scenario including the HI era (coherent floor)"
assert RES["D HI ERA: SKA2/ngVLA + ELT (~2035+)"]["coh"] < BAR3S_LN, \
    "the HI era must clear BAR-3S (a manufactured NO-GO is penalized like a manufactured GO)"
assert sig_N(RES["C OPTIMISTIC, still NO direct HI"]["coh"],
             RES["C OPTIMISTIC, still NO direct HI"]["rnd"], 40) < BAR3S_LN, \
    "scenario C at N=40 must clear BAR-3S (the marginal GO must be real)"
assert sig_N(RES["C OPTIMISTIC, still NO direct HI"]["coh"],
             RES["C OPTIMISTIC, still NO direct HI"]["rnd"], 25) > BAR3S_LN, \
    "scenario C at N=25 must NOT clear BAR-3S (the GO must be knife-edge, as reported)"
assert PRESS[(1.0, 0.25)] > BAR3S_LN, \
    "at the REAL lensed V/sigma=1.0 the pressure term alone must exceed the 3-sigma bar"
assert cohm > RES["B PURPOSE-BUILT JWST+ALMA (~2028-31)"]["coh"], \
    "massive HSB must be WORSE than lensed deep-MOND (the lever gain must be real)"
assert 0.6 <= cohm / DEX <= 1.0, \
    "the recomputed massive-HSB coherent floor must land inside the parent's 0.6-1.0 dex range"
assert abs(MEDIAN_PENALTY - 1.2533) < 1e-3, "median efficiency penalty must be sqrt(pi/2)"
assert JEAN_A0_DEX > RES["B PURPOSE-BUILT JWST+ALMA (~2028-31)"]["coh"] / DEX, \
    "the forecast must be flagged as better than the best in-hand measurement"
print(f"  fork z=2: DEC {DECz:.3f} RISE {RISEz:.3f} ratio {RISEz/DECz:.2f}x  OK")
print(f"  bars: BAR-3S {BAR3S_DEX:.4f} dex ({100*BAR3S_FRAC:.1f}%), "
      f"BAR-20 {BAR20_DEX:.4f} dex ({100*BAR20_FRAC:.1f}%)  OK")
print(f"  1/L == AMP_gbar exactly; lever gain {GAIN_MASS[0]:.1f}-{GAIN_MASS[1]:.1f}x "
      f"(not 8-13x)  OK")
print(f"  coherent floors (dex): A {RES['A TODAY / ARCHIVAL (JWST+ALMA in hand)']['coh']/DEX:.3f} "
      f"B {RES['B PURPOSE-BUILT JWST+ALMA (~2028-31)']['coh']/DEX:.3f} "
      f"C {RES['C OPTIMISTIC, still NO direct HI']['coh']/DEX:.3f} "
      f"D {RES['D HI ERA: SKA2/ngVLA + ELT (~2035+)']['coh']/DEX:.3f}  OK")
print(f"  BAR-3S: NO-GO today/B, marginal GO C@N=40, GO D@N=15;  BAR-20: NO-GO everywhere  OK")
print("\nEXIT 0 (budget computed + GO/NO-GO rendered; not a verdict).")
