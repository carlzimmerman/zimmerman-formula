#!/usr/bin/env python3
"""
Developing the premise: a0 = c/(2 t_ff). Stress-test it, then derive from it.
============================================================================

Start working on the cosmic-free-fall picture as a real premise. Serious
development means stress-testing first, then deriving. Three parts:

  PART 1 (stress-test the black-hole reading): is R = c*t_ff actually a black
    hole? No -- it is overdense by 8pi/3. The PHYSICAL cosmic black hole (where
    enclosed mass = Schwarzschild mass) is at the HUBBLE radius, and its surface
    gravity is cH/2 (overshoots a0 by sqrt(8pi/3)). So the honest premise is not
    'a0 = a black hole's surface gravity'; it is 'a0 = c/(2 t_ff)' -- the
    free-fall (gravitational) clock.

  PART 2 (motivate the timescale): why t_ff (free-fall) and not t_H (Hubble)?
    MOND is GRAVITATIONAL dynamics, whose natural clock is the dynamical/free-fall
    time, not the expansion time. The sqrt(8pi/3) is exactly t_ff/t_H.

  PART 3 (derive): a0 = a surface-gravity scale -> a Hawking/Unruh temperature
    T_a0 -- the bridge to emergent gravity. Plus an environmental test that
    distinguishes 'a0 from local density' (variable) from 'a0 from global density'
    (universal -- what the data shows).

Pure stdlib. Run:  python reviews/freefall_clock_development.py
"""

import math

C = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
MSUN = 1.989e30
HBAR = 1.054571817e-34
KB = 1.380649e-23
H0 = 71.5e3 / MPC
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)


def main():
    rho_c = 3 * H0 ** 2 / (8 * math.pi * G)
    t_ff = 1 / math.sqrt(G * rho_c)
    t_H = 1 / H0
    R_H = C / H0
    R_ff = C * t_ff

    print("=" * 78)
    print("PART 1 -- stress-test: is the 'cosmic black hole' real? (honest finding)")
    print("=" * 78)
    # Is R = c*t_ff a black hole? Compare enclosed mass to the Schwarzschild mass.
    def ratio_at(R):
        M_enc = rho_c * (4 * math.pi / 3) * R ** 3
        M_sch = R * C ** 2 / (2 * G)
        return M_enc / M_sch
    print(f"   at R = c*t_ff = {R_ff/MPC/1e3:.2f} Gpc:  M_enclosed/M_Schwarzschild = "
          f"{ratio_at(R_ff):.3f}  = 8pi/3")
    print("     -> OVERDENSE by 8pi/3; it is NOT a black hole (it would have collapsed).")
    print(f"   at R = R_Hubble = {R_H/MPC/1e3:.2f} Gpc: M_enclosed/M_Schwarzschild = "
          f"{ratio_at(R_H):.3f}  = 1 (EXACT, Friedmann)")
    print("     -> the PHYSICAL cosmic black hole is at the HUBBLE radius (escape v = c).")
    print(f"   its surface gravity g(R_H) = c^2/2R_H = cH/2 = {C**2/(2*R_H):.2e} m/s^2")
    print(f"   observed a0                                  = {A0:.2e} m/s^2 (sqrt(8pi/3) smaller)")
    print()
    print("   HONEST: the literal 'a0 = cosmic black-hole surface gravity' OVERSHOOTS")
    print("   (the real cosmic BH is at R_H, giving cH/2). The Schwarzschild reading was")
    print("   arithmetically exact but physically loose. The premise that survives is")
    print("   the cleaner one: a0 = c/(2 t_ff) -- the free-fall clock.\n")

    print("=" * 78)
    print("PART 2 -- motivate the timescale: gravity's clock is t_ff, not t_H")
    print("=" * 78)
    print(f"   free-fall (dynamical) time t_ff = 1/sqrt(G rho_c) = {t_ff:.3e} s")
    print(f"   Hubble (expansion) time    t_H  = 1/H            = {t_H:.3e} s")
    print(f"   ratio t_ff/t_H = {t_ff/t_H:.3f} = sqrt(8pi/3) (Friedmann)")
    print("   MOND is GRAVITATIONAL dynamics -- rotation, collapse, virialization. Its")
    print("   natural clock is the DYNAMICAL/free-fall time, not the expansion time. So")
    print("   a0 = c/(2 t_ff) is the physically motivated form; a0 = c/(2 t_H)=cH/2 uses")
    print("   the wrong (expansion) clock. The sqrt(8pi/3) IS the gravity-vs-expansion")
    print("   clock conversion -- motivated, though the '2' and 'exactly t_ff' remain")
    print("   normalization choices.\n")

    print("=" * 78)
    print("PART 3 -- derive from it: a temperature, and an environmental test")
    print("=" * 78)
    T_a0 = HBAR * A0 / (2 * math.pi * C * KB)
    print(f"   (a) a0 is a surface-gravity scale, so it has a Hawking/Unruh temperature")
    print(f"       T_a0 = hbar a0/(2pi c kB) = {T_a0:.3e} K  (= T_deSitter / Z).")
    print("       => the MOND transition is a HORIZON-THERMODYNAMIC threshold: dynamics")
    print("       change when the Unruh temperature of a body's acceleration drops to")
    print("       T_a0. This is the concrete bridge to the emergent-gravity completion,")
    print("       and the next derivation target (a0 from horizon entropy as surface")
    print("       gravity, the still-open coefficient).")
    print()
    print("   (b) ENVIRONMENTAL TEST -- the sharp, derived, falsifiable consequence:")
    print("       a0 = c/(2 t_ff(rho)).  If rho = LOCAL density, a0 ~ sqrt(rho_local)")
    print("       and VARIES with environment (bigger in clusters, smaller in voids).")
    print("       If rho = GLOBAL mean, a0 is UNIVERSAL. MOND data (SPARC) shows a0 is")
    print("       universal to ~10%, so the premise forces rho = GLOBAL/cosmic -- i.e.")
    print("       a0 = c/(2 t_ff,cosmic) = cH/Z. PREDICTION: a0 does NOT correlate with")
    print("       local density. Find a0 varying with environment, and the global free-")
    print("       fall-clock premise (and a0=cH/Z) is falsified. A clean, near-term test")
    print("       (WALLABY void vs cluster galaxies).\n")

    print("=" * 78)
    print("VERDICT -- where the development stands after stress-testing")
    print("=" * 78)
    print("  KEPT: a0 = c/(2 t_ff) with the free-fall (gravitational) clock. Motivated")
    print("        (gravity's timescale), and it yields a0 = cH/Z + all the consequences.")
    print("  DROPPED: the literal 'cosmic black hole' reading -- the real cosmic BH is at")
    print("        R_H (cH/2), so the BH picture overshoots; it was a loose analogy.")
    print("  BRIDGED: a0 <-> a Hawking temperature T_a0 = T_dS/Z, pointing at the")
    print("        emergent-gravity completion (where the coefficient must finally come from).")
    print("  DERIVED (new, testable): a0 must be set by the GLOBAL density, not local --")
    print("        no environmental dependence. A falsifiable prediction for WALLABY.")
    print()
    print("  Honest state: one normalization posit remains (the '2' and the exact t_ff),")
    print("  now physically framed as 'gravity's free-fall clock + escape-velocity 2',")
    print("  with a thermodynamic bridge and a fresh falsifiable test. That is a real")
    print("  start -- a premise with motivation, a derivation, and a way to be killed.")


if __name__ == "__main__":
    main()
