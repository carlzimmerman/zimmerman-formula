# Research findings through preparation and joint microscopic bounds

Start here for the current status. The original top-level README describes the
initial spherical prototype; later stages below supersede its scope.

**No successful microscopic explanation of disk tethering, dwarf/cluster free
mass retention, and the galaxy acceleration relation has been established.**
This archive contains derivations, bounded tests, useful negative results,
conservation checks and explicitly documented limitations.

## Latest findings

| Stage | Finding | Scope / unresolved issue |
|---|---|---|
| [State preparation and joint bounds](state_preparation_2026_10_25/README.md) | A controlled gapped thermal start reaches the target source remainder within0.4%; contact interaction feedback and autonomous live-field dynamics tested. Combining current, inventory and Fermi packing rejects the local fundamental-fermion interpretation under explicit hypotheses. | No autonomous formation or population separation. Emergent quasiparticles remain open but need a different physical mass/current mapping and electric operator. |
| [Nodal medium](nodal_medium_2026_10_25/README.md) | An explicit effective nodal-ring band yields the cold critical response; a slow unitary field ramp preserves the small source remainder to 2.23% in the refined test. | Initial band and filling assumed; no microscopic assembly, live-gravity population separation or derived acceleration scale. Finite temperature and filling remain obstacles. |
| [Decisive checks](decisive_checks_2026_10_25/README.md) | Finite-temperature response and conditional mass/response bounds derived; simple contact and degeneracy selectors tested. | Constraints apply to stated realizations, not all quantum media; no full population mechanism established. |
| [Rotating state](rotating_state/README.md) | Rotation and explicit matter-wave energy transport implemented; equal-state equal-mass carriers stay neutral exactly. Unequal masses produce electric support with and without rotation. | No disk-specific capture; static baryons, periodic boundaries, incomplete spatial convergence and no common-mass four-system resolved comparison. |
| [Quantum medium](quantum_medium/README.md) | Derived a two-component Bose mean-field dipole spectrum with a physical quantum Jeans scale, explicit mass and oscillator-strength checks. | Coherent state assumed; mean-field approximation; stability ordering does not select disks over both dwarfs and clusters. |
| [Microscopic medium](microscopic_medium/README.md) | Ground-state Coulomb pairs have a finite dipole gap; the simple acoustic mode is electrically dark. Explicit moving countercharges and their gravity tested. | No critical dipole spectrum; classical homology prevents mass-size separation; some long trajectories unresolved. |
| [Causal collective response](causal_collective/README.md) | A conditional critical-spectrum ansatz approximates the target static law and admits a causal local field response. | Spectrum not microscopically derived; medium mass, preparation and response-time constraints prevent interpreting the fit as a galaxy model. |
| [Countercharge action](countercharge_action/README.md) | Explicit charge accounting exposes screening, transport and causality constraints. | The original nonlinear action is not a viable causal completion. |
| [Microscopic capture](microscopic_capture/README.md) | Atomic binding and reversible rates constrain a common microscopic model. | No tested common parameter choice meets the desired population separation. |
| [Adaptive kinetic capture](adaptive_kinetic/README.md) | Local capture with separate transported populations and live gravity tested. | Sparse capture and resolution limits do not establish robust formation. |

Earlier spherical, assembly, vorticity, local-capture and full-3D stages are
retained in their original directories with per-stage READMEs and handoffs.
Energy conservation checks do not establish physical realism, population
separation, continuum convergence or observational agreement. Electric support,
neutral pairs, quantum Jeans instability and charged tethering are distinct
observables; they must not be relabeled as each other.

## Latest verification

The state-preparation stage has seven completed runs and one retained failed
invocation (output-path typo). All eight provenance records validate; only the
completed records supply numerical findings. See its [validation](state_preparation_2026_10_25/VALIDATION.json)
and [audit](state_preparation_2026_10_25/AUDIT.md).

At the preceding checkpoint, all five new manifests in decisive_checks_2026_10_25 and nodal_medium_2026_10_25
validate against their current inputs. Fresh validator output is in
[LATEST_VALIDATION.json](LATEST_VALIDATION.json). This validates provenance,
not the physical interpretation.

## Earlier archive verification

At the preceding archive checkpoint, validation checked all 90 then-recorded manifests against the current source:
79 completed records validated; 11 historical records did not. All 12 unit tests
across microscopic_capture, countercharge_action and causal_collective passed.
The latest successful microscopic-medium, quantum-medium and rotating-state
records all validate. Full validator output is in
[PUBLISH_VALIDATION.json](PUBLISH_VALIDATION.json).

Historical failed/stale records below are retained for transparency and must
not be used as current validated evidence. A completed status by itself does
not repair a source-hash mismatch. Interrupted folders without manifests also
remain historical only; consult each stage's audit before using its outputs.

- `microscopic_medium/run_transport/manifest.json` — recorded run status `failed`, current validation failed.
- `run_dynamics/manifest.json` — recorded run status `completed`, current validation failed.
- `run_static/manifest.json` — recorded run status `completed`, current validation failed.
- `vorticity_gate/run_probe128_final/manifest.json` — recorded run status `failed`, current validation failed.
- `vorticity_gate/run_probe256_final/manifest.json` — recorded run status `failed`, current validation failed.
- `vorticity_gate/run_probe64_final/manifest.json` — recorded run status `failed`, current validation failed.
- `vorticity_gate/run_scan/manifest.json` — recorded run status `failed`, current validation failed.
- `vorticity_gate/run_scan_v1/manifest.json` — recorded run status `failed`, current validation failed.
- `vorticity_gate/run_scan_v2/manifest.json` — recorded run status `failed`, current validation failed.
- `vorticity_gate/run_spectrum/manifest.json` — recorded run status `completed`, current validation failed.
- `vorticity_gate/run_spectrum_final/manifest.json` — recorded run status `completed`, current validation failed.

## Reproduction and portability

Each stage retains scripts, explicit numerical bounds, contracts, raw results
and manifest hashes. The manifests record the original machine's absolute
paths and software versions; use the relative source paths from a repository
checkout and install the documented dependencies when rerunning elsewhere.
The mathbox bounded-runner/validator is an external tool, not vendored here.
Individual scripts provide their command-line entry points; per-stage READMEs
specify limitations and reproduction details. Keep historical inputs immutable
or create a new run with a new manifest when revising an experiment.

This commit publishes research code and evidence, not a claim of a validated
new physical theory. Unrelated workspace files and pre-existing local commits
are excluded from this research branch.
