# Restricted hyperbolicity barrier for a combined concentration

Independent derivation and correction: review/BRANCH_BARRIER_AUDIT.md.
The initial suggestion Astar>2sqrt(gamma) was too weak and is NOT used.
The correct condition below is Astar²>6gamma.

For the native auxiliary H, direct differentiation gives
 R=H_rr=3+A²/gamma-6Ar+6gamma r²,
 h=H_r.
At r=A/(2gamma), D_r=0, h=r and
 R=3-A²/(2gamma), c²=h/(rR)=1/R.
If A²>6gamma, this is a strictly elliptic scalar state, not merely a vanishing
coercivity bound. Also Q=Ar=A²/(2gamma)>3, so the native switch is strictly on.

Consider a continuous clock-slice path from an outer state with
r_out<Astar/(2gamma) toward an unbounded-r layer. Uniform cap separation,
r>=r_min, regular crossing geometry and finite regular outer A imply from
eA=Wp/r that A stays uniformly close to Astar across the shrinking layer.
For a fixed strict Astar²>6gamma margin, the continuous function
r-A/(2gamma) must cross zero before reaching large r. At that crossing R<0
and h>0. Off-branch excursions cannot bypass this crossing: Q=1 requires
r=1/A, strictly below A/(2gamma) in the same A range.

Thus no everywhere-hyperbolic smooth native layer in this regime can realize
the large-r component of the PF09 mixture. Without finite-current assumptions,
a realization retaining the other bounds must pass through a loss of Cauchy
hyperbolicity. This is not a theorem that mixed-type solutions do not exist.

The coupled principal symbol retains this obstruction. At any fixed smooth
state, the spatial auxiliary equations make their perturbations lower order
in the high-frequency scalar equations. Their finite-coupling response cannot
change the leading determinant R omega²-(h/r)k². The Einstein wave block has
algebraic stress sources and does not repair the nonreal scalar root. At the
crossing, additionally D_r=0 removes the leading n(A) coefficient directly.
This is a local principal-symbol calculation, not an exact frozen-A wave ansatz.
An elliptic patch gives growth rates proportional to arbitrarily large |k| in
the continuum Cauchy problem; it supplies no stable predictive continuation.

For outer D=0 data A0=1/r0+gamma r0, write u=gamma r0²<1. Then
 A0²/gamma=(1+u)²/u.
The barrier condition is u<2-sqrt(3), about0.267949. The numerical fixture
u=.001 and the previously recorded tiny physical footing satisfy this condition;
this does not turn the fixture into a proved event-time prediction.

The restriction is essential. At u=1/2, A0²/gamma=4.5 and
R>=3-4.5/2=.75 for every r. Since h(r0)=r0 and h'=R>0, the constitutive
path r>=r0 remains scalar-hyperbolic. This is a counterexample to the initial
universal u<1 barrier claim, not a full native layer or a survival example.
The separate finite-current exclusion does not require this barrier condition.
