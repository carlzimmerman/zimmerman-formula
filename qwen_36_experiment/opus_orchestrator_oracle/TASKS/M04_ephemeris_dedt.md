# M04 — Ephemeris de/dt: the eccentricity drift nobody has computed
COST: M | KILLS FAST: YES | script: `mi_ephemeris_dedt_2026.py`

## The task
On the corpus's open list since 2026-08-01 and never run. The exact law forces a **constant a₀/2 sunward
residual** (Theorem 4: Δ = a₀/2 identically). A constant radial perturbation does not just shift the
perihelion — it drives a secular **eccentricity** drift de/dt. Planetary ephemerides bound de/dt directly,
and that bound is independent of the perihelion-precession bound already used.

## Do
1. Lagrange planetary equations: for a constant radial perturbing acceleration Δ, derive de/dt and
   dω/dt secularly. Note the corpus found ⟨cos f⟩_t = **−e exactly** (not −3e/2), verified at three
   eccentricities — use the right one.
2. Evaluate for Mercury, Earth, Mars, Saturn at Δ = a₀/2, both footings.
3. Compare against published INPOP/EPM de/dt bounds (search for them; Fienga et al. and Pitjeva).
4. Report the margin per planet. Is de/dt a **tighter or looser** constraint than the 1279× perihelion one?

## Settles if / refuted if
Either it is tighter (a new, stronger liability — report it plainly) or looser (the perihelion bound stays
the binding one). Both are useful; the point is that it is currently unknown.

## Known walls
The 1279× (canonical) / 1544× (ALT) figures over Sereno & Jetzer's 3.66e-14 are already established and
reproduce to <1%. Fienga's ~200×-looser relief is **outer-planet only** and does not reach the inner bound.
