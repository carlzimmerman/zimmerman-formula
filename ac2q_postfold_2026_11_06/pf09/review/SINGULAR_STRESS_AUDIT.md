# Independent audit: transverse positivity and large-r stress

**Verdict: correct under the stated strong slice/trace controls, made
explicit here.** These are restricted exclusions, not singular selection.

The exact full-switch transverse formula is

    T_perp+V=r^2/2+(gamma/2)D_eff^2+P W_P-W,
    D_eff=max(D,-r^2).

Convexity and W(0)=0 imply P W_P-W>=0. Therefore
T_perp+V>=(gamma/2)(D_+)^2 on both branches. This sign does not rely
on signed total-action coercivity or on penalizing negative divergence.

Along a clock slice, e(Pi)=exp(2beta)D. A layer of proper width epsilon
has positive Pi variation bounded by C sqrt(epsilon)||D_+||L2. A fixed
cap excursion beyond compact endpoint P values requires fixed positive
Pi variation if the nondegenerate metric weights have vanishing oscillation
across the layer. Uniform regular metric convergence/bounded first
derivatives are sufficient. Bounded weights alone, without this trace
regularity, would not make a P excursion imply a Pi excursion.

Hence a uniform per-clock-slice bound on integral(T_perp+V) excludes
such a cap excursion: its cost would be at least c/epsilon. The candidate
correctly does not infer that slice bound from finite spacetime stress
measures. Intermittent bursts are outside this particular estimate.

## Large invariant r with bounded unit-clock rapidity

Retain r>=r0, cap separation, bounded rapidity, regular metric, controlled
clock crossings, bounded anchored A and strong same-clock endpoint Pi
matching. Then e(A)=W_P/r controls A. The preceding uniform slice stress
bound makes positive Pi variation O(sqrt(epsilon)); endpoint matching
makes its negative variation tend to zero. Bounded metric weights give
vanishing slice integral of D_- and hence of mu<=D_-.

To transfer this to a spacetime statement, retain uniformity on compact
clock-label intervals and controlled coarea/crossing geometry. In particular
clock labels intersecting the layer over a compact interface-time interval
must lie in a uniformly bounded range. Regular bounded outer clock traces
and bounded rapidity/crossing length supply this: a clock slice reaches
the exterior within O(epsilon) interface time. Merely naming a slice
estimate without this time/label control is insufficient.

On multiplier mass Q=1. Bounded rapidity therefore makes the mu stress
vanish in L1. With bounded A,P and cap margin,

    H=(gamma/2)r^4-A r^3+O(r^2+1),
    rH_r=2gamma r^4-3A r^3+O(r^2+1),

uniformly in the layer. Both quantities are bounded below by a positive
multiple of r^4 minus a constant. For a unit spacelike interface normal N,

    T_NN=H+(rH_r-mu Q)(n.N)^2>=c r^4-C-C mu.

Bounded connection times finite stress measures can have a measure defect
but not a normal dipole. The normal delta-prime coefficient of the limiting
stress conservation law therefore gives N^a S_ab=0, in particular S_NN=0,
provided the stress has the assumed bulk-plus-surface measure decomposition
and the regular metric permits these contractions. The inequality then
excludes r^4 surface concentration. Since every stress component is
bounded by C(1+r^4+mu) for bounded rapidity, none has a surface measure.

No upper bound on r is used in that restricted conclusion. It is replaced
by finite stress-measure compactness, uniform slice control, bounded
rapidity and strong trace/coarea assumptions. Null-clock degeneration,
unbounded boosts, intermittent cap events, singular metric products, and
nonmeasure or unidentified bulk limits remain outside the result.

Independent delegated audit of SINGULAR_STRESS_ROUTE.md, 2026-11-06.
No outgoing solution or uniqueness principle is constructed.
