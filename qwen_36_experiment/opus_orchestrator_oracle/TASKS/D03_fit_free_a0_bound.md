# D03 — Reproduce the fit-free a₀ ≤ 1.1606e-10 bound
COST: S | script: `mi_fitfree_a0_bound_2026.py` | PREREQ: D01

> ENGINEERING / DATA task. Import `TOOLS/mi_constants.py` — never retype a constant.
> `../02_HOUSE_RULES.md` and `../03_NUMERIC_HAZARDS.md` apply.

## The claim
The joint over-determination found a bound with **no RAR fit and no mass-to-light ratio**: SPARC orbital
frequencies combined with the lunar-laser-ranging Ġ/G ceiling give **a₀ ≤ 1.1606e-10**. Canonical clears it
by 24%; ALT by only **2.6%**. That is unusually clean — a bound that does not depend on Υ at all — so it is
worth reproducing independently.

## Do
1. Extract orbital frequencies Ω = V/R per galaxy from D01's loader (no mass model needed — that is the point).
2. Combine with the LLR constraint and re-derive the bound. Show every step; the value of this task is that
   the chain is short enough to audit.
3. Report the bound and the margin for canonical and ALT.
4. Then push it: what would tighten it? A better LLR bound, or more galaxies at extreme Ω? Quantify which.

## Settles if
You reproduce 1.1606e-10 to a few percent, or you find the chain has a hidden Υ dependence — either is worth
knowing, since three of the four binding constraints prefer the ALT footing.
