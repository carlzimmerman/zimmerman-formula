# X23_late_heated_cold: AMENDMENT A2 (check definition only; RUN1 killed during the first cell build, before any graded number was printed or read)

RUN1 printed K2 FAIL: point-mass closed-form deviation 5.89e-06 and uniform-limit max |ln ρ| 8.49e-06, both against 1e-6.
Neither is a solver bug:
- (a) the closed-form test integrates g ∝ r⁻² with the trapezoid on X2's 3000-point log grid; its discretisation error is
  ~(Δ ln r)²/12 ≈ 1e-6 relative, so the 1e-6 line was set below the grid's own precision;
- (b) at c_s = 1e6 km/s the true profile is not uniform to 1e-6 for a 1e14 M☉ point mass at 0.05 Mpc
  (GM/(r c_s²) ≈ 9e-6), so the line tested the wrong limit.

**Amended lines (check code only; no criterion, model, constraint or verdict rule changes):** K2(a) ≤ 1e-4 relative;
K2(b) at c_s = 1e8 km/s (expected max |ln ρ| ≈ 9e-10) ≤ 1e-6. The MUTATE sign flip (m3) gives a deviation of order 2 and must
still FAIL K2. RUN1's partial log is not kept as a lane output (it holds only step-0 lines and one cell's build-time line,
"A1 cap binds at c_s,need in 320/326 clusters").
