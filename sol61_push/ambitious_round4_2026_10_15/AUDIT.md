# Round-four evidence and scope audit

The analytic arguments, actual code and scientific outputs were inspected
by root and a separate same-team agent for each route. This is an internal
research audit, not external peer review or formal verification. The
machine-readable integrity observation is `verification_final.json`.

| Route | Authoritative evidence | Independent audit | Accepted scope |
|---|---|---|---|
| Angular | `angular/PROOF.md`, `run_exact` | [Einstein agent](angular/EINSTEIN_AGENT_AUDIT.md) | All-l static hybrid density/shape estimate; null symmetries retained |
| Einstein | `einstein/PROOF.md`, `run_v3` | [Angular agent](einstein/ANGULAR_AGENT_AUDIT.md) | Full static Einstein branch and both wall jumps; selected tension |
| Inventory | `inventory_energy/PROOF.md`, `run_v2` | [Angular agent](inventory_energy/AUDIT.md) | Exact gamma-zero binding and finite-start conserved-energy budget |
| Lensing | `native_all_verified_001`, source diagnostics, `summary_verified_001` | [Einstein agent](lensing/INDEPENDENT_AUDIT.md) | Controlled finite post-data projections/fits; absolute gate fails |

Root independently reconstructed the angular electric-phase jump/completion,
fluid and wall gravity shape terms, all-l shell kernel identity, and uniform
coefficient estimates; the static Einstein Hilbert stress, conservation and
Israel mass/load elimination; the binding-energy envelope derivative and
series; and the finite-cylinder/environment projection and covariance
profiling. Root visually inspected the final lensing figure. Detailed
line-by-line arguments remain in the route proofs and audits.

The angular agent also read the root RESULT/CURRENT synthesis. Its required
correction explicitly restricted the strong-convergence obstruction to the
conserved-energy topology; that correction is applied. Its optional heading
clarification, “static energy,” is also applied. No theorem or run bytes were
changed by this synthesis review.

The angular 219 exact checks include finite Legendre and ratio ranges. The
all-l conclusion depends on the analytic proof, not those ranges. Einstein's
128 assertions and eight IVPs support symbolic bounds and finite illustrative
solutions; the contraction establishes existence in the full function box.
Inventory's nine exact checks, three independent high-precision integrals
and nine finite starts support the formula and examples; the universal
energy obstruction uses the analytic minimum and conservation. Lensing's
19 completed runs are bounded fits/controls, never a population theorem or
prospective empirical confirmation.

## Failures and supersession

There are 25 bounded manifests: 22 completed and three failed. All 22
completed manifests validate against their current input/output bytes.
Inventory `run_v1` is a hash-valid failed record: a CAS positive-root
simplification was replaced by an explicit squared identity/positive branch
in separately named v2 code. The original code and output remain.

Einstein `run_v1` and `run_v2` failed on a logarithm-domain simplification
and a strict rational endpoint comparator. Their original input pathname
was reused during harness repair, so both are **stale under current-root
validation**. This provenance defect is not hidden by refreshing hashes.
Exact old preimages at `DRAFT_CHECK_V1.py` and `DRAFT_CHECK_V2.py` match both
recorded before/after hashes; all other inputs/logs still match. See
[the recovery receipt](einstein/HISTORICAL_INPUT_RECOVERY.json). The old
manifests are unchanged, and only `run_v3` is accepted for the current code.

The first lensing launcher attempt failed before scientific execution due
to an absolute output path and has a separate receipt. The initial
`controls_002` normalization entry was algebraic rather than a runtime
mutation; `refinement_001` executes the actual mutation through both paths.
The final point-source fit was rerun afterward. Earlier `native_all_001`
and `summary_001` remain historical. The old external K2 failed control
and all frozen old scores remain unchanged.

## Remaining mathematical and physical limits

Static hybrid positivity, static GR existence and gamma-zero canonical
energetics apply to different functionals or parameter domains. Their
combination does not establish a dynamically stable GR galaxy. The actual
Einstein wall/EOS/phase and tension selection are effective inputs. The
new lensing profile follows a spherical acceleration algebra with finite
truncation and an inherited environmental template; no action-level join
to that Einstein body has been derived. Fitted baryon sizes are not measured
source constraints. Post-data nominal p values do not include selection
calibration. Formation receivers, abundance, cosmology and coefficient
selection remain missing physical implications.

Historical source copies and proof/run hashes are frozen; navigation and
this synthesis are updated separately. The top-level source checkpoint
records the concurrent census and filed DR4 amendment. No sealed data were
read or production simulation launched in this round.

The default staged whitespace check flags CSV-writer CRLF line endings and
one extra blank line at the end of the frozen extended-source code. These
bytes are preserved to retain the run/audit hashes. The check with
`core.whitespace=trailing-space,space-before-tab,cr-at-eol,-blank-at-eof`
passes; it treats CRLF as a line terminator and explicitly disables the
harmless blank-at-EOF warning.
The current Markdown links resolve and all 24 Python sources parse.
