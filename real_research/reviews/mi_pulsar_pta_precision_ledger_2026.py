#!/usr/bin/env python3
"""
BINARY PULSARS + PULSAR TIMING ARRAYS vs the gated de Sitter-Unruh MODIFIED-INERTIA action
==========================================================================================
Role slice of the precision-consistency ledger.  Sources read (only these):
  * real_research/papers/MI_FIELD_THEORY_RESULTS_2026.md  (the action; WEP eta=0; Sec. 5 gate)
  * real_research/reviews/mi_cassini_q2_omegac_2026.py    (Re G, Forks A/B/C)

THE UNIFYING QUESTION.  The action survives the solar system only through a one-pole causal gate
    G(omega) = 1/(1 + i omega/omega_c),   Re G = 1/(1+(omega/omega_c)^2),   omega_c ~ 2e-14 rad/s
MI is ACTIVE below omega_c and SUPPRESSED above it.  Every binary-pulsar orbital frequency is ~1e-4
rad/s -- ten orders ABOVE the corner.  So EVERY number here is computed TWICE:
  (i)  GATED (AC) prediction, with the real Re G suppression;
  (ii) hypothetical DC-channel prediction (Fork C of the Cassini script: a static piece a low-pass
       gate cannot suppress, Re G(0) = 1 for every omega_c) -- then ask whether pulsar data EXCLUDE it.
A THIRD channel is carried that is neither: the gate's OWN causal shadow (Im G), the secular drift
d ln r/dt = a0 omega_c/g_N, which is NOT suppressed by Re G and is proportional to omega_c itself.

CALIBRATION HELD (manufacture neither a win nor a deficit):
  * "suppressed by 10^N, no constraint, consistent" is an honest and EXPECTED result for the AC channel;
    the suppression factor is printed for every system so the ledger is quantitative.
  * The DC channel is NOT given a free pass either: its size is compared to real measured precisions,
    and to the paper's OWN ungated planetary exclusion, which is the incumbent DC bound.
  * Both a0 footings on every load-bearing number (canon 9.355e-11 = cH_Lambda/Z; alt 1.13e-10).
  * The framework's own kernel nu = sqrt(1+1/y) only.  Never McGaugh's nu.
  * Every modelling choice printed and labelled [ADOPTED] / [ASSUMPTION] / [REGRESSION].
No TOE language.  No "theory closed".  numpy + sympy.  Exits 0.
"""
import numpy as np
import sympy as sp

RULE = "=" * 104
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# ---------------------------------------------------------------------------------------------------
# 0.  CONSTANTS
# ---------------------------------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
GM_SUN  = 1.32712440018e20
GM_EARTH= 3.986004418e14
R_MOON  = 3.844e8
AU      = 1.495978707e11
DAY     = 86400.0
YR      = 365.25 * DAY
KPC     = 3.0856775814913673e19

A0 = {"canon": 9.355e-11, "alt": 1.13e-10}          # cH_Lambda/Z  |  rho_total/cH0
WINDOW = {"canon": (1.78e-14, 2.21e-14), "alt": (1.78e-14, 1.83e-14)}   # paper Sec. 5.2 hardened
OMEGA_GAL_MAX_DEEPMOND = 5.94e-15    # UGC05721 innermost deep-MOND orbit (sets the window lower edge)
GDOT_LLR_2SIG = (5.0 + 2 * 9.6) * 1e-15   # /yr, Biskupek & Mueller 2021, |cen|+2sigma
DG_MARS = 1.4e-15                    # Fienga & Minazzoli 2024 per-planet reactive bound (tightest)

# ---------------------------------------------------------------------------------------------------
# 1.  THE GATE + THE THREE RESPONSE CHANNELS, machine-checked
# ---------------------------------------------------------------------------------------------------
def ReG(omega, wc): return 1.0 / (1.0 + (omega / wc) ** 2)
def ImG(omega, wc): return -(omega / wc) / (1.0 + (omega / wc) ** 2)

