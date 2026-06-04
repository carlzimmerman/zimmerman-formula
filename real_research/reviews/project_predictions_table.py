#!/usr/bin/env python3
"""
The testable-predictions table: discriminating numbers + honest classification. Verified.
=========================================================================================
Carl wants a complete first-principles prediction table -- what, vs LCDM, the instrument, the timeline, the
status. This computes the discriminating NUMBERS and classifies each test honestly:
  [LCDM-IMPOSSIBLE] LCDM forbids it (shell theorem / no a0) -- a clean kill if confirmed
  [DISCRIMINATING]  framework and LCDM differ measurably
  [DEGENERATE]      real but LCDM gives the same -- matching != beating
  [INHERITED]       standard-MOND success, not unique to the framework
  [FAILURE]         LCDM wins
Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
c, Mpc = 2.998e8, 3.086e22
Z = 2*np.sqrt(8*np.pi/3)
a0 = 1.2e-10


def main():
    print("#"*94); print("# The discriminating-prediction numbers (verified)"); print("#"*94 + "\n")

    print("="*94); print("a0(z)/a0(0): the framework's distinctive evolution + the 3-way discriminator"); print("="*94)
    print(f"  {'z':>4}{'framework E(z)':>16}{'constant MOND':>15}{'SIV (Maeder)':>14}")
    siv = {1: 0.70, 2: 0.52, 3: 0.42}                 # Maeder SIV: a0 DECREASES (from STATE doc)
    for z in (1, 2, 3):
        print(f"  {z:>4}{E(z):>16.2f}{1.0:>15.2f}{siv[z]:>14.2f}")
    print(f"  => at z=3 the three are ~10x apart (4.57 / 1.0 / 0.42): a CLEAN discriminator IF a0(z) is measured")
    print(f"     halo-free. STATUS: contested, leaning UNFAVORABLE (MUSE rises FASTER than E(z) & needs a halo).\n")

    print("="*94); print("EFE-vs-z: the LCDM-FORBIDDEN test"); print("="*94)
    print(f"  external-field strength eta(z) = g_ext/a0(z) prop 1/E(z): high-z galaxies are MORE isolated-MOND.")
    print(f"  {'z':>4}{'eta(z)/eta(0) = 1/E(z)':>24}")
    for z in (0, 1, 2):
        print(f"  {z:>4}{1/E(z):>24.2f}")
    print(f"  => the external field effect WEAKENS x3 by z=2. LCDM has NO EFE (shell theorem) -> LCDM-IMPOSSIBLE.\n")

    print("="*94); print("a0-cosmography: H0 and q0 read off galaxy dynamics"); print("="*94)
    H0_pred = Z*a0/c*Mpc/1e3
    print(f"  H0 = Z a0/c = {H0_pred:.1f} km/s/Mpc (in the tension band) -- but DEGENERATE/H0-hostage (Door A/B).")
    print(f"  q0 from a0's slope = -0.527 = LCDM value -> DEGENERATE (matching != beating).\n")

    print("="*94); print("THE CLASSIFICATION (what could actually break LCDM)"); print("="*94)
    rows = [
        ("Galaxy RAR / 1-param rotation curves", "INHERITED", "real (McGaugh); LCDM fine-tunes; foundation contested"),
        ("BTFR, Faber-Jackson, Freeman Sigma", "INHERITED", "tight, MOND-predicted; standard MOND"),
        ("Crater II / dwarf sigma (EFE)", "INHERITED", "MOND win: 2 km/s vs LCDM 4, obs 2.7"),
        ("External field effect (z=0)", "LCDM-IMPOSSIBLE", "Chae 4-5sigma -- the STRONGEST distinctive, CONTESTED"),
        ("Wide binaries (Gaia)", "LCDM-IMPOSSIBLE", "the FOUNDATION; SPLIT (Banik 16-19sig vs Chae); DR4 decides"),
        ("EFE-vs-z (eta prop 1/E(z))", "LCDM-IMPOSSIBLE", "framework-distinctive; FORECAST, needs high-z RCs"),
        ("a0(z) = cH(z)/Z evolution", "DISCRIMINATING", "the one original idea; leaning UNFAVORABLE (MUSE/McGaugh)"),
        ("a0-H0 link (H0=71.5)", "DEGENERATE", "H0-hostage; not a win"),
        ("JWST early massive galaxies", "DISCRIMINATING", "a-priori DIRECTIONAL (Sanders 1998); NOT decisive, LCDM absorbs"),
        ("Galaxy clusters (~2x residual)", "FAILURE", "MOND under-predicts; LCDM wins"),
        ("CMB acoustic peaks / BAO / LSS", "FAILURE", "LCDM fits; AeST still under test"),
    ]
    print(f"  {'prediction':<40}{'class':>17}   status")
    for p, cl, st in rows:
        print(f"  {p:<40}{cl:>17}   {st}")
    print(f"""
  => The path to "LCDM is broken" runs through the LCDM-IMPOSSIBLE tests -- the EFE (Chae 4-5sigma, contested)
     and wide binaries (split). Those are the only places a clean kill can happen. The framework's OWN
     distinctive test (a0 evolution) is leaning unfavorable. Galaxy RAR is real but accommodatable. No test
     currently delivers a decisive kill; the near-term deciders are Gaia DR4 (wide binaries) and halo-free
     high-z dynamics (a0(z), EFE-vs-z).""")
    print("#"*94)


if __name__ == "__main__":
    main()
