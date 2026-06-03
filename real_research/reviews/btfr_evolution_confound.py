#!/usr/bin/env python3
"""
Is the high-z BTFR an independent test of a0(z)? Honest answer: NO -- it is gas-confounded.
==========================================================================================
Carl asked for calculations that would support the posit a0(z)=a0(0)E(z). The obvious independent test
is the high-z Tully-Fisher zero-point (hundreds of existing galaxies). This script computes the
framework's BTFR prediction and shows -- against the real data (Ubler+2017 KMOS3D, arXiv:1703.04321) --
that the test is CONFOUNDED by gas-fraction evolution and is NOT clean. A genuinely sobering result,
reported straight: there is no clean EXISTING-data calculation that confirms a0 prop E(z). Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("="*88)
    print("BTFR zero-point as a test of a0(z): the framework prediction, and why it is CONFOUNDED")
    print("="*88)
    print("""  FRAMEWORK (pure MOND, a0 increasing): BTFR is M_bar = v_flat^4/(G a0). At fixed v_flat the
  baryonic-TFR zero-point should DROP with z, M_bar(fixed v) prop 1/a0 prop 1/E(z):""")
    print(f"     M_bar(fixed v) at z=2.3 vs z=0.9 should be E(0.9)/E(2.3) = {E(0.9)/E(2.3):.2f}  (a ~2.3x DROP).")
    print("""
  DATA (Ubler+2017 KMOS3D): the OPPOSITE -- at fixed circular velocity, baryonic mass is HIGHER at
  z~2.3 than z~0.9 (positive baryonic-TFR zero-point evolution; the STELLAR TFR barely moves).

  WHY THE DATA RISE (and why it is not a0): M_bar = M_star + M_gas, and gas fractions climb steeply
  with z. The stellar TFR is ~flat while the baryonic one rises => the rise is a GAS-FRACTION effect,
  not a change in a0. Reading it as a0 would falsely imply a0 DECREASES -- an artifact of the confound.

  ALSO confounding the high-z TFR: pressure support (V/sigma ~ few; the asymmetric-drift correction),
  the baryon-to-dark fraction within the disk, and selection toward bright compact systems.

  => VERDICT: the high-z BTFR zero-point is dominated by gas/pressure/selection evolution, NOT a0. It is
     NOT a clean independent probe of a0(z); the framework's a0-only prediction is swamped. The largest
     existing high-z kinematic dataset therefore can neither confirm nor refute a0 prop E(z).
""")
    print("="*88)
    print("HONEST CONSEQUENCE FOR 'calculations that show the posit is correct'")
    print("="*88)
    print("""  * A posit cannot be PROVEN by calculation -- only its falsifiable PREDICTION (a0 prop E(z)) tested.
  * That prediction is currently supported only by:
      (i)  the de Sitter-Unruh DERIVATION -- a0~cH and a0(z)=a0(0)E(z) fall out of horizon thermodynamics
           coefficient-free (desitter_unruh_mond.py): the posit is not arbitrary, but a derivation is not
           a confirmation;
      (ii) the 3 DIRECT a0(z) points, which rise and favour the framework over SIV/constant (chi^2 3 vs
           64 vs 28) -- but at ~2 sigma, single-point-driven, and systematics-limited.
  * The obvious extra existing-data test (BTFR evolution) is GAS-CONFOUNDED and not clean (this script).
  * THEREFORE: there is no clean existing-data calculation that confirms a0 prop E(z). The decisive
    evidence requires a DIRECT a0 from the deep-MOND tail with a per-galaxy gas census at z~3 -- which
    controls exactly the gas confound that wrecks the TFR. That is the proposal, and it is the honest
    bottom line: the posit stands as a derived, data-favoured-but-unconfirmed, decisively-testable claim.""")
    print("="*88)


if __name__ == "__main__":
    main()
