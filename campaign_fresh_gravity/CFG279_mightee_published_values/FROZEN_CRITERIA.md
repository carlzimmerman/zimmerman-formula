# CFG279 — FROZEN CRITERIA: the MIGHTEE-HI / LADUMA RAR paper (arXiv:2608.03576) read against FLAT, a₀ ∝ H(z) and the anchored slope, with CFG258's frozen rules; PUBLISHED VALUES ONLY (no per-galaxy data is public)

**This file is committed before the CFG279 script exists.** It is **NOT blind**: the paper's numbers were read while designing (§0).

> **κ = ½ FITTED. a₀(z) FLAT is the framework's distinctive law, a₀ ∝ H(z) the rival, ANCH = the anchored slope taken as a law (CFG258). The owner approved fetching "the public RAR sample of arXiv:2608.03576 (and the paper)" (the owner's explicit yes in the calc chat). The paper was fetched; **no public RAR sample exists**: the appendix table of per-galaxy g_bar and g_obs is commented out in the source, the Data availability statement says the other data "are available on request to the corresponding author", and the public MIGHTEE-HI spectral cubes are unprocessed (GB-scale, outside the approved scope). So this lane can use only the paper's PUBLISHED FIT RESULTS, in the authors' own M/L modelling; it is not our implied-a₀ estimator and forms no per-galaxy a₀. Class: published values. No sentence says the data favour a law.**

