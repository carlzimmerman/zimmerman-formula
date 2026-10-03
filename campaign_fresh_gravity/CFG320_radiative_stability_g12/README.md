# CFG320: gate G12 (radiative stability, Lorentz-violation leakage) on the filtered C-H/K chassis

Criteria frozen first: `FROZEN_CRITERIA.md` (commit 7d25a59e6). Script: `cfg320_radiative_stability.py`.
- Main run: `.out` and `_results.json`. 15/16 checks pass, 0 load-bearing failures, rc 0.
- MUTATE run: `_MUTATE.out` and `_results_MUTATE.json`. rc 1, as required.
- Each run takes about 15 s.

```
python3 campaign_fresh_gravity/CFG320_radiative_stability_g12/cfg320_radiative_stability.py
CFG320_MUTATE=1 python3 campaign_fresh_gravity/CFG320_radiative_stability_g12/cfg320_radiative_stability.py
```

## Verdict: CONDITIONAL (recipe section 6), by the frozen rule

The chassis is L340's: β = 0, α_c ∈ [9.62e-14, 3.2e-9], c₂ ∈ [7.29e-3, 0.0667], scored on a 9 × 9 log grid. At each
point the cutoff is that point's own strong-coupling scale, Λ_sc = √α_c M_P c_s^{-1/2} (XC1). Λ_sc runs from 8.48e8 GeV
to 3.56e12 GeV.

**(A) Naturalness: holds at every point.**
- α_c = c₂ = 0 is a symmetry point. There the khronon drops out and the action is GR plus matter, so loop corrections
  are proportional to the couplings. The derived propagator Lorentz violation (LV) carries an overall factor α·λ.
- Matter couples only to g, so pure matter loops cannot generate α or c₂.
- With generic mixing (c₂ may generate α) and N_g = 10, the largest correction is δα/α_c = 9.7e-7 and δc₂/c₂ = 1.4e-13.
- Closed form at Λ_sc: δα/α_c = N_g √(c₂ α_c (2+3c₂)/(2−α_c))/16π². This is small at every point, because the cutoff
  itself scales as α_c^{3/4}.
- Feedback from LV in matter at the bound: δα ≤ 8e-32.
- Reading only: with Λ = M_P (no hierarchy), δα/α would be 4e10, so the couplings would be unnatural.

**(B) LV leakage into matter: the EFT piece holds everywhere; the UV piece is the condition.**
- The scalar-sector graviton propagator was derived in-lane with sympy. The tensor and vector sectors are GR's at β = 0.
  The result is
  ΔW = −α λ (2k⁴σ + k²ρ + 3ω²ρ)² / [8k⁴(αλk² + α(3λ+2)ω² − 2λk²)].
- Its Euclidean phase-space average is eps_LV = α_c, to the precision printed. LV of size O(c₂) appears only inside the
  khronon cone ω_E > c_s k, which is a 1/c_s³ sliver of phase space.
- EFT leakage, δ_EFT = eps_LV Λ_sc²/(12π² M_P²) ln(M_P²/Λ_sc²): at most 1.5e-21, which is 40 times below the load-bearing
  bound of 6e-20 (Klinkhamer & Schreck 2008, 2σ upper side, PROVISIONAL). It passes at 81/81 points.
- Worst-case UV piece: assume O(1) LV enters at Λ_HL = Λ_sc, i.e. a Collins / Pospelov–Shang completion. Then
  δ_UV = 4.5e-20 to 4.8e-13. It passes at only 3/81 points, all at α_c = 9.6e-14 with c₂ ≥ 0.038.

**(C) The heat filter and the kernel: radiatively stable.** Both footings and both ξ floors were checked.
- Filtered MOND-vertex loops shift the kernel coefficients by at most 9e-41.
- The only unfiltered U vertex is C-H's quadratic term, so the unfiltered (∂U)⁴ operator comes only from graviton loops.
  At 0.1 AU it is 1.8e-105 of the Newtonian term.
- δξ/ξ ≤ 1.4e-14.

**The condition** (either form):
1. **Pospelov–Shang hierarchy.** The UV completion's anisotropic-scaling scale must satisfy M_* ≤ 9.9e8 GeV (and
   M_* ≤ Λ_sc). This number uses the strict scoring: reduced M_P, the log factor, and the 6e-20 bound.
