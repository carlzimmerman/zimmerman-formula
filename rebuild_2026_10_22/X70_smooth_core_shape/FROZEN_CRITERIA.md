# X70_smooth_core_shape: FROZEN CRITERIA (committed alone, before any script or graded number)

**Source:** the external model's proposal (relayed by the owner, 10-29, "keep pushing"). Burkert's linear (1 + x) factor
gives dρ/dr ≠ 0 at the origin. Replace the Burkert halo with the smooth core ρ = ρ₀/(1 + x²)^(3/2) (x = r/r₀), which
has zero central slope and the same r⁻³ tail.

**Standing:**
- κ = ½ FITTED. Footings never pooled.
- c_f = 4 EXTERNAL.
- Not "theory closed". Nothing here may say the data favour the framework.

**Already in the record (not re-run):** CFG408's measured-f★ regrade leaves X-COP CONSISTENT and worsens G-OUT-M3
(ungraded; its K2 failed).

## Hypothesis SC

X43 with every Burkert enclosed-mass call replaced by the smooth core:

M(r) = 4π Σ r₀² [asinh(x) − x/√(1 + x²)]

The X43 code's B(x) becomes B_S(x) = 4[asinh(x) − x/√(1 + x²)].

**PRIMARY (consistent).** X43's η comes from matching the halo's enclosed mass at r₀ = r_f/c_f to the infall profile,
η = (4/(3 B(1))) c_f^(5/4). With the smooth shape, B(1) becomes B_S(1) = 4[asinh 1 − 1/√2] = 0.69707, so
η_S = 14.83 × 0.50865/0.69707 = 10.82. Nothing else changes: the floor a₀/(2πG), the mass normalization and the grading.

**REPORTED (not graded):** the shape swapped with η kept at 14.83.

## Checks (all must pass, else UNDECIDED, exit 1)

- **K0:** with the Burkert shape restored, the script reproduces X43's committed SPARC rms, groups Z and every cluster
  pred on both footings to 1e-6.
- **K1:** B_S(x) matches quadrature of the smooth density to 1e-6; a solved r₀ returns the target mass to 1e-8; η_S
  equals 14.8286 × B(1)/B_S(1) to 1e-6.
- **K3:** peak RSS < 2 GB.

## Verdict (per footing; the class needs both to agree)

- **SC PASSES:** SPARC line on both backgrounds, all 15 cluster keys |Z| ≤ 2, and groups CONSISTENT.
- **SC FAILS:** <keys with sign>.

**Reported:** every key's Z against X43's.

**Out of scope:** the native-c_f residual G-IN-Mall (X48) waits for the A4 zooms.

MUTATE: shape (1 + x²)^(−1) × (1 + x)^(−1) with exponent 1 replaced by 2 in the first factor, i.e. Burkert again. It must
reproduce X43 exactly, confirming the switch is the only change.
