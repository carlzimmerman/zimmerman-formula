# Actual backward ideal-fluid transfer through ordinary equality

Base: `1db53a670a09a76c023e70784fddc5f351fb8a81`. This child preserves the audited parent action, background and Newton-gauge perturbation closure. It changes the tested time interval, adds an independent radiation seed, and decomposes the actual Weyl source. It does not modify Claude's CFG355 switch or replace the background by EdS.

## Exact regular transport statement

The four-dimensional action is the parent's nonminimal complex carrier with separately conserved ordinary dust and ideal barotropic radiation, tensor coefficient M=1 and F=M−2ξ|χ|². The background solves its Friedmann root, geometric Ricci closure and charged Klein–Gordon equation. The state has four real carrier perturbations, Φ, and the dust/radiation density and velocity pairs. Slip fixes Ψ=Φ−δF/F. The parent proves the nine-dimensional first-order system and Hamiltonian residual C obey

    dC/dt = (Fdot/(2F)−3H) C.

On every compact background interval with F>0, B=F+12ξ²|χ|²>0, H>0 and finite smooth background, the coefficient matrix of this linear system is continuous. Its fundamental matrix is invertible: det U=exp(∫tr A dt). Constraint propagation has the nonzero multiplier √(F/F_initial)(a_initial/a)³. Thus the eight-dimensional constraint-compatible initial-data subspace maps bijectively to the corresponding subspace at every time in the interval. Ordinary equality is not a denominator or singularity of these equations. This is a mathematical regular-transport statement, conditional on that admitted background; it is not positivity of the physical kinetic matrix.

Here ρd=(4/3)a⁻³ and ρr=.01(4/3)a⁻⁴, so ordinary radiation/dust equality occurs exactly at a=.01. This equality compares the two ordinary components, not all effective gravitating stress. Their equality need not imply the textbook radiation/matter expansion history.

## Actual source decomposition and stress

Let p²=k²/a², W=(Φ+Ψ)/2, Y=Φdot+HΨ, δq=ρd vd+(4/3)ρr vr−2 Re(χdot*δχ), and Δd=δd−3Hvd. The exact constrained Weyl equation gives

    W = Wd + Wr + Wχ,
    Wd = −ρd Δd/(2Fp²),
    Wr = [−ρr δr+4Hρr vr]/(2Fp²),
    Wχ = [−δE−6H Re(χdot*δχ)+6H²δF−3Fdot Y]/(2Fp²).

All δF and derivative stress terms are retained. These are an additive bookkeeping decomposition at the actual evolved solution, not three independent Poisson equations. The response of one seed induces the other species' perturbations.

A separate operational dictionary uses fixed M Einstein gravity and moves the full nonminimal carrier to the right-hand side. Its Newton-gauge energy and isotropic pressure perturbations are

    δρχ,EH = −2M[p²Φ+3HY]−ρdδd−ρrδr,
    δpχ,EH = [ρdδd+δρχ,EH−MδR]/3.

The second identity is the full improved trace, not canonical |χdot|² pressure. These are gauge-invariant Newton-gauge completions. A nonzero δp here is not a proof about carrier rest-frame sound speed; it does show that this seed's stress is not the exact pressureless δT of ordinary conserved dust in this gauge. Effective carrier background density may be negative, so assigning a dust particle interpretation or dividing by ρχ+pχ without checking its sign would be unwarranted.

## Adiabatic preparation and the missing early boundary

The ordinary relative entropy Sdr=δd−3δr/4 obeys exactly

    dSdr/dt = p²(vd−vr).

At k=0 the actual equations admit the residual time-shift family with constant spatial dilation ℓ:

    Tdot+(H+Fdot/F)T=ℓ,
    δχ=−χdot T, δχdot=−χddot T−χdot Tdot,
    Φ=HT−ℓ, Ψ=−Tdot,
    δd=3HT, δr=4HT, vd=vr=T.

Substitution into the actual background equations, momentum, slip, trace/KG and fluid rows verifies this family. Its general solution is

    T(t)=[C_T+ℓ∫ a(t)F(t) dt]/[a(t)F(t)].

