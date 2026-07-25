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

# ---------------------------------------------------------------------------------------------------
# 4.  PERIASTRON ADVANCE -- the sharpest binary-pulsar handle, computed TWICE (gated + DC)
# ---------------------------------------------------------------------------------------------------
head("4.  ANOMALOUS PERIASTRON ADVANCE:  gated (AC) vs hypothetical DC channel")
D2Y = (180.0 / np.pi) * YR          # rad/s -> deg/yr
print(f"""
  wdot_anom = delta_g_rel * sqrt(1-e^2) / (n a)      [Gauss secular, e cancels; validated REGRESSION #1]
  equivalently  wdot_anom / n = (delta_g_rel/g_N) sqrt(1-e^2)  -- the fractional-dynamics number directly.
  DC:    delta_g_rel = a0            (both bodies get +a0/2; Re G(0) = 1)
  GATED: delta_g_rel = a0 * Re G(n, omega_c^max)
  DEGENERACY, stated up front: wdot is the parameter used to MEASURE the total mass, so an anomalous
  wdot is absorbed by delta_M/M = 1.5 * wdot_anom/wdot_GR.  The non-degenerate signature is the resulting
  inconsistency in a SECOND post-Keplerian parameter; using Pbdot ~ M^(5/3) that is 2.5x the wdot ratio.
""")
print(f"  {'system':<17}{'footing':<8}{'wdot_anom DC [deg/yr]':>23}{'/wdot_GR':>11}{'/sigma(wdot)':>14}"
      f"{'PKcons/sigma':>14}{'wdot_anom GATED':>18}{'/sigma':>10}")
print("  " + "-" * 102)
prec = {}
for k in ("J0737-3039A/B", "B1913+16"):
    d = PSR[k]
    for f_, a0v in A0.items():
        wdot_gr_rad = d["wdot"] / D2Y
        w_dc = a0v * np.sqrt(1 - d["e"] ** 2) / (d["n"] * d["a"])
        w_gt = w_dc * ReG(d["n"], WINDOW[f_][1])
        r_gr = w_dc / wdot_gr_rad
        r_sig = (w_dc * D2Y) / d["swdot"]
        pk = 2.5 * r_gr / d["fPbdot"]
        prec[(k, f_)] = dict(dc=w_dc * D2Y, r_gr=r_gr, r_sig=r_sig, pk=pk, gt=w_gt * D2Y,
                             gsig=(w_gt * D2Y) / d["swdot"])
        print(f"  {k:<17}{f_:<8}{w_dc*D2Y:>23.3e}{r_gr:>11.2e}{r_sig:>14.2e}{pk:>14.2e}"
              f"{w_gt*D2Y:>18.2e}{(w_gt*D2Y)/d['swdot']:>10.2e}")
p0c = prec[("J0737-3039A/B", "canon")]
p0a = prec[("J0737-3039A/B", "alt")]
print(f"""
  GATED (AC) VERDICT:  the anomalous precession is {p0c['gsig']:.1e} of the double pulsar's wdot uncertainty
  (canon) / {p0a['gsig']:.1e} (alt) -- suppressed by Re G = {ReG(PSR['J0737-3039A/B']['n'], WC_C):.2e}.
  ==> CONSISTENT, GATED OFF, by ~22 orders.  NO CONSTRAINT.  Expected, and reported as such.

  DC-CHANNEL VERDICT -- and this is the genuinely interesting number in the pulsar sector:
    * raw:  the DC anomalous precession is {p0c['r_sig']*100:.2f}% (canon) / {p0a['r_sig']*100:.2f}% (alt) of
      sigma(wdot) for PSR J0737-3039.  That is only ~2 orders below a real, already-published measurement.
      Binary pulsars therefore come CLOSER to the DC channel than any lab or LLR test does -- but they do
      NOT reach it.  NOT excluded.
    * degeneracy-cleaned: absorbed into the total mass, the surviving PK inconsistency is {p0c['pk']:.1e}
      (canon) / {p0a['pk']:.1e} (alt) in units of the measured Pbdot consistency precision
      ({PSR['J0737-3039A/B']['fPbdot']:.1e} fractional) -- i.e. ~{-np.log10(p0c['pk']):.1f} orders short.  B1913+16 is weaker on both counts.
    * RANKING against the incumbent: planetary ephemerides exclude the same DC term by {mars_excl:.0f}x (Mars).
      A DC exclusion needs sensitivity BETTER than a0/2; J0737's wdot corresponds to a constant-acceleration
      sensitivity of delta_g <= {PSR['J0737-3039A/B']['swdot']/D2Y*PSR['J0737-3039A/B']['n']*PSR['J0737-3039A/B']['a']/np.sqrt(1-PSR['J0737-3039A/B']['e']**2):.2e} m/s^2, i.e. {A0['canon']/(PSR['J0737-3039A/B']['swdot']/D2Y*PSR['J0737-3039A/B']['n']*PSR['J0737-3039A/B']['a']/np.sqrt(1-PSR['J0737-3039A/B']['e']**2)):.2e} of what is needed, versus Mars at {A0['canon']/2/DG_MARS:.0f}x OVER.
      Mars is ~{(PSR['J0737-3039A/B']['swdot']/D2Y*PSR['J0737-3039A/B']['n']*PSR['J0737-3039A/B']['a']/np.sqrt(1-PSR['J0737-3039A/B']['e']**2))/DG_MARS:.1e}x more sensitive to a constant extra acceleration than the double pulsar is.
      ==> Binary pulsars add an INDEPENDENT but strictly WEAKER line on Fork C.  They neither exclude the
          DC channel nor rescue it; the exclusion, if it stands, is owned by the ephemerides.
""")

