# Cluster baryon-budget forensic — is the eRASS1 η≈2 a missing-baryon artifact?

*2026-06-14. Carl's challenge: clusters need no second mass component; the ~2× MOND deficit is suspected to be a
methodology/footing artifact, specifically (a) a local/canonical a0 smuggled in, and (b) an incomplete baryon budget +
hydrostatic assumptions inflating the deficit. This file tests the BARYON-BUDGET half on the real eRASS1 data + the
2024–2025 cluster baryon census. Tested on the framework's OWN terms (a0=9.36e-11), both ways.*

Data: `real_research/data/erass1cl_primary_v3.2.fits` (Bulbul+2024). Clean cut (0<z<1, M500>0, Mgas>0, 0.01<fgas<0.30):
**N=9830, z_med=0.30, M500_med=2.0e14 M⊙** (group/cluster boundary). η ≡ g_obs/(ν·g_bar) at R500, framework
de Sitter–Unruh interp g_pred=√(g_bar²+g_bar·a0). Reproduces the banked sample exactly.

## The η ladder (framework a0=9.36e-11, median; geomean in parens)

| baryon budget within R500 | f_b(R500) | η_median | η_geomean | note |
|---|---|---|---|---|
| gas only (FGAS500 as-is) | 0.067 | **2.57** | 2.79 | what the X-ray catalog measures |
| gas + 0.2·gas stars (banked f*) | 0.081 | 2.33 | 2.54 | banked headline 2.15 mixes this with regular-MOND a0 |
| gas + generous stars+ICL (×1.65) | 0.111 | 1.97 | 2.15 | stars/ICL maxed |
| gas → 0.85×cosmic in R500 (sim depletion ceiling) | 0.133 | 1.84 | 1.82 | Planelles Yb,500=0.85 |
| gas → **FULL cosmic** in R500 (impossible ceiling) | 0.157 | **1.69** | 1.67 | every cosmic baryon forced inside R500 |
| to reach η=1 | **0.48** | 1.00 | — | **3.1× cosmic — nonphysical** |

Deep-MOND scaling η∝1/√M_bar verified on the data: η(gas)/η(cosmic)=1.518 vs √(M_cos/M_gas)=1.526. So the +30%-baryons
→ η/1.14 rule the brief cites is exact here.

## Reducers (every honest effect that LOWERS η) with sizes

1. **Stars (f*=0.2, banked):** 2.57→2.33, ×0.91. Real, already in the banked baseline.
2. **Stars+ICL maxed (gas×1.65):** →1.97, ×0.77 from gas. Lit caps stars+ICL at ~1.3–2% of M500 (Andreon/Gonzalez; ICL
   adds 20–40% to a small stellar component), so this is already generous.
3. **Gas → 0.85×cosmic within R500** (the depletion ceiling sims predict, Planelles; Yb,500=0.85±0.03): →1.84.
4. **Gas → FULL cosmic within R500** (theoretical absolute ceiling, physically impossible — clusters are *depleted*,
   never *enriched*): →1.69 median / 1.67 geomean. **This is the floor of any baryon-only fix.**

Net robustness across a0 × interpolation function: gas-only η spans 2.12 (regular MOND a0, std/RAR ν) to 2.57 (framework
a0, simple ν); the full-cosmic ceiling spans 1.37–1.69. **No combination reaches 1.** Mirrors the banked "robust to
baryon budget (1.9–2.4)" — and pushes the ceiling lower (1.67) by going all the way to cosmic.

## Inflaters (every effect that RAISES η / makes the deficit look bigger than the true enclosed one)

1. **Framework a0 < canonical** (9.36 vs 12e-11): +√(1.28)=×1.13 vs regular MOND in deep MOND. This is the one place a
   *lower* a0 is used — it INFLATES η by ~13% vs canonical MOND. (Carl's "did they use a local a0?" — answer: no, the
   framework uses its OWN *lower* a0, which works AGAINST the framework, not for it. Using canonical 1.2e-10 would
   *help*, dropping gas-only η to 2.28.) ~+13%.
2. **R500 is an overdensity radius** (deep-MOND regime g_bar/a0~0.03–0.04): η is read at a radius defined by 500ρ_c, far
   into deep MOND. Not a budget effect; flagged as the regime limitation, not an inflation of the budget per se.
3. **Hydrostatic / WL mass systematic:** M500 is WL-calibrated (eRASS1 uses HSC/DES/KiDS shear), so it is NOT a pure
   hydrostatic-bias number; a residual ~50% scaling-relation systematic on the *absolute* η remains (banked caveat).
   This is symmetric (could go either way), not a one-sided inflater.

## The crux that defeats the missing-baryon hypothesis: the RADIAL location of the missing gas

Carl's instinct is **half right and important**: the budget IS incomplete. The 2024–2025 census is unambiguous —
**at the group/low-mass-cluster scale that dominates eRASS1, the hot gas within R500/R200 is only ~20–40% of the cosmic
baryon budget** (Popesso+2024, arXiv:2411.16555), rising to ~cosmic only in the most massive clusters; eRASS1 gas
fractions are ~2× below older scaling relations (Siegel+2025, arXiv:2509.10455) and ~40% below HSC-XXL at 1e14.

