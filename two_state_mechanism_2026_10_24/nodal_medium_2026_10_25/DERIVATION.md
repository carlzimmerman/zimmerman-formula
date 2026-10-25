# A different route: derive the critical response from a nodal quantum band

## What this construction does and does not claim

This route replaces a prescribed gap distribution by an explicit interacting-
with-field fermionic band Hamiltonian. It is an effective quasiparticle model,
not a derived self-assembled dark material or an exact interacting many-body
phase. A microscopic interaction that creates and stabilizes the band remains
missing. Do not treat a possible electronic band structure as evidence that
astrophysical matter occupies it.

Use five anticommuting Hermitian4x4 matrices Gamma_a, with
Gamma1=tau_x tensor I, Gamma2=tau_y tensor I,
Gamma3,4,5=tau_z tensor sigma_x,y,z. Consider

h(p,E)=xi(p_x,p_y)*Gamma1 + v_z*p_z*Gamma2
       -d*(E_x*Gamma3+E_y*Gamma4+E_z*Gamma5),
xi=(p_x²+p_y²-p0²)/(2*m_star).

At E=0 this has a nodal ring p_z=0,p_x²+p_y²=p0². The field opens an isotropic
spectral gap: eigenvalues +/-sqrt(xi²+v_z²*p_z²+d²|E|²), each twice degenerate.
The electric term is gauge invariant, and a number-conserving bilinear in the
fermion fields. It is an effective neutral interband dipole response; it does
not create an uncompensated monopole source. If the fermions themselves have
a gauge charge, the occupied density requires explicit compensating carriers.
The SO(3) property of these matrices establishes spectral isotropy, not a full
microscopic spatial/inversion symmetry or a relativistic gauge completion.

## The linear density of states follows from the dispersion

Let u=sqrt(xi²+v_z²*p_z²). Since p_perp*dp_perp=m_star*d xi,
for u<Lambda<p0²/(2*m_star) the integration domain never reaches the physical
p_perp=0 boundary. Angular integration in the two transverse coordinates gives

g(u)du=C*u*du, C=g_deg*m_star/(2*pi*hbar³*v_z),

where g_deg counts the occupied negative-energy degeneracy and independent
flavors, consistently once. This density of states follows exactly in the
stated low-energy cutoff domain; it is not a sampled exponent or a galaxy-type
assignment. The cutoff, effective mass, velocity and existence of a nodal ring
are still band-structure inputs. The underlying quadratic dispersion cannot
be extrapolated to arbitrarily large relativistic momentum.

At half filling and T=0 the negative bands are occupied. The field-dependent
energy density relative to E=0 is

Delta F=-(C/3)*[(Lambda²+d²E²)^(3/2)-Lambda³-|dE|³].

The polarization is -partial F/partial E, giving
P=C*d²*E*[sqrt(Lambda²+d²E²)-|dE|].
Define chi=C*d²*Lambda and e=dE/Lambda. Then

P/(chi*E)=sqrt(1+e²)-|e|.

This is exactly the predecessor critical constitutive curve. Here the exponent
and interband dipole coupling follow from one explicit effective Hamiltonian;
they were not assigned as an independent oscillator density. Because the mass
matrices anticommute with both kinetic matrices, the dipole transition matrix
is nonzero even near the node. A mere acoustic DOS would not give this result.

This is positive partial progress: an effective band realization of the needed
zero-temperature response. It is not a derivation of its microscopic material,
parameters, preparation, gravitating mass or dark-matter force law.

## Stability cannot be omitted

F above is matter free energy at imposed E, not the complete field Hamiltonian.
For the previous Maxwell dielectric use ell(E)=E²/2-DeltaF, D=partial ell/partial E.
Its longitudinal derivative is positive for the cutoff band: D'>=1. The proper
static energy at fixedD is the Legendre transform E*D-ell(E), not DeltaF alone.
Positive static differential response does not establish dynamical causality,
collective stability, absence of spontaneous band gaps or full gauge invariance.
No negative matter free energy is a free energy source: changing E exchanges
work with the field/source. Finite-temperature F includes entropy; it is not an
isolated energy evolution or a new cooling calculation.

