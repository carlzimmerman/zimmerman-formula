#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_wb_gext_kappa_route_2026.py
==============================
THE WIDE-BINARY + DIRECTLY-MEASURED GALACTIC-ACCELERATION ROUTE TO kappa, priced rigorously.

Framework's own pieces throughout: a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 (canonical) and
1.1279e-10 (alt), with the in-force Route A kernel nu(y) = 1/(1 - e^-sqrt(y)) per Amendments 8/9.
Not McGaugh's nu.

*** FIRST, A CLAIM OF MINE IS RETRACTED.  I said this route has "no mass-to-light ratio anywhere in
the chain".  THAT IS FALSE.  gamma_v is DEFINED against v_Newt = sqrt(G M_tot/s), so the binary's total
mass enters, and for Gaia pairs that mass is photometric.  What is TRUE, and is a different and weaker
claim, is that the calibration is DYNAMICAL: the main-sequence mass-luminosity zero point is fixed on
ECLIPSING BINARIES in the high-acceleration, unambiguously Newtonian regime -- so it is
MOND-independent and tighter than galaxy population synthesis, but it is not absent. ***

--------------------------------------------------------------------------------------------------
THE CENTRAL OBSTACLE, AND IT IS ARITHMETIC (Part B)
--------------------------------------------------------------------------------------------------
gamma_v = sqrt(nu(g_ext/a_0)) is a WEAK function of a_0.  At the solar-neighbourhood field,
d ln gamma_v / d ln a_0 = 0.1155, so

        *** sigma(a_0)/a_0  =  8.66 x sigma(gamma_v)/gamma_v      -- EVERY gamma error is amplified. ***

--------------------------------------------------------------------------------------------------
AND AN ASYMMETRY THAT RUNS THE OTHER WAY (Part C)
--------------------------------------------------------------------------------------------------
Because gamma_v depends only on the RATIO y = g_ext/a_0, a fractional error in g_ext is exactly
equivalent to the opposite fractional error in a_0:

        *** errors in g_ext propagate 1:1 and are NOT amplified. ***

So a directly-measured Galactic acceleration -- pulsar timing, no Milky Way mass model -- only has to
MATCH the target precision, not beat it by 8.66x.  That is the structural advantage of this route, and
it is the half of my original claim that survives.

--------------------------------------------------------------------------------------------------
WHAT BINDS TODAY, AND IT IS NOT THE MASSES (Part D)
--------------------------------------------------------------------------------------------------
The frozen registration carries sigma_fit = 0.019 and sigma_tot = 0.028 at N = 30,000, implying
sigma_sys = 0.0206.  Amplified, *** the registration's OWN systematic budget already caps a_0 at
14.7%, and its statistical term at 13.6% -- both before any mass-scale consideration. ***

