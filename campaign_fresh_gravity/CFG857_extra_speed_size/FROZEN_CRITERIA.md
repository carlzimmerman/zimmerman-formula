# CFG857 FROZEN CRITERIA: does the extra speed V_x depend on size, and does that remove the MW/M31 offset while still passing SPARC? (before any script)

**Why.** CFG856: an extra isothermal speed V_x ≈ 9.4 km/s on top of the law passes SPARC out of sample, but M31 satellites want
14.3 km/s (z 2.7). M31's satellites are larger. If V_x ∝ r^β, the extra mass is M_x(<r) = V0² r (r/r0)^{2β}/G (r0 = 0.3 kpc).

## Steps
1. Over all dwarfs with an excess (CFG856's set; MW + M31 + field), least squares log V_x = a + β log10(r_1/2/0.3 kpc) + c [M31]; and
   the same without the host term. Bootstrap σ (2000, seed 857).
2. **Host offset at fixed size:** c must be within 2σ of 0 (else the offset is not a size effect).
3. **SPARC re-test with the size-dependent form** (CFG856 sample, canonical a0, ν_e): Δ_pred(r) = log10[(g_law + V0² (r/r0)^{2β}/r)/g_law]
   with a, β from step 1 (no host term); D = mean over galaxies of median(Δ_obs − Δ_pred). PASS if |D| < 0.05 dex and ≤ 2σ_D.
## Classes
- **SIZE LAW WORKS** if β ≠ 0 at ≥ 2σ, the host offset vanishes (step 2), AND SPARC passes (step 3).
- **SIZE LAW FAILS SPARC** if steps 1–2 hold but SPARC fails (the size-dependent extra over-predicts rotating dwarfs).
- **NO SIZE DEPENDENCE** if β is consistent with 0 (|β| < 2σ). **OFFSET REMAINS** if c stays ≥ 2σ.
- Alt footing reported.

## Controls
- K1: β = 0 with a = CFG856's MW calibration reproduces CFG856's SPARC D (+0.017). MUTATE (separate output): r_1/2 shuffled across
  dwarfs → β must become consistent with 0.

κ = ½ fitted; cold energy mass required; not theory closed.
