# FSP-010 reproduction and evidence scope

Repository root: /Users/carlzimmerman/new_physics/zimmerman-formula. Completed run inputs and output directories are immutable. Use each exact contract and fresh directory for a reproduction.

- [Hard-proton commands](hard_proton/REPRODUCE.md): source-table stencils, scalar calibration and finite quark matching. Published extraction fits and source calibrations are inputs; no new form-factor or target fit is applied.
- [All-scale commands](hard_bridge/REPRODUCE.md): independent full radial/Feynman-parameter Dirac representations, finite and infinite endpoint reconstruction. This is an elementary benchmark, not a proton replacement.
- [Closed vacuum commands](global_qcd/REPRODUCE.md): actual group/connected-support/cell/rank arithmetic and explicit finite Taylor bound. Tiny bare beta is an algorithmic test point, not a physical calibration.
- [Finite-gluon commands](gluon_matching/REPRODUCE.md): source-derived sequential matching, vector projection and regulator moments. Both failed symbolic runs and the corrected third execution remain.
- [Sea-Hodge commands](coordinator/sea_hodge/REPRODUCE.md): finite cell/phase/rank enumeration, independent tree-gauge covariance and direct hopping-matrix derivative controls. No continuum QCD spin/taste equivalence is supplied by these checks.

Every executed mathematical computation has an actual bounded v2 manifest. Validate a selected record with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Validation certifies recorded execution and input freshness; it does not prove the physical transfer, a quadrature error interval or a continuum limit. Source-specific cache hashes/versions and extraction choices remain distinct from application verdicts. Full public source files are retained only in the authorized ignored cache or temporary retrieval paths; receipts do not assume those local paths exist on another clone. No RLIMIT_AS was requested on macOS. Independent review and its exact exposure/check scope are reconciled separately.

The final current hard-proton execution is the [exact archived-handoff replay](coordinator/hard_proton_replay/REPRODUCE.md). Updating live navigation made one original administrative input stale; its completed record is preserved. The replay reuses the original numerical code/data and exact archived original handoff bytes, and its result matches byte for byte. The replay companion review distinguishes mathematical review from this new execution record.
