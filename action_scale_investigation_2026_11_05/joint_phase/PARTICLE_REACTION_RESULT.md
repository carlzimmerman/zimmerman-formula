# Particle reactions, energy supply, and the proposed halo feedback

## Result

A concrete decay/annihilation interaction supplies particles and energy and can
erase local abundance and kinetic-temperature memory. Its rates do NOT yield
the global feedback assumed in COUPLED_FEEDBACK_RESULT.md. Its simple reaction-
balanced density is approximately 1/r, is not hydrostatically supported by its
selected constant temperature, and does not give an extended flat rotation curve.
A conditional peak-speed fourth-power scaling survives, but is not a physical
halo solution. The target coefficient1/2 remains unselected.

This is an illustrative particle theory being tested, not a discovered actual
interaction in nature. It extends, rather than follows uniquely from, the
previous scalar model. Base65954af232; inputs frozen in1188fb699f and57eb3cf214.
No target coefficient or observational fit was used.

## 1. Explicit interaction and rates

Use natural units for this section. Introduce a real Z2-odd stable scalar chi
of mass m, a mediator S of mass M>2m, and light scalar radiation a. In addition
to canonical kinetic/mass terms, take

    L_int = -g S chi^2/2 -lambda chi^2 a^2/4 -y S Nbar N.

N denotes a baryonic fermion in an effective description. Positive quartic
terms can stabilize the large-field potential; their elastic effects must be
included if important. Vacuum stability, radiative corrections and experimental
constraints are not established here. The portal permits emission from baryonic
processes, such as bremsstrahlung, but does not compute a stellar luminosity
or prove a universal luminosity per unit baryonic mass.

The two-body integrated phase space is beta/(8pi). Including identical-final-
particle symmetry factors gives, at tree level,

    Gamma(S->chi chi) = g^2/(32 pi M) sqrt(1-4m^2/M^2),
    K = <sigma_ann v_rel> = lambda^2/(64 pi m^2)

for nonrelativistic chi annihilation to effectively massless a, at leading
constant s-wave order. The decay uses the factor1/(2M), the annihilation uses
1/(4m^2), and each has a final-state factor1/2!. The pair-annihilation event
rate is K n^2/2; two chi disappear per event, giving particle loss K n^2.
These factors are derived rate normalizations, not a MOND coefficient.

Inverse reactions are neglected only when the escaping a bath is dilute and
occupation factors are negligible. If trapped, radiation supplies inverse
reactions and pressure, changing the kinetics. The displayed luminosity and
mean energy are boundary data, not predictions from the portal coupling y.

## 2. Production profile and energy source

Let stars supply a steady central mediator number luminosity dotN_S with mean
energy E_S and approximately fixed outward speed v_S. Write Gamma_lab for its
lab-frame decay rate, l=v_S/Gamma_lab, and L_S=dotN_S E_S. Outside the emission
region, ballistic transport gives

    n_S(r)=dotN_S exp(-r/l)/(4 pi r^2 v_S),
    J_chi(r)=2 Gamma_lab n_S
            =dotN_S exp(-r/l)/(2 pi l r^2).

The rest mass and kinetic energy of the daughters come from S. Their mean
injected energy per chi is E_in=E_S/2. The total deposition satisfies

    integral_0^infinity 4 pi r^2 J_chi E_in dr = L_S.

Thus there is an explicit energy budget, not an unspecified energy supply from
vacuum. A finite source radius changes the lower boundary, but not this
energy accounting. A nontrivial branching ratio reduces the deposited fraction.
The power must ultimately be paid for by the stellar/baryonic source. No claim
is made that real stars can supply the required amount for arbitrary g,y,M.

Cold production and retention are extra requirements. For S at rest, daughter
speed is beta_chi=sqrt(1-4m^2/M^2). Keeping daughters below a small escape speed
v_esc requires beta_chi less than v_esc/c, unless collisions cool them first.
That means a near-threshold mass ratio, with (M-2m)/(2m) approximately less than
v_esc^2/(2c^2). Mediator boosts usually worsen the retention problem. Neither
near-threshold masses nor rapid cooling is selected by this Lagrangian.

## 3. Local feedback derived with the correct energy moment

At fixed volume, neglect transport and self-gravity temporarily. With constant
leading-order K, particle number obeys

    n_dot=J-K n^2.

Define kinetic temperature by mean kinetic energy c_v T, with c_v=3kB/2 in
three nonrelativistic isotropic dimensions. Let e_in=E_in-mc^2. The total
material energy density is u=n(mc^2+c_v T). Escaping annihilation radiation
removes the annihilated particles' mean rest and kinetic energy. At this order,

    u_dot=(mc^2+e_in)J -(mc^2+c_v T)K n^2,
    c_v n T_dot=J(e_in-c_v T).

The term -c_v T J follows from differentiating nT; omitting it violates energy
accounting. No extra cooling law was inserted to obtain the local result.
The moment closure assumes annihilation samples mean kinetic energy at constant
K. Velocity-dependent rates require a distribution-level calculation. Elastic
collisions may isotropize/thermalize, but a sufficient rate was not derived.

For J,K>0 this has the unique positive steady state

    n*=sqrt(J/K),  T*=e_in/c_v.

The Jacobian eigenvalues are -2sqrt(JK) and -sqrt(JK). More strongly, positive
n converges monotonically to n*, and T-T* obeys

    d(T-T*)/dt=-(J/n)(T-T*),

