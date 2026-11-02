# TM2 AMENDMENT A1, written after Part A, B and C's first numbers, before any number below. Post-result; none of this changes a frozen label

Seen when writing: labels on P (F1, F2, W1, W3 DEAD; W2 WOUNDED or DEAD at k fit, PASS cells at pi^2 and k x 0.65, tau 300-600); W2 main M300 Z about +4 at k fit; Part B and C rows.

**A1.1 K1 stays FAILED as frozen.** Peak within one 20 kpc cell: 41 kpc on N1's row, against 28. By the frozen rule a failed K1 stops the verdict. Suspected cause: N1's sub maximum has no local maximum and lies on the window edge, so it's grid-dependent (UX6: "no local max"). M300 agree to 1e-4 and dkappa to 0.2 %. Test: W3 tau-to-0 with this lane's own code at UX6's 10 kpc grid. If the peak matches UX6's within 10 kpc, labels are read with that disclosed; K1 is not rewritten.

**A1.2 An error in my relaxed check, found on reading it.** Part B's W orbit factor averages |g_gas| along orbits, which is W1's. W2 stores a vector. A star's past field points at the centre from where the star was then, so on an orbit the stored vectors rotate and cancel. Frozen text said "m = <g_gas>/g_gas" without saying which, and W2 is the nearest miss, so this must be run:
- **m_v(r, tau)** = orbit ensemble mean of g_gas(r(s)) rhat(s).rhat(0), X-COP, isotropic and beta 0.5. X-COP lines and keys with it, k fixed and refit on UX3's 4.
- **W2-s:** the Bullet's W2 with each flow's memory multiplied by m_v, read off tau/t_dyn(r_c), both at k fit and k refit.
- **Discs, circular orbits:** radial factor 1/(1 + (V tau/R)^2) for the exponential kernel; and a tangential part, (V tau/R)/(1 + (V tau/R)^2), pointing forward along the orbit. Rows: UX3's disc lines on the radial factor; spin-up time V/a_t on SPARC points. A stored vector is a transported field on the flow, more than a scalar memory; stated.

**A1.3 Verification of W2's PASS cells, as hard as a fail.** Fresh code, no import from `tm2_map.py`, UX6's 10 kpc grid, map-sum masses. W2 is linear in k, so k is scanned: per tau, the k range reading PASS, TENSION on both footings, against CU1's k error and the X-COP pass range. Histories P, t150, t260, p2, b256, q40 at pi^2. Pair rows of Part C re-read at pi^2 with tau 300, 600 added (`TM2_POST=1`, separate outputs).

No new label. Reported as post-result rows. A pass here isn't a candidate unless section 7's conditions hold as written.
