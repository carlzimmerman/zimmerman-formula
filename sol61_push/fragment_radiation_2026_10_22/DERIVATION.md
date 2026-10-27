# Fully spatial passive particle/field model

FR-20261022 starts from revision f1803b025624a5bf494d76cb13308431128f2634. It removes the previous affine constraint: every particle has three independent coordinates and velocities, while P and χ have field coordinates and momenta in three dimensions. It is a finite particle-mesh model of the passive action, not a completed covariant theory or a galaxy simulation with baryons.

Hamiltonian in predecessor units:

 H=sum m_i |v_i|²/2 + Ugrav + (1/4π)∫[e²/(2χ)+W(|P|)+a(χ-1)²/2+d|gradχ|²/2+η|Pdot|²/2+bχdot²/2],
 e=ρ-divP, h=e/χ, W(p)=-p-ln(1-p).

The equations used are

 xddot_i=-sum_cells (Φ+h) ∂w_cell(x_i)/∂x_i,
 η Pddot=-P/(1-|P|)-grad h,
 b χddot=h²/2-a(χ-1)+d∇²χ.

Density is deposited as ρ_cell=sum m_i w_cell/vol, vol=dx³/(4π). The TSC assignment weights sum to one and the derivative of their sum vanishes. The particle force is the derivative of the discrete Hamiltonian, not an independently interpolated force. The periodic Poisson operator uses the same lattice Laplacian. Exact material conservation is built into particle motion; no particles are removed as a proxy for radiation.

Static initial fields minimize the nonlinear nonlocal dual from the preceding checkpoint. This eliminates large artificial field startup transients. Field velocities start at zero. Coherent initial spin is supplied with a declared fraction of the periodic Newtonian binding energy.

Field energy current in the continuum is

 S=h Pdot-d χdot gradχ.

With the declared forward gradient and backward divergence, the exact discrete current on the i edge is

 S_i(cell)=h(cell+i) Pdot_i(cell)-d χdot(cell+i) grad_i χ(cell).

At fixed particle density, the discrete local field-energy derivative equals minus div S. This identity is independently checked numerically. Flux through the interior control cube is signed: inward flux is retained and can cancel outward flux. A sponge outside the control region damps field momenta, not field coordinates or matter, and its exact kinetic-energy loss is accumulated. Absorbed energy is not automatically permanent radiated energy at infinity; static tails, finite boxes and wave reflections require controls.

The field radiation carries energy and angular momentum but no separately conserved cold particle mass. Removing cold mass from a central core therefore requires transport/ejection or multiple material fragments. Smooth cold fluid flow can cross; independent particles provide a kinetic continuation through that crossing, but particle noise and deposition self-energy must be refined before interpreting clump masses.

A particle's instantaneous v²/2+Φ+h is not conserved in evolving fields. The reported ejecta diagnostic instead labels far-outward particles with positive isolated softened Newtonian energy; it is only a candidate label, particularly while h remains appreciable. FoF groups at several fixed physical links are connectivity diagnostics, not certificates of self-binding. A selected population would require persistent, resolved, bound clumps and stability of their mass distribution under time, grid, particle and initial-condition changes.

Material angular momentum alone is not conserved when it is exchanged with nonradial fields. For continuum fields the canonical angular momentum includes

 Jfield=(1/4π)∫[η P×Pdot - x×(η sum_j Pdot_j grad P_j+bχdot gradχ)].

Consequently material-L changes alone must not be called numerical torque error. The Cartesian and periodic discretization does not retain exact continuous rotational symmetry; total matter+field+sponge accounting is a refinement diagnostic, not a guaranteed invariant.

The original homogeneous linear response remains the same when expanding about P=h=0 and χ=1. This says nothing by itself about an early nonlinear core population, radiation stress, live baryonic fits or a covariant growth history.
