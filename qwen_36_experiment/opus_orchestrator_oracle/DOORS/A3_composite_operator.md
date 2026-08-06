# DOOR A3 — Composite operator (phi^2, T_mu_nu) where rho is genuinely state-dependent
STATUS: OPEN | RANK: 3 | COST: M | KILLS FAST: YES | PREREQ: A1

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
A1's wall holds because `[phi(x), phi(y)]` is a **c-number**, so rho cannot depend on the state. For a
composite operator `O = phi^2` (or the stress tensor) `[O(x), O(y)]` is **not** a c-number, so rho_O genuinely
depends on the state. This is the cleanest legal escape and it also repairs the review's defect #1: tn26's
Eq.(19) is Gaussian-plus-linear-source, so every connected propagator is exactly q-independent (sympy:
`<phi phi^T>_conn - A^-1 = 0` identically in q). Replacing `q*phi` with `q*phi^2` fixes that at the root —
it makes Eq.(24) a real sunset diagram with signs, and lets G_R actually move.

## Why it works with the framework
The MI coupling is to the vacuum's response to accelerated matter; nothing in the framework specifies that
the coupled operator must be the elementary field. T_mu_nu is arguably the *more* natural choice for a
gravitational mechanism, and the corpus's own open list from 2026-08-01 already names `rho_m/T_mu_nu coupling`
as an unexplored escape.

## Concrete first calculation
1. Compute rho_{phi^2}(omega) on the dS worldline by the same residue method as A1. It is a one-loop
   convolution of two BD propagators — do it analytically if you can, numerically otherwise.
2. Check the sign in the BD vacuum first (expect >= 0 — that is the control).
3. Then compute it in a **squeezed** state. de Sitter squeezes modes, so this is physically motivated, not
   arbitrary, and KMS does not apply to a squeezed state.
4. Report whether any admissible squeezing gives a negative band, and how deep.

## Settles if / refuted if
SETTLED: rho_{phi^2} >= 0 for all admissible states ⇒ the state-deformation class is closed rigorously, which
would be a strong publishable theorem covering both A1 and this.
OPENS: a negative band in a normalizable squeezed state ⇒ the mechanism has a legal home. Then go to C1
immediately to see whether it carries any T-dependence.

## Known walls — do not rediscover
The one-loop sunset has a UV divergence — regularize it and say how; the *sign* of the finite part is the
question, not the divergence. And a negative band alone is not MOND: it must also produce T-dependence (C1)
and survive complete positivity (A5).
