# Spatial conversion checkpoint

Status: mechanism OPEN; conditional spatial transport established in finite simulations.
Publication parent: `6139426df70e868f02c0ee2faa8cba9e3ba902f1`.
Run repository state: `{'commit': '8c713f68d86a1bf907e0edd6c2c60a4156d66c3e', 'dirty': True}`.

Executed: five physical/dimensionless cases at three resolutions each; two Lean algebraic results and two damaged controls; optical mass-budget calculation at three masses and two cutoff ratios. No joint photon/gravity simulation or empirical discovery.

The MeV/5 eV example with density 1000 kg/m^3 gives microscopic acceleration about 6.31e-17 m/s^2. The hypothetical portal benchmark zeta=1, Lambda=10M gives about 1.08e-29 visible watts per kilogram of MeV sources. These are conditional scale calculations, not universal no-go results.

- `INPUT_CARRIER_ACTION.tex`: `f1046138aaa7f03f1fd3ee44b4c0cad8768e73b879fc2154296791010c6929f3`
- `run/manifest.json`: `3d11f999fb789e381d3e4c98ce363caff2a8ddaa629b2ada0243e3438e0ff9bc`
- `lean_run/manifest.json`: `49ae6ec5879234f95d06d0a430c8d2ff2cdef2a66a29bad2f8310693d84ca4ba`
- `optical_run_v2/manifest.json`: `a8344358d1c9875a26dbba1b1610d1d32f03490091803a509136bc0d9c984178`

Failure retained: optical_run ended at NumPy-boolean JSON serialization; exact old script preserved in optical_budget_failed_snapshot.py. optical_run_v2 is the successful replacement.

Next microscopic obligation: derive a resonant phi phi -> chi -> phi phi gamma gamma collision kernel, with detailed balance, photon escape and validity regime. Do not substitute arbitrary cooling into a fluid model. Finite geometry and a force observable are also pending. Self-review only; see REPORT.md for scope.
