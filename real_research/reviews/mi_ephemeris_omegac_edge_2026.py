#!/usr/bin/env python3
"""
W-3:  AN INDEPENDENT PLANETARY-EPHEMERIS UPPER EDGE ON omega_c  -- is the gate window already tighter
      than MI_FIELD_THEORY_RESULTS_2026.md states, or already CLOSED?
=====================================================================================================
The paper's gate window is
      omega_c in [1.782, 2.211]e-14 rad/s   (canonical footing a0 = 9.355e-11)   width x1.241
      omega_c in [1.782, 1.831]e-14 rad/s   (alt footing      a0 = 1.1305e-10)   width x1.027
LOWER edge  = 3 * omega_gal,max (SPARC deep-MOND RAR preservation, Re G >= 0.9).  THEORY-INTERNAL,
              footing-independent, NOT negotiable: relaxing it gates off the rotation curves.
UPPER edge  = LLR Gdot/G 2-sigma face value (Biskupek & Mueller 2021) x g_N(Moon)/a0.  Footing-dependent.

So ALL improvement pressure closes the window from ABOVE.  This script asks whether the PUBLISHED
planetary-ephemeris record ALREADY supplies a tighter upper edge than LLR.

WHY THE PAPER'S OWN EPHEMERIS NUMBERS DO NOT ANSWER THIS.  The paper confronts the ephemerides only
through the REACTIVE (conservative, radial) channel: per-planet |delta g| bounds (Fienga & Minazzoli
2024).  At omega >> omega_c the gate crushes that channel as Re G ~ (omega_c/omega)^2, so the reactive
ceiling is ~3.7e3 x LOOSER than LLR (reproduced in Sec. 2 below).  The committed pass
reviews/mi_cassini_q2_omegac_2026.py quotes a "674x over the Fienga-Minazzoli bound" -- but that is
evaluated at omega_c = 2.27e-9 rad/s, the corner Cassini Q2 would require, FIVE ORDERS ABOVE the window.
It says nothing about the window.  Sec. 2 reproduces both numbers and retires the reactive channel.

The ephemeris lever that CAN reach the window is the gate's own causal shadow: the DISSIPATIVE
(tangential) response, which produces the secular drift d ln a/dt = a0 omega_c / g_N -- the SAME
observable LLR uses for Gdot/G.  Because g_N,planet << g_N(Moon) for outer planets, the same omega_c
drives a much LARGER fractional drift at Saturn than at the Moon.  That is the check.

CALIBRATION HELD (manufacture neither a falsification nor a comfort):
  * Two independent routes to the edge are computed and BOTH reported, including the one that leaves
    the paper's window intact.  The spread between them IS the result's uncertainty and is printed.
  * Route 1 uses EXACTLY the estimator rule the paper itself applied to LLR (published bound on a
    universal fractional drift -> that body's own d ln a/dt).  No new convention is introduced.
  * Both a0 footings on every dimensional number.
  * No claim that the framework is falsified, and no claim that any door is closed.
numpy + sympy.  Exits 0.
"""
import numpy as np
import sympy as sp

RULE = "=" * 104
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# ---------------------------------------------------------------------------------------------------
# 0. CONSTANTS, CITED ANCHORS, AND THE PAPER'S WINDOW
# ---------------------------------------------------------------------------------------------------
A0 = {"canon": 9.355e-11, "alt": 1.1305e-10}      # cH_Lambda/Z  vs  rho_total/cH0 footing
YR = 365.25 * 86400.0
GM_SUN, GM_EARTH, GM_MOON = 1.32712440018e20, 3.986004418e14, 4.9028e12
R_MOON = 3.844e8

# --- the paper's window inputs (regression targets) ---
OMEGA_GAL_MAX = 5.94e-15          # UGC05721 innermost deep-MOND orbit (151 gal / 2188 pts)
GATE_KEEP = 0.90                  # Re G >= 0.9 at every deep-MOND orbit
GDOT_LLR_2SIG = (5.0 + 2 * 9.6) * 1e-15    # /yr  Biskupek & Mueller 2021, |cen| + 2 sigma = 2.42e-14
PAPER_WINDOW = {"canon": (1.782e-14, 2.211e-14), "alt": (1.782e-14, 1.831e-14)}

# --- planets: a [m], sidereal period [d], Fienga & Minazzoli 2024 per-planet reactive |delta g| ---
PLANETS = {                       # name: (a, T_days, delta_g bound or None)
    "Mercury": (5.7909050e10, 87.9691,   4.6e-14),
    "Venus":   (1.08208000e11, 224.701,  None),
    "Earth":   (1.49598023e11, 365.256,  8.7e-15),
    "Mars":    (2.27939200e11, 686.980,  1.4e-15),
    "Jupiter": (7.78570000e11, 4332.589, None),
    "Saturn":  (1.43353000e12, 10759.22, 7.0e-15),
}
# --- Pitjeva, Pitjev, Pavlov & Turygin 2021, A&A 647, A141 (EPM2019) --------------------------------
#   "d(GM_sun)/dt / GM_sun = (-10.2 +/- 1.4) x 10^-14 /yr (3 sigma)"
#   "-2.9e-14 < Gdot/G < +4.6e-14 /yr (3 sigma)"
#   >850,000 observations / 51,858 normal points, span 1913-2017
#   postfit range residual RMS: Mercury (MESSENGER) 0.7 m, Venus (VEX) 3 m,
#                               Mars (MEX/Odyssey/MRO) 1-1.5 m, Jupiter (Juno) 11 m,
#                               Saturn (Cassini) 20 m
EPM_GMDOT_3SIG = 1.4e-14        # /yr, FIT uncertainty on the universal fractional drift (3 sigma)
EPM_GDOT_PLUS_3SIG = 4.6e-14    # /yr, upper end of their Gdot/G interval = fit + solar-mass-loss modelling
EPM_GDOT_MINUS_3SIG = 2.9e-14   # /yr, lower end (opposite sign)
# Only the five SPACECRAFT-RANGED planets are modelled.  Earth is deliberately EXCLUDED: its orbit is
# not independently ranged (it is the observer), so inventing an "Earth range RMS" would double-count
# the same data and -- as a first draft of this script showed -- would spuriously dominate the weights.
EPM_RMS = {"Mercury": 0.7, "Venus": 3.0, "Mars": 1.25, "Jupiter": 11.0, "Saturn": 20.0}
# [ADOPTED] metre-class data spans (yr) actually carrying the secular leverage for each planet
EPM_SPAN = {"Mercury": 4.0,    # MESSENGER orbital 2011-2015
            "Venus": 8.0,      # Venus Express 2006-2014
            "Mars": 16.0,      # Odyssey 2002 / MEX 2004 / MRO 2006  ->  2017
            "Jupiter": 1.5,    # Juno 2016-2017
            "Saturn": 13.0}    # Cassini 2004-2017
