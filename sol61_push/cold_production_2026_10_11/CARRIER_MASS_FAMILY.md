# Raising the original carrier mass also accelerates its resonance

Status: linked parameter-family audit of the original repulsive charged
production model, without the added nonlinear vacuum-pressure portal.
This returns to kinetic/orbital support and tests whether a mass change
can make its threshold scattering appreciable. It does not establish a
halo transport rate, observational viability or the required halo law.

## Keep one common production family

Hold fixed the chosen source energy density, near-threshold velocity u,
pump parameter epsilon=g A_source/m^2, and lambda_rep=lambda_min=g^2/Delta,
with Delta=4m^2 u^2. Let b=m/m_ref. The source energy normalization gives

    A_source proportional to m^-1,
    g proportional to m^3,
    lambda_rep proportional to m^4.

Therefore the vacuum threshold quantities scale as

    sigma_threshold/m proportional to lambda_rep^2/m^3 proportional to m^5,
    c_contact^2 proportional to lambda_rep rho/m^4 = constant

at fixed halo density. Increasing the mass can increase binary scattering
without making the coherent contact pressure support the halo. In this
family the latter speed stays at the earlier value 0.01997 m/s.

This family holds some dimensionless production parameters fixed, but not
H/(m epsilon), quantum seed occupation, or the cosmological history.
Previous nonlinear yields cannot simply be assigned to every new mass.

## The resonant channel must be rescaled too

At fixed halo density and velocity dispersion, the occupation at the
resonance scales as f_star proportional to m^-4, while the vacuum source
width scales as Gamma_0 proportional to g^2/m proportional to m^5.
The fixed-bath rest-source relaxation coefficient is

    Gamma_0(1+2f_star)=Gamma_ref[b^5+2f_star,ref b].

The vacuum term cannot be neglected as the halo occupation becomes small.
The script retains it. This is the same conditional source-mode diagnostic
as RESONANT_KINETICS.md, not a bulk heat-conduction or settling clock.

There is also a directly relevant initial halo rate. For the initially
source-empty Plummer distribution, the birth integral is proportional to
(g^2 m^2) f_1 f_2. In this fixed-u family that integral's number-production
rate is independent of m: its prefactor scales as m^8 and occupations as
m^-8. Dividing by the daughter number density, which scales as m^-1, gives
an initial charge-conversion rate proportional to m. This scaling uses the
previously normalized initial collision integral; it does not extrapolate
that initial rate through depletion or equilibrium.

## An illustrative threshold target

Choose 1 cm^2/g only as a numerical threshold-cross-section target. No
observational preference, allowed range or halo transport identification
is implied. The rescaling reaches it at

    m=30.67284 eV,
    g=2.61869e-6 eV,
    lambda_rep=1.82221e-9.

For the inherited rho=1e-21 kg/m^3, sigma_1d=200 km/s bath, this gives

    f_star=0.0839867,
    source vacuum lifetime=147.987 seconds,
    fixed-bath rest-source relaxation time=126.704 seconds.

The reciprocal of the initial global Plummer charge-conversion rate is
5,812.57 seconds, about 1.61 hours. The previously computed source radial
orbital periods were of order hundreds of Myr for that halo. The hierarchy
therefore changes dramatically; a collisionless-tracer or slow-reaction
halo treatment would need re-evaluation.

The quoted reciprocal initial rate is not the time to convert the entire
halo, which requires evolving gain, loss and transport. Nor is the source
mode lifetime a transport time. The rate/dephasing-energy ratio in the
fixed bath is about 3.81e-13, so the rapid rate in seconds does not itself
invalidate that particular weak-coupling diagnostic. Other kinetic and
macroscopic approximations still require checking.

The threshold cross section also has a restricted momentum domain. With
the same u=0.001 and coupling ratio, the earlier 10%-accuracy contact
criterion remains p/m<=0.3015 u, about 90 km/s per particle in the pair
center-of-mass frame. A 200-km/s-dispersion halo samples the resonance;
its actual scattering cannot be represented just by the threshold number.
At f_star<1 the earlier highly occupied classical halo approximation is
also inappropriate for those modes; the quantum/statistical collision
operator must retain spontaneous terms.

## Research implication

A mass change can make the contact cross section look familiar while
leaving coherent support negligible and making resonant reactions many
orders faster than orbital motion. It does not provide an independently
tunable scattering rate. Conversely, this result does not exclude all
masses, couplings, source histories or a rapidly equilibrating medium.
Changing u, epsilon or the ratio lambda_rep/lambda_min explores a different
family and needs its own stability, production and transport analysis.

The original kinetic-support route remains logically distinct from the
nonlinear pressure portal. The latter's cosmological pressure problem is
not solved by assigning a larger mass to the former. Neither family yet
selects the required baryonic/vacuum-dependent halo normalization.

## Verification

carrier_mass_family.py independently recomputes the source width,
resonance occupation, SI threshold cross section and contact pressure
for seven masses, then checks their analytic scalings and the illustrative
target. All 43 checks pass; the manifest validates provenance. The initial
Plummer rate uses its derived scaling rather than a fresh quadrature for
each mass. Small differences at about 1e-9 in the SI cross-section scaling
come from the rounded hbar used here versus the earlier SI conversion.
The derivation and interpretation are self-reviewed.

This is concrete progress on parameter selection, not a completed
cold-energy construction or a claim that the interaction is observed.
