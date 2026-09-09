# IC14: a local conformal-square matter construction

2026-09-08. **Constructive local matter result; full theory OPEN.** Carl's
retained-clock hypothesis motivates this route. The new algebraic construction
below is the present investigation's proposal, not an attribution of these
formulas to Carl. It changes the off-shell auxiliary potential while preserving
the IC11 vacuum pressure. It is not a global completion of IC11's phase action.

## Action and the exact root

Use the IC10 Einstein metric and physical metric relation
`g = exp(2w) gtilde`, with `X=exp(-2S)/2`, and a canonical massless matter
scalar with `Y=-gtilde^{mu nu} psi_mu psi_nu/2`. Define `z=exp(2w)>0`.
Let `w0(X)` be the same implicit original vacuum root `P0_w(X,w0)=0`,
on the chart used in IC10, with `P0_ww != 0`. Define

    z0(X)=exp(2w0(X)),
    F(X)=P0(X,w0(X))+(5/64)(2X)^16,
    L(X,z,Y)=F(X)-(z-z0(X))²/(2t)+zY,   t=1/10.

The local action is `integral sqrt(-gtilde)[mstar Rtilde/2+L]`, with
the unchanged `mstar=exp(-1/6)` normalization. The term `zY` is exactly the
canonical matter action minimally coupled to the physical metric. The constant
`t=1/10` is an explicit design choice, not a measured or derived constant.

Independent variation of `z` gives the unique root

    z=z0+tY,
    Leff(X,Y)=F(X)+z0(X)Y+tY²/2.

For `Y>=0,t>0`, the root is positive. At this root, `L_ww=-4z²/t<0`;
the finite-matter velocity-root fold of the IC11 balanced-square trial is
absent in this local model. Vacuum pressure and its eliminated derivatives
are exactly those of IC11. This reconstructs the potential around the implicit
vacuum branch; it does not assert equality to IC11 away from that branch.

## Implicit jets and a conditional all-density cone statement

All coefficient derivatives in `ic14_matter_square.py` are differentiated
implicitly, without a fitted table. At the original vacuum root put
`B=P0_ww`, `C=P0_Sw`. Since the added IC11 pressure has no w dependence,

    w0_S=-C/B,
    w0_SS=-(P0_SSw+2P0_Sww w0_S+P0_www w0_S²)/B,
    z0_S=2z0 w0_S,
    z0_SS=2z0(w0_SS+2w0_S²).

For any branch function `h`,

    h_X=-h_S/(2X),    h_XX=(h_SS+2h_S)/(4X²).

With `P=P0+f`, the envelope gives `F_S=P_S` and
`F_SS=P_SS-P_Sw²/P_ww`. These identities supply F's derivatives and
the first two derivatives of z0.

The eliminated pressure derivatives are

    Leff_X=F_X+Y z0_X,    Leff_Y=z0+tY,
    Hess(Leff)=[[F_XX+Y z0_XX,z0_X],[z0_X,t]].

At each X satisfying

    F_X>0, z0>0, z0_X>=0, z0_XX>=0,
    t F_XX-z0_X²>0,

both first derivatives are positive and the pressure Hessian is positive
definite for every `Y>=0`. On aligned homogeneous timelike backgrounds,
write `V=diag(sqrt(2X),sqrt(2Y))`. Direct variation gives

    D=diag(Leff_X,Leff_Y),    K=D+V Hess(Leff) V.

Therefore `K>0` and `K-D>=0`, with positive squared characteristic speeds
at most one. At Y=0 the ordinary matter mode is luminal; at Y>0 the stated
strict inequalities give `K-D>0`. This is an exact conditional statement,
not a proof that its hypotheses hold on an entire sampled X interval.

The bare velocity Hessian in auxiliary coordinate z is

    M=diag(Leff_X+2X[F_XX+Y z0_XX-z0_X²/t], z),
    q=(sqrt(2X)z0_X/t, sqrt(2Y)),
    Acan,z=-1/t-q^T M^-1 q.

