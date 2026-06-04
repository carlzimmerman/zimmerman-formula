#!/usr/bin/env python3
"""
Wide binaries: the framework's (standard-MOND+EFE) prediction, the geometric transition scale, and why the test
is marginal by construction.
===============================================================================================================
Wide binaries (separation s > a few thousand AU) are the cleanest test of MOND's basic premise -- a low-
acceleration force-law change, with NO dark matter and NO cosmology, inside the Galaxy. For THIS framework they
test the *derived deep-MOND enhancement* (the sign) at z=0: if wide binaries are Newtonian, the central derived
result is locally falsified. The framework adds no new term here (a0(z=0) = today's value), so its prediction IS
standard MOND under the Milky Way external field.

KEY RESULTS:
 1. GEOMETRIC SCALE. The MOND radius r_M = sqrt(GM/a0) -- where a binary's internal acceleration drops below a0
    -- is the GEOMETRIC MEAN of the object's Schwarzschild radius r_s=2GM/c^2 and the cosmic horizon R_H=c/H0:
        r_M = (8pi/3)^(1/4) * sqrt(r_s * R_H)              [exact, given a0 = cH0/Z, Z=2sqrt(8pi/3)]
    For ~1 Msun this is ~7000 AU; wide binaries probe EXACTLY this scale. So a0=cH0/Z makes the wide-binary
    transition the geometric bridge between the smallest (r_s ~ km) and largest (R_H ~ 10^26 m) length scales.
 2. EFE SUPPRESSION. The Milky Way external field at the Sun is g_ext ~ V^2/R ~ 1.86 a0 -- ABOVE a0. Wide
    binaries are therefore EFE-DOMINATED: the external field partially Newtonizes them, suppressing the orbital-
    velocity boost from the isolated deep-MOND +41% (sqrt2) down to ~3-15%, the exact value set by the (uncertain)
    interpolation function. The framework's OWN derived (DSSYK, sharp/standard-like) interpolation sits at the
    SMALL end (~3-5%).
 3. WHY IT IS CONTESTED. The predicted signal (~5-15%) is small by construction, and the observational camps
    (Chae: detection ~+15-20% velocity / gravity-boost ~1.4; Banik/Pittordis: ~0%, Newtonian at 19 sigma) sit on
    either side of it. The dispute is driven by triple-system contamination, eccentricity priors, and orbital/
    statistical modeling -- and recent (2025-2026) methodological papers find the anomaly is *sensitive to those
    choices*. So the test is genuinely marginal and currently neither confirms nor refutes the framework.

This script reproduces the numbers. Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; Msun = 1.989e30; H0 = 67e3/3.086e22
Z = 2*np.sqrt(8*np.pi/3); AU = 1.496e11
a0 = c*H0/Z


def nu_simple(y):   return (1+np.sqrt(1+4/y))/2.0          # mu(x)=x/(1+x)
def nu_standard(y): return np.sqrt((1+np.sqrt(1+4/y**2))/2.0)  # mu(x)=x/sqrt(1+x^2)


def efe_boost(nu, y, h=1e-4):
    """Orbital-velocity boost sqrt(G_eff/G) for an internal binary deep in MOND, in a dominant external
    field g_ext = y*a0 (angle-averaged QUMOND estimate G_eff/G = nu_e*(1+L_e/3), L_e=dln nu/dln g)."""
    nue = nu(y)
    L = (np.log(nu(y*(1+h)))-np.log(nu(y*(1-h))))/(2*h)
    return np.sqrt(max(nue*(1+L/3.0), 1.0))


def main():
    print("#"*94)
    print("# Wide binaries: framework prediction (standard MOND+EFE), the geometric scale, and the marginal test")
    print("#"*94 + "\n")

    print("="*94); print("1. THE GEOMETRIC TRANSITION SCALE: r_M = geometric mean of r_s and R_H"); print("="*94)
    for M in (1.0, 1.4):
        rM = np.sqrt(G*M*Msun/a0); rs = 2*G*M*Msun/c**2; RH = c/H0
        print(f"  M={M} Msun: r_M={rM/AU:6.0f} AU | r_s={rs/1e3:6.2f} km | R_H={RH:.2e} m | "
              f"r_M/sqrt(r_s R_H)={rM/np.sqrt(rs*RH):.4f} = (8pi/3)^1/4={ (8*np.pi/3)**0.25:.4f}")
    print("  => a0=cH0/Z makes the wide-binary transition (~7000 AU) the geometric mean of the Schwarzschild")
    print("     radius (~km) and the cosmic horizon (~10^26 m). The test probes exactly this geometric scale.\n")

    print("="*94); print("2. EFE SUPPRESSION: the MW external field is above a0, so the boost is small"); print("="*94)
    y = 1.86  # g_ext/a0 at the Sun
    print(f"  g_ext(Sun) ~ V^2/R = {y:.2f} a0  (EFE-dominated regime)")
    print(f"  predicted orbital-velocity boost at the widest separations (internal a << a0):")
    print(f"    isolated deep-MOND, no EFE : +41%  (sqrt2, the naive expectation)")
    print(f"    simple   mu + EFE          : +{(efe_boost(nu_simple,y)-1)*100:.0f}%")
    print(f"    standard mu + EFE          : +{(efe_boost(nu_standard,y)-1)*100:.0f}%   (the framework's derived interpolation is standard-like -> here)")
    print(f"  => EFE knocks the signal down to ~3-15%; the value is interpolation-function-dependent.\n")

    print("="*94); print("3. WHERE THE DATA CAMPS SIT (all inside the same small band)"); print("="*94)
    print("""  Chae (2023-2026):  velocity boost ~+15-20% (gravity-boost g_obs/g_N ~ 1.4), >~3.5-5 sigma 'anomaly'
                     -> at/above the simple-mu+EFE prediction.
  Banik 2024 / Pittordis & Sutherland: ~0% (Newtonian), up to 19 sigma vs MOND
                     -> below even the standard-mu+EFE prediction.
  Recent 2025-26 (realistic-triples; 'No evidence for MOND'; 'sensitive to orbital modeling'): lean Newtonian /
                     not-robust. Crux = triple contamination + eccentricity priors + statistical modeling.
  => the framework's EFE-suppressed prediction (~3-15%) lives INSIDE the contested 0-20% band. The signal is
     marginal BY CONSTRUCTION, which is exactly why method choices flip the verdict. Genuinely unresolved;
     Gaia DR4 astrometry is the hoped-for arbiter, not yet decisive.\n""")

    print("="*94); print("VERDICT for the framework"); print("="*94)
    print("""  Wide binaries are a z=0 test of the framework's DERIVED deep-MOND enhancement -- clean (no DM, no
  cosmology) but currently MARGINAL and CONTESTED. The framework predicts a small, EFE-suppressed boost (~3-15%,
  its own sharp interpolation at the low end), so it does not strongly predict either camp's result. Honest
  status: wide binaries NEITHER confirm NOR refute the framework today. If the recent skeptical (Newtonian) trend
  hardens with Gaia DR4, it is a real problem for the *premise* that local MOND is real (on which the a0(z) work
  rests); if Chae's anomaly survives, it supports it. We do NOT lean either way -- correcting the repo's earlier
  pro-Chae summary, and noting our own past wide-binary data analysis was a velocity units bug (discarded).""")
    print("="*94)


if __name__ == "__main__":
    main()
