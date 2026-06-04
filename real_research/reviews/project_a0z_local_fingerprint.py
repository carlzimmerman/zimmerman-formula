#!/usr/bin/env python3
"""
Does the two-horizon law leave a fingerprint in the z=0 SPARC RAR? No -- it is degenerate locally, and that
is itself the point. Plus an honest correction: the rate-spread is NOT the interpolation-broadening spread.
=========================================================================================================
Last step proposed that a sub-E(z) rise points to a two-horizon law a0 = c sqrt(H(z) H_L)/Z' (H_L = H0 sqrt(OL),
the constant event-horizon rate), p=1/2, vs the framework's a0 = cH(z)/Z, p=1. Question: can the LOCAL SPARC
RAR -- the framework's most solid result -- tell them apart?

ANSWER: NO. At z=0 the two forms differ only by a factor OL^{1/4} = 0.91 (a 9% shift, fully absorbable into the
O(2pi) coefficient and far inside the SPARC a0 uncertainty +-0.26e-10 ~ 20%). They are DEGENERATE locally. The
reason is the coincidence we live in: the apparent-horizon rate H0 and the event-horizon rate H_L = H0 sqrt(OL)
differ by only 1/sqrt(OL) = 1.21 (21%, = 0.082 dex) TODAY, because we sit near the onset of Lambda domination.
So the z=0 RAR is ORTHOGONAL to the rate question -- the local data we are most confident about carry NO
information on cH vs c sqrt(H H_L). ALL the discriminating power is at high z: the ratio a0(p=1)/a0(p=1/2) =
E(z)^{1/2} exceeds 10% only beyond z~0.4, reaching 34% at z=1 and 114% at z=3. The clean deep-MOND z~3 disk is,
again, the unique settler.

HONEST CORRECTION to the previous step's "one structure, two fixes": the two-horizon RATE spread at z=0 (the
apparent-vs-event temperature difference) is only 0.082 dex, whereas the interpolation BROADENING that fixed
the RAR shape needs ~0.33 dex -- a factor ~4 larger. So the rate and the shape are NOT set by the same single
parameter; they are different SCALES of the de Sitter temperature structure (both "many temperatures"
qualitatively, but quantitatively distinct). The earlier "one knob fixes both" was overstated; recorded
straight. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
c = 2.998e8
H0 = 67*1e3/3.086e22
Z = 2*np.sqrt(8*np.pi/3)


def main():
    print("#"*92)
    print("# Two-horizon law vs the z=0 SPARC RAR: degenerate locally; all discriminating power is at high z")
    print("#"*92 + "\n")
    cH0 = c*H0

    print("="*92); print("(A) AT z=0 -- the two forms give the SAME local a0 (degenerate)"); print("="*92)
    a0_p1 = cH0/Z
    a0_p05_clean = c*np.sqrt(H0*(H0*np.sqrt(OL)))/Z       # geom mean, same clean Z
    print(f"  a0 (p=1,   cH/Z):                  {a0_p1/1e-10:.3f}e-10")
    print(f"  a0 (p=1/2, c sqrt(H H_L)/Z):       {a0_p05_clean/1e-10:.3f}e-10   ({100*(a0_p05_clean/a0_p1-1):+.0f}%, = OL^1/4)")
    print(f"  a0 (p=1/2, with Z'=Z OL^1/4):      {a0_p1/1e-10:.3f}e-10   (identical by calibration)")
    print(f"  SPARC measured: a0 = 1.20 +- 0.26e-10 (~20%). The 9% gap is WELL inside the error.")
    print(f"  => the precision RAR fit (precision_rar_test.py, a0~local) applies to BOTH forms identically:")
    print(f"     the z=0 RAR CANNOT fingerprint cH vs c sqrt(H H_L).\n")

    print("="*92); print("(B) WHY -- the Lambda-onset coincidence we live in"); print("="*92)
    print(f"  apparent-horizon rate / event-horizon rate today = H0/H_L = 1/sqrt(OL) = {1/np.sqrt(OL):.3f}")
    print(f"  the two horizons differ by only {100*(1/np.sqrt(OL)-1):.0f}% NOW (= {np.log10(1/np.sqrt(OL)):.3f} dex) -> degenerate at z=0.")
    print(f"  This is the same 'why now' coincidence that makes a0 ~ cH0 ~ c sqrt(Lambda/3) both hold today.\n")

    print("="*92); print("(C) WHERE they diverge: ratio a0(p=1)/a0(p=1/2) = E(z)^(1/2)"); print("="*92)
    print(f"  {'z':>6}{'ratio':>9}{'% diff':>9}")
    for z in (0.2, 0.4, 0.7, 1.0, 2.0, 3.0):
        print(f"  {z:>6.1f}{E(z)**0.5:>9.2f}{100*(E(z)**0.5-1):>8.0f}%")
    print("  => >10% only beyond z~0.4; the discriminating power is entirely at high z (z~3 best).\n")

    print("="*92); print("(D) HONEST CORRECTION -- the rate spread is NOT the interpolation-broadening spread"); print("="*92)
    sig_rate = np.log10(1/np.sqrt(OL)); sig_broad = 0.33
    print(f"  two-horizon RATE spread at z=0 (apparent vs event temperature): {sig_rate:.3f} dex")
    print(f"  interpolation BROADENING that fixed the RAR shape (project_manytemp): {sig_broad:.2f} dex")
    print(f"  ratio = {sig_broad/sig_rate:.1f}x  ->  DIFFERENT parameters. Both are 'many temperatures' qualitatively,")
    print(f"  but the shape needs a ~4x larger spread than the rate provides. The previous step's 'one structure,")
    print(f"  two fixes' was overstated: rate and shape are different SCALES of the temperature structure.\n")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  No -- swapping cH for c sqrt(H H_L) leaves NO detectable fingerprint in the z=0 SPARC RAR: the two
  forms agree to 9% locally (absorbed by the O(2pi) coefficient, inside the 20% a0 error), because the apparent
  and event horizons differ by only 21% at the present epoch (the Lambda-onset coincidence). So the local RAR
  we 'nailed' is ORTHOGONAL to the rate question and cannot be leaned on either way; the entire discriminating
  power lives at high z (E(z)^1/2: 34% at z=1, 114% at z=3), where the clean deep-MOND z~3 disk decides. And an
  honest correction: the rate-structure spread (0.08 dex) and the interpolation-broadening spread (0.33 dex)
  are NOT one parameter -- 'one structure, two fixes' was too strong. Net: the two-horizon refinement is
  consistent with everything local (trivially, by degeneracy), distinguished only by the high-z rate, and less
  unified than I claimed last step.""")
    print("="*92)


if __name__ == "__main__":
    main()