# ---------------------------------------------------------------------------------------------------
# 5.  CHANNEL 2 -- the gate's OWN causal shadow: a secular orbital drift, NOT suppressed by Re G
# ---------------------------------------------------------------------------------------------------
head("5.  THE GATE-FORCED SECULAR DRIFT (Im G):  Pbdot from d ln a/dt = a0 omega_c / g_N")
print(f"""
  This channel is neither gated-AC nor hypothetical-DC.  It is FORCED: Kramers-Kronig ties Im G to Re G,
  so any gate that suppresses the reactive tail must produce a dissipative secular drift (paper Sec. 5.2;
  derived from Im G in Section 1 above).  It is FREQUENCY-INDEPENDENT (the omega cancels) and scales as
  1/g_N -- so binary pulsars are BAD probes of it in tight orbits and potentially GOOD in wide ones.
      d ln a/dt = a0 omega_c / g_N   =>   Pbdot/Pb = (3/2) a0 omega_c / g_N   (Kepler, Pb ~ a^(3/2))
  Reference point: LLR binds omega_c from above using exactly this drift at g_N(Moon) = {gN_moon:.3e} m/s^2.
  ANY system with g_N < g_N(Moon) is intrinsically MORE sensitive per unit fractional-drift precision.
""")
print(f"  {'system':<17}{'g_N [m/s^2]':>13}{'g_N/g_N(Moon)':>15}{'dlnPb/dt [1/s]':>17}"
      f"{'Pbdot [s/s]':>14}{'sigma(Pbdot) needed':>21}{'resid over 20 yr':>18}")
print("  " + "-" * 102)
drift_rows = {}
for k, d in PSR.items():
    dl = 1.5 * A0["canon"] * WC_C / d["gN"]
    Pb_s = d["Pb"] * DAY
    pbdot = dl * Pb_s
    # cumulative orbital-phase timing residual after T: delta_t = (1/2)(Pbdot/Pb) T^2 * Pb/(2pi) x 2pi -> (1/2) dl T^2 Pb/Pb
    T20 = 20 * YR
    resid = 0.5 * dl * T20 ** 2 * (Pb_s / Pb_s)   # seconds of accumulated orbital-phase delay: (1/2) dl T^2
    drift_rows[k] = dict(dl=dl, pbdot=pbdot, resid=resid)
    print(f"  {k:<17}{d['gN']:>13.3e}{d['gN']/gN_moon:>15.3e}{dl:>17.3e}{pbdot:>14.3e}"
          f"{pbdot:>21.3e}{resid:>18.3e}")
