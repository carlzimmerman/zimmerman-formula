# IR regularity result

The finite-(k) trace-free cancellation equation is

\[
R_{TF}+k^2\Lambda_{TF}=0,
\qquad R_{TF}=2M^2 S y^2e^{-y}.
\]

The action-level principal-symbol solution is therefore

\[
\Lambda_{TF}(k)=-\frac{2M^2 S y^2e^{-y}}{k^2}.
\]

For a generic anisotropic source (R_{TF}(0)\ne0), the multiplier diverges
as (k\to0).  Conversely, any regular (\Lambda_{TF}) has
(k^2\Lambda_{TF}\to0), so it cannot cancel the source in the zero-mode
limit.  The vanishing angular average of a spherical (ell=2) pattern is a
special source restriction and does not supply a generic inhomogeneous
(k=0) continuation.

`ir_regularity_gate.py` derives these statements and returns exit 0 when all
four symbolic checks pass.  This is not a universal no-go for every possible
nonlocal theory, but it is an obstruction to claiming that the present local
tensor-multiplier branch has a regular all-(k) Dirac closure without an
additional infrared prescription.  It also flags the inverse-Laplacian,
instantaneous channel that must be tested against the physical-metric
causality requirement.
