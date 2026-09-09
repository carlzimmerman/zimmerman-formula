# IC48: initial interface reaction is dominated by sampled-field rounding

Status: OPEN. Initial-slice numerical diagnosis only.

IC47's initial reaction is 6.12149e-6 at seven nodes and -9.12001e-6
at nine nodes. Replacing only canonical-field derivatives by analytic
derivatives of the same stored initial Taylor polynomials gives respectively
-8.16339e-12 and -2.54711e-10. All auxiliary constraints, boundaries,
Jacobian increments and acceptance tolerances remain those of IC47.

An independent 70-digit barycentric differentiation calculation isolates the
input rounding mechanism. For Q on the active patch, the second-derivative
error is 5.75658e-6 (seven nodes) or 9.05289e-6 (nine nodes) when input samples
have already been rounded to float64. Evaluating the same float64 polynomial
coefficients at 70 digits before differentiation reduces these errors to
5.87557e-18 and 8.53060e-19. This comparison holds the polynomial and nodes
fixed. It does not recover uncertainty already present in the coefficients.

Thus higher precision in differentiation alone cannot recover information
lost in storing nearly constant canonical fields on the narrow patch.
The observed initial reaction is not evidence for a physical interface
source. This does not explain or certify all finite-time interface residuals.

Next implementation: evolve canonical deviations from the known initial
polynomials, differentiating the polynomial background analytically and the
deviations numerically. This is an algebraic change of variables, not an
interface projection. Re-run the time/spatial refinements afterward. The
initial-derivative oracle in IC48 must never be used on unknown evolved data.

## Reproduction

From repository root:

```
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic48_initial_derivative_control.py > /tmp/ic48_results.json
```

Exit status 0. Output preserved as `ic48_results.json`. Four initial solves
compare two resolutions and two derivative prescriptions; the high-precision
sampling calculation is repeated alongside each. No time evolution or full
theory certification is performed. No empirical data are tested here.

The action, initial-data and symbolic dependencies are inherited from IC46
and IC47; this is not a self-contained dependency archive. Mathbox's bounded
computation-audit distinction is maintained: a diagnosed numerical error
does not prove the target relativistic theory exists.
