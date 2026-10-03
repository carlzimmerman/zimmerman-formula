# CFG306: hostile referee of PAPER40 (MIGHTEE-HI a₀ width chain)

*A referee lane. It wrote only into this folder; no paper, lane, data or other file was edited, and nothing was committed or pushed. Every diagnostic here is post hoc and was not frozen. Nothing here is an a₀ measurement. κ = ½ is FITTED. No sentence says the data favour any law.*

**Recommendation: MAJOR REVISION; do not deposit v1.0.** Severity counts: 1 CRITICAL, 5 MAJOR, 12 MINOR, 9 NIT. Details are in `REFEREE_REPORT.md`.

## What was run

### 1. Clean-mirror reproduction (`cfg306_mirror_reproduction.out`)
- **The mirror.** `git archive 00d6c89ae` of the paper's inputs:
  - `campaign_fresh_gravity/`;
  - `real_research/{data, derivation_chain_2026, cross_thread_review_2026_09_26}`;
  - `data_assembly/`;
  - `qwen_claude_field_theory/papers_2026/`.

  It was unpacked in the session scratchpad and re-initialised as a one-commit git repository, so that the audit's `git show HEAD:` works.
- **What was re-run in the mirror:**
  - CFG301: stages A, SELFTEST, CC2 and B, plus B with MUTATE=1, B with MUTATE=2, and M5;
  - CFG302: main, MUTATE=1 and post hoc, with the 24 GB r1p0 cubes read in place through `MIGHTEE_R1P0_DIR`;
  - CFG304: main, MUTATE=a/b/c and post hoc;
  - `make_paper40_figures.py`;
  - `PAPER40_audit.py`, together with `--mutate` and `--mutate-tex`.
- **Result.**
  - Every results JSON and CSV is byte-identical. The only exceptions are CFG302's `cube_folder` string, which the environment variable sets, and the timing and memory lines in the `.out` files.
  - The figures are identical once their CreationDate is removed.
  - In the mirror the audit gives 299 of 306. The 7 misses are the B31 commit-existence rows, which cannot pass in a repository without history.
  - In the real repository at HEAD (run read-only) it gives **306 of 306**.
  - Both mutation modes fail as required.
  - All check tallies match the committed ones: CFG301 5/5, 3/3, 2/2, 7/7, 3/3, 3/3, 3/3; CFG302 12/13 with C-OFF(b) failing as committed, 8/8, 1/1; CFG304 9/10, 11/13, 9/10, 9/10, 2/2.

### 2. Number trace (`cfg306_number_trace.py` → `number_trace.csv`, `uncovered_numbers.csv`, `cfg306_number_trace.out`)
- 60 quoted numbers were re-derived with this lane's own code, from committed files at HEAD or from this lane's own re-implementation of the chain, and then looked for in the tex.
- **59 match.**
- **N39 does not.** The paper's "74.2–77.3″" beam range is copied from CFG302's README. CFG302's own output gives valid-channel beams of 62.2–77.3″ and per-sub-cube medians of 74.7–77.3″. The audit checks this row against the README.
- `uncovered_numbers.csv` lists the numeric tokens in audited blocks that no audit literal covers. They are mostly layout parameters, recipe constants and the references' journal data. The substantive ones are the abstract's "0.6" lower bound, "about 0.2 dex" (B24) and the SPARC "1.20" mentions.

