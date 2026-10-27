# Spherical two-state energy and its limits

Status: candidate Newtonian energy functional with a phenomenological reversible
conversion closure. Self-derived and self-reviewed. No claim of microscopic
origin, observational fit, relativistic stability or novelty.

## 1. Positive mass, two states, one gravitational source

Let rho_T,rho_F>=0 be equal-rest-mass states, with rho_c=rho_T+rho_F.
In an isolated spherical system define

    M_T(r) = integral_0^r 4 pi s^2 rho_T(s) ds,
    P_r(r) = M_T(r)/(4 pi r^2),
    u(r) = 4 pi G P_r(r) = G M_T(r)/r^2,  0<=u<a0.

There is no extra mass added for P. It is a representation of the T mass.
The finite isolated calculation uses zero background; it is not an embedding
in cosmological background density. The adopted energy is

    E = kinetic + U_grav[rho_b+rho_T+rho_F]
        + integral W_full(u) d^3x - epsilon M_T + E_receiver,
    W_full(u) = (a0^2/K)[-log(1-u/a0)-u/a0],   K=4 pi G.

U_grav contains the cold self-interaction once and baryon-cold interaction
once. Baryon self energy is irrelevant to the cold equations for a prescribed
baryon source. Epsilon has dimensions velocity squared, lowers the internal
energy of T, and is spatially constant in the tested selector.

This is an extension of the paper, rather than a consequence of its action.
Stiffness is omitted. In particular there is no claim of quantitative validity
for the inner regions of dwarfs, globulars or the Solar System.

If S is the mass converted T->F per volume per time, continuity requires

    partial_t rho_T + div j_T = -S,
    partial_t rho_F + div j_F = +S.

The original displacement-current identity cannot simply be kept unchanged:

    partial_t P_r = -j_T,r - r^-2 integral_0^r S(s) s^2 ds.

Its divergence gives the T equation. The radial integral is bookkeeping in
Newtonian spherical symmetry, not a relativistic causal transport law.

## 2. Forces and coexistence equilibrium

Displacing a positive, infinitesimal T shell outward decreases the tether
energy. Its outward specific restoring force is

    D_full(u) = K W_full'(u) = a0 u/(a0-u).

A T element therefore has radial acceleration

    a_T = -(g_b+g_F+u) + D_full(u)
        = -(g_b+g_F) + u^2/(a0-u),

while an F element has only gravitational acceleration

    a_F = -(g_b+g_F+u).

For cold static T, a_T=0. Write g=g_b+g_F+u. Then

    g_b+g_F = u^2/(a0-u) = g^2/(g+a0),
    g = [g_source + sqrt(g_source^2+4 a0 g_source)]/2,
    g_source = g_b+g_F.

Thus F gravity does not disappear from the law. It is incorrect to use
g=law(g_b)+g_F for this coexisting equilibrium. The static relation is
conditional on adequate positive T supply and the omitted stiffness being
negligible. It is not the force law of the all-F experiment below.

Let g0=law(g_b). Allow a positive acceleration residual delta dex. Monotonicity
of g^2/(g+a0) gives the exact allowed enclosed F-to-baryon ratio

    eta_max = [(10^delta g0)^2/(10^delta g0+a0)-g_b]/g_b.

In the deep limit eta_max tends to 10^(2 delta)-1; in the Newtonian limit it
tends to 10^delta-1. At delta=0.05 these are 0.2589 and 0.1220. These are
fractions of enclosed baryonic mass, not fractions of total dark mass.
The tolerance is illustrative, not a fit or confidence limit.

## 3. Conversion energy and a candidate rate law

Convert a small mass dm at radius r from T to F, preserving position and
velocity. Gravity is unchanged at the instant of conversion. The first-order
change in system energy is

    dE_system = [epsilon - mu_P(r)] dm,
    mu_P(r) = integral_r^infinity D_full(u(s)) ds.

The receiver must take (mu_P-epsilon)dm. An uphill conversion must instead
absorb energy. This is not a new source of energy. For a finite conversion use
the full difference of field energies; holding mu_P at its initial value
through a large conversion is wrong.

For all T->F at epsilon=0 the exact field energy U_full is exported. At a
nonzero epsilon, the exported amount is U_full-epsilon M_T. The receiver is
specified as an energy ledger only: no interaction that emits or absorbs
physical quanta has been derived. Momentum/recoil and relativistic rest-energy
corrections are not modeled. Spherical balanced export is an assumption.

