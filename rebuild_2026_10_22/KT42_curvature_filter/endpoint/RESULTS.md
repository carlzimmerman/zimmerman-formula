# Endpoint closure result

**The constant isotropic quadratic Hessian endpoint family cannot repair KT40
while removing its all-background cold-fluid short-wave obstruction.** The
analytic statement is proved under the fixed-matter, constant-coefficient and
boundary hypotheses in `DERIVATION.md`. The symbolic implementation and stated
finite checks are verified: **24/24 passed**, including three deliberately
incorrect-sign/omitted-term controls detected as incorrect.

Write c=alpha+beta for Delta E=alpha(tr H)^2+beta H:H. The exact changes are

    Delta N=c,
    Delta Phi=-4 pi G c rho,
    Delta W=6 pi G c integral rho^2,

with the separately stated boundary qualifications. The UV-helping sign c<0
makes the already outward MW force and already negative Draco virial worse.
The sign c>0 cannot remove the existing positive-N high-frequency witness.
This closes this constant quadratic family; nonlinear coefficients and the
curvature-filter model in the sibling MW directory are different hypotheses.

Both fixed MW cells have a positive stellar column 41.51003903475583 Msun/pc^2.
Their disk-plus-gas vertical density derivative at R12,z.3 is
-3.67803037456329e7 Msun/kpc^4; their bulge adds another negative term. These
reported magnitudes are floating calculations, not certified numerical
interval bounds. The sign also follows analytically from the positive source
components, whose derivatives were checked symbolically.

The reused KT40 deficits demand changes of at least 843.7699442474329 and
936.1114251316735 (km/s)^2/kpc in the canonical/alternate vertical potential
derivatives, and at least 19.338292177662662 (km/s)^2 in the canonical Draco
W/(3M) witness. These are necessary zero-crossing thresholds with the original
finite-grid uncertainties attached; equality establishes neither hydrostatic
restoration nor a positive-dispersion equilibrium. No old physics solve was
rerun and no physical cut or baryon parameter was changed.

## Provenance and validation

- `run_002/manifest.json`: v2, **completed**, exit0, 2.071126 seconds; 60-second
  wall, 50-second CPU and 1-thread requested caps; no memory or affinity cap
  requested. Python3.9.6, SymPy1.14.0. Input hashes unchanged before/after.
- `run_002/results.json`: exact symbolic identities, 24 check records, two
  fixed MW sign witnesses, one saved Draco threshold and constant-extraction
  source lines.
- `contract_v2.json` and `check_endpoint_v2.py` were written before execution.
- The installed computation-audit `validate_manifest.py` with `--root` reported
  `valid evidence record (run status: completed)` for run002.
- Original `run_001`, `contract.json`, and `check_endpoint.py` are retained and
  their manifest validates with status **failed**. Its bulge derivative check
  stopped because `simplify` alone did not cancel equivalent radical/power
  factors. A minimal diagnostic found exact `cancel`, `factor`, and the expanded
  logarithmic derivative all produce zero; the one v2 change applies exact
  `cancel` before the same zero test. No physical assertion or tolerance changed.

Regeneration uses the installed bounded runner described by the contract:
pass every `execution_artifacts` entry as `--input`, a fresh output directory,
the same bounds, and

    python3 rebuild_2026_10_22/KT42_curvature_filter/endpoint/check_endpoint_v2.py --output FRESH_DIRECTORY/results.json

The runner command and all actual arguments are in the manifest. Validation:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py rebuild_2026_10_22/KT42_curvature_filter/endpoint/run_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

## Self-review

The source-variation, rank-one, Fourier, null-divergence, virial integration and
Plummer normalization routes agree. The analytic proof supplies universal
coverage of the stated quadratic class; finite checks do not create it.
Boundary stress, finite-box harmonic response, regularity and unchanged matter
coupling are explicit. The original KT40 witness accuracy is inherited rather
than independently certified. This is same-author self-review with different
algebraic constructions, not an independent-agent proof audit.

Mathematical proofreading covered the new derivation and this result record.
Notation and the sign convention a=-grad Phi are consistent; no unresolved
typographic mathematical-token issue remains. Generic dynamical completion,
zero-frequency inheritance, and density-contact mechanisms were already in
the repository; the newly recorded part is their quantified KT40 application
and this constant quadratic classification.
