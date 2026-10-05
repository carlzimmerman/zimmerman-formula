# CFG333 FROZEN CRITERIA: one ownership rule for four Milky Way populations?

κ = ½ FITTED, fixed. Both footings a₀ = 9.36e-11 / 1.13e-10 m s⁻². Kernel ν_mono (`CFG7_common.nu_mono`). On-disk inputs only; no downloads, no fitting, no scans. Written before any score.

**Candidate B's rule** (PAPER35 §2, `qwen_claude_field_theory/papers_2026/PAPER35_hierarchical_ownership_dr4_2026.tex`; FG001 = `campaign_fresh_gravity/CFG7_hierarchy_fg001.py` header): only the outermost bound system carries the phantom; a uniform host field never enters a subsystem's internal dynamics (no EFE).

## What each class predicts (fixed for all rules)
- **TOP-LEVEL:** the isolated law ν_mono(y_int) on the system's own baryons, no EFE.
  - Dwarfs: per CFG313 the native cold mass M_c = M_b/f_b is inert (f_ex = 0), so this is the bare law.
  - Globulars and wide binaries: no cold component.
- **OWNED:** Newtonian.
  - Globulars and wide binaries: baryons only (FG001 class E, no cold component).
  - Dwarfs (they collapsed with their cosmic share; CFG35/CFG313): Newton on M_b/f_b (f_b = 0.157126). This is CFG313's f_ex with zero own phantom, so f_ex = 1. **PRIMARY.** Stars-only Newton is reported.

## Rules (at most 3; thresholds fixed by physical scales)
- **R1, binding (tidal):** TOP-LEVEL if g_int > g_tide. Owned otherwise.
  - g_int is the system's own isolated-law field at r₁₂ = (4/3) r_h (half the mass inside).
  - g_tide = 2 g_host(D) r₁₂ / D. This is the tidal plus centrifugal field of a flat (deep-MOND) host. Standard: Binney & Tremaine §8.3; Zhao & Tian 2006.
  - g_host = ν_mono(g_N,host/a₀) g_N,host, with M_MW = 6e10 (h93/FG001).
- **R2, formation (FG001 classes T/A/E):** TOP-LEVEL (class T/A) if the system formed by its own collapse with its own cold share (dwarf galaxies). OWNED (class E) if it formed embedded (globulars, wide binaries).
  - This is in the record (FG001; PAPER35 §2), so it is **not** a new postulate.
  - Class A's "isolated law of the infall baryons" uses current baryons (FG001 H8's infall gas is an exploratory escape, not scored).
- **R3, acceleration (EFE dominance):** OWNED if g_int < g_ext. Top-level otherwise.
  - Both fields are actual MOND fields: g_int as in R1, g_ext = g_host at the system's position. Standard MOND EFE criterion: Milgrom 1986; Famaey & McGaugh 2012 §6.3.
  - Under B this is a **NEW POSTULATE** (B itself never uses g_ext).
- **R0, all top-level (control row):** must reproduce the bare-law results.

## Populations and statistics (pass = |tension| < 2σ on BOTH footings)
- **Wide binaries (WB):** the DR3 dry-run builder γ̂ (`prep_2026/gaia_dr4_prep/dr4_ready_1/DRY_RUN_2026-10-03.md`): 1.0750 ± 0.0550 (canonical), 1.0775 ± 0.0512 (alt). Used as a reading only; it is non-scoring for the prereg.
  - The representative system sits at the pipeline's deep edge, y = g_N/a₀ = 0.3, with M_tot = 1.5 M☉ and R₀ = 8.2 kpc. The host field is the prereg's banked g_ext = 1.778e-10.
  - Prediction: owned → γ_v = 1. Top-level → γ_v = √ν_mono(0.3).
  - Tension = (γ̂ − γ_pred)/σ.
- **Globulars (GC):** h93's four clusters, inputs, Wolf estimator and measured σ. Each cluster's class sets its prediction.
  - **PRIMARY:** h93's joint one-Υ fit against the SPS band [1.3, 2.2]. The signed tension is the distance to the band over σ_Υ (0 inside the band).
  - **ALSO REQUIRED:** h93's marginalised one-sided Fisher statistic L, with Υ ~ lognormal(1.6, 0.15 dex), 4000 draws, seed 931.
  - GC passes only if both are < 2σ.
  - Reported, not scored: the two-sided version, since Pal 3 is high for Newton.
- **Classical dwarfs (CL):** the AUDIT_UFD estimator on the LVD MW table, M_V ≤ −7.7, σ and r_h present (14 systems including LMC and SMC).
  - M_b = 2 L_V + 1.33 M_HI.
  - Median; error = bootstrap (1000, seed 42) ⊕ half the Υ_V 1–4 shift. z = median/error.
  - CFG313's infall-gas law row (+0.027) is quoted as a reference.
- **Ultra-faint dwarfs (UFD):** the AUDIT_UFD estimator exactly (31 + 9 upper limits, Kaplan–Meier median), with each system's class prediction.

## Decision
- **ONE RULE WORKS:** some rule (R1–R3) passes all four populations on both footings.
- **PARTIAL:** the best rule passes 3 of 4; name the failing population.
- **NONE:** otherwise.

All rules are reported. None is selected or tuned after scoring.

## Controls
- **C1:** reproduce h93's L = 4.6σ / 4.9σ (EFE law, ±0.1) and the joint Υ 0.76 (framework) / 2.14 (Newton).
- **C2:** reproduce AUDIT_UFD's +0.3245 / +0.3045 (±5e-4) and z 3.77 / 3.55 (±0.02).
- **C3:** the R0 row equals the bare-law values (UFD as C2; GC isolated law = h93's isolated column to 1e-6 with nu_s).
- **MUTATE** (CFG333_MUTATE=1, separate outputs `*_MUTATE.*`): the class labels of every scored unit (1 WB unit + 4 GC + 14 CL + 40 UFD) are randomly permuted for each rule (seed 333).
  - Check: the best unmutated rule's pass count drops for the seed-333 permutation.
  - Check: its mean pass count over 50 permutations is lower than the unmutated count.

## Lean
One Lean 4 + Mathlib file. Each rule × population × footing gets one theorem certifying the decisive inequality from rational bounds rounded outward from the results JSON:
- **pass:** −2e < m < 2e;
- **fail:** m ≥ 2e or m ≤ −2e.

It is checked with `lake env lean`, with no sorry. It certifies arithmetic, not statistics.
