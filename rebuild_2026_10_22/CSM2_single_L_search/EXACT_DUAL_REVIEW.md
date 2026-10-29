# Exact covariance/nuisance checkpoint

exact_dual_001 completes in3.6 seconds. The saved60x60 covariance is exactly
symmetric and has an exact rational LDL decomposition with60 positive pivots.
All3600 entries reconstruct exactly. LDL coefficients stay below4124bits. A separate full-certificate bit audit
finds4413bits maximum across all serialized rationals, below the20000bit cap.
The fixed witness annihilates all four template columns exactly, and its
quadratic denominator is positive. No approximate Q appears in the inequality.

For x=y-m and any nuisance b, use the C-inner-product Cauchy-Schwarz inequality:

 (a^T x)^2 = (a^T(x-Tb))^2
           <= (a^T C a) (x-Tb)^T C^-1 (x-Tb).

This proves the bound for unconstrained and nonnegative nuisance amplitudes.
The exact numerator interval over the published anchored native prediction
boxes gives a lower score569.5338658431842. An exact feasible-law candidate
upper score is154.34346325076024. The lower exceeds that upper plus9 in exact
rational arithmetic, so it also exceeds the actual law minimum plus9, provided
the actual model predictions belong to the stated native boxes.

All12 run controls pass. The self/adversarial full rational reconstruction has
13 controls. A separate exact law solve verifies all60 original covariance
rows and the candidate quadratic (3 more controls). The complete bit-cap audit adds2 controls. Full certificate.json
contains the rational LDL, witness and numerator boxes, not just rounded scores.
The dual witness is a derived inequality certificate, not a physical parameter.

This closes covariance/whitening/nuisance arithmetic for these fixed C,T and
native boxes. It does NOT prove native box membership for the original model
on real L: projection coefficient construction, anchor consistency and the
column/branch/continuum enclosure remain. No real-L or global exclusion yet.

Performance history: original signed_dot_001 hit its CPU480 bound after
506.748 seconds (exit-24, resource-limit), with no result file. The complete
failure manifest/logs/source are preserved. It is an NPZ-loading implementation
failure, resolved by the already-published cached run3.726seconds; it supplies
no scientific score. No native simulation/follower was altered or restarted.
