# Collective recoil does not supply an unrestricted N-squared gain

2026-10-14. Base checkpoint: 0e180d138d7b4e109e2fd4ac652daebcbd79fdbf.
This tests an unaddressed production idea: a crystal takes the photon momentum
collectively while the proposed 2 MeV mediator is created almost at rest.
The elastic coherent channel must retain its internal-state overlap, and a
Bragg peak cannot be treated as a broadband N-squared production enhancement.

## Center-of-mass recoil and internal overlap are different

At nearly zero outgoing mediator momentum, the target must accept momentum
Q approximately 2 MeV. For a constituent mass M=200 GeV, the free-constituent
recoil energy would be Q^2/(2M)=10 eV. Replacing the recoil mass by the entire
crystal can make its center-of-mass recoil energy much smaller, but does not
remove the internal matrix element of the local scattering operator.

Writing a constituent position as X_CM+R_j+u_j separates the factors

    exp(i Q.x_j)=exp(i Q.X_CM) exp(i Q.R_j) exp(i Q.u_j),

where hbar=c=1 in these expressions. Elastic coherence depends on the last
factor as well as on the center-of-mass recoil. Making the whole object heavy
does not automatically make its internal displacements vanish.

For a harmonic projected displacement u along Q, let Omega be the mode
energy. Its thermal variance is

    <u^2>=1/(2M Omega) coth[Omega/(2k_B T)].

The thermal mean amplitude and its squared magnitude are

    <exp(i Q u)>=exp[-Q^2<u^2>/2],
    f_coh=|<exp(i Q u)>|^2
         =exp[-E_recoil/Omega * coth(Omega/(2k_B T))].

At T=0, coth is replaced by one. The ground-state term remains: cooling cannot
remove zero-point motion. In SI displacement units the same exponent is
Q^2 sigma_u^2/(hbar c)^2. This is an assigned single-mode harmonic model;
the energies below are not measured phonon spectra of a named material.

The script independently checks the thermal characteristic function with
the number-state sum

    <exp(i Q u)>=(1-z) exp(-eta/2) sum_n z^n L_n(eta),
    eta=E_recoil/Omega, z=exp[-Omega/(k_B T)].

Nine cases, eta=0.1,1,5 and z=0.1,0.5,0.8, are evaluated through n=600 at
80-decimal precision. They agree with the Gaussian characteristic function
within the stated 1e-40 relative check. This tests the amplitude calculation;
it does not prove the harmonic approximation for a particular target.

## A generous coherent peak bound

For N identical sites and their static phases a_j=exp(i Q.R_j),

    I_coh(Q)=f_coh |sum_j a_j|^2 <= f_coh N^2.

This is a structure factor relative to one site's squared amplitude, before
the process-dependent kinematic kernel. Relative to the N-site independent
intensity scale, even the optimally phased peak is at most N f_coh. We grant
N=1e23 fully participating sites solely to make this a generous coherence
diagnostic. It is not an experimentally established coherence volume or beam
overlap specification.

| Assumed Omega (eV) | T (K) | Projected RMS displacement (pm) | log10(f_coh) | log10(N f_coh), N=1e23 |
|---:|---:|---:|---:|---:|
| 0.01 | 0 | 3.120 | -434.29 | -411.29 |
| 0.03 | 0 | 1.801 | -144.76 | -121.76 |
| 0.1 | 0 | 0.9866 | -43.43 | -20.43 |
| 0.01 | 300 | 7.138 | -2273.41 | -2250.41 |
| 0.03 | 300 | 2.491 | -276.89 | -253.89 |
| 0.1 | 300 | 1.007 | -45.28 | -22.28 |

At all tested values, the coherent peak cannot enhance the N-site independent
scale, even with perfect phasing. This statement concerns that coherent
component, not the total inclusive scattering or all possible materials.

For N f_coh>=1, the harmonic Gaussian model requires

    sigma_u <= (hbar c/Q) sqrt(ln N)=0.718006 pm.

