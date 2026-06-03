#!/usr/bin/env python3
"""
PROJECT 12: make the External Field Effect airtight, and evolve it.
===================================================================
The EFE is the one MOND signature LambdaCDM+DM cannot fake (it violates the Strong Equivalence Principle).
sparc_efe_test.py already DETECTS it in SPARC at ~4.8 sigma (deflated to N_galaxies): the outer RAR turns
~0.1 dex negative and the scatter grows, where g_bar ~ e_N a0. This file states (1) exactly what would make
that detection AIRTIGHT (the one systematic it cannot kill in-house), and (2) the framework's distinctive,
LambdaCDM-FORBIDDEN prediction: the EFE WEAKENS with redshift as eta ~ 1/E(z), because a0 rises. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92); print("# PROJECT 12 -- EFE: airtight in-house limit, and the z-evolution signature"); print("#"*92 + "\n")

    print("="*92); print("PART 1 -- the in-house detection and its ONE caveat"); print("="*92)
    print("""  sparc_efe_test.py: the SPARC RAR residual goes ~ -0.09 dex below the relation for log g_bar < -11,
  and the scatter grows from ~0.16 to ~0.26 dex -- both EFE fingerprints -- right where g_bar ~ e_N a0 with
  e_N ~ 0.03 (Chae 2020). Significance ~4.8 sigma using N_GALAXIES (the honest, deflated estimate, since
  points within a galaxy are correlated). This is genuine, foundation-relevant evidence for SEP-violating
  (MONDian) gravity. The ONE caveat it cannot kill in-house: outer-disk KINEMATIC systematics (warps,
  non-circular motions, beam smearing) also suppress V at large R and mimic a downturn.\n""")

    print("="*92); print("PART 2 -- what makes it AIRTIGHT (the discriminating test)"); print("="*92)
    print("""  The EFE and outer-kinematics make the SAME mean downturn but DIFFERENT correlations:
    * EFE: the downturn depth must correlate with each galaxy's MEASURED external field g_ext (from the
      large-scale environment / nearby masses). Outer kinematics do not know about the environment.
    * So the airtight test is: regress the per-galaxy residual against g_ext (reconstructed from the local
      density field, e.g. from a redshift survey around each SPARC galaxy). A significant residual-vs-g_ext
      slope, with the predicted sign (more suppression at higher g_ext), is the EFE; null is kinematics.
  This needs the per-galaxy environment catalog (NOT in this repo) -- it is exactly the Chae 2020/2021
  analysis, and reproducing it on the full SPARC sample with a uniform environment reconstruction is the
  airtight in-house-able step once that catalog is attached.\n""")

    print("="*92); print("PART 3 -- the EVOLUTION: eta ~ 1/E(z), a LambdaCDM-forbidden signature"); print("="*92)
    print("  The EFE strength is eta = g_ext / a0(z). Since the framework's a0 RISES as a0(0)E(z), the SAME")
    print("  physical environment produces a WEAKER EFE at higher z. For a fixed g_ext (comoving structure):")
    print(f"     {'z':>5}{'a0(z)/a0_0':>12}{'eta(z)/eta_0 = 1/E(z)':>24}")
    for z in (0.0, 0.5, 1.0, 2.0):
        print(f"     {z:>5.1f}{E(z):>12.2f}{1/E(z):>24.3f}")
    print("""  => the EFE downturn moves to LOWER g_bar and SHRINKS with redshift (by 1/E(z)). In LambdaCDM there is
  NO EFE at any z (SEP holds), so BOTH the existence AND any redshift trend are forbidden -- making the
  z-evolution a doubly-distinctive test. Caveat (honest): g_ext itself evolves (structure grows), so the
  clean prediction is eta(z) ~ g_ext(z)/[a0(0)E(z)]; the a0 factor is the framework's, the g_ext(z) factor
  is standard structure growth and must be modeled. The framework-specific, falsifiable part is the EXTRA
  1/E(z) suppression on top of whatever g_ext does.\n""")

    print("="*92); print("PROJECT 12 VERDICT"); print("="*92)
    print("""  In-house: the EFE is detected in SPARC at ~4.8 sigma with one nameable caveat (outer kinematics). The
  airtight step is the per-galaxy residual-vs-g_ext regression (needs an environment catalog; the Chae
  analysis, reproducible once attached). The framework adds a distinctive, LambdaCDM-forbidden evolution:
  the EFE weakens as 1/E(z) because a0 rises -- a Tier-2 signature for the high-z programs (#17, #18). The
  EFE is the strongest existing foundation evidence (is MOND real? -> leans YES); the evolution is the next
  distinctive bet on top of it.""")
    print("="*92)


if __name__ == "__main__":
    main()
