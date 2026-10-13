# Finite reaction capacity and conditional halo contraction

Status: analytical constraints on a stationary endpoint of the same isolated
NR kinetic model, with numerical checks of the initial Plummer integrals.
No endpoint existence, stability or finite-time evolution is established.
This calculation answers what energy conservation permits; it does not
assert that reactions achieve the permitted conversion fraction.

## Conserved energy includes the reaction gap

Let M_h=m Q be the conserved leading inertial/gravitating mass, and let
F=2 N_chi/Q be the fraction of charge in sources. Thus 0<=F<=1. At the
retained nonrelativistic order, the rest energy above m Q is

    U_gap=DeltaE N_chi=(M_h v_*^2/2) F,   v_*=u c.

The same truncation used in INITIAL_HALO_RESPONSE.md retains this energy
while assigning the source inertial mass 2m. Relativistic corrections,
contact energy, coherent gradients, baryons, external tides, expansion,
and escape are excluded here. Total energy above the common rest energy is

    E=K+W+U_gap.

K is total kinetic energy, including both species and any bulk motions;
W=(1/2) integral rho Phi d^3x is gravitational potential energy. The
reaction contribution obeys K_dot|coll=-U_gap_dot. It transfers energy
internally and cannot provide an unlimited cumulative cooling sink.
Repeated forward/backward reactions do not increase the net storage
beyond M_h v_*^2/2. This statement does not forbid redistribution of energy
between particles or radii.

## Conditional stationary endpoint

Initially the daughter-only Plummer equilibrium has U_gap=0, W_0=-2 K_0,
so E=-K_0. Suppose the system later reaches a stationary isolated state
with the same total mass, convergent kinetic and potential energies, and
vanishing virial surface term. The stationary momentum equation integrated
against position gives

    2 K_f+W_f=0.

This argument uses the stationary stress equation, not the second time
derivative of a finite global radius-squared moment. That distinction
matters because the initial Plummer model has a divergent global second
moment. Combining energy conservation with the stationary virial relation,

    K_f=K_0+U_gap,f,
    W_f=-2(K_0+U_gap,f).

Define the gravitational radius r_g=G M_h^2/|W|. For any such endpoint,

    r_g,f/r_g,0 = 1/(1+alpha F_f),
    K_f/K_0 = 1+alpha F_f,
    alpha = M_h v_*^2/(2 K_0).

These relations require neither a final Plummer shape nor an isotropic
final velocity distribution. They do require stationarity and the stated
energy/virial assumptions. They are necessary conditions, not a dynamical
closure or a chemical-equilibrium solution.

## Evaluation for the existing test halo

For the initial Plummer model,

    W_0=-3 pi G M_h^2/(32 b),
    K_0=3 pi G M_h^2/(64 b),
    G M_h/b=6 sigma_0^2.

With sigma_0=200 km/s and v_*=299.792458 km/s,

    K_0/M_h=3.534291735e10 m^2/s^2,
    alpha=1.271478483.

| Final source charge fraction | r_g,f/r_g,0 | K_f/K_0 | Mass-weighted RMS speed ratio |
|---|---:|---:|---:|
| 0 | 1.0000 | 1.0000 | 1.0000 |
| 0.25 | 0.7588 | 1.3179 | 1.1480 |
| 0.50 | 0.6113 | 1.6357 | 1.2790 |
| 0.75 | 0.5119 | 1.9536 | 1.3977 |
| 1 | 0.4402 | 2.2715 | 1.5071 |

Consequently r_g,f>=0.440241899 r_g,0 for any stationary endpoint in this
model. F=1 is a kinematic capacity limit, not a demonstrated attainable
chemical state: sources can decay, and detailed balance generally includes
both species. No final F is selected by this calculation. A homologous
Plummer endpoint would have the same ratio of scale radii, but homology
has not been derived and is not assumed in the gravitational-radius bound.

The increase in kinetic energy is consistent with the earlier initial
pressure loss. Binding energy released during contraction can exceed the
energy stored in the mass gap. The medium can remain nonrelativistic while
becoming dynamically hotter; continuing contraction is not synonymous
with ever lower velocity dispersion.

## What the bound does not constrain

The bound applies only to an assumed stationary endpoint. During transient
motion the virial relation need not hold. Energy conservation alone allows
large negative W balanced by large K, so the formula is not an all-time
radius bound and does not rule out overshoot.

Nor is r_g a central core radius. As a mathematical illustration, a Plummer
core of mass epsilon M_h and scale epsilon^2 b has a fixed self-energy
-3 pi G M_h^2/(32 b), while its radius tends to zero and central density
increases as epsilon^-5. This scaling shows why a total-energy bound cannot
by itself control local concentration. It is not a constructed stationary
solution of the reacting system or a physical prediction at arbitrarily
small scales; neglected stresses and relativistic effects can intervene.

Escape would change the bound system's mass and energy and require an
explicit outgoing flux. Contact stress or quantum gradients would add
terms to both energy and virial balance. Neither should be silently folded
into the current numerical bound.

## Verification and next unresolved step

virial_capacity.py independently integrates the Plummer gravitational
shell energy, Jeans kinetic energy and force virial. It checks the energy
and virial identities with exact rational substitutions and checks the
small-core scaling. All 39 checks pass; the run manifest validates input
and output provenance. The derivation and interpretation are self-reviewed.

The result strengthens the conservative contraction mechanism while
excluding an interpretation as unlimited energy removal. The unresolved
step is coupled finite-time source/daughter transport and gravity, including
reverse reactions, to determine whether a stationary endpoint is approached
and which conversion fraction it has. This does not derive the repo's
universal halo profile, baryonic scaling or vacuum-dependent acceleration
law, and does not complete the cold-energy construction.
