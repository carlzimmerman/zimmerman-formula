# CFG453: T15/T16's group and cluster "overdraft" is a units mismatch

Criteria: `FROZEN_CRITERIA.md` (b1132dd48, committed alone before the script). Script: `cfg453_deficit_units.py`.
Outputs: `cfg453_deficit_units.out`, `cfg453_results.json` (MUTATE: `*_MUTATE.*`).

**Verdict: mismatch CONFIRMED. The overdraft was a units artefact.** On T15's own definition of the deficit, groups and
clusters have POSITIVE cold mass on both footings, and the floor-vs-cluster λ bind disappears.

## The mismatch
- **T15 defines** x = M_missing/M_b = (M_tot − M_b)/M_b, with f_obs = 1/(1 + x). Its Milky Way point uses exactly that.
- **For groups and clusters it inserted CFG382's definition A**, x_A = (M_tot − M_b − M_ph)/(5.364 M_b). That is the
  excess beyond the law, per cosmic cold share. The exact identity is x_T15 = 5.364 x_A + (ν − 1), which holds to 4e-15 per
  object.
- **T15's own output shows it.** Its C1 gives clusters f_obs = 0.709, a 71% baryon fraction. The measured value is 0.163
  (b = 0) and 0.114 (b = 0.3); groups are 0.084 / 0.059.

## On T15's own definition (b = 0 / 0.3; median over objects)

| | canonical 9.3603e-11 | alt 1.1312e-10 |
|---|---|---|
| x_T15 clusters (a0-free) | 5.12 / 7.74 | 5.12 / 7.74 |
| x_T15 groups | 10.8 / 15.9 | 10.8 / 15.9 |
| clusters M_cold/M_b, T15 conventions | **+3.90 / +6.53** | **+3.77 / +6.39** |
| clusters M_cold/M_b, per-object S | **+4.31 / +6.94** | **+4.22 / +6.84** |
| groups M_cold/M_b, T15 conventions | +9.34 / +14.4 | +9.18 / +14.3 |
| cluster λ ceiling | none (the deficit exceeds the whole kernel supply) | none |

- **The λ bind is gone.** Even fully settled kernel supply (S/M_b 2.9–4.8) is less than the dark mass, so no λ overdraws
  the budget, and the MW floor λ = 0.028 is allowed at R500. T16's three-way "window" is no longer defined: clusters and
  groups give no upper bound. The frozen V4/V5 labels print "BREAKS / EMPTY" only because gap = 0 and the intervals are
  infinite. Read them as "no constraint".
- **Like-for-like ledger at R500 (b = 0):**
  - **Clusters:** law phantom 2.9–3.3 M_b plus beyond-law excess 1.9–2.2 M_b gives a dark mass of 5.12 M_b. That is 0.95
    of one cosmic cold share (5.364): **clusters are a closed box.**
  - **Groups:** dark mass 10.8 M_b = **2.0 cosmic shares**, because they are gas-poor (f_b 0.084). This is the
    baryon-depletion ordering, as the original-baryon reservoir reading (CFG365) expects.
  - The per-object kernel supply equals the law's phantom (S/M_b 2.94 vs median ν − 1 2.94, canonical).

## What this changes on the record
- **T15 S2 ("cold fluid forced NEGATIVE at every clock except the MW") and S3 ("cold fluid nearly absent at cluster scales")
  are withdrawn-level.** So are T16 C1–C4 ("the floor and the cluster budget cannot share one λ"). All of them rest on x_A
  read as x_T15. The deepseek_push files are not edited here.
- **CFG451 and CFG452 inherited the same inputs.** Their "no rescue" verdicts answered a problem that does not exist on
  T15's definition. Their footing and a0(z) shifts (−0.003 etc.) are still correct as sensitivities.
- **NOT changed:** CFG382's own frozen cluster miss (P2: predicted leftover e 0.714 vs measured x_A 0.41 at b = 0). That
  comparison is like-for-like on the leftover branch and stands. Per the CFG382 audit it would match at b ≈ 0.2 (0.700),
  where groups miss (1.35). **The real open problem is groups needing about 2× clusters' excess per present baryon**, which
  a local-density rate cannot produce and baryon depletion can.
- CFG431 reads x_A as the leftover e, which is the correct branch, so it is unaffected.

## Controls
- C1: def-A inputs with T15 conventions reproduce CFG451's rows to 1e-9.
- C2: the x_A medians match CFG450.
- D1: the identity holds to 4e-15.
- MUTATE re-plants x := x_A. Clusters at b = 0 return negative on both footings (−0.80/−1.00 with T15 conventions,
  −0.34/−0.48 per-object), and the headline flips to "mismatch real, overdraft survives it".

## Caveats
- The group stellar mass is the audit's placeholder (0.10 M_gas). Seven clusters.
- T15's M_cold here means the dark mass beyond the settled kernel supply. Its split into "beyond-law excess" and
  "phantom not yet settled" depends on how the framework assigns the phantom, which this lane does not decide.
