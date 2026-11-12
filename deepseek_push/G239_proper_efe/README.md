# G239 — the proper external field: QUMOND EFE solve for the Milky Way's phantom halo

**Why.** DW1 (`closure_2026_11_11/DW1_desi_dr2_mw_mass/`) found the external field to be the dominant
modelling uncertainty on the framework's MW mass: with the scalar-additive approximation
`ν((g_bar + g_ext)/a₀)` the 80 kpc prediction fell to 4.31×10¹¹ (−4.1σ) and the 13-point DESI profile
degraded to 7.0% rms, while with no field it was 5.69×10¹¹ (−1.34σ) at 2.9% rms. That approximation is the
**maximum-suppression** case — it adds the external field to the internal one in the same direction
everywhere. The real EFE is a vector sum.

**What this lane does.** The exact QUMOND monopole integral, with no approximation beyond QUMOND itself:

```
g_N(r,θ) = g_b(r) r̂ + g_ext ẑ ,   |g_N|² = g_b² + g_ext² + 2 g_b g_ext cos θ
g_r(r,θ) = ν(|g_N|/a₀) (g_b + g_ext cos θ)
⟨g_r⟩(r) = ½ ∫₋₁¹ dμ  ν(|g_N|/a₀) (g_b + g_ext μ)          M_dyn(<r) = r²⟨g_r⟩/G
```

The uniform external field's own contribution integrates to zero, so `M_dyn(<r)` is exactly the mass a
spherical Jeans analysis would credit to the Galaxy sitting in that field.

**Instrument checks (all exact limits):** `e_N = 0` reproduces `ν(g_bar/a₀)M_b` to 1e-9 (DW1's law); a
constant kernel returns `2.5 M_b` with no anisotropy and no field dependence; the proper average lies
strictly between the no-EFE and scalar-additive values at all 12 (footing, field, radius) combinations.

## Results at the repo's own Local-Group field, e_N = 0.01273 (hunt item 81)

| | canonical | alt | DW1's scalar-additive hack |
|---|---|---|---|
| M(<80 kpc), A = 1 | 4.98×10¹¹ (−2.77σ) | 5.11×10¹¹ (−2.50σ) | 4.31 / 4.51 (−4.11 / −3.70σ) |
| 13-point fit, χ²/dof | 0.38 (rms 3.3%) | 0.49 (rms 4.0%) | 1.37 (rms 7.0 / 7.8%) |
| amplitude A* | 1.360 ± 0.035 | 1.205 ± 0.030 | 1.505 / 1.360 |
| M(<200 kpc), A = 1 | 5.26×10¹¹ | 5.27×10¹¹ | (naive ν(e)M_b = 6.27×10¹¹) |
| M(<200 kpc), at A* | 7.16×10¹¹ | 6.35×10¹¹ | — |

**Verdict: 8/8 checks PASS, and two DW1 statements are corrected.**

1. **The hack over-suppressed by 16% (canonical) / 13% (alt).** The EFE tension at 80 kpc is real but
   modest: −2.77σ / −2.50σ, inside 3σ on both footings.
2. **DW1's "the EFE spoils the shape" is withdrawn.** With the proper EFE the profile fits at 3.3% rms
   (χ²/dof 0.38), not 7.0%. The degradation was the approximation, not the data — so the earlier reading
   "the profile prefers a weak external field" loses its main support (the rotation curve's `e_N = 0.000
   [0, 0.008]` and the LMC bound still stand, on their own).
3. **The plateau is LOWER than the naive cap.** `ν(e_N)M_b = 6.27×10¹¹` (item 38's cap) overestimates by
   16%: the angle average costs a further 16%, giving 5.26×10¹¹. Against the paper's own NFW extrapolation
   of 11.35×10¹¹ at 200 kpc the split is **2.2× (A = 1) to 1.6× (A\*)** — the ARMED falsifier (row 32)
   gets stronger, and the registered kill `M(<200 kpc) ≥ 1.0×10¹²` remains untouched even at the
   RC-preferred weak field (`e_N = 0.008` → 6.54×10¹¹).

## The anisotropy — a real caveat, and a DR4 test

The angle average converges past `r_EFE` (×1.06 from 80 to 150 kpc) while the **parallel** direction
diverges (×2.7): along the field the external acceleration itself gets credited to the Galaxy. At 80 kpc
the parallel and perpendicular readings differ from the average by +58% and +1%. So a spherical Jeans
analysis is unbiased only for an **angle-isotropic** tracer sample. That is testable: split the halo
tracers by angle to the Local Group's field direction (Gaia DR4 class), the same azimuthal channel item 81
priced at 0.3–1.4% on the rotation curve.

## Honest limits

- QUMOND (the algebraic kernel). h34's own AQUAL solve finds the algebraic boost ~15% high, so the EFE
  suppression here is, if anything, **understated** and the plateau correspondingly overstated.
- The external field is uniform and static; the LMC's contribution to it is neglected.
- `A` remains a nuisance, not a derivation; `κ = 1/2` stays **FITTED**.

Files: `g239.py`, `g239.out`, `g239_results.json`.
