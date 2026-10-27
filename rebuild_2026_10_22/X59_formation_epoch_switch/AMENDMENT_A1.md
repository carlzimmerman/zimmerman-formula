# X59 AMENDMENT A1 (implementation fix; committed before any graded number)

The first normal run stopped at check K4 and was killed before any graded number was printed (no retention, R1 or f_EC
line had been written). K4 compares the Monte Carlo single-epoch progenitor fraction with the analytic excursion-set
value. It failed at one of three points: host 10¹², m 10¹¹, z 0.5 gave 0.7867 against 0.8071 (|Δ| 0.0204, gate 0.02).
The other two points were 0.7259 vs 0.7375 and 0.5873 vs 0.5922.

**Cause.** The walk is checked against the barrier only at the grid points, ΔS = 0.01 apart. Crossings that happen
between two grid points are missed. This delays the first crossing, so the progenitor masses come out too small. The
bias is largest where S(m) − S0 is small.

**Fix.** The frozen ΔS = 0.01 is kept. The crossing search uses the standard continuity correction for barriers that
are monitored only at discrete points (Broadie, Glasserman & Kou 1997): B_eff = B − 0.5826 √ΔS. That is a shift of
0.058 in δ. The analytic side of K4 keeps the true barrier.

Nothing else changes: the rule, the inputs, the gates, the verdict classes and the MUTATE plan are all as frozen.
