# LAM10_imf_single_slope: K1 passes, and the frozen labels are Q1 IMF PARTLY, Q2 NO VERDICT, Q3 NO VERDICT on both footings. On real sums, 60 % of the fits sit at the grid's top-light edge (Γb 0.3), where α ≈ 4.7 comes from remnants. Γb falls with σ and [M/H], and the IMF-corrected ellipticals come out sub-Newtonian. So the α behind these labels is not a credible IMF measurement

| step | commit |
|---|---|
| Criteria, frozen first and committed alone | `e70770e272` |
| Scripts, before any fit | `009f39ec2f` |
| K1 and the grader, before the full fits | `9e76d668b1` |

κ = ½ FITTED; not theory closed. Footings canonical and alt are never pooled. The cold sector stays retired. Nothing here
says the data favour the framework. No download: LAM9's E-MILES files only.

## Labels (as frozen; variant B agrees on every one)
| | canonical | alt |
|---|---|---|
| **Q1** KU2's absolute r_half residual | **IMF PARTLY**: R0 +1.295 [1.278, 1.318] → R1 +0.292 [0.261, 0.325] ln, f 0.774 [0.748, 0.798] | **IMF PARTLY**: +1.239 → +0.262, f 0.788 [0.762, 0.810] |
| **Q2** HX1's MaNGA need, 395 Tian rows in Q2-Q4 | **NO VERDICT**: y0 +0.574 ± 0.092 (B 3.75); after α the median B_need is -1.21, so y1 is undefined | **NO VERDICT**: y0 +0.518 ± 0.093 (B 3.30); median B_need -1.05 |
| **Q3** LAM6's h4 lean at fixed IMF | **NO VERDICT**: E0 +0.014 [-0.022, +0.055], E1 -0.105 [-0.164, -0.045], ΔE -0.119 [-0.162, -0.079] | **NO VERDICT**: E0 +0.018, E1 -0.099 [-0.158, -0.040], ΔE -0.117 |

- **M1 MUTATE** (α shuffled within groups): ΔE intervals [-0.075, +0.002] and [-0.073, +0.002] include 0, so it PASSES on
  both footings.
- **Checks.**
  - C1 passes (N 1586) and C2 passes.
  - C3 passes: HX1's MaNGA medians are reproduced exactly, and α = 1 gives back R0.
  - C4 passes.
  - K2 passes (0.0006 ln).
- **K3, reported:** Spearman(Γb, log Σ_Re) is **-0.397** (p 6e-61). The literature trend is positive.
- **These caveats stay with every label:**
  - NSA's h units are unresolved.
  - [Na/Fe] is not modelled.
  - CaT sits in telluric water bands above z ≈ 0.05.
  - Tian's Kroupa IMF was read only through a summariser.
  - New here: the fits pile up at the top-light edge (below).

## K1: recovery (the gate), on LAM9's 300 synthetics
LAM9's α_in was reproduced exactly.

| | variant A | variant B | line |
|---|---|---|---|
| Γb bias, rms | -0.017, 0.177 | -0.016, 0.175 | 0.15, 0.40 |
| log α bias, rms | +0.0009, 0.076 dex | +0.0011, 0.075 | 0.03, 0.10 |
| K1 | **PASS** | **PASS** | |

- **By Γb_in** (variant A), the log α bias is between 0.000 and +0.004 at every input. The rms is 0.20 dex at 0.8, 0.12 at
  1.3 and 0.03-0.06 elsewhere.
- **By S/N third,** the log α rms is 0.102, 0.061 and 0.056.
- There are 2 edge hits. The median σ(Γb) is 0.15 and the pull rms is 0.92.
- The beside estimator (ungraded) has a bias of +0.005 and an rms of 0.062.
- The single-slope fit removes LAM9's mixture bias. Jensen's bias, the risk stated in advance, did not show.

## Why the labels can't be read as an IMF result
- **The synthetics are built from the same templates as the fit.** So K1 tests noise and the method, not whether E-MILES base
  models describe real MaNGA spectra.
