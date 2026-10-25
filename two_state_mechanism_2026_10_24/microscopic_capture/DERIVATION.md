# A calculable microscopic candidate and its compatibility test

## Microscopic assumptions, not derived constants

Choose two distinguishable charged species X,C with opposite unit charges under
a massless dark U(1), with coupling alpha_D. The nonrelativistic Hamiltonian is

    H_rel=p²/(2mu)-alpha_D hbar c/r, mu=mX*mC/(mX+mC).

It follows from minimally coupled matter plus a Maxwell action. The ground radial
wavefunction is proportional to exp(-r/aD). Substitution in the Schrodinger
equation cancels the 1/r term when aD=hbar/(mu c alpha_D), leaving

    E_1=-B, B=mu c² alpha_D²/2; E_n=-B/n².

Here mX,mC,alpha_D remain fundamental model inputs, not numbers fixed by
conservation. The code expresses masses as rest energies in eV. Unit charges
and distinguishable species forbid annihilation of the two constituents.
Ground statistical weights use gA/(gX*gC)=1 (spinless species, or unresolved
spin states with this same ratio). A spin-selective channel needs new factors.

The E1 interaction -d.E couples a continuum p wave to the 1s bound wavefunction.
Fermi's golden rule uses that same dipole matrix element in both directions:

    X+C <-> A+gamma_D.

For a Coulomb continuum its evaluated ground-state photoionization cross section
is, with omega the photon ENERGY, z=sqrt(omega/B-1),

    sigma_PI = (512 pi²/3) alpha_D aD² (B/omega)^4
               exp[-4 atan(z)/z] / [1-exp(-2pi/z)], omega>=B.

The threshold limit is 512 pi² alpha_D aD²/(3 exp(4)). Below B it vanishes.
This uses the published Coulomb matrix-element result, not a new independent
derivation of that integral. Eq27 of Rosenberg & Fan (2017) gives the equivalent
expression in the heavy-core limit; relative-coordinate separation replaces the
light mass by mu at leading nonrelativistic dipole order. For opposite unit
charges the relative dipole is charge times r, independent of the mass ratio.
Recoil and relativistic corrections are omitted at this order.

https://link.aps.org/accepted/10.1103/PhysRevD.96.123001

## Inverse rate is fixed by the same matrix element

For the stated degeneracy convention, phase-space balance gives the Milne relation

    sigma_rec(E) = omega²/(mu*c²*E) sigma_PI(omega), omega=B+E.

The factor counts two photon polarizations; different definitions of atomic/ion
spin weights can move a factor2 into the usual tabulated Milne formula. This
normalization is checked by the explicit thermal equilibrium identity below.
No independently fitted forward or reverse normalization is introduced.

Let T and Tgamma denote k_B times temperature, and
f_E(E)=2 sqrt(E) exp(-E/T)/(sqrt(pi) T^(3/2)). Then

    k_rec(T,Tgamma)=integral f_E(E) sqrt(2E/mu) sigma_rec(E)
                    [1+n_gamma(B+E)] dE,
    beta(Tgamma)=c/[pi²(hbar*c)³] integral_B^infinity
                  omega² sigma_PI(omega) n_gamma(omega) d omega,
    n_gamma(omega)=1/[exp(omega/Tgamma)-1].

Speeds in the first expression are physical; the code multiplies the
dimensionless sqrt(2E/(mu*c²)) by c. For Tgamma=0 there is spontaneous capture
but no photoionization. Removing stimulated emission while retaining a Planck
bath would violate the exact equilibrium check.

At Tgamma=T, using n_gamma=e^(-omega/T)(1+n_gamma), both integrals imply

    beta/k_rec = S(T)
               = [mu*T/(2pi*hbar²)]^(3/2) exp(-B/T).

Thus nX*nC/nA=S(T). The tests integrate the two kernels separately; additional
speed-space quadrature checks the energy-space recombination integral.
This is the inverse of radiative capture, not collisional impact ionization.
The latter and its three-body inverse are additional channels allowed by the
same Hamiltonian, omitted from this ground-state radiative subsystem. Excited
states, line transfer, screening and plasma processes are also omitted. Therefore
the code is not a complete atomic-dark-matter halo simulation.

