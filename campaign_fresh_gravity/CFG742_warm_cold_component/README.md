# CFG742: a warm cold component cannot be the two-sector selector

**Label: CLOSED.** A cold component with the dispersion needed to stay out of galaxies but sit in clusters (σ_C = 250–700 km/s)
has a comoving Jeans length of **23–96 Mpc** at z ≤ 0.5 on both footings. That is far above the 2 Mpc bar. It would be smooth on
every scale cosmic shear probes. Linear shear power would then come from the baryons alone, (Ω_b/Ω_m)² = 0.025 of the total
(amplitude × 0.16).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first.
- **Script:** `python3 cfg742.py` → `cfg742.out`, `cfg742_results.json`. `CFG742_MUTATE=1` exits 1: σ_C = 5 km/s clusters below
  2 Mpc.
- **Settings:** κ = ½ FITTED; ρ̄_m from each footing's ρ_Λ; the cold energy's mass is required; no particle species; not
  "theory closed".

| σ_C [km/s] | λ_J at z = 0, canonical / alt [Mpc] | λ_J at z = 0.5 [Mpc] |
|---|---|---|
| 250 | 34.3 / 28.4 | 28.0 / 23.2 |
| 400 | 54.8 / 45.4 | 44.8 / 37.0 |
| 700 | 95.9 / 79.4 | 78.3 / 64.8 |

## Reading
Together with CFG741, this closes both routes that rely on the cold component's own kinematics or energy. What is left for the
two-sector problem is a **dependence on the baryons' state**: something about gas or baryon fraction that keeps cold mass out
of galaxies. Nothing on the record supplies one yet. Nonlinear retention in clusters (σ_cluster > σ_C) is not claimed to
restore the missing linear power.
