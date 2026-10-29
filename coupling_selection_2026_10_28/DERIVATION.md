# CS28 coupling selection: three routes and a model-building constraint

## 1. Flow does not select the MV28 vacuum couplings

Write u=h^2, v=lambda^2, w=g^2, k=1/(16 pi^2), t=ln(mu).
For the same SU(5) model and normalization as MV28,

    u_t=2ku(14u+21v/5-20w),
    v_t=2kv(2u+21v/4-30w),
    w_t=-10kw^2.                                           (1)

The radial vacuum condition is w=29v/200, with u,v>0. There,

    beta_h/h=k(14u+13v/10)>0,
    beta_lambda/lambda=k(2u+9v/10)>0,
    d ln(h/lambda)/dt=k(12u+2v/5)>0.                        (2)

Thus even the Yukawa ratio is not stationary on the radiative vacuum.
The vacuum selects a crossing scale, rather than a simultaneous fixed point.

Allowing the overall gauge coupling to run does not fix this. Set p=u/w,
q=v/w. A fixed ray with p,q>0 requires

    14p+21q/5=15,   2p+21q/4=25.

Its unique algebraic solution is p=-25/62, q=3200/651; p is negative.
The nonzero boundary rays are (15/14,0) and (0,100/21).
Neither gives the positive-coupling vacuum q=200/29. This is a one-loop
statement, not an exclusion of all nonperturbative trajectories.

There is also an ultraviolet obstruction within these equations. Starting
on the vacuum, v increases and w decreases toward increasing t. Therefore
w/v stays at most 29/200 and

    v_t >= (9/5) k v^2,
    1/v(t) <= 1/v_* - (9/5)k(t-t_*).                       (3)

The one-loop solution cannot extend to arbitrarily high energy with finite
couplings; its formal blow-up time is at most 5/(9kv_*). More conservatively,
it must leave any prescribed finite perturbative domain before that bound.
This excludes continuation to the Gaussian ultraviolet fixed point using
this one-loop model on this branch. It is not a claim of a physical Landau
pole after perturbation theory has failed.

## 2. An exact obstruction to an interior superconformal fixed point

Take f=0 when seeking a fixed point of the dimensionless theory. Suppose
the original field content reaches a unitary four-dimensional N=1 SCFT
with both superpotential interactions nonzero, and X remains a nontrivial
gauge-invariant chiral primary in that interacting theory. Superpotential
R charge two and the anomaly-free gauge R current require

    R_X+2R_A=2,   R_B+2R_A=2,
    5+5(R_A-1)+5(R_B-1)=0.

These imply exactly

    R_A=1,   R_B=R_X=0.                                   (4)

But a nontrivial gauge-invariant chiral primary has R>=2/3 and dimension
Delta=3R/2. In particular X would have dimension zero, a contradiction.
This excludes that interior SCFT even at strong coupling under the stated
hypotheses. These representation-theoretic facts and the anomaly condition
are checked in Intriligator-Wecht v3, introduction, pp. 1-3; see SOURCES.md.

An accidental free X must instead have R_X=2/3 and decouple: one cannot keep
both nonzero interacting superpotential constraints (4). Boundary fixed
points, singular descriptions where X ceases to be such an operator, added
fields, confinement, and gravity are not excluded by this argument. In
particular, this is not a classification of every possible UV completion.

## 3. Multiplet normalization can fix h/lambda, but not the stiffness ratio

As a conditional algebraic embedding, put an SU(5) adjoint A in the upper
block of an SU(6) adjoint and combine B and X into

    B_6=diag(B,0)+X H,   H=diag(1,1,1,1,1,-5)/sqrt(30).

Tr(H^2)=1, so X has the same canonical normalization as the adjoint
components. Restricting (lambda/2)Tr(A_6^2 B_6) to these components gives

    h/lambda=1/sqrt(30),  30h^2=lambda^2,
    V_tree=f^2/2,
    B_curv/V_model=5887 lambda_*^4/[10800(16pi^2)^2].        (5)

This fixes a relative normalization, while leaving a fourth power of an
unselected coupling. The MV28 vacuum also requires lambda^2/g^2=200/29.
Any proposed exact relation lambda=c g must have c^2=200/29 at that
stationary point in the original one-loop matching. An arbitrary choice
of c is not a vacuum derivation.

Equation (5) is an embedding identity, not a completed SU(6) model. The full
adjoints contain additional components; breaking SU(6), giving those fields
masses, and generating fX require additional dynamics and alter thresholds
and beta functions. Those cannot be silently discarded. Ordinary SU(5)
internal symmetry cannot rotate its singlet X into its adjoint B: they are
inequivalent gauge representations. Enlarging the group is a concrete way
to remove that representation obstruction, with the above costs.

## 4. What additional dynamics must change

Write extra anomalous-dimension contributions as k delta_X, k delta_A,
k delta_B, keeping the original terms and field normalization. At a
perturbative fixed point with h,lambda nonzero, eliminating w gives the
necessary relation

    delta_B-delta_A-(3/2)delta_X = 19u+(21/20)v > 0.         (6)

Pure spectator matter changing only the gauge beta function leaves the
left side zero at this order, and cannot produce this fixed point.
Additional Yukawa interactions preferentially affecting B are required
in this restricted perturbative route. This is necessary, not sufficient;
the gauge beta function, unitarity, potential and thresholds must also work.

For comparison, setting beta_h=beta_lambda=0 without new gamma terms gives
u/w=-10/31, v/w=3800/651: again the required h^2 is negative.
This is distinct from the running-gauge fixed-ray calculation above.

## Status

No predicted numerical B/V has been obtained. The new results distinguish
three mechanisms instead of assuming they work: flow selection fails in
the stated approximation, an interior SCFT is obstructed under explicit
operator hypotheses, and a group embedding fixes only h/lambda. Equation
(6) specifies a concrete requirement on a replacement microscopic model.
All MV28 common-threshold, full-spectrum, gravity-energy and halo-portal
limitations still apply. None of the couplings has been fitted to data.
