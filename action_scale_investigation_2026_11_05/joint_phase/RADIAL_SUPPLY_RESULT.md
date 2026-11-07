# Radial redistribution of the mediator source

2026-11-06. Base ce5bb4fcd4f019e48c2938a804792d8593d07d15;
frozen contract f647cbb72c. Continues SELF_COOL_SUPPLY_RESULT.md.

**New result:** radial transport removes the previous no-flow source-profile
obstruction at the level of particle conservation. An explicit inward flow
redistributes particles from the mediator source toward stronger inner losses.
However, its energy budget requires heat transport, and strong elastic opacity
reduces conductive efficiency. Neither a full finite halo nor its stability or
the coefficient1/2 is established. The no-flow failure in the previous report
must not be interpreted as a failure of every flowing configuration.

Natural units c=kB=hbar=1; theta denotes temperature in energy units. The
calculations below distinguish exact number/kinematic identities from a leading
subsonic isothermal energy approximation.

## 1. Continuity with the actual source

The earlier ballistic mediator gives

    J(r)=j exp(-r/l)/r^2,    j=dotN_S/(2 pi l).

Test a material tail n=A/r^2, annihilation coefficient K, radial mean velocity
u positive outward. Steady particle conservation is

    (r^2 n u)'/r^2=J-Kn^2.

It integrates exactly to

    u(r)=U-(jl/A)exp(-r/l)+KA/r.

U is a boundary integration constant, not a velocity selected by dark energy.
For a shell r0<r<R, integration also gives

    A[u(R)-u(r0)]
      =jl[exp(-r0/l)-exp(-R/l)]-KA^2(1/r0-1/R).

The source-profile mismatch therefore need not prevent a trial inverse-square
number profile: flow can carry the difference. Number balance alone says
nothing about hydrostatic support, temperature, or stability.

### Explicit long-decay example

For a finite shell with l much greater than R, approximate J=j/r^2. If both
matching surfaces have zero mean particle flux, the required amplitude is

    j=KA^2/(r0 R),
    u(r)=KA (r-r0)(r-R)/(r r0 R).

The velocity is negative throughout r0<r<R. This exact solution of the
long-decay continuity approximation supplies inner annihilation by inward
redistribution; it need not create a wind. Its magnitude must still be much
smaller than the thermal speed for the subsequent subsonic approximation.

These zero-flux surfaces are an illustrative matching choice, not the
previous evaporating exobase. A real evaporating surface instead sets a
positive number flux there and changes U and the integrated balance. Neither
boundary condition is selected here.

The long-decay calculation holds the local amplitude j fixed. Taking l to
infinity at fixed dotN_S would instead make j vanish; the finite-l model, not
an infinite-l source of finite luminosity, is physical. In fact the fraction
of parent decays in the shell is

    f_shell=exp(-r0/l)-exp(-R/l) approximately (R-r0)/l.

Even perfect retention deposits only f_shell of the parent energy there.
Thus a long decay length also increases the parent luminosity required to
supply a fixed local rate. Capture inefficiency increases it further.

## 2. Momentum and energy must include the arriving particles

Let u_in be the mean radial injection velocity in the nonrelativistic
momentum moment and e_in the mean lab-frame injected kinetic energy. With
q=J/n, the steady momentum equation is

    u u'=-(n theta)'/(mn)-Phi'+q(u_in-u).

The injected energy measured relative to the local bulk velocity is

    e_rel=e_in-m u u_in+(m/2)u^2.

The internal-energy equation, with conductive energy flux F positive outward,
is

    n c_v u theta'+n theta (u'+2u/r)
       =J(e_rel-c_v theta)-(r^2 F)'/r^2,    c_v=3/2.

Constant-K annihilation removes the mean particle energy, so it cancels from
the direct temperature equation when continuity is used. It remains in
continuity, compression and the total-energy budget. The source momentum term
is essential: its bulk-work contribution combined with e_rel restores the
lab injection power J e_in. Deleting it while retaining e_rel produces an
unphysical residual J m u(u-u_in), which the negative control detects.

The ballistic parent has outward momentum. Its retained daughter population
cannot automatically be assigned u_in=0. In the simple nonrelativistic,
fully retained two-daughter limit, m u_in equals half the parent's radial
momentum. If source momentum or retention is important, it must be included.
The approximate hydrostatic calculation below requires

    |u u'| << v_h^2/r,     |q(u_in-u)| << v_h^2/r,
    |m u u_in|, m u^2 << theta or the relevant injection energy scale.

No calculation here proves these inequalities for a galaxy.

## 3. The heat flux required by an approximately flat tail

Neglect the preceding small bulk terms to leading order. Halo-dominated
isothermal support gives theta=theta0 and

    v_h^2=4 pi G m A,    theta0=m v_h^2/2.

For an ideal shell, this also requires the inner gravitating mass to match
the flat-force continuation, or that the central correction be negligible
in the interval. The actual core and baryonic force are not solved.

The thermal equation then demands a conductive-flux divergence

    Q_cond=(r^2 F)'/r^2
          =J(e_in-c_p theta0)+K n^2 theta0-2n theta0 u/r,
    c_p=c_v+1=5/2.

Positive Q_cond removes heat from the local material; negative Q_cond means
conductive heat converges and heats it. It is a derived required flux, not a
new adjustable cooling function. For L_cond=4 pi r^2 F,

    L_cond(r)-L_cond(r0)=4 pi [P(r)-P(r0)],
    P(r)=-jl(e_in-c_p theta0)exp(-r/l)
         +2jl theta0 Ei(-r/l)-2A theta0 U ln(r)
         +KA^2 theta0/r.