- **On real sums, the profile runs to the grid's top-light edge.**
  - 947 of 1586 galaxies (60 %) have their χ² minimum at Γb 0.3. The median Γb_best is 0.30, with 16-84 % at 0.30-0.92.
  - At Γb 0.3, α is about 4.7, almost all from stellar remnants. The median α_KU2 is 4.76.
- **Γb_best runs against the literature's IMF trends.** It falls with σ (-0.40), [M/H] (-0.57), age and M★. The literature
  finds bottom-heavier IMFs in more massive, metal-rich early types.
  - The pattern is what template mismatch would give, for example from [α/Fe] or [Na/Fe], which the base models fix. Most
    χ² pixels are blue, so the fit can trade the IMF slope for abundance mismatches.
- **Q2 shows the α is too large to be physical.**
  - With these α, the median B_need of the ellipticals falls to -1.2 / -1.05. Their IMF-corrected stars alone would give a
    larger dispersion than is observed (sub-Newtonian).
  - HX1's L-ORDER cannot be recomputed for the same reason: a rung is SUB-NEWTONIAN.
- **Q1's PARTLY follows from the same large α.** The h70 row would read OVERSHOOTS (R1 -0.35 / -0.36 ln).
- **Q3's E1 turns negative** because α tracks h4 within groups (Spearman of Γb with h4 -0.26). The lines give NO VERDICT, and
  M1 passes.
- **Bottom line:** the frozen labels stand as computed. This lane does not show that a spectroscopic IMF absorbs KU2's
  residual or HX1's need. What it shows is that a single-slope E-MILES base-model fit of these sums does not return a
  physically consistent IMF.

## Rows (reported, not graded)
- **Colour row** (variant A; B matches to 0.01). Red, u - r > 2.0 (1490): α_KU2 4.84 [4.76, 4.89], R1 - R0 -1.04 ln. Blue
  (96): α_KU2 1.42 [1.35, 1.45], R1 - R0 -0.24 ln (canonical; alt -1.01 / -0.23). The red-blue split is the top-light pile-up
  again: the blue galaxies mostly avoid the edge.
- **Q1 by class.** Slow +1.400 → +0.347 and fast +1.276 → +0.287 (canonical). KU2's slow-minus-fast D goes from +0.045 to
  +0.168.
- **Early minus late D** (gas-poor 1586 against gas-bearing 1180, which keep α = 1): -0.024 before, -0.83 after (canonical).
- **Q3 with log α as a covariate:** E +0.019 / +0.022.
- **By z third,** the median Γb_best is 0.30, 0.43 and 0.30, and the median α_KU2 is 4.96, 2.79 and 4.91.

## Run notes
- **The fits.** 1586 sums, one profile per variant, 0 failures. They ran as four single-thread shards with `nice -n 10`,
  outside `compute_queue`.
- **Memory, corrected.** The shards held **4.5-5.7 GB RSS each, about 21 GB in all**. Their physical footprint was under
  1 GB, so the plan's "under 1 GB" was wrong for the queue.
- **The queue.** Running outside it, the shards kept its head (`L1_calib_512`, 38.6 GB) from starting for about 1 h. The
  owner chose "Let LAM10 finish".
- **A grader dry run** with α permuted, on 961 sums, revealed the Γb pile-up before the grade. Nothing was changed after it.

`EXECUTION_NOTE.md` has the details.

## Files
- **Criteria and run record:** `FROZEN_CRITERIA.md`, `EXECUTION_NOTE.md`.
- **Fit code:** `lam10_core.py` (the profile fit), `lam10_k.py` (K1 and K2: `lam10_k.out`, `.json`, `_rows.json`) and
  `lam10_fit.py` (`lam10_fits.json`, both variants).
- **Grade:** `lam10_grade.py`, with `lam10_grade.out` / `.json`, `lam10_grade_B.out` / `.json` and
  `lam10_grade_MUTATE.out` / `.json`.

κ = ½ FITTED; not theory closed.