But the SAME literature says WHERE the missing baryons are: **expelled by AGN feedback to BEYOND several R500**, not
hiding inside R500 (Siegel+2025 title: "efficient gas expulsion from groups and clusters"; the baryon fraction "returns
to the universal value at large radii"). **g_bar(R500) depends only on mass ENCLOSED within R500.** Expelled gas sitting
at >R500 does not contribute to g_bar at R500 — so it cannot lower η at R500. The η=1.69–1.84 rungs above are the
*counterfactual* ceiling of cramming all cosmic baryons INSIDE R500, which **directly contradicts the feedback
measurement** that places them outside. The physically-correct enclosed budget keeps η≈2.3–2.6.

## The cleanest sub-test (removes the missing-baryon defense entirely)

In the MOST massive eRASS1 clusters, X-COP (Eckert+2019) shows the gas within R500 is GENUINELY near the universal value
(f_gas,univ=0.131±0.003; X-COP clusters even 7% gas-RICH) — there is no missing-baryon excuse. Handing those clusters
the **full X-COP universal f_b=0.146** (gas 0.131 + stars 0.015):

| sub-sample | N | f_gas_med | η(gas+stars) | η(@X-COP f_b=0.146) |
|---|---|---|---|---|
| M500≥3e14 | 2622 | 0.088 | 2.37 | 2.01 |
| M500≥5e14 | 860 | 0.096 | 2.41 | 2.13 |
| M500≥7e14 | 284 | 0.101 | 2.42 | **2.19** |

**The deficit persists at ~2.0–2.2 exactly where the baryon budget is most complete and gas is near cosmic.** The
deficit does NOT come from missing baryons — if it did, it would vanish in the massive, gas-complete regime. It does the
opposite (mildly worse), because completing the budget helps the *depleted groups* more than the *complete clusters*.

## Could a defensible fuller budget bring η toward 1? — NO.

- The most generous DEFENSIBLE budget (full cosmic f_b inside R500, which over-counts by ignoring real depletion) floors
  η at **1.67–1.69** (geomean/median) — a real ~35% reduction from gas-only, NOT to be dismissed, but **not to 1**.
- η=1 requires f_b=0.48 within R500 = **3.1× cosmic** — you must invent baryons that do not exist.
- The missing baryons are measured to be at >R500, so they cannot act on g_bar(R500) at all; the honest enclosed η stays
  ~2.3–2.6.
- In the gas-complete massive regime the deficit is undiminished (2.0–2.2).

## Grade

**CARL'S BARYON-BUDGET HYPOTHESIS: PARTIALLY VINDICATED ON THE PREMISE, REFUTED ON THE CONCLUSION.**
- *Vindicated:* the eRASS1 X-ray baryon budget IS incomplete — gas within R500 is only ~6.7% of M500 (f_b≈0.08 with
  stars) vs cosmic 0.157, a genuine factor ~2 budget shortfall at the group scale, real and literature-confirmed.
  Completing it is a real, non-trivial reducer (η 2.57→1.69, ×0.66). Do NOT repeat "baryons are fully counted."
- *Refuted:* even the impossible ceiling (all cosmic baryons inside R500) leaves η≈1.67–1.69, not 1; reaching 1 needs
  3.1× cosmic; the missing baryons are measured to be EXPELLED beyond R500 (cannot lower g_bar at R500); and the deficit
  is undiminished (~2.1) in the massive clusters where the budget is already complete. **Baryons close ~⅓ of the gap and
  no more.** The residual ~1.7× at R500 is real and is the standing, MOND-shared cluster mass discrepancy — not a
  budget/footing artifact, and not erased by any defensible baryon census.
- *Footing note (Carl's a0 worry):* the analyses used the framework's OWN a0=9.36e-11, which is LOWER than canonical and
  therefore *inflates* η by ~13% vs regular MOND — the opposite of a local-a0 smuggle. Using canonical 1.2e-10 would
  *reduce* η (2.57→2.28 gas-only). No local/canonical-a0 artifact inflates this deficit; if anything the framework's a0
  choice makes its own cluster problem ~13% worse.

**Net η spread, real data, framework a0:** gas-only 2.57 → defensible-fuller-budget floor 1.67 (geomean). Baryons are a
real ~33% reducer, not a closer.

## Sources
- Bulbul et al. 2024, A&A 685 A106 (eRASS1 catalog, on disk).
- Popesso et al. 2024, arXiv:2411.16555 — hot gas f_gas(M500): groups 20–40% of cosmic within R200, cosmic only at high
  cluster mass; gas expelled to larger radii.
- Siegel et al. 2025, arXiv:2509.10455 — kSZ+X-ray+WL: efficient gas expulsion beyond several R500; f_b returns to
  cosmic at large radius; eRASS1 gas ~2× below FLAMINGO.
- Eckert et al. 2019, A&A 621 A40 (X-COP) — f_gas,univ=0.131±0.003 at R500; massive clusters gas-near-cosmic.
- Planelles et al. 2013 / sims — Yb,500≈0.85±0.03 depletion within R500.
- Andreon 2010 / Gonzalez+2013 — stellar+ICL fraction ~1–2% of M500, weak mass dependence.
