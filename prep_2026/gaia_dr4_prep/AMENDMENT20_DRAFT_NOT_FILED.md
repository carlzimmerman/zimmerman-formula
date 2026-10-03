> ### 🚨 AMENDMENT 20 — 2026-10-03, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **THIS AMENDMENT ADDS A MEASURABILITY CONDITION TO THE ANISOTROPY FALSIFIER. IT CHANGES NO CUT, THRESHOLD, ESTIMATOR SETTING, GRID, σ_tot, DECISION ROW, SEED OR ARM.**
> **κ = ½ FITTED, NOT DERIVED.**
>
> **(a) The defect.** In the 2026-10-03 offline dry run on DR3 (`dr4_ready_1/DRY_RUN_2026-10-03.md`), every proj-PARALLEL fit (both builds, both footings) returned γ̂ = 0.9000, the lower edge of the frozen estimator grid `GRID = np.arange(0.90, 1.5001, 0.0025)`. A fit on a grid edge is boundary-pinned: the true minimum may lie outside the grid, and its σ_fit is not a measurement. The split γ_perp − γ_par built from it (+0.30 to +0.35, printed as about +4σ) is therefore not a measurement either.
>
> **(b) The rule.** For each a₀ footing separately, the anisotropy split is **MEASURABLE** only if neither the proj-PARALLEL nor the proj-PERPENDICULAR fit returns γ̂ equal to either edge of the frozen grid (0.90 or the grid's top value).
> - **Measurable:** the anisotropy-sign falsifier of Amendment 2(f), as preserved by 3(c), reaffirmed by 8(f) and arm-updated by 11(d2), stands exactly as registered and is reported as registered.
> - **Not measurable:** the split for that footing is **NOT QUOTED**. It cannot falsify, support or be read in any direction. The report states which fit sat on which edge.
> - The condition is evaluated mechanically from the pipeline's printed fits, before the split is read (`dr4_ready_1/amdt14_distances.py` prints it).
>
> **(c) Against interest.** A boundary-pinned PARALLEL fit at the floor inflates the split in the pre-declared (perpendicular-larger) direction, so this rule removes an artifact that favours the framework. But if the PERPENDICULAR fit pins at the floor, a genuine opposite-sense anisotropy could be present and cannot be scored: in that case this rule forfeits a possible kill. That cost is accepted and stated here before the data.
>
> **(d) What it does not do.** It does not widen or move the grid, change the estimator, or add any substitute statistic. A pinned split is not re-fit on another grid after the data exist.
>
> **Untouched:** the estimator and its grid; the cut table; the error model and σ_tot; the strictness ladder; the frozen N = 30,000; both a₀ footings; Arms A, B and C; Amendments 2(f), 3(c), 8(f) and 11(d2) whenever the split is measurable; Amendments 10–19; the seeds. κ = ½ remains fitted.
>
> **Provenance.**
> - `dr4_ready_1/DRY_RUN_2026-10-03.md` and commit 6e515fd8f (the dry run); 48f6e0e14 (the owner's first, unconditional note in the checklist, superseded by this amendment)
> - `dr4_ready_1/amdt14_distances.py` (implements the condition)
> - Filed on the owner's explicit instruction, 2026-10-03, choosing the conditional form over an unconditional withdrawal of the falsifier.
>
