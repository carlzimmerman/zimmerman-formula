# Transport and capture of the candidate pool particles

## Result and scope

Including transport changes the previous local-reaction conclusion. A steady,
slowly moving annihilating fluid with central radiative heating admits a
self-consistent *leading outer balance* with n proportional to r^-2 and
asymptotically constant temperature. These powers follow from the continuity,
momentum and energy exponents, not from imposing local production=annihilation.
The existing contact interaction also relates heating to annihilation and
cancels one coupling from the formal speed normalization:

    v_flat^4 = 2 G zeta L_a/c.

This is conditional asymptotic progress, not a constructed finite captured halo.
Capture efficiency, fluid closure, inner supply, radiation spectrum, outer
pressure and stability are not established. Neither L_a/Mb nor its relation
to dark-energy density is selected. No MOND1/2 is derived.

Base b66bc87f22; contract TRANSPORT_CAPTURE_CONTRACT.md frozen at0a7ec50d29.
The same scalar interactions are used. Only this investigation is changed.

## 1. Gravitational capture requires energy transfer

In a time-independent weak potential, specific orbital energy
E_orb=v^2/2+Phi is conserved between collisions. A particle arriving with
positive energy cannot become bound merely because gravity bends its orbit.
It must be born bound, lose energy, or encounter an evolving potential.
Annihilation removes a particle; it does not cool that particle into a bound
orbit. Elastic self-scattering can redistribute energy and eject another
particle, but capture then depends on both particles' distribution functions.

The portal already tested, -g S chi^2/2-y S Nbar N, permits elastic chi-N
scattering. For mediator mass M large compared with momentum transfer and
nonrelativistic particles, the spin-averaged amplitude squared is

    |M_scatt|^2 approximately 4 g^2 y^2 m_N^2/M^4,
    sigma_chiN = g^2 y^2 m_N^2/[4 pi M^4(m+m_N)^2]

in natural units. The baryonic fermion mass is m_N and particle mass is m.
For an initially stationary target, the maximum fraction of kinetic energy
transferred is b=4m m_N/(m+m_N)^2. With angle-independent contact scattering,
the fractional loss is uniform on [0,b]. A particle entering from infinity
with speed v_infty has local squared speed v_infty^2+v_esc^2. Its single-
scatter capture probability, conditional on scattering, is

    P_cap = max[0, 1-v_infty^2/{b(v_infty^2+v_esc^2)}].

For particles created inside, replace the required loss by that implied by
their actual local energy; the infinity formula is not automatically applicable.
A baryon column with optical depth tau=integral n_N sigma_chiN dl gives
P_scatter=1-exp(-tau). In the thin, approximately single-scatter limit,
capture probability is approximately tau P_cap. Multiscatter paths, moving
targets, nuclear form factors and changing potentials require more work.

This derives a possible capture channel, not its efficiency. It depends on
g,y,M, baryon columns, particle injection energies and the halo potential.
For a specified truncated isothermal halo, Phi(r)=-v_h^2[1+ln(Rt/r)] outside
its core and inside Rt, before adding baryons. Thus even its escape speed
requires a finite outer radius; an infinite log potential is not a physical
way to guarantee capture. The user analogy supplies none of these rates or
boundary data. Capture in a dense stellar region also does not by itself
populate an extended halo.

## 2. Steady transport outside the production region

Now consider a region beyond most mediator decays. Set the local source J
approximately zero there, retain two-particle annihilation K n^2, and allow
radial velocity u. In a nonrelativistic, isotropic fluid description,

    (r^2 n u)'/r^2 = -K n^2,
    u u' = -[n kB T]'/(m n)-G M_p(r)/r^2,
    n c_v u T' + n kB T div(u) = H,
    M_p'=4 pi m r^2 n,            c_v=3kB/2.

The energy equation follows from the number and energy moments: annihilation
removes the sampled mean internal energy and therefore cancels out of the
specific-temperature equation at constant leading K. It is not an additional
free heating term. Momentum loss similarly cancels when removed particles
sample the mean velocity. Radiation forces, conduction, distributed heating
and baryonic gravity are neglected only in this outer leading balance.

