# CFG465: input audit of the globular verdicts (CFG332, CFG333)

The criteria were frozen first, in commit 4a31670c2 (`FROZEN_CRITERIA.md`). κ = ½ is fitted and held fixed. Both footings (9.36e-11 / 1.13e-10) are scored separately. Only on-disk data were used; nothing was downloaded.

The question comes from failure-ledger row 10, which rates the tile "Globulars + ownership rule" (CONDITIONAL) as HIGH artefact risk: Pal 3's dispersion is unsourced and Pal 14's is unsettled. This lane traces every input of CFG332 and CFG333 to its source, then re-runs both verdicts three ways:
- on sourced inputs only;
- on every alternative value the record holds, as a full factorial of 768 variants;
- on the committed inputs, as a control.

## Verdict
**Tile: FRAGILE.** The verdict moves, and the direction matters.

- **CFG332's frozen NOT for class E (globulars Newtonian, T = 2.83σ) is FRAGILE.** It rests entirely on Pal 3's unsourced 1.70 km/s.
  - On sourced inputs only, T falls to 0.88σ on both footings and the label becomes **MATCH**.
  - The label flips in 500 of the 768 variants. That includes every variant that drops Pal 3.
  - It also flips in 116 of the 384 variants that keep Pal 3. All of those use BH2018's luminosities, under which Pal 3 is 1.75× brighter.
- **CFG333's globular cell under its own rule R2 (PASS) is ROBUST** (0 of 768 flips). So is the CFG333 decision, PARTIAL (3 of 4; the ultra-faints fail). Two caveats:
  - The robustness is partly built into the statistic. It is a one-sided L plus a wide Υ band, so even MUTATE's doubled Pal 4 still passes.
  - At a prior centre of Υ = 2.2 (reported, not scored) the sourced-only L reaches 2.12.
- **The tile number is ROBUST:** class E with the published errors (AUDIT), T = 1.58σ, stays below 2σ in all 768 variants. The worst variant reaches **1.997σ**, a knife-edge (BH2018 D and r_h, Frank, Jordi, Pal 3 kept).
- **Globulars under the law stay excluded: ROBUST.** This holds for h93 (law + algebraic EFE), B's isolated law and the full QUMOND EFE.
  - On sourced inputs the tension *rises*: h93 5.77 / 6.04σ (was 4.13 / 4.46), isolated law 6.63 / 6.88σ, QUMOND 5.84 / 6.10σ.
  - The lowest values anywhere in the factorial are 3.63 / 3.99σ (h93), 4.87 / 5.19σ (isolated law) and 3.84 / 4.17σ (QUMOND).
- **Route 2 (MF-slope Υ, already CONDITIONAL) is FRAGILE.** Branch K reaches MATCH, as low as 1.31 / 1.59σ, only with BH2018 luminosities, 2023 MF slopes and the catalogue's Pal 14 value. Branch S flips on canonical only, in 12 variants.
- **Sourced-only keeps 3 of 4 clusters:** NGC 2419, Pal 4 (Frank+12) and Pal 14 (Jordi+09). That meets the frozen threshold of at least 3.
  - At the stricter paper-verified level only Pal 4 and Pal 14 qualify, which is **UNSUPPORTED** under the same rule.
  - There, class E gives T = 0.94σ and R2 still passes.

**Plain reading.** No sourced input supports the claim that globulars contradict Newton-at-stellar-M/L (class E). That claim came only from Pal 3's unsourced number. The claim that globulars contradict the law holds under every input the record holds. Class E being consistent is still *Newton fitting*, not evidence for the framework (AUDIT). Ownership from an action remains OPEN.

## Input provenance

