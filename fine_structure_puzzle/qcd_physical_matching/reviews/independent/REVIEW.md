# Independent audit: proton normalization, matching artifact, and radius functional

The normalized claims are the finite connected proton subtraction functional,
the retuned flat-baseline cancellation, and the finite-radius power/logarithm
projectors. Their algebra and normalizations pass. None determines a physical
QCD small-curvature coefficient or complete proton electromagnetic derivative.

This review uses the `mathbox:proof-audit` skill. It is independent in the
specific sense that the critical derivations in `PRETARGET_DERIVATION.md` and
the raw numeric result in `PRETARGET_NUMERICS.json` were saved before opening
the author's targets. They use raw tensor definitions, the supplied lattice
points, and primary sources. Later checks of author code are distinct from
that pretarget stage. No target, navigation, prior evidence, or Git state was
modified. All review outputs are confined to this directory.

## Claim cards and one primary verdict per claim

| Claim and exact audited scope | Primary verdict | Decisive evidence |
|---|---|---|
| C1. With canonical alpha=e²/(4pi), spin-averaged tensor (-g+qq/q²)T1 and rational charges in the current, the leading subtraction response is -3/(64pi²M²) integral dQ² S1. | **externally proved in the exact required form** | Walker-Loud v2 Eq. (13), with its Eqs. (2)-(7), and independent trace/angular reconstruction. Can's different T2 convention leaves T1 unchanged. |
| C2. For the six declared Can middle-ensemble samples, exact trapezoidal transformation equals -876375/152571904, with conditional covariance ceiling 166375/76285952 at fixed aM. | **computationally verified only in a stated range** | Exact Fraction reconstruction of all six inputs, five segments, native-unit coefficient, covariance ceiling; no continuum interpolation or total theory error claim. |
| C3. Given the QED_L leading shift alpha Q²c1/(2L) and a smooth matching branch M_ell!=0, a fixed-reference vacuum comparison has the baseline term -alpha Q²c1 E0,ell/(2LM_ell). | **conditional on a named input** | Named input: the large-L QED_L mass expansion. Chain rule independently reproduces its coefficient and sign. No S4 coefficient follows. |
| C4. Same-theory flat subtraction cancels the retuned baseline exactly, leaving F_L(theta_L)=E_L(theta_L)-E0(theta_L), without eliminating a possible intrinsic finite-size term. | **proved as written** | Algebraic identity holds before expansion. No assumptions on a QCD intrinsic coefficient are needed for cancellation of the bracket. |
| C5. The partial metric stress evaluated on a parameter path and the metric derivative of the composed path differ by -(H/4)lambda'_a partial_lambda_a f; a linear flat baseline changes by 3/4 only for the composed operation. | **proved as written** | Independent explicit flat model and direct chain rule agree with RAW_DERIVATION.md:189-198. The torus baseline itself receives no sphere 3/4 factor. |
| C6. At one fixed theory, the four-point stress and five-point W functionals have their declared exact nullspaces, moments, and normalizations. | **proved as written** | Independent spectral-polynomial expansion gives stress moment 28, W moment -49/128, and metric conversion 3/4. Target rerun passes 23 finite symbolic checks. |
| C7. These functionals converge to A_rho/m_p³ under the respective stated remainder hypotheses. | **proved as written** | Finite linear combination of o(H) stress remainders; for W-to-stress interpretation the explicitly stated D r=o(H) is also required. These are hypotheses, not established QCD properties. |
| C8. The logarithmic ratio sensitivity in proton DERIVATION.md:109 applies on every common parameter path without any further domain condition. | **correct only after a stated restriction** | Real log(A_rho) requires A_rho>0. One may instead use log|A_rho| locally when A_rho!=0. It is undefined on a zero-coefficient branch. The unlogged quotient derivative remains available there. This is a minor domain omission, not a failure of C1-C7. |
| C9. The current package supplies complete physical D_p, A_rho, or R(alpha). | **incomplete, with the smallest missing implication** | Missing complete matched proton kernel/matrix elements and common-theory curved rho/W/current-insertion data with continuum/radius control. The author expressly disclaims C9; passing C1-C7 must not be cited as C9. |

## Dependency graph and obligation matrix

C1 depends on the external tensor/current normalization and the spin average;
its trace, Wick sign, and angular integral are internal reconstruction. C2
depends on C1, the source table transcription, a finite chosen quadrature, and
conditional input errors. C3 depends on the external QED_L mass law and the
internal implicit-function chain rule. C4 is an exact subtraction identity
independent of C1-C3. C5 depends only on the specified partial metric stress.
C6 depends on that stress definition and finite polynomial algebra. C7 adds
the stated asymptotic remainder assumptions. C9 additionally needs physical
nonperturbative data, matching, and limit control; it is not a consequence of
any finite computation here. No circular dependence was needed.

