# Finite computation and provenance

The authoritative control is `run_004/manifest.json`, runner schema v2,
status **completed**, with unchanged before/after script hash. Its root-aware
validator returned `valid evidence record (run status: completed)`.
This records execution and finite controls; physical or asymptotic
interpretations require the derivations and hypotheses in `LANDSCAPE.md`.

Observed HEAD: e54c33252909e38a529a69f7adac265e37b54cb4. The checkout was dirty
with concurrent unrelated work. Twelve parent/action/matching/source files
are byte-pinned in `source_pins.json`; the final check found none changed.
No inherited old hash was copied in place of hashing the current bytes.

Python 3.9.6, numpy 1.26.2, scipy 1.11.4; macOS arm64. Deterministic controls,
no random sampling. Caps: 45 seconds wall, 30 CPU seconds, 1 conventional
numerical-library thread, 1 MiB logs; no memory cap or affinity request.
The manifest records actual elapsed time and effective limits.

Exact executed command, from the project root:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract sol61_push/nonlinear_origin_2026_10_19/occupied_landscape/contract.json \
  --input sol61_push/nonlinear_origin_2026_10_19/occupied_landscape/check_landscape.py \
  --output sol61_push/nonlinear_origin_2026_10_19/occupied_landscape/run_004 \
  --result sol61_push/nonlinear_origin_2026_10_19/occupied_landscape/run_004/results.json \
  --timeout 45 --max-output-bytes 1048576 --max-cpu-seconds 30 --max-threads 1 \
  -- python3 sol61_push/nonlinear_origin_2026_10_19/occupied_landscape/check_landscape.py \
  --output sol61_push/nonlinear_origin_2026_10_19/occupied_landscape/run_004/results.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/nonlinear_origin_2026_10_19/occupied_landscape/run_004/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

To rerun, substitute a **fresh** output directory for run_004 in all three
output/result/program arguments; retain the same script and contract. Existing
scientific outputs must not be overwritten. The script now accepts its output
path as an argument, so no code edit is needed for reproduction.

Finite coverage and orthogonal checks:

- Sphere intersection: integrate independent perpendicular slices and compare
  with 5 pi/12; infer union 9 pi/4 and numerically integrate the pair intensity
  at n_b=.037. Pair-node fraction is .5925925925925928.
- Variable subsystem dipole: five x values .2,1,3,7,12; Lambert-W inversion,
  analytic Jacobian versus an independent centered finite difference, and an
  integrated first dipole-count moment. This is explicitly a subsystem
  diagnostic, not the complete source dictionary.
- Fixed binding WKB: seven separations12,20,50,100,200,500,1000, with actual
  turning points and fixed E_b=-.5 in declared units. Last secant slope
  .9972464396956247 approaches1. These quadratures are not an exact spectrum.
- Two-center LCAO: generalized two-by-two overlap eigenvalues at r/a_G=4,8,
  12,20; the stable closed splitting is also evaluated at40, where subtracting
  the full eigenvalues would lose precision. Its asymptotic ratio at40 is
  .9990625. Exact algebra in the trial subspace does not certify the exact
  two-center splitting or exact asymptotic prefactor.
- Complete source: compare a direct sum of scalar and two baryon source
  expectations with the compact recoil formula, then check four finite k
  values .02,.01,.005,.0025. The final k^2 coefficient relative error is
  6.939769064961965e-7. Affine source cancels algebraically and numerically.
- Contact bath: four energies .01,.003,.001,.0003; invert the full
  nongravitating Bogoliubov dispersion and independently integrate its angle
  factor. The E^5 coefficient relative error is1.8065784168630472e-6 at the
  last point. This checks a local stable-phonon approximation, not the
  self-gravitating infrared or finite-patch bath spectrum.
- Sector occupation: four V_LR values-.04,-.01,0,.03, with fixed J=.013,
  beta4.1, E_b=-.7, mu_Q=-.71. Direct four-state Fock diagonalization agrees
  with the trace fraction. Ground-sector inequalities and the maximum-f1
  formula are checked separately.

Floating-point tolerances are explicit in the script. scipy quadrature error
estimates are not interval certificates. The finite tested ranges are not
exhaustive physical parameter coverage, and a successful control does not
prove existence, single loading, capture kinetics, bath stability, uniform
normalization, or a continuum limit.

History is retained honestly:

- run_001 completed before accounting for recoil of the packet's quantum
  width. Its source result is superseded; its old input path no longer has
  the historical script hash. It is not current evidence for the source.
- run_002 completed after that source correction, before adding the sector
  occupation control. Its old script path has since changed.
- run_003 completed with sector occupation. `check_landscape_run003.py`
  preserves exactly its historical input hash. Root-aware validation of that
  old manifest at its original path would still see a changed script; the
  authoritative current manifest is run_004.
- run_004 adds the actual original-potential two-1s LCAO control and an output
  argument for repeatable fresh runs. Its current input hashes validate.

No failed historical run is hidden or relabeled as a current pass.
