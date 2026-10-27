# Validation and reproduction

26 local provenance manifests validated:24 completed executions and two preserved
failures. See manifest_validation.json. Completion is not physical acceptance;
ideal-boundary results are rejected and nuclear convergence remains unresolved.

The authoritative aggregate is run_audit_v2/results.json. The previous run_audit
failed during JSON serialization and contains no completed result. The initial
run_preflight failed before computation due to missing PYTHONPATH, then the
unchanged script completed as run_preflight_env.

Environment: Python3.9.6, NumPy1.26.2, SciPy1.11.4, PySCF2.11.0 in
/private/tmp/two-electron-pyscf, mpmath1.3.0. Use OPENBLAS_NUM_THREADS=1 and
PYTHONDONTWRITEBYTECODE=1. Nuclear scripts use one thread. The inherited UKRmol
point driver uses two OpenMP threads, and its new runner requests two. The warning
that this PySCF build lacks OpenMP is retained; setting lib.num_threads does not
magically add it. External source hashes/build instructions are in ../continuum.

Quick audit repeat from repository root, preserving recorded outputs:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/two-electron-pyscf \
OPENBLAS_NUM_THREADS=1 python3 \
  two_state_mechanism_2026_10_26/nuclear_flux/audit_v2.py \
  --output /private/tmp/nuclear-flux-audit-repeat.json
```

The independent tests can likewise be rerun with checks.py and a new output path.
They cover independent CI eigenvalues, analytic discrete scattering, closed lead
channels, electronic signs, coupled lead flux/reciprocity/cut invariance, exact
branch-event conservation, thermal Einstein balance and streamed-versus-stored
propagation. These do not validate a physical DR cross section.

For new streamed nuclear runs:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/two-electron-pyscf \
OPENBLAS_NUM_THREADS=1 python3 \
  two_state_mechanism_2026_10_26/nuclear_flux/launch_stream.py \
  NEW_LABEL rydberg3 .025 30
```

Use a new label, never reuse a completed output. launch_stream.py writes the
bounded contract before executing. Other exact commands are in run manifests.
The code and configuration are the reproducible source; there is no hidden
astrophysical rate fit or galaxy selector.

## Large local artifacts

The initial saved-grid runs produced about493MiB of grid.npz arrays. These files
remain in the local workspace and are deliberately excluded from Git. Exact
paths, sizes, hashes and regeneration commands are in LOCAL_ARTIFACTS.json.
Their compact results, manifests, input scripts and commands ARE committed.
A clean clone cannot validate a grid-dependent manifest until it regenerates the
missing grid. Do not describe the remote checkout as containing these arrays or
as passing those full hash checks without regeneration.

Later streamed runs avoid this storage requirement and reproduce the stored-grid
solver to1.5e−12 in the tested case. The compact aggregate audit depends on committed
results and small electronic kernels, so it does not require the large grids.
Electronic source CI files and kernel.npz outputs are committed. Any absent
temporary UKRmol binary must be rebuilt/authenticated using ../continuum/BUILD.md.

Figure output is regenerated from archived audited values and visually checked.
