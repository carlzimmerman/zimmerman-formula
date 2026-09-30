# CFG200 — the DR4 separation forecast with the corrected P2 merge band

- **Criteria:** `FROZEN_CRITERIA.md` (7a5f6a314), committed before any number. **κ = ½ FITTED, NOT DERIVED.**
- **Run:** `python3 campaign_fresh_gravity/CFG200_dr4_merge_band_forecast/cfg200_merge_forecast.py`, under a second. The main run exits 0 (4/4 checks). The MUTATE run (merge = 1.000) exits 1: the load-bearing H fails with S = 0 and N₃σ = ∞, and (b) = (c). That is the control biting.
- **Scope.** This is a forecast from frozen budgets. No data are scored, nothing in the preregistration is changed (sha256 prefix 97aa97c40fc1be25, checked), and no verdict language is added. Row labels are quoted from the frozen text.
- **Inputs relayed from CFG191.** The P2 merge values come from CFG191 (the Opus chat's referee lane), relayed by the orchestrator; its re-run is pending. Carry them as provisional until CFG191's outputs are committed. No battery spread was relayed, so no theory error is carried on the merge band.

## Separations at the frozen N = 30,000 (σ_tot = 0.02759; canonical decides)

S is in σ_tot. N₃σ is the pair count for 3σ. The cap is Δ/σ_sys, the separation at infinite N.

| pair | Δ | S(30k) | N₃σ | cap |
|---|---|---|---|---|
| (a) P2-merge floor 1.089 vs ownership 1.000 (g_ext 1.778e-10, primary) | 0.089 | **3.23** | 22,557 | 4.45 |
| (a) P2-merge top 1.102 vs ownership | 0.102 | **3.70** | 14,325 | 5.10 |
| (a) P2-merge floor 1.063 vs ownership (g_ext 2.146e-10) | 0.063 | 2.28 | 264,146 | 3.15 |
| (a) P2-merge top 1.077 vs ownership (g_ext 2.146e-10) | 0.077 | 2.79 | 41,851 | 3.85 |
| (b) P2-merge vs the chain ceiling 1.0725, all four anchors | 0.0045–0.0295 | 0.16–1.07 | never | 0.22–1.48 |
| (c) chain ceiling 1.0725 vs ownership | 0.0725 | 2.63 | 58,850 | 3.63 |
| (d) P2-merge vs Arm A's floor 1.1614 | 0.059–0.098 | 2.15–3.57 | 16,025 to never | 2.97–4.92 |

- **Alt footing (reported):**
  - (a) is 4.02 / 4.60 for the primary g_ext (N₃σ 11,176 / 7,780) and 2.86 / 3.59 for 2.146e-10.
  - (b) is 0.33–1.34, never 3σ.
  - (c) is 3.26 (N₃σ 21,660).
- **At the DR3 dry run's precision** (σ_fit 0.035 at 10,624): every S is lower by a factor of 0.69 at 10,624 pairs and 0.95 at 30,000. Both are in the `.out`.
- **Comparison with CFG63.** There the registered Arm A floor sat 5.85σ above ownership (N₃σ = 4,342). With the corrected P2 merge band the separation from ownership is 2.3–3.7σ canonical, and it needs 14,000–264,000 pairs for 3σ.

## Landing: where a true value falls in the frozen rows

The table uses γ̂ drawn as normal around the true value with σ_tot(30k), on the canonical footing, with the illustrative edges. Contamination is not modelled; the frozen text says it only raises γ̂.

| true value | §1.5 "1.007–1.083, undecided" / "1.083–1.23, framework-band, arm NOT decided" | Arm C "consistent" / "disfavored 2–3σ, not a kill" / "falsified if the stability requirements pass" | chain "consistent" / "above the ceiling, not a kill" |
|---|---|---|---|
| ownership 1.000 | 39.9% / 0.1% (60.0% in "≤ 1.007") | 95.8% / 2.0% / 0.1% | 99.6% / 0.4% |
| chain ceiling 1.0725 | 63.9% / 35.2% | 27.5% / 38.7% / 33.8% | 50.0% / 49.9% |
| P2-merge floor 1.089 (primary g_ext) | 41.2% / 58.6% | 11.6% / 31.2% / 57.2% | 27.5% / 71.8% |
| P2-merge top 1.102 (primary g_ext) | 24.5% / 75.5% | 4.8% / 20.9% / 74.3% | 14.2% / 83.4% |
| P2-merge floor 1.063 (2.146e-10) | 74.5% / 23.4% | 40.0% / 37.7% / 22.3% | 63.5% / 36.5% |
| P2-merge top 1.077 (2.146e-10) | 58.1% / 41.4% | 22.3% / 37.7% / 40.0% | 43.5% / 56.3% |

- The z-rule edges at σ_tot(30k) give the same numbers within 1.5 percentage points. Both are in the `.out`, and the alt footing is there too.
- **z-distances at the P2-merge values:**
  - 1.089: z = +3.23 to 1.000, +0.60 to the chain ceiling, −2.62 to Arm A's floor, −0.04 to the §1.5 hypothesis 1.09.
  - 1.102: +3.70, +1.07, −2.15, +0.43.

## Fixes after the first run (kept)

- The first run exited 1 on C0. The two CFG63 README citations used line numbers 13 and 15 instead of 15 and 17.
- The line numbers were fixed. Every number was identical, and every prereg citation passed in both runs.
- The first run is kept as `*_firstrun*`.
