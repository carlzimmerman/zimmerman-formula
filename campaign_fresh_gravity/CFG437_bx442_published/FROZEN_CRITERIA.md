# CFG437 FROZEN CRITERIA: BX442 (z = 2.18 grand-design spiral, Law et al. 2012) from its published numbers. Flat a₀ or a₀ ∝ H(z)?
(owner 2026-10-07: "yeah bro swing it". Disclosure: a back-of-envelope estimate was made in chat before this freeze; the rule below is fixed regardless of it.)

**Inputs (Law+12 Supplementary table, read from the PDF and matched by position):**
- M* = 6 (+2, −1) × 10¹⁰ M⊙;
- M_gas = 2 (+2, −1) × 10¹⁰ M⊙ (inverted from the star-formation law, which is the calibration wall);
- V_rot = 234 (+49, −29) km/s at R = 8 kpc;
- σ = 71 ± 1 km/s;
- half-light radius ≈ 5 kpc.

**Method.**
- The law is g_obs = g_N ν(g_N/a₀) with ν_mono. Solve for the implied a₀.
- g_N = G M_b/R² (spherical enclosed). A thin-disc factor of 1.1–1.3 is reported only.
- g_obs = V_c²/R, read two ways:
  - (A) V_c = V_rot;
  - (B) V_c² = V_rot² + 2σ²(R/R_d), with R_d = r_half/1.68.
  - These are never pooled.
- 20,000-draw Monte Carlo with split-normal errors.

**Predictions at z = 2.18.**
- FLAT: a₀ = 9.36e-11 (canonical) / 1.13e-10 (alt).
- Rival: a₀ × H(z)/H₀ = 3.29×, i.e. 3.08e-10 / 3.72e-10.

**Decision, per reading (A, B).** From the median and the 16–84% interval of log a₀:
- **FAVOURS FLAT:** the interval includes the flat value and excludes the rival.
- **FAVOURS H(z):** the reverse.
- **NOT DIAGNOSTIC:** it includes both, or neither.

**Lane verdict.** If readings A and B give different classes, the lane is NOT DIAGNOSTIC (pressure-support systematic). One galaxy can never establish evolution (record rule: a lean is not a detection).

**MUTATE.** V_rot × 1.81 (= √3.29). This must move reading A's class toward H(z).
