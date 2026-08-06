# DOOR F2 — Is the Volterra operator bounded at all with the real de Sitter kernel?
STATUS: OPEN | RANK: 12 | COST: S | KILLS FAST: YES

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
Every q^2_crit in the corpus was computed with a **toy** kernel `exp(-dtau/0.1)`, on a log grid, with no
quadrature measure, and it turned out to be a pure grid artefact (`||K|| ∝ N`, so `q^2_crit → 0`). Nobody has
asked whether the operator is bounded at all when the **real** dS retarded Green's function is used.

## Why it works with the framework
The real kernel is the framework's own; the toy was a placeholder. This door replaces a placeholder with the
thing it stood for.

## Concrete first calculation
1. Build the Volterra kernel from the committed dS retarded Green's function (from
   `mi_circular_dS_response_2026.py`, whose `D(s) >= s^2` guarantee means no real-axis pole).
2. Compute `||K||` **with** the quadrature measure, at N = 64…4096, and check whether it converges or scales
   with N.
3. If it converges, report the continuum `q^2_crit = 1/||K||` with its refinement error.

## Settles if / refuted if
CONFIRMS: `||K||` converges ⇒ the programme finally has a real, grid-independent coupling threshold, which
would replace the artefact at every place tn26 cites 0.06248.
KILLS: `||K||` diverges with the real kernel ⇒ the resummation is ill-defined and no threshold exists, which
closes the "critical coupling" narrative entirely.

## Known walls — do not rediscover
The boost sector's memory integral `int K(s) cosh(h s) ds` **diverges for h > omega_c** — that is an open item
from the auxiliary-field work, and it may be the same divergence. Check whether they are the same fact.
