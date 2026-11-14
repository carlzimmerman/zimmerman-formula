# EUC20R (BLIND RE-GRADE OF EUC20): READING OF THE FROZEN CRITERIA

Written and committed alone, before any EUC20R script exists and before any number of this lane is computed.
2026-11-14. The criteria are `closure_2026_11_14/EUC20_mask_mass_grade_b_reread/FROZEN_CRITERIA.md`; this file
restates how this blind lane reads them. κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s²,
graded separately, never pooled. Not "theory closed". A re-read: it adopts nothing, edits no ledger, scorecard,
README or memory file, and no outcome is a pass of the lensing gate.

## 0. What this session's starting context showed about EUC20 (blindness record)

- **Recent-commit list** (five subjects): an XJ1 amendment A7 script, the XJ1 amendment A7 itself, a PAPER72 v1.5
  draft, a BJ1 result, and a CJ1 scorecard update. None begins with `EUC20`. The PAPER72 draft subject names other
  lanes (XJ1, CSD1, FWN2, RRL1R, RB1R, RB2R, GAS1, CJ1 updates) and says nothing about EUC20.
- **Auto-loaded memory index** (shown before any action; the memory directory itself was not opened): one line says
  that the Euclid catalogue stellar mass is the mass inside the modelling circle, that lanes EUC17, the blind EUC17R,
  EUC18 and EUC20 re-read the Euclid lens rows and are pushed, that mask tables for all 6,173 lenses of sample S are on
  disk (EUC17 + EUC19), that a blind EUC20R is owed "so words and numbers are in the linked file only", and that the
  gas lanes ESZ1 / EXR were not re-read. No EUC20 word or number was shown. Other index lines showed committed words
  of source lanes (EUC1 NO VERDICT / NO VERDICT; ESZ1; EXR1 / EXR2), which this lane may read anyway.
- **Git status snapshot** (truncated) listed untracked file names including three handoff files about Euclid / DESI
  and a mass budget; none was opened.
- **The task brief** named the EUC20 folder, said it holds a `RESULT.md`, scripts, a `runs/` folder and `.out` /
  `.json` files, named the EUC21 folder (`EUC21_mask_mass_gas_lane_reread`), and said an earlier blind attempt
  stopped after seeing a result in a commit subject (it committed nothing). No label was given.
- **Linked-session note:** session names `euc17r-blind-re-grade-of` and `euc20r-blind-re-grade-of` (idle).
- Files opened so far: the EUC20 `FROZEN_CRITERIA.md` (only); the EUC17 and EUC18 `FROZEN_CRITERIA.md`; the two mask
  tables (column names, row counts, status counts, overlap); committed code, criteria and outputs of EUC1, EUC4, EUC5
  (criteria amendment A1, `euc5.py`, `euc5_a1.py`, `euc5_a1.out`), EUC6, EUC8 and LNJ1; three values of the
  catalogue's mass columns (to see that `_low` / `_upp` are error widths). Nothing else of EUC20, EUC21, EUC17's or
  EUC18's code or results, EUC17R, the memory directory or any Euclid handoff file was opened. The shared notes folder
  for this session group was listed and is empty. Recent history is read with `git log --format=%h` only.

So this lane is blind to EUC20's labels and numbers. It knows (from the criteria, §4) the lead's pre-run hand estimate.

## 1. The correction, as read