Request (the owner via the High-z peer, 2026-10-01): lane J — MIGHTEE-HI / LADUMA real data, z ≈ 0.02–0.09: a precise z < 0.1 a₀ level for the chart (the laws differ by ≤ 2 % there: a level, not a test) and a direct check of the claimed rise (the anchored slope implies ×1.11 / ×1.31 / ×1.50 at z 0.02 / 0.055 / 0.09; is it in the data, or in the selection: CFG258's mimic table M\* scale 0.107 dex, distances 11 %, velocities 5.4 %, sample mix 0.116 dex?); use CFG258's frozen estimators and controls where they apply; deliverable a results JSON plus a chart-shape points CSV.

## 0. What I have read and what I have seen (disclosure)
1. **Read in this design phase (so seen), from the fetched TeX (`_external_data/arxiv_src/2608.03576/main.tex`, sha256 in `data_assembly/FETCH_MANIFEST_2026-10-01.jsonl`):** the abstract (130 purely HI-selected galaxies, z ≲ 0.09; RAR a₀ = (1.50 ± 0.05)×10⁻¹⁰ m s⁻², intrinsic scatter 0.096 ± 0.006 dex; "no significant redshift evolution in the RAR acceleration scale"; the inverse bTFR 3.4σ and forward 8.7σ trends); the Redshift-evolution section (a(z) = a₀ + a₁ z; MIGHTEE+LADUMA alone a₀ = (1.54 ± 0.11), a₁ = (−1.60 ± 2.33) in 10⁻¹⁰ m s⁻² per unit z; with SPARC as the z = 0 anchor a₀ = (1.15 ± 0.02), a₁ = (5.23 ± 1.05), "a formal 5.0σ" rise; the statement that the MIGHTEE-only fit "differs from the fit using our sample with SPARC as the z = 0 anchor at the 2.5σ level"; the bTFR-derived a₁ = (−8.1 ± 2.3) alone and (−6.3 ± 0.9) with SPARC) and the Data availability statement.
2. **CFG258 (read, committed a88864716 / cdedfca46):** the laws (i) FLAT, (ii) RIVAL E(z) = √(0.315 (1 + z)³ + 0.685) (≈ 1 + 0.4725 z; the within-sample E2 slope over CFG258's C0 design is 0.588 per unit z), (iii) ANCH = 1 + b₃ z with b₃ = a₁/a₀; E1 (anchored, never decisive) and **E2 (within-sample intercept and slope, decisive)**; the decision rule POSSIBLE iff R1 (Δ/σ_tot ≥ 3.29) and R2; the C0 E2 numbers from `cfg258_preflight_results.json`: σ_stat = 2.721, level A σ_sys = 1.255 (σ_tot 2.997), level B σ_sys = 4.012 (σ_tot 4.848) per unit z; CFG258's verdict (mocks only): FLAT against RIVAL and FLAT against ANCH both NOT POSSIBLE.
3. **No per-galaxy data of this paper has been read; none is public.** The MIGHTEE-HI cubes are not fetched. No number below was computed before this freeze except the arithmetic of §3 (hand estimates §7).

## 1. Inputs (frozen; each is re-read from the TeX by a control)
| quantity | value (10⁻¹⁰ m s⁻² unless stated) | source in the paper |
|---|---|---|
| a₀, whole sample, z-averaged | 1.50 ± 0.05 | abstract |
| a₀ (z-dependent RAR fit), MIGHTEE+LADUMA only | 1.54 ± 0.11 | Redshift-evolution section |
| a₁ (per unit z), MIGHTEE+LADUMA only | −1.60 ± 2.33 | same |
| a₀ (z-dependent RAR fit), with SPARC anchor | 1.15 ± 0.02 | same |
| a₁ (per unit z), with SPARC anchor | 5.23 ± 1.05 | same |
| a₁ from the inverse bTFR, MIGHTEE+LADUMA / with SPARC (reported only) | −8.1 ± 2.3 / −6.3 ± 0.9 | same |
| the stated difference between the MIGHTEE-only and the anchored fit | 2.5σ | same |

## 2. Statistics (frozen)
- **Slope in relative units:** b ≡ a₁/a₀ (per unit z). **b_E2 = −1.60/1.54 = −1.04** (the MIGHTEE-only fit: intercept and slope both free, the E2 analogue), error by propagation without a covariance term: σ_b = √[(2.33/1.54)² + (1.60 × 0.11/1.54²)²]. **b_ANCH = 5.23/1.15 = 4.55** (the anchored claim in the paper's own units; its error by the same propagation); CFG258's canonical-footing b₃ = 5.587 is reported beside it.
- **Laws:** FLAT b = 0; RIVAL b = 0.4725 (z → 0; sensitivity 0.588, CFG258's C0 E2 value); ANCH b = b_ANCH.
- **Pulls of the within-sample slope against each law** (b_E2 − b_law)/σ at three widths: (F) the paper's formal σ_b only; (A) σ_b ⊕ CFG258's C0 level-A systematic scatter 1.255; (B) σ_b ⊕ the level-B scatter 4.012 (per unit z; CFG258 declared budgets, UNVERIFIED, applied here as they were frozen there). **DISFAVOURED iff |pull| ≥ 3.29 (CFG258's R1 threshold), CONSISTENT otherwise.** Separations Δ/σ for the three pairs are reported, with the decision rule NOT POSSIBLE iff Δ/σ_tot < 3.29 at the level.
- **The anchored fit's own pulls** (E1 analogue, reported): (b_ANCH − b_law)/σ_ANCH. **The sample offset:** a₀(MIGHTEE-only)/a₀(SPARC-anchored z = 0 value) = 1.54/1.15 in dex with its error; compared with what ANCH implies at the sample's mean z and with CFG258's mimic table (M\* scale 0.107 dex, distances 0.047 dex, velocities 0.023 dex, sample mix 0.116 dex at z̄ = 0.055).
- **Levels for the chart (published, the authors' M/L modelling):** s = a₀/0.93603 on the canonical footing **only as a convention** (CFG4's ν_mono equals the exponential RAR kernel numerically, which a control checks); the points file carries the whole-sample level, the MIGHTEE-only level and the SPARC-anchored z = 0 level, each labelled "published, not our estimator".

## 3. Arithmetic frozen before the run (reproduced and checked by the script)
a(z)/a(0) at z = 0.02 / 0.055 / 0.09 for FLAT 1; RIVAL 1.0096 / 1.0271 / 1.0454 (CFG258); ANCH with b_ANCH = 4.55: 1.091 / 1.250 / 1.409 (paper units) and with CFG258's b₃ = 5.587: 1.112 / 1.307 / 1.503.

## 4. Controls (each can fail)
- **C1:** every input of §1 is found verbatim in the paper's TeX (regex on the strings "(1.54 \pm 0.11)", "(-1.60 \pm 2.33)", "(1.15 \pm 0.02)", "(5.23 \pm 1.05)", "(1.50 \pm 0.05)", "8.1 \pm 2.3", "6.3 \pm 0.9", "2.5\sigma") and the Data-availability sentence contains "available on request"; the appendix table line is commented out.
- **C2:** the §3 arithmetic reproduces CFG258's committed `part_a` numbers (f_iii and f_rival at z = 0.02, 0.055, 0.09) to 1e-9 and the C0 E2 σ's from its results JSON; ν_mono equals 1/(1 − e^{−√y}) to 1e-9 on a grid (so s = a₀/0.93603 is an identity of kernels).
- **C3:** the propagated σ_b equals a 10⁶-draw Monte Carlo of a₁/a₀ (independent normals) to 2 %.
- **MUTATE=1 (reactivity):** the inputs replaced by a world on the anchored slope (a₁ = +5.23 for the MIGHTEE-only fit): the within-sample slope must then be CONSISTENT with ANCH and DISFAVOURED against FLAT at the formal width (the decision logic flips). **SELFTEST:** fabricated inputs on FLAT (a₁ = 0, the published errors): CONSISTENT with FLAT, DISFAVOURED against ANCH at the formal width.

## 5. Outputs
`cfg279_mightee_published.py` → `cfg279_results.json`, `cfg279.out`, `cfg279_points.csv` (chart shape; three rows: whole-sample level, MIGHTEE-only level and slope, SPARC-anchored z = 0 level; `no_root` empty; the extra columns carry b, pulls and the budget levels), `_MUTATE1`, `_SELFTEST` variants; README. One run; no re-run to change a result; hashes to the orchestrator and the peer.

## 6. What this lane cannot say
It is not an implied-a₀ measurement of ours: no per-galaxy data, the authors' mass-to-light modelling, their RAR kernel and their selection; the budgets are CFG258's declared (UNVERIFIED) numbers; the formal error of the within-sample slope is the authors'. It cannot say whether the 0.127 dex sample offset to SPARC is a stellar-mass scale, a distance scale, a velocity scale or a sample mix (CFG258's mimic table lists all four). No law statement is made.

## 7. Hand estimates (frozen)
- **HE1:** the within-sample slope b_E2 = −1.04 ± 1.5 per unit z lies within 1σ of FLAT (|pull| < 1 at every width) and of RIVAL.
- **HE2:** FLAT against RIVAL is NOT POSSIBLE at every width (Δ/σ_tot < 1).
- **HE3:** the anchored slope b_ANCH = 4.55 is DISFAVOURED at the formal width (pull ≥ 3.29) and not at levels A and B.
- **HE4:** the sample offset a₀(MIGHTEE-only)/a₀(SPARC) is +0.127 ± 0.04 dex, within 0.02 dex of CFG258's sample-mix offset 0.116.
- **HE5:** C1–C3, MUTATE=1 and SELFTEST pass.
