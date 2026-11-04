# AZ28: remove the mixed-invariant fold; normalization remains free

κ = ½ FITTED; not theory closed

**PASS** for removal of AZ27's particular momentum fold and for the frozen, locally flat principal-mode tests; **NO VERDICT** for global nonlinear stability; **FAIL** for width selection; **NOT EVALUABLE** for physical κ. Both canonical and alt are separately assigned these grades. No full requirement or RQ3 row is established. Criteria commit 018dcc30b9.

The repair uses separate expansion and acceleration terms. This is a declared action choice, not a symmetry-derived physical mechanism. Constant-lambda clock dynamics and a curvature-squared k^4 repair already appear in sol61_push/CANONICAL_CLOCK_RESULTS.md. They are inherited mechanisms, not new discoveries. The new tests here address AZ27's fold, acceleration-direction dependence, and the stabilizer's actual sourced response.

## 1. Explicit action and exact momentum map

Take the same hypersurface-orthogonal preferred foliation and minimally coupled baryons, with

    S=B/2 integral N sqrt(gamma) [KijKij−lambda K²+R3−2Lambda
                                  +f(g²)−ell² R3²] + S_baryon,
    f(g²)=4A g−4A² ln(1+g/A),       g²=a_i a^i,
    B,A,Lambda,ell²>0, lambda>1.

Every coefficient is unselected. The curvature term contains spatial derivatives, not additional time derivatives in the preferred foliation. That fact alone is not a full health proof.

The exact momentum tensor is proportional to K^i_j−lambda K delta^i_j. Its trace map is (1−3lambda)K and its traceless map is the identity. Thus the momentum/velocity Legendre map has no acceleration-dependent fold: its eigenvalues cannot vanish in the stated lambda>1 domain. Unlike F((-C2 K²+C1 g²)/m²), the acceleration term cannot change its trace derivative.

This removes the particular local algebraic obstruction found in AZ27. It does not solve the spatial momentum constraint globally, exclude all boundary-value branches, or establish global evolution. A constant-sign constraint coefficient is not by itself a physical kinetic-energy sign; the latter is checked after eliminating lapse and shift below.

## 2. Acceleration Hessian and directional stability

Let y=g/A. The coefficients of the lapse-gradient quadratic form parallel and transverse to the background acceleration are

    alpha_T=f_s=2/(1+y),
    alpha_L=f_s+2s f_ss=2/(1+y)²,       s=g².

For a wave making angle theta with that acceleration,

    alpha_theta=alpha_T+(alpha_L−alpha_T)cos²(theta)
               =2[1+y sin²(theta)]/(1+y)².

For every finite y>0, 0<alpha_L<=alpha_theta<=alpha_T<2. At y=0 the continuous Hessian equals 2 in every direction. No acceleration direction recreates the AZ26 wrong-sign gradient in this local test. Positivity is not uniform as y tends to infinity, so it cannot automatically supply a global coercive estimate.

On locally flat spatial geometry with frozen coefficients, eliminating lapse and shift gives the scalar principal bracket

    C ζdot² − [G_theta k²+16ell² k⁴] ζ²,
    C=2(3lambda−1)/(lambda−1)>0,
    G_theta=2(2−alpha_theta)/alpha_theta>=0.

Hence omega²=[G_theta k²+16ell² k⁴]/C>0 for k>0. At g=0 this reduces to the inherited k^4 result

    omega²=8ell²(lambda−1)k⁴/(3lambda−1).

The tensor has the ordinary local flat principal term: its linear spatial Ricci scalar vanishes for transverse-traceless perturbations, so this R3² term does not alter that flat quadratic tensor dispersion. These are frozen local principal tests. Background curvature, coefficient derivatives, matter dynamics, long-wavelength gravitational modes and nonlinear constraint propagation are not thereby proven stable. A local field configuration is not being claimed as a solved galaxy background.

## 3. The stabilizer changes the sourced static response

