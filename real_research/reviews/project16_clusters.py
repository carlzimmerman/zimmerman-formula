#!/usr/bin/env python3
"""
PROJECT 16: galaxy clusters under the cosmic a0(z) -- pinning the known weakness honestly.
=========================================================================================
MOND's worst failure is galaxy clusters: even in MOND, relaxed clusters need ~a factor 2 MORE mass than the
baryons provide (the residual-mass problem; usually patched with neutrinos or unseen baryons). The framework
adds a knob clusters did not have: a0 rises with z. Does the z-boost help? This file shows, honestly, that
it does NOT -- it raises the MOND dynamical mass only as sqrt(E(z)), the wrong magnitude at the low-z
clusters where the discrepancy is measured. The weakness survives; the density reading is caught between
galaxies (RAR kills an environmental a0) and clusters. Stated plainly. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92); print("# PROJECT 16 -- clusters under cosmic a0(z): the known weakness, pinned"); print("#"*92 + "\n")
    print("="*92); print("THE PROBLEM AND WHETHER a0(z) HELPS"); print("="*92)
    print("""  In MOND the cluster dynamical mass goes as M_dyn ~ sqrt(G M_bar a0)/G in the deep-MOND regime, so for
  fixed baryons M_dyn ~ sqrt(a0). The cosmic a0(z)=a0(0)E(z) therefore boosts M_dyn by sqrt(E(z)):""")
    print(f"     {'z':>5}{'a0(z)/a0':>11}{'M_dyn boost = sqrt(E(z))':>26}")
    for z in (0.0, 0.3, 0.6, 1.0):
        print(f"     {z:>5.1f}{E(z):>11.2f}{np.sqrt(E(z)):>26.2f}")
    print("""  The classic cluster residual is ~a FACTOR 2 in mass, measured mostly at z < 0.3 (Coma, relaxed X-ray
  clusters). There the boost is sqrt(E(0.3)) ~ 1.08 -- an ~8% help against a 100% shortfall. Even at z=1 the
  boost is only ~1.34x. So the cosmic a0(z) does NOT close the cluster gap at the redshifts it is measured.\n""")

    print("="*92); print("THE DEEPER BIND (why this is not fixable by tuning a0)"); print("="*92)
    print("""  One might hope an ENVIRONMENT-dependent a0 (larger in the dense cluster core) closes the gap. But the
  galaxy-scale RAR (Project 13) is TIGHT and shows no such large environmental a0 boost -- the same a0 that
  fits galaxies is too small for clusters. So the density reading is caught in a vise:
    * make a0 bigger in clusters  -> breaks the tight galaxy RAR;
    * keep a0 from the RAR        -> clusters still miss a factor ~2.
  The cosmic a0(z) does not escape this: it is a function of EPOCH, not of local density, so it cannot
  selectively help clusters without also moving galaxies at the same z. The residual must come from real
  extra mass (neutrinos ~2 eV, warm/unseen baryons) -- the standard MOND patch -- which the framework neither
  improves nor worsens.\n""")

    print("="*92); print("PROJECT 16 VERDICT (honest negative)"); print("="*92)
    print("""  The cosmic a0(z) gives clusters only a sqrt(E(z)) boost (~8% at z=0.3), nowhere near the factor-2 gap,
  and it cannot be turned into an environmental fix without breaking the galaxy RAR. The cluster residual-
  mass problem -- MOND's hardest known failure -- SURVIVES unchanged in the framework; it still requires the
  standard extra-mass patch. This is the framework's clearest weak point, and a0(z) does not rescue it.
  Reporting it as a non-fix (not spinning the modest sqrt(E) boost as help) is the honest call.""")
    print("="*92)


if __name__ == "__main__":
    main()
