# MG-ZERO: the orbit-history sigma-spread is MG-impossible (theorem + boundary)

**Lane:** MG-impossibility. **Script:** `mg_zero.py` (exit 0, sympy+numpy, both footings).
**Date:** 2026-07-17. **Companion:** `rederive_mi_spread.py` (MI amplitude), `power_analysis.py` (power).

## The claim, stated precisely

In a pressure-supported system (dSph, elliptical, cluster), at a fixed cluster-centric
position `x`, does **every** modified-gravity (MG) theory predict **exactly zero**
non-adiabatic *orbit-history* spread in the internal velocity dispersion of its members --
so that a finite spread is a clean fingerprint of modified **inertia** (MI)?

The observable is the RELATIONAL spread: the variance of `E[ln sigma_int | position x,
internal baryons]` taken **across orbit families** (eccentricity / infall phase) at matched
`x` and matched internal baryons. Not the mean boost -- the spread.

## The MG class and the one structural premise that kills the spread

The class {QUMOND, AQUAL, AeST/TeVeS, f(R), local-modified-g} is defined by:

- **(P1)** the theory **sources a field** `g(x)` from baryons (elliptic quasi-static, or
  hyperbolic/retarded in general);
- **(P2)** matter tracers are **WEP geodesics** of the single (Jordan) metric built from that
  field: a test body's acceleration at event `x` is a **function of `x`** (and, with
  retardation, of the *source's* past) -- **independent of the body's own orbit, velocity, or
  acceleration history**.

Under (P2), orbit shape / infall phase (`y = omega_ex/omega_in`) and velocity `v` label the
**tracer**, and they appear **nowhere** in the equations for the internal dynamics. Hence

    d sigma_int / dy == 0   and   d sigma_int / dv == 0   identically,

for **any** `a0` and **any** interpolation function. This is verified symbolically in `[A]`
(arbitrary `mu`, arbitrary `a0`) and numerically across
{canonical, alt} x {framework nu, standard MOND, exp-RAR} -- four orbit families at matched
`x` give **identical** internal boost, spread `= 0` exactly. **This is a genuine theorem
within the class.** A member's internal heat is fixed by *where it is*, not *how it got
there*.

**MI violates (P2):** the inertial response is a time-nonlocal functional of the body's
**own** worldline 4-acceleration through the kernel `K(Box_u/a0^2)`. Two members at the same
`x` with different orbital histories carry different effective inertia -> the spread. That is
the whole distinction.

## The EFE trap (guards against a false detection)

A **constant** external-field boost `theta0` gives `A = a_in + theta0*a_ex`, a pure position
function -- MG reproduces it trivially by an `a0`-rescale / EFE term. Only the
**y-dependence** `theta(y)` (a member's history-sampling of a *varying* external field along
an eccentric orbit) is MG-impossible. So the discriminator must be the SPREAD across orbit
families, **never** the mean boost.

## Boundary stress test -- can any "MG" force fake the spread? (`[C]`)

