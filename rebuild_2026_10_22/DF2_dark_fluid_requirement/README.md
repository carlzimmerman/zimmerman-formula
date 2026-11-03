# DF2_dark_fluid_requirement: DENSITY KEY PASSES GATE 1 at five of ten barotrope cells. My expectation was wrong: pressure at recombination isn't what gate 1 limits. One gate only

Criteria `FROZEN_CRITERIA.md` (332dae21b7), committed alone first. `AMENDMENT_A1.md`, post-result. `df2.py`, `df2_patch.py`, `df2.out`, `df2_results.json`, `df2_analytic.out`, `cells/`. A requirement map: it adopts nothing, reinstates no retired sector, offers no action. κ = ½ FITTED, and a₀ is absent from linear FRW. Not theory closed. Nothing here says the data favour the framework. A family statement on these inputs, not a no-go theorem.

## Barotropes anchored to discs (c_s = σ at 0.05 M☉/pc³), by fit
| Γ | σ km/s | c_s at z 1100 | c_s at z 0 | S − S_min (line 25) | plik | σ8 | P halves at k h/Mpc | Read |
|---|---|---|---|---|---|---|---|---|
| 7/3 | 30, 100 | 2770, 9240 | 0.002, 0.008 | screen 22989, 66787 | 23416, 67136 | 0.30, 0.18 | 0.08, 0.06 | fails screen; not fit by the frozen rule |
| 5/3 | 30 | 288 | 0.26 | 0.4 | 582.0 | 0.820 | 1.89 | PASS |
| 5/3 | 100 | 961 | 0.87 | 4.4 | 583.4 | 0.784 | 0.54 | PASS |
| 1 | 30 | 30 | 30 | 0.2 | 581.8 | 0.823 | 2.99 | PASS |
| 1 | 100 | 100 | 100 | 1.4 | 582.3 | 0.801 | 0.81 | PASS |
| 2/3 | 30 | 9.7 | 321 | 4.1 | 582.6 | 0.755 | 0.40 | PASS |
| 2/3 | 100 | 32 | 1070 | 50.9 | 588.0 | 0.467 | 0.12 | FAIL S |
| 0 | 30, 100 | 1.0, 3.4 | 3.7e4, 1.2e5 | 416.8, 813.2 | 725, 1081 | 0.07, 0.05 | 0.007, 0.003 | FAIL |

**I expected this family to fail at every Γ, and it didn't.** Mean density at z 1100 is 44 M☉/pc³, nearly a thousand times a disc's, so Γ ≥ 1 is stiff at recombination as I said. But stiff isn't fatal: at z 1100 a c_s of 1000 km/s has k_J near 1 /Mpc, above the CMB's scales. So density-keyed exclusion isn't killed by gate 1. It fails at the two ends, Γ 7/3 and Γ 0.

## Ceilings, largest c_s passing (km/s), by fit where the frozen rule fits; grid top means no ceiling found
| Family | Reads |
|---|---|
| Window z > 3000 | ≥ 1000, grid top |
| z 500-3000 | ≥ 1000, grid top. S − S_min 0.5 |
| z 50-500 | ≥ 1000, grid top. 6.4 |
| z 5-50 | 100 to 1000 (fails at 1000, 61.8) |
| z < 5 | 100 to 1000 (fails at 1000, 101.0) |
| Late switch, z < 50 | ≥ 300, grid top. 14.7 |
| c_s constant, N = 0 | ≥ 300, grid top. 15.3 |
| c_s ∝ a⁻¹, N = 1 | c0 1 to 2 (6.0 pass, 28.7 fail). VW1's FD edge is 2 to 4 |
| c_s ∝ a⁻², N = 2 | below 0.25, all fail; the grid was misplaced (A1); the fit at 0.25 is unconverged |
| c_s ∝ a, N = −1 | ≥ 1000, grid top. 16.3 |
| w, c_s 0 | −1e-3 passes (5.4). +1e-3 and +3e-3 clear S (1.1, 14.6) and fail G-A0. −3e-3 fails S (40.6) |
| c_vis, N = 0 | ≥ 100, grid top. 0.4 |
| c_vis ∝ a⁻², N = 2 | below 0.5, all fail. Fit at 0.5 S 4285.9 |

