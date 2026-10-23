# CFG963 AMENDMENT A1 (2026-10-23): extra controls, a CFG646 bracket, a reusable feedback-matched scorer, and SC1x vs the surrogate

- Committed ALONE, before any number in this amendment was computed. The frozen criteria (FROZEN_CRITERIA.md, d3b18181c) stand
  unchanged: primary transfer M3-1024 (T1x / T12, already the PRIMARY there), brackets, classes and reading. Everything below is
  REPORTED ONLY and cannot change the frozen class.
- **Seen before this file (disclosed):** the full frozen-criteria result (commit f2354ed22): K exact, M0 / M1 pass, C1 closure −10.21
  / −9.51 (PASS), S0+M3 vs NCS0 −11.87 / −11.37 / −10.08 (M3-1024 / M3-256 / M3-alone-256), NC1x vs S0+M3 +1.78 / +1.28 / −0.02, NC2x vs
  S0+M3 +2.47 / +1.97 / +0.67, class **M3-CARRIED on both footings and all three transfers**; S0+M12 vs NCS0 +2.66. Also seen: the stored
  CFG960 SC1x vs NCS0 score (KiDS +47.28, EXCLUDED; DES +15.64), the stored CFG650 T12 / T1x / T2x scores (+2.03 / −7.70 / −7.18), and
  the new-angles scout's NA-1 text. SC2x was not run.
- **Why:** the orchestrator relayed (i) the scout's NA-1 request to verify T12's +2.03 as a K item and to keep CFG646 as a bracket,
  and (ii) CFG960 addendum A2 (8aaf67bf8, frozen before SC1x output existed), which promises a reported-only score of SC1x against
  this lane's feedback-matched surrogate with all brackets.

## Added items (script `cfg963_reuse.py`; MUTATE pass first; outputs `cfg963_reuse[_MUTATE].{out,json}`)

1. **K2 (inherited-pipeline reproduction).** The frozen CFG654 module's inherited library (`load_lib("inherited")`, CFG592's library
   unchanged) and its CFG596-statistic `score` function re-score the stored inherited runs T12, T1x, T2x against CFG596 P0. They must
   reproduce the stored CFG650 results (`cfg650_native_results_T12.json`, `cfg650_native_results.json`): N_kept, Δχ² and the
   robustness values widen2 / noIA / held / DESI, to |Δ| ≤ 1e-6 (the record's REPRODUCED tolerance in CFG654's post-hoc check). The
   inherited-pipeline step T12 → T1x (Δχ² change from adding M3 on the same ICs) is then reported beside the native attribution.
2. **K3 (control-slot unit test, the scout's MUTATE).** NC1x and NC2x against a control-slot surrogate with T ≡ 1 must reproduce the
   stored −10.08 / −9.39 and every robustness value exactly (|Δ| ≤ 1e-9).
3. **K4 (reusable scorer).** A function `score_vs_feedback_control(run, transfer)` takes any native_cmb 1024³ run dictionary and
   returns its frozen-scorer score against NCS0 × T(k, z) (the control-slot surrogate of FROZEN_CRITERIA.md §2). It must reproduce,
   with T ≡ 1, the stored CFG960 SC1x vs NCS0 result (`cfg960_score_results_SC1x.json`: N_kept, χ², Δχ², robustness, DESI, class;
   both surveys) to |Δ| ≤ 1e-9, and the K3 numbers.
4. **Bracket R3 = CFG646 static post-process** (DIFF-S, the declared primary placement; CFG596 P1 canonical fields at 256³, z = 0 /
   0.5 / 1; no back-reaction): T^grav = the stored DIFF-S ratio; T^part = 1 (the post-process does not move particles). Mapped to the
   1024³ bins by the frozen rule (log-log interpolation, held at its value at k_hi,256 = 2.011 h/Mpc above that). Scored as
   S0+M3[R3] vs NCS0 and NC1x / NC2x vs S0+M3[R3]; its class is computed by §6's rule and reported only.
5. **SC1x vs the feedback-matched control (CFG960 A2, reported only).** `score_vs_feedback_control(SC1x, T)` for every bracket:
   M3-1024 (primary), M3-256, M3-alone-256, CFG646-R3. Reported side by side with SC1x vs NCS0 (first). Plain reading, by the
   frozen classes applied to SC1x vs S0+M3: **EXCLUDED** (Δχ² ≥ 9 and every robustness value ≥ 9) = SCT-M's capped cold sector
   over-produces structure relative to plain dust plus the same gas expulsion; **CONSISTENT** = it does not; otherwise as the class
   says. No alt statement (SC2x was not run).

## Unchanged

Data, cuts, scorer, robustness set, T-OWN / NZ1, the §6 attribution rule and the §7 reading. Same process rules: one process,
< 1 GB RSS guard, one thread, nice 10, pause if free + inactive memory < 3 GB; no PM run of any size; no edits to other lanes.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
