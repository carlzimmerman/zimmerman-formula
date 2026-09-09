# IC24 numerical review and next construction

This post-run review supplements IC24_INTEGRATED_POTENTIAL.md without changing
the input bytes pinned in the computation manifests. It is self-review,
not independent peer review. Full objective remains OPEN.

## Results read from the actual strict run

- All seven scoped checks are true; scientific child exit2, runner exit1.
- Coarse/fine first-event Q: .04860087249690356 / .048600872496904625.
  These agree numerically; agreement is not an interval-certified enclosure.
- Conserved-charge maximum absolute drift: 2.812e-15 / 6.111e-15.
- Actual auxiliary ranks are4 at the specified k²=0,1,10000 samples.
- All sampled three-field kinetic eigenvalues are positive.

IMPORTANT: there is NO full stability PASS. At k²=1, instantaneous positive
real roots include .77662994 (Q=0), 1.42537532 (Q=.005), 5.57229935 (Q=.02),
and 17.86005579 (Q=.04), in the normalized coordinate-time convention of the
script. Nonautonomous growth requires integrating the perturbation system;
it cannot be certified benign from the principal symbol. At Q=.04 some
oscillatory roots also have positive real parts. Every root is retained.

The initial reconstructed D''' is about 4.258427e6, falling to 13483.873 at
Q=.04. A large coordinate-dependent coefficient alone does not prove strong
coupling, but the interaction scale after canonical normalization is an
unavoidable check. Merely fixing the lapse constraint or its principal speed
does not establish the user's stability requirements.

## Next: constrained two-function reconstruction

Keep the complete goal. The missing step is not another isolated healthy
point. Let A(S) evolve together with D(S). At fixed (S,q,z,Q,A), denote
alpha=A'. The auxiliary equations algebraically determine D and D'; after
choosing negative M the principal clock diagonal is quadratic in alpha.
An exploratory initial-point numerical evaluation found

    c_g²(alpha) ~= 2.026519572714 alpha²
                   -6.810002734305 alpha +5.175709425133.

At c_g²=.3 the smaller real root is alpha~1.034317797589 and gives
Sdot~.002853675513, with the actual lapse Schur still -3. This is a local
design diagnostic, not a derived global coefficient. A subsequent INLINE
background-only trial toward Q=.1, keeping that target fixed, terminated
with 'No real derivative root'. It is not a certified fold location or a
no-go: the trial did not bracket the event and did not reconstruct the true
A''/D'' action jets. Do not promote it into an integrated-theory result.

The next reproducible implementation must:

1. Derive/check the quadratic dependence and its discriminant, selecting a
   continuously tracked root; treat linear/degenerate cases explicitly.
2. Use the actual combined matter cone inequalities, not a fixed diagonal
   target that may leave the feasible range. Investigate whether a varying
   negative lapse Schur can preserve a real causal root.
3. Integrate A_Q=alpha S_Q; derive A''=alpha_dot/Sdot and the corresponding
   D'' so BOTH coefficient-integrability identities are satisfied. Reject
   unhandled S turning points or multivalued coefficients.
4. Re-vary the frozen S-only functions, compute all perturbation roots and
   integrate their nonautonomous evolution. Enforce growth/interaction-scale
   controls alongside the high-frequency condition.
5. Test other matter amplitudes with the SAME constructed functions, then
   address global static matching, full nonlinear Dirac, PPN and empirical
   constraints. Reconstructing a separate theory for each matter source is
   not an acceptable universal theory.

The decisive advance here is local action-function integrability plus actual
evolution beyond the previous crossing. Neither that advance nor this next
route changes the remaining requirements or warrants a complete-theory claim.
