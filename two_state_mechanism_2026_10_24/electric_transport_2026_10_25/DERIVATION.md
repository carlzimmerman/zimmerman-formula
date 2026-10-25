# Electric bond coupling and conservative energy transport

Base: published checkpoint 310c2885e247c229c8a7628a51779e34fcaffa07.
Target remains a dynamical, gravitating, charge-conserving collective medium
with the galaxy acceleration relation and population separation from initial
conditions, not galaxy labels. This checkpoint tests necessary ingredients;
it is not a galaxy formation simulation or a complete microscopic material.

## 1. Physical charges constrain the effective electric operator

Take a neutral cell with charges +Q,-Q, rest masses m+,m-, relative displacement
x along a specified bond, reduced mass mu=m+ m-/(m++m-), and center coordinate R.
Its dipole is Qx, not a quasiparticle rest mass times a fitted dipole length.
Minimal electromagnetic coupling of the two charges conserves charge; in the
long-wavelength electric-dipole limit the interaction is -Qx E. Both masses,
ionic elastic energy, and collective excitations contribute to gravity.

For a Mott bond with one particle per site, virtual double occupation costs U.
Second-order hopping gives H_ex=J(x)(S_i.S_j-1/4), J=4t(x)^2/U.
With t=t0 exp(-x/r0), J'= -2J/r0. This exponential overlap is a material model,
not a universal law or derivation of t0,U,r0. A spin-orbit material can instead
have an anisotropic bond operator; its coefficients must be derived separately.
The scalar Hubbard model does NOT by itself derive a Kitaev phase.

Let O be the symmetry-allowed signed combination of bond operators and g=J'.
H_cell=p_x^2/(2mu)+K x^2/2+g x O-Q E x+H_band.
In a centrosymmetric crystal a polar x cannot couple to an inversion-even O.
Use an inversion-odd difference of opposite bonds, or an explicitly polar cell;
assuming either is an additional material specification, not spontaneous disk
selection. In the static/adiabatic limit completing the square gives

H_eff=H_band-(QE-gO)^2/(2K),
P=Q^2 E/K-Qg O/K.

Thus the effective electric bond coefficient d_b=Qg/K and attraction g^2/K
are linked to the ordinary ionic susceptibility chi_ion=n Q^2/K:
(n d_b^2)/(g^2/K)=chi_ion. They are not three independent knobs.
For dynamic x, retain its kinetic energy and retarded oscillator response;
instantaneous elimination is not a causal transport law. The ionic response
has frequency sqrt(K/mu), not a postulated scale-free electric spectrum.
Coulomb longitudinal forces must be included once, not added again to an
already screened irreducible susceptibility. The transport test below is an
elastic subsystem, not a solved Maxwell/Poisson medium.

## 2. Bond modulation is not an anticommuting mass

A locally real two-band nodal-line patch has H0=v1 q1 tau_x+v2 q2 tau_z.
Real changes of nearest-neighbor bonds add a(E) tau_x+b(E) tau_z: the node moves.
The missing mass tau_y is imaginary and is forbidden while this real symmetry
is preserved. Extra bands, symmetry breaking, or other physical operators can
evade this restricted statement. It is not a theorem about all spin liquids.

Use uniform transverse state measure C d^2q/(2pi) in a unit disk, absorbing
velocities and nodal-line length into C. For a bond displacement s, the occupied
energy is F_shift(s)=-C int_0^1 r dr (2(r+|s|)/pi)
E_elliptic[4r|s|/(r+|s|)^2]. For an actual mass,
F_mass(s)=-C[(1+s^2)^(3/2)-|s|^3]/3.
The mass has +C|s|^3/3 after its analytic quadratic term. The translated node
has no such cubic: shift integration coordinates; a fixed neighborhood of the
moving zero has constant integral, and all changed boundary terms are analytic
for |s|<1. Rotational symmetry makes the analytic series even. A critical
node-annihilation boundary is outside this argument and requires tuning.

Test B(h)=[F(2h)-4F(h)+3F(0)]/(4h^3). It tends C/3 for a mass and zero for the
bond shift. The latter cannot supply the previous positive |E|^3 free-energy
term, hence cannot retain that mechanism's deep-acceleration law after linear
matching. Changing cooling rates cannot repair the missing static operator.

