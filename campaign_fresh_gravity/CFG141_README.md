# CFG141 — KURVS a₀(z) with each galaxy's measured outer dispersion

- **Criteria:** frozen in `CFG141_FROZEN_CRITERIA.md` (4da622ccf), before the σ(R) extraction was opened.
- **Data:**
  - the data chat's extraction of the paper's plotted Hα σ(R) major-axis profiles (94e4a5181; observed σ, both sides, exact vector geometry);
  - CFG140's pipeline, exec'd read-only.
- **Script:** `CFG141_kurvs_measured_sigma.py`, under a second.
- **Runs:**
  - The main run passes 9 of 10 and exits 0. The one miss is the reported H2 verdict.
  - The MUTATE run (velocities × 2) fails H1 and exits 1.
  - The two runs differ on H1, so the control is informative.

## Bottom line

**By the frozen map: NON-DIAGNOSTIC. The measurement sharpens it into one testable requirement.**

- **The outer dispersion does not fall.** At R_max (4–7 disc scale lengths) the measured σ equals the paper's σ₀: median σ_out/σ₀ = 1.05, range 0.70–1.13.
  - So the constant-σ pressure correction that CFG140 carried as its scenario P1 is supported by data.
  - CFG140's caution that it over-corrects, drawn from the KROSS control, is not borne out.
- **With the measured σ (P2, the self-gravitating isothermal layer)**, the pressure-corrected outer accelerations exceed what flat a₀ predicts unless the discs are very gas-rich.

