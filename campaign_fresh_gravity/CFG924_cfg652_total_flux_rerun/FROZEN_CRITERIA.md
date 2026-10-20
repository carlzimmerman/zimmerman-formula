# CFG924 FROZEN CRITERIA: CFG652 re-run with CFG922 A1's total-flux census (does any CFG652 class or bracket move?)

Block CFG920–929 (LEDGER row 663; 924–929 listed free). DATA RE-CHECK of CFG652 (criteria 11c7906ef, result ef182618d), prompted
by CFG922's side finding (README §post-hoc 2): CFG652's condensed masses M_cond come from KiDS DR4 bright-sample LePhare masses,
which are GAaP aperture masses (biased low), with masked galaxies dropped. No new posit, no new model.
Committed ALONE, before any script is written and before any A1-corrected mass of any eFEDS group is computed. Date 2026-10-20.
κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. "Cold energy"; its mass is required; no
particle species; not "theory closed". Raw data and framework-native models only (CFG652's models, unchanged).

## Seen before this freeze (disclosed)
- Every CFG652 output: `cfg652_test{,_MUTATE,_POSTHOC}.out` and results JSONs (primary BOTH EXCLUDED in all 10 cells, both
  footings; χ²_a 22.9 / 22.3, χ²_b 28.7 / 25.2; A_out (a) +0.16, (b) +0.43; POSTHOC hint "(a) FAVOURED", FRAGILE), its README,
  criteria and code; CFG652's own disclosure that 66 of 148 groups have no bright galaxy within 0.2 R_X.
- CFG922's README, criteria, code and A1 outputs: sample fluxscale median −0.457 mag (16–84%: −0.669 / −0.298); eRASS1 S_up
  3.8e11 → 9.5e11, S_cen 9.8e10 → 3.5e11; for bright galaxies at z > 0.25 the rebuild gives −1.6 to −2.9 mag (may include
  envelope light).
- The prompt's expectation that M_cond is low by ×1.5–3. No A1 mass of any eFEDS group, and no CFG924 number, has been seen.

## Data and code (read-only; nothing downloaded; no other lane edited)
- CFG652 stored work files (`_external_data/cfg652_work`): `cfg652_inputs.npz` (148 groups), `cfg652_esd.npz` (per-group ESD
  sums; the lensing measurement does not depend on M_cond and is reused unchanged), `cfg652_models.npz` (for K tests only).
- KiDS DR4 bright sample + LePhare (`real_research/data/lensing_rar/`).
- Code reused by exec of text slices of committed sources (never imported, so nothing of theirs is written):
  CFG922 `read_cols`, `load_bright` (with its A1 branch), `census_652`, `Census`, `mlim_table`, `unit`; CFG652 `cfg652_test.py`
  preamble + `models` block + `score` block verbatim (only WORK and the output directory redirected); `cfg652_model.py`
  (sha256 04352d4e…d60d1, imported from this checkout). CFG686's distance slice only for K4b (as CFG922 does).

## Census variants (all use CFG652's frozen recipe: G09 box, |z_phot − z| ≤ 0.05(1+z), net = mass inside R_X − area-scaled
## mass in 3–6 R_X, floor = most massive galaxy inside 0.2 R_X; planar ra·cos(dec) metric)
- **F (frozen):** CFG922's `load_bright` with AMEND off → must reproduce CFG652's stored masses (K1).
- **A1c (central, PRIMARY):** CFG922's `load_bright` with AMEND = "A1": MASS_MED scaled to total (AUTO) flux with the GAaP r
  magnitude rebuilt from M_abs + DM + K, brightening only, capped at 1 mag (×2.5); masked galaxies kept. Then the A1 footprint
  step, mirrored on CFG652's apertures: coverage = (all bright rows in the box, any z / mask / mass, inside R_X) / ((those in
  3–6 R_X) / 27).
  - coverage < 0.5: NOT MEASURED → M_cond = median(M_cond/M_hot over measured groups with M_cond > 0) × M_hot; M_bcg = median
    BCG share (M_bcg/M_cond over the same groups) × M_cond;
  - 0.5 ≤ coverage < 1: M_cond and M_bcg divided by coverage; coverage ≥ 1 unchanged.
- **A1u (upper bracket):** as A1c but the flux correction uncapped (CFG922's upper-end treatment, applied to MASS_MED, the column
  CFG652's recipe uses); NOT MEASURED groups get the 84th percentile of M_cond/M_hot instead of the median.
- Groups whose variant M_cond is 0 are excluded (CFG652's post-freeze rule; the models are undefined there). All other fields of
  `cfg652_inputs.npz` (z, R_X, M_hot, coverage, ids) are copied unchanged; f_hot is recomputed as M_hot/(M_hot + M_cond).

## Models and statistic
- A1c: CFG652's `models` block verbatim on the A1c inputs: (a) and (b), both footings, variants x1, M_cond × 10^±0.2, gas to
  1 / 4 R_X, plus CFG652's MUTATE M1 arrays.
- A1u: the same `cfg652_model.system` / `delta_sigma` calls, x1 only (both footings, both models). For the verbatim score its
  p02 / m02 / g1 / g4 entries are copies of x1, so **A1u's FRAGILE flags are not evaluated** (it is a bracket on the label only).
- Statistic and labels: CFG652's `score` block verbatim (8 bins 53–783 kpc, jackknife covariance with Hartlap, χ²_a, χ²_b,
  Δχ² = χ²_b − χ²_a; (a) FAVOURED / (b) FAVOURED / BOTH EXCLUDED / NOT DIAGNOSTIC; FRAGILE under M_cond ±0.2 or gas extent;
  footings must agree; the 2-halo conditional tag on any (b) FAVOURED).

## CFG924 decision rule
**Cell level** (2 footings × 5 variants): HOLDS if the A1c label equals CFG652's stored label for that cell, else MOVES (old →
new). Δχ²_a, Δχ²_b and ΔA_out against CFG652 are reported for every cell.