j = drift_rows["J0737-3039A/B"]
sig_pbdot_j = PSR["J0737-3039A/B"]["fPbdot"] * abs(PSR["J0737-3039A/B"]["PbdotGR"])
print(f"""
  TIGHT SYSTEMS (the well-known tests):  J0737-3039  Pbdot_drift = {j['pbdot']:.2e} s/s  vs  measured
  sigma(Pbdot) = {sig_pbdot_j:.2e} s/s  ->  {j['pbdot']/sig_pbdot_j:.1e} of the uncertainty, i.e. {-np.log10(j['pbdot']/sig_pbdot_j):.1f} orders below
  detectability.  CONSISTENT, no constraint.  Same for B1913+16 ({drift_rows['B1913+16']['pbdot']/(PSR['B1913+16']['fPbdot']*abs(PSR['B1913+16']['PbdotGR'])):.1e} of sigma) and J1738+0333
  ({drift_rows['J1738+0333']['pbdot']/(PSR['J1738+0333']['fPbdot']*abs(PSR['J1738+0333']['PbdotGR'])):.1e}).  Reason: g_N is 1e5x the Moon's, so the drift is 1e5x smaller than the LLR-bounded one.

  WIDE SYSTEMS -- a genuinely UNTESTED and potentially COMPETITIVE channel [FORECAST, not a constraint]:
      PSR B0820+02 has g_N = {PSR['B0820+02']['gN']:.2e} m/s^2 = {PSR['B0820+02']['gN']/gN_moon:.2f} x the Moon's -- i.e. BELOW it.
      PSR J0337+1715 (outer)  g_N = {PSR['J0337+1715 out']['gN']:.2e} = {PSR['J0337+1715 out']['gN']/gN_moon:.2f} x the Moon's.
      At the band's top corner the predicted drifts are Pbdot = {drift_rows['B0820+02']['pbdot']:.2e} s/s (B0820+02) and
      {drift_rows['J0337+1715 out']['pbdot']:.2e} s/s (J0337 outer), accumulating {drift_rows['B0820+02']['resid']*1e3:.2f} ms and {drift_rows['J0337+1715 out']['resid']*1e3:.2f} ms of orbital-phase
      delay over 20 yr, {drift_rows['B0820+02']['resid']*1e3*4:.1f} ms / {drift_rows['J0337+1715 out']['resid']*1e3*4:.1f} ms over 40 yr (the drift residual grows as T^2).
      For a slow pulsar timed to ~1 ms and an MSP triple timed to ~1 us, those are AT or ABOVE the plausible
      residual floor.  So a long-baseline wide-binary-pulsar Pbdot fit is a REAL independent ceiling on
      omega_c -- the only pulsar observable in this ledger with that property.
      Required sensitivity to match the LLR ceiling (omega_c <= {(GDOT_LLR_2SIG/YR)*gN_moon/A0['canon']:.2e} rad/s):
        sigma(Pbdot) <= {drift_rows['B0820+02']['pbdot']:.2e} s/s for B0820+02, {drift_rows['J0337+1715 out']['pbdot']:.2e} s/s for J0337 outer.
  CAVEAT, load-bearing: real Pbdot in wide systems is dominated by the Shklovskii term (mu^2 d/c) and the
  Galactic differential acceleration.  Both must be subtracted with independent distance/proper-motion data,
  and that subtraction -- not the timing noise -- is what would actually limit this channel.  Stated as a
  forecast requiring that work, NOT as an achieved bound.
""")

# ---------------------------------------------------------------------------------------------------
# 6.  THE SECULAR-ACCELERATION CHANNEL:  Pbdot/Pb = a_los/c   -- the sharpest pulsar handle on a DC term
# ---------------------------------------------------------------------------------------------------
head("6.  SECULAR LINE-OF-SIGHT ACCELERATION:  the one pulsar channel with a0-scale sensitivity")
print(f"""
  A constant (DC) acceleration of the binary's BARYCENTRE along the line of sight is not absorbable:
      Pbdot/Pb = P dot/P = a_los / c        (the Doppler/Shklovskii-type secular term)
  So pulsar timing is a direct ACCELEROMETER.  Derived sensitivity from each system's own measured
  sigma(Pbdot), no literature acceleration numbers assumed:  sigma(a_los) = c sigma(Pbdot)/Pb.
""")
print(f"  {'system':<17}{'sigma(Pbdot) [s/s]':>20}{'Pb [s]':>12}{'sigma(a_los) [m/s^2]':>22}"
      f"{'vs a0/2 canon':>16}{'vs a0/2 alt':>14}")
