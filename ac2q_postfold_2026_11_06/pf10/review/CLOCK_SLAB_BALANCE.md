# Clock-slab balance without assuming finite scalar-current variation

**Verdict: the exact balance yields a conditional exclusion and a necessary
nonnegative cumulative-feed condition. It does not derive vanishing layer
charge from finite stress and initially absent charge alone.** Independently
matched outer side fluxes would close the exclusion without finite J;
that matching is an extra condition, not a conclusion of this argument.

Independent delegated audit, 2026-11-06. Scope: the specified current in
`COMBINED_CURRENT_EXCLUSION.md`, retaining its native equations, regular
metric, compact clock/cap and trace controls, but removing its finite-J
total-variation assumption. No existing proof file is changed.

## Exact moving-domain identity

Write tau=phi and use x as the second coordinate. A future timelike clock
has phi_t>0, so this change is valid at every smooth stage, even if its
Jacobian is not uniformly bounded above. The transformed current density
and explicit source are

    Jtilde^tau=(J^t phi_t+J^x phi_x)/phi_t,
    Jtilde^x=J^x/phi_t,
    Stilde=S/phi_t,    S=partial_a J^a=-E(V_phi+W_phi).

Let the two timelike strip sides be x=X_-(tau), x=X_+(tau), with regular
transverse intersections with clock levels. Define

    Q_epsilon(tau)=integral_[X_-,X_+] Jtilde^tau dx,
    F_+/-=Jtilde^x-X_+/-'(tau) Jtilde^tau on the respective side.

Reynolds transport and the exact scalar equation give

    Q_epsilon'(tau)=F_-(tau)-F_+(tau)
                    +integral_[X_-,X_+] Stilde dx.

For a side expressed in the original chart as x=X(t), this flux is

    F=(J^x-Xdot J^t)/(phi_t+Xdot phi_x).

The denominator is the derivative of the clock along the side. Its
regular positive limiting trace is required for passage to the limiting
side flux; regular timelike geometry alone does not bound arbitrary
scalar-gradient traces. The signs above mean positive F_- feeds the
strip from the left and positive F_+ leaves on the right.

Using d ell=exp(2 alpha) r dx/phi_t, the charge is exactly

    Q_epsilon(tau)=integral_clock_crossing exp(2 beta)
                     r(3-2Ar+2 gamma r^2) d ell.

The integrand is bounded below by gamma r^3-C when A is bounded.
The clock crossing has proper length O(epsilon), so Q_epsilon>=-C epsilon.
This lower bound is not an assumed uniform upper slice-charge bound.

The source on a slice obeys

    integral |Stilde| dx <= C integral r^-1 d ell <= C epsilon,

using bounded explicit source per volume and r>=r_min. These bounds
are uniform on a fixed compact clock interval under the declared
transversality and crossing controls.

## The topological piece does not invalidate the charge formula

Its contribution to Q is

    Q_top=-integral A dPi

along the clock slice. The earlier positive-variation estimate and strong
signed endpoint matching give total variation of Pi along that crossing
o(1), uniformly in the clock label. Bounded A therefore gives Q_top=o(1).
Equivalently one can integrate by parts using bounded Pi and
eA=W_P/r, whose crossing variation is O(epsilon).

This does not control the two coordinate derivatives of Pi in spacetime.
Nor does vanishing spacetime absolute mass of J_base imply vanishing
Q_base: the charge contracts with the potentially unbounded clock normal
and restricts to a moving clock slice. Such slice/product convergence
must be proved by this balance, not borrowed from the base-current
spacetime estimate.

## Passage to a charge balance: actual additional inputs

Assume the side current traces F_epsilon,+/- converge in L1 on the compact
clock interval to regular F_+/-, and the initial slice charge converges
to a finite q0. In particular "initially absent layer" must mean
Q_epsilon(tau0)->0 when q0=0; absence of a spacetime current surface
measure alone does not imply this initial slice statement. The integral
balance then gives uniform convergence of Q_epsilon to

    q(tau)=q0+integral_[tau0,tau] (F_-(s)-F_+(s)) ds,
    q(tau)>=0.

Uniform bounded side fluxes make q Lipschitz; L1 convergence is enough
for the displayed uniform convergence and absolute continuity. No finite
measure bound on the full interior current has been used.

Thus an initially empty layer must have nonnegative cumulative net feed
at every later clock level:

    integral_[tau0,tau](F_--F_+) ds >=0.

A strictly negative cumulative feed is incompatible with such a smooth
layer sequence. Positive inward mismatch can create q>0. For example a
constant net feed b>0 gives q=b(tau-tau0), which is fully consistent with
this balance and its positivity. This is an allowed balance, not a
constructed native solution.

## Relation to the stress concentration

Coarea turns the integrated charge into

    integral Q_epsilon d tau
      =integral_layer r^2(3-2Ar+2 gamma r^2) dVol.

Finite transverse stress supplies a uniform r^4 spacetime bound. Since
the layer volume vanishes and A is bounded, Holder estimates give
vanishing integrals of r^3 and r^2. Hence the possible r^4 surface measure,
pushed to the clock label, is exactly

    q(tau) d tau/(2 gamma).

This is a concrete necessary scalar balance for any proposed stress-only
combined concentration. The constitutive tensor and no-dipole condition
alone do not supply this evolving nonnegative charge or its outer fluxes.

If q0=0 and F_-=F_+ independently throughout the interval, then q=0.
The lower bound on Q, integrated in tau, gives
integral_layer r^4 dVol->0. Together with the previously proved vanishing
multiplier mass, regular trace contractions, and normal no-dipole stress
conservation, the base-trace argument excludes all matter surface stress
there. This conditional conclusion does not assume finite total variation
of J. More generally nonpositive cumulative net feed at every tau is
sufficient: q0=0 and q>=0 force that cumulative feed and q both to vanish
for any existing limiting sequence. Strict negativity at even one tau
instead excludes the sequence outright. Exact flux matching is a stronger
sufficient condition than this one-sided cumulative-feed criterion.

Flux matching cannot be deduced here from div J by declaring there is no
surface current: no such current-measure conclusion is available after
removing that hypothesis. Inferring it would be circular. A finite outer
flux mismatch can instead feed the charge/product defect above despite
the vanishing spacetime base-current mass.

## Remaining obligation

The route supplies either an exclusion under independently matched side
fluxes or a necessary nonnegative charge-feeding law for a candidate
layer. It does not select the outgoing outer state or force its current
flux to match the incoming flux. Deriving that matching, excluding every
positive-feed solution by additional native equations, or constructing
a compatible fed layer remains separate work. No universal singular
nonexistence, current-variation estimate, or same-data uniqueness follows.
