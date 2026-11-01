# X48: conditional nonlinear energy closure

Checkpoint **X48-DEN-2026-11-01-A**. The original common-time
central-quarter compression bound remains **unproved**. The target and its
quantifiers are fixed in [TARGET.md](TARGET.md); live state is in
[STATUS.md](STATUS.md).

This continuation resolves the named density-gradient, local-reaction,
and collar costs in a complete conditional first-energy estimate for the
unchanged actual equations. It also justifies integration from cold
activation; zero activation energy alone is not the justification.

Let `s=t-t_a`, `v=x-x_d`, and `z=log rho`, using the homogeneous heated
reference. Assume the actual tight envelope

\[
 |v_i(u)|\le1/32\quad
 (i\le\lceil N/2\rceil,\ 0<u\le s\le10^{-3}).
\]

The reference and prefix then remain on the active branch `2<x<=8`.
Use the three fixed, ceiling-correct material cutoffs in Section 7 of
[gradient_symmetrizer.md](gradient_symmetrizer.md). Define

\[
 F_z=\kappa,\qquad
 U(z_l,z_r)=2\{F(z_l)+F(z_r)-2F((z_l+z_r)/2)\}.
\]

The combined energy is the sum of the velocity term
`sum V phi v^2/(2s)`, the midpoint density-gradient term
`(x_d-2) sum a eta U/s`, the small density term
`sum V phi (z-z_d)^2/(32s^3)`, a fixed multiple of
`s^-6 sum dm W phi (K-K_d)^2/2`, and the negative-memory-gradient
energy `sum a eta ((K_l-K_r)^-)^2/2`.

The exact identities give, for constants independent of N,

\[
 Y'+c_1sD_\eta(v)+c_2s^{-6}\sum_e\eta_eL_e(K_l-K_r)
 \le\left\{\frac1{16s}+C(s^{-1/2}+1)\right\}Y
       +C_Ls^2E_{v,\mathrm{outer}}+C_Ls^4.
\]

All heat gates, both heaters, moving volumes, shear, and cutoff work are
retained. The midpoint identity cancels the principal nonlinear mechanical
cross term exactly. Outward flux dissipation controls positive K drops;
the one-sided gradient energy controls negative drops. A physical drop
threshold `q/d=s^3` supplies the required powers even on closed heat faces.

For each fixed N, the actual finite-dimensional activation trace satisfies
`Y=O_N(s)`. Thus `s^-1/16 Y -> 0` separately for every N. This suffices
to launch the uniform scalar inequality without a uniform trace constant.
The outer amplitude bound and two nested collars then give

\[
 Y_{\mathrm{outer}}\le Cs^2,\qquad
 Y_{\mathrm{inner}}\le Cs^5,\qquad
 \sum_iV_i\phi_{\mathrm{inner},i}(x_i-x_d)^2\le Cs^6.
\]

These are conditional, all-resolution conclusions on any interval where
the displayed actual prefix hypothesis holds. The interval in the hypothesis
has not been proved to persist uniformly in N. The energy conclusion alone
does not bound the maximum compression error at the origin or other cells.
Improving only the innermost region also does not improve the hypothesis at
the outer edge of its prefix.

## Proof and review map

| Record | Exact contribution |
| --- | --- |
| [gradient_symmetrizer.md](gradient_symmetrizer.md) | Midpoint convex gap, cancellation, explicit singular exponent `1/16`, full mechanical collar, combined estimate and cutoffs |
| [relative_entropy.md](relative_entropy.md) | Weighted relative K entropy, exact heat collar, time-dependent drop threshold, negative-gradient propagation, activation trace and collar integration |
| [flux_potential.md](flux_potential.md) | Earlier flux-potential defects; Sections 4–7 prove the nonlinear memory-gradient conversion and one-sided energy |
| [local_work.md](local_work.md) | Reference-subtracted local work, Hardy shear bound, coarse collar bounds; reaction chart and restricted local-metric obstruction |
| [boundary_transfer.md](boundary_transfer.md) | Energy-constrained total volume variation and a fixed cut with controlled adjacent capacities; actual Poisson-kernel estimate remains open |
| [pointwise_continuation.md](pointwise_continuation.md) | Actual constitutive reduction to a normalized-stress maximum bound; exact all-p heat defect, with the coupled iteration still open |
| [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md) | Exact reviewed scopes, hypotheses, reconstructed critical steps, hashes, and remaining gaps |
| [PROVENANCE.md](PROVENANCE.md) | Unchanged physical sources and verification record |

The next exact proof obligation and surviving alternatives are in
[HANDOFF.md](HANDOFF.md). The normalized-stress reduction does not presume
that a scalar smoothing theorem applies to the actual coupled equation.

No new physical simulation or extrapolation is used. The conditional theorem
is stronger than the previous disconnected energy bounds, but does not
establish (UC) or the unconditional all-time entropy floor.
