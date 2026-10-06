# Independent external-field operator review

Accepted in the stated stationary NR, constant-boundary and external-dominated scope. I reconstructed the constitutive Jacobian, general-n Green normalization and matched QUMOND response from the field equations before inspecting the author's claimed differences. No blocking mathematical correction was found. This does not accept a projected Solar-System Q2 prediction, a globally admitted nonlinear source solution or full covariant health.

## Exact inspected inputs

- REPORT.md: SHA256 0b59ed2f18c6e1a90347f65fa99846490c9287e4efd2a444e24cb5089cb886ff.
- checks.py: SHA256 3eaaa9e03f28df6d64982e637b4aebd0204dc07d1c4b2785e64c4539a020c884.
- contract.json: SHA256 32a1de6f7ea8bbe5c7fea276cb5196274a217093442417fd19ad4c1dd8f74428.
- SOURCE_AUDIT.json: SHA256 d27f5cba35bc12f1c7c657cc0178abdd75e68b51030d941c29acf0d10ba89ed8.
- sources.json: SHA256 002040cacaaa708ffb565fa20addbc879c257ec24634ab6649cbd307707f5de1.

The inherited projected action's stationary source section was independently read, not treated as QUMOND by radial analogy. No author input was changed or author experiment executed by this reviewer. Current manifests were independently validated against the repository root.

## Actual operator and source normalization

Writing φ*=φ−hatφ and φ+=φ+hatφ, the actual varied stationary equations with zero twin source give div[μ(x)∇φ*]=ΩG_Nρ and Δφ+=ΩG_Nρ. Thus the physical potential is half the sum and half the star, under the stated source/boundary conditions. The factor one half cannot be absorbed into μ without changing the radial matching dictionary. The Newton potential satisfies Δφ_N=ΩG_Nρ with physical G_N from the parent tensor-to-Gauss normalization.

Let the external star gradient point along z, have magnitude a0 x_e>0, and assume |∇δφ*|≪a0 x_e in the domain of linearization. Differentiation of μ(|v|/a0)v gives Aij=μ_e δij+x_e μ'_e e_i e_j. Its eigenvalues are μ_e and μ_e(1+L_e), L_e=x_e μ'_e/μ_e. Hence μ_e>0 and 1+L_e>0 are precisely the local ellipticity hypotheses. They are not tensor/scalar stability of the covariant completion.

Set b=1+L_e and z'=z/√b. The star operator becomes μ_e Δ', while δ^(n)(x)=δ^(n)(x')/√b. Since Δ r^(2−n)=−(n−2)Ωδ, for n≥3 the star Green function is

ψ*=−G_N M[(n−2)μ_e√b]^(−1)(r_perp²+z²/b)^((2−n)/2).

Adding φ_N and dividing by two reproduces the displayed physical response. The √b source Jacobian and n−2 factor are both required. In dimensions other than n=3, the polar star coefficient is b^((n−3)/2)/μ_e; the special equality of the physical polar coefficient with radial ν must therefore stay four-dimensional, as the report does.

A distributional point Green source is formal at the center: it cannot satisfy external dominance there. For an actual compact nonlinear body the mass-normalized far monopole additionally needs an admitted decaying asymptotic perturbation. The full star flux then fixes the mass because the quadratic correction to the flux vanishes on large spheres: δ∇φ*∼r^(1−n) implies its quadratic flux scales as r^(1−n). This is a conditional matching argument, not existence or regularity of the nonlinear interior.

## Independent matched-QUMOND derivation

For the same radial kernel, y=μx and ν=(1+μ)/(2μ). Differentiating with respect to x gives K_e=dlnν/dlny=−L_e/[(1+μ_e)(1+L_e)]. This comparison also chooses aligned Newton-sum and star boundary vectors with y_e=μ_e x_e. A real nonspherical host does not automatically satisfy that relation or alignment.

Fourier inversion gives P_proj(u)=[1+1/(μ_e(1+L_e u))]/2, u=k_z²/k². Linearizing the separate QUMOND Poisson source gives P_Q(u)=ν_e(1+K_e u). Subtraction yields

P_proj−P_Q=L_e²u(u−1)/[2μ_e(1+L_e)(1+L_e u)].

Thus the two Fourier axial directions agree, whereas interior angular directions differ whenever L_e≠0. No inversion of a radial force law equates these operators.

In n=3 one can derive the QUMOND real-space potential directly: Δ^(−1)φ_N=−G_NMr/2 and ∂z²r=(1−cos²θ)/r, hence ψ_Q=−G_NMν_e[1+K_e sin²θ/2]/r. The projected star Green function instead gives its square-root angular factor. Their equatorial difference is −(√b−1)²/(4μ_e b). Expanding the projected factor, its cos⁴θ coefficient is 3L_e²/(16μ_e); using cos⁴θ=(8/35)P4+lower harmonics gives l4=3L_e²/(70μ_e)+O(L_e³). QUMOND's displayed linearized potential is quadratic in cosθ and has no l4. This is a far 1/r angular multipole, not an inner analytic r4 coefficient or a local solar tidal quadrupole.

The Newtonian all-angle local response condition follows independently: the transverse susceptibility fixes μ_e=1; the longitudinal then fixes L_e=0. This provides no universal lower bound on the inner Q2.

## Primary verification and remaining scope

I independently reopened [Milgrom 0911.5464v2](https://arxiv.org/pdf/0911.5464v2) on 2026-10-06. Equations 5–6 fix the QUMOND Poisson convention; 60/66 give the distinct asymptotic angular potentials and 67–69 give the constant-external-field linear operators. The text expressly distinguishes their boundary axes. The projected calculation is a half-Newtonian plus nonlinear-star operator, rather than an unsupported transfer of one of those pure theories.

I also reopened [Park et al. 2602.17884v2](https://arxiv.org/pdf/2602.17884v2): the exact version reports Q2=(1.6±1.8)×10^(−27) s^(−2) at 1σ with simultaneous ephemeris estimation. [Hees et al. 1402.6950v2](https://arxiv.org/pdf/1402.6950v2) was reopened for the historical convention. These retrievals authenticate the cited primary leaves, not an independent ephemeris likelihood or proof that the two-potential model obeys an AQUAL/QUMOND kernel-to-Q2 conversion. No original PDF byte hash is claimed.

The author preserves the right limitation: p57's internally dominated solar solution cannot be obtained from this constant-coefficient far Green function, even with an exactly matched radial law. New nonlinear star boundary/source matching is needed. Claude source-revision statements are a bounded snapshot recorded by SOURCE_AUDIT, not an audit of untracked output correctness or all concurrent Claude work.

## Bounded computational evidence

All four current a manifests independently validate against current input hashes: main 23/23; transfer-equivalence, inner-solar applicability and omitted-sum controls each 23/24 with the single intended rejection. I inspected the actual candidate substitutions and raw constitutive differentiation. The general-n harmonic check corroborates the Green solution away from its source; its delta normalization comes from the analytic coordinate/flux proof above. Numerical boundary values are conditional on the declared p57 kernel and aligned external field, not fitted solar predictions. No additional numerical run was needed for this independent analytic audit.
