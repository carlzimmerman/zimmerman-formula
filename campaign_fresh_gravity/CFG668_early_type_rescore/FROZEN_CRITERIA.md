# CFG668 FROZEN CRITERIA: is the KiDS early-type excess a stellar-mass artefact? (morphology-blind test, raw lensing)

Date: 2026-10-12. Written and committed ALONE, before any CFG668 code or score. Block CFG660–669. Nothing below may be edited
after this commit.

Raw data only (owner's 10-10 rule): raw KiDS excess surface density, no ΛCDM ingredient. In particular **CFG529/CFG531's ε is not
used**, because its environment term is ΛCDM-built (halofit two-halo, HOD grids, Moster/Behroozi SHMR; CFG529 README). The only
framework statement used is that the law reads baryons only, so it is **morphology-blind**: at matched baryonic mass, early and
late types must show the same lensing (ratio 1) at the radii used (≥ about 50 kpc, where each lens acts as a point mass). Not
"theory closed". Nothing will be phrased as "the data favour the framework".

## 0. What has been seen (stated before any choice below)

- CFG667: within f30 early types, OLD − YOUNG = +0.123 dex in log M*_Taylor − log M*_LePhare; matched on Taylor mass the age signal
  falls from +0.166 to +0.032 ± 0.080.
- Record: KiDS matched-mass red − blue +0.35 dex (cm06), colour slope +0.34 dex/mag (CFG115); CFG531's alt footing deficit is
  "explained by a +0.10 dex stellar-mass shift" (inside its ΛCDM-built environment, so not used here).
- The lens table (`lr_lenses.npz`) carries Mgal = M*(1 + f_cold) with f_cold a smooth per-type function of log M* (medians, per
  0.26 dex bin: late 0.14–4.9, early 0.13–1.19; small scatter at high mass). No early-vs-late Taylor-vs-LePhare offset has been
  computed.
- **Author's expectation, before any score:** some reduction of the early excess, size unknown.

## 1. Two baryonic-mass estimators

- **L (LePhare):** M_b,L = Mgal from the table.
- **T (Taylor):** M*_T = 10^(−0.68 + 0.70(g − i) + 0.4(4.58 − M_i)) from LePhare rest-frame absolute g, i (as CFG667); M_b,T = M*_T
  (1 + f_cold,type(log M*_T)), with f_cold,type the per-type median relation of the table's f_cold against log M* (0.1 dex bins,
  linear interpolation, clamped at the ends).

## 2. Test

Sample: f30 lenses (CFG585's head, executed unedited), early (TYP = 1) and late (TYP = 0). For each estimator X:
- 10 bins in log M_b,X (deciles of the early types' log M_b,X); bins with fewer than 300 lenses of either type are dropped and
  reported.
- Late types are re-weighted per bin to the early types' counts (lens weights WG and WW multiplied by N_E,bin/N_L,bin), so both groups
  share one log M_b,X distribution. Early weights unchanged.
- A_X = log10[(W·ΔΣ_early)/(W·ΔΣ_late)] over K9 (bins 6–14; W the CFG700 inverse-variance weights), with the patch jackknife (as
  CFG700). Also reported: the inner band K-in + K-mid (bins 9–14).
- Δ = A_L − A_T with its jackknife (same patches, paired).

**Classes (primary, K9):**
- **ARTEFACT EXPLAINS THE EXCESS** if |A_T| < 2σ_T and Δ ≥ 0.10;
- **EXCESS PERSISTS** if A_T ≥ 0.15 with A_T/σ_T ≥ 3;
- **PARTIAL** otherwise (the reduction Δ and the residual A_T are stated).

Reported: per-bin matched medians of log M_b,X (must agree within 0.02 dex); the median log M*_T − log M*_L for early minus late at
fixed L mass.

## 3. MUTATE (`CFG668_MUTATE=1`, exit 1 iff both bite)

- M1 (null): early/late labels shuffled within each L-mass bin → |A_L| < 2σ.
- M2 (linearity): early WG × 0.8 → A_L shifts by log10(0.8) within 0.002.

## 4. Machine rules

Light: one process, `nice -n 10`; precomputed per-lens stacks; allowed while the 1024³ run is live.