Without appreciable spatial-curvature corrections, the weak-static constitutive law is

    mu(g)=1−f_s/2=g/(A+g),
    mu(g) approximately g/A for g<<A.

Thus A is the putative deep-force scale, still a freely assigned coupling. The stabilizer cannot simply be ignored when calibrating the actual force. Retain both weak-static metric potentials, lapse Phi and spatial Psi. In a locally isotropic linear test, the Fourier action is

    L=B/2 [2k²Psi²−4k²Phi Psi+alpha k²Phi²−16ell² k⁴Psi²]−rho Phi.

The exact linear constraints are

    Psi−alpha Phi/2=−rho/(2B k²),
    Phi=(1−8ell² k²)Psi.

Therefore

    Phi=−rho(1−8ell² k²)
             /[2B k²(1−alpha/2+4alpha ell² k²)].

For the actual zero-acceleration background alpha=2. Keeping alpha symbolic provides a separate constraint check and the known Newton limit alpha=ell=0. This expression is not asserted for a general nonzero-gradient anisotropic source; the angular principal test above has a different declared scope.

For 0<alpha<=2 and k>0 the denominator is positive. There is no pole at k²=1/(8ell²); instead the lapse response vanishes there and changes sign above it. No conclusion about an observed spatial force profile follows without its source transform and boundary conditions, but the stabilizer demonstrably changes the force response. Calibration to ordinary Newton gravity requires a justified regime with ell k small and the appropriate high-acceleration constitutive limit. No measured or fundamental value of ell has been supplied. This is why the stable principal dispersion is not a complete operational force model.

## 4. Vacuum and the remaining freedom

On homogeneous flat slices g=R3=0. The lapse equation is

    3(3lambda−1)H²=2Lambda+2rho/B,
    H0²=2Lambda/[3(3lambda−1)] in vacuum.

The width A and the spatial stabilizer ell do not enter this vacuum equation. Conversely the local sign conditions require A>0, lambda>1 and ell²>0, but impose no equality tying A to Lambda or H0. All positive A remain admitted by the tested gates.

If a future sourced calibration justified G=1/(8pi B), effective vacuum density 3BH0² and a0=A, the familiar conditional dictionary would give b=(H0/(2A))sqrt(3/(8pi)) and κ=1/(2b). Those identifications have not all been established for this completed action. Even conditionally, the ratio A/H0 remains free. The repair supplies no equation selecting b=1 or κ=1/2.

## 5. What remains before a fully stable completion could be claimed

The exact momentum map is fold-free, and the specified local principal modes pass. The requested **fully stable nonlinear completion has not been established**. Required work includes the curved-background constrained symbol, well-posed evolution with matter and boundary conditions, source matching across the stabilizer scale, and a controlled quantum/cutoff interpretation. Earlier finite-shell Lifshitz work in the record also warns that a chosen classical cubic is not automatically radiatively protected. We did not repeat that loop calculation or use it as a new result.

No expensive galaxy run was launched on the assumption that these unproved properties hold. A credible next calculation is the curved, sourced constraint system with this exact action, retaining the spatial-curvature term and testing its domain of validity. An independent normalization principle remains necessary even if that calculation passes: separability and positive coefficients by themselves leave the vacuum and force scales independent.

## Evidence

`results.json`: **23/23** checks, including the all-angle Hessian identities, exact constant trace Jacobian, constrained scalar action, inherited k^4 known answer, weak-static source constraints and vacuum equation. Both sign mutations bite. Lean verifies three finite rational controls and rejects the false positive-dispersion claim for the wrong stabilizer sign; it does not certify global stability or physical κ. Interval proofs and interpretation are self-reviewed. No observational error or significance is assigned to the exact control values.

Reproduce: `python3 astra_goal_2026_11_03/P3/AZ28_separable_fold_repair/run.py`. Input hashes and versions are recorded. Free A,lambda,ell,Lambda,B and initial/boundary data are unselected/FITTED if assigned. No new data, species, cold sector, scans, heavy simulations or push.