print("  " + "-" * 102)
alos = {}
for k in ("J0737-3039A/B", "B1913+16", "J1738+0333"):
    d = PSR[k]
    sp_ = d["fPbdot"] * abs(d["PbdotGR"])
    Pb_s = d["Pb"] * DAY
    s_a = C_LIGHT * sp_ / Pb_s
    alos[k] = s_a
    print(f"  {k:<17}{sp_:>20.3e}{Pb_s:>12.1f}{s_a:>22.3e}"
          f"{(A0['canon']/2)/s_a:>15.1f}x{(A0['alt']/2)/s_a:>13.1f}x")
best = min(alos, key=alos.get)
print(f"""
  RESULT.  The double pulsar's Pbdot precision corresponds to a line-of-sight accelerometer at
      sigma(a_los) = {alos[best]:.2e} m/s^2      vs   a0/2 = {A0['canon']/2:.2e} (canon) / {A0['alt']/2:.2e} (alt)
  i.e. pulsar timing is ALREADY {(A0['canon']/2)/alos[best]:.0f}x (canon) / {(A0['alt']/2)/alos[best]:.0f}x (alt) more sensitive than the a0/2 scale.
  This is the ONLY pulsar observable in the ledger with sub-a0 sensitivity.  (Consistent with the published
  pulsar-acceleration literature working at 1e-12 - 1e-10 m/s^2 per pulsar; my number is derived, not read.)

  BUT -- and this decides the verdict -- WHICH acceleration does this channel probe?  The barycentre's
  acceleration is the GALACTIC one, and its direction rotates only with the system's GALACTIC orbit:
      omega_gal ~ V/R ~ 1e-15 rad/s  <<  omega_c ~ 2.2e-14   ->  Re G = {ReG(9.209e-16, WC_C):.4f}   GATE OPEN.
  So this channel does NOT test the hypothetical DC/Fork-C piece at all.  It tests the framework's
  ALREADY-LIVE, gate-open galactic prediction: at the solar circle y = g_gal/a0 = {2.15e-10/A0['canon']:.2f}, the framework's
  own kernel nu = sqrt(1+1/y) gives a boost of {np.sqrt(1+A0['canon']/2.15e-10)-1:.1%} (canon) / {np.sqrt(1+A0['alt']/2.15e-10)-1:.1%} (alt), an excess of
  {2.15e-10*(np.sqrt(1+A0['canon']/2.15e-10)-1):.2e} / {2.15e-10*(np.sqrt(1+A0['alt']/2.15e-10)-1):.2e} m/s^2 -- comfortably above sigma(a_los).
  HONEST VERDICT on that: NOT a constraint and NOT a win.  The measured a_los is compared to a GALACTIC
  MASS MODEL, and a uniform +20% enhancement is exactly degenerate with the disk+halo surface density
  (and with the Shklovskii term mu^2 d/c, which needs an independent distance).  It is also MOND-SHARED:
  every MOND-family theory with the same a0 predicts the same enhancement.  Live, degenerate, shared.
""")

# ---------------------------------------------------------------------------------------------------
# 7.  PTAs -- the gate corner, the GWB, and whether nHz is the closest precision approach
# ---------------------------------------------------------------------------------------------------
head("7.  PULSAR TIMING ARRAYS:  Re G in the nHz band, and the GWB")
pta = [("f = 400 nHz (Nyquist, 2-wk cadence)", 2*np.pi*400e-9), ("f = 30 nHz", 2*np.pi*30e-9),
       ("f = 10 nHz (GWB peak sensitivity)", 2*np.pi*10e-9), ("f = 1/(15 yr) = 2.11 nHz", 2*np.pi/(15*YR)),
       ("f = 1/(25 yr) = 1.27 nHz", 2*np.pi/(25*YR)), ("f = 1/(40 yr) = 0.79 nHz  [B1937+21 baseline]",
        2*np.pi/(40*YR))]
print(f"\n  {'PTA frequency':<46}{'omega [rad/s]':>14}{'omega/omega_c':>15}{'Re G canon':>13}{'Re G alt':>12}")
print("  " + "-" * 102)
for nm, om in pta:
    print(f"  {nm:<46}{om:>14.3e}{om/WC_C:>15.3e}{ReG(om, WC_C):>13.3e}{ReG(om, WC_A):>12.3e}")
