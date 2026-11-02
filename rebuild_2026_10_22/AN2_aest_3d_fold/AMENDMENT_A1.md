# AN2 AMENDMENT A1: check KD's comparison, after its first-run miss, before any science row

**Timing:** written after KD missed on first run, and after KZ and KE2 had also missed. No S1 row, and none of KT, KB, KE, KG, has been run. Line 2e-3 unchanged. This doesn't touch KZ or KE2, which stay failed.

1. **KD as frozen missed: 6.2e-3 against 2e-3,** comparing each tet's det with the continuum det J at the tet's centroid. Error halves with N (3.1e-3 at 128^3), so it is first order. A tet's columns are differences along different edges, whose midpoints aren't the centroid; the comparison point was wrong, not the sign or indexing. Changed: each analytic column is evaluated at its own edge midpoint. Result 1.0e-4 at 64^3, 2.6e-5 at 128^3. **This changes a test after seeing it miss, so it can be discounted.** The frozen-form error is still printed in each KD record. It also means a single tet's det differs from the continuum at first order in the cell; the fold is defined on the tet, so this is part of the grid dependence.
2. **KD's held-core setup** reached det 1.8e-5, not the frozen 1e-9: code fault, the core wasn't flat. Fixed to det 1.2e-9. Doesn't fire, as before.
3. **Not frozen, stated here:** S0 and KE1 integrators use rtol 1e-9 (first setting 1e-10 returned no collapse), and the quad form uses a finite-range substitution. KE2 reads its fold within ellipsoidal radius 0.8 of the edge.
kappa = 1/2 FITTED. Reinstates nothing. Not theory closed.
