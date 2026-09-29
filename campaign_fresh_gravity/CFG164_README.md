# CFG164 — a measured gas prior for the KURVS discs from PHIBSS, and the decision-cell verdict marginalised over it

- **Criteria:** frozen in `CFG164_FROZEN_CRITERIA.md` (9a1d4bc9d), before any PHIBSS gas value was examined.
- **Data:** `data_assembly/kmos3d_phibss/phibss13_joined.csv`, from Tacconi et al. 2013. The 51 clean rows are what remain after removing:
  - the CO upper limits;
  - the three inconsistent-f_gas rows;
  - one secondary component.
- **Script:** `CFG164_gas_prior.py`, about 6 s. It runs CFG141's pipeline read-only and unmutated in every mode.
- **Runs:**
  - The main run passes all three controls (C1, C2, C3) and exits 0. Its headline is reported.
  - MUTATE=1 multiplies μ by 4. The probability of "lean rival" at s = 1 drops to 0.01, as required; exit 0.
  - MUTATE=2 multiplies μ by 0.25. The probability of "lean flat" drops to 0.00, as required; exit 0.
  - The two controls move the verdict in opposite directions.

## Bottom line

**NON-DIAGNOSTIC at Kretschmer's correction. The measured prior is uncertain by about a factor of 2 in μ, and that moves the verdict across both classes.**

- **The primary prior.** It uses the 17 PHIBSS rows matched in z and M*, with molecular gas only. The sample-median μ is 1.01, with a 16–84% range of 0.60–1.69.
  - 68% of the prior falls in the rival's window (μ 0.6–1.7) and 7% in flat's (2.1–3.7).
  - At the decision cell, s = 1 (Kretschmer): lean rival 0.55, lean flat 0.21, both within 2σ 0.24. The largest class is below the frozen 68% bar.
- **Class probabilities at s = 1 (Kretschmer) and s = 1.42–1.69 (Dalcanton & Stilp, fixed height, Price):**

  | prior | median μ (16–84%) | s = 1.00: lean flat / lean rival / both | s = 1.42–1.69: lean rival |
  |---|---|---|---|
  | **primary, molecular only (h = 0)** | **1.01 (0.60–1.69)** | **0.21 / 0.55 / 0.24** | **0.70–0.81** |
  | primary + HI = ½ molecular (h = 0.5) | 1.57 (0.91–2.57) | 0.47 / 0.24 / 0.25 | 0.58–0.68 |
  | primary + HI = molecular (h = 1) | 2.05 (1.19–3.47) | 0.59 / 0.11 / 0.19 | 0.37–0.52 |
  | variant M (μ–M* regression, extrapolated for 8 of 10 discs) | 1.30 (0.75–2.26) | 0.37 / 0.32 / 0.29 | 0.67–0.70 |
  | variant Z (declared (1+z)^2.5) | 1.31 (0.75–2.19) | 0.33 / 0.31 / 0.34 | 0.65–0.71 |
  | α_CO ULIRG-like (× 0.8/4.36) | 0.18 (0.11–0.31) | 0.00 / 1.00 / 0.00 | 0.01–0.06 (the rest "neither") |

  Under P2 (self-gravitating, s = 3) the class is mostly "neither": both readings under-predict.
- **The uncertainty in the prior, X.** Across the declared variants at s = 1, the probability of "lean rival" spans 0.11–1.00, and the median μ spans 0.18–2.05. The ULIRG-like α_CO is the extreme case; without it the median μ spans 1.0–2.05.
  - **The HI bracket alone,** from none to equal to the molecular, turns Kretschmer's cell from 0.55 lean rival into 0.59 lean flat.
  - **The mass matching matters.** Every clean PHIBSS row at z < 1.7 has log M* ≥ 10.40, and 8 of the 10 KURVS discs lie below that. The mass-scaled prior (slope −0.22 dex per dex; residual scatter 0.28 dex) raises the median μ from 1.01 to 1.30, and the verdict at s = 1 becomes an even split.
- **The KURVS-15 check.** The primary prior gives KURVS-15 a median μ of 1.00. Its dust limit (μ < 1.90 at the nominal calibration, from CFG163) excludes the 16% of the prior above 1.90. With h = 1 it would exclude 53%.

## Reading

- **With a measured, mass- and redshift-matched molecular prior,** the KURVS gas most likely lies in the rival's window. The decision cell then leans rival:
  - 55% under Kretschmer's correction;
  - 70–81% under the stronger published corrections.
- **That lean is not robust to the declared unknowns:**
  - HI comparable to the molecular gas reverses it at s = 1;
  - extrapolating the gas–mass relation to KURVS's lower masses splits it;
  - the α_CO bracket spans it.
- **The frozen headline is NON-DIAGNOSTIC.** The measured prior narrows the question, but it does not settle it.
- **What would settle it:**
  - gas measured for the KURVS discs themselves: CO or dust at a depth reaching μ ≈ 1 (CFG163 reached 1.9 for one disc);
  - an HI measurement, or a constraint on HI, at z ≈ 1.5.

