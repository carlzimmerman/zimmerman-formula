# Independent robust-tail review

I reconstructed the map, constitutive derivative, moment range and EFE estimate directly. The analytic theorem is sound under its declared positive, smooth, strictly decreasing, finite-moment response assumptions and the already audited QUMOND quadrupole kernel. Initial numerical-baseline normalization needed correction; final repair acceptance/pins will be appended below. I did not edit or execute author inputs.

## Exact map and admissibility

For the stated symmetric smooth step, S'=θ∈[0,1], S''≥0 and ∫₀¹θ=1/2, so S=y−3Y/2 beyond 2Y. Convexity gives yS'−S≥0. Direct subtraction yields

T_L−yT_L'=(1−1/L)(yS'−S)≥0.

Also T_L'≥1/L>0 and y/L≤T_L≤y; the map is increasing from the identity portion and T_L≥Y for y≥Y. Consequently f_L=f₀∘T_L is positive, strictly decreasing and pointwise no smaller than f₀. Strict decrease concerns the function; f₀' need not be strictly negative at every point. With α=yT_L'/T_L∈(0,1],

1+f_L+yf_L'=(1−α)(1+f₀(T_L))+α[1+f₀(T_L)+T_Lf₀'(T_L)]>0.

This is a genuine exact finite deformation inside the declared NR constitutive class; it is not an infinitesimal unverified positivity assertion. The flat exponential step supplies the C-infinity theorem. The finite polynomial ramp in the script is only C2 at its joins; using it numerically does not prove the universal smooth construction but is consistent with its shared inequalities.

## Finite moment and complete upward range

Since f_L≤f₀(y/L), C_L≤L²C₀. Every finite L therefore has a finite moment. On a compact L interval, y f₀(y/Lmax) gives an integrable majorant, proving continuity. For y∈[LY,2LY], L≥2, the affine tail gives T_L=y/L+(1−1/L)3Y/2<4Y. Hence C_L≥(3/2)L²Y²f₀(4Y), which diverges with L. This argument never uses an infinite-L kernel as admissible evidence.

C_L is in fact strictly increasing for L>1: S>0 on a set of positive measure, ∂T_L/∂L=−S/L²<0 there, and f₀ is strictly decreasing. Thus every finite target ≥C₀ is reached exactly by a finite L (uniquely for targets above C₀). This is only an upward range; the theorem does not remove previously derived positive-tail lower bounds or permit arbitrary downward changes.

## Uniform quadrupole control

The parent field-equation operator is Q₂(e)=−9a₀/(4r_M)∫f(y)√y F(e/y)dy. Its authenticated analytic F has F(q)=q²/10+O(q⁴) and no singularity on 0<q≤1/2. Therefore B=sup|F(q)|/q² on that interval is finite; no sampled numerical estimate of B is needed. For Y≥2E the changed tail never crosses the e=y shell. Since 0≤f_L−f₀≤f₀(Y),

sup_(0<e≤E)|ΔQ₂|≤9a₀ B E² f₀(Y)/(2r_M√Y).

The factor 2 comes from ∫_Y^∞y^−3/2dy=2/√Y. This bound is uniform in L, tends to zero with Y, and justifies choosing Y for the tolerance before choosing L for the target moment. It is consistent with exact continuum moment identification: no finite member is asserted to have exactly identical Q₂ on all external fields.

The exact response equality is equality of the constitutive kernel on y≤Y. It gives exact full QUMOND fields if the Newtonian field stays within that range throughout the source domain and the boundary data agree. It does not automatically preserve arbitrary finite-radius galaxy forces when unresolved central regions visit y>Y: changed nonlocal phantom sources can influence those forces. It also preserves neither all multipoles/orbital likelihoods nor full covariant health or an independently established vacuum-action dictionary. These restrictions are essential to the scientific conclusion.

## Initial defect and required repair

The initial report/script claimed C₀=π/8 for f₀=y^−1/2(1+y)^−5/2. Independently integrating y f₀ gives Beta(3/2,1)=2/3. Beta(3/2,3/2)=π/8 would require exponent −3 instead of −5/2. The wrong upper bound at L=1 conflicts with the actual numerical integrand, so this was a real finite-control normalization defect, not an interpretation disagreement. I requested correction of the exact baseline and all relative bounds/control thresholds before freezing. The map and uniform EFE theorem do not depend on this baseline number.