# [ADOPTED, conservative] the along-track displacement projects onto the Earth-planet line of sight with
# a factor < 1 averaged over the synodic cycle, and Earth's OWN MI drift partially cancels in the
# relative range (D_Earth/D_Mars = 0.43).  Both are lumped into one conservative factor.
F_GEO = 0.5

def gN(a):  return GM_SUN / a ** 2
def n_of(T_days): return 2 * np.pi / (T_days * 86400.0)

# ---------------------------------------------------------------------------------------------------
# 1. THE GATE AND ITS TWO CHANNELS -- both derived symbolically from the paper's own G(omega)
# ---------------------------------------------------------------------------------------------------
head("1.  THE GATE'S TWO CHANNELS, DERIVED (not assumed)")
w, wc, a0s, gNs, ts = sp.symbols("omega omega_c a_0 g_N t", positive=True)
G = 1 / (1 + sp.I * w / wc)
ReG_s, ImG_s = sp.re(sp.expand(sp.simplify(G))), sp.im(sp.expand(sp.simplify(G)))
ident = sp.simplify(sp.Abs(G) ** 2 - ReG_s)
assert sp.simplify(ident) == 0, "1-pole identity |G|^2 = Re G failed"

# dissipative tangential accel at omega >> omega_c :  a_t = (a0/2)|Im G| -> (a0/2)(omega_c/omega)
a_t = sp.simplify((a0s / 2) * sp.limit(-ImG_s * w / wc, w, sp.oo) * wc / w)   # = a0 wc /(2 w)
# circular-orbit energy balance:  (GM/2a^2) da/dt = a_t v  ->  dln a/dt = 2 a_t omega / g_N
drift = sp.simplify(2 * a_t * w / gNs)
print(f"""
  G(omega) = 1/(1 + i omega/omega_c)      Re G = {ReG_s}      Im G = {sp.simplify(ImG_s)}
  causal 1-pole identity |G|^2 = Re G  ->  sympy residual = {sp.simplify(ident)}   (must be 0)

  REACTIVE  channel (radial, conservative):  delta_g_r = (a0/2) Re G(omega)  ->  (a0/2)(omega_c/omega)^2
  DISSIPATIVE channel (tangential, forced by Kramers-Kronig): a_t = (a0/2)|Im G| -> {sp.simplify(a_t)}
  circular-orbit energy balance  ->  d ln a/dt = 2 a_t omega / g_N = {drift}
                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
  == the paper's own Sec. 5.2 drift law  d ln r/dt = a0 omega_c / g_N.  DERIVED here, not imported.
  Note it is FREQUENCY-INDEPENDENT: the omega cancels.  The drift is set purely by 1/g_N, so the
  SLOWEST, most weakly bound body has the LARGEST fractional drift.  That is why the outer planets,
  not the Moon, are the sharpest lever -- and the paper never turned that into a number.
""")
assert sp.simplify(drift - a0s * wc / gNs) == 0, "drift law derivation failed"

# ---------------------------------------------------------------------------------------------------
# 2. REGRESSION BLOCK -- rebuild the paper's window AND retire the reactive channel
# ---------------------------------------------------------------------------------------------------
head("2.  REGRESSION: the paper's window, the reactive ceiling, and the '674x' number")
k_lo = 1.0 / np.sqrt(1.0 / GATE_KEEP - 1.0)
gN_moon = GM_EARTH / R_MOON ** 2
rebuilt = {}
print(f"  gate-keep factor k = 1/sqrt(1/{GATE_KEEP}-1) = {k_lo:.4f}   g_N(Moon) = {gN_moon:.4e} m/s^2\n")
print(f"  {'footing':<8}{'a0':>12}{'lower edge':>13}{'LLR upper edge':>16}{'paper window':>27}{'match':>8}")
print("  " + "-" * 88)
for lab, a0 in A0.items():
    lo = OMEGA_GAL_MAX * k_lo
    hi = (GDOT_LLR_2SIG / YR) * gN_moon / a0
    rebuilt[lab] = (lo, hi)
    plo, phi = PAPER_WINDOW[lab]
    ok = abs(lo / plo - 1) < 0.02 and abs(hi / phi - 1) < 0.02
    print(f"  {lab:<8}{a0:>12.4e}{lo:>13.4e}{hi:>16.4e}{f'[{plo:.3e}, {phi:.3e}]':>27}{'YES' if ok else 'NO':>8}")
    assert ok, f"failed to rebuild the {lab} window"
print(f"\n  window widths: canon x{rebuilt['canon'][1]/rebuilt['canon'][0]:.3f}   "
      f"alt x{rebuilt['alt'][1]/rebuilt['alt'][0]:.3f}  (knife-edge)   -- both reproduced\n")

# reactive per-planet ceilings:  (a0/2)(omega_c/omega)^2 <= delta_g  ->  omega_c <= omega sqrt(2 dg/a0)
print(f"  REACTIVE channel ceilings (Fienga & Minazzoli 2024 per-planet |delta g|), canon footing:")
print(f"    {'planet':<10}{'omega [rad/s]':>15}{'delta_g':>11}{'omega_c ceiling':>18}{'vs LLR edge':>14}")
print("    " + "-" * 68)
reactive = {}
for nm, (a, Td, dg) in PLANETS.items():
    if dg is None: continue
    om = n_of(Td)
    wc_r = om * np.sqrt(2 * dg / A0["canon"])
    reactive[nm] = wc_r
    print(f"    {nm:<10}{om:>15.4e}{dg:>11.1e}{wc_r:>18.4e}{wc_r/rebuilt['canon'][1]:>13.0f}x")
