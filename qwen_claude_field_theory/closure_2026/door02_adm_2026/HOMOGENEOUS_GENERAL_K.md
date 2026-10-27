# Homogeneous general-⁠(K) check on the trace-degenerate branch

This is a small exact symbolic supplement to `RESULT.md`. It varies the
homogeneous reduced action before specializing the trace coefficient to
(D=0), keeps (K(Q)) arbitrary, and checks the resulting continuity identity
with SymPy. It is a necessary-condition calculation, not a full Dirac or
perturbation analysis.

## Result

For (h_{ij}=a^2gamma_{ij}), sectional curvature κ, (H=˙a/a), and
homogeneous (Q), the (D=0) branch gives

\[
 \rho=-C+\frac{6F\kappa}{a^2}-K(Q)+QK'(Q),\qquad
 p=C-\frac{2F\kappa}{a^2}+K(Q),
\]
\[
 \rho+p=\frac{4F\kappa}{a^2}+QK'(Q),
 \qquad a^3K'(Q)=\text{constant},
 \qquad
 \dot Q=-3H\frac{K'}{K''}.
\]

The matter continuity identity is exact:

\[
 \dot\rho+3H(\rho+p)=0.
\]

The adiabatic slope computed before setting κ to zero is

\[
 \frac{\dot p}{\dot\rho}
 =\frac{a^2(K')^2}
 {(4F\kappa+Qa^2K')K''}.
\]

For the spatially flat branch this reduces to

\[
 \frac{dp}{d\rho}=\frac{K'}{QK''}.
\]

Thus, on a flat expanding solution with (QK'>0), choosing the isolated
scalar Hessian sign (K''<0) (the sign that makes the standalone
(-K''\dot Q^2) block positive) forces (dp/d\rho<0). This is a precise
gradient-instability warning for this degenerate homogeneous branch. It is not
a universal no-go, because the full coupled scalar/metric principal symbol
has not been diagonalized here.

The affine limit (K(Q)=\ell Q+K_0) is separately singular: the scalar
equation becomes

\[
 3\ell a^3H=0.
\]

Therefore ℓ≠0 forbids (H\ne0) in this homogeneous ansatz, while ℓ=0
returns the constant-(K) branch. In the flat constant-(K) case,
ρ+p=0, excluding ordinary dust/radiation as the sole source.

## Reproduction

```sh
python3 qwen_claude_field_theory/closure_2026/door02_adm_2026/homogeneous_generalK.py \
  > qwen_claude_field_theory/closure_2026/door02_adm_2026/homogeneous_generalK.json
python3 -m json.tool \
  qwen_claude_field_theory/closure_2026/door02_adm_2026/homogeneous_generalK.json
```

The script exits 0 and its exact JSON output records the identities and a
symbolic witness with (QK'=1), (K''=-1), κ=0, (H=1), for which
ρ+p=1 and (dp/dρ=-1). The witness is illustrative only; it is not a
global stability proof.

## Scope

This result applies only to the trace-degenerate (D=0) homogeneous branch of
the submitted ADM reduction. It does not establish the full constraint count,
the PPN parameters, the MOND law, or the health of the tensor-preserving
trace-regular branch. Those remain separate gates.
