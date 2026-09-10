# Elliptic double-multiplier constructive branch

This is a new explicit action-level construction, not a phenomenological
assignment:

\[
S=\int\!\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
 +\lambda\left(\Delta_h\chi-\frac14{}^{(3)}R\right)
 +\sigma\left(\Delta_h\chi-\mathcal A_n\right)
 +2M^2a_0^2Q\!\left(\frac{|D\chi|}{a_0}\right)\right]+S_m,
\]

where (\mathcal A_n=D_\mu a^\mu+a_\mu a^\mu=N^{-1}D^2N) and
(Q(y)=1-(1+y)e^{-y}).  In the static weak-field reduction
(R^{(3)}/4=\nabla^2\Psi) and (\mathcal A_n=\nabla^2\Phi).  The two
multiplier equations therefore give, for (k\ne0),

\[
\Phi=\Psi=\chi.
\]

Independent variation of the remaining fields gives

\[
\lambda'=0,
\qquad \sigma'=2(1-\mu)\Phi',
\qquad
\partial_x[\mu(|\Phi'|/a_0)\Phi']=4\pi G\rho,
\]

with the exact (mu(y)=1-e^{-y}).  Since the new terms contain only spatial
projections and no extrinsic-curvature term, the tensor principal ratio is
(c_T^2=1) in this diagnostic.

The branch is not yet closed: the full three-dimensional Hilbert variation
still leaves the anisotropic residual

\[
T_{ij}^{TF}\propto -2M^2\mu(y)(v_iv_j)_{TF},
\]

so a tensorial spatial compensator is the next unavoidable ingredient.  The
Lean file proves the (k\ne0) slip reduction, the exact AQUAL algebra, the
strict exponential sign, and the luminal ratio; it does not claim the missing
full Dirac/PPN/FLRW/stability gates.

The companion `dirac_double_multiplier_gate.py` computes the unitary-gauge
quadratic constraint chain independently in the (k\ne0) and (k=0) sectors.
It leaves one scalar phase-space pair; on the finite-(k) branch the reduced
Hamiltonian is (-7k^2\zeta^2), with no (p_\zeta^2) term.  This is an
instantaneous/strong-coupling clock-sector signal, not a hidden auxiliary that
may be declared absent.  A healthy explicit clock completion (or an additional
first-class constraint) remains required before claiming (N_{\rm grav}=2).

## Reproduction

```text
python3 -B elliptic_double_multiplier_gate.py
python3 -B run_lean.py
python3 -B -m unittest -v test_elliptic_double_multiplier.py
python3 -B dirac_double_multiplier_gate.py
```