For the retained exponent −5/2, the report's other source bound is correct: 1+f₀+yf₀'≥1−2√y/(1+y)^(7/2); the squared subtractand has maximum (2/3)(6/7)^7<1 at y=1/6. The baseline therefore remains admissible with the repaired C₀=2/3.

## Repaired final acceptance

The final report/script now use C₀=2/3, exact Beta(3/2,1), and consistent finite-control thresholds. The report explicitly separates constitutive equality from generic global galaxy force preservation. I inspected these repairs directly. The restricted analytic theorem and corrected computation are accepted; no blocking mathematical correction remains. Pinned final mathematical inputs:

- `REPORT.md` SHA256 `93b9685c3fee6f7b6a72a8668782c0107d4fa62300b0c8d8fe5837d35b8dff51`.
- `checks.py` SHA256 `87a93ae65220e81b06b794b7872dbcf66e9f0d7da3d32b81e24ac696f5613183`.

Historical a-run inputs were preserved by the author; fresh b-runs are being produced. This peer note establishes the mathematical reconstruction and repair acceptance, not an assertion that pending manifests have already validated.

Final fresh-run check: independently validated current main_b and control_bound_b manifests with --root repository. Main passes 19/19; control fails only CONTROL_bounded_EFE_weight_bounds_moment as intended. Input/output freshness holds for both records. The finite examples corroborate the stated bounded controls; the analytic proof establishes the universal theorem.

## General-dimensional extension accepted

Independently read GENERAL_DIMENSION.md and the parent exact angular operator. No mathematical correction is required. Final pins:

- GENERAL_DIMENSION.md SHA256 `c480784281b4657d22518bb117c7985cbb78b415ab9c86e922fe96e9299ca028`.
- Parent general_dimension/REPORT.md SHA256 `6396c57536a117e2a6c223754d87e5602248356eedea4ecdd473ec1a3641c412`.

The essential small-q cancellation can also be reconstructed directly. Set τ=1+qz in the parent's shell integral; then ξ=−[2z+q(1+z²)]/[2(1+qz)]. The angular measure factors as

(1−ξ²)^((n−3)/2)=(1−z²)^((n−3)/2) [1+qz−q²(1−z²)/4]^((n−3)/2)/(1+qz)^(n−3).

On |q|≤1/2 the remaining factors are uniformly regular for each fixed n, so the weighted compact integral is analytic. At q=0 its numerator is nz²−1, whose weighted integral vanishes since the weighted mean z² is 1/n. The combined substitution (q,z)→(−q,−z) preserves the integrand, so its linear term vanishes by parity. Thus F_n(q)=O(q²) follows for every fixed integer n≥3, rather than from sampled dimensions. The constant B_n is finite by the removable zero and compact continuity; no bound uniform in n is inferred.

The tail map/source convexity and moment range are dimension-independent. With p=1/(n−1) and changed support y≥Y≥2E, the quadrupole weight estimate is |y^p F_n(e/y)|≤B_n E² y^(p−2). Independently integrating gives ∫_Y^∞ y^(p−2)dy=Y^(p−1)/(1−p), finite because 0<p≤1/2. Since Δf≤f₀(Y), the reported uniform bound follows, remains independent of L and tends to zero as Y grows. The same target moment C=∫yf is justified by the parent's Mellin change e=yq, not a guess about relativistic vacuum coefficients.

For n=3, c₃=9/8, p=1/2 and F₃=−2F_parent imply B₃=2B_parent. Hence c₃B₃/(1−p)=9B_parent/2, reproducing the exact 3D prefactor and units a₀/r_M. No Einstein-coupling or covariant vacuum normalization is identified by this calculation. Its conclusion is the same bounded-response, finite-precision upper-moment nonidentifiability for each fixed formal n; generic galaxy/orbit, all-dimensional uniformity and covariant health claims remain excluded.

GENERAL_DIMENSION.md is outside the unchanged 3D execution inputs. No rerun is warranted for this analytic extension; the already validated main_b/control_bound_b evidence retains its original finite 3D scope.
