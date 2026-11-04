# LAM10_imf_single_slope: FROZEN CRITERIA, committed alone before any fit

κ = ½ FITTED and held fixed. Footings canonical a0 9.3603e-11 and alt a0 1.1312e-10 are graded apart and never pooled.
No ΛCDM input. The cold sector stays retired: no particle, no cold component and no halo is added. The IMF changes only
the stellar mass. Nothing here says the data favour the framework. Reinstates nothing. Not theory closed.

**Owner's yes, 2026-11-04:** "Yes, refit the IMF". The option was a new lane that fits one IMF slope per galaxy (a χ² profile
over the Γb grid, not a mixture), with the same K1 recovery check first, using the E-MILES files already on disk.

**No download.** The lane uses only LAM9's files: `_external_data/lam9_emiles_bi_basti/`, the template library built from
them (`_external_data/lam9_templates_2026_11_04/lam9_templates.npz`, from the manifest in LAM9) and LAM9's work files.
LAM9's committed files are imported or read, never edited.

## Question (LAM9's, unchanged)
- **Q1.** Does KU2's absolute residual at r_half shrink when M★ carries each galaxy's measured IMF?
- **Q2.** HX1 found that MaNGA ellipticals need B 3-4 inside R_e. Does that need go away?
- **Q3.** Does LAM6's h4 lean survive with IMF-corrected masses?

## What changes from LAM9, and only this
- **One slope at a time.** For each sum, each variant (A, B) and each of LAM9's 13 Γb values (0.3, 0.5, 0.8, 1.3, 1.5, 1.8,
  2.0, 2.3, 2.5, 2.8, 3.0, 3.3, 3.5), fit with only that slope's 84 templates (14 ages x 6 [M/H]). Ages, [M/H], masks m1-m7,
  the fixed kinematics, the polynomials and the regularisation stay as in LAM9's variant A or B.
  - **Step a.** That slope's templates; degree -1, mdegree 10, regul 0.
    χ²(Γb) = Σ over the variant's good pixels of ((sum - step-a model) / formal noise)², which is pPXF's chi2 x dof. The same
    pixels and noise are used for every slope, so the profile is comparable across Γb.
  - **Step b.** The sum and its noise are divided by step a's polynomial, and the noise is multiplied by sqrt(step a's
    chi2 / dof). Then degree -1, mdegree 0, regul 100, reg_dim (14, 6), reg_ord 2. This gives the weights w(Γb).
- **Γb_best.** j is the grid point with the lowest χ². A parabola through j and its two neighbours (in Γb value) gives the
  vertex, which is Γb_best.
  - At a grid edge (j = 0 or 12), Γb_best is the edge value. The parabola then uses the three end points, and the edge hits
    are counted and reported.
- **σ(Γb).** χ² is divided by s = χ²_min / dof_min. σ is the Δχ² = 1 half-width of the scaled parabola, 1 / sqrt(curvature).
  If the parabola is not convex, σ is undefined and counted.
- **α.** LAM9's α rule applied to step b's weights at the grid point j (the best single slope on the grid):
  α = Σ m M / Σ m L_r Υ_r(age, [M/H], Γb 1.3), with m = w / n_t.
  - α_KU2 and α_Tian use LAM9's reference factors, at the table point nearest that fit's light-weighted age and [M/H].
- **Beside, ungraded.** log α at the χ²-weighted mean Γb:
  - p(Γb) = exp(-(χ² - χ²_min) / (2 s)) and Γ̄b,χ = Σ p Γb / Σ p.
  - log α at Γ̄b,χ is linearly interpolated in Γb between the slopes' own step-b log α.
  - It never replaces the primary.

## Not blind
- **LAM9's K1 failed, and its cause is known.** On these 300 synthetics the mixture fit read log α +0.152 dex high (variant A;
  rms 0.216; Γb bias -0.177).
  - By Γb_in the bias was +0.29 to +0.34 dex at 0.8-1.5, +0.23 at 1.8, then falling to +0.03 at 3.0 and 0.00 at 3.3.
  - The cause: noise spread light to both grid ends, and α is U-shaped in Γb. In the 330 real donor fits, a median 35 % of the
    light sat at Γb 0.3 or 3.5.
- I know LAM9's code test, its donor fits (330 sums) and every LAM9 number.
- A software timing of single-slope pPXF fits on random templates (no data) took 0.41 s for step a and 0.02 s for step b.
- I have not run any single-slope fit on any sum or synthetic.

