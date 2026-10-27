# Q1_m6_selection_share: the measured share of galaxies that need M6, and M6N1's verdict at that share

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (a46adc2f90), committed alone before any script or number.
- **Script:** `q1_share.py` (a2b07453d4), committed before its first run.
- **Amendment A1** (label only, committed before the rerun): the MIXED label of *reported* variants now names the corners
  that are over budget at full retention. No number or graded verdict changed.
- **Before any number:** the first attempt stopped at Step 0 because the closure population file (uncommitted in the
  record) was missing from this worktree. It was copied in untracked, and the pinned sha256 matched.
- **Data:** untracked under `_external_data/q1_gama/`, with sha256s in the criteria.
  - GAMA DR4 G3C v10 group catalogue, reused from CFG471.
  - GAMA DR4 StellarMassesLambdarv20, downloaded with the owner's approval.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component,
not a particle. No ΛCDM input: G3C's mock-calibrated MassA is never read, and there is no abundance matching. Not
"theory closed". Nothing here says the data favour the framework.

## The predicate (from the record, frozen)

**A galaxy needs M6 ⇔ it is not a satellite AND its system's ΣM★ lies below X43's crossover.** This is X62's environment
rule.

- **Crossover.** The crossover M200 is mapped to baryons through EM1's own route-E R1 relation, the mapping X58/X62 use
  for SPARC, groups and lensing: log M_b,x = 10 + (log M200,x − 11.18)/0.90.
- **Primary: c_f = 4** (10^12.09 / 10^12.43 → M_b,x 10^11.02 / 10^11.39). It is the only crossover in the record at which
  the lensing galaxies keep the law.
- **Native-c_f crossovers are variants.** They are unconverged and put the lens galaxies on halos.

## Measured q (1/Vmax-weighted stellar-mass share; 19 215 GAMA galaxies, 0.01 ≤ z ≤ 0.10, M★ ≥ 1e8 M☉)

| | canonical | alt |
|---|---|---|
| **q_star** | **0.517** ± 0.020 (jackknife, 15 strips) ± 0.052 (selection systematics) | **0.666** ± 0.020 ± 0.046 |
| largest systematics (half-differences) | z-split 0.030 (0.473 / 0.532), fluxscale 0.029, gas in M_b 0.028, unseen members 0.015 | z-split 0.033, fluxscale 0.021, gas 0.018 |
| q_full with the < 1e8 tail bracketed (1.5 %) | 0.509–0.524 | 0.656–0.671 |
| **2σ interval used for the verdict** | **[0.397, 0.636]** | **[0.556, 0.771]** |
| q_cold (stars + cold gas, gas share bracketed [q_star, 1]) | 0.397–0.714 | 0.556–0.820 |
| q at which the budget is just met at record retention, stellar / cold | 0.299 / 0.235 | 0.174 / 0.137 |

**What makes up q (canonical).**
- Ungrouped galaxies hold 0.346 of the inventory. Alpaslan+2015's ungrouped marginal is 0.30.
- Satellites hold 0.263. They never need M6.
- Group centrals below the crossover add the remaining ≈ 0.17.

**By mass decade (canonical).**
- 1e10–1e11 holds 63 % of the inventory, and 64 % of it needs M6.
- Above 1e11 holds 20 %, and almost none of it needs M6 (0.6 %); on alt, 53 % does.

## Verdict (frozen rule, both footings): **BUDGET BINDS AT RECORD RETENTION**

| quantity | canonical | alt |
|---|---|---|
| F_need at full retention, as a multiple of the budget | 0.25–0.58 × | 0.52–0.98 × |
| F_need at the record's retention (ε_ref 0.191 / 0.163), as a multiple of the budget | **1.33–3.04 ×** | **3.20–6.00 ×** |
| retention M6 needs, ε_crit | ≥ 0.25–0.58 | ≥ 0.52–0.98 |

- **Compared with M6N1.** M6N1 bracketed q in [0.30, 0.69]. Its knife-edge corner (canonical, q 0.30, stellar,
  1.00 × budget) is now excluded: the measured q sits 3.8 σ_tot above the canonical stellar threshold of 0.299, and the
  2σ lower edge is 0.397.
- **Alt is nearly over budget even at full retention.** Its top corner (q_hi, cold gas) reaches 0.98 × the budget at
  ε = 1.
- **The budget is still provisional.** F_allowed is X57's provisional variance line, not a measured forest limit (P1D1–P1D3
  are NOT DIAGNOSTIC). So this verdict hardens the q side of M6N1 only.

## What can change it: the crossover

| variant (reported, labelled) | q canonical | q alt | verdict canonical / alt |
|---|---|---|---|
| NAT-X48 (X58's native c_f) | 0.058 | 0.102 | MIXED / MIXED: the stellar corners fit the budget |
| NAT-A2 (X62's native c_f) | 0.006 | 0.015 | MIXED / MIXED |
| mapping band −0.5 dex M200 | 0.237 | 0.428 | MIXED / BINDS |
| mapping band +0.5 dex M200 | 0.701 | 0.730 | BINDS / MIXED (cold top corner over budget even at ε = 1) |
| SAT-LOW (satellites of low systems need M6 too) | 0.580 | 0.807 | BINDS / MIXED (same) |
| mass floor 1e8.5 | 0.515 | 0.666 | BINDS / BINDS |

- **The verdict is a statement about the c_f = 4 crossover.** It survives the systematics, the satellite rule and the
  mass floor.
- **It does not survive a crossover about ≥ 0.5 dex lower in M200** (canonical), and it certainly does not survive the
  native c_f values. At native c_f almost nothing needs M6, but those crossovers put SPARC-size and lensing galaxies on
  halos, which X58/X62's lensing line rejects by +430 to +490.
- **So the record has no crossover that both keeps the law where the data need it and keeps M6 inside the budget at
  record retention.** M6 survives only if the needing galaxies retain ≥ 25–58 % (canonical) or ≥ 52–98 % (alt) of their
  patch baryons.

## Caveats

- **ρ★ check.** The Vmax-weighted ρ★ is 0.60 × the closure value. GAMA at z < 0.1 is under-dense, and Lambdar masses are
  aperture masses. This is reported, not graded; q is a ratio, and the fluxscale variant is in σ_sys.
- **Cold gas is bracketed, not measured.** GAMA has no per-galaxy HI.
- **The R1 mapping is FITTED.** Its own Υ leg failed in EM1. The ±0.5 dex band shows how much rides on it.
- **X62's ENV rule itself FAILS** as a full theory, on c_f, lensing and clusters. This lane measures the share it implies.
  It does not validate the rule.

## Checks

- **Main: 7/7 PASS, exit 0.**
  - S0: four sha256s; M6N1, X58 and EM1 inputs reproduced.
  - K1: 98.05 % Lambdar match.
  - K2: GSMF shape 0.968 vs 0.969.
  - K3: partition exact, both footings.
  - K4: predicate unit tests.
  - K5: 0.33 GB.
- **Rerun.** Identical apart from the RSS line.
- **MUTATE (`Q1_MUTATE=1`, separate `*_MUTATE.*` outputs): exit 1.** It fails S0 (m2, altered sha) and K4 (m1, satellite
  key inverted), as required. Its verdict flips to MIXED on both footings, so the satellite key is load-bearing.

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I q1_share.py`. Graded lines: `q1_share.out` /
`q1_share_results.json`.
