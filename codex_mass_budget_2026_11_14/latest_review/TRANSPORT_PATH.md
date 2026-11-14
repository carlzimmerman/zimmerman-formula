# A constructive charge-conserving path to a positive target profile

Checkpoint CTRANSPORT_XJ1_2026_11_14, a continuation of CJUMP_XJ1_2026_11_14.
This closes a kinematic continuity obligation. It is not a new physical
model, a new blind test, or a solution of the clock action.

## Statement and hypotheses

Let L,T>0 be fixed. Let C_R,C_E be absolutely continuous, nondecreasing
cumulative charge profiles on [0,L], with

    C_R(0)=C_E(0)=0,     C_R(L)=C_E(L)=T.

Assume C_R'(r)>0 almost everywhere for 0<r<L and C_E'(r)>=0. Piecewise
smooth profiles with finite one-sided density jumps are allowed. For a
uniform velocity bound on a chosen region additionally require

    B = ess sup |C_E-C_R|/C_R' < infinity

there. This bound is a real hypothesis; positivity of C_R' alone does not
guarantee it near a zero-density origin or other endpoint. Infinite target
mass, a time-varying total T, imposed baryon growth, or an accreting outer
boundary are outside this theorem.

For any continuously differentiable mixing schedule 0<=a(t)<1, define

    C(r,t) = (1-a)C_R(r) + a C_E(r),
    N(r,t) = partial_r C/(4 pi r^2),
    v(r,t) = -a_dot (C_E-C_R)/[(1-a)C_R'+a C_E'].

**Verdict: proved under the stated hypotheses.** The density is
nonnegative, its total charge is T, and it obeys the spherically symmetric
source-free continuity equation in the weak sense. Where C_R'>0 the
finite-time mixture has positive density and the displayed velocity is
well-defined. The charge flux through the origin and outer boundary is
zero. The path approaches the specified target when a(t) approaches 1.

## Proof, including interface and endpoint fluxes

Convex combination preserves monotonicity and the two endpoint values.
At every differentiability point,

    partial_t C + v partial_r C = a_dot(C_E-C_R)-a_dot(C_E-C_R)=0.

Thus the spherical current is

    4 pi r^2 j(r,t) = 4 pi r^2 N v = -a_dot(C_E-C_R).

Differentiating this identity with respect to r gives
partial_t N + r^-2 partial_r(r^2 N v)=0, distributionally as well as in
each smooth interval. C_E-C_R is continuous, so the current has matching
one-sided traces at a fixed density interface even if v jumps. No surface
charge is introduced. Both endpoint fluxes vanish because C_E-C_R is zero
at 0 and L. This is a condition on r^2 j at the origin, not an unjustified
assertion that the velocity itself must vanish there.

If the target has more enclosed charge than the reference at a radius,
the flow is inward for a_dot>0. If it has less, the flow is outward.
Unlike the static-interior matching ansatz, this interpolation allows the
interior itself to flow while it assembles. It does not assume the law's
profile is already stationary throughout the transition.

## Bounded schedule and a zero-density obstruction to naive schedules

Choose an arbitrary constant tau>0 and

    a(t)=1-exp(-t/tau),        t>=0.

Since a_dot=(1-a)/tau and C_E'>=0,

    |v| = (1-a)|C_E-C_R| / {tau[(1-a)C_R'+a C_E']}
         <= |C_E-C_R|/(tau C_R') <= B/tau.

This gives a bounded transport path on every region where B is finite.
It approaches C_E asymptotically. Where C_E'>0, v approaches zero; where
C_E'=0 and C_E-C_R is nonzero, v may approach a finite nonzero value while
the charge density and current approach zero. The latter is not a
derivation of a stationary clock in a vacuum region.

In contrast, a finite-time linear schedule a=t/tau has, at a target
zero-density point with C_E-C_R nonzero,

    v = -(C_E-C_R)/[(tau-t)C_R'],

which diverges as t approaches tau. More generally, reaching a=1 at finite
time cannot keep a_dot/(1-a) uniformly bounded: integrating a uniform
bound would leave 1-a positive. This excludes only such fixed convex
interpolations with a nonzero target-reference difference at a flat
target region. It is not a no-go for other transport paths or new physics.

The 27 degenerate z=0 k=2 XJ1 snapshots motivate stating this edge case
explicitly. The experiment does not claim they possess the theorem's
uniform velocity bound globally; that depends on their complete profile
derivatives and endpoint behavior.

## What has and has not been achieved

An explicit positive, globally charge-conserving kinematic path now exists
under clear hypotheses. Therefore the stationary-interface obstruction
alone cannot rule out all assembly paths. The construction supplies a
candidate density/current pair for a subsequent field-equation residual
test, rather than merely requesting an unspecified transport mechanism.

It does **not** satisfy QX17 by construction. Even in COL1's Newtonian
reduction, the chosen v must also obey the clock's force equation and its
relation to h and polarization. In the exact action, the total current
includes -lambda P/Q. No P, h, lapse, stress field, energy transfer,
entropy production, stability result or unique caustic selector has been
derived here. The arbitrary tau is a kinematic schedule parameter;
it is not a derived physical constant or settling time. The target is
approached only asymptotically by this schedule.

`check_junction.py` verifies the symbolic continuity identity, schedule
identity and bound decomposition. It also checks 36 exact rational traces
for C_R=r and C_E=min(2r,1), including both sides of the density jump and
the zero-density target region. For that example the exponential schedule
has bounded velocity while the linear schedule diverges at the cap.

This is new self-reviewed mathematics. It preserves the distinction
between the supplied mode-B target and an independently established
algebraic-law solution. No existing research label is changed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
