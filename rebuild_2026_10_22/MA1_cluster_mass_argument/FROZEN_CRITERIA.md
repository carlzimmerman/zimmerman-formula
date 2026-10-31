# MA1_cluster_mass_argument: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Route E's core strength is S(M) = f_c η(M) Σ_coll(M). Σ_coll(M) is defined for the object whose collapsed mass today is M: X43's Lacey–Cole half-mass formula takes M as the final mass, and X48's zooms are built that way, with M/2 collapsing at z_f. SPARC and groups pass M200. Clusters pass (M_fair + M_b,t), the whole mass inside the turnaround radius. Since GS1 extended the budget to r_ta, that argument has been about 3× a cluster's M200 (XH1: log M 15.31–15.69 on X-COP). FC1's criteria checked only that it was total mass, not that it was collapsed mass. Does passing the same collapsed mass on all three paths change the grade?

**Disclosed: this is post hoc.** I found it after seeing that clusters need a lower S, while looking for a way out on the owner's request. FC1 was found the same way. The protection is that nothing can be tuned: the definition is the one SPARC and groups already use, there is no parameter, and every frozen key is graded unchanged. A pass does not derive S, η or κ.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input. Not "theory closed". Nothing here says the data favour the framework. No downloads. Single-thread niced workers, at most two at once, under 1 GB each, beside the live zooms. No A4 snapshot is read except through `--A4`.

## The rule
Cluster path only, in FC1's grader, in its namespace:
- S = max(a₀/2πG, f_c η(M₂₀₀) Σ_coll(M₂₀₀)).
- M₂₀₀ is the model's own total mass (baryons + cold) inside R₂₀₀, where M_b(R₂₀₀) + π S r₀² B(R₂₀₀/r₀) = 200 ρ_c (4π/3) R₂₀₀³.
- ρ_c is the z = 0 critical density of the `A_c2b_refit` background, the same expression SPARC and groups use.
- r₀ = `solve_r0(M_fair, r_ta, S)`. M_fair and r_ta are unchanged, so the cold mass inside r_ta is still the native fair share.
- S and M₂₀₀ are solved as a fixed point per cluster, per h, per footing: |Δ ln M₂₀₀| ≤ 1e-8 within 100 iterations.
- SPARC and groups are not touched. η table: CE1's median at the graded f★ (cluster masses ng 48).

## Grade (X74's grader, FC1's thresholds, unchanged)
SPARC line on both backgrounds, groups, all 15 cluster keys at h 0.672 and 0.686, |Z| ≤ 2. Graded at f★ 0.034 and 0.0615.

## Verdict (canonical headline)
- **MASS ARGUMENT PASS:** passes at both f★.
- **F★-DEPENDENT:** passes at exactly one.
- **MASS ARGUMENT FAIL:** passes at neither, naming the keys.

Alt is reported beside it. Its SPARC line is X78's known failure and is not expected to change.

## Reported, not graded
1. Worst key and its Z, and all 15 Z, at both f★, against FC1's.
2. CE1's p16 and p84 η points, at both f★.
3. η at 10¹³ and 10¹⁴ × g, for g = 1.1144 and 1.206 (the guide for A4 and its 68 % upper end, `fc1_a4_expect.out`), at both f★. Does the pass survive what A4 is expected to do?
4. **Definition sensitivity:** M at 18π² ρ_m(z = 0), native Ω_m, instead of 200 ρ_c, at both f★. The zooms' virial radius is defined this way at z_f, so this brackets the choice. If this variant changes the label, the label is DEFINITION-DEPENDENT and I say so.
5. X-COP on this rule (XH1's line, |mean| ≤ 0.05, rms ≤ 0.10), by x, with M₂₀₀ from each cluster's own budget.
6. M₂₀₀ / (M_fair + M_b,t) and S / S_FC1, median and range.
7. `--A4`, once CE1's A4 tables exist: same grade on them, beside this one.

## Checks
- **K0:** with the switch off, FC1's committed cluster predictions, SPARC rms and groups Z are reproduced: |d| ≤ 1e-9.
- **K1:** with the switch on, SPARC rms and groups Z are unchanged from FC1: |d| ≤ 1e-9.
- **K2:** at every converged cell, the R₂₀₀ equation holds to 1e-6, and every fixed point converges. Non-converged cells are counted; any such cell means no verdict.
- **K3:** M₂₀₀ < M_fair + M_b,t at every cell.
- **MUTATE** (`--mutate`, separate outputs): the mass argument × 2. It must move G-IN-Mall by more than 0.05 in Z, else the lane is UNDECIDED.
- Any K failure: no verdict, exit 1.
