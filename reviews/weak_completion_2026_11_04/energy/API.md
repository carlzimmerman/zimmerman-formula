# Matched energy update API

The frozen reference implementation is `split_energy_v7.py`, SHA256
`d2079fafa099f2b2e1b7274f4549856c45e166a8444720b9297f89a7a513cd56`.
Its population solver closure is `hybrid_number_v4.py` and
`seeded_number_v3.py`, plus the exact prior sources listed in every run
manifest. Import with this directory on `sys.path`:

```python
from split_energy_v7 import step, QuantumState
newstate, Jnew, neworbit, work, diagnostics = step(
    model, background, operator_factory, N, state, J, dN,
    geometry='midpoint', population='BE', max_outer=8, outer_tol=2e-5,
)
```

`state` retains physical numbers and independent fermion vacancies. Its
`numbers()` returns flattened Y=gWf/(2pi²), species-major. No accepted
population is clipped. Exactly empty old species may have a positive Newton
guess, which is not an initial population or source.

`operator_factory(background, xs, weights, temperature, q, W)` returns a
physical-number operator: `number_rhs(f, availability)`, sparse
`number_jacobian(f, availability)` with respect to Y, `number_gross`,
`measure`, `eta`, `energy`, `energy_average`, `local_events`, and
`phase_weights`. Each local operator exposes its energy and RHS protocol.
Bosons have eta=+1, fermions -1. The factory is rebuilt on the actual
midpoint-action/population orbit. The method has no fixed species count.

The model supplies `orbit(N,Y,J=...)` or `orbit(N,Y,E=...)`, `hubble(N)`,
`q`, `W`, `measure`, and `eta`; orbit dictionaries retain E, J, minimum,
omega, xs, weights, kin2, gas rho/pressure and physical energy arrays.
The temperature convention is T0 exp(-N), T0=.004657258204883617 in mu
units. A different convention needs a versioned extension, not a silent
change. The 30-group `CommonOrbit` supplied by the coordinator preserves
bosonic vector eta and satisfies this interface.

Returned `work` is the independently Simpson-integrated FRW work of the two
expansion subflows. `diagnostics` separately exposes expansion energy/work
defects, collision endpoint energy, physical-number residual, entropy,
quantum bounds and outer fixed-point changes. The caller accumulates work
from the fresh initial state without resetting its reference.

BE is the promoted population scheme. `population='midpoint'` activates the
separate arithmetic f/availability midpoint diagnostic. It is conditionally
positive and not L-stable: reject failed endpoints and reduce the step.
No successful midpoint history is implied by this API.

The inherited harmonic geometry branch below J_initial*1e-7 is an
approximation without an action floor. It is not used in the completed
fresh warm benchmarks. Cold excitation needs the separately validated
offset oracle and state/time convergence.
