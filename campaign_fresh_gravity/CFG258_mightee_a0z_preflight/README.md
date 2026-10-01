# CFG258 — could the public MIGHTEE-HI / LADUMA RAR sample separate FLAT a₀ from a₀ ∝ H(z), or from the anchored slope a₁ ≈ 5×10⁻¹⁰ per unit z? A blind pre-flight: NOT POSSIBLE for both

> **κ = ½ FITTED. A forecast from mocks, not a measurement. Nothing was downloaded; no MIGHTEE number was read beyond the quoted a₁ = (5.23 ± 1.05)×10⁻¹⁰ m s⁻² per unit z and "130 resolved HI galaxies to z ≈ 0.09". Every MIGHTEE-like input is a declared scenario (UNVERIFIED). No sentence says the data favour a framework.**

- **Criteria:** `FROZEN_CRITERIA.md` (**a88864716**), committed before any script existed and before any forecast number. **Script:** `cfg258_preflight.py` (main run 935 s on 12 processes; `MUTATE=1` about 6 min; `MUTATE=2` about 15 min). Outputs: `cfg258_preflight.out` / `_results.json`, `_MUTATE1*`, `_MUTATE2*`, the chart `cfg258_preflight.png` (`cfg258_plot.py`), and two post hoc files, `cfg258_posthoc_c4.*` and `cfg258_posthoc_formal.*`. Hashes: the commit that carries this file.
- **Method in one paragraph:** SPARC-resampled mocks (135 template galaxies, Υ_disc 0.6), ν_mono, both footings; an anchor sample at z = 0 (a library of 1,500 SPARC-resampled a₀ fits, SD 0.039 dex) and a MIGHTEE-like sample of N = 130 at z ∈ [0.02, 0.09]. **E1** fixes the anchor's a₀ and fits the slope b in a₀(z) = a₀(1 + b z): the claim's own statistic, which cannot tell a rise from a shared offset. **E2** fits intercept and slope within the sample: immune to shared offsets, sees only z-dependent systematics. A declared 8-term shared-systematics budget (level A optimistic, level B conservative; each knob Gaussian with SD = half its half-range) is drawn once per mock; the decision statistic is the total scatter over mocks (the CFG219 lesson); rules R1 (5th percentile of the law above the 95th of FLAT) and R2 (signal above the aligned worst case plus 2σ_stat); POSSIBLE iff both; E2 decisive at level B.

## Bottom line

