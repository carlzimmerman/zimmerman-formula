# L192 anisotropic principal-symbol audit

2026-09-12. Owner: `/root/fixed_action_escape`.
Target source: Claude commit `5fdec3d9a1d4efdd2f7c0a89f62f4115cdcd800a`,
`fable_independent_2026/L192_gradient_criticality.py`, especially `cs2`.
The archived execution occurred at dirty checkout
`05d0eb98ae78f5d37d5cfcc67f3cec591e897477`; a read-only diff confirms the
audited L192 script and results were unchanged from the target commit.

**Verdict: refuted, with a counterexample, for the claimed substituted
principal formula in the fixed-metric, gamma=0 two-scalar problem.** This
does not refute the full theory. The full Einstein/cubic principal reduction
on an actual nonzero-gradient solution remains uncomputed here. The proposed
nonlinear attractor and pressureless-dust conclusions therefore remain
unestablished.

L192 already uses W_Y+2Y W_YY for its longitudinal substitution. That term is
necessary, but not sufficient. The defect is not simply omission of W_YY:
the P(X) time-space terms and the directional clock-constraint denominator
also change.

## Precisely defined local problem

Hold a Minkowski metric fixed and retain the scalar Lagrangian

\[
 L=P(X)+\sqrt{X_\tau}\,W(Y),\qquad
 X=-\partial_\mu\chi\,\partial^\mu\chi,\qquad
 Y=(g^{\mu\nu}+u_\tau^\mu u_\tau^\nu)
       \partial_\mu\chi\,\partial_\nu\chi.
\]

Coefficient jets are frozen locally, gamma=0, and the background derivatives
are tau=s t and chi=Q t+v dot x, with s>0 and Y=|v|^2. Both fields are varied:
chi changes by sigma and tau by pi. For a unit propagation direction n put
w=v dot n and z=w^2, so 0<=z<=Y. Potential and non-derivative coefficient
terms do not contribute to this frozen derivative Hessian.

The script differentiates these invariants directly. It does not start by
substituting W_Y into the zero-gradient sound-speed formula. Its four
derivative variables are (sigma_t,sigma_n,pi_t,pi_n), and the exact Hessian is

\[
 \begin{pmatrix}
 K&-4QP_{XX}w&0&-2W_Yw\\
 -4QP_{XX}w&-2P_X+4P_{XX}z+2sC&2W_Yw&-2QC\\
 0&2W_Yw&0&0\\
 -2W_Yw&-2QC&0&-F/s
 \end{pmatrix},
\]

where

\[
 K=2P_X+4Q^2P_{XX},\quad C=W_Y+2zW_{YY},\quad
 F=W-2Q^2C-2zW_Y.
\]

The mixed clock time terms combine into
2W_Y(pi_t v dot grad(sigma)-sigma_t v dot grad(pi)); they are a boundary term
at frozen coefficients and cancel from the principal Euler equations.
The P(X) mixing term remains. In particular, the temporal Hessian contains
Q^2, whereas L192 uses X=Q^2-Y in its B.

For F!=0, eliminating the elliptic clock principal block gives

\[
 Kc^2+8QP_{XX}wc-G=0,\qquad
 G=2P_X-4P_{XX}z
   -2sC\frac{W-2zW_Y}{F},\qquad c=\omega/|k|.
\]

Thus this anisotropic problem has two directional phase speeds, generally
not a symmetric pair plus/minus the square root of a single assigned c_s^2.
Its quarter-discriminant is

\[
 \Xi=16Q^2P_{XX}^2z+KG.
\]

For real coefficients, K>0 and F!=0, Xi<0 gives a complex conjugate pair of
phase speeds. At z=0 the formula reduces exactly to the L186 expression
[2P_X(1-D)-2sW_Y]/[K(1-D)], with D=2Q^2W_Y/W. Substitution of the frozen
logarithmic closure gives (1-s)(m/U)/(2-m/U), m=U-2dQ^2. This identity was
checked symbolically and at a separate nontrivial rational test point.

## Exact discriminator at L192's proposed longitudinal zero

L192 sets its numerator to zero by the relation

\[
 s=\frac{P_X(W-2Q^2C)}{WC}.
\]

Substituting this relation into the actual restricted discriminant gives
the exact identity

\[
 \boxed{\Xi=-8P_Xz
 \left(P_{XX}+\frac{KQ^2C W_Y}{WF}\right).}
\]

