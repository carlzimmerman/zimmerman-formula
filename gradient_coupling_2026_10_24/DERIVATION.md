# Coupled material and phase gradients

Target is unchanged: original baryonic galaxy law through50kpc, mobile material and boundary, a materially populated transition, restoring radial boundary and a free outer reservoir, with fixed total mass5.364Mb. Original-law M(<50)=4.801579Mb remains a diagnostic, not a constraint or objective penalty. No radius is pinned.

## New constitutive hypothesis

Let a=sqrt(rho), q=sin²(πx/2), and w=a′−eta a q′. Add the positive energy

    Ec=(κ/2)∫r²w²dr, κ=(L/rM)³.

The base is the corrected response/pressure energy already tested. This is a completed-square density/phase-gradient coupling, distinct from the earlier fixed-density alignment with a baryonic gate, local mixing binding, interface charge and uncoupled material stiffness. No target profile or baryonic-law discrepancy appears in Ec. The physical origin and universality of κ and eta are unproved.

Where w≈0, log(rho)′≈2eta q′. For a monotone phase decrease from q≈1 inside to0 outside, eta>0 favours a density contrast rho_in/rho_out≈exp(2eta). This is a preferred gradient relation, not proof of inward transport, a particular radius or equilibrium. Negative eta is a sign control. The square remains nonnegative for either sign; positivity does not guarantee a positive coupled Hessian.

## All additional forces

Integration by parts gives per-volume functional derivatives

    μrho,c=−κ/(2a)[r⁻²∂r(r²w)+eta q′w],
    cq,c=κ eta r⁻²∂r(r²a w),
    cx,c=cq,c q_x.

The species potentials and forces are

    μT,c=μrho,c+(1−q)cq,c/rho,
    μF,c=μrho,c−q cq,c/rho,
    force_T,c=−∂r μT,c, force_F,c=−∂r μF,c.

Both density and conversion derivatives are retained. The boundary variation is κr²w δa−κ eta r²a w δq. Origin regularity and negligible outer-edge density/phase are required before an isolated-halo interpretation. All discrete derivatives come from the same energy and are independently tested with logarithmic-mass and phase directions.

This interaction is active when gradients overlap, but it is not a force-free pure-phase modification. At q′=0 the energy contains ordinary material capillarity, μrho,c=−κ Δa/(2a), and cq,c can also be nonzero. Thus the cold pure-T force law changes to

    0=g−W′(u)+∂r μrho,c.

Any claimed original-law preservation must be measured, not inferred from the unmodified cold-bulk proof. Pure-phase nucleation stability also needs testing because q_x=0 can hide an adverse second variation.

## Complete base forces

For the original base define

    A=W′(u)+beta C F′(u)s+(ell²/2)F′(u)x′²,
    Psi(r)=∫ᵣ∞A(t)dt,
    Xi=beta C F(u)s′−ell²r⁻²∂r(r²F(u)x′),
    hF=(5/2)K[rho(1−q)]^(2/3).

The full material and phase derivatives are

    μrho=Phi+q Psi+(1−q)hF+μrho,c,
    cx=rho q_x(Psi−hF)+Xi+cx,c.

Transform these full derivatives to species potentials as above; their negative gradients include gravity, pressure, response, both gradient energies and every mixed term. At a mixed equilibrium cx=0 and both mobile species have a common constant chemical potential. No pressure or outward acceleration is added after optimization.

## Boundary restoration test

At a stationary constrained state, density relaxation subtracts a Schur complement from phase stiffness. The complete tangent Hessian, including the new cross terms, must be used. A positive square or fixed-density Hessian cannot establish restoration. Joint material/phase±1kpc displacements and a refined grid are required for a candidate; a law match with a depleted interval or an effectively absent free reservoir fails before certification.

GC-1 tests six (L,eta) pairs on n96/domain12,beta2,K30,ell10kpc, initialized from the previous high-pressure mobile branch. Material amplitudes sqrt(m) are optimized with sum m=5.364, positivity and the original response saturation cap. The mass floor remains1e-12. Endpoint-aware law error, mass allocation, chemical residual and minimum material in the transition are reported. Tiny positive tails are not counted as successful material support.

## GC-5: homology stress and force audit

Under a mass-preserving dilation r→lambda r, rho→lambda^-3rho and q(r)→q(r/lambda), the coupling energy scales exactly Ec→lambda^-2Ec. Its outward generalized dilation force is therefore2Ec/lambda. This does not prohibit inward transfer between shells, but it supplies no additional net confining stress under that deformation. The scaling was checked independently on both discrete grids at lambda=.8,1.2 to about1e-15. This is not a general exclusion theorem for all coupled equilibria.

For the selected L5,eta3 state, the finite-active-set Hessian and material Hessian are positive on both grids, with no detected negative pure-endpoint diagonal. Relaxed local boundary stiffness is1.81034e-4Eunit/kpc² on n96 and4.71094e-5 on n144. Both states return after joint±1kpc displacements. Nevertheless the boundary changes122→176kpc and a density rebound grows1.09→85.4 on refinement. Local restoring force does not certify a physically resolved, populated boundary. The law error remainsabout10% and mass outside50kpc still exceeds the allowed budget.

## GC-6: inward response-capacity stress plus coupled material stiffness

This is a combined test, not a repetition of the earlier standalone charge route. The existing supplied response capacity is retained with all its variations alongside the new gradient coupling:

    EQ=k/I, I=∫r²F(u)f(rho)b(q)D(q′)dr,
    f=rho/(rho+rhos), b=[4q(1−q)]²,
    D(v)=sqrt(v²+delta²)−delta.

Write alpha=k/I² and J(r)=∫ᵣ∞F′(u)f b D ds. The additional derivatives are

    μrho,Q=−alpha[F f_rho b D+q J],
    cq,Q=−alpha[rho J+F f b_q D−r⁻²∂r(r²F f b D′)].

Add these to the full potentials already derived, then transform to species potentials and differentiate radially. These terms include response under enclosed T-mass changes, local density susceptibility, mixing changes and phase gradients. Omitting any contribution would give a different material balance.

For a sharp interface, the logarithmic dilation derivative of the capacity integrand is

    2−2u F′/F−3rho f_rho/f
      =−2/(1−u)−3rhos/(rho+rhos)<0.

Thus EQ grows with dilation and can supply an inward contribution opposing Ec's expansive stress. Regularized small gradients modify the exponent, and actual relaxed balance is determined by the full minimization. No charge creation, microscopic carrier or real-time dynamics is established by supplying k. The earlier failures of capacity storage in inner mixed layers, fragmentation and reservoir conversion remain explicit rejection criteria.

GC-6 screens k=.003,.03,.3 at n96,domain12,L5,eta3,beta2,K30,phase length10kpc, from the selected coarse populated state. No radial target or enclosed-mass equality is imposed.
