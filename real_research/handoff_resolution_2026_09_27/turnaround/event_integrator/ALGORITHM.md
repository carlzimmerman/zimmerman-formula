# Bracketed-event KDK audit — specified operator and limits

This copied no-cooling benchmark keeps the source enclosed-mass force, potential, softening and radial floor, constant spin0.25 assigned at turnaround, source phase sequence, sorted-neighbor pressure, cap, isotropic exact kick and one-daughter second-moment closure. It changes event timing. The pressure inequality is evaluated at every accepted step; an every-fifth-step cadence is a numerical sampling choice and is not retained as a physical waiting time. No event-time fit or pressure smoothing is added.

For an unaccepted KDK proposal h from (R,V), frozen current masses/J give

    R(h)=max[R+h(V+h A(R)/2), 1e-3],
    V(h)=V+h[A(R)+A(R(h))]/2.

The enclosed masses and forces are recomputed at each trial R(h). Candidate phase-event margins are V for the expanding and post-pericentre-outgoing phases, and -V for the infalling phase. Inactive/dead/phase-mixed shells receive infinite margin. Candidate pressure margin is P_cap-P_d for coherent unconverted dark shells. A nonnegative initial margin and negative trial-end margin bracket a detected event. No accepted state is advanced to the full endpoint before deciding whether to subdivide.

The locator bisects the interval until its width is <=1e-6 of the proposed step or1e-12 in source time units, at most40 bisections. It retains the event-side high state, advances only to that time, applies the unchanged source phase transitions and impulses, and refreshes forces before the next trial. It searches for the earliest crossing retained by this bracket procedure, not a proven globally earliest event if trial margins cross repeatedly. No interpolation across an accepted sign-changing step is used.

A preceding conversion can make another shell's pressure already exceed the cap. Such a right-limit event is applied without further time advance; the source's simultaneous batch firing rule is retained within each batch. A zero-time cascade can only convert the finite set of kind0 shells, since daughters never convert again. It is bounded additionally by the100,000 accepted-step limit and48-second per-run wall budget. Boundary cases that would demand a positive step below1e-12 are recorded as failures, not regularized. No cooling extension is claimed.

## Controls

The independent elementary controls use constant-acceleration KDK (turnaround at0.37), a separate smooth pressure-margin crossing at0.63, and no-trigger harmonic KDK against its analytic trajectory. At event tolerance1e-8, turnaround and pressure errors are4.77e-9 and2.68e-9; harmonic errors decrease by approximately4 on each timestep halving. Exact-kick retained-plus-escaped mass accounting is checked separately. Main passes6/6; deliberately placing events at the late endpoint fails exactly the four event-placement checks while retaining the two unrelated controls. These establish the elementary locator and integrator, not convergence of the nonsmooth shell system.

The full-driver benchmark begins with two N80 no-trigger runs, then matched N600/1000, eta.03/.015 and tiny-spectrum runs. These controls test actual mass accounting and reveal coarse-shell trajectory sensitivity even without any conversion. All full event records retain bracket widths, phase velocity residuals, pressure excess and zero-time cascade status. A tight time bracket alone is not a small pressure or phase residual.

## Exact remaining numerical/model obligations

1. Sorted enclosed masses and rank-neighbor pressure are nonsmooth when shells reorder. A margin can jump across zero, so bisection may localize a discontinuity without producing a zero residual. The pressure rule is retained rather than replaced by a new smoother constitutive rule.
2. Multiple crossings within an otherwise same-sign proposal can be missed. This is endpoint-bracketed event detection, not an exhaustive event-isolation theorem.
3. Neighbor exchange/shell sorting and the radial floor are not independently event-located. Their force and stress effects can affect the KDK trial map itself. Collisionless shell crossing should not silently be assigned an invented collision impulse.
4. The source's batch conversion and one-daughter closure are retained; they are not derived kinetic evolution. A post-event cascade convention is explicitly stated above, rather than concealed as a new fitted regularization.
5. No generic symplectic or energy-conservation claim is made after variable-step subdivisions, cosmological forcing, changing masses and escape. The smooth harmonic control does not establish order across the nonsmooth events.

This is a bounded candidate numerical improvement within the specified shell prescription. Remaining sensitivity may require a better-defined continuum stress/phase-space discretization as well as event treatment; the finite experiment does not identify one unique cure.

## Why a narrow pressure bracket need not have a small residual

This is already possible in the exact source estimator, without numerical roundoff. Let a neighbor window have fixed mass M, volume V, radial momentum sum S and radial second-moment sum Q. Replacing one equal-mass boundary neighbor of mass m and velocity u by another with velocity u_prime changes its pressure numerator Q-S²/M by

    delta = m(u_prime²-u²) - 2 S m(u_prime-u)/M - m²(u_prime-u)²/M.

At a radial rank exchange, the two boundary particles can have the same radius but different velocities, so this change need not vanish as their radial separation tends to zero. For example, a two-particle window with both old velocities0, replacing one by U, has M=2m and delta=mU²/2, hence a finite pressure jump mU²/(6V). Tangential moments provide another such term. Consequently the current stress functional has no continuous root across every threshold crossing. Event localization can identify the jump time and choose the declared event-side limit; it cannot manufacture the equation P=P_cap there. Smoothing or changing neighbor weights would change this finite-N stress rule and has deliberately not been invented.

Similarly, the thin-shell sorted enclosed force jumps when ranks exchange. The endpoint acceleration in the finite-h KDK trial makes trial velocity a piecewise function of h, so a phase-margin sign jump need not be a true zero of a continuous trial velocity. Independently localizing shell-rank exchanges, with a consistent crossing/force convention, is an additional numerical obligation; it is not covered by the three phase and pressure events implemented here.
