# CFG924 AMENDMENT AM1 (POST HOC; after the frozen M-INJ failed, BEFORE the main run)

Dated 2026-10-20. Named AM1 to keep it apart from CFG922's census amendment "A1", which this lane applies.
No A1c or A1u mass, model or score of any eFEDS group had been computed when this was written. The main run had not started.

## What happened (recorded as a frozen failure; it stands)
- **K1–K4b all PASS exactly** (max rel 0.0; `cfg924_K.out`).
- **M-INJ, census leg: PASS.** A planted fluxscale of −0.5 mag gives M_cond = 10^0.2 × F to 3.9e-15 (N 131) and M_bcg to 1.9e-15
  (N 82); zeros stay zero.
- **M-INJ, end-to-end leg: FAIL as frozen** (tolerance |Δχ²| < 1e-6). Labels agree (BOTH EXCLUDED), but:
  - χ²_a 23.052 vs stored p02 23.650 (canonical) and 23.529 vs 23.392 (alt);
  - χ²_b 27.416901 vs 27.416938 and 23.761745 vs 23.761410.

  Outputs: `cfg924_MUTATE.out`, `cfg924_results_MUTATE.json`.

## Mechanism (diagnosed, no new data)
The planted masses differ from CFG652's stored p02 inputs (stored M_cond × 10**0.2) only by float rounding (~1e-15 relative).
CFG652's model (a) responds to that with per-group ΔΣ changes of up to 62%, mostly in the inner bins:
- (a) differs by more than 1e-6 in nearly every group (116 of 131 on alt);
- (b) differs in only 1–2 groups, by ≤ 5%.

Model (a) is CFG637's Method A, a time-stepped 1D shell-infall integration (`cfg637_lib.Infall`) with shell crossings. Its
reservoir is placed from each shell's state at t_obs, and that state is chaotic in its inputs. Identical inputs reproduce bit for
bit (K3), so this is a property of the re-run model, not a fault of the CFG924 pipeline. The consequence: CFG652's stacked χ²_a
carries model noise of order a few tenths. Its primary χ²_a (22.9 / 22.3) is 2.8 / 2.2 above the p = 0.01 line (χ² = 20.09,
8 dof).

## Additions (post hoc; the frozen rules, controls and verdict logic are unchanged)
1. **M-INJb (wiring control).** Plant using the exact float operation CFG652 used: M_cond = stored M_cond × 10**0.2 (M_bcg
   likewise). Then run write_inputs → x1 models → the verbatim score. It must reproduce CFG652's stored p02 cell on both
   footings (χ²_a, χ²_b abs < 1e-6; same label). Outputs: `cfg924_MUTATE_B.out`, `cfg924_results_MUTATE_B.json`.
2. **Model-noise ensemble (JITTER)** for the decision cell x1, both footings:
   - four realizations of model (a) with M_cond × (1 + k·1e-12), k = 1..4;
   - done for F (CFG652's own masses, 131 groups) and for A1c (the main run's inputs);
   - model (b) is kept at its unjittered arrays (its sensitivity is 1–2 groups at ≤ 5%; disclosed);
   - each realization is scored verbatim.

   Reported: χ²_a mean, sd and range, and the label in each realization.

   **Role in the verdict.** The CFG924 verdict is still the frozen rule applied to the unjittered main run. Two
   qualifications are added:
   - **NOISE-SENSITIVE:** any F or A1c realization changes its x1 label relative to the unjittered run on either footing.
   - **WITHIN MODEL NOISE:** a frozen cell move whose |Δχ²_a| is under 2 × the larger jitter sd.

   Outputs: `cfg924_JITTER.out`, `cfg924_results_JITTER.json`.
3. **Run order:** M-INJb, then MAIN (as frozen), then JITTER. One process at a time, one core, nice 10, < 1 GB. About 6 h
   beside the live 1024³ job.
