# KT1_slope_tail_interlock: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: think from the repo, not the literature. κ = 1/2 FITTED. Footings never pooled. Not theory closed. Reinstates nothing. No cold component, no particle. Nothing here says the data favour the framework. **Not blind:** L230, L232 and L235's readings, lane K's README and the n = 2 selection are read. The idea was built knowing the target.

## Idea
In the repo's kernel (L230, L231), mu_n(Y) = 1 - (1+Y)^(-n), Y = g/s, s = c sqrt(G rho). One integer plays two roles:
- deep slope n, which gives a0 = s/n and kappa = 1/n;
- high-g tail 1 - mu ~ (s/g)^n = (c^2 G rho / g^2)^(n/2).

So the tail is first order in rho only at n = 2. n = 1 goes as sqrt(rho); n = 4 has no first-order term. **Added hypothesis P, named: the vacuum enters the high-g correction at first order in rho.** Inside the family, P gives n = 2 and kappa = 1/2. P is the same fact as L235's convergence boundary and lane K's "N = 2 has c = infinity", which L235 counts as one criterion at chance level. P is not a derivation and is not offered as one. It has no action behind it, and the family itself is an input.

**What is new is a test.** L232 only compares integers, where slope and tail move together. Nothing has measured them apart. If slope and tail are unrelated in the data, the route through this family is dead, whatever P says.

## Measurement
Two-parameter kernel: 1 - mu = (1 + n Y / p)^(-p). Slope n, tail exponent p; n = p is L232's family. s is fixed from G, c and the density on each footing, as in L232; nothing else is fitted.

Data and loader exactly as L232: SPARC `*_rotmod.dat`, eV/V < 0.10, at least 3 points, Upsilon disc 0.5, bulge 0.7. Statistic from the L232 robustness audit: each galaxy's mean squared log residual, galaxies equally weighted. Grid: n from 0.8 to 4.0 in steps of 0.1; p from 0.5 to 8.0 in steps of 0.25. Error: 1000 galaxy bootstrap draws, seed 20261102, best-fit (n, p) per draw. Intervals are 16-84 and 2.5-97.5 percent. Reported at Upsilon x 0.8 and x 1.25 too; the primary label uses Upsilon as stated.

## Labels, per footing, frozen
1. **TAIL NOT MEASURED:** the 95 percent interval on p reaches either grid edge, or contains both 1 and 4. No test. Checked first.
2. **INTERLOCK BROKEN:** the 95 percent interval on n - p excludes 0.
3. **INTERLOCK HOLDS AT 2:** the 95 percent intervals on n, on p and on n - p contain 2, 2 and 0.
4. **INTERLOCK HOLDS, NOT AT 2:** n - p contains 0, and n or p excludes 2.

Interlock holding is a shape description, not a derivation. It does not make κ forced, and it isn't a kappa hit. It would be the second prediction S4 asks for, conditional on P and on the family.

## Second reading, reported only
Plain mu_2 is worse than the mu_3 that RETRACTIONS records as failing Cassini at 1.25x, so the kernel needs stiffening in the Solar System (n >= 4 was the plain pass). State this beside any label.

## Controls, before the real run is read
- **Planted:** mock from the real g_bar with the real residual scatter at (n, p) = (2, 2) and (2, 4). If p isn't recovered inside its 68 percent interval for either, the real run reads NO VERDICT.
- **MUTATE:** g_obs shuffled across all points. Scatter must rise above the real best by at least 0.1 dex. Outputs `_MUTATE`, exit 1 by design.

## Limits declared now
Point errors, distances, inclinations and galaxy-level Upsilon are not marginalised, as in L232. The p37 lane found shape and Upsilon degenerate, which is why the x 0.8 and x 1.25 rows are reported. SPARC reaches Y of order 30, not the far tail (lane K). No download. Single thread, under 1 GB, minutes. Register row after the result, class `obs`.
