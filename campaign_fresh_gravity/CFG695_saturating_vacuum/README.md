# CFG695: a vacuum whose polarization saturates at a₀

**Label: SATURATING VACUUM PASSES C2 on both footings (0.1009 @ Υ 0.60; 0.0994 @ Υ 0.55). Structure and stability PASS;
Solar-System carry-over PASS. R0-SHAPED (saturation). Post-hoc in origin (disclosed).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (dd0f52abe), before any CFG695 number.
- **Script:** `cfg695.py`, about 30 s, exit 0 → `cfg695.out`, `cfg695_results.json`. `CFG695_MUTATE=1` exits 1 (both bite).
  Controls reproduce CFG4's ν_mono and CFG690's T3.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory
  closed"; nothing here says the data favour the framework.

## Results

| test | result |
|---|---|
| **S1** structure | W(u) = −(a₀/4πG)[u + a₀ ln(1 − u/a₀)] expands to the critical quadratic + SI cubic + c₄ = 1 quartic, exactly. Resummed: u = a₀g/(a₀ + g), **g_N = g²/(g + a₀)**: deep coefficient exactly a₀, polarization saturates at u → a₀. Stable for every u ∈ (0, a₀) (W″ = 4πG a₀²/(a₀ − u)²). PASS |
| **S2** raw SPARC | **canonical 0.1009 dex @ Υ 0.60; alt 0.0994 @ Υ 0.55** (ν_mono 0.1003 @ 0.61 / 0.0991 @ 0.57; CFG690 cubic 0.1012 @ 0.46 / 0.1007 @ 0.42). PASS |
| **S3** Solar System | screened inner anomaly u/a₀ = 4.5e-5 / 3.7e-5 at L* = 5.75 pc: saturation is negligible, so CFG691 carries over. PASS |
| S4 (reported) | u ≤ a₀ ⇒ mean phantom surface density ≤ a₀/πG = 214 / 258 M☉/pc² (twice the record's Σ_M = 107 / 129) |
| MUTATE | saturation at 2a₀ breaks the deep coefficient; ν = 1 gives 0.2755. Both bite |

## Reading
1. **One physical postulate fixes the whole interpolation: the vacuum's gravitational polarization saturates at a₀.**
   - Its expansion supplies the scale-invariant cubic (so the deep law follows).
   - Its resummation supplies the transition that SPARC wants, at a normal stellar M/L.
   - It needs no constant beyond a₀ itself.
   - Dielectric saturation (Langevin-type) is ordinary physics in other media; that is the analogy, not a derivation.
2. **What is not new.** The static law it produces, g_N = g²/(g + a₀), is the long-known "simple μ" interpolation, so a good
   SPARC fit was to be expected. What is new is that a single saturating, critical, gravitating polarization field produces it,
   together with lensing, the mass ledger, stability, stiffness screening and free-fall basins (CFG691–694).
3. **Honest limits.**
   - **Post-hoc origin.** Saturation was recognised after CFG694's c₄ scan landed on 1. The resummed form was frozen before
     scoring, but the idea was seen in the data.
   - **R0-SHAPED.** Saturation is a postulate chosen to give a law shape.
   - **Not re-scored here:**
     - PAPER44's satellites, scored with the quadrature law; in the deep regime the two agree.
     - CFG529 early types (C3).
     - CFG596 growth (D2).
     - Clusters.
   - **Open:** the attractor (M1a), the basin reading as an action (B1), the relativistic completion (Φ = Ψ), and κ fitted.