w_low = 2 * np.pi / (40 * YR)
print(f"""
  (a) IS THE PTA BAND THE CLOSEST APPROACH TO THE CORNER?  Among AC/periodic high-precision channels: YES.
      lowest accessible PTA frequency  omega = {w_low:.2e} rad/s  ->  Re G = {ReG(w_low, WC_C):.2e}
      vs binary-pulsar orbits          Re G ~ 1e-21      ({ReG(w_low,WC_C)/9.66e-22:.0e}x closer)
      vs Earth/Saturn orbits           Re G ~ 1e-14/1e-11 ({ReG(w_low,WC_C)/1.232e-14:.0e}x / {ReG(w_low,WC_C)/1.069e-11:.1f}x)
      NOTE, deflating my own headline: Saturn's orbital frequency (6.8e-9 rad/s) is essentially the SAME as
      the lowest accessible PTA frequency (5.0e-9), so PTAs beat the outer planets on gate proximity by only
      1.8x.  The PTA advantage over binary pulsars is real and ~10 orders; the advantage over Saturn is not.
      vs lab (1 rad/s and up)          Re G <= 5e-28     ({ReG(w_low,WC_C)/ReG(1.0,WC_C):.0e}x closer)
      So the nHz band is ~10 orders closer to the corner than any binary-pulsar orbit and ~17-47 orders
      closer than any laboratory frequency.  That is a real, quantitative statement -- and it is still
      5.4 orders in FREQUENCY above omega_c, with Re G = 2e-11.  For a PTA observable to feel the corner it
      would need ~1e-11 fractional sensitivity to a MI-induced DYNAMICAL effect; nothing in PTA analysis
      has that.  And PTAs are NOT the closest channel overall: Gaia wide binaries sit at Re G ~ 1e-2 - 2e-1,
      nine orders closer, and the paper already names Gaia DR4 the decisive dataset.  Honest ranking:
          wide binaries  >>  galactic orbits (gate open)  >>  PTA nHz  >>  planets  >>  binary pulsars  >>  lab
      The most promising PULSAR channel is therefore NOT the AC gate; it is the secular/galactic channel of
      Section 6 (gate open by construction) and the Im G drift of Section 5.

  (b) THE GW BACKGROUND.  Two independent reasons the GWB carries no MI signal:
      1. SOURCE side: SMBHB orbits in band have f_orb ~ 1-100 nHz, so omega_orb ~ {2*np.pi*3e-9:.1e} rad/s and
         Re G ~ {ReG(2*np.pi*3e-9, WC_C):.1e}; and even ungated the deep-Newtonian fraction is tiny -- for M = 1e9 Msun at
         f_orb = 3 nHz, g_N = {(1e9*GM_SUN)/((1e9*GM_SUN/(2*np.pi*3e-9)**2)**(2/3)):.2e} m/s^2 so a0/g_N = {A0['canon']/((1e9*GM_SUN)/((1e9*GM_SUN/(2*np.pi*3e-9)**2)**(2/3))):.1e}.  Product ~ {A0['canon']/((1e9*GM_SUN)/((1e9*GM_SUN/(2*np.pi*3e-9)**2)**(2/3)))*ReG(2*np.pi*3e-9, WC_C):.1e}.
         Against a GWB amplitude uncertainty of tens of percent that is a factor {0.3/(A0['canon']/((1e9*GM_SUN)/((1e9*GM_SUN/(2*np.pi*3e-9)**2)**(2/3)))*ReG(2*np.pi*3e-9, WC_C)):.0e} too small to matter.
      2. PROPAGATION side, structural: the graviton rides g with c_T = 1 EXACT (paper Sec. 2.3), and the
         disformal photon metric is a separate, GW170817-excluded sector (paper Erratum v2) -- so GWB
         propagation and the timing-residual response are unmodified.  The MI kernel acts through X =
         |a|^2/a0^2, the body's own kinematic acceleration; a GW of strain h at omega_gw perturbs that by
         ~ (1/2) omega_gw^2 h L over an internal scale L.  For a neutron star (L ~ 1e4 m, h = 1e-15,
         omega_gw = {2*np.pi*10e-9:.1e}): delta|a| ~ {0.5*(2*np.pi*10e-9)**2*1e-15*1e4:.1e} m/s^2, i.e. {0.5*(2*np.pi*10e-9)**2*1e-15*1e4/A0['canon']:.1e} of a0.
         ==> The GWB is MI-BLIND.  No prediction, no constraint, in either channel.  (Caveat stated: the
         delta|a| estimate is gauge/scale-dependent; the structural c_T = 1 argument is the load-bearing one.)

  (c) OTHER PTA OBSERVABLES, checked and dismissed with numbers:
      * solar-system-barycentre / ephemeris systematics (the BayesEphem sector): this is the Earth's orbit,
        omega = {2*np.pi/YR:.2e} rad/s, Re G = {ReG(2*np.pi/YR, WC_C):.2e}, and its DC limb is ALREADY the paper's own
        INPOP/EPM constraint (Mars {mars_excl:.0f}x).  PTAs add nothing the ephemerides do not already own.
      * pulsar spin / spin-down: omega_spin ~ 1e2-4e3 rad/s, Re G ~ 1e-32; and the NS surface g ~ 1e12 m/s^2
        gives a0/g ~ 1e-22.  Dead twice over.
      * a secular ACCELERATION term common to the array (the "monopole" of the a_los channel): same physics
        as Section 6, gate OPEN, degenerate with the Galactic potential model.  Live but not discriminating.
""")

