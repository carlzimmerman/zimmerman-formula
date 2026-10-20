# AG4g FROZEN CRITERIA (2026-10-20): per-galaxy pull census. Who needs a non-stellar-population Υ, and does any property predict it?

Committed alone, before any AG4g script or number. Owner's go (2026-10-20, in chat): "freeze and run the per-galaxy pull test
(law-true mocks for the expected pull fraction, then a pre-declared property scan with a multiple-testing correction), as a
small job beside NC2x" (owner's 10-20 small-job rule: < 1 GB RSS, single thread, minutes).

## Seen before this file (disclosed)
AG4b: with no distance or inclination term, 22.4% (n=1, canonical) and 24.7% (n=2) of galaxies have MAP Υ ≥ 3σ from the prior
centre. No per-galaxy property was looked at.

## Fit (AG4b's pipeline, plus the coherent distance and inclination term, profiled analytically)
- Data: CFG4_common.load_sparc() with AG4b's cuts (170 galaxies). Law n=1, ν₁ = (1 + √(1 + 4/y))/2, at a₀ = 9.3603e-11
  (canonical). Υ grid as AG4b; prior log₁₀Υ ~ N(log₁₀0.50, 0.10); bulge 1.4Υ; s₀ = 0.05 dex.
- Per galaxy, χ²(Υ, c) = Σ_i w_i(r_i − c)² + c²/c_g² + ((log₁₀Υ − log₁₀0.5)/0.10)², with w_i = 1/(σ_i² + s₀²).
  - c_g is CFG4's coherent log-g error from distance and inclination: √((eD/D/ln10)² + (2 cot i · e_i/ln10)²).
  - c is profiled analytically: χ²_min(Υ) = Σwr² − (Σwr)²/(Σw + 1/c_g²) + prior.
- MAP Υ = argmin over the grid. Pull p_g = (log₁₀Υ_MAP − log₁₀0.5)/0.10. A **large pull** means |p_g| ≥ 3.

## Stage 1: is the number of large pulls more than the model expects?
- 200 law-true mocks (seeds 1–200) drawn from exactly the fit's error model: per galaxy, Υ_true from the prior,
  c_true ~ N(0, c_g), and per-point ε ~ N(0, √(σ_i² + s₀²)); log g_obs = log₁₀[ν₁(g_bar(Υ_true)/a₀) g_bar(Υ_true)] + c_true + ε.
- Each mock is refitted identically. N_large is counted for the data and for every mock; p₁ = the fraction of mocks with
  N_large ≥ N_obs.
- **EXCESS** if p₁ < 0.01: the stated errors do not explain the pulls.
- **NO EXCESS** otherwise: the pulls are what the stated errors produce.

## Stage 2: property scan (run in both cases; graded only if stage 1 = EXCESS, otherwise reported as exploratory)
- **Eleven properties**, from the master table, fixed now:
  - Hubble type T; Hubble-flow distance (fD = 1, binary); inclination Inc; quality Q; log L[3.6]; log SBdisk; log Rdisk;
    log M_HI;
  - V_flat (0 treated as missing); eD/D;
  - gas fraction f_g = 1.33 M_HI/(1.33 M_HI + 0.5 L[3.6]).
- **Two statistics per property:** Spearman ρ of the signed pull p_g and of |p_g| with the property. That makes 22 tests.
- **p-values:** two-sided, from 10,000 permutations (seed 20261020); missing values are dropped per test.
- **Correction:** Holm–Bonferroni, family-wise α = 0.05.
- **LEAD:** a test with Holm-adjusted p < 0.05. Its ρ and the galaxies driving it (the top 10 by |p_g|) are reported.

## Secondary (reported, not graded)
- Stage 1 also on n=1 at the alt a₀, and on n=2 at the alt a₀ (its AG4f-paired world), with the same mocks drawn from each.
- AG4b's no-c_g version, so that the 22.4% is reproduced (K1).

## Controls
- K1: with c_g = 0 the large-pull fraction reproduces AG4b's 22.4% (n=1, canonical) to ±1 galaxy.
- K2: on the mocks, the mean pull is within ±0.1 of 0.
- K3: the scan's family-wise false-positive rate on 50 law-true mocks is ≤ 0.10, using 1,000 permutations per test on mocks.

## MUTATE
`AG4G_MUTATE=1` runs the stage 2 scan on a law-true mock with injected property dependence:
log₁₀Υ_true = log₁₀0.5 + 0.10·z_T, where z_T is the standardised Hubble type. The scan must flag T (signed pull, Holm
p < 0.05); the script then exits 1 (the control bites).

## Settings
κ = ½ fitted; not theory closed. A LEAD is a pointer to a systematic or to physics, not a detection. It needs its own
pre-registered test. Outputs: `ag4g.py` → `ag4g.out`, `ag4g_results.json`; MUTATE → `_MUTATE`.
