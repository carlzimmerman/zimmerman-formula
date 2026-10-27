# Preserved implementation corrections

Version1's direct fine-grid analysis sampler changed the observation operator.
The independent four-cloud fixture found1.19–2.17% L1 error at native
resolution, but3.98–4.56% at the original direct refinement2. Version2
anchors the fine lattice on actual native centers, restricts to those centers,
and reapplies the unchanged native-analysis interpolator. The corrected
refinement2 errors are0.34–0.83% in the tested fixtures. Version1 and its
completed nominal and audit records remain untouched; they do not establish
same-operator convergence. Version2 also resolves Gaussian arm azimuth by
CDF quadrature split at half-disk boundaries, including zero-width/finite-peak
limits. Its35 angular fixtures and actual model refinement controls are
separate evidence from source reconstruction completeness.

The scenario generator's first unpinned draft dispatched phase/width shape
names through a broad prefix test. Exact-name handling was corrected before
any scenario runner pinned it; the final source-design audit checks actual
JSON profile shapes. No completed scenario run uses that draft.

`analysis_run001` failed before producing results. Its saved float32
component arrays and measured scales yielded a float32 design matrix. The
bounded SciPy QR path raised `Buffer dtype mismatch, expected double but got
float`. A narrow reproduction showed the same error; explicit float64 inputs
succeeded, matching `fit_components`' existing input rule. The original
script and failed record remain unchanged. `analyze_family_v2.py` adds those
two boundary casts; fresh `analysis_run002` completed and was independently
checked. No failed execution is counted as scientific evidence.

Independent audit fixtures also retain their failed setup/NumPy-boolean JSON
serialization records and corrected fresh runs. See the audit reports for
scope. These failures are history, not successful model or physical tests.

The frozen `followup_contract.json` inherited a HALOGAS-only descriptive
`nativeROI_pixels=[69,192,192]` entry. Actual WHISP has127 native channels
(and253 at refinement2 in its analytic fixture); the adapter derives the
shape from the actual header. This corrects that metadata description only.
The run's actual input cube, coordinate grid, byte/hash provenance, dynamic
allocation and wall/CPU/thread caps are recorded; no69-channel WHISP crop
was used. The contract is preserved rather than silently rewritten.

Two historical failed manifests reference their original script names, now
occupied by corrected versions: `audit/stats_run001` and
`recovery/digitization_run001`. Their `--root` current-input checks therefore
fail. The original input bytes remain under explicit `*_v1_failed.py` names;
verification checks these archived hashes separately. Neither failed record
is used as scientific evidence. All22 completed records pass current checks.
The final plotted target/velocity-width/background labels are corrected in
`plot_run002`; the first plot record remains as presentation history.