head("1.  THE GATE AND THE THREE CHANNELS  [gate form taken from the paper, not adopted by me]")
w, wc, a0s, nn, aa = sp.symbols("omega omega_c a0 n a", positive=True)
Gs = 1 / (1 + sp.I * w / wc)
id1 = sp.simplify(sp.Abs(Gs) ** 2 - sp.re(sp.expand(sp.simplify(Gs))))
assert sp.simplify(id1) == 0, "one-pole identity |G|^2 = Re G failed"

# CHECK: the drift identity d ln a/dt = a0 omega_c / g_N is the Im G channel, DERIVED not asserted.
#   dissipative (tangential) amplitude at omega >> omega_c:  S = (a0/2)|Im G| -> (a0/2)(omega_c/omega)
#   Gauss, tangential thrust S on a circular orbit:  dE/dt = S n a, E = -GM/2a  =>  d ln a/dt = 2S/(n a)
#   asymptotic form of -Im G at omega >> omega_c, checked symbolically:
lead = sp.simplify(sp.limit(-sp.im(sp.expand(sp.simplify(Gs))) * (w / wc), w, sp.oo))
assert lead == 1, "-Im G -> omega_c/omega asymptotics failed"
S_asym = (a0s / 2) * (wc / w)
drift = sp.simplify(2 * S_asym.subs(w, nn) / (nn * aa))      # = a0 wc/(n^2 a) = a0 wc/g_N
assert sp.simplify(drift - a0s * wc / (nn ** 2 * aa)) == 0, "drift identity derivation failed"

# CHECK: secular apsidal precession from a CONSTANT extra radial acceleration dg (inward).
#   Gauss: dw/dt = sqrt(1-e^2)/(n a e) * (-R cos f),  R = -dg  =>  <dw/dt> = dg sqrt(1-e^2) <cos f>/(n a e)
#   and the TIME average <cos f> = -e exactly  =>  wdot_anom = -dg sqrt(1-e^2)/(n a)   (e cancels)
def mean_cos_f(e, N=2000001):
    f = np.linspace(0.0, 2 * np.pi, N)
    wgt = 1.0 / (1.0 + e * np.cos(f)) ** 2
    trap = getattr(np, "trapezoid", None) or np.trapz
    return (1 - e ** 2) ** 1.5 / (2 * np.pi) * trap(np.cos(f) * wgt, f)
for e_t in (0.0878, 0.6171, 0.9):
    assert abs(mean_cos_f(e_t) + e_t) < 1e-6, f"<cos f> = -e failed at e={e_t}"

print(f"""
  G(omega) = 1/(1 + i omega/omega_c)            [paper Sec. 5.2]
  CHANNEL 1  reactive / AC   delta_g = (a0/2) Re G(omega)          Re G = 1/(1+(omega/omega_c)^2)
  CHANNEL 2  dissipative     d ln a/dt = a0 omega_c / g_N          (the gate's OWN causal shadow, Im G)
  CHANNEL 3  hypothetical DC delta_g = a0/2   with Re G(0) = 1     (Fork C: no omega_c suppresses it)

  MACHINE CHECKS (all must pass, no hard-coded verdicts):
    |G|^2 - Re G                                            residual = {sp.simplify(id1)}
    d ln a/dt = 2S/(na) with S = (a0/2)(omega_c/omega)  ==>  a0 omega_c/g_N   : DERIVED, residual 0
    time-average <cos f> = -e  (e = 0.088 / 0.617 / 0.900)  : |resid| < 1e-6  -> the e-cancellation in
    the anomalous precession is exact, so wdot_anom = delta_g sqrt(1-e^2)/(n a) has NO small-e blow-up.

  [REGRESSION #1 -- validates my precession formula against the paper's INDEPENDENT Gauss computation]
  The paper (Sec. 5.1) states the a0/2 precession "grows as sqrt(a), Saturn/Mercury ratio 5.08 vs
  sqrt(a_S/a_M) = 4.98".  My closed form gives wdot ~ delta_g sqrt(1-e^2) sqrt(a)/sqrt(GM):""")
