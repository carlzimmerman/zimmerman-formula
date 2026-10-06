# Independent second-order projected-mode source audit

Verdict: accepted for the exact relative-order-two, fixed-coordinate torus averaging chart specified in the report. No blocking mathematical error found. The negative curvaturelike mean source is a common lapse/trace-row result in that chart, not a complete nonlinear solution or a coordinate-independent no-go against cold abundance.

## Frozen inputs and records

- REPORT.md: `67954f18130df24505d0c22045188123ae7aca0727e87577dd8ae5e2acd5ce93`
- checks.py: `5e5ac435fddb4a280be26d98317b24e651c60eb142fcf0750d8a3d181253120d`
- contract.json: `95c89abec2a8ab87ccafbf5da965085c21d6d9b5dd2c6d8f81018d26a7082891`

Only this review was written; no author inputs were changed. Independently validated all four current manifests against the repository root: main_a, control_canonical_a, control_geometry_a and control_dust_a return valid evidence/exit zero. Main is 20/20; the canonical and omitted-geometry controls each fail the source identity (19/20), while the zero-pressure mutation also fails conservation (18/20). Development preflight is not substituted for these records. REPORT is outside the execution inputs.

## Raw ADM and common variation reconstruction

For the plane metric, direct spatial curvature gives exp(−2u)(−4v_xx+4u_x v_x−6v_x²). The directional extrinsic-curvature contraction is −4κ_xκ_y−2κ_y². In the exponential chart, multiplying the two kinetic expansions by exp[±ε(T−ν)cos/2] and averaging cos²=sin²=1/2 independently reproduces

C=A_x Zdot+Zdot²/2+hX(A_x+2Zdot)+3h²X²/4−hPβT,

where X=T−ν, T=3Z+E and A_x=Zdot+Edot+Pβ. The intrinsic-curvature contribution after the same averaging is KNa k²(Zν+Z²/2). The actual projected interaction contributes KNa k²ν²/2, so their sum is KNa k²(Z+ν)²/2. The constant geometric-mean volume is independent of relative variables in this symmetric exponential chart; it is retained in the common background action, not silently deleted as a source. Thus the raw coefficient is precisely L2=−Ka³C/N+KNa k²Q, Q=(Z+ν)²/2.

Varying N while keeping the declared relative coordinate variables fixed gives −L2_N/a³=−K(C+PQ) at N=1. Varying ln a requires both the explicit a dependence, including P=k²/a², and the time derivative of L2_h. It gives [a L2_a−d(L2_h)/dt]/(3a³). These variations must precede the relative constraint substitution. The common background Einstein coefficient is 4K, the sum of the two individual M=2K coefficients, which agrees with the source normalization used here.

After imposing the inherited linear constraints and Z=Z0+Z1/a, ν=−Z1/a, independent substitution gives ρ_eff=−K(H²ν²+PZ0²)/2 and p_eff=−ρ_eff/3. The coefficient therefore scales as a^(−2) and obeys the stated trace-row continuity relation. The shift derivative is P(Zdot−hν), checking the unreduced constraint convention. On the first-order relative constraints the raw kinetic coefficient is the displayed time boundary −(KH/2)d(a³ν²)/dt. Its presence explains why using the boundary-corrected reduced Hamiltonian as the raw gravitational lapse source changes the result.

## Separately varied interaction tensor

On D=ν+T=0, the full proper four-volume ratios coincide to first order. In the sum of the two normal-frame density variations, a second-order relative volume correction enters with opposite signs, while the derivative lapse Euler pieces multiply the first-order volume difference and cancel at order two. The common spatial variation of the remaining gradient action is independently L_I2=KN(a_y a_z/a_x)k²ν²/2. Its lapse derivative gives summed ρ_I=−KPν²/2; directional length variations give p_parallel=ρ_I and p_transverse=−ρ_I. The trace is −ρ_I/3. This retains the gradient measure variation as well as its inverse-metric variation.

The density alone scales as a^(−4), but the isotropic continuity residual is −2Hρ_I. Perturbed connections acting on opposite first-order sector stresses and nonlinear Einstein terms cannot be ignored in treating the separate summed tensor. It is not an isolated conserved homogeneous radiation or dust fluid. This distinction is independent of the total effective mean source derived above.

## Boundaries of the conclusion

The fixed coordinate torus average and symmetric exponential common/relative split are part of the calculation. The proper spatial volume already differs from a³ at order two by ν²/16 in each sector. A different geometric background definition can therefore rearrange the mean contribution. In particular the frozen mode has zero first-order Bardeen Weyl curvature while contributing to this coordinate source; it is not legitimate to promote that source into an invariant energy for every foliation state.

A single plane wave produces anisotropic mean stress. The isotropic common lapse/trace rows do not solve the homogeneous shear equations or the second-order relative metric/clock equations. A Bianchi-I mean response, boundary/initial data and a geometric expansion observable are still required for a completed solution. The positive quadratic canonical H/a³ and the linear signed dustlike mode are different source questions; neither supplies a positive homogeneous cold abundance by itself. The present exact calculation rejects the shortest Hamiltonian-to-dust inference in its declared chart, while leaving full nonlinear admission and observable backreaction open. No primordial spectrum, recombination transport, full health or 32π selector is established.
