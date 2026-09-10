# Normalized-acceleration parent: action gate (2026-09-09)

## Candidate action

Let

\[
s=\sqrt{-g^{\mu\nu}\nabla_\mu T\nabla_\nu T},\quad
n_\mu=-\nabla_\mu T/s,\quad a_\mu=n^\nu\nabla_\nu n_\mu,
\]

and define

\[
Y=\frac{c^2\sqrt{a_\mu a^\mu}}{a_0s},\qquad
H(Y)=G(Y)-Y^2=2(1+Y)e^{-Y}-2.
\]

The proposed covariant parent is

\[
S=S_{EH}-\frac{c^3a_0^2}{8\pi G_b}\int d^4x\sqrt{-g}\,sH(Y)+S_{clock}+S_m[g,\psi].
\]

The ordinary Einstein lapse piece supplies the `Y^2` primitive.  In clock
unitary gauge (`T=t`, zero shift), `sqrt(-g)s=sqrt(h)` and
`sqrt(a^2)/s=|D N|`, so the combined static constitutive primitive is exactly
`G(c^2|DN|/a0)`.  The script derives the resulting Euler operator rather than
inserting the divergence equation.

## What survives

The normalized density is independent of the undifferentiated lapse in this
gauge.  Its lapse variation is a pure spatial divergence, and the Einstein
plus auxiliary flux is

\[
\frac{G'(Y)}{2Y}=1-e^{-Y}.
\]

The old `sqrt(-g)G(sqrt(a^2))` normalization has a nonzero affine lapse
Euler residual; this parent removes that particular obstruction.  The local
Fourier primary/secondary lapse Poisson matrix is computed directly and has a
rank jump at `k=0`, so the homogeneous sector is not silently identified with
the local elliptic sector.

## Exact obstruction still visible

The covariant parent has metric dependence through the spatial norm and volume
element.  On `h_ij=diag(exp(2 sigma_parallel), exp(2 sigma_perp),
exp(2 sigma_perp))` the script obtains a nonzero finite-`Y` difference between
parallel and transverse metric Euler derivatives.  The transverse variation
contains two equal directions, so the per-direction anisotropy is

\[
E_\parallel-E_\perp/2=YF'(Y).
\]

Exact no-slip stress would require `F'=0`, while the lapse equation requires
`F'=2Y(1-exp(-Y))` (up to normalization).  This is a pointwise contradiction
for every finite `Y>0`; changing only the scalar constitutive function cannot
repair it.  The first-order `Psi` variation in the script gives the same
nonzero finite-gradient source.  The previous two-potential weak-field
calculation had suppressed this metric variation.  A compensator would have
to cancel this stress without adding a propagating mode and without destroying
the lapse constraint.

This is a scoped no-go theorem for the entire scalar-norm, lapse-neutral
parent class, not just for the selected `H`: a nonzero constitutive lapse flux
always carries directional stress because the same spatial norm is varied in
the metric equation.  The additive high-acceleration constant in `H` produces
only a volume offset (the script reports it separately); it cannot cancel the
directional term `Y H'(Y)`.

The companion `algebraic_compensator_gate.py` closes the obvious finite-tensor
escape.  If an auxiliary tensor has no derivatives and a nonsingular algebraic
Hessian, the actual envelope derivative after eliminating it is the partial
constitutive derivative.  The reduced theory is therefore still in the same
scalar-norm class and inherits the contradiction.  Its `(p_q,F_q)` Dirac block
has computed rank two for a regular Hessian and rank zero at a singular one.
Only a singular/topological or derivative compensator remains a genuinely
different door; those cases must be audited for extra modes and causal support.

## Status

**OPEN, not closed.**  This is a genuine architectural advance (the lapse
residual is removed), but it is not a complete relativistic MOND theory.  The
unavoidable next calculations are: covariant variation with respect to `T` and
`g^{mu nu}`, full hypersurface-deformation/Dirac closure including the clock,
independent `Phi`/`Psi` equations, PPN preferred-frame parameters, Ward identity,
FLRW perturbations, and the `Y -> 0` rank-controlled limit.

## Reproduction

```text
python3 -B normalized_acceleration_action_gate.py
python3 -B -m unittest -v
```