## Physical energy ledger, rather than a restitution parameter

Ignoring recoil at leading order, an individual recombination emits E+B.
There is no adjustable restitution coefficient. With a tether field also present
the event would instead require

    E_gamma+K_recoil = E+B-Delta_U_tether.

Negative right-hand side forbids that channel. Simply inserting this shifted
threshold into the vacuum cross section would not derive the field-dressed
matrix element or its inverse. It requires a microscopic field coupling.

For a constant-volume neutral plasma let n be total X nuclei density, x its
ionized fraction. Then nX=nC=nx and nA=n(1-x). Its internal energy per nucleus is

    u=1.5(1+x)T-(1-x)B.

With no incoming photons, dx/dt=-n*x²*k_rec, and escaped energy per nucleus obeys
dq/dt=n*x²*k_rec*(B+<E>_rec). The temperature follows

    dT/dt=[-dq/dt-(1.5T+B)dx/dt]/[1.5(1+x)].

These equations conserve u+q without a global energy correction. They assume
rapid elastic rethermalization. The temperature may increase because capture
preferentially removes slow relative pairs; radiation loss is not equivalent to
lower temperature when particle number changes. No gravitational contraction or
volume work is present in this closed-parcel check. Photon momentum/recoil and
mass defect are higher-order omissions; the check conserves the stated leading
nonrelativistic energy, not an exact relativistic stress tensor.

## Population screen with universal parameters

Use the four pre-existing numeric (Mb,b) pairs, reservoir eta=5.364, and the same
uniform-volume proxy for each:

    rhoD=3 eta Mb/(4pi b³), n=rhoD/(mX+mC),
    v0²=G(1+eta)Mb/b,
    T=(mX+mC)*v0²/6.

The last expression is a specified virial-temperature proxy for the initially
fully ionized gas, NOT an equilibrium calculation or a disk temperature inferred
from morphology. Units restore c² if rest energies are used. Rotation does not
enter: a common velocity boost leaves the collision integrals unchanged. A
counterfactual rigid rotation at the same local distributions must give identical
rates. Real disks may develop different distributions, which this screen cannot
predict.

At fixed T, no incoming photons, initially x=1, the radiative-only solution is

    f_A=1-x=A/(1+A), A=n*k_rec*t.

Fixed T requires a thermostat (energy exchange); this algebraic screen is not
the energy-conserving parcel evolution above. It is an exposure/selectivity
diagnostic. For desired f_disk>=.8 and f_other<=.2 at a common age, a necessary
condition is exposure ratio A_disk/A_other>=16. The numerical mass scale cancels
this ratio: at fixed mass ratio, alpha_D and virial velocities, k_rec scales as
mC^-2 while n scales as mC^-1. The scan therefore samples 61 alpha_D values for
selectivity and 31 common mass scales for absolute exposure, not independent
binding energies or cross sections for each object.

## Exact obstruction to identifying A with the current T state

The U(1) charge of A is qX+qC=0. Gauss's law therefore gives zero monopole charge
for a distant neutral atom. It cannot simultaneously be the sole positive
source of the existing tether field, whose source is proportional to T mass.
Indeed the free ions carry the microscopic charges, the opposite of the existing
F-neutral/T-charged field assignment. Charge conservation also forbids a neutral
photon carrying away a missing gauge charge in a state-changing event.

This is a conditional no-go for identifying the binding U(1) with the tether
field, independent of the rate scan. A second mediator with state-dependent
scalar couplings or a neutral polarization mechanism is possible, but adds a
new action and parameters and must reproduce w(z), source assignments and the
acceleration relation. Neutral atomic recombination by itself does none of these.
Nor does a dark atom bind to ordinary baryons in this chosen model.

We consequently do not insert a fitted negative binding energy into the old
packet-switching solver or call the resulting atoms tethered mass. Such a run
would conceal, rather than solve, the missing microscopic-to-field connection.
