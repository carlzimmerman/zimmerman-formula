#!/usr/bin/env python3
"""
PROJECT 4b: scoping the DSSYK calculation that would close the deep-MOND sign (the merged #1<->#4 target).
=========================================================================================================
Projects 1b/1c reduced the deep-MOND sign to two concrete quantities in the (1+1)D near-horizon theory: the
probe's coupling to the flat-DOS sector, and the exact cutoff that pins Z. That near-horizon theory is the
proposed dual of DOUBLE-SCALED SYK (DSSYK = the 2D de Sitter static-patch dual: Narovlansky-Verlinde 2023;
Rahman 2022; Susskind). This file does HONEST SCOPING -- it defines exactly what the calculation is, computes
one rigorous INDICATOR (the DSSYK density of states near the de Sitter point), and states the difficulty and
risk plainly. It does NOT fake the derivation; faking it would be the hand-waving this repo rules out. numpy.
"""
import numpy as np


def the_dictionary():
    print("="*92); print("THE DSSYK <-> de Sitter DICTIONARY (what plays what)"); print("="*92)
    print("""  DSSYK is the double-scaled limit of SYK (N Majoranas, random q-body coupling; N->inf, q->inf,
  lambda=2q^2/N fixed). It is solvable by CHORD diagrams, and is conjectured dual to the de Sitter STATIC
  PATCH. The dictionary relevant to Project 1:
     * chord number n            <->  bulk geodesic length / radial position in the static patch
     * DSSYK Hamiltonian         <->  static-patch (bulk) Hamiltonian
     * energy E (spectrum below) <->  bulk energy; the CENTER E=0 (max DOS) = the maximal-entropy / HORIZON state
     * a matter operator = a 'matter chord' insertion  <->  the PROBE MASS
  So Project 1's 'horizon DOF' ARE the DSSYK chord states, and the 'probe mass' is a matter-chord insertion.
  The deep-MOND freezing becomes: how many chord states does the matter chord excite at temperature T?\n""")


def the_calculation():
    print("="*92); print("THE CALCULATION (precisely what must be computed)"); print("="*92)
    print("""  1. Take the DSSYK chord Hilbert space and its Hamiltonian (known: the q-deformed transfer matrix on
     chord-number states).
  2. Insert a matter chord of weight Delta (the probe) and compute its two-point function / the energy it
     deposits across the chord spectrum (the Berkooz-Isachenko-Narovlansky-Torrents 2018 / Lin 2022 formalism
     gives DSSYK correlators in closed q-form).
  3. Extract N_eff(T) = the effective number of chord states sharing the probe's energy at temperature T
     (the equipartition count). MOND requires N_eff(T) ~ T (LINEAR) below the de Sitter temperature T_dS,
     saturating above -> a = sqrt(a0 g_N), a0 ~ cH.
  4. Read off the coefficient (the analog of Z) from the exact cutoff. Pins a0 = cH/Z.
  Items 2-3 are the substance; item 1 is standard, item 4 follows once 3 is done.\n""")


def dos_indicator():
    print("="*92); print("ONE RIGOROUS INDICATOR -- is the DSSYK DOS flat at the de Sitter point? (computed)"); print("="*92)
    def qH_dos(q, n=6000, K=4000):
        th = np.linspace(1e-4, np.pi-1e-4, n); lw = np.zeros_like(th)
        for k in range(K):
            qk = q**k
            if qk < 1e-15: break
            lw += np.log(np.maximum(1 - 2*qk*np.cos(2*th) + qk**2, 1e-300))
        rho = np.exp(lw)/np.sin(th); E = np.cos(th)
        idx = np.argsort(E); E, rho = E[idx], rho[idx]; rho /= np.trapz(rho, E)
        return E, rho
    print("  DSSYK DOS = the q-Gaussian (continuous q-Hermite weight). Flatness near the de Sitter point E=0:")
    print(f"     {'q':>5}{'rho(.3)/rho(0)':>16}{'flat-to-10% window |E|/Emax':>30}")
    for q in (0.1, 0.3, 0.5, 0.7, 0.9):
        E, rho = qH_dos(q); r0 = np.interp(0, E, rho)
        within = np.abs(rho-r0)/r0 < 0.10; i0 = int(np.argmin(np.abs(E))); lo = hi = i0
        while lo > 0 and within[lo-1]: lo -= 1
        while hi < len(E)-1 and within[hi+1]: hi += 1
        print(f"     {q:>5.1f}{np.interp(0.3, E, rho)/r0:>16.3f}{min(abs(E[lo]), abs(E[hi])):>30.2f}")
    print("""  => the DSSYK DOS has a SMOOTH MAXIMUM at the de Sitter point and is flat to ~10% over a central window
  (~0.34 of the half-width near the semicircle/low-q limit, narrowing toward the Gaussian/q->1 limit). So the
  flat near-horizon DOS that 1b requires DOES exist in DSSYK -- near E=0. That is a real, encouraging
  consistency (the right qualitative shape is present), not a derivation.\n""")


