# CFG289 — how far the 17 wrong cells in the repo's RC100 CSV reach (orchestrator lane, 2026-10-02)

**Why.** CFG287's integrity audit found that `real_research/data/rc100_nestorshachar2023_table3.csv` still carries the 17 cell errors (16 rows) first found on 09-29. Seven rows hold log M_bulge where log M_baryon belongs; there are also two wrong V_c values, one wrong f_DM and five wrong names. Thirty-three committed scripts name the file. CFG287 bounded CFG52/90 only. This lane bounds every reader. κ = ½ is FITTED. Nothing was fetched.

**Order.** Criteria 80f05e155 were committed before the corrected file or any re-run existed. The corrected copy came next (51c70923f). This README was written after the runs.

## Bottom line
- **One verdict moves against the framework: L323.** Its frozen check "the level is a tie" goes from PASS to FAIL. On the corrected table the framework's best systematic cell's **68% bootstrap interval** (about 1σ, with no calibration systematic in it) is [−0.038, −0.007] (it was [−0.028, +0.009]), so it no longer contains zero offset. Three ΛCDM variants (NFW, H, C) still contain zero. The record's "a tie (L323/L331)" (CFG0 inventory W14) holds only through L331, whose numbers move toward both models: framework +0.9σ → +0.3σ, ΛCDM +3.0σ → +2.6σ.
- **One check breaks by a fit failure: hunt k-hzs-4.** The Υ-lever check turns from PASS to FAIL because, with the corrected masses at Υ × 1.5, the RC100 level fit returns NaN. That sample's lever is undetermined, not measured. In the same script, RC100's own residual slope moves from −0.43σ to −2.00σ, and the two-survey common slope separates less from the rivals (a₀ ∝ cH(z): −2.97σ → −2.33σ; MUSE-DARK III: −3.23σ → −2.47σ). Its flat-law distance is unchanged (−1.65σ → −1.61σ).
- **CFG287's bound for CFG90 was too small.** CFG90 hard-codes the absolute repository path, so the driver could not substitute the file. Run with the path pointed at each mirror (`cfg289_supplement.py`), the z ≥ 1.5 pool loses two RC100 galaxies (K20 ID9, GS4 01529; N 15 → 13):
  - ⟨D_flat⟩ +0.137 → +0.035 (+1.00σ → +0.25σ);
  - ⟨D_rival⟩ −0.034 → −0.131 (−0.25σ → −0.94σ);
  - a 0.10 dex shift, 0.74σ of σ_pool, with no check flip.
  CFG52's own pool, which already excluded GS4 01529, moves 0.03 dex as CFG287 said: D_flat +0.135 → +0.107, D_rival −0.037 → −0.063. Both pools move toward the flat law. Neither is decisive.
- **Everything else is numeric and under 1σ, or unchanged.** CFG216 and CFG217 reproduce their 09-29 corrected outputs exactly, which independently confirms the corrected copy. The a₀(z) chart is unaffected: it already plots the corrected RC100 quartiles (Q2 s* = 2.10).

## Controls
- **Corrected-copy build (`cfg289_build_corrected.py`), 4/4 pass:**
  - C1: the frozen constants reproduce the original's derived columns on the 84 untouched rows to 3.7e-5;
  - C2: untouched rows are byte-identical;
  - C3: exactly the 17 listed cells changed;
  - C4: all 100 rows equal the paper-values file.
  - The only deep-flag flip is row 44 (U4 33383).
- **Reproduction:** the ORIG run reproduces the committed outputs for every reader except CFG90. Its hard-coded path read the live repo, and 9 r_h rows of its .out differ from the committed copy for reasons unrelated to RC100.
- **MUTATE:** CFG216 with row 1's V_c doubled differs from ORIG (24 lines), so the substitution path is live.
- **Mirror safety:** no run wrote through a symlink into the repo (checked per run).

