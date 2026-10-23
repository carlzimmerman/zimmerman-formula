# Medium inertia is already derived; pressure and relaxation cannot be separated

CFG939 already derives the polarization inertia from mass motion in the identified-medium model. Importing that inertia into the independent-field A33 model without changing its matter degrees of freedom is not legitimate. In the identified model the local restoring interaction is repulsive, the kinetic determinant differs, and collisionless relaxation can be strong. Its velocity dispersion also changes the equilibrium force law. A model-specific relation ties that pressure correction to the wavelength at which phase mixing can be effective.

This identifies a possible short-scale relaxation regime, not a derivation of the required halo/cluster selector or a new fundamental interaction.

## What is inherited and what is different

CFG939/DERIVATION.md §§1–2 establishes, in the identity branch,

    div P=rho-rhobar, Pdot=-j,
    T=sum_s rho_s v_s²/2=j²/(2rho)+rho variance/2.

At linear order about a single rest stream this gives T=|Pdot|²/(2rhobar). That is the origin of eta_eff=1/rhobar, not a free phenomenological choice. At finite amplitude and with multiple streams, density and velocity variance remain essential variables. Two distributions can have identical density and current (hence identical instantaneous P and Pdot given the same integration history) and different stresses. The explicit witness is unit mass at rest versus two equal counterstreams of speed1: both have rho=1,j=0; their second moments are0 and1. A spatially varying stress then changes the current evolution. Thus a field-only kinetic term cannot close the multistream dynamics.

The same identified action cancels the cold medium's Newtonian self-gravity through its critical quadratic. This is already documented in CFG939 and the D9b obstruction. The preceding KINETIC_RESULT.md instead retained independent matter coupled gravitationally to an independent polarization mode. Its attractive Jeans determinant must not be reused after the identification.

## The consistent local response in the identity branch

Let h be the longitudinal Hessian of the reduced remainder potential and gamma the gradient stiffness. With delta_rho=ik delta_P, the quadratic spatial energy of a longitudinal mode is

    deltaE=(h+gamma k²)|delta_rho|²/(2k²).

The corresponding chemical-potential perturbation is

    delta_mu=(h/k²+gamma) delta_rho.

It is repulsive for positive h,gamma. Combining it with a local Maxwellian Vlasov response gives

    1+A R(z)=0,
    A=rho(h+gamma k²)/(k² s²),
    R(z)=1+z Z(z), z=omega/(sqrt(2) k s).

There is no independent beta-controlled scalar inertia in this particular kinetic equation. Its static determinant is1+A>0, rather than the gravitational Jeans1-J(1+a). This observation is not a global nonlinear stability theorem.

Representative roots with the exp(-i omega t) convention are:

| A | z | amplitude e-folding / oscillation period |
|---|---|---:|
| 0.3 | 1.16104 - 0.948612 i | 0.195 |
| 1 | 1.44667 - 0.601982 i | 0.382 |
| 3 | 1.85720 - 0.290659 i | 1.017 |
| 10 | 2.63668 - 0.0412508 i | 10.17 |
| 20 | 3.42141 - 0.00141837 i | 383.9 |
| 40 | 4.64591 - 2.98199e-7 i | 2.480e6 |

These are poles of the analytically continued local response, not a complete initial-value solution or eigenvalue census. At strong damping the pole does not justify treating the whole evolution as a long-lived sinusoid. All six root solves report success and residuals below2.4e-14.

## Pressure also changes the static law

The inherited identified-medium radial force is

    acceleration=-gNb+R(K|P|)-gamma rho'.

For stationary isotropic constant dispersion s, the Jeans moment requires

    R(K|P|)=gNb+(s²/rho+gamma)rho'.

For declining density, pressure reduces the required polarization restoring force relative to the cold zero-stiffness balance R=gNb. Therefore one cannot make the medium warm enough to phase-mix rapidly while simply retaining its cold algebraic profile as an exact equilibrium.

For a point baryonic mass in the theory's own deep-acceleration cold limit, define rM²=GMb/a0. The cold law and density identification give

    P~a0 rM/(K r), rho~a0 rM/(K r²),
    h~2K rM/r, rho h~2GMb/r³.

This assumes the background density is negligible relative to the excess, positive radial polarization, and gradient corrections are small. It is derived from the framework's own remainder potential and identity, not imported as a standard-MOND observational recipe.

Define the warm fractional force correction on that profile,

    epsilon_warm=2s² r/(GMb).

Then, when gamma k² is negligible,

    A epsilon_warm=4/(k r)².

This is an exact algebraic relation within the stated asymptotic profile. It ties two effects that cannot be independently adjusted. For example, epsilon_warm=0.01 and A=3 would require kr approximately11.55. Shorter-scale local responses may relax efficiently while the mean pressure correction stays small. The calculation has not demonstrated the transport of halo-scale energy into those modes or their subsequent nonlinear evolution.

Formally setting kr=1 and epsilon_warm=0.1 gives A=40, where the local root is weakly damped. But kr=1 is outside the controlled uniform-patch limit. The numerical2.48-million-period value must NOT be reported as a proved global halo damping time or no-go. The useful result is the compatibility relation and the need for a global calculation, not that extrapolation.

Including stiffness adds rho gamma/s² to A and changes the mean balance; its contribution must be kept when gamma k² competes with h. Anisotropy, streaming, inhomogeneity and finite boundaries can also change the response. None has been folded into a claimed universal relaxation rate.

## What this advances and what remains missing

This closes a tempting but inconsistent shortcut: lowering a field's phase speed by inserting medium inertia requires changing the theory's dynamical variables and restoring forces. There is a legitimate identified-medium route with local phase mixing, and a separate independent-field route with its own kinetic response. Their successful pieces cannot be combined as if they were one action.

The compatible short-scale regime gives a sharper next target: derive whether a conserved, inhomogeneous evolution transfers large-scale perturbations into local kinetic structure while approaching the correct warm equilibrium. CFG939 already shows phase mixing and ejection in its shell engine; it also shows that shell crossing does not generate the free S4 population. This new local analysis does not undo that obstruction. A source partition, kappa, and the required excess-mass population remain unproved.

The current wave-E repository brief emphasizes the screened candidate and raw/framework-native observational gates. No external calibrated halo profile or observational verdict is introduced here, and the concurrent screened Cassini lane is not duplicated.

## Verification

medium_inertia_run/manifest.json validates; seven checks pass: kinetic decomposition, density energy, warm force balance, the nonclosure witness, representative roots, static sign and pressure/relaxation relation. The A=40 and asymptotic-profile comparison were added after the first root probe and are labeled in MEDIUM_INERTIA_CONTRACT.md. No new mutation, independent discretization or global initial-value simulation was performed. This is self-reviewed mathematical work, with no novelty certification for phase mixing or kinetic theory.