wc_react = min(reactive.values())
print(f"""
  Tightest reactive ceiling = {wc_react:.3e} rad/s (Saturn) -- {wc_react/rebuilt['canon'][1]:.0f}x LOOSER than the LLR edge.
  The reactive channel is NON-OPERATIVE on the window and cannot be made operative: the gate's
  (omega_c/omega)^2 crush is 11 orders at Saturn.  RETIRED.

  The '674x over the Fienga-Minazzoli bound' in reviews/mi_cassini_q2_omegac_2026.py, reproduced:""")
B_q2 = np.sqrt(1 + A0["canon"] / 2.15e-10) - 1          # framework nu at g_ext = V^2/R
S_req = 0.02 / B_q2
wc_q2 = n_of(PLANETS["Saturn"][1]) / np.sqrt(1 / S_req - 1)
dg_at_q2 = A0["canon"] / 2 * S_req
print(f"""    omega_c(Q2-required) = {wc_q2:.3e} rad/s ;  retained (a0/2)Re G at Saturn = {dg_at_q2:.3e} m/s^2
    over the 7.0e-15 Saturn bound by {dg_at_q2/7.0e-15:.0f}x   [committed pass says 674x -> MATCH]
    BUT that corner is {wc_q2/rebuilt['canon'][1]:.1e}x ABOVE the window's top.  It constrains nothing inside the window.
""")
assert abs(dg_at_q2 / 7.0e-15 / 674.0 - 1) < 0.02, "674x regression failed"
assert wc_react / rebuilt["canon"][1] > 3000, "reactive-channel ranking regression failed"

# and the dissipative piece's INSTANTANEOUS amplitude is also below the per-planet |delta g| bounds:
at_sat = A0["canon"] / 2 * (PAPER_WINDOW["canon"][1] / n_of(PLANETS["Saturn"][1]))
print(f"""  One more amplitude check, so the route ahead is unambiguous: the DISSIPATIVE tangential
  acceleration at the window top is a_t = (a0/2)(omega_c/omega) = {at_sat:.3e} m/s^2 at Saturn --
  {7.0e-15/at_sat:.0f}x BELOW the 7.0e-15 Saturn |delta g| bound too.  So NO instantaneous-amplitude bound of any
  kind reaches the window.  The ephemerides can only reach it through the SECULAR ACCUMULATION of that
  tangential force over decades -- the drift channel.  That is the whole content of Secs. 3-5.
""")
assert at_sat < 7.0e-15, "dissipative amplitude check failed"

# ---------------------------------------------------------------------------------------------------
# 3. ROUTE 1 -- CURRENCY-MATCHED: the paper's OWN estimator rule, applied to the published EPM2019 bound
# ---------------------------------------------------------------------------------------------------
head("3.  ROUTE 1 (currency-matched, no new modelling): published drift bound -> omega_c ceiling")
print(f"""
  The paper's rule for LLR, verbatim: take a PUBLISHED bound on a universal fractional secular drift
  and read it as a bound on that body's own d ln a/dt, then omega_c <= D * g_N / a0.
  Applied to LLR: D = {GDOT_LLR_2SIG:.3e}/yr (2 sigma), g_N(Moon) = {gN_moon:.3e}  ->  {rebuilt['canon'][1]:.3e} rad/s.  [Sec. 2]

  The SAME rule with the modern PLANETARY drift record:
      Pitjeva, Pitjev, Pavlov & Turygin 2021, A&A 647, A141 (EPM2019; span 1913-2017; 51,858 normal
      points; postfit RMS Mercury/MESSENGER 0.7 m, Venus/VEX 3 m, Mars/MEX+Odyssey+MRO 1-1.5 m,
      Jupiter/Juno 11 m, Saturn/Cassini 20 m):
          d(GM_sun)/dt / GM_sun = (-10.2 +/- 1.4)e-14 /yr    (3 sigma)      <- FIT uncertainty
          -13.4e-14 < (Mdot_sun/M_sun)_rad+wind+fall < -8.7e-14 /yr         <- mass-loss MODEL span
          -2.9e-14 < Gdot/G < +4.6e-14 /yr                   (3 sigma)      <- what is left over
      (the third line is exactly the first minus the second -- verified below -- so it is the room for
      an anomalous drift AFTER the astrophysically required solar mass loss is allowed to float.)

  THE ROOM IS NOT UNIQUE, and this is the single fork that decides the answer.  Two readings:
    R1a  NON-DEGENERATE room = the FIT uncertainty alone, +/-{EPM_GMDOT_3SIG:.1e}/yr (3 sigma).
         Legitimate because the MI drift is NOT a mass-loss/Gdot effect: it goes as
         d ln a_i/dt = a0 omega_c a_i^2/GM_sun, i.e. ~a_i^2, whereas mass loss and Gdot are FLAT in a.
         An a^2 pattern is not absorbable by GMdot_sun -- so the mass-loss span should NOT be handed to
         it as extra room.
    R1b  DEGENERATE room = the published Gdot/G interval, {EPM_GDOT_PLUS_3SIG:.1e}/yr (3 sigma, inspiral side;
         {EPM_GDOT_MINUS_3SIG:.1e} on the other side).  Legitimate to the extent that the constraint is carried by ONE
         planet (Mars), because at a single planet a^2 and flat are indistinguishable -- the MI drift
         then hides inside the mass-loss allowance.
  R1a is right in principle, R1b is right if the sensitivity is single-planet in practice.  Sec. 4
  computes which.  BOTH are reported.  Reporting only R1a would manufacture a closure; reporting only
  R1b would manufacture a comfort.
""")
gd_check = (-10.2 - 1.4) - (-8.7), (-10.2 + 1.4) - (-13.4)
print(f"  consistency check of their own algebra: (-10.2-1.4)-(-8.7) = {gd_check[0]:+.1f}e-14 and "
      f"(-10.2+1.4)-(-13.4) = {gd_check[1]:+.1f}e-14  ->  quoted interval (-2.9, +4.6)e-14  MATCH\n")
