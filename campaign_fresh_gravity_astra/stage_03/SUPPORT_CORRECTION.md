# Additive correction to AFG-005 / AFG-007 necessity statements

The independent proof lane identified a missing support qualification. Earlier
evidence is retained unchanged; this note supersedes the affected unrestricted
necessity wording in `stage_02/DERIVATIONS.md`.

## Correct statement

With alpha=P^T l4 and beta=P^T l2, the exact correction error is

    6 sum_i I_i (alpha_i s_i²-beta_i) u_i².

Thus, for **every independently variable nonnegative source velocity square**,
the necessary and sufficient condition is

    diag(I) [s² alpha-P^T l2] = 0.

The stronger full-vector equation P^T l2=s² alpha is sufficient, and becomes
necessary after deleting zero-intensity source columns or assuming I_i>0
throughout. Zero-emission source cells cannot constrain a measured spectrum.

Counterexample: P=(1,1), I=(1,0), s²=(1/25,4/25), l4=1, l2=1/25. The old full
equation has residual (0,3/25), but its intensity-weighted residual is zero,
so the corrected moment is exact for every emitting-source velocity.

Similarly, for x=Iu², necessity in the linear-estimator condition D^T h=0 is
over the active columns if x ranges over physically supported vectors. The
unrestricted equation remains correct for arbitrary formal x in the full
vector space, which is a stronger nuisance-cancellation problem. Restricting
to active source columns can admit estimators rejected by that larger problem.

There is a further quantifier distinction: if circular kinematics and a known
zero projection q_i=0 force u_i²=0, that source provides no unknown second-moment
contribution either. More generally, any imposed dynamical relation can reduce
the allowable latent space. The corrected iff above deliberately concerns
arbitrary supported velocity squares; it is not a necessity claim for every
restricted physical model. For such a model one must use its actual admissible
latent space.

## Impact

The stored synthetic disk has I_i>0 and q_i>0 at every grid point. Its numerical
recoveries, noise calculations and coarsening example are unchanged. The
positive-weight RAR inversion and algebraic moment identities survive. The
common-width calibration obstruction survives on the active unknown-velocity
support if every active width is positive.

The correction matters for using the proposed method on masked real data or
sources with exactly zero emission/projection. It is retained as a genuine
theorem-scope correction, not hidden as a harmless typographical change.
