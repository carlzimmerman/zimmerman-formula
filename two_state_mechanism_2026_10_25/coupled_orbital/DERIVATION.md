# Self-consistent orbital, countercharge and elastic dynamics

Base findings commit: 4b7cbb7865eb1997a7ada1609e79da49a8e9f745.
This is a necessary-condition microscopic Hamiltonian test, not an assumed
successful galaxy model. Use the established opposite-parity orbital band.
The research-program and computation-audit workflows govern these bounded tests.

## Choices and scope

A static Hartree calculation would test screening but omit energy transport.
An imposed relaxation law would not meet the user's conservation requirement.
We instead use Hamiltonian Ehrenfest dynamics with a self-consistent Poisson
field and moving, elastically bound ionic countercharges. All coefficients are
common across initial states. Initial rotation and occupation temperature vary
continuously; no galaxy-type parameter appears. This approximation does not
include photons, spontaneous quantum phonon emission, gravity or crystal assembly.

On a periodic cubic lattice (spacing1, hbar1), one spinless charged particle per
cell half fills a two-orbital band. Let W contain occupied orbitals weighted by
sqrt(f): R=WW†, 0<=f<=1. Each cell has an ionic countercharge -Q with displacement
vector u and canonical momentum p, mass M. Let n_i=Tr R_ii, s_i=Tr(tau_x R_ii),
z_i=Tr(tau_z R_ii). Orbital polarization is d s_i e_z; ionic polarization is
-Q u_i. Their charges are deposited consistently to linear displacement order:

rho_i=Q(n_i-1)+rho_source,i - sum_a D_a[d s_i delta_az-Q u_ai].

D is the skew-adjoint central lattice derivative (sin k symbol), including
periodic boundary terms. Source has zero mean and is static; it does no work
after initialization. It represents a probe charge pattern, not baryonic charge.
The central polarization deposition has Nyquist blind modes; it is an explicitly
specified lattice approximation, not a demonstrated continuum charge shape.
Let L be the positive nearest-neighbor Laplacian with symbol sum4sin²(k_a/2).
phi=kappa L^+ rho, zero mean, and U_C=1/2 sum rho phi. kappa contains Q-independent
field normalization; Q is set1 in numerical units. This is electrostatics,
not a causal radiative Maxwell completion. The full physical charge is conserved:
sum rho=Q(Tr R-N)+sum rho_source=0.

H=Tr(R H0)+U_C+sum p²/(2M)+K/2 sum_(i,a,b)(u_(i+e_a),b-u_i,b)²
  +g sum_i (div u)_i z_i,
H0(k)=[2-cos kx-cos ky-cos kz]tau_z+sin kz tau_y.

The deformation term is an assumed linear strain derivative of orbital energy.
Numerical g=-4/3 illustrates a confinement energy m∝a^-2, with m=2 and isotropic
strain div u≈3 delta a/a, giving g=-2m/3. This is a material assumption, NOT a
universal relation for an inverted band. M=100,K=10,kappa=1,d=.2 are common
finite-test coefficients, not derived cosmological constants. Retain all as
material inputs; no capture, damping or forward/reverse rate is added.

Varying the SAME Hamiltonian gives
h=H0+Q phi_i I+d(D_z phi)_i tau_x+g(div u)_i tau_z,
i Wdot=h W,
udot=p/M,
pdot=-K L u+Q grad phi+g grad z.

Thus the local electric mass is -d E_z with E=-grad phi; it is not held at the
bare source field. Counterions feel -Q E. Charge and dipole polarization both
source phi. There is no extra energy -P.E added on top of U_C, which would
double count the electrostatic interaction. Analytically dH/dt=0:
Tr[h Rdot]=Tr[h(-i[h,R])]=0, with classical canonical terms cancelling.
H0's link currents transport particle number; changes of internal or ionic
polarization supply the bound-current contribution to local continuity.

## Integrator and tests

Split into three exactly solvable Hamiltonian flows:
A: H0 plus elastic kinetic/spring terms (Fourier evolution);
B: U_C; u,n,s and therefore rho stay fixed, orbitals rotate about tau_x with
   scalar phase Qphi, and p receives Q grad phi dt;
C: g(div u)z; u,z stay fixed, orbitals rotate about tau_z, p receives g grad z dt.
Compose A(dt/2) B(dt/2) C(dt) B(dt/2) A(dt/2). Charge and density-matrix
occupation spectrum are exact up to roundoff. Total H has splitting error,
which must converge with dt; never renormalize energy or charge to hide it.

Prepare W from Fermi occupations of H0-Omega Lz at fixed total numberN.
Lz=(X Vy+Vy X-Y Vx-Vx Y)/2, V_a=i[H0,X_a]. Coordinates and this diagnostic
on a periodic lattice have a seam: Omega is an initial circulating-state probe,
NOT physical conserved galactic angular momentum. Evolve with H above, not
H-Omega Lz. Ionic u,p start0; source=.02 cos(2pi z/L). Vary Omega and thermal
occupation with common dynamics. A field-only control sets g0, but counterion
motion and Coulomb energy are still present. No system is named disk or dwarf
inside the numerical law. Measure response, energy transfer and mean angular
momentum; do not call them tether/free fractions.

Orthogonal validation: finite-difference energy derivatives versus orbital,
ionic and deformation forces; charge continuity; timestep refinement; a larger
lattice to expose finite-volume effects; no-source stationary-band control.
The thermal occupation eigenvalues are preserved by Ehrenfest evolution;
coarse energy transfer does not establish true thermalization or capture.

## Why a population claim has an additional prerequisite

The elastic reference lattice retains every counterion and has no dissociation
or assembly channel. It cannot spontaneously make a galactic disk from free
matter. Unitary orbital transport within it also does not define a separate
positively charged tethered species. A rotation-dependent response would be a
local necessary-condition result only. Assigning a tether fraction to polarization,
small field, energy loss or ionic displacement would insert the missing mechanism
by definition. This mathematical limitation persists even if conservation passes.
