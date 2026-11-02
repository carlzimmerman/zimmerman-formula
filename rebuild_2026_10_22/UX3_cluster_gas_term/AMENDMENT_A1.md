# UX3 AMENDMENT A1 (committed alone, before any Part B holdout is graded)

**Adds the one candidate the criteria allow, from Part A:**
- **C5, gas-dominated switch:** theta = 1 where gas share f > 1/2, else 0. Statement: the term acts only where gas, not stars, dominates the enclosed baryons. 1/2 is "majority", not read from the separation table. Unlike C1, it does not pass discs by construction: gas-rich dwarfs keep the term, so it is the real test of Part A's dwarf overshoot. In the grader f = 1/(1 + f*), theta = 1. FITTED (search-picked k), like every rule here.

**Disclosed departures, Part A:**
1. Criteria said Part A touches no holdout. `ux3_a.py` printed X-COP unseen and even-SPARC rows for theta = 1 forms, so F1 A=1's unswitched X-COP holdout (+0.040, 0.078) has been seen. BF1 had printed the same for the B members. Switched rows are unread.
2. K3 first read FAIL, 0.0025: I typed line 6's numbers of BF1's output against the expression on its line 8. Corrected the constant, K3 passes to print precision. Seen and fixed, no number moved.
3. F1 with A = 1, k = pi^2 reads X-COP train +0.084, 0.123, which misses line 1 before any switch. Grade stands as frozen; F1k is the frozen fitted row.
