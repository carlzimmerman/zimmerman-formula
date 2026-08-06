# DOOR A2 — Bounded-spectrum matter sector, where inversion is legal
STATUS: OPEN | RANK: 2 | COST: M | KILLS FAST: YES | PREREQ: A1

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
A1's wall is specific to the unbounded bosonic ladder: n >= 0 forces `<[a, a_dag]> = 1 > 0`. For a **bounded**
spectrum the analogous object changes sign. For a two-level system `<[sigma_-, sigma_+]> = -<sigma_z>`, which
is negative exactly when the upper level is more populated. For an L-level ladder the explicit criterion is

    sum_k (p_k - p_{k+1}) (k+1) < 0

which is satisfiable with all eigenvalues >= 0 — e.g. p = [.05, .10, .15, .70] gives -1.8. So a genuinely
positive, normalizable state CAN have rho < 0 if the sector is bounded. This is the first legal negative
spectral density in the programme.

## Why it works with the framework
MI couples the vacuum to **matter**, and matter degrees of freedom are not required to be free scalar modes.
A bounded internal sector is a modelling choice about the detector, not a change to a0 or the a0-line. The
Unruh-DeWitt detector the corpus already uses IS two-level.

## Concrete first calculation
1. Set up a steady-state Bloch/Redfield equation for a two-level UDW detector on a circular dS worldline.
2. **Use the already-committed transition rates** from `real_research/reviews/mi_circular_dS_response_2026.py`
   (8/8) — do not rebuild them; that script's F(E) and T_eff(E) are validated against Deser-Levin to 1e-15.
3. Ask: is `<sigma_z> > 0` (inversion) reachable anywhere in (Omega, v/c, R)? Scan it.
4. If yes, compute the resulting rho band and delta_m, and report the magnitude.

## Settles if / refuted if
SETTLED (closes cleanly): detailed balance holds for a single bath, so `<sigma_z> < 0` always ⇒ the
single-bath NESS route is dead and B2 becomes the only live NESS door. That is a valuable negative.
OPENS: inversion reachable ⇒ first legal rho < 0. **But expect the magnitude to be bounded by ~(v/c)^2** —
the committed number is 8.6e-07 at galactic v/c (FRAMEWORK_FACTS #6), so report the size, not just the sign.

## Known walls — do not rediscover
A single bath at one temperature cannot invert a two-level system — that is detailed balance, not an open
question. If you find inversion with one bath, you have a bug.