| Obligation | Status | Audit result |
|---|---|---|
| Tensor, spin, coupling and current conventions | passed | Can T1 and Walker T1 agree; spin average is already included. No extra 2 or 4pi is available. |
| Cottingham subtraction sign | passed | Trace is -3 S1. The positive six-point S1 stencil gives a negative subtraction contribution; this does not determine the sign of the complete mass shift. |
| Native lattice normalization | passed | (2pi/N_L)² cancels the kernel pi². Neither physical M_p nor numerical alpha nor the rounded GeV² coordinates enter. |
| Exact source table transcription | passed | Visually inspected Can PDF pages 5 and 14: N_L=48, aM=.3860(44), all six vectors, central values and marginal errors agree with INPUTS.json. |
| Quadrature coverage | conditional | The defined six-point functional is evaluated exactly. No error bound for a continuous S1 integral or momentum tails is supplied. |
| Sea-current covariance sign/charge factor | passed | At degenerate u,d,s, Wick same-loop contraction is -tr(gamma S gamma S), Tr Q=0 but Tr Q²=2/3. Vacuum subtraction removes its disconnected expectation, not its baryon covariance. Nonzero amplitude remains unevaluated. |
| Mass constraint and matching coordinates | conditional | Chain rule is correct on a regular fully specified branch. Physical values, complete coordinate conversion, and matrix elements remain inputs. |
| Identity/contact terms in vacuum versus proton | passed | Connected proton subtraction removes an identity insertion; vacuum W retains it. The target keeps scalar, gluonic, identity, gravitational and regulator contacts in the derivative definition. No deletion of them was used in the finite results. |
| Metric partial versus parameter-path total derivative | passed | Explicit check gives A_base versus 3A_base/4. Targets correctly distinguish them. |
| Torus versus sphere geometry | passed | No transfer of c1 to closed S4 is made. QED_L zero-mode prescription and anisotropic vacuum stress are explicitly scoped. |
| Radius nullspaces and log multiplicity | passed | Double root at E=1 is necessary and present for log H. Normalization 28 is correct; the obsolete 42 is not used by v2. |
| Limit existence / derivative interchange in QCD | not addressed | Explicitly conditional in targets. Finite checks cannot establish uniform QCD asymptotics, H/u interchange, or D r=o(H). |
| Full topology/mixed-trace source audit | out of scope | Parent delegated this to another fresh reviewer. This audit does not certify the complete vacuum_response package or every ancillary source in proton REPORT.md. |

## Independent numerical and source checks

The raw trapezoid sum in squared integer momentum is 10.5165, giving
I/M²=1.2094109009924046 and partial_(e²)M_sub/M=-0.005744012999929529.
The corresponding alpha derivative differs by 4pi and is
-0.0721813961708115. Exact nodal weights are (3/2,5,21/2,15,31/2,15/2).
The covariance ceiling .0021809388968495797 is conditional on treating aM as
fixed; an arbitrary admissible correlation can also give zero variance here.
It is not a confidence interval on physical D_p. The published mass error and
all non-statistical systematics remain outside this ceiling.

Primary authentication was performed against supplied PDF version footers and
public arXiv metadata. [Can v2](https://arxiv.org/abs/2501.08619v2) is dated
21 May 2025; PDF pages 5 and 14 contain the transcribed tables. Public full PDF
text independently corroborates Eqs. (1)-(5), the valence-only implementation,
and the Type I/II limitation. [Walker-Loud et al.](https://arxiv.org/abs/1203.0254)
public metadata identifies the current version as v2, 3 June 2012; its supplied
PDF page 2 was rendered and visually checked at Eq. (13). The direct versioned
Walker web-PDF fetch failed, so no redownloaded-byte-identity claim is made.

Davoudi-Savage v2 source text at `/private/tmp/fsp-matching-1402.6741v2.txt`
Eqs. (6), (18)-(19) gives the stated leading QED_L mass term with negative
c1. Its spatial-zero-mode condition is essential. The Ewald derivative and
integral in RAW_DERIVATION.md:202-225 reconstruct the same shape constant;
the analytic omitted-cube bound follows from erfc(x)<=exp(-x²)/(sqrt(pi)x),
a coordinate union bound and a Gaussian tail ratio. The high-precision
decimal is not interval-certified, exactly as the target states.

Source hashes are recorded in `PRETARGET_NUMERICS.json` and
`TARGET_INPUT_HASHES.json`; the latter pins every author target opened here.
Key PDF hashes are:

| Source | SHA-256 |
|---|---|
| Can 2501.08619v2 | 29ce7af1791830fbdff9bb7d246c0ca76b704c44c596f3e9bbfd03a103d58804 |
| Walker 1203.0254v2 | 7ce483761fb4be5d15fc1f19b2935bd635c5dc411c5f43c88ae616f90b2bf761 |
| Davoudi-Savage 1402.6741v2 | 607f469de91fdcad22939f02f03f0ec58a1b2642d1fb76baf5aac98788dfd67f |

Executed bounded commands, all with fresh outputs in this directory:

    python3 .../reviews/independent/independent_checks.py
    python3 .../proton_compton/compute_response.py --inputs .../proton_compton/INPUTS.json --output .../reviews/independent/proton_rerun.json
    python3 .../matching_path/check_matching.py --output .../reviews/independent/matching_rerun.json
    python3 .../coordinator/check_finite_radius_v2.py .../reviews/independent/radius_rerun.json

The first is a separate stdlib-only Fraction implementation, with no import
of target code. The target reruns pass proton assertions, 21 matching checks,
and 23 radius checks. Their finite tested domains are retained. Source-page
PNGs in this directory are visual transcription receipts, not new data.

## Remaining gap and strongest safe statement

The cheapest next physical check is a declared common-theory continuum datum
for rho at four radii or W differences at five radii, with its covariance,
matched current insertions and a radius-limit error estimate. For the proton,
complete all-sea kernel data and UV/IR matching are needed before a full D_p.
Neither can be supplied by a charge-trace identity, by the shape constant, or
by evaluating a finite synthetic family. The safe current statement is an
exactly evaluated, conditional published-data functional plus exact
calibration cancellation and measurement functionals; the physical QCD
coefficient and alpha remain undetermined.

Review provenance: independent isolated subagent `/root/physical_independent_review`.
Pretarget derivation SHA-256:
`8dea4e9e458a2bfdfe1e0574deea1dc74e0f47fa710c1b543ff7c6c7998e0e1c`.
Pretarget numerics SHA-256:
`da48a0f9f84e9c27224b590c3f2a36c21cfeb4e06e7e4f4db19e8b7d622c3f73`.
