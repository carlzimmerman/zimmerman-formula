#!/usr/bin/env python3
"""
The last two scale-fixing mechanism classes: BOUND SATURATION (max force / min accel) and DIMENSIONAL TRANSMUTATION.
====================================================================================================================
The structural obstruction (symmetry fixes the cubic FORM but never the symmetry-BREAKING SCALE a0) closes every
SYMMETRY route to forcing the coefficient. But symmetry is only ONE of the three ways physics fixes a scale or a
dimensionless coefficient. The other two are NOT symmetries, so they could in principle evade the obstruction:
  (2) BOUND SATURATION -- a maximum force F=c^4/4G (Gibbons 2002, Schiller), a minimal acceleration, a horizon
      surface gravity. A bound is not a symmetry; saturating it can fix an O(1).
  (3) DIMENSIONAL TRANSMUTATION -- a dimensionless coupling + RG running generates a scale (Lambda_QCD paradigm).
This script checks (2) head-on and characterizes (3). RESULT: neither forces 32pi. Bound saturation reproduces the
SCALE a0~cH (coefficient O(1)) but lands in the HORIZON/KINEMATIC cluster (cH/a0 ~ 1-2), NOT the framework's
DENSITY cluster (cH/a0 ~ 5.8-6.3) and NOT 32pi/3=33.5. So the coefficient spread is even wider than the 5.79-6.28
previously emphasized: it spans TWO O(1) clusters (1-2 kinematic, ~6 density/thermal), and no bound selects the
framework's value -- that comes specifically from the density factor sqrt(3/8pi). Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; Mpc = 3.086e22
H0 = 67.4e3/Mpc; L = c/H0                     # Hubble / de Sitter radius
Lam = 3*H0**2/c**2                            # de Sitter Lambda = 3H^2/c^2 (Omega_Lambda->1 floor)
rho_L = Lam*c**2/(8*np.pi*G)                  # vacuum mass density
Z = 2*np.sqrt(8*np.pi/3)                      # framework coefficient cH/a0 = 5.789
a0_fw = (c/2)*np.sqrt(G*rho_L)                # framework a0 (density / free-fall route)
Fmax = c**4/(4*G)                             # Gibbons-Schiller maximum force
cH = c**2/L                                   # = cH0


def coeff(a):                                  # report cH/a0 and Lambda c^4 / a0^2
    return cH/a, Lam*c**4/a**2


def main():
    print("#"*100); print("# Bound saturation (max force/min accel) + dimensional transmutation: do they force 32pi?"); print("#"*100 + "\n")
    print(f"  framework a0 (density route) = {a0_fw:.3e};  cH/a0 = Z = {Z:.3f};  Lam c^4/a0^2 = 32pi = {32*np.pi:.2f}\n")

    print("="*100); print("(2) BOUND SATURATION -- compute a0 candidate from each bound, read the coefficient"); print("="*100)
    print(f"   {'bound-saturation principle':<46}{'a0 [m/s^2]':>12}{'cH/a0':>9}{'Lc^4/a0^2':>12}")
    rows = [
        ("naive horizon  a = c^2/L = cH",            cH),
        ("de Sitter surface gravity  k=c^2/2L",      c**2/(2*L)),
        ("max force / Hubble mass  Fmax/(c^2 L/2G)",  Fmax/(c**2*L/(2*G))),
        ("Unruh accel = de Sitter temp  a=cH",        cH),
        ("max force / vacuum mass in horizon volume", Fmax/(rho_L*(4/3*np.pi*L**3))),
    ]
    for name, a in rows:
        r1, r2 = coeff(a)
        print(f"   {name:<46}{a:>12.3e}{r1:>9.3f}{r2:>12.2f}")
    print(f"   {'-- framework (density/free-fall route) --':<46}{a0_fw:>12.3e}{cH/a0_fw:>9.3f}{Lam*c**4/a0_fw**2:>12.2f}")
    print(f"   => every bound lands cH/a0 ~ 1-2 (the HORIZON/KINEMATIC cluster), NOT the framework's 5.79")
    print(f"      and NOT 32pi/3=33.5. Bound saturation CONFIRMS the scale a0~cH; it does NOT force the coefficient.\n")

    print("="*100); print("(3) DIMENSIONAL TRANSMUTATION -- would it give 32pi? No."); print("="*100)
    print("   Transmutation generates a scale from a dimensionless coupling g via RG: mu ~ Mcut * exp(-1/(b g)).")
    print("   * The induced dimensionless ratio is an EXPONENTIAL exp(-1/bg) of the coupling -- a transcendental")
    print("     tuned by g, never a clean 32pi (you would have to pick g to MAKE it 32pi -- that is fitting, not")
    print("     forcing).")
    print("   * There is no identified running coupling whose IR fixed value generates a0; a0 ~ cH is an IR/horizon")
    print("     scale set by Lambda, not a UV-transmuted dynamical scale. So transmutation does not apply cleanly,")
    print("     and where it would apply it gives exp(-1/bg), not 32pi.\n")

    print("="*100); print("THE MECHANISM-CLASS CLOSURE"); print("="*100)
    print(f"""  All THREE ways physics fixes a scale/coefficient are now checked:
    (1) SYMMETRY            -> fixes the cubic FORM, never the breaking SCALE (structural; proven).
    (2) BOUND SATURATION    -> reproduces a0~cH at coefficient O(1)~1-2 (kinematic cluster); does NOT give 5.79/32pi.
    (3) DIM. TRANSMUTATION  -> would give exp(-1/bg), a tuned transcendental; no clean 32pi, no a0 coupling anyway.
  Plus the worked QG routes (DSSYK, AeST, entanglement, heat-kernel), all negative. CONCLUSION: the SCALE a0~cH is
  over-determined -- EVERY mechanism reproduces it -- but the COEFFICIENT is fixed by NO mechanism; it spans two O(1)
  clusters (kinematic ~1-2, density/thermal ~6) and the framework's 5.789 comes specifically from the density factor
  sqrt(3/8pi) of the Friedmann route. Z = 2sqrt(8pi/3) stays GR-traceable (8pi, 3) and route-forced, NOT uniquely
  forced -- now closed across all three mechanism classes, not just the symmetry ones.""")
    print("#"*100)


if __name__ == "__main__":
    main()
