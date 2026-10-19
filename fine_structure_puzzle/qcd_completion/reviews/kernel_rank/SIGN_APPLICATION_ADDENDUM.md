# Sign application addendum

This addendum supplies the source-to-target sign conversion requested by the coordinator and independent vector reviewer after they read `RAW_DERIVATION_v1.md`. The frozen raw proof and its input/hash receipt are unchanged. This is an additional hand argument; no new source or computational claim is introduced.

The raw factorization uses \(B=D\Phi\). The actual angular background, with \(D=\partial+A\times\) and the stated orientation, satisfies \(B=-D\Phi\). Set

\[
X=-\Phi,\qquad U(a_i,a_4)=(a_i,-a_4).
\]

Then \(B=DX\), so the raw proof applies to the background \((A,X)\). The map \(U\) is a constant orthogonal involution on the real fluctuation space. The source covariant fourth derivative and mixed curvature are
\(D_4^{X}=-D_4^{\Phi}\) and \(F_{i4}^{X}=-F_{i4}^{\Phi}\), while the spatial connection and spatial curvature are unchanged. Consequently

\[
H_X=U H_\Phi U^{-1}.
\]

The gauge conditions agree under the same map:

\[
D_i(Ua)_i+[X,(Ua)_4]
 =D_i a_i+[\Phi,a_4].
\]

Likewise the plus-sign Bogomolny deformation at \((A,X)\), evaluated on \(Ua\), is

\[
\operatorname{curl}_D a+D a_4-[\Phi,a],
\]

which is exactly the variation of the target equation \(B+D\Phi=0\). Thus the factorization, gauge-fixed kernel and weighted Fredholm bridge transfer unitarily. The weights split into the same neutral line and charged complement for \(X\) and \(\Phi\), so the target isometries and compactness argument are preserved. Smooth-origin, whole-space \(L^2\), and the relative finite-wall conditions are also preserved by \(U\).

For the source index, choose the positive asymptotic root chamber using \(X_\infty=-\Phi_\infty\). In the actual hedgehog convention, \(B_i\sim-n_i n/r^2\) and \(X\sim-n\); the magnetic charge is therefore the positive unit co-root relative to this chamber. Its positive-root pairing is two, and Kottke's charge is \(k=1\). Retaining the chamber determined by \(\Phi_\infty\) while changing only the Bogomolny sign would be an inconsistent application and would produce a spurious index-sign error.

The reflection commutes with grand-spin rotations. It sends the source translation modes to the actual \(F_{j\mu}^{\Phi}\) modes; the source phase differs from the target phase by an irrelevant overall sign. The kernel remains three real \(J=1\) translations plus one \(J=0\) phase before the unframed quotient. It also preserves the Wronskian form, charged/neutral dimensions, and nonzero translation tail. Therefore the kernel and conditional rank conclusions in the raw proof apply to the actual angular operator without changing the index sign.

Self-review: the fourth-component reflection, mixed-curvature sign, gauge condition, root chamber, and translation/phase mappings were checked algebraically. This addendum does not discharge the separate exact outer-basis/remainder obligation stated in the raw proof.
