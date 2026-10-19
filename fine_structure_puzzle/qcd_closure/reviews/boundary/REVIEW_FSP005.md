# Independent review of FSP-005 boundary heat calculation

Review date: 2026-10-19 UTC. Reviewer: fresh delegated agent, independent
derivation before target inspection. Only files under `reviews/boundary/`
were written. Target sources and prior evidence were left unchanged.

## Normalized claim and primary verdict

For the stipulated complex charged-pair determinant on the smooth ball,

\[
\Gamma_m=\operatorname{Tr}_{\mathbb C^4}\log(-\Delta+m^2)_{\rm rel}
-2\operatorname{Tr}_{\mathbb C}\log(-\Delta+m^2)_D,
\qquad m>0,
\]

with tangential vector components Dirichlet and normal component
`(partial_r+2/R)A_r=0`, the combined coefficient is

\[
A_4=-{128\pi\over315R},\qquad
\Gamma_m\big|_{1/(mR)}=+{16\over315mR}.
\]

**Primary verdict: proved as written**, for this constant-mass benchmark.
The mixed-projector calculation and independent TE/TM spectrum specialization
both establish it. There is no coefficient, multiplicity, or Robin-sign
discrepancy in the inspected target derivation.

The scalar-profile and common-PV expressions also agree with the fresh local
calculation. Their use as the inverse-R coefficient of a complete monopole
determinant remains **conditional**, for the reasons below. This is the
scope already stated by the target files, rather than a newly required
repair to their benchmark.

## Artifacts and independence boundary

The raw result was saved in `RAW_INDEPENDENT_FSP005.md` before reading any of
the three target files, their code, or their outputs, and was then sent to
the parent reviewer. The only project input read before that save was
`boundary_heat/SOURCE_RECORDS.json`, as a receipt locating primary source
PDFs; it contains wall conventions but no target coefficient. Primary
formula text was read directly from those PDFs' extracted text, and exact
version stamps were checked against the arXiv PDFs.

Raw independent file SHA256:
`c0ef2e2eec2924c02d9c7082bccb7da06eb457b4bd77f446ca4a0be7196a08e0`.

Targets audited at these exact SHA256 revisions:

| File | SHA256 |
|---|---|
| `boundary_heat/INDEPENDENT_DERIVATION.md` | `6423b09b5d1f1b9b4f1898c019bc8e429568656abf13508871391893d8ad5a97` |
| `boundary_heat/ADDENDUM_COMMON_PV_PROFILE.md` | `b81008355d8dcfd6d05d23267c64180f4b0ba89a237bbb5b5c35d0340a8f1a92` |
| `boundary_heat/REPORT.md` | `ba0f97f2a8c6e47dc33a569bf82f7a656dd7df3c197a51270978cc4d5084ec24` |
| `boundary_heat/SOURCE_RECORDS.json` | `5414c7edd43a416da719815258a2c1baf4e0a98c1c387b1c11982861ebef102e` |

Repository HEAD at review: `9516ee01c79f35c04b7556050669ba77b0c98b99`.
Content hashes, rather than HEAD alone, pin these working-tree artifacts.

## Dependency graph

1. **Operator/domain convention:** one complex four-vector trace minus two
   complex Dirichlet scalar traces; inward-normal relative wall.
2. **External heat theorem:** Vassilevich (3.58), (5.31)-(5.33), cross-checked
   with BGKV Theorem 2.1 for smooth mixed domains.
3. **Internal geometry:** rank-one moving normal projector, positive
   L_ab=delta_ab/R, S=-2P_normal/R, and flat bulk connection.
4. **Internal exact contractions:** geometric cubic, Robin, and projector
   derivative terms give the combined A4 and hence the constant benchmark.
5. **Independent internal spectrum:** Hodge exact gradients cancel the
   scalar traces, leaving TE and TM with l>=1; their two absent l=0 towers
   have no t^(1/2) term.
6. **Auxiliary local scalar route:** Duhamel variation and smeared heat
   coefficients determine the collar mass jets. Boundary-value resummation
   of the lower K*mass term supplies the necessary quadratic correction.
7. **Auxiliary common-PV route:** apply the same regulator filter and domains
   before the Matsubara sum; a hand Riemann-sum limit gives the finite
   heavy-regulator term.
8. **Unchecked promotion:** regulator-uniform large-R remainder, complete
   smooth operator/core, bulk/surface matching, and fixed finite wall scheme
   are required for a global determinant or stress.

No dependency points back to a target coefficient or a numerical fit.

## Obligation matrix

| Obligation | Status | Decisive evidence / limit |
|---|---|---|
| Complex-pair and ghost multiplicity | passed | Stipulated trace is used directly; A4 is Dirichlet and no extra factor 1/2 is inserted. |
| Inward normal and Robin sign | passed | Primary relative-domain formula gives S=-2P/R. |
| Moving projector | passed | tr chi_a chi_b=8 delta_ab/R^2; all three derivative terms retained. |
| Constant A4 contraction | passed | Independent supertrace polynomial -256/(7R^3). |
| Determinant sign and normalization | passed | Minus proper-time integral turns negative a4 into +16/(315mR). |
| TE/TM specialization | passed | D and outward Robin 1/R spectra for l>=1. |
| l=0 subtractions | passed | Union of roots is pi q/(2R), q>=1; no t^(1/2) term. |
| Scalar collar first and second normal jets | passed locally | Smeared a2 derivative and a3 second-jet terms cancel by str chi=0; the surviving a3 first jet is retained. |
| Quadratic boundary-mass correction | passed locally | Expansion of -8R sqrt(q^2+M^2+U_b)/3 is necessary and gives the displayed regulator term. |
| Finite-regulator coefficient series | passed as a local series | Common-PV cancellations make its Matsubara tails absolutely summable. |
| Heavy-regulator Riemann-sum limit | passed for that series | Integral of (1+t^2)^(-3/2) is 2, giving L/pi. |
| Uniformity of full determinant remainder | conditional | Coefficient-series convergence does not prove the expansion can be interchanged with the complete four-dimensional trace. |
| Complete spin/connection monopole operator and core | not addressed | This independent derivation starts from the stipulated scalar collar operator. |
| Finite cubic boundary counterterm | conditional | Its coefficient must be fixed by an explicit surface renormalization condition. |
| Full spectral/global result, physical stress, alpha | out of scope | None follows from the local wall calculation. |

