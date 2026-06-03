#!/usr/bin/env python3
"""
PROJECT 3b: adversarial stress-test of the apparent-horizon LEAN (Project 3's strongest theory support).
========================================================================================================
Project 3 argued FRW thermodynamics LEANS to the apparent horizon (Cai-Kim: dQ=TdS on the apparent horizon
IS Friedmann), hence a0 rises with z. That is the framework's best theoretical card, so it must be attacked.
The attack: Cai-Kim is about the cosmic BACKGROUND (Friedmann); a0 is a LOCAL (galaxy) scale -- the leap
'apparent horizon governs the background' -> 'apparent horizon sets the local a0' is not automatic. This
file runs the attack, finds the bridge that is required (the Deser-Levin Unruh-temperature floor), and
downgrades #3 honestly from 'leans' to 'conditional, two-ingredient support'. Needs numpy.
"""
import numpy as np

c, Mpc = 2.99792458e8, 3.0857e22
H0, Om, OL = 67.4e3/Mpc, 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92); print("# PROJECT 3b -- stress-testing the apparent-horizon lean"); print("#"*92 + "\n")
    print("="*92); print("THE ATTACK -- background vs local"); print("="*92)
    print("""  Cai-Kim establishes that dQ=TdS holds on the APPARENT horizon and yields the FRIEDMANN equation -- a
  statement about the cosmic BACKGROUND. But a0 is the LOCAL acceleration scale of galaxy dynamics. Nothing
  in 'the apparent horizon is the consistent background boundary' AUTOMATICALLY makes the LOCAL a0 track it.
  That inferential leap is the weak joint in Project 3. To survive, the framework needs a mechanism that
  ties the local a0 to the cosmic (apparent) horizon.\n""")

    print("="*92); print("THE BRIDGE IT REQUIRES -- the Deser-Levin Unruh floor"); print("="*92)
    print("""  The only thing that connects them is the de Sitter-Unruh temperature FLOOR: a locally accelerated
  detector in de Sitter space sees T(a) = (hbar/2pi c k) sqrt(a^2 + (cH)^2), which does NOT vanish as a->0
  but saturates at the cosmic de Sitter temperature T_dS = hbar H/2pi k. The MOND knee is where the floor
  bites, a ~ cH:""")
    for r in (10, 1, 0.1, 0.01):
        a = r*c*H0
        print(f"     a/cH = {r:>6}:  sqrt(a^2+(cH)^2)/a = {np.sqrt(a**2+(c*H0)**2)/a:.3f}")
    print(f"""  => for a >> cH the detector temperature is ordinary Unruh (T~a); for a << cH it floors at T_dS. So
  a0 ~ cH is the local-Unruh-meets-cosmic-floor scale -- THAT is the bridge from local dynamics to the cosmic
  horizon. And the floor uses the INSTANTANEOUS de Sitter temperature T_dS = hbar H(z)/2pi -> H(z), the
  APPARENT horizon, so a0 ~ cH(z) rises: a0(z=3)/a0(0) = E(3) = {E(3):.2f}. (The event-horizon floor would use
  sqrt(Lambda) = const.) The bridge exists -- but it is a SECOND, independent ingredient.\n""")

    print("="*92); print("PROJECT 3b VERDICT -- survives, but CONDITIONAL (downgrade from 'leans')"); print("="*92)
    print("""  Project 3 SURVIVES the attack but is honestly weaker than 'theory leans to the framework':
    * Cai-Kim alone does NOT prove a0 tracks the apparent horizon -- it proves the apparent horizon is the
      consistent BACKGROUND (Friedmann) boundary;
    * the local a0 link needs a SECOND ingredient: the Deser-Levin Unruh floor (a0 ~ local-Unruh-meets-cosmic-
      de-Sitter-T), which is independent physics, not implied by Cai-Kim;
    * the EVENT-horizon reading is still NOT excluded -- if a0 is set by the fundamental Lambda rather than
      the instantaneous thermal state, a0 is constant and nothing here forbids it.
  HONEST STATUS: #3 is CONDITIONAL, TWO-INGREDIENT support -- IF a0 comes from the local Unruh temperature
  hitting the cosmic de Sitter floor (Deser-Levin), AND that floor is the instantaneous/apparent one
  (Cai-Kim consistent), THEN a0 ~ cH(z) rises. That is a coherent package and a genuine reason the apparent
  reading is tidier -- but it is not a one-step proof, and the data (z~3, #17) remain the real arbiter.
  Calling it 'theory leans to the framework' was slightly too strong; 'theory provides a consistent,
  two-ingredient package for the framework, and does not exclude the alternative' is the accurate statement.""")
    print("="*92)


if __name__ == "__main__":
    main()
