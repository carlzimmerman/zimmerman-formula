# KT12_compact_kernel_milky_way: MW FAILS on both footings. On star-count baryons the compact kernel is nearly Newtonian at the Sun, so v_c falls 14-19 km/s short of the line; K_z passes. The near misses of KT11 close

Criteria: `FROZEN_CRITERIA.md` (d6732fb2eb), alone first, confirmed landed before any script, **not blind**. `kt12.py`, `kt12.out`, `kt12.json`, `kt12_MUTATE.out`, `kt12_MUTATE.json`. No download. κ = 1/2 FITTED and held fixed: this tests a kernel, not κ. Footings never pooled. Not theory closed. Register K823. Runtime about 4 minutes, peak RSS 0.29 GB, one thread, nice 15.

Kernel: KT11's mu = x - x^2/4 for x <= 2, 1 above (x = g/a0), on UX5's QUMOND form Q, its three boxes, its four lines and its prior tags, all unchanged.

| | canonical (about rho_DE) | alt (about rho_crit) |
|---|---|---|
| B175 / BV / BV2 class | V+K ONLY / V+K ONLY / INFEASIBLE | V+K ONLY / V+K ONLY / INFEASIBLE |
| in-prior cells passing L1 (v_c), any box | 0 of 1375 | 0 of 1375 |
| highest in-prior v_c, line bottom 219.9 | 201.4 | 205.6 |
| in-prior cells passing L2b (K(R0)) | 306 | 662 |
| in-prior best cell (BV2): v_c, Newton v_c, K, Ou chi2 | 201.4, 200.0, 65.5, 533 | 205.6, 200.0, 68.6, 316 |
| best cell anywhere: R_d, M*, v_c, K | 1.60, 9.8e10, 243.5, 68.9 (BV) | 1.93, 8.6e10, 228.5, 71.1 (BV) |
| **Label** | **MW FAILS** (L1, L3) | **MW FAILS** (L1, L3) |

## Reading
- **It's the expectation stated before running.** At R0 the observed field is about 2.2 a0 on canonical and 1.8 a0 on alt, where this kernel is exactly or nearly Newtonian. The phantom at R0 adds 1.4 km/s (canonical) and 5.6 km/s (alt) to Newton on the in-prior best cells. So v_c needs a Newtonian disc near 229 km/s.
- **Star-count baryons don't give that.** Cells near the line need R_d 1.6-1.9 kpc and M* 8.6-9.8e10, below LN16's R_d tag (2.38) and at or above its M* top (8.36e10). Ou's outer curve fails everywhere in priors too.
- **This closes the canonical question KT11 left.** SPARC asked for stars 41 percent heavier than its tolerance. The one galaxy with star-count masses also asks for more, or more concentrated, baryons than the counts allow. Both say the same thing: the kernel gives too little boost near g = a0 to 2 a0.
- **Against mu_2, B175 only (no label):** mu_2 gets closer on v_c (in-prior best 214.7 canonical, 212.6 alt) but its K(R0) is 80 against a line top of 70.8. So the Milky Way sits between the two shapes. The smooth kernel gives enough boost at R0 and too much vertical force; the compact kernel gives the right vertical force and too little boost. Neither does both on these baryons. That's a reading of two kernels, not a theorem about all of them.

## Checks
C1: the law's nu through this code reproduces UX5's stored form Q on all 175 B175 cells, both footings, max relative 0. C2: inversion 4.4e-16. C3: Plummer 0.0020. C4: Kuzmin 0.0012, at y 0.56-2.72, which spans the corner. Q5: doubled grid on the in-prior best cell, dK +0.03 and +0.04, dv -0.04 and +0.02: converged. MUTATE (nu = 1, Newton): in-prior v_c 159-200, same class, exit 1.

**Disclosed.** The first run's Q5 printed exactly 0 because `run` copied the old cell's results over the new solve. Fixed by copying only the cell keys and the whole run repeated. Classes, counts and lines are unchanged, since the bug touched only Q5's re-solve. The MUTATE run came from the earlier code; its path never calls Q5.

## Where this leaves the compact kernel
Three gates, three results across KT11 and KT12: canonical passes Cassini and fails SPARC's stellar scale and the Milky Way; alt passes SPARC's scale at the edge and fails Cassini and the Milky Way. No footing survives. I'd stop working on this shape. A sharper corner would make the Milky Way worse, since it removes more of the boost at R0.
