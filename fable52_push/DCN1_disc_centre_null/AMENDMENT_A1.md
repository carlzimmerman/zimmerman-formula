# DCN1 AMENDMENT A1 (post hoc; committed alone, after KA4's first run and before KA5 or any P1 / P2 local number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Criteria d603f1703c.

## What was seen first

- **Run before this amendment:** Part A (dcn1_symbol.py: PASS), KA1 at R4-R6 (SCS3's flagged rows reproduced, relative 0),
  KA2 (SCS2's 32 isolated R1 rows, relative 0), the variant-C global backgrounds (BC) and the P2 global maps (P2G, running),
  and **KA4** (the uniform sphere, both geometries).
- **KA4 fails as frozen.** Route L's Q = max Gamma_loc^2 converges, but to the wrong value:
  - P1 geometry, N_R 48-243: -3.415, -3.370, -3.336, -3.309, -3.288 (1e-29 s^-2);
  - P2 geometry: -3.490, -3.432, -3.387, -3.350, -3.321;
  - exact sup -5.331 (= -(5/3) 4 pi G rho_0, the null limit). Ratio 0.62-0.65, against the frozen 2 %.
  - Q sits on the cell next to the null at every resolution.
- **Why (diagnostic, scratchpad, reported).** Putting the exact Phi through the same route-L operator, the error at the
  first cells is 0.45 (4 pi G rho_0 units) for s < 2h, then 0.057, 0.015, 0.004 for s in [2,4], [4,8], [8,16] h: the same
  at every resolution. The null is self-similar (Part A2: D.P ~ s^-1/2, u ~ s^1/2), so the cell at distance k h sees the
  same relative discretisation error at every h. The error is bounded and resolution-independent: it neither vanishes
  nor grows. The solved solution adds a slowly converging error (0.15-0.45 at s ~ 0.1-0.3 L).
- **A slip found in the M2 code:** the spike was scaled (48/N_R)^2 instead of the frozen (h_0/h)^2 = (N_R/48)^2. No M2
  value had been graded. The code is corrected to the frozen formula.

## The amendment

1. **KA4 and KA5 pass iff** Q converges by the frozen rule, Q_inf has the sign of the exact sup over the analysis region,
   and 0.5 <= Q_inf / sup <= 2. This is a factor-2 magnitude bracket, set by the measured resolution-independent null-cell
   error. KA4 also passes if the rule calls Q Converged and the frozen 2 % fails only on magnitude: the frozen grading is
   reported first and fails.
2. **A rate graded BOUNDED is reported with the same factor-2 bracket.** Reported beside it, not graded:
   - Q_8, the maximum over cells with s >= 8 h (where the exact-Phi operator error is below 0.4 %);
   - the identity's Q_id.
3. Labels, the rule and every other known answer are unchanged. The frozen reading comes first in RESULT.md: KA4 fails, so
   the lane is NO VERDICT as frozen. The A1 reading follows.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
