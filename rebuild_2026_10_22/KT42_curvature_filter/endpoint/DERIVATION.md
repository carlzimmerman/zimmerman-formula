# Constant quadratic curvature endpoints cannot repair the KT40 witnesses

This is a new application of old static-inheritance reasoning, and a bounded
classification of one endpoint modification. It does not introduce a viable
response law. The prior formula and route search is recorded in
`../../KT41_route_inventory/dynamics/AUDIT.md` with its explicit coverage limits.

## Claim and hypotheses

Use KT40's nonrelativistic action conventions in three-dimensional Euclidean
space:

    g = grad psi, H = Hess psi, Delta psi = 4 pi G rho,
    Delta Phi = (1/2) div E_g - (1/2) partial_i partial_j E_Hij,
    a_matter = -grad Phi, W = integral rho r.grad Phi d^3x.

Hold the prescribed ordinary matter density and physical matter coupling fixed.
Consider the constant, rotation-invariant, homogeneous quadratic addition

    Delta E = alpha (tr H)^2 + beta H:H, c = alpha+beta.

Here alpha and beta are real constants with units length squared; they cannot
depend on g, H, density, position or the background. Require enough regularity
for the displayed derivatives, and the boundary qualifications below. For the
local symbol let n be a unit vector and N(n)=E_HH[nn,nn]/2. Then:

1. Delta N(n)=c in every direction and on every background.
2. Delta Phi=-4 pi G c rho, up to the harmonic solution fixed by the boundary.
3. With no extra harmonic field and partial_z rho<0 at z>0, c<0 changes
   partial_z Phi downward. It worsens a previously negative vertical derivative.
4. With a sufficiently decaying centered density and no confining surface term,
   Delta W=6 pi G c integral rho^2. Thus c<0 also worsens a negative total W.

KT40 already exhibited N>0 on some positive-density local jets. Any constant
shift capable of making N nonpositive on *all* such jets must therefore have
c<0. Such a shift cannot repair either the fixed MW outward-force witness or
the fixed uniform-external-field Draco virial witness. A sufficiently large
negative c is not asserted to exist: the necessary-sign argument suffices.
For c>=0 the original positive-N witness remains. Consequently no member of
this constant quadratic family both removes that all-background cold-fluid
obstruction and repairs those specified static failures.

## Exhaustiveness of the stated quadratic class

A real symmetric H can be orthogonally diagonalized. An orthogonally invariant
quadratic polynomial in its eigenvalues is a symmetric quadratic polynomial,
so it has only the independent sums sum lambda_i^2 and
sum_(i<j) lambda_i lambda_j. Since
(sum lambda_i)^2=sum lambda_i^2+2 sum_(i<j) lambda_i lambda_j, these span exactly
the two displayed invariants. An SO(3)-invariant scalar of a single symmetric
matrix gives the same quadratic class: orientation can be restored by changing
one eigenvector's sign without changing the diagonal matrix. A background g
used to form anisotropic contractions would enlarge the class and is excluded.

## Full source and rank-one variation

Differentiation with respect to the symmetric tensor, with the full contraction
convention, gives

    Delta E_Hij = 2 alpha (Delta psi) delta_ij + 2 beta partial_i partial_j psi.

There is no Delta E_g. Commuting partial derivatives yields

    Delta(Delta Phi) = -(alpha+beta) Delta^2 psi.

Solving the Poisson equation gives

    Delta Phi = -c Delta psi + h = -4 pi G c rho+h, Delta h=0.

For the independent rank-one check, replace H by H+t nn. The coefficient of
t^2 in Delta E is alpha|n|^4+beta|n|^4. Thus the second derivative divided by
two is c for |n|=1. The sign is consistent with the Fourier response:
Delta Phi=-c Delta psi gives Delta Phi_hat=+c k^2 delta psi_hat. Thus the
transfer coefficient T=K+Nk^2 changes by **Delta T=+c k^2**, in agreement
with Delta N=c.

## Boundary and null-Lagrangian restrictions

The difference of the two invariants is an exact divergence:

    (Delta psi)^2-H:H
      = div[(grad psi) Delta psi - H grad psi].

Therefore alpha=-beta gives zero bulk source and zero Delta N. Its integrated
energy need not vanish on a finite domain. It can affect natural boundary
conditions unless the boundary variation is fixed appropriately. Bulk
equivalence is sufficient with compactly supported variations or with fixed
psi and normal derivative; boundary stresses cannot be silently discarded.
An affine term proportional to tr H is also a boundary term and does not
change the old rank-one second variation.

For isolated smooth finite-mass densities decaying at infinity, require the
additional potential to decay and introduce no new external harmonic field;
then h=0. A fixed uniform auxiliary external field has zero Hessian and does
not change this contact result. A constant physical acceleration has zero
scalar virial for a centered density. On a finite computational box with an
incompatible imposed zero boundary value for Delta Phi while rho remains
nonzero there, h need not vanish; the formulas require its explicit inclusion
or a controlled isolated limit. This note does not infer an exact finite-box
identity from an asymptotic continuum argument.

## Independent virial route

