# Independent local-SUSY, Goldstone and critical-sector review

2026-10-20. Reviewer: gap_selection_physics, author of EXTENDED_SUSY.md.
Base b37b50b1c; criteria-only commit 1d58a0851. The original healthy
microscopic xi=1/4 and full formal-bridge goal remains open.
This is independent analytic review of P0/P1/P3. Remarks on P2 are author
self-review, not independent evidence. No script, build, download, scan
or Lean run was used; no other author's source was edited.

## 1. Exact files reviewed

All files are in this directory; SHA256 pins:

| File | SHA256 |
| --- | --- |
| LOCAL_SUSY.md | d1b104c3440decf0473540f974d963ebc4a3c113c340ba2e489b08b5458cbecb |
| SOURCES_LOCAL_SUSY.md | 91948b04636314961337c2d12dc4f33b9b5d804531e9a58006efb5eac752be72 |
| GOLDSTONE.md | a29364b134bd4768bdb7a4ffd5114a1f8a6b51c43611423c560d2e31285ec21c |
| SOURCES_GOLDSTONE.md | 4995d39fe8dd13159e37d9823d3a54c182190a1984de5bdea15def752058ed3e |
| CRITICAL_SYMMETRY.md | c19743fb0b06876363309ddda9ed275e8de4b35b4618f3e66f08f2ddee69f159 |
| SOURCES_CRITICAL.md | 1f11df72b1e6857e6afedaa1025e73ac7086cf48d3956fca023dfc882e3b12c7 |
| EXTENDED_SUSY.md, author self-review only | 321aa3c412e19d683f3a946cf7c65ec11c01d0498b0920b6361738b0e6a20314 |
| SOURCES_EXTENDED.md, author self-review only | ba2e140b70d65f804783f8013d7ba7b8c56e395b3b4d7cd3bf0ba0db07219206 |

I authenticated primary exact-version headers and selected load-bearing
text for Dall'Agata--Farakos1512.02158v2 section3.2 Eqs71--79;
de Rham--Tolley1003.5917v2 Eqs2--9 and its gravity caveat;
Nicolis--Rattazzi--Trincherini0811.2197v2 Eqs52--57;
Banerjee--Buican2306.12521v2 section4.3 dimension/freely generated powers;
Cordova--Dumitrescu--Intriligator1602.01217v1 Eq1.10;
Hellerman et al1505.01537v4 section3.3; and
Komargodski--Schwimmer1107.3987v2 Eqs2.13--2.14.
Other supplied source cards were read, without claiming new authentication
of every citation or a source-byte cache. The computations below are
independent applications, not external MOND theorems.

## 2. P0: the exact deformation is compatible with local N1 symmetry

The real constrained-matter formula must be used after removing A's
auxiliary. It gives exactly U_eta=f_eta^2-3w^2 and kinetic Z^2/2;
the unconstrained A potential would be a different theory. The local
positive holomorphic square-root branch and bound r<=1/64 ensure F_S
does not vanish on the real slice. At the common vacuum the eta-dependent
jets start at sixth order, so the specified vacuum/quadratic data remain
unchanged. The source's own component formula supports this application.

The ordinary S,T diagnostic also checks independently. At S=0 the metric
is block diagonal with entries z_eta and Z^2/2, and the inverse gives
V=e^(Z^2 y^2) f0^2/z_eta(x). Both S=0 and y=0 are transverse stationary
slices. Cross metric entries are O(S); they cannot supply an S tadpole.
At the common origin z_eta=1 and its relevant derivatives vanish.
Expanding the full inverse metric gives 1+4c|S|^2/Lambda^2 in its SSbar
entry. The other |S|^2 coefficients cancel as 1+2-3, leaving

    m_S^2=4c epsilon/Lambda^2,
    m_y^2=2epsilon, m_x^2=0.

These are positive retained transverse scalar masses with regular local
bosonic kinetic terms. They are not a full fermionic/quantum UV theorem.
The separate Khoury-response implication dC3/deta=1/s_eta^3>0 checks;
the report correctly does not claim a completion of that entire portal.

## 3. P1: exact Ward and physical-source checks

