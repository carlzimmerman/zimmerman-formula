# FSP-008 reproduction and interpretation

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. Use fresh output paths; do not overwrite a completed author's result or change a declared input merely to make an old manifest validate.

- [Proton commands](proton_kernel/REPRODUCE.md) document both the full Born/point-Dirac kernel and its separate dimensional MSbar matching. Their current records are [kernel run001](proton_kernel/run_001/manifest.json) and [matching run001](proton_kernel/msbar_run_001/manifest.json). The elementary theory's matching does not reproduce full QCD.
- [Sphere commands](sphere_chiral/REPRODUCE.md) document the global pion determinant, spectral and heat quadratures, charge and metric derivatives. The current [sphere run001](sphere_chiral/run_001/manifest.json) uses its declared positive-mass/curvature domain. It does not simulate a QCD ensemble or the massless nonlinear chiral integral.
- [Sea flavor contract](sea_flavor/COMPUTATION_CONTRACT.json), [script](sea_flavor/check_flavor.py) and [run001](sea_flavor/run_001/manifest.json) record the exact finite-matrix source-Hessian benchmark. This tests algebra, contacts, cumulants and estimator bias, not actual QCD gauge fluctuations. The physical variance bound has no assigned numerical value.
- [Coordinator contract](coordinator/contract.json), [script](coordinator/check_global.py) and [run001](coordinator/run_001/manifest.json) check exact source-to-stress, group-trace and RG conversions and scalar heat coefficients. The script takes one fresh result-file argument. Its declared inputs are the script, UV_SPHERE.md and SOURCES.json; use the installed bounded runner with those inputs and a fresh run directory.

All declared mathbox-v2 manifests can be validated with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The wall model's independent contract and actual execution are in global_state/. Reviewer-owned source-first derivations and checks are in reviews/. Their provenance and physical scope are distinct from the authors' bounded runs. Source cache paths and byte hashes are recorded; temporary files may need reacquisition, while retained primary PDFs are ordinary programme artifacts.

The [matched compact continuation](chiral_zero_mode/REPRODUCE.md) records its new mixed-pion checks and subtraction rather than re-executing inherited base-integral grids. The [photon derivation](epsilon_photon/DERIVATION.md) and local contract define a distinct nonconstant-photon run; its orientation ratio omits absolute source-only normalization and is not a full NLO vacuum energy. The [elastic data derivation](proton_elastic_data/DERIVATION.md), source-TeX table, local contract and actual run001 define the finite nineteen-point trapezoid exactly. Reproducing its many arithmetic digits does not improve the precision of the published lattice data or bound the continuum quadrature error.

Validation establishes recorded execution and content freshness. It does not authenticate an external physics premise, prove a numerical quadrature tolerance as an interval bound, compute unprovided lattice data, or establish a nonperturbative radius limit. Source discrepancies and any reviewer/author corrections are reconciled separately without rewriting executed evidence.