| input | cluster | value used | grade | source on disk / cited | alternative in the record |
|---|---|---|---|---|---|
| σ_obs | NGC 2419 | 4.771 (bins interpolated at r_h; N 62) | **B** catalogue-only | Baumgardt web veldisp table: 3 bins, N 62/62/59 = 183. BH2018 lists 195. Ibata+11 and Baumgardt+09 are named, but neither value nor star list is on disk | light-weighted global 4.648 ± 0.407 (N 183) |
| σ_obs | Pal 3 | 1.70 +0.38/−0.30 (N 22) | **U UNSOURCED** | Web table only. BH2018 lists 14 members, so 8 stars came from an unnamed source. The catalogue's own Newtonian model (σ₀ 0.80) sits 3σ below the bin | none measured (σ₀ is a model output and is excluded) |
| σ_obs | Pal 4 | 0.88 +0.20/−0.17 (N 23) | **A** paper-verified | N 23 = BH2018 23 = Frank+12 (MNRAS 423, 2917), whose 0.87 ± 0.18 is quoted in h93 | Frank+12 0.87 ± 0.18 |
| σ_obs | Pal 14 | 0.71 +0.18/−0.14 (N 16) | **C MISMATCHED** | N 16 = Jordi+09's 16 stars (AJ 137, 4586), but Jordi reports 0.38 ± 0.12 (quoted in h93). BH2018 lists 17 | Jordi+09 0.38 ± 0.12 (A) |
| D_sun | all | 88.47 / 94.84 / 101.39 / 73.58 kpc | A | Baumgardt & Vasiliev 2021, via the 2023 table | BH2018 "literature" distances 83.20 / 92.50 / 103.00 / 71.00 |
| R_GC | all | 95.93 / 98.17 / 104.05 / 68.55 kpc | A (derived) | 2023 table; reproduced to 4e-5 from D with R₀ = 8.178 kpc (C5) | recomputed at the BH2018 D: 90.66 / 95.83 / 105.65 / 65.98 |
| V | all | 10.56 / 14.56 / 14.23 / 14.13 | B | 2023 table; the primary photometry is not named | via the BH2018 L_V below |
| E(B−V) | all | 0.08 / 0.04 / 0.01 / 0.04 | cited, not on disk | hard-coded as "Harris (2010)" | none |
| L_V | all | rebuilt from V, E(B−V), D | B | matches the 2023 Mass/(M/L) to 1–3% | BH2018 Mass/(M/L_V). At a common D: NGC 2419 ×0.99, **Pal 3 ×1.75 (−0.61 mag)**, Pal 4 ×0.96, **Pal 14 ×0.62 (+0.52 mag)** |
| r_h,l | all | 19.76 / 20.16 / 15.88 / 27.63 pc | B (N-body fit to the light profile) | 2023 table | BH2018 `rmlp` 18.29 / 19.69 / 17.87 / 23.60 |
| Υ_V prior | all | lognormal(1.6, 0.15 dex) | assumption | h93's SPS fiducial; no SPS table on disk | band edges 1.3 / 2.2 (reported); route-2 Υ_MF |
| MF slope (route 2) | all | −1.57 / −1.14 / −0.34 / −1.26 | B (Newtonian N-body) | 2023 combined table | BH2018: −1.50 (d) / −1.50 (d) / −1.52 (c) / −1.52 (c). Note d means estimated from the relaxation time |
| M_MW,b (external field) | all | 6e10, point mass | parameter | h93 / FG001 / CFG333 | 5e10 (h37), 7.3e10 (CFG286) |
| binary correction | all | none | not applied | no measured correction on disk (CFG334 is a model) | none |
| σ₀, M_dyn, M/L_dyn | all | never used as inputs | Newtonian model outputs | used only as checks | — |

## Provenance gaps (flags)
1. **Pal 3, σ = 1.70: UNSOURCED** (confirmed). No paper in the record names its 22 stars, and the BH2018 sample was 14.
2. **Pal 14: MISMATCHED.** The catalogue gives 0.71 for the same 16 stars on which Jordi+09 measured 0.38. This one swap moves h93 from 4.13 to 5.46σ, and class E from 2.83 to 3.12σ.
3. **NGC 2419: catalogue-only.** This gap is not in the ledger. The sample (183 stars) matches no named paper; BH2018 lists 195.
4. **The luminosities disagree between catalogue versions.** This gap is new.
   - BH2018's own Mass/(M/L_V) makes Pal 3 1.75× brighter and Pal 14 0.62× fainter than the 2023 V photometry. That is 0.61 and 0.52 mag, far outside V's ±0.03 mag.
   - This one swap moves class E from 2.83 to 2.09σ, and route 2K from 2.17 to 1.53σ.
