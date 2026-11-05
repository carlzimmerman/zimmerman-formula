# Can a finite pool select its speed?

## Result and scope

A pressure-confined, self-gravitating isothermal pool has a calculable first
mass maximum. At that point its dispersion obeys

    cs^4 = G^(3/2) Mp sqrt(Pext) / 1.18222658849960.

This derives a mass–pressure–speed relation, without inserting the desired
1/2. However, Mp is the gravitating pool mass, not the baryonic mass Mb;
Pext is positive confining pressure, not automatically dark-energy pressure.
Neither universal marginality nor either identification is derived. The
finite sphere also must not be identified with its infinite-radius flat tail.
This is a bounded new boundary-condition test, not adoption of a dark sector.

## Derivation

Assume Newtonian spherical equilibrium, P=cs^2 rho, constant cs, negligible
baryonic gravity for this first pool-only calculation, and a fixed positive
external pressure. Write r=r0 x, rho=rho_c exp(-psi), with
r0=cs/sqrt(4 pi G rho_c). Hydrostatic balance and mass conservation give

    (x^2 psi')' = x^2 exp(-psi),  psi(0)=psi'(0)=0.

At the surface rho_s=Pext/cs^2. Eliminating rho_c yields

    Mp = mu(x) cs^4 / [G^(3/2) sqrt(Pext)],
    mu = x^2 psi' exp(-psi/2)/sqrt(4 pi),
    mu' = x^2 exp(-psi/2)/sqrt(4 pi) [exp(-psi)-psi'^2/2].

The first maximum therefore satisfies psi'^2=2 exp(-psi). We found this
zero from the differential equation, without supplying its radius or mass.
Two independently integrated tolerances give:

| Quantity | Computed value |
| --- | ---: |
| First critical x | 6.45075144417408 |
| Critical mu | 1.18222658849960 |
| Central/surface density | 14.0420320486408 |
| beta = x psi' at surface | 2.43450306787798 |

The sign change verifies a mass maximum on the sampled sequence; no radial
stability eigenproblem or formation attractor was solved. Calling this
critical configuration universal would add a physical assumption.

## What coefficient actually follows?

The infinite regular isothermal solution has v_flat^2=2 cs^2, as derived in
MATERIAL_POOL_DERIVATION.md. If that asymptotic formula is *formally* used
with the critical finite pool's dispersion, define

    eta_M = Mp/Mb,  eta_P = Pext/(rho_DE c^2),
    kappa = [v^4/(G Mb)]/[c sqrt(G rho_DE)].

Here rho_DE is a mass-equivalent density. The formal result is

    kappa_flat,formal = (4/mu_crit) eta_M sqrt(eta_P)
                     = 3.38344615060343 eta_M sqrt(eta_P).

The actual circular speed at the finite surface instead obeys
v_edge^2=beta cs^2. The critical equation gives the exact identity

    beta^2/mu_crit = sqrt(8 pi),
    g_edge = sqrt(8 pi G Pext),
    kappa_edge = sqrt(8 pi) eta_M sqrt(eta_P).

Neither expression is a prediction of the requested universal 1/2.
The finite edge is not an extended flat rotation curve. Selecting the mass
ratio or pressure ratio to make either expression 1/2 would insert the target.
In particular, making Mp small relative to Mb invalidates neglect of baryonic
gravity; such tuning is not a consistent repair of this calculation.

## Can dark energy supply the pressure?

Let V_in and V_out denote vacuum energy densities (energy per volume),
Penv an ordinary external pressure, and Sigma an interface tension. The
spherical pressure jump, with positive tension, is

    Ppool(R) = Penv + (V_in - V_out) + 2 Sigma/R.

The vacuum has pressure -V. Consequently the same vacuum inside and outside
cancels; its absolute negative pressure cannot simply be replaced by a
positive confining pressure rho_DE c^2. With no pressure difference, wall,
or ordinary environment, a positive isothermal pool has no finite surface
at which its pressure vanishes.

