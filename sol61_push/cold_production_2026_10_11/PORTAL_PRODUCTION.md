# Dense spatial conversion with the nonlinear vacuum portal

Status: a classical seeded envelope test of the new softened interaction.
The leading high-density mass shift is absorbed into the free frequencies;
the remaining density-dependent force is retained. This is not a quantum
vacuum-production calculation or a full relativistic field evolution.

## Separating the mass shift without discarding the interaction

For U(S)=A_*[sqrt(S^2+S_0^2)-S_0], write

    U(S)=A_* S-A_* S_0+V_res(S),
    V_res(S)=A_* S_0^2/[sqrt(S^2+S_0^2)+S].

The constant does not affect local dynamics. The linear term changes the
aligned mass parameters to

    mbar^2=m^2+A_*,    Mbar^2=4mbar^2+Delta.

The residual derivative is

    U'(S)-A_*=-A_* S_0^2 /
              [sqrt(S^2+S_0^2)(sqrt(S^2+S_0^2)+S)].

This stable expression avoids catastrophic cancellation when S/S_0 is
large. It also remains finite at S=0. No high-density series is used to
compute the force.

Use the leading NR normalization of SPATIAL_CONVERSION.md, with daughter
and source envelopes A and B and n=|A|^2+|B|^2. At this retained order,
S=S_ref n with S_ref=4 A_source,0^2. The exact relativistic number-to-field
normalizations differ at relative order u^2; they are not included in this
local density relation. Define

    d=S_0/S_ref,    K=A_*/(2 mbar^2 epsilon_bar),
    epsilon_bar=g A_source,0/mbar^2,
    D(n)=-K d^2/[sqrt(n^2+d^2)(sqrt(n^2+d^2)+n)].

The local envelope equations gain D(n)A and 2D(n)B respectively. The factor
of two follows from the charge alignment and unequal source/daughter
symplectic normalizations. Their Hamiltonian gains

    2K <d^2/[sqrt(n^2+d^2)+n]>,

up to the discarded constant. The interaction therefore preserves total
charge and the retained Hamiltonian; it is not a damping or cooling term.

The free detunings use mbar, u_bar=u m/mbar and Mbar/mbar, with the
conversion normalization and quartic coefficient recalculated. This
absorbs the uniform mass shift into actual frequencies rather than merely
ignoring a large phase in the old frame. As in the original envelope pilot,
the free dispersion is relativistic but the vertices are leading NR.
This mixture does not establish a full relativistic error bound.

## Numerical scope

portal_production.py uses the existing classical seed (471901), a periodic
24^3 grid, fixed Fourier spacing 0.4 and final dimensionless time x=30.
It repeats the portal calculation at steps 0.01 and 0.005, then runs the
same shifted-mass model without the residual force at step 0.005.
The comparison isolates the residual interaction, not the common mass shift.
Charge, Hamiltonian, moving-source population and high-mode population are
recorded. The minimum local charge density and largest residual phase rate
are measured at every nonlinear Runge-Kutta stage, including intermediate
stages, not just coarse output snapshots.

These minima cover sampled spatial sites and numerical stages. They are
not a certified continuum lower bound between grid points or steps. Nor
does a small local force alone prove a uniform long-time solution-error
bound in a nonlinear system. The paired finite simulation supplies a
separate numerical comparison.

## Results and interpretation

| Step | Endpoint daughter fraction | Moving-source charge | Maximum energy drift |
|---|---:|---:|---:|
| 0.01 | 0.63615053 | 0.24006900 | 5.63e-5 |
| 0.005 | 0.63618321 | 0.24006944 | 1.41e-5 |

The finer run's maximum charge drift is 5.11e-11. Halving the step changes
the endpoint daughter fraction by 3.27e-5 and reduces energy drift by
about four. The paired shifted-mass control differs in sampled daughter
fraction by at most 2.642e-14; this is a roundoff-level numerical
comparison, not a physical accuracy claim at that precision.

The smallest sampled local charge density in the fine run is
2.72576e-4 of the normalization. Even there, S/S_0 is approximately
6.14389e+08. The maximum residual phase rate is 1.66743e-17 in
the dimensionless evolution units. These measurements explain why the
nonlinear pressure correction has no resolved effect on this trajectory
after the common mass shift is included. The outer-mode charge is about
1.00e-8 at the endpoint.

All eight pilot checks pass and the manifest validates provenance. No new
spatial-resolution or ensemble convergence study has been performed for
this portal, and there is no rigorous envelope or quantum error estimate.
The former model's resolution results are context, not proof of convergence
for every state of this new interaction. The derivation is self-reviewed.

## What this advances and what remains

The nonlinear portal has now been included in a spatial seeded production
trajectory, rather than being judged solely from its homogeneous linear
band. Substantial transient conversion and moving-source population survive
in this example. The endpoint fraction is not a permanent abundance.

The dense regime is almost a linear mass shift. The pressure-support regime
is different: it occurs near S/S_0 of order unity and was deliberately not
reached in this fixed-density periodic production run. Expansion, dilution,
chemical conversion, kinetic stress and gravity must connect the two regimes
before the production result and the pressure-only equilibrium family can
be treated as one history. Neither the earlier Gaussian quantum yields nor
the original loading-clock trajectory have been recomputed for this action.

This result makes the proposed nonlinear interaction compatible with one
explicit dense production scenario, within its retained approximation. It
does not establish the repo's halo profile, acceleration law, vacuum flux
selection, observed abundance or complete cold-energy construction.