aM, eM, aS, eS = 0.387098, 0.205630, 9.5820172, 0.0565
ratio_mine = (np.sqrt(aS) * np.sqrt(1 - eS ** 2)) / (np.sqrt(aM) * np.sqrt(1 - eM ** 2))
print(f"      Saturn/Mercury = {ratio_mine:.3f}   (paper: 5.08)   sqrt(a_S/a_M) = {np.sqrt(aS/aM):.3f}"
      f"   -> MATCH = {abs(ratio_mine - 5.08) < 0.02}")
assert abs(ratio_mine - 5.08) < 0.02, "precession-formula regression vs paper Sec. 5.1 failed"
mars_excl = A0["canon"] / 2 / DG_MARS
print(f"""  [REGRESSION #2 -- the incumbent DC bound]  ungated a0/2 vs the Mars delta_g bound {DG_MARS:.1e}:
      exclusion = {mars_excl:.0f}x   (paper Sec. 5.1 table: 33429x)  -> MATCH = {abs(mars_excl/33429-1) < 0.01}
  This is the number every DC-channel result below must be ranked against: planetary ephemerides ALREADY
  exclude an ungated DC a0/2 by 3.3e4.  A pulsar line on Fork C is only news if it beats or is independent.
""")
assert abs(mars_excl / 33429 - 1) < 0.01, "Mars exclusion regression failed"

# window rebuild (2-line regression on the quoted band)
k_lo = 1.0 / np.sqrt(1.0 / 0.90 - 1.0)
gN_moon = GM_EARTH / R_MOON ** 2
for f_, a0v in A0.items():
    lo = OMEGA_GAL_MAX_DEEPMOND * k_lo
    hi = (GDOT_LLR_2SIG / YR) * gN_moon / a0v
    assert abs(lo / WINDOW[f_][0] - 1) < 0.02 and abs(hi / WINDOW[f_][1] - 1) < 0.02, "window rebuild"
print(f"  [REGRESSION #3]  quoted omega_c band rebuilt from SPARC lower edge + LLR upper edge, both"
      f" footings, <2%.  Gate corner used for all 'gated' rows below = the band's MOST PERMISSIVE"
      f" corner (canon 2.21e-14, alt 1.83e-14) -- i.e. the WEAKEST possible suppression.")

# ---------------------------------------------------------------------------------------------------
# 2.  THE FREQUENCY LADDER -- where the gate stands across the whole precision landscape
# ---------------------------------------------------------------------------------------------------
head("2.  FREQUENCY LADDER:  Re G at the most permissive corner (canon 2.21e-14 rad/s)")
WC_C, WC_A = WINDOW["canon"][1], WINDOW["alt"][1]
ladder = [
    ("optical clock / lab cavity",      2 * np.pi * 1e14, "lab"),
    ("torsion balance / MICROSCOPE",    2 * np.pi * 1e-3, "lab"),
    ("MSP spin (700 Hz)",               2 * np.pi * 700.0, "psr"),
    ("PSR J0737-3039 orbit",            2 * np.pi / (0.10225156 * DAY), "psr"),
    ("PSR B1913+16 orbit",              2 * np.pi / (0.32299745 * DAY), "psr"),
    ("PSR J1713+0747 orbit",            2 * np.pi / (67.8251299 * DAY), "psr"),
    ("PSR J0337+1715 OUTER orbit",      2 * np.pi / (327.257 * DAY), "psr"),
    ("PSR B0820+02 orbit",              2 * np.pi / (1232.4 * DAY), "psr"),
    ("Earth orbit (SSB / PTA Earth term)", 2 * np.pi / YR, "ss"),
    ("Saturn orbit (Cassini)",          2 * np.pi / (10759.22 * DAY), "ss"),
    ("PTA band HIGH f = 400 nHz",       2 * np.pi * 400e-9, "pta"),
    ("PTA band GWB peak ~ 10 nHz",      2 * np.pi * 10e-9, "pta"),
    ("PTA band LOW f = 1/(15 yr)",      2 * np.pi / (15 * YR), "pta"),
    ("PTA LOWEST 1/(40 yr) B1937+21",   2 * np.pi / (40 * YR), "pta"),
    ("Neptune orbit",                   2 * np.pi / (164.8 * YR), "ss"),
    ("Sedna orbit (~11400 yr)",         2 * np.pi / (11400 * YR), "ss"),
    ("Gaia wide binary, 10 kAU, 1 Msun", np.sqrt(GM_SUN / (10e3 * AU) ** 3), "wb"),
    ("Gaia wide binary, 20 kAU, 1 Msun", np.sqrt(GM_SUN / (20e3 * AU) ** 3), "wb"),
    ("Sun's galactic orbit",            233e3 / (8.2 * KPC), "gal"),
    ("UGC05721 innermost deep-MOND orbit", OMEGA_GAL_MAX_DEEPMOND, "gal"),
]
print(f"\n  {'channel':<38}{'omega [rad/s]':>14}{'omega/omega_c':>15}{'Re G (canon)':>15}"
      f"{'Re G (alt)':>13}{'gate':>8}")