def the_three_targets():
    print("="*92); print("THE THREE QUANTITATIVE TARGETS (what the calculation must hit)"); print("="*92)
    print("""  (i)  THE REGIME: what effective q (lambda) describes the de Sitter horizon? The semiclassical de Sitter
       limit is lambda->0 (q->1), where the flat window NARROWS (to ~0.07) -- but T_dS also shrinks there. So
       there is a RACE: does T_dS/E_max stay inside the flat window as q->1? That competition must be resolved.
  (ii) THE CUTOFF: compute T_dS/E_max in the de Sitter regime and check it lies inside the flat window. If yes,
       the freezing is linear (MOND); the exact ratio fixes a0/cH = 1/Z.
  (iii)THE COUPLING: does the matter chord couple to the flat CENTRAL modes (the analog of 1c's spherical-
       probe->monopole selection rule)? This is the DSSYK version of 'why the probe sees the flat sector'.
  All three are computable in the existing DSSYK correlator formalism. None is hand-waving; each is a defined
  q-series calculation.\n""")


def difficulty_and_risk():
    print("="*92); print("HONEST DIFFICULTY AND RISK"); print("="*92)
    print("""  DIFFICULTY: paper-level, ~6-18 months for someone fluent in the chord formalism. The machinery exists
  (Berkooz et al. 2018 for the spectrum and correlators; Lin 2022 for the bulk Hilbert space; Narovlansky-
  Verlinde 2023 / Rahman for the de Sitter map), but assembling it into an N_eff(T) freezing is new.
  MAIN RISK: the 'equipartition / freezing' framing may not map cleanly onto a DSSYK observable -- N_eff might
  not be the natural quantity, and the MOND interpretation could fail to survive a careful translation. If it
  fails, that is itself a real result (it would say the freezing picture is not the right route, and push the
  sign problem back to the modified-entropy alternatives of Project 1, Part 5).
  WHAT THIS FILE IS: a precise statement of the calculation + one computed indicator (the DOS is flat near the
  de Sitter point) + an honest difficulty/risk. NOT a derivation. The derivation is the research project.\n""")


def main():
    print("#"*92); print("# PROJECT 4b -- scoping the DSSYK calculation that would close the deep-MOND sign"); print("#"*92 + "\n")
    the_dictionary(); the_calculation(); dos_indicator(); the_three_targets(); difficulty_and_risk()
    print("="*92); print("PROJECT 4b VERDICT"); print("="*92)
    print("""  The deep-MOND sign closes (or fails) in a DEFINED DSSYK calculation: insert a matter chord, extract
  N_eff(T), test for linear freezing below T_dS, read off Z. One rigorous indicator is already positive -- the
  DSSYK DOS is flat near the de Sitter point, the shape 1b needs. Three quantitative targets remain (the q
  regime, the T_dS/E_max ratio, the matter-chord coupling), all computable in existing formalism. This is the
  honest end of the in-session theory thread: not solved, but reduced from 'a vague gap' to 'a specific,
  paper-level q-series calculation with one encouraging indicator and a named failure mode'.""")
    print("="*92)


if __name__ == "__main__":
    main()
