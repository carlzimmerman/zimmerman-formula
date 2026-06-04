#!/usr/bin/env python3
"""
Cosmogony doors: the framework the universe sits in, the kick-off action, and what a0 encodes. Verified numbers.
===============================================================================================================
Grounds the synthesis of three literature sweeps (origin/action, cosmic topology, origin of Lambda) in real
numbers. Honest scope flagged throughout: Lambda is INPUT here as in every current framework; nothing below
DERIVES its value -- the new content is that the SAME number (the de Sitter entropy S_dS ~ 1e122) shows up in
the cosmic horizon AND in the galactic acceleration scale a0.

(1) THE NUMBER. S_dS = pi R_dS^2 / lP^2 = (horizon area)/4lP^2 ~ 1e122 = ln(dim Hilbert space) [Banks-Fischler].
    Deriving this number is the open frontier no framework has crossed (the cosmological-constant problem).
(2) THE BRIDGE (new, verified). a0 = (sqrt(pi)/Z) * a_Planck / sqrt(S_dS): the galactic acceleration scale is the
    Planck acceleration c^2/lP suppressed by the square root of the cosmic entropy. So a0 -- measured in galaxies
    -- is a low-energy readout of S_dS (the cosmic bit-count). A UV/IR bridge made quantitative. (Restatement of
    a0=c^2/(Z R_H) via S_dS=pi R_H^2/lP^2; not a new derivation, but it reveals what a0 is.)
(3) THE KICK-OFF. Nucleation weight |Psi|^2 ~ exp(+-S_dS): no-boundary (Hartle-Hawking) favors small Lambda
    (the empty-universe problem); tunneling (Vilenkin) favors large Lambda. The sign dispute (Feldbrugge-Lehners-
    Turok vs Hartle-Hawking-Hertog) is UNRESOLVED. Neither DERIVES de Sitter -- both assume it; the framework's
    job would be to SUPPLY the Lambda they take as input.
(4) THE TESTABLE DOOR. Cosmic topology: the 20.6 Gpc torus is DEAD (matched circles), but a thin band just above
    the horizon (nearest clone < 1.2x LSS diameter) plus rotation topologies whose loops miss us SURVIVE, and are
    testable with CMB polarization (LiteBIRD, CMB-S4) and large-scale structure (Euclid, Rubin, 21cm).
Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; hbar = 1.055e-34
lP = np.sqrt(hbar*G/c**3)
H0 = 67.4e3/3.086e22
OmL = 0.685
Lam = 3*H0**2*OmL/c**2
Z = 2*np.sqrt(8*np.pi/3)


def main():
    print("#"*92)
    print("# Cosmogony doors: the framework the universe sits in, the kick-off, and what a0 encodes")
    print("#"*92 + "\n")

    print("="*92); print("(1) THE NUMBER: de Sitter entropy = ln(dim Hilbert space)"); print("="*92)
    RdS = np.sqrt(3/Lam)
    SdS = np.pi*RdS**2/lP**2
    print(f"  R_dS = sqrt(3/Lambda) = {RdS:.2e} m = {RdS/9.46e15/1e9:.1f} Gly")
    print(f"  S_dS = pi R_dS^2/lP^2 = {SdS:.2e}  (= A/4lP^2; dim H ~ e^(1e122), Banks-Fischler)")
    print("  Deriving THIS number is the open frontier no framework has crossed (the CC problem).\n")

    print("="*92); print("(2) THE BRIDGE (new, verified): a0 is a_Planck suppressed by sqrt(cosmic entropy)"); print("="*92)
    aP = c**2/lP
    a0_entropy = (np.sqrt(np.pi)/Z)*aP/np.sqrt(SdS)
    a0_direct = c**2*np.sqrt(Lam/(32*np.pi))
    print(f"  a_Planck = c^2/lP                        = {aP:.2e} m/s^2")
    print(f"  a0 = (sqrt(pi)/Z) a_Planck / sqrt(S_dS)  = {a0_entropy:.3e} m/s^2")
    print(f"  a0 = c^2 sqrt(Lambda/32pi)               = {a0_direct:.3e} m/s^2   (observed ~1.2e-10)")
    print("  => the galactic acceleration scale IS the Planck acceleration / sqrt(1e122).")
    print("     a0 measured in galaxies is a low-energy readout of S_dS (the cosmic bit-count). UV/IR bridge.\n")

    print("="*92); print("(3) THE KICK-OFF: nucleation weight ~ exp(+-S_dS); the sign dispute is unresolved"); print("="*92)
    print(f"  |Psi|^2 ~ exp(+S_dS) [no-boundary]  favors SMALL Lambda (empty-universe problem)")
    print(f"  |Psi|^2 ~ exp(-S_dS) [tunneling]    favors large Lambda")
    print(f"  S_dS = {SdS:.1e}: astronomically peaked either way. Neither DERIVES de Sitter -- both ASSUME it.")
    print("  The framework's distinctive shot: SUPPLY the Lambda that no-boundary/tunneling take as input.\n")

    print("="*92); print("(4) THE TESTABLE DOOR: cosmic topology -- narrow but live"); print("="*92)
    chi = 14.0; LSSdiam = 2*chi; RI_excl = 0.94*chi
    print(f"  chi_rec = {chi:.0f} Gpc, LSS diameter = {LSSdiam:.0f} Gpc")
    print(f"  matched circles exclude inscribed radius < {RI_excl:.1f} Gpc  => torus side < {2*RI_excl:.1f} Gpc DEAD")
    print(f"  20.6 Gpc torus: inscribed radius {20.6/2:.1f} Gpc < {RI_excl:.1f}  => EXCLUDED (matches repo)")
    print(f"  COMPACT: nearest clone < 1.2*LSSdiam = {1.2*LSSdiam:.1f} Gpc still imprints low-l correlations")
    print(f"  => SURVIVING band: torus side ~{2*RI_excl:.0f}-{1.2*LSSdiam:.0f} Gpc + rotation topologies missing us.")
    print("     Test path: CMB polarization (LiteBIRD, CMB-S4) + LSS (Euclid, Rubin, 21cm).\n")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  The framework the universe sits in (current, honest): a FINITE holographic de Sitter quantum system
  (dim H = e^S_dS / Type II_1 algebra) -- NOT a string compactification (dead), NOT necessarily a nontrivial
  spatial topology (narrow, testable). The kick-off: no current proposal DERIVES de Sitter; all assume it, so
  the framework's role is to supply Lambda. What no one can do -- and the framework cannot either -- is derive
  the NUMBER S_dS ~ 1e122. The framework's genuine content: that same number sets the galactic a0 via
  a0 = (sqrt(pi)/Z) a_Planck / sqrt(S_dS) -- a UV/IR bridge from the Planck scale to the cosmic horizon.""")
    print("#"*92)


if __name__ == "__main__":
    main()
