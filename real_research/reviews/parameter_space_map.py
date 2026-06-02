#!/usr/bin/env python3
"""
COMPLETE parameter-space map of the evolving-a0 framework.
==========================================================

Carl asked for a complete, honest review of the parameter space. This maps both axes:
  THEORETICAL  -- the coefficient Z and the exponent p (what is free, what is derived).
  OBSERVATIONAL -- where (if anywhere) evolving-a0 is DISTINGUISHABLE from LCDM, grounded
                   in the literature (Magneticum 2022; NIHAO; Rodrigues+2018; MUSE-DARK 2026).

Nothing here is asserted as a framework 'win'. Run: python <thisfile>   (needs numpy)
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)


# ===========================================================================
def theoretical_coefficient():
    print("=" * 82)
    print("THEORY 1 -- the coefficient: a0 = k*c*sqrt(G rho_c) = cH/Z,  Z = sqrt(8pi/3)/k")
    print("=" * 82)
    base = np.sqrt(8 * np.pi / 3)   # = 2.8945, the Friedmann factor (REAL)
    print(f"   sqrt(8pi/3) = {base:.4f}  (exact Friedmann; this part is NOT free)")
    print(f"   {'reading':28}{'k':>7}{'Z=sqrt(8pi/3)/k':>18}{'status':>26}")
    rows = [
        ("Schwarzschild (literal)", base / 2.0, 2.0, "wrong: a0 ~2.9x too big"),
        ("Milgrom a0~cH0/2pi",      base / (2*np.pi), 2*np.pi, "posited (1983)"),
        ("Verlinde a0~cH0/6",       base / 6.0, 6.0, "posited (2017)"),
        ("framework 2*sqrt(8pi/3)", 0.5, 2*base, "posited (k=1/2)"),
        ("data-preferred (~5.8)",   base / 5.8, 5.8, "FIT to SPARC a0,H0"),
        ("29/5 = 5.800",            base / 5.8, 5.8, "fits data BETTER, ~0 bits"),
    ]
    for name, k, Z, st in rows:
        print(f"   {name:28}{k:>7.3f}{Z:>18.3f}{st:>26}")
    print("   VERDICT: sqrt(8pi/3) is real; k (=> Z) is a free O(1) number in ~[0.46,0.50].")
    print("   No principle derives it (Bridge 2, horizon-entropy, Schwarzschild all fail).")
    print("   The framework's k=1/2 is one posit among several, and not the data's best. [FREE]\n")


def theoretical_exponent():
    print("=" * 82)
    print("THEORY 2 -- the exponent p in a0(z)=a0(0)E(z)^p (which density a0 tracks)")
    print("=" * 82)
    print(f"   {'p':>5}  {'meaning':30}{'a0(z6)/a0(0)':>14}{'vs p=0.80+/-0.17':>18}")
    for p, mean in [(0.0,"sqrt(Lambda): de Sitter,const"),(1.0,"sqrt(rho_tot)~H: premise"),
                    (1.5,"sqrt(rho_matter): free-fall")]:
        nsig = abs(p - 0.80) / 0.17
        print(f"   {p:>5.1f}  {mean:30}{E(6)**p:>14.1f}{nsig:>15.1f}sg")
    print("   data WEAKLY (~2sigma, single-point) prefer p~1; constant & matter ~2sigma off")
    print("   after the inter-method systematic. The exponent is a fitted choice, not derived. [FIT]\n")


# ===========================================================================
def observational_distinguishability():
    print("=" * 82)
    print("OBSERVATION -- is evolving-a0 DISTINGUISHABLE from LCDM? (the deciding axis)")
    print("=" * 82)
    rows = [
        ("RAR amplitude / apparent a0(z)", "rises as E(z)", "rises (halo+baryon evol)",
         "both ~x3 to z=2.3", "NO -- degenerate (Magneticum,NIHAO)"),
        ("RAR intrinsic SCATTER",          "~0 (a0 universal)", "grows with z",
         "grows 0.13->0.19 dex", "YES -> currently FAVORS LCDM"),
        ("a0 universality at fixed z",      "universal", "galaxy-dependent",
         "CONTESTED (Rodrigues18", "YES -> against/contested"),
        ("EFE (host dependence)",           "yes*", "none",
         "seen locally (MOND)", "YES -- but *framework EFE withdrawn"),
        ("z>4 multi-channel coherence",     "one E(z)", "uncertain",
         "NO DATA YET", "the ONLY open window"),
        ("compact high-z galaxies",         "Newtonian (boost~0)", "dark matter",
         "de Graaff M_dyn/M*~40", "predictions don't apply (regime)"),
    ]
    print(f"   {'observable':32}{'framework':18}{'LCDM':24}")
    print("   " + "-" * 78)
    for obs, fw, lcdm, data, dist in rows:
        print(f"   {obs:32}{fw:18}{lcdm:24}")
        print(f"   {'':32}data: {data:22} -> {dist}")
    print()
    print("   READ: the ONE observable that exists (amplitude) is degenerate; the observables")
    print("   that DO discriminate (scatter, universality) currently lean LCDM or are contested;")
    print("   the framework's own discriminator (EFE) was withdrawn as a category error; and the")
    print("   only clean untested window is z>4, where no kinematic a0 data exist.\n")


def regime_window():
    print("=" * 82)
    print("OBSERVATION 2 -- the regime window: where do the a0(z) boosts even apply?")
    print("=" * 82)
    Z = 2 * np.sqrt(8 * np.pi / 3); H0 = 67.4e3 / Mpc
    a0z = lambda z: (c * H0 / Z) * E(z)
    Msun, kpc = 1.989e30, 3.0857e19
    print("   deep-MOND (boosts apply) needs g_bar < a0(z). g/a0 at z=6:")
    print(f"     {'M*':>9}{'R[kpc]':>8}{'g/a0(z6)':>10}{'regime':>13}")
    for M, R in [(1e9,2.0),(1e9,1.0),(1e10,1.0),(1e10,0.5)]:
        g = G * (M*Msun) / (R*kpc)**2
        r = g / a0z(6)
        reg = "deep-MOND" if r<0.3 else ("Newtonian" if r>3 else "transition")
        print(f"     {M:>9.0e}{R:>8.1f}{r:>10.2f}{reg:>13}")
    print("   only EXTENDED, low-mass high-z galaxies are deep-MOND; the compact/massive ones")
    print("   (the headline JWST targets) are Newtonian, where a0(z) barely matters. [WINDOW NARROW]\n")


def verdict():
    print("=" * 82)
    print("COMPLETE-PARAMETER-SPACE VERDICT")
    print("=" * 82)
    print("  THEORY axis: sqrt(8pi/3) real; the coefficient k(Z) and exponent p are FITTED,")
    print("               not derived. Two free O(1) choices, neither unique.")
    print("  OBSERVATION axis: degenerate with LCDM on the only existing observable; the")
    print("               discriminating observables (scatter, a0-universality) currently lean")
    print("               LCDM/contested; EFE withdrawn; z>4 is the sole untested window and")
    print("               applies only to EXTENDED galaxies.")
    print("  => The viable region of parameter space where the framework is BOTH distinct from")
    print("     LCDM AND not already disfavoured is: z>4, extended deep-MOND galaxies, the")
    print("     cross-channel COHERENCE (and tightness) of the RAR. Everything else is")
    print("     degenerate, fitted, or leaning the other way. That single region is the whole")
    print("     testable content -- and it has no data yet.")
    print("=" * 82)


def main():
    theoretical_coefficient(); theoretical_exponent()
    observational_distinguishability(); regime_window(); verdict()


if __name__ == "__main__":
    main()
