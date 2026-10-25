# Interacting quantum medium: a minimal two-component charged Bose candidate

## Hypothesis, not a derived identity of dark matter

Two nonrelativistic bosonic fields psi_+,psi_- have masses m,epsilon*m, charges
+q,-q, and equal number density n. Baryons are neutral under this new charge.
Use Heaviside electromagnetic units, c explicit when needed, and
q²/(4*pi)=G*m² (vacuum positive-positive force matching). This relation is a
conditional phenomenological matching, not forced by symmetry. Do NOT import
the earlier fitted dielectric chi into this different microscopic theory.
There is no contact interaction, fitted gap distribution or reaction rate.
The remaining microscopic parameters are m and epsilon, plus the bosonic
statistics hypothesis. Density and occupation are state information, not couplings.

A nonrelativistic gauge-coupled action has the usual i*hbar*psi*D_t psi term,
kinetic |(-i*hbar*grad-qA)psi|²/(2m), gravitational m*Phi*|psi|²,
Maxwell (E²-B²)/2 and -|grad Phi|²/(8*pi*G). The Schrödinger and Newton sectors
are low-speed approximations; this is not a relativistic causal completion.
For an isolated system its Hamiltonian is

H = sum_s integral hbar²|grad psi_s|²/(2m_s) + (E²+B²)/2
    + (1/2) rho_m*Phi,

with covariant gradients when A is present, rho_m=sum m_s|psi_s|², and
lap Phi=4*pi*G*rho_m. Charge density=sum q_s|psi_s|², currents follow from the
same covariant kinetic term. Each species number is conserved. Opposite charges
remain explicit even in electrically neutral regions. Pairing/ionization is
not a separate species conversion in this continuum truncation.

Rest mass density is rho=n*m*(1+epsilon). Field energy and binding contribute
at order1/c² beyond this Newtonian mass source. No additional neutral-medium
mass is added. Uniform density is a local background approximation: self-gravity
is treated for nonzero wavevectors, not as an exact static finite galaxy.

## Derivation of the longitudinal spectrum

Take the explicit cold coherent mean-field state psi_s=sqrt(n), with no relative
flow. Expand its density/phase Hamiltonian to second order. For a longitudinal
displacement u_s at wavenumber k, delta n_s=-i*k*n*u_s. In mass-normalized
coordinates X_s=sqrt(n*m_s)*u_s the kinetic energy is |dot X|²/2. The quadratic
potential is X^T D X/2, with

D_st = delta_st*hbar²*k^4/(4*m_s²)
       + n*q_s*q_t/sqrt(m_s*m_t)
       - 4*pi*G*n*sqrt(m_s*m_t).

The first term follows from the quantum gradient energy, not an adjustable
sound speed. The Coulomb term is positive semidefinite (like charges repel);
the gravitational term is negative semidefinite and includes both species.
Eigenvalues are squared mode frequencies. A negative eigenvalue is a Jeans
instability, NOT a zero-energy equilibrium spectral line.

For zero gravity, at k=0 the electric vector z=(1,-1/sqrt(epsilon)) in units
sqrt(n)*q/sqrt(m) gives the charged plasmon omega_p²=n*q²*(1/m+1/(epsilon*m)).
The neutral displacement eigenvector (1,sqrt(epsilon)) is dark. Quantum pressure
mixes the branches at k>0 when masses differ. For equal masses neutral/charged
modes decouple exactly, with omega_neutral²=hbar²*k^4/(4m²)-8*pi*G*n*m
and omega_charge²=hbar²*k^4/(4m²)+2*n*q²/m.

Define omega0²=4*pi*G*n*m and Q=hbar*k²/(2*m*omega0). With the vacuum matching,

D/omega0² = diag(Q²,Q²/epsilon²) + z z^T - v v^T,
v=(1,sqrt(epsilon)).

Without gravity omit v v^T. No finite-bin gap ansatz occurs in this expression.
The force terms are genuine interactions, but the diagonalization is a Gaussian
(Bogoliubov/linearized Hartree) approximation, not an exact many-body solution.
Strong correlation, molecular formation and finite-temperature kinetics are absent.

## Dipole response, weights, state and conservation

Polarization is P_L=sqrt(n)*q*(u_massnormalized,+/sqrt(m)
-u_massnormalized,-/sqrt(epsilon*m)) = d^T X. For positive omega_j² the
retarded susceptibility per volume in this normalization is

chi_L(k,omega)=sum_j |d^T e_j|²/[omega_j²-(omega+i0)²].

