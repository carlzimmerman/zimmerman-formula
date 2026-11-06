# Physical replenishment routes and their power

## Outcome

Three physical supply routes were examined rather than inserting an arbitrary
reservoir source. Constant vacuum cannot supply advective power. Ordinary
material accretion supplies power but retains environmental parameters and,
in the simplest derived model, the wrong mass scaling. An expanding phase
front accesses fresh ambient vacuum, but its intercepted radiation has the
wrong spatial heating profile and is insufficient in the simple phase-pressure
halo closure tested here. A tempting cosmological sweeping prescription gives
linear mass scaling only after imposing an unselected speed and capture rule.

No source with the required universal power, whole-halo stability, or1/2 has
been derived. These are scoped results, not a universal prohibition on externally
powered or more complicated halos. Base209e0af365; contract40193fd0a9.

## 1. Inflow of a true cosmological vacuum carries no replenishing flux

For a perfect fluid of rest-frame energy density rho_E and pressure p, moving
radially at speed v in a local inertial frame, the advected energy flux is

    F_E=(rho_E+p) gamma^2 v.

This follows from T^{mu nu}=(rho_E+p)u^mu u^nu/c^2+p g^{mu nu}.
For p=-rho_E, the enthalpy density vanishes and F_E=0. Changing the notional
velocity of a pure vacuum does not turn it into a stream of fuel. Using only
rho_E v would falsely predict energy transport by a Lorentz-invariant vacuum.

A dynamic medium with p different from-rho_E, gradients, defects, radiation or
particles may carry flux. It requires its own stress tensor, state, velocity
and interaction. Its supply is not specified by cosmological rho_DE alone.
Phase conversion is different from advection and is considered below.

## 2. Ordinary accretion: an actual supply with environmental normalization

For a nonrelativistic isothermal gas with sound speed c_s, density rho_infty,
steady spherical inflow, negligible gas self-gravity, zero rotation and a central
point mass M, continuity and Euler's equation give the transonic critical point

    r_s=G M/(2c_s^2),  |u_s|=c_s.

The isothermal Bernoulli relation referenced to rest at infinity is

    u^2/2+c_s^2 ln(rho/rho_infty)-GM/r=0.

At the sonic point it yields rho_s=rho_infty exp(3/2), hence

    dotM=4 pi r_s^2 rho_s c_s
        =pi exp(3/2) G^2 M^2 rho_infty/c_s^3.

This derives a physical rate rather than assigning one from the target.
A luminosity L=eta_acc dotM c^2 then still needs an energy-release mechanism
and its efficiency. For ordinary galaxy-scale gravitational energy release,
the specific available energy is of order GM/R, not an automatically available
rest-mass conversion. The isothermal assumption itself requires heat transport.

At fixed environment and efficiency, L is proportional to M^2. Even granting
M=Mb and the earlier conditional v_flat^4=2G zeta L/c, the result is proportional
to Mb^2 rather than Mb. Letting the external sound speed, density, efficiency
or central mass vary can change the exponent, but requires a derived relation.
M is fundamentally the accretor's gravitating mass, not necessarily baryonic
mass or a black-hole mass with a known universal relation to it.

This gas calculation cannot be applied to p=-rho_E vacuum by replacing its
mass density with rho_DE. The equations of state and fluxes are different.
Accretion can sustain a driven system in principle, but its supply does not
follow from dark-energy density. No galaxy-specific accretion or stability
solution is claimed here.

## 3. A conversion front can harvest fresh ambient phase

Consider a spherical front at R_f>R_h surrounding a halo of radius R_h. It
converts an external higher-energy phase to a lower-energy phase, releasing
energy density DeltaV while moving outward at speed w<=c. Its latent power is

    L_front=4 pi R_f^2 w DeltaV.

