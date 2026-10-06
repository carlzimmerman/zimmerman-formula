# Frozen authoritative bounded evidence

`REPORT.md` SHA-256 `11d8f8feeb130813ef20c7c1fd76b9f5c18eaa495e93406cd62b9a9a1edc3022`.

`growth.py` SHA-256 `3d5934f3e00344f47e6dc6dd042c84f9fb92ddec084c53cf3e0fbcbe83b62367`.

`checks.py` SHA-256 `5fc84c57407c190be463bdfa5a6c88051c421644a03619788a22c2c9534793ee`.

`contract.json` SHA-256 `c307c0495e1af81f9425af8c547dc4ed8f859622755b7c19de2ff063fbfcd727`.

- `control_drop_trace_a`: 43/55; manifest validator exit 0; failures: constraint_propagation_derivative_100, actual_geometric_Ricci_constraint_100, Hamiltonian_preserved_100_phase_DOP853, Hamiltonian_preserved_100_phase_Radau, Hamiltonian_preserved_100_dust_DOP853, Hamiltonian_preserved_100_dust_Radau, constraint_propagation_derivative_1000, actual_geometric_Ricci_constraint_1000, Hamiltonian_preserved_1000_phase_DOP853, Hamiltonian_preserved_1000_phase_Radau, Hamiltonian_preserved_1000_dust_DOP853, Hamiltonian_preserved_1000_dust_Radau.
- `control_dust_only_a`: 47/55; manifest validator exit 0; failures: initial_actual_Hamiltonian_100_phase, phase_changes_W_at_equal_dust_100, Hamiltonian_preserved_100_phase_DOP853, Hamiltonian_preserved_100_phase_Radau, initial_actual_Hamiltonian_1000_phase, phase_changes_W_at_equal_dust_1000, Hamiltonian_preserved_1000_phase_DOP853, Hamiltonian_preserved_1000_phase_Radau.
- `main_a`: 55/55; manifest validator exit 0; failures: none.

Main maximum sampled relative Hamiltonian residual: 7.1525145e-07; maximum common-vector independent-solver discrepancy: 2.685359e-08; maximum nfev: 14275. These are bounded sampled checks, not continuum error bounds.

The dust-only mutation actually sets the phase-seed potential to zero and recomputes the true initial/action constraints. The trace mutation actually removes the local Ricci perturbation from KG and recomputes the resulting geometric/constraint equations; it preserves charge transport but loses Einstein compatibility. Their failures are intended. All three current manifests validate against unchanged inputs. No historical parent trajectory or Claude script was rerun or modified.

Historical development `preflight/results.json` has53 checks before two geometric-Ricci assertions were added; its old script revision was not separately archived and it is not current evidence. `preflight_b/results.json` has55 current checks. The authoritative standard main/controls use frozen55-check code and capture input hashes before/after execution.
