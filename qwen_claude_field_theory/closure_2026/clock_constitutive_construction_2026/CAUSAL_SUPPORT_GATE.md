# Causal-support gate for the clock/projector action

The clock construction contains spatial York/Hodge pseudoinverses. A
pseudoinverse is not automatically an observable instantaneous channel: its
`1/k^2` residue can cancel after all metric equations and source-conservation
constraints are solved. `causal_support_gate.py` audits that cancellation in
the exact constant-coefficient Fourier family of `parameter_family_gate.py`.

The six independent symmetric conserved-source seeds are solved from the
varied scalar, vector and tensor equations. The scalar residue condition has
two branches, but the full six-source denominator test selects exactly one.
At `C=5/3, ell=1/100`, the selected branch has no bare spatial pole and its
denominators divide the product of

\[
\omega^2-k^2,
\qquad
 (2-C)(C+3\ell)\omega^2-2\ell k^2,
\]

after the usual `r=-i omega` continuation. The second cone has derived speed

\[
c_{\rm clk}^2=\frac{2\ell}{(2-C)(C+3\ell)}=\frac{18}{509}<1,
\]

while the tensor/light cone has `c_T^2=1`. The alternate residue-free branch
retains a bare `k^-2` pole and is rejected by the same calculation.

This is a genuine linear causal-support result for the selected branch, not a
full theory certificate. It does not vary the nonlinear metric-dependent
pseudoinverses, derive the complete curved-leaf Dirac algebra, or compute
boosted PPN `beta, alpha2, alpha3`. The action remains **OPEN** until those
obligations and the zero-field/FLRW/empirical gates are completed.

Run:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/causal_support_gate.py \
  --output qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/run_002/causal_support_results.json
python3 -B -m unittest discover \
  -s qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026 \
  -p 'test_*.py' -v
```