Let eta_rad<=1 be the fraction radiated. As a specific transfer model, assume
isotropic emission in the lab frame and free propagation. A surface element
sees the halo in a cone with sin(theta)=R_h/R_f. The intercepted fraction is

    f_hit=[1-sqrt(1-y^2)]/2,  y=R_h/R_f,

so, in the quasisteady geometric approximation,

    L_hit=eta_rad L_front f_hit
         =2 pi eta_rad R_h^2 w DeltaV/[1+sqrt(1-y^2)].

It approaches pi eta_rad R_h^2 w DeltaV for a distant front and is at most
2 pi eta_rad R_h^2 w DeltaV in this geometry. Thus the increasing converted
area does not deliver unlimited power to the finite halo: interception falls
with distance. A constant-speed distant front can, in principle, provide
approximately constant intercepted power while consuming new ambient volume.
This genuinely evades the *closed finite reservoir* assumption, but it is an
evolving external source with its own phase history and environment.

Retardation, radiation efficiency, wall energetics and relativistic beaming
must be included in a real model. The displayed calculation uses isotropic
lab emission as specified, not an invariant claim about all moving walls.
It is an optimistic quasisteady transfer budget, not a full radiation solution.

### The illumination profile is different

Integrating the shell's radiation at an interior radius R_h gives

    U_a(R_h)=eta_rad DeltaV (w/c) atanh(y)/y.

For R_f much greater than R_h, U_a approaches eta_rad DeltaV w/c and is nearly
uniform across the halo. That is not the central1/r^2 radiation flux assumed
in TRANSPORT_CAPTURE_RESULT.md. For a material density n proportional to r^-2,
heating from this approximately uniform bath scales as r^-2, whereas the
previous slow-flow flat tail needed r^-4 heating. Direct shell illumination
therefore cannot simply be substituted for its L_a without re-solving transport.
The ideal zero-thickness shell formula grows logarithmically as the evaluation
point approaches the front; finite thickness, absorption and boundary dynamics
then matter. No infinite radiation density is claimed from that limit.

### Even a generous power test fails the simple phase-pressure closure

For an optimistic comparison, grant that ALL intercepted power could be
redistributed to reproduce the preceding central-heating geometry with no
loss. This redistribution is not derived. Retain its conditional equations

    v_h^4=2G zeta L_a/c,
    v_h^4=8 pi G Pext R_h^2.

They require the dimensionless power ratio

    Q=[2G zeta L_hit/c]/[8 pi G Pext R_h^2]
      =zeta eta_rad (w/c)(DeltaV/Pext)
        /{2[1+sqrt(1-y^2)]}

at least1. For the simple identification Pext=DeltaV, with the earlier
microscopic zeta<=1/2, eta_rad<=1 and w<=c, Q<=1/4. It is smaller for a distant
front. Hence that simple closure lacks sufficient intercepted power even
under the lossless-redistribution grant.

The pressure identification is a tested hypothesis, not a general law. One
possible configuration has a higher-energy material-filled central phase,
a lower-energy surrounding shell, and an outward front consuming the external
higher-energy phase. If a positive wall tension is added at the inner halo
boundary without other stress terms, Pext is at least DeltaV and the bound
strengthens. If the inner phase splitting differs from the outer front's,
if matter coupling changes pressure, or if Pext is much smaller than DeltaV,
this particular bound need not apply. Such changes introduce new physical
relations to derive. Strongly directed radiation or trapping also changes the
transfer problem and is not excluded by this scoped test.

### Cooling-bath budget in the correct external geometry

The previous boundary cooling mechanism needs U_a>rho_pool c^2/16. In the
far-front limit above, and using the conditional flat-tail density and
Pext=DeltaV relation, one finds

    U_a/(rho_pool c^2/16)
       =8 eta_rad (w/c)(v_h^2/c^2).

