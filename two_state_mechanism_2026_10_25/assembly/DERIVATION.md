# Physical assembly: charged molecular channel

Base: ef7fcda34feac7e7f9a859fbdd3187ba2cf778cb. The goal is a charge/energy
conserving microscopic assembly mechanism and unlabeled population separation.
This work uses the research-program and computation-audit approach. It does not
assume the requested astrophysical mechanism exists.

## What can and cannot follow from the current Hamiltonian

A harmonic lattice potential has no finite dissociation threshold. Its local
curvature K cannot fix one: V_D(x)=D[1-exp(-sqrt(K/(2D)) x)]² has the same
curvature K for every D>0, but dissociation energy D. This is an identifiability
obstruction, not a numerical problem. Adding a well depth by hand would violate
the intended parameter reduction.

Choose an explicit microscopic Coulomb parent instead: mobile positive carriers
X of mass M and charge+Q, negative carriers C of mass m and charge-Q, minimal
coupling to the same U(1) field, and all pair Coulomb terms. In Coulomb gauge,
H=sum_a (p_a-q_a A)^2/(2m_a)+sum_(a<b) q_a q_b/(4pi epsilon r_ab)+H_transverse.
Longitudinal field energy is represented by the Coulomb term once. This is a
nonrelativistic microscopic completion candidate, NOT uniquely implied by the
previous phenomenological band and springs. No new force or binding constant is
introduced. The actual band, stiffness, state and a0 still require derivation.
Gravity can later couple to all masses/energy; it is not simulated below.

Define a_D=hbar/(m c alpha), E_H=m c² alpha², alpha=Q²/(4pi epsilon hbar c).
Use m=1, E_H=1, a_D=1 atomic units. Born-Oppenheimer approximation M/m=100 is
used in the main chemical test. Finite-mass electronic corrections O(m/M) are
not resolved; nuclear motion is retained with reduced mass M/2.

The first bound channel X+C=A is neutral, binding B_A=1/2 in this approximation.
The new channel A+X=T has T=X2C, charge+Q and mass approximately2M+m. It can
repel another positive charge under the same U(1); countercharges must remain
explicit. It is a charged molecular candidate, not proof of galactic tethering.
Free X already has charge+Q; assembly does not switch that charge on.

## Two-center electronic variational derivation

At heavy separation R, take normalized1s orbitals phi_A,phi_B with exponent1.
S=exp(-R)(1+R+R²/3), J=-1/R+exp(-2R)(1+1/R),
K_ex=-exp(-R)(1+R), H_AA=-1/2+J, H_AB=-S/2+K_ex.
Bonding/antibonding states (phi_A±phi_B)/sqrt[2(1±S)] give potentials INCLUDING
heavy-heavy repulsion U_±=(H_AA±H_AB)/(1±S)+1/R. Both approach-1/2.
The bound curve is a two-orbital variational approximation, not an exact H2+
curve. Its well depth is a prediction of this basis, not fitted. Missing
polarization tails and electronic basis functions limit rates and shallow levels.

For each angular momentum J_rot solve
[-1/(2mu_N) d²/dR²+J_rot(J_rot+1)/(2mu_N R²)+U_+(R)+1/2] u=E u.
E<0 identifies genuine rovibrational bound states; binding D_vJ=-E. Dirichlet
radial endpoints and mesh are stated in code. Bound states are counted from
spectra, never a distance/galaxy-type flag. Formation without a third body or
emitted quantum cannot occur in conservative two-body motion: the bound spectral
projector commutes with the isolated radial Hamiltonian. A continuum state stays
in its continuum subspace. A local overdensity alone cannot be counted as capture.

Electric dipole coupling to emitted/absorbed quanta follows from the same charge
operator. In this basis |<g|z|u>|=R/[2 sqrt(1-S²)] (in unitsQ a_D). Ground-surface
g-g internal E1 transitions vanish by inversion; g-u transitions are allowed.
A+X association can therefore access bound g states through a u continuum with
radiation, conserving total charge and photon+matter energy. In particular
hbar omega=E_cont+D_vJ. Photon emission and absorption use the same matrix element,
not independent forward/reverse constants. This establishes a channel, not its
finite-age efficiency.