### 3. Physics (`cfg306_physics_checks.py` → `.out`, `_results.json`)
- **Own estimator.** An independent chain and estimator reproduce CFG301 to 3 × 10⁻⁹ dex with the exponential kernel, and to 10⁻¹⁶ dex with `nu_mono`. An independent cut reproduces the 47 IDs, and CC2 is reproduced exactly.
- **P1: velocity frame.** k = 0 gives a₀ = 1.311 × 10⁻¹⁰ (68% 1.27–1.42), κ = 0.70 / 0.58. The recipe half-width at k = 0 is 0.128 dex, and the drift changes sign.
- **P2: kernel.** The kernel spread at y ≈ 0.03 runs from −0.001 to +0.078 dex. The framework's own closed form gives 1.216 × 10⁻¹⁰ at k = 1.
- **P3: flux × frame.** P3 crosses the flux scale with the frame. P3b combines frame, width correction and flux into a grid running from 0.59 to 1.31 × 10⁻¹⁰.
- **P4: selection.** The SNR_3D ≥ 8 cut: the 70 discs before it give 1.23, and the 23 it removes give 1.72 × 10⁻¹⁰. P4 also has the residual correlations.
- **P5: slope and errors.** The BTFR slope is 3.50 (inverse), and the error of the median is ±0.036 dex.
- **P6: SPARC × ALFALFA.**
  - W50/(2 sin i) exceeds V_flat by +0.026 dex.
  - The CC2 recipe with W50 gives +0.18 dex.
  - SPARC's M_HI sit +0.053 dex above ALFALFA's.
- **P7: H₂ and H₀.** M_H2 lowers a₀ by 0.027 / 0.070 dex. At the H₀-consistent distances a₀ is 0.962 / 1.208 × 10⁻¹⁰.

### 4. Velocity frame (`cfg306_velocity_frame.py` → `.out`, `_results.json`)
- **F1.** In the catalogue paper's own example spectra, the km s⁻¹ per channel equals c·Δν/ν_obs, the rest-frame width, to 0.07% in all five. The observed-frame conversion misses by 1.6–8.3%.
  - This reads the local arXiv PDF of MM26, which sits in the external data folder outside the repository. When it is absent, the script falls back to the transcribed values.
- **F2.** CFG302's z-trend is consistent with rest-frame and only weakly against observed-frame.
- **F3.** The ALFALFA width test does not discriminate.

### 5. Flux scale (`cfg306_flux_scale.py` → `.out`, `_results.json`)
- **S1.** The matched pairs are nearer, brighter and larger than the 47. Only 30% of the 47 lie inside the pairs' z range.
- **S2.** R_cat trends extrapolated to the 47 give −0.09 to −0.14 dex.
- **S3.** ALFALFA confusion would need about 500 times the mean density of uncatalogued HI.

### 6. Presentation (`cfg306_presentation_checks.py` → `.out`, `_results.json`)
- The abstract is 333 words.
- No e-mail address or home path appears in the paper files, the PDF text, or the 75 committed files of the paper and the three lanes.
- The Zenodo creator field carries the owner's name. That is the established practice, so flagged only as a NIT.
- The PDF is 7 pages with all fonts embedded, and 27 of 27 sampled numbers are present in its text.
- Zenodo description numbers equal the abstract's.

### 7. References
- **Checked on the arXiv API and Crossref** (abstracts and metadata only; no downloads): D23, MLS16, P21, R22, W16, V25, V26 (plus its source already on disk), MM26, H18, MS08. Lelli+2019 and Papastergis+2016 were located as missing prior art.
- **Provisional.** W16's size-relation coefficients were confirmed only by a web-search snippet.

## Reproduce
```
cd campaign_fresh_gravity/CFG306_paper40_referee
python3 cfg306_physics_checks.py      # ~1 min
python3 cfg306_velocity_frame.py      # needs pdftotext for F1's PDF re-read (else uses the transcription)
python3 cfg306_flux_scale.py
python3 cfg306_number_trace.py > cfg306_number_trace.out   # reads cfg306_physics_checks_results.json
python3 cfg306_presentation_checks.py # reads committed files via git show HEAD
```
All inputs are committed files, plus the optional local MM26 PDF. The scripts write only into this folder.

## Files
- `REFEREE_REPORT.md`: the recommendation, the numbered findings with location and fix, the proposed 247-word abstract, the over-claim sweep and the reference table.
- `number_trace.csv` and `uncovered_numbers.csv`.
- `cfg306_*.py` with their `.out` and `_results.json`.
- `cfg306_mirror_reproduction.out`.
