# CFG221 — FROZEN CRITERIA: the decision rule for the pooled z > 3.5 two-sided test, and its operating characteristics on mocks

Written 2026-09-30 and committed BEFORE any new disc value (GN20, REBELS-25, class B, Corpus Z1, the Dessauges-Zavadsky+20 / Jones+21 tables) is read, and before the rule is run on anything. **κ = ½ is FITTED, not derived.** Both footings and both kernels are carried. Author decompositions, not a direct a₀ measurement. Nothing here says the data favour a framework. The rule is fixed here so that it cannot be tuned after the values are seen; it is a rule for a verdict, not a result.

## Aim
Fix (1) which discs enter, (2) how the shared gas calibration is treated, (3) what counts as separating the a₀(z) laws, and (4) the rule's operating characteristics (its false-separation rate and its power, as functions of N and of the true calibration offset) on mocks, so that a later analysis of real discs is a lookup, not a choice.

## Sample rule (class A, from the data chat's list 2ad335eea)
A disc enters only if it has all of: (i) a rotation curve or V at a stated radius with the pressure treatment stated; (ii) a stellar mass from SED, not from the dynamical fit; (iii) a gas mass from a measured tracer with a stated conversion (dust, CO or [CII]) that is a DETECTION. Dust upper limits, discs with a circular gas mass (gas set by M_dyn − M★) and every class-B disc are **never entered as values**; upper limits are reported as one-sided lower bounds on δ (an upper limit on the gas caps g_bar, and δ falls as g_bar rises). CRISTAL-09 and -15 stay excluded as frozen in CFG213. **The radius is the outermost radius at which the velocity is MEASURED** (the outermost data marker, not a model extrapolation); R_e is reported beside.

## Per-disc statistic
g_obs = V²/R at that radius; g_bar from the independent baryon normalisation, g_bar = (M★ + M_gas) × (the baryon curve's g per unit mass at R; the fit's baryon curve shape, or a thin exponential disc if none is given); D = g_obs/g_bar; δ_L = log₁₀[D / ν(g_bar / a₀,L(z))] for the laws FLAT (a₀), H(z) (a₀ E(z), Ω_m 0.315), HORIZON and LCDM-NATIVE (Z1, 1138d817f, read-only). **FLAT vs H(z) is the primary pair; the other five pairs are reported extras, each its own test, never pooled.** Four cells: ν_mono and P2 × canonical (9.36e-11) and alt (1.131e-10).

## The calibration box (a nuisance, not fitted)
Tracer classes k ∈ {dust, CO, [CII]} present in the sample each get one shared gas-mass offset τ_k (dex; M_gas → M_gas 10^τ_k). The box is |τ_k| ≤ t_k with **t_dust = 0.25, t_CO = 0.25, t_[CII] = 0.35** (the declared one-sigma calibration uncertainty on the gas mass; CFG219's baseline). The rule evaluates the grid {−t_k, 0, +t_k} per class present (3^K points).

## The rule
For each cell, each law and each τ on the grid: the median δ over the discs with a 95% galaxy-bootstrap CI (B = 500 in the operating-characteristics runs, B = 10,000 on real discs, percentile method).
- A law is **DISFAVOURED-under** in a cell if the CI upper edge is below 0 at EVERY τ of the grid; **DISFAVOURED-over** if the CI lower edge is above 0 at every τ; otherwise **NOT-DISFAVOURED** (some τ in the box lets it be consistent).
- **FLAT-SEPARATED**: in ALL FOUR cells the rival (H(z)) is DISFAVOURED-under and FLAT is NOT-DISFAVOURED, and the same holds after dropping any single disc (LOO). **RIVAL-SEPARATED**: in all four cells FLAT is DISFAVOURED-over and the rival NOT-DISFAVOURED, LOO-robust. Anything else is **NO-SEPARATION**, reported with the failed condition. For an extra pair (A, B): **A-SEPARATED** if B is DISFAVOURED (the same direction at every τ) and A NOT-DISFAVOURED in all four cells and LOO-robust.
- The nominal (τ = 0) class per cell, as CFG213/216/220, is reported beside; it is never the verdict.

## Operating characteristics (mocks)
Template: the six CRISTAL detections of CFG219 at their R_out (z, R, M★, f_molgas and errors from the tables; nothing from velocities or f_DM), resampled with replacement to N ∈ {6, 13, 20, 30}. TRUTH ∈ {FLAT, H(z)}: g_obs from the true law. Measured masses as CFG219 (M★ error σ★ = 0.15 dex, gas error from f_molgas), the shared true offset **c ∈ {0, +0.25, −0.25, +0.40, −0.40} dex** on the gas mass (the box contains |c| ≤ 0.25; ±0.40 is OUTSIDE it and shows what the rule does when the box is wrong). Two noise scenarios: **OPT** (baryon errors only, as CFG219) and **REAL** (plus an independent per-disc scatter η ~ N(0, 0.21 dex) on log D, so that the total per-disc scatter is the 0.25 dex CFG220 measured on the real six discs). K = 100 mocks per cell, seed 221; LOO evaluated only for mocks that pass the base rule. Outputs per (N, truth, c, scenario): P(FLAT-SEPARATED), P(RIVAL-SEPARATED), P(NO-SEPARATION). Also FLAT vs HORIZON at N = 13 and 20 (REAL, c = 0, ±0.25).
- **Feasible at N** if under REAL and c = 0: P(correct separation) ≥ 0.8 for both truths; **FALSE-SEPARATION-CONTROLLED** if for |c| ≤ 0.25 the rate of the WRONG separation is ≤ 0.05 + 2 √(0.05·0.95/K) (= 0.094) for every N and truth. N_feasible = the smallest N on the grid meeting the first, else "NOT FEASIBLE up to N = 30" with the best power reached.

## Controls (all must pass)
- **C1 (type I control)** the false-separation rate at |c| ≤ 0.25 stays within the 0.094 line above in every cell, both scenarios (the frozen FALSE-SEPARATION-CONTROLLED); a failure is reported plainly as the rule not controlling its error.
- **C2 (noise-free)** with ε = 0, η = 0 and c = 0, the truth FLAT gives FLAT-SEPARATED and the truth H(z) gives RIVAL-SEPARATED for every N (the rule's arithmetic).
- **C3 (non-vacuous response, MUTATE=1, outputs `*_MUTATE`)** an injected D × 1.5 (+0.176 dex) in a noise-free FLAT-truth mock destroys FLAT-SEPARATED in every N (FLAT becomes DISFAVOURED-over at every τ).
- **C4** the rule's status of a law at τ = 0 equals the CFG220 machinery's status on the CFG220 six real discs when the box is collapsed to τ = 0 (the CFG220 headline cell reproduced: flat +0.106, rival −0.203).

## Reporting rules
No sentence says the data favour the framework; the rule is conservative by design (a worst case over the box) and the false-separation control holds only if the true calibration is inside the box; REAL is the primary scenario, OPT the optimistic one; the operating characteristics describe THIS rule on THIS template, not a claim about any real sample; first-run outputs are kept if a check implementation is fixed; outputs named by mode.
