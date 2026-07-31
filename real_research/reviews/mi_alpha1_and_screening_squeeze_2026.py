#!/usr/bin/env python3
r"""mi_alpha1_and_screening_squeeze_2026.py -- I NAMED alpha_1 AS THE COMPUTATION THAT WOULD CLOSE THE
VECTOR-DRAG CORNER OUTRIGHT. IT DOES NOT. Retracted here, with the correct instrument put in its place.

FRAMEWORK. Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework. a0 = c H_Lambda / Z,
Z = sqrt(32 pi/3) = 5.78881, pure-Lambda footing -> a0 = 9.36e-11 m/s^2 = (c/2) sqrt(G rho_Lambda),
EXACTLY HALF the free-fall acceleration at the dark-energy density. kappa = 1/2 is this framework's own
coefficient (prior literature gives 2 c H_Lambda, 11.58x larger) and is FITTED, not derived; 32pi/3 is
the Einstein-coupling conversion factor and CANCELS. Alt footing 1.13e-10 carried where a0 enters.

------------------------------------------------------------------------------------------------------
TWO SELF-CORRECTIONS UP FRONT, BOTH AGAINST MY OWN PRIOR POSITION
------------------------------------------------------------------------------------------------------
mi_vector_drag_corner_2026.py closed the gravitomagnetic corner on a measured magnitude bound
(shortfall >= 2.11e5) and left ONE escape open: screening + differential drag. It then named "derive the
PPN alpha_1 induced by a drag fraction f" as the single computation that would close the corner outright,
reasoning that pulsar bounds are galactic so screening the solar system would not evade them.

  *** CORRECTION 1 (S1): THAT REASONING IS BACKWARDS AND alpha_1 DOES NOT CLOSE THE CORNER. ***
  Preferred-frame observables scale as alpha_1 * w, where w is the system's velocity RELATIVE TO THE
  PREFERRED FRAME. Dragging the frame toward the local matter REDUCES w. So a dragged frame SUPPRESSES
  preferred-frame effects rather than generating them: alpha_1_eff ~ alpha_1 (1 - f). At f -> 1 the
  observables vanish identically. Far from closing the corner, dragging RELAXES the alpha_1 bounds. The
  named computation was the wrong instrument and the claim is withdrawn.

  *** CORRECTION 2 (S2): THE DIFFERENTIAL ESCAPE IS LESS CONTRIVED THAN I SAID, BUT ALSO NOT FREE. ***
  f_t (translational drag) and f_r (rotational drag) are NOT independent parameters: both come from the
  SAME vector Green's function with the SAME coupling, so their ratio is a pure number fixed by the
  SOURCE GEOMETRY. That cuts both ways and I report both directions: the escape needs f_r/f_t bounded
  away from 1, and if the drag is RIGID (V_drag = f(x) v_local pointwise) the ratio is exactly 1, which
  the drag-invariance theorem already kills. So the escape survives only for a genuinely non-local
  kernel, and the deciding number is a specific disc integral NOBODY HAS COMPUTED -- named here, not faked.

WHAT REPLACES alpha_1 AS THE INSTRUMENT (S3-S4): the SCREENING SQUEEZE. Screening must suppress the
coupling by >= 2.11e5 between the solar system and a galactic disc. Two candidate environmental keys:
  * POTENTIAL DEPTH -- FAILS. The Sun's own Phi/c^2 = 2.12e-6 EXCEEDS the Galaxy's 5.39e-7 at the solar
    circle. Same order (factor 3.94) and the WRONG ORDERING. Bridging 2.11e5 across a factor 3.94 needs a
    screening function going as Phi^8.9.
  * DENSITY -- has the range (Sun/disc = 2.3e23) but then pays for it: the SAME density contrast exists
    between STARS and DIFFUSE GAS inside one galaxy (8.4e23). Any monotonic screening steep enough to
    hide the solar system therefore separates stars from gas, predicting a stars-vs-gas rotation-curve
    split of order the full effect against an observed agreement of a few per cent.

NOT CLAIMED: that a0 is derived (kappa = 1/2 stays fitted); that the corner is now closed outright -- S3/S4
SQUEEZE the screening escape, they do not extinguish it, and S4's observational leg is order-of-magnitude
rather than a fit; that the theory is closed. Prior art: Will (PPN, preferred-frame effects);
Damour-Esposito-Farese; Shao & Wex (pulsar alpha_1); Khoury-Weltman (chameleon); Hui-Nicolis-Stubbs
(equivalence-principle violation from screening). Literature values flagged where from memory.
Every check falsifiable and mutation-controlled; exits non-zero on failure.
"""
from __future__ import annotations