The zero-temperature positive-frequency spectral weight is
W_j=hbar*|d^T e_j|²/(2*omega_j). At temperature T it is multiplied by
1+n_B(hbar*omega_j); the opposite-frequency part contains n_B. The retarded
commutator weights of this quadratic model do not depend on occupation.
The thermal state is NOT used in the numerical runs. At an unstable mode there
is no stationary oscillator vacuum and this spectral representation is invalid.

The oscillator sum rule follows from completeness:
sum_j omega_j W_j = hbar*|d|²/2.
The implementation checks the equivalent sum of dipole residues, and compares
the modal susceptibility with direct inversion of D-(omega+i0)² I.
This is a dipole response, not a count of mechanical modes. In a uniform medium
an external Fourier component couples only to modes at the same k: summing a
phonon DOS over k cannot stand in for local internal saturable dipoles.

For each mode-pair the energy H_k=(V^T V+X^T D X)/2 is conserved under
Xdot=V,Vdot=-D X, including unstable modes (where it is not positive definite).
The numerical check directly evolves these equations and monitors H_k; there
is no renormalization, damping or energy reset. This is a linear-mode energy
test, not a live nonlinear gravitating galaxy evolution.

## Physical scale and test protocol

The exact stability threshold is determined without fitting. Put t=Q²:

epsilon²*det(D/omega0²) = t² + epsilon*(1-epsilon²)*t - epsilon*(1+epsilon)².

With a=epsilon*(1-epsilon²), b=epsilon*(1+epsilon)², the positive root is
t_J=2b/(a+sqrt(a²+4b)), Q_J=sqrt(t_J).
The medium is stable against this longitudinal mode for Q>Q_J.
The physical Jeans wavenumber satisfies k_J²=2*m*omega0*Q_J/hbar.
This introduces a genuine quantum length scaling as m^(-1/2)*rho^(-1/4),
which breaks the preceding classical homology. It does not fix m itself.

Use the same local inventory estimate rho=eta*M_b/(4*pi*b³/3), eta=5.364,
for all four historical numerical mass/size pairs. Choose k=pi/b as an explicit
object-scale diagnostic (wavelength2b), not an exact finite-galaxy eigenmode.
Then m_critical=hbar*pi²/(2*b²*omega0*Q_J). Changing the boundary wavenumber
convention rescales every threshold by its square. No threshold is fit per object.
The inputs contain only mass and size, never a galaxy-type switch. Scan the
same m,epsilon for every object; stability is a diagnostic, not a tether fraction.

The threshold scales as 1/sqrt(M_b*b) at fixed eta,epsilon. The historical
ordering M_b*b is strictly increasing from smallest dwarf to cluster.
Consequently if the large disk mode is Jeans-unstable the cluster mode is also
unstable. No common m yields stable dwarf AND cluster modes with an unstable
large-disk mode in this proxy. This is NOT a general no-go theorem: gravitational
instability does not equal charged tethering and stability does not equal retained
free mass. A uniform bulk velocity merely Doppler-shifts the spectrum; rotation,
shear, equilibrium geometry and cooling are not represented by this local state.

We separately report occupation plausibility using sigma²=G*(1+eta)*M_b/(6*b),
n*(sqrt(2*pi)*hbar/(m_s*sigma))³ for each species, plus the nonrelativistic
wave-speed test hbar*k/(m_s*c)<.1. Large occupation permits a field description
but does not establish thermalization, condensation or the assumed zero-T state.
A two-species attractive bosonic Coulomb theory need not have a stable extensive
many-body ground state; no stability-of-matter theorem is assumed. The local
Gaussian spectrum must not be labeled a realized equilibrium quantum medium.

## Verification and exclusions

Check the determinant formula, equal-mass analytic eigenvalues, dipole sum rule,
modal versus matrix resolvent, and energy of stable/unstable modes. Scan the
physical thresholds and test the analytic ordering. Finite spectra cannot
establish the critical nonlinear constitutive relation, population separation,
or the galaxy acceleration relation. Do not convert a Jeans pole into the
previous independent internal-level density n(s)d~s. The quadratic response has
no saturation or radiative capture channel.

Primary context, not proofs of this two-species result:
- Charged Bose gas Bogoliubov collective spectrum:
  https://journals.aps.org/prb/abstract/10.1103/PhysRevB.51.5887
- Quantum gravitational Jeans scales:
  https://arxiv.org/abs/1710.10486
  https://arxiv.org/abs/2011.01038
All load-bearing two-by-two algebra here is derived explicitly and checked
numerically; cited models are not claimed to validate this mechanism.
