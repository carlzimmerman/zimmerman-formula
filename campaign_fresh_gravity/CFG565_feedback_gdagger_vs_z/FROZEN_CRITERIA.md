# CFG565: which way does ΛCDM-with-feedback move the RAR's acceleration scale with redshift? The sign test against a₀ tracking ρ_DE. FROZEN before any script exists

Owner chat 10-09 (the final council session). κ = ½ fitted; both footings for the framework rows. ΛCDM is the comparator.

**Why.** Council synthesis: the "box" (an active, outward, nonlocal arranger keyed to baryons) has the properties of baryonic feedback acting on cold matter, and CFG477 showed the DC14 recipe nearly reproduces the z = 0 RAR (g† 9.7e-11). The question that separates "feedback arranges it" from "a₀ is tied to Λ" is the **sign** of g†(z).

**Model.** CFG477's machinery (the same SPARC baryon curves, noise, statistic with a₀ free, DC14 response, 0.15 dex SHMR scatter, 0.11 dex c-scatter), evaluated at z = 0, 1, 2, 2.5 with:
- **Moster+13 z-dependent SHMR:** log M₁ = 11.590 + 1.195 z/(1+z); N = 0.0351 − 0.0247 z/(1+z); β = 1.376 − 0.826 z/(1+z); γ = 0.608 + 0.329 z/(1+z).
- **Dutton & Macciò 2014 c(M, z):** log c₂₀₀ = a + b log(M/10¹² h⁻¹), with a = 0.520 + 0.385 exp(−0.617 z^1.21) and b = −0.101 + 0.026 z. The halo is defined at 200 ρ_c(z), with E(z) for Ω_m = 0.315.
- **Galaxy size evolution** (declared): radii scale by s = (1+z)^−0.75 at fixed baryonic mass, so g_bar(r) → g_bar(r/s)/s², at radii r·s.
- DC14 is used at its z = 0 calibration (declared limitation).
- 100 realisations per redshift, seed 565.

**Output.** The emergent g†(z)/g†(0) and its spread, against:
- the framework, a₀ tracking ρ_DE (the record: DESI-like ≈ 0.87 at z = 2, 0.78–0.83 at z = 2.5);
- a flat a₀ (1.0);
- a₀ ∝ H(z) (E(z) = 1.77 / 3.0 / 3.7 at z = 1 / 2 / 2.5).

**Verdict.**
- **FEEDBACK RISES** if g†(2.5)/g†(0) > 1.3 in ≥ 84% of realisation pairs. That is opposite in sign to the framework's prediction, so the high-z a₀ test separates them cleanly.
- **FEEDBACK FLAT** if 0.85 ≤ ratio ≤ 1.15 (16–84%): the test does not separate them.
- **FEEDBACK FALLS** if the ratio is < 0.85, the same sign as the framework.
- Otherwise INTERMEDIATE.
- The record's Magneticum note (an apparent a₀ rising ×2.3–3 by z ≈ 2; CFG1) is a prior expectation, not an input.

**Controls.**
- K1: at z = 0 the machinery reproduces CFG477's g† 9.69e-11 within 3% (different seed).
- K2: the Moster z-terms vanish at z = 0.

**MUTATE (`--mutate`).** Freeze the halo at its z = 0 properties (no SHMR, concentration or ρ_c evolution; size evolution kept). The ratio must change by > 10% from the main run; exit 1 when it does.

**Compute.** Light; niced, BLAS threads 1.
