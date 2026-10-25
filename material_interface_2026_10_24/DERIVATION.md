# Material-supported interface, MI-1

This is a new conditional constitutive hypothesis, not a derivation of a microscopic carrier or its charge production. It continues LD-17/18's corrected common-quadrature energy and stable response function. Neither a target density nor a target radius enters the energy. The previous density-free charge capacity is replaced, not added a second time. Density, phase and the outer reservoir remain variational.

Use the previous dimensionless spherical units, with angular factors absorbed. Set q=sin²(πx/2), u(r)=r⁻²∫₀ʳ s²ρq ds, F(u)=u²/(1−u), f(ρ)=ρ/(ρ+ρs). Add

    Ec = k/I,  I = ∫ r² F(u) f(ρ) D(q′) dr,
    D(v) = sqrt(v²+δ²)−δ.

Here k is proportional to a supplied conserved charge squared. D is the same smooth total variation as the previous interface tests. Capacity vanishes in vacuum and in a homogeneous phase. The finite volume implementation uses the harmonic mean of the two adjacent densities at a face, so a populated cell cannot supply capacity across a vacuum neighbour. All gradients used by the optimizer include density dependence, enclosed mass dependence, and phase dependence through this same action.

## First variations and all additional forces

Let α=k/I² and L(r)=∫ᵣ∞ F′(u)f(ρ)D(q′)ds. Functional derivatives below are per volume r²dr, at fixed independent ρ and q:

    μρ,c = −α [F f′ D + q L],
    cq,c = δEc/δq = −α [ρ L − r⁻² ∂r(r² F f D′)].

For species densities ρT=ρq and ρF=ρ(1−q),

    μT,c = μρ,c + (1−q)cq,c/ρ,
    μF,c = μρ,c − q cq,c/ρ.

The extra force per unit species mass is −∂r μi,c. Thus the carrier contributes both a local density attraction −αF f′D and nonlocal response and conversion forces. Omitting any of them would give a false material balance. At ρ=0 the fraction coordinate is singular; the calculation keeps a stated positive mass floor and must be checked against refinement before a continuum claim.

In a pure interior away from all interfaces, D=0 and L is constant: μT,c=−αL, μF,c=0. Their radial derivatives vanish there. Therefore the cold bulk relation remains g²/(1+g)=gb+gF. This is only a bulk identity: shell mass, free material and transition forces can still spoil the actual galaxy law through the transition. No comparison against the target law enters the minimizer.

## Material stiffness and boundary force

For any coupled perturbation,

    δ²Ec = 2k(δI)²/I³ − k δ²I/I².

At fixed response and phase, f′>0 and f″<0. The local density part of −αδ²I is positive. This offers a concrete means to retain matter without the unbounded linear-density capacity that favours concentration. It does not establish positivity of the full coupled Hessian: the response and mixed terms remain.

For a thin monotone interface with a fixed jump, I≈R²F(MT/R²)f(ρR)|Δq|. At fixed MT,

    I′/I = −2/[R(1−uR)] + (f′/f) dρR/dR,
    FR,c = k I′/I².

The response part is inward; it must balance the bulk pressure and every pre-existing interface force. The density derivative cannot be suppressed when assessing that balance. Generalized force for the full discretized system along a specified material-and-phase displacement v(R) is −∇E·v′. At an equilibrium its restoring stiffness is the full constrained second variation, with density relaxation subtracting the appropriate Schur complement. A positive fixed-density curvature or an unchanged crossing-cell index is not sufficient.

## Declared first experiment

MI-1 tests n64, domain4, beta20, ell30kpc, K3, rho_s=.01 and k=0,.003,.03,.3,3, each transferred independently and species-conservatively from LD-18's depleted state. SLSQP has 1200 iterations per case and the whole run has a 240s wall cap. Check derivatives at three step sizes before optimization. Report mass in the historical 17–43kpc gap, actual gravity errors to15/30/50kpc, outer conversion, density KKT residuals, cap slack and interpolated boundaries. This is a screen, not a resolution or formation certificate. Conserved charge is supplied, not formed by this calculation.

## MI-7: require a genuinely mixed carrier

MI-2–6 exposed capacity storage in small core phase variations, with a separate outer phase crossing sitting beyond a new vacuum gap. A phase crossing alone is not a material boundary. MI-7 replaces f by f b(q), b=[4q(1−q)]², without a prescribed radial window. Then

    Lb(r)=∫ᵣ∞ F′ f b D ds,
    μρ,c=−α[F f′ b D+q Lb],
    cq,c=−α[ρ Lb+F f b′ D−r⁻²∂r(r²F f b D′)].

Use the same species transformation and force −∂rμi,c above. Both b and b′ vanish in pure phases. This is a tested constitutive variant, not a proven microscopic consequence. It suppresses weak core variations but cannot prohibit the optimizer from creating a new mixed layer; any such layers must be reported. MI-8 continues pressure from the compact boundary instead of initializing at the remote-gap branch, and uses the unscaled energy with ftol1e-14 because the previous E/100 tolerance admitted appreciable central material residuals.

## Charge-free material balance: why the matched control matters

In MI-9, removing charge at the same beta2, ell10, K10 retains a continuous transition. Thus this branch cannot be attributed to the new carrier interaction. The useful change relative to LD-18 is the coupled pressure/barrier/stiffness regime. Narrowing ell to3 creates a new empty interval even when integrated gravity looks better; that is not a solution to depletion.

For the existing charge-free continuum action let

    A = W′(u) + beta C F′(u)s(x) + (ell²/2)F′(u)(x′)²,
    Psi(r) = ∫ᵣ∞ A(s)ds,
    Xi = beta C F(u)s′(x) − ell² r⁻²∂r[r²F(u)x′],
    hF = (5/2) K [rho(1−q)]^(2/3),  hp=dq/dx.

With gravitational potential Phi including baryons and all material, the complete first variations per volume are

    μrho = Phi + q Psi + (1−q)hF,
    cx = rho hp(Psi−hF) + Xi.

The species chemical potentials and forces in a mixed cell are

    μT = Phi + Psi + (1−q)Xi/(rho hp),
    μF = Phi + hF − q Xi/(rho hp),
    force_T = −∂r μT,  force_F = −∂r μF.

These formulas include the response of enclosed T mass to density, the response dependence of the barrier/stiffness, conversion pressure, and the phase-gradient stress. At equilibrium cx=0 and material transport gives μT=μF=constant wherever both species are mobile and present. The pure-phase transport limits must be taken in the original action: in a pure T region μT=Phi+Psi and in pure F μF=Phi+hF. Division by hp at an endpoint is not a numerical prescription.

Inside a pure T core, A=W′ and ∂rμT=g−u/(1−u). Thus g²/(1+g)=gb+gF remains the derived bulk law, without adding a fitted force. Within the actual mixed transition the Xi and pressure terms need not vanish: the measured full radial gravity error is reported separately. Parameter selection here is a constitutive experiment, not a microscopic derivation of beta, ell or K.
