# Compression source found; formation still unclosed

This phase continues nonlinear_transfer_2026_10_25. Read that phase's STATUS,
ACTION_CANONICAL and HANDOFF before interpreting this changed hypothesis.
All tests concern one synthetic spherical Plummer benchmark. These are not
new fits to real galaxy data and do not establish a population law.

## What was actually added and checked

The original constant-current derivative interaction has no direct source in
conserved bulk T matter. The new proposed effective interaction has charge
q(rho_T)=g1 rho_T+g2 rho_T² and spatial current (g1+g2 rho_T)j_T.
It supplies the actual source

    S=g1 Gamma+g2[2rho_T Gamma-rho_T² div(v_T)].

ACTION.md derives the canonical transformation, positive linked spatial
square, alignment force, extra density chemical potential, scalar source,
and quartic shift charge. The density force from carrier inertia remains
included. There is no supplied compression history or assigned wave power.
The old real static Hamiltonian is exactly recovered at rest, so the static
law and constrained restoring Hessian are unchanged. The new term starts
beyond quadratic order about all F; that preserves the old *linear* exterior
conversion margin, not a nonlinear no-nucleation theorem.

The coefficient g2 is NOT derived from the Zimmerman formula or microscopic
physics. It is matched to one specified compression tangent's induced inertia
as a discriminator: eta=1 gives g2=1716.80273197, eta=.01 gives171.680273197.
It is not fitted to a law residual. K30 and the other inherited constitutive
choices remain assumptions.

The complete force audit finds material derivative relative error1.87e-9,
scalar derivative error5.79e-10, and shift identity error5.34e-16. A pure-T
compression test has a nonzero bulk source with negligible conversion. The
static energy identity is exact in the checked discretization. The first
Picard solver fails strongly coupled steps; those are not physical evidence.
A joint Newton-Krylov solve restores short-step energy/mass/charge closure.
The first Newton script failed on a SciPy import before execution; it remains
recorded, with the corrected version in krylov_checked.py.

## Actual free evolution, with transfer and propagation separated

The infall initial state is the same conservative20% core dilation used in
NT. Density, both material phases, carrier coordinate/momentum and scalar
all evolve. No outer phase conversion is prescribed. The solver rejects
steps that fail physical-cap, nonlinear-root or local-energy tolerances.

| Run | Actual time(Myr) | Total work into scalar | Bulk-current work | Net500kpc flux | Energy error bound |
|---|---:|---:|---:|---:|---:|
| g2=0 control |30.0000|3.28812e-4|0|3.12888e-4|4.47e-7|
| eta=.01, continued |2.08976|2.61674e-4|2.80775e-4|2.34705e-5|3.18e-9|
| eta=1, continued |1.81927|1.19080e-4|8.72902e-5|5.59323e-6|5.46e-9|

Energies are Eunit=3.2572137002e51J. The two continued runs reached wall limits,
not their4Myr targets. Compare curves at equal times, not these different
endpoints. Conversion work can be negative: it is -1.91007e-5 for eta=.01,
and +3.17902e-5 for eta=1. Total work is not all escaping radiation; most
scalar energy is still inside500kpc at these early endpoints. The flux ledger
closes below5.3e-20. The accumulated mass error is below4e-13. Shift-charge
errors for a continuation are segment-relative; add the reported previous
error bound (total upper bounds approximately3.11e-11 and2.73e-10).

Both partial infall cases still have law error17.3676%, one material boundary,
density rebound1.0, and exterior T fractions below1.6e-11 at these early
times. Neither has repaired the galaxy law. No joint formation success is
claimed. The all-F seeded run only reaches18.25Myr, converts about.00114Mb,
and has seven crossings and law error473.69%; its energy accuracy is too weak
relative to its tiny far flux for a strong cooling claim.

The original g2=0 control reproduces NT's nonlinear infall. The new channel
has direct compression work and outward scalar flux in the discretization,
but long-time and spatial convergence for g2>0 have NOT been established.
In particular the central fast coupled branch may be underresolved by the
2kpc scalar grid. Exact energy conservation cannot certify its spectrum.

## Why increasing the coupling is not the missing answer

LINEAR_RESPONSE.md derives both uniform coupled branches. Stronger g2 adds
positive induced inertia, slows the material mode, and creates a fast branch.
The nonrelativistic truncation has an upper low-wavenumber branch faster than
the bare scalar c. This is a completion issue, not a proof that every possible
relativistic completion is acausal. A complete temporal/spatial kinetic action
and its Noether mass have not been derived. At eta=1, local mixing reaches
about32384 centrally (about1096 at1.49kpc); these are not small corrections.

mode_rate.py applies the slow-source calculation to an actual benchmark
compression tangent, rather than assuming a prescribed full-release pump.
Both species are transported; the carrier relaxes in the exact static
Hessian. K=13.38461, I=72.32180, actual induced-inertia ratio1.00543.
The uncoupled period is816.97Myr, coupled period1156.94Myr, and compactness
Omega*200kpc/c=.00354. For this coherent mode,

    P/E=[eta/(1+eta)^2](M_source²/D_source)Omega0²/c,

which is maximized at eta=1. The grid-specific minimum energy damping time
is3.156e6Myr, approximately3156Gyr. The calculation is not a continuum-certified
bound on the full nonlinear PDE. Nonradial, incoherent and short-scale modes
are outside it. It does show that merely naming a compression outlet does
not make the actual slow radial mode cool efficiently.

## Exact missing pieces

1. An actual nonlinear energy cascade from slow infall into faster escaping
   modes, with backreaction and resolved spectrum. Positive work into a
   near field or additional inertia is not this cascade.
2. A physical origin and coefficient for any new compression operator,
   together with consistent kinetic completion where its mixing is large.
3. A converged free initial-value solution that forms the law while its
   interface remains restoring, transition remains filled and outer phase
   remains free. Static existence and local preservation do not establish it.

The unconverted F reservoir was independently checked as an existing outlet
in NT's run_reservoir_flux. Its apparent positive raw energy flux is inward
bound-mass advection, not demonstrated positive outgoing excitation cooling
in the tested30Myr window. Do not claim this outlet was omitted from the
energy budget and therefore supplies the needed missing power.
