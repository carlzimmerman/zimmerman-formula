#!/usr/bin/env python3
"""
REAL-DATA cluster a0(z) test on eRASS1 -- and the honest finding: R500 data CANNOT cleanly test it.
===================================================================================================
We pushed the "rising a0 => the cluster mass discrepancy shrinks with z" idea onto real data: the eROSITA
eRASS1 cluster catalog (Bulbul+2024), 12,247 clusters, one homogeneous pipeline, z=0.003-1.32, tabulating
M500 (WL-calibrated), MGAS500, FGAS500, R500 per cluster. Clean sample (0<z<1, valid masses, 0.01<fgas<0.30):
N~9830, z to ~0.66. At R500 the accelerations are g_bar ~ 0.03 a0 (deep MOND), and the MOND missing-mass
factor eta = g_obs/(nu(g_bar/a0) g_bar) ~ 1.9 -- the classic factor-2 cluster problem, reproduced from real
data.

THE TRAP WE CAUGHT. The cluster effective acceleration scale a0_eff = g_obs^2/g_bar RISES with z, and fitting
a0_eff ~ A E(z)^beta gives beta = 1.03 +- 0.05 -- which LOOKS like a stunning confirmation of a0 ∝ cH(z)/Z ∝
E(z). It is NOT. a0_eff = g_obs^2/g_bar is a KINEMATIC combination: with R500 the standard overdensity radius
(verified: R500_tab/R500_overdensity = 0.975), a0_eff = G M500^(1/3) E(z)^(4/3) / f_bar EXACTLY -- the E(z)
scaling comes from the overdensity-radius definition (R500 ∝ E^-2/3 => g ∝ E^4/3), NOT from the MOND a0. Pure
geometry gives beta = 4/3 = 1.33; mass selection (M500 rises 1.1->2.6e14 with z in this flux-limited sample)
and f_bar evolution pull it to the measured 1.03. So the "signal" carries no a0(z) information.

WHY R500 DATA STRUCTURALLY CANNOT TEST a0(z): (1) at R500 every cluster is deep-MOND (g_bar << a0), so there
is NO transition region in which a0 is located; the a0 dependence enters only through the transition shape,
which lives at smaller radii (cluster cores, g_bar ~ a0) absent from integrated R500 quantities. (2) the
deep-MOND amplitude a0_eff = eta^2 a0 is DARK-dominated (eta~1.9), and its z-evolution is kinematics +
selection + the cluster dark-fraction evolution, all degenerate with any true a0(z). The catalog's only fixed-
physical aperture (300 kpc) has count-rate/flux/luminosity but NO mass, so the geometry-free test is not
possible here either.

HONEST VERDICT: real data, real measurement, but a NEGATIVE methodological result -- eRASS1 R500 integrated
masses are CONSISTENT with the framework (a0 ∝ E(z) + a z-stable dark fraction is one natural reading) yet
CANNOT detect or test rising a0: the apparent a0_eff(z) ∝ E^1.03 is overdensity kinematics, not physics. A
clean test needs the acceleration at a FIXED baryonic/physical scale reaching the MOND transition (g_bar ~ a0)
across z -- resolved hydrostatic profiles (XRISM/Athena, or a uniform profile reanalysis of X-COP/CHEX-MATE-
class samples), not integrated overdensity masses. Catching the kinematic artifact is the result. Needs numpy,
scipy, astropy + the eRASS1 catalog in ../data/.
"""
import os
import sys
import numpy as np
from scipy.optimize import curve_fit

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data"))
import _load_erass1 as L  # noqa: E402

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
A0 = 1.2e-10
Msun, kpc, G = 1.989e30, 3.086e19, 6.674e-11
H0 = 67*1e3/(3.086e22); RHO_C0 = 3*H0**2/(8*np.pi*G)
EDGES = np.array([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.70])


