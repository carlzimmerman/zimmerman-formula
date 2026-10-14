# CFG775: black holes, cold energy, dark energy and the horizon

**Label:**
- **A: ONE COINCIDENCE.** Every black-hole / horizon / a₀ / tether relation is a fixed function of q = a₀/(cH∞) = 0.1727.
- **B1: EXCLUDED.** Stellar-remnant black holes cannot be dark energy's source: they would need 3.8–4.6× all the mass ever
  formed into stars.
- **B2: the timing nearly matches DESI** (within 0.017–0.029 dex), but DIFFERS by the frozen 0.02-dex line at z_max = 8.
- **B3: SEALED.** sha256 `3d2363782783e9ca4190afdb607162b2d14c00e257b8823ffb1bdf5af8d3249e`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (d5c63f856). Block CFG770–779.
- **Script:** `python3 cfg775.py` (seconds, exit 0). `CFG775_MUTATE=1` (k = 0) exits 1 as designed. M2 (ε-free shape) passes
  in-run.

## A. Geometry: one number

| relation (both footings identical) | value | from q |
|---|---|---|
| MOND radius r_M / √(r_s R_H) | 1.7013 | 1/√(2q) |
| tether capacity a₀/πG ÷ horizon surface density M_H/4πR_H² | 1.3820 | 8q |
| same, projected (M_H/πR_H²) | 0.3455 | 2q |
| mass of the BH whose surface gravity is a₀, ÷ horizon mass c³/2GH∞ | 2.8944 | 1/(2q) |
| a₀ ÷ the de Sitter horizon's surface gravity cH∞ | 0.1727 | q |
| Nariai mass ÷ M_H | 0.3849 | 2/(3√3) (no a₀) |
| MOND radius of the horizon mass ÷ R_H | 1.7013 | 1/√(2q) |

**Reading.** Each of these is the single statement "a₀ ∝ cH∞" re-expressed. The MOND radius of any mass is the geometric
mean of its Schwarzschild radius and the cosmic horizon. The tether's capacity is the horizon's own surface density. a₀ is
17% of the horizon's surface gravity. These are real and pretty, but they are one coincidence, and the record already works
it (κ is not derivable from the horizon: equation book, 32π campaign). No horizon relation fixes q, and none touches cold
energy's amount (5.364).

## B. Are black holes the source of dark energy? (cosmologically coupled BHs, k = 3)

| z_max | ∫ψ(1+z)³dt (M☉ Mpc⁻³) | ε_req (BH mass / star mass formed) | a₀(z)/a₀(0) at z 0.5 / 1 / 1.5 / 2 / 2.5 |
|---|---|---|---|
| 8 | 2.05e10 | **4.60** | 0.993 / 0.970 / 0.923 / 0.851 / 0.769 |
| 15 | 2.31e10 | **4.07** | 0.994 / 0.974 / 0.932 / 0.870 / 0.799 |
| 30 | 2.45e10 | **3.85** | 0.994 / 0.975 / 0.936 / 0.877 / 0.811 |
| DESI CPL (record's F-DESI) | | | 1.032 / 0.989 / 0.931 / 0.874 / 0.822 |

- **The amount fails decisively.** ρ_DE0 = 9.4e10 M☉ Mpc⁻³. Even with the (1 + z)³ boost, black holes from the observed star
  formation history supply at most a few × 10⁻³–10⁻² of that (ε ≲ 0.01–0.05). The factor needed is about 80–400× beyond any
  IMF, and ε > 1 is impossible outright. A generous Pop III population adds only 1.2%.
- **The timing nearly matches DESI.** DE built by black-hole formation weighted by (1 + z)³ rises over cosmic time almost
  exactly as DESI's w₀w_a fit does at z ≳ 1: 0.92 vs 0.93 at z = 1.5, 0.85–0.88 vs 0.87 at z = 2. This reproduces Croker et
  al.'s (2024) shape claim. The one real miss is DESI's ρ_DE > 1 at z ≈ 0.5 (its phantom crossing), which a monotone
  production history cannot make.
- **For the framework:** a₀(z) = κc√(Gρ_DE(z)) would then follow the black-hole history. But that branch is
  indistinguishable from F-DESI in the sealed ALMA tests: GS4_24110 required gas within 0.0–0.2 dex of F-DESI. So ALMA
  separates "flat" from "evolving" dark energy, not black holes from other sources of evolving dark energy.

## B3. Sealed (before the 2026-11-06 / 11-28 releases)
r_BH(1.419) = 0.932, r_BH(1.997) = 0.852. GS4_24110 required log M_gas:

| logM* | canonical: BH / DESI / flat | alt: BH / DESI / flat |
|---|---|---|
| 10.89 | 9.87 / 9.82 / 9.46 | 9.31 / 9.11 / FLOOR |
| 10.76 | 10.44 / 10.43 / 10.36 | 10.34 / 10.33 / 10.24 |

U4_27928 is conditional on V_c; it gives FLOOR below 225 km/s. The full grid is in `SEALED_BH_BRANCH.json`.

## What this means for the owner's idea
- The geometric link between black holes, the horizon and a₀ is real but single: everything is a₀ ≈ 0.17 cH∞.
- The physical link "black holes make dark energy" has the right *timing* but about 100× too little *mass* from stars.
- Cold energy (Ω_c ≈ 5.4 Ω_b) shows no geometric tie to either.

## Disclosures
- Measured BH masses are taken as the coupled masses (the k = 3 literature's convention).
- MD14 is a fit to observed luminosity densities, using a standard luminosity-distance cosmology and Salpeter mass units
  (Chabrier would lower the stellar mass by ×0.63 and raise ε_req).
- dt/dz uses a constant-ρ_DE expansion; the DE evolution's effect on dt is second order.
- The DESI CPL values are the record's (CFG571).
- κ fitted; not theory closed.
