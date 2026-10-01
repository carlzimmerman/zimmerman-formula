# Independent constitutive and finite-region review — 27 September 2026

**Normalized claim and primary verdict: proved as written.** At fixed positive a0 and G, the unshifted, singular point-baryon P2 hydrostatic family, for all positive host masses and radii, cannot be represented by a single-valued universal barotropic P(rho_d) without another state variable. Its displayed conditional constitutive derivative is correct, but interpreting it as a perturbative sound speed requires an extra constitutive assumption. This verdict is for these algebraic assertions, not the existence or stability of any full action.

Read-only sources: `constitutive/EQUATION_OF_STATE.md` (SHA-256 `0dd0826eed86a71bc1a70f21ddbde53d26440c66ad3d1cb2354f0b7b6719e8b4`) and `constitutive/eos_audit.py` (`ee24db66633042b344b832589c4aa46723b1eda10793e071a6e1085114670ae8`). No source changes.

## Dependency and obligation audit

The graph is: prescribed enclosed mass -> radial density -> strictly increasing density coordinate -> unique positive inverse -> distinct pressures at fixed density. Differentiating the same equilibrium curve gives the displayed slope; it does not close perturbation dynamics. All leaves here are direct algebra or stated model definitions; no external theorem is needed.

| Obligation | Status | Evidence |
|---|---|---|
| Density actually follows from enclosed mass | Passed | d[M sqrt(1+a0 r²/(GM))]/dr divided by 4 pi r² equals a0 M/(4 pi G r M_total) |
| Hydrostatic equation and density transformation | Passed | Independent source rerun; all three exact SymPy identities hold |
| Inverse and positivity | Passed | q=y/sqrt(1+y)>0; derivative (1+y/2)/(1+y)^(3/2)>0; positive quadratic root is the displayed y(q) |
| Fixed-density contradiction | Passed | C_M decreases with M, so q, y and P increase strictly at fixed rho_d>0 |
| Constitutive derivative | Passed | dP/d rho_d = sqrt(GMa0)/2 times (1+y)^(3/2)/(1+y/2) |
| Physical sound speed or full stability | Conditional | Requires the perturbative EOS and missing dynamics; the source correctly does not assert either |
| Arbitrary pressure offsets rescue universal EOS | Refuted on common open density intervals | Slopes themselves remain strictly ordered by mass, as shown below |
| Free-boundary dilation admitted in Fourier coercivity proof | Not addressed by that proof | It is outside periodic/decaying perturbations; exact conditional obstruction below |

The supplied main script passes **7/7**, and MUTATE passes **3/7**, failing exactly the equal-density and distinct-pressure checks for both footings. At rho_d=1e-23 kg/m³ and host masses 1e9/1e11 solar masses, pressure ratios are **10.1529797335** (a0=9.3603e-11) and **10.1149350126** (a0=1.1312e-10). Mutation gives ratio 1 and high-mass actual density 1e-24, so it catches removal of host dependence rather than merely crashing. Exact identities do not mutate and appropriately remain true.

Independent `constitutive_review_check.py` additionally derives density from the enclosed mass instead of accepting the script's density expression. Its **7/7 exact checks** pass. Raw reruns are `constitutive_eos_independent.json`, `constitutive_eos_mutation_independent.json`; independent check output also records source hashes. Commands used `/usr/bin/python3` on the two source modes and independent script, writing only in this review directory.

## Pressure-offset clarification

A radius-independent boundary subtraction P_tilde(rho;M)=P(rho;M)-P_edge(M) preserves hydrostatic gradients and dP/d rho. It can align two pressures at one chosen density, so the unshifted two-point contradiction alone must not be advertised as a proof against every shifted family.

A stronger direct argument is available. Write F(y)=(1+y)^(3/2)/(1+y/2). Then

    F'(y) = sqrt(1+y) (y+4)/(y+2)^2 > 0.

At a common positive density, M2>M1 implies y2>y1; both sqrt(M) and F(y) increase. Thus the EOS slope for M2 is strictly greater than for M1. No choice of constant per-host pressure offsets makes these curves the same differentiable function on any shared open density interval. For truncated hosts this argument requires overlap of the realized density intervals; disjoint intervals or agreement at one boundary point do not supply that contradiction. Entropy/environment/baryonic-field dependence remains outside this one-variable claim. The source's more cautious statement about offsets is therefore sound.

## Exact finite-sphere dilation caveat

Take the fixed-background quadratic kinetic functional used in the frame audit on a sphere of radius R, with uniform positive rho and uniform BW'' evaluated on the background. Here W'' means differentiation with respect to theta; if W is written W(theta/K), it includes the factor K^-2. Let the perturbation velocity be v(x)=lambda x. Its divergence is 3 lambda, while

    sigma_ij = (partial_i v_j+partial_j v_i)/2 - delta_ij div(v)/3 = 0.

Both the local shear-square compensator and the scalar projection compensator vanish. For the latter, this means a specified linear inverse Laplacian mapping the zero source to zero; a nonzero homogeneous solution would be extra boundary data, not a consequence of the shear source. The nonzero Fourier relation s=(2/3)theta is inapplicable to this affine free-boundary velocity field.

Since the volume average of |x|² is 3R²/5, the quadratic kinetic Lagrangian per volume is

    L_kin^(2)/V = (lambda²/2) [(3/5) rho R² + 9 BW''].

Equivalently, a displacement xi=epsilon(t)x gives this coefficient multiplying dot(epsilon)²/2. Therefore, if BW''<0, strict positivity on this admissible mode requires

    R² > -15 BW''/rho.

Equality leaves a zero kinetic direction; smaller R gives a negative one. This is a necessary condition for this mode, not a sufficient finite-domain positivity theorem. It quantifies the already declared finite-boundary caveat and is worth recording: increasing either shear coefficient cannot repair this mode because its shear is identically zero.

The qualification is essential. Dilation violates periodic/decaying conditions and fixed normal-velocity boundary conditions; the result applies only when the chosen region/interface prescription admits it. Extending the flow by zero outside the sphere produces interface distributions and is a different operator domain. Moving-boundary terms, density/metric constraints, field-dependent B and compensator coefficients, and any extra boundary dynamics have not been included. The exact remaining implication is whether the intended constrained matter-plus-region action admits this mode and what its complete reduced kinetic coefficient is. This review neither excludes an unknown covariant completion nor contradicts the stated periodic/decaying Fourier repair.

**Strongest safe conclusion:** the universal one-variable EOS obstruction is algebraically established for the stated family; constant pressure offsets do not cure it on common density intervals. Both shear repairs retain a quantitatively identifiable free-boundary dilation obligation. The cheapest next check is an explicit region boundary/constraint prescription, before adding further kinetic operators or interpreting the equilibrium slope as a sound speed.
