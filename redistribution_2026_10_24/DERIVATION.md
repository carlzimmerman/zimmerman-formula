# Redistribution with phase-local material stiffness

Target remains simultaneous material/conversion equilibrium, original baryonic galaxy law through50kpc, a populated transition, restoring finite boundary and a free exterior. Radius and density may change. Total available mass remains5.364Mb; no law-error penalty or mass-profile constraint is present in the free experiments.

The prior budget implies M(<50)=4.801579Mb and M(>50)<=.562421Mb. At the old58.9289kpc boundary the law would require5.744122Mb, exceeding the entire supply. The old radius is not imposed. This is a constraint on redistribution, not an exclusion of a moved boundary.

## Release control

TF-2 supplied an exact-law state using external enclosed-mass constraints. RD-1 removes them and minimizes the original energy with only total mass, positivity and response-cap constraints. This distinguishes a new equilibrium basin from a profile that requires external holding forces. A return to the old branch would rule out that initialization as a solution at these constitutive parameters; it would not exclude every original-energy basin.

## New constitutive route

Add the positive energy

    Eκ=(κ/2)∫r² b(q)[∂r sqrt(rho)]²dr,
    b(q)=[4q(1−q)]², κ=(L/rM)³.

L parametrizes the coefficient in the existing dimensionless units; it is not derived as a microscopic length. Unlike previous phase stiffness, this term directly penalizes variation of material amplitude. Unlike a fitted radial binding field, it contains no prescribed radius, density, baryonic-law profile or measured force correction. It is an additional constitutive hypothesis.

Writing a=sqrt(rho), the complete additional functional derivatives per radial volume are

    μrho,κ=−κ/(2a) r⁻²∂r[r² b(q)a′],
    cq,κ=(κ/2)b_q(q)(a′)².

Equivalently cx,κ=cq,κ q_x. With independent species densities rhoT=rho q and rhoF=rho(1−q),

    μT,κ=μrho,κ+(1−q)cq,κ/rho,
    μF,κ=μrho,κ−q cq,κ/rho,
    force_i,κ=−∂r μi,κ.

Both b and b_q vanish in pure phases. Hence the pure cold-T bulk-law derivation is unchanged away from the interface. In mixed material these forces alter conversion as well as radial redistribution. Their sign and second variation are not assumed to restore the boundary. The full base gravity, response, barrier, phase stiffness and F pressure are retained.

The discrete term uses face-average q, cell sqrt(m/vol), and the existing radial gradient quadrature. All gradients include the mass normalization and phase dependence. Mass floors prevent evaluating sqrt at negative density; no continuum claim is made on a floor-active or unconverged result.

RD-1 screens L=1,3,10kpc, plus the released exact-law control, at n96/domain12,beta.5,K15,phase length10kpc. Every run allows material and phase to adjust. Three-step directional checks precede minimization. Any promising state requires endpoint-aware law diagnostics, actual exterior mass, grid/domain checks and joint material/phase displacements before a success claim.

## RD-2: binding only mixed material

A distinct local constitutive route adds

    Eb=−epsilon∫r² rho b(q)dr, b=[4q(1−q)]².

The additional derivatives and species forces are

    μrho,b=−epsilon b,
    cq,b=−epsilon rho b_q,
    μT,b=−epsilon[b+(1−q)b_q],
    μF,b=−epsilon[b−q b_q],
    force_i,b=−∂r μi,b.

This is a local mixing energy, not the earlier position-dependent bulk binding proportional to q B(C), and it contains no target profile or specified radius. Its two pure-phase first variations vanish. Nevertheless it can favour a mixed phase over a pure one at finite amplitude, contaminate the inner core, pile up a shell or consume the free reservoir. Those are explicit failure modes, not assumed absent. Positive F pressure and the existing nonlinear response remain in the full energy; no force is inserted after solving.

RD-2 screens epsilon=.01,.03,.1,.3 from independent copies of the old state, with the same n96/domain12 and all material/phase variables free. Directional energy derivatives are checked before each solve. No equilibrium is counted successful just because the integrated force profile improves at a single radius.

## RD-3: material stiffness across a pure-phase cavity

The interface-local coefficient b vanishes in a pure phase, so it cannot penalize an empty interval whose phase remains nearly pure. RD-3 uses the distinct global term

    Eκ=(κ/2)∫r²[∂r sqrt(rho)]²dr.

It acts on the high-pressure beta2,K30 branch which previously developed a detached shell. Its extra density potential is μκ=−κ Δsqrt(rho)/(2sqrt(rho)); its conversion derivative at fixed total density is zero. Both species receive μκ, and the force is −∂rμκ. This force persists inside a pure core, so the old exact cold-bulk identity no longer follows. Any apparent law match is a numerical result for the modified energy, not proof that this new term preserves the original derivation. It must reduce the measured mismatch while filling the cavity, without using a density prior. The physical origin of κ is unproved.

The initial checkpoint has floor-level masses in the cavity; direct-mass directional steps must stay positive. The run's direction check has a very small mass component and does not adequately test this new density term. An independent logarithmic-mass gradient check is required before interpreting a promising candidate.

## RD-4 amplitude solver and interpretation

The global-density direct-mass solves reached their iteration limits with large chemical residuals. Since sqrt(rho) generates stiff derivatives near an empty cell, RD-4 reparametrizes m_i=a_i², enforcing sum a_i²=M and the same physical response cap. Its exact gradient is E_ai=2a_i E_mi; the cap Jacobian and mass Jacobian are transformed consistently. This changes numerical coordinates, not the energy. The amplitude floor is1e-6, corresponding to the existing1e-12 mass floor. Three continuations then report optimizer success, but material residuals remain7e-5–2.4e-4; these are not exact stationarity certificates.

RD-5 independently checks logarithmic-mass directional derivatives on the gapped starting states, rather than relying on the tiny direct-mass components in RD-3's initial test. All pass. RD-6 reconstructs cell edges from midpoints and conservatively integrates mass in radial volume to50kpc. The enclosed-mass values are finite-volume reconstructions; the force operator uses the inherited midpoint enclosed-mass quadrature. They need not coincide exactly on this coarse grid. Endpoint-aware gravity errors are reported separately.

Neither a zero count of floor cells nor small force error proves a filled transition. At L3 the minimum cell mass between50kpc and the boundary is1.08e-7Mb while nearby populated cells have orders of magnitude more material. It is a depleted interval with numerical tails, not a solved gap. L10 materially populates that interval but has21.2% gravity error. These states therefore fail the combined target before a restoration certification is appropriate.
