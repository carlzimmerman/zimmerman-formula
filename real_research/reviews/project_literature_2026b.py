#!/usr/bin/env python3
"""
LITERATURE PULL 2026 (part b): wide binaries (still contested) + a DSSYK contingency on the sign-closure.
========================================================================================================
Two more doors from the real search, both reported straight -- one neutral, one that TEMPERS my own
sign-closure (the honest kind a literature pull is for).

(1) WIDE BINARIES (the 'is MOND real' foundation): still genuinely CONTESTED. Chae 2023-24 + Hernandez find
    the ~40% low-acceleration boost (MOND-consistent); Banik + Pittordis-Sutherland find Newtonian at 19 sigma;
    the 2026 work (arXiv:2603.11015) finds the result is SENSITIVE TO ORBITAL MODELING. Unresolved -- it does
    not settle whether there is an a0 at all. Consistent with the ~50% on 'MOND is real'.

(2) A DSSYK CONTINGENCY on the deep-MOND-sign closure. The DSSYK<->de Sitter program has TWO proposals:
    * Narovlansky-Verlinde 2023 (arXiv:2310.16994): de Sitter at the SPECTRAL CENTER (infinite-temperature,
      flat DOS) -- the reading the sign-closure (projects 4c-4f) USED;
    * Rahman 2022 (arXiv:2209.09997): dS-JT gravity from scaling around the EDGE E=E0 (Schwarzian DOS, NOT flat).
    The MOND linear freezing needs the FLAT DOS, so it follows under the CENTER reading and does NOT under the
    EDGE reading. So the sign-closure is CONTINGENT on de Sitter = center (Narovlansky-Verlinde). Honest caveat
    I did not know I was making until pulling the literature. Needs numpy.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal


def main():
    print("#"*92); print("# LITERATURE 2026b -- wide binaries (contested) + DSSYK center-vs-edge contingency"); print("#"*92 + "\n")

    print("="*92); print("(1) WIDE BINARIES -- still contested, does not settle 'is MOND real'"); print("="*92)
    print("""  Chae (2023-24): ~40% velocity boost at low acceleration, MOND-consistent. Hernandez (2023-24): anomaly
  confirmed. BUT Banik + Pittordis-Sutherland (2023-24): Newtonian preferred at ~19 sigma; and 2026 work
  (arXiv:2603.11015) shows the measurement is SENSITIVE TO ORBITAL MODELING (eccentricity priors, undetected
  tertiaries). Net: the highest-stakes 'is there an a0 at all' test remains UNRESOLVED and methodology-driven
  -- Gaia DR4 is needed. No update to the ~50% on whether MOND is real.\n""")

    print("="*92); print("(2) THE DSSYK CONTINGENCY -- center (flat, MOND) vs edge (Schwarzian, NOT MOND)"); print("="*92)
    # quantify: the q-Gaussian DOS is flat at CENTER, vanishes (~sqrt) at the EDGE. The freezing power differs.
    q = 0.5; N = 3000
    n = np.arange(1, N); b = np.sqrt((1-q**n)/(1-q))
    Ev, V = eigh_tridiagonal(np.zeros(N), b); E = Ev/(2/np.sqrt(1-q)); w = V[0, :]**2; w /= w.sum()
    # density near center vs near edge
    cen = w[np.abs(E) < 0.05].sum()/0.10
    edg = w[np.abs(np.abs(E)-0.95) < 0.05].sum()/0.10
    print(f"""  The DSSYK chord-vacuum DOS (q-Gaussian) is FLAT at the center and VANISHES (~sqrt) at the edge:
     density near center (|E/E0|<0.05): {cen:.2f}    density near edge (|E/E0|~0.95): {edg:.2f}
  The deep-MOND LINEAR freezing (N_eff~T) requires a FLAT DOS (project 1b/4c) -> it follows ONLY at the
  CENTER. At the EDGE the DOS ~ sqrt(distance) -> a different (non-MOND) freezing power.
  TWO competing de Sitter readings:
    * CENTER = de Sitter (Narovlansky-Verlinde): flat DOS -> the sign-closure (4c-4f) HOLDS.
    * EDGE = dS-JT (Rahman): Schwarzian DOS -> the MOND freezing does NOT follow.
  => the deep-MOND-sign closure is CONTINGENT on the Narovlansky-Verlinde (center) reading being the correct
     de Sitter dual. That is an open question IN the DSSYK-de Sitter program itself. Honest tempering of the
     'sign closed' claim: it is closed UNDER a specific (serious, but not sole) de Sitter correspondence.\n""")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  Net of part b: the wide-binary foundation is unresolved (no change to 'is MOND real'~50%); and the
  deep-MOND-sign closure, while it rests on the VERIFIED matter element (Okuyama eq.18, part a), additionally
  ASSUMES the de Sitter horizon sits at the DSSYK spectral center (Narovlansky-Verlinde) where the DOS is
  flat -- it would fail under the competing edge/dS-JT reading. So the sign is closed CONDITIONALLY on that
  correspondence. This slightly tempers the 'sign solved' headline to 'sign solved given de Sitter = the
  DSSYK center', and identifies that as the next thing to pin in the holography literature. Reported straight
  -- a literature pull that both confirmed (the element) and qualified (the de Sitter location) the result.""")
    print("="*92)


if __name__ == "__main__":
    main()
