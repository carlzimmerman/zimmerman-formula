# Original projection evaluation: implementation-model bound

source_forward_001 completes in24seconds. The derived positive operation-path
bound uses4930 operations, unit-roundoff majorant2^-50, and absolute
underflow allowance2^-1022. Profile-aware envelopes avoid a loose global mass
maximum by exact positive linear aggregation. The maximum projected native
error is1.534657376e-7. These constants come from the inspected operation graph
and binary64 arithmetic, not adjustment to the score.

All11 run controls pass, including240 full-envelope/alternating stress cases
and a1% mutation. The exact-rational recomposition has8 controls; an additional
4 checks verify the actual nonuniform-gradient branch, normal fixed preparation
and roundoff premise. It uses the larger of each independently derived error
upper and the recorded upper. Their maximum relative difference is3.85e-16.
The resulting exact conditional dual lower is569.5338648476735, above the
unchanged feasible-law upper+9 of163.34346325076024.

The operation model was checked against installed NumPy gradient and the
[official version-matched interpolation source](https://github.com/numpy/numpy/blob/v1.26.4/numpy/core/src/multiarray/compiled_base.c).
The cached source, installed gradient text, provenance and NumPy redistribution
license are under source_audit_numpy_1_26_4/. This is not an independent
attestation of the installed C binary's build. The bound assumes those reviewed
implementations and standard binary64 basic-operation semantics, with fixed
primitive values and covered mass arrays. The intermediate majorants also
exclude overflow for each registered input, using the minimum positive
inventory weight to turn aggregate path bounds into individual bounds.

This treats projection floating evaluation, not all model evaluation. Nonlinear
mass construction, original catalogue interpolation/stacking roundoff and
column/branch/continuum coverage remain. Fixed deterministic primitives are
not analytic-transcendental certificates at arbitrary real arguments. There
is still no real-L/global obstruction or passing model witness. Remaining
work should target these mass/stack/domain obligations, not rerun completed
projection benchmarks or introduce fitted physical tolerances.

Native monitor: all five published seeds remain unchanged. The four pending
seeds2,4,5,6 have recent rolling checkpoints; no native jobs were changed.