def main():
    print("#"*92)
    print("# REAL eRASS1 cluster a0(z) test -- and why R500 integrated data cannot cleanly test it")
    print("#"*92 + "\n")
    c = L.load_clean()
    z, gobs, gbar, M500, fgas, R500 = c["z"], c["gobs"], c["gbar"], c["M500"], c["fgas"], c["R500"]
    nu = lambda y: 0.5 + np.sqrt(0.25 + 1/y)
    eta = gobs/(nu(gbar/A0)*gbar)
    print("="*92); print("(1) THE REAL SAMPLE & DISCREPANCY (reproduces the known factor-2 cluster problem)"); print("="*92)
    print(f"  eRASS1 (Bulbul+2024), clean cut: N = {c['N']} clusters, z median {np.median(z):.2f} (10-90%: "
          f"{np.percentile(z,10):.2f}-{np.percentile(z,90):.2f}).")
    print(f"  at R500: g_bar/a0 median {np.median(gbar)/A0:.3f} (deep MOND; {100*(gbar<0.1*A0).mean():.0f}% have g_bar<0.1a0),"
          f" g_obs/a0 {np.median(gobs)/A0:.2f}.")
    print(f"  Newtonian discrepancy g_obs/g_bar = 1/f_bar ~ {np.median(gobs/gbar):.1f}; MOND deep-regime boost nu ~ "
          f"{np.median(nu(gbar/A0)):.1f}; residual eta ~ {np.median(eta):.2f} (= classic factor-2).\n")

    print("="*92); print("(2) THE APPARENT SIGNAL: a0_eff = g_obs^2/g_bar rises as E(z)^beta, beta ~ 1"); print("="*92)
    a0eff = gobs**2/gbar
    zc, ac, ae = [], [], []
    print(f"  {'z_med':>7}{'N':>6}{'a0_eff/a0':>11}")
    rng = np.random.RandomState(0)
    for i in range(len(EDGES)-1):
        m = (z >= EDGES[i]) & (z < EDGES[i+1])
        if m.sum() < 30:
            continue
        am = np.median(a0eff[m])
        aerr = np.std([np.median(rng.choice(a0eff[m], m.sum())) for _ in range(300)])
        print(f"  {np.median(z[m]):>7.3f}{int(m.sum()):>6}{am/A0:>11.3f}")
        zc.append(np.median(z[m])); ac.append(am); ae.append(aerr)
    zc, ac, ae = map(np.array, (zc, ac, ae))
    fE = lambda x, A, b: A*x**b
    pE, cE = curve_fit(fE, E(zc), ac/A0, sigma=ae/A0, absolute_sigma=True, p0=[3, 1])
    p1, c1 = curve_fit(fE, 1+zc, ac/A0, sigma=ae/A0, absolute_sigma=True, p0=[3, 1])
    print(f"  fit a0_eff/a0 = A E(z)^beta : A={pE[0]:.2f}, beta={pE[1]:.2f}+-{np.sqrt(cE[1,1]):.2f}  "
          f"(looks like a0 ∝ E(z)!)")
    print(f"  fit a0_eff/a0 = A (1+z)^beta: A={p1[0]:.2f}, beta={p1[1]:.2f}+-{np.sqrt(c1[1,1]):.2f}\n")

    print("="*92); print("(3) THE TRAP: a0_eff is KINEMATIC -- the E(z) is the overdensity radius, not a0"); print("="*92)
    rho_cz = RHO_C0*E(z)**2
    R500_od = (M500*1e13*Msun/((4/3)*np.pi*500*rho_cz))**(1/3)/kpc
    print(f"  R500(tabulated)/R500(500*rho_c(z) overdensity) = {np.median(R500/R500_od):.3f} -> R500 IS the")
    print(f"  overdensity radius. Then identically  a0_eff = g_obs^2/g_bar = G M500^(1/3) E(z)^(4/3) / f_bar :")
    ident = G*(M500*1e13*Msun)**(1/3)*E(z)**(4/3)/(1.2*fgas) / (kpc**0)  # check ratio to a0eff (units consistency below)
    # dimensionless check: ratio a0eff / [G M^{1/3} E^{4/3}/f_bar * (overdensity const)]
    Cod = ((4/3)*np.pi*500*RHO_C0)**(2/3)                       # from R500^2 = (M/( (4/3)pi500 rho_c0 E^2))^{2/3}
    pred = G*(M500*1e13*Msun)**(1/3)*E(z)**(4/3)*Cod/(1.2*fgas*Msun**(0))  # G M^{1/3} E^{4/3} (4/3 pi 500 rho_c0)^{2/3} / f_bar
    print(f"     a0_eff / [G M500^(1/3) E^(4/3) (4/3 pi 500 rho_c0)^(2/3) / f_bar] = {np.median(a0eff/pred):.3f} (=1: identity holds)")
    print(f"  => pure geometry (fixed M, f_bar) gives beta_E = 4/3 = 1.33. The sample's mass selection")
    print(f"     (M500 median rises {np.median(M500[z<0.15])*1e13/1e14:.2f}->{np.median(M500[z>0.5])*1e13/1e14:.2f} e14) and f_bar evolution pull 1.33 down to the measured ~1.03.")
    print(f"     The a0_eff(z) rise is OVERDENSITY KINEMATICS + SELECTION, carrying NO clean a0(z) signal.\n")

    print("="*92); print("VERDICT -- honest"); print("="*92)
    print("""  We did it on real data (9830 eRASS1 clusters) and reproduced the factor-2 cluster discrepancy. The
  apparent a0_eff ∝ E(z)^1.0 is NOT a detection of rising a0: it is the R500 overdensity geometry (g ∝ E^4/3),
  modulated by flux-limited mass selection and f_bar evolution. R500 integrated data STRUCTURALLY cannot test
  the MOND a0(z): (i) at R500 all clusters are deep-MOND, so there is no transition region in which a0 lives;
  (ii) the deep-MOND amplitude is dark-dominated and degenerate with the cluster dark-fraction evolution. The
  result is CONSISTENT with the framework (a0 ∝ E(z) + a z-stable dark fraction is a natural reading) but does
  NOT confirm it. A clean test needs the acceleration at a FIXED baryonic scale reaching the MOND transition
  (g_bar ~ a0) across z -- resolved hydrostatic profiles (XRISM/Athena; or a uniform X-COP/CHEX-MATE profile
  reanalysis), not integrated overdensity masses. The deliverable is the caught artifact and the sharpened,
  correct requirement -- not a manufactured confirmation.""")
    print("="*92)


if __name__ == "__main__":
    main()