so both initial conditions are forgotten for a persistent source. Four finite
trajectories verify this behavior in fixed dimensionless units. This is a
local reaction attractor with external energy supply, not the earlier global
halo-amplitude feedback X_dot=gamma(Theta-X). In particular the abundance source
here is fixed by the mediator distribution, not by the pool's gravitational
support or its own temperature.

## 4. The spatial and mechanical checks

Balancing the actual source against two-body annihilation gives

    n(r)=C exp[-r/(2l)]/r,
    C=sqrt(dotN_S/(2 pi l K)).

For r much less than l this is 1/r, not1/r^2. Counting its nonrelativistic rest
mass as a diagnostic gives

    Mp(r)=16 pi m C l^2 [1-(1+r/(2l))exp(-r/(2l))],
    v_c^2(r)=8 pi G m C l f(x),
    x=r/(2l),  f(x)=[1-(1+x)exp(-x)]/x.

These formulas idealize the central source as pointlike; a real stellar core
regularizes the center. At small x, f=x/2+O(x^2), hence v_c^2 grows as r.
At large x, f approaches1/x and the curve becomes Keplerian. Its nonzero
maximum solves exp(x)=1+x+x^2. The computed root is x=1.79328213290078,
with f=0.298425607525639. No peak radius was inserted into the root finder.
A maximum or a limited nearly horizontal portion is not an extended flat tail.

There is a still stronger consistency issue. The selected T* is independent
of r for fixed injected spectrum. Isothermal pressure would require inward
acceleration

    g_required=(kB T*/m)[1/r+1/(2l)],

whereas this profile supplies g_actual=G Mp(r)/r^2. Near the ideal inner region,
g_actual tends a constant while g_required grows as1/r; far outside,
g_actual decays as1/r^2 while g_required tends a constant. No single T*
makes this profile globally hydrostatic. Central baryons do not repair these
opposite asymptotic forms. A flowing solution or different transport/reaction
balance might exist, but has not been calculated. The displayed circular
speeds are therefore the gravity of a diagnostic density profile, not a
self-consistent galaxy prediction.

### A mass-power coincidence must not be mistaken for success

For fixed particle parameters and mediator spectrum, C proportional to sqrt(L_S).
At fixed x, including the peak,

    v_peak^4=32 pi G^2 m^2 l dotN_S f_peak^2/K.

Consequently if one assumes L_S=ell_S Mb, then v_peak^4 proportional to Mb.
This conditional fourth-power *peak* scaling is retained, despite the wrong
profile and mechanical balance. Its inferred normalization would be

    a_peak=32 pi G m^2 l ell_S f_peak^2/(K E_S).

It depends on g through l, on lambda through K, on mediator energy, particle
masses, and stellar emissivity. Neither the peak factor nor any symmetry factor
fixes its ratio to c sqrt(G rho_DE). The profile is not a valid substitute for
the desired flat-curve result.

## 5. Could a different elementary loss or transport repair it immediately?

A linear particle loss instead of pair annihilation would give n proportional
to J, hence a1/r^2 region, but its amplitude would scale as L_S. With fixed
parameters this yields v_flat^4 proportional to L_S^2, not the required linear
baryonic relation. Moreover a stable Z2-odd chi does not have that elementary
decay in the current action; changing its stability is new physics.

A steady outward particle wind can also have rho=dotM/(4pi r^2 u), but it is a
flow, not a stationary bound pool. With fixed injection energy and speed,
dotM proportional to L_S again gives v^4 proportional to L_S^2. Allowing speed,
capture and energy partition to vary with gravity requires an actual transport
solution, rather than assigning whatever dependence restores the target.
These are discriminating scaling checks, not universal exclusions of transport.

## 6. Vacuum pressure and the remaining normalization freedom

A constant V0 can be added to this local particle Lagrangian without changing
the tree-level decay rate, annihilation coefficient or source energy budget at
fixed geometry. It changes the cosmological vacuum energy. The local reaction
network therefore contains no identity relating those rates to rho_DE.
Loop corrections require renormalized vacuum and coupling parameters; they
cannot be declared a selector without computing the effective theory and its
renormalization conditions. No such quantum-vacuum calculation is claimed.

A two-phase pressure boundary remains a separate input. Particles being created
and annihilated does not itself set that boundary's phase-energy difference.
Thus this reaction supplies real local feedback and explicit energy transfer,
but fails to derive the previously postulated global feedback, a supported
flat halo or the coefficient1/2.

## Evidence and disposition

particle_reaction.py passes25 checks: tree phase-space factors, mediator
continuity, integrated energy supply, moment conservation, local stability,
profile gravity and four positive trajectories. The kinetic-dilution mutation
fails energy conservation and thermal equilibrium as intended. Both evidence
manifests are validated. This is self-review and finite computation, not an
independent audit or empirical validation.

A primary-source search identified work such as
[Dark matter from mediator decay in early matter domination](https://doi.org/10.1103/PhysRevD.110.023511).
Its abstract was checked only for the broad mediator-decay precedent; its
cosmological setting is different and it does not validate this stellar-halo
construction. All rate and energy claims used here are explicitly derived above.

The current elementary source/annihilation model is closed as a realization of
the requested global feedback under the stated ballistic/local-balance assumptions.
A source/transport/capture theory remains open, requiring stellar emissivity,
phase state, particle distribution and collisional rates. Those inputs cannot
be reconstructed uniquely from the river analogy or from a desired attractor.
More parameter fitting in the present model would not derive the missing
coefficient. No impossibility claim for all microscopic pool models is made.
