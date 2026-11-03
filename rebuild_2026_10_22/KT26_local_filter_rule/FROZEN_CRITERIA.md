# KT26_local_filter_rule — FROZEN CRITERIA (before any script or number beyond the hand estimate below)

Owner, 2026-11-03: go after why the filter length is r_M / 2 (KT25: ε = κ = 1/2 survives on canonical), from a field equation.

κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. No
download.

## Part A — identity (exact; checked numerically, not graded)
With a0 = κ c sqrt(G ρ) and ξ = κ r_M, r_M = sqrt(G M / a0), V∞^4 = G M a0:
  ξ = V∞^2 / g*,  g* := c sqrt(G ρ) = a0 / κ.
So ε = κ is the statement "the smoothing length is where the deep-MOND field V∞^2 / r equals g*". In this form ξ carries no
1/2; the 1/2 sits only in a0 = κ g*. Check A1: both forms agree to 1e-12 for M = 1 Msun and 1e11 Msun, both footings.

## Part B — the local rule
Deep-MOND fields have V∞^2 = g^2 / |dg/dr|. The local, mass-free version of the filter is
  **ξ_loc(x) = |g|^2 / (|∇|g|| g*)**,
which equals κ r_M exactly for an isolated point mass in the deep limit (check B1, numerically on the board law's point-mass
field at r = 100 r_M, within 1e-3), and needs no "system mass".

## Part C — the Milky Way screen (graded)
ξ_loc at R0 from the observed curve: V(R0) = 229.1 km/s (UX5 line L1), dV/dR = -1.7 km/s/kpc (Eilers+19 slope, PROVISIONAL
from the record), R0 = 8.178 kpc: |dg/dR| = (V^2 / R0^2)(1 - 2 dlnV/dlnR), so ξ_loc(R0) = V^2 / ((1 - 2 dlnV/dlnR) g*).
Hand estimate before running: about 8.1 kpc (canonical), 6.7 kpc (alt), between KT17's passing ε 0.55 (about 5-6 kpc) and
failing ε 1.0 (about 10-11 kpc).

Run: KT17's code (`kt26.py`, a copy) on all 1375 in-prior MW cells per footing with the filter length per cell set to
ξ_loc(R0) of that footing (one universal value per footing, quantised as KT17 does), lines L1, L2a, L2b, L3 and strict h
unchanged. This approximates the position-dependent ξ_loc by its value at R0, where the lines are measured; stated.

Labels per footing: **LOCAL RULE PASSES MW** if at least one in-prior cell passes all four; **LOCAL RULE FAILS MW**
otherwise. Passing cells reported by thick share. A pass here is a screen, not a full solve of the local rule.

## Part D — direction only, not graded
ξ_loc for the Sun at Saturn's orbit and at r_M including the MW external field 2.32e-10 (where |g| is dominated by the
uniform field, ξ_loc grows), and for a Fornax-like dwarf in the MW field. Printed, with the direction it would move Cassini and
the dwarfs. No label.

## Checks
A1, B1 as above. KT17's checks as they are (its C3 half-space factor is a known failure; disclosed if it recurs). MUTATE: KT17's
own path, not rerun.