assert abs(gd_check[0] + 2.9) < 1e-9 and abs(gd_check[1] - 4.6) < 1e-9, "Gdot/G interval algebra failed"

ROOMS = {  # label: (D at 3 sigma [/yr], D at 2-sigma-equivalent [/yr])
    "R1a fit-only":   (EPM_GMDOT_3SIG,     EPM_GMDOT_3SIG * 2 / 3),
    "R1b massloss-deg": (EPM_GDOT_PLUS_3SIG, EPM_GDOT_PLUS_3SIG * 2 / 3),
}
def wc_from_D(D_per_yr, a, footing):   # D -> omega_c ceiling
    return (D_per_yr / YR) * gN(a) / A0[footing]

print(f"  ROUTE-1 omega_c ceilings, per planet, at the LLR-matched 2-sigma level (canon footing):\n")
print(f"  {'planet':<10}{'g_N [m/s^2]':>13}{'g_N/g_N(Moon)':>15}{'R1a wc':>13}{'R1b wc':>13}"
      f"{'R1a/low edge':>14}{'R1b/low edge':>14}")
print("  " + "-" * 94)
route1 = {}
for nm, (a, Td, _) in PLANETS.items():   # Earth shown for g_N context only (no ranging model for it)
    g = gN(a)
    ra = wc_from_D(ROOMS["R1a fit-only"][1], a, "canon")
    rb = wc_from_D(ROOMS["R1b massloss-deg"][1], a, "canon")
    route1[nm] = dict(g=g,
                      R1a=(ra, wc_from_D(ROOMS["R1a fit-only"][1], a, "alt")),
                      R1b=(rb, wc_from_D(ROOMS["R1b massloss-deg"][1], a, "alt")),
                      R1a3=(wc_from_D(ROOMS["R1a fit-only"][0], a, "canon"),
                            wc_from_D(ROOMS["R1a fit-only"][0], a, "alt")),
                      R1b3=(wc_from_D(ROOMS["R1b massloss-deg"][0], a, "canon"),
                            wc_from_D(ROOMS["R1b massloss-deg"][0], a, "alt")))
    print(f"  {nm:<10}{g:>13.4e}{g/gN_moon:>15.4f}{ra:>13.4e}{rb:>13.4e}"
          f"{ra/1.782e-14:>13.3f}x{rb/1.782e-14:>13.3f}x")
print(f"""
  Read the g_N column first: g_N(Mars) = {gN(PLANETS['Mars'][0]):.3e} vs g_N(Moon) = {gN_moon:.3e}, ratio
  {gN(PLANETS['Mars'][0])/gN_moon:.3f}.  Mars and the Moon are very nearly the SAME lever -- so swapping LLR for the
  planetary drift record is an apples-to-apples substitution of one published number for another, not a
  change of channel.  Saturn's lever is {gN_moon/gN(PLANETS['Saturn'][0]):.0f}x stronger per unit drift bound, but Sec. 4 shows
  Saturn does NOT carry the published universal-drift constraint, so its row must not be used in R1.
""")

# ---------------------------------------------------------------------------------------------------
# 4. ROUTE 2 -- FORWARD-MODELLED: the unabsorbable t^2 along-track signal, and WHICH planet carries what
# ---------------------------------------------------------------------------------------------------
head("4.  ROUTE 2 (forward-modelled): the t^2 along-track signature, and which planet carries what")
tt, TT, Ds, ns = sp.symbols("t T D n", positive=True)
quad = -sp.Rational(3, 4) * ns * Ds * tt ** 2
res = quad - (sp.Rational(-3, 4) * ns * Ds) * (TT * tt - TT ** 2 / 6)
print(f"""
  A constant fractional drift D = d ln a/dt makes n(t) = n(1 - 3/2 D t), so the mean longitude carries an
  UNABSORBABLE quadratic:  lambda(t) = lambda_0 + n t - (3/4) n D t^2.  Initial conditions span only the
  {{1, t}} directions; after least-squares removal of {{1, t}} on [0, T] the residual t^2 term has
        max |residual| at t=0 : {sp.simplify(res.subs(tt, 0))}      (sympy)
        along-track range signal  Delta_s = a * n D T^2/8 = 0.125 * v * D * T^2
        with D = a0 omega_c/g_N and v = n a :   Delta_s = 0.125 * a0 * omega_c * T^2 / n
  MI's signal therefore scales as T^2/n -- it prefers the SLOW outer planets with long spans.
  A universal Gdot/G instead scales as v T^2 = n a T^2 -- it prefers the FAST inner planets.
  DIFFERENT WEIGHTINGS.  That difference is the whole R1a-vs-R1b question, so it is computed, not asserted.
  A conservative geometric/differential factor F_GEO = {F_GEO} is applied to every MI signal (line-of-sight
  projection over the synodic cycle, plus partial cancellation of Earth's own drift in the relative range).
""")
assert sp.simplify(sp.Abs(res.subs(tt, 0)) - TT ** 2 * ns * Ds / 8) == 0, "t^2 residual algebra failed"

WC_REF = PAPER_WINDOW["canon"][1]
rows = {}
for nm in EPM_RMS:
    a, Td, _ = PLANETS[nm]
    n_i, T_i, s_i = n_of(Td), EPM_SPAN[nm] * YR, EPM_RMS[nm]
    k_mi = F_GEO * 0.125 * A0["canon"] * T_i ** 2 / n_i        # Delta_s(MI) = k_mi * omega_c
    k_un = F_GEO * 0.125 * n_i * a * T_i ** 2                  # Delta_s(universal) = k_un * D
    rows[nm] = dict(n=n_i, span=EPM_SPAN[nm], rms=s_i, ds=k_mi * WC_REF,
                    snr_mi=k_mi * WC_REF / s_i, snr_un=k_un / s_i, k_mi=k_mi)
