# EUC21R (BLIND RE-GRADE OF EUC21, THE GAS LANE ESZ1 ON THE MASK-APERTURE STELLAR MASS): READING NOTE

2026-11-14. Written and committed alone, before any EUC21R script exists and before any number of this lane is
computed. A blind re-grade: this session reads only EUC21's frozen criteria (and the sources they name), writes its
own code, reports its own labels, and only after its result is committed opens EUC21's `RESULT.md`.

kappa = 1/2 FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not
"theory closed". Adopts nothing; edits no README, ledger, scorecard or memory file; no outcome is a pass.

## 1. What this session had already seen about EUC21 before reading anything

Blindness check, done first: **blind.** Nothing in the starting context carried a result word or number of EUC21.

- **Recent-commit subjects shown at start (five):** XJ1 amendment A7 script; XJ1 amendment A7; PAPER72 v1.5 draft;
  BJ1 result (light stage); CJ1 scorecard eleventh update. None names EUC21.
- **Memory-index lines shown at start that touch the Euclid lenses:** an ESZ1 line (the source lane's own committed
  word, "ONLY A CUSP IS LEFT" on both footings, 237 lenses; ESZ1's full result is allowed reading anyway); an EUC17
  line saying the catalogue's stellar mass is the in-mask mass, that EUC17, EUC17R, EUC18 and EUC20 re-read the lens
  rows, that mask tables for all 6,173 lenses of sample S are on disk (EUC17 + EUC19), that a blind EUC20R is owed,
  and that "gas lanes ESZ1 / EXR not re-read"; an EXR1 + EXR2 line (both NOT EVALUABLE as frozen). No line names
  EUC21. I did not open the memory directory.
- **The task brief** names the folder `closure_2026_11_14/EUC21_mask_mass_gas_lane_reread/`, says the lead has graded
  it, and repeats what the criteria say (EUC18 and EUC20 lower the wide lenses' missing mass by about 40 %). No result.
- **Linked-session names** (EUC17R, EUC20R, an EUC20R relaunch): names and states only.
- **Git status at start** (truncated): no file name in the EUC21 folder was visible.
- **Not opened before my result is committed:** every file of the EUC21 folder other than `FROZEN_CRITERIA.md` (I did
  not list the folder); EUC18 and EUC20 files other than criteria (none opened); EUC17's and EUC17R's RESULT files;
  the memory directory; handoff files; and the shared side-session notes folder of this group of sessions, which may
  hold the lead's notes (read only after my result is committed).

Read for this note: EUC21 `FROZEN_CRITERIA.md`; ESZ1 in full (criteria, script, log, result); the code of EUC1, and
the parts of EUC4 (`GasEngine`), EUC8 (`Lens2`, `zs_case`) and EUC5 (imports) that ESZ1 uses; EUC17's frozen criteria;
the header lines of the two mask tables.

## 2. How I read the criteria

**The correction.** For every catalogue row whose identifier has a mask (`has_mask` = 1, `mask_radius_arcsec` > 0) in
EUC17's or EUC19's table: `f = M2D_frac(mask_radius_arcsec, te, n)` with EUC1's own `M2D_frac`, where `te` and `n`
are the `eclipse_effective_radius` (arcsec) and `eclipse_sersic_index` that EUC1's loader already reads; then
`lm ← lm − log10 f`. The lens's Sérsic shape in the law is untouched; only its total mass changes.

**Route.** My driver reads ESZ1's committed `esz1.py` as text, applies one substitution and executes it with
`__file__` set to ESZ1's own path, so ESZ1 imports EUC1, EUC4 and EUC8 from their own folders and reads EUC8's stored
results for K7 exactly as it did. The substitution: the text `if not all(v["ok"] for v in CK.values()):` (the gate
before the stack) becomes `if not all(v["ok"] for k, v in CK.items() if k not in ("K6", "K7")):`; the driver asserts
that the old text occurs exactly once (the later `allok = all(...)` line does not contain `if not all`, so it is not
touched; that later line is the "final gate" the criteria say will read NOT EVALUABLE). EUC1's loader is wrapped:
after EUC1's own `load` returns, each row with a mask gets the shifted `lm`; nothing is printed into ESZ1's log by the
wrapper, so the f = 1 harness can reproduce the log. Every file ESZ1 writes into its own folder is redirected (by an
`open` in the executed module's namespace) into `runs/<mode>/` of this lane; a write anywhere else stops the run.
Bytecode writing is switched off so no `__pycache__` file appears in a source folder. ESZ1_MUTATE is unset.

**Runs (one at a time, at most 4 threads, nice 19):** `harness` (f = 1 through the same code path), `corrected`,
`F1a` (f with R_e × 0.80 inside f only), `F1b` (R_e × 1.25 inside f only), and the twin `invert` (lm + log10 f with
the primary f). The bracket runs change R_e only inside f; the stars' Sérsic body in the law keeps the catalogue R_e,
as in EUC17's §5.

**Words.** My collector re-implements ESZ1's rules (I do not import ESZ1's functions for grading):
- family word: NO POWER if pred_min < 3σ (or not finite); EXCLUDED if measured + 2σ < pred_min; ALLOWED otherwise;
  pred_min = the far, b★ = +0.10 setting;
- lane word: NOT EVALUABLE if the checks fail or N_W < 100; HOT GAS DOES NOT SUPPLY THE WIDE LENSES if B30, B100 and
  G2 are all EXCLUDED; ONLY A CUSP IS LEFT if B30 and B100 are EXCLUDED; HOT GAS NOT EXCLUDED if B30 or B100 is
  ALLOWED; NO VERDICT otherwise; tag [BRACKET-DEPENDENT: list] if any of ESZ1's five brackets (CIB-deprojected map;
  θ_d 1.5′, 3.0′; grade A only; z_l ≤ 0.6 only) gives another lane word, each bracket's lane word recomputed by the
  same rule from that bracket's family words and N (ESZ1's own bracket words read NOT EVALUABLE in a corrected run);
