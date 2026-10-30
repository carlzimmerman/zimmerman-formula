# X78_cgm_closure_regrade: FROZEN CRITERIA (committed alone, before any script or graded number)

**Question.** X77_cgm_budget found that the measured eROSITA hot CGM (Zhang+24) supplies the fair-share budget lensing
needs if it continues to ~2.8 R_vir, and that satellites need ~5 R_vir. Both numbers were budget-only and post-result.
This lane does the real regrade with the gas gravitating and the cut fixed by the measurement paper, not by us. Zhang
et al.'s own closure radius is R_c ≈ 3 R_vir, so k = 3.

Does route E (smooth core, fair share to the self-consistent r_ta) with that CGM pass KiDS lensing and GAMA satellites
in the stellar-mass range Zhang measure?

## Model (PRIMARY, nothing fitted)

Per lens or host of native log M★ = l, both models use the same baryons:
- **Stars and cold gas:** as F2/X53.
- **Hot CGM:** replaces F2's 0.5 M★ hot gas.
  - Shape: ρ ∝ [1 + (r/r_c)²]^{−3β/2}, with β = 0.43 and r_c = 6 kpc (Zhang Table 4, MW-mass).
  - Normalisation: M_hot(<R_vir) = 1.84 M★, Zhang's MW-mass central (0.12 · 1.3e12 − 5.5e10) / 5.5e10.
  - R_vir(l) is interpolated in log M★ from Zhang Table 1: (10.5, 178), (10.75, 210), (11.0, 295) kpc, flat outside.
  - The profile is cut at 3 R_vir.
- **(H) route E:** X76's fair share. M_b,tot = M★ + M_cold + M_hot(<min(r_ta, 3 R_vir)), with r_ta its self-consistent
  fixed point (X76 `rta_pc`). The halo M_fair = R_nat M_b,tot sits inside r_ta, with the X70/X73 smooth core and
  Σ = max(Σ_a0, ηΣ_coll).
  - z for r_ta: 0.285 for lensing, 0.1797 for satellites, as X76.
- **(L) law:** isolated AQUAL M_eff = M_b ν(g_N/a₀), with the same M_b(r) including the CGM.

## Grading (bins 3–4 = log M★ 10.6–11.0, inside Zhang's MW-mass bin)

- **Lensing:** X53 harness. For L2H and H2H, the sum of block-diagonal per-bin χ² over bins 3–4, all radii, with 2h
  (b fitted jointly as in X53). Report Δ = H2H − L2H with X53's class rule (≥ 9 LAW, ≤ −9 HALOS, else NOT DIAGNOSTIC),
  and the absolute H2H χ² for bins 3–4 (30 points).
- **Satellites:** X75's frozen measurement. χ² over bins 3–4 (2 points), pair-weighted, β_aniso = 0, X75's γ.

## Verdict (per footing)

- **CGM-CLOSURE HALOS PASS:** satellites χ²_H(bins 3–4) ≤ 6.0 **and** lensing Δ(H2H − L2H) < 9.
- **CGM-CLOSURE HALOS FAIL: <lines>** otherwise.

**Reported:**
- the law's χ² on the same lines;
- the generous and tight edges (normalisation 3.25 / 0.418, β 0.37 / 0.53);
- bins 1–2 with the same CGM ratio (an extrapolation below Zhang's range);
- cuts k = 2 and k = 5.

## Checks

- **K1:** with the CGM replaced by F2's 0.5 M★ (r/100 kpc)³ profile, my lensing reimplementation reproduces X76's
  fair-share H2H χ² (all radii) to 1e-6 relative.
- **K2:** with F2's hot gas, the law stack reproduces X53's L2H χ² to 1e-6 relative.
- **K3:** the CGM mass at R_vir equals 1.84 M★ to 1e-8.
- **MUTATE:** k = 1 (no gas beyond R_vir) must lower σ_sat(H) in bins 3–4.

κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
not theory closed; nothing here says the data favour the framework. One thread, nice 15. Zhang's M★ and R_vir are taken
as published (their SHMR/ΛCDM aperture; disclosed, as in X77_cgm_budget).
