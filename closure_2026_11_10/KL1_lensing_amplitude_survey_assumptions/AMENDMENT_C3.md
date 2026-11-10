# KL1 PART C AMENDMENT C3 (POST HOC; committed alone, before DES Y3's gate row is seen and before the polish is run)

Part C criteria 190161a7f7; amendments C1 fe976ca7d3, C2 2fd0710da0. TEST lane; adopts nothing. **kappa = 1/2 FITTED; not
theory closed.**

**Timing, disclosed: post hoc.** Seen so far:
- on Legacy, every Part C row (the gate, C3b, MP5);
- on DES Y3 and KiDS-1000, KC1 and C0's four rows.

DES Y3's GATE, C2 and bracket rows have not been seen.

**The defect.** DES's preferred sigma8 and width from the scan are not stable at the precision the two-sided gate needs:
- C0 (R1) on DES reads best 0.7582 +- 0.0189 (canonical) against 0.7609 +- 0.0282 (alt), i.e. gaps of 2.85 and 1.81, with inputs
  that differ by 1e-4 in sigma8;
- Part A's A4 row gave a DES width of 0.0736 on one footing.

C2's diagnostic showed why. DES's 10-parameter L-BFGS-B fit stops up to about 0.1 in chi^2 above its minimum (an abnormal
line-search termination). Neighbouring grid points differ by only about 0.25 in chi^2 near the minimum, so the five-point parabola
inherits that noise.

**As frozen:** DES's gate reading uses the frozen scan; it is reported first.

**Added (C3): a polished DES scan for the gate.**
- Every grid sigma8 of DES's GATE row is refitted:
  - from kl1_lib.fit's default starts;
  - then repeatedly restarted from the lowest point found, until a restart improves by less than 1e-4 (at most 8 restarts);
  - with two sweeps along the grid (up and down), each grid point also started from its neighbour's polished nuisance vector.
- The lowest chi^2 per point is kept; CO2's parabola rule is applied to the polished points.
- Reported beside it: the same polish on DES's KC1 base (Part A's ALL settings), to show how much of the Part A / B DES
  numbers is optimiser floor.
- Under C3, DES's gate reading uses the polished scan.
- KiDS-1000 and Legacy (KiDS-style fits with 6 to 7 parameters, widths equal between footings to 3 digits) are not polished.

**Nothing else changes.**
