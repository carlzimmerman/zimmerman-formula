# Resonant cooling checkpoint

Status: full mechanism OPEN; dilute collision rates and asymptotic regimes derived.
Publication parent: `8286c5061b4821d71f2c4ba298a2312e8c337c11`.
Run repository record: `{'commit': 'ce642f4f2d44162f26f4cfdf03d83fe707b9356b', 'dirty': True}`.

New result: photons can be emitted at source formation as well as decay. Their two narrow-pole cooling contributions were derived and evaluated. Deep off-shell scattering has a power-law cooling tail; both tree attachments add coherently in that limit. The general two-diagram thermal integral is still pending.

Evidence: 40 finite numerical checks, three Lean algebraic bottleneck statements, two rejected damaged controls. Analytical matrix-element normalization is self-reviewed, not Lean-certified or independently agent-reviewed.

- `INPUT_RADIATIVE_REPORT.md`: `e54ba50e87553d24411f56da0dc6d9460c7b4ca5a44862e95bf38b6747c65992`
- `run/manifest.json`: `7c0ed5aa3bb6d6df26c51022fc29e505cd71d7c67f5f627165dafba64483529e`
- `lean_run/manifest.json`: `6742d59be2d2f8a243e4bd8838880410e22dc8660ee3b678f7c01785cc5cea44`

Benchmarks: with gap=T=5 eV, zeta=1, Lambda=10M and dilute occupation eta=1e-4, optimistic two-pole cooling remains slower than the gravitational timescale. These are conditional examples, not an exclusion of arbitrary couplings or dense coherent states.

Next obligation: a conserving high-occupation collision/field description including Bose factors, coherence, dephasing and photon escape. Do not extrapolate classical n-squared rates into a condensate. Full two-diagram thermal integration would refine the dilute transition regime, but does not close the dense-state or force-observable gaps. See REPORT.md for all assumptions and formulas.
