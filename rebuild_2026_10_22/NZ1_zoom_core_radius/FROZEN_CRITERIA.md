# NZ1_zoom_core_radius: FROZEN CRITERIA (committed alone, before any script or graded number)

**Question.** Route E takes S from the zooms but solves r₀ from a budget: `solve_r0(M_fair, r_ta, S)` on clusters, `solve_r0(M200, R200, S)` on galaxies and groups. The zooms also give r₀. Their fit has M(<r_f) = M/2 at r_f, so η = (4/3) a²/B(a) with a = r_f/r₀, which fixes a from η alone. Does taking r₀ from the zooms too, with the fair share only setting the mass beyond r_f, pass the graders?

**Disclosed: post hoc, and I have seen one number.** While checking MA1 I computed r₀(budget)/r₀(zoom) ≈ 1.6 on X-COP. As a quick look, I then swapped in r₀(zoom) with S unchanged on X-COP: mean +0.047, rms 0.087. That would pass HO1's line, and it is the reason for this lane. It is not a grade: it used a single r⁻³ tail and MA1's M. I have not seen any cluster key, SPARC or group number under this rule.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input. Not "theory closed". Nothing here says the data favour the framework. No downloads. At most two single-thread niced workers, under 1 GB each, beside the live zooms. No A4 snapshot is read except through `--A4`.

## The rule (no fitted parameter)
At collapsed total mass M, on the collapse branch of S:
- S_c = f_c η(M) Σ_coll(M), as MA1.
- r_f² = 3 (M/2) / (4π Σ_coll(M)), from Σ_coll = Δρ_m(z_f) r_f and M/2 = (4/3)π Δρ_m(z_f) r_f³.
- a from η(M) = (4/3) a²/B(a), B(x) = 4[asinh x − x/√(1 + x²)]. r₀ = r_f / a. The cold share keeps the same r₀ (FC1's K2).
- Inside r_f: M_c(r) = π S_c r₀² B(r/r₀), which gives M_c(r_f) = f_c M/2.

**Clusters** also have a budget, so beyond r_f:
- ρ_c = ρ(r_f) (r/r_f)^(−γ) from r_f to r_ta, continuous at r_f. M_c(r_ta) = M_fair fixes γ per cluster. Nothing is free; γ is an output, reported against the record's 2.25 and the gas's 2.777.
- If M_c(r_f) ≥ M_fair, no tail exists: that cell is counted and keeps the profile at M_fair.
- M = MA1's M₂₀₀, from MA1's fixed point on its single-tail profile, kept as it is. This is a hybrid, and I say so: the frozen profile cannot itself hold M inside R₂₀₀ at z = 0, because the zooms stop at z_f with M/2 inside r_f.

**SPARC and groups** have no tail to solve: all graded radii are inside r_f. On the collapse branch r₀ = r_f/a at M = M200/f_c, as FC1's argument. A system on the floor keeps its budget r₀, because the zooms give no r₀ for a floor.

η table: CE1's median at the graded f★. Below 10¹² η and a are clamped at the 10¹² values, because no native value exists until X80.

## Grade
- **Keys:** X74's grader, FC1's thresholds, unchanged: SPARC line on both backgrounds, groups, 15 cluster keys in both h.
- **X-COP:** XH1's line, unchanged: 35 points, |mean Δ| ≤ 0.05, rms ≤ 0.10, with the same two-zone profile.
- Graded at f★ 0.034 and 0.0615, on the canonical footing. Alt is reported.

Two sets of runs: **ALL** (the rule above on every path, the one rule the theory could claim) and **CLUSTERS** (only the cluster path changes, SPARC and groups stay as FC1).

## Verdict (canonical, ALL)
- **NATIVE CORE PASSES ALL:** keys and X-COP pass at both f★.
- **F★-DEPENDENT:** all pass at exactly one f★.
- **CLUSTERS PASS, GALAXIES BREAK:** in CLUSTERS, keys and X-COP pass, but in ALL the SPARC line or groups fail. Then the rule is split between paths and I say that it is split.
- **X-COP PASSES, KEYS BREAK:** X-COP passes and cluster keys fail, naming them. That is IB1's trade again.
- **NATIVE CORE FAILS:** anything else, naming what fails.

## Reported, not graded
1. All 15 Z, X-COP by x, γ median and range, r_f, r₀ and the counted cells.
2. SPARC under ALL: Υ on both backgrounds, rms, and ΔV by V_flat bin against FC1's (L★ −16, 250–400 −57).
3. η at 10¹³ and 10¹⁴ × 1.1144 (A4's guide), both f★, under the verdict's run set.
4. `--A4`, once CE1's A4 tables exist.

## Checks
- **K0:** with the rule off, MA1's cluster predictions, SPARC rms and groups Z are reproduced: |d| ≤ 1e-9.
- **K1:** a(η) returns η: (4/3) a²/B(a) = η to 1e-9, and M_c(r_f) = f_c M/2 to 1e-9 at every collapse-branch cell.
- **K2:** M_c(r_ta) = M_fair to 1e-6 at every cluster cell with a tail, and ρ continuous at r_f to 1e-9.
- **K3:** under CLUSTERS, SPARC rms and groups Z equal FC1's: |d| ≤ 1e-9.
- **MUTATE** (`--mutate`, separate outputs): r₀ × 1.5. It must move X-COP's rms by more than 0.01 dex, else the lane is UNDECIDED.
- Any K failure: no verdict, exit 1.