At zero temperature in the single-mode model this requires

    Omega >= E_recoil/ln N=0.188824 eV.

These are necessary conditions for the generous pointwise comparison, not
sufficient conditions for useful production. They neither identify a material
meeting them nor include the needed incident spectrum and collection geometry.
Other displacement distributions or a full phonon spectrum require their
actual characteristic function, not an arbitrary replacement of Omega.

## Peak height is not integrated gain

For a finite one-dimensional lattice with sites 0,...,N-1,

    S_N(theta)=|sum_j exp(i j theta)|^2,
    (1/2pi) integral_0^(2pi) S_N(theta) dtheta=N,

while its Bragg peak height is N^2. The integral follows by expanding the
double sum: the phase integral vanishes for every unequal pair of sites.
The code checks discrete Fourier counterparts at N=3,17,64 with sufficiently
large reciprocal grids. This does not imply that every physical luminosity
integral equals N; real energy/momentum weighting and reciprocal-space
coverage matter. It rules out simply multiplying a broad uncorrelated-beam
rate by the pointwise peak factor N.

## Coherence does not remove the scalar charge-field node

For the static Coulomb part of the target response, the scalar photon vertex
is proportional to epsilon.q, multiplied by the Fourier charge potential.
Since the incoming transverse photon obeys epsilon.k=0 and q=k-p_R, this
factor is -epsilon.p_R. At p_R=0 the charge-field conversion amplitude is
zero. Multiplying it by a finite lattice structure factor cannot make it
nonzero. This statement excludes transverse current, magnetic, dynamic and
other interaction channels; it is not a claim about every material response.

Consequently a static coherently arranged charge source does not evade the
node found in the preceding stationary-target calculation. At small nonzero
p_R, both the microscopic vertex and the structure factor must be included.

## Do not reinterpret lost coherent weight as cold production

The quantity f_coh is the square of the thermal mean amplitude. It is not,
in general, the fraction of the complete production rate that is elastic.
For example, a thermal average of squared diagonal oscillator matrix elements
is different from the square of their thermal average. Inelastic channels
also have different energy transfer and available final-state phase space.

A full rate must weight an appropriate dynamic charge/current response
S(Q,omega) by the photon spectrum, scalar kinematics and daughter acceptance.
An unweighted matrix-element completeness sum cannot bypass these constraints.
In particular, near the cold threshold it is incorrect to set an omitted
phonon-assisted cold yield equal to 1-f_coh times an elastic rate.

Harry J. Lipkin's primary exposition, [Physics of Debye-Waller Factors,
cond-mat/0405023v1, May 3, 2004](https://arxiv.org/pdf/cond-mat/0405023),
Eqs. (1.1)-(1.4) and Sec. I, distinguishes the bound-system matrix element
from its final-state-weighted transition rate and explains the limitation of
a probability interpretation. Checked 2026-10-14. It supports that distinction;
it provides no material-specific input or evidence for the proposed carrier.
The oscillator calculations and finite-N bounds here are not novelty claims.

## Verification and route decision

Twenty-five bounded checks pass: nine oscillator sums, nine displacement/recoil
normalizations, six Fourier normalization/peak checks and the necessary
zero-temperature scale. CoherentBound.lean proves the finite coherent amplitude
and intensity bounds under unit-norm-amplitude and nonnegative-weight
hypotheses. It does not certify a crystal, an inclusive response or a device.

The proposed shortcut of a free N-squared enhancement for recoilless creation
is not supported. A material-assisted source remains a distinct open route,
but its next useful calculation must supply a dynamic response and its cold
phase-space weighting. Changing N or scanning additional assumed oscillator
energies alone would not establish a source. The alternative production-and-
cooling route likewise needs an actual cooling channel with verified rates.
The manufacturing and storage goal remains unresolved.

Reproduce:

    python3 sol61_push/collective_recoil_audit_2026_10_14/check.py /tmp/collective_recoil_results.json