- Part C: from the primary and CIB words the code produced before its final gate; tag if the CIB word differs;
  NOT EVALUABLE if the checks fail.

The input I take from each run is the family words, measured stack, σ and N per bracket, and the Part C words and
intervals, all from the run's `esz1_results.json`. **Rule self-test (R0):** the collector applies the same rules to
ESZ1's committed results file and must return its committed Part G and Part C words; if it does not, my collector is
wrong and nothing is graded.

**"The checks" in the lane-word rule** for the corrected run: H0 to H4 all pass (H2 includes K1–K5, K8, K9 passing).
K6 and K7 are excluded because they are expected to fail. H0 is judged on the harness run; H1 after every run; H2, H3
and H4 on the corrected run (also reported for F1a, F1b and the twin).

**Ambiguities and how I resolve them (before any number):**
1. *What is "the word" for UNCHANGED / CHANGED and FRAGILE / ROBUST?* The full string including any tag, because the
   committed column states the tag state ("no tag" for Y1; the CIB tag for Y2). I also report whether the untagged
   word moved, so a tag-only change is visible.
2. *Y2 per footing.* Part C uses no a₀: its measurement and matching are footing-free, so its word and labels are the
   same on both footings. Stated, not pooled.
3. *Which lenses get a mask.* Every catalogue row whose identifier is in either table with a usable mask. I check that
   every lens of sample S has one and that f is finite and in (0, 1]. The criteria assert full coverage; if any S lens
   has none, it keeps f = 1, the count is reported as a failed premise, not repaired silently. If a lens appears in both
   tables with different radii, the conflict is reported and EUC17's value (the first named) is used.
4. *H0 "log".* ESZ1's `.out` file (its log); every line is compared except lines that carry an elapsed time (ESZ1
   prints those only to stderr, so I expect none in the `.out`). The results file and per-lens file are compared byte
   for byte against the working-tree files after confirming git shows ESZ1's folder unmodified.
5. *H1.* `git status --porcelain --untracked-files=all --ignored` on ESZ1's, EUC1's, EUC4's, EUC5's and EUC8's folders
   and on the two mask tables, before and after each run, must be identical; and the sha256 of every file in ESZ1's
   folder must be unchanged.
6. *H3.* f recomputed by the collector from the mask tables and the catalogue on its own (same formula), compared with
   (corrected `log_Mstar`) − (committed `log_Mstar`) per lens of the per-lens file, to 0.001 (the file holds 4
   decimals).
7. *H4.* Primary map: the run's `stack_W` (N, mean, sigma) and Part G primary (N, meas, sigma); CIB map: the Part G
   bracket "CIB-deprojected map" (N, meas, sigma); each against the committed value to 1e-9 relative (N exact).
8. *Twin.* Bites if B100's pred_min (Part G primary) is above ESZ1's committed pred_min on both footings; the driver
   then exits 1 (2 if it does not bite).
9. *Exit codes.* The source exits 3 whenever K6 or K7 fail (its final gate), so `corrected`, `F1a`, `F1b` are expected
   to end with the source's exit 3; the harness with 0. The driver records the source's code and passes it on.
10. *If H0 fails* (for example floating-point summation that is not reproducible byte for byte), the as-frozen word is
    NOT EVALUABLE for Y1 and Y2; the numbers are still reported, and any amended reading goes in a separate file
    committed alone and labelled post hoc, after the as-frozen word.

**Reported, no word:** each family's pred_min, (pred_min − measured)/σ and f_T, corrected against committed; the
Salpeter-star (b★ = 0) and central-source settings from the model table; Part D as the code prints it; the
distribution of −log10 f over W and over S.

## 3. Not claimed

No measurement of a₀ or κ; no statement that hot gas exists or not beyond ESZ1's rule; no pass under any outcome.
The premise (catalogue mass = in-mask mass) rests on the paper's text and on one lens, as in EUC17.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
