# DOOR B4 — Solve the Volterra equation exactly by resolvent, not by Picard
STATUS: OPEN | RANK: 12 | COST: S | KILLS FAST: no

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
The equation `G = G_BD + q^2 |G_R|^2 * G` is **linear** with an exponential kernel. It is analytically solvable
by Laplace transform and needs no iteration at all. Iterating it is what produced every spurious result: the
operator is unit lower triangular (verified at N = 64…4096), so `det(I - q^2 K) = 1` identically and the
resolvent always exists — there is no bifurcation at any q^2.

## Why it works with the framework
Method upgrade only. No physics changes.

## Concrete first calculation
1. Laplace-transform the equation. Locate the pole: `s* = q^2 A - 2 eta` with `A = thermal_factor^2`.
2. Confirm the only threshold is `q^2_thr = 2 eta / A = 0.0199254`.
3. Solve by forward substitution (exact, one pass) and fit the late-tau growth rate; review got agreement
   with `q^2 A - 2 eta` to 0.05-0.14%.
4. Watch for overflow: forward substitution at N = 4096 overflows to inf for large q^2 — work in log space or
   cap the range, and say which.

## Settles if / refuted if
SETTLED: the exact solution reproduces the pole prediction to < 1% and shows no bifurcation at 0.06248.
REFUTED: a genuine bifurcation exists at some q^2 — then find what operator it belongs to.

## Known walls — do not rediscover
numpy's `det` returns 1 at N <= 256 but 0 with overflow warnings at N >= 512 — that is a float64 artefact
(hazard H3), not a physical change. Use the triangular structure analytically.
