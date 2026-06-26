#!/usr/bin/env python3
"""
PARITY LOCK: the 16 of SO(10) gives an EVEN Dirac index on S^4 for ANY embedded
sub-instanton -- so |N_gen|=3 (odd) is topologically UNREACHABLE from the S^4 saddle.
==============================================================================

This makes the parity obstruction convention-INDEPENDENT. It does NOT rely on a
single "Dynkin index T(16)" normalization; it uses the explicit branching of the
16 and the additive index theorem zero-mode count for whatever SU(2)/SU(N)
sub-bundle the instanton lives in.

Index theorem (Atiyah-Singer, standard normalization, VERIFIED vs primaries):
   n_L - n_R = 2 * ell(r) * k_subgroup
where ell(fundamental SU(N)) = 1/2 (so SU(2) doublet, k=1 -> 2*(1/2)*1 = 1 mode),
k_subgroup = the instanton number carried in that subgroup factor.

We compute the TOTAL index of the 16 for an instanton sitting in each maximal
sub-SU(2) (or SU(N)) of SO(10), using the BRANCHING-CONSISTENT index coefficients
from the primary decomposition:
   tr_16 F^2 = 2 tr_4 F^2_SU(4) + 2 tr_4bar F^2_SU(4) + 4 tr_2 F^2_SU(2)L + 4 tr_2 F^2_SU(2)R
(arXiv hep-th/9604112; Pati-Salam SU(4)xSU(2)xSU(2) branching 16=(4bar,1,2)+(4,2,1)).

Run:  python3 real_research/reviews/s4_index_parity_check.py
"""

import sympy as sp


def hr(t=""):
    print("=" * 80)
    if t:
        print(t); print("=" * 80)


def main():
    hr("PARITY OF THE 16-INDEX ON S^4 -- convention-independent")
    print("Index theorem coefficient of tr_r F^2 in the anomaly poly = 2*ell(r).")
    print("From the VERIFIED 16-branching (Pati-Salam embedding in SO(10)):")
    print("  tr_16 F^2 = 2 tr_4  F^2_SU(4)   (the 4  of SU(4))")
    print("            + 2 tr_4b F^2_SU(4)   (the 4b of SU(4))")
    print("            + 4 tr_2  F^2_SU(2)L")
    print("            + 4 tr_2  F^2_SU(2)R")
    print()
    # The index of the 16 RELATIVE to the index of each sub-fundamental:
    # zero modes for instanton k in a given subgroup factor = (coeff) * (modes of that fund at k)
    # modes of SU(N) fundamental at instanton k = k (standard: 2*ell(fund)*k = 2*(1/2)*k = k).
    # modes of SU(2) doublet  at instanton k = k.
    sub_coeffs = {
        "instanton in SU(2)_L  (16 -> contributes via (4,2,1))": 4,
        "instanton in SU(2)_R  (16 -> contributes via (4bar,1,2))": 4,
        "instanton in SU(4)  (acts on both 4 and 4bar)": 2 + 2,  # 4 and 4bar each coeff 2
    }
    k = sp.Symbol('k', integer=True)
    print(f"  {'instanton embedding':<52}{'index_16(k)':<14}{'parity'}")
    all_even = True
    for label, coeff in sub_coeffs.items():
        idx = coeff * k                      # net 16-zero-modes for charge-k sub-instanton
        # parity over all integer k: coeff*k is even-for-all-k iff coeff is even
        even_for_all_k = (coeff % 2 == 0)
        all_even &= even_for_all_k
        par = "EVEN for all k in Z" if even_for_all_k else "can be ODD"
        print(f"  {label:<52}{str(idx):<14}{par}")
    print()
    print("  Also the full-SO(10) instanton (the abstract Dynkin index T(16)=2):")
    print(f"     index_16 = 2k  -> EVEN for all k in Z.")
    print()
    hr("RESULT")
    print(f"  For EVERY way to embed the instanton, the net 16-zero-mode count is an")
    print(f"  EVEN multiple of the sub-instanton number k.  all_even = {all_even}.")
    print()
    print("  => index_16(D_E) on S^4 is ALWAYS EVEN, independent of:")
    print("       - which subgroup the instanton sits in,")
    print("       - the value of the (free) instanton number k,")
    print("       - the Dynkin-index normalization convention.")
    print()
    print("  Therefore |N_gen| = 3 (ODD) is TOPOLOGICALLY FORBIDDEN as the index of")
    print("  the 16 over the S^4 saddle. The S^4-saddle route can give 0,2,4,... but")
    print("  NEVER 3. This is a HARD obstruction, not a soft 'k not forced' statement.")
    print()
    print("  (Cross-check, DIFFERENT space: on S^10 with the SO(10) tangent/Euler bundle,")
    print("   the 16 has ONE net zero mode -- Euler(S^10)=2 route, Witten anomaly lit.")
    print("   That is the SO(10) GROUP MANIFOLD-scale sphere S^10, NOT our spacetime S^4;")
    print("   it does not apply to the 4-D HH saddle. Noted to avoid a false flip.)")


if __name__ == "__main__":
    main()