1. **What (iii) implies.** a₀(z)/a₀(0) = 1 + 5.59 z (canonical; 1 + 4.62 z alt): **×1.11 at z = 0.02, ×1.31 at a mean z of 0.055, ×1.50 at z = 0.09** (alt ×1.09 / 1.25 / 1.42), i.e. +0.046 / +0.116 / +0.177 dex. The rival a₀ ∝ H(z) gives ×1.010 / 1.027 / 1.045: **(iii) changes a₀ about eleven times as much as the rival over this range** (nine times on the alt footing). At a mean z of 0.04 / 0.055 / 0.07 the anchored slope means the sample's fitted a₀ lies **+0.088 / +0.116 / +0.143 dex above SPARC's** (alt +0.074 / +0.098 / +0.122), a +22 to +39 % offset.
2. **(i) FLAT vs (iii): NOT POSSIBLE. (i) FLAT vs (ii) the rival: NOT POSSIBLE.** In the primary cell C0 at both budget levels, and in **12 of the 13 cells** for (iii) and **13 of 13** for (ii) (the frozen C11 was unreachable; the post hoc C11b stands in for it). The one exception is the requirement scenario C12 (z up to 0.3, not MIGHTEE): POSSIBLE only at the optimistic budget (level A), and NOT POSSIBLE once T5 and T7 are widened to what SPARC's own sub-samples show (post hoc level C, run for C0 and C12 only: R1 fails in both; R2 holds for C12's (iii) and fails for C0).
3. **The anchored claim is a ≈1σ effect once a modest shared budget is acknowledged.** E1's signal (the shift of the mean slope between truth (iii) and FLAT) is 5.2 per unit z against a total scatter of **1.5** statistics-only (3.4σ), **2.2** at level A (2.4σ) and **5.1** at level B (**1.0σ**). The formal error of the E1 fit is 0.29–0.31 per unit z (post hoc, `cfg258_posthoc_formal.py`), but the empirical scatter of the slope in the same mocks is 0.87 with the anchor at the truth and no shared draw (2.8× the formal), **1.55 with the library anchor (5.2×)** and 5.2 at level B (17.8×): per-galaxy Υ, inclination and distance errors act on a whole curve, and the anchor and the shared terms act on the whole sample. Under FLAT the formal statistic gives z > 3 in 11.5 % of mocks with no shared draw and in **32 % at level B** (z > 5 in 5.2 % and 27 %). A shared offset of **0.025 dex (6 %)** in the sample's a₀ is already 3 formal σ (a slope shift of 0.9 per unit z), and **0.04 dex (10 %)** is 5 formal σ. That the authors attribute their formal 5σ to the anchor choice is consistent with this.
4. **What mimics (iii)** (noiseless levers, canonical, mean z 0.055, target +0.116 dex): an assumed **stellar-mass scale too low by 0.107 dex (a factor 0.78)**, or **distances too small by 0.047 dex (11 %; H₀ too high by 11 %)**, or **velocities too high by 0.023 dex (5.4 %)**, or a **sample-mix offset of 0.116 dex**; a gas-mass offset would need 0.38 dex (its lever is only −0.39). Against level B's half-ranges: the stellar-mass offset needed is inside (0.107 against 0.15), the velocity offset is inside (0.023 against 0.03), the distance offset is 17 % beyond (0.047 against 0.04), the sample-mix offset is 45 % beyond (0.116 against 0.08), the gas offset is 6× beyond (0.38 against 0.06). The aligned worst case of the whole budget at the optimistic level A is 6.6 per unit z for E1, already above the 5.2 that (iii) predicts. **Empirically (post hoc C8): fitting real SPARC sub-samples with fixed Υ gives a₀ values that differ by 0.234 dex across V_flat terciles and morphological groups** (the lowest-V_flat tercile −0.18 dex, the others +0.05 to −0.06), twice the offset (iii) implies: a selection difference of that size is ordinary.
5. **The planted offset (MUTATE=1) is detected by E1 exactly as often as the physical law, and E2 does not attribute it reliably.** A shared stellar-mass-scale offset τ_ML* = −0.118 dex, sized so that E1's noiseless slope equals b₃, is flagged by E1 (formal z > 3) in 94.2 % of C0 mocks with no shared budget and 70.6 % at level B, against 94.8 % and 70.1 % for the physical law (the two agree within 0.02 in every cell; FLAT itself reaches 28–41 % at level B). E2's mean slope in C0 reads +0.36 (no budget) / +0.97 (level B) for the planted offset against +6.31 for the physical law (b₃ = 5.59; FLAT's own +0.33). But at level B one 130-galaxy sample classifies the planted offset as the physical slope in 26.5 % of mocks and the physical law as an offset in 31.7 % (C0; 20–29 % and 27–34 % across C0–C10; C12 only 1.9 % and 12.9 %). The frozen C6 control FAILS in all 12 cells (clause table below).
6. **What would make it possible (reported, not pursued):** (a) a within-sample z lever about four times longer (z to ≈ 0.3, C12), which makes (iii) POSSIBLE only at the optimistic budget; (b) N alone does not help at level B: E2's statistical scatter falls as 1/√N (σ_stat·√N ≈ 29–31; N = 130 → 1,040 gives 2.72 → 0.91 per unit z) but its level-B systematic scatter of 4.0 per unit z does not, against the 1.8 the 3.3σ requirement (Δ/3.29) allows: **UNREACHABLE at any N**; at the optimistic level A with N = 1,040 (C10) R2 passes and R1 fails; statistics alone would need about 290 galaxies at C0's design (130 × (2.72 / 1.82)²). The slope the C0 design could certify is **≥ 9.9 per unit z (E2, level A) or ≥ 17.5 (level B)** against the claim's 5.6; for E1, ≥ 9.7 / ≥ 23.3.

## Decisions (C0, per unit z; Δ the mean slope under the law minus FLAT's; σ_stat the SD over mocks with no shared systematics; σ_tot with the level's budget; S_joint the aligned worst case)

| law | estimator | Δ | σ_stat | level A: σ_tot / S_joint (R1, R2) | level B: σ_tot / S_joint (R1, R2) | decision |
|---|---|---|---|---|---|---|
| (iii) ANCH | E1 (anchored; never decisive) | 5.18 | 1.54 | 2.18 / 6.61 (fail, fail) | 5.07 / 20.22 (fail, fail) | NOT POSSIBLE |
| (iii) ANCH | **E2 (decisive)** | 5.98 | 2.72 | 3.00 / 3.73 (fail, fail) | 4.85 / 12.01 (fail, fail) | **NOT POSSIBLE** |
| (ii) RIVAL | E1 | 0.48 | 1.54 | 2.18 / 6.61 (fail, fail) | 5.07 / 20.22 (fail, fail) | NOT POSSIBLE |
| (ii) RIVAL | **E2 (decisive)** | 0.59 | 2.72 | 3.00 / 3.73 (fail, fail) | 4.85 / 12.01 (fail, fail) | **NOT POSSIBLE** |

The rival's noiseless slope over this design is about 0.5 per unit z against a statistical scatter of 1.5 to 2.7 and a level-A worst case of 3.7 to 6.6: it is not separable at any N in the grid (N = 1,040: σ_stat 0.9, level-A σ_tot 1.4, S_joint 3.7).

**All 13 cells, (iii) by the decisive E2** (the rival reads NOT POSSIBLE in every one; `cfg258_preflight.out` carries every row, E1 included):

| cell | design | Δ | σ_stat | A: σ_tot / S_joint (R1 R2) | B: σ_tot / S_joint (R1 R2) | decision |
|---|---|---|---|---|---|---|
| C0 | canonical, z ~ U[0.02, 0.09], 6 random points, σ_V/V 0.07, N 130 | 5.98 | 2.72 | 3.00 / 3.73 (n n) | 4.85 / 12.01 (n n) | NOT POSSIBLE |
| C1 | alt footing | 4.87 | 2.65 | 2.95 / 3.68 (n n) | 4.73 / 11.84 (n n) | NOT POSSIBLE |
| C2 | z ∝ z² | 6.40 | 3.68 | 4.03 / 3.76 (n n) | 6.16 / 12.30 (n n) | NOT POSSIBLE |
| C3 | z from 0.005 | 5.58 | 2.23 | 2.34 / 3.04 (n n) | 3.54 / 9.38 (n n) | NOT POSSIBLE |
| C4 | all points | 6.12 | 3.37 | 3.63 / 4.10 (n n) | 6.08 / 13.12 (n n) | NOT POSSIBLE |
| C5 | 6 outermost points | 5.83 | 2.33 | 2.62 / 3.46 (n n) | 4.30 / 11.24 (n n) | NOT POSSIBLE |
| C6 | σ_V/V 0.04 | 5.84 | 2.63 | 3.05 / 3.73 (n n) | 4.85 / 12.01 (n n) | NOT POSSIBLE |
| C7 | σ_V/V 0.12 | 5.96 | 2.96 | 3.27 / 3.73 (n n) | 5.34 / 12.01 (n n) | NOT POSSIBLE |
| C8 | N 260 | 5.67 | 1.84 | 2.20 / 3.73 (n n) | 4.07 / 12.01 (n n) | NOT POSSIBLE |
| C9 | N 520 | 5.65 | 1.28 | 1.70 / 3.73 (n n) | 3.85 / 12.01 (n n) | NOT POSSIBLE |
| C10 | N 1,040 | 5.59 | 0.91 | 1.40 / 3.73 (n Y) | 3.57 / 12.01 (n n) | NOT POSSIBLE |
| C11b (post hoc) | authors-matched scatter, anchor at its formal error, λ = 1.44 | 6.11 | 4.17 | 4.34 / 3.73 (n n) | 6.18 / 12.01 (n n) | NOT POSSIBLE |
| C12 (requirement, not MIGHTEE) | z ~ U[0.02, 0.30] | 5.78 | 0.66 | 0.72 / 0.92 (Y Y) | 1.07 / 2.86 (n Y) | POSSIBLE IF OPTIMISTIC |

The chart `cfg258_preflight.png` shows the percentile ranges of E1 and E2 per law and level: the flat law's level-B range contains the anchored slope.

## Levers and the offsets that mimic (iii)

| knob (analyst's input against the truth) | lever R (dex of log₁₀ â₀ per dex), canonical C0 / alt C1 / outermost points C5 | size that reproduces +0.116 dex at mean z 0.055 (canonical; alt +0.098 dex) | level-B half-range |
|---|---|---|---|
| T1 stellar mass scale τ_ML | −1.12 / −1.10 / −0.87 | **−0.107 dex** (alt −0.092) | ±0.15 |
| T2 gas mass scale τ_gas | −0.39 / −0.38 / −0.51 | −0.38 dex (alt −0.32) | ±0.06 |
| T3 distance scale τ_D | −2.51 / −2.47 / −2.38 | **−0.047 dex** (alt −0.040) | ±0.04 |
| T4 velocity scale τ_V | +5.03 / +4.95 / +4.76 | **+0.023 dex** (alt +0.020) | ±0.03 |
| T5 sample-mix offset τ_sel | +1.00 | +0.116 dex | ±0.08 |

(The deep-regime limits are −1, −1, −2, +4, +1; the levers sit above them because part of the sample is not deep.) At mean z of 0.04 and 0.07 the offsets needed scale to 75 % and 123 % of these.

## Statistics, scatter and the authors' error

- **σ_stat:** E1 1.54, E2 2.72 per unit z in C0 (E1's scatter includes the anchor library's 0.039 dex, about 1.3 per unit z of it in quadrature, 1.55² − 0.87² from the post hoc table below; the library carries a +0.022 dex fitted-a₀ bias from the error structure, so FLAT's E1 mean is −0.9, not 0: it cancels in Δ). σ_stat·√N is constant for E2 within 6.6 % (31.0, 29.7, 29.1, 29.3 at N = 130, 260, 520, 1,040) and not for E1 (17.6 → 43.8) because the anchor's error does not average down.
- **Formal against empirical error (post hoc, C0, FLAT truth, 1,500 mocks per level, `cfg258_posthoc_formal.out`):**

| fit | level | formal σ_b (median) | empirical SD of b̂ | ratio | formal z > 3 | formal z > 5 |
|---|---|---|---|---|---|---|
| E1, anchor at the truth | no shared draw | 0.31 | 0.87 | 2.8 | 7.1 % | 1.5 % |
| E1, library anchor | no shared draw | 0.29 | 1.55 | 5.2 | 11.5 % | 5.2 % |
| E1, library anchor | B | 0.29 | 5.17 | 17.8 | 32.4 % | 27.5 % |
| E2 | no shared draw | 0.91 | 2.89 | 3.2 | 9.6 % | 0.27 % |
| E2 | B | 0.91 | 4.84 | 5.3 | 19.1 % | 2.3 % |

  (A calibrated statistic gives 0.13 % and 0.00003 %.) The noiseless shift of E1's slope for a shared sample offset d is +0.37 / +0.75 / +1.34 / +1.96 / +5.00 per unit z at d = 0.010 / 0.020 / 0.035 / 0.050 / 0.116 dex, i.e. 1.2 / 2.4 / 4.3 / 6.3 / 16.1 formal σ.
- **Authors-matched scatter (C11):** the scenario's per-galaxy terms cannot reproduce the quoted formal σ(a₁) = 1.05×10⁻¹⁰ with the anchor library: even with every M-side term at zero the floor is 1.27×10⁻¹⁰. **UNREACHABLE** (the formal SPARC anchor error would have to be about 0.007 dex, not the 0.039 dex a galaxy-level resampling gives). With the anchor at that formal error (post hoc C11b) the match needs the M-side per-galaxy terms scaled by **λ = 1.44**; that cell reads NOT POSSIBLE too (E1 4.5σ statistics-only, 1.1σ at level B; E2 1.4σ at level A, 1.0σ at level B).
- **S_joint terms (C0, level B, E1 / E2 per unit z):** τ_ML −4.9 / 0.3; τ_gas −0.9 / 0.0; τ_D −3.2 / 0.1; τ_V +6.7 / −0.2; τ_sel +3.3 / 0.0; κ_V +0.6 / **+6.7**; κ_sel +0.3 / 2.2; κ_ML −0.4 / −2.5. E2 is immune to the first five, as designed, and sees the drifts (T6 to T8).

## Controls

**C1, C2, C3, C5, C7 pass; C4 FAILED in the main run (a Monte Carlo fluctuation, see below); MUTATE=2's C4 fails as designed; C6 (MUTATE=1) fails in every cell.**
- **C1** the arithmetic (b₃ 5.5874 / 4.6234, E(0.09) = 1.0454, ×1.5029). **C2** noiseless consistency (FLAT θ̂ = log a₀ and b̂ = 0; ANCH b̂ = b₃; RIVAL's E2 slope equals an independent scipy least-squares fit; largest deviation 1.3×10⁻⁸). **C3** the deep-regime levers −1, −1, −2, +4, +1 to 1e-3. **C5** the level-B R1 margin of E2 (−11.8) and its reseeded rerun (−12.1) agree, 65 bootstrap errors from zero (not MC-limited). **C7** the unreachability of the authors' σ is reported.
- **C4 (reactivity): FAIL as frozen in the main run.** Z_tot (E1, ANCH) fell from 3.36 to 1.02 at level B (ratio 0.30, as required) but the blind within-mock-bootstrap statistic moved from 3.80 to 4.93 (+29.8 %) against the frozen "< 10 %". **Post hoc** (`cfg258_posthoc_c4.py`, 600 mocks per level, different seeds): 3.70 → 3.80 (**+2.7 %**): the main run's change was a fluctuation of its 150-mock median; the control's purpose (the blind statistic does not fall while Z_tot does) is met. The main run's FAIL stays as printed.
- **MUTATE=2** (every shared draw removed): C4 FAILS as designed (Z_tot 3.36 → 3.40, blind 3.80 → 3.80): a statistic that does not see the budget reads the same at every level. With the draws removed C0 stays NOT POSSIBLE (statistics alone fail R1 there) and C12 reads POSSIBLE; the cells for (iii) by E2 become 1 POSSIBLE, 1 POSSIBLE IF OPTIMISTIC, 11 NOT POSSIBLE.
- **MUTATE=1 / C6 (a shared stellar-mass offset equal to (iii) planted into FLAT mocks): FAILS in every cell.** The clause table (E2 slopes are relative to FLAT's own mean slope, as coded):

| clause | cells passing (of 12) | detail |
|---|---|---|
| E1 detects the planted offset, clean ≥ 95 % | 7 | C2, C4, C6, C8, C9, C10, C12 (C0 94.2 %) |
| E1 detects it at level B, ≥ 80 % (a clause the code added; frozen H6 names no level) | 1 | C12 only (C0 70.6 %; the other cells 64–75 %) |
| E2 reads the planted offset as no slope (within 0.15 b₃ of FLAT's) | 12 | planted E2 mean minus FLAT's: −0.04 to +0.06 per unit z (C0 +0.03) |
| E2's physical slope within 5 % of b₃ (relative to FLAT's) | 6 | C3, C6, C8, C9, C10, C12; C0 +7.1 %, C1 +8.2 %, C2 +16.7 %, C4 +7.8 %, C5 +5.0 %, C7 +5.3 % |
| classification rate of the planted offset equals the Gaussian prediction (3 MC errors + 0.01) | 2 | C3, C12; the observed PHYS rate is below the prediction in 11 of 12 cells, by 0.03–0.11 |
| classification rate of the physical law equals the Gaussian prediction | 6 | C3, C5, C6, C8, C9, C10 |
| **all clauses** | **0** | |

  **Reading:** E1 flags a planted offset as often as the physical law (so the anchored statistic cannot tell them apart) and E2 separates them only in the mean; per sample the attribution error at level B is 20–29 % (planted called physical) and 27–34 % (physical called offset) in C0–C10, and only C12 attributes (1.9 % and 12.9 %). The control fails on frozen thresholds, which the E2 slope distribution (heavy-tailed, biased upward by the nonlinear fit and the error structure) does not meet: the design cannot attribute at the frozen level, consistent with NOT POSSIBLE. Under the frozen text's literal reading (raw E2 slopes, clean E1 detection only) no cell passes all clauses either (C12 fails on the physical-law rate). The first MUTATE=1 attempt crashed in the offset solver (a ±1.5 dex bracket gave a NaN fit) before writing anything; the first run with the corrected bracket is kept as `_MUTATE1_firstrun*` (its C12 row had NaN rates); the rerun differs only in the NaN handling (and a C12 FLAT level-B detection of 0.345 against 0.334).

## Hand estimates (frozen before the run)
**PASS:** H1 (arithmetic), H2 (levers inside the bands: −1.12, −0.39, −2.51, +5.03, +1.00), H3 (mimic sizes inside the bands). **MISS:** H4 (the two σ_stat clauses hold: E1 1.54 inside 0.5–2.0, E2 2.72 inside 1.2–4.0; the frozen authors-matched cell C11 is unreachable with the library anchor, and the post hoc C11b solves at λ = 1.44, inside the predicted 1.0–4.0); H5 (clause b: E1 at C0 does NOT pass R1 statistics-only: P5 of (iii) is 0.90 against P95 of FLAT 1.67, margin −0.78 per unit z, because the (iii) slope distribution is wider than FLAT's, 2.12 against 1.54; clauses a, c, d, e hold, and the frozen text's "S_joint,E2 of order 5 to 8" is 12.0 at level B); H6 (MUTATE=1, above); H7 (the main run's C4 fluctuation, above); H8 (the SPARC sub-sample range 0.234 dex is above the 0.04–0.20 band); H9 (σ_stat·√N for E2 varies by 6.6 %, above the 5 % band; E1 fails by construction).

## Disclosures
- **Seen before the main run:** QUICK-mode smoke runs (150–300 mocks per run) and a small scatter check were run while the script was developed and their printed numbers were seen; their outputs were not kept. Nothing in the criteria was changed after them. **Two scoring clarifications were made in the code after the QUICK run and before the main run:** the scope of H5's E1 clauses was fixed to the primary cell C0, and "POSSIBLE at most at level A" was scored as POSSIBLE IF OPTIMISTIC only. The post hoc cell C11b and the level-C extension were added because the smoke run showed the library anchor alone exceeds the authors' formal error and C8's range exceeds the level-B T5 band.
- **Code against frozen text (C6):** the code scores E1 detection at both the clean (≥ 95 %) and level-B (≥ 80 %) levels (the frozen H6 names ≥ 95 % with no level) and takes E2 slopes relative to FLAT's own mean (+0.33; the frozen text says relative to 0). Neither changes the verdict (0 of 12 cells pass all clauses under either reading).
- **Post hoc, labelled:** C8 (real SPARC sub-sample fits), the level-C rerun (T5 and T7 widened to 0.117 dex), the formal-anchor cell C11b, `cfg258_posthoc_c4.py` and `cfg258_posthoc_formal.py` (both report only; no decision depends on them).
- The repo holds earlier MIGHTEE files (found by filename only; none opened by this lane). The criteria's budget sources are flagged UNVERIFIED; T5, T7 and T8 are declared with no source beyond the C8 cross-check.

## Limits
The forecast is optimistic: the analyst's kernel is the truth kernel, Υ is not fitted, scatter is Gaussian, no outliers, no external-field effect, no asymmetric drift or beam-smearing profile model; the "galaxies" are resamples of 135 SPARC templates; every MIGHTEE-like number (σ_V/V, points per curve, the z distribution, σ_Υ,M, σ_i,M, the budget half-ranges) is a scenario, and the real sample's error budget may be better or worse. The decisions hold across the 13-cell grid; they do not say what the real MIGHTEE data show. A measurement would need the download, which needs the owner's go in the calculation chat.

## Files
`FROZEN_CRITERIA.md`, `cfg258_preflight.py` (+ `.out`, `_results.json`), `cfg258_preflight_MUTATE1.out` / `_results.json` and `_MUTATE1_firstrun.out` / `_results_firstrun.json`, `cfg258_preflight_MUTATE2.out` / `_results.json`, `cfg258_preflight.png` (`cfg258_plot.py`), `cfg258_posthoc_c4.py` / `.out` / `_results.json`, `cfg258_posthoc_formal.py` / `.out` / `_results.json`.

Re-run: `python3 cfg258_preflight.py` (about 16 min on 12 processes), `MUTATE=1 python3 cfg258_preflight.py`, `MUTATE=2 python3 cfg258_preflight.py`, `python3 cfg258_posthoc_c4.py` (about 3 min), `python3 cfg258_posthoc_formal.py` (about 40 s).