For optically thin central luminosity L_a and energy-transfer cross section
sigma_E, H=n sigma_E L_a/(4 pi r^2). Take candidate powers

    n=A r^-p,  u=B r^-s,  T=T0 r^-t.

Continuity gives s=p-1. In the halo-dominated, subsonic leading momentum
balance, self-gravity requires t=p-2 (with1<p<3 for this local power-law mass
balance). The energy equation has advective power r^-(2p+t), while central
heating has power r^-(p+2). Their equality gives

    p=2,  s=1,  t=0.

The nonzero coefficients then give

    n=A/r^2,  u=K A/r,
    v_h^2=4 pi G m A,
    kB T0=m v_h^2/2=2 pi G m^2 A,
    H_leading=K A^2 kB T0/r^4.

The outward number flux decreases as1/r because particles annihilate along
the flow. Its value at an inner matching radius R0,
4 pi K A^2/R0, equals the integrated annihilation outside R0 for the ideal
tail. Inner creation/capture must supply that flux. It is not a static pool
with zero particle turnover, nor necessarily an unbound wind: outward bulk
velocity can be small compared with random/escape velocities. Actual binding
requires a finite configuration and distribution, not just a small u.

### What the leading solution does and does not prove

For the exact n=A/r^2 and u=K A/r ansatz, retaining inertial acceleration in
momentum gives

    T(r)=T0-m K^2 A^2/(4 kB r^2),

after discarding an r^2 homogeneous temperature term inappropriate to this
outer balance. Substituting into the energy equation requires

    H=K A^2 kB T0/r^4
       +m K^3 A^4/(2 r^6).

The assumed constant-luminosity heating supplies only the first term. Hence
this is an asymptotic solution to leading order, not an exact global solution.
Density, luminosity or temperature corrections would need a coupled solve.
A useful regime requires K A/r much less than sqrt(kB T0/m), T>0, negligible
central baryonic force relative to halo force, and r inside an eventual cutoff.
The infinite tail has infinite total mass; no outer radius or phase pressure
has been selected. A proof of formation, capture and dynamical stability is
not supplied by these dominant balances.

Without heating, the same n and u would require T proportional to r^-2/3
from the internal-energy equation. Thus gravity and transport alone do not
sustain this approximately isothermal flat tail.

## 3. Heating from the same contact interaction

Use -lambda chi^2 a^2/4, with massless a incident on a chi initially at rest.
In natural units, at tree level the amplitude is angle-independent in the
center-of-mass frame. For incident radiation energy E,

    sigma_el=lambda^2/[16 pi m(m+2E)],
    <Delta E>=E^2/(m+2E),
    sigma_E=sigma_el <Delta E>/E
           =lambda^2 E/[16 pi m(m+2E)^2].

The nonrelativistic annihilation coefficient from the earlier calculation is
K=lambda^2/(64 pi m^2). Their dimensionless ratio, restoring c for SI transport,
is therefore

    zeta = c sigma_E/K = 4mE/(m+2E)^2.

Here m and E in the final fraction are energies in natural units; with SI
masses replace m there by mc^2. The common coupling lambda cancels at this
order. This is an actual microscopic relation, unlike choosing independent
absorption and annihilation coefficients. It does not remove the particle
mass, radiation spectrum, luminosity, transport or boundary dependencies.
For a spectrum, use the energy-luminosity-weighted cross section, not a
single arbitrarily chosen E.

The identity

    1/2-zeta=(m-2E)^2/[2(m+2E)^2] >= 0

shows a kinematic maximum zeta=1/2 at E=m/2. This is NOT the requested MOND
coefficient. No mechanism selects that photon energy; the resulting acceleration
normalization also contains L_a/Mb. For photons from cold chi annihilation,
E approximately m instead gives zeta=4/9 at this scattering order.

