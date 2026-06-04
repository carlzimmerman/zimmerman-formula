#!/usr/bin/env python3
"""
a0(z) reconciled with PRIMARY data: the repo's two overclaims corrected. Verified, honest, uncomfortable.
========================================================================================================
The framework's ONE distinctive prediction is a0 = cH(z)/Z -> a0 rises x3 by z=2 (= E(z)). A primary-literature
sweep (corrected attributions) shows the repo's A0Z_STATUS_CORRECTED.md OVERSTATED the case on two counts:

OVERCLAIM 1 (repo): "constant-a0 MOND is excluded."  -> FALSE on primary data.
  - McGaugh, Schombert, Lelli & Franck 2024 (ApJ 976, 13; arXiv:2406.17930): "no clear sign of evolution" in the
    BTFR / DM-fraction relations up to z~2.5 (BTFR normalization ~ a0). FAVORS constant.
  - Milgrom 2017 (arXiv:1703.06110), the ONE direct high-z rotation-curve MOND analysis: "all but exclude ~4 a0
    at z~2", explicitly excluding a0 propto (1+z)^{3/2}. FAVORS constant; bounds the rise.
  Constant a0 is the MAINSTREAM MOND position and is fully viable. NOT excluded.

OVERCLAIM 2 (repo): "Mayer (2023) confirms the framework's x3 rise."  -> WRONG (mis-cited & inverted).
  - It is Mayer, Teklu, Dolag & Remus 2022 (MNRAS 518, 257; arXiv:2206.04333), a LCDM HYDRO SIMULATION. The x3 is
    the APPARENT a0 you recover by fitting a MOND law to LCDM galaxies that do NOT obey MOND. The paper's stated
    purpose: a measured rise would "distinguish between MOND and LCDM" -- i.e. the rise FAVORS LCDM and is used to
    REJECT constant-a0 MOND. The framework's evolving a0 is DEGENERATE with LCDM's apparent rise, not confirmed.

WHAT THE STRONGEST RISE-MEASUREMENT ACTUALLY SAYS (and it does not cleanly help):
  - MUSE-DARK III: Ciocan, Bouche, Fensch et al. 2026 (A&A 709, L16; arXiv:2604.22613). 79 SFGs, 0.33<z<1.44,
    pressure-support corrected, low-acceleration sample. a0(z~1) = 2.38e-10 (~19 sigma above local 1.2e-10),
    rise significant at ~30 sigma. REAL. BUT: the authors say it runs "faster than H(z)" (~x4 by z=2 vs cH(z)'s
    x3), matches the Mayer LCDM sim, and admit a +0.45 dex stellar-mass shift would erase the offset. So it
    OVERSHOOTS the framework and is read by its own authors as plausibly LCDM, not evolving-a0-MOND.

NET (honest): the framework's a0 propto cH(z) is CONSISTENT-WITH-but-NOT-confirmed, and is in genuine TENSION
with the mainstream high-z MOND analyses (McGaugh constant; Milgrom squeeze). It is NOT killed (data are split;
MUSE measures a real rise), but it is CONTESTED and leans UNFAVORABLE -- and the two repo claims above are wrong.
Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*96)
    print("# a0(z) reconciled with primary data -- two repo overclaims corrected")
    print("#"*96 + "\n")

    print("="*96); print("THE PREDICTIONS, side by side"); print("="*96)
    print(f"  {'z':>4}{'framework E(z) [cH(z)/Z]':>26}{'(1+z)^1.5 [steeper]':>22}")
    for z in (0.5, 1.0, 1.5, 2.0):
        print(f"  {z:>4}{E(z):>26.2f}{(1+z)**1.5:>22.2f}")
    print(f"  Milgrom 2017 RC bound: ~4 a0 at z~2.  framework E(2)={E(2):.2f} (just inside, squeezed); "
          f"(1+2)^1.5={3**1.5:.2f} (EXCLUDED).\n")

    print("="*96); print("MEASUREMENTS vs the framework"); print("="*96)
    rows = [
        ("McGaugh+ 2024 (2406.17930) BTFR/f_DM", "<=2.5", "no clear evolution", "favors CONSTANT"),
        ("Milgrom 2017 (1703.06110) direct RC", "~2", "excludes ~4a0; excl (1+z)^1.5", "favors CONSTANT; squeezes x3"),
        ("MUSE-DARK III 2026 (2604.22613)", "~1", "a0=2.38e-10 (x1.98), ~19sig", "RISE, but faster than cH(z); LCDM-read"),
        ("Mayer+ 2022 (2206.04333) LCDM SIM", "0-2", "apparent a0 x3", "rise FAVORS LCDM; rejects const-MOND"),
    ]
    print(f"  {'source':<40}{'z':>6}{'result':>32}   reading")
    for s, z, r, rd in rows:
        print(f"  {s:<40}{z:>6}{r:>32}   {rd}")
    print(f"  MUSE x1.98 at z~1 vs framework E(1)={E(1):.2f}: MUSE OVERSHOOTS by {100*(1.98/E(1)-1):.0f}% (runs faster than H(z)).\n")

    print("="*96); print("VERDICT (honest, uncomfortable)"); print("="*96)
    print("""  The framework's a0 propto cH(z) (x3 by z=2) is CONSISTENT-WITH but NOT confirmed, and in genuine TENSION
  with the mainstream high-z MOND analyses. The two prior repo claims are CORRECTED:
    * "constant-a0 MOND excluded"  -> FALSE. McGaugh 2024 + Milgrom 2017 favor constant; it is the mainstream
      position and fully viable.
    * "Mayer confirms the framework" -> WRONG. Mayer is a LCDM sim; its rise favors LCDM and rejects constant
      MOND. The framework's rise is degenerate with LCDM, not evidence for the framework.
  The strongest measured rise (MUSE-DARK III) is real (~19 sigma) but OVERSHOOTS cH(z) and is read as LCDM by its
  own authors, with a +0.45 dex stellar-mass escape hatch. Milgrom 2017 squeezes the x3 hard and excludes the
  (1+z)^1.5 version. So: NOT killed (data split; a real rise exists), but CONTESTED and leaning UNFAVORABLE --
  and the framework's "one distinctive prediction" is on much shakier empirical ground than the repo claimed.""")
    print("#"*96)


if __name__ == "__main__":
    main()
