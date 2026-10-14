# Direct muon photoproduction and a free-electron recoil bound

2026-10-14. Base checkpoint: 134630e7d321783512b3dfe4e2519aabe6b1679d.
This tests the direct coupling already assumed in the reduced source model,
L_int=-y_mu R mubar mu, with y_mu=2e-4. The reaction gamma+mu -> R+mu
avoids a loop-induced production vertex. It has a nonzero near-rest scalar
amplitude, but the accepted phase space and short-lived target inventory make
the specified cold-source benchmark ineffective.

## Tree amplitude with finite scalar mass

Let p be the initial muon four-momentum, k the incoming photon and q the
outgoing scalar. With metric (+---), both tree diagrams give

    Mcal=e y_mu ubar(p') [ (slash(p+k)+m_mu)/(2p.k) slash(epsilon)
                   + slash(epsilon)(slash(p-q)+m_mu)/(M_R^2-2p.q) ] u(p).

The script evaluates the Dirac trace, averaging initial muon spin and photon
polarization and summing final muon spin. Both diagrams are necessary for the
photon Ward identity and the near-rest cancellation. No massless-scalar
approximation is used in the cold-source integral.

For an initial free muon at rest and an outgoing R exactly at rest,
0<M_R<m_mu is required for the physical kinematics. At

    omega_0=M_R(2m_mu-M_R)/[2(m_mu-M_R)],

the spin-averaged result simplifies to

    average |Mcal|^2 = e^2 y_mu^2 M_R^2/[m_mu(m_mu-M_R)].

The dimensionless trace divided by e^2 y_mu^2 is 0.000365217571 for
m_mu=105658375.5 eV and M_R=2 MeV+2e-9 eV. This is nonzero, unlike the
stationary spin-zero Primakoff target's transverse node. However, cancellation
between the two diagrams suppresses this corner by M_R^2/m_mu^2 when M_R is
small. A single-diagram estimate or the massless total cross section would
misrepresent it.

Here omega_0=2019294.148 eV, whereas the reaction threshold is
2018928.930 eV. Producing at the total reaction threshold is not equivalent
to preparing a mediator at rest in the laboratory.

## Cold momentum integral

As in the target calculation, for scalar momentum magnitude P and direction
u=cos(theta) relative to the photon,

    E_R=sqrt(M_R^2+P^2),
    omega(P,u)=[2m_mu E_R-M_R^2]/[2(m_mu-E_R+P u)].

Integrating the energy-conservation delta function over the photon spectrum
gives the production kernel

    average |Mcal|^2/[64pi^2 m_mu omega E_R (m_mu-E_R+P u)].

We multiply by the earlier isotropic scalar-decay acceptance A(P), requiring
both daughters to have laboratory K<=1e-8 eV. The accepted momentum volume
is 0.0513213 eV^3, with P<=0.268328 eV. In this tiny neighborhood the full
kernel is almost constant; explicit angular/radial quadrature agrees with
the rest-amplitude approximation within the tested numerical precision.

For an assumed Gaussian beam with total flux 1e8 photons/s, area 1 mm^2,
energy RMS 5000 eV, and center omega_0, the spectral flux per area is
7.97885e9 photons/(m^2 s eV). Including Br(R -> phi anti-phi)=1/2 gives

    cold pair rate per muon = 3.82252e-49 /s.

This is the tree direct-Yukawa contribution for a free, stationary, unpolarized
muon. Beam polarization, target binding and motion, other production channels,
collection geometry and subsequent losses have not been supplied. It is not
a measured yield or a total cross-section limit for every muon environment.

## A muon delivery rate is not a stored target population

For ideal continuous stopping at rate I_mu and removal only by muon decay,

    dN_mu/dt=I_mu-N_mu/tau_mu,
    N_mu,steady=I_mu tau_mu.

