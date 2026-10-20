# AG4c FROZEN CRITERIA (2026-10-20): capacity census. Can any in-repo measurement see the tether cap?

Committed alone, before any AG4c script, number or data pull. Owner's go as for AG4b (2026-10-20, in chat).

## The frozen falsifier (AG4 FROZEN_CRITERIA kill test 2, from G3)
A tethered phantom field obeys u = g_ph < a₀/n: g_ph < a₀ for n=1 and g_ph < a₀/2 for n=2. In AG4's convention
Σ̄_ph = g_ph/(πG), these caps are 214 and 107 M☉/pc² on the canonical footing (258 and 129 on the alt footing). A
well-measured tethered system with g_ph above a₀/2 excludes n=2; above a₀ it excludes n=1 as well.

## A structural fact, derived by algebra before any data
Each cap is that law's high-acceleration asymptote: u → a₀/n as g_bar → ∞. For example, at g_bar = 5a₀,
u = 0.854 a₀ (n=1) and 0.477 a₀ (n=2). At g_bar ≲ a₀ both laws give u ≈ √(a₀ g_bar) − g_bar/2, so lensing and dynamics there
cannot test the cap. A census therefore measures g_ph = g_obs − g_bar where g_bar ≫ a₀, and its error is dominated by the
baryonic mass (Υ or IMF, and distance).

## Scope
Tethered systems only: late types. Merger-freed ellipticals and cluster cores are out of scope, because their cold energy is
free under S4 and not capacity-limited.

## Classes (in-repo data only; no data pull in this lane)
- **C1, used:** SPARC points with g_bar ≥ 2a₀ (CFG4_common.load_sparc). Υ_disk = 0.50 and Υ_bul = 0.70 at 3.6 μm, with a
  0.10 dex coherent error per galaxy; distance and inclination errors from the master table; the velocity error per point.
  g_ph,j = g_obs,j − g_bar,j, and σ_j combines those terms, propagated linearly.
- **Omitted, with the reason fixed now:**
  - the Milky Way at the solar circle: its baryon model is not a committed record input;
  - DiskMass: CFG576–578 found a 40–65% σ_z deficit shared by every model, larger than the n=1/n=2 difference;
  - KiDS isolated-galaxy lensing: the structural fact applies, since g_bar ≲ a₀ at the lensing radii.

## Readings, per footing
- "Well-measured" means σ_j ≤ 0.15 a₀, so that the two caps, 0.5 a₀ apart, separate at ≥ 3σ.
- **EXCLUDES n=2:** at least one well-measured point in a Q ≤ 2 galaxy with g_ph − 2σ > a₀/2. The n=1 exclusion
  (g_ph − 2σ > a₀) is reported too.
- **CONSISTENT:** well-measured points exist, and none exceed the cap.
- **NOT DIAGNOSTIC:** no well-measured point. The lane then names the data that would decide (for example, late-type strong
  lenses with kinematic mass-to-light ratios) without pulling them.
- **Input to the ALMA step:** "n=2 survives AG4c" iff the reading is not EXCLUDES n=2 on either footing.

## Power pre-flight
Reported first: the number of C1 points and galaxies with σ_j ≤ 0.15 a₀, and the median σ_j/a₀ at g_bar ≥ 2a₀.

## Controls
- K1: cap algebra. For n = 1, 2, u(g_bar) < a₀/n everywhere and u → a₀/n as g_bar → ∞, to 1e-9 on g_bar ∈ [1e-3, 1e6] a₀.
- K2: the Σ̄ conversion reproduces AG4's 213.7 M☉/pc² and the half, 106.9 (canonical).

## MUTATE
`AG4C_MUTATE=1` injects g_obs = g_bar + 0.9 a₀ on the C1 points, with every σ_j shrunk ×10. This is a phantom that violates
the n=2 cap. The run must return EXCLUDES n=2, and the script then exits 1 (the control bites).

## Seen before this file (disclosed)
AG4's caps (214/107) and AG3's diagnostic. The asymptote values 0.854/0.477 at g_bar = 5a₀ were computed by hand while writing
this file. No census number.

## Settings
κ = ½ fitted; footings never pooled; not theory closed. Runs only after NC2x ends. Outputs: `ag4c.py` → `ag4c.out`,
`ag4c_results.json`; MUTATE → `ag4c_MUTATE.out`, `ag4c_results_MUTATE.json`.
