# CFG946 amendment A1 (2026-10-21; code and reporting only; partly post-result)

Criteria: `FROZEN_CRITERIA.md` (08f3b30a6). No test, tolerance, control, construction or class rule changes.

**Pre-result (before any number of this lane existed).**
1. K4's check was written with a rounding expression that would have failed CL-AR's own rounded value (54.48% printed by CL-AR
   as "55%"). Replaced by |100 f − target| ≤ 0.55 for the three printed targets (2.9 / 25 / 55). Made before the first run.
2. The Gauss-flux integrand subtracts a constant before integrating (an exact identity). The constant is now ν(g_e) only when
   g_e > g_s and 0 otherwise, which avoids cancellation in both limits. Made before the first run.
3. The QUMOND non-invariance check compared the phantom divergence of a point mass with zero; a point mass has a non-zero
   phantom density, so the correct check is the *difference* with and without the uniform gradient. Fixed before the first run.
4. The O2c deep-BTFR limit was parametrized by y and became singular at c₂ = 2; it is now taken along the static branch in u.
   The cubic-Galileon fit was re-parametrized (dimensionless c₂) with a stable root. Made before the first run.
5. The first K-stage attempt produced no output for 10 minutes: K3 called `sympy.simplify` on nine three-body expressions. It
   was stopped (own process) and K3 now checks the coefficients by expansion (simplify only as fallback). No K number had been
   printed.

**Post-result (after the first main run; classes unchanged).**
6. The first main run's class listing counted two printed PASS values as fails: `put()` stored numpy booleans, and the class
   rule tests `is not True`. Affected entries: O2a-G (b) and O2c (b). Both constructions are NOT VIABLE on other tests in that
   run, so no class and not the overall result changed; only the printed fail lists were wrong. `put()` now converts numpy
   booleans to Python booleans.
7. O2d1 (b): the detail text now also prints the growth exponent at the coupling c₁ that its own best (a) fit needs, beside the
   lenient value (PASS for c₁ ≥ 1/ε_max). The grade is unchanged (each test at its most lenient parameter, as for O2c).

The first main run's outputs are kept as `cfg946_firstrun_npbool.out` and `cfg946_results_firstrun_npbool.json`. K, MUTATE and
main are rerun in that order from the final script.
