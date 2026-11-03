# LE1_lensing_estimator_audit: FROZEN CRITERIA, committed alone before any script or number

**Not blind.** Read before freezing: RQ3_acceptance_v2 (A30 law +9.27 canonical, +6.52 alt; keys B4-B18 on `results/law.out`), NP1 (A30 +8.45 / +6.75; CX1 lensing line z +1.69 L3 canonical; oracle note that RQ3's ΔΣ forward model is not CX1's g = 4GΔΣ), CX1's `cx1_rows.py`, CRG1's `crg1_lens.py` and SPEC §5, the key chain (LW1 → DR1 tail → SL1 → NF1 → X73/X30 → X2/F1 projector), LF1, DA1 (D2: n(z) bound, B < 1), BL1/S2. κ = ½ FITTED. Cold sector retired; nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

## Question
Is the lensing failure (A30, the eRASS1 × KiDS outskirt keys) a property of the data or of the estimator?

LE1 reads and reports. **No existing grader is edited.** Graders are imported or exec'd read-only, or their text is copied into this lane's own cache with a recorded string swap. A defect found is reported for the owner, never fixed in place.

## Graders audited
- **G1 = RQ3 A30.** CRG1 `crg1_lens` as RQ3's `rows_lens` calls it: KiDS-1000 bright isolated lenses, Fig-3 mass bins 1-4 × 15 radii, native conversion, stack over the lens mass distribution, ΔΣ by CRG1's `Stencil` from M_lens = M_B ν, two-halo template with b ≥ 0 per bin, full covariance, χ² on 56 dof, Z = (χ² − 56)/√112.
- **G2 = 15-key cluster grader.** RQ3's `run_keys` path (LW1's), keys B4-B18, worst |Z| over h 0.672/0.686 and f★ 0.034/0.0615, |Z| ≤ 2. Model side: M_lens = r² g/G from the candidate, F1/X2 projector (`project_floor`, `offset_floor`, `dsig_from_sig`, `at_bins`), catalogue miscentring, reduced-shear factor, ratio to the C* reference vector.
- **G3 = CX1 lensing line.** `cx1_rows.systems` + `mc`, via NP1's `np1_core.cx_rows`: g_obs = 4 G ΔΣ at R ≤ 0.3 Mpc, point-mass baryons M★ + 0.25 M★, diagonal errors; statistic = NP1's weighted mean of log10(g_obs / g_model), z = mean/se, |z| ≤ 2.
- S2/BL1 (Brouwer+21 RAR, 4GΔΣ) is described from its text only, not rerun.

## Step 1: estimator table
Written from the code for each grader: projection and phantom mass, miscentring, two-halo, boost/dilution, n(z) and Σ_crit, stacking, aperture and R500 source, covariance, statistic.

## Step 2: controls and known answers, run and read before any real result
| ID | Test | Pass line |
|---|---|---|
| KA1a | G1 `Stencil.dsig` on SIS (tail linear), point mass (tail const), NFW c = 8, M200 = 1e12 (tail linear), at G1's native radii, against closed forms | max \|ratio − 1\| ≤ 0.01 |
| KA1b | G1 self-recovery: mock Y = stack(law table) + Σ b_true T0, b_true = (0, 0, 0.15, 0.07), noise-free, through G1's `fit` | χ² ≤ 1e-6, max \|b − b_true\| ≤ 1e-4 |
| KA1c | G1 χ² calibration: 300 noisy mocks from C^n (seed 20261103) | mean χ² in [52, 60] |
| KA1d | G1 covariance assembly: 3600 cells filled once, symmetric to 1e-10 relative, positive definite; the four bins' radii identical to 1e-6 relative | all hold |
| KA1e | G1 covariance against data: χ² of the cross ESD (ESD_x / bias, raw C, no fit) on 60 points and on the 32 points R ≤ 0.31 | 60: [27.1, 92.9]; 32: [8.0, 56.0] (dof ± 3√(2 dof)) |
| KA2a | G2 projector chain (`project_floor` → `dsig_from_sig` → `at_bins`, no offset) on SIS, NFW (c 4, M200 1e14 M☉, truncated at the grid edge as the grader is), point-mass-like compact Plummer (a 0.01 Mpc), against closed forms at the 8 RC bins | max \|ratio − 1\| ≤ 0.01, all 8 bins |
| KA2b | G2 `offset_floor` on SIS at d = 0.05, 0.2 Mpc against an independent 2-D average (direct quadrature in φ of Σ_SIS at the offset radius, 2000 points, then the same `dsig_from_sig`/`at_bins`) | max \|ratio − 1\| ≤ 0.01 |
| KA2c | G2 replica: this lane's swap hook with no swap reproduces the base key Z | max \|dZ\| ≤ 1e-9 |
| KA3a | G3 conversion: the law's own lensing profile on CX1's baryons per bin (canonical, alt); exact ΔΣ by G1's `Stencil` (if KA1a passes); 4GΔΣ / g_law at CX1's radii | inverse-variance mean \|log10 ratio\| ≤ 0.02 dex over the L rows |
| KA3b | G3 SIS: 4GΔΣ_SIS / g_SIS | \|ratio − 1\| ≤ 1e-3 |
| R1 | Reproduce RQ3 A30: law canonical +9.27 (χ² 154.1), alt +6.52 (125.0); NP1 real L3 +8.45 (145.5), +6.75 (127.5) | \|dZ\| ≤ 0.01 |
| R2 | Reproduce RQ3's law keys: every Z in `RQ3_acceptance_v2/cache_keys/law_{g005_f034,g005_f0615}/keys.json`, R1\|c0\|{canonical, alt}, both h | max \|dZ\| ≤ 1e-6; and B4-B18 worst Z equal to `results/law.json` to 1e-6 |
| R3 | Reproduce NP1's G3 lensing line for the real L3 rule: z +1.686 canonical, +0.918 alt | \|dz\| ≤ 0.01 |
| MUT | Model ΔΣ (or model g) × 2 in each grader | G1 χ² rises by ≥ 50; G2 ≥ 5 of 15 keys change label or every \|dZ\| ≥ 1; G3 z moves by ≥ log10(2)/se |

