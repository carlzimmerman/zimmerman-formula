# Independent audit of target-only pressure information

**Primary verdict: proved as written**, within the expressly finite noiseless model with fixed offset and exact rational interpretation of the stored binary64 operator. The generic rowspace theorem is an exact linear-algebra statement; the particular ranks and witnesses are certified for this stored matrix only. This is not an authenticated detector response, a continuum inverse theorem, a fitted pressure profile or a gravitational-force result.

Auditor `/root/metric_intake`, 2026-09-30. The root's independent derivation, root check code/contract/record and original FGF019 model were read. No FGF024 worker derivation or code was read or used. Exact hashes are recorded in `audit_result.json`.

## Claim, assumptions and dependency graph

There are 15 free nodal pressures and one additive map offset. The pressure at the final support node x=5 is fixed to zero and is not an additional free coordinate. H has 12 measurement rows; C=[H; e_offset] incorporates the **assumed fixed offset** b=b0. This is an added constraint, not evidence that a detector has calibrated the background. The nullity and controls would need reconsideration if the offset remained unknown.

Let N be a basis matrix for ker C, L the scalar pressure-gradient target, ell=L N and D=W N for additional rows W. The claim is that W determines the target on the affine solution family exactly when ell is in row(D), without requiring recovery of every pressure coordinate. Under positive/strictly decreasing inequalities the same condition is necessary for **local** target identification at an interior feasible point; it is sufficient globally. Actual physical observation rows must come from the same response conventions, not from an unconstrained algebraic choice.

Dependencies: stored H and target L -> rank(C)=13 -> three-dimensional complete null basis -> reduced target ell -> rowspace/annihilator criterion -> synthetic distinguishing controls -> feasible strict-interior counterwitness. FGF019 supplies the conditional meaning of H and L, not an independent force calibration. Noise robustness and authentic response remain separate missing inputs.

## 1. Generic target-only proof and strict-interior qualification

Given one compatible theta0, every solution of C theta=c is theta0+N z. Two members also agreeing on W differ by N delta_z with D delta_z=0. Their targets agree for every such pair exactly when ell delta_z=0 for all delta_z in ker D. In finite-dimensional real linear algebra this is equivalent to ell in row(D): row(D) is the annihilator of ker D. The exact rational rank computations also establish this real-coefficient statement for the stored rational matrices.

For inequality-restricted pressures, sufficiency is unchanged. For necessity near an interior feasible theta0, take any null perturbation v=N delta_z with ell delta_z nonzero and D delta_z=0. Each positivity/monotonicity constraint has positive margin at theta0. There are finitely many linear margins, so both theta0+t v and theta0−t v remain feasible for sufficiently small nonzero t, while preserving C and W and changing the target. This establishes local nonidentifiability.

The strict-interior condition cannot be removed. For example, with two nonnegative coordinates, the equality theta1+theta2=0 leaves a singleton feasible set. L=(1,0) is determined there although it is not in the equality rowspace span(1,1). The root derivation correctly excludes such boundary-only necessity claims.

The block identities also follow directly: invertible inner A gives theta_i=A^-1(d−B z−h_b b0). Therefore D=W_o−W_i A^-1B, ell=L_o−L_i A^-1B, and the target contains the stated measured-data and offset particular-solution terms. A response aligned with ell identifies this one target, not all three free coordinates.

## 2. Root exact calculation reviewed

`check.py` converts each stored finite binary64 entry using Fraction(float), so the arithmetic is exact for those binary64 numbers. Its elimination normalizes a nonzero pivot and removes it from every other row. The expected pivots are columns 0,...,11 and 15. The three returned vectors have free coordinates 12,13,14 equal to the identity and offset component zero; direct C-null checks are included. Since all three ell components are nonzero, the target is not already identified.

The synthetic aligned row has reduced response ell and raises the constrained rank from 13 to 14; adjoining L adds no rank, leaving nullity two. The coordinate row selecting free coordinate 12 has reduced row (1,0,0) and fails because ell has nonzero other components. The nonzero orthogonal row (ell_2,−ell_1,0) cannot span ell over the reals; it measures new information but not the missing target. Perturbing the first component of the aligned row by one makes a nonparallel row because ell_2 is nonzero. Two independent rows including the aligned one give rank 15 while retaining target identification; all three free-coordinate selectors recover rank 16. These controls check target-specific information, rather than assuming any new measurement or full recovery is necessary.

The two feasible witnesses use the second canonical null vector, which leaves the selected first free coordinate unchanged. The exact epsilon is one half the minimum of every positive baseline margin divided by its nonzero directional change. Thus every affected margin stays at least half its original value for either sign; unaffected margins remain positive. Exact H equality, fixed background, added-coordinate equality and unequal target values are checked. Strict positivity applies to the 15 free nodal values; the final support endpoint remains the prescribed zero. Linear interpolation preserves positivity before that endpoint and strict monotonicity on each segment.

