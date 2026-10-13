# CFG667: the KiDS age signal is likely a stellar-mass artefact

**Combined label: STELLAR-MASS ARTEFACT LIKELY** (Part A NOT DECIDED, and underpowered; Part B M* BIAS EXPLAINS). CFG700's raw
old-vs-young lensing excess (×1.46 at fixed LePhare M*) disappears when the same galaxies are matched on an independent stellar-mass
estimator.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (fd97db64b), 2026-10-12. Block CFG660–669.
- **Settings:** raw lensing only (no law, κ, footing, environment model, ΛCDM or MOND ingredient). Not "theory closed"; nothing here
  says the data favour the framework.
- **Script:** `cfg667.py` (CFG585's head and CFG531's `esd_loo` executed unedited; CFG589's stratified tertiles), one process,
  minutes → `cfg667.out`, `cfg667_results.json`. MUTATE: `CFG667_M=M1` exits 1 (bites); `CFG667_M=M2` exits 0 (**does not bite**,
  see below).

## Results

| item | result |
|---|---|
| C1: CFG700 reproduction | K9 A = +0.165779 ± 0.081 (CFG700: +0.166) |
| **Part A**: per-bin log10(OLD/YOUNG), k = 6…14 | −0.03, +0.42, −0.08, +0.37, −0.02, +0.37, +0.15, +0.21, +0.39 (σ 0.14–0.40 each) |
| Part A slope (inner minus outer across K9) | S = +0.139 ± 0.213, Z = +0.65, χ² 8.4 / 7 → **NOT DECIDED** |
| **Part B1**: median(log M*_Taylor − log M*_LePhare) | OLD +0.027, YOUNG −0.097 → **OLD − YOUNG = +0.123 dex** |
| **Part B2**: tertiles re-matched at fixed Taylor mass | medians log M*_T 10.752 / 10.752 (LePhare 10.776 / 10.848); **A_T = +0.032 ± 0.080, Z = +0.40 → M\* BIAS EXPLAINS** |
| MUTATE M1 (OLD × 0.8) | A shifts by log10 0.8, S unchanged: bites |
| MUTATE M2 (injected ×1.5 inner excess in bins 12–14) | S = +0.368 ± 0.213, Z = +1.73 < 2: **does not bite** |

## Reading

1. **The age signal is estimator-dependent.** At fixed LePhare mass the old (redder) early types are 0.12 dex heavier according to the
   Taylor et al. 2011 colour–M/L relation; matched on Taylor mass, the lensing difference falls from +0.166 to +0.032 (consistent with
   zero). The raw-data "age signal" is therefore not evidence for extra cold mass in old systems; the simplest reading is a colour-
   dependent stellar-mass calibration difference.
2. **Part A cannot discriminate.** M2 shows the radial-shape test misses even an injected 1.5× inner excess at the 2σ line, so its
   NOT DECIDED is a power limit, not a null. The radial anatomy of the signal needs a larger sample or coarser bands.
3. **Limits.** Both estimators are colour-based; a bias common to both is untested. Which estimator is closer to the truth is not
   decided here: the result is that the signal does not survive a change of estimator, not that Taylor masses are right.
   A_T's error (±0.08) also allows a residual of up to about 0.19 at 2σ, so a smaller physical effect is not excluded.
4. **Consequences for the record:** CFG700's AGE SIGNAL, CFG585–589's age readings and the ACE motivation (MODEL_accumulating_cold_energy)
   all rest on LePhare-matched samples; their physical reading should carry this caveat. This also removes the main data motivation for
   history-dependent settling (and the CFG666 clock, already closed on shape).