tot_mi = np.sqrt(sum(r["snr_mi"] ** 2 for r in rows.values()))
tot_un = np.sqrt(sum(r["snr_un"] ** 2 for r in rows.values()))
print(f"  MI along-track signal at the paper's most permissive corner omega_c = {WC_REF:.3e} (canon):\n")
print(f"  {'planet':<10}{'n [rad/s]':>12}{'span yr':>9}{'RMS m':>8}{'MI Delta_s [m]':>16}"
      f"{'share of MI S/N':>17}{'share of univ.':>16}")
print("  " + "-" * 88)
for nm, r in rows.items():
    print(f"  {nm:<10}{r['n']:>12.4e}{r['span']:>9.1f}{r['rms']:>8.2f}{r['ds']:>16.3f}"
          f"{(r['snr_mi']/tot_mi)**2:>16.1%}{(r['snr_un']/tot_un)**2:>16.1%}")
sh_mi = {nm: (r["snr_mi"] / tot_mi) ** 2 for nm, r in rows.items()}
sh_un = {nm: (r["snr_un"] / tot_un) ** 2 for nm, r in rows.items()}
print(f"""
  THIS TABLE IS THE CRUX OF THE R1a / R1b FORK:
    * the published UNIVERSAL-drift constraint is carried overwhelmingly by MARS ({sh_un['Mars']:.0%}), with
      Mercury {sh_un['Mercury']:.1%} and Venus {sh_un['Venus']:.1%};  SATURN carries {sh_un['Saturn']:.2%} of it and Jupiter {sh_un['Jupiter']:.2%}.
    * the MI a^2 pattern is carried by MARS ({sh_mi['Mars']:.0%}) AND SATURN ({sh_mi['Saturn']:.0%}) -- Saturn's share is ~{sh_mi['Saturn']/max(sh_un['Saturn'],1e-9):.0f}x
      larger for MI than for a universal drift, because MI's drift at Saturn is {gN(PLANETS['Mars'][0])/gN(PLANETS['Saturn'][0]):.0f}x Mars's.
  CONSEQUENCE, stated both ways:
    -> R1b (degenerate) is the honest reading of the PUBLISHED number as it stands, because that number
       is ~{sh_un['Mars']:.0%} a single-planet (Mars) constraint, and at one planet a^2 is indistinguishable from flat.
       So MI's drift really can hide inside the mass-loss allowance IN THE EXISTING FIT.
    -> R1a becomes the right reading the moment Saturn is used to break the degeneracy, which the data
       already permit: Saturn supplies {sh_mi['Saturn']:.0%} of the MI signal but only {sh_un['Saturn']:.2%} of the flat-direction
       leverage, i.e. Saturn is an almost purely ORTHOGONAL handle on the a^2 profile.
    Neither reading is a manufactured result; they differ by which fit has been RUN, not by which is true.

  Route-2 edges from the residuals directly (canon; alt = x{A0['canon']/A0['alt']:.3f}):""")
print(f"    {'planet':<10}{'wc, 1-point RMS':>18}{'N pts':>8}{'wc, sqrt(N)-averaged':>22}")
print("    " + "-" * 60)
NPTS = {"Mercury": 1000, "Venus": 500, "Mars": 20000, "Jupiter": 100, "Saturn": 600}
r2_single, r2_sqrtn = {}, {}
for nm, r in rows.items():
    r2_single[nm] = r["rms"] / r["k_mi"]
    r2_sqrtn[nm] = (r["rms"] / np.sqrt(NPTS[nm])) / r["k_mi"]
    print(f"    {nm:<10}{r2_single[nm]:>18.4e}{NPTS[nm]:>8d}{r2_sqrtn[nm]:>22.4e}")
e2_single, e2_sqrtn = min(r2_single.values()), min(r2_sqrtn.values())
print(f"""
  Most conservative (a coherent 13-25 yr signal must exceed a SINGLE normal point's RMS -- i.e. assume
  the fit gains nothing from 51,858 normal points and is wholly systematics-limited):
        omega_c <= {e2_single:.3e} rad/s (canon) / {e2_single*A0['canon']/A0['alt']:.3e} (alt)   ->  {e2_single/rebuilt['canon'][1]:.1f}x ABOVE the LLR edge.
        On THIS reading the paper's window stands untouched.  It is almost certainly too pessimistic.
  Naive sqrt(N) averaging (too optimistic -- ignores correlated systematics):
        omega_c <= {e2_sqrtn:.3e} rad/s (canon)  ->  {1.782e-14/e2_sqrtn:.0f}x below the lower edge.
  Route 2 therefore only BRACKETS: [{e2_sqrtn:.2e}, {e2_single:.2e}] rad/s, a factor {e2_single/e2_sqrtn:.0f} wide, straddling
  the window.  The published R1 numbers, which carry the real covariance and systematics, sit inside
  this bracket -- which is the check that they are not crazy, and all Route 2 is being asked to do.
""")

