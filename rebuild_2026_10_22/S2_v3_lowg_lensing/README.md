# S2_v3_lowg_lensing: N0 batch R2, isolated-galaxy lensing at low g for v3 (tiles 17 and 30)

## Verdicts (per frozen rule; both before R6, since the μ_K²ψ term is not included)

| tile | old | v3 canonical | v3 alt | board (less favourable footing) |
|---|---|---|---|---|
| 17 Isolated-galaxy lensing, inner (blue lenses) | PASS | **PASS** (FRAGILE) | **CONDITIONAL** (FRAGILE): consistent only at the maxclu field | **CONDITIONAL** (footing split) |
| 30 Red (early-type) lenses | COND | **CONDITIONAL** (FRAGILE): only with CFG667 + IMF α–σ | **CONDITIONAL** (FRAGILE): with CFG667 alone, or with + IMF | **CONDITIONAL** (the old COND survives) |

κ = ½ FITTED. Footings are never pooled. No dark-matter particle. Not theory closed. Nothing here says the data favour the
framework.

## The numbers

A = data / v3, from CFG829's estimator in its window (g_bar 10^−13.3–10^−11.9 m/s², 6 B21 points). The v3 model is
forward-modelled as 4GΔΣ over the record's 181,477 lenses.

| class | y_e = 0 | primary (noclu) | maxclu |
|---|---|---|---|
| blue, canonical | 0.878 ± 0.074 consistent | 0.882 ± 0.074 consistent | 1.035 ± 0.094 consistent |
| blue, alt | 0.802 ± 0.067 between (−2.9σ) | 0.806 ± 0.068 between | 0.948 ± 0.086 consistent |
| red R0 (inventory), canonical / alt | 1.313 ± 0.063 / 1.200 ± 0.058 short | 1.315 / 1.201 short | 1.558 / 1.427 short |
| red R1 (+0.123 dex, CFG667) | 1.191 short / 1.089 consistent | 1.189 short / 1.086 consistent | 1.373 / 1.257 short |
| red R2 (+0.123 + IMF 0.172, CFG926 R5) | 1.023 ± 0.049 / 0.935 ± 0.045 consistent | 1.020 / 0.933 consistent | 1.131 between / 1.037 consistent |
| all R0 (feeds tile 31) | 1.207 ± 0.042 short / 1.103 between | 1.210 short / 1.105 between | 1.431 / 1.311 short |

Red − blue split z at the primary field: +4.45 (R0) → +1.55 (R2) on both footings.

## Ladder (canonical; alt in the `.out`). Blue / red / all

