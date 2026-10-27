# Reciprocal field continuation checkpoint

RF-2026-10-22-1, base 581d52210bced1231c2517b1d894221edd171f40. Owner/write scope: this chat / this directory. Original goal remains open. No large/external/background job was started; no .mathbox ledger is present. Predecessor PC-2026-10-22-1 remains unchanged. Check other active work before starting a new overlapping route.

Read RESULT.md, AUDIT.md and STIFFNESS_EXTENSION.md. The current strongest results are the complete reciprocal circular-force formulas, the repaired density-independent transverse speed, and the conditional first-zero bound R_positive_e<=pi ell0, including positive P stiffness. Exact inputs/hashes are in manifests and CHECKPOINT_SHA256.json.

## Route status

- Constant-g field: homogeneous stable transverse block, but its high-k speed diverges as baryon density tends to zero. Do not promote it to a universal parent.
- g0 sqrt(rho_b) field: repairs that principal-speed dependence and has an explicitly varied baryonic density force. Still open as a reduced candidate. Exact-vacuum regularity and all-background dynamics unproved.
- Passive spherical extended surplus: fails to provide a large positive-surplus region while retaining the declared growth response. This restriction survives positive P gradient energy and a range of growth-tolerance diagnostics.
- Compact surplus lensing: open, not excluded by the radius bound; no predicted amplitude or exterior matching.
- Dwarf-scale surplus: open, no mass or retention selected.
- Driven/turbulent/nonequilibrium cluster phase: untried, not a consequence of the mean-vorticity-zero model. A stochastic or kinetic source must be derived with backreaction, not assigned by object class.

## Next discriminators, without repeating the failed construction

1. If pursuing the compact surplus, solve one global spherical boundary-value problem with prescribed total cold inventory and physical exterior. Check rho_c>=0 outside the first zero as well as inside. Then compute both dynamical mass and projected lensing at MID and OUTER radii. Do not fit an independent mass per system or use the zero of e as an arbitrary truncation surface.
2. If pursuing a driven extended cluster phase, first specify its source from a baryonic kinetic or fluid stress/current action. Mean-zero turbulent vorticity is not zero mean-square vorticity; a stochastic source is not automatically a coherent X field. Derive averaging, energy input and reciprocal heating/drag. A source or boundary that lowers chi below chi0 changes a named hypothesis of the radius theorem and requires its own checks.
3. For rotating systems, solve the actual varying-chi/finite-DX disc equations. Use the general material force, not the local constant-chi formula beyond its regime. Freeze one coupling choice from independent physics or explicitly classify it as a fit before using SPARC. Check the same choice on scalar growth and the passive branch.
4. A covariant clock/reference-density completion and full constraint analysis remain required. The current weak-field tests neither supply nor certify one. Finite P inertia requires a real expanding-background reduction before numerical cosmology claims.

No parameter-free common prediction is available: g0, phase stiffness, field inertias, spatial coefficients, inventory and initial state are inputs. Unknown inputs cannot be replaced by per-dwarf or per-cluster target profiles. Existing formation E/J/charge and retention requirements still apply.

## Reproduce and validate

From repository root:

    OMP_NUM_THREADS=1 python3 sol61_push/reciprocal_field_2026_10_22/checks.py --output /tmp/rf_checks.json
    OMP_NUM_THREADS=1 python3 sol61_push/reciprocal_field_2026_10_22/density_checks.py --output /tmp/rf_density.json
    OMP_NUM_THREADS=1 python3 sol61_push/reciprocal_field_2026_10_22/stiffness_checks.py --output /tmp/rf_stiffness.json
    OMP_NUM_THREADS=1 python3 sol61_push/reciprocal_field_2026_10_22/tradeoff.py --output /tmp/rf_tradeoff.json

First three accept --mutate, expected exit 1; tradeoff has solver-repeat/dust-family controls rather than a separate mutation. Current supporting runs: run2, density_run2, stiffness_run, tradeoff_run. Expected failed controls: mutation, density_mutation2, stiffness_mutation. Older run/density_run/density_mutation are retained historical artifacts with superseded script hashes. Do not report them as current-source validated evidence.

Each runner invocation records argv, hashes, versions, dirty state and outputs. Limits were 60 seconds wall, 55 seconds CPU, numerical-library threads set to one; no memory hard cap. No network use, installation, commit or push. Current results are self-reviewed, not independently certified. Open routes are deferred, not exhausted or disproved by the scope of this checkpoint.
