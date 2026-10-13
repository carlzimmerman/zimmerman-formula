# CFG742 — can a "warm" cold component be the two-sector selector? (frozen criteria, committed alone; order-of-magnitude)

Block CFG740–749. Written before any CFG742 number. κ = ½ fitted; both footings; the cold energy's mass is required; no
particle species; not theory closed.

## Why
CFG741 closed P-wave heating and left two options for keeping the cold component C out of galaxies but in clusters:
- a velocity scale σ_C ≈ 250–700 km/s (above galaxy, below cluster dispersions);
- a baryon-fraction or gas-state dependence.

This lane tests the first. C must be cold at recombination (CMB), so σ_C must be acquired late. Whatever its origin, today it
sets a Jeans scale below which C cannot cluster linearly.

## Test
- **J.** λ_J(z) = σ_C √(π/(G ρ̄_m(z))), comoving λ_J(1 + z).
  - Inputs: ρ̄_m = (Ω_m/Ω_Λ) ρ_Λ, with ρ_Λ from each footing (a₀ = κc√(Gρ_Λ)), Ω_m = 0.309, Ω_Λ = 0.686.
  - Evaluate at σ_C = 250, 400, 700 km/s and z = 0, 0.5.
  - **Selector viable iff comoving λ_J ≤ 2 Mpc (cluster scale) for some σ_C in the window at z ≤ 0.5.** Otherwise C is smooth on
    every scale KiDS/DES shear probes (k ≳ 0.1 h/Mpc), and the record's D2 requirement fails for this route.
- **Reported:** the linear shear-power factor on scales k ≫ k_J if only baryons cluster, (Ω_b/Ω_m)², as an order of magnitude
  against the record's absolute KiDS levels (CFG624 NCE σ₈ ≈ 0.01, χ² 226 / 51).

## Verdict
VIABLE / CLOSED. Not claimed: nonlinear retention of C in clusters, where σ_cluster > σ_C would bind it. That does not restore
linear power on group and galaxy scales.

## MUTATE (`CFG742_MUTATE=1`, exit 1 iff it bites)
σ_C = 5 km/s (genuinely cold): λ_J must drop below 2 Mpc.