# ---------------------------------------------------------------------------------------------------
# 8.  CROSS-CUTTING: WEP -- is eta = 0 structural, and can the KERNEL ARGUMENT leak composition?
# ---------------------------------------------------------------------------------------------------
head("8.  WEP CROSS-NOTE (pulsar-sector anchor + the honest structural question)")
# MICROSCOPE orbit, and the nuclear-binding differential of its Ti / Pt test masses
R_MSC = 6.371e6 + 710e3
G_MSC = GM_EARTH / R_MSC ** 2
W_MSC = np.sqrt(GM_EARTH / R_MSC ** 3)
BA_TI, BA_PT, MU_N = 8.723, 7.921, 931.494      # MeV/nucleon, MeV -- [ADOPTED] standard nuclear data
d_bind = abs(BA_TI - BA_PT) / MU_N              # fractional binding-energy difference Ti-48 vs Pt-195
eta_dc_leak = d_bind * (A0["canon"] / G_MSC)
ETA_MSC_SIG = 2.3e-15
print(f"""
  PULSAR-SECTOR ANCHOR.  The strongest pulsar equivalence-principle test is the triple system
  PSR J0337+1715: Delta = (+0.5 +- 1.8)e-6 (Voisin+2020), |Delta| < 2.6e-6 at 95% (Archibald+2018), on the
  OUTER orbit where g_N = {PSR['J0337+1715 out']['gN']:.2e} m/s^2, y = {PSR['J0337+1715 out']['gN']/A0['canon']:.1e}.  A neutron star's gravitational
  binding is ~10-20% of its mass -- 2 orders MORE self-gravity contrast than MICROSCOPE's nuclear one.
  Framework prediction: Delta = 0 exactly, because the dressing W = s u.K(Box_u/a0^2)u carries NO
  matter-species label and multiplies the SAME rho_m that appears in T_munu.  PASS.  But note what the
  triple does and does not do: Delta is a DIFFERENTIAL, and a universal inertial correction produces none,
  so the triple tests the UNIVERSALITY of the correction and says nothing about its magnitude.

  THE HONEST STRUCTURAL QUESTION (calibration item 3), reasoned from the matter coupling:
   * The COEFFICIENT is structurally species-blind.  W multiplies rho_m, the total mass-energy density,
     which is also what sources gravity.  So binding energy, composition, and compactness are carried
     identically by the inertial and the gravitational side, to ALL orders.  eta = 0 is exact in the
     coefficient -- and the paper's 1e-12 residual is a grid artefact of evaluating K numerically, NOT a
     physical bound.  The derivation is tighter than its own machine check; that gap is bookkeeping.
   * The ARGUMENT of K is where a real opening sits, and the action as written does not close it.
     X = |a|^2/a0^2 must be evaluated on SOME worldline.  If evaluated per CONSTITUENT, a nucleon in a
     nucleus has |a| ~ 1e28 m/s^2 (y ~ 1e38), K -> 1, and MI would switch off for every composite body --
     MOND would never occur.  So the framework must evaluate K on the body's CENTRE-OF-MASS worldline.
     That CoM/internal split is NOT exact for a nonlinear K, and its residual is composition-dependent:
     the natural leak parameter is (fractional binding energy) x (the MI fractional size a0/g).
     SIZE OF A FIRST-ORDER LEAK, at MICROSCOPE (h = 710 km, g = {G_MSC:.2f} m/s^2, a0/g = {A0['canon']/G_MSC:.2e}):
       Ti-48 vs Pt-195 binding differential  = |{BA_TI} - {BA_PT}|/{MU_N} = {d_bind:.2e}
       eta_leak(DC, ungated)  ~ {d_bind:.2e} x {A0['canon']/G_MSC:.2e} = {eta_dc_leak:.2e}   vs MICROSCOPE sigma = {ETA_MSC_SIG:.1e}
                              = {eta_dc_leak/ETA_MSC_SIG:.1f} sigma          (alt footing: {d_bind*A0['alt']/G_MSC/ETA_MSC_SIG:.1f} sigma)
       eta_leak(GATED)        ~ x Re G(omega_orb = {W_MSC:.2e}) = {ReG(W_MSC, WC_C):.1e}  ->  {eta_dc_leak*ReG(W_MSC, WC_C):.1e}   = {eta_dc_leak*ReG(W_MSC, WC_C)/ETA_MSC_SIG:.1e} sigma
     READING, both ways: GATED, any such leak is invisible ({eta_dc_leak*ReG(W_MSC, WC_C)/ETA_MSC_SIG:.0e} sigma) -- consistent, no constraint.
     DC/ungated, a FIRST-ORDER leak would sit at ~{eta_dc_leak/ETA_MSC_SIG:.0f} sigma of MICROSCOPE, i.e. MARGINALLY EXCLUDED.
     So the DC channel does not merely have to survive the ephemerides; it must ALSO have an exactly
     structural CoM reduction with no first-order composition leak.  That is a second, independent
     structural demand on Fork C -- and it is a computable one (the CoM reduction of K on a bound system),
     currently unwritten.  Not a falsification: a named, sized, open computation.  This paragraph belongs
     to the WEP lane of the ledger; recorded here because the pulsar triple is its strong-field anchor.
""")

