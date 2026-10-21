# AG5: November ALMA scoring, ready before release. ⚠️ Under its own frozen rules, neither release can trigger the theory's kill line

> **STATUS NOTE (dated 2026-10-20, after commit; FROZEN_SCORING.md unchanged): SECONDARY READING, NO VERDICT WEIGHT.**
> - The owner decided in the orchestrator chat: "keep the original CFG806/809 plans". The governing ALMA scoring plans are
>   `campaign_fresh_gravity/CFG806_u4_27928_scoring` (1bf70683b) and `CFG809_gs4_24110_ci21_scoring` (966d50a87), scored with
>   the CFG942 harness. This is recorded in `campaign_fresh_gravity/OWNER_DECISION_2026-10-20_ALMA_GOVERNING_PLANS.md` and the
>   LEDGER row OWNER-DECISION-ALMA.
> - AG5 duplicated those earlier plans: its inventory grep was case-sensitive and missed the lowercase lane folders.
> - AG5 may be reported alongside them as a labelled secondary reading. Its power finding (the kill line cannot fire on one
>   disc under its 0.15 dex floor) agrees with the governing plans' rule that one disc excludes no model.


- **Rules:** `FROZEN_SCORING.md`, committed alone first (7ea94d2ae).
- **Scorer:** `score_alma.py`.
  - Self-tests: `python3 score_alma.py --selftest` → `score_alma_selftest.out`; `AG5_MUTATE=1 python3 score_alma.py --selftest`
    → `score_alma_selftest_MUTATE.out`.
  - Release day: fill `measured_TEMPLATE_<target>.json` from `measure_<target>.py`, which is written after download and before
    any pixel is read. Then run `python3 score_alma.py measured_<target>.json`.
- **Settings:** κ = ½ fitted; footings never pooled; not theory closed.

## The power finding (from the scorer itself, sealed numbers only, no data)
- **U4_27928 (11-06):** suppose the measured gas equals exactly what a₀ ∝ H(z) needs. Every framework branch is still within
  0.7–1.0σ_tot at V_c = 250–300 km/s, and R-H is FLOOR at 225 km/s and below. **So the kill line cannot fire on U4.**
- **GS4_24110 (11-28):** scanning log M_gas from 8.0 to 11.0, detected or as an upper limit, **the kill never fires.** Some
  framework branch always stays within 2σ_tot. At log M_gas 11.0 detected, the best framework branch is at 2.0σ (M* 10.89) and
  1.65σ (M* 10.76).
- **Why:** stars dominate the baryons inside R_e. A 1-dex change in gas moves the total baryons far less than the 0.15 dex
  systematic floor (CFG571's, frozen) allows to be resolved.
- **What the November data CAN do:**
  - a ≥ 3σ gas detection in GS4_24110 counts against a₀ ∝ H(z) and the ΛCDM-feedback RAR scale, which are FLOOR at
    M* 10.89. CFG572's public CO(4–3) and dust already point that way;
  - they can show which law form (ν_mono, n=1, n=2) sits closest.
- **What they cannot do** is falsify the framework by its canonical §2 kill line. The canonical statement's table lists ALMA
  as a kill test. With one disc each and the frozen floor, they are **demonstrations**, as CFG571 itself said for single discs.
- **The only scheduled kill test is Gaia DR4 (2026-12-02).**

## Controls
- **S1 PASS:** every seal's sha256 matches (CFG571 be27457d…, CFG775 3d236378…, CFG778 b9f3e827…, AG4e 9802de0d…,
  AG4d d64727b5…).
- **S2 FAILED as frozen, diagnosed:**
  - CFG571, CFG778, AG4e and AG4d reproduce exactly (0.0 dex).
  - CFG775 reproduces to 5.6×10⁻⁵ dex: its own sealed numbers were computed with a BH ratio that differs slightly from both
    the r_BH stored in its seal and its results table. This is a seal-internal inconsistency, about 0.04% of σ_tot.
  - First run: 4.9×10⁻⁵ dex, because the scorer took CFG775's stored r_BH. It now uses the results-table interpolation that
    CFG778, AG4d and AG4e were computed with.
- **S3 PASS:** a synthetic measurement equal to F-DESI's requirement scores Δ = 0, CONSISTENT, and the kill does not fire.
- **S4 (as frozen) cannot be built:** no U4 V_c separates the framework from R-H by > 3σ_tot. That is the power finding above.
- **S4b (disclosed; code path only):** the same synthetic R-H case with the systematic floor set to 0 fires the kill, exit 1.
  The kill logic works; the limitation is power, not code.

## Gaia DR4 (2026-12-02): scorer ready
`campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring` (lane ID CFG825):
- The synthetic controls C0–C3, C5 and MUTATE pass.
- C4, the once-only DR3 code-path run, has been made: PASS, R = 0.97 ± 0.18 at N = 348, UNDECIDED as expected.
- The DR4 run is once-only (`--dr4 TABLE`), after release, on the owner's yes.

## Measurement scripts (to be written at release, before any pixel is read)
`measure_U4_27928.py` and `measure_GS4_24110.py` implement FROZEN_SCORING.md's procedure. The ALMA product download needs the
owner's yes, with file names and sizes stated.
