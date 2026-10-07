# Session 4 calcs: results (2026-10-06) — trying to break Session 3

Criteria: `FROZEN_CRITERIA.md` (C, S and U each frozen before their scripts ran). κ = ½ fitted; both footings. Promoted into committed lane CFG440 (scripts and outputs byte-identical to the exploratory run). All MUTATE runs were detected (exit 1).

| test | script | frozen verdict | key numbers |
|---|---|---|---|
| C: the Session-3 supply rule on the 12 MW classicals | `classicals_supply.py` | **CONSISTENT** at the nominal yield (q = 1); **BROKEN** at yield +0.1 | median −0.158 ± 0.089 (law alone +0.100); yield −0.5 −0.085; yield +0.1 −0.277 |
| C: single-rule check (one q for UFDs and classicals within ×2) | same | **FAIL** | q zeroing UFDs 0.76, classicals 0.18: ratio **4.1** (alt 5.0) |
| S: SPARC residual skew at low g_bar (a binding supply limit predicts negative) | `sparc_skew.py` | **NO SUPPLY SIGNAL** | lowest bin −0.47 ± 0.43 (1.1σ); every bin is negatively skewed, high g_bar included (−0.77 ± 0.32), so the tail is generic |
| U: one universal cold-fluid density, fit on UFDs, predicting the classicals | `universal_density.py` | "PASS" as frozen, but **vacuous** | at ρ_c = 0.63 M☉/pc³ (UFD fit) every classical gets q = 1, so the prediction is just C's −0.158. The classicals alone need 0.030, a ratio of **21** |

## What this settles
- **Session 3's reconciliation is not one rule.** The galaxy-level retention can pay for the UFDs and does not wreck the classicals on the median at the nominal yield. But making both come out right needs the cold mass to be about 4–5× more concentrated (inside r_½) in ultra-faints than in classicals, or about 21× denser under a uniform-sphere model. That is a free parameter per population. It is no longer a zero-parameter result.
- **A physical candidate exists but is untested:** formation epoch. A density ratio of 21 corresponds to ultra-faints collapsing at a (1+z) about 2.8× larger than classicals (for example z ≈ 10 against z ≈ 3). This is the same mechanism ΛCDM uses for halo concentrations, so even a pass would not discriminate. The on-disk LVD table has no ages (0 of 45), so testing it needs star-formation-history data, which needs the owner's go to fetch.
- **No sign in SPARC that the supply limit binds.**

## Caveats
- U's model (uniform sphere) is crude. q = 1 for every classical at the UFD density is a property of that shape.
- All C/U numbers inherit CFG317's leaky-box R_ind and its yield bracket.
