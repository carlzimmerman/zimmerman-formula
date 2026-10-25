# Dynamical state, rotation and an energy-carrying exterior

Continue the two-species Bose mean-field hypothesis. Do not add a friction,
thermal bath, cooling efficiency, local galaxy label or capture rate. The state
is no longer a prescribed homogeneous condensate: evolve two colliding coherent
wave packets, optionally with transverse velocities carrying orbital angular
momentum. Coherence remains an assumption; this is not a calculation of quantum
thermalization from a mixed many-body state.

Use G=M_dark=b=1, mass ratios m_s=(1,epsilon), charge signs=(1,-1), and
h=hbar/[m*sqrt(G*M_dark*b)]. Norms of both fields are 1/(1+epsilon), so total
dark rest mass is exactly1 and total charge zero. A common stationary baryon
potential Phi_b=-(1/5.364)/sqrt(r²+1) provides a central reference. It is an
explicit approximation: no live baryon response, baryonic cooling, or galaxy
formation is claimed. The fixed potential is time independent and enters H.

rho_m=|psi_+|²+epsilon*|psi_-|²; rho_q=|psi_+|²-|psi_-|².
Phi_self=-4*pi*(-lap)^(-1)rho_m; phi_q=4*pi*(-lap)^(-1)rho_q.
The numerical inverse omits the zero Fourier mode in a periodic cube.

H=integral [sum_s h²/(2*m_s)*|grad psi_s|²
          +rho_m*Phi_b +rho_m*Phi_self/2 +rho_q*phi_q/2] dx³.

i*h*dot psi_s=[-h²/(2*m_s)*lap +m_s*(Phi_b+Phi_self)+sign_s*phi_q]psi_s.

Both charges, all dark mass, and the same interactions as the spectrum model
are evolved. Strang splitting preserves species norms; total energy has numerical
time-step error, measured without resetting it. The fixed central potential and
periodic box break exact isolated-system assumptions; only the displayed
Hamiltonian is tested. No full retarded photons or general relativity is evolved.

## Cooling and rotation

Initialize two equal-amplitude Gaussian packets at (+/-1.6,0,0), width .8,
with incoming x speed .2 and transverse y speeds +/-v, v=0 or .5. Their phase
wavevectors are m_s*velocity/h, so both species have the same prescribed bulk
velocities, not artificially equal phase gradients. Normalize total particle
numbers once at initialization only. At equal masses the fields coincide.
Each pair has nonzero orbital angular momentum for v=.5; neither initial
packet is a disk or a preselected tethered population.

Core r<2.5, exterior its complement. Record species mass, kinetic and potential
energy density in both, as well as outer-box mass r>6.5. The local convention
uses half of each self-field interaction energy and full external potential
energy, so H_core+H_exterior=H exactly. This partition is diagnostic; long-range
interaction energy is not uniquely localized. An outward mass/energy transfer
can cool a core without deleting energy. It is not automatically irreversible
relaxation, thermal cooling or proof of gravitational cooling's late-time attractor.
Periodic waves can return; boundary contamination is explicitly monitored.

The split core is not a new species. Electric tether support is measured separately
by the outward projection ratio -a_e.dot(a_g)/|a_g|² for positive carriers.
The fraction with ratio between .5 and1.5 is only an illustrative force-support
diagnostic, not a tether classification. Gravitationally bound free fraction
cannot be inferred from central mass or that diagnostic.

## Exact symmetry reduction

For epsilon=1 and psi_+(0)=psi_-(0), uniqueness of these evolution equations gives
psi_+(t)=psi_-(t). Hence rho_q=0, phi_q=0 and electric support=0 at all times,
regardless of rotation, radial inflow or wave emission. This is a precise invariant
subspace, not a theorem about asymmetric initial states. A small displaced minus
packet tests sensitivity to explicit initial asymmetry, and epsilon=.1 tests
mass asymmetry. No arbitrary state is claimed to evolve into the invariant subspace.

## Universal microscopic mapping and numerical limits

For the historical profiles set M_dark=5.364*M_b and compute h from the same
physical m and epsilon, never different masses per object. The wave packet phase
resolution and nonrelativistic gradient criteria must hold before interpreting
any physical mapping. Numerical h=.5 or1 benchmarks cannot be relabeled as the
same particle mass in all four profiles. The corresponding mass varies as
1/sqrt(M_dark*b). A finite cube needs k_Nyquist=N*pi/L well above m_s*v/h;
check a factor4 margin for that prescribed transverse phase and also a quantum
wave-speed condition hbar/(epsilon*m*b*c)<.1. These are necessary, not sufficient,
conditions: they do not establish resolved cores or nonlinear collapse.

There is no generic photon cooling constant to insert. In the original matched
Coulomb theory electric dipole radiation has P=|ddot p|²/(6*pi*c³),
p=sqrt(4*pi*G)*[M_plus*R_plus-M_plus*R_minus]. This gives
P=2G*M_plus²*|a_plus-a_minus|²/(3c³), with M_plus=M_dark/(1+epsilon).
For a chosen coherent acceleration difference A*vvir²/b, vvir²=G*Mtot/b,
and reference kinetic energy M_dark*vvir²/2, the estimated fractional loss per
dynamical time b/vvir is
(4/3)*(M_dark/Mtot)*A²/(1+epsilon)²*(vvir/c)³.
We report A=1 as an illustrative coherent estimate, NOT a universal upper bound
or derived radiation history. Exact symmetric fields have p=0 and dipole emission
zero. Higher multipoles and asymmetric trajectories require their actual currents.
The wave solver includes transported matter energy, not photon emission; the
estimate does not remove energy from the evolved fields.

Primary context for scalar wave ejection (not validation of this candidate):
https://arxiv.org/abs/gr-qc/9309015 and https://arxiv.org/abs/astro-ph/0603613 .
Electric dipole radiation convention:
https://farside.ph.utexas.edu/teaching/jk1/Electromagnetism/node156.html .
