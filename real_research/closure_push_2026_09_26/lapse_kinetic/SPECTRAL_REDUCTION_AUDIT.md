# Independent audit: normalized ground-state lapse reduction

Date: 2026-09-26. Scope is the one new constraint-preservation implication in
`../spectral_lapse/RESULT.md`, not a new review of the entire theory.
The inspected report hash was
`3a54e5608ae39c68dad14dede3a17f864fee70cfe4e14c1c5d14da4be3b3f7a7` and its
`check.py` hash was
`983c7d1550c8bf9bec9199b95d31c6be59902a278fd5b5db068e2645daa64bd1`.

**Conclusion:** there is a valid conditional local symplectic reduction that
preserves the residual global eigenvalue constraint. It is stronger than the
initial-data construction alone. It needs the lapse-shape second-class
reduction and full canonical dependencies stated explicitly; a bare
Hellmann–Feynman identity or a spectral gap alone is not a full Dirac or
evolution theorem. One metric-volume correction is essential off shell.

## 1. Normalization and the metric-volume correction

Let z denote **all** remaining canonical metric, momentum, and matter data.
On a compact connected leaf without boundary, define

\[
 Q_z(y)=\int d\mu_{h(z)}[4b|D y|^2-\mathcal A(z)y^2],
 \qquad n_z(y)=\int d\mu_{h(z)}y^2.
\]

Assume the proposed Hamiltonian really has exactly the displayed N dependence,
with b>0 and A independent of N at fixed z. Normalize the positive simple
ground state by `n_z(y)=1`, write its eigenvalue as `lambda(z)`, and assume a
C1 eigenpair map in the function spaces used. This assumption includes a
nonzero spectral gap and appropriate regularity of all metric and coefficient
dependencies; a frozen-metric derivative is insufficient.

The normalized Rayleigh identity is `Q_z(y(z))=lambda(z)`. Differentiating the
quadratic form and its normalization gives

\[
 \delta\lambda=(\delta_zQ_z)(y)-\lambda(\delta_zn_z)(y).
\]

The second term is required when the metric volume changes. Therefore, for
the Hamiltonian at fixed coordinate lapse shape,

\[
 (\delta_zH)_y=-\delta\lambda-\lambda(\delta_zn_z)(y).
\]

It agrees with `-delta lambda` on the constraint `lambda=0`. The **total**
normalized pullback, including the change of y(z), obeys
`H[y(z),z]=-lambda(z)` and `dH=-d lambda` exactly off shell. These are different
variation statements. Metric variations of the Laplacian, gradient norm,
volume measure, and A must all be included in `delta_zQ`.

An arbitrary positive lapse on the selected branch is
`N=c(t)y(z)^2`, `c>0`; its spatial integral is c in this normalization.
The pullback Hamiltonian is consequently `H_red=-c lambda`.

The normalization fixes the **shape convention**, not this remaining global
scale. To embed the root's exact profile in its original clock chart, rescale
the raw `y=exp(epsilon cos x1)` to `exp(S_bar/2)y`. For `wc<0`, choosing
`S_bar-2|epsilon|>-2wc` gives
`0<u=(S+2wc)/(S+wc)<1` everywhere. If `y_norm=y/sqrt(I)` with
`I=integral y^2`, this same choice is represented by
`c=exp(S_bar) I`, not by deleting c or assuming the unshifted S=0 chart is
admissible. The scaling leaves the kernel shape, A, rho, and spectral gap
unchanged. Activation of the pin and other embedding constraints remains a
separate requirement.

## 2. Why canonical Hamiltonian preservation is conditional but substantive

Before imposing the remaining global constraint, solve the **projected**
shape equation `P_perp L(z)y=0` together with normalization. Its linearization
on the normalized complement is `L-lambda`. The simple isolated ground-state
gap makes this elliptic shape derivative invertible. The full equation
`L y=0` is then equivalent to the projected equation plus `lambda=0`.

The lapse has vanishing conjugate momenta. Locally, suppose the projected
secondary shape constraints and their primary momenta form an invertible
second-class block, so they can be replaced by the equivalent graph constraints

\[
 p_{\rm shape}=0,\qquad\chi=\text{shape}-Y(z)=0.
\]

Their matrix and inverse have the block form

\[
 C=\begin{pmatrix}0&-I\\I&\{\chi,\chi\}\end{pmatrix},
 \quad C^{-1}=\begin{pmatrix}\{\chi,\chi\}&I\\-I&0\end{pmatrix}.
\]

For observables depending only on z, their brackets with the primary shape
momenta vanish, and the lower-right inverse block is zero. Thus the reduced
Dirac bracket on z equals its original canonical bracket, even if Y depends
on both positions and momenta. Equivalently, pulling back the canonical
one-form with lapse momenta zero leaves exactly the canonical one-form of z.
A phase-dependent normalization change must include its induced momentum
shift before setting those primary momenta to zero; omitting that step off
the primary surface can give a wrong bracket.

