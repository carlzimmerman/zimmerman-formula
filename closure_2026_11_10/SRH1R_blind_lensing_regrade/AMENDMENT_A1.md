# SRH1R AMENDMENT A1 (2026-11-12): KA2's expected value was mis-stated

Written after the model-side known answers were first run and before any data file was opened by an SRH1R script. No
lensing number, pair count or gate value existed. Post hoc to the criteria in the sense that KA2's first run was seen.

**What happened.** KA2 as frozen: for the law's untruncated halo, 4 G DeltaSigma = sqrt(G M_b a0) / R to 1e-3 for
30 <= R / r_M <= 1000. The code returned a deviation of 2.14 % at R / r_M = 30, the same on both footings.

**Why.** The frozen expectation is my hand error, not a code fault. The untruncated enclosed mass is
M_b [1/2 + sqrt(1/4 + x^2)] = M_b (x + 1/2 + ...). The constant M_b / 2 projects as a point mass and adds
(2 / pi) / u to the ratio, u = R / r_M: 2.12 % at u = 30, 0.06 % at u = 1000. The frozen line left that term out.

**Amended KA2.** 4 G DeltaSigma / [sqrt(G M_b a0) / R] = 1 + (2 / pi) / u to 1e-3 on 30 <= u <= 1000. The code gives a
largest residual of 2.1e-4 (the next term, of order 1 / u^2). The as-frozen reading (FAIL) is printed beside it in
`srh1r_model_ka.out`.

**Also disclosed (no criteria change).** Three numerical settings of the neighbour tables were changed while KA7 was
failing, before any data: the quadrature is split where a circle crosses a neighbour's centre and at the halo's edge;
the table coordinate pins that crossing; the table has a row for a centred halo. KA7 then passes as frozen (largest
deviation on 200 random pairs 0.30 % of the point-mass scale against the 1 % line).

Nothing else in the criteria changes. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