2. **Sub-window.** Alternatively, restrict the window to Λ_sc(α_c, c₂) ≤ 9.9e8 GeV. That leaves essentially the
   α_c ≈ 1e-13 edge.

How the hierarchy depends on the bound (readings): it would be ≤ 1.2e7 GeV against Pospelov–Shang's quoted "1e-23"
(source not read), ≤ 1.4e11 GeV against 9e-16, and ≤ 1.7e13 GeV against 1e-11.

**Reading that would tighten things.** Suppose the EFT piece is scored with the unweighted maximum (the O(c₂)
khronon-cone value) instead of the phase-space average that a loop actually integrates. It then passes at only
23/81 points and falls under the same hierarchy / sub-window condition. The frozen rule uses the average.

## Controls (load-bearing; all pass)

| control | what was checked | result |
|---|---|---|
| K1 | Collins et al. 2004 eq. A.2, reproduced by a numerical one-loop integral (m = 0.01 Λ) | ratio 0.9974 for f = e^{−x²}, 0.9995 for f = 1/(1+x⁴); a Lorentz-invariant regulator gives ξ = 3e-15 |
| K2 | GR scalar-sector amplitude vs the covariant [T·T − T²/2]/(k² − ω²) | equal up to the constant 1/4 |
| K3 / K3b | α_c, c₂ → 0 | W → W_GR symbolically; at α_c = c₂ = 1e-20, eps_LV = 5e-21 |
| K4 | static limit for a density source | 1/(1 − α_c/2), the G_N of FP2 |
| K5 | propagator pole | ω² = c_s² k², L340/XC1's c_s |
| K6 | minimum Λ_sc over the window | 8.48e8 GeV, matching XC1's 8.5e8 GeV |
| K7 | doubling the θ sampling | eps_LV changes by 2e-10 |

**R1 (reading).** Pospelov–Shang's "Λ_HL ≲ 1e10 GeV for 1e-20" comes out at 1.3e10 GeV only with M = 1.22e19 GeV and no
log. Their stated reduced M_P with the log gives 3.9e8 GeV. The lane scores the stricter form.

## MUTATE (c₂ = 0.5)

The run fails part B through B0: 1.5 c₂ = 0.75 > 0.1, which is outside the BBN edge of the window. rc = 1. As
pre-registered, the leakage numbers themselves do not flag c₂ = 0.5: a larger c₂ lowers Λ_sc, and δ_EFT ≤ 2.6e-22.

## Departures from the frozen text (dated 2026-10-03, all on the conservative side or neutral)

1. **The LV measure.** The frozen text defined the LV measure as the ratio R = W_chassis/W_GR. That ratio is undefined:
   for density sources W_GR has a Euclidean zero at k² = 3ω_E², and for pure stress sources it vanishes identically.
   The lane uses Δ = ΔW_E/N_E instead, where N_E is the O(4)-invariant positive norm of the source over 4Q², with the
   same constant 1/4 as K2. The weighted mean is not subtracted, so the measure also includes the Lorentz-invariant G_N
   rescaling. That makes it larger, i.e. conservative.
2. **k_M for part C.** It was read from XC1's committed results JSON (the per-footing minimum) rather than recomputed.
3. **K4 and K3b.** K4 is stated for a density source; with stress present there is an extra O(α) term, which is
   included in Δ. K3b uses α_c = c₂ = 1e-20.

## What this lane cannot say

- It is power counting. B1 is the tree-level propagator that a loop integrates; no gravity-sector loop is evaluated,
  and O(1) coefficients are not computed. N_g = 10, N_m = 100 and the log factor are conservative choices.
- The UV completion is unknown. B3 is a worst-case model of it, which is why the verdict is CONDITIONAL and not PASS.
- All bounds are PROVISIONAL: either fetched through a summariser (Klinkhamer–Schreck eq. 16; Pospelov–Shang eq. 59)
  or recalled from memory (LEP/Tevatron).
- The cosmological-constant fine-tuning is GR's and is inherited unchanged. Nothing here derives a₀ or the a₀–Λ
  relation; κ = ½ is FITTED.
- This is one gate on one chassis, and a chassis result is not a result for candidate B. The cold mass is still
  required.
