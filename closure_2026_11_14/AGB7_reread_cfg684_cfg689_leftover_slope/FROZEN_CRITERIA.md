# AGB7 — CFG684 and CFG689 re-read with the age slope that is left in the DES distances (FROZEN, before any number)

2026-11-14. Owner: "Yes, re-read them". A re-read of two of this repository's own lanes. It adopts nothing and
edits no ledger. No script of this lane is in the repository when this file is committed.

## Why
AGB1's Part B re-read CFG684 and CFG689 with the published age correction at full size (A = 1) and found them
AGE-DEPENDENT / SHIFTED. AGB3 to AGB6 then found that the published slope double counts what the surveys' own
host corrections have removed, and that the slope still left in the published DES moduli is 0.23 ± 0.06 of it
(AGB3, fit U on the published moduli), or 0.35 ± 0.09 if noise in the host ages is allowed for (AGB6). This lane
asks what **that** amount does to the two lanes.

## What is run
`agb7_reread.py` is AGB1's harness (`agb1_reread.py`, itself LGS1's) with two generalisations and nothing else:
the amplitude may be any number, and the redshift template may be AGB1's cosmic-average T_S or the sample's own
drift T_H of AGB3 (`agb3_S.json`, curves `full_sfr` and `des_only_sfr`). The committed sources of CFG684 and CFG689
are executed unchanged apart from the harness's exact text substitutions: the moduli become μ − A × T(zHD).
- **Primary: A = 0.23 with T_S.** Bracket: **A = 0.35 with T_S.**
- CFG684, combinations BAO+DES5 and BAO+DES5+CC; CFG689, modes D5 and TD5F at the frozen 60,000 steps and seeds;
  samples `full` and `des_only`, as in AGB1.
- CFG689 is run with its own `CFG689_PARALLEL=1` mode (owner 2026-10-20: small runs may go beside another job
  under the script's memory watchdog), because another session's chain is alive and the default guard would exit.
  The mode changes the guard only. A run that exits on a guard (exit 75) is NOT RUN and is reported so.

## Rules (AGB1 Part B's, unchanged; each run against the A = 0 run of the same sample in LGS1's committed outputs)
- **CFG684:** A1 DEGENERACY BROKEN if Δχ²_max ≥ 4, else NOT BROKEN; A2 ROBUST if the flat-a0 Ω_m agrees with A = 0
  within the two sd added in quadrature, else AGE-DEPENDENT; A3 FLOOR HOLDS if the lower edge of the tracking band
  √X(2.33) is above 0, else FLOOR LOST.
- **CFG689:** B1 per z* (1.0, 1.2, 1.5, 2.33): STABLE if the run's median of tracking √X lies inside the A = 0 68 %
  band and the A = 0 median inside the run's 68 % band, else SHIFTED; B2 CLASS UNCHANGED if the script's P1 and P0
  classes are the same, else CLASS CHANGED. The script's chain check (its K4) must be ok and the step count 60,000,
  or the mode is NOT EVALUABLE. P2, e_3σ and the native H0 are reported, no label.
- **Second word of every label:** ROBUST if the bracket (A = 0.35) gives the same label, else FRAGILE.

## Harness checks (judged before any label is read)
- **H1.** `cfg684 full` at A = 0 reproduces `cfg684_results.json` (Δχ²_max, flat-a0 Ω_m mean and sd, tracking and
  rival bands at z* 1.0, 1.5, 2.33) to 10⁻⁶ in both combinations.
- **H2.** `cfg684 full` at A = 1 with T_S equals AGB1's committed `agb1_cfg684_full_A1.json` in the same quantities
  to 10⁻⁹ (the generalised harness is the same code path).
- **H3.** `cfg689 TD5F des_only` at A = 1 with T_S reproduces AGB1's committed tracking √X quantiles at the four z*
  to 0.005.
CFG684's labels are NOT EVALUABLE if H1 or H2 fails; CFG689's if H3 fails.

## Reported only (no label)
- CFG684 with the sample's own drift, A = 0.35 with T_H, both samples.
- For each run the shift of the flat-a0 Ω_m and of the tracking medians in units of the A = 1 shift AGB1 found.

## What the result may and may not say
- ROBUST / STABLE means the lane's committed numbers do not lean on the age question at the size that is left in the
  distances; AGE-DEPENDENT / SHIFTED means they still do. It does not say the amount is right: 0.23 rests on
  photometric host ages and a simple age model (AGB3), and the bracket 0.35 on a noise estimate made after the fact.
- The template is a redshift drift; a fit cannot tell age from anything else with that shape.
- AGB1's Part B stands as the reading at A = 1. Nothing here adopts either amplitude.

## Files and order
`agb7_reread.py` (harness), `agb7_collect.py` (checks and labels; `agb7_results.json`, `agb7_collect.out`).
This file is committed alone, before any script; the scripts next, before any run.

kappa = 1/2 FITTED; not theory closed.
