# PF09 singular stress: positivity routes and their limits

Candidate extension of PF07 exclusions; not yet independently audited.
No unique singular continuation is asserted.

## 1. A cap-excursion cost that does not assume a uniform cap margin

Native full-switch transverse stress is
 Tperp = r²/2 - V + (Q-1-gamma r²)²/(2gamma) + P Wp-W.
The hold law is convex, W(0)=0, so P Wp-W>=0. Put
 Deff=(Q-1-gamma r²)/gamma=max(D,-r²).
Then pointwise
 Tperp+V >= r²/2+(gamma/2)Deff² >= (gamma/2)(D_+)².
This holds on and off branch. The native cap |P|<a0/Khold still applies,
but there need not be a fixed separation inside the layer.

On a regular clock slice, Pi=exp(2beta)P obeys ePi=exp(2beta)D.
For a layer of proper width epsilon and bounded metric weights,
 positive_variation(Pi) <= C sqrt(epsilon) [integral(D_+)² d ell]^(1/2).
Any interior cap excursion a fixed distance beyond both exterior endpoint
values requires positive variation bounded below: the excursion must either
rise from the left endpoint or return upward to the right endpoint.
Thus such an excursion costs integral(Tperp+V)d ell >= c/epsilon.
A uniform per-clock-slice transverse-stress bound excludes it for small epsilon.
This derives cap separation from that stronger compactness assumption.

A spacetime finite-stress-measure bound alone does NOT provide the required
uniform slice bound. Intermittent excursions over time sets of size O(epsilon)
can retain finite spacetime cost. Dense short bursts can converge weakly to a
nonzero surface measure. The cost estimate does not eliminate that mechanism.
It also assumes regular clock-slice geometry and separated outer cap traces.

## 2. Candidate exclusion of invariant-clock blowup with bounded rapidity

Retain regular metric/frame, r>=r0>0, uniform cap separation, bounded unit
clock-frame n (rapidity), and anchored A. Allow r to be unbounded above.
The exact equation eA=Wp/r and bounded crossing length imply A bounded.
Assume strong matching Pi endpoints across shrinking layers, finite stress
measures with native bulk identification, and bounded integrated transverse
stress on clock slices. The latter gives positive Pi variation O(sqrt(epsilon))
by section1; endpoint matching then gives total negative variation o(1).
Consequently integral mu d ell<=integral D_- d ell=o(1) for the off-branch
multiplier mu=-(D+r²)>=0. Bounded n ensures its stress term -mu Q n_a n_b
has no surface mass (Q=1 wherever mu>0).

On shell T_ab=H h_ab+(r H_r-mu Q)n_a n_b.
With bounded A,P and cap margin,
 H=(gamma/2)r^4-A r^3+O(r²+1),
 r H_r=2gamma r^4-3A r^3+O(r²+1).
Thus H and rH_r are positive at large r and grow as r^4; any negative parts
are uniformly bounded and cannot contribute a layer measure. For a unit
spacelike normal N to a timelike interface,
 T_NN=H+(rH_r-mu Q)(n.N)².
The multiplier contribution has vanishing integral under bounded rapidity.
Therefore the singular part of T_NN dominates the nonnegative r^4 concentration.

If the limiting stress conservation law has no dipole source and the metric
connection remains bounded, its delta-prime coefficient requires N^a S_ab=0
for a surface stress S. In particular S_NN=0. Positivity then excludes r^4
concentration. All remaining native stress components are bounded by
C(1+r^4+mu) with bounded n,A,P, so none can have a surface measure.

This would remove the upper invariant-clock bound from a restricted no-stress
lemma, replacing it with finite-stress compactness, bounded rapidity and the
stated slice/trace controls. It does NOT remove clock degeneration r->0,
unbounded boosts, intermittent cap concentration, singular gravity, or failure
of finite-measure compactness/native bulk identification.

The normal no-dipole condition must be justified from the actual limiting
conservation law; it is not automatic for arbitrary distributional metrics.
The strong endpoint condition is required to exclude negative-divergence
multiplier mass. Neither follows merely from finite signed action.

## 3. Selection status

No construction here exhibits two native continuations of the same incoming
data, and no intrinsic singular admissibility law is obtained. Positivity
narrows controlled escape classes; it does not prove universal nonexistence.
Any extension claim must distinguish a required mathematical solution/admissibility
specification from a proved need for new physical fields or action terms.
