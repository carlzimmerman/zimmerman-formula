# W4-10: is there ONE 4? κ in every KiDS isolated-lens subsample (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-10 script exists or any subsample fit is made.** Append-only. Rules: CFG894
`KAPPA_CAMPAIGN_RULES.md`. Observational lane (`obs`). **κ = ½ is FITTED.** Not theory closed.

## Question

"Why 4" presumes a single constant. W4-06 fitted κ_Λ = 0.52 ± 0.09 for isolated blue lenses. The record knows that red and
early-type lenses sit above the law (CFG829: +0.20 dex for red lenses at the dwarfs' g_bar; CFG840: all-isolated KiDS
A 1.44 ± 0.05, GAMA 1.72 ± 0.21). Nobody has expressed that as κ per subsample, tested it across B21's disjoint partitions,
or checked whether B21's hot-gas variant restores a single κ.

## Data and estimator (fixed; reused, not rewritten)

- B21 KiDS-1000 public RAR files, read only. The estimator is W4-06's committed `fit_kappa` (imported from
  `why_4_puzzle/W4_06_lensing_kappa/w4_06.py`), with its loader, s = c√(Gρ), ν_simple, and footing ρ_DE.
- Window: CFG829's W = [10^−13.3, 10^−11.9] for every subsample.
- σ_i is the half-width of the Δχ² = 1 interval (a symmetric approximation, stated).

**Subsamples (file, covariance bin):**
- Partition C, colour: blue (Colorbin_1, 0.0) and red (Colorbin_2, 2.5).
- Partition S, Sérsic: n < 2 (Sersicbin_1, 0.0) and n > 2 (Sersicbin_2, 2.0).
- Partition M, stellar mass: Massbin-1 to -4 (log M★ bins starting at 8.5, 10.3, 10.6, 10.8).
- Report only (overlapping samples): isolated dwarfs (Fig-10), all isolated KiDS (Fig-4-5-C1), all isolated with B21's
  hot-gas estimate (Fig-4 hotgas), and GAMA isolated (Fig-4-C1 GAMA).

## Tests (frozen)

- **T1, universality within each disjoint partition (C, S, M).**
  - χ²_U = Σ(κ_i − κ̄)²/σ_i², with κ̄ the inverse-variance mean and dof = n − 1.
  - **UNIVERSAL** if p > 0.05.
  - **NOT UNIVERSAL** if p < 0.0027 (3σ).
  - **INTERMEDIATE** otherwise.
  - A subsample with fewer than 3 window points or an edge minimum is dropped and listed.
- **T2, hot gas.** Is κ(all + hot gas) within 2σ of κ(blue)? Report κ(all) → κ(all + hot gas) as well.
- **T3, survey cross-check.** κ(GAMA) against κ(KiDS all): z-score, reported.
- **T4, trend.** The sign of dκ/d log M★ across the mass bins (weighted linear fit), reported.

**Lane verdict:**
- **ONE κ:** all three partitions UNIVERSAL.
- **ONE κ FOR LATE TYPES ONLY:** C or S NOT UNIVERSAL, with the early-type member high.
- **NO SINGLE κ:** a partition NOT UNIVERSAL in a way not ordered by type.
- **NOT DIAGNOSTIC:** too few usable subsamples.

## Hand expectation (disclosed)

From the recorded amplitudes, using κ ≈ ½A² in the deep regime:
- blue about 0.52;
- red about 1.2–1.3;
- all isolated about 1.0;
- GAMA about 1.5;
- the mass bins rising with mass as the red fraction rises.

Expected verdict: **ONE κ FOR LATE TYPES ONLY.** Hot gas is not expected to close the gap fully. That is a guess; T2 decides.

## Checks and controls

- **K1:** the import reproduces W4-06's blue PRIMARY (κ 0.520 [0.433, 0.614]).
- **K2:** each covariance block is non-singular and positive definite for every fitted subsample.
- **MUTATE (`W4_10_MUTATE=1`), a universal mock sky.** Every subsample's g_obs is replaced by the law at the blue κ plus
  Gaussian noise from its own covariance (seed 101). T1 must return UNIVERSAL in every partition. The real-data verdict must
  differ, or the control has no power, which would be reported. Exit 1 when the control bites (the verdict changes).

## Register

One `obs` row for the lane (κ per partition summarised), then `kappa_campaign_lee.py` rerun. Nothing downloaded.