For a cold nonrelativistic halo this is much less than1. Thus the distant-front
bath cannot provide the required cooling energy density in this same closure.
This compares radiation ENERGY DENSITY in the shell geometry, not the central
source's luminosity-flux relation. It is distinct from the preceding generous
heating-power comparison. A different pressure ratio or optically thick
transfer could change it, but must be calculated explicitly.

## 4. Why cosmological sweeping can look promising without selecting power

Let H_Lambda^2=8 pi G rho_DE/3, and choose a turnaround-scale radius

    R_t^3=G M_grav/H_Lambda^2.

If a front is ASSUMED to sweep fresh phase at w=epsilon H_Lambda R_t, its total
latent power, before interception, would be

    L_sweep=4 pi R_t^2 w DeltaV
           =4 pi epsilon G M_grav DeltaV/H_Lambda.

If one additionally identifies DeltaV=rho_DE c^2, this becomes

    L_sweep/M_grav=(3epsilon/2)c^2 H_Lambda.

It has the tempting linear mass and cosmological-scale dimensions. But epsilon
is not selected by turnaround or nucleation, the phase splitting identification
is unproved, M_grav is not automatically Mb, and the halo does not intercept
all the luminosity of a distant front. A true cosmological vacuum's apparent
Hubble motion is not an inward energy flux; treating it as fluid accretion
would additionally omit the zero-enthalpy factor.

Even granting complete interception and M_grav=Mb for diagnosis, the inferred
normalization would be

    kappa=3 zeta epsilon H_Lambda/sqrt(G rho_DE)
          =sqrt(24 pi) zeta epsilon.

Neither epsilon nor the particle spectrum that sets zeta is fixed. Choosing
them to make this1/2 would put the answer in by hand. With general phase
splitting and mass ratio there are further multiplicative inputs. This is a
conditional dimensional match, not a derived luminosity law.

## 5. Whole-halo stability and interpretation

A source capable of supplying energy does not automatically stabilize capture,
material abundance, radiation pressure, a phase boundary and stellar orbits.
The preceding local thermal fixed point and global two-variable toy attractor
are not full hydrodynamic stability results. Here the pure-vacuum inflow has
zero power, the concrete accretion rate retains environmental scaling, and
the simple phase-front pressure model fails its power/geometry tests. There
is therefore no newly established complete halo on which to claim stability.

An external material flow or different phase geometry could still sustain a
halo in principle. To select its power it would need a specified equation of
state, boundary supply, emission/capture efficiency and transport, all coupled
to the finite halo. None of those inputs follows uniquely from the pool analogy.
The barrier controls how conversion proceeds, but does not supply a universal
source flux or impose the MOND normalization.

## Evidence and review

replenishment_geometry_checked.py passes16 exact checks, and the deliberate
replacement of enthalpy by energy density fails the vacuum-zero-flux check.
The first implementation, replenishment.py, passes14 algebra checks but included
a comparison with the PREVIOUS CENTRAL-SOURCE luminosity cooling bound. During
interpretation review that comparison was found inapplicable to a directly
illuminating external shell. It is preserved but superseded for cooling by the
explicit shell-energy-density derivation and revised checks. Algebraic success
alone did not validate that geometric interpretation. All evidence and inputs
are retained and manifests validated.

This is self-review of conditional calculations, not an independent audit or
a simulation of a stable galaxy. Primary-source context for the derived gas
rate is [Bondi accretion in early-type galaxies](https://academic.oup.com/mnras/article/460/2/1188/2608946),
which also discusses modifications due to galaxy potentials and radiation.
Its existence does not justify treating vacuum as ordinary accreting gas;
the rate used here was derived from the explicitly stated equations.

Disposition: no tested replenishment route selects the required power and
stable halo. The surrounding-phase front is a genuine open-system mechanism,
but the simple isotropic/free-streaming phase-pressure realization fails.
Environmental accretion, other stresses, trapping or a different equation of
state remain possible changed models, with their unselected inputs recorded.
No universal impossibility statement or successful1/2 derivation is claimed.