The MuLan measurement, [Tishchenko et al., arXiv:1211.0960v1 / Phys. Rev. D
87, 052003](https://arxiv.org/abs/1211.0960v1), reports the positive-muon lifetime
tau_mu=2.1969803 microseconds. This measured lifetime, rather than a beam flux
alone, controls the ideal stationary inventory. At the ASSUMED stopping rate
I_mu=1e8/s, it is only 219.698 muons on average. Perfect stopping, retention
and overlap inside 1 mm^2 are assumed; no facility performance claim is made.
Negative-muon capture or other removal would change the inventory, and a
bound muon target requires different kinematics and matrix elements.

The resulting ideal inventory rate for this channel is

    8.39801e-47 cold pairs/s.

Avoiding a photon loop does not produce a useful source at these parameters.
The result cannot be improved by treating a muon arrival rate as though it
were a macroscopic persistent population. Pulsed operation requires its actual
time-dependent population and photon overlap; no universal pulse bound is
inferred from this continuous example.

## Why a free resting electron is not a direct substitute

This is a kinematic restriction independent of coupling strength. For
gamma+T -> R+T with a free target initially at rest, take the photon along +z.
Conservation of minus light-cone momentum gives

    m_T=(E_R-P_z)+(E_T'-P_z').

The last term is strictly positive for the outgoing massive target. Since
P_z<=|P|, one has E_R-|P|<m_T. Together with E_R^2=M_R^2+|P|^2 this implies

    |P| > (M_R^2-m_T^2)/(2m_T), when M_R>m_T.

For a free electron initially at rest and M_R=2 MeV this lower bound is
3.6584 MeV, vastly above the 0.268328 eV cold-source acceptance. No choice
of incoming photon energy fixes that two-body kinematic obstruction. It does
NOT apply unchanged to a bound electron with a recoiling atom/nucleus, a
moving target, external fields, or a different multiparticle initial state.
Those are distinct channels requiring their own dynamics and energy account.

LightConeBound.lean proves the momentum inequality from the positive-energy
mass shell and minus-momentum assumptions, and the implication from the
explicit conservation relation. It does not formalize QFT or assert that
every material is a free-electron target.

## Independent source control and empirical obligations

Caputo, Raffelt and Vitagliano, [Phys. Rev. D 105, 035022 (2022), Sec. II B,
Eqs. (4)-(5a)](https://wwwth.mpp.mpg.de/members/raffelt/mypapers/202102.pdf),
provide the massless-scalar semi-Compton cross section. Their assumptions
exclude applying that formula directly to the near-rest massive scalar here.
As an independent normalization check only, setting the outgoing scalar mass
to zero in this code and integrating its angular distribution reproduces
their result at omega/m_mu=0.01, 0.1 and 1. The respective ratios to the scalar
Thomson cross section are 0.98044935, 0.83719121 and 0.37448314.

That paper also treats astrophysical constraints on the muon-philic model.
This calculation does not make the chosen y_mu empirically admissible. Its
extra carrier decay channel and interactions require a consistent constraint
analysis; neither historical magnetic-moment motivation nor an unmodified
bound from a model without those carriers is a viability certificate.
Source checks were performed on 2026-10-14; no broad novelty claim is made.

## Verification and next decision

Thirteen checks pass: Clifford algebra, analytic rest-scalar trace, five Ward
identity cases, three independent massless cross sections, quadrature
refinement, constant-amplitude cold-region control and the electron bound's
comparison with the cold acceptance. The cold integral uses Gauss-Legendre
orders 16 and 32, split at the acceptance change point; their dimensionless
ratios differ by 2.45e-11. This is floating-point agreement, not an accuracy
claim beyond the stated particle and target assumptions. The manifest pins
the prior coupling and acceptance inputs. Lean compilation evidence is separate.

The direct free-muon channel is now calculated and ineffective at the specified
source parameters. Simply substituting free stationary electrons is excluded
for the same cold output by kinematics. The remaining plausible source work
must change the physical preparation: for example a specified many-body
recoil reservoir or a production-and-cooling route with actual cooling rates.
The hot-population calculations and artificial coupling switch do not supply
either. No usable creation or storage mechanism has been established.

Reproduce:

    python3 sol61_push/cold_muon_compton_2026_10_14/check.py /tmp/cold_muon_compton_results.json
