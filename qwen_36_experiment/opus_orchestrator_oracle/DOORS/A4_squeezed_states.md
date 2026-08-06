# DOOR A4 — Squeezed de Sitter states: KMS does not apply
STATUS: OPEN | RANK: 9 | COST: S | KILLS FAST: no | PREREQ: A1

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
de Sitter expansion **squeezes** field modes — that is standard inflationary physics, and a squeezed state is
not thermal, so the KMS argument simply does not bind it. The programme has only ever evaluated Bunch-Davies.
The alpha-vacua were touched (`tn03_alpha_vacua_passivity.py`) but squeezing was not.

## Why it works with the framework
Squeezing is a property of the dS background the framework already assumes; it introduces no new parameter
beyond the squeezing amplitude, which is fixed by the expansion history rather than chosen.

## Concrete first calculation
1. Write the two-point function for a squeezed BD state with squeezing parameter r_sq and phase.
2. Compute rho(omega) for the elementary field — **expect it to stay positive** (A1's c-number argument
   applies regardless of state, so this is a consistency check on your algebra, not a hope).
3. Then compute it for phi^2 (this is where A3 and A4 join).
4. Fix r_sq from the number of e-folds and report whether the physically realised squeezing is anywhere near
   what a sign flip would need.

## Settles if / refuted if
SETTLED: the physically realised r_sq gives a negative band far too small to matter — quantify "far too
small" as a ratio, and this door closes with a number.
OPENS: realised squeezing gives an O(1) effect on rho_{phi^2}.

## Known walls — do not rediscover
For the elementary field, squeezing cannot flip rho — A1's argument is state-independent. If your elementary
field calculation shows a flip, it is a bug. Only the composite operator can move.