## Decisive local checks

In the combined vector/ghost trace the formal projector ranks are one plus
and one minus. The L-cubic, S, and moving-projector groups contribute
1088/7, -1344, and +1152 in units R^-3. Their sum is -256/7. The factor
`4*pi*R^2/[360*(4*pi)^(3/2)]` gives
`a4=-16/[315*sqrt(pi)*R]`, or the target A4 above.

For the TE/TM check the scalar a4 values are
`-2/[315*sqrt(pi)*R]` for D and
`-14/[315*sqrt(pi)*R]` for outward Robin 1/R. The omitted l=0 traces sum to
`R/sqrt(pi*t)-1/2+exponentially small`; thus they do not alter a4. This check
uses an actual vector spectral decomposition, including the lowest modes.

For the profile use q=2*pi*n/L+v, mu^2=q^2+M^2 and
`U=-2q/r+1/r^2`. With inward normal N,

\[
U_b=-2q/R+1/R^2,\quad
U_N=-2q/R^2+2/R^3,\quad
U_{NN}=-4q/R^3+6/R^4.
\]

The combined smeared boundary coefficients needed at this order are

\[
a_2^\partial[U]=(4\pi)^{-3/2}\int_\partial {-8U\over3R},
\qquad a_3^\partial[U]={5U_b\over8}-{5R U_N\over16}.
\]

The a3 value term yields -5q/(4 mu^2 R), while its normal derivative yields
+5q/(8 mu^2 R). The final odd term is therefore -5q/(8 mu^2 R), exactly as
in the target. A boundary-mass-only substitution would miss half of this
answer. At M=0, expanding the lower wall term only to first order in U
would create a spurious -4/(3|q|R); its second-order term cancels it.

At finite regulator mass the complete local scalar-collar coefficient is

\[
C(q,M)={16\over315\sqrt{q^2+M^2}}
-{5q\over8(q^2+M^2)}
-{4M^2\over3(q^2+M^2)^{3/2}}.
\]

This independently agrees with the addendum's formula for unit Coulomb
tail. For a tail h=v-b/r, the second and third terms acquire factors b and
b^2 respectively. Its heavy-regulator third term sums to
`+4 b^2 L/(3*pi)` because `sum_(j>0)c_j=-1`. At v=pi/L the odd term cancels
under n -> -n-1 for every finite common PV mass. The addendum's center
formula is therefore correct as a statement about this local wall series.

## Bulk/surface and renormalization convention

The scalar-profile formulas use the integrated Duhamel convention: total
bulk derivatives are integrated by parts, and their normal flux is assigned
to the surface. For example, direct unsmeared a4 with E=-U contains an
explicit E_N boundary term. Its combined value cancels the flux from the
bulk Delta E term, agreeing with the vanishing smeared a2 derivative term.
Keeping only one term changes the separation.

Thus the target's statement that its first-jet coefficient is derived
directly from the smeared heat trace is justified. Nevertheless any later
comparison to a bulk representative must declare the same integrated
convention. It would be incorrect to add an integration-by-parts surface
density to this spectral wall sector without matching what was removed
from the bulk.

The local counterterm `lambda integral_(S^1_L x S^2_R) K^3` evaluates to
`32*pi*lambda*L/R`; hence it changes the absolute inverse-R coefficient.
The geometric sum has a logarithmic divergence and its finite part is not
fixed by common PV alone. A same-scheme local comparison can cancel this
geometric ambiguity. That does not supply the omitted bulk/core terms in
the full difference of determinants.

## Source and computation checks

The exact primary source application is verified for the smooth benchmark
and scalar collar variation. The Vassilevich and BGKV PDF hashes are in the
raw report and match the target receipts. Inward normal, E sign,
Pi_plus/Pi_minus roles, smearing derivatives, and heat normalization were
checked explicitly. No secondary source or uncited remembered coefficient
was used to determine the result.

Commands used included `sha256sum` on retained source PDFs and inspected
targets, `sed` on primary extracted texts, and `nl -ba` for target locators.
Exact-version PDFs were opened at the primary arXiv URLs. No numerical
experiment, frequency fit, existing checker, or run output was used or
executed. The conclusion rests on the displayed analytic specialization,
not on the target's bounded rational test evidence.

## Remaining implication and strongest safe statement

The constant smooth-ball wall benchmark is independently established. The
profile addendum's scalar collar coefficient and heavy-PV contribution are
independently verified at the level of the specified local heat expansion.
The report accurately limits their meaning.

The smallest missing implication is a regulator-uniform estimate showing
that the local collar expansion, after the full frequency trace, has a
remainder smaller than R^-1 in the declared common bulk/surface convention.
That estimate must be accompanied by a specified smooth full operator and
core/neutral matching before it identifies a global monopole coefficient.
Surface matching must fix the finite cubic counterterm. A metric stress
and electromagnetic normalization remain separate obligations.

No target correction is requested. Do not promote this review to a proof
of the full summed/global determinant, a physical stress, or an alpha
selection claim.

Final mathematical proofreading covered the two new review files only:
routine edits none; mathematical-token changes to prior files none;
unresolved notation issues none. No build applies to these Markdown reports.
