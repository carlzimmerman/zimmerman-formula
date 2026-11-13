# Independent mathematical review of finite shape-capacity probe

**Primary verdict: conditional on the numerical deflection arrays and the four-position association.** The orthogonal-projection elimination and the diameter lower bound are mathematically valid. The result supports finite fixture-specific necessary-condition failures; it does not exclude a continuous photometric uncertainty region or establish a full-theory exclusion. This is a cold reconstruction of the algebra from code by a delegated reviewer; field solver correctness is not independently re-established here.

## Exact claim and dependencies

Audited `shape_capacity_probe.py` and completed `shape_probe_01/result.json`, with conventions checked against `aqual_lensing.py::geometry` and `projected_deflection`. Twenty fixtures:5 light-shape points (COOLEST point and4 Cartesian n/Re marginal3sigma endpoint pairs)×2 aperture-mass choices(median,+3 upper-error units)×2 inclinations(90°,50°). Fixed projected q, center, orientation; constantM/L oblate light-mass model and recomputed analytic pixel-union aperture fraction. Four supplied position vectors theta_i are assumed to be images mapping into one source region with diameter≤0.3arcsec. External convergence is excluded from this calculation.

Dependencies: coordinate association/convention → supplied positions; light/mass/aperture assumptions → fixed fixture; AQUAL field+projection → unreduced alpha; ordinary finite-dimensional Euclidean projection → eliminated SSE; elementary pair-distance identity → necessary diameter lower bound. The last two implications pass analytically. The numerical-field and observational leaves remain conditional.

## Algebra reconstructed

For fixed unreduced alpha_i and efficiency b∈[0,1], let y_i=theta_i−b alpha_i−Gamma theta_i, where Gamma=[[g1,g2],[g2,−g1]]. An arbitrary source origin contributes a common2vector. Flattening in point-major(x,y)order produces exactly code columns d1,d2,g1=(X,−N),g2=(N,X). Signs of shear columns do not matter to their span. Changing the shear reference origin only adds a common vector, already included.

With T these four columns, orthogonal P=I−QQᵀ annihilates both center and shear. For every choice of source center and arbitrary real shear coefficients, the centered source-vector SSE is at least ||P(theta−b alpha)||². QR is safe for the supplied nondegenerate positions; code verifies PT≈0 and P²≈P at1e−14. A robust reusable implementation should explicitly check rank(T)=4 and ||P−Pᵀ|| too; the present QR construction is symmetric by construction. The code's clipped scalar b=clip((Ptheta·Palpha)/||Palpha||²,0,1) is the exact minimizer of that quadratic when ||Palpha||>0. A zero denominator would need a special case in a generic implementation; it is not evidence of an error in these finite completed fixtures.

For any four2vectors y_i with centroid ybar and diameter D,

sum_i ||y_i−ybar||² = (1/4) sum_{i<j} ||y_i−y_j||² ≤ (6/4)D² =1.5D².

Combining inequalities gives D≥sqrt(SSE_min/1.5). The six-pair bound is conservative and need not be attainable for four planar points. It remains a VALID necessary lower bound; using it does not claim exact optimal diameter. In particular a lower bound below0.3 proves nothing about the existence of a fit. No source center/shear choice can evade a strict lower bound above0.3 for the same fixed alpha fixture.

## Efficiency and nuisance scope

`projected_deflection` multiplies the LOS integral by Dls/Ds; dividing its zs=3 output by geometry ratio removes that factor. Lens distance scale is fixed by zl. Thus the later scalar b multiplies an unreduced deflection, rather than double applying source distance. The code's flat positive-density background geometry gives0<Dls/Ds<1 for sources behind the lens. Allowing ALL[0,1], including b=1, is a relaxation beyond finite physical source distances: a rejection on that enlarged set is conservative. b here is efficiency, not source angular position. Every listed optimum is atb=1, but this alone is not a recovered source redshift.

Shear is genuinely unbounded in this necessary test; no shear-amplitude prior is used. If physical shear carries an efficiency factor, independent arbitrary shear coefficients still enlarge the admissible set and hence preserve the necessary rejection. This is ONLY a uniform trace-free linear external shear. It is not arbitrary tidal structure, a separate mass plane, external convergence, or an external-field modification of the nonlinear AQUAL solution. A convergence term scales theta and survives P, so it can change this witness and is explicitly outside scope.

## Reading the actual result

At nominal apertureSED mass, all10 finite shape/inclination fixtures have diameter lower bounds>1.15arcsec (minimum1.15608845). The nominal COOLEST point is1.18514838arcsec edge-on and1.28836082arcsec at50°. These are necessary-condition failures of the0.3 gate conditional on the inputs.

At +3 upperSED-error units,9 of10 fixtures still have lower bound>0.3. The lowerRe/uppern,90° fixture gives SSE=.1287712128 and lower bound=.2929973979<.3. **That fixture is INCONCLUSIVE under this necessary witness, NOT a passed lens fit.** It establishes neither existence of a source/shear solution satisfying the diameter gate nor a viable pixel-image model. Also the nominal-shape +3mass edge-on bound.33091568 is near enough to the gate that numerical-model and photometric-systematic qualifications matter.

The marginal n/Re endpoints are not a joint posterior contour. Finite corners plus the point do not exhaust or bound the intervening continuous shape box: no monotonicity/convexity of the nonlinear field witness in n/Re has been proved. Two inclinations do not cover all admissible inclinations; q/center/angle and stellarpopulation assumptions were not varied. '+3sigma' is an arithmetic conditionalSED fixture, not a global3sigma confidence/exclusion statement. A0 was not varied. The0.3arcsec association gate itself must be justified observationally rather than promoted to an axiom of the theory.

## Numerical and formal-certification limits

Reported field residual≈1e−8 and depositedmass ratios≈.99986–.99995 are useful solver diagnostics, NOT interval bounds on the deflections or witness. This review did not rerun expensive fields or certify boundary/LOS/grid errors. Existing convergence studies must support precision claims. A later Lean finite-array witness can certify exact arithmetic inequalities for specified rounded arrays, but cannot by itself certify the PDE, alpha rounding error, observational association, stellarM/L, or environmental assumptions. Those bridges must be separately explicit.

Strongest safe statement: the projection/diameter algebra is sound; the20 recorded numerical fixtures produce the stated necessary-condition bounds, with one high-mass endpoint inconclusive. This supplies conditional finite-fixture tension, not a full-theory exclusion or a fit pass at that endpoint. No audited inputs were mutated.
