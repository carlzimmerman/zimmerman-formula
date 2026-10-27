# Nonlinear three-dimensional mean-field verification

Dimensionless periodic box [0,2*pi]^3, mean |psi_+|²=|psi_-|²=1, mass=(1,epsilon),
charge signs=(1,-1), Q=hbar*k0²/(2*m*omega0). Let I=(-laplacian)^(-1) on
nonzero Fourier modes. The implemented Hamiltonian per volume is

H=mean(sum_s Q/m_s*|grad psi_s|²)
  +mean(rho_q*I*rho_q-rho_m*I*rho_m)/(4Q),

rho_q=|psi_+|²-|psi_-|², rho_m=|psi_+|²+epsilon*|psi_-|².
The field equation i*dot psi_s=delta H/delta psi_s* has kinetic coefficient
Q/m_s and potential (sign_s*I*rho_q-m_s*I*rho_m)/(2Q).
Its linearization reproduces DERIVATION.md's D with Q replaced by Q*k².
Both charges transport, and both masses source gravity. The homogeneous
self-gravity mode is removed as a periodic Jeans-background convention, not a
finite isolated halo solution. Net charge is zero without an added species.

Use Strang potential/kinetic/potential splitting. Each substep preserves both
species' norms exactly in exact arithmetic. Total Hamiltonian energy is conserved
by the continuous equations; splitting has finite time-step error. Recompute the
potential from updated densities after the kinetic step. No renormalization,
cooling, mass transfer or energy correction is applied. FFT kinetic energy is
computed with Parseval normalization. All energy/number observations occur at
every full step. Initial densities/phases are specified in wave3d.py identically
at all resolutions. Evolution is short and weakly nonlinear, not a collapse run.

Check dt=.01,.005,.0025 and N=12,18,24, Q=.7,epsilon=.1,duration=.5. Compare
energy and species conservation and temporal wavefunction refinement; compare
final energies/density-mode amplitudes across spatial grids. This finite test
supports a conservative two-species 3D mean-field implementation, not a full
quantum many-body computation, causal Maxwell transport, or galaxy assembly.