| case | mechanism | verdict |
|------|-----------|---------|
| **C1 gravitomagnetic** `F = m v x B_g` | velocity-dependent but antisymmetric | `F.v == 0` (verified) -> does **no work**, cannot heat a member; bends orbits (shared w/ GR), **zero** dispersion spread |
| **C2 dissipative drag** `F = -gamma(x) v` | genuine velocity-dependent force | non-conservative, no medium in a collisionless system; if imposed it **cools** (`sigma -> 0`), no steady spread; not a field theory of `g` -- excluded as MG |
| **C3 disformal/aether coupling** `delta a ~ beta (v.grad phi)` | field couples to the **tracer's own velocity** | **DOES** create an orbit split (9.5% at beta=0.1, 26% at beta=0.3) -- **but** this is a (P2)-breaking, WEP-breaking, **worldline-dependent** response: it is modified INERTIA in an MG costume. It does **not** rescue MG; it **collapses** the MG/MI distinction. Standard MG is WEP-exact (`beta == 0`). |
| **C4 retarded MG** `g(x,t) = F[source past]` | finite propagation, hyperbolic | retardation is in the **source**, not the tracer; every member at `(x,t)` feels the **same** `g(x,t)` -> still `d sigma/dy = 0`. (Contrast: MI's kernel is retarded along the **tracer's own** worldline.) |
| **C5 f(R)/chameleon** `G_eff(x)` | environment-dependent coupling | `G_eff` is a function of local density/potential = a function of `x` -> shared by all tracers -> spread 0 |
| **C3' Finsler/SME** velocity-dependent metric | free-fall depends on tracer's own 4-velocity | same verdict as C3: a kinematic/**inertia** modification (the SME sector), not a sourced field `g(x)` -> collapses to MI, does not rescue MG |
| **C6 non-adiabatic EFE / tidal heating** | member orbits through a time-varying external field | **the honest nonzero, SHARED channel.** MG-field part stays **exactly 0** (g still evaluated at position, no orbit label off-adiabatic, verified). BUT ordinary **tidal heating** (~2-8%) is orbit-history-dependent and nonzero in **both MG and Newton+DM** -- not an MG signal, a real **confound** sharing the MI sign; separated only by radial profile + `y`-correlation (GAP E6), not amplitude |

**The only door that opens (C3) is not an MG door.** Any theory that manufactures an
orbit-family spread has, by construction, made the tracer's acceleration depend on how it
moves -- i.e. it has put orbit-history into the *inertial* response. Whatever one names it, a
finite orbit-history spread **is** the modified-inertia signal. There is no pure
"sources-a-field-g(x)" MG channel to it.

## Jeans-level confirmation (`[D]`) -- an MG "spread" is ordinary anisotropy

Spherical Jeans: `d(rho sigma_r^2)/dr + (2 beta/r) rho sigma_r^2 = -rho g(r)`. The source
`-rho g(r)` is **identical** for every orbit family (the single sourced field has no orbit
label). Two families differ **only** through the anisotropy-transport term `2 beta/r` -- the
**same** beta-vs-sigma degeneracy that Newton+DM already carry. So any residual sigma
structure in MG is indistinguishable from ordinary velocity anisotropy, not a new inertial
term. MI adds, *on top of* `beta`, a term set by the member's own orbit history -- in
principle orthogonal to `beta`, though **beta-degenerate in current data** (that is the power
problem, not a failure of MG=0).

## How airtight is the exact-0, and the honest demotion

- **Exact-0 side: airtight for the MG-SPECIFIC (sourced-field) channel** within the stated
  class, and the class is the natural definition of "modified gravity" (sources a field,
  WEP-exact tracers). It holds for any `a0`, any interpolation, both footings, elliptic or
  retarded field equations, **and off-adiabatic** (C6: `g(x(t))` never acquires an orbit
  label). Labelled a theorem, scoped to the field channel.
- **The only evasion is definitional, not physical:** velocity/disformal/Finsler-SME coupling
  to the tracer's own worldline (C3/C3') -- and that is modified inertia, so it cannot serve
  as a rival MG explanation of a detected spread.
- **The exact-0 is NOT the whole orbit-history spread (honest scope):** ordinary non-adiabatic
  **tidal heating** (C6) is a nonzero (~2-8%), orbit-history-correlated spread present in
  **both MG and Newton+DM**. It is not sourced by the MG sector and is not an MI signal -- it
  is a shared *dynamical* confound that carries the **same sign** as the MI spread. It is
  separated only by the **radial profile + `y`-correlation** (MI peaks at `R500-R200` and dies
  toward the core; tidal heating grows toward pericenter/core and is radially anti-correlated;
  banked separator `GAP_STATEMENT.md` E6, `RECON.md`). So "MG = 0" is precise for the
  modified-gravity channel; it is *not* a claim that the total observed orbit-history spread is
  zero in an MG universe.
- **Demotion note (both ways):** the clean exact-0 baseline does **not** by itself make the
  discriminator powerful. A finite MI spread is `beta(r)`-degenerate, projection- and
  measurement-limited; the in-hand carrier count is a no-go (`power_analysis.py`: `z ~ 0.05-0.24`,
  needs `N ~ 10^3-10^5` at today's tier or a <=10% sigma tier + FJ floor <=0.10-0.15). The MG=0
  side is exact; the MI-detection side is underpowered. Both are true.
- **Not claimed derived:** `a0`'s value and the sign `s=-1` remain postulates. MG=0 is the
  theorem; it is not a derivation of the framework's number.

## Credit

Milgrom 1983 (MOND) / 1999 PLA 253:273 (the nu-kernel wellhead) / 2022 PRD 106 064060 (MOND
as modified inertia; Eq.34-35 two-frequency EFE). dSph kinematics: Walker, Wolf, Battaglia;
Gaia dSph proper motions. Framework-distinctive content = the `cH_Lambda/Z` coefficient + the
MI covariant completion (worldline `K(Box_u)`).