Only log differences occur physically, equivalently ln(r/r0); Ei is the
exponential integral. Differentiation verifies this expression against the
sourced thermal equation.

An EXACTLY isothermal region with ordinary finite conductivity has F=0.
Therefore the preceding expression is a diagnostic for a nearly isothermal
profile requiring small but nonzero temperature gradients, not an exact
isothermal conductive solution. Density and momentum must also acquire
consistent corrections. Specifying the required flux does not solve them.

### Energy test for the explicit inward-flow shell

For the long-decay, zero-particle-flux example of section1, write D=1/r0-1/R.
The net required outward conductive power is

    [L_cond(R)-L_cond(r0)]/(4 pi)
       =KA^2 {D[e_in-(11/2)theta0]
               +2theta0(1/r0+1/R)ln(R/r0)}.

If both surfaces were thermally insulated, the injection energy would have
to obey

    e_in/theta0=11/2-2(R+r0)/(R-r0) ln(R/r0).

For a thin shell the right side tends to3/2, agreeing with the local
injection/annihilation balance. For R/r0=10 it is negative:
11/2-(22/9)ln10<0. A nonnegative kinetic injection energy therefore cannot
sustain this wider isothermal shell without net heat export. This is an
explicit energy obstruction to the insulated version of the model, not to a
conductively cooled shell. Compression associated with inward transport
releases heat even when injection is cold. A zero mean number flux at the
surfaces does not imply zero conductive energy flux.

## 4. Self-scattering helps stopping but can hinder conduction

In a dilute gas with a mean free path much shorter than the temperature scale,
kinetic transport gives the scaling

    F=-kappa_theta theta',
    kappa_theta=C_k sqrt(theta/m)/sigma_self.

C_k is a positive dimensionless collision-operator coefficient not calculated
here. This is a scaling estimate, not an exact conductivity or a substitute
for the relativistic stopping calculation. Increasing sigma_self reduces
the mean free path and thus heat conduction in this short-path regime.

At a radius r, let v_th=sqrt(theta0/m) and local opacity over scale r be

    tau_self=n sigma_self r=A sigma_self/r.

The fractional temperature gradient required by L_cond is then

    epsilon_T=|r theta'/theta0|
       =|L_cond| sigma_self/(4 pi C_k r theta0 v_th)
       =|L_cond| tau_self/(4 pi C_k A theta0 v_th).

A collisional nearly isothermal window requires both tau_self much greater
than one and epsilon_T much smaller than one. In particular it requires

    |L_cond| << 4 pi C_k A theta0 v_th,
    r/A << sigma_self << 4 pi C_k r theta0 v_th/|L_cond|.

These are necessary approximate compatibility conditions, not sufficient
stability criteria. If the required flux is too large, arbitrarily increasing
self-scattering does not repair the problem. In the long-path regime this
conductivity law fails and a kinetic, flux-limited treatment is needed.

At an evaporative boundary, a real transport solution must match the number
and energy fluxes of the escaping distribution. Bulk enthalpy, random heat
flux and gravitational work must not be counted twice. The previous local
Maxwell-reservoir cooling formula does not automatically furnish that boundary
condition for this flowing spatial halo. The two examples have not been
silently combined into a purported global solution.

## 5. What changed, and what remains unselected

The prior no-flow profile obstruction is bypassed by an explicit radial
number-flow solution. The resulting heat requirement is now known for the
trial tail, including a constructive long-decay example and its insulation
failure. A possible conductive window is stated, but no self-consistent
corrected temperature/density profile or radial stability spectrum is solved.

For zero particle flux at both matching radii, the exact finite-l number
budget selects only

    A^2=jl[exp(-r0/l)-exp(-R/l)]/[K(1/r0-1/R)].

Thus v_h^4=16 pi^2 G^2 m^2 A^2 still depends on j,l,K and both radii. The
source's relation to baryonic mass, retained spectrum, actual core and outer
boundary remain inputs. Neither conductivity nor the boundary budget relates
that combination to rho_DE, and neither produces the desired1/2. A flat-tail
ansatz was tested, not derived as an attractor.

Next unresolved implication: solve the coupled source, momentum, energy,
conductivity and Poisson boundary problem with a physically supplied source
and escape boundary, then test radial perturbations. Source data and the
conductive coefficient can be treated as explicit model parameters for such
a conditional study, but adjusting them to force the target normalization
would not derive it. This route remains open; the broader goal is incomplete.

## Evidence and review

radial_supply.py passes12 exact checks: sourced continuity, injection energy
reconstruction, heat divergence and primitive, finite number budget, explicit
long-decay flow and matching conditions, shell energy integral and thin-shell
limit, and the conduction-opacity identity. Omitting source momentum fails
exactly the injection-energy check(11/12). Hash-recorded runs are preserved
under evidence/radial_supply and evidence/radial_supply_mutate. The integration
and algebra checks do not validate the physical closures by themselves.

Self-audit verdict: **conditional on named inputs**. Exact identities passed;
subsonic support, contact-dominated conductivity, retained source moments,
inner mass matching and escape-boundary physics remain obligations. The
zero-particle-flux example is explicitly separated from the evaporating
boundary. Dimensional review uses natural units and logarithm differences;
no executed inputs were changed after recording. This is author self-review,
not independent verification or a complete halo simulation.