If R1, R2 or R3 fails, the lane stops for that grader and the label is UNDETERMINED for it.

## Step 3: real grades (law, NP1 real L3 frozen rule, read-only; Newton as a reference), both footings, never pooled
Through every grader that passes its known answers:
- G1 base, and a swap ladder, one choice at a time, then all CX1-like together:
  - S1 radii R ≤ 0.31 only (CRG1's IDX_PRIM), two-halo kept, dof = 4 × n − 4;
  - S2 no two-halo term (b = 0), dof 60;
  - S3 CX1's baryons (point mass M★ + 0.25 M★, gas share 0.2), no CGM, no hot gas;
  - S4 diagonal covariance;
  - S5 no native conversion (raw R, Y, C, lens masses);
  - S6 one mass per bin (weighted mean of 10^lm_i) instead of the stack;
  - S7 all of S1-S6.
  - A1: G1's own forward model graded with G3's statistic (weighted mean log residual, diagonal σ, R ≤ 0.31): isolates projection versus the 4GΔΣ conversion.
- G2 base and model-side swaps: K1 no miscentring (offset 0), K2 no reduced-shear factor. Data-side swaps (boost B = 1, bin n(z)) need X7's re-measurement or the 17 GB KiDS catalogue: NOT COMPUTABLE here; DA1's numbers are quoted as record, labelled.
- G3 base and, if KA3a fails, G3 with the model mapped to 4GΔΣ_model (the number the defect moves).
- Every chi² row gives Z = (χ² − dof)/√(2 dof).

## Verdict (one label for the lane; per-grader notes beside it)
Precedence top to bottom.
1. **UNDETERMINED**: R1, R2 or R3 fails, or a known answer needed for the graded comparison is NOT COMPUTABLE.
2. **ESTIMATOR DEFECT FOUND**: some grader fails a KA beyond its line, and replacing the failing piece by the KA-passing alternative moves a graded number (A30 Z, a key Z, the G3 z) of the law or of NP1 by ≥ 1.0. Named, with that number. A KA failure that moves graded numbers by < 1.0 is reported as an immaterial defect and does not set the label.
3. **ESTIMATORS AGREE, FAILURE IS IN THE DATA**: all KAs pass; for each of the law and NP1 L3, G1 and G3 give the same PASS/FAIL label; and no single swap S1-S6 moves the law's A30 Z across the line (|Z| ≤ 2) on either footing.
4. **ESTIMATORS DISAGREE, NO DEFECT**: all KAs pass, but G1 and G3 differ in label for the law or NP1, or a single legitimate swap S1-S6 brings the law's A30 within |Z| ≤ 2. The spread is reported as a systematic, with the swap that carries it.

"Carries A30": the swap(s) S1-S6 whose single application brings |Z| ≤ 2, or, if none does, the swap with the largest |ΔZ|, reported for both footings.

## Run rules
`PYTHONHASHSEED=0 nice -n 10 python3 -I le1.py <mode>` (key-chain subprocesses `python3 -B`), thread env vars 1, RSS < 1 GB, nothing large written. No downloads; missing input = NOT COMPUTABLE. Outputs named by mode: `le1_<mode>.{json,out}`. Key-chain caches in `cache_keys/` are not committed (they print local paths); their keys JSON values are carried into `le1_<mode>.json`. Amendments in `AMENDMENT_A*.md`, labelled pre- or post-result. κ = ½ FITTED. Not theory closed.