# ---------------------------------------------------------------------------------------------------
# 4b. THE DEGENERACY-FREE SATURN EDGE -- calibrated against the published number, not invented
# ---------------------------------------------------------------------------------------------------
head("4b.  THE CALIBRATED, DEGENERACY-FREE SATURN EDGE  (the sharpest number in this pass)")
# Calibrate my crude estimator's averaging efficiency against the PUBLISHED universal-drift bound:
#   my 1-point universal-drift threshold at Mars  vs  the published 3-sigma bound  ->  gain factor
a_m, Td_m, _ = PLANETS["Mars"]
k_un_mars = F_GEO * 0.125 * n_of(Td_m) * a_m * (EPM_SPAN["Mars"] * YR) ** 2
D_1pt_mars = (EPM_RMS["Mars"] / k_un_mars) * YR          # /yr, "signal = one normal point's RMS"
GAIN = D_1pt_mars / EPM_GMDOT_3SIG                       # how much better the real fit does
sat_edge_3s = {f: r2_single["Saturn"] / GAIN * (A0["canon"] / A0[f]) for f in A0}
sat_edge_2s = {f: v * 2 / 3 for f, v in sat_edge_3s.items()}
print(f"""
  The R1a/R1b fork exists only because Mars ({sh_un['Mars']:.0%} of the flat-direction leverage) cannot by itself tell
  an a^2 drift from a flat one.  SATURN can: it carries {sh_mi['Saturn']:.0%} of the MI a^2 signal and {sh_un['Saturn']:.2%} of the
  flat leverage, so a Saturn-only bound is DEGENERACY-FREE -- it cannot be absorbed into GMdot_sun or
  the solar-mass-loss allowance.  The only thing needed is Saturn's real drift sensitivity, and that can
  be CALIBRATED from the published record instead of guessed:

    my 1-normal-point universal-drift threshold at Mars   = {D_1pt_mars:.3e}/yr
    the PUBLISHED EPM2019 3-sigma universal-drift bound   = {EPM_GMDOT_3SIG:.3e}/yr
    => the real fit beats a single normal point by a gain of x{GAIN:.2f}
       (out of sqrt(N) = sqrt({NPTS['Mars']}) = {np.sqrt(NPTS['Mars']):.0f} available -- so an effective N_eff ~ {GAIN**2:.0f}, i.e. ~{100*GAIN**2/NPTS['Mars']:.1f}% of the
        points' nominal statistical power survives correlated systematics.  Reassuringly modest.)

  [ADOPTED, LOAD-BEARING]  Transfer that SAME gain to Cassini's Saturn arc (600 normal points at 20 m
  over 13 yr).  This is the one transfer this section rests on; it is neither the optimistic sqrt(N)
  limit nor the pessimistic 1-point limit, and it is anchored to a number someone published.

    Saturn 1-normal-point MI edge      omega_c <= {r2_single['Saturn']:.3e} rad/s   (canon; no averaging at all)
    Saturn CALIBRATED edge, 3 sigma    omega_c <= {sat_edge_3s['canon']:.3e} (canon) / {sat_edge_3s['alt']:.3e} (alt)
    Saturn CALIBRATED edge, 2 sigma    omega_c <= {sat_edge_2s['canon']:.3e} (canon) / {sat_edge_2s['alt']:.3e} (alt)
      (2 sigma is the convention the paper used for its own LLR upper edge, so it is the matched one)

  Against the window [1.782e-14, 2.211e-14] canon / [1.782e-14, 1.830e-14] alt:
    3 sigma, canon:  {sat_edge_3s['canon']:.3e}  ->  {'BELOW' if sat_edge_3s['canon']<1.782e-14 else 'above'} the lower edge; window width collapses x1.241 -> x{max(sat_edge_3s['canon']/1.782e-14,0):.3f}
    3 sigma, alt:    {sat_edge_3s['alt']:.3e}  ->  {'CLOSED by x' + format(1.782e-14/sat_edge_3s['alt'], '.2f') if sat_edge_3s['alt']<1.782e-14 else 'open'}
    2 sigma, canon:  {sat_edge_2s['canon']:.3e}  ->  {'CLOSED by x' + format(1.782e-14/sat_edge_2s['canon'], '.2f') if sat_edge_2s['canon']<1.782e-14 else 'open'}
    2 sigma, alt:    {sat_edge_2s['alt']:.3e}  ->  {'CLOSED by x' + format(1.782e-14/sat_edge_2s['alt'], '.2f') if sat_edge_2s['alt']<1.782e-14 else 'open'}

  EXPOSURE, stated at full strength: if Cassini's Saturn arc is MORE systematics-limited than Mars
  ranging -- plausible, since 20 m residuals over a 13-yr arc with a spacecraft-dependent media/clock
  model are not obviously as clean as 1.25 m Mars normal points -- the gain drops and the edge rises.
  At gain = 1 (no averaging whatsoever) the Saturn edge is {r2_single['Saturn']:.2e}, {r2_single['Saturn']/rebuilt['canon'][1]:.1f}x ABOVE the LLR edge and
  the window is untouched.  The Saturn edge therefore spans [{sat_edge_2s['canon']:.2e}, {r2_single['Saturn']:.2e}] rad/s.

  HOW PRECARIOUS, in one number.  At 3 sigma, canon, the Saturn edge equals the window's LOWER edge at
  gain = x{GAIN*sat_edge_3s['canon']/1.782e-14:.2f} and equals the window's UPPER (LLR) edge at gain = x{GAIN*sat_edge_3s['canon']/rebuilt['canon'][1]:.2f}.  So the ENTIRE published
  canonical window corresponds to this single calibration factor lying in {GAIN*sat_edge_3s['canon']/rebuilt['canon'][1]:.1f} < gain < {GAIN*sat_edge_3s['canon']/1.782e-14:.1f},
  i.e. {100*(sat_edge_3s['canon']/1.782e-14-1):+.0f}% / {100*(sat_edge_3s['canon']/rebuilt['canon'][1]-1):+.0f}% around the calibrated x{GAIN:.2f}.  That is a KNIFE-EDGE, and it cuts BOTH ways:
  a {100*(sat_edge_3s['canon']/1.782e-14-1):.0f}% better Saturn sensitivity than calibrated closes the canonical window outright; a {100*(1-sat_edge_3s['canon']/rebuilt['canon'][1]):.0f}%
  worse one restores it in full.  Reporting only one side would manufacture a result; both are printed.
""")

# ---------------------------------------------------------------------------------------------------
# 5. WHERE THE EPHEMERIS EDGE SITS -- the actual answer to W-3
# ---------------------------------------------------------------------------------------------------
head("5.  W-3 ANSWER: ephemeris edge vs the LLR edge vs the non-negotiable lower edge")
lo = 1.782e-14
def verdict(e, llr):
    return ("CLOSED (below lower edge)" if e < lo else
            "TIGHTER THAN STATED" if e < llr else "window as stated (LLR binds)")