A choice of lower endpoint or C_T is needed to select an early regular/growing member. The demonstrated positive-F history ends at a tensor-coefficient guard before a primordial radiation asymptotic regime is established. This calculation therefore supplies no unique primordial adiabatic condition. At equality we also construct an entropy-free, equal-ordinary-velocity finite-k initial preparation using T=1/H and ℓ=1, and solve the actual Hamiltonian constraint for Φ. It is compatible initial data; after that correction it is not asserted to be the exact k=0 residual or a uniquely physical growing adiabatic mode. In these examples p/H≈.745 and .717 at equality, so it is particularly inappropriate to label the finite-k preparation an asymptotically superhorizon mode.

## Bounded new experiment

Use ξ=100,1000, S_initial=.4, a_initial=1 and k=10H_initial. Three independent unit late seeds are (i) a carrier phase-velocity kick δχ=0, δχdot=iH_initial χ, (ii) ordinary dust density δd=1, and (iii) ideal radiation density δr=1. Other nonmetric seed entries vanish; Φ is solved from the actual initial Hamiltonian constraint. A phase-velocity kick changes local Noether-charge density and is not a constant U(1) phase rotation. Finite-k seeds do not prescribe a change in global spatially averaged charge.

Integrate the shared background and these three columns backward with DOP853 and Radau, rtol=1e−9, atol=1e−12. Radau has an explicit analytic complex-step Jacobian. Sample 101 logarithmic nodes plus exact ordinary equality. End at a=.0098 (ξ100) or .002 (ξ1000), before the parent's F=1e−8 stop. Require F>0, charge conservation, propagated Hamiltonian/Weyl constraints, additive source equality and solver agreement in a common physical vector norm. Each path is bounded by 160000 solver nfev and an enforced 200000 total RHS calls including Jacobian calls; external execution is bounded separately. Unit columns may be rescaled arbitrarily small on this finite interval; the large backward coefficients are not observed perturbation amplitudes.

The initial development runs are preserved in preflight and preflight_b with their exact scripts. Both fail the originally declared 60000 nfev acceptance bound for the ξ1000 Radau path despite reaching the endpoint (130841 and 130626 respectively). The Jacobian removes numerical differentiation warnings but does not remove the actual integration cost. The final experiment explicitly declares the larger bounded resource case; the old failures are not relabeled as passing.

Development results show equality F≈.06182935,.90209512 for ξ100,1000. Endpoint F≈.03454566,.08313457, and radiation/dust≈1.0204,5. Effective carrier fractions of 3MH² at equality are approximately −.10030,−.01911. Thus neither equality nor the admitted earlier interval identifies a positive cold carrier abundance.

At the same equality epoch, rescaling each transported column to Δd=1 yields W approximately

| ξ | phase-velocity seed | dust-density seed | radiation-density seed |
|---|---:|---:|---:|
|100|−156.5405|−208.9310|−1601.3433|
|1000|−1.793026|−1.853026|−4.846916|

For comparison, the instantaneous bare-M dust source coefficient −ρd/(2M p²) at this same equality epoch is −1.4851448104 (ξ100) or −1.4851481445 (ξ1000). This is an algebraic source-only reference on the actual background, not an EdS transfer history or a complete GR solution with the carrier removed. The ratios are evaluated only where Δd is demonstrably nonzero; no ratio is used to classify a near-zero dust perturbation.

The finite differences persist between independent solvers. They are a direct witness that evolved dust alone does not determine Weyl transfer; carrier and radiation initial data matter. They do not prevent solving a full transfer matrix after all initial data are specified. The phase column's improved pressure at equality is nonzero (approximately −1.2051e6 and −5267.3 in the unit-seed normalization). This is an exact-pressureless interpretation failure for these columns, not a theorem that no approximately cold stress can occur for another prepared mode.

Final authoritative counts and input hashes are recorded in RUNS.md after execution. REPORT is an interpretation document outside executable inputs so that run reconciliation can be appended separately without invalidating the science inputs.

## Remaining implication

All eight coordinates can be transported regularly through ordinary equality in the proven compact positive-F interval. The model does not thereby provide their physical primordial covariance, a past completion across F=0, scalar/tensor health throughout this epoch, or a measured cold abundance. Actual photons, baryons, Thomson scattering, recombination and Boltzmann multipoles are absent from the ideal-fluid closure. These numerical columns cannot establish CMB, recombination or particle identity. The next load-bearing input would be a healthy earlier background and a physically justified initial-state preparation, rather than another dust-only frozen-EdS growth calculation.
