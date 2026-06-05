#!/usr/bin/env python3
"""
The geometric core (a0=c^2 sqrt(Lambda/32pi), constant) vs the evolving claim (a0=cH(z)/Z) -- distinct, separated.
=================================================================================================================
An honest correction: the verdict "the framework's one claim leans ~2-3 sigma unfavorable" is about the EVOLVING
extension, NOT the geometric core. Two distinct claims:
  (A) GEOMETRIC CORE   a0 = c^2 sqrt(Lambda/32pi)  -- tied to the CONSTANT cosmological constant -> a0 CONSTANT.
      This is the MOND scale = the de Sitter CURVATURE scale (sqrt(Lambda) ~ 1/length, x c^2 -> acceleration).
      Empirically SAFE: it is well-supported constant-a0 MOND, with a0's VALUE explained geometrically by Lambda.
  (B) EVOLVING CLAIM   a0(z) = cH(z)/Z            -- tied to the INSTANTANEOUS Hubble rate -> a0 RISES as E(z).
      Distinctive and falsifiable; the part that leans unfavorable; what the z~3 a0(z) test probes.
They agree to ~20% TODAY (cH0 ~ c^2 sqrt(Lambda) in our Lambda-dominated era) and diverge in the past. Needs numpy.
"""
import numpy as np

c=2.998e8; G=6.674e-11; Mpc=3.086e22; H0=67.4e3/Mpc; OmM=0.315; OmL=0.685
Z=2*np.sqrt(8*np.pi/3); Lam=3*OmL*H0**2/c**2
E=lambda z: np.sqrt(OmM*(1+z)**3+OmL)
a0_geom=c**2*np.sqrt(Lam/(32*np.pi))      # constant (tied to constant Lambda)
a0_obs=1.2e-10


def main():
    print("#"*96); print("# Geometric core (constant, safe) vs evolving claim (distinctive, leaning unfavorable)"); print("#"*96+"\n")
    print(f"  (A) GEOMETRIC  a0 = c^2 sqrt(Lambda/32pi) = {a0_geom:.3e}  (CONSTANT; = de Sitter curvature scale)")
    print(f"  (B) DYNAMICAL  a0(z) = cH(z)/Z                             (tracks the EVOLVING Hubble rate)")
    print(f"  observed a0 (SPARC) ~ {a0_obs:.1e}   [(A) reproduces it to {100*(1-a0_geom/a0_obs):.0f}% -- coeff route-chosen at that level]\n")
    print(f"  {'z':>4}{'(A) geometric/const':>22}{'(B) cH(z)/Z evolving':>22}{'B/A':>8}")
    for z in (0,0.5,1,2,3):
        aB=c*H0*E(z)/Z
        print(f"  {z:>4}{a0_geom:>22.3e}{aB:>22.3e}{aB/a0_geom:>8.2f}")
    print(f"\n  => agree ~20% TODAY (only epoch tested), diverge in the past.")
    print("="*96); print("VERDICT"); print("="*96)
    print("""  The GEOMETRIC CORE (A) -- the MOND scale equals the de Sitter curvature scale, a0 = c^2 sqrt(Lambda/32pi) --
  is real, robust, and EMPIRICALLY SAFE: it is constant-a0 MOND with a0's value explained by Lambda. The
  "leaning ~2-3 sigma unfavorable" verdict applies ONLY to the EVOLVING extension (B), a0(z)=cH(z)/Z, a separate
  and stronger hypothesis. Honest trade-off: (A) is safe but shared with Milgrom/Blanchet/CKN/Singh and NOT
  distinctively testable (predicts nothing different from constant-a0 MOND); (B) is distinctive and testable but
  disfavored. You cannot get distinctive AND safe from one version. Geometric relationship: YES, and it stands --
  it just is not, by itself, a distinctive prediction.""")
    print("#"*96)


if __name__=="__main__":
    main()
