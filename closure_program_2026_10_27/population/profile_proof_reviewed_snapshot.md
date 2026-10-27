# Hard-edge profile admissibility: a bounded necessary-condition result

**Result.** The literal hard-truncated **cluster** Burkert profiles in X38 and
SC1 cannot be regular, nonnegative, isotropic collisionless equilibria confined
inside their stated boundary without a reflecting wall. Their interior density
approaches a finite positive value at the boundary; such a distribution
function requires density to vanish there. This is a physical-admissibility
obstruction for that equilibrium interpretation, not an observational exclusion
of all halo profiles, all cold-fluid models, M6, or the wider mechanism family.

**Exact claim and hypotheses.** Let a stationary spherical component have
an isotropic distribution function f(E), where

    psi(r) = Phi(r_t) - Phi(r),       E = psi(r) - v^2/2.

Assume a finite continuous potential with psi(r) > 0 in an interior
neighborhood and psi(r) -> 0 as r -> r_t from below. Confine the component
without a wall or an exterior source: its regular energy distribution has
f(E) = 0 for E <= 0. Isotropy would otherwise populate radial orbits with
energy above the boundary potential, which can reach/cross the boundary.
Assume f is an ordinary measurable nonnegative function and its density is
finite at some interior potential psi_0 > 0. No nonzero boundary-force
assumption is needed. Baryons may contribute to Phi; self-gravity alone is
not required for the argument.

Integrating velocities gives

    rho(psi) = 4 pi sqrt(2) integral_0^psi f(E) sqrt(psi-E) dE.       (1)

Since sqrt(psi_0-E) >= sqrt(psi_0/2) on [0,psi_0/2], finite rho(psi_0)
implies f is integrable there. For 0 < psi < psi_0/2,

    0 <= rho(psi) <= 4 pi sqrt(2 psi) integral_0^psi f(E) dE
                 = o(sqrt(psi)).                                  (2)

The last step is absolute continuity of the integral of an integrable
nonnegative function. Thus rho(psi) -> 0. A positive finite jump to vacuum
contradicts (2). Allowing a nonintegrable positive divergence of f near E=0
does not repair it: it makes (1) infinite at every positive psi. This is an
analytic argument, not a conclusion from a finite numerical scan.

For a bounded regular f near zero, the stronger condition is
rho = O(psi^(3/2)); if f is continuous with f(0+) = f_0 > 0, then

    rho(psi) ~ (8 pi sqrt(2)/3) f_0 psi^(3/2).                     (3)

More generally f(E) ~ A E^p, p > -1, gives
rho ~ 4 pi sqrt(2) A B(p+1,3/2) psi^(p+3/2). If the inward binding force
has a finite positive boundary magnitude g_t, then
psi ~ g_t (r_t-r), permitting the corresponding radial powers. At a
turnaround boundary with g_t = 0 that translation is not justified; (1)–(3)
remain statements in relative potential and the vanishing-density result
still holds under the stated potential assumptions.

This agrees with the ergodic hard-truncation obstruction in Baes,
*Self-consistent dynamical models with a finite extent – II. Radially
truncated models*, arXiv:2301.03873v1 (2023), section 2.1. Its discussion of
tangential models also illustrates why the result must retain its isotropic
scope. The proof above is self-contained; the source corroborates it.
[Exact source version](https://arxiv.org/html/2301.03873v1).

**Application to the actual code.** In X38, the enclosed cold-component mass is

    M_c(r) = pi Sigma r_0^2 B(min(r,r_t)/r_0),
    B(x) = log(1+x^2) + 2 log(1+x) - 2 atan(x).

Differentiation inside r_t gives

    rho_c(r) = Sigma r_0^2 / [(r+r_0)(r^2+r_0^2)],
    rho_c(r_t-) = (Sigma/r_0)/[(1+x_t)(1+x_t^2)] > 0,
    x_t = r_t/r_0.                                                (4)

Outside, M_c is constant and rho_c=0. The mass is continuous: there is no
surface mass delta in dM/dr. The density nevertheless jumps. Every finite
positive Sigma, r_0 and r_t has this problem, independent of the quality of
its fitted lensing prediction. Numerical differentiation on a finite radius
grid blurs the jump but does not supply a physical distribution function.

Source anchors (repository-relative):

- `rebuild_2026_10_22/X38_a0_surface_density_halos/FROZEN_CRITERIA.md:35`
  explicitly places zero cluster density beyond r_ta.
- `X38_a0_surface_density_halos/x38_sd_halos.py:52` defines B; lines 56–64
  return a positive finite compact root (or the disclosed saturation root).
  Lines 111–113 impose min(R,r_ta); line 109 differentiates mass numerically.
- `SC1_self_coupled_core_law/sc1_core_law.py:75`–77 uses the same Burkert
  mass and truncation, replacing Sigma by positive Sg. SC1's core-law
  motivation is isothermal; its implemented profile is still Burkert.
  `SC1_self_coupled_core_law/FROZEN_CRITERIA.md:10`–16 states that distinction.
- The SPARC functions in X38 lines 93–96 and SC1 lines 60–62 use B(R/r_0)
  without min(R,r_t). Normalization at R200 alone is not a hard cutoff.
  The current obstruction is therefore not an audit of those galaxy profiles.

The saved X38 result contains positive cluster **tercile medians** of r_0:
0.2388–0.4381 Mpc across the two footings/backgrounds; Sigma is 106.8793 or
129.1646 solar masses/pc^2. These are not paired per-cluster (r_0,r_t) records.
SC1 saves positive median Sigma multipliers (1.8405, 1.9420, 2.1535), but
does not save per-object roots. We therefore do not manufacture numerical
edge densities by pairing unrelated medians. Equation (4), the positive-root
construction, and the explicit cutoff settle the sign for the finite
profiles. A bounded re-evaluation of the original X38 K1 root fixture is
recorded separately in `run_PROFILE_001/profile_checks.json`; it is a check
of the actual root/mass formula, not a re-run of the cluster catalog.

A hard-truncated isothermal density with a finite positive edge value has
the same obstruction. An unlowered Maxwellian does not naturally have compact
support. The result does not assert that a collisional fluid with a different
equation of state or a physical confining surface obeys the collisionless
formula (1); that would require a separate boundary/dynamical analysis.

**Precise remaining requirement.** Before calling a replacement a regular
isotropic equilibrium, declare its potential and an energy cutoff, and make
rho(psi) vanish with at least the bounded-f condition O(psi^(3/2)) if bounded
f is claimed. A merely positive smooth density or an arbitrary taper to zero
does not prove global distribution-function nonnegativity. For example a
lowered isothermal f proportional to exp(E/sigma^2)-1 for E>0 behaves as E
near zero and gives rho proportional to psi^(5/2). This is an example of a
compatible local boundary, not a fitted replacement or a global existence
proof for this program.

Any proposed replacement still needs the global DF/Poisson consistency check
in its actual combined potential, normalization and exact shear projection,
and a fresh common-profile observational test with its changed boundary.
Anisotropic distributions, non-equilibrium transport, walls and genuinely
different fluid models are outside this theorem. A successful admissibility
check would remove one necessary-condition failure; it would not establish
formation, stability, conservation through formation, or a complete theory.

The empirical hard cutoff can remain a declared lensing boundary convention.
It cannot simultaneously serve as a proven no-wall isotropic equilibrium.
All historical artifacts are preserved. Independent proof review is recorded
in `AUDIT_RECORD.json`; the bounded computation is supporting evidence only.
