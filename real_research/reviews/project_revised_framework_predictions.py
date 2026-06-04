#!/usr/bin/env python3
"""
The horizon revision FLIPS predictions -- and the one with data (RC100 f_DM) favors the revised framework.
=========================================================================================================
The which-horizon resolution (project_which_horizon_dssyk.py) replaced the original RISING a0 ~ cH (apparent
horizon) with the DSSYK-consistent a0 ~ sqrt(rho_DE) (event horizon), which is CONSTANT-to-mildly-DECLINING
(DESI). Flipping the sign of the a0 evolution flips several downstream predictions; here are the two concrete
ones, with the honest finding that the data-anchored one (galaxy dark-matter fraction vs z) FAVORS the revised
(declining) reading -- the same trend the original rising reading got BACKWARDS.

FLIP 1 -- the cluster missing-mass factor eta(z). Rising a0 => more MOND boost at high z => eta SHRINKS; a
declining a0 => less boost => eta GROWS (or stays flat). Opposite sign. (Small at the z<1 of eRASS1; a forecast
for resolved high-z cluster profiles.)

FLIP 2 -- the galaxy dark-matter fraction f_DM(R_e) vs z, against REAL data. RC100 (Nestor Shachar 2023) finds
f_DM ~ 0.38 at z~1 and 0.27 at z~2 -- it DECREASES. In MOND f_DM(R_e) = 1 - 1/nu(g_bar/a0), so the decrease
needs g_bar/a0 to RISE z1->z2 (inferred 1.0 -> 2.0). Decomposing that into the density (g_bar) increase each a0
law requires:
  * RISING a0 (original): needs g_bar to jump ~3.3x from z~1 to z~2 -- implausible (size evolution gives ~2.25x).
  * DECLINING a0 (event): needs ~1.7x -- comfortably within plausible density evolution.
  * constant a0:          needs ~1.9x -- also fine.
So the observed f_DM DECREASE is naturally accommodated by the DECLINING (or constant) a0 and STRAINED by the
rising one. The revised framework predicts the right sign of the dark-fraction-vs-redshift trend; the original
rising headline predicted the wrong sign (project_bigwheel_framework_prediction.py TEST 3 already flagged this).

HONEST: f_DM(z) is a population trend with scatter and selection, so this FAVORS but does not PROVE the
declining reading; and at z<1 the cluster flip is too small to test with current integrated masses. But it is a
genuine, real-data-anchored consequence of the revision, and it points the same way as the high-z disks and
DESI -- a coherent picture. Needs numpy + scipy.
"""
import numpy as np
from scipy.optimize import brentq

Om, OL = 0.315, 0.685
a0 = 1.2e-10
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
nu = lambda y: 0.5 + np.sqrt(0.25 + 1/y)


def rho_de(z, w0=-0.8, wa=-0.7):
    a = 1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))


a0_rise = lambda z: a0*E(z)                    # apparent horizon (ORIGINAL, revised away)
a0_decl = lambda z: a0*np.sqrt(rho_de(z))      # event horizon ~ sqrt(rho_DE), DESI (REVISED)
a0_const = lambda z: a0 + 0*z


def main():
    print("#"*92)
    print("# The horizon revision FLIPS predictions -- and the RC100 dark-fraction trend favors the revision")
    print("#"*92 + "\n")
    print("  REVISION: a0 ~ cH (rising, original) -> a0 ~ sqrt(rho_DE) (event horizon; constant-to-declining).\n")

    print("="*92); print("FLIP 1 -- cluster missing-mass factor eta(z) (representative g_bar ~ 0.6 a0_local)"); print("="*92)
    gx = 0.6*a0
    print(f"  {'z':>4}{'rising (orig)':>15}{'DECLINING (event/DESI)':>24}{'constant':>10}")
    for z in (0.0, 0.5, 1.0, 2.0):
        er = 1.8*nu(gx/a0_rise(0))/nu(gx/a0_rise(z))
        ed = 1.8*nu(gx/a0_decl(0))/nu(gx/a0_decl(z))
        print(f"  {z:>4.1f}{er:>15.2f}{ed:>24.2f}{1.80:>10.2f}")
    print("""  => the SIGN flips: rising a0 -> eta SHRINKS with z; declining a0 -> eta GROWS. (Small at z<1; a forecast
     for resolved high-z cluster profiles -- the eRASS1 integrated masses cannot test it, see
     project_cluster_erass1_a0z.py.)\n""")

    print("="*92); print("FLIP 2 -- galaxy f_DM(z) vs REAL data (RC100), the decisive one"); print("="*92)
    print("  RC100 (Nestor Shachar 2023): f_DM(R_e) ~ 0.38 (z~1), 0.27 (z~2) -- DECREASES with z.")
    y_of = lambda f: brentq(lambda y: (1 - 1/nu(y)) - f, 1e-3, 100)
    y1, y2 = y_of(0.38), y_of(0.27)
    print(f"  MOND inversion f_DM = 1 - 1/nu(g_bar/a0): inferred g_bar/a0 = {y1:.2f} (z~1) -> {y2:.2f} (z~2).")
    print(f"  Required baryonic-density increase g_bar(z~2)/g_bar(z~1) under each a0 law:")
    print(f"    {'a0 law':22}{'g_bar ratio z1->z2':>20}{'plausible? (~2.25x)':>22}")
    for lab, fn in [("rising (original)", a0_rise), ("DECLINING (event)", a0_decl), ("constant", a0_const)]:
        ratio = (y2*fn(2.0))/(y1*fn(1.0))
        verdict = "STRAINED (too big)" if ratio > 2.7 else "plausible"
        print(f"    {lab:22}{ratio:>18.2f}x{verdict:>22}")
    print("""  => the observed f_DM DECREASE needs an implausible ~3.3x density jump under the RISING a0, but a
     comfortable ~1.7-1.9x under DECLINING/constant. The revised (event-horizon, declining) framework predicts
     the RIGHT sign of the dark-fraction-vs-redshift trend; the original rising reading predicted the WRONG
     sign. Real data, favoring the revision.\n""")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  The horizon revision is not just internally tidier -- it makes concrete, FLIPPED predictions, and the one
  anchored to real data (RC100 f_DM(z)) favors it: massive galaxies being MORE baryon-dominated at high z is
  what a declining a0 predicts and what the original rising a0 got backwards. Together with the high-z disks
  (a0 not risen) and DESI (rho_DE weakening -> a0 declining), three independent lines now point the same way:
  a0 tracks the de Sitter EVENT horizon (sqrt rho_DE), constant-to-declining, NOT the apparent horizon (rising).
  HONEST: f_DM(z) is a population trend (scatter + selection), so it FAVORS, not proves; the cluster flip is too
  small to test below z~1 with integrated masses. But the revised framework is now coherent across galaxies
  (RAR + f_DM trend), the high-z disks, and DESI -- where the original rising version was in tension with all
  three. A genuine, data-supported consequence of correcting the horizon.""")
    print("="*92)


if __name__ == "__main__":
    main()