The force-derived change is

    Delta W = -4 pi G c integral rho r.grad rho.

For a finite domain with outward normal nu,

    integral rho r.grad rho
      = (1/2) integral_boundary rho^2 r.nu - (3/2) integral rho^2.

Thus

    Delta W = 6 pi G c integral rho^2
              -2 pi G c integral_boundary rho^2 r.nu,

plus any contribution integral rho r.grad h. A smooth isolated Plummer density
has both omitted boundary contributions zero. With

    rho = 3M/(4 pi a^3) (1+r^2/a^2)^(-5/2),

direct radial integration gives

    integral rho^2 = 45 M^2/(1024 a^3),
    Delta W/(3M) = 45 pi G c M/(512 a^3).

This sign is an independent force-integral test, rather than an inference from
the sign of the raw auxiliary energy. Raw constrained gravitational energies
may be saddle functionals; no propagating-ghost conclusion is made here.

## Fixed MW source sign

The exact source is `UX5_mw_stellar_mass/ux5_core.py:29-37`, through KT33's
`rho_cell`. At z>0 the stellar terms have logarithmic derivative -1/h; each gas
term sech^2(z/h) has derivative -2 tanh(z/h)/h; the bulge with
r_p=sqrt(R^2+(z/Q)^2) has logarithmic derivative

    -[A/(r0+r_p)+2r_p/r_cut^2] z/(Q^2 r_p).

All amplitudes, lengths and A are positive for the two saved cells. At R=12,
z=.3 kpc, the source's radius floors and far-tail cosh clamp are inactive.
The symbolic experiment checks each expression and independently checks
stellar-column positivity from the pinned source constants. The thin/thick/gas
subtotal is negative; the bulge adds another negative contribution. No density
refit, numerical derivative, force recomputation or different baryon model is
needed to fix this sign.

## Quantitative static changes required by the old witnesses

These numbers are **reused KT40 numerical evidence**, not new continuum bounds:

| Witness | Old value | Necessary additive correction to reach zero |
|---|---:|---:|
| Canonical MW cell1368, R12,z.3, refinement6 | partial_z Phi=-843.7699442474329 (km/s)^2/kpc | >=843.7699442474329 (km/s)^2/kpc |
| Alternate MW cell1287, same point/refinement | partial_z Phi=-936.1114251316735 (km/s)^2/kpc | >=936.1114251316735 (km/s)^2/kpc |
| Canonical Draco, Upsilon2, uniform eta=.01 | W/(3M)=-19.338292177662662 (km/s)^2 | >=19.338292177662662 (km/s)^2 |

The raw sources are `KT40_mechanism/mw/force_001/results.json`, `cases` entries
with `refine=6`, `points` entry `(R_kpc,z_kpc)=(12,.3)`, `force_parts.total`,
and `KT40_mechanism/efe/localize_001/results.json`, `profiles` entry
`Draco/canonical/eta=.01/upsilon=2`, `total_variance_terms.total`.
The independent old force review is
`KT40_mechanism/dynamics/MW_FORCE_REVIEW.md:14-43`; it reports approximately
0.39 percent refinement5-to6 changes, and potential-difference checks. Its
finite-grid error limits remain attached to these extracted thresholds.

Equality merely reaches zero force or virial. A positive-compressibility
decreasing barotropic gas density needs strictly restoring force, and a
stationary system with nonzero kinetic trace needs W>0. The Draco condition
assumes gravity-only equilibrium, positive-mass tracers and vanishing virial
surface stress; it is not a model of the satellite's actual orbit and tides.

## Reused static-inheritance implication

Let q_*(rho) be a stationary auxiliary-field solution with the same boundary
data. If eliminating q leaves the same static functional up to terms with zero
matter variation, the chain rule gives

    delta E_red/delta rho = (delta E/delta rho)_(q_*)
                            +(delta E/delta q)_(q_*) delta q_*/delta rho,

and the second term is zero on that stationary branch. The physical matter
potential is unchanged if the matter coupling is unchanged. Adding positive
inertia, a relaxation time, or a causal kernel with the same fully reduced
static response cannot supply the nonzero corrections in the table. A matching
linear zero-frequency susceptibility by itself does not imply equality of the
nonlinear static functional. Persistent field currents, different branches,
nonstationary density histories, independent gravitating energy, confining
stresses or changed boundary conditions alter the hypotheses.

This implication is prior reasoning, including the repository's static Schur
reductions and covariant-host discussions. The added result here is its explicit
application to the KT40 deficits and the constant quadratic endpoint family.

## Verification scope

`contract.json` fixes the computational assertions and bounds before execution.
`check_endpoint_v2.py` independently constructs the full tensor Euler derivative,
rank-one variation, null divergence, generic virial identity and a complete
Plummer radial integral, then extracts the saved witnesses and checks their
source signs. Symbolic checks supplement the analytic proof; no finite scan is
presented as universal coverage. Three wrong-sign/omitted-component mutations
must be detected. Manifest status and exact check results are reported in
`RESULTS.md` after the run. This is same-author derivation and self-review,
with different symbolic/force-integral routes, not an independent-agent audit.