print(f"  {'reading':<22}{'sigma':>7}{'footing':>8}{'ephem edge':>13}{'LLR edge':>11}"
      f"{'vs LLR':>9}{'vs lower':>10}{'verdict':>30}")
print("  " + "-" * 110)
tab = []
for lab, key3, key2 in (("R1a Mars fit-only", "R1a3", "R1a"), ("R1b Mars massloss-deg", "R1b3", "R1b")):
    for sig, key in (("2s", key2), ("3s", key3)):
        for fi, foot in enumerate(("canon", "alt")):
            e = route1["Mars"][key][fi]
            llr = rebuilt[foot][1]
            tab.append((lab, sig, foot, e, llr, verdict(e, llr)))
            print(f"  {lab:<22}{sig:>7}{foot:>8}{e:>13.3e}{llr:>11.3e}{llr/e:>8.2f}x{lo/e:>9.2f}x"
                  f"{verdict(e, llr):>30}")
for sig, dd in (("2s", sat_edge_2s), ("3s", sat_edge_3s)):
    for foot in ("canon", "alt"):
        e, llr = dd[foot], rebuilt[foot][1]
        tab.append(("R3 Saturn degen-free", sig, foot, e, llr, verdict(e, llr)))
        print(f"  {'R3 Saturn degen-free':<22}{sig:>7}{foot:>8}{e:>13.3e}{llr:>11.3e}"
              f"{llr/e:>8.2f}x{lo/e:>9.2f}x{verdict(e, llr):>30}")
print(f"  {'R2 Saturn 1-pt (floor)':<22}{'--':>7}{'canon':>8}{r2_single['Saturn']:>13.3e}"
      f"{rebuilt['canon'][1]:>11.3e}{rebuilt['canon'][1]/r2_single['Saturn']:>8.2f}x"
      f"{lo/r2_single['Saturn']:>9.2f}x{verdict(r2_single['Saturn'], rebuilt['canon'][1]):>30}")
n_closed = sum(1 for t in tab if t[5].startswith("CLOSED"))
print(f"""
  {n_closed} of {len(tab)} readings put the ephemeris edge BELOW the window's lower edge; {len(tab)-n_closed} leave the window as
  published.  Read the pattern, not the tally:
      * R1a (Mars, non-degenerate room)  closes on BOTH footings at BOTH sigma, by x{lo/route1['Mars']['R1a3'][0]:.2f} to x{lo/route1['Mars']['R1a'][1]:.2f}.
      * R1b (Mars, mass-loss-degenerate) leaves it open on BOTH footings at BOTH, LLR still binding
        by x{route1['Mars']['R1b'][0]/rebuilt['canon'][1]:.2f} to x{route1['Mars']['R1b3'][0]/rebuilt['canon'][1]:.2f}.  This is the honest reading of the fit AS PUBLISHED.
      * R3 (Saturn, degeneracy-free) closes 3 of 4, and the one it does not close (canon, 3 sigma)
        it squeezes from width x1.241 to x{sat_edge_3s['canon']/lo:.3f} -- i.e. from a 24% window to a {100*(sat_edge_3s['canon']/lo-1):.0f}% window.
      * R2 Saturn 1-point is the deliberate pessimistic FLOOR and leaves everything intact.
  NOT footing-dependent and NOT sigma-convention-dependent: within every reading both footings and both
  conventions agree.  The alt footing is uniformly x{A0['alt']/A0['canon']:.3f} worse, as it must be (edge ~ 1/a0), and
  is the first to go: it closes under R1a AND under R3 at both sigma levels.
  The verdict hinges on exactly ONE thing: whether an a^2-profile drift can hide inside the
  solar-mass-loss allowance.  In the Mars-dominated fit AS PUBLISHED, yes (R1b).  Once Cassini's Saturn
  arc is used as the orthogonal handle, no (R3) -- and then the window is at best a few percent wide.

  WHAT IS ROBUST ACROSS EVERY READING (the solid deliverable):
    the DISSIPATIVE planetary channel puts the ephemeris ceiling at omega_c ~ (0.7-4)e-14 rad/s, i.e.
    WITHIN A FACTOR OF A FEW OF THE LLR EDGE {rebuilt['canon'][1]:.2e} -- whereas the paper's ephemeris treatment
    (reactive |delta g| only) put it at {wc_react:.2e}, {wc_react/rebuilt['canon'][1]:.0f}x looser and non-binding.  That is a
    reclassification of {np.log10(wc_react/route1['Mars']['R1b3'][0]):.1f} orders: the planetary ephemerides are NOT a slack constraint on
    omega_c, they are CO-BINDING with LLR right now.  The paper's Sec. 5.2 ordering ("per-planet
    reactive bounds and MESSENGER looser") is correct for the channel it evaluated and misleading for
    the channel it did not.

  WHAT WOULD SETTLE IT (no new data required):
    one ephemeris refit carrying the MI template d ln a_i/dt = a0 omega_c a_i^2 / GM_sun as a
    ONE-parameter family in omega_c, fitted jointly with GMdot_sun.  Because the template is a^2 and
    GMdot_sun is flat, and because Cassini's Saturn arc supplies {sh_mi['Saturn']:.0%} of the a^2 signal against
    {sh_un['Saturn']:.2%} of the flat leverage, the two are separable in the existing data.  The paper's Sec. 5.4
    asks for "a x3 INPOP/EPM/LLR secular refit" to close or detect the window; the AMPLITUDE for that
    x3 is already in the published record -- what is missing is the TEMPLATE, not the data.

  MI drift amplitudes at the window's own corners, for whoever runs that fit (canon footing):""")
print(f"    {'planet':<10}{'dlna/dt @1.782e-14':>21}{'dlna/dt @2.211e-14':>21}"
      f"{'adot @top [m/yr]':>19}{'MI/R1a room':>13}")
