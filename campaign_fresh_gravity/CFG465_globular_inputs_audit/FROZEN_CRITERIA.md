# CFG465 FROZEN CRITERIA: input audit of the globular verdicts (CFG332, CFG333)

**Lane:** CFG465. On-disk data only; no downloads. κ = ½ is FITTED and held fixed. Both footings, a₀ = 9.36e-11 and 1.13e-10 m s⁻², are scored and reported separately. Kernels as committed: CFG332's exp-RAR `nu_s` form, CFG333's `nu_mono` (`CFG3_common`, read-only). Written before any CFG465 code was run or any CFG465 number computed.

**Disclosure.** Some sensitivities are already on the record and make parts of the outcome predictable: CFG332's "no Pal 3" T = 0.27 (class E) and "published-alt" T = 3.13; AUDIT_GLOBULARS' published-error T = 1.58 (class E) and −0.42 (class E, no Pal 3, Jordi's Pal 14). The provenance grades below are fixed by reading the record, not by any score.

## Question
Board tile "Globulars + ownership rule" is CONDITIONAL. The failure ledger (`LEDGER_failure_mechanisms_2026-10-08/README.md`, row 10) rates its artefact risk HIGH: Pal 3's 1.70 km/s has no named source; Pal 14 is unsettled (0.71 vs 0.38 ± 0.12). Does the CFG332/CFG333 verdict survive (a) sourced inputs only and (b) every alternative value the record holds?

## Provenance grades (fixed now, from the record)
Dispersions:
- **A, paper-verified:** the value, or a catalogue bin whose star count and value match a named paper in the record.
  - Pal 4: catalogue 0.88 (+0.20/−0.17, N 23) = BH2018 table2 N_RV 23 = Frank+12 0.87 ± 0.18 (N 23, quoted with its reference in `hunt_2026/h93_outer_halo_globulars.py`).
  - Pal 14: Jordi+09 0.38 ± 0.12 (N 16, quoted with its reference in h93).
- **B, catalogue-only:** a named catalogue bin whose star sample matches no named paper's sample, with no contrary evidence in the record.
  - NGC 2419: three bins, N 62/62/59 = 183 (BH2018 lists 195). Candidate primaries Ibata+11 and Baumgardt+09 are named in the record, but neither their values nor their star lists are on disk.
- **C, mismatched:** a catalogue bin contradicted by the named paper for the same stars. Pal 14 catalogue 0.71 (+0.18/−0.14, N 16) vs Jordi+09 0.38 on 16 stars.
- **U, unsourced:** Pal 3 catalogue 1.70 (+0.38/−0.30, N 22). No paper in the record names its stars. BH2018 lists 14 members, so 8 were added from an unnamed source. The catalogue's own Newtonian model (σ₀ 0.80) sits 3σ below it.
- **Excluded as an observed value:** Newtonian N-body model outputs (σ₀, M_dyn, M/L_dyn). They are never used on the observed side.

Other inputs (graded, none dropped):
- **D_sun:** Baumgardt & Vasiliev 2021 via the 2023 catalogue (A). Alternative: BH2018 table2 "literature" distances (A).
- **R_GC:** derived from D and the position. The geometry uses R₀ = 8.178 kpc, which must reproduce the 2023 R_GC (control C5).
- **V:** 2023 catalogue, primary photometry unnamed (B). E(B−V) is hard-coded as "Harris 2010": cited, the catalogue not on disk, one value only.
- **L_V alternative:** BH2018 table2 Mass/(M/L_V) (A, derived), the luminosity BH2018 used.
- **r_h,l:** 2023 catalogue, from N-body fits to surface-density profiles (B). Alternative: BH2018 projected half-light radius `rmlp` (A).
- **MF slope (route 2):** 2023 catalogue (B, Newtonian N-body). Alternative: BH2018 slope (A; notes c/d) with the 2023 Δα.
- **M_MW,b (external field):** 6e10 in h93, FG001 and CFG333 (a parameter). The record's bracket is 5e10 (h37) and 7.3e10 (CFG286).
- **Υ_V prior:** lognormal(1.6, 0.15 dex) is an assumption. No SPS table is on disk. The band edges 1.3 and 2.2 are reported as a sensitivity of class E only; they are not scored.
- **Binary corrections:** none applied in CFG332/333. No measured correction is on disk; CFG334 is a model, not a measurement. Not varied.

## Variants
- **BASE:** the committed inputs. This is a control: it must reproduce CFG332 and CFG333.
- **(a) SOURCED-ONLY, scored:** grades A and B only.
  - Pal 3 is dropped.
  - Pal 4 uses Frank+12.
  - Pal 14 uses Jordi+09.
  - NGC 2419 uses the catalogue bins at r_h.
  - All structural inputs stay at BASE, because all are sourced.
- **(a′) PAPER-VERIFIED, reported:** grade A only, i.e. Pal 4 and Pal 14.
- **(b) ALTERNATIVES, scored:** the full factorial over the record's alternatives. Distance, luminosity and radius are rescaled consistently (L ∝ D², r ∝ D, R_GC recomputed).

  | input | values |
  |---|---|
  | NGC 2419 σ | at r_h (4.77, N 62); light-weighted global over its 3 bins (N 183; AUDIT 1b) |
  | Pal 3 σ | 1.70; dropped |
  | Pal 4 σ | catalogue; Frank+12 |
  | Pal 14 σ | catalogue; Jordi+09 |
  | D | 2023; BH2018 |
  | L_V | 2023 V; BH2018 |
  | r_h | 2023; BH2018 |
  | M_MW,b | 6e10; 5e10; 7.3e10 |
  | MF slope | 2023; BH2018 (route 2 only) |

  One-at-a-time swaps from BASE are reported to attribute any flip.

## Verdict elements, each footing separately
Statistics, all exactly as committed:
- CFG332's T: two-sided, Υ-marginalised χ²_(N−1) Fisher, 4000 draws, seed 931.
- CFG332's MATCH / PARTIAL / NOT rule, where PARTIAL's "half the h93 T" uses the same variant's h93 T.
- CFG333's GC cell: joint-Υ t against the band [1.3, 2.2] AND the one-sided L, both < 2σ. Labels R0–R3 are recomputed per variant.

Elements:
- **E1** CFG332 route 1(a): class E, Newton.
- **E2** route 1(b-EFE).
- **E3** route 1(b-B).
- **E4/E5** route 2, branches S and K.
- **E6** route 3 (QUMOND monopole flux).
- **E7** CFG333 GC cell under R2.
- **E8** CFG333 GC cells under R0, R1 and R3.
- **E9** CFG333 decision. The WB, CL and UFD cells are read from the committed `cfg333_one_rule_results.json`; GC inputs do not enter them.
- **E10 (tile number, tracked):** AUDIT's published-error T (log-normal bin errors ⊕ 0.075 dex). Reported for class E and for law + EFE. For the NGC 2419 global variant, the error is propagated from its bins.

## Classes (per element, per footing; and for the frozen combined label)
- **UNSUPPORTED:** (a) retains fewer than 3 of the 4 clusters. Under (a′) this applies at the paper-verified level; it is reported, not scored.
- **ROBUST:** the pass/fail at 2σ (and the frozen label) is identical in BASE, (a) and every (b) variant.
- **FRAGILE:** any change. Every flipping input is named.
- **Tile class:** the tile is ROBUST only if E1, E7 and E9 are all ROBUST. It is FRAGILE if any one is.

## Controls (a failure is kept and reported)
- **C1:** BASE reproduces CFG332's committed T, all six routes × 2 footings, ±0.01. It also reproduces route 1(a)'s and 1(b-EFE)'s no-Pal-3 and published-alt T. The matching factorial cells must equal them.
- **C2:** BASE reproduces CFG333's GC cells (t_joint, L) for R0–R3, both footings, ±0.01.
- **C3:** BASE reproduces AUDIT's published-error T: 1.58 (class E), and 3.22 / 3.54 (law + EFE), ±0.01.
- **C4:** BH2018 table2 parses to N_RV 195/14/23/17 and D 83.20/92.50/103.00/71.00. The three on-disk copies of the 2023 table agree (< 1e-6).
- **C5:** R₀ = 8.178 kpc reproduces the 2023 R_GC at the 2023 D to < 1e-3.
- **C6:** the route-2 Kroupa input (α −2.3, branch K) returns Υ_MF = 1.6 (1e-6).

## MUTATE (`CFG465_MUTATE=1`, separate `_MUTATE` outputs)
Pal 4's dispersion (and its errors) is inflated × 2 in BASE. The per-object result is each cluster's signed z, Φ⁻¹ of the Υ-marginalised χ² CDF, per route; its class is |z| < 2 / high / low.

Pass requires all three:
- Pal 4's z moves by ≥ 1 in every route (E1–E6, and CFG333's Newton and isolated-law modes);
- Pal 4's class flips in at least one route;
- the other three clusters' z are unchanged (< 1e-9).

## Needs owner go (not fetched)
- Individual-star, multi-epoch RVs for Pal 3 (source unknown), Pal 4 (Frank+12) and Pal 14 (Jordi+09).
- The NGC 2419 star lists (Ibata+11, Baumgardt+09).
- The Harris 2010 catalogue.
- The catalogue's Pal 3 RV source paper.