The same hypotheses imply `M>0` and `Acan,z<0`, so this auxiliary pair
stays second class on these aligned backgrounds. At the root,
`Acan,w=4z² Acan,z`. This is the fixed-canonical-momentum check; it is
not inferred merely from nonzero `L_ww`.

## Finite evidence and the actual local domain

At 50 decimal digits, a uniform grid of 101 S values from .03 to .2 gives:

| Quantity | Sampled minimum or maximum |
| --- | ---: |
| minimum F_X | 1.554711533598 |
| minimum F_XX | 6.429505440591 |
| minimum z0_X | 0.638566943072 |
| minimum z0_XX | 0.129424547941 |
| maximum z0_X²/F_XX | 0.064525403710 |
| minimum (0.1 F_XX-z0_X²) | 0.228418649089 |

This gives 101 positive witnesses for the conditional cone statement.
It is not an interval-arithmetic certificate. For example at `S=.1,Y=.01`,
the squared speeds are `(0.2268706498,0.9989570886)`, the physical Hubble
rate is `0.8665022055`, and `Acan,w=-58.0092270250`.

The inherited auxiliary chart also requires `-S/2<w<0`, equivalently
`exp(-S)<z<1`. The upper matter bound is therefore
`Y<(1-z0)/t`. A mathematical formula for every Y does not extend this chart.

The energy and activation are recomputed from this action:

    rho=2X F_X-F+(2X z0_X+z0)Y+3tY²/2,
    Htilde²=rho/(3mstar),
    r=exp(S-1/6)Htilde/(z0+tY).

The inherited plateau predicate is `3/4<=r²<=5/4`. Solving both boundary
quadratics and selecting the first positive crossing gives the following
fixed-S controls; these are not time-evolution trajectories:

| S | first upper activation crossing Y | original chart cap Y |
| --- | ---: | ---: |
| .03 | .173625098348 | .226639651087 |
| .05 | .426329041946 | .358511338785 |
| .10 | .469573702846 | .651386366285 |
| .20 | .101292168789 | 1.132548879470 |

At S=.05 the inherited chart ends before the activation crossing, so the
displayed latter value is only a formal continuation control. Admissibility
requires the chart, plateau, and local cone predicates together. No activated
phase action or transition extension for this reconstructed potential has
been supplied.

The FLRW rate in the code follows the two scalar charge equations
`vdot=-3Htilde K^-1 D v` and `wdot=(z0_X Xdot+tYdot)/(2z)`.
It is recomputed rather than borrowed from the vacuum background. Positive
physical expansion is observed at the reported samples, not established for
all allowed densities or complete cosmological histories.

## Relative-flow control and reproducibility

The optional frozen-background control places the clock at rest and boosts
the timelike matter gradient with speed v, keeping Y its invariant kinetic
argument. For a wave parallel to the boost, the actual principal matrix is

    Qij(c)=diag(Leff_X,Leff_Y)ij (1-c²)-Hess(Leff)ij di(c)dj(c),
    d(c)=(sqrt(2X)c, sqrt(2Y)gamma(c-v)).

`boosted_characteristics` solves its quartic determinant and checks each
root against this matrix. The v=0 limit is tested against the aligned
speeds. The v=.5 and .9 controls use `S=.1,Y=.0001`; they do not establish
the principal cones for arbitrary relative flow, direction, or density.
The physical activation and gravitational background for these boosted
controls are explicitly uncomputed.

Reproduce from this directory:

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_ic14_matter_square -v
    PYTHONDONTWRITEBYTECODE=1 python3 ic14_matter_square.py

The tests were written first and observed failing before implementation.
They compare implicit jets against independent five-point branch differences,
compare the matter kinetic matrix against the raw three-variable velocity
Hessian's auxiliary Schur complement, check root and domain behavior, and
test the boosted principal polynomial. The finite-difference calculation is
a verification of implicitly derived coefficients, not how they are defined.
The program's `--require-full-closure` mode exits 2: this is not a global
theory certificate.

The missing steps include a certified continuous coefficient domain, a
global extension and activation-transition action, arbitrary matter and
relative-gradient analysis, a strong-coupling estimate, sourced weak fields,
and the MOND/PPN/galaxy and cosmological gates. None is replaced by these
local positive witnesses.
