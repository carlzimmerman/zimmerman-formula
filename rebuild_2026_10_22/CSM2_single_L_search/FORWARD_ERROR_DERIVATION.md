# Source operation graph

The installed gradient computes three coefficient-weighted mass values and two
sums, then source divides by radius. Its coefficient preparation takes at most
four basic operations along a path. Fixed log steps and their differences obey
Sterbenz exact subtraction when the checked ratios lie within[1/2,2]. All
nonzero preparation results must be normal. Edge gradient uses one mass
difference and two divisions. Source and version-matched implementation are
retained in source_audit_numpy_1_26_4/.

The official real interpolation implementation forms a difference quotient,
multiplies by the fixed query offset and adds the left value, with exact-knot
and exterior copies. Its ideal absolute path is G0+alpha*(G0+G1), where
alpha=(query-x0)/(x1-x0). For underflow injections the same graph gives
V=((V0+V1+1)/dx+1)*offset+1+V0+1. Direct mass interpolation takes input V=0.
No-NaN fallback requires the proved finite intermediate bounds.

Each projection integral multiplies f by fixed primitive factors and sums2401
terms, then divides by fixed positive radius/pi factors. Track products,
quotients, additions and final subtraction with the same positive path rules.
Coefficient preparation/normal rounding is absorbed into gamma_N. For each
mass-dependent path N=2*2401+128 is larger than the source graph's reduction
and scalar-operation count; changing reduction order cannot exceed this count.
Relative perturbations compose to gamma_N. Absolute underflow injections,
propagated by V, are amplified by at most1/(1-Nu). This yields the frozen E.

U is a positive linear functional of coordinatewise mass absolute values.
Thus sum_j w_j U(M_j) <= U(sum_j w_j mass_envelope_j), w_j>=0. V is independent
of M and is multiplied by the group's total weight. This avoids a loose global
mass maximum without selecting or tuning any error allowance after scoring.

This is an implementation-model forward-error bound. It assumes the reviewed
NumPy algorithm/basic-operation semantics, fixed deterministic primitives and
covered mass inputs. It does not certify transcendental primitive evaluations
as real mathematical functions, nonlinear mass construction, column/branch/
continuum coverage, or original catalogue stacking roundoff. Those remaining
obligations must be stated separately from a real-L/full-model exclusion.
