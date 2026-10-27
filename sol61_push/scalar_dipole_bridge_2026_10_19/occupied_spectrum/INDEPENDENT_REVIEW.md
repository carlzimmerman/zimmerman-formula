# Coordinator review of the occupied-spectrum algebra

The coordinator independently rederived the following from the canonical
vertex and the displayed definitions, and communicated the result on
2026-10-19 before this lane's closeout:

- `v_p=g/(omega_p sqrt(2MV))` for each unordered nonzero pair;
- `J_H(E)=g^2 beta(E)/(16pi^2 M)` and its on-shell normalization;
- `f_Phi(p)=16pi^2 n_X rho_s(E-2m)/(p E)`;
- the finite-production-energy condition
  `U_gap=2 integral Delta w(Delta) dDelta`, conditional on an actually
  occupied excitation whose energy is `Omega=2dDelta`;
- the retained NR contact Schur formula
  `Sigma=gamma^2 L/(1-U L)` and its positive threshold detuning under
  `U delta>gamma^2`.

The coordinator explicitly required that `delta` in the last statement be
the specified coefficient of the retained finite-regulator Hamiltonian,
rather than a physical pole detuning after additional mass counterterms.
That restriction has been incorporated into the note. The reviewer did not
assert that the formal UV tail is a full relativistic occupation prediction,
that thermalization occurs, or that a local gravitational dipole exists.

Final integration scope correction: the contact positivity/no-zero-threshold
claim is restricted to the displayed flat-space source/pair/contact block,
which omits Newtonian gravitational pair binding. It is not a no-bound-state
claim about the full gravitating model. Gravitational levels below `2m`
would require their own pair resolvent and source-production overlaps.

This is an independent algebra review within the same collaborative task.
The smooth-cutoff numerical implementation, primary-source extraction, and
thermal asymptotic derivations otherwise retain this lane's self-review
label. The independent parent sum-rule review is recorded separately in
`SUM_RULE_REVIEW.md` with the precise reviewed hashes.
