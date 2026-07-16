# FORK CONFRONTATION — a0(z) footing fork vs in-hand high-z TFR zero-points (Lane C)

**2026-07-16.** Script: `fork_confrontation.py` (exit 0; re-derives the banked anchors of
`prep_2026/btfr_forecast_audit/btfr_forecast_check.py` before computing anything — canonical
dlogV(z=3) = −0.033, ALT +0.164, opposite signs; ΛCDM halo term −0.346 at z=1 reproduces
Jeanneau+26's −0.34). Data: `DATA_LEDGER.md` / `data_ledger.csv` (all real published numbers,
cited there). Figure: `fork_confrontation.png`.

**Convention:** Δb = bTFR zero-point offset along the mass axis at fixed velocity vs local, dex.

## 1. Predictions (exact per-sample, framework's own ν, each footing's own a0)

The deep-MOND mapping Δb = −log10(a0(z)/a0(0)) is NOT available in hand: every published sample
sits at g_bar ≈ (0.3–7) a0. The exact fixed-g_obs prediction Δb = log10[g_bar(a0(z))/g_bar(a0(0))]
per usable sample:

| sample (bTFR) | z | g_bar/a0 (canon) | canonical Λ | canonical CPL | ALT | canon+size | ALT+size |
|---|---|---|---|---|---|---|---|
| Jeanneau+26 lensed | 0.9 | 0.30 | 0.000 | −0.006 | **−0.179** | −0.060 | −0.226 |
| Übler+17 KMOS3D | 0.9 | 1.66 | 0.000 | −0.002 | −0.081 | −0.148 | −0.218 |
| Übler+17 KMOS3D | 2.3 | 2.32 | 0.000 | +0.014 | −0.206 | −0.281 | −0.467 |
| Amvrosiadis+25 DSFG | 2.4 | 6.44 | 0.000 | +0.006 | −0.096 | −0.352 | −0.438 |

"+size" = the framework's OWN constant-a0 prediction once observed disc compactness
(R ∝ (1+z)^−0.75, van der Wel+14) is folded in — at high g, M_bar = v²R/G tracks size; in
deep-MOND (Jeanneau) the size term nearly cancels. This term is mandatory, not optional.

## 2. Confrontation (honest bands: stat ⊕ full per-row systematic budget)

Usable measurements (bTFR only — the fork's observable): Jeanneau+26 0.00 ± 0.06(stat) ± 0.27(sys);
Übler+17 −0.44 ± 0.04 ± 0.35 (z≈0.9) and −0.27 ± 0.05 ± 0.35 (z≈2.3); Amvrosiadis+25
−0.26 ± 0.19 ± 0.30. Honest χ² (4 points):

| model | χ² z~1 | χ² z~2.3 | Σ |
|---|---|---|---|
| canonical pure-Λ (a0 const) | 1.56 | 1.12 | 2.68 |
| canonical DESI-CPL (a0 declining) | 1.54 | 1.21 | 2.75 |
| ALT ρ_tot/cH0 (a0 rising) | 1.46 | 0.25 | 1.70 |
| canonical const-a0 + size evol. | 0.73 | 0.07 | **0.80** |
| ALT rising-a0 + size evol. | 1.07 | 0.56 | 1.63 |
| ΛCDM halo edge (no gas comp.) | 1.43 | 2.50 | 3.93 |

## 3. Verdicts (straight)

- **z≈1: UNDERPOWERED.** The bin's two bTFR points are mutually 6σ inconsistent on stat errors
  (Jeanneau 0.00 vs Übler −0.44). The best-in-hand point (Jeanneau — the only near-a0-regime
  sample, g_bar ≈ 0.3 a0) leans **canonical at 0.65σ**; the full bin leans <1σ either way
  (a0-only lane: ALT by 0.32σ; size lane: canonical by 0.85σ). Binding systematic: model-mediated
  gas masses (Tacconi scaling + NeutralUniverseMachine HI, 0.8 dex scatter) + local bTFR ZP ±0.16
  → ±0.27 band vs 0.08–0.18 dex per-sample fork separation.
- **z≈2.3: WASH by degeneracy.** The concordant −0.27 (Übler/Amvrosiadis) leans ALT on the
  a0-only lane (0.93σ) but canonical+size once the mandatory compactness term enters (0.42σ).
  At g_bar = (2–6) a0 only 7–18% of the a0-lever survives; the measurement is simultaneously
  ALT-shaped, ΛCDM-halo-shaped, and canonical+size-shaped — unattributable.
- **COMBINED: WASH/UNDERPOWERED.** Canonical-vs-ALT = 0.99σ (ALT side) on the a0-only lane,
  0.95σ (canonical side) with the size term — the lean flips sign under a known, mandatory
  astrophysical systematic. The naive stat-only 7.8σ is FORBIDDEN as a claim (it treats
  scaling-relation gas masses and cross-convention offsets as noiseless).
- **Neither footing is preferred or excluded by in-hand high-z TFR data.**

## 4. ΛCDM-degeneracy statement (mandatory check)

ALT's undiluted Δb = −log10 E(z) tracks the standard halo-scaling drift
−log10[E(z)√(Δc(z)/Δc(0))] to within **0.118 dex max over z = 0.5–5**: a negative measured drift
can never pick ALT-MI over ΛCDM disk evolution anywhere probed. A flat bTFR is
canonical-compatible but ΛCDM-absorbable via rising gas fractions (Jeanneau+26's own reading of
their 0.00). The fork is **internally decisive (canonical vs ALT) exactly as banked, but is not an
MI-vs-ΛCDM discriminator at any in-hand z**.

## 5. What breaks the wash

1. **Jeanneau+26 low-acceleration third refit** (in-hand data, needs a refit): at g_bar < 0.5 a0
   the size term ~cancels (deep-MOND kills R), canonical stays ~0, exact ALT = −0.15…−0.20;
   a stable 0.00 ± 0.10 would be the first real published-data constraint on the ALT branch.
2. **DESI DR3 w0–wa**: sets the canonical-CPL amplitude (+0.09 dex undiluted at z=2.3);
   w → −1 collapses canonical to exactly flat.
3. **Deeper JWST kinematics**: N ≈ 15–40 clean rotators at z = 2.5–3.5 **selected at
   g_bar ≲ 0.3 a0** (the banked forecast) — there the 0.20 dex velocity-axis fork separation
   clears the 0.04–0.06 dex floor AND the size/gas degeneracies cancel. No current published
   sample meets the selection.
