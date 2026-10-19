# Common-PV profile correction to the boundary sector

2026-10-19 UTC. This hand addendum supplements the immutable
`INDEPENDENT_DERIVATION.md` and completed exact-001 run; it does not change
their inputs. The constant-mass spectral coefficient +16/(315 m R) is
unchanged. The earlier scalar-mass profile candidate is a fixed-frequency
statement and cannot itself be summed after dropping the PV fields.

## Order of work and consulted inputs

The independent derivation and exact-001 run were completed before reading
the prior far-field work. The files read afterwards were:

* `qcd_completion/far_field/ADDENDUM_2026-10-19_COMMON_PV.md`, SHA-256
  `234dc4a55e2cfe7ff007e2a2c525285f2d19f087399b001b6d734bc187acba18`;
* `qcd_completion/far_field/RAW_STATIC_DERIVATION.md`, SHA-256
  `de5b6d71c6c377e26400d2deb103d59f8d0b948857ff63c05a8acc24d1d12b16`.

These inputs make the order-of-limits issue explicit for the bulk. The
boundary correction below is independently derived from the boundary heat
table, not identified with a bulk integration-by-parts surface density.

The independent raw derivation is pinned by SHA-256
`6423b09b5d1f1b9b4f1898c019bc8e429568656abf13508871391893d8ad5a97`.
The exact-001 manifest is pinned by SHA-256
`38dec8b12a4dae14ffbfdfd2ec18fd26fed8b70945a8a6a04039b53c40e91003`.

## Derivation at finite regulator masses

Let the tail be h=v-a/r, with a fixed dimensionless number (a=1 in the
contract), q_n=2 pi n/L+v, U_nj=q_n^2+M_j^2, and mu_nj=sqrt(U_nj).
Use fixed PV ratios and coefficients c_j, c_0=1, M_0=0. The common
regulator is imposed on the entire four-dimensional determinant; all
vector/ghost boundary domains are retained. The moment conditions in the
independent derivation are sufficient for this finite regulated operation.

At the wall, the scalar part of a regulated mode has mass

    mu_b = sqrt((q_n-a/R)^2+M_j^2)
         = mu_nj-a*q_n/(mu_nj R)
           +a^2*M_j^2/(2 mu_nj^3 R^2)+O(R^(-3)).

The term -8 R mu_b/3 in the wall determinant therefore contributes

    -4 a^2 M_j^2/(3 mu_nj^3 R)

at inverse radius. It vanishes modewise for the physical M_0=0 field.
It does not vanish when the infinite Matsubara tower is summed before
the common PV masses are removed.

The log term contributes -5a*q_n/(4 U_nj R). The smeared a3 first-jet
term in the independent derivation contributes +5a*q_n/(8 U_nj R).
The cubic geometry gives +16/(315 mu_nj R). Thus the local scalar-mass
wall sector through inverse radius, with the stated heat separation, has
the finite-regulator coefficient

    C_wall(PV) = sum_n sum_j c_j {
                    16/(315 sqrt(q_n^2+M_j^2))
                  - 5a*q_n/[8(q_n^2+M_j^2)]
                  - 4a^2*M_j^2/[3(q_n^2+M_j^2)^(3/2)] },

with Gamma_wall|inverse = C_wall(PV)/R. The profile derivative terms in
this formula inherit the independent derivation's explicit local-response
scope; they require fresh mathematical review before use in a full closure.

## The finite contribution lost by taking d=3 modewise

For each heavy regulator, put t=q_n/M_j. The spacing in t is 2 pi/(M_j L).
The positive, integrable function (1+t^2)^(-3/2) has integral 2, directly
from the antiderivative t/sqrt(1+t^2). Its Riemann sum gives

    sum_n M_j^2/(q_n^2+M_j^2)^(3/2) -> L/pi.

Since sum_{j>0}c_j=-1, the last line of C_wall tends to

    +4 a^2 L/(3 pi).

It is an actual lower-order wall heat term evaluated on the profile. It is
not a new value of the constant-mass cubic coefficient. It cannot be
obtained by setting all M_j to zero in each frequency before summation.

At center holonomy v=pi/L, the map n -> -n-1 sends q_n -> -q_n.
Consequently the middle term of C_wall vanishes exactly for every finite
PV mass. The first term still has the logarithmic cubic-wall divergence
and its surface matching constant. Before that cubic surface matching,

    C_wall,center(PV) = (16/315) sum_n,j c_j/mu_nj
                       +4 a^2 L/(3 pi)+o(1).

The divergent geometric sum is independent of a at this inverse-radius
order. Comparing this *local wall sector* on a=1 with a=0, in the same
surface scheme, leaves +4L/(3pi R) at center. This is not a result for
the full difference of the monopole and vacuum determinants: their bulk,
core, and other matching contributions must also be supplied.

For general gapped holonomy the regulated odd sum must be retained in the
same common scheme. No closed-form cotangent identity is needed for the
center statement, and none has been imported as unchecked source input.

## Why other candidate wall terms do not repair closure

The leading area term is zero in the actual gauge/ghost heat combination.
The flat-wall first and second mass jets have the cancellations already
shown in the smeared heat calculation. Magnetic and electric spin effects
start quadratically in F in the local wall trace; at fixed mode they give
wall order R^(-2). Their frequency coefficients scale as inverse mass
squared or faster, so their heavy-PV sums do not generate the R^(-1)
term above. Bulk F^2 and mass-gradient-squared terms remain order R^(-1)
after the radial integral and cannot be omitted. These statements still
presume a smooth, gapped derivative expansion near the outer wall.

No numerical computation or frequency fitting was performed for this
addendum. The PV limit is a hand Riemann-sum argument. The exact-001
manifest validates only its previously declared finite rational checks.

## Remaining implication

The wall benchmark closes the specific all-Dirichlet/moving-projector
ambiguity. A full gauge/ghost monopole inverse-radius action requires a
single matched bulk and boundary density convention, a fixed finite
surface counterterm, regulator-uniform control of the local expansion,
and the core/neutral angular matching. A physical stress and physical
electromagnetic charge remain separate missing maps. A fresh reviewer
should first reconstruct the smeared a3 jet coefficient and the finite
PV contribution above from the operator and domain.
