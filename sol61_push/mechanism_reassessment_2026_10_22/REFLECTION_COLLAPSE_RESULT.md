# Continuing collapse through an unresolved logarithmic barrier

The event-based solver reaches t=20, beyond the previous t=13.7105 precision failure. It demonstrates contraction followed by rebound and outward ejection in a declared cutoff approximation. It does not yet establish a converged retained core or solve primordial formation.

## Numerical method and its qualification

The original shell Hamiltonian is unchanged between events. At an inward crossing of q_j=1-epsilon, reverse that node's radial velocity. At fixed positions the kinetic energy is unchanged, so the reflection is exactly elastic. This replaces the unresolved excursion closer to the logarithmic singularity by an instantaneous reflection. It is a **hard-wall approximation**, not an exact integrator of the original barrier. No physical wall or dissipative cooling is claimed.

DOP853 integrates between terminal events. Its stage-only force extension beyond the event surface allows root bracketing; accepted physical segments end at that surface. The event force must therefore be tested by both integration and cutoff refinement. Dense samples check ordering and q<1. The gas remains live and reciprocal; its radius is not prescribed. The chosen cold initial state and gas entropy are still inputs.

The numerical runs use N=32,64, epsilon=1e-4,1e-6 and relative tolerances 1e-8,2e-9, in the combinations recorded by collapse_reflection_contract.json. All four complete t=20, preserve the sampled domain, and have maximum absolute energy drift below 3e-5. The tightest original 32-shell run has drift 5.12e-8. Each reflection's computed energy jump is zero. The manifest validates with completed status; that status is not a convergence claim.

At t=20:

| N | epsilon | rtol | cold half-mass radius | outer radius | gas radius |
|---|---:|---:|---:|---:|---:|
|32|1e-4|1e-8|3.0414|27.6495|1.2569|
|32|1e-6|1e-8|3.1511|27.6503|1.2647|
|32|1e-6|2e-9|3.2459|27.6477|1.3122|
|64|1e-6|1e-8|4.1238|24.7671|1.0307|

The 32-shell half-mass radius is about 1.44 at t=15 and has expanded substantially by t=20. This is not monotonic settling. Tolerance and spatial differences in the inner state are material, despite small global energy error. Energy conservation alone is insufficient validation of a final core.

## An escape diagnostic stronger than total negative energy

For the outermost node, the pressure force is nonnegative because the exterior pressure is zero. The polarization force R(q) is positive. A unit-mass uniform baryon sphere obeys g_b(r,B)<=1/r² both inside and outside its surface. Consequently, while the ordered solution exists,

    r_outer'' >= -1/r_outer².

Define e_escape=v_outer²/2-1/r_outer. While v_outer>0,

    d e_escape/dt = v_outer (r_outer''+1/r_outer²) >= 0.

If e_escape>0 at an outward-moving state, velocity cannot subsequently reach zero: that would require e_escape=-1/r_outer<0. Indeed v_outer>=sqrt(2 e_escape_initial)>0 thereafter. Thus the outer degree of freedom escapes in any continued ordered solution of these equations. Its positive margin is a sufficient certificate; it is not a decomposition of the full interacting energy into individual conserved shell energies.

At t=20 the numerical margins are 2.36504, 2.36520, 2.36473 and 1.89138 respectively, with outward speeds 2.19144, 2.19151, 2.19130 and 1.96558. These are far from zero in all tested variants. This supports outer ejection conditional on the numerical states and the stated model. It does not certify an escaped continuum mass fraction: the outer endpoint weight is only dm/2 and changes with resolution. Nor does it prove that the rest remains bound. Globally negative energy was present initially and permits simultaneous ejection and a bound baryonic component.

## Remaining gate

Additional tight runs (collapse_reflection_tight_run, validated completed manifest) use N=32, rtol=2e-11 and epsilon=1e-6,1e-8. Both reach t=20. Their maximum absolute energy errors are 1.40e-8 and 1.80e-9; final outer radii are 27.6477412 and 27.6477181, with escape margins 2.3647334 and 2.3647293. The maximum sampled outer-radius difference is 2.31e-5. Thus outer ejection is stable under this cutoff comparison. However, maximum sampled half-mass-radius and gas-radius differences are 0.13986 and 0.04007. Tightening rtol from 2e-9 to 2e-11 at fixed epsilon=1e-6 changes the sampled half-mass radius by as much as 0.13116, despite changing the outer radius by only 3.51e-6. The interior is not certified converged, and global energy accuracy must not be substituted for that test.

Separate the strongly supported qualitative outflow from the unresolved interior. A cutoff-refined, time-accurate and spatially converged retained-mass calculation is still required. Even a successful bound remnant in this setup would only demonstrate collapse from an assumed cold, subvirial initial state; the independent seed-production problem is addressed in EMPTY_STATE_OBSTRUCTION.md.