For a chosen bound J0 state and u J1 continuum we report energy-normalized radial
matrix elements from box-state strengths divided by level spacing. In the
isotropic dipole convention sigma_PI/a_D²=(4pi² alpha/3) omega |D_E|², with the
J0->J1 angular sum included and polarization average1/3. This is a selected
rovibrational channel in this approximate basis, not total chemistry. It omits
nuclear-spin exchange factors, other surfaces and multipoles. No radiative-rate
population claim is made from it. Box/mesh comparisons assess only this model.

Primary cross-check of E1 parity rule: NIST Atomic Spectroscopy, Spectral Lines,
https://physics.nist.gov/Pubs/AtSpec/node17.html . Homonuclear g/u parity and
matrix element above are derived directly here. This is standard molecular
physics, no novelty claim. The wavefunctions and integrals are explicit, so no
unverified external molecular potential is imported.

## Restricted equilibrium network with explicit countercharge

Species X+, C-, A0, T+ conserve N_X=N_C=N. Let x=nX/N, a=nA/N, t=nT/N,
c=nC/N. Then x+a+2t=1 and c=x+t. Charge x+t-c=0 identically.
Only neutral atoms and singly charged molecules are included. Neutral X2C2,
negative ions, excited atomic states, interactions and condensed phases are
omitted; this is not a full equilibrium solution of the Coulomb Hamiltonian.
Statistical weights are1 except molecular rotational multiplicity2J+1; nuclear
spin exchange selection is not enforced. This is an explicit statistical model.

In a dilute Maxwell-Boltzmann gas at temperature T (k_B=1),
nX nC/nA=K_A=(mu_XC T/(2pi))^(3/2) exp(-B_A/T),
nA nX/nT=K_T=(mu_AX T/(2pi))^(3/2)/Z_T,
Z_T=sum_(bound v,J)(2J+1) exp(D_vJ/T).
Here mu_XC=M/(M+1), mu_AX=M(M+1)/(2M+1). Translational masses use finite M;
electronic energies remain leading BO. No arbitrary binding or equilibrium
constant is supplied. The molecular internal energy follows the same spectrum.

With k_A=K_A/N,k_T=K_T/N, t=x(1-x)/(2x+k_T), a=k_T(1-x)/(2x+k_T).
Solve x(x+t)=k_A a. A useful diagnostic bound is t<=1/(2+sqrt(K_T/K_A));
it follows from t(x+t)=a² K_A/K_T and x>=0. Internal rovibrational Z_T is retained;
using only a ground-state degeneracy can spuriously strengthen this bound.

Total matter energy per initial pair is
U/N=3T(1+x)/2-B_A a-[B_A+<D>_T]t.
For an initially fully ionized isolated parcel at T_i, solve U(T)=3T_i. Binding
energy heats the remaining degrees of freedom. This is a microcanonical-energy
matched ideal-gas equilibrium endpoint, not a time-dependent rate calculation.
No radiation is removed in this endpoint. Formation requires actual three-body
or radiative processes to approach it; their timescale is not inferred.
Also report fixed-T endpoints distinctly as externally thermostatted diagnostics.
Mass defect is leading nonrelativistic binding energy, not a fully relativistic
rest-mass evolution. Total constituent mass and charge are conserved explicitly.

## Common-parameter environmental screen

Use the existing numeric (baryon mass, radius) pairs (3e5Msun,.3kpc),
(1e8,1), (6e10,3), (1e14,300). Common reservoir factor eta5.364;
rho=3eta Mb/(4pi b³), sigma²=G(1+eta)Mb/(6b),
N=rho/[(M+1)m], k_B T_i=(M+1)m sigma²/2.
This assumes an initially equipartitioned mixture with the stated total virial
kinetic energy. It does not derive thermalization, a disk, or morphology.
Vary common alpha and light mass; same equations for all profiles. Molecular
charged mass fraction fT=(2M+1)t/(M+1). Neutral atoms count as non-tethered mass
in this diagnostic, not as free fundamental particles. They do not carry the
old positive tether charge. Retain all four composition fractions for clarity.

Flag ideal-gas/ground-atom applicability: small quantum degeneracy (<.1), small
plasma coupling (<.1), dilute atomic/molecular sizes (<.01), T/E_H<=.05, and
nonrelativistic light-particle temperature T alpha²<.01. These are conservative
screens, not a proof all omitted physics is negligible. The morphology target
fT(index2)>=.8 and other three<=.2 is an output comparison only, not an equation
or selector. No successful equilibrium point would by itself establish finite-
age formation, repulsive tethering, acceleration/lensing consistency or disks.