A higher-energy interior phase could supply positive V_in-V_out. That is a
specific possible mechanism, but the phase difference is not set by the
outside cosmological vacuum energy alone. A tension-dominated wall makes
pressure radius-dependent, invalidating the fixed-Pext critical coefficient
above. It must be varied with the wall dynamics rather than substituted after
the calculation. Even granting Pext=rho_DE c^2, the mass inventory and the
choice of critical configuration remain undetermined.

For cs much less than c, that granted pressure would imply
rho_s/rho_DE=c^2/cs^2. Thus neglecting the cosmological gravitational term
inside the dense pool can be locally consistent; it does not justify the
unproved pressure identification.

## Cosmic expansion alone: a different mass scaling

An alternative boundary uses cosmic acceleration rather than pressure.
With H_Lambda^2=8 pi G rho_DE/3 and an exterior pointlike baryonic source,

    cs^2 d ln(rho)/dr = -G[Mb+Mp(r)]/r^2 + H_Lambda^2 r,
    dMp/dr = 4 pi r^2 rho.

Define R_Lambda=(G Mb/H_Lambda^2)^(1/3),
v_Lambda^2=(G Mb H_Lambda)^(2/3), x=r/R_Lambda,
m=Mp/Mb, d=4 pi R_Lambda^3 rho/Mb, b=cs^2/v_Lambda^2. Then

    m' = x^2 d,
    (ln d)' = -(1+m-x^3)/(b x^2).

Turnaround is x^3=1+m. It specifies zero net acceleration, not a wall or a
vanishing density. For a fixed dimensionless family, Mb -> s Mb implies
R -> s^(1/3) R and cs^2 -> s^(2/3) cs^2. Accordingly the formal flat-tail
normalization has

    v_flat^4 proportional to Mb^(4/3),
    kappa = 4 b^2 sqrt(8 pi/3) (G Mb H_Lambda/c^3)^(1/3).

It is mass-dependent, whereas the desired MOND relation requires v^4
proportional to Mb at fixed rho_DE. A baryonic radius, different formation
history, or mass-dependent dimensionless boundary can break this homology;
none has been selected by the pool analogy. This restricted scaling result
is not a no-go theorem for every relativistic or multiphase medium.

Earlier turnaround-bounded isothermal cluster models were already rejected
in covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md, X30. Their
fits were not rerun or reopened. The present pressure extremum is a separate
conditional calculation; the homology argument explains why a tidal
boundary alone supplies no universal MOND coefficient.

## Evidence and review

The contract was frozen before execution. pool_pressure.py implements the
symbolic derivative and two DOP853 integrations (relative tolerances 1e-9
and 1e-11), searching for the first root through x=12. All 12 checks pass;
a deliberate omission of the surface-density derivative fails its intended
symbolic check. Both evidence manifests were validated, including the
expected failed control. Exact edge identities and mass scaling supplement
the numerical root; these are not galaxy data fits.

Metadata correction: the archived computation and manifests contain stale
boilerplate saying 'collocation/quadrature' and 'c=1, signature -+++,
fixed polarization versus fixed conjugate'. The actual executable uses
DOP853 integration and dimensionless Newtonian Emden variables; those
polarization and spacetime-signature conventions are inapplicable. The
archived records are retained unchanged for provenance. This note corrects
the interpretation; it does not alter any executed input or output.

Self-review checked dimensions, the surface derivative, vacuum-pressure
sign, distinction between edge and asymptotic speed, and the mass labels.
No independent review, complete dynamical stability proof, baryonic-coupled
pool solve, or microscopic derivation of the equation of state is claimed.

The remaining physical requirements are explicit: determine the phase/wall
pressure, determine pool mass from baryonic sourcing or exchange, and show
which equilibrium is selected dynamically. An analogy does not fix those
three relations. This route supplies a conditional speed law, not the 1/2.
