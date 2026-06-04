#!/usr/bin/env python3
"""
What works on the derivation front: ground a0 ~ sqrt(rho_DE) on Verlinde's Lambda-entropy -- N-V-free.
=====================================================================================================
The breakthrough "failed" only in the sense that it bottomed out at the unsettled Narovlansky-Verlinde
proposal (de Sitter = the DSSYK center). The question: is there a derivation path for the data-testable claim
that does NOT depend on N-V? Yes -- and it is cleaner.

THE PATH. Verlinde (2017) derives MOND from the de Sitter VOLUME-LAW entanglement entropy -- the entropy that
exists *because* Lambda>0. Read correctly, that entropy IS the dark-energy entropy: its density is fixed by the
de Sitter (Lambda) horizon L_dS = c/H_L, NOT by the instantaneous Hubble volume c/H(z). So the MOND scale it
sources tracks the EVENT horizon ~ c sqrt(Lambda/3) ~ sqrt(rho_DE) -- constant/declining, the data-favored
branch -- NOT a0 ~ cH(z) rising. (Verlinde's own "a0 = cH0" plugged in the instantaneous H0; the MECHANISM,
sourced by the Lambda-entropy, gives cH_L = cH0 sqrt(OmegaLambda).)

This matters because it makes the FALSIFIABLE PREDICTION robust:
  a0(z) ~ sqrt(rho_DE(z))  is now DOUBLY-derived, two independent frameworks that AGREE:
    (1) Verlinde thermodynamics: volume-law entropy = the Lambda-entropy => a0 ~ sqrt(Lambda).   [NO N-V]
    (2) DSSYK microscopics: the dual is the de Sitter static patch = the event horizon => a0 ~ sqrt(Lambda). [N-V]
  N-V is then needed ONLY for the clean microscopic sign and the exact prefactor -- NOT for the data-testable
  claim a0(z) ~ sqrt(rho_DE(z)). The prediction stands on Verlinde alone.

WHAT IS LEFT (the genuine, N-V-FREE derivation problem): the NORMALIZATION. The event-horizon a0(0) = c H_L/Z
~ 0.93e-10 is ~22% below the observed 1.2e-10, while the apparent-horizon c H0/Z ~ 1.12e-10 is ~7% low. No
single horizon gives BOTH the right value (wants rho_total, ~1.12) AND the declining evolution (wants rho_DE).
The gap is exactly sqrt(OmegaLambda) = 0.83 -- the matter fraction of today's total density. So the target is:
a density/scale that is rho_total-like at z=0 but rho_DE-like in evolution. The two-horizon geometric mean
a0 ~ c sqrt(H H_L) is the leading candidate (a0(0)~1.02e-10, mild rise) -- imperfect, but a clean, named,
N-V-free problem to crack.

HONEST CAVEATS: Verlinde's volume-law entropy is ITSELF contested (Hossenfelder; the dwarf-spheroidal and
cluster failures), so path (1) trades the N-V assumption for Verlinde's -- but the two are DIFFERENT
assumptions, so their agreement on a0 ~ sqrt(Lambda) is a real cross-check, not circular. And the "Lambda-
entropy not instantaneous-H-entropy" re-reading is an interpretation of Verlinde, defensible but mine. Needs
numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; hbar = 1.055e-34
H0 = 67e3/3.086e22; OL = 0.685; HL = H0*np.sqrt(OL)
Z = 2*np.sqrt(8*np.pi/3)


def main():
    print("#"*92)
    print("# Derivation front: a0 ~ sqrt(rho_DE) from Verlinde's Lambda-entropy (N-V-free); the residual is norm.")
    print("#"*92 + "\n")

    print("="*92); print("THE PATH -- the volume-law entropy is the dark-energy (Lambda) entropy => a0 ~ sqrt(Lambda)"); print("="*92)
    L_dS = c/HL
    print(f"  Verlinde's MOND source = the de Sitter VOLUME-LAW entropy, present because Lambda>0 (the DE entropy).")
    print(f"  Its density is set by L_dS = c/H_L = {L_dS:.2e} m (the Lambda horizon), not the instantaneous c/H(z).")
    print(f"  => emergent scale ~ c^2/L_dS ~ c H_L ~ c sqrt(Lambda/3) ~ sqrt(rho_DE).")
    print(f"     a0 ~ c H_L/Z = {c*HL/Z/1e-10:.2f}e-10 (EVENT horizon, declining) -- the data-favored branch.")
    print(f"     Verlinde wrote a0 = cH0 = {c*H0/1e-10:.2f}e-10*; the mechanism gives cH_L = {c*HL/1e-10:.2f}e-10 (factor sqrt(OmegaL)).\n")

    print("="*92); print("WHY IT WORKS -- the falsifiable prediction is now DOUBLY-derived, N-V-free"); print("="*92)
    print("""  a0(z) ~ sqrt(rho_DE(z)) follows from TWO independent frameworks that agree:
    (1) Verlinde thermodynamics (volume-law = Lambda-entropy)        -> a0 ~ sqrt(Lambda)   [NO N-V]
    (2) DSSYK microscopics (dual = de Sitter static patch/event hzn) -> a0 ~ sqrt(Lambda)   [needs N-V]
  So the DATA-TESTABLE claim no longer rests on N-V; N-V is only for the clean microscopic sign + exact prefactor.
  Two different contested assumptions (Verlinde's volume law; N-V's center) AGREEING on a0 ~ sqrt(Lambda) is a
  genuine cross-check, not circular.\n""")

    print("="*92); print("THE RESIDUAL -- the real, N-V-FREE derivation problem: the normalization"); print("="*92)
    print(f"  event   a0(0) = c H_L/Z = {c*HL/Z/1e-10:.2f}e-10  (~22% low)   [right EVOLUTION, declining]")
    print(f"  apparent a0(0) = c H0/Z  = {c*H0/Z/1e-10:.2f}e-10  (~7% low)    [right VALUE, wrong evolution, rising]")
    print(f"  geom mean a0(0) = c sqrt(H0 H_L)/Z = {c*np.sqrt(H0*HL)/Z/1e-10:.2f}e-10  [splits it; mild rise]")
    print(f"  observed: 1.2 +- 0.26 e-10. The event/apparent gap is exactly sqrt(OmegaLambda) = {np.sqrt(OL):.3f}.")
    print("""  TARGET: a density/scale that is rho_total-like at z=0 (value ~1.12) but rho_DE-like in evolution
  (declining). No single horizon does both; the two-horizon geometric mean is the leading candidate. THIS is the
  derivation problem to crack -- and it is clean, named, and has NOTHING to do with N-V.\n""")

    print("="*92); print("VERDICT -- what could work"); print("="*92)
    print("""  Yes, there is a derivation path that works for the part that matters (the falsifiable prediction). Ground
  a0 ~ sqrt(rho_DE) on Verlinde's de Sitter VOLUME-LAW entropy -- correctly read as the dark-energy (Lambda)
  entropy, fixed by the event horizon, NOT the instantaneous Hubble volume. Then a0 ~ sqrt(Lambda) and the
  a0(z) ~ sqrt(rho_DE(z)) prediction is N-V-FREE, and independently cross-checked by the DSSYK event-horizon
  dual. N-V is demoted to "the clean microscopic story for the sign + the exact prefactor" -- nice to have, not
  load-bearing for the data test. The one genuinely open derivation problem that remains is the NORMALIZATION
  (the ~22% / the apparent-vs-event sqrt(OmegaLambda) gap), a concrete two-horizon question with no N-V in it.
  So the derivation front is not dead -- it moved from "stuck on an unsettled QG proposal" to "the testable
  prediction is doubly-derived; crack the normalization." That is a much better place to push.""")
    print("="*92)


if __name__ == "__main__":
    main()
