# CFG779: the FRB baryon census excludes black-hole dark energy that eats baryons

**Label: P0 (no conversion) CONSISTENT. P1 (MD14 conserved history, 57% of baryons eaten) EXCLUDED at 16.6σ. P2 (Croker-like,
30% eaten) EXCLUDED at 7.8σ, or 5.6σ with a 5% systematic floor.**

The 114 localized FRBs see the full Big Bang baryon density today: B = 1.064 [1.010, 1.122], both footings.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (25f2c4548). Block CFG770–779 (last ID).
- **Script:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg779.py` (~3 min, exit 0). It imports CFG632's likelihood read-only.
  `CFG779_MUTATE=1` (mock controls) exits 1 as designed.
- **Data:** Sharma et al. 2026 extended sample (114 FRBs, raw DM_exgal and host z), already on disk from CFG632
  (owner-approved fetch).

## Method
- ⟨DM_cosmic⟩(z) = B × the record's mean (BBN Ω_b h², MD14 f_d, h = 0.70).
- Scatter = census PRIMARY σ(z) × A, with ln A free and marginalised.
- Host DM is marginalised over the authors' flat box (μ 4–6, s 0.2–1), with the authors' eq. 1 likelihood.

## Controls

| control | result |
|---|---|
| K1: B = 1 slice reproduces CFG632's lnA | −0.057 / −0.132, exactly as reported |
| K2: injection B = 0.5 (50 mocks) | median ln B −0.705 vs −0.693. **PASS**: the host box does not absorb the mean |
| MUTATE: mocks B = 1 / B = 0.43 | median −0.021 / −0.874 (true 0 / −0.844); separated by 17.2σ. **DIAGNOSTIC** |

## Result

| prediction | sightline multiplier | Z (stat) | Z (+5% sys) | class |
|---|---|---|---|---|
| P0: no conversion (s_b = 1) | 1.000 | +1.19 | +0.86 | CONSISTENT |
| P1: MD14 conserved history (s_b,0 = 0.43, astra) | 0.450 | +16.6 | +11.9 | **EXCLUDED** |
| P2: Croker-like (s_b,0 = 0.70) | 0.710 | +7.8 | +5.6 | **EXCLUDED** |

Survival histories used: s_b(z) = 0.43 / 0.53 / 0.65 / 0.86 (P1) and 0.70 / 0.75 / 0.82 / 0.93 (P2) at z = 0 / 0.5 / 1 / 2.

## Post-hoc (reported only, no verdict weight): which reservoir could black holes convert?
Astra showed (`sol61_push/claude_bh_followthrough_2026_10_14/REPORT.md` §4) that the same expansion history can come from
converting baryons, cold energy, or both. Scored against this fit with the 5% systematic floor:

| partition (astra) | baryon survival today | Z |
|---|---|---|
| baryons only | 0.43 | 11.9 |
| proportional (η = 5.364, keeps Ω_c/Ω_b fixed) | 0.91 | 2.2 (TENSION) |
| cold energy only | 1.00 | 0.9 (CONSISTENT) |

**Reading.** If coupled black holes do source dark energy, the FRBs say the mass converted must come from the **cold
component, not the baryons**. That is a data-driven link between cold energy and dark energy, but the conversion
mechanism, the partition and BH-DE itself are not derived. Cold-only conversion with the MD14 amount takes Ω_c down by
~11%, so Ω_c/Ω_b today ≈ 4.79 rather than 5.364 (astra's table). That is testable against the cluster/lensing record.

## Disclosures
- B is tied to the assumed Ω_b h² (BBN), h = 0.70 (DM ∝ Ω_b h²/h, ±4% for h 0.67–0.73) and the MD14 f_d model. The 5%
  systematic floor above covers these; it is a stated estimate, not a fit.
- The authors' own f_IGM interval (~13%, recalled) is wider because their mean model has halo-gas freedom.
- P2 uses the MD14 shape at Croker's amount; their Trinca history is not reproduced.
- Mock grids are coarser (ln B step 0.05, ln A step 0.1) than the data fit; this is a numerical choice.
- κ fitted; not theory closed.
