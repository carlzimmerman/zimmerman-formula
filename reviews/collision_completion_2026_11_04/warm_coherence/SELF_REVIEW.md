# Focused self-review

Claim card: for the declared frozen-bath eight-phase coefficients at the two
pinned warm occupation states, every PSD periodic four-parent density obeys
the source-trace/damping-gap current envelope in DERIVATION.md. The local and
orbit-averaged stationary density diagnostics quantify isotropic-parent error
within their separately stated closures. No full physical history is claimed.

Primary verdict: **conditional on the named finite coefficient/kinetic model**.
Review provenance is self-review. Exact source hashes and all input revisions
are pinned in PROVENANCE.json; no independent reviewer claim is made.

Dependencies and checks:

| Obligation | Outcome |
|---|---|
| Correct parent identity | Passed: massive S1_1, four states; massless S1_0 not substituted. |
| Actual-x amplitudes and common kinematic masses | Passed in the finite construction; full basis/couplings rebuilt and interpolation difference measured separately. |
| Daughter-group isotropy/unpolarized closure | Named input; weights are scalar on each channel matrix only under it. |
| Spin/identical-particle/parent normalization | Controlled by independent P-only scalar operator, pole eigenvalues and thermal KMS checks. |
| Quantum holes/angular projection | Exact within the declared finite entropy projection; warm002 independent holes retained, unavailable warm001 sub-ulp holes not invented. |
| Positivity of gain/loss matrices | Actual Gram/spin-sum construction with positive statistical factors; finite eigenspectrum checks pass. |
| Positive total damping D | Measured at every represented parent node and phase with a gap around 1e-8; not assumed for arbitrary inverted baths. |
| Common frame | Actual parent projector overlaps have leakage below1e-15 over the tested orbit packets. |
| PSD periodic trace inequality | Passed internally: trace commutator vanishes; comparison with Smax-gamma_min N bounds any periodic trace. |
| Charged-current operator norm | Passed internally: affine gains cancel and the PSD trace inequality applies; factor two for charged daughter pairs retained. |
| Whole25 phase cancellation | Explicitly computed with exact angles and snapshot-matched source convention; numerator compared to the signed phase-averaged whole current magnitude. |
| General physical medium/history | Out of scope: varying baths, rate-changing dispersive matching, broken vectors, nonlocal correlations and additional channels remain. |

The analytic trace inequality is not inferred from a numerical scan. Its
numerical coefficients are floating-point evaluations with large positive
damping margins and independent controls; this is not an interval-arithmetic
or formal proof certificate for microscopic matching.

Strongest surviving statement: the isotropic four-parent closure has a large
relative P-branching error at these warm states, but the directly tested
whole-current correction is below .02%, and the stronger frozen-periodic
trace envelope is below .64%. It cannot be turned into a global transport
multiplier. The exact first broader bridge is changing-bath coherent
transport plus matching of the omitted physical sectors.

Mathematical proofreading covered the new contract, derivation, source note,
status and review. Routine edits: spacing only. Mathematical-token changes: none.
Unresolved scientific conditions remain explicitly stated. Validation uses
the installed v2 manifest checker and is recorded verbatim in provenance.
