# CFG772 FROZEN CRITERIA: laboratory tests (torsion balances, G measurements, free-fall balances) under the framework's action

Committed alone, before any script or number. 2026-10-14. Block CFG770–779.

## Question
What does the framework predict for each existing or proposed laboratory test below a0, in each of its three forms?
- (F1) the committed stiffened action (L* = 5.75 pc to 1 kpc);
- (F2) the action without stiffness (γ = 0, local, AQUAL-type);
- (F3) γ = 0 plus the free-fall-basin rule (CFG693).

Do any existing data test it? Seal a prediction that can kill it.

## Tests (each a declared calculation)
- **L1, Gundlach et al. 2007** (Newton's second law at 5e-14 m s⁻²). The framework modifies gravity, not inertia. The
  pendulum's restoring force is elastic. Prediction: an exactly Newtonian response in F1–F3 (symbolic statement plus a numeric
  check of the gravitational anomaly from the lab surroundings).
- **L2, a Cavendish-type G measurement (Quinn et al. 2013/2014 geometry).** Source 4 × 11 kg at about 0.214 m; test
  4 × 1.2 kg at about 0.12 m. The geometry is quoted from memory, so provisional; the verdict must be robust to ×10.
  Compute δG/G:
  - F1: the screened anomaly G M_s/L*², relative to G M_s/r².
  - F2: linear response about Earth's field. Anisotropy L_E = a0/(g_E + a0) and μ_E ≈ g_E/(g_E + a0) give
    δG/G ≲ a0/g_E.
  - F3: the source mass is supported, not free-falling. In the lab's free-fall frame, its basin radius is
    r_J = √(G M_s/g_E).
  - Compare with Klein's model, as used by Scarpa et al. 2026: F = [1 + (a0/a_N)^β]^{1/(2β)}, β = 1.3, a0 = 1.2e-10,
    applied to the source field alone. Their stated prediction is G = 6.6769 vs 6.6747 for half / twice the source
    acceleration.
- **L3, free-fall torsion balances** (Das & Patitsas 2013; drop tower / LEO / interplanetary).
  - In F3, a test body of mass m has its own basin r_J = (G m/T)^{1/3} in a tide T.
  - It shows a boost only if r_J exceeds its MOND radius r_M = √(G m/a0), i.e. m < a0³/(G T²).
  - Compute this mass ceiling for: drop tower (Earth tide at the surface), LEO (400 km), and interplanetary space at 1 AU
    (solar tide).
  - F1: the boost is suppressed by the stiffness in all three cases. Compute the anomaly for m = 1 kg at r = 0.1 m.

## Sealed prediction (the output of this lane)
A repeat of a Cavendish-type experiment that changes the source acceleration by ×4 must show |ΔG/G| below the F1/F2/F3
maximum. The framework, in every form, is **EXCLUDED** if such a repeat finds |ΔG/G| ≥ 1e-6 that is attributable to the
source acceleration. This is the declared kill line; all three forms predict far below it.

## Controls
- K1: Newtonian limit (a0 → 0) gives δG/G = 0 in every form.
- K2: Klein's F reproduces Scarpa et al.'s own two numbers for the Quinn variants to 2e-4 relative, given the
  source-acceleration ratio and the Newtonian G = 6.6742. If it does not, report the discrepancy and do not use their numbers.

## MUTATE (CFG772_MUTATE=1)
- M1: Earth's field switched off in F2. δG/G must rise toward Klein-like values, ≥ 1e-6.
- M2: L* → 1e-4 pc in F1. The anomaly must rise by (5.75e4)².

## Hand estimate (before any script)
- F1: δG/G ~ (0.2 m / 5.75 pc)² ~ 1e-36.
- F2: ~ a0/g_E ~ 1e-11.
- F3: r_J ≈ 9 μm, inside the source mass, so no node: null.
- Klein: ~1e-4.
- L3 mass ceilings: drop tower ~ 1e-9 kg, LEO similar, 1 AU ~ 1e6 kg.

## Disclosures fixed now
- The Quinn geometry and LPF-like numbers are from memory (provisional); orders of magnitude only.
- No raw G-measurement table is scored: no per-experiment source accelerations are available in the record. Stated, not
  hidden.
- κ fitted; not theory closed.
