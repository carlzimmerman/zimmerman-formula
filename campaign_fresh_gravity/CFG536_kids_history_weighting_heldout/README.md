# CFG536: CFG534's post-hoc overlap weighting, frozen and run on held-out lenses (stack P minus f30). CONSISTENT on both footings: Δε(early − late) = +0.52 ± 0.18 / +0.47 ± 0.17 (Z 2.84), short of the frozen Z ≥ 3

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (416acbb62), before any script or any held-out number.
- **Script:** `cfg536_heldout.py`. It execs CFG534's `cfg534_kids.py` read-only up to its `SPL = {` line, so the estimator is CFG534's own code path. For the held-out sample it swaps in only the stack-P environment tables. MUTATE (`CFG536_MUTATE=1`) writes `*_MUTATE.*`. The main run reads the MUTATE JSON for the MU1 condition in the verdict.
- **Settings:**
  - κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 are never pooled. The kernel is ν_mono.
  - The cold energy's mass is still required. Nothing was downloaded. This is not "theory closed".
- **Numbers** come from `cfg536_heldout_results*.json`. Pairs are canonical / alt.

## Hypothesis and design
**H:** at fixed stellar mass, early-type (quenched) lenses carry extra settled cold energy beyond the law's minimum, so Δε(early − late) > 0.

**The problem with CFG534's hint:** CFG534 picked its overlap weighting, W_A W_B/(W_A + W_B) per (group, bin) cell, *after* seeing the f30 data. With it, f30 gave Z +3.18. Running it on f30 again cannot confirm anything.

**This lane's design:**
- The estimator is frozen unchanged.
- It is applied to the 124,212 stack-P lenses that are **not** in f30. That sample is disjoint from the weighting choice.
- Scoring uses the validated stack-P environment: CFG529 G1m, W10, measured leakage 0.2234, constructions A and B.
- **Disclosed in the criteria:** the held-out sample is not blind to the record. The unmatched stack-P early/late split was already known (CFG505/509). The mass-matched Δε on this sample had never been computed.

## Controls (all pass, 6/6 main + 4/4 MUTATE)
- **C1 (NOT CONFIRMATORY):** the overlap estimator on f30 reproduces CFG534 exactly (max |d| 0.0): +0.777 ± 0.245 / +0.712 ± 0.224, Z +3.18.
- **C2:** CFG534's frozen estimator on f30 is reproduced exactly: +0.529 ± 0.324 (Z 1.63).
- **C3:** on the held-out sample, the matched model stacks are identical (9e-16).
- **C4:** the held-out sample and f30 are disjoint, and together they make up stack P.
- **C5:** CFG529 G1m is reproduced exactly (0.0).
- **C6:** CFG519's f30 leakage 0.16863 is reproduced exactly.

## Power forecast (stated before scoring)
- The forecast for the overlap σ on the held-out sample was ~0.169 / 0.155, with a declared range of 0.17–0.24.
- **Observed: 0.182 / 0.167**, inside that range. The sample is not "not diagnostic" (the threshold is σ > 0.30).

## Held-out result (K9; constructions A / B agree to 0.001)
| | Δε (overlap, VERDICT) | Z (min of the two SHMR templates) | ε early | ε late | frozen CFG534 estimator (reported) |
|---|---|---|---|---|---|
| canonical | **+0.519 ± 0.182** | **+2.84 / +2.85** | +0.539 | −0.024 | +0.554 ± 0.324 (Z 1.71) |
| alt | **+0.475 ± 0.167** | **+2.84 / +2.85** | +0.406 | −0.107 | +0.508 ± 0.297 (Z 1.71) |

- **By band** (canonical, overlap): K-in +0.53 ± 0.27, K-mid +0.31 ± 0.31, K-out +0.52 ± 0.36.
  - The profile is flat. On f30 it rose outward.
  - KiDS radial shape was already declared non-discriminating in CFG534.
- **Matched late types sit on the law** (ε −0.02 / −0.11 ± 0.15). The excess is carried by the early class.
- **The held-out amplitude is lower than f30's** (+0.52 against +0.78). The difference is 0.26 ± 0.30, about 0.9σ. This is what is expected if part of f30's overlap value was an upward fluctuation that the post-hoc choice of weighting happened to favour.

