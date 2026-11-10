# DCN1 AMENDMENT A2 (post hoc; committed alone, after A1, before any corrected local number or any P1 / P2 local number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Criteria d603f1703c; A1 0a6e46fb52.

## What was seen first

- **After A1, KA5 ran once** (manufactured saddle). Its Q converged to 3.52e-30 s^-2 against an exact sup of 1.79e-30. The
  maximum sat at the edge of the analysis region (s = 0.49 L), far from the null, and the identity Q_id agreed with route
  L there. So the solved field itself was wrong, not the rate operator.
- **Diagnostic (scratchpad):** the exact sphere potential leaves a residual of 855 (relative) in the system as solved, and
  0.023 with the Dirichlet term's sign flipped. The solved field differs from the exact one by twice the potential's range.
- **The cause: a sign slip in dcn1_local.py's solve().** The Dirichlet faces' contribution entered the right-hand side as
  src - radd where it should be src + radd, so the solve imposed -Phi_b on the boundary. diagnostics() used the correct
  sign, so every D.P and rate was computed correctly, but on the wrong field.
- **So the KA4 failure that A1 answers came from this slip, not from the scale-invariant null error A1 describes.** A1's
  exact-Phi diagnostic (the operator's error at the first cells: 0.45, 0.057, 0.015, 0.004 for s in [0,2], [2,4], [4,8],
  [8,16] h) is unaffected: it never called solve().

## The amendment

1. solve() uses src + radd. Nothing else in the solver changes.
2. KA4 and KA5 rerun with the corrected solver. They are graded **first by the frozen criteria** (2 % and 5 %). If both
   pass, A1's factor-2 bracket is not used for them, and a BOUNDED rate carries the rule's E only. If either fails as
   frozen, A1's reading applies as written, and that is disclosed.
3. The buggy KA4 / KA5 outputs are kept in the scratchpad, not the repo. Their numbers are quoted here and nowhere graded.
4. P1 and P2 run only after the corrected KA4 and KA5.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