## Selection differences (stated before the data)

- **Mass:** PHIBSS at z < 1.7 has log M* 10.40–11.23, against KURVS's 9.55–10.68. The prior likely under-states KURVS's gas; variant M sizes this.
- **Redshift:** 1.0–1.53 against 1.33–1.61. Another under-statement; variant Z sizes it.
- **CO detection:** removing the upper limits biases the prior toward gas-rich galaxies, an over-statement. It is not corrected.
- **Selection:** PHIBSS galaxies are SFR- or optically selected; KURVS discs are Hα-selected and rotation-supported. The net effect is unknown.

## Controls

- **C1:** with μ = 0.67 for every disc, the per-disc pipeline reproduces CFG160's decision cell (+0.1441 / −0.0060).
- **C2:** 51 clean rows, 17 matched, 38 at z < 1.7.
- **C3:** f_gas = Mmol/(Mmol + M*) holds exactly on the clean rows.
- **R0 (power):** the 16–84% width of the median μ is 0.45 dex, against the 0.53-dex separation of the break-evens at s = 1. So the prior's width alone is almost enough to span both windows.

## Untested (declared)

- HI, which is bracketed only;
- the selection difference beyond variants M and Z;
- α_CO beyond the bracket;
- the pressure prescription, used at its placed values only;
- PHIBSS-2 and Tacconi et al. 2018, which are not in the repo.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## After CFG166's independent re-derivation (appended 2026-09-29; the text above is unchanged)

- **Wording: the gas prior gives a weak lean toward the rival, uncertain by a factor of about 2 and reversible by HI; read with CFG165, it is weak evidence, not a detection.** CFG166 (ea66f9f17), the Opus chat's independent re-derivation, reproduces CFG164: 57 of 57 pass lines; counts 73/51/17/38; primary median μ 1.025 (0.604–1.719), 68% rival and 7.6% flat; at s = 1, lean flat 0.210, rival 0.540, both 0.245; the HI, mass-scaled (slope −0.219) and ULIRG rows. The largest class gap, 0.018, is Monte Carlo at N = 4000. (a) Extrapolating to lower mass: by the frozen rule the verdict is driven by the extrapolation, but only just (the P(lean rival) span is 0.202 against the 0.20 line). The mass slope is −0.22 ± 0.20 with a permutation p of 0.28, i.e. undetermined (checked here: −0.219 ± 0.196, p = 0.27). Carrying that uncertainty lowers lean rival from 0.54 to 0.34; a per-disc nearest-mass prior gives 0.52–0.55 (CFG166). (b) The redshift exponent implied by the data in the repo is 0.23 ± 0.52 (checked here, with the mass term, on all 51 clean rows), inconsistent with the 2.5 declared in Variant Z. The z ≈ 1.2 and z ≈ 2.2 PHIBSS samples are selected differently, so neither number is a clean evolution measure. The CO-detection bias cannot be tested, because no flagged row has z in the window; a bounding run moves lean rival to 0.43–0.62 (CFG166). (c) Window edges: the frozen stability line fails narrowly (5 of 105 near-frozen windows miss ±0.12, the worst by 0.199, all with z_hi = 2.5). There is no sign of tuning toward a class, and lean rival is the modal class in 97% of 317 windows (CFG166). (d) The marginalisation does not depend on its definition: bootstrap and lognormal draws differ by at most 0.013 (CFG166). CFG166's controls M1 and M3 did not bite, and are kept. Disclosed here: CFG164's HI rows (h = 0.5, 1) are not exact rescalings of the h = 0 draws, because one sequential random stream was used, so each HI row carries its own Monte Carlo noise (~0.01–0.02).

## Provenance correction: the KURVS outer velocity is a model value (appended 2026-09-29; the text above is unchanged)

- **The KURVS outer velocity this lane uses is the authors' fitted exponential-disc MODEL evaluated at R_max, not the last measured data point.** It is Table B1 col 3, read as `v_at_last_point_kms` through CFG140's loader.
- **How this was established.** The data chat's digitisation of the paper's figures (5e8617c81, `data_assembly/arxiv_tables/kurvs_rc_profiles/`) includes a control file (`kurvs_rc_control_vs_table.csv`). In it, the authors' model curve at R_max divided by sin i_SFR equals the tabulated velocity to about 1% for all ten discs (for example KURVS-3: 208.6 against 209.8 km/s; KURVS-15: 113.2 against 112.2). I checked this from the control file alone.
- **Where the record says otherwise.** Where this lane or CFG140 calls the velocity "measured" or "the velocity at the last observed point", read "the fitted model at R_max". The authors deprojected it with i_SFR; CFG140 uses i* only in its inclination-error term.
- **The a₀(z) numbers here are therefore model-velocity numbers.** The measured outer markers can differ from the model: an indicative, unreconciled probe found −15% to +10% for seven discs.
- **A re-run with the measured outer markers** is planned as a new frozen lane (proposed CFG189), after CFG184. The measured markers have not been read in the meantime.