## MUTATE
- **MU1 PASS:** 50 within-group label shuffles of the held-out sample give mean Z +0.02 and SD 0.99 in all four cells. The shuffles kill the signal, and the jackknife σ is calibrated (SD ≈ 1). Seed 5360 gave Z −0.81.
- **MU2 PASS:** an injected Δε of 0.3 is recovered to 1e-16.

## Companion / leakage mix (L1, L2)
Within a matched cell the environment term is colour-blind and cancels. So a class difference in leaked satellites feeds straight into Δε, with a positive sign.

**L1:** satellite fractions per class (CFG519 S_IC, 48-cell reweighting, 12-region jackknife):

| | all | early | late | Δf (early − late) |
|---|---|---|---|---|
| f30 | 0.169 ± 0.006 | 0.195 | 0.132 | +0.063 ± 0.007 |
| held-out | **0.241 ± 0.003** | **0.273** | **0.178** | **+0.095 ± 0.008** |

- As expected, the held-out sample is less isolated than f30.
- Its class difference is 1.5× f30's. This agrees in direction with CFG509's counts-based stack-P value, Δf +0.055 ± 0.004 (a different estimator).

**L2:** the leakage bias, Δf × the GLS projection of ∂model/∂f on the own template:
- **Held-out: +0.108 / +0.096**, which is 21% / 20% of the measured Δε. This is below the frozen 50% "LEAKAGE-LIMITED" threshold, so no label is attached.
- **Leakage-adjusted Z (reported, no verdict weight): +2.25 / +2.27.**
- For f30 the bias is +0.075 / +0.067 (10%), and the adjusted Z is +2.87.
- **The leakage bias is first order and model-based.** It uses the CFG503/504 host term per unit leaked fraction, and it assumes early-type satellites have the same hosts as late-type ones. If early-type satellites sit in more massive hosts, the bias is larger.

## Verdict (frozen rule)
- **canonical: CONSISTENT.** Z 2.84 / 2.85 in A / B: in [2, 3), same sign, and MU1 passes.
- **alt: CONSISTENT.** Z 2.84 / 2.85.
- **Headline: CONSISTENT on both footings. NOT CONFIRMED at the frozen Z ≥ 3 bar.**

**What this means** (written after the results; no verdict weight):
1. The overlap-weighted early − late excess **reappears on lenses that played no part in choosing the weighting**, with the same sign, at 2.8σ, and the shuffles kill it.
   - That makes the CFG534 hint harder to dismiss as a pure weighting artefact.
   - It is not a confirmation. CFG534's original frozen estimator gives only Z 1.7 on the same held-out lenses.
2. **About a fifth of the held-out Δε is plausibly class-dependent satellite leakage.** Corrected for it to first order, the excess is about 2.3σ.
3. **The amplitude is large.** A held-out Δε of about +0.5 corresponds to roughly the +0.39 dex uniform M* shift that CFG534's amplitude reading gave. That is well above what stellar-mass systematics allow (≤ 0.15–0.20 in CFG531).
   - KiDS cannot tell extra settled cold energy apart from an M/L effect, because the bands are deep-MOND.
   - SPARC's radial pattern (CFG534 Test 3) remains the only on-disk discriminant.
4. **Nothing here says the data favour the framework.** κ is fitted, and the cold energy's mass is still required.

## Dated disclosures (2026-10-09)
1. **Order of runs.** MUTATE was run before the main run, because the main run's verdict reads MU1 from the MUTATE JSON. No criterion changed.
2. **Interpretation.** The "what this means" paragraph and the regression-to-the-mean reading were written after the results. They carry no weight.
3. **No frozen text was edited.** Nothing was downloaded.

## What would decide it
- **More lensing area.** KiDS-Legacy / DR5, a large fetch, would allow a pre-registered overlap-weighted test at σ ≈ 0.1.
- **A per-class leakage measurement with host masses.** Spectroscopic group membership by class, from GAMA G3C on disk, could replace the first-order L2 bias with a measured one.

## Run
```
CFG536_MUTATE=1 nice -n 10 python3 cfg536_heldout.py ; nice -n 10 python3 cfg536_heldout.py
```

κ = ½ is fitted. The cold energy's mass is still required. This is not "theory closed".
