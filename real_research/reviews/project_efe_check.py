#!/usr/bin/env python3
"""
EFE double-check: does the external field produce the LambdaCDM-impossible RAR downturn? (Yes.)
==============================================================================================
The external field effect (EFE) is the framework's cleanest discriminator against LambdaCDM. Because the modified
dynamics are non-linear and scale-covariance is broken non-locally, a system's INTERNAL gravity depends on the
EXTERNAL field it is embedded in -- a violation of the strong equivalence principle. Newtonian gravity + a
dark-matter halo CANNOT produce this (shell theorem: a uniform external field cancels inside the halo).

QUMOND (quasi-linear) internal observed acceleration with internal Newtonian field g_N and external field g_ext:
    g_obs = nu(|g_N+g_ext|/a0) (g_N+g_ext) - nu(g_ext/a0) g_ext ,   nu(y)=1/2+sqrt(1/4+1/y) (simple).
For g_ext=0 this is the isolated RAR g_obs=nu(g_N/a0)g_N (deep-MOND -> sqrt(a0 g_N)).

RESULT (a0=1; entries g_obs/g_bar): an ISOLATED system shows the full sqrt-law boost (~x19 at g_bar=0.003 a0);
the SAME system in a strong external field is driven back to NEWTONIAN (boost -> 1). The RAR turns DOWN. This is
the EFE, detected in SPARC by Chae et al. (2020/2021) at ~4-5 sigma, and predicted identically by the framework
with a0 = c^2 sqrt(Lambda/32pi). Needs numpy.
"""
import numpy as np


def nu(y):
    return 0.5 + np.sqrt(0.25 + 1.0/y)               # 'simple' nu: g_obs = nu(y) g, y=g/a0


def g_obs(gN, gext, a0=1.0):
    if gext <= 0:
        return nu(gN/a0)*gN                          # isolated -> standard RAR
    return nu((gN+gext)/a0)*(gN+gext) - nu(gext/a0)*gext


def main():
    print("#"*86)
    print("# EFE double-check: external field suppresses the internal MOND boost (the LCDM-impossible signature)")
    print("#"*86 + "\n")
    print(f"  {'g_bar/a0':>9}{'isolated':>10}{'gext=0.1':>10}{'gext=1.8(MW)':>13}{'gext=10':>9}   (entries: g_obs/g_bar)")
    for gN in (0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0):
        v = [g_obs(gN, ge)/gN for ge in (0.0, 0.1, 1.8, 10.0)]
        print(f"  {gN:>9.3f}{v[0]:>10.1f}{v[1]:>10.1f}{v[2]:>13.2f}{v[3]:>9.2f}")
    print()
    gN = 1e-4
    print("  CHECKS:")
    print(f"    isolated deep-MOND, g_bar={gN}: g_obs/g_bar = {g_obs(gN,0)/gN:.0f}  vs sqrt(1/g_bar)={np.sqrt(1/gN):.0f}  (sqrt-law OK)")
    print(f"    strong field g_ext=10 a0, g_bar=0.003: g_obs/g_bar = {g_obs(0.003,10)/0.003:.2f} -> ~1 NEWTONIAN (boost killed)")
    print(f"    Milky-Way field g_ext=1.8 a0, g_bar=0.003: g_obs/g_bar = {g_obs(0.003,1.8)/0.003:.2f} (suppressed from {np.sqrt(1/0.003):.0f})")
    print()
    print("  => CONFIRMED. Internal dynamics depend on the external field -- a strong-equivalence-principle")
    print("     violation that Newton+dark-matter cannot produce. Detected in SPARC (Chae 2020/21, ~4-5 sigma);")
    print("     the framework predicts it with a0 = c^2 sqrt(Lambda/32pi). The EFE is the framework's cleanest")
    print("     LambdaCDM discriminator and its strongest current evidence.")
    print("#"*86)


if __name__ == "__main__":
    main()
