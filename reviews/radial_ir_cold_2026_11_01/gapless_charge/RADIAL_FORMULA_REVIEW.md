# Restricted independent radial formula audit

Inputs: ../radial/DERIVATION.md as read 1 November 2026. This is a direct algebra
audit of the displayed graph kernels, not an independent execution or a full
audit of derivative vertices, state matching or pole gauge invariance. Final
input bytes are pinned in REVIEW_INPUTS.json.

The real scalar determinant gives the momentum-dependent term from two
H_s vertices with coefficient−Tr(G H_s G H_s)/4. Differentiating the bubble
at p²=0 gives the displayed ordered |H_s,ij|² I/(64pi²). A seagull lacks
external momentum. For a scalar Majorana mass perturbation the chirality-flip
mass product has the opposite sign from a phase/pseudoscalar perturbation;
the stated single-chiral ungauged SUSY constant cancellation is consistent.

The transverse-vector projector contraction is exactly

    Tr[P(k)P(k+p)] = d−1−[p²/k²−(k.p)²/k⁴]+O(p³).

Angular averaging gives−(d−1)p²/(d k²). Combining determinant−1/4, the
denominator derivative−I/L and the explicit projector term gives

    deltaA_VV=sum_ordered |(M²)_s,ab|²/(4L)[3I+3K/4].

Both derivative integrals are UV finite. Thus d→4 here introduces no
pole-generated evanescent constant. For equal masses I=1/(6x), K=1/x,
the coefficient is5|(M²)_s|²/(16Lx), as displayed. The separate SV finite
+1/2 has its own pole/projector origin from TP03 and should not be removed.

A gauged f=0 equality of the isolated off-shell radial and angular metrics
is not an established validation requirement: the fixed slice contains
additional light moduli, and component Landau coordinates need not be
manifest superspace Kähler coordinates. Its failure is not by itself a
physical pole anisotropy or an identified missing graph. The radial author
correctly discloses gauge/coordinate and occupied derivative limitations.
Verdict: the displayed scalar, fermion chirality sign and VV kernel pass this
restricted formula audit; no complete gauge-invariant pole claim is certified.
