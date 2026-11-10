# SCS3 AMENDMENT A4 (post hoc, AFTER the first label pass on the frozen, A1 and A2 maps; committed alone, before any A4 number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**The frozen, A1 and A2 readings stay and are reported first, with KA3 failing in all three (below).** A4 adds a fourth
reading. It builds on A1 (axial) and A2 / A3 (in-plane) and changes only the following.

1. **The rule's "flat" clause is removed.** Section 3's "already flat" case (both differences within 2 % of Q_fine: Q_inf =
   Q_fine, E = max(|d1|, |d2|)) is dropped. A monotone sequence with |d2| < |d1| is always extrapolated; the oscillating,
   growing and order-range clauses and the 20 % line are unchanged; d2 = 0 gives Q_inf = Q_fine, E = |d1|.
2. **The region's inner radius is judged against the cell size.** It is the centre radius of a grid cell, so its sequence
   moves in steps of a cell. It is converged when its values on the finest three resolutions agree within two radial cells of
   the finest grid (|ln(r_i/r_j)| <= 2 dx_finest); Q_inf is the finest value and E the spread. The section-3 rule is not
   applied to it.
3. **One more axial resolution, R6 = (546, 273)** (base counts, ratio 1.5 continued). The rule runs on the finest three
   (R4-R6) with the multi-resolution error max(E, |Q_inf(R4-R6) - Q_inf(R3-R5)|). KA1's isolated check extends to R6; M2's spike
   to R6. Route 2 keeps its A1 resolutions (its rule on its finest three). The in-plane family keeps R0-R2 (A2 / A3).
4. KA3 is rerun with the A4 rule, unchanged otherwise (same sequences, same seed, same lines). Everything else is as A1 / A2.

**Why, and what was seen first (post hoc).**
- **KA3 fails under the frozen rule.** Its random sequences Q_inf (1 + c h^p) with small |c| fall into the flat clause, which
  returns Q_fine. The worst miss is 2.4e-2 (line 1e-6), on a p = 1 sequence where the flat clause's E (|d2|) is about half the
  true error. This is a defect of the rule: for order p the remaining error is |d2|/(1.5^p - 1), up to 2 |d2| at p = 1. As
  KA3 is a graded known answer, every frozen, A1 and A2 label is NO VERDICT on this ground alone.
- **Seen in the A1 label pass (route 2 not yet run).** Route L's Gamma_L^2 met the rule on 31 of 32 axial backgrounds,
  through the flat clause (17; E/Q 0.013-0.046) or Richardson (14; orders 1.3-4.0). The one that did not: alt expo
  10.7 at 0.01 a0, e-folding 49.90, 48.74, 47.73, 47.42 Gyr at R2-R5, where the R2-R4 triple has order 0.16, so the
  four-resolution error clause gives E/Q = 0.58. That is the reason for R6.
- The inner radius of the negative region came out 0.73-0.82 r_e at R3-R5 on every axial background; its rule failed on two
  (canonical Kuzmin 9.4 at 0.1 a0: 0.758, 0.738, 0.737, observed order 8.7, outside [0.5, 6]; alt expo 10.7 at 0.1 a0).
  Cell-quantised values give meaningless orders: the reason for item 2.
- The A1 axial maps (R0-R5) and the frozen and A1 in-plane maps (R0-R1), the A2 diagnostics, and the KA3 rows are the
  numbers seen. No R6 solve has been run; no PL R2 number exists yet (its run started under A2 / A3 before this amendment and
  is not read before this commit).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
