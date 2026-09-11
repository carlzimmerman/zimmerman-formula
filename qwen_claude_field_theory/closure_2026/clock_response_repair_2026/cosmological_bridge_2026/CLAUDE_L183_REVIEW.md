# Bounded review of the new L183 CLASS experiment

Reviewed source/output at 9b9974e691e87e7ca3b69d5558253d5a691c3e0d,
including computation commit 8b5f0a7cc. No L183 files were edited.
The patched experiment was read, not rerun here. A separate stock CLASS
comparator was run and its manifest is included in this package.

## Useful advance

L183 modifies species evolution during integration, not merely final
\(C_\ell\). Its kernel-off Newtonian and synchronous runs agree on the
recorded peak summaries. Its smooth-fluid comparison is a useful test case.
The code documents the RMS envelope, cap and sub-horizon/redshift switches.

## Load-bearing limitation: incompatible metric derivative

Source: fable_independent_2026/L183_class_mond_kernel/apply_mond_kernel_patch.py,
lines 26–45 at the reviewed commit. The patch declares/evaluates
\[
\phi_{\rm eff}=\nu(\tau,k)\phi_N,\qquad
\phi'_{\rm supplied}=\nu(\tau,k)\phi'_N,
\]
and divides stored \(\phi_N\) evolution by \(\nu\) after rescaling the
metric derivative. But
\[
(\nu\phi_N)'=\nu\phi'_N+\nu'\phi_N.
\]
The last term is absent. It is generally nonzero because the kernel depends
on the evolving envelope, scale factor and switches. The source replacement
also excludes the derivative-array entries, leaving derivative-source paths
inconsistent with the rescaled potential.

Matching kernel-off GR peaks does not repair this: when \(\nu=1\), the
discrepancy vanishes. No action-derived compensating stress/current or
constraint-preservation identity establishes an alternative consistent
interpretation. Finite-time switches also require transition treatment.

## Scope of the fluid and comparison

Source: fable_independent_2026/L183_class_kernel_recombination.py,
lines 9–15, 21–30, 45–52.
The no-CDM proxy uses \(w_0=-10^{-4},c_s^2=1,\Omega_{\rm fld}=0.12/h^2\),
plus residual \(\omega_{\rm cdm}=10^{-6}\). That is not the stress/current
response of the frozen \(P,W,\gamma\) clock derived here.

Both “stock synchronous” and kernel-off Newtonian runs import the same
patched module. Their agreement is a useful gauge control, not a separate
unpatched-binary comparison over the full spectrum. This package's
gr_reference.py uses the existing stock installation.

The low-multipole criterion mixes the smooth-fluid baseline discrepancy with
the incremental kernel effect. In stored L183 output, at \(\ell=60\), the
no-kernel proxy already has \(D_\ell/D_\ell^{\Lambda{\rm CDM}}=7.11\);
its kernel-on counterpart has 7.26. That incremental change is about 2%,
not a sevenfold kernel-caused increase. Larger changes elsewhere remain
properties of the implemented proxy.

## Defensible conclusion

The output describes this envelope-based, capped, time-switched
metric/source prescription. It does **not** falsify every peculiar-field
MOND theory, establish a Planck likelihood exclusion for the frozen clock,
or determine whether its dust behaves correctly. Conversely, this limitation
is not positive CMB evidence for our action.

The next test must use derived stress/current/clock constraints and ordinary
matter equations together, validate Ward identities, then couple to CLASS.
Changing only one metric equation or refitting a background does not
complete that test.