So what gate 1 limits is growth in the last 50 redshifts, plus any stiffness that rises steeply into the past.

## What this doesn't clear
- **Forest, not graded.** X22's c_s ≤ 6 km/s at z 3 is met only by the Γ 5/3 cells (about 1 and 3.5 km/s); Γ 1 and Γ 2/3 miss it. But those Γ 5/3 cells also carry a cut set early: P halves at 1.89 and 0.54 h/Mpc at z = 0, inside or below the forest's range. RF5's own diagnostic says such early cuts matter there. The raw P1D forward model wasn't run. It's the next test for this family, and I expect it to be hard on σ 100.
- **The anchor isn't exclusion.** c_s = σ at ρ_disc is a requirement I posited, not a solved hydrostatic disc. A bound Γ > 1 fluid compresses until c_s is about the local V, so its density sits *near* ρ_disc, comparable to baryons, not far below. Holding it to a small share likely needs σ higher, or the anchor lower, and that moves up the table toward the failing cells. Not computed.
- **The same barotrope in clusters.** Γ 5/3, σ 100 has c_s about 34 km/s at 2e-3 M☉/pc³, so it's cold there, then compresses until c_s reaches the cluster's speed, near 50 M☉/pc³. That's a small dense core, not X-COP's profile, by rough arithmetic only.
- **Standing kills, from the record, not re-derived:** the Bullet Cluster on any pressure fluid (X19); BOLTZ1 Part B's pressure core excluded within shift-symmetric P(X), and its no turn-on; AN1, which folds before hydrostatic settling in its reduced system. A Γ 5/3 fluid is also the thermal history of VW1's slow fermion, c_s ∝ a⁻¹, with collisions added. Nothing here gives those collisions a source.
- **Simplifications.** Barotrope w from c_s is neglected (about 6e-6 at z 1100 for Γ 5/3, σ 100; about 5e-5 at z 3000; it grows into the past and reaches order 0.05 near z 1e5). c_s capped at c/√3. Adiabatic initial δ isn't corrected for w. Γ 0's P isn't increasing. c_vis's normalisation differs among papers by order unity. No BBN check.
- **Screen rule.** Six cells above the P 2000 limit or above a family's next-up cell were not fit; a screen read is never a pass, and failing cells could lower with a fit (W ±3e-3 lowered by an order of magnitude). P Γ 7/3 at screen S 22989 and up wasn't fit under the frozen limit: read as fail by screen, a limit of this method.

## Variables left (`df2_analytic.out`, order of magnitude, mode k 0.1 /Mpc at recombination)
| Variable | Recombination | Disc | Cluster | Status |
|---|---|---|---|---|
| Density, M☉/pc³ | 44 | 0.05 | 2e-3 | this lane, passes gate 1 at five cells |
| Acceleration, m/s² | 3e-9 | 1.3e-10 | 6.5e-11 | no separation of recombination from discs here; X60 and X19 on systems |
| \|∇ρ\|/ρ, /Mpc | 0.11 | 333 | 3.3 | gives recombination < cluster < disc. No lane in the record has graded it that I found. Higher-derivative, no action |
| Phase density, M☉/pc³/(km/s)³ | ≥ 4e-9 | 5e-8 | 2e-12 | VW1: no window on the Υ floor; conserved, not a local switch |
| Entropy | none assigned | | | conserved on smooth flow; keys on history, needs a process |

## Controls
K_rf5: c_s 0, Newtonian, reproduces RF5's cell (plik −0.002, shear −0.003, BAO, SN under 0.001; σ8 0.8261 against 0.8260). K_patch_zero d 0. K_jeans k_half/k_J 1.31 at c0 30. MUTATE as frozen **failed its line** (plik −0.09: no teeth at c0 30). Replacement under post-result A1: the flip stops CLASS at N = 1, c0 4, where the unflipped plik is 954. The frozen rule says a failed control means NO VERDICT; the label above stands on that replacement, disclosed. Fluid against VW1 FD at about 2 km/s: S 28.7 against 22.3, no line.

## Departures
Lane is DF2, since DF1 was taken. A1 as above. Fit-job scheduling fix before any fit. Cells below the bracket in each family carry the screen read only.