## The known risk, stated now
α is convex in Γb around Kroupa: α is 1.36, 1.00 and 1.12 at Γb 0.8, 1.3 and 1.8 (12 Gyr, [M/H] +0.06). So a symmetric scatter
of Γb_best still biases α high (Jensen's inequality). The single-slope fit removes the mixture spread, not that. K1 is
reported by Γb_in and by S/N third, as LAM9 did, so the reader can see where any bias sits.

## Sample (LAM9's, unchanged)
- LAM9's steps 1-5: KU2's 6056 galaxies, fibre gas-poor, Σ_Re ≥ 100, LAM4/LAM7 kinematic fit ok, and at least 70 % of the
  Na I 8190 and TiO2sdss feature pixels unmasked. That is 1586 galaxies (`../LAM9_imf_from_spectra/lam9_prepare.json`).
- Step 6 here: the variant-A profile fit returns all 13 slopes without error.

## K1: recovery, run first
- **Synthetics.** LAM9's 300 synthetic sums, exactly. They have the same donors, Γb_in and noise seeds. They are built the same
  way from LAM9's donor fits (`_external_data/lam9_work_2026_11_04/w/`), using LAM9's code.
- **Reproduction check.** Every synthetic's α_in must equal LAM9's recorded α_in (`lam9_k_rows.json`) to 1e-9 relative.
  Otherwise the lane is NO VERDICT (the code is wrong).
- **Fits.** Each synthetic is fitted with the frozen profile fit, in both variants.
- **The lines are unchanged.** K1 PASSES for a variant only if all four hold:
  - |median(Γb_best - Γb_in)| ≤ 0.15;
  - rms(Γb_best - Γb_in) ≤ 0.40;
  - |median(log α - log α_in)| ≤ 0.03 dex;
  - rms(log α - log α_in) ≤ 0.10 dex.
- **The gate is variant A.**
  - If A fails, every label is NOT MEASURABLE. The full fits are then not run, and the lane stops and reports.
  - If B fails and A passes, A's labels carry "(Na I robustness not tested)".
- **Reported for both variants:**
  - the four lines by Γb_in and by S/N third (LAM9's thirds);
  - edge hits and undefined-σ counts;
  - the median σ(Γb), and the rms of the pull (Γb_best - Γb_in) / σ;
  - the beside estimator's log α bias and rms.
- **K2, as in LAM9.** The first 100 synthetics are refitted (variant A profile) with h4 at the true value ± 0.03.
  b = median d log α / dh4. K2 PASSES if 0.69 ln(10) |b| IQR(h4_int) ≤ 0.01 ln. If it fails, Q3 is NOT MEASURABLE.

## If K1 passes: the full fits and the grade (LAM9's frozen text)
- Each of the 1586 sums gets one profile fit per variant.
- Everything downstream is LAM9's frozen text with this lane's α and Γb_best:
  - the α → M★ conversions (KU2: Chabrier reference; HX1: Kroupa reference, whole Mbar primary, 0.92 Mbar variant);
  - Q1 (R0, R1, f; lines ±0.15 ln and 0.5; labels IMF ABSORBS, OVERSHOOTS, DOESN'T, PARTLY, NO VERDICT);
  - Q2 (y0, y1 with HX1's rung error; NO NEED ON THIS SUBSET, then ABSORBS, OVERSHOOTS, DOESN'T, PARTLY);
  - Q3 (E0, E1, ΔE; DOESN'T if ΔE is inside ±0.01 ln, then ABSORBS, then DOESN'T if E1 excludes 0 with E0's sign);
  - C1-C4 (C4 is LAM9's, on the same template library: PASS), K3, the variant-B rule;
  - the M1 MUTATE twin (α shuffled within groups; outputs `lam10_grade_MUTATE.*`), and the rows;
  - the colour row, ungraded (α_KU2 by NSA u - r at 2.0);
  - bootstraps of 2000 draws, seed 20261105.
- These caveats stay with every label:
  - NSA's h units are unresolved.
  - [Na/Fe] is not modelled.
  - CaT sits in telluric water bands above z ≈ 0.05.
  - Tian+2026's Kroupa IMF was read only through a summariser.

## Compute
- Single thread per process, `nice -n 10`, under LAM9's job contract: SIGTERM or `compute_queue/YIELD` gives exit 75 at a
  boundary, `--resume` continues, and every line is fsync'd.
- The heavy queue's head of line is a 38.6 GB job waiting for memory. Queueing this lane above it would hold that job back
  for hours. So up to four shards run directly, each under 1 GB, as the standing rule allows small jobs. Each fit is done
  exactly once, and an execution note records it.
- **Estimate.** About 13 x (0.4-0.7 s) per variant, so about 15-25 s per sum for both variants.
  - K1 (300 synthetics, plus K2 on 100) takes about 30-45 min on four shards.
  - The full fits take about 2-3 h on four shards.

## Expectations on record (priors, before any fit)
| | prior |
|---|---|
| K1 passes, variant A | 30 %. Jensen's bias remains, and the α bias lines are tight |
| Edge hits under 10 % of K1 synthetics | 70 % |
| If K1 passes: Q1 IMF DOESN'T on both footings | 85 % |

κ = ½ FITTED; not theory closed.