### Cold-fluid and optical-depth limits

The scattering calculation is valid kinematics for a stationary target; using
its mean energy transfer as a smooth cold-fluid heating rate is an additional
approximation. Hard radiation with E comparable to m imparts order-m rest-energy
recoil in a single event. A particle may escape rather than share that energy
with a cold halo. Rapid thermalization/cascading before escape must be shown,
not inferred from the contact cross section. For genuinely soft photons,
<Delta E> approximately E^2/m; keeping individual recoils small relative to
binding energy demands a correspondingly small E/m and generally small zeta.
Doppler/recoil thermal corrections also matter when radiation energy is close
to the thermal energy scale; the stationary-target heating formula alone is
then insufficient.

Optical thinness requires integral n sigma_el dr much less than1 over the
heating path. Fluid closure requires enough momentum/energy redistribution
among chi particles. Their stabilizing quartic may provide elastic collisions,
but its magnitude and timescale have not been selected or checked. A dilute
radiation path and a collisional material halo are distinct requirements.
Radiation momentum force decays as1/r^2 per particle for fixed luminosity,
subleading to the formal halo gravity1/r at sufficiently large r; this does
not establish that it is negligible throughout a finite galaxy.

## 4. Normalization after the coupling cancellation

Equating the leading heating and energy requirements gives

    A^2=sigma_E L_a/(8 pi^2 G m^2 K),
    v_flat^4=2 G (sigma_E/K) L_a=2 G zeta L_a/c.

If L_a=ell_a Mb is independently justified, then

    a_eff=2 zeta ell_a/c,
    kappa=2 zeta ell_a/[c^2 sqrt(G rho_DE)].

The flat-curve power can therefore survive conditionally, and one coupling has
cancelled. But rho_DE appears nowhere in the derived capture, scattering or
transport coefficients. The target would require a new physical relation

    ell_a=c^2 sqrt(G rho_DE)/(4 zeta).

Assigning this luminosity by hand would insert the answer. Even zeta=1/2
only gives a_eff=ell_a/c; it is not a derivation of a_eff=c sqrt(G rho_DE)/2.
The outside vacuum offset and phase boundary remain independent parameters.

Annihilation-powered inner radiation does not immediately fix the issue.
If a fraction f of supplied rest-mass power produces the inner radiation,
L_a=f m c^2 dotN_supply, and if dotN_supply matches the ideal outer sink
4 pi K A^2/R0, substitution into the leading energy equation cancels A^2.
It instead requires

    R0=f sigma_E c^2/(2 pi G m).

This conditional relation is a constraint on inner geometry/efficiency, not
a selected abundance or baryonic luminosity law. Core luminosity, surviving
particle supply, and radiation fractions must be solved consistently; the
same particles' energy cannot be counted twice. No core solution is claimed.

## Evidence, review, and continuation

transport_capture.py passes14 exact checks: portal scattering factors, capture
kinematics, recoil averaging, shared-coupling ratio, exponent selection,
continuity, momentum, energy correction and total particle-flux balance. The
negative control reverses the sink sign and fails continuity. Both manifests
are retained and validated. This is self-review of conditional analytic
relations, not an independent audit or a numerical galaxy simulation.

Primary-source context: the abstract of
[Improved Treatment of Dark Matter Capture in Neutron Stars](https://arxiv.org/abs/2004.14888)
describes capture through scattering and energy transfer. Its compact-star
calculations are not being transplanted into a galaxy; our nonrelativistic
single-scatter formulas and their limits are derived above.

Disposition: transport removes the immediate local-reaction profile obstruction
at the level of an outer heated fluid balance. It does not establish a finite
supported captured halo. Remaining work requires a specified inner source and
spectrum, optical depth and thermalization rates, baryonic distribution and
outer phase boundary, followed by a coupled transport/stability calculation.
Those choices affect physical existence and cannot be chosen to match a target
coefficient without making the model a fit. The cancellation of lambda is real
within the tree approximations; the normalization and1/2 remain unresolved.
