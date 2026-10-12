# Reaction relaxation along the source orbits

Status: integrating the fixed-bath Bose gain–loss coefficient along the bound
source orbits finds modest change over one radial period, and substantial
change over several periods. This supports orbital averaging as a useful
leading approximation, but does not make the collisionless residence profile
a permanent halo component or a self-consistent kinetic equilibrium.

## The quantity being propagated

Keep the daughter Plummer distribution and gravitational potential fixed.
Along a source characteristic, the collision term from RESONANT_KINETICS.md
has the form

    dF/dt = G(r,P)-L(r,P)F,
    G = Gamma_NR <f+ f->,
    L = Gamma_NR [1+<f+ + f->],
    Gamma_NR = g^2 u/(16 pi m).

Angle brackets average over the outgoing daughter direction in the source
rest frame, at retained nonrelativistic order. The two daughter occupations
are evaluated in the halo frame, including the zero occupation of unbound
states. This is the full angular average, not the earlier rest-source value
at one selected halo velocity.

For two source distributions on the same fixed orbit in the same bath,
their difference obeys

    d(delta F)/dt=-L delta F,
    delta F(T_r)/delta F(0)=exp[-integral_0^Tr L dt].

This is memory of a phase-space occupation perturbation. It is **not a
tagged-particle survival probability**. The net loss coefficient follows
from cancellation between stimulated forward and inverse terms. Gross
stimulated decay probabilities cannot be substituted for it. In a closed
system the daughters would respond too; their perturbations are frozen here.

## Angular integral and orbital variables

Use the source-orbit units in SOURCE_ORBITS.md. For conserved specific
energy E, define

    B=-esc0 E-1/2 > 0,
    q=vchi/(u c),
    f+(mu)=C (B-q mu)_+^(7/2),
    C=A0/esc0^(7/2).

A0 is the central daughter occupation amplitude, 1.60488e53 in the test
halo. The constant B follows from esc-ec/2=-esc0 E-1/2 and the bound-source
inequality. The partner occupation is obtained by mu -> -mu. Therefore

    <f+>=C [(B+q)^(9/2)-(B-q)_+^(9/2)]/(9q),

with limit C B^(7/2) at q=0. The calculation evaluates the difference using
log1p/expm1 where cancellation would otherwise lose precision. Independent
angular quadrature checks the expression on both sides of q=B and near
q=0. L=Gamma_NR(1+2<f+>) is then integrated with the radial residence
measure dr/|vr| already validated in SOURCE_ORBITS.md.

## Results and refinement

Use the same birth weights, fixed potential, density and microscopic coupling
as the prior bound-halo calculation. The finest quadrature gives:

| Diagnostic | Birth-weighted value |
|---|---:|
| Mean radial period | 0.26490 Gyr |
| Mean orbit-averaged L | 0.53623 Gyr^-1 |
| Mean integral of L over one radial period | 0.13148 |
| Mean occupation memory after one radial period | 0.87737 |
| Mean occupation memory after three radial periods | 0.67801 |

Each orbit has its own period. “Three radial periods” therefore does not
mean one common elapsed time for the entire ensemble. Also, the mean of
exp(-integral L dt) is not exp of the mean integral. The script performs
these distinct averages explicitly.

No sampled orbit has an integrated one-period coefficient exceeding one.
This finite sample does not prove a uniform maximum over all allowed orbits.
The orbit-averaged rates in the finer sample span roughly 0.00617 to
1.22023 Gyr^-1; extreme sample values are not certified global extrema.

The 8192-orbit and 27,648-orbit quadratures agree in one-period mean memory
to better than 2e-11, and changing the radial residence quadrature from 32
to 64 points changes it by less than 4e-13. These are finite numerical
comparisons, not interval bounds. All 16 checks pass, including the angular
integral, turning-point/binding conditions and refinements.
`orbital_reaction_memory.py` and
`orbital_reaction_memory_run/manifest.json` preserve the calculation; the
manifest validates. Interpretation is self-reviewed.

## Consequence for a coupled halo calculation

Source occupations can move around their bound orbits before the net
reaction substantially changes a perturbation, so an orbit-averaged kinetic
treatment has a quantitative basis in this example. The ratio is modest,
not asymptotically tiny: order-ten-percent change per period can matter,
and no controlled averaging-error theorem has been established.

The result also limits the earlier collisionless residence calculation:
after repeated orbits, reactions cannot be omitted if one wants a stationary
mixed-species distribution. The next self-consistent treatment must evolve
daughter depletion, source gain and loss, orbital distributions, and gravity
together while preserving the appropriate conserved quantities. This test
does not supply those coupled dynamics, heat export, a final core, or the
repo's baryonic/vacuum-dependent acceleration law.