Per lens, `f = M2D_frac(mask_radius, eclipse_effective_radius, eclipse_sersic_index)` with EUC1's own `M2D_frac`
(imported from `euc1.py`), both radii in arcsec, and `lm_corr = lm − log₁₀ f`. EUC1's loader keeps the mass errors
as widths (`lm_lo`, `lm_up` are positive offsets; EUC1's Monte Carlo adds them to `lm`), so "mass errors as
catalogued" means those two columns are left untouched.

**Masks.** The union of `euc17_masks.csv` and `euc19_masks.csv` (the two tables share no identifier). A lens has a
mask record when its row has `has_mask = 1` and a positive `mask_radius_arcsec`. Every other lens, including the
EUC17 rows with HTTP status −2 and lenses absent from both tables, keeps its catalogued mass (f = 1) and is counted.
The correction is applied only where f is finite and in (0, 1]; a lens failing EUC1's validity cuts cannot reach any
sample, so this guard cannot change a sample.

**Brackets.** F1a uses `R_e × 0.80` and F1b `R_e × 1.25` **inside f only**; the lens model (Sérsic body, `b`, Jeans
model) keeps the catalogue's `R_e`. **Twin** `invert`: `lm + log₁₀ f` (exact shift route: `b − log₁₀ f`).

## 2. Routes, as read

- **EUC8 and EUC5 A1, wrapped loader.** One fresh Python process per run. The driver imports EUC1's `euc1.py` as
  module `euc1` (the name both source scripts import), replaces `euc1.load` with a wrapper that calls the original
  and then shifts each row's `lm`, imports the source script as a module from its own folder, injects into that
  module a write-redirecting `open` (any write-mode open is sent to this lane's run folder; reads are untouched), sets
  `sys.argv` to `--data-dir _external_data/euclid_dr1_eclipse` and calls its `main()`, catching its exit code.
  Bytecode writing is off, so no `__pycache__` is written into a source folder. The source text is not edited.
- **LNJ1, one substitution.** Its text is read, the expression `fl(r["eclipse_log_survived_mass_med"])` (it occurs
  once; the run stops if the count is not exactly one) becomes
  `(fl(r["eclipse_log_survived_mass_med"]) - <log₁₀ f of r["unique_identifier"]>)`, and the text is compiled with its
  own file path as filename and executed with `__file__` set to that path (so it finds its own inputs), with the same
  write-redirecting `open` in its globals. With f = 1 the substitution subtracts zero.
- **EUC4 bins, exact shift.** `euc4.py` and `euc1.py` imported; EUC1's original `load` / `select` (grade B); the
  three bins W_B (θ_E ≥ 1.7″), secondary (1.3″ ≤ θ_E < 1.7″), complement (θ_E < 1.0″); `b` from `E.build` and
  `Engine.solve_b` at full precision, laws S and B, both footings; `b_corr = b + log₁₀ f`; statistics with EUC1's
  `stats` drawing from one generator seeded 20261112 in EUC4's own order (W_B, secondary, complement; within each,
  law S then B, canonical then alt), so that with f = 1 the bounds are EUC4's to the last digit; words with
  `euc4.word`.

## 3. Rows and how each word is taken

- **G1** EUC4's secondary bin, law S, per footing, f₂₅ with EUC4's lines (BREAK lower ≥ 0.25 / NOT CONFIRMED upper ≤
  0.10 / NO VERDICT; N < 30 NOT EVALUABLE), labelled secondary. Committed BREAK / BREAK.
- **G2** EUC8's lane word from its Part B rule. **Ambiguity resolved here:** under the correction EUC8's own script
  prints NOT EVALUABLE as its lane word whenever any of its checks fails, and H2 requires K1 and K5 to fail (they
  assert uncorrected reference numbers). That printed line is not this row's word. The word is EUC8's Part B rule
  applied to the family words the script computes (`family_words` in its results file): NO FAMILY FITS if no family
  is ALLOWED; SLOPE BRACKETED if γ = 0 is TOO DIFFUSE and T is TOO CONCENTRATED; RESIDUAL MUST BE CONCENTRATED / MUST
  BE EXTENDED for one of the two; SLOPE NOT CONSTRAINED for neither; NOT EVALUABLE if the dispersion sample D has
  N < 10. In place of EUC8's all-checks gate this lane uses its own H0–H3: if H2 does not hold exactly (K2, K3, K4
  and K6 pass, K1 and K5 fail) or H0, H1 or H3 fail, G2 is NOT EVALUABLE. With f = 1 this construction must give the
  committed SLOPE NOT CONSTRAINED / SLOPE NOT CONSTRAINED (part of H0). Committed SLOPE NOT CONSTRAINED on both.
- **G3** LNJ1's word before its known-answer gate. **Ambiguity resolved here:** under the correction its KA-1 and
  KA-2 fail and its WORD line prints NOT EVALUABLE. The word is rebuilt from the results file exactly as the script
  builds it before that gate: the primary configuration's final word (its raw word passed through its own twin power
  gates) followed by ", FRAGILE" if any of LNJ1's bracket words (catalogue scale, c × 0.7, c × 1.4, X = PD1 share,
  measured-speed rule, AGEL draw majority) differs from it. The primary raw word and the bracket words are reported
  beside it. With f = 1 the rebuilt word must equal the committed NO POWER, FRAGILE / NO POWER (part of H0). G3 is
  NOT EVALUABLE if H2 does not hold exactly (KA-0, KA-3, KA-4, KA-5, KA-6 pass; KA-1, KA-2 fail) or H0 / H1 fail.
