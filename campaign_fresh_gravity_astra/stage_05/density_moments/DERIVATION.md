# DM1: what two integrated density moments can and cannot bound

Parent: independently reviewed FGF-012 density-shape countermodel. This route
adds one observation beyond its enclosed mass: an idealized integrated
emission measure. It does not fit either cluster, a detector or a plasma.

## Precisely defined observation model

Use positive volume measure normalized to one on a spherical aperture. Let
x=rho/rho_ref>0, with independently specified moments

    mean(x)=mu>0, mean(x²)=nu, V=nu-mu².

The second moment represents integrated emissivity only if composition,
emissivity coefficient and geometric weights are fixed and known. Real
temperature-dependent emissivity and resolved profiles are extra constraints,
not established by this toy observation map. We do not assert independent
mass and emission information in an actual X-ray gas-mass reduction.

Take 0<V<mu². The strict upper bound is sufficient for the equal-volume
two-component construction below; it is not a necessary condition for all
positive density distributions.

## Exact three-region construction

Prescribe any finite target density L>0 in a boundary shell occupying volume
fraction epsilon, 0<epsilon<1. Divide the remaining volume into equal halves
with constant densities x_minus=m-sqrt(v), x_plus=m+sqrt(v), where

    m=(mu-epsilon L)/(1-epsilon),
    v=[V-epsilon(V+(L-mu)²)]/(1-epsilon)².                 (D1)

Direct substitution yields EXACTLY

    (1-epsilon)m+epsilon L=mu,
    (1-epsilon)(m²+v)+epsilon L²=nu.                     (D2)

As epsilon tends to zero, m tends to mu and v tends to V. Since
mu>sqrt(V)>0, sufficiently small positive epsilon gives v>0 and
m>sqrt(v)>0. Thus for every finite L>0 there is a positive finite-volume
three-region profile with the same two integrated moments and that shell
density. No limit of zero shell volume is needed for any fixed finite L.
An ideal piecewise-constant profile suffices for this counterexample; no smooth
hydrodynamic equilibrium or full radial pressure solution is asserted.

The construction falsifies a universal inference from these two integrated
numbers alone to a unique or finite upper pointwise density bound when shell
width is unrestricted. It does not falsify a fit to resolved X-ray/SZ images,
temperature spectra, regularity constraints or a complete dynamical model.

## There IS an exact finite-volume bound

Even without the equal-volume construction, the complement has mean m and
nonnegative variance. Decomposing total variance between a constant-density
region L and its complement gives

    V >= epsilon (L-mu)²/(1-epsilon),
    epsilon <= V/[V+(L-mu)²]                            (D3)

when L differs from mu. Equivalently, if a correction is independently known
to occupy volume fraction at least epsilon_min>0,

    |L-mu| <= sqrt[V(1-epsilon_min)/epsilon_min].         (D4)

This is an exact necessary condition, not generally sufficient once additional
positivity, geometry or dynamics constraints are imposed. It specifies what a
spatial extent or regularity constraint would add. An instrument PSF width is
NOT automatically a lower bound on the physical thickness of a density
feature: unresolved thin structures remain possible without further evidence.

If V=0, mean[(x-mu)²]=0 forces x=mu almost everywhere. This equality case
blocks any different L on a positive-volume shell and is a decisive negative
control. At a measure-zero point integral data still make no pointwise claim
without regularity. D1's square root is not real when D3 is violated.

## Gravity and the user's scale stay explicit

Fix aperture r, enclosed baryonic mass and stars, and the thermal pressure
gradient at the boundary. Preserving the first density moment preserves that
gas mass and thus B=G(Mgas+Mstar)/r². For Q or R separately,

    Q: F=sqrt(B²+aB), R: F=B/[1-exp(-sqrt(B/a))],
    rho_required=(-P')/F(B;a).

With a=kappa c sqrt(G rho_Lambda), carry both reference a values and constant
vacuum versus the separate a(z)=a(0)E(z) history. Each specified branch gives
a finite positive L=rho_required/rho_ref if -P'>0. D1 applies to that value;
it does not alter the MOND acceleration or fit an arbitrary extra mass.
The same integral argument is independent of the kernel for any specified
finite positive F, including a correctly evaluated M branch. This does not
derive the filtered-MONO field equations or transfer spherical flux assumptions
to a filtered nonlocal model.

Changing rho at fixed pressure changes temperature in an ideal-gas model,
which can change real emissivity. Consequently preservation of this idealized
second moment is not a claim of preservation of actual detector counts under
a coupled thermal change. The exact scientific gain is an observation-map
counterexample and a finite-volume bound, not a cluster repair.

## Bounded verification and interpretation

`check_moments.py` uses rational arithmetic for D1/D2 and positivity checks at
mu=3/2, nu=5/2, seven rational L values from 1/10 to 100. No square-root
roundoff enters the moment equalities; numerical roots are display only.
Controls deliberately violate D3, impose V=0, and freeze the compensating
bulk densities. Q/R force-restoration examples use declared synthetic B and
pressure gradient, both a normalizations and vacuum/frozen E(3), not catalog
measurements. Universal claims above rest on algebra and continuity, not
the finite set. No literature mechanism or historical novelty claim is used.