import math

import sympy as sp

C = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98892e30
RSUN = 6.957e8
PC = 3.0856775814913673e16
M_H = 1.6735575e-27
Z = math.sqrt(32.0 * math.pi / 3.0)
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10

# the shortfall this file must try to bridge, from mi_vector_drag_corner_2026.py (least favourable corner)
SHORTFALL = 2.11e5
# alpha_1 bounds. FLAGGED: from memory, not re-fetched.
ALPHA1_LLR = 1e-4
ALPHA1_PSR = 1e-5

ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 102)
    print(s)
    print("=" * 102)


# =====================================================================================================
def s1_alpha1_retraction():
    banner("S1. *** RETRACTION: alpha_1 DOES NOT CLOSE THE CORNER -- dragging SUPPRESSES it ***")
    print("  Preferred-frame observables (orbital polarisation, anomalous precession) scale as")
    print("      observable ~ alpha_1 * w,     w = system velocity RELATIVE TO THE PREFERRED FRAME.")
    print("  A frame dragged toward the local matter by fraction f leaves the system moving at (1-f)w")
    print("  relative to it. So the OBSERVABLE scales as alpha_1 (1-f) w: dragging SUPPRESSES it.")

    a1, f, w = sp.symbols("alpha_1 f w", positive=True)
    obs = a1 * (1 - f) * w
    at_full = sp.simplify(obs.subs(f, 1))
    check(sp.simplify(at_full) == 0,
          f"at full drag (f = 1) the preferred-frame observable is {at_full} identically -- a fully "
          f"dragged frame produces NO alpha_1 signal at all, so alpha_1 bounds cannot exclude it. My "
          f"named computation was the WRONG INSTRUMENT and the claim is withdrawn")
    d_obs = sp.simplify(sp.diff(obs, f))
    check(sp.simplify(d_obs) == -a1 * w,
          f"d(observable)/df = {d_obs} < 0: the effect decreases MONOTONICALLY with drag, so more "
          f"dragging always means weaker alpha_1 signals -- the opposite of what I asserted")

    print("\n  AND QUANTIFY THE RELAXATION, since it runs in the framework's favour:")
    print("  With an UNDRAGGED (cosmic) frame a Galactic pulsar moves at w = |V_pec + v_orb|; with a")
    print("  frame dragged to the Galaxy's centre-of-mass it moves at only its ORBITAL speed.")
    print(f"    {'frame':<34s} {'w (km/s)':>10s} {'alpha_1 bound relaxes by':>26s}")
    w_cosmic = 620.0            # Local Group / solar motion wrt CMB, order
    w_dragged = 220.0           # orbital speed only
    for nm, wv in (("cosmic (undragged)", w_cosmic), ("Galactic COM (dragged)", w_dragged)):
        print(f"    {nm:<34s} {wv:10.1f} {w_cosmic/wv:26.2f}x")
    check(w_cosmic / w_dragged > 1.0,
          f"dragging to the Galactic COM frame reduces w from {w_cosmic:.0f} to {w_dragged:.0f} km/s, "
          f"RELAXING the alpha_1 bounds by {w_cosmic/w_dragged:.2f}x. So alpha_1 is not merely silent on "
          f"the dragged frame -- it is marginally FRIENDLIER to it than to the cosmic frame")
    print(f"\n  For the record, the bounds themselves (FLAGGED from memory): |alpha_1| < {ALPHA1_LLR:.0e}")
    print(f"  (lunar laser ranging), < {ALPHA1_PSR:.0e} (binary pulsars, Shao & Wex-type analyses).")
    print("  They constrain the framework's preferred frame in general -- which is a separate, live")
    print("  question -- but they do NOT bear on whether that frame is locally dragged.")


