# CFG290 — referee lane for the MNRAS v3 manuscript (2026-10-02)

The target is `qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/` at commit 32f9a609c. This lane is read-only on the manuscript: nothing outside this directory was edited, and nothing was committed. κ = ½ is FITTED; the cold mass is still required.

**Result:** MAJOR REVISION. Findings by severity: 1 CRITICAL, 10 MAJOR, 20 MINOR, 8 NIT. The full report is in `REFEREE_REPORT.md`.

## What was run

1. **`reproduce_all.sh` in an isolated mirror** (scratch directory, not in the repo).
   - **The paper directory** was taken with `git archive 32f9a609c`.
   - **Read-only data** were symlinked: SPARC rotmod + MRT, the KMOS3D FITS/CSV, both RC100 CSVs, the MIGHTEE-HI digitised CSV, the corpus JSON and `campaign_fresh_gravity/`.
   - **The estimator scripts** were copied with `git show 32f9a609c:…`. Running in place would rewrite tracked files (`paper_numbers.out`/`.json`, the figures, the PDF, and `real_research/dark_sector_2026/L332_…_results.json`).
   - **First attempt** stopped at step 1. The mirror lacked `real_research/reviews/mi_route_a_kernel.py`, which `mi_btfr_intercept_kappa_door_2026.py` imports. That was an omission in my mirror, not a repo defect.
   - **Second run: ALL STEPS PASSED** (about 67 s):
     - estimator A gives 0.465 ± 0.076;
     - the earlier estimator B gives 0.551 ± 0.043;
     - the H₀-convention audit runs; its check C4 makes R1 = 0.450 ± 0.074 OPERATIVE;
     - L332 passes 4/5 (0 load-bearing failures), and T1/K1 are identical on the corrected RC100 file;
     - the profile-likelihood table reproduces;
     - `paper_numbers.py` gives 71 checks, 0 FAIL;
     - `make_figures.py` gives 6/6;
     - the tectonic build succeeds (14 pages).
   - **Diffs against the committed files:**
     - `paper_numbers.out`: byte-identical;
     - `paper_numbers.json`: identical;
     - `L332_kmos3d_trend_replication_results.json`: identical.
2. **`cfg290_referee_checks.py`** (+ `.out`, `_results.json`). Independent re-derivations, written without importing `paper_numbers.py`:
   - **R1** abstract length;
   - **R2** the RC100 inversion without RC100's own flagged rows (eq.-8 violators 67 and 83; 14 below V_rot/σ₀ = 2.3, re-derived from the table), and the comparator slopes fitted at RC100's redshifts;
   - **R3** the design odds: the closed form against Monte Carlo, the probability of reaching 20:1, and the odds at the halo mass the gate selects;
   - **R4** one shared-calibration cell by Monte Carlo;
   - **R5** estimator-A pulls on the four H₀ conventions;
   - **R6** the two likelihood ratios separately;
   - **R7** the SPARC Hubble-flow count (97) and the MIGHTEE-HI colour groups (18 for 19 galaxies);
   - **R8** M₂₀₀ of gate-passing discs at z = 2.5, and Desmond (2023) on both footings;
   - **R9** estimator B, the standard fit, and the Υ_disc needed for κ = ½, with SPARC's H₀ = 73 Hubble-flow distances moved to 67.4 (R1).
   - **Cross-check:** the re-implementation reproduces the paper's 0.547 (B), 0.636 (standard fit at Υ = 0.5) and 0.621 (Υ for κ = ½).
3. **`cfg290_reference_check.py`** (+ `.out`, `_results.json`). Compares all 49 bib entries with Crossref (DOI), arXiv (eprint-only) or Zenodo metadata. Small JSON/Atom reads; nothing saved. One wrong DOI was found (KlinkhamerKopp2011).
4. **`cfg290_abstract_reads.py`** (+ `.out`). Prints the arXiv abstracts (CC0 metadata) of the 16 papers whose content the manuscript characterises, for comparison with the text: Limbach+08, Milgrom 1999/2017/2020, Oppenheim & Russo, Hertzberg & Loeb, Mayer+23, MUSE-DARK II/III, Vărăşteanu+25/26, Übler+17, Desmond 2023, Hirtenstein+19, RC100, KURVS.
5. **`number_trace.csv`.** 73 quoted values traced to their committed sources: 66 match, 3 partial, 3 mismatch, 1 n/a.
   - **Mismatches:** the decision value against the gated halo mass; the comparator-slope label; "three decades".
   - **Partial:** estimator B's H₀ range (old variant); Mayer's z = 2.3 against the z = 2 in the abstract; Ciocan's Δ against their own intercept.
6. **Figures** rendered to PNG in scratch and inspected by eye.
7. **Personal-path check:** `git grep` at 32f9a609c, and a byte scan of the PDF and figures, for e-mail and home paths. All clean.

## Re-run

All of these run from the repository root or from anywhere:

```
python3 campaign_fresh_gravity/CFG290_mnras_v3_referee/cfg290_referee_checks.py      # about 1 min, offline
python3 campaign_fresh_gravity/CFG290_mnras_v3_referee/cfg290_reference_check.py     # network: Crossref, arXiv, Zenodo
python3 campaign_fresh_gravity/CFG290_mnras_v3_referee/cfg290_abstract_reads.py      # network: arXiv API
```

The `reproduce_all.sh` re-run needs a mirror, as in item 1. Running it in place rewrites tracked files.

## Not verified

- **Journal versions:**
  - the published RC100 table (ApJ 944, 78) against the arXiv v1 copy;
  - likewise FS+18 and Umehata+25 (CFG287 lists these as OPEN).
- **Table- or body-level statements, unreadable at abstract level:**
  - Übler+17's −0.44 / −0.27 dex;
  - Jeanneau+26's "gas 70 per cent of M_b";
  - Ciocan+26's 95% interval and a₀(0) = 1.0 (taken from CFG190's criteria, which say abstract-level/summariser);
  - Vărăşteanu+25 Table 3 and the K_s median 0.35;
  - Marasco+25's 0.72;
  - the V26 table a₁ values;
  - OLAS M0717-02064's parameters (z, μ, M★, v/σ);
  - Mayer+23's z = 2.3.
- **Lane outputs checked only against the text, not re-derived:**
  - MUSE-DARK (CFG262/236);
  - KURVS (CFG140/160/165/189/194);
  - MIGHTEE mocks (CFG258);
  - z ≥ 4 pools (CFG269);
  - the gas bracket (CFG224b).
  - These lanes were not re-run here. CFG269's committed `.out` shows its control C1 FAIL (max |dev| 1.87×10⁻³ against 10⁻⁴).
- **AI tool provenance.** Whether DeepSeek, GLM or Qwen models produced any input. Only directory and commit-message names were seen.
- **OUP policy.** The 2026-09-10 AI-disclosure policy page (the checklist says it would not load) and the current MNRAS keyword list were not re-read. The six keywords are standard MNRAS keywords.
- **CFG240 label.** Its "nu_mono" is literally the exponential kernel, b = s/(2(e^s − 1)) (`CFG240_fisher.py` l.8), so S4q compares like with like. The memory note "ν_mono ≠ exp-RAR kernel" refers to the framework's own ν_mono (≤ 2.4% off), which the paper does not use.

## Files

- `REFEREE_REPORT.md`: recommendation, 39 numbered findings, the RC100 answer, and the compliance and figure checks.
- `number_trace.csv`
- `cfg290_referee_checks.py` / `.out` / `_results.json`
- `cfg290_reference_check.py` / `.out` / `_results.json`
- `cfg290_abstract_reads.py` / `.out`