| step | blue | red | all |
|---|---|---|---|
| L0 CFG829 (ν_e, algebraic, B21 distances; reproduced exactly) | 1.016 | 1.587 | 1.439 |
| L1 kernel ν₁ (v3's μ = x/(1+x)) | 1.016 | 1.587 | 1.438 |
| L2 native h 0.679, Ω_m 0.3085 | 0.999 | 1.559 | 1.413 |
| L3 forward 4GΔΣ of the isolated AQUAL profile | 0.988 | 1.543 | 1.399 |
| L4 + hot CGM 0.5 M★ (= v3 at y_e = 0) | 0.878 | 1.313 | 1.207 |
| L5 + EFE, primary y_e (T_central) | 0.882 | 1.315 | 1.210 |
| L6 screening L★ 24 / 90 pc | = L5 (l_g ≤ 0.20 / 2.8 pc; l_g/R ≤ 2e-4) | | |

## What moves the answer, and what does not

1. **The external field barely matters inside this window.** This was the reason N0 flagged both tiles as at risk.
   - At the primary field A moves by ≤ +0.004.
   - ΔΣ is a differential quantity, so an EFE cut-off beyond r_e ≈ 35 r_M acts almost like a mass sheet. A point mass's
     ΔΣ ratio (EFE / isolated) is ≥ 0.97 for R ≤ 30 r_M.
   - A y_e scan up to 3e-4 changes no class.
   - The field does matter at the maxclu value: blue +0.15, red +0.24. It also matters outside the window: blue χ² over
     all 15 points rises 27.5 → 45.8 → 119.5 with y_e, which is F2's outer range.
   - N0's expectation that "the EFE adds to the red excess" holds only at maxclu.
2. **The hot CGM is the main mover**, at −0.11 (blue) and −0.23 (red). F2's f_hot = 0.5 comes from a quiescent stack. It
   suits red lenses and is an extrapolation for blue ones.
   - With f_hot = 0, tile 17 is PASS on both footings.
   - With f_hot = 1, it is CONDITIONAL on canonical and NOT DECIDABLE on alt.
3. **SPS masses decide the fragility.** E1 brackets:
   - M★ +0.2 dex: v3 over-predicts the blue lenses ("over").
   - M★ −0.2 dex: the red tile becomes FAIL on canonical, even with the IMF posit.
4. **The red-lens excess survives v3 on the inventory alone:** 5.0σ canonical, 3.5σ alt. It is removed only by the
   declared CFG667 + IMF α–σ posits, with discs kept at Chabrier.
   - The R5-blue variant puts the IMF on the blue lenses too. Blue then sits "over" at 0.77 / 0.71, so the asymmetric
     premise is still necessary.
   - Reported only: with CFG850's window convention, R2 gives 1.099 / 1.003.
5. **"Inner" check.** The window points' lens-weighted median radii are 70–289 kpc (blue) and 89–366 kpc (red), so the
   outermost red point lies beyond 0.31 Mpc. Reported only: F2's ESD-space A_in for all lenses at R ≤ 0.31 Mpc is
   1.129 ± 0.036 canonical ("short") and 1.035 ± 0.033 alt.

## How

- Criteria and ledger `FROZEN_CRITERIA.md` / `ASSUMPTION_LEDGER.md` were committed alone first (c94150c05d). `AMENDMENT_A1.md`
  is post-result.
- `s2_v3_lowg_lensing.py`:
  - **Model and inputs:** F2's AQUAL solver (`../F2_outer_lensing/f2_aqual.py`, imported read-only); F2's inventory and EFE
    construction; the record's lens catalogue and per-lens source weights; CFG885's T_Ωm; CFG926's committed D_red.
  - **Checks:** 8/9 PASS. K0a reproduces CFG829 to 2e-16. K0b reproduces CFG926's window850 to 7e-16. K1 solver: isolated
    1e-4, far field 4e-4. K2 forward point mass: mass spread 3e-5, against an independent quadrature 4e-5. K3 2.9e-7. K4
    6e-14. K5: the `typ` colour split matches B21's colour bins (1.07 / 1.05) and is reconstructed exactly. K7 passes.
  - **K6 FAILS** (EFE monotonicity, a false premise at 0.06 σ_A; see A1), so the run exits 1.
  - `--mutate` (B21 g_obs × 1.10) breaks K0a and exits 1.
  - Resources: one thread, `nice 15`, peak RSS 0.90 GB, 267 s. Nothing downloaded.

## What this does not show

- **The μ_K²ψ term is not included** (BS24 Eq. 35; batch R6). It acts beyond about 0.1 Mpc, inside this window, so both
  verdicts are provisional on R6.
- **No external field is measured for the KiDS lenses.** The bracket comes from Chae+21 SPARC environments. P2
  (spectroscopic GAMA isolation, per-galaxy y_e from catalogue baryons) has committed criteria only, so nothing was read
  from it.
- **The hot CGM of blue lenses is not measured.** The blue verdict hinges on it.
- **The lens stack is a proxy.** It is the record's 181k reconstruction, not B21's 259k lenses.
- **Boost correction:** none was applied, because none is released.

## Suggested board edits (not made here)

- **Tile 17:** PASS → CONDITIONAL. Suggested note: "v3 (AQUAL + EFE, inventory + hot CGM): blue A 0.88 canonical / 0.81
  alt; EFE ≤ 0.004 in window; hinges on hot CGM and SPS M★; before R6".
- **Tile 30:** COND stays. Suggested note: "v3 with EFE: inventory 1.31 / 1.20 short; CFG667 + IMF α–σ → 1.02 / 0.93; EFE
  adds only at maxclu; before R6".
