# DCN1 AMENDMENT A5 (post hoc; committed alone, AFTER seeing the P1 and P2 local outputs, before the label script ran)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Criteria d603f1703c; A1 0a6e46fb52; A2 15f6f993e4;
A3 f5e101ba9a; A4 d08610695e.

## Disclosure: written after seeing the outcome

These had been seen when this amendment was written:
- **P1, 16 backgrounds, and P2, 8 backgrounds, at all five resolutions under A4.** Every cell of every analysis region has
  D.P > 0 at every resolution. Every shell maximum of Gamma_loc^2 is negative.
- **P2's Q_A converges smoothly** (canonical 9.4: -3.537, -3.521, -3.511, -3.510, -3.507 x 1e-29 s^-2).
- **On the external-field nulls at 0.1 a0, Q_A jumps with resolution.** Q_A is the least-negative decay rate in the annulus.
  Canonical 9.4: -1.61, -2.54, -1.20, -3.08, -3.08 x 1e-29. The likely reason is that the local null sits off the box
  centre taken from the global R4 grid, so the null's own resolution-independent cell error lands in the annulus. So
  A3's stable(b), which requires Q_A Converged, would leave those backgrounds open.

## The amendment

**The frozen criteria (d603f1703c, section 3) had a second sufficient condition for stable(b):** "no D.P < 0 cell exists in
the analysis region on the finest two resolutions". A3 rewrote stable(b) to fix the rate quantity at the null cell, and in
doing so dropped that clause. A3's stated purpose did not include removing it. A5 restores it:

- **stable(b)** iff not unbounded(b) (A3 item 2), and either:
  - (A3) Q_A Converged with Q_A,inf + E < 0 and every shell maximum negative on the finest two grids, or
  - (frozen) no D.P < 0 cell in the analysis region on the finest two resolutions.

  By SCS3's Lean growth_sign, Gamma^2 > 0 iff D.P < 0, so the second condition means no cell grows.
- Everything else in A3 and A4 stands.

**Order of readings in RESULT.md:**
1. frozen (NO VERDICT: KA4 fails);
2. A1 (NO VERDICT: KA4's Q not Converged);
3. A3 as written (computed and reported as it falls);
4. A5 (this restoration), labelled post hoc after seeing the outcome.

**Also reported, not graded.** Whether each P1 box contains a resolved null: the fitted slope of u against s must be at
least 0.3 (the deep-law value is 0.5). The frozen search window (1e-3 to 0.3 R_d) misses the null wherever it sits closer
to the centre than 1e-3 R_d. At 0.01 a0 that is where it sits, near the centre, where P2's limit applies.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