With no other Hamiltonian term or unaccounted constraint contribution, the
remaining primary `p_c=0` has secondary `lambda(z)=0`, and

\[
 \dot\lambda=\{\lambda,-c\lambda\}_{\rm red}=0.
\]

If the momentum constraints generate the natural spatial diffeomorphism of
every canonical coefficient, metric, and volume measure in L, its eigenvalue
is invariant, hence `{λ,D[xi]}=0` as well. The pair `(p_c,lambda)` is then
first class relative to this remaining sector and describes one undetermined
global lapse scale. This is a conditional local constraint-preservation
theorem, not merely a numerical observation.

Regularity of the residual constraint is separate from simplicity of the
eigenvalue. For the root's exact family, varying its constant trace datum q
gives `d lambda/dq=2 ell q!=0` on the negative nonzero q branch, since L
contains `ell q^2` times the identity. That supplies a local regularity witness.

What still prevents an unconditional full-theory claim:

- The displayed H must be derived after all auxiliary reductions with the
  correct remaining canonical symplectic form; A must have no hidden lapse
  dependence.
- Every surviving metric, clock, matter, shift, and interface constraint must
  be included. Brackets with an omitted constraint can generate further
  conditions.
- In the continuum, the eigenpair map, projected inverse, Poisson functional
  derivatives, and Hamiltonian vector field require compatible domains and
  regularity. The finite-dimensional bracket identity does not prove local
  existence or prevent derivative loss in the nonlinear PDE.
- Preservation applies while the positive simple branch and its gap persist.
  It proves no noncompact-leaf gap or global-in-time evolution.
- The result does not complete the operative filtered-MOND splice, establish
  the physical field count, or derive a dark-energy scale.

## 3. Exact finite-dimensional analogue

The independent check uses a nonconstant positive mass matrix, so it detects
the volume term rather than silently fixing the inner product. Let `(q,p)` be
a canonical pair, `theta=q+pi/4`, `lambda=p+q^2`, and g>0. Set

\[
 M=\operatorname{diag}(e^q,e^{-q}),\quad
 u=(\cos\theta,\sin\theta)^t,\quad
 v=(-\sin\theta,\cos\theta)^t,
\]
\[
 K=M^{1/2}[\lambda I+g vv^t]M^{1/2},\qquad y=M^{-1/2}u.
\]

This generalized two-mode eigenproblem has eigenvalues `lambda,lambda+g`,
`y^tMy=1`, and positive y for `-pi/4<q<pi/4`. It is a Galerkin-style algebraic
analogue, not a discretization-based continuum proof. Its negative
off-diagonal K entry on this range also selects a positive ground vector.

Direct differentiation verifies

\[
 y^t K_q y=2q+\lambda\cos(2\theta),\qquad
 y^t M_q y=\cos(2\theta).
\]

Thus deleting the volume correction fails off shell; an explicit nonzero
control is recorded. Parameterize the normalized shape by the angle
`theta+eta`. The complete reduced-coordinate Hamiltonian is exactly

\[
 H=-c[\lambda+g\sin^2\eta].
\]

At eta=0, the shape primary/secondary bracket is `2cg!=0`, leaving
`H_red=-c(p+q^2)`. Its canonical equations
`qdot=-c`, `pdot=2cq` preserve `lambda` identically. The generic graph
constraint-block inverse is also checked independently.

The initial execution left the rotated quadratic-form trigonometric identity
unreduced and failed an equality assertion. Expanding angle sums **and their
products** before exact trigonometric reduction resolves it; a separate
minimal rotation check verified the cause. The original source and failed
manifest are retained. Only the successful corrected run is accepted.

## 4. Accepted bounded evidence

`run_spectral_reduction_002` completed in 1.306546 s with 37 passing exact
checks, including the nonzero missing-volume-term control and sixteen entries
of the graph-constraint inverse. These are algebraic checks, not 37 distinct
physics requirements. The run used Python 3.9.6 and SymPy 1.14.0, a 60 s wall
limit and 50 s CPU limit, no random sampling. Its recorded commit was
`7daaa5426076a2d78a50f3316007c7093255ce9a` with a dirty workspace.

The manifest passed `validate_manifest.py --root` with current input and result
hashes. Source SHA256:
`dd13b3182152891653ca253e7afca4607e915c0304b0dfeecf0053fa3623c3bc`.
Result/stdout SHA256:
`68b0ab20c234b30657665423dda5f882f23314e08bdc5381bbae3072cf92ad5d`.
The archived first script matches the failed run's recorded input hash.
There is no new Lean continuum or Dirac theorem in this bounded audit.
