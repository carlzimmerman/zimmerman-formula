# Density and pressure do not determine a release lifetime

Coordinator analytic result. This addresses a precise missing input in a
rate prediction, not the existence of a universal bath or the stationarity
of every distribution below. The actual collision matrix element and
threshold are derived in `collisions/RESULT.md`.

## 1. The threshold-bearing rate functional

Let one daughter occupy a normalized gravitational orbital of energy
`epsilon_b=-B`, `B>0`. In the existing quartic channel an incident free
daughter of energy `E>=0` can release it into two continuum daughters
only if

\[
 E-B=E_p+E_q\ge0.                                    \tag{1}
\]

The host is static, energies share its continuum zero, and host recoil
or excitations are absent in this control. Other channels need their
own thresholds. Let `K(E)>=0` be the inclusive release kernel for this
actual matrix element, averaged over specified incoming angular states
and unoccupied outgoing modes. It follows that `K(E)=0` for `E<B`.
Assume `K(E)>0` on some accessible interval above `B`; a vanishing
orbital overlap or a selection rule would instead close this channel.

In the dilute weak-coupling, fixed-reservoir loss limit, if `F(E)dE` is
the incoming number density in the specified local or asymptotic energy
measure, the loss hazard has the linear form

\[
 \Gamma[F]=\int_0^\infty F(E)K(E)\,dE.                \tag{2}
\]

All flux, normalization, distorted-wave factors and the one fixed host
geometry belong to `K`. Equation (2) is not a new fitted rate coefficient.
Final-state Bose occupation, other channels, bath evolution, recapture
and correlations alter the kinetic functional when they matter.

## 2. An exact same-moments discriminator

Fix `n>0` and `0<E_0<B`. In an energy-diagonal reservoir control consider

\[
 F_A(E)=n\delta(E-E_0),
\]

and choose `0<E_l<E_0<B<E_h` with positive release kernel at `E_h`.
Define

\[
 w={E_0-E_l\over E_h-E_l}\in(0,1),\qquad
 F_B(E)=n[(1-w)\delta(E-E_l)+w\delta(E-E_h)].           \tag{3}
\]

Both distributions are positive and have exactly the same number and
mean energy:

\[
 \int F_A=\int F_B=n,\qquad
 \int E F_A=\int E F_B=nE_0.
\]

For isotropic asymptotic incoming velocities they also have zero mean
momentum and the same incoming kinetic pressure `2nE_0/3`. Their hazards
are different:

\[
 \boxed{\Gamma[F_A]=0,\qquad
 \Gamma[F_B]=nwK(E_h)>0.}                             \tag{4}
\]

For smooth distributions replace each delta by a normalized compact
energy bump with the indicated mean, with the low bumps supported below
`B` and the high bump on an interval where `K>0`. The same weight `w`
preserves both moments exactly. The zero/positive distinction survives.

This is a reservoir or instantaneous incoming-data example. It does not
assert two complete self-consistent stationary galaxy solutions with
identical local profiles. In a nonuniform host the energy measure,
orbital density of states, local velocity moments and flux are distinct;
they must be transformed consistently rather than silently identified.
The exact counterexample applies already in the simpler incoming
reservoir control, so number and one kinetic moment alone cannot fix a
release lifetime there. Additional frozen distribution assumptions could
fix it, but must actually be supplied by the physical model.

## 3. Interpret a lifetime only after checking the state

In the same loss-only Markov limit, a particle loaded at time zero has

\[
 P_{\rm surv}(T)=\exp[-\int_0^T\Gamma[F_t]dt].          \tag{5}
\]

Retention at least `r`, `0<r<1`, requires
`integral_0^T Gamma[F_t]dt <= -ln r`. This is a transparent criterion
in the derived kernel and actual bath. It supplies no numerical age
without that state. If capture remains on, occupation probability and
the contrast between two preparations follow the two-way kinetics
instead of (5); `cubic/RESULT.md` derives that separate test.

An empty reservoir after all ejecta leave gives no collision-induced
loss. A high-energy incoming tail can reopen release at the same total
number and mean incoming energy. Energy created by capture itself must
be included in the reservoir/transport accounting; prescribing a
permanently cold bath would assume the needed heat removal.

This is why a collisionless pressure estimate, a positive static energy
barrier, or an arbitrarily assigned temperature cannot establish an
actual storage time. Existing couplings determine the kernel in a
specified host; the incoming state and its evolution are additional
physical data. No new fitted parameter, external source or numerical
experiment is used in (1)-(5).

Review provenance: coordinator analytic self-review and separately scoped
reconstruction in `audit/RESULT.md`. Scope is the stated threshold-bearing
linear kinetic control, not all many-body channels or all orders of scattering.