- **Labels per row and footing:** the corrected word; UNCHANGED or CHANGED against the committed word (for G3 the
  whole word including LNJ1's own FRAGILE tag is compared); this lane's FRAGILE if F1a or F1b gives a different word
  (for G3, the whole rebuilt word), else ROBUST. A CHANGED word is said to move toward the law or away from it, never
  called a pass.

## 4. Checks, as read

- **H0** per route, with f = 1: every file the source script writes is compared with the committed file of the same
  name byte for byte; for logs (`.out`), every line not carrying elapsed time must match, where an elapsed-time line
  is one containing `elapsed` or a `(<digits> s)` group. EUC4 bins: every committed point statistic of the three
  bins, both laws and footings, to 1e-9, bounds to 0.01, words identical. A failure makes that source lane's rows and
  readings NOT EVALUABLE.
- **H1** `git status --porcelain` empty for the folders of EUC1, EUC4, EUC5, EUC6, EUC8, EUC10, EUC17, EUC19, LNJ1,
  JNT2 and PD1 after every run (EUC20's own folder is not inspected).
- **H2** as frozen: EUC8 exactly K1 and K5 fail; LNJ1 exactly KA-1 and KA-2 fail; EUC5 A1 none, meaning its
  validation states stay as committed (F1 FAIL, F2 pass) and its N(P) stays 32. Checked on the primary run; the
  bracket runs report their states.
- **H3** EUC8's K1 value under the correction reads 0.444 / 0.379 to 0.001.
- **H4** mask coverage per row: G1 the 292 secondary lenses; G2 the lenses of EUC8's sample D (θ_E ≥ 1.3″ with a
  qualifying DESI dispersion), with all 55 dispersion lenses and class W reported beside; G3 sample S. A row is NOT
  EVALUABLE if more than 5 % of its lenses have no mask. Readings report their own coverage (complement bin, EUC8
  Part A classes, EUC5 A1's 55 lenses, EUC6's paired lenses).
- **Twin** `invert`, own outputs, the twin driver exits 1 only if all of these hold, else 2: EUC8's Part A median
  far-case excess ΔM of class W (b★ = 0) is above the committed value on both footings; EUC5 A1's raw median `b_dyn`
  under law S is above the committed value on both footings for sample P **and** for sample S (the criteria say
  "sample median"; both are required, the stricter reading); G1's f₂₅ (law S) is not below the committed 0.4247 /
  0.3801 on either footing. LNJ1 has no twin here.

## 5. Readings without a word, as read

- EUC4's complement bin, with its would-be word (committed NO VERDICT / NOT CONFIRMED), and the W_B bin beside
  EUC17's corrected fractions.
- EUC8 Part A, from the corrected run's results: per class (W, 1.3–1.7″, 1.0–1.3″, below 1.0″), far and central
  cases, both footings: fraction needing extra mass, median excess mass with 16–84 %, share of the lensing mass.
- EUC5 A1 from the corrected run: `b_dyn` by Einstein-radius class (raw, F1-corrected, `b_∞`) and the median of
  `b_dyn − b_∞`. Its word stays NOT EVALUABLE (F1 gate).
- **EUC6.** EUC6's 243 complete pairs are rebuilt from its committed targets and ring counts with its own coverage
  rule (checked: 243 pairs, median D +3.38). Per pair `Δ = lm_corr(W) − lm_corr(C)`; reported: the median Δ (and the
  catalogued median beside it), the controls' own richness–mass slope (ordinary least squares of the controls'
  richness on their corrected log mass; the catalogued-mass slope beside it), and the worth = slope × median Δ, with a
  2,000-resample bootstrap interval over pairs (seed 20261112). **"A large part", resolved here:** if the worth's
  magnitude is at least one third of EUC6's +3.38 (1.13 galaxies), in either sign, the RESULT says EUC6 needs a
  re-matched control set; whether it would reach +2.28 (the size that, as a uniform shift, would take EUC6's lower
  bound to zero) is stated beside it.

## 6. Order of work

READING (this file, committed alone) → code → one run per route and mode as frozen (f = 1 harness, primary, F1a,
F1b, invert; LNJ1 without invert; EUC5 A1 without brackets, as it carries no word) → `RESULT_BLIND.md` with the
as-frozen labels first → commit code, outputs and result → only then open EUC20's `RESULT.md` and write
`RECONCILE.md`. Any check judged wrongly designed goes into a post hoc amendment file committed alone, reported after
the as-frozen word. Nothing is pushed.

κ = ½ FITTED; not theory closed. Adopts nothing.
