# Parameter-family gate: the response repair is not arbitrary tuning

This door asks a narrower question than “is the full theory closed?”  In the
constant-coefficient high-acceleration quadratic family, does the observed V3
repair survive if its coefficients are not inserted by hand?

The scalar block is varied with free coefficients `d` and `t`, while the
constitutive Hessian is `alpha = 2-C` and the expansion stiffness is `ell`.
The conserved source is generated from an arbitrary symmetric seed `A_ij`:

\[
T_{00}=\partial_i\partial_j A_{ij},\qquad
T_{0i}=-\partial_t\partial_j A_{ij},\qquad
T_{ij}=\partial_t^2 A_{ij}.
\]

The script first derives the order-`r^2` longitudinal matching condition,
then computes the independent isotropic-stress `k -> 0` residue.  It finds two
scalar residue-free branches:

\[
d=t=C/2, \qquad d=t=(C-3\ell)/2.
\]

That is not yet a selection: a scalar source alone cannot decide between them.
The six symmetric seed polarizations are then varied independently and the
full electric-curvature response is checked.  The vector and tensor response
normalizations are also solved from the measured Newton constant, rather than
assigned:

\[
q_{\rm vector}=\tau_{\rm tensor}=C/2.
\]

At the witness `C=5/3`, `ell=1/100`, the first branch has zero uncancelled
`k^2` denominators and every entry denominator divides the product of the
luminal tensor symbol and the subluminal clock-wave symbol.  The second branch
has surviving `k^2` poles in the six-polarization response.  Thus the exact
linear gate selects `d=t=C/2`; it is the algebraic reason the V3 TT repair is
needed and it is a genuine narrowing of the construction space.

The result is a structural linear-response checkpoint, not a complete theory.
The curved/nonlinear York-TT variation, full Dirac closure, boosted PPN, the
`y -> 0` nonlinear limit, FLRW perturbations, and empirical catalogue fits are
still open.  In particular, “zero `k^2` poles” is not a proof that the
metric-dependent spatial pseudoinverses are causal on arbitrary backgrounds.

## Reproduce

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/parameter_family_gate.py
python3 -m unittest qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/test_parameter_gate.py
```

The provenance record for the durable JSON result is in `run_002/manifest.json`.