| total gas μ = M_gas/M* (unmeasured) | Δ′_flat, anchor-corrected (canonical, δ = 0) | Δ′_H, the rival a₀ ∝ H(z) |
|---|---|---|
| 0.25 | +0.449 ± 0.065 | +0.293 ± 0.064 |
| 0.67 (the paper's 40% molecular) | +0.390 ± 0.065 | +0.237 ± 0.063 |
| 1.5 | +0.300 ± 0.064 | +0.153 ± 0.063 |
| 4 | +0.126 ± 0.065 | −0.009 ± 0.063 |

**Under P2, flat a₀ survives in only 3 of 24 cells, all at μ = 4** (4× the stellar mass in gas, with stellar mass at or above nominal). The rival survives only at μ = 4 as well (6 of 24 cells).
- **What flat a₀ requires:** these z ≈ 1.5 discs (log M* ≈ 9.7–10.5) must hold about 4 M* in total cold gas, molecular plus atomic. At the paper's own molecular fraction, flat a₀ under-predicts by 0.39 dex (6σ).
- **This is a testable prediction.** Molecular fractions near μ ≈ 1 at these masses and redshifts, plus a comparable HI reservoir, would put μ in the 2–5 range. So it is plausible, but not measured.
- **The fixed-scale-height variant (P3)** halves the correction and adds the measured gradient. Flat is then disfavoured in 16 of 24 cells and survives at μ = 4, and at μ = 1.5 with heavier stars. The rival survives in 16 of 24.
- **Between the two readings,** the power row gives 2.7–3.9σ separation per cell under P2. The gas bracket, about 0.3 dex, is larger than the gap between them, about 0.15 dex. So measured gas would turn this into a discriminating test.

**Per galaxy** (central cell, P2, unanchored):

| KURVS | σ₀ | σ_out | R_max/R_d | V_c²/V_obs² | Δ_flat | Δ_H |
|---|---|---|---|---|---|---|
| 3 | 51 | 55 ± 8 | 4.7 | 1.65 | +0.26 | +0.12 |
| 7 | 61 | 69 ± 13 | 4.3 | 4.66 | +0.37 | +0.22 |
| 8 | 40 | 28 ± 20 | 7.4 | 3.43 | +0.22 | +0.04 |
| 9 | 48 | 51 ± 5 | 3.4 | 1.96 | +0.32 | +0.16 |
| 11 | 62 | 66 ± 5 | 3.5 | 1.50 | +0.38 | +0.25 |
| 13 | 62 | 61 ± 10 | 6.0 | 6.06 | +0.73 | +0.58 |
| 15 | 68 | 67 ± 4 | 4.1 | 3.91 | +0.44 | +0.28 |
| 16 | 69 | 73 ± 4 | 4.7 | 3.57 | +0.54 | +0.38 |
| 17 | 65 | 62 ± 6 | 6.9 | 4.61 | +0.85 | +0.70 |
| 21 | 74 | 77 ± 9 | 7.6 | 5.24 | +0.72 | +0.57 |

At R_max the pressure term dominates the circular speed for most of these discs (V_c²/V_obs² up to 6). Even the three with the smallest corrections (IDs 3, 9 and 11, all below 2) sit at Δ_flat +0.26 to +0.38 before the anchor.

## Controls

- **C1:** with σ_out set to the tabulated σ₀, the P2 pipeline reproduces CFG140's committed P1 grid exactly (difference 0.0, 24 cells).
- **C2:** all 10 profiles are finite, positive and consistent with the velocity table's R_max. None is dropped.
  - Two reach R_max and are interpolated there: KURVS-8 and KURVS-21.
  - Eight use the outermost three points.
    - Five of these end at R_max within about 0.05 kpc (KURVS-7, 9, 11, 13 and 15), just inside the interpolation rule.
    - Three end short: KURVS-3 at 10.1 against 11.7 kpc, KURVS-16 at 10.0 against 10.9, and KURVS-17 at 8.2 against 9.9.
- **MUTATE:** with the velocities doubled, flat a₀ is disfavoured beyond 3σ in every cell.

## Disclosures

- **The authors' clipped pixels are excluded.** These are 18 white-filled markers, contaminated by sky lines or broad components. Excluding them applies the source's own quality flag; the frozen text did not mention them. The variant that includes them (R5) gives flat disfavoured in 22 of 24 cells.
- **Two small script fixes before the first successful run, neither changing a declared choice:**
  - CFG140's `power()` is defined after its controls marker, so its committed source is exec'd separately.
  - σ_out's two-sided average uses each side's interpolation where that side reaches R_max. Otherwise it uses the outermost three points, as declared.

## Caveats (declared untested)

- **The dispersion model:** anisotropic dispersion (σ_R ≠ σ_z), and vertical structures beyond the isothermal layer and the fixed-height variant. The correction is large at 4–7 R_d.
- **Beam smearing** of the plotted outer σ. It is smallest there, and not corrected.
- **Correlated profile points:** neighbouring points are correlated, about one per pixel, so σ_out's error is if anything underestimated.
- **The gas:** unmeasured, and no public measurement exists for these discs (data chat).
- **The COSMOS half** of the survey.

## Reading

- **Where the decisive test stands:** B's a₀(z) test now reaches a sharp conditional.
  - With the measured outer dispersion, the framework's flat a₀ holds at z ≈ 1.5 only if these discs carry about four times their stellar mass in cold gas.
  - The rival a₀ ∝ H(z) needs nearly as much under P2, and less under P3.
- **What settles it:** a measured total gas mass, CO plus HI or a dust-based proxy, for KURVS-like discs. If μ ≤ 1.5 is measured, flat a₀ is disfavoured at z ≈ 1.5 under P2.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Correction (appended 2026-09-29; the text above is unchanged)

Wording corrections at the orchestrator's check. The frozen verdict (NON-DIAGNOSTIC) and every number above are unchanged.

1. **Under P2 both readings under-predict at realistic gas.**
   - At the paper's 40% molecular fraction (μ = 0.67), Δ′_flat = +0.39 ± 0.07 (6.0σ) and Δ′_H = +0.24 ± 0.06 (3.7σ).
   - At μ = 1.5 the rival is still 2.4σ high. Both readings survive only at μ = 4: flat in 3 cells, the rival in 6.
   - So the P2 excess is NOT evidence against flat a₀ in particular.
   - The rival sits 0.12–0.16 dex closer in every cell. That gap is about half the gas bracket (0.32 dex), so it does not discriminate while the gas is unmeasured.
   - Under P2, either both readings need about 4 M* of cold gas, or the P2 dispersion model over-corrects.
     - Four M* is far above the molecular gas the paper assumes: 40%, μ = 0.67, from Tacconi+2020 scaling relations.
     - It is also above PHIBSS-type molecular fractions at these masses and redshifts: about 0.4–0.6 of M* + M_mol, μ ≈ 0.7–1.5.
     - It would need an atomic reservoir of roughly 2.5–3.3 M*, the top of the declared bracket.
   - Under P3 at the paper's gas the two readings separate more: flat +0.24 ± 0.07 (3.5σ), the rival +0.09 ± 0.07 (1.3σ).
2. **The conclusion rests on the dispersion model.**
   - The pressure term dominates V_c at R_max: V_c²/V_obs² runs from 1.5 to 6.1.
   - At 4–7 R_d, anisotropy, disc thickness and non-equilibrium are untested. That is the regime where beam smearing and pressure support are debated.
3. **The measured σ shows only that σ does not fall.**
   - σ_out/σ₀ ≈ 1.05 supports P1's constant-σ input at R_max.
   - It does not validate the isotropic, isothermal, self-gravitating layer that P2 assumes.
   - Read "the constant-σ pressure correction … is supported by data" in that narrower sense.
4. **The gas requirement belongs to the P2 model, not the framework.**
   - "About 4 M* of cold gas" is what the P2 dispersion model requires of these discs, for either reading. It is not a prediction of the framework.
   - A measured μ ≤ 1.5 would disfavour both readings under P2, and would point at the dispersion model before either law.
   - Read "This is a testable prediction" and "What flat a₀ requires" in that sense.
5. **The KROSS caution is narrowed, not removed.**
   - The measured σ rules out one source of the over-correction CFG140 suspected: a falling outer σ.
   - The KURVS − KROSS differential under P1 (+0.27 ± 0.07) is unchanged and unexplained.
   - Read "CFG140's caution … is not borne out" as "not explained by a falling outer σ".
