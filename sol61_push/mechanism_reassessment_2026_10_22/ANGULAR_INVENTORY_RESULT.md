# A conserved angular-momentum inventory constrains formation

The four constructed unit-mass equilibria occupy different angular-momentum distributions. In particular the A10 warm equilibrium has13.269 times the mean squared angular momentum of A10000. Closed, spherical collisionless evolution cannot turn one into the other, even if collective oscillations damp. This is a conditional reachability obstruction, not an exclusion of primordial cold initial data or the theory.

## Exact invariant and its scope

For the identified-medium spherical force, including the density stiffness term, acceleration is radial. Thus each particle satisfies

    d(x cross v)/dt = x cross a = 0.

This remains true for a time-dependent spherical potential, including spherical baryonic assembly. Under collisionless transport with no boundary flux, the entire mass-weighted distribution of L²=|x cross v|² is invariant. In particular both integral f L² dGamma and integral f L⁴ dGamma are conserved. Zero total vector angular momentum does not imply zero values of these positive moments: oppositely directed orbital angular momenta do not cancel them.

This conclusion concerns a closed central-force system. Nonspherical torques can redistribute individual L; collisions or other interactions can do so even while preserving total vector angular momentum. Escape, capture and boundaries change the inventory of a selected subsystem. None of those processes has been demonstrated here as a selector of the desired law.

## Equilibrium calculation

For the constructed f(Q)=F Q_+, Q=Psi-v_r²/2-(1+r²)v_t²/2, with anisotropy radius1, direct velocity integration gives

    local <L²> = 4 r² Psi/[7(1+r²)],
    local <L⁴> = 32 r⁴ Psi²/[63(1+r²)²].

Multiply by r²rho dr and divide by total mass to obtain global moments in the existing dimensionless units. These formulas follow by rescaling the two tangential velocity components to an isotropic velocity ball and integrating its radial and angular moments. Independent two-dimensional velocity quadrature at Psi=r=1 checks the coefficients: <L²>=2/7 and <L⁴>=8/63.

| A | global <L²> | global <L⁴> |
|---|---:|---:|
|10|.1045142173|.0183626423|
|100|.0459184826|.0035626641|
|1000|.0192081384|.0006281389|
|10000|.0078764226|.0001062157|

The mean L² would have to decrease by about92.46% to map the complete warm population to the complete cold one at fixed unit mass. This is a change in a positive orbital moment, not a required change of net vector angular momentum. The finer numerical mass for A10000 is.99999919; this small background mass residual is far too small to explain the factor13.27 difference. Radial quadrature orders256/512 agree within the prescribed1e-6 relative check for both moments.

## What this changes

The existing canonical-dilation live tests use x -> lambda x, v -> v/lambda. They preserve each particle's L exactly. They test disturbances on the equilibrium's own invariant population; their damping cannot demonstrate movement from a different warm occupation to the near-law cold family. This distinction survives a more accurate damping calculation.

The phase-packing bound already obstructed a particular warm-to-cold transformation through fine-grained occupation. The angular inventory is an additional independent diagnostic with a direct dynamical interpretation. It applies to these specified equilibrium distributions; it does not forbid every distribution producing a similar density or acceleration profile. Such alternatives would need their own force-balance and invariant checks.

The formation route now has a concrete test: specify an initial distribution and compare its cumulative L² inventory with the target, as well as its fine-grained phase-space occupation. If those do not match, a proposed process must explicitly account for torque, interaction or boundary flux. Simply making radial damping faster cannot fix the mismatch. Initially cold radial material can evade this particular warm-inventory example, but its subsequent evolution and selection remain unproved.

## Repository cross-check and evidence

The current CFG955 report says its thermostatted kinetic law state is neither selected nor dynamically maintained; CFG958 supplies a conditional work reservoir but explicitly does not supply the heat bath required by that cooling model. Those are separate theories from the identified-medium system analyzed here. Their reports were inspected, not independently rerun. The reciprocal_field_2026_10_22 report likewise does not claim a completed joint mechanism. None supplies a demonstrated angular-inventory evolution for our cold branch.

angular_inventory.py rebuilds the four spherical backgrounds from cold_limit_run/results.json and evaluates the moments. angular_inventory_run completed; its manifest validates. Three checks pass: mass normalization tolerance, radial refinement and independent velocity moments. The exact invariant argument is self-reviewed; the numerical values are conditional floating-point evidence. No source priority or novelty claim is made. Full formation, a complete dynamical parent and derivation of kappa remain unresolved.
