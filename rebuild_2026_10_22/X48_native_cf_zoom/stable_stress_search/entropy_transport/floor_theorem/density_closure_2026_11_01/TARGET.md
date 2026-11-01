# X48 density and collar continuation: target contract

Checkpoint **X48-DEN-2026-11-01-A**, descended from
**X48-NLC-2026-11-01-B**. The coordinator observed shared Git revision
`27a0d27db1c343e1752698da36aa300398214689` at this continuation's start.
Other work changes the shared HEAD concurrently; exact source hashes, rather
than a later HEAD, identify the unchanged model.

The user requests control of the remaining density-gradient and local/collar
terms uniformly in resolution, followed by closure of the actual compression
bootstrap and completion of the all-time entropy-floor theorem.

The original assertion remains exactly

\[
 \exists T>0\ \forall N\ge32\ \forall s\in[0,T]\quad
 x_i(t_a+s)\ge4\quad(1\le i\le\lceil N/4\rceil).
 \tag{UC}
\]

Here `x=-Vdot/V` is signed compression; on this interval it would equal the
positive compression `C`. The activation datum is the tested virgin sphere,
with common `t_a=0.5907973398405011` and
`x(t_a)=5.4145849604427`. Initial data, all material parameters, energy,
viscous stress, heater, heat gates, and luminosity are fixed as in the base.
No alternative initial datum or regularized law is an equivalent target.

A proof must propagate actual hypotheses on one common interval, cover the
origin and the last central-quarter cell, and justify every nonlinear
pointwise and collar implication. A conditional energy bound, fixed-N
continuity, a finite grid sample, or a leading-model smoothing estimate is
partial evidence only. A failed energy construction is not a counterexample
to (UC).

The already established source-driven seeding and prefix preservation
theorems turn (UC), for sufficiently small `T`, into the all-time floor

\[
 K_i(t)\ge\frac{64}{125}T^3(1-2T)>0
 \quad (i/N\le1/20,\ t\ge t_a+T).
\]

Those downstream theorems are not new proof leaves in this continuation;
their status and sources remain in [../STATUS.md](../STATUS.md).

The continuation separates four obligations: the nonlinear gradient and
local-work estimates; their integration from the cold activation; an actual
pointwise estimate; and closure of the prefix/collar hypotheses on the same
interval. Success on the first two does not establish the last two.
