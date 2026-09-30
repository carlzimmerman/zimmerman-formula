# AMENDMENT 18 — DRAFT, NOT FILED (written 2026-09-30; filing needs the owner's explicit go)

This is a draft. `PREREGISTRATION_DR4.md` and every `*_HASH.txt` are untouched. If the owner approves, the text below the line is appended verbatim (append-only) after Amendment 17, with a new `AMENDMENT18_HASH.txt`.

**Why now.** The DR3 dry run (`dr4_ready_1/WP2_GAMMA_SPREAD_FROZEN.md`, question frozen in 01bc48e32, results in 72f9a7ed4, code-path tests only, Amendment 7(e)) rebuilt the same primary DR3 base with ten seed sets of the frozen builder's three Monte Carlo streams, at the real setting N_SHIFT = 30:
- the stage-E shifted realisations;
- the r_chance leave-10%-out folds;
- the stage-G velocity-error Monte Carlo.

Results:
- **Final pairs:** about 2.6% of the final pairs flip between builds.
- **γ̂ build-to-build SD:** 0.30 σ_fit on the canonical footing (0.0164 against σ_fit 0.0554) and 0.34 σ_fit on the alt footing. The build-only part is 0.24 / 0.32 σ_fit once the fit's own seed noise is removed.

The frozen builder fixes its seeds, so the primary DR4 build is deterministic. But the particular seed choice carries a noise term that σ_tot = √(σ_fit² + 0.02²) does not include. Its size at DR4's N (~30,000 pairs) is not measured, so it may be relatively larger or smaller than at DR3's ~6,200. This draft adds a reported measurement and a flag. It does not change the estimator, σ_tot or any decision row.

---

> ### 🚨 AMENDMENT 18 — 2026-09-30, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **THIS AMENDMENT ADDS A REPORTED BUILD-SEED SENSITIVITY TO THE DR4 WIDE-BINARY RESULT. IT CHANGES NO CUT VALUE, THRESHOLD, ESTIMATOR SETTING, σ_tot DEFINITION OR DECISION ROW.** Arms A, B and C, the estimator, the frozen seeds of the primary build and every frozen number are untouched.
> **κ = ½ FITTED, NOT DERIVED.**
>
> **What was found.** On DR3 (a code-path test; Amendment 7(e)), rebuilding the same primary base with ten seed sets of the builder's three Monte Carlo streams (N_SHIFT = 30) gave these results:
> - about 2.6% of the final pairs flip between builds;
> - γ̂'s build-to-build SD is 0.30 σ_fit (canonical) and 0.34 σ_fit (alt);
> - the build-only part is 0.24 / 0.32 σ_fit.
>
> Source: `prep_2026/gaia_dr4_prep/dr4_ready_1/WP2_GAMMA_SPREAD_FROZEN.md` and `wp2_gamma_spread_full_dr3.{py,out,json}`, commit 72f9a7ed4.
>
> **The amendment.**
>
> **(a) The primary is unchanged.** The DR4 primary γ̂ is the single build with the builder's frozen seeds, exactly as before.
>
> **(b) A reported build-seed spread (σ_build).** Alongside the primary, the full DR4 build is repeated with K = 10 further seed sets for the three Monte Carlo streams, with everything else frozen.
> - The seed sets are listed in the fetch manifest before the data are opened: the integers 1 to 10 added to each stream's frozen base seed.
> - The SD of γ̂ across the K + 1 builds is reported as σ_build, on both footings, with the fit-only control (the primary catalogue refitted with K fit seeds) so that the build-only part is separated.
> - σ_build is REPORTED ONLY. It does not enter σ_tot and does not move any decision edge.
>
> **(c) A seed-sensitivity flag.** If the primary γ̂ lies within max(σ_build, 0.3 σ_fit) of any decision edge in §1.5 or Amendments 12–14, the verdict is reported with the label **"seed-sensitive"**. The label states how many of the K + 1 builds fall on each side of that edge. The primary's verdict is the one recorded; the label is added, never substituted.
>
> **(d) Against interest.**
> - The flag can attach a caveat to a verdict favourable to the framework as well as to an unfavourable one.
> - Reporting σ_build without adding it to σ_tot keeps the frozen decision thresholds. If σ_build turns out comparable to σ_fit at DR4's N, the frozen σ_tot understates the total error, and the "seed-sensitive" label is the only protection. This is stated here, before the data exist.
> - Running K = 10 extra full DR4 builds costs compute time on release day. If that is not feasible within the release-day schedule, the number actually run is recorded, and at least K = 3 are required for the label.
>
> **Untouched:** the estimator; the cut table; the error model and σ_tot; the strictness ladder; the frozen N = 30,000; both a₀ footings; Arms A, B and C; Amendments 14–17's decision rows and cut choices; the primary build's frozen seeds. κ = ½ remains fitted.
>
> **Provenance.** `prep_2026/gaia_dr4_prep/AMENDMENT18_DRAFT_NOT_FILED.md` (this draft); `dr4_ready_1/WP2_GAMMA_SPREAD_FROZEN.md` and `wp2_gamma_spread_full_dr3.*` (72f9a7ed4).

---

**Implementation note (not part of the amendment text).** The WP5 driver needs a `--seed-offset k` option that adds k to each of the three streams' frozen seeds, gives each build its own correlation-cache path (the overwrite hazard in PLAN.md), and writes the K builds' γ̂ into the manifest. That is new code only, with a MUTATE control in which K builds on identical seeds must return σ_build = 0. It should be built whether or not this amendment is filed.
