# Removal alone has a severe mass cost for the tested warm populations

Allow the most favorable possible selective removal: retain the particles with lowest L² until their conditional mean matches the A10000 target. Starting with A10, at most12.735% of the mass can remain while attaining that mean or a smaller one. This constrains a removal-only formation route; it is not a simulation of escape or an exclusion of primordial cold material.

## Optimality and marginal distribution

Let ell=L² and let a retained fraction be specified. Of all selections of that mass, keeping the lowest ell minimizes its mean. Exchanging a retained high-ell element with a discarded lower-ell element decreases the moment at fixed mass. Thus a threshold selection supplies an optimistic upper bound on retained mass at the desired mean. The distributions here are continuous, so boundary randomization is unnecessary.

For f=F Q_+, integrate over radial velocity. At fixed r the tangential variable

    t=(1+r²)v_t²/(2Psi), 0<=t<=1,

has normalized density (5/2)(1-t)^(3/2). Write b=2r²Psi/(1+r²), so ell=b t. For a cutoff c, z=min(c/b,1), the retained local mass fraction and unnormalized ell moment are

    P(ell<=c)=I_z(1,5/2),
    <ell 1[ell<=c]>=(2b/7) I_z(2,5/2),

where I is the regularized incomplete beta function. Integrating these against the normalized spatial mass measure yields the global fraction and moment. Their ratio is set to the target mean .00787642258. This is an algebraic population-selection calculation without a force or escape prescription.

## Results

| source equilibrium | maximum retained fraction | minimum removed fraction | fraction of initial L² moment exported |
|---|---:|---:|---:|
|A10|.12735451|.87264549|.99040228|
|A100|.27502022|.72497978|.95282563|
|A1000|.57281960|.42718040|.76511158|

All sources initially have approximately unit mass. Their retained masses would therefore fall far below the unit-mass target. One cannot restore the target by silently renormalizing the remaining particles: that would add physical mass and alter the self-consistent field. A larger initial reservoir or subsequent accretion requires a new dynamical and phase-space calculation; these fractions do not establish that such a reservoir evolves like a rescaled unit-mass equilibrium.

Matching one moment is necessary but insufficient to match the target distribution. The threshold-remnant distribution, energy, spatial density and fine-grained occupation are not shown to match A10000. Selective removal also cannot increase the initial fine-grained phase-space ceiling. The earlier phase-packing obstruction therefore remains in force for the specified warm-to-cold density transformation.

## Verification

selective_escape_v2.py reconstructs the three initial backgrounds and integrates at radial orders256,512,1024. The512-to1024 retained-fraction differences are below4e-10 relatively. Independent velocity-marginal quadrature checks the beta formulas at four cutoffs. Four finite checks pass and selective_escape_v2_run/manifest.json validates with completed status. The initial selective_escape_run failed during JSON serialization of a NumPy boolean; its script and failure record are preserved. No scientific output from that failed execution is used.

These results are self-reviewed numerical bounds conditional on the supplied distributions and removal-only selection. They sharpen the route choice: making spherical damping stronger or allowing modest escape is insufficient for these initial populations. A successful formation model still needs suitable primordial occupation and angular inventory, or explicit interactions/torques and mass exchange with their conservation accounting. No novelty or completed mechanism is claimed.