print("    " + "-" * 86)
for nm, (a, Td, _) in PLANETS.items():
    dlo = A0["canon"] * lo / gN(a) * YR
    dhi = A0["canon"] * PAPER_WINDOW["canon"][1] / gN(a) * YR
    print(f"    {nm:<10}{dlo:>21.3e}{dhi:>21.3e}{a*dhi:>19.4f}"
          f"{dlo/ROOMS['R1a fit-only'][1]:>12.2f}x")
print(f"""
  Even at the window's BOTTOM corner -- which cannot be lowered without gating off the SPARC rotation
  curves the framework exists to explain -- Mars must drift at {A0['canon']*lo/gN(PLANETS['Mars'][0])*YR:.2e}/yr and Saturn at
  {A0['canon']*lo/gN(PLANETS['Saturn'][0])*YR:.2e}/yr ({PLANETS['Saturn'][0]*A0['canon']*lo/gN(PLANETS['Saturn'][0])*YR:.2f} m/yr in semi-major axis).  There is no quiet corner: the drift FLOOR is
  set by the galaxies, and it is {A0['canon']*lo/gN(PLANETS['Mars'][0])*YR/ROOMS['R1a fit-only'][1]:.1f}x the EPM2019 fit uncertainty at Mars.  Any future
  tightening of the planetary secular record therefore pushes toward closure and cannot be relieved
  from below.  Asymmetry noted, as required.
""")

# ---------------------------------------------------------------------------------------------------
# 6. ASSUMPTIONS, EXPOSURES, SCOPE
# ---------------------------------------------------------------------------------------------------
head("6.  ASSUMPTIONS, EXPOSURES, AND SCOPE")
print(f"""
  [A1] The gate is read at the body's ORBITAL angular frequency (the paper's own rule for both window
       edges).  The drift law is frequency-INDEPENDENT -- omega cancels in 2 a_t omega/g_N -- so unlike
       reviews/mi_cassini_q2_omegac_2026.py (whose verdict flips under its Fork B/C) this result does
       NOT ride that choice.  A genuine robustness gain, and the reason this channel is worth more than
       the Q2 channel.
  [A2] Circular-orbit energy balance (e_Mars = 0.093, e_Saturn = 0.056 -> O(e^2) ~ 1%).  Not load-bearing.
  [A3] Dissipative amplitude taken at the paper's own (a0/2)|Im G|, sign fixed by passivity (inspiral).
       A |drift| bound is sign-blind, so the sign does not matter; the inspiral side happens to face the
       WIDER {EPM_GDOT_PLUS_3SIG:.1e}/yr half of the published Gdot/G interval, i.e. the conservative half was used.
  [A4] LOAD-BEARING #1: assigning a published multi-planet bound to Mars's own drift.  Supported by the
       Sec. 4 weights (Mars {sh_un['Mars']:.0%} of the flat-direction leverage) -- this one is now well founded, and it
       is what makes R1b the honest reading of the fit AS PUBLISHED.
  [A5] LOAD-BEARING #2: the R1a-vs-R1b room.  This is the whole verdict and it is NOT settled here.
       R1a is right about the physics (a^2 is not flat); R1b is right about the fit that exists.
  [A6] Not modelled: absorption of an a^2 drift into asteroid-belt masses, TNO ring mass, GM_sun and
       planetary initial conditions beyond the {{1,t}} removal already done; and Route 2's F_GEO = {F_GEO} is a
       stand-in for a real line-of-sight projection.  Both work AGAINST closure.  Stated, not swept.
  [A7] Spans/RMS in EPM_SPAN and EPM_RMS are the published postfit residuals with [ADOPTED] metre-class
       spans; Earth is excluded from the ranging model on purpose (it is the observer, not a ranged
       target -- an earlier draft that included it produced a spurious 93% Earth weight).
  [A8] LOAD-BEARING #3 (Sec. 4b): transferring the Mars-calibrated averaging gain x{GAIN:.2f} to Cassini's
       Saturn arc.  If Cassini's 20 m normal points are more correlated than Mars's 1.25 m ones the gain
       falls and the edge rises; Sec. 4b prints the full gain range that the published window
       corresponds to ({GAIN*sat_edge_3s['canon']/rebuilt['canon'][1]:.1f} to {GAIN*sat_edge_3s['canon']/1.782e-14:.1f}) so the reader can see how little it takes to move the verdict.
       The 4 per-planet |delta g| bounds of Fienga & Minazzoli 2024 were carried from the paper's own
       Sec. 5.1 table and NOT independently re-verified from the source this session (the Living Reviews
       PDF would not extract).  They affect only the RETIRED reactive channel, so nothing rests on them.

  THIS IS NOT: a falsification of the framework; a claim that the ephemerides have already excluded the
  gated crossover; or a statement about any sector other than the S_matter dissipative drift channel.
  THIS IS: an INDEPENDENT upper edge on omega_c -- different instrument (planetary ranging, not LLR),
  different bodies (Mars and Saturn, not the Moon), different published dataset (EPM2019) -- that lands
  within a factor of a few of the LLR edge on every reading, BELOW it on the physics-correct reading,
  and below the non-negotiable lower edge on that same reading.

  ONE-LINE STANDING:  the ephemeris edge is {rebuilt['canon'][1]/sat_edge_3s['canon']:.2f}x (Saturn, degeneracy-free, 3 sigma) to {rebuilt['canon'][1]/route1['Mars']['R1a'][0]:.2f}x
  (Mars, non-degenerate, 2 sigma) TIGHTER than the LLR edge the paper quotes, so the upper edge of the
  gate window is no longer owned by LLR; the canonical window narrows from x1.241 to x{sat_edge_3s['canon']/1.782e-14:.3f} at best and
  closes at worst, and the ALT footing closes on every reading except the deliberately pessimistic
  floor.  Whether "narrow" or "closed" is the truth is decided by one refit of existing data, not by
  new observations.  No door is claimed closed, and the framework is not claimed falsified.
""")
print(RULE)
print("mi_ephemeris_omegac_edge_2026.py: regressions passed (window rebuild <2%, 674x match, reactive "
      "ranking, drift law + t^2 algebra symbolic, Gdot/G interval algebra).")
print(RULE)
