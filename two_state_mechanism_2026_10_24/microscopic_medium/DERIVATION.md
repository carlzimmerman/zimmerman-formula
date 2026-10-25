# What microscopic dynamics actually fix

## Coulomb pair

Let masses m and epsilon*m carry +q and -q, with kappa=q²/(4*pi).
In units hbar=c=1, reduced mass mu=epsilon*m/(1+epsilon),
H_rel=p²/(2*mu)-kappa/r gives E_n=-B/n², B=mu*kappa²/2.
a_B=1/(mu*kappa). The ground-state electric-dipole spectrum starts at
Delta_2=3B/4, not at zero. All ground-to-bound excited gaps are
Delta_n=B*(1-1/n²); their accumulation point is B. The continuum also starts
at B. Arbitrarily small adjacent Rydberg spacings are not low-energy excitations
of a ground-state medium. An excited Rydberg population would be an additional
state-preparation assumption, with decay, transport and energy to account for.

For hydrogenic 1s->np transitions the total oscillator strength is
f_n=256*n^5*(n-1)^(2*n-4)/(3*(n+1)^(2*n+4)). In atomic units B=1/2,
|d_x|²=f_n/(2*Delta_n), summed over the degenerate p manifold for one axis.
Thus both the actual gaps and their dipole weights are fixed once m,epsilon,q
are specified; there is no free forward/reverse rate or formation-energy knob.
This does not fix those three microscopic constants. Radiative formation needs
photons; the particle test below does not simulate that process.

## Simplest collective alternative

A diatomic nearest-neighbor chain has spring constant K, masses m and epsilon*m,
and the mass-normalized dynamical matrix
D(k)=[[2K/m,-K*(1+exp(-ik))/sqrt(epsilon*m²)],
      [conjugate,2K/(epsilon*m)]].
Its frequencies squared are eigenvalues. The charge-coupling vector is
z=(q/sqrt(m),-q/sqrt(epsilon*m)); a normal-mode dipole matrix element squared
is hbar*|z.dot(e)|²/(2*omega). At k=0 the acoustic eigenvector is proportional
to (sqrt(m),sqrt(epsilon*m)), so its dipole coupling vanishes exactly.
The optical mode is charged but gapped: omega²=2K*(1/m+1/(epsilon*m)).
A gapless mechanical DOS therefore does not supply a gapless uniform electric
response. Finite wavelength, disorder, interactions and boundaries can mix
modes; none derives the required critical weighted distribution automatically.
K and the lattice itself are assumptions, not parameters fixed by Coulomb theory.
This is a diagnostic counterexample to the DOS shortcut, not a model of a galaxy.

## Transport Hamiltonian and accounting

Use dimensionless G=M_b=b=1 and N baryon particles plus N positive and N
negative particles. Total dark mass eta=5.364, m_plus=eta/[N*(1+epsilon)],
m_minus=epsilon*m_plus. The numerical particles are macroparticles, not the
quantum atoms above. Set charges +/-sqrt(lambda)*m_plus, so lambda is the
positive-positive Coulomb/gravity ratio. Test lambda=1 (vacuum force matching),
epsilon=.1. No phenomenological dielectric or preceding fitted chi is inserted.

H=sum p_i²/(2m_i)+sum_{i<j}(q_i*q_j-m_i*m_j)/sqrt(r_ij²+h²).
F_i=sum_{j!=i}(q_i*q_j-m_i*m_j)*(x_i-x_j)/(r_ij²+h²)^(3/2).
All constituents move and gravitate, including neutral pairs' constituent mass;
there is no added medium mass or duplicate free reservoir. Central pair forces
conserve momentum and angular momentum; the time-independent H conserves energy.
Softening h is a numerical regularization. It prevents Coulomb collapse but is
not a derived microscopic core. Report h sensitivity rather than call it physics.
The full causal parent would have Maxwell field energy and retarded transport;
Newton/Coulomb evolution only checks its slow-motion limit. Rest-mass energy of
binding and radiation are beyond this Newtonian test.

Initial conditions use common isotropic position sampling and a continuous spin
fraction in kinetic energy, with total K=.35*|U|. Two preparation endpoints:
independent charge positions, or near-coincident positive/negative pairs. These
are the same choices for every physical scale, not galaxy-specific assignments.
No cold disk or dissipation is imposed. A pair diagnostic requires mutual nearest
opposite neighbors and negative instantaneous relative two-body energy including
gravity. It is NOT the desired positively charged tethered population: a neutral
pair cannot become that population by renaming it. Report inner charge counts
and mass, shape and rotation separately. No capture/ionization classifier changes
forces, masses, charges or energies.

## Exact scale reduction and its boundary

For this classical model x=b*xhat, mass=M_b*mhat,
t=sqrt(b³/(G*M_b))*that. With the same eta,epsilon,lambda,h/b and dimensionless
initial conditions, all trajectories are identical for every M_b,b. Thus the
four historical mass/size profiles are one dimensionless test, not four
independent simulations. Spin can change dynamics but cannot distinguish a
rotating dwarf from a larger rotating system with the same dimensionless state.
There is no a0 in this Hamiltonian. Consequently it cannot predict a universal
acceleration transition: a dimensionless acceleration simply rescales as GM/b².
This is an exact limitation of the tested classical approximation. It does not
apply to a quantum theory retaining fixed a_B, or radiation/cooling, or a genuine
collective critical phase. Introducing a common physical core would break the
homology but is not justified by convergence of a macroparticle solver.

Required target from the predecessor: n(s)*d proportional to s down to s=0,
s=Delta/(2d), with a mass- and sum-rule-consistent normalization. Neither a
Coulomb ground-state atom nor the uniform acoustic mode supplies this target.

Reference cross-checks: NIST hydrogen level and oscillator-strength compilations
https://pml.nist.gov/PhysRefData/Handbook/Tables/hydrogentable5.htm
https://srd.nist.gov/jpcrdreprint/1.3077727.pdf
A Coulomb glass single-particle DOS is a different observable from neutral dipole
response: https://arxiv.org/abs/1105.1712 . No Coulomb-glass result is used as a
proof of this model's spectrum.