**Verdict level** (CFG652 stored final: BOTH EXCLUDED, not fragile, both footings):
- **CFG652 VERDICT HOLDS**: the A1c final label equals the stored final (same label, no new FRAGILE flag, footings agree) AND
  the A1u x1 label equals the stored x1 label on both footings.
- **HOLDS AT CENTRAL, MOVES AT UPPER (BRACKET-DEPENDENT)**: A1c final equals the stored final, A1u x1 differs on either footing.
- **CFG652 VERDICT MOVES**: the A1c final differs (the new label is named, including a new FRAGILE flag or FOOTING-DEPENDENT).

**Bracket level** (CFG652 declared M_cond × 10^±0.2 as its stellar-mass / cold-gas / completeness bracket):
Δ_i = log10(M_cond,A1c / M_cond,F) over groups with both > 0.
- **BRACKET EXCEEDED (HIGH)**: median Δ > +0.2; **BRACKET COVERS**: |median Δ| ≤ 0.2; **BRACKET EXCEEDED (LOW)**: median
  Δ < −0.2. Reported with the 16/84 percentiles, the fraction with Δ > 0.2, the fraction with Δ < 0 (masked galaxies can raise
  the background), and the same numbers for A1u.

**Reported, no verdict weight:** (i) SAME-SAMPLE: A1c masses on the groups with M_cond > 0 in both F and A1c (separates the mass
change from the sample change); (ii) CFG652's POSTHOC cut (M_bcg > 0 and M_cond ≥ 1e11) under A1c; (iii) CFG652's secondary
f_hot split and its MUTATE M2 under A1c; (iv) census bookkeeping: groups NOT MEASURED / partial, groups entering or leaving the
M_cond > 0 sample.

## Controls (all must PASS before the main result is read; a failure makes the lane VOID until fixed and disclosed)
- **K1** census F (exec'd CFG922 `census_652` on the unamended sample) reproduces CFG652's 148 stored M_cond and M_bcg: max rel
  < 1e-9.
- **K2** CFG652's verbatim `score` block on its own stored work files reproduces `cfg652_test_results.json` (all 10 cells: χ²_a,
  χ²_b abs < 1e-6; p, A_out, sA abs < 1e-9; labels; final; K1 cross-shear χ²; split D_obs, σ_D, M2 median), and the stored
  POSTHOC (χ², labels, final) and MUTATE (M1 χ²) JSONs.
- **K3** `cfg652_model` (this checkout, sha256 checked) reproduces the stored model arrays (all 22 per group) for 6 groups: the
  groups at M_cond rank fractions 0, 0.2, 0.4, 0.6, 0.8, 1 among CFG652's 131 (rank = round(q × 130)): max rel < 1e-10, NaN
  pattern equal.
- **K4a** exec'd CFG922 `load_bright` (A1) reproduces CFG922's stored A1 fluxscale median and 16/84 percentiles: abs < 1e-12.
- **K4b** exec'd CFG922 `Census` under A1 on the 318 eRASS1 positions reproduces `cfg922_census_A1.json` net_med, net_sup,
  sig_sup and coverage: max rel < 1e-9.

## MUTATE (run before the main score is read)
- **M1** (CFG652's own, data level, on A1c): (a) with the hot gas relabelled condensed reproduces (b)'s χ² to < 0.01, both
  footings.
- **M-INJ** (bites; census → models → score, end to end): plant a uniform fluxscale of −0.5 mag (×10^0.2 in mass; below the 1 mag
  cap) through the CFG924 census path with A1's masked and footprint steps off. Every M_cond and M_bcg must equal 10^0.2 × F
  (max rel < 1e-9); the x1 models on the planted masses for the 131 groups, scored verbatim, must reproduce CFG652's stored p02
  cell on both footings (χ²_a, χ²_b abs < 1e-6; same label).

## Budget and rules
One process at a time, one core (OMP/BLAS threads 1), nice 10, < 1 GB RSS, beside the live 1024³ job. Estimated 4–5 h (≈ 3.8 s
per model call: A1c ≤ 148 × 22, A1u ≤ 148 × 4, M-INJ 131 × 4, K3 6 × 22). Outputs written only in this directory and
`_external_data/cfg924_work`. Commits with explicit paths; history never rewritten.