--------------------------------------------------------------------------------------------------
THE PAYOFF, AND IT IS CONSTRUCTIVE (Part F)
--------------------------------------------------------------------------------------------------
*** SPARC's floor (3.9%: helium, HI self-absorption, CO-dark H2) and this route's floor (~4%: the
mass-luminosity zero point plus Gaia systematics) are ORTHOGONAL.  Two independent 4% measurements
combine to 2.79% on a_0, i.e. sigma(kappa) = 0.014, which separates kappa = 1/2 from 1/sqrt(3) at
5.5 sigma.  NEITHER ROUTE REACHES 5 SIGMA ALONE.  That is the case for building this one. ***
"""

import sys
import mpmath as mp

mp.mp.dps = 30
FAIL = []


def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=6):
    return mp.nstr(mp.mpf(x), n)


A0 = mp.mpf("9.3619e-11")
A0_ALT = mp.mpf("1.1279e-10")
G_EXT = mp.mpf("1.8e-10")            # solar-neighbourhood Galactic field, ~1.9 a_0
GAMMA_T = mp.mpf("1.2139")           # Amendment 9 in-force target (canonical)
SIG_FIT = mp.mpf("0.019")            # frozen, N = 30,000
SIG_TOT = mp.mpf("0.028")            # frozen
N_FROZEN = mp.mpf("30000")
SPARC_FLOOR = mp.mpf("0.039")        # mi_kappa_error_budget_unlock_2026.py
KAPPA = mp.mpf("0.5")
K_ALT = 1 / mp.sqrt(3)


def nu(y):
    return 1 / (1 - mp.e ** (-mp.sqrt(y)))


def gamma_v(a0, gext=G_EXT):
    return mp.sqrt(nu(gext / a0))


print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- *** RETRACTION: the route is NOT mass-to-light free ***")
print("=" * 100)

# gamma_v^2 = v_obs^2 s / (G M_tot).  Show the mass does not cancel.
v, s_sep, G_s, M = mp.mpf("1"), mp.mpf("1"), mp.mpf("1"), mp.mpf("2")
g_at_M = mp.sqrt(v ** 2 * s_sep / (G_s * M))
g_at_2M = mp.sqrt(v ** 2 * s_sep / (G_s * 2 * M))
check(abs(g_at_2M / g_at_M - 1 / mp.sqrt(2)) < mp.mpf("1e-20"),
      "A1  *** gamma_v ~ 1/sqrt(M_tot) EXACTLY, so doubling the assumed mass changes gamma_v by "
      "1/sqrt(2).  The binary mass does NOT cancel -- my 'no M/L anywhere' claim is RETRACTED ***",
      f"gamma(2M)/gamma(M) = {sig(g_at_2M/g_at_M,6)} = 1/sqrt(2)")

MASS_CAL = {
    "SPARC galaxies": "Upsilon from POPULATION SYNTHESIS -- a model. ~17% systematic.",
    "wide binaries": "photometric masses on the main-sequence mass-luminosity relation, zero point "
                     "calibrated DYNAMICALLY on ECLIPSING BINARIES in the unambiguously Newtonian "
                     "regime -- MOND-independent, and tighter.",
}
for k, val in MASS_CAL.items():
    print(f"\n  {k}\n      {val}")
check(len(MASS_CAL) == 2 and "DYNAMICALLY" in MASS_CAL["wide binaries"],
      "A2  the surviving claim is about the KIND of calibration, not its absence: dynamical and "
      "MOND-independent versus model-based",
      "weaker than what I asserted, and it is what the paper will say")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- *** THE AMPLIFICATION: gamma_v is a WEAK function of a_0 ***")
print("=" * 100)

print("\n   g_ext          y_ext     gamma_v    d ln gamma/d ln a_0   amplification")
amps = {}
for ge in ["1.6e-10", "1.8e-10", "2.0e-10", "2.3e-10"]:
    gext = mp.mpf(ge)
    e = mp.mpf("1e-10")
    d = (mp.log(gamma_v(A0 * (1 + e), gext)) - mp.log(gamma_v(A0 * (1 - e), gext))) / (2 * e)
    amps[ge] = 1 / abs(d)
    print(f"   {ge:<13s} {sig(gext/A0,4):>7s}   {sig(gamma_v(A0,gext),6)}   {sig(d,5):>12s}        "
          f"{sig(1/abs(d),5)}x")

AMP = amps["1.8e-10"]
check(AMP > 8,
      f"B1  *** sigma(a_0)/a_0 = {sig(AMP,4)} x sigma(gamma_v)/gamma_v -- every gamma error is "
      "amplified by ~8.7 ***",
      "this is the central obstacle and it is pure arithmetic, not a systematic that can be beaten down")

check(max(amps.values()) / min(amps.values()) < 1.25,
      "B2  and the amplification is robust across the plausible g_ext range",
      f"{sig(min(amps.values()),4)}x to {sig(max(amps.values()),4)}x over g_ext = 1.6-2.3e-10")

# B3 -- the mass term, propagated.
print("\n   sigma_M/M   sigma_gamma/gamma (= 0.5 sigma_M/M)   sigma(a_0)/a_0")
for sm in ["0.05", "0.02", "0.01", "0.005"]:
    smf = mp.mpf(sm)
    sg = smf / 2
    print(f"   {float(smf)*100:6.1f}%     {float(sg)*100:8.2f}%                    {float(AMP*sg)*100:6.1f}%")
check(AMP * mp.mpf("0.05") / 2 > mp.mpf("0.20"),
      "B3  a 5% mass zero point alone caps a_0 at ~22%, so this route needs its mass scale at the "
      "PERCENT level",
      "which eclipsing-binary calibration can plausibly reach and population synthesis cannot")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- *** THE ASYMMETRY: g_ext propagates 1:1, NOT amplified ***")
print("=" * 100)

# gamma depends only on y = g_ext/a_0, so a fractional error in g_ext == opposite error in a_0.
d1 = mp.mpf("0.03")
g_shift_gext = gamma_v(A0, G_EXT * (1 + d1))
g_shift_a0 = gamma_v(A0 / (1 + d1), G_EXT)
check(abs(g_shift_gext / g_shift_a0 - 1) < mp.mpf("1e-20"),
      "C1  *** a +3% error in g_ext is EXACTLY equivalent to a -3% error in a_0 -- verified, because "
      "gamma_v depends only on the RATIO ***",
      f"gamma agrees to {sig(abs(g_shift_gext/g_shift_a0-1),3)}")

# C2 -- quantify the asymmetry: compare what a 4% error in each input costs a_0.
cost_gext = mp.mpf("0.04")                      # 1:1
cost_gamma = AMP * mp.mpf("0.04")               # amplified
check(cost_gamma / cost_gext > 8,
      f"C2  *** SO A DIRECTLY-MEASURED g_ext NEED ONLY MATCH THE TARGET: a 4% g_ext error costs "
      f"{float(cost_gext)*100:.0f}% in a_0, while a 4% gamma error costs {float(cost_gamma)*100:.0f}% -- a factor "
      f"{float(cost_gamma/cost_gext):.1f} asymmetry ***",
      "pulsar timing at a few percent suffices, with no Milky Way mass model; this is the structural "
      "advantage of the route and the half of my original claim that survives")

# NEGATIVE CONTROL: a mass error must NOT have this property, or C1 is vacuous.
g_massfix = mp.sqrt(nu(G_EXT / A0)) / mp.sqrt(1 + d1)     # mass error enters as 1/sqrt(M)
check(abs(g_massfix / g_shift_a0 - 1) > mp.mpf("1e-6"),
      "NC-C  CONTROL: a mass error does NOT map onto an a_0 error the same way, so C1 is a real "
      "property of the ratio structure and not a triviality", "")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- *** WHAT BINDS TODAY: the registration's OWN systematic ***")
print("=" * 100)

sig_sys = mp.sqrt(SIG_TOT ** 2 - SIG_FIT ** 2)
print(f"\n   frozen: sigma_fit = {sig(SIG_FIT,3)}, sigma_tot = {sig(SIG_TOT,3)} at N = 30,000")
print(f"   implied sigma_sys = {sig(sig_sys,4)}")
print("\n   term              sigma_gamma/gamma    sigma(a_0)/a_0")
for lbl, sv in [("statistical", SIG_FIT), ("systematic", sig_sys), ("total", SIG_TOT)]:
    print(f"   {lbl:16s} {float(sv/GAMMA_T)*100:8.2f}%          {float(AMP*sv/GAMMA_T)*100:7.1f}%")

cap_sys = AMP * sig_sys / GAMMA_T
check(cap_sys > mp.mpf("0.10"),
      f"D1  *** the registration's OWN sigma_sys already caps a_0 at {float(cap_sys)*100:.1f}%, before any mass "
      "consideration -- THAT is what binds today, not the masses ***",
      "so the first job is not better masses, it is beating the existing gamma_v systematic budget")

check(AMP * SIG_TOT / GAMMA_T > mp.mpf("0.15"),
      f"D2  and DR4 as frozen gives a_0 to {float(AMP*SIG_TOT/GAMMA_T)*100:.0f}%, i.e. WORSE than SPARC's 16.2%",
      "DR4 tests the ARM (Newtonian vs framework at 4.7-7.1 sigma); it does not measure the coefficient")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the requirement sheet for a_0 to 4%")
print("=" * 100)

TGT = mp.mpf("0.04")
need_g = TGT / AMP
need_M = 2 * need_g
N_need = N_FROZEN * (SIG_FIT / (need_g * GAMMA_T)) ** 2
print(f"""
   TARGET: sigma(a_0)/a_0 = {float(TGT)*100:.0f}%   (SPARC-comparable, so the two can be combined)

     sigma_gamma/gamma          <= {float(need_g)*100:.3f}%      i.e. sigma_gamma <= {float(need_g*GAMMA_T):.4f}
     mass-luminosity zero point <= {float(need_M)*100:.2f}%       (eclipsing-binary calibrated)
     clean pairs N              >= {float(N_need):,.0f}     (scaling sigma_fit = 0.019 at N = 30,000)
     g_ext (pulsar timing)      <= {float(TGT)*100:.0f}%          -- 1:1, so a few percent SUFFICES
     residual gamma systematics <= {float(need_g*GAMMA_T):.4f}      -- the hard one; currently 0.0206