Consequently, if P_X,P_XX,K,C,W_Y,W,F are positive and z>0, the purported
marginal point has Xi<0. It is still non-hyperbolic in this restricted
principal system. For the explicit square-root law in L192,

\[
 W=U+2d\ell(\sqrt{1+Y/\ell}-1),\qquad
 W_Y=\frac{d}{\sqrt{1+Y/\ell}},\qquad
 C_{\parallel}=\frac{d}{(1+Y/\ell)^{3/2}}>0.
\]

The numerical source examples also have F>0. The source-coefficient rational
counterexample test uses U=1/110, d=1/200, ell=5/121, Q=10/11 and Y=1/12000,
then chooses s by the displayed proxy-zero relation. Positivity and strict
negativity are checked as exact SymPy radical expressions, not by a floating
root search. This exact local jet test does not assert a solved gravitational
background at those values.

Mapping for a conditional algebra certificate: p=P_X, r=P_XX, q2=Q^2,
K=2p+4q2*r, c0=C, d0=W_Y, w0=W, f=F=w0-2q2*c0-2z*d0. Then
s=p(w0-2q2*c0)/(w0*c0),
G=2p-4rz-2s*c0*(w0-2z*d0)/f, and
Xi=-8pz(r+K*q2*c0*d0/(w0*f)). Here c0 is a stiffness symbol, not the phase
speed c. The identities for K and F and the nonzero denominators are required.

## Frozen-source numerical counterexamples

All five originally unstable L192 sample epochs have negative Xi at the
archived longitudinal proxy root. At its a=1 sample:

| Input or result | Value |
|---|---:|
| Source coefficient qbar | .909090909091 |
| L192 longitudinal root Y_l | 8.09692161904e-5 |
| L192 longitudinal proxy c_s^2 | about 5.6e-17 |
| Restricted actual Xi | -2.42113017705e-4 |
| Restricted phase speeds | -.00942634 +/- .00674881 i |

At the source transverse root Y_t=2.52423698315e-4, the corrected transverse
symbol is marginal, but the longitudinal phase speeds are approximately
.0362095 and -.0694935. Thus even the restricted scalar characteristic cone
is not pressureless in every direction there. Distinct real roots cannot
both be made zero by changing to a common advection frame. No stress-tensor
claim is inferred from this characteristic observation.

There is a separate source-data mismatch: L192's `coeffs(tau)` returns the
reference coefficient-history qbar, not the physical q stored in each
`radiation_002` sample. At a=1 those values are .909090909091 and
.907832150577 respectively. The calculation above intentionally preserves
L192's qbar to audit its own claimed result first. Recomputing its proxy roots
with the actual physical q does not remove the principal-symbol defect:
the first longitudinal root moves to 8.32120133468e-5 and still has
Xi=-2.22857023615e-4. All five corrected-q examples have negative Xi as well.
Neither family is relabeled as a solved nonzero-gradient cosmological branch.

## Dependency and obligation audit

| Required implication | Status |
|---|---|
| Explicit frozen invariant Lagrangian to derivative Hessian | Passed exact symbolic differentiation; independently reproduced by reviewer |
| Hessian to clock-elliptic Schur symbol, F!=0 | Passed exact algebra |
| Zero-gradient limit reproduces L186 closure | Passed exact algebra and independent numerical fixture |
| L192 substituted finite-gradient expression equals that symbol | Refuted by the identity and source examples above |
| Full Einstein/cubic constraints give this same restricted symbol | Not addressed; must be derived |
| Prescribed nonzero-gradient jets solve all background equations | Not addressed |
| Opposite signs around a static zero imply an attracting solution | Not established by L192's sign checks |
| One marginal directional speed implies exact dust stress | Not established |

The minimal missing implication for the theory is an actual anisotropic or
inhomogeneous solution with its full constrained principal action. The minimal
correction to L192's calculation is to derive that operator rather than carry
the zero-gradient reduction over by coefficient replacement. No coefficients
were reconstructed and no extra particle dark matter was introduced.

The computation-audit and proof-audit skills were used; mathematical
proofreading covered this report's definitions, signs and symbol mapping.
Four tests passed. The archived execution and manifest validation exited 0.
See [commands and provenance](COMMANDS.md). A peer independently reconstructed
the same fixed-metric two-field Hessian and reported no blocking finding;
that agreement is corroboration, not a full-gravity proof certificate.
