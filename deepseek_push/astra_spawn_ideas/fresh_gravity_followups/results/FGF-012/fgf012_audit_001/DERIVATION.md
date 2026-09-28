# FGF-012 independent audit derivation (written before numerical audit)

Audit agent: Astra /root/catalogue_audit; no DeepSeek execution. Evidence setup
started 2026-09-27T18:46:07Z. The numerical manifest records actual child start/end.

## Claim and conventions

The core is a=kappa c sqrt(G rho_Lambda), with kappa adopted. Constant vacuum
density means constant a; a=a0 sqrt[.315(1+z)^3+.685] is a separate comparison,
not identified with the same constant vacuum model. Both a0=9.3619e-11 and
1.1279e-10 m/s^2 are required. Pressure identity a^2=kappa^2 G(-p_vac) needs
p_vac=-rho_Lambda c^2; thermal gas pressure below is a different quantity.

Positive inward hydrostatic acceleration is gH=-P'(r)/rho(r). At fixed
physical radius, if gas density is multiplied everywhere by eta>0 and the
pressure gradient by p>0, gH_new=(p/eta)gH. Spherical gas mass scales by eta;
stars are held fixed. With C=G M_sun/(r kpc)^2, masses in solar masses,
B_new=C(Me+Ms), eta=Me/Mx, and gH=C Mh. Force equality therefore gives

    p_required = Me F(C(Me+Ms);a)/(Mx C Mh).

This is a MOND source/force transformation, not a Newtonian missing mass.
Q=sqrt(B^2+aB), R=B/[1-exp(-sqrt(B/a))]. M remains the registered monotone
radial implementation from the pinned stage-three constraint.py. Q/R and all
mass parsing/interpolation/matching will be separately implemented here; M
will be called from its registered implementation and clearly marked shared.

For positive masses and fixed a,r with monotone F, the numerator increases
with Me and Ms and the denominator increases with Mx,Mh. Thus rectangular-box
extrema are opposite corners. Enumerating all 16 corners checks arithmetic;
it does not turn marginal intervals into joint probabilities. A rectangular
superset ceiling below one remains a deterministic exclusion of p=1 for any
correlated subregion contained in that box, but unknown systematic excursions
and unknown joint coverage remain outside it.

## Raw data, stopping rule and controls

Audit exactly seven measured-star clusters and their cached eRASS1/PSZ2 nearest
neighbors, including rejected neighbors, with <=5 arcmin and |delta z|<=.01.
Use a haversine sky separation independent of the worker's SkyCoord call.
Use FITS units and per-file R500 headers to convert radii; JSON R500 is not a
replacement for a FITS R/R500 conversion. Keep nominal eRASS R500 fixed;
require it inside each gas/star/hydro support; do not extrapolate. Record
raw row identities, endpoint units, brackets, and center offsets. Equal kpc
labels alone do not establish equal angular apertures, centers or cosmology.

Mass boxes retain the registered interpretations: eRASS gas endpoints,
X-COP gas error magnitudes, hydro symmetric error magnitudes, star endpoints.
Their numerical ordering is testable; pipeline probability semantics are not
authenticated merely by that ordering or a column name. Log-mass/log-radius
piecewise interpolation is fixed. Alternate interpolation of endpoint masses
will be tested as a sensitivity, not substituted silently.

Use float64, deterministic arithmetic; no randomness. One bounded computation
will terminate after 120 s wall time, 110 s CPU, 1 MiB logs and cooperative
single numerical-library thread. No claimed memory/affinity cap. Source hashes
must agree before interpreting results. Missing input or numerical exception
means implementation/data failure, never a physical refutation.

## Attempt to falsify a broader reading

Enclosed gas mass constrains the volume integral, not rho(r) at its boundary.
Dropping uniform density shape while holding pressure fixed gives the equality
rho_new(r)/rho_old(r)=gH/F(B_new;a)=L. It need not equal eta=Me/Mx.
Split original gas into an outer layer containing fraction f=.05 of Mx and
an inner part containing 1-f. Choose outer density multiplier L and inner
multiplier t=(eta-f L)/(1-f). When t>0 this positive two-zone profile has the
same enclosed Me and exactly closes the local force at the audited boundary
with p=1. A step can be smoothed with arbitrarily small adjustments to the
interior normalization. No claim is made that this profile fits X-ray imaging
or additional shells. It is a constructive negative control on extending an
enclosed-mass result to arbitrary density shape, not a refutation of the
stated uniform-shape conditional result.

## Information independence

A pressure reconstructed by integrating rho*gH satisfies -P'/rho=gH identically;
its boundary zero point adds integrated signal while leaving the derivative
unchanged. A PSZ2 integrated Y or ACT+Planck file is not an independent resolved
pressure gradient. Algebraic near-identities YX~KT*MGAS and FGAS~MGAS/M500 do
not authenticate pipelines, but cannot be promoted into new independent
likelihood factors. Shared Planck information and unknown cross-covariance
must remain explicit. Photon/instrument differences alone do not prove
independence of plasma, geometric, mass-proxy or aperture inference.
