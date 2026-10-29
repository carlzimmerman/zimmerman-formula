# Actual corrected native point: necessary calibration failure

The predeclared binary64 L=4.8646 fails the unchanged actual CSM1 same-column
calibration. This is a new corrected point test, separate from legacy NL1's
fixed-T primary and CL3 extrapolation. No independent T or fitted parameter was added.

| Footing | SPARC own / basin | Groups | Cluster failures, own and basin | Lensing delta chi-square versus law / pure halo |
|---|---|---|---|---|
| canonical | pass / pass | pass, Z=1.6789769595 | G-MID-T3, G-OUT-all, G-IN-Mall (all OVER) | +435.9582717514 / -0.02616563835: fail |
| alt | fail / pass | pass, Z=1.6789769595 | same three (OVER) | +461.8035053955 / -3.44203312566: fail |

Lensing requires delta-law<=9 and delta-halo<0; the first cut fails on both
footings. Cluster lines require absZ<=2 on both backgrounds. A necessary
calibration failure rejects this point without a heldout rescue. No full-model
passing witness or global-L obstruction follows. The native estimator's known
binning instability remains; this does not derive a robust physical L.

The unchanged audited replay and all234 declared baseline inputs passed
preflight; cached baseline/template provenance and actual read closure were
checked. Main run:150.112 seconds, peak RSS0.641417216GB, one thread,
wall900/CPU600 limits, four outer controls pass, actual input hashes stable.
Independent CLASS/EPS/table reconstruction covers11962 recorded columns and
1400 SPARC selector decisions: no flag/mass disagreement; maximum relative
column discrepancy3.330669074e-15 against predeclared1e-10. It independently
implements column arithmetic but shares CLASS and declared physical inputs.
All52 raw-grade/dimension/core/flag/mutation review controls pass. Packaging
also checks every scientific floating value finite; see package audit.
Both manifests validate. X53 capture logs preserve the original SciPy
IntegrationWarning about quadrature roundoff/tolerance. Finite scores and
column/grade agreement do not prove quadrature convergence. The four trailing
spaces flagged by git diff --check belong to these verbatim warning lines and
are intentionally retained for byte-identical evidence. This arithmetic review does not independently refit
every SPARC curve or recompute the entire lens projection.

Do not hide source failures: each transformed X43 source exits1, with K0 and
K0x38 failing its historical EM1/X30/X38 baseline-value guards; the other five
source checks pass. These are recorded alongside the separately pinned audited
replay/baseline controls, not relabeled as successful source checks. Both X53
sources exit0. Executed sources, raw summaries, complete capture TXT copies,
outer result/input hashes and explicit source exit records are included.
The main runner and wrapper exit0; this means completed computation, not a
physical pass. No running simulation/follower or historical input was changed.

Reproduce with launch_native_corrected_point.py only into a NEW owned output
(after adapting its fixed destination); do not overwrite this immutable run.
Independent checks are launch_native_point_columns.py and
review_native_corrected_point.py. Frozen criteria precede the arithmetic.

Next: resume GROUP_MESH_008_ROUTE.md, fixed tiles14[2.76,2.77] and15[2.77,2.78],
with separately frozen runnable criteria/resources and immutable input inventory.
Continuous canonical feasibility remains OPEN. All frozen legacy NL1 validation
is already complete; do not rerun it or refresh final native inventories.