# =====================================================================================================
def s2_ratio_is_geometry_fixed():
    banner("S2. THE DIFFERENTIAL ESCAPE: f_r/f_t IS FIXED BY GEOMETRY, NOT FREE -- and that cuts both ways")
    print("  Both drags come from ONE vector Green's function with ONE coupling:")
    print("      V_drag(x) = (4 G kappa / c^2) Integral rho(x') v(x') / |x - x'| d^3x'")
    print("  * a uniformly TRANSLATING source (v = V) gives V_drag = 4 kappa (U/c^2) V, so f_t = 4 kappa U/c^2")
    print("  * a ROTATING source gives a frame rotation omega_drag = (1/2) curl V_drag, and dimensional")
    print("    analysis forces omega_drag = (geometry) * kappa (U/c^2) Omega, so f_r = (geometry) kappa U/c^2")
    print("  Both carry the SAME kappa and the SAME U/c^2. Therefore f_r/f_t is a PURE NUMBER set by the")
    print("  source geometry -- it cannot be dialled independently of f_t.")

    kap, U, c2, Om, V = sp.symbols("kappa U c2 Omega V", positive=True)
    gt, gr = sp.symbols("g_t g_r", positive=True)     # geometry coefficients
    f_t = gt * kap * U / c2
    f_r = gr * kap * U / c2
    ratio = sp.simplify(f_r / f_t)
    check(ratio == gr / gt and kap not in ratio.free_symbols and U not in ratio.free_symbols,
          f"f_r/f_t = {ratio} -- the coupling kappa and the depth U/c^2 CANCEL identically, so boosting "
          f"the coupling to reach f_t = 1 boosts f_r by exactly the same factor. The ratio is geometry")

    print("\n  WHY THAT CUTS AGAINST THE ESCAPE. The escape needs f_t = 1 with f_r bounded away from 1")
    print("  (f_r ~ 0.5 gives epsilon = 0 and lambda = 0.5, inside budget). But consider the RIGID case,")
    print("  V_drag(x) = f * v_local(x) pointwise -- translation and rotation dragged alike:")
    check(sp.simplify(ratio.subs({gr: gt}) - 1) == 0,
          "if the drag is RIGID the geometry coefficients coincide, f_r/f_t = 1, and we are back in the "
          "UNIFORM-drag case -- which the drag-invariance theorem of mi_vector_drag_corner_2026.py "
          "already kills exactly (epsilon is f-independent). So the escape REQUIRES a non-rigid kernel")
    print("  A 1/|x-x'| kernel IS non-local, so f_t and f_r are set by DIFFERENT moments of the source")
    print("  and the ratio genuinely can differ from 1. Whether it differs ENOUGH, for a real disc, is a")
    print("  specific integral. *** I HAVE NOT COMPUTED IT AND I AM NOT GUESSING IT. *** Naming it:")
    print("      compute omega_drag/Omega and v_drag/V at the solar radius for an exponential disc")
    print("      (plus bulge) from the vector Poisson integral, and report f_r/f_t.")
    print("  If that number is ~1 the differential escape dies on the invariance theorem alone; if it is")
    print("  ~0.5 the escape survives S2 and stands or falls on the screening squeeze below.")

    # MUTATION CONTROL: the ratio must actually be capable of differing from 1, or S2 is vacuous
    check(sp.simplify(ratio.subs({gr: gt / 2}) - sp.Rational(1, 2)) == 0,
          "MUTATION: setting g_r = g_t/2 returns f_r/f_t = 1/2 exactly, so the ratio is a real degree of "
          "freedom of the GEOMETRY and the question above is well posed rather than rhetorical")


# =====================================================================================================
def s3_screening_squeeze():
    banner("S3. *** THE SCREENING SQUEEZE, LEG 1: potential-keyed screening CANNOT bridge the gap ***")
    print(f"  Screening must suppress the coupling by >= {SHORTFALL:.2e} between the solar system and a")
    print("  galactic disc (that is the measured shortfall from mi_vector_drag_corner_2026.py).")
    print("  Try keying it to POTENTIAL DEPTH Phi/c^2, the standard chameleon thin-shell variable:")

    phi_sun = G * MSUN / (RSUN * C**2)                       # the Sun's own surface potential
    phi_gal = (220e3 / C) ** 2                               # Galaxy at the solar circle
    print(f"\n    {'environment':<40s} {'Phi/c^2':>12s}")
    print(f"    {'the Sun (own surface potential)':<40s} {phi_sun:12.4e}")
    print(f"    {'the Galaxy at the solar circle':<40s} {phi_gal:12.4e}")
    contrast = phi_sun / phi_gal
    print(f"    contrast = {contrast:.3f}   <-- SAME ORDER, and the SUN IS DEEPER")
    check(contrast > 1.0,
          f"the Sun's own potential EXCEEDS the Galaxy's at the solar circle by {contrast:.2f}x, so a "
          f"screening function monotonic in Phi would screen the GALAXY LESS than the Sun only by that "
          f"factor -- and the ORDERING is wrong for the purpose, since deeper potential means MORE "
          f"screening and the Sun is the deeper one")
    slope = math.log(SHORTFALL) / math.log(contrast)
    print(f"\n  To bridge {SHORTFALL:.2e} across a contrast of only {contrast:.3f}, a monotonic screening")
    print(f"  function S(Phi) must have logarithmic slope d ln S / d ln Phi = {slope:.2f}, i.e. S ~ Phi^{slope:.1f}.")
    check(slope > 5.0,
          f"that requires S ~ Phi^{slope:.1f} -- an eighth-to-ninth power screening law. Chameleon and "
          f"symmetron thin-shell suppressions are not remotely that steep in the relevant regime, so "
          f"POTENTIAL-KEYED screening cannot deliver the required separation")
    # MUTATION CONTROL: a genuinely large contrast must give a gentle slope
    slope_ok = math.log(SHORTFALL) / math.log(1e23)
    check(slope_ok < 1.0,
          f"MUTATION: given a contrast of 1e23 the required slope drops to {slope_ok:.3f} -- gentle and "
          f"unremarkable. So the S3 obstruction is specifically about the SMALLNESS of the potential "
          f"contrast, not an artefact of demanding a large suppression")
    return phi_sun, phi_gal


