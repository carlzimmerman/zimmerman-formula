# QX3 iter1: AC2q's clock cannot supply the CMB-lensing potential: FAIL (no-go)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (93562260e2).

- **C1 (Lean, `clock_jeans` in fable_independent_2026/lean_2026/QX3_dust_eos.lean):** a c_s^2 = 1 component with
  0 <= rho_phi <= rho_tot and 8 pi G rho_tot = 3H^2 has k_J^2 = 4 pi G rho_phi <= (3/2) H^2 (c = 1). It clusters only on
  Hubble scales. The MUTATE twin, which claims <= H^2/10, fails to build.
- **C2 (iter1.json):** the largest (k_J/k)^2 over L 8-400, z 0.1-10 and the six WG1 background corners.
  - With rho_phi = rho_DE (AC2q's clock is the dark energy): **0.0065**, at L = 8 and z = 2.45 (Omega_m 0.05). That is
    under the 0.05 line, so the label is **FAIL (no-go)**.
  - With the looser C1 bound (rho_phi = rho_tot, not AC2q's background): 0.18-0.45, only in the first band (L < 30) at
    z near 10, on 0.7-2 % of cells. At L >= 30 it is <= 0.035. Reported, not used for the label.
  - The frozen text names C1's k_J for C2 but says "on a framework-native background". Its natural reading is
    rho_phi = rho_DE; that ambiguity is disclosed here.
- **MUTATE** (`QX3_MUTATE=1`, c_s^2 = 1e-6): the ratio reaches 6.5e3, so the label flips to OPEN. The test sees a slow fluid
  when one is present.

**Meaning.** AC2q's only cosmological addition is the clock, and the clock adds at most about 0.6 % to the lensing potential on
graded scales. AC2q's CMB-lensing spectrum is therefore baryons plus the a0 law on the web, which WG2 already graded:
FAIL under every rule. AC2q cannot pass CMB lensing or linear growth without a clustering sector. Its clock's density
is also subdominant at z >= 1 (Omega_DE(z) is small), so it would not matter even if it clustered.
