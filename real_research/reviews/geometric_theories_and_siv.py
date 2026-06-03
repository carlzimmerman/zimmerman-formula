#!/usr/bin/env python3
"""
Geometric theories that tie to a0=cH/Z -- the class the established-paths ledger under-covered.
==============================================================================================
Carl asked: "is there no other literature of geometric theories we can tie to this?" Fair catch --
the engine ledger covered the emergent-gravity/thermodynamic routes and the relativistic-MOND field
theories (AeST, TeVeS), but NOT the explicitly geometric modified-gravity class. The standout, verified
this session, is Maeder's SCALE-INVARIANT VACUUM (SIV) -- and it produces a clean, decisive result:
SIV predicts a0 EVOLVES too, but in the OPPOSITE DIRECTION, so the z~3 test discriminates the framework
from SIV with a ~10x lever arm. Literature verified June 2026 (arXiv:2409.11425, MNRAS-L 535, L13, 2024;
'MOND as a peculiar case of SIV', MNRAS 520, 1447, 2023). Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685


def E(z):                                  # FRAMEWORK: a0(z)/a0(0) = E(z)  (a0 prop H(z) prop sqrt(rho_crit))
    return np.sqrt(Om*(1+z)**3 + OL)


def siv(z):                                # MAEDER SIV Eq.16: a0 DECREASES with z
    return (1+z)**-1.5 * ((1-Om)/(1+z)**1.5 + Om)**(-4/3.)


def main():
    print("="*88)
    print("GEOMETRIC THEORIES THAT TIE TO a0=cH/Z (the class the engine ledger under-covered)")
    print("="*88)
    print("""  [1] Maeder SCALE-INVARIANT VACUUM (SIV) -- THE CLOSEST COUSIN.
      A geometric theory: macroscopic empty space is scale-invariant (Dirac 1973; Bouvier-Maeder 1979;
      Maeder 2017+). 'MOND as a peculiar case of SIV' (MNRAS 2023): SIV CONTAINS MOND, and DERIVES a0
      from cosmology -- a0_0 = c(1-Om^{1/3})(1-Om)/(2 tau0), with 2*pi*a0 ~ cH0 ~ c^2 sqrt(Lambda/3).
      This is the SAME a0~cH~c^2 sqrt(Lambda) family as the framework, from a GEOMETRIC principle, not a
      posit. AND SIV predicts a0 EVOLVES (arXiv:2409.11425) -- so the framework's headline claim is NOT
      unique to it. Status: serious, published (MNRAS/A&A), but a MINORITY paradigm (scale-invariance of
      the vacuum is a strong, non-mainstream gauge choice). The framework's a0=(c/2)sqrt(G rho)=cH/Z is
      the same relation from a DIFFERENT (surface-gravity/density) reading.

  [2] Conformal / Weyl gravity (Mannheim-Kazanas). Geometric (Weyl-conformal-invariant, 4th order):
      weak-field V=-GM/r + gamma c^2 r/2, a linear potential that flattens rotation curves with no DM,
      with a cosmological gamma0. MOND-adjacent and cosmologically-scaled, but NOT a0=cH/Z and does not
      predict the E(z) evolution; known cluster/lensing tensions and 4th-order ghost concerns.

  [3] MOG / Scalar-Tensor-Vector Gravity (Moffat). Geometric extra scalar(G) + vector fields; fits
      rotation curves, clusters, the Bullet -- but with a FITTED acceleration scale (the vector mass and
      coupling), NOT tied to cH. A successful DM-alternative, but its scale is not the framework's.

  => Of the geometric class, ONLY SIV ties a0 to cH/sqrt(Lambda) AND predicts evolution. It is the true
     cousin. The framework is NOT alone. But -- crucially -- it is DISTINCT from SIV:\n""")

    print("  THE DISCRIMINATOR: a0(z)/a0(0) -- framework (INCREASES) vs SIV (DECREASES) vs constant")
    print(f"  {'z':>4}{'framework E(z)':>16}{'Maeder SIV':>12}{'constant':>10}{'framework/SIV':>15}")
    for z in (0, 0.5, 1, 2, 3, 4, 6):
        print(f"  {z:>4}{E(z):>16.2f}{siv(z):>12.2f}{1.0:>10.1f}{E(z)/siv(z):>15.1f}")
    print(f"""
  => at z=3: a0(3)/a0(0) = {E(3):.2f} (framework) vs {siv(3):.2f} (SIV) vs 1.0 (constant). The framework and
     SIV predict OPPOSITE DIRECTIONS and differ by ~{E(3)/siv(3):.0f}x at z=3. A single clean a0(z=3) point
     discriminates ALL THREE at once -- a far sharper test than the evolving-vs-constant framing.\n""")

    print("="*88)
    print("WHAT THIS MEANS (honest, both ways)")
    print("="*88)
    print(f"""  GAIN: the framework's distinctive claim sharpens from the vague 'a0 evolves' (shared with SIV,
  Milgrom 2014, and the a0~cH school) to the SPECIFIC, bold 'a0 INCREASES as E(z)' -- which is the
  OPPOSITE of the leading geometric competitor (SIV). The z~3 measurement is upgraded from a 2-way test
  (evolving vs constant) to a 3-way discriminator (framework {E(3):.1f} vs SIV {siv(3):.2f} vs constant 1.0).
  And the framework now has a named geometric ALLY/predecessor in spirit (a0 from cosmic scale) and a
  named geometric RIVAL in detail (opposite z-trend) -- it is situated in the real literature.

  RISK: the current a0(z) data read as ~FLAT (the SIV analysis of existing data; and our own single-
  point-driven ~2 sigma hint). Flat/decreasing favours SIV/constant and is AGAINST the framework's
  strong increase. So the framework makes the BOLDEST and most falsifiable of the three predictions:
  a0 must SHOOT UP at high z (x4.6 by z=3). If a clean z~3 a0 comes back flat or low, the framework is
  killed and SIV/constant survive. That is exactly the high-stakes, decisive test the proposal wants --
  now with a concrete geometric rival to beat, not just a null.

  HONEST CORRECTION to the prior ledger: 'every established path' was incomplete -- it omitted the
  geometric modified-gravity class. Added here. The omission did not change the verdict (no route
  DERIVES the framework's coefficient or its increasing-E(z) trend), but SIV is a genuine, close,
  geometric tie that the framework should cite, contrast against, and aim to beat at z~3.""")
    print("="*88)


if __name__ == "__main__":
    main()