5. **E(B−V) is cited "Harris (2010)" but the catalogue is not on disk.** The record holds no alternative.
6. **The Υ_V = 1.6 centre has no SPS table on disk.**
7. **No binary correction exists for any of the four clusters.**

## One-at-a-time swaps (T, canonical/alt)

| swap | 1(a) class E | h93 | isolated law | route 2 K | QUMOND | tile (class E, published errors) |
|---|---|---|---|---|---|---|
| BASE | 2.83 | 4.13 / 4.46 | 5.07 / 5.41 | 2.17 / 2.40 | 4.28 / 4.62 | 1.58 |
| drop Pal 3 | **0.27** | 4.42 / 4.72 | 5.30 / 5.59 | 2.33 / 2.63 | 4.54 / 4.83 | −1.26 |
| Pal 14 = Jordi | 3.12 | 5.46 / 5.75 | 6.38 / 6.67 | 3.72 / 3.94 | 5.56 / 5.86 | 1.87 |
| L_V = BH2018 | 2.09 | 3.87 / 4.23 | 4.98 / 5.33 | **1.53 / 1.84** | 4.05 / 4.41 | 0.90 |
| D = BH2018 | 2.92 | 4.03 / 4.35 | 4.99 / 5.32 | 2.14 / 2.35 | 4.17 / 4.50 | 1.71 |
| NGC 2419 global | 2.95 | 4.36 / 4.70 | 5.27 / 5.63 | 2.34 / 2.60 | 4.51 / 4.86 | 1.56 |

The other swaps (Pal 4 = Frank, r_h = BH2018, M_MW,b = 5e10 or 7.3e10, MF slope = BH2018) move no verdict on their own. The full table is in `cfg465_globular_inputs.out` §5.

## Controls (6/6 pass) and MUTATE (3/3 pass)
- **C1.** BASE reproduces CFG332 exactly: all six routes on both footings, the frozen labels, and the no-Pal-3 and published-alt cells (|ΔT| = 0.0000).
- **C2.** BASE reproduces CFG333's globular cells R0–R3 and its PARTIAL decision (0.0000).
- **C3.** BASE reproduces AUDIT's published-error T: 1.58, and 3.22 / 3.54.
- **C4.** BH2018 parses to N_RV 195/14/23/17 and D 83.20/92.50/103.00/71.00. The three 2023 copies agree exactly.
- **C5.** R₀ = 8.178 kpc reproduces the 2023 R_GC to 3.5e-5.
- **C6.** The Kroupa input gives Υ_MF = 1.6.
- **MUTATE** (Pal 4's σ doubled):
  - Pal 4's per-object z moves by at least 3.07 in all 16 route-footings, and its class flips in all 16.
  - The other three clusters do not move (Δz = 0).
  - Informational: the doubling turns route 2 into MATCH, CFG333 R3 into PASS, and the tile number into a fail. CFG333 R2 still passes.

## Needs owner go (not fetched)
- Individual-star, multi-epoch radial velocities:
  - Pal 3 (source paper unknown; the catalogue's Pal 3 RV source paper is needed first);
  - Pal 4 (Frank+12);
  - Pal 14 (Jordi+09).
- NGC 2419 star lists (Ibata+11, Baumgardt+09).
- The Harris 2010 catalogue, for E(B−V) and M_V, which would settle the luminosity disagreement between catalogue versions.
- Measured local MF slopes (Jordi+09, Frank+12 HST).

## Run
```
python3 campaign_fresh_gravity/CFG465_globular_inputs_audit/cfg465_globular_inputs.py                  # ~1.5 min, 6/6
CFG465_MUTATE=1 python3 campaign_fresh_gravity/CFG465_globular_inputs_audit/cfg465_globular_inputs.py  # ~1 s, 3/3, writes *_MUTATE.*
```
- Outputs: `cfg465_globular_inputs.out` and `_results.json`. The JSON holds every factorial variant, the classes, the margins and per-object z.
- MUTATE outputs: `cfg465_globular_inputs_MUTATE.out` and `_MUTATE_results.json`.
- CFG332, CFG333 and AUDIT are read-only. None was edited.