## Temperature and filling are actual state variables

At T>0 and chemical potential mu, the negative-minus-positive band occupation
is f(-r-mu)-f(r-mu), r=sqrt(u²+d²E²). It equals
sinh(r/T)/[cosh(r/T)+cosh(mu/T)] in units k_B=1. At mu0 the factor is
tanh(r/(2T)). Therefore, with t=kBT/Lambda,

P/(chi*E)=2t*[log cosh(sqrt(1+e²)/(2t))-log cosh(e/(2t))].

At zero field chi_T/chi=2t*log cosh(1/(2t)); at small t this is1-2t*log2.
For every fixed positive t the weak-field response is analytic. With the
original charge matching retained, the source has a leading linear term.
This thermal smoothing has a different coefficient from the four-level atom
but does not evade its qualitative obstruction. A critical collective phase
outside this quadratic band can change it; none is assumed here.

At T=0 and finite mu_bar=|mu|/Lambda, the response is
P/(chiE)=max(sqrt(1+e²)-max(|e|,mu_bar),0).
Pauli blocking removes the low-energy dipole transitions. This independently
requires filling near the node, not just a low temperature. Particle-hole
symmetry can pin half filling for a suitable neutral lattice at exact density;
that lattice and density state are not derived for a galaxy. Finite mu changes
particle number at fixed chemical potential, and its countercharge/mass budget
must change correspondingly; it is not a free tuning knob at fixed inventory.

## Local charged-carrier speed bound: audit the light-mass escape

For a restricted local realization with one positive and one negative carrier
per polarizable unit, charges +/-q and dipole operator p=q*(x_plus-x_minus),
dot p=q*(v_plus-v_minus). If each carrier's velocity operator along the measured
axis has norm<=c and the potential commutes with positions, then

Delta*|p_0n| = hbar*|<0|dot p|n>| <= 2*hbar*q*c.

For a constant transition dipole d=q*ell and interband gap2Lambda this implies
Lambda<=hbar*c/ell, or Omega_max<=2c/ell. This is a current-matrix-element bound,
not the heuristic assumption that every transition takes one crossing time.
It remains valid as carrier masses are reduced within these fixed-number,
local-dipole hypotheses. Pair production, genuinely nonlocal collective dipoles,
additional carriers and momentum-dependent interaction currents require a new
analysis; this bound is not asserted for all possible nodal media.

The same critical curve and one pair per occupied-state inventory give
n=C*Lambda²/2=chi*s_max/(2d), s_max=Lambda/d. Under the predecessor force and
a0 matching, rho_medium*ell=(1+epsilon)*f²*a0/(8*pi*G), f=chi/(1+chi).
Hence a local realization cannot simultaneously hide its dipole length in a
small mass inventory and arbitrarily raise its cutoff by taking epsilon->0.
Combine a thermal tolerance t_tol with the speed bound:
T<=t_tol*hbar*c/(k_B*ell_min), using the full dark reservoir for the optimistic
ell_min. Do NOT transfer the independent-pair count blindly to a strongly
correlated many-carrier collective band; that is a named restriction.

## Parameter and goal accounting

Band parameters: m_star,v_z,p0,Lambda,d,flavor multiplicity and filling/state.
The linear exponent is now derived rather than fitted. Matching chi,a0 and
counting mass constrain combinations but do not determine a unique band or a0.
Carrier charge conservation is respected by interband transitions. No interband
excitation becomes a positive tether source merely because it polarizes.
There is no demonstrated rotation-selected nodal phase, mobile-countercharge
transport, disk/dwarf/cluster population separation or RAR observational fit.
The absence of galaxy-type switches in the Hamiltonian is necessary, not sufficient.
