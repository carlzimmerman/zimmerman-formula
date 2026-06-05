#!/usr/bin/env python3
"""
The Faber-Jackson / velocity-dispersion channel for a0(z): real prediction, but NOT a clean test. Literature-checked.
====================================================================================================================
Carl asked to explore the pressure-supported channel and the literature. Done (THE_FABER_JACKSON_CHANNEL.md). The
prediction is real; the test is degenerate AND in the wrong acceleration regime; and the directly-relevant PUBLISHED
tests already DISFAVOR the evolving (a0~cH) coupling while FAVORING the constant/geometric (a0~sqrt(Lambda)) one.

THE PREDICTION (real, standard): deep-MOND Faber-Jackson sigma^4 = (4/9) G M a0 (Milgrom 1984 ApJ 287,571;
coefficient from Sanders 2010 MNRAS 407,1128). With a0(z)=cH(z)/Z, at FIXED baryonic mass M: sigma proportional
a0^(1/4) proportional E(z)^(1/4). Magnitudes: +16% at z=1, +32% at z=2. Arithmetically correct.

WHY IT IS NOT A CLEAN TEST (three honest strikes):
 1. DEGENERACY (worse than the disk RAR): high-z quiescent galaxies are a factor ~2-4 more COMPACT at fixed mass;
    sigma^2 ~ GM/R, so a factor-2 size shrink alone raises sigma by ~sqrt(2)=+41% -- larger than, same sign as, and
    degenerate with the +32% MOND effect. No clean separator (Belli+2014; Bezanson+2013 mass-FP in place by z~2).
 2. WRONG REGIME: the FJ relation needs the GLOBAL, large-radius, low-acceleration (g<<a0) dispersion. High-z
    dispersions are CENTRAL, at g ~ 3-11 a0 (Milgrom 2017 arXiv:1703.06110) -- near-Newtonian -- so sigma^4=(4/9)GMa0
    is not even the operative physics. The deep-MOND dispersion regime is reached only in globular-cluster outer
    profiles / dSph (Scarpa & Marconi), inaccessible at z>1.
 3. THE PUBLISHED DIRECT TESTS DISFAVOR EVOLVING a0:
      - Limbach, Psaltis & Ozel 2008 (arXiv:0809.2790): Tully-Fisher to z=1.2 tests a0~cH0 AND a0~sqrt(Lambda);
        both excluded within formal errors, but the data MARGINALLY FAVOR sqrt(Lambda) (constant/geometric) over H(z).
      - Milgrom 2017 (arXiv:1703.06110): high-z disks "all but exclude ~4 a0 at z~2, excluding a0 ~ (1+z)^1.5".
    The framework's E(2)=3.0 a0 is milder than the excluded (1+z)^1.5 = 5.2, but uncomfortably close to the ~4 line.
Needs numpy.
"""
import numpy as np

c=2.998e8; Mpc=3.086e22; H0=67.4e3/Mpc; Z=2*np.sqrt(8*np.pi/3)
E=lambda z: np.sqrt(0.315*(1+z)**3+0.685)


def main():
    print("#"*100); print("# Faber-Jackson / sigma channel for a0(z): real prediction, NOT a clean test"); print("#"*100+"\n")

    print("="*100); print("(1) the prediction: sigma proportional E(z)^(1/4) at fixed baryonic mass (deep-MOND FJ)"); print("="*100)
    print(f"   sigma^4 = (4/9) G M a0  (Milgrom 1984; Sanders 2010) -> sigma(z)/sigma(0) = (a0(z)/a0(0))^(1/4) = E(z)^(1/4)")
    for z in (0.5,1,2,3):
        print(f"     z={z}: E={E(z):.2f}, predicted sigma elevation at fixed M = +{100*(E(z)**0.25-1):.0f}%")
    print()

    print("="*100); print("(2) strike 1 -- DEGENERACY with structural (compactness) evolution"); print("="*100)
    for fac in (2,3,4):
        print(f"     high-z size smaller by x{fac} at fixed M -> sigma up sqrt({fac}) = +{100*(np.sqrt(fac)-1):.0f}% (Newtonian, no MOND)")
    print(f"   the observed compactness effect (+41% to +100%) EXCEEDS and mimics the +32% MOND prediction -> degenerate.\n")

    print("="*100); print("(3) strike 2 -- WRONG REGIME: high-z dispersions are central (Newtonian), not deep-MOND"); print("="*100)
    print(f"   FJ relation needs g << a0 (global, large-radius). High-z sigma are CENTRAL: g ~ 3-11 a0 (Milgrom 2017).")
    print(f"   At g ~ 3-11 a0 the dynamics are near-Newtonian -> sigma^4=(4/9)GMa0 does NOT apply. Test invalid there.\n")

    print("="*100); print("(4) strike 3 -- the PUBLISHED direct tests disfavor evolving a0, favor the geometric core"); print("="*100)
    print(f"   {'test':<46}{'probes':>22}{'verdict':>26}")
    print(f"   {'Limbach-Psaltis-Ozel 2008 (TF to z=1.2)':<46}{'a0~cH0 vs a0~sqrtLam':>22}{'favors sqrt(Lambda)=CONST':>26}")
    print(f"   {'Milgrom 2017 (high-z disks)':<46}{'a0(z~2)':>22}{'all-but-excl ~4 a0':>26}")
    print(f"   framework: a0(z=2)/a0 = E(2) = {E(2):.2f}  (excluded (1+z)^1.5 = {(1+2)**1.5:.2f}; milder, but near the ~4 line)")
    print(f"   => Limbach 2008 literally compared the EVOLVING (cH) vs GEOMETRIC (sqrtLambda) couplings and favored the")
    print(f"      GEOMETRIC one -- a published result aligning with THE_GEOMETRIC_CORE_VS_THE_EVOLVING_CLAIM.md.\n")

    print("="*100); print("VERDICT"); print("="*100)
    print("""  The sigma proportional E(z)^(1/4) prediction is real and standard, but the Faber-Jackson channel is NOT a clean
  independent test of a0(z): (1) it is degenerate with the larger, same-sign compactness evolution; (2) high-z
  dispersions are central/near-Newtonian (g~3-11 a0), the wrong regime for the deep-MOND FJ relation; (3) the
  closest PUBLISHED tests (Limbach+2008, Milgrom 2017) already disfavor a0~cH(z) and favor a0~sqrt(Lambda)=constant.
  It is the existing a0(z) door wearing different clothes -- and it points the same way the disk data do: AGAINST the
  evolving extension, FOR the geometric/constant core. (Also: highz_kinematic_test.py's 'mildly favors evolving'
  read is RETRACTED -- those z~6 dispersions are central, not deep-MOND, and degenerate with low star-formation
  efficiency.) No new door; one more confirmation that the distinctive evolving claim leans unfavorable.""")
    print("#"*100)


if __name__=="__main__":
    main()