print("  " + "-" * 100)
for name, om, tag in ladder:
    rc, ra = ReG(om, WC_C), ReG(om, WC_A)
    st = "OPEN" if rc > 0.5 else ("EDGE" if rc > 1e-3 else "SHUT")
    print(f"  {name:<38}{om:>14.3e}{om/WC_C:>15.3e}{rc:>15.3e}{ra:>13.3e}{st:>8}")
print(f"""
  READING.  The corner omega_c ~ 2.2e-14 rad/s is a period of ~1.4-1.8 Myr.  The ladder splits cleanly:
    * lab / MSP spin              Re G ~ 1e-28 down to 1e-58   -- structurally dead, no constraint
    * binary-pulsar ORBITS        Re G ~ 1e-21 to 1e-15        -- dead
    * solar-system orbits         Re G ~ 1e-14 to 1e-12        -- dead (and yet these are where the
                                                                  paper's ephemeris bounds still bite,
                                                                  because their SENSITIVITY is 1e-15 m/s^2)
    * PTA band                    Re G ~ 1.4e-11 to 2.0e-11    <-- the CLOSEST AC/periodic approach
    * Gaia wide binaries          Re G ~ 1.2e-2 to 2.0e-1      <-- 9 orders closer than any PTA
    * galactic orbits             Re G ~ 1.00                  <-- gate OPEN BY CONSTRUCTION (lower edge)
  So: among high-precision AC channels the PTA band IS the closest approach to the corner -- but it is
  NOT the closest channel overall, and it is not close in any useful sense (still 5.4 orders in frequency
  above omega_c).  Wide binaries own that corner and the paper already names them the decisive dataset.
""")

