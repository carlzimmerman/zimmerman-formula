#!/usr/bin/env python3
r"""mi_gw_memory_effect_2026.py -- CAN MODIFIED INERTIA SAY ANYTHING ABOUT GRAVITATIONAL WAVES, AND
SPECIFICALLY ABOUT THE MEMORY EFFECT? Answer computed, not asserted.

THE GRAVITATIONAL MEMORY EFFECT (Zel'dovich & Polnarev 1974; Christodoulou 1991; Blanchet & Damour 1992;
tied to BMS supertranslations by Strominger and by Hawking, Perry & Strominger 2016): after a burst passes,
freely-falling test masses are left PERMANENTLY DISPLACED -- a non-oscillatory strain offset Delta h that does
not return to zero. It is real, unobserved individually, and expected to be stackable.

THE NAIVE HOPE, and why it is wrong: "GWs are the inertia of black holes rippling outward, maybe slightly
faster than light." Not so. GW170817 + GRB 170817A pins |v_g/c - 1| to [-3e-15, +7e-16] -- the single most
destructive constraint in modified gravity, which killed TeVeS, most Horndeski G4/G5, and generic disformal
couplings in 2017. Nothing here travels faster than light.

BUT there is a real question underneath, and it has a computable answer. MI modifies the INERTIAL RESPONSE of
a body at LOW acceleration. A GW detector's test mass responds to a passing wave with a TINY acceleration. So:
is a GW detector in the MOND regime? If yes, MI predicts a modified response and is testable -- or dead. This
script computes the accelerations and answers.

  G1  the memory amplitude and the accelerations a test mass actually feels
  G2  *** THE AMBIENT FIELD: is any GW detector in the MOND regime? ***
  G3  the size of the MI correction to a detector's response, both kernels
  G4  where MI COULD touch the GW sector, and the one live channel

Exit 0 = ran and every check held. No check(True).
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import A0_CANON, log_nu_minus1, nu_alpha2  # noqa: E402

ok: list[tuple[bool, str]] = []
G, MSUN, AU, KPC = 6.674e-11, 1.989e30, 1.496e11, 3.0857e19


def num1_a2(y):
    """alpha=2's nu - 1, CANCELLATION-FREE. Needed because nu_alpha2(y) - 1 underflows to exactly 0.0 in
    float64 by y ~ 1e8 (nu = 1 + 5e-23 rounds to 1.0), which killed an earlier version of this script's own
    contrast line with a log10(0) domain error -- the corpus's documented trap, caught again in the very place
    it was being written about. nu = sqrt((1 + sqrt(1+4t))/2), t = 1/y^2; use u = 4t/(sqrt(1+4t)+1)."""
    t = 1.0 / (float(y) * float(y))
    u = 4.0 * t / (math.sqrt(1.0 + 4.0 * t) + 1.0)
    return math.expm1(0.5 * math.log1p(0.5 * u))


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 104)
    print(f"  {t}")
    print("=" * 104)


banner("G1  THE MEMORY AMPLITUDE, AND THE ACCELERATIONS A TEST MASS FEELS")

# GW150914-like: h_peak ~ 1e-21 at f ~ 250 Hz; memory is a few % to ~20% of peak, rise over the merger time.
H_PEAK, F_GW, L_ARM = 1.0e-21, 250.0, 4000.0
H_MEM, TAU_MEM = 0.1 * H_PEAK, 5.0e-3          # 10% of peak, developing over ~5 ms
a_osc = H_PEAK * L_ARM * (2 * math.pi * F_GW) ** 2 / 2.0
a_mem = H_MEM * L_ARM / TAU_MEM**2 / 2.0
print(f"  oscillatory: a ~ h L omega^2 / 2 = {a_osc:.3e} m/s^2   = {a_osc/A0_CANON:.4f} a0")
print(f"  memory:      a ~ dh L / tau^2 / 2 = {a_mem:.3e} m/s^2   = {a_mem/A0_CANON:.4f} a0")
check(a_osc < A0_CANON and a_mem < A0_CANON,
      f"G1a *** BOTH ARE BELOW a0, AND THAT IS WHY THE QUESTION IS NOT SILLY. *** The wave-induced "
      f"acceleration of a LIGO test mass is {a_osc/A0_CANON:.3f} a0 oscillatory and {a_mem/A0_CANON:.4f} a0 for "
      f"the memory offset -- both in the deep-MOND regime taken in isolation. So a naive reading of modified "
      f"inertia WOULD predict an O(1) modification of every GW detection ever made, which would have killed the "
      f"framework in 2015. G2 is why it did not")


banner("G2  *** THE AMBIENT FIELD -- is any GW detector in the MOND regime? ***")

# MI depends on the TOTAL acceleration, not the perturbation. Every detector sits in a background field.
# THE GALACTIC FIELD IS AN IRREDUCIBLE FLOOR THAT ADDS TO EVERY LOCAL SOURCE -- not one row of a table.
# A first version of this section took the MINIMUM over local contributions and FAILED its own check, because
# a detector parked at 10^4 AU sees only 0.63 a0 from the Sun. It still sits in the Galaxy.
G_GAL = (233.1e3) ** 2 / (8.2 * KPC)
LOCAL = {
    "LIGO/Virgo mirror (Earth surface)": 9.81,
    "LISA test mass (drag-free, 1 AU)": G * MSUN / AU**2,
    "hypothetical detector at 100 AU": G * MSUN / (100 * AU) ** 2,
    "hypothetical detector at 10^4 AU": G * MSUN / (1e4 * AU) ** 2,
    "free-floating, Sun negligible": 0.0,
}
ENV = {k: v + G_GAL for k, v in LOCAL.items()}
print(f"  the Galactic field at the solar radius is an IRREDUCIBLE FLOOR: g_gal = {G_GAL:.3e} m/s^2 "
      f"= {G_GAL/A0_CANON:.2f} a0")
print(f"  {'environment':<38}{'g_local/a0':>13}{'g_total/a0':>13}")
print("  " + "-" * 66)
for k, v in LOCAL.items():
    print(f"  {k:<38}{v/A0_CANON:>13.3e}{(v+G_GAL)/A0_CANON:>13.3e}")
g_min = min(ENV.values())
check(g_min > A0_CANON and abs(g_min - G_GAL) < 1e-30,
      f"G2a *** NO GW DETECTOR ANYWHERE IN THE GALAXY CAN BE IN THE MOND REGIME, AND THE FLOOR IS SET BY THE "
      f"GALAXY ITSELF. *** Remove the Sun entirely and a free-floating detector at the solar radius STILL sits "
      f"in {g_min/A0_CANON:.2f} a0 from the Galaxy -- that is the irreducible floor, and every actual detector "
      f"is far above it: LIGO "
      f"mirrors sit at {ENV['LIGO/Virgo mirror (Earth surface)']/A0_CANON:.1e} a0, LISA at "
      f"{ENV['LISA test mass (drag-free, 1 AU)']/A0_CANON:.1e} a0. Even a detector parked at 10^4 AU is at "
      f"{ENV['hypothetical detector at 10^4 AU']/A0_CANON:.1e} a0. *** The external-field effect therefore "
      f"protects the entire GW sector STRUCTURALLY, not by luck: you cannot build a MOND-regime interferometer "
      f"inside a galaxy ***")


banner("G3  THE SIZE OF THE MI CORRECTION TO A DETECTOR'S RESPONSE")

print(f"  fractional response modification = nu(y_tot) - 1 at the AMBIENT y, both kernels:")
print(f"  {'environment':<38}{'y_tot':>12}{'Route A: log10(nu-1)':>22}{'alpha=2: nu-1':>16}")
print("  " + "-" * 90)
worst_ra = -1e99
for k, v in ENV.items():
    y = v / A0_CANON
    lra = float(log_nu_minus1(y)) / math.log(10)
    a2 = num1_a2(y)
    worst_ra = max(worst_ra, lra)
    print(f"  {k:<38}{y:>12.3e}{lra:>22.1f}{a2:>16.3e}")
y_ligo = ENV["LIGO/Virgo mirror (Earth surface)"] / A0_CANON
l_ligo = float(log_nu_minus1(y_ligo)) / math.log(10)
check(l_ligo < -100.0,
      f"G3a AND THE CORRECTION IS NOT MERELY SMALL, IT IS UNREPRESENTABLE. At a LIGO mirror "
      f"(y = {y_ligo:.2e}) Route A gives log10(nu - 1) = {l_ligo:.0f}, i.e. the fractional response "
      f"modification is 10^{l_ligo:.0f} -- computed in LOG space because it underflows every float format. The "
      f"superseded alpha=2 kernel gives {num1_a2(y_ligo):.2e}, still {abs(math.log10(num1_a2(y_ligo))):.0f} "
      f"orders below LIGO's ~1e-3 calibration accuracy. *** MI makes NO detectable prediction for any GW "
      f"observation, on any kernel, and that is a consistency requirement it passes rather than a test it "
      f"offers ***")

check(num1_a2(y_ligo) > 10 ** l_ligo,
      f"G3b and the kernel choice matters even here, which is worth recording: the retired power law leaves a "
      f"{num1_a2(y_ligo):.1e} residual while Route A's exponential leaves 10^{l_ligo:.0f} -- a gap of "
      f"~{abs(l_ligo) - abs(math.log10(num1_a2(y_ligo))):.0f} orders. The same structural difference "
      f"that discharged the ephemeris (a power-law tail versus an exponential one) reappears here, three decades "
      f"of acceleration further up")


banner("G4  WHERE MI *COULD* TOUCH THE GW SECTOR -- the one live channel")

print("""  Three candidate channels, and only one survives:

  (a) GENERATION. At the ISCO of a 30+30 Msun binary the orbital acceleration is ~1e11 m/s^2 = ~1e21 a0.
      Utterly Newtonian. MI cannot affect waveform generation, so no inspiral-merger-ringdown test applies.
  (b) DETECTOR RESPONSE. Killed structurally by G2a/G3a -- the ambient field forbids it.
  (c) PROPAGATION, via the Lorentz-violating spurion the framework INDUCES. This is the live one, and the
      corpus's gw_sme_door.py already frames it: the induced gravity-sector background is
          s_munu ~ (a0 / 2|a|) x (u^mu u^nu)_traceless,   CPT-EVEN, apex = CMB rest frame,
      which is ACCELERATION-DEPENDENT rather than a constant Sun-frame background. That dependence is the whole
      subtlety: |a| is large in the Solar System (suppressing s) but small along an intergalactic geodesic.""")

# the one number worth computing here: what ambient |a| would be needed to reach the GW170817 bound
BOUND = 3e-15                       # |k_(I)^(4)| <~ 3e-15 from GW170817 + GRB170817A
a_needed = A0_CANON / (2 * BOUND)
g_igm = 1e-13                       # a generous intergalactic/void field scale, m/s^2
s_igm = A0_CANON / (2 * g_igm)
print(f"\n  s ~ a0/(2|a|) reaches the GW170817 bound {BOUND:.0e} only where |a| >= {a_needed:.3e} m/s^2")
print(f"  = {a_needed/A0_CANON:.2e} a0 -- i.e. only in fields FAR STRONGER than a0, which is the opposite of")
print(f"  where GWs spend their propagation time. Along a void geodesic at |a| ~ {g_igm:.0e} m/s^2 the naive")
print(f"  spurion would be s ~ {s_igm:.1f}, i.e. O(1000) -- violating the bound by ~{s_igm/BOUND:.0e}x.")
check(s_igm > BOUND,
      f"G4a *** SO THE ACCELERATION-DEPENDENT SPURION IS THE FRAMEWORK'S REAL GW EXPOSURE, AND IT IS NOT SMALL. "
      f"*** Taken literally, s ~ a0/(2|a|) evaluated along a low-acceleration intergalactic geodesic gives "
      f"s ~ {s_igm:.0f}, exceeding the GW170817 isotropic bound of {BOUND:.0e} by ~{s_igm/BOUND:.0e}x. The "
      f"framework therefore REQUIRES one of: (i) the isotropic d=4 speed piece cancels identically (the "
      f"corpus's gw_sme_door.py records c_T = 1 as a REQUIREMENT the construction must satisfy, not a "
      f"prediction it makes), (ii) |a| in the spurion means the SOURCE's acceleration rather than the "
      f"propagation-path field, or (iii) the spurion does not couple to the tensor sector at all. Which of "
      f"those holds is NOT settled by this script and is the honest open item -- it is a structural constraint "
      f"on any covariant completion, and it is why the AeST-type realisation (Skordis & Zlosnik), built to have "
      f"c_GW = c EXACTLY, is the only completion the corpus treats as viable")

check(a_needed / A0_CANON > 1e13,
      f"G4b and the scaling makes the point sharply: suppressing the spurion to the GW170817 bound needs "
      f"|a| > {a_needed/A0_CANON:.1e} a0. Deep-MOND galaxy outskirts -- the framework's OWN home regime -- sit "
      f"at y ~ 0.01-1, which is {1e13:.0e}x too weak. *** So the regime where the framework does its work is "
      f"precisely the regime where a literal reading of its induced spurion is most dangerous. Any completion "
      f"must decouple the two, and that decoupling is an assumption rather than a result ***")


banner("VERDICT")
print(f"""  ON THE MEMORY EFFECT SPECIFICALLY: it is real physics (Zel'dovich-Polnarev 1974, Christodoulou 1991,
  BMS supertranslations) and MI has NOTHING to say about it. The memory offset drives a test mass at
  {a_mem/A0_CANON:.4f} a0, which looks like deep-MOND territory -- but the mass sits in an ambient field of
  {ENV['LIGO/Virgo mirror (Earth surface)']/A0_CANON:.1e} a0, so the modification is 10^{l_ligo:.0f}. Not
  small: unrepresentable.

  AND THE PROTECTION IS STRUCTURAL, WHICH IS THE ONE GENUINELY NEW THING HERE: the weakest ambient field
  available anywhere in the Galaxy is the Galaxy's own, {g_min/A0_CANON:.2f} a0. *** You cannot build a
  MOND-regime interferometer inside a galaxy. *** So the entire GW sector is inaccessible to MI's distinctive
  physics by construction -- no test, and equally no vulnerability, from generation or response.

  GWs DO NOT TRAVEL FASTER THAN LIGHT: |v_g/c - 1| in [-3e-15, +7e-16] from GW170817 + GRB 170817A. That
  constraint is the reason most modified-gravity theories died in 2017, and it is a hard boundary on any
  covariant completion of this framework.

  THE ONE LIVE EXPOSURE, and it is against interest: the framework's induced spurion s ~ a0/(2|a|) is
  ACCELERATION-DEPENDENT, so it is largest exactly where |a| is smallest -- along intergalactic geodesics and
  in the deep-MOND regime the framework is built for. Read literally it exceeds the GW170817 bound by
  ~{s_igm/BOUND:.0e}x. The corpus's c_T = 1 is a REQUIREMENT its completion must satisfy, not a prediction;
  the AeST realisation is treated as viable precisely because it is constructed with c_GW = c exactly. Whether
  the spurion decouples from the tensor sector is an open structural question, not a settled one.

  NOT CLAIMED: no derivation, no new prediction, and nothing here bears on kappa = 1/2, which remains FITTED.""")

banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the GW sector is structurally inaccessible to MI (no galaxy-based detector can be in the MOND")
print("  regime); the memory effect is untouched; the acceleration-dependent spurion is the one live exposure.")
