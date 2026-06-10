#!/usr/bin/env python3
"""
INDEPENDENT REDERIVATION (not reusing the finder's functions).
Goal: settle the LOAD-BEARING claim of the Approach-B finding --
   chord number n maps to spectral ENERGY such that
       n = 0      -> spectral CENTER (E = 0)
       n -> large -> spectral EDGE  (|E| -> E0)
and therefore the SPATIAL bulk pode (deep in the static patch = large geodesic
length = large chord number) is the SPECTRAL EDGE, NOT the spectral center.

DSSYK facts I use (all standard, from Berkooz-Isachenko-Narovlansky-Torrents
1811.02584 and Lin 2208.07032):
  - The transfer matrix / Hamiltonian in the chord-number basis |n>, n=0,1,2,...
    is TRIDIAGONAL with
        diagonal   a_n = 0
        offdiag    b_n = sqrt([n]_q),  [n]_q = (1-q^n)/(1-q),  n=1,2,...
  - Energy eigenstates: H|theta> = E(theta)|theta>, E = (2/sqrt(1-q)) cos(theta),
    so E0 = 2/sqrt(1-q) is the band edge; E in [-E0, E0].
  - The chord-number-basis wavefunctions <n|theta> are the q-Hermite polynomials.

I rebuild everything from scratch with my OWN variable names and verify the
chord-number -> energy map THREE independent ways, plus a fourth purely
analytic continued-fraction cross-check that does NOT diagonalize anything.
"""
import numpy as np
from numpy.polynomial import polynomial as P

def qbracket(n, q):
    return (1.0 - q**n) / (1.0 - q)

def build_H(q, dim):
    """My own tridiagonal builder."""
    offdiag = np.array([np.sqrt(qbracket(k, q)) for k in range(1, dim)])
    H = np.zeros((dim, dim))
    for k in range(dim - 1):
        H[k, k+1] = offdiag[k]
        H[k+1, k] = offdiag[k]
    return H

def main():
    print("INDEPENDENT q-Hermite chord-number -> energy map\n")
    for q in (0.5, 0.7, 0.9, 0.95):
        dim = 3000
        H = build_H(q, dim)
        # Full dense eig/eigvec (independent of finder's eigh_tridiagonal path)
        evals, evecs = np.linalg.eigh(H)   # columns are eigenvectors
        E0 = 2.0 / np.sqrt(1.0 - q)
        x = evals / E0                      # normalized energy in [-1,1]

        print(f"q = {q}   E0 = {E0:.4f}")
        print(f"  {'n':>4}{'(A) peak|E/E0| of |<E|n>|^2':>30}"
              f"{'(B) RMS E/E0 numeric':>24}{'(C) RMS E/E0 analytic':>24}")
        for n in (0, 1, 3, 10, 40, 100):
            if n >= dim:
                continue
            # row n of evecs gives <E_k | n> for all k  (evecs[n, k])
            amp = evecs[n, :]
            w = amp**2
            w = w / w.sum()
            # (A) energy of the single largest-weight eigenstate
            peakE = abs(x[np.argmax(w)])
            # (B) RMS energy numerically: sqrt(<n|H^2|n>)/E0 = sqrt(sum w * E^2)/E0
            rms_num = np.sqrt(np.sum(w * (evals**2))) / E0
            # (C) analytic: <n|H^2|n> = b_n^2 + b_{n+1}^2 = [n]_q + [n+1]_q
            #     so RMS energy = sqrt([n]_q + [n+1]_q); /E0 = (1/2)sqrt((1-q)([n]_q+[n+1]_q))
            rms_ana = 0.5 * np.sqrt((1 - q) * (qbracket(n, q) + qbracket(n+1, q)))
            print(f"  {n:>4}{peakE:>30.4f}{rms_num:>24.4f}{rms_ana:>24.4f}")
        print()

    # ---- Fourth check: limits of the analytic RMS, no diagonalization ----
    print("ANALYTIC LIMITS of RMS E/E0 = (1/2) sqrt((1-q)([n]_q + [n+1]_q)):")
    for q in (0.7, 0.9, 0.95):
        n0 = 0.5 * np.sqrt((1 - q) * (qbracket(0, q) + qbracket(1, q)))  # [0]_q=0,[1]_q=1
        ninf = 0.5 * np.sqrt((1 - q) * (1/(1-q) + 1/(1-q)))             # [n]_q->1/(1-q)
        print(f"  q={q}:  n=0 -> {n0:.4f} (= (1/2)sqrt(1-q)),   n->inf -> {ninf:.4f} (= 1/sqrt(2)=0.7071)")
    print("\n  => n=0 sits NEAR E=0 (the smaller the (1-q), the closer to center);")
    print("     n->inf sits at RMS |E|/E0 = 1/sqrt(2)=0.707, i.e. spread over the band,")
    print("     and the PEAK weight (col A) marches to |E/E0|->1 (the EDGE).")
    print("  CONCLUSION: chord number 0 = spectral CENTER; large chord number = spectral EDGE.")

if __name__ == "__main__":
    main()