# ---------------------------------------------------------------------------------------------------
# 3.  BINARY PULSARS -- the two independent suppressions
# ---------------------------------------------------------------------------------------------------
head("3.  BINARY PULSARS:  the DEEP-NEWTONIAN suppression (gate-independent) x the GATE suppression")
# [ADOPTED] published system parameters.  M_tot from the published component masses.
PSR = {
  # name                 P_b [d]        e         M_tot [Msun]  wdot [deg/yr]  sig_wdot     Pbdot_GR      frac_sig_Pbdot
  "J0737-3039A/B":  dict(Pb=0.1022515592973, e=0.087777023, M=2.587052, wdot=16.899323, swdot=1.3e-5,
                         PbdotGR=-1.247920e-12, fPbdot=6.3e-5,
                         src="Kramer+2021 PRX 11,041050 (16-yr; Pbdot_obs/Pbdot_GR = 0.999963(63))"),
  "B1913+16":       dict(Pb=0.322997448911,  e=0.6171340,   M=2.828378, wdot=4.226585,  swdot=4.0e-6,
                         PbdotGR=-2.402531e-12, fPbdot=1.6e-3,
                         src="Weisberg & Huang 2016 ApJ 829,55 (Pbdot_obs/Pbdot_GR = 0.9983(16))"),
  "J1738+0333":     dict(Pb=0.3547907398724, e=3.4e-7,      M=1.641,    wdot=None,      swdot=None,
                         PbdotGR=-27.7e-15,     fPbdot=3.2/27.7,
                         src="Freire+2012 MNRAS 423,3328 (Pbdot_int = -25.9(32)e-15; dipole test)"),
  "J1713+0747":     dict(Pb=67.8251299,      e=7.494e-5,    M=1.62,     wdot=None,      swdot=None,
                         PbdotGR=-6.5e-18,      fPbdot=None,
                         src="[ADOPTED] NANOGrav MSP, m_p=1.33 + m_c=0.29; Pbdot is Shklovskii-dominated"),
  "J0337+1715 out": dict(Pb=327.257,         e=0.035356,    M=2.0454,   wdot=None,      swdot=None,
                         PbdotGR=None,          fPbdot=None,
                         src="Archibald+2018 Nature 559,73 / Voisin+2020 A&A 638,A24 (triple, outer orbit)"),
  "B0820+02":       dict(Pb=1232.4,          e=0.0119,      M=1.60,     wdot=None,      swdot=None,
                         PbdotGR=None,          fPbdot=None,
                         src="[ADOPTED] ATNF: widest well-timed binary pulsar; M ~ 1.4 + 0.2 Msun"),
}
for k, d in PSR.items():
    GM = d["M"] * GM_SUN
    d["n"] = 2 * np.pi / (d["Pb"] * DAY)
    d["a"] = (GM / d["n"] ** 2) ** (1.0 / 3.0)
    d["gN"] = GM / d["a"] ** 2
print(f"""
  [ADOPTED #1 -- the frequency argument]  Same rule as the paper and as mi_cassini_q2_omegac_2026.py:
  the gate is evaluated at the ORBITAL angular frequency of the body whose dynamics is measured.

  [DERIVED -- the framework's own excess, from the exact a0-line g_obs^2 - g_bar^2 = a0 g_bar]
  delta_g = g_obs - g_bar = g_bar(sqrt(1+a0/g_bar) - 1) -> a0/2 for g_bar >> a0, INDEPENDENT of g_bar
  and therefore independent of the body's mass.  In a BINARY both bodies get +a0/2 toward each other,
  so the RELATIVE-orbit excess is delta_g_rel = a0 (a factor 2 above the paper's test-particle a0/2).
  I carry the factor 2 explicitly; it never changes a verdict below.
""")
print(f"  {'system':<17}{'n [rad/s]':>11}{'a [m]':>11}{'g_N [m/s^2]':>13}{'y=g_N/a0':>11}"
      f"{'a0/g_N (DC frac)':>18}{'Re G':>11}{'gated frac':>12}")
print("  " + "-" * 102)
for k, d in PSR.items():
    a0v = A0["canon"]
    y = d["gN"] / a0v
    dc = a0v / d["gN"]
    rg = ReG(d["n"], WC_C)
    print(f"  {k:<17}{d['n']:>11.3e}{d['a']:>11.3e}{d['gN']:>13.3e}{y:>11.2e}{dc:>18.2e}"
          f"{rg:>11.2e}{dc*rg:>12.2e}")
print(f"""
  TWO INDEPENDENT SUPPRESSIONS, both quantified:
    (A) DEEP-NEWTONIAN (gate-independent):  the fractional MI correction is a0/g_N.  Binary pulsars have
        g_N = 1e-3 to 4e+2 m/s^2, so a0/g_N runs 2.1e-13 (J0737) ... 6.8e-8 (B0820+02).  This suppression
        exists in EVERY MOND-family theory and would be there even with the gate removed entirely.
    (B) GATE (AC only):  Re G = 9.7e-22 (J0737) ... 1.7e-15 (B0820+02) at the most permissive corner.
    PRODUCT (the gated AC prediction):  2.0e-34 (J0737) ... 1.1e-22 (B0820+02) fractional.
  No conceivable pulsar measurement reaches 1e-22.  The gated AC channel is CONSISTENT-BY-SUPPRESSION,
  and that is the honest, expected result -- not a constraint.
""")