# ---------------------------------------------------------------------------------------------------
# 9.  VERDICT
# ---------------------------------------------------------------------------------------------------
head("9.  VERDICT -- binary pulsars + PTAs")
jw = prec[("J0737-3039A/B", "canon")]
print(f"""
  (a) BINARY PULSARS, GATED (AC) CHANNEL -- the answer the task expected, quantified:
      J0737-3039: two independent suppressions multiply.
        deep-Newtonian (gate-free)  a0/g_N       = {A0['canon']/PSR['J0737-3039A/B']['gN']:.2e}  (alt {A0['alt']/PSR['J0737-3039A/B']['gN']:.2e})
        gate at omega_orb = {PSR['J0737-3039A/B']['n']:.2e} rad/s   Re G = {ReG(PSR['J0737-3039A/B']['n'], WC_C):.2e}  (alt {ReG(PSR['J0737-3039A/B']['n'], WC_A):.2e})
        product (fractional MI correction to the orbit)  = {A0['canon']/PSR['J0737-3039A/B']['gN']*ReG(PSR['J0737-3039A/B']['n'], WC_C):.2e}  (alt {A0['alt']/PSR['J0737-3039A/B']['gN']*ReG(PSR['J0737-3039A/B']['n'], WC_A):.2e})
      Anomalous periastron advance = {jw['gt']:.2e} deg/yr = {jw['gsig']:.1e} of sigma(wdot).  Orbital decay from
      the same term is smaller still.  ==> CONSISTENT, GATED OFF BY ~22 ORDERS.  NO CONSTRAINT.  Honest and
      expected.  The deep-Newtonian factor alone (1e-13) is MOND-family-generic and would leave binary
      pulsars unconstraining even if the gate were deleted.

  (b) BINARY PULSARS, DC CHANNEL (Fork C) -- computed, and NOT excluded:
      DC anomalous precession = {jw['dc']:.2e} deg/yr = {jw['r_sig']*100:.2f}% of sigma(wdot) (canon) / {prec[('J0737-3039A/B','alt')]['r_sig']*100:.2f}% (alt);
      degeneracy-cleaned (mass-absorbed, read out in Pbdot) = {jw['pk']:.1e} of the Pbdot precision.
      Equivalent constant-acceleration sensitivity of the double pulsar (on delta_g_rel): {A0['canon']/jw['r_sig']:.2e} m/s^2,
      i.e. {1/jw['r_sig']:.0f}x WORSE than needed.  Mars is {(A0['canon']/jw['r_sig'])/DG_MARS:.1e}x more sensitive to the same term.
      ==> Binary pulsars are an INDEPENDENT but strictly WEAKER line on Fork C: they come within ~2 orders
          (raw) / ~3 orders (non-degenerate) of the DC term, whereas planetary ephemerides already exclude it
          by {mars_excl:.0f}x.  So pulsars neither exclude the DC channel nor rescue it.  The DC verdict stays
          owned by the ephemerides -- and per Section 8 the DC channel now carries a SECOND structural demand
          (an exactly composition-blind CoM reduction, else ~{eta_dc_leak/ETA_MSC_SIG:.0f} sigma at MICROSCOPE).
          Reading of the joint DC picture: if Fork C is the true physics, the framework is in trouble on the
          ephemerides by 3-4 orders; the framework's structural escape is that MI has NO DC channel, which is
          a constraint ON THE THEORY, not a free choice.  That is the ledger's contribution to Fork C.

  (c) PTAs:  the nHz band is the closest AC/periodic approach to the corner in the whole precision landscape
      (Re G = {ReG(w_low, WC_C):.1e} at 1/(40 yr), ~10 orders closer than binary orbits, ~17-47 orders closer than lab)
      -- but only 1.8x closer than Saturn's orbit, still 5.4 orders in frequency above omega_c, and no PTA
      observable has 1e-11 fractional sensitivity to a MI dynamical effect.  The GWB is MI-BLIND on two
      independent counts (source-side {A0['canon']/((1e9*GM_SUN)/((1e9*GM_SUN/(2*np.pi*3e-9)**2)**(2/3)))*ReG(2*np.pi*3e-9, WC_C):.0e}; propagation-side c_T = 1 exact).  PTAs do NOT reach the gate.
      Overall gate-proximity ranking:  wide binaries >> galactic orbits (OPEN) >> PTA nHz ~ Saturn >>
      binary pulsars >> lab.  Gaia DR4 wide binaries remain the decisive corner test, not PTAs.

  (d) THE TWO PULSAR CHANNELS THAT ARE ACTUALLY LIVE (both outside the AC gate):
      1. Secular a_los accelerometry.  Derived sigma(a_los) = {alos[best]:.2e} m/s^2 from J0737's Pbdot alone --
         {(A0['canon']/2)/alos[best]:.0f}x BELOW a0/2.  But the acceleration it probes is GALACTIC (omega ~ 1e-15 << omega_c,
         Re G = {ReG(9.209e-16, WC_C):.3f}, gate OPEN BY CONSTRUCTION), so it tests the framework's live +{np.sqrt(1+A0['canon']/2.15e-10)-1:.0%} boost, not
         Fork C.  Verdict: LIVE, MOND-SHARED, and degenerate with the Galactic mass model and the Shklovskii
         distance term.  Neither a constraint nor a win today.
      2. The Im G drift ceiling in WIDE binary pulsars.  d ln a/dt = a0 omega_c/g_N is frequency-independent
         and scales as 1/g_N, and PSR B0820+02 has g_N = {PSR['B0820+02']['gN']/gN_moon:.2f}x the Moon's -- BELOW the system LLR
         uses to set the window's upper edge.  Predicted Pbdot = {drift_rows['B0820+02']['pbdot']:.2e} s/s, {drift_rows['B0820+02']['resid']*1e3*4:.1f} ms of accumulated
         orbital-phase delay over 40 yr.  [FORECAST]  A Shklovskii-subtracted wide-binary Pbdot fit is a real
         independent ceiling on omega_c -- the single most useful thing the pulsar sector could contribute to
         this framework, and to my knowledge not yet done.  Not claimed as a bound here.

  SCOPE.  Dynamics sector (S_matter) only; the disformal photon sector is separately GW170817-excluded
  (paper Erratum v2) and is not used.  Both a0 footings carried on every load-bearing number.  omega_c is a
  free postulated fifth constant and nothing here upgrades it.  No door is claimed closed.
""")
print(RULE)
print("mi_pulsar_pta_precision_ledger_2026.py: 3 regressions + 5 machine checks passed; exit 0.")
print(RULE)
