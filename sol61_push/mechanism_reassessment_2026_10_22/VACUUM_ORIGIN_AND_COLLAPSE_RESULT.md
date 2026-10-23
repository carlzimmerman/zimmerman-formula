# Vacuum production candidate and a longer reciprocal collapse calculation

The original formation goal is not reached. Two concrete advances replace the earlier assumed source and prescribed baryonic ramp: a leading-order quantum calculation produces excitations from an in-vacuum under a declared expanding background, and adaptive reciprocal collapse passes the original breakdown epoch and develops a concentrated interior with an expanding outer shell. Neither establishes the observed abundance, a stable final object, or the link between the scalar carrier and the identified medium.

## 1. What the existing action permits without occupied sources

Use the existing charged-carrier action, not the distinct ARGON real-mediator model:

    L=|partial Phi|²+|partial X|²-V,
    V=m²|Phi|²+M²|X|²+g(X*Phi²+X Phi*²)+lambda_tot|Phi|⁴,
    M²=4m²+Delta, lambda_tot=g²/Delta+lambda_rep,
    m,Delta,lambda_rep>0.

The positive-square form is recorded in cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md. Its classical equations have the exact solution Phi=X=0 with zero initial derivatives. Local uniqueness preserves that solution. The quadratic masses are positive; no spontaneous classical tachyonic growth from exact zero follows. Simply integrating classical empty fields cannot create the missing population.

Quantization is different. Under the **minimal covariant extension** of the displayed kinetic terms, and on a spatially flat FLRW metric in conformal time, the rescaled linear mode u=a Phi_k obeys

    u''+[k²+m² a²-a''/a]u=0,

and X has the same equation with m replaced by M. The cubic and quartic vertices do not enter the linearized vacuum mode equations. Minimal coupling, no curvature term xi R|Phi|², is a stated choice here; the flat-space action alone does not uniquely fix curvature couplings or a renormalized gravitational completion.

An early positive-frequency vacuum mode evolves into a mixture of late positive and negative frequencies. At an asymptotically static late epoch,

    n_k=|beta_k|²,
    beta_k=(omega_out u-i u')/sqrt(2 omega_out),
    |alpha_k|²-|beta_k|²=1.

No occupied X or Phi source is supplied. The time-dependent gravitational background provides the energy; vacuum production is not energy creation in a closed stationary system. This general mechanism is established physics: [Parker, Phys. Rev.183,1057 (1969)](https://journals.aps.org/pr/abstract/10.1103/PhysRev.183.1057). The primary publication's metadata/abstract were checked for attribution, not used as a substitute for deriving our mode equation.

## 2. Executed source test

For an unambiguous in/out numerical test choose

    a(eta)=1.5+.5 tanh(eta/tau),

so a runs from1 to2. Units are hbar=c=m_Phi=1; M=2.2. This is a prescribed scattering background, **not a derived cosmological expansion**. It is not asserted to solve Einstein equations with an admissible source. It tests the production operator and cannot supply an actual cosmic abundance by itself.

Evolve36 selected modes: two masses, three transition times tau=.2,1,3, and k=.05,.2,.5,1,2,5. Repeat at two integration tolerances. Representative daughter occupations are:

| tau | n(k=.05) | n(k=1) |
|---|---:|---:|
|.2|1.16486|.752626|
|1|.0249637|.00348852|
|3|1.12656e-7|1.95545e-10|

The static-background control remains empty to its numerical threshold. Four checks pass: successful integration, conserved Wronskian, tolerance comparison and static vacuum control. vacuum_seed_run completed and its manifest validates. Very tiny occupations in slow heavy-field cases approach numerical floors; they are not accurate abundance predictions. Finite start/end truncation and spectral-domain convergence have not been audited.

The populated daughter k=.05 mode has late speed about.025c, while k=1 has.447c. This demonstrates that production is not automatically cold as a whole. Later free redshifting decreases physical momentum, but abundance, integrated pressure and free-streaming length require the full spectrum and a physical expansion history. The selected low-k modes alone do not establish a cold population.

For these complex charged fields the vacuum process makes opposite-charge pairs and preserves net U(1) charge. It does not produce a charged classical expectation value or automatically prepare ARGON's coherent charged condensate. X decay could redistribute the resulting neutral stock, but that kinetic calculation, interaction survival and the carrier-to-medium mapping remain absent. This is a source candidate that removes the need to postulate an occupied parent **in this conditional test**, not a completed origin of the halo seed.

## 3. Collapse integrator repair and its remaining limit

Keep the exact closed Hamiltonian, gas thermal coefficient and diffuse initial data from FORMATION_FOCUS_RESULT.md. No force or pressure law was softened. Replace fixed-step Verlet by step-doubling error control: compare a full step with two half steps, reject invalid states, and retain the two-half-step result when the scaled local defect is acceptable. State updates are transactional; rejected steps do not alter the trajectory. Adaptivity means the scheme is no longer fixed-step symplectic, so energy is explicitly monitored.

The first adaptive runs cross the original t~6.5 failure but hit a minimum step near a later compression. Lowering the step floor from1e-11 to1e-15 allows the32-shell run to reach t=13.7105. It then fails with step9.2e-16, close to the resolution of the accumulated time, and central-node q=1-1.52e-12. The positive logarithmic barrier has not been crossed. Full final state is saved. These are failed completion records, not passing full-collapse runs.

At the final accepted state, cold half-mass radius has decreased from4.7622 to1.7864, whereas the outer radius has increased from6 to13.8256 with outward speed2.2077. Gas radius is.5488. Between t8 and the last sample it oscillates between about.484 and2.064. Thus this prototype shows concentration, rebound and outward redistribution rather than simple adiabatic settling. No outer-shell unbinding or permanent core retention is certified: that requires a longer trajectory and an appropriate energy/flux diagnosis.

Initial total energy is-.40363046; final accepted energy is-.40364010, a drift of approximately9.64e-6. Negative global energy was already present initially and does not prove all material is bound. The late extended run is only32 shells and is not spatially converged. Early contraction was resolution checked in the preceding experiment; that does not certify this later behavior.

collapse_adaptive_run and collapse_adaptive_floor_run preserve the failures. The latter manifest validates with failed status. The remaining solver problem is extreme barrier stiffness/precision, not an untested instruction simply to decrease a fixed step. A barrier-aware coordinate or implicit energy-controlled treatment, with independent refinement, is needed before deciding whether a lasting bound object forms. The cold-fluid approximation and homologous gas closure also require validation through compression.

## 4. Next decisive dependencies

For origin, use a physically sourced expansion history and declared curvature couplings to compute the full in-vacuum spectrum, its abundance and redshifting/free streaming; then include the existing interactions and test whether the resulting neutral distribution can supply the identified medium. Do not substitute an initially coherent charged field at that step.

For assembly, continue the same reciprocal Hamiltonian through the barrier with a solver that resolves its energy cost, then measure retained mass, outflow, rebound and profile. Gas radiation and a cosmological initial state have not been added; their absence limits any claim of natural formation. No new portal, abundance normalization, or optimized baryonic history has been inserted to force success. Both branches remain open, with this checkpoint self-reviewed and no novelty claim.
