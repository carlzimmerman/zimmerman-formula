# CFG894: κ campaign ledger, rules and doors (2026-10-20)

This is the foundation for a many-attempt campaign to derive κ in a₀ = κ c √(G ρ_DE). **κ = ½ is FITTED** (CFG493:
κ_Λ = 0.417 ± 0.095, κ_crit = 0.345 ± 0.078). This lane derives nothing. It catalogues, sets rules and lists doors.

| file | what |
|---|---|
| `KAPPA_ATTEMPTS_LEDGER.md` | every prior κ attempt, grouped by family, with verdicts, record conflicts and pending lanes. Tables are rendered from the CSV |
| `kappa_attempts_register.csv` | the source register (594 rows, K001–K594), append-only |
| `KAPPA_CAMPAIGN_RULES.md` | the rules every new attempt follows: register first, forbidden inputs, entry screen (S1 = c required, from CFG893), mutation and identity checks, outcome classes, look-elsewhere rule |
| `KAPPA_DOORS.md` | the four walls, 5 prerequisites, 5 genuinely untried doors (ranked), 17 excluded candidates |
| `kappa_campaign_lee.py` | stdlib-only script (under 1 s): validates the register, counts, computes the look-elsewhere numbers, renders the ledger |
| `kappa_campaign_lee.out` / `.json` | normal run, 4/4 checks pass |
| `kappa_campaign_lee_MUTATE.out` / `.json` | the window centre moves 0.417 → 0.300; the in-window count moves 17 → 15 (the control bites) |
| `ledger_intro.md` | prose that heads the rendered ledger |

**Run** from the repo root:

    OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG894_kappa_campaign_ledger/kappa_campaign_lee.py > campaign_fresh_gravity/CFG894_kappa_campaign_ledger/kappa_campaign_lee.out

Then repeat it with `MUTATE=1` and `_MUTATE.out` as the output.

## Counts (from `kappa_campaign_lee.out`)

Totals:
- 594 rows: 585 counted, 9 κ-blind listed for completeness.
- **439 derivation or selection attempts**, and none derives κ = ½.
- 114 produced a number: 51 determinate values and 63 menus.
- 33 rows are measurements and 7 are registered but unrun.

| family | rows | determinate | menu | no number |
|---|---|---|---|---|
| HT horizon/thermal | 55 | 13 | 13 | 29 |
| HE holographic/entropic | 41 | 8 | 14 | 19 |
| VM vacuum matching | 57 | 4 | 10 | 43 |
| FN normalisation of W / action | 99 | 4 | 5 | 85 (+5 pending) |
| PS π-counting / geometry | 56 | 9 | 11 | 35 |
| GB graviton bath | 15 | 2 | 3 | 10 |
| TA topological/anomaly | 24 | 1 | 0 | 23 |
| QG quantum gravity | 18 | 6 | 1 | 11 |
| KS kinetic / cold-energy dynamics | 30 | 0 | 1 | 29 |
| CC cosmological consistency | 29 | 1 | 3 | 21 |
| NU numerology (flagged) | 29 | 1 | 2 | 8 (rest controls) |
| OB measurements (not derivations) | 43 | – | – | 33 measurements |
| AU audits / LN Lean / EX pasted | 64 / 16 / 9 | 0 / 0 / 2 | – | – |

## What the numbers say

**17 of the 51 determinate values land in today's 2σ window, [0.227, 0.607]. Chance predicts about 14.**
- The landings are mostly repeats: 0.461 (Z = 2π) five times, 0.482 (Verlinde 6) six times, plus 0.55–0.557.
- Landing in the window carries no evidential weight until σ(a₀) ≤ 2.8%, which is what separating ½ from 0.461 needs.

**64 of the 439 attempts output exactly ½, and every one was voided or left conditional.**
- The routes were insertion, posit, tuning, naming (the SIS ratio), polarisation counts, circularity, or gauge and algebra
  errors.
- So far, P(flawed | output = ½) = 1.

**P_LEE for an exact ½ over the prior determinate trials is 0.20 with simplicity weighting (0.03 flat).**
- No new exact ½ can reach 3σ at the campaign level on its own.
- The rules therefore require a second, independently testable prediction from the same mechanism.

## Active parallel efforts (not duplicated here)

- **The "32pi squared puzzle" chat:** the empirical provenance of the measured κ values, and the logic/Lean argument
  (KAPPA_LOGIC_2026_10_20.lean, written, not compiled).
- **CFG893:** κ from the new cold-energy structures. Finished: NOT SELECTED (131bedf33). Its scaling no-go is rule S1 here:
  doors without c are excluded.
- **CFG895:** the α ledger (a separate constant).

## Top six doors to launch first (details in `KAPPA_DOORS.md`)

1. **P1:** run the frozen p63-C1/C1b/C2/C3 (a₀ as a field: cosmic bound charge, patch bootstrap, flux lattice, Kaloper–Sorbo
   ħ audit) after the 1024³ chain. It must run before any four-form or a₀-as-field door.
2. **D1:** the stiffness term's own FRW vacuum (covariant CFG770 action). This is a closure door; the expected κ ~ R_H/L* ~ 10⁶–10⁸
   is EXCLUDED, or the term vanishes (identity).
3. **D3:** a census of every place c meets a₀ in the record (π-weight, ħ-weight and class of each term). It tests whether any
   record equation can give exact ½.
4. **P4:** settle RT-17 against RT-19 (KMS 0.4607 versus a₀ = 2cH_Λ after a 4π error) before anyone cites "the dS tie gives
   0.461".
5. **D2:** causality saturation of the gated drift (CFG893 R12), with α taken from the Israel–Stewart / collisionless closure
   and the saturation loci declared in advance.
6. **D4:** the nodal fermion medium made Lorentz-invariant (v = c), with its own vacuum energy taken as the dark energy. The
   expected outcome is a TRADE (ARGON10's parameter count).

Each is light. No door is expected to give ½. Each is built to close cleanly.

## Lane rules followed

- **Read-only outside this directory.** LEDGER.md, the canonical files and other lanes were not edited.
- **Searches.** Five read-only catalogue sweeps used text greps restricted to markdown and tracked files. After the
  orchestrator's 00:32 note, no further searches were run. The only computation was the one stdlib script (under 1 s, under
  20 MB) plus a `git cat-file` existence check on all 340 cited commits (all exist).
- No downloads. No personal names or home paths.
