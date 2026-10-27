# Nonthermal preparation attempt

The finite-temperature result does not exclude a coherently prepared, isolated
half-filled band. Test that loophole with a prescribed ramp e(t)=e_f*sin²(pi*t/2T),
starting from the occupied negative band at e=0. Each transverse-energy mode u
obeys H=u*sigma_x-e(t)*sigma_z, rdot=2*b cross r, b=(u,0,-e). Its polarization
is r_z; mode weights are chi*u*du. This conserves fermion number, not energy
of matter alone because the source is time-dependent.

A midpoint constant-H rotation evolves each Bloch vector unitarily. For each
step, explicitly account for source work during the initial E0->Em and final
Em->E1 quenches. Work accumulated into the source is
DeltaW=(Em-E0)*P_before+(E1-Em)*P_after. Then H_matter+W is conserved by the
discrete piecewise protocol. This is an honest driven-system energy ledger,
not an isolated galaxy energy solution. Timestep refinement tests approximation
to the smooth ramp; the exact discrete ledger alone does not validate that limit.

Record instantaneous final polarization and the diagonal-ensemble polarization
obtained by projecting each Bloch vector onto its final Hamiltonian axis.
The latter is an infinite-time dephased expectation for this fixed independent-
mode Hamiltonian, not a claim of irreversible cooling or thermalization.
Compare the *small source remainder* chi*E-P with its analytic ground-state
value, not just the much larger total P. This is the sensitive quantity for
retaining the intended acceleration law after leading-force cancellation.

Use e_f=.01,.1; T=1,10,100,1000 in hbar/Lambda units; N64 Gaussian quadrature,
dt=.1, and N128/dt.05 refinement at the most demanding long weak-field case.
An initially filled ground band, no scattering, no chemical-potential drift,
no medium assembly and a prescribed ramp are assumptions. A success shows this
restricted state is dynamically accessible from that prepared initial state;
it does not derive cosmological preparation, a relaxation mechanism or disk
selection. Low-frequency modes require increasingly long ramps as field falls.