Literature check (2026-10-25): Kanega, Ikeda, Sato, arXiv:2101.06081v2,
https://arxiv.org/html/2101.06081 (29 July 2021 revision), Fig.1 and Eqs.1-2,
uses electric bond modulation that changes Jx and Jy. Its supplemental S3
assumes a single relaxation coefficient; that coefficient is not a microscopic
energy-transport derivation. This is supporting 2D context, not a 3D realization
of the model here. HTML Eq.2 is malformed; Fig.1's coupling changes are explicit.
No novelty claim. No article text copied into this derivation.

## 3. Replace an imposed damping rate with an elastic energy carrier

A bounded Hamiltonian test of a polar optical displacement x_i coupled to a
scalar acoustic displacement u_i on a 3D cubic lattice is

H=sum_i [mu xdot_i^2/2+M udot_i^2/2+K(x_i-a D_x u_i)^2/2
          +k/2 sum_j (D_j u_i)^2].

D_j u_i=u_(i+e_j)-u_i. Here a is an allowed piezoelastic coupling in the chosen
polar material; it is not a derived cosmological constant. mu=M=1 is a valid
reduced-mass ratio (e.g. equal constituents of mass2 give mu1); M represents a
separate acoustic inertia per cell. The simplified scalar branch is not a full
vector crystal, Maxwell field, or self-gravitating material. Cell countercharge
is explicit but cannot dissociate in this harmonic model. Total free charge is
zero. A neutral electric dipole does NOT acquire the positive monopole charge
needed for repulsive tethered matter.

In mass-weighted Fourier variables the positive dynamical matrix is
A11=K/mu, A12=-K a D_x/sqrt(mu M),
A22=[k sum_j |D_j|^2+K a^2 |D_x|^2]/M, A21=A12*.
Diagonalize this matrix and evolve each mode by cos(omega t),sin(omega t).
There is no damping term: local energy can fall only by flowing to other cells.
Periodic boundaries retain the exported energy. Recurrence is possible.
Physical speed is set by lattice spacing and the springs/inertias; this
nonrelativistic long-wavelength description requires speeds below c. It is not
an exact relativistic completion. All parameter choices here are dimensionless
implementation/transport diagnostics, not astrophysical fits.

For a quantized version, the same eigenvectors fix x-mode matrix elements.
If a collective transition couples as g O x, Fermi's golden rule yields
Gamma_down=(2pi/hbar) sum_alpha |g O_fi x_alpha|^2(n_alpha+1)
 delta(Delta-hbar omega_alpha), and Gamma_up has n_alpha instead.
At thermal equilibrium their ratio is exp[-Delta/(k_B T)]. This fixes the
relation between rates and makes transition energy enter the carrier. It does
not justify a Markov rate in a finite closed lattice, a universal rate constant,
or a formation rate without a specified many-body transition and state.

## 4. Geometry test without galaxy labels in the transport law

Homogeneous ballistic escape time is L/c_s; homogeneous diffusion time scales
L^2/D. For the same transport coefficients and comparable boundary conditions,
smaller systems cool faster. With the established size proxies .3,1,3,300 kpc,
any threshold that lets the 3 kpc system export its energy also lets the two
smaller systems do so. This rules out size-only transport as the desired
selector, not density-dependent scattering or dynamically formed thin disks.

For a rectangular domain with absorbing boundaries, diffusion's lowest decay
rate is pi^2 D(1/Lx^2+1/Ly^2+1/Lz^2), where L are full side lengths. A thin
rotating system could cool faster, but assigning it a small Lz by label would
beg the question. Compute the thickness needed to beat a .3 kpc cube with
Lx=Ly=3 kpc: Lz < [3/.3^2-2/3^2]^(-1/2) kpc. This is a conditional geometry
criterion, not simulated formation. Acoustic energy exported into a bound halo
still contributes to gravity; an absorbing boundary is not free energy loss.

No disk/tether/free fractions are inferred from these tests. The concrete bond
route fails the required static law before population evolution. The distinct
elastic transport construction passes energy accounting but leaves a physical
mass-generating electric operator and self-consistent material assembly open.