For the inherited canonical real order parameter the independent kinetic
jet forces Q'=0. Independent h^2 and h^4 coefficients then force Q=0;
the remaining reflection permits U_eta. This is the specified fixed-metric,
fixed-source internal-point classification, not a universal symmetry list.

Direct variation of flat DBI gives the stated divergence plus
[2(1+X)P_X-P] b.partial pi. Requiring its Euler derivative to vanish
forces that bracket constant, hence the square-root plus independent
constant. The induced-metric matter current has the reported sign and
contravariant stress indices, and gives no linear source at constant pi.
The separately imposed charged flux gives a quadratic IR and a finite
flux singularity, rather than MOND.

For AdS DBI the particle expansion gives canonical charge
-1/(ell sqrt(T)) and attractive scalar coefficient 1/(4pi T ell^2).
The displayed finite constant-brane potential is stationary only when
A_t=T, with zero value in its explicitly stated zero-additive-constant
convention. A flat-probe constant also preserves the scalar Ward identity;
its gravitating meaning requires a bulk/metric completion. Thus the
geometric charge improvement is real, while its force and state still
fail the requested pair of limits.
No independent graviton Newton constant is inferred from a probe modulus.

The general-n cubic Galileon current has exactly the coefficient (n-1)
and radial power r^(n-2)h^2. The four-dimensional static polynomial has
powers giving h proportional to r^-2, r^-1/2 or r^0, after the stated
d1=0 background subtraction. The static quintic vanishes by Hessian rank.
The source-breaking and matter/gravity-loop qualifications are retained.

## 4. P3: critical source, stress and duality

For the concrete H1 Coulomb primary, Delta=4/3 gives the proposed bottom
source's dimensional energy power 3/2. The full Coulomb-vacuum trial-state
argument then gives runaway if those homogeneous sectors are admissible.
The report explicitly excludes fixed boundary-sector and modified-source
claims from this conclusion. Q^2 and Q^4 descendants instead have the
reported source dimensions and one-scale powers 12/5 and 6.

The common-domain Hermitian affine Hamiltonian infimum is concave.
Its finite right tangent bounds the subtracted response from above, so
a leading positive z^(3/2) is excluded under exactly those hypotheses.
The spectral sign is used only in its isolated-eigenvalue domain.
The portal dimension equations and primary unitarity comparisons check;
derivative descendants, nonlocal/multiscale sources and other ensembles
are correctly kept outside that small classification.

I independently checked the minimal static stress variation, the off-shell
Wess--Zumino coefficients, and sqrt(-ghat)Rhat^2=36(Box tau-X)^2 in flat
space. The on-shell scattering representative cannot be transferred to
a static sourced calculation without changing the other operators.
Neither exact anomaly data nor the nonzero stationary compensator fixes
a positive vacuum in the displayed unbroken conformal state.

For general spacetime D, P=c X^(D/2) gives n=Dc mu^(D-1),
epsilon=(D-1)c mu^D, p=epsilon/(D-1) and cs^2=1/(D-1).
The fixed-n Legendre envelope has positive quadratic spatial stiffness.
In D=3, substituting n=sigma B gives exactly the stated |B|^(3/2)
coefficient, with sigma explicitly a flux convention. The independent
static scalar Legendre transform has coefficient 2/[3sqrt(3C)] and
returns the original C|h|^3 for every C>0. These dual descriptions do
not select a gravitational charge, vacuum or crossover amplitude.

## 5. P2 self-review and scoped disposition

For my own N2 packet I checked FI auxiliary elimination, p's constant,
canonical scalar normalization, the analytic t relaxation and the allowed
holomorphic prepotential jet. The nonstationary v=0 slice and missing
gravitational/matter operator are explicitly retained. This is self-review;
independent reconstruction was supplied by the other packet authors.

No required algebra correction remains in P0/P1/P3 at the pinned revisions.
Their constructive content and limits stand: N1 permits the exact real
potential; the tested exact shifts/brane/Galileon symmetries select other
responses; the interacting protected data and dual ensembles do not give
the requested sourced same-state amplitude. This review does not establish
an all-symmetry no-go, a microscopic completion, a global halo or xi=1/4.
