# CFG470: a second hole for the light end, and PG 1426+015 feasibility. The light end STAYS OPEN.

Criteria 0b70d2b38 (committed alone, before any fetch). Script `cfg470_second_hole.py`: 6/6 checks pass, and the MUTATE run exits 1 (detected). `fetch_aux.py` is the one-off informational lookup. Every number below comes from `cfg470_second_hole.out` / `_results.json`.

## Verdict

**Part A: CANDIDATE FOUND (frozen rule), but only on paper.**
- 6 BASS DR2 broad-line AGN pass S1-S6 (1.1-2e9 Msun, z ≤ 0.31, Brγ/Paα in K, dec ≤ +30, λ ≥ 0.01).
- Two of them close the light end together with PG 1426+015, *at their catalogue masses*, if all three conditions below hold:
  - every mass is known to ±10%;
  - both spin edges are ≥ 0.98;
  - the true mass equals the catalogue value.
- The two:
  - **HS 0749+1943**: 1.45e9, z = 0.117, dec +19.6, top-ranked;
  - **1RXS J084521.7-353048**: 1.48e9, z = 0.137, dec -35.5.
- The frozen ranking metric then integrates over the virial-mass scatter (0.3 dex):
  - E98 ≈ 0.69-0.70 for all six candidates;
  - P(close) ≈ 0.10 each.
  - So the metric barely separates them, and each has about a 10% chance that its GRAVITY mass would land where the pair closes.
- The AGN Black Hole Mass Database and the vdB16 RM table have nothing in 1.1-2e9 at z ≤ 0.31.

**Part B (`PROPOSAL_MEMO.md`): the premises behind CFG444's 34% / 56% are beyond what has been demonstrated.**
- **Mass.** ±10% is 0.04 dex. The best achieved GRAVITY BLR-based mass is about 0.06 dex, from SARM on NGC 3783. GRAVITY+-only masses carry 0.11-0.28 dex.
- **Spin.** W25 quote a reflection-spin systematic of Δa* ~ 0.1, so a robust edge is at most about 0.85-0.90.
  - Their hard band alone, with no soft-excess assumption, gives only a* ≳ -0.15.
  - A labelled ESTIMATE puts a hard-band edge of 0.9 at about 23× W25's exposure: NuSTAR ~2.5 Ms and pn ~1.7 Ms.
- **Realistic exclusion for PG 1426+015:**
  - best case (e = 0.15, edge 0.89-0.9): 5-9%;
  - typical case (e ≥ 0.2): 0%.
  - Adding HS 0749+1943, which has no RM lag and so no SARM route, changes nothing under those conditions.

## Controls

| control | result |
|---|---|
| K0: CFG367 code and CSV sha256; control run reproduces CFG367's intervals | PASS |
| K1: CFG444 PG 1426+015 (9.12e8, ±10%) | 0.335 / 0.565 at a ≥ 0.9 / 0.98, matching CFG444 to 1e-12 (CFG444's README rounds these to 0.34 / 0.56) |
| K2: CFG444 pair PG 1426+015 + Q2237+305, a ≥ 0.98 | 0.870, reproduced |
| MUTATE (CFG470_MUTATE=1, all spins 0) | all 150 fractions are 0, detected, exit 1 (`_MUTATE` outputs kept) |

## Ranked candidates

Pair with PG 1426+015, both at ±10%. C98 is at the catalogue mass; E98 is averaged over a 0.3 dex true-mass scatter.

| # | object | log M (method) | z | dec | λ | K (2MASS) | X-ray archive | C98 | E98 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | HS 0749+1943 | 9.16 (Hα; Hβ 9.29) | 0.117 | +19.6 | 0.019 | 12.9 | NuSTAR 20 ks accepted; no XMM | 1.000 | 0.698 |
| 2 | 1RXS J072352.4-080623 (Sy1.9) | 9.08 | 0.145 | -8.1 | 0.032 | 14.2 | none | 0.875 | 0.694 |
| 3 | 1RXS J084521.7-353048 | 9.17 (Hβ 8.93) | 0.137 | -35.5 | 0.023 | 12.5 | NuSTAR 11 ks | 1.000 | 0.697 |
| 4 | 3C 206 | 9.22 (Hβ 8.58) | 0.198 | -12.2 | 0.093 | 12.8 | NuSTAR 17 ks | 0.965 | 0.697 |
| 5 | Q1739+184 | 9.23 (Hβ) | 0.186 | +18.5 | 0.032 | 13.7 | NuSTAR 23 ks | 0.935 | 0.696 |
| 6 | 2E 233 | 9.27 (Hα) | 0.171 | +14.8 | 0.022 | 12.1 | NuSTAR 20 ks accepted | 0.815 | 0.690 |

The script also lists 11 near misses (0.8-1.1e9 or 2-3e9).

## Departures (disclosed)

1. **Tie handling.** The frozen tie rule (|ΔE98| < 0.005, then E90) is implemented as bucketing by round(E98/0.005). That is why #2 (C98 0.875) ranks above #3 (C98 1.000).
   - Because all E98 values fall within 0.008 of each other, the order within the list carries little information. C98 and P(close) are the informative columns.
2. **Informational lookups that were not frozen**: 2MASS K and NuSTAR/XMM archive exposures (`fetch_aux.py`). They are not cuts.
3. **Spin edges 0.85 / 0.89 were not frozen.** They equal a_true of 0.95 / 0.998 minus W25's systematic of 0.1, and are added to the Part B grid as rows labelled D3.
4. **The exposure ESTIMATE was not frozen.** It assumes Δχ² ∝ T·(Δr_isco)² and that the hard-band 90% edge at -0.15 corresponds to Δχ² = 2.71 against a near-maximal best fit. It is an order-of-magnitude scaling, not a simulation.
5. **S5 used the catalogue L_bol over L_Edd at the mass actually used** (MR22 Hα), not Koss22's logEdd, which is based on Koss's adopted mass.
   - All five candidates in Koss table 9 also pass on Koss's own logEdd (-0.46 to -1.94).
   - 2E 233 is not in Koss table 9 and uses CFG444's 8 × L(14-195) estimator.
6. **CFG444's `dmask` is re-stated verbatim, not imported.** CFG444 is a script that rewrites its own outputs when run. Its numbers are reproduced exactly (K1, K2).
7. **J/ApJS/261/1 has no VizieR tables.** The DR2 catalogue quantities come from J/ApJS/261/2 table 9.

## Owner items

1. **No proposal is recommended on the current premises.** CFG444's 34-56% for PG 1426+015 needs a ±10% mass and a spin edge of 0.9-0.98. Neither has been demonstrated, and W25's own systematic forbids an edge of 0.98.
2. **If a PG 1426+015 program is still wanted**, the defensible ask is a GRAVITY+ Paα/Brγ SARM mass plus a fakeit study with W25's models. The study would replace this lane's exposure estimate before any X-ray time is requested.
3. **HS 0749+1943 and 1RXS J084521.7-353048 are the best second holes on paper.** Neither has an RM lag, an XMM pointing or a deep NuSTAR pointing.

## Scope

- A gravity-only test. It bounds where the field's mass can be and detects nothing.
- κ = ½ is fitted. The cold-fluid amount stays free.
- No dark-matter particle species is claimed. The theory is not closed.
