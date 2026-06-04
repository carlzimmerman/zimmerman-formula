#!/usr/bin/env python3
"""
LITERATURE PULL 2026 (part d): the MUSE-DARK III RATE is a real tension; the many-temperatures structure.
========================================================================================================
Two current sources pulled and reported straight -- one of them unfavorable.

(1) THE a0(z) RATE (MUSE-DARK III, A&A 2026, arXiv:2604.22613) -- RISING confirmed, RATE in tension.
    Their dedicated intermediate-z RAR fit: a0(z) = a0(0) + a1*z, with a0(0) = 1.0(-0.04,+0.04) and
    a1 = 1.59(-0.10,+0.11), in units 1e-10 m/s^2. They state explicitly: "our measured a0(z) is FASTER than
    that of H(z) ... in tension with the scale-invariant vacuum paradigm." The framework's prediction is
    a0 ∝ cH(z)/Z ∝ H(z) = H0 E(z), E(z)=sqrt(Om(1+z)^3+OL). So the framework RATE is ALSO too shallow:
      * the data rise ~2.8x STEEPER at low z (slope 1.59 vs E(z)*1.0 slope 0.47);
      * GOOD for the framework: "rising" is now firmly CONFIRMED -- constant a0 (the event-horizon reading)
        is dead, and the apparent-horizon DIRECTION the framework bet on is right;
      * BAD for the framework: the SPECIFIC cH(z)/Z RATE is too slow -- the data are steeper than the
        apparent-horizon surface gravity. A genuine, specific tension, not spun away.
    Honest counter-caveats (both ways): the low-z anchor is 1.0 here vs 1.2 (SPARC); intermediate-z RAR
    systematics (beam smearing, pressure support, HSB selection) tend to INFLATE high-z a0; and the data/E(z)
    ratio PEAKS ~1.45 near z~1 then falls to ~1.26 by z~3 -- a linear fit overshoots at high z, so the true
    law likely curves back toward E(z). => the gas-clean z~3 point (program #17) is the decider: framework
    predicts a0(z=3) ~ 4.6-5.5, the linear fit ~5.8 -- distinguishable.

(2) THE MANY-TEMPERATURES STRUCTURE (Rahman-Susskind, arXiv:2401.08555) -- richer than the Gaussian proxy.
    The "many temperatures of de Sitter" is NOT a single continuous spread: it is FOUR discrete temperatures
    -- Boltzmann T_B, Cord T_cord (stretched-horizon proper temp), Hawking T_H (pode), and the Tomperature
    (~T_H) -- with hierarchy T_B > T_cord >> T_H, PLUS a Tolman blue-shift across the static patch:
    T(r) = T_pode / sqrt(f(r)), f=1-r^2/L^2, with blue-shift factor BSF ~ L_dS/L_string ~ p at the stretched
    horizon. So the relevant temperature RANGE is [T_H, p*T_H] with p large. CONSEQUENCES for the broadening
    thread (project_manytemp_broadening.py): (a) GOOD -- the STRETCHED HORIZON is the natural cutoff that my
    Tolman estimate was missing (it resolves the u_max ambiguity: u_max <-> sin(theta_stretch) = 1/p); (b)
    HONEST -- the predicted spread depends on the large parameter p and on WHICH temperature the freezing
    samples, so my fitted sigma~0.33 dex is a phenomenological PROXY, not a derived number; (c) OPEN+
    interesting -- which temperature sets a0 (T_H gives a0 ∝ E(z); T_cord scales differently) is part of the
    unsettled dictionary, and the RATE tension in (1) may be a clue that a0 is NOT simply ∝ T_H = cH/2pi.
    Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92); print("# LITERATURE 2026d -- MUSE-DARK III rate tension; the many-temperatures structure"); print("#"*92 + "\n")

    print("="*92); print("(1) THE a0(z) RATE -- RISING confirmed, but FASTER than cH(z)/Z = E(z)"); print("="*92)
    print("  MUSE-DARK III (A&A 2026) linear fit: a0(z) = 1.0 + 1.59 z (1e-10). Framework: a0 = a0(0) E(z).")
    print(f"  {'z':>5}{'data 1.0+1.59z':>16}{'E(z)*1.0':>10}{'E(z)*1.2':>10}{'data/[E(z)*1.0]':>17}")
    for z in (0.0, 0.33, 0.5, 1.0, 1.44, 2.0, 3.0):
        dat = 1.0 + 1.59*z
        print(f"  {z:>5.2f}{dat:>16.2f}{1.0*E(z):>10.2f}{1.2*E(z):>10.2f}{dat/(1.0*E(z)):>17.2f}")
    print(f"""
  Initial slope d a0/dz at z=0: data 1.59 vs framework E(z)*1.0 = {1.5*Om:.2f} -> data ~{1.59/(1.5*Om):.1f}x steeper.
  GOOD: "rising" is CONFIRMED (constant / event-horizon reading dead) -- the apparent-horizon DIRECTION is right.
  BAD : the SPECIFIC cH(z)/Z RATE is too shallow -- MUSE-DARK III say a0(z) is "faster than H(z)". Real tension.
  CAVEATS (both ways): low-z anchor 1.0 vs 1.2; intermediate-z RAR systematics inflate high-z a0; data/E(z)
  PEAKS ~1.45 at z~1 then falls to ~1.26 by z~3 (linear fit overshoots) -> the gas-clean z~3 point decides
  (framework ~4.6-5.5, linear ~5.8).\n""")

    print("="*92); print("(2) THE MANY-TEMPERATURES STRUCTURE -- discrete + Tolman, not a Gaussian spread"); print("="*92)
    print("""  Rahman-Susskind (arXiv:2401.08555): FOUR discrete temperatures (Boltzmann T_B, Cord T_cord, Hawking
  T_H/pode, Tomperature~T_H), hierarchy T_B > T_cord >> T_H, PLUS a Tolman blue-shift T(r)=T_pode/sqrt(1-r^2/L^2)
  with blue-shift factor BSF ~ L_dS/L_string ~ p at the stretched horizon. Temperature RANGE [T_H, p*T_H].
  For the broadening thread:
   (a) GOOD: the STRETCHED HORIZON gives the natural cutoff my Tolman estimate lacked (u_max <-> 1/p), so the
       cutoff is not arbitrary -- it is the string-scale stretched horizon.
   (b) HONEST: the predicted spread depends on the LARGE p and on which temperature the freezing samples, so
       the fitted sigma~0.33 dex stays a PHENOMENOLOGICAL proxy -- the structure is real, the number is not yet
       derived.
   (c) OPEN: which temperature sets a0 is part of the unsettled dictionary (T_H -> a0 ∝ E(z); T_cord scales
       differently). The RATE tension in (1) may be telling us a0 is NOT simply ∝ T_H = cH/2pi -- a concrete,
       falsifiable lead rather than a fix.\n""")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  (1) The latest dedicated measurement CONFIRMS the framework's headline bet -- a0 RISES, constant is dead --
  but finds the RATE faster than cH(z)/Z = E(z) (steeper than H(z) by their own statement). The apparent-
  horizon DIRECTION is vindicated; the SPECIFIC cH/Z RATE is in real tension, modulo low-z anchor + high-z
  systematics + the z~1 turnover that the z~3 point resolves. Reported straight: a partial win (direction)
  with a sharpened, specific loss-or-refinement (rate).
  (2) The many-temperatures dual is a discrete-four-plus-Tolman structure, not a Gaussian spread: it supplies
  the natural stretched-horizon cutoff for the interpolation-broadening thread but does NOT pin sigma, and it
  raises the right question -- which de Sitter temperature actually sets a0 -- whose answer would bear on BOTH
  the interpolation shape AND the a0(z) rate. The honest state: rising vindicated, rate tensioned, mechanism
  structure mapped, the coefficient/temperature dictionary still the open hinge.""")
    print("="*92)


if __name__ == "__main__":
    main()
