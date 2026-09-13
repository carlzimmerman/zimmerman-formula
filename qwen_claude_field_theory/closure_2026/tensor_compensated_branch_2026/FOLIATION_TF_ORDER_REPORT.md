# Conditional derivative-order no-go

For linear scalar perturbations about an isotropic static clock foliation, the
standard local foliation invariants have trace-free spatial principal parts

\[
(D_i a_j)^{TF}\sim k^2\Phi,\qquad
{}^{(3)}R_{ij}^{TF}\sim k^2\Psi,qquad
[D_iD_j{}^{(3)}R]^{TF}\sim k^4\Psi.
\]

The scalar perturbation of (q_{ij}) is conformal, hence (q_{ij}^{TF}=0).
Therefore every finite local linear combination in this basis has

\[
P(k^2)=k^2\bar P(k^2),\qquad P(0)=0.
\]

Coupling a trace-free multiplier through such an operator reproduces the
previous result: a generic nonzero residual requires
\(\Lambda\propto1/P\), with an inverse-Laplacian infrared pole, while any
finite local regulator reintroduces slip.  The Python gate and Lean algebra
certificate verify the factorization without target ranks, PPN values, or DOF
counts.

This is conditional, not a universal theorem: it can be evaded only by adding
an extra background anisotropic/reference tensor, an algebraic nonlocal
operator, or a genuinely new field representation.  Each escape must then be
varied and subjected to the full Dirac, causality, PPN, FLRW, and stability
gates.
