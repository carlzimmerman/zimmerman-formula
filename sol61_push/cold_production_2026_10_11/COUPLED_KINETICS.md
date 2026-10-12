# Coupled isotropic source–daughter kinetics

Status: a finite conservative kinetic calculation evolves both species and
shows population/energy redistribution. It removes the fixed-bath assumption
from RESONANT_KINETICS.md for a homogeneous isotropic test. It does not model
spatial heat flow, gravity, halo settling or a profile attractor.

## Nonrelativistic resonance and reduction

Use daughter kinetic energy e=p^2/(2 m^2 u^2) and source energy above two
units of daughter rest mass ec=1+P^2/(4 m^2 u^2). Physical excess energies
are m u^2 times these variables. This keeps the leading mass gap M-2m=m u^2
and source inertial mass 2m. Relativistic corrections are omitted; at the
chosen u=0.001 their natural relative scale is order u^2 in this reduction.

Momentum and energy conservation in phi+phi <-> chi require

    ec=e1+e2,
    cos(theta)=(e1+e2-2)/(2 sqrt(e1 e2)),
    (e1+e2-2)^2 <= 4 e1 e2.

The last inequality selects pairs with a physical relative angle. With the
identical-particle factor included, angular integration of the collision
measure in RESONANT_KINETICS.md gives the net source number-production rate

    Rchi = [g^2/(16 pi^3)] integral_allowed dE1 dE2 J,
    J=f1 f2-F(1+f1+f2),

where E1,E2 here are dimensional daughter kinetic energies. To check the
normalization, the angular delta-function integral is
16 pi^2 m^3 dE1 dE2; multiplying by the nonrelativistic invariant measure
and |2g|^2/2! gives the displayed coefficient. The phase-space convention
is the one already checked against [PDG Kinematics](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf).

Set w0=(m u)^3/(2 pi^2). The isotropic densities are

    nphi = w0 integral de sqrt(2e) f(e),
    nchi = w0 integral dec 4 sqrt(ec-1) F(ec),  ec>=1.

For a fixed source energy, allowed daughter e1 spans an interval of length
2 sqrt(ec-1). Dividing its spontaneous loss integral by the source measure
therefore gives g^2 u/(16 pi m)=Gamma_NR, matching the leading rest-source
width independently. This provides a normalization check beyond moment
conservation, which alone would not fix the rate.

## Conservative finite discretization

Daughter centers are e_i=(i+1/2)de and source centers ec_k=(k+1)de. Every
allowed ordered pair (i,j) maps exactly to k=i+j. Its collision flux removes
one particle from each daughter shell and adds one source. The ordered-pair
symmetry factor is already included in the rate above.

The shell weights are wp_i=sqrt(2e_i)de and wc_k=4sqrt(ec_k-1)de. Source
centers at or below threshold carry no continuum shell weight and are not
updated. No coherent zero-momentum condensate is represented. The angular
boundary is a midpoint mask, not a cell-integrated quadrature.

Writing f=A a and F=A b, the flux is proportional to

    de^2 [a_i a_j-b_k(a_i+a_j+1/A)].

Time is tau=2 Gamma_NR A t in natural units. This retains the spontaneous
term although it is negligible for the large A used here. Shell-number
updates divided by their respective weights preserve exactly the discrete
moments

    Q = sum wp a + 2 sum wc b,
    Eexcess = sum wp e a + sum wc ec b.

The physical energy, to the retained order, is mQ + m u^2 Eexcess, times
the common density normalization. A non-equilibrium positive sample's
collision moments are checked separately from the evolution. The classical
Rayleigh–Jeans detailed-balance family a=1/(e-mu), b=1/(ec-2mu) also makes
the leading quadratic collision flux vanish. This algebra does not assert
that the finite-time solution has reached that family.

## Illustrative evolution

Use the existing m=1e-12 eV, g=9.07447e-47 eV and u=0.001. Initially there
are no source particles and the daughters have the stipulated isotropic
Gaussian spectrum with density 1e-21 kg/m^3 and one-dimensional dispersion
200 km/s. Thus A=2.28630e53 and one tau unit is 0.278437 Gyr. These halo-like
inputs are not predicted by the earlier formation calculations.

For N=256 daughter shells up to e=8:

| Time | Source fraction of total charge | Daughter mean e | Source mean ec |
|---|---:|---:|---:|
| 0 | 0 | 0.66676 | — |
| 0.278 Gyr | 0.19971 | 0.62411 | 1.67540 |
| 1.392 Gyr | 0.39900 | 0.54614 | 1.69690 |
| 2.784 Gyr | 0.42302 | 0.51918 | 1.73613 |
| 5.569 Gyr | 0.41189 | 0.49565 | 1.82218 |

The daughters cool in the limited sense that their mean kinetic energy
falls. This is not net energy loss: converting two daughters into the heavier
source stores m u^2 of energy per conversion in extra rest mass. The total
kinetic energy in these units is Eexcess-Nchi. Population conversion and
kinetic redistribution both contribute; there is no spatial energy current
in this homogeneous calculation.

The source fraction is already nonmonotonic at the sampled late times, so
the endpoint is not a frozen yield. A halo cannot be assigned a universal
cooling time from this table.

## Resolution and verification

At the 5.569 Gyr endpoint the source charge fractions are 0.40222, 0.40789
and 0.41189 for 64, 128 and 256 daughter shells with emax=8. The last
refinement changes the fraction by 0.00399. Initial quadrature moments also
change modestly across grids. No continuum precision is claimed.

Doubling emax to 16 at fixed de=0.0625 changes the endpoint source fraction
by 3.01e-8. The outer-shell charge diagnostic is about 2.2e-6 in the finest
e=8 run. These support insensitivity to that high-energy cutoff over the
tested time, while low-energy/threshold resolution remains a larger error.
They do not justify an infinite-time limit or neglect of a condensate.

All 28 checks pass. The largest relative charge and energy drifts across
all four runs are below 3.2e-15, and sampled occupations stay nonnegative.
`coupled_kinetics.py`, its contract and
`coupled_kinetics_run/manifest.json` preserve the experiment. Evidence and
interpretation are self-reviewed. Conserved moments validate the update's
structure; they do not validate the kinetic closure against coherent field
physics.

## Consequence and next physical gap

The same microscopic resonance used for formation can, in a declared
incoherent kinetic regime, exchange substantial populations and redistribute
energy without an external bath. This supplies a concrete collision channel
rather than an imposed relaxation toward a target halo temperature.

The calculation omits spatial streaming, self-consistent gravity, coherent
condensates, elastic quartic scattering and correlation corrections. It
must not be treated as the complete dynamics of the charged action. A heat
current requires spatial dependence and an angular distribution; an isotropic
homogeneous calculation cannot determine its sign or magnitude. No vacuum-
dependent coupling or baryonic mass selector has been added, so this result
does not derive the repo's acceleration law or establish the full medium.
