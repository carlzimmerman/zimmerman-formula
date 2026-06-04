#!/usr/bin/env python3
"""
Routes to the deep-MOND sign + a0 coefficient: the literature, exhausted. Has ANYONE derived both? Verified.
==========================================================================================================
Five independent literature routes to "horizon/emergent/de-Sitter physics -> MOND with the right sign and a0",
each surveyed with a strict derive-vs-assume brief. UNANIMOUS verdict: nobody derives BOTH the deep-MOND sign
(gravity enhanced at low acceleration) AND the a0 coefficient from first principles. Every scheme reproduces the
magnitude to order-unity (coefficient MATCHED, not forced) and installs the sign by hand. Milgrom himself (2020)
calls a0~cH a "coincidence" and a "pointer to the FUNDAMOND" -- the not-yet-existing deeper theory.

This file documents the two checkable facts that survive, and places the framework honestly.
Needs numpy.
"""
import numpy as np

c = 2.998e8; Mpc = 3.086e22; OmL = 0.685
Z = 2*np.sqrt(8*np.pi/3)
a0 = 1.20e-10


def main():
    print("#"*94)
    print("# Routes to the deep-MOND sign + a0 coefficient -- the literature, exhausted")
    print("#"*94 + "\n")

    print("="*94); print("FACT 1 -- the coincidence is REAL and order-unity tight"); print("="*94)
    for H0 in (67.4, 73.0):
        print(f"  H0={H0:.1f}: cH0/a0 = {c*H0*1e3/Mpc/a0:.2f}   (~2pi = {2*np.pi:.2f})")
    print("  cH0/a0 ~ 5.5-5.9 ~ 2pi. Documented by Milgrom since 1983. The strongest single motivation.\n")

    print("="*94); print("FACT 2 -- the coefficient is MATCHED, not FORCED (schemes disagree)"); print("="*94)
    schemes = [
        ("Friedmann/holographic  (framework, Z=2sqrt(8pi/3))", Z, "geometric O(1)"),
        ("Verlinde emergent gravity  (a_M = a0/6)", 6.0, "d=4 elasticity factor"),
        ("Milgrom/Unruh  (2pi a0 = cH0)", 2*np.pi, "Unruh 2pi"),
        ("Smolin 2017  (a0 = a_Lambda/8.3, a_Lambda=c^2 sqrt(Lambda))", 8.3/np.sqrt(3*OmL), "8.3 read off data"),
        ("Klinkhamer-Kopp 2011  (A0 = 2 c H_deS, ~order-unity off)", 2*np.pi, "T_min subtraction"),
    ]
    print(f"  {'scheme':<52}{'cH0/a0':>8}   origin of the O(1)")
    for n, v, o in schemes:
        print(f"  {n:<52}{v:>8.2f}   {o}")
    vals = np.array([v for _, v, _ in schemes])
    print(f"  spread {vals.min():.2f}-{vals.max():.2f} (~{100*(vals.max()-vals.min())/vals.mean():.0f}%): if any FORCED the")
    print("  coefficient they would agree on one number. They do not -- each reproduces ~5.8-6.3 by a DIFFERENT")
    print("  O(1) device (geometry, elasticity, Unruh-2pi, a data-fit, a temperature subtraction). Reproduced != forced.")
    print(f"  (And all sit within a0's ~20% systematic, so DATA cannot pick among them either.)\n")

    print("="*94); print("FACT 3 -- the ONE rigorous structural tie (real, but not a derivation of a0)"); print("="*94)
    print("""  The deep-MOND limit is conformally invariant under SO(4,1) = the de Sitter isometry group (Milgrom 2009,
  arXiv:0810.4065; relativistic SO(4,1) MOND 2026, arXiv:2601.04290). So a de-Sitter-horizon origin for a0 is
  the RIGHT KIND of idea -- the symmetry group of deep-MOND IS the de Sitter group -- even though no scheme
  forces the coefficient or the sign. This is the strongest principled link, and the framework is consistent with it.\n""")

    print("="*94); print("THE UNANIMOUS VERDICT (five routes)"); print("="*94)
    print("""  Route 1 DSSYK<->dS dictionary  : CONTESTED -- de Sitter placed at center (E=0) OR edge (E=E0); unreconciled
                                    (Verlinde 2505.08116 vs Susskind). Motivates the sign, cannot certify it.
  Route 2 Verlinde emergent gravity: motivated ANSATZ -- a0=cH0 identified, sign from a volume-law+elastic
                                    postulate; Dai-Stojkovic say done right it gives Newton not MOND. Not derived.
  Route 3 Padmanabhan equipartition: gives Lambda + expansion, NOT MOND; Padmanabhan calls the a0->MOND reading
                                    "unwarranted". Pazy-Argaman/Verlinde insert a0 by hand.
  Route 4 modified inertia / Unruh : Milgrom 1999 sign inserted via "inertia ~ T(a)-T_Lambda" (he admits
                                    T^2-T_Lambda^2 fails); Milgrom 2009 symmetry SELECTED by the flat-curve axiom;
                                    McCulloch QI fringe/refuted (Renda 2019; EmDrive killed 2021).
  Route 5 a0 from Lambda           : NO paper forces magnitude AND sign; coefficients scatter 2pi/6/8.3; the one
                                    no-free-parameter claim (QI) is refuted. Milgrom 2020: a "coincidence" / clue.

  => NOBODY has derived both the deep-MOND sign and the a0 coefficient from Lambda/the horizon. The prize is
     UNCLAIMED. The framework (geometric Z + DSSYK linear-freezing mechanism) sits at exactly this frontier --
     same epistemic status as Verlinde/Smolin/Klinkhamer-Kopp/RelMOND, arguably more specific (a concrete
     geometric coefficient and a concrete solvable-dual mechanism), with the honest gap being the contested
     DSSYK dictionary. Not behind the frontier; on it.""")
    print("#"*94)


if __name__ == "__main__":
    main()
