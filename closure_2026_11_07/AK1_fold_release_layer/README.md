# AK1: fold release layer vs the outside critical-layer claim

**Label (frozen, CRITERIA.md c61447452a): NO VERDICT (check failed).** Adopts nothing. Kappa = 1/2 FITTED; not theory
closed. Footings are graded separately, never pooled.

Criteria:
- CRITERIA.md: origin c61447452a (local 8ed1798939).
- Addendum A1, exponents reported only: 858f4ea326.
- Addendum A2, filed after the result and disclosed: 7291797cb1.

Every number below is from GRADE.json and grade.out, made by grade.py.

## Claim tested

- Release speed: v_k = 2c(a0 L*/c^2)^(1/3) = 577.6 / 571.3 km/s.
- Critical layer: lambda_crit = (L*^2 c^2 / a0)^(1/3).
- The machinery is the certified planar fold machinery: FS2 scheme S, with core ak1_core.c = FS2's core plus snapshots
  and run-on after the fold.

## Checks

| check | result |
|---|---|
| KA, 960 rung files vs FS2 (t_reg, t_fold, t_fold_all, J_min, steps) | PASS, 0 mismatches |
| MUTATE-V2, planted spread (v_post) | PASS: 576.9 / 570.5 km/s |
| MUTATE-0, null row | PASS: V 119 / 128, v_post 0.14 / 0.05 km/s |
| K-visc, 40 rows at (c_Q, c_L) = (2, 1) | PASS, 0 fails |
| **MUTATE-V, planted stream v0 = 577.6/w (power on V)** | **FAIL** |

MUTATE-V failed because, at t_max = 6, the planted row never reached t_reg; the snapshots never fired.

Addendum A2 (post-result, never the label) reran that one row with t_max = 60:
- It regularizes at t_reg = 8.016 (N 4000 and N 8000 agree to 3e-5).
- V reads 317.7 / 309.2 km/s at the two snapshots, outside 500-650. MUTATE-V **fails under A2 too**.
- Run-wide max |v| was 589.8 km/s. By the time the fold regularizes, the stream has slowed to about 318 km/s.

So V, measured after the fold, cannot carry a planted infall speed. That is a real power gap, not a code fault, and
the frozen NO VERDICT stands.

## What the graded rows read

Graded rows: AC2q clock-only and phantom at the lower L*, 20 + 20 per footing; N 8000; Delta 0.5. All converged.

| footing, kind | v_post (km/s) | V (km/s) | FWHM (pc) | W (pc) | R_delta = FWHM / lambda_crit |
|---|---|---|---|---|---|
| canonical, clock-only | 0.045-0.050 | 128-139 | 1e-5 - 4e-4 | 0.024-0.54 | 5e-10 - 2e-8 |
| canonical, phantom | 0.024-0.157 | 121-139 | 0.0018-0.0064 | 2.5-4.3 | 8e-8 - 3e-7 |
| alt, clock-only | 0.050-0.056 | 128-139 | 1e-5 - 4e-4 | 0.028-0.63 | 5e-10 - 2e-8 |
| alt, phantom | 0.024-0.157 | 122-139 | 0.0012-0.0072 | 2.6-4.3 | 5e-8 - 3e-7 |

- 160 converged readings fall outside the frozen bands. The refutation would rest on v_post, whose power check
  (MUTATE-V2) passes. With every check passing, the frozen line logic would read REFUTED. It does not, because
  MUTATE-V failed: **REFUTED is not the label.**
- **Speed form.** Of the three named forms, the speed follows the well depth.
  - V tracks the infall speed: d ln V / d ln v_f = 1.000 (clock-only) and 0.95 (phantom).
  - L* x2 leaves V unchanged (ratio 1.000; the identity predicts 1.260).
  - It is neither 2 a0 lambda_crit nor stored stiffness.
- **Width.**
  - The collapsed layer W scales linearly with L*: x2 ratio 2.00 (identity 1.587); 90 pc ratio 4.0-4.2.
  - FWHM is 6.5-9.3 orders below lambda_crit.
  - Against the brief's 2.09 / 2.25 kpc, FWHM is 2e-7 to 3e-6 of it.

## Exponents (A1, reported only, bootstrap 2000, 16-84 %)

| footing | alpha_L (FWHM) | alpha_L (W) | alpha_v | alpha_M |
|---|---|---|---|---|
| canonical | 0.94 [0.93, 1.02] | 1.008 [1.004, 1.009] | 0.56 [-1.23, 2.19] | not computed: blend region visited (min Pi/ref 9.1e-5) |
| alt | 0.94 [0.93, 0.96] | 1.014 [1.005, 1.015] | -0.08 [-1.52, 1.45] | not computed: blend region visited (min Pi/ref 1.0e-4) |

- alpha_L is about 1 on both footings: regime I's row, not the 2/3 of regimes II and III.
- alpha_v is unconstrained: its CI spans all three regimes.
- alpha_M is not computed, because the phantom rows drive Pi to about 1e-4 of Pi0.

## Disclosures

1. **lambda_crit.** The formula gives 22.53 / 24.04 kpc, not the brief's 2.09 / 2.25 kpc (a factor-10 slip). Only the
   formula values reproduce 577.6 / 571.3 km/s via 4 a0 lambda_crit.
2. **No D.P = 0 crossing.** In the planar reduction D.P = Pic/J with Pic constant per label, so D.P never changes sign
   along a label. There is no dynamical D.P = 0 crossing.
3. **Non-relativistic.** Max (1 - X/X_bg) = 2.4e-7. Regime III, which needs Q - 1 = O(1), cannot appear. Any
   reading is "within the certified non-relativistic fold reduction".
4. **Resolution.** L* is resolved everywhere (0.22-5.7 pc cells at N 8000). lambda_crit/2 fits in the stream only on
   the 73 / 91 / 156 kpc hosts, which are the only rows where R_delta is graded.
5. **Not graded.** M234 / M490 are moving-Sun runs, not fold runs.
6. **One code-check run** (clock-only row 1, N 4000) came before A1.
7. **A2** was filed after the frozen grade. It cannot change the label, and it also failed.

## Reproduce (from the repo root; checkpointed, resumes)

    nice -n 15 python3 closure_2026_11_07/AK1_fold_release_layer/ak1.py run --workers 4
    nice -n 15 python3 closure_2026_11_07/AK1_fold_release_layer/ak1.py a2 --workers 2
    python3 closure_2026_11_07/AK1_fold_release_layer/grade.py > closure_2026_11_07/AK1_fold_release_layer/grade.out
