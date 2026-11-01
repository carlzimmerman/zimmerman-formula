# Direct finite canonical energy check: all six frozen witnesses lower energy

**Outcome:** conditional on numerical tolerance and the specified PN28 static
model, the finite assertion is verified for all six pre-existing kinetic
witnesses. Small admissible canonical deformations in both signs decrease
the complete configuration energy. This independently confirms an accessible
energy saddle in each case. It does **not** establish exponentially growing
kinetic modes or a full nonlinear vacuum-crossing theory.

This check was independently implemented by `/root/core_gap_check` after the
coordinator supplied the already optimized witnesses. No vector, parameter,
physical closure or pass threshold was fitted or changed by this check.

## Frozen assertion and actual deformation

`canonical_energy_contract.json` was written before execution. The six inputs
are the last, 12-component vector in the refined evaluation of each case in
`kinetic_run_002/result.json`: `psi_c={0.8,0.95,0.99}` crossed with
`epsilon={0.0001,0.01}`. The static source is the same frozen PN28 code. The
scalar response is independently solved for each supplied displacement, with
tolerance `3e-8`, without optimizing the displacement again.

The radial material map and canonical momentum map are

```text
r_t = r+t xi(r),
a = 1+t xi'(r),         b = 1+t xi(r)/r,
p_t = J^(-T) p_0,       eigenvalues(J)=(a,b,b).
```

The scalar uses the independent Eulerian path
`s_t(x)=s_0(x)+t sigma(x)` on the fixed scalar domain. Positive stretches
make the matter map one-to-one, preserve radial ordering, and preserve every
finite phase-space Casimir under its canonical lift. The occupied phase-space
volume and total matter mass therefore remain fixed exactly. The map can be
smoothly continued through the empty exterior; its values there do not enter
the matter energy. All tested deformed matter edges remain inside the scalar
domain.

In units `4 pi B ell^3`, the directly evaluated energy is

```text
E_rel(t) = integral_0^R E_rel,0(r)
  exp{-2[s_0(r_t)+t sigma(r_t)-s_0(r)]}
  [a^(-2)+2b^(-2)]/3 r^2 dr,

E_U(t) = integral_0^L {exp[3(s_0+t sigma)]-3(s_0+t sigma)-1} r^2 dr,

E_grad(t) = (3epsilon/2) integral_0^L (s_0'+t sigma')^2 r^2 dr,

W(t) = -(5/2) integral_0^R m(r)n(r) r^2/r_t dr.
```

The asymptotic quadratic scalar tail adds
`(3epsilon/2)L^2[sqrt(3/epsilon)+1/L][s_0(L)+t sigma(L)]^2`.
It is the same static exterior approximation as in the Hessian. The domain
is already extended by the frozen background's refinement procedure; the
small background and perturbation tails remain an explicit numerical
approximation, not an exact nonlinear exterior solution.

The script accumulates `E(t)-E(0)` directly using `expm1` and exact rational
increments for the stretches and gravity. It avoids subtracting two large
total energies. The central second difference is
`[E(h)-E(0)+E(-h)-E(0)]/h^2`. The independent Hessian includes the obligatory
kinetic shear term derived in `THEORY_REVIEW.md`.

Four predeclared steps are `h={0.02,0.01,0.005,0.0025}/M`, where `M` is a
fixed, sampled bound on the displacement gradients, scalar amplitude and
distance to the outer boundary, with minimum value one. Both 512- and
1024-point quadratures separately integrate matter and scalar exterior.
The two smallest steps at each quadrature must lower energy in both signs,
match the independent quadratic curvature to relative tolerance `0.001`,
and pass the predeclared first-variation check.

## Results

The table reports the 1024-point quadratic curvature and direct energy
increments at the smallest step. Curvature normalization follows the supplied
frozen vector; it is not a claimed physical kinetic mode frequency.

| psi_c | epsilon | Independent Q | h | E(h)-E(0) | E(-h)-E(0) |
|---:|---:|---:|---:|---:|---:|
| 0.80 | 0.0001 | -0.01577394080 | 0.00250000 | -4.88869e-8 | -4.97010e-8 |
| 0.80 | 0.01 | -0.01482514138 | 0.00250000 | -4.59292e-8 | -4.67287e-8 |
| 0.95 | 0.0001 | -0.09161850704 | 0.000673155 | -2.07353e-8 | -2.07805e-8 |
| 0.95 | 0.01 | -0.09914846764 | 0.000927592 | -4.25918e-8 | -4.27182e-8 |
| 0.99 | 0.0001 | -0.08736959419 | 0.000395663 | -6.83434e-9 | -6.84329e-9 |
| 0.99 | 0.01 | -0.10905979485 | 0.000364318 | -7.23319e-9 | -7.24209e-9 |

All six cases pass every frozen control. Across the cases:

- Changing quadrature from 512 to 1024 changes `Q` by at most `6.64e-10`.
- The independently calculated `Q` differs from the original supplied-vector
  curvature by at most `6.64e-10`.
- The finest-step finite second difference differs from `Q` by at most
  `8.53e-6` relatively; the worst error over both required small steps and
  both quadratures is `3.25e-5`, below the frozen `0.001` threshold.
- The largest absolute independently calculated first variation is
  `2.09e-11`; every case passes the condition that its linear residual be
  less than `0.1 |Q| h_min`.
- All required positive- and negative-step energy increments are negative,
  with admissible positive stretches and an interior deformed matter edge.

The both-sign test matters: it prevents a small nonzero equilibrium residual
from masquerading as a negative curvature solely because one step happens to
move downhill.

## Provenance, scope and reproducibility

`canonical_energy_run_001/manifest.json` records `status: completed`, exit
status zero, and runtime **2.830303 seconds**. The run was limited to 180
seconds wall time, 150 seconds CPU, one numerical-library thread and 262144
log bytes. Input hashes match before and after execution. The installed v2
manifest validator reports a valid completed evidence record.

The script uses the frozen background source through `radial_stability_v2.py`
but independently constructs the combined displacement, solves its scalar
BVP, integrates the quadratic energy, and evaluates the finite configuration
energy. This is an orthogonal check of the witness energy, not a fully
independent derivation of the background profile or the PN28 parent action.

The authorized execution command was:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract field_response_2026_11_01/canonical_energy_contract.json \
  --input field_response_2026_11_01/canonical_energy_check.py \
  --input field_response_2026_11_01/radial_stability_v2.py \
  --input field_response_2026_11_01/inputs/check_gradient.py \
  --input field_response_2026_11_01/inputs/PARENT.md \
  --input field_response_2026_11_01/inputs/STATIC_GRADIENT.md \
  --input field_response_2026_11_01/kinetic_run_002/result.json \
  --output field_response_2026_11_01/canonical_energy_run_001 \
  --result field_response_2026_11_01/canonical_energy_run_001/result.json \
  --timeout 180 --max-output-bytes 262144 --max-cpu-seconds 150 \
  --max-threads 1 -- \
  python3 field_response_2026_11_01/canonical_energy_check.py \
  field_response_2026_11_01/canonical_energy_run_001/result.json
```

For repetition, replace all three occurrences of the output run directory
with the same fresh directory; do not overwrite this evidence. The supplied
kinetic input remains `kinetic_run_002/result.json`.

Validation command:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  field_response_2026_11_01/canonical_energy_run_001/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

No failed attempt or post-result threshold adjustment occurred in this check.
The calculations are floating-point evidence in six fixed cases, not
interval-certified inequalities or an all-parameter theorem. The remaining
decisive theoretical gap is the inference from an accessible negative-energy
direction to the full kinetic dynamical spectrum; this report makes no such
inference.