For an explicit restricted kinetic closure, freeze the total radial profile
and set rho_T=q rho_c, rho_F=(1-q)rho_c. Then u=q u_initial. Define

    mu_bar(q) = (1/M_c) dU_full(q)/dq,
    Gamma_TF = Gamma0 sigmoid((mu_bar(q)-epsilon)/theta),
    Gamma_FT = Gamma0 sigmoid((epsilon-mu_bar(q))/theta),
    dq/dt = (1-q)Gamma_FT - q Gamma_TF.

Theta>0 is an assumed common bath specific energy, not the gas temperature.
Gamma0 is unspecified. Rates are nonnegative and conserve total rest mass.
They obey the chosen detailed-balance ratio. For epsilon=0 conversion is
energetically favored; without an internal binding offset the tethered phase
is not protected against releasing its field energy.

The stationary fraction satisfies

    epsilon = mu_bar(q) + theta log(q/(1-q)).

Since W_full''>0, mu_bar'(q)>0 on the admitted profiles. The right side is
strictly increasing from -infinity to +infinity for theta>0, so there is one
stationary fraction and the one-variable rate dynamics restores toward it.
This is stability of the frozen-profile chemical variable only. It says
nothing about spatial modes, orbits, gravity or a relativistic ghost.

Requiring q_dwarf<=0.1 and q_disk>=0.95 gives the necessary interval

    max_disks mu_bar_disk(0.95) + theta log(19)
       <= epsilon <= mu_bar_dwarf(0.1) - theta log(9).

The computed intercepts are about 49656 and 3.843 (km/s)^2. The lower bound
increases with nonnegative theta and the upper decreases. Thus there is no
common epsilon,theta in this *frozen-profile, common-bath* selector for those
declared targets. The numerical intercept comparison is overwhelmingly
separated, but is quadrature evidence, not an interval arithmetic certificate.
No claim is made about a model with different local baths, history-dependent
barriers, extra couplings, or a self-consistently changed density profile.

## 4. Imposed-conversion retention experiment

An initial finite T halo is sampled from the spherical simple-law profile of
a Plummer baryon source. Choose its outer radius so M_T=5.364 M_b,initial.
Truncation is a supplied boundary, not a predicted catchment law. At fixed
positions convert all T to F and reduce the baryon mass to 10%. The remaining
particles start at rest; the conversion time and population selection are
imposed. Baryon removal is external work: it raises the cold gravitational
energy by the change in the prescribed baryon potential. It must not be
counted as conservation of the isolated cold system across the impulse.

After the impulse the baryon potential is fixed and the simulated free system
is autonomous. Normalize G=M_cold=R_initial=1. Equal radial shells have the
pair kernel -m_i m_j/sqrt(max(r_i,r_j)^2+eps_soft^2) and half their own shell
self energy. The baryon potential is -M_b/sqrt(r^2+b^2). The exact acceleration
away from shell crossings is

    a_i = -(M_inside + m_i/2) r_i/(r_i^2+eps_soft^2)^(3/2)
          -M_b r_i/(r_i^2+b^2)^(3/2).

The implemented potential derivative is checked by independent finite
differences. Shell order is recomputed every step, allowing crossing. Radial
origin crossings reflect position and velocity. Leapfrog is used with fixed
eps_soft=0.02 and two N/timestep pairs. The force changes at shell crossings;
the measured energy error, not a claimed smooth-force error order, controls
interpretation. No zero-softening limit or 3D orbital stability is tested.

The initial law density is Newtonian/unsmoothed; it is not an exact static
solution of the softened pre-conversion model. These experiments test whether
a positive, cold, finite mass distribution can remain bound after conversion,
not whether a realistic halo naturally reaches that initial condition.

Binding is diagnosed from instantaneous kinetic plus removal potential
energy, including the outer-shell potential and half shell self energy.
A negative value is a snapshot diagnostic in a time-varying potential, not
a promise of eternal retention. No stellar velocities are evolved.

In this all-F branch the field is ordinary gravity, g=g_b+g_F. The profile
continuation compares that instantaneous acceleration with law(g_b,postloss).
Do not insert the coexistence amplification into this branch or treat its
transient force as an observed dispersion/lensing prediction.
