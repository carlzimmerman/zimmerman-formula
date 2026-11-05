# An attractive material pool: deriving the flat-curve tail

This analytic continuation tests the user's description of clumped pools.
It changes the model from a phase vortex to a Newtonian self-gravitating,
spherical fluid. It is not an identification of the two actions or a claim
that the user's medium must be isothermal. No density profile or target
acceleration normalization is imposed.

Assume P=c_s^2 rho with constant c_s>0, where rho is mass density and
c_s<<c. Spherical equilibrium, thermal/dispersion support and negligible
rotation are explicit assumptions. They model a concentration, not a
swirling eddy. The equations are

    dP/dr=-rho G M(r)/r^2, dM/dr=4pi r^2 rho.

Let rho=rho_c exp(-psi), r=r0 x, r0^2=c_s^2/(4pi G rho_c). A regular
central density gives

    (x^2 psi')'=x^2 exp(-psi),
    psi(0)=psi'(0)=0, psi=x^2/6+O(x^4).

The regular solution exists at all finite x: psi'>=0 and exp(-psi)<=1
imply psi'<=x/3, preventing finite-radius blowup. For the large-radius
behavior set t=log x and y=psi-2t+log2. Then

    y_tt+y_t+2(1-exp(-y))=0,
    E=y_t^2/2+2[y+exp(-y)-1], dE/dt=-y_t^2.

The nonnegative energy confines y and y_t to a compact sublevel set after
any finite t. The only invariant trajectory with y_t=0 is y=0. The bounded
autonomous dissipative flow therefore approaches y=y_t=0, giving

    rho(r) -> c_s^2/(2pi G r^2),
    M(r) -> 2c_s^2 r/G,
    g_pool(r) -> 2c_s^2/r,
    v_flat^2 -> 2c_s^2.

The inward force and flat asymptotic rotation curve follow from hydrostatic
balance. A finite baryonic mass is subleading to the ideal tail's growing
mass; its presence does not fix c_s. A real pool must be truncated and
matched to an environment. The ideal infinite tail has infinite mass.
Neither its asymptotics nor the phase-plane argument proves stability of
a finite pressure-confined object; core size and cutoff require more data.

## Normalization test

In SI units the scale inferred for baryonic mass M_b is

    a0_eff=4c_s^4/(G M_b),
    kappa_eff=4c_s^4/[G M_b c sqrt(G rho_DE)].

Obtaining1/2 requires dynamics to produce

    c_s^4=G M_b c sqrt(G rho_DE)/8.

That relation was not supplied to the equations. The dispersion c_s is
independent of M_b and rho_DE here. Choosing c_s separately to satisfy this
relation would fit the target. Relating a boundary density to a cosmic
density still leaves a radius or pressure datum unless further dynamics
selects it.

The fluid has positive pressure, so this component is not a negative-pressure
cosmological vacuum. A shared field could have a vacuum plus material
excitations, but their state, support and energy exchange must be derived.
Adding a constant vacuum term does not determine c_s in these local equations.

## Review and outcome

This is an analytic calculation, not an executable test run. Self-review
checked the dimensionless reduction, regular-origin expansion, energy
derivative, compactness of its sublevel sets, unique invariant
zero-dissipation set, and SI units. The phase-plane argument concerns
radial asymptotics, not time-dependent stability. No observational fit or
independent audit is claimed.

The pool interpretation can produce the required force shape in this
concrete model. It does not yet predict the baryonic mass-speed relation or
the coefficient1/2. Those remain targets for a microscopic interaction or
thermal/history selection mechanism.