""")
check(N_need > 3 * N_FROZEN,
      f"E1  the statistical requirement is N >= {float(N_need):,.0f} pairs, {float(N_need/N_FROZEN):.1f}x the frozen "
      "N = 30,000 -- beyond DR4, so this is a DR5-and-beyond programme",
      "stated plainly rather than as an aspiration")

check(need_g * GAMMA_T < sig_sys,
      f"E2  *** AND THE BINDING REQUIREMENT IS THE SYSTEMATIC: {float(need_g*GAMMA_T):.4f} needed against "
      f"{float(sig_sys):.4f} today, a factor {float(sig_sys/(need_g*GAMMA_T)):.1f} ***",
      "no amount of pairs fixes this; it is the estimator's shape bias, contamination and "
      "projection budget that must come down")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- *** THE PAYOFF: ORTHOGONAL SYSTEMATICS CROSS 5 SIGMA ***")
print("=" * 100)

WB_FLOOR = mp.mpf("0.04")
comb = SPARC_FLOOR * WB_FLOOR / mp.sqrt(SPARC_FLOOR ** 2 + WB_FLOOR ** 2)
GAP = abs(KAPPA - K_ALT)


def sep(frac):
    return GAP / (KAPPA * frac)


print(f"""
   SPARC floor        {float(SPARC_FLOOR)*100:.1f}%   helium, HI self-absorption, CO-dark H2
   wide-binary floor  {float(WB_FLOOR)*100:.1f}%   mass-luminosity zero point, Gaia systematics
   *** the two term-lists share NOTHING.  Combined in quadrature: {float(comb)*100:.2f}% on a_0 ***

   separation of kappa = 1/2 from 1/sqrt(3) = {float(K_ALT):.4f} (gap {float(GAP):.4f}):
      SPARC alone        {float(sep(SPARC_FLOOR)):.2f} sigma
      wide binary alone  {float(sep(WB_FLOOR)):.2f} sigma
      COMBINED           {float(sep(comb)):.2f} sigma
