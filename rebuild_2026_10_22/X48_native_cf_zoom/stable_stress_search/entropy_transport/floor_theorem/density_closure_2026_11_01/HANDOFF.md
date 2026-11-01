# Open continuation after conditional density/collar closure

Checkpoint **X48-DEN-2026-11-01-A**; exact target and ancestry:
[TARGET.md](TARGET.md). Current proof and review inventory:
[README.md](README.md), [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md),
[PROVENANCE.md](PROVENANCE.md), [checks.json](checks.json).
No physical integration or external job was launched in this continuation.

## What changed mathematically

The complete actual conditional first-energy theorem is now available.
The midpoint convex gap cancels the density/velocity cross term exactly,
with positive singular growth at most `1/(16s)`. Weighted relative entropy
and a one-sided K-gradient energy absorb the full mechanical memory cost
even when some heat gates close. Cold fixed-N traces legitimately launch
the N-independent inequality. Two explicit material collars give inner
`Y<=Cs^5`, hence weighted velocity-error square `<=Cs^6`.

The earlier large-constant singular Gronwall problem is resolved for this
energy. Repeating absolute local-work estimates or trying to force a
positive smooth state-only local metric would discard the new cancellation.
The exact-law source hashes and reviewed notes must remain pinned.

## First unresolved implication

Let `f=S-S_d`. The conditional first energy gives
`||f/s^2||_(L2(V phi))<=Cs^3`. Actual constitutive divided differences give

\[
 \zeta'+a_i(s)\zeta=f/\nu_i-b_i(s)(K-K_d),\qquad
 a_*/s\le a_i(s)\le a^*/s,\quad |b_i(s)|\le C.
\]

Therefore a uniform actual pointwise estimate
`||f/s^2||_infinity<=Cs^theta`, theta>0, would imply
`||x-x_d||_infinity<=C(s^theta+s^3)`. This exact reduction is in
[pointwise_continuation.md](pointwise_continuation.md).

Its attempted all-p stress argument reaches the explicit heat flux

\[
 \sum_eL_e\Delta(\phi M_p),\qquad
 M_p=\alpha|f|^{p-2}f-\frac\beta p|f|^p,
\]

including the weight derivative. The coefficient remainder is

\[
 \overline{|f|^{p-2}f}\,\Delta\alpha
 -\frac1p\overline{|f|^p}\,\Delta\beta.
\]

The next discriminating task is an actual coupled level-set or all-p
estimate handling these terms, or a different actual pointwise mechanism.
A scalar Moser estimate or the earlier homogeneous semigroup does not
establish this implication without that transfer. The successful p=2
energy does not itself prove arbitrary-p absorption. This continuation
stops at that precise unresolved estimate, rather than a theorem claiming
it holds or fails.

There is a second logical obligation even if this smoothing succeeds:
the tight provisional envelope must cover a prefix and its collars on the
same interval. Improving only the inner cutoff does not improve the
bootstrap at its outer edge. An exterior bound, global weighted estimate,
or other coverage argument remains necessary. Both obligations stay open;
they are not declared impossible or exhausted.

## Surviving alternative and scope restrictions

The boundary route has an actual N-independent bound on summed cell-volume
variation, conditional only on a one-sided prefix compression cap plus
energy, and a fixed good cut with controlled adjacent capacities. Its next
unproved step is a separated moving-graph Poisson-kernel estimate or an
estimate tailored to the actual constitutive adverse-stress history.
Two good capacities are not a whole controlled collar. The auxiliary
capacity-inflation counterexample violates actual energy; it does not
refute the specified IVP.

No new finite collapse sample is proposed as evidence for all N. A sample
would be useful only for distinguishing a concrete remaining mechanism.
The original seeding and all-time floor theorem remain conditional until
the actual common compression interval, or another sufficient actual
uniform seeding statement, is proved.
