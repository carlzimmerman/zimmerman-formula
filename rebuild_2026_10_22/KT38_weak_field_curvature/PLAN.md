# KT38: curvature correction suppressed in weak fields

The user authorized new response laws while keeping baryons and observational
cuts fixed. This is a new, explicitly specified construction within the
generalized-action framework, motivated by KT37's isolated dwarf deficit and
its short-wavelength linear response. It is not Milgrom Eq.16 verbatim and
is not claimed to follow from a fundamental theory.

Starting checkpoint: KT37 analytic law and compatible, factored FV Hessian
`mw/generalized_v3.py`, plus accepted covariance and energy controls.
The original KT37 angular implementation and its provisional empirical scores
were withdrawn after a spherical covariance failure. No such scores transfer
to this new law. Exact source hashes are pinned in each run.

## Fixed candidate

    x=|g|^2/a0^2, s=ell^2(H:H)/a0^2, z=x+s^2,
    P=x Q(z)/z, Q(0)=0, Q'(z)=nu_simple(sqrt(z)).

There is one physical length ell shared by all matter. The exponent 2 is an
explicit phenomenological functional choice, not a derived number or a
hidden free fit. There is no Gaussian convolution or object-mass assignment.
The complete response is

    A=[R-1+x R']g,
    B=2 ell^2 s x R' H,
    Delta Phi_ph=div A-double_div B,  R=Q/z.

For simultaneous weak-amplitude scaling of g,H, the new curvature term is
fourth order while x is second order. Thus away from persistent zero-gradient
saddles the leading deep-MOND response is restored. A uniform limit through
all saddles is not assumed. Around a constant nonzero field with H=0, B begins
at cubic order in H: KT37's additional negative k^2 linear term is absent.
These statements are targeted analytic checks, not dynamical health proofs.

## Predeclared discriminators

Lengths: .3, 1, 3, 5, 10 kpc, both original a0 footings. All original MW
1,375-cell populations, four primary cuts and separate strict Lh remain
fixed. Solar mass, external field and ceiling remain fixed. The auxiliary
isolated dwarf test retains the old 24 objects and 41 Upsilon values on [1,3].

Owners: response_obstruction owns analytic/ and dwarfs/; cassini_sign_route
owns cassini/; root owns mw/ and integration. Every worker writes only within
that scope. KT37 sources remain frozen and are imported read-only.

Before empirical scores: Newton mutation, ell=0 QUMOND, direct full-energy
variation, source reciprocity, spherical covariance and spherical analytic
reduction. Solar interpretation requires full Hessian terms, smooth-core
contacts, and an audited point-source limit. Every accepted candidate needs
spatial/angular/domain refinement. No replacement of the baryon density or
cut relaxation is authorized or used.

Current status: **checkpoint complete**. The initial five lengths and the
explicitly adaptive 1.5,1.75,2,2.25,2.5 kpc continuation have completed on both
footings. The ten-length Milky Way grid has zero four-cut passes; all sampled
Cassini quadrupoles pass; isolated dwarf counts and their limited meaning are
recorded in [README.md](README.md) and [RESULTS.json](RESULTS.json). No continuous-
length exclusion is claimed. The initial MW serialization failure remains a
failed record; fresh complete runs preserve all rows and the original cuts.

Closure verification is in [VERIFICATION.json](VERIFICATION.json), reproduced
by `verify.py --check`. The root closure aggregates lane outputs without
editing their frozen inputs. The active next route is the explicit exponent
interpolation [KT39](../KT39_power_curvature/PLAN.md); no result is assumed.
