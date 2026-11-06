# Brief independent reduced v2/v3 checkpoint review

Core changes pass read-only review. Explicit reconstructed-mean, tangent-
mean and unaugmented tangent-residual checks address the earlier audit.
Checkpoint-only prolongation rejects previously failed states, preserves
the retained Fourier coefficients and scalar mean, carries polarization
gvar and the p cache, and performs an immediate state check. Optional
evaluation padding changes numerical quadrature, not physical data.

Inspected reduced_validation002 reports six passing checks. The r511,
r1023_a and r2047_b results stop on the reconstructed p_beta spectrum,
not a domain singularity; r511_half passes t=1.4. STATUS.md's numerical
claims match these outputs and correctly distinguish endpoint diagnostics
from full-field convergence and checkpoint prolongation from independent
fine initial-data runs. No broad suite was rerun for this review.

Minor robustness gaps: reject even independent n and evaluation<n
explicitly, and make failure serialization tolerate initial failure before
gvar/cached_pl exist. Otherwise unconditional .tolist calls could mask the
original exception. These were not observed failures of the quoted runs.

STATUS.md should now distinguish the audited small-amplitude auxiliary/ADM
initial-family construction from the still-unproved full coupled local-
existence/continuation theorem. Conditional Riccati formation and numerical
accuracy stops must not be promoted to scientific closure. The singular
selection question remains open.

Full detail and reviewed hashes are in the v2/v3 addendum to
REDUCED_REVIEW.md. Independent delegated code/claim review, 2026-11-06.
