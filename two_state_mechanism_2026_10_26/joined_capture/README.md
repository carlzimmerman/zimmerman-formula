# Capture/nuclear join: a validated map and a limited nonlocal benchmark

**Physical dissociation rates and galaxy separation remain unresolved.**
This stage follows research commit f1a0e9f1a10a94d614db1dc246853da739e1b7ba.

Material progress:

- Decoded the signed 42-state Q configurations at R=2,3,4. Independent Hamiltonian
  matrix agreement is better than 2.74e-9; exact embedding into 130/192-state
  nuclear bases has isometry residual below 1.24e-12. The transferred electronic
  source and escape kernel preserve their optical identity. See `run_map`.
- Added a fourth-order Hermitian radial stencil and fixed a varying inner-boundary
  artifact. For the 130-state basis, E=-.60, wall=.2, outer R=30, transition
  probability changes from 1.0776724e-6 (h=.05), to 1.0860377e-6 (.025), to
  1.0871662e-6 (.0125). The last change is about 0.104%. Moving the wall .1 to
  .05 changes it only about 0.025%, but moving the exterior 30 to 40 still changes
  the wall=.2 result about 2.6%. These are **neutral transitions, not DR**.
- Electronic-basis convergence is still poor: 130 to 192 states at h=.025 changes
  that neutral transition from 1.0860e-6 to 6.0993e-6. Results at two other
  energies are in the audit table. The 266-state result is 6.9795e-6, another
  14.4% change; at E=-.58 that refinement changes the probability by 72%.
- Computed ionic BO vibrational thresholds at mass ratio 100. At incident .001,
  only one bound vibrational channel is open; at .05, two are open. At .199 the
  ionic dissociation continuum opens and cannot be dropped.
- Built a Feshbach source/escape solver and joined the actual R=2 electronic
  Hamiltonian to four ionic nuclear modes in an explicitly **frozen-electronic
  benchmark**. Open-channel optical residuals are below 2.65e-15. The benchmark
  retains real shifts and closed electron channels, but has no nuclear product
  continuum: it is not a DR calculation. A local width replacement fails this
  benchmark. See `DERIVATION.md` and `run_nonlocal_v2`.
- Independent full-inverse/Schur, free-dispersion, flux, charge and event-energy
  checks pass. Photon ledger energy residual is 1.4e-17 for the tested events;
  no physical-rate photon trajectory is implied.

## Reproduce

Use Python3.9+, NumPy, SciPy, mpmath and PySCF; the recorded environment used
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/two-electron-pyscf
OPENBLAS_NUM_THREADS=1`. The external mathbox runner path is recorded in launchers.
The project-root commands and all input hashes are in each manifest. Example:

`python3 two_state_mechanism_2026_10_26/joined_capture/launch_wall.py NEW_LABEL run_fourth_wall.py --basis rydberg2 --h .025`

Launchers require a new label/output directory. Do not overwrite pinned files.
All new data files are small enough to publish. Previous-stage compact electronic
inputs are needed; no old large nuclear `grid.npz` file is required.

## Interpretation warnings

Original `run_fourth_*` data used a changing inner endpoint: retain as debugging
evidence, not a clean grid-convergence test. Use `run_wall_*` and the explicit
inner/outer/basis checks. Original `run_nonlocal` reports relative error 1 for
closed zero-width blocks because it divides roundoff by roundoff; this is a
reporting error, not physical loss. Version2 uses absolute closed-channel error.
All conservation checks concern the stated finite operators or specified events.
They do not certify complete physical reaction rates.

All19 new manifests validate against current inputs; see `manifest_validation.json`.
The aggregate result hashes auxiliary arrays and summarizes the finite evidence.