## 3. Independent saved-certificate verification

Rather than rerunning root elimination, the reviewer checked the saved rational null and witness certificates by direct exact products and used a different rank certificate: reduction of the 12-by-12 inner block modulo prime 65537. All binary64 denominators are powers of two, hence invertible modulo that prime. The modular determinant is **45395**, nonzero. Therefore the rational determinant is nonzero. Appending the offset selector gives a nonsingular 13-by-13 minor of C, so rank(C)=13. Three independent exact C-null vectors then span the entire nullspace; their canonical free rows certify independence.

Direct exact products verified ell=L N and the aligned/coordinate controls. The orthogonal row satisfies d dot ell=0 and is nonzero, hence is not proportional to nonzero ell. The damaged aligned row has a nonzero two-coordinate determinant equal to ell_2, so it fails target identification. This independently verifies the rank consequences without trusting a floating-point singular-value cutoff or the author's block inverse.

The baseline and two witness minimum pressure/monotonicity margins are respectively 1.831563888873418e−7, 1.5735714739564885e−7 and 1.6562215516469977e−7. The two target values are approximately −3.6700618483688887e−6 and −3.6997957558830675e−6; the exact rational inequality and difference are preserved in the saved results. These are dimensionless finite pressure-model derivatives, not accelerations or mass estimates.

The three root input hashes match their before/after records; all three root output/log hashes match, for six explicit checks. The review's direct checks also confirm the witnesses preserve the model bins, assumed offset and added coordinate exactly. No tolerance is substituted for equality.

## 4. Execution and provenance

The root recorded run completed in 0.21027 seconds with exit 0, 120-second wall bound, 110-second per-process CPU bound and cooperative one-thread environment; no memory cap is claimed. The present reviewer inspected that source and record rather than executing the root's script.

A preliminary read-only inline certificate check was executed, then preserved as the equivalent saved `reviewer_check/check_certificates.py` and repeated under the standard bounded runner after the parent expanded this review's write scope. `reviewer_check/PRELIMINARY_RECORD.md` records that sequence. This repetition records provenance for the same bounded checks, not an expanded parameter scan. The fresh runner record, results and logs are in `reviewer_check/run_001/`; exact command, input hashes, environment and limits are in its manifest. Manifest validation returned `valid evidence record; mathematical interpretation requires review`. Source and result hashes are included in this audit's JSON. The preliminary inline run is not retroactively represented as having a runner manifest.

The review performed one 12-by-12 modular determinant and direct rational checks of three basis vectors and two witnesses. It did not execute the FGF024 worker's code, recompute maps, build a new response, fit observations, or survey extra pressure models.

## 5. Instrument and framework limitations

FGF019's operator uses a particular spherical piecewise-linear pressure basis/support, center, assumed distance conversion, tangent-plane FFT beam approximation/cutoff, actual mask weights and twelve annular bins. Equality in these compressed rows is not equality in the full map, another binning or another support. Rationalizing binary64 coefficients certifies the stored finite matrix, not the exact continuum projection or provenance of an instrument calibration.

The aligned and orthogonal rows are synthetic algebraic designs, not available calibrated outer-annulus measurements. Their construction does not establish which real detector response combinations realize them. Extra physical rows require the same basis, beam, center, distance, pixel mask/weights and background treatment. Noise, calibration uncertainties and near dependence can invalidate practical recovery even where exact rowspace identification holds; no covariance or conditioning bound is supplied here. The synthetic baseline/witnesses fit their own model data, not the actual observed map bins.

No electron-to-total pressure conversion, gas-density inference, MOND force, source mass or mass discrepancy was calculated. Such a later bridge must preserve both a0 normalizations, distinct constant-vacuum/frozen H histories and separate Q/RAR/registered M laws. This finite target-information result does not choose a gravitational branch or close the physical theory.

## Verdict matrix

| Obligation | Status |
|---|---|
| Generic target-only rowspace criterion | Passed |
| Strict-interior necessity under inequalities | Passed with essential hypothesis retained |
| Complete exact nullspace and stored rank | Passed by direct rational certificates plus modular determinant |
| Aligned, wrong-coordinate, orthogonal and damaged-row controls | Passed |
| Strictly positive decreasing two-sided witness | Passed for synthetic fixed-offset data |
| Root provenance and fresh review record | Hashes checked; bounded review manifest validated |
| Actual additional detector row or noisy inference | Not established |
| Continuum, force or observational acceptance | Not established |

No gap requiring rejection was found in the stated finite mathematical claim. The next physical obligation is to specify and calibrate actual additional response rows before using their reduced rowspace and uncertainty propagation to infer the target.