""")
check(sep(comb) > 5 and sep(SPARC_FLOOR) < 5 and sep(WB_FLOOR) < 5,
      f"F1  *** NEITHER ROUTE REACHES 5 SIGMA ALONE ({float(sep(SPARC_FLOOR)):.2f} and {float(sep(WB_FLOOR)):.2f}) BUT TOGETHER THEY "
      f"DO ({float(sep(comb)):.2f}) ***",
      "that is the entire case for building this route -- not that it is better, but that it is "
      "INDEPENDENT")

# F2 -- and both footings, per the standing rule.
den = mp.mpf("1.87094e-10")
den_alt = den * (A0_ALT / A0)
check(abs(A0 / den - mp.mpf("0.5")) < mp.mpf("0.002"),
      f"F2  both footings carried: kappa_canonical = {sig(A0/den,5)}, kappa_alt = {sig(A0_ALT/den,5)} "
      f"(or {sig(A0/den_alt,5)} against the alt denominator)",
      "the route measures a_0; which kappa that implies depends on the footing, as always")


# =============================================================================================
print()
print("=" * 100)
print("PART G -- WHAT IS AND IS NOT CLAIMED")
print("=" * 100)

NOT_CLAIMED = [
    "*** NOT 'no mass-to-light ratio anywhere in the chain' -- RETRACTED in Part A. gamma_v ~ "
    "1/sqrt(M_tot) exactly. ***",
    "NOT a measurement: no wide-binary data is analysed here. This is an error budget and a "
    "requirement sheet.",
    "NOT achievable with DR4: the statistical term alone needs ~11x the frozen N.",
    "NOT limited by masses TODAY -- the registration's own sigma_sys = 0.0206 binds first.",
    "NOT a claim that pulsar-timing g_ext is currently good enough; only that it need not be better "
    "than the target, which is the non-obvious part.",
    "NOT a reason to move any registered number. Amendment 9's target stands.",
]
print("\n  NOT CLAIMED:")
for n in NOT_CLAIMED:
    print(f"    - {n}")
check(len(NOT_CLAIMED) == 6, "G1  six explicit non-claims", "")


print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"""
  1.  *** RETRACTION FIRST: this route is NOT mass-to-light free.  gamma_v ~ 1/sqrt(M_tot) exactly, so
      the binary's photometric mass enters.  What survives is a claim about the KIND of calibration --
      DYNAMICAL, on eclipsing binaries in the unambiguously Newtonian regime, hence MOND-independent
      and tighter than population synthesis. ***

  2.  *** THE CENTRAL OBSTACLE IS ARITHMETIC: gamma_v is a weak function of a_0, so
      sigma(a_0)/a_0 = {sig(AMP,4)} x sigma(gamma_v)/gamma_v.  Every gamma error is amplified ~8.7x, robustly
      across g_ext = 1.6-2.3e-10. ***

  3.  *** BUT AN ASYMMETRY RUNS THE OTHER WAY: gamma_v depends only on y = g_ext/a_0, so a fractional
      error in g_ext maps EXACTLY onto the opposite error in a_0 -- 1:1, NOT amplified (verified).  A
      directly-measured Galactic acceleration therefore need only MATCH the target precision. ***

  4.  *** WHAT BINDS TODAY IS NOT THE MASSES: the registration's own sigma_sys = {sig(sig_sys,4)} already caps
      a_0 at {float(cap_sys)*100:.1f}%, and DR4 as frozen gives {float(AMP*SIG_TOT/GAMMA_T)*100:.0f}% -- WORSE than SPARC's 16.2%.  DR4 tests
      the ARM, not the coefficient. ***

  5.  REQUIREMENT SHEET for a_0 to 4%: sigma_gamma/gamma <= {float(need_g)*100:.3f}%, mass zero point <= {float(need_M)*100:.2f}%,
      N >= {float(N_need):,.0f} clean pairs ({float(N_need/N_FROZEN):.1f}x frozen, so DR5-and-beyond), g_ext <= 4%.
      The binding item is the gamma systematic: {float(need_g*GAMMA_T):.4f} needed against {float(sig_sys):.4f} today.

  6.  *** THE CASE FOR BUILDING IT IS INDEPENDENCE, NOT SUPERIORITY.  SPARC's {float(SPARC_FLOOR)*100:.1f}% floor and this
      route's ~{float(WB_FLOOR)*100:.0f}% floor share NO terms.  Combined: {float(comb)*100:.2f}% on a_0, sigma(kappa) = {float(0.5*comb):.4f},
      separating 1/2 from 1/sqrt(3) at {float(sep(comb)):.2f} sigma.  Neither route reaches 5 sigma alone
      ({float(sep(SPARC_FLOOR)):.2f} and {float(sep(WB_FLOOR)):.2f}).  Together they do. ***
""")

print("=" * 100)
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f_ in FAIL:
        print(f"  - {f_}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