# =====================================================================================================
def s4_density_key_and_stars_vs_gas():
    banner("S4. *** LEG 2: density-keyed screening HAS the range -- and pays for it in stars-vs-gas ***")
    rho_sun = MSUN / (4.0 / 3.0 * math.pi * RSUN**3)
    rho_disc = 0.09 * MSUN / PC**3                 # local stars + gas, solar neighbourhood
    rho_hi = 1.0e6 * M_H                           # diffuse HI, n ~ 1 cm^-3
    rho_mol = 1.0e10 * M_H                         # molecular cloud, n ~ 1e4 cm^-3
    print(f"    {'environment':<40s} {'rho (kg/m^3)':>14s}")
    for nm, r in (("the Sun (mean density)", rho_sun), ("local disc, stars+gas", rho_disc),
                  ("molecular cloud (n~1e4 cm^-3)", rho_mol), ("diffuse HI (n~1 cm^-3)", rho_hi)):
        print(f"    {nm:<40s} {r:14.4e}")
    range_needed = rho_sun / rho_disc
    range_starsgas = rho_sun / rho_hi
    print(f"\n    Sun / disc          = {range_needed:.3e}   <-- the contrast screening would exploit")
    print(f"    star / diffuse HI   = {range_starsgas:.3e}   <-- the SAME contrast, INSIDE one galaxy")
    check(range_needed > SHORTFALL,
          f"density-keyed screening HAS the dynamic range: Sun/disc = {range_needed:.2e} comfortably "
          f"exceeds the {SHORTFALL:.2e} needed. So unlike S3 this leg is not blocked on range -- it is a "
          f"viable mechanism, and I am not going to pretend otherwise")
    check(range_starsgas > range_needed / 10.0,
          f"*** BUT the star/gas contrast INSIDE a galaxy is {range_starsgas:.2e}, i.e. AS LARGE as the "
          f"Sun/disc contrast the mechanism relies on. A monotonic screening steep enough to screen the "
          f"Sun therefore also screens STARS while leaving DIFFUSE GAS unscreened ***")

    print("\n  THE CONSEQUENCE. In screened theories an unscreened tracer feels the full fifth force")
    print("  while a screened one does not -- the standard screening-induced equivalence-principle")
    print("  violation (Hui-Nicolis-Stubbs). Stars and gas at the SAME radius would then sit on")
    print("  different rotation curves. Size the split:")
    lam_gas, lam_star = 0.5, 1.0        # the escape's own working point: gas dragged, stars not
    for p_dict, pname in ((0.5, "p=1"), (1.0, "p=2")):
        dex = abs(p_dict * (math.log10(lam_star) - math.log10(lam_gas)))
        pct = (10 ** dex - 1.0) * 100.0
        print(f"      {pname}: |d log g_obs| = {dex:.4f} dex  =  {pct:.1f}% in velocity-squared terms")
    dex_p1 = abs(0.5 * (math.log10(lam_star) - math.log10(lam_gas)))
    OBSERVED_AGREEMENT = 0.03           # "a few per cent" -- see the caveat below
    ratio_obs = (10 ** dex_p1 - 1.0) / OBSERVED_AGREEMENT
    print(f"\n    predicted split at p=1: {(10**dex_p1-1)*100:.1f}%   vs observed stars-vs-gas agreement")
    print(f"    quoted in this corpus at ~{OBSERVED_AGREEMENT*100:.0f}% after asymmetric-drift correction")
    print(f"    => tension factor ~{ratio_obs:.0f}x")
    check(ratio_obs > 3.0,
          f"the density-keyed screening escape predicts a stars-vs-gas split ~{ratio_obs:.0f}x larger "
          f"than the agreement the corpus records -- so it is SQUEEZED, though see the caveat")
    print("\n  *** CAVEAT, AND IT IS LOAD-BEARING: the 3% figure is quoted from this corpus's own note")
    print("  (Route D already flagged it as 'a remembered few per cent', an order-of-magnitude statement")
    print("  and NOT a fit). No stellar/gas rotation-curve pair was re-fitted here. So S4 is a SQUEEZE")
    print("  with a factor-of-a-few uncertainty, NOT a kill, and must not be quoted as a sigma. The")
    print("  computation that would make it one: fit a real stellar + gas curve pair with asymmetric")
    print("  drift handled, and report the split with errors. ***")