## Classification (frozen rules; "mechanical" means a reproduction row that compares against committed old-table targets, so it must fail whenever the input changes)
| reader | class | what moves |
|---|---|---|
| L323 (framework vs ΛCDM stress) | **VERDICT-MOVES** (against interest) | S "level is a tie" PASS → FAIL; S4 least-rising ΛCDM cell 3.7σ → 3.2σ above RC100's trend |
| hunt k_high-z_amplified_scatter | **VERDICT-MOVES** | k-hzs-4 PASS → FAIL (NaN level fit for RC100 at Υ × 1.5); RC100 slope −0.43σ → −2.00σ; rival separations shrink (above) |
| CFG217 attack | **VERDICT-MOVES** (recorded 09-29) | G2 'no' → 'yes'; V2 "rival deficit survives" NO → YES (borderline); identical to the 09-29 corrected run |
| CFG233 main | **VERDICT-MOVES**, mechanical | 17 reproduction rows against CFG216's committed targets fail; values equal the 09-29 corrected numbers (z −5.5 → −5.27; RC41 names 38 → 41) |
| CFG6 | **VERDICT-MOVES**, mechanical | replay control C2 (h16's committed line) fails; the RC100 slope moves −0.1123 → −0.1115 ± 0.063 (0.01σ) |
| CFG90 (with the mirror path) | NUMERIC-MINOR | pooled D_flat +0.137 → +0.035, D_rival −0.034 → −0.131 (0.74σ); NOT-REPRODUCIBLE as committed (hard-coded path) |
| CFG52 feas + pooled | NUMERIC-MINOR | pooled 0.03 dex (0.2σ); low-y counts 32 → 28 |
| CFG216 ×3 | NUMERIC-MINOR | = the 09-29 corrected outputs (flat slope −0.029 → −0.030; rival z 5.53 → 5.29) |
| CFG218 | NUMERIC-MINOR | b_RC100 0.100 (default path) vs 0.097 in its own 09-29 corrected mode |
| CFG222 / CFG223 | NUMERIC-MINOR | only the "committed table" rows move; both headlines already use the paper values |
| L320 / L322 | NUMERIC-MINOR | 3.0–3.4σ → 2.8–3.2σ; 3.5–3.7σ → 3.3–3.5σ |
| L331 / L332 | NUMERIC-MINOR | L331 above; L332 data slope +0.045 at every β (0.7σ); β = 0: framework +1.5σ → +0.9σ, ΛCDM +3.5σ → +3.1σ |
| h101, h105, h16, k01, k02, k03, k_high-z_floor_census | NUMERIC-MINOR | each headline < 1σ (h16's y < 2 median 1.385 → 1.841e-10 is a table row with no quoted error) |
| MNRAS v2 paper_numbers.py | NUMERIC-MINOR | RC100 slope −0.1123 → −0.1115; v3 is being rebuilt on the corrected file |
| zimmerman_theory_figures, rc100_deepMOND_framework_fit | NUMERIC-MINOR | deep-flag set 10 → 11; median ratio 1.31 → 1.18 / 1.03 → 0.92 (figures and prints only) |
| CFG227, CFG237, k04, k_contrarian_lever, a0z_clean_ledger | UNCHANGED | |

## Consumers to correct (by forward addenda, never by editing history)
- **`campaign_fresh_gravity/CFG0_own_findings_inventory.md` W14** ("a tie (L323/L331)"): the L323 half no longer holds.
- **Root `STANDING.md`** (an older status file): L320 "3.0–3.4σ" → 2.8–3.2σ on the corrected table. The adopted status record is `campaign_fresh_gravity/STANDING_2026-09-29.md`, where this lane is recorded.
- **CFG287 AUDIT.md**: its "CFG52/CFG90 pool moves 0.03 dex" holds for CFG52; CFG90 moves 0.10 dex (0.74σ).
- **MNRAS v3** reads the corrected file directly.

## Post hoc (labelled, at the owner's question "are we sure RC100 did it right?")
- `cfg289_posthoc_l323_flagged_rows.py`: L323 on the corrected table without RC100's own flagged rows. The flip survives:
  - without rows 67/83 (V_rot² < 0 by the paper's eq. 8): [−0.038, −0.007];
  - without all 16 flagged rows (n = 84): [−0.034, −0.004].
  S4 (every ΛCDM variant's inverted a₀ rises, against RC100's trend) also survives.
- **What it is not:** a statement about nature. RC100's f_DM and M_baryon come from the authors' own mass models, with gas from scaling relations, and f_DM tracks their M_baryon prior (CFG217 G2). The edge sits at the ~1σ level and carries no calibration systematic. The record's standing stays: **RC100 decides nothing.**

## Disclosed departures
- `cfg289_supplement.py` (CFG90 with the mirror path; CFG52's pooled.py and mock_bias.py) was added after the first comparison. CFG90's hard-coded path made the driver's FIX run of it void, and CFG52's pooled result lives in a script that does not name the CSV.
- The comparison's pass/fail-flip detector does not see verdict words such as YES/NO. CFG217's word changes were found by reading its diff.
- The 1σ judgement for each NUMERIC row was made by reading the diffs, as the criteria say.
- CFG90's committed script contains an absolute home path (committed earlier, 0137d584d). Per the owner's 2026-10-02 decision it is not scrubbed from history; a forward fix is noted for the owner.

## Files
- `FROZEN_CRITERIA.md`.
- `cfg289_build_corrected.py` (+ .out / _results.json).
- `cfg289_rerun.py`: the driver (scratch mirrors; ORIG / FIX / MUTATE).
- `cfg289_compare.py` (+ cfg289_compare.out / _results.json).
- `cfg289_supplement.py` (+ cfg90_mirrorpath_{ORIG,FIX}.out, cfg52_pooled_{ORIG,FIX}.out, cfg52_mock_bias_{ORIG,FIX}.out).
- `*_RC100FIX.diff`: FIX vs ORIG, text.
- `*_RC100FIX.*`: the FIX outputs that differ, with mirror paths scrubbed.
- **Re-run:** build → `cfg289_rerun.py <scratch> ALL` → `cfg289_supplement.py <scratch>` → `cfg289_compare.py <scratch>`.
