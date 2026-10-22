# Author self-review (not independent acceptance)

The entire 418-line derivation was reviewed after its first completed draft.
The mathematical proofreading skill and its checklist were read. No external
sources or new stage39 coordinator/reviewer content were exposed.

Substantive direct checks:

- The exterior initial balls have gap r h and outer radius 3 R_i h/4;
  condition S B_dagger N^-1/2<r/2 preserves a nonempty endpoint
  neighborhood. Comparison uses actual bounded local characteristic paths.
- Differentiating gB-W gives g B_x+T k. This fixes minus tau p g/C
  and the plus T k/C Q exchange. Differentiating scale momentum fixes
  minus U in its stress and minus T k/C exchange. Full force cancels.
- Individual hydrostatic boundary stresses need not agree. Only their sum
  with cs^2 rho agrees. Thus the precise force excess contains rho g0.
- Two integrations of P'=-A and F'=A give I=I0+P0T-int F.
  Positivity makes I<M0D_N strict, so a non-strict transfer threshold
  already contradicts existence through the test time.
- The exact polynomial integrals were rederived by antiderivatives, not
  executed in code. The error estimates use Taylor remainder H2 z^2/2;
  odd velocity-weighted integrals vanish. Delta0's linear-density term
  has the negative sign. The limiting horizon coefficient is 15/8.
- Energy retains n phi and the internal energy lower bound. The field
  scale bound uses a fixed endpoint and Cauchy-Schwarz. W>=g^2/4-a^2/4
  holds in the stated positive chart. The field momentum bound is
  unconditional on transfer within an existing branch but misses its
  requested scale by one power of N. No closure is asserted.
- The zero-velocity hydrostatic solution satisfies every separate balance
  and cannot satisfy the positive-momentum contradiction hypothesis.
- Physical momentum/energy units, both normalizations, separately frozen
  history and evolving protocol work are explicitly distinguished.

Proofreading:
- Scope: all of DERIVATION.md and this run's short accompanying prose.
- Routine corrections: none needed after the completed draft.
- Mathematical-token proofreading changes: none.
- Cross references: equations (1)-(27) are sequential and references resolve.
- LaTeX build: not applicable; the requested artifact is a Markdown proof.
- Remaining mathematical issue: exactly the signed transfer budget (27),
  or equivalently (19), at O(N^-6), with a sufficiently small constant.

This self-review is not the independent result review required by the
framework. Hash validation certifies bytes, not mathematical correctness.
