# Quantitative exceptional crossover and conditional tail screen

The regular exceptional branch with saturating scalar force can mimic MOND only over a limited force range: even with both branch scales freely optimized, its best uniform relative error is 13.7488% over one decade and 38.4089% over two decades. This is an exact minimax obstruction for the scalar constitutive map, not an observational rejection. Under a separately declared response-moment convention its high-force tail also has divergent C. Neither statement assigns the GR scalar action a BIMOND vacuum dictionary.

## Exact minimax problem

Consider u(j)=j/√(c+d j²), c,d>0, and a fixed target K√j, K>0, on [j1,j2], j2/j1=R>1. Both c and d are free; their common rescaling freely sets overall amplitude. Define h=u/√j=1/√(c/j+d j), turnover j0=√(c/d), x=ln j, x0=ln j0, L=ln R. Then

h(x)=(2√(cd))^−1/2 [cosh(x−x0)]^−1/2.

Let q=hmax/hmin. If x0 lies inside the interval, q²=cosh(max(x0−x1,x2−x0))≥cosh(L/2), with equality uniquely at x0=(x1+x2)/2. If x0 is outside, the near/far distances are a,a+L, a≥0, and q²=cosh(a+L)/cosh a≥cosh L>cosh(L/2). The first inequality follows either cosh addition with tanh a≥0, or the positive derivative tanh(a+L)−tanh a. Thus exterior turnover cannot improve the centered optimum.

For any positive function h with fixed ratio q, adjusting its amplitude t minimizes max|t h/K−1| by balancing the extrema: t hmin/K=1−ε and t hmax/K=1+ε. Therefore ε=(q−1)/(q+1), and the sharp global result is

q*=√cosh(L/2)=√[(√R+1/√R)/2],
ε*=(q*−1)/(q*+1),   j0*=√(j1j2).

The bound is attained with c=d j1j2 and the common scale chosen by the displayed amplitude condition. Interior maximum and equal endpoint minima show all errors, not merely sampled endpoints, are controlled. For R=10, q*=√[11/(2√10)] and ε*=0.1374876239474425. For R=100, q*=√(101/20), ε*=0.3840886392965812.

The opposite exceptional branch u=j/√(c−d j²), c,d>0, exists only when d j2²<c. Here h increases monotonically and

(h(j2)/h(j1))²=R(c−d j1²)/(c−d j2²)>R.

Hence ε>(√R−1)/(√R+1); this is an infimum reached only in the canonical limit d→0, not a finite positive-d optimum. Canonical u=j/√c has equality. The scalar-to-physical acceleration normalization is fixed and source independent as in the parent; allowing an extra Newtonian force in a data fit changes the minimax problem and is not covered by this bound.

## Conditional high-force moment

Now make a different, explicit premise: weak Einstein gravity plus the same linearly sourced scalar measures g=gN+αu(j), j=λgN, with α,λ>0 fixed and gN=A y, A>0. Define ν=g/gN and the mathematical response moment Cresp=∫0∞ y(ν−1)dy, with no counterterm/subtraction. This is a convention for a response functional, not a derived cosmological vacuum C=Λc4/a0² for this action.

For canonical u=j/√c, ν−1=αλ/√c is positive constant, so the upper integral diverges quadratically. For c+d j² with d>0,

y(ν−1)=αu(λAy)/A → α/(A√d)>0,

so it diverges linearly. The c−d j² branch ends at y=√c/(λA√d); it does not define the entire integral. Each regular branch also has a finite constant scalar enhancement at y→0, failing deep-MOND ν∝y^−1/2. These are elementary consequences of the same source inverse, not an independently chosen kernel tail. A UV completion or different physical force map could change them and is outside this pure P(X) test.

## Evidence and scope

checks.py uses exact identities and mpmath50-digit evaluation, with a bounded grid only as a negative-control/attainment corroboration. The proof above establishes the global minimax bound including outside turnarounds. Three controls falsely assert ≤1% one-decade error, opposite-branch improvement, and finite saturating-tail moment; each must fail exactly once. Parent source review authenticates arXiv:1605.06418v2; no new external theorem is used. Parent scientific files are read-only inputs pinned by the standard runner. No observed galaxy errors, full gravitational caustic theorem, vacuum coefficient selector or all-action exclusion is claimed.
