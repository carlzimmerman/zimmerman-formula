# N2 -- existence / regularity thresholds of the MOND field in a de Sitter static patch (c = G = 1)

## Bottom line
- **SHARP NO-GO (scoped).** For every interpolating family in the record (simple, standard, RAR, Milgrom mu_n, exponential, OR N = 2, 3) and for the Born-Infeld/DBI electrostatic form, the static spherical problem S(g) = mu(g/a0) g = s(r) has a **regular global solution for every mass M and every a0/H**, out to the horizon. The map S is monotone and onto, so no fold, no cusp, no existence threshold, no hyperbolicity breakdown (45/45 checks, controls included).
- The only existence thresholds are **folds of non-monotone S**, found in the cubic Galileon (two signs). They are **pure rational numbers** (s_fold = a0/4; a0/H = 4 in the vacuum, r_fail/L = 1/(4Z)), contain no pi, are independent of M in the vacuum, and their value comes from the hand-chosen polynomial (coefficient 1 in a0 units), i.e. from a convention for a0 (cubic coefficient c3 is the free coupling). The physical ratio Z = 5.789 lies on the failing side: a cubic Galileon with a0 = H/Z has no global vacuum solution. That **excludes** the family; it does not select Z.
- The FRW version: the de Sitter attractor exists for every a0/H (perturbation coupling dies as a^-2), and a shift-symmetric k-essence de Sitter fixed point needs P_X = 0, unavailable when mu = F' > 0. No threshold.
- Decoys: a random number from the menu hits a target within 10% 56% of the time; 5 of 13 menu values "hit" (all are mu(1) values times convention factors) -> uninformative. **No pure number from an existence threshold equals 5.789, 5.196, 6 or 2 pi.** Nothing derived; kappa = 1/2 stays FITTED.

## Declared (hashed) before computing
`n00_menu_declared.txt` (sha256 `4ed1cc40...`, verified by the script: check 1): readings P1 (Lambda inside the operator, s = M/r^2 - H^2 r) and P2 (Lambda outside), the families, threshold menu T1-T9, and the decoy recipe. Targets were compared only at the end.

## Setup
Units a0 = 1, H = Z, L = 1/Z. Spherical AQUAL: S(g) = s, where s is the Kottler-corrected Newtonian field (attractive M/r^2, repulsive H^2 r, reaching Z a0 = H at the horizon). QUMOND, g = nu(s) s, is the same map in spherical symmetry, so it has identical existence properties. Free-function status: **none of the families is free-function-free** (each is a hand-picked shape; DBI-BI and cubic Galileon have one scale and a fixed algebraic/polynomial form, but the choice of form is the function).

## Results (script `n01_thresholds.py`, output `n01_thresholds.out`, PASS 45 / FAIL 0)
| threshold | outcome | M-indep.? | pi | variable held |
|---|---|---|---|---|
| T1 fold of S | none for simple, standard, RAR, mu_n, exponential, OR N = 2,3, DBI-BI; Galileon c = +1 fold at s = -a0/4 (repulsive side), c = -1 at s = +a0/4 (attractive side) | yes (family shape) | none | a0 fixed, s free |
| T2 vacuum (M = 0) | Galileon c = +1: global solution iff Z <= 1/4 (a0 >= 4H); r_fail/L = 1/(4Z) (analytic, checked); all others: none | yes | none | Lambda |
| T3 with mass | Galileon c = -1 fails below r ~ sqrt(4M/a0) (root of M/r^2 - Z^2 r = 1/4 checked); others none | no (M-dependent) | none | G rho / M |
| T4 y_h = 1 | Z = mu(1): simple 0.5, standard 0.707, RAR 0.511, OR2 0.556, ... -- a property of the chosen shape, not a threshold of existence | yes | none | Lambda |
| T5 observer transition | r_t/L = 1/sqrt(1+Z^2) (0.170 at Z = 5.789): a location, not a threshold | yes | none | Lambda |
| T6 mass scale | sqrt(M/a0) = turnaround radius gives M_c = L/Z^3, M_c/M_Nariai = 3 sqrt3/Z^3 = 0.027; equal to 1 at Z = sqrt3 (conventional, M-dependent) | no | none | Lambda |
| T7 DBI speed limit | g_h/a0 = Z/sqrt(1+Z^2) < 1 for all Z: never reached (and DBI-BI has no MOND regime: g -> a0, constant force) | yes | none | Lambda |
| T8 FRW | delta -> const for all tested y0 (standard, RAR); k-essence fixed point needs mu = 0 | yes | none | Lambda |
| T9 'transition centre' | degenerate: dln mu/dln y is monotone for all families, extremum on the boundary | -- | -- | -- |

Controls and mutations (all passed, i.e. behaved as they must): detector flags a planted non-monotone S; Galileon fold matches the analytic -1/4, +1/4 and 1/(4Z); MUTATE: making Lambda attractive removes the c = +1 fold; RAR initially tripped the monotonicity check on root-finder noise (fixed openly by a noise floor; the check still flags the real Galileon folds). Two of my own first-pass checks (wrong r_fail branch, and an r_fail formula that ignored the Z^2 r term) failed and were corrected.

## Compared with the target (end)
Existence thresholds: rational (1/4, 4) only for the excluded Galileon; none for MOND-direction families. mu(1)-type values (0.5-0.89), sqrt3, 1/4, 4 are not 5.789, 5.196, 6 or 2 pi; the apparent hits after x{1/4..4} or inversion are decoy-level (56%). a0/H at which the actual universe sits (0.173) gives no special feature: r_t = 0.17 L is just 1/sqrt(1+Z^2).

## Not established / not done
- Only the weak-field (Kottler-corrected Newtonian) reading; no relativistic completion (AeST/TeVeS) and no full-metric horizon solution with MOND phantom mass (a MOND-corrected Nariai mass M_N(Z) would be M-dependent anyway). The static observer's proper acceleration diverges at the horizon, so in a relativistic version y -> infinity there (Newtonian regime at the horizon); not solved.
- P2 (Lambda outside the operator) has no fold by construction (sum of two fields); not scanned numerically.
- The FRW part is the quasi-static perturbation sector; a background scalar (time-dependent) completion was not constructed.
- Structural reason for the null: a threshold gives a number only through a non-monotone S, i.e. through a chosen function; a monotone transition (required by ellipticity and by data) has no eigenvalue condition. An eigenvalue for a0/H would need a boundary condition coupling the two ends (r = 0 and horizon) that AQUAL's algebraic spherical reduction does not have.

**Verdict: SHARP NO-GO (scoped to static spherical AQUAL/QUMOND/BI/cubic-Galileon in a fixed dS patch and the linear FRW perturbation sector).** Nothing new on the coefficient.