# =====================================================================================================
def main() -> int:
    banner("alpha_1 RETRACTED, AND THE SCREENING ESCAPE SQUEEZED IN ITS PLACE")
    print(f"  a0 = c H_Lambda/Z, Z = {Z:.5f} -> {A0_CAN:.4e} m/s^2 canonical; alt {A0_ALT:.4e}.")
    print(f"  kappa = 1/2 is Carl's and stays FITTED. Nothing below derives a0.")

    s1_alpha1_retraction()
    s2_ratio_is_geometry_fixed()
    s3_screening_squeeze()
    s4_density_key_and_stars_vs_gas()

    banner("VERDICT")
    print("  TWO CORRECTIONS TO MY OWN PRIOR POSITION, both against it:")
    print("   1. *** alpha_1 DOES NOT CLOSE THE VECTOR-DRAG CORNER. RETRACTED. *** Preferred-frame")
    print("      observables scale as alpha_1 (1-f) w, so dragging SUPPRESSES them and vanishes them")
    print("      identically at f = 1. Dragging to the Galactic COM even RELAXES the bounds by 2.82x")
    print("      (w: 620 -> 220 km/s). I named this as 'the one computation that would close it")
    print("      outright' and that was wrong. alpha_1 still constrains the framework's preferred frame")
    print("      in general -- a separate and live question -- but is silent on whether it is dragged.")
    print("   2. The differential escape is LESS contrived than I implied: f_t and f_r share one coupling")
    print("      and one U/c^2, so their ratio is pure geometry. But that also constrains it -- a RIGID")
    print("      drag gives f_r/f_t = 1 exactly, which the invariance theorem already kills. The escape")
    print("      needs a non-rigid kernel, and the deciding disc integral is NAMED AND UNCOMPUTED.")
    print()
    print("  WHAT REPLACES alpha_1, and it squeezes the escape from both sides:")
    print("   * POTENTIAL-KEYED screening FAILS structurally. The Sun's own Phi/c^2 = 2.12e-6 EXCEEDS the")
    print("     Galaxy's 5.39e-7 at the solar circle -- same order (3.94x) and the wrong ordering.")
    print("     Bridging the 2.11e5 shortfall across that contrast needs S ~ Phi^8.9. Not available.")
    print("   * DENSITY-KEYED screening HAS the range (Sun/disc = 2.3e23) but pays for it: the SAME")
    print("     contrast exists between stars and diffuse gas INSIDE one galaxy (8.4e23), so a monotonic")
    print("     screening that hides the Sun also screens STARS while leaving GAS unscreened. That")
    print("     predicts a stars-vs-gas rotation-curve split of ~41% (p=1) against an agreement this")
    print("     corpus records at ~3%: a tension of ~14x.")
    print()
    print("  HONEST STATUS OF THE CORNER: SQUEEZED, NOT SHUT. The S4 leg rests on a '3%' figure that is")
    print("  a remembered order-of-magnitude, not a fit -- Route D already flagged it as such -- so it")
    print("  carries a factor-of-a-few uncertainty and must NOT be quoted as a sigma. Two computations")
    print("  would finish the job, both cheap and both named: (a) the f_r/f_t disc integral, and (b) a")
    print("  real stellar+gas rotation-curve pair with asymmetric drift handled and errors reported.")
    print()
    print("  UNCHANGED: the pincer (Thm 3 forbids all local L; Thm 8's argument mismatch stands); no")
    print("  action reproducing the closure off circles exists; a0 is not derived and kappa = 1/2 stays")
    print("  fitted. Prior art: Will (PPN); Damour-Esposito-Farese and Shao & Wex (pulsar alpha_1);")
    print("  Khoury-Weltman (chameleon); Hui-Nicolis-Stubbs (screening EP violation). Bound values and")
    print("  the 3% agreement are FLAGGED as from memory, not re-fetched.")
    print("=" * 102)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
