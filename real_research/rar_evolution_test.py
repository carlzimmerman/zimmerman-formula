#!/usr/bin/env python3
"""
The cascade's central prediction, tested on REAL measured a0(z).
================================================================

The premise forces a0(z) = a0(0) E(z) (constant-a0 MOND is excluded). For the first
time there are DIRECT measurements of the RAR acceleration scale a0 vs redshift. This
fits the three hypotheses to the real data points and reports which survives.

REAL DATA (measured a0 in 1e-10 m/s^2, with source):
  z~0.00  1.20 +/- 0.26   SPARC local RAR (McGaugh, Lelli & Schombert 2016)
  z~0.05  1.69 +/- 0.13   Varasteanu et al. 2025 (z<0.08 galaxies)
  z~0.90  2.38 +/- 0.11   MUSE-DARK III (A&A 2026): 79 SF galaxies, MUSE IFU, 0.33<z<1.44
  [within MUSE-DARK the binned a0 rises 1.99 -> 2.71 across the sample -- a0 evolves.]

Hypotheses (a0(0) free normalization, fit to the points):
  CONSTANT:  a0(z) = A                     (standard MOND -- the null)
  E(z):      a0(z) = A * E(z)              (a0 ~ H(z), total density -- THIS cascade)
  (1+z)^1.5: a0(z) = A * (1+z)^1.5         (a0 ~ matter free-fall -- the steeper fork)

Run:  python real_research/rar_evolution_test.py    (needs numpy, scipy)
"""

import numpy as np
from scipy.optimize import minimize_scalar

OM, OL = 0.315, 0.685

# real measured points
Z = np.array([0.00, 0.05, 0.90])
A0 = np.array([1.20, 1.69, 2.38])      # 1e-10 m/s^2
ERR = np.array([0.26, 0.13, 0.11])
SRC = ["SPARC (McGaugh+16)", "Varasteanu+25", "MUSE-DARK III (2026)"]


def E(z):
    return np.sqrt(OM * (1 + z) ** 3 + OL)


MODELS = {
    "CONSTANT  (standard MOND)": lambda z: np.ones_like(z),
    "E(z)      (a0~H(z), this cascade)": lambda z: E(z),
    "(1+z)^1.5 (a0~matter free-fall)": lambda z: (1 + z) ** 1.5,
}


def chi2(A, f):
    return np.sum(((A0 - A * f(Z)) / ERR) ** 2)


def main():
    print("=" * 74)
    print("REAL measured a0(z) -- the data being fit")
    print("=" * 74)
    for z, a, e, s in zip(Z, A0, ERR, SRC):
        print(f"   z={z:<5.2f}  a0 = {a:.2f} +/- {e:.2f} e-10   [{s}]")
    print()
    print("=" * 74)
    print("Fit each hypothesis (a0(0)=A free), report chi^2 (2 dof)")
    print("=" * 74)
    results = {}
    for name, f in MODELS.items():
        res = minimize_scalar(lambda A: chi2(A, f), bounds=(0.1, 5), method="bounded")
        A, c2 = res.x, res.fun
        results[name] = c2
        pred = A * f(Z)
        print(f"\n   {name}")
        print(f"     best a0(0) = {A:.2f} e-10,  chi^2 = {c2:.1f} (2 dof)")
        print(f"     {'z':>6}{'a0_obs':>9}{'a0_pred':>9}{'pull':>7}")
        for i in range(len(Z)):
            print(f"     {Z[i]:>6.2f}{A0[i]:>9.2f}{pred[i]:>9.2f}{(A0[i]-pred[i])/ERR[i]:>7.1f}")
    print()
    print("=" * 74)
    print("VERDICT")
    print("=" * 74)
    cbest = min(results, key=results.get)
    print(f"   chi^2:  " + "   ".join(f"{k.split()[0]}={v:.0f}" for k, v in results.items()))
    print(f"   * CONSTANT a0 is strongly REJECTED (chi^2={results[list(results)[0]]:.0f}): the RAR")
    print("     scale a0 robustly EVOLVES -- the central cascade prediction is confirmed,")
    print("     and standard constant-a0 MOND is disfavoured by real 2026 data.")
    print(f"   * Best fit: {cbest.split()[0]}. E(z) and (1+z)^1.5 both fit far better than")
    print("     constant; which of the two depends on the LOCAL ANCHOR, which is itself")
    print("     uncertain (1.20 SPARC vs 1.69 Varasteanu -- a ~40% spread at z~0).")
    print()
    print("   HONEST CAVEATS:")
    print("    - small samples (SPARC local; 79 MUSE-DARK galaxies); a0(0) spans 1.0-1.7.")
    print("    - MUSE-DARK fit a LINEAR a0=1.0+1.59z (phenomenological) and note their rate")
    print("      is 'faster than H(z)' using their low intercept 1.0; anchored at SPARC 1.2,")
    print("      E(z) fits the z~1 point to ~15%. So 'E(z) vs steeper' is anchor-limited.")
    print("    - NOT MOND-vs-LCDM evidence: the authors note an evolving RAR is ALSO")
    print("      expected in LCDM from halo-profile evolution. The cascade PREDICTED a0(z),")
    print("      and the data CONFIRMS evolution -- but the same data fits LCDM too.")
    print()
    print("   NET: the one forced, central prediction of the premise -- that a0 evolves --")
    print("   is borne out by the first real a0(z) measurements (a0 ~doubles by z~1, rising")
    print("   within the MUSE-DARK sample), at a rate consistent with a0~H(z) given the")
    print("   anchor. Constant-a0 MOND is the casualty. The decisive refinement is a tighter")
    print("   local a0 + the deep-MOND z>2 RAR knee (Z2_cascade_part2.py, Step 8).")


if __name__ == "__main__":
    main()
