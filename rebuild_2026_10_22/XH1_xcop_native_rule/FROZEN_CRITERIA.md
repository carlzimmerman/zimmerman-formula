# XH1_xcop_native_rule: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Does route E's current rule (FC1), unchanged, predict X-COP's hydrostatic mass profiles? This rule has never been graded on them. HO1 graded X-COP only under the older CL2 picture (Burkert, c_f slope, Σ 630–770 M☉/pc²).

**Why now, disclosed.** The owner asked for a way to win. FC1's cluster grade is decided by G-IN-Mall, an over-prediction of 1.90× in the shear band 0.15–0.46 Mpc. That band's error is dominated by its cross-shear term (IC1 D2), and it is not covered by X7's calibration. HO1's X-COP read went the opposite way in the cores under the older rule. So this lane looks for a way out, and is guarded as one: the pass line is inherited unchanged, nothing is scanned, and a fail is reported as found. I have seen HO1's X-COP numbers and FC1's shear numbers. I have not seen this rule on X-COP.

**Standing.** κ = ½ FITTED. Footings scored separately, never pooled. Newtonian gravity on baryons plus cold dark energy halos. No ΛCDM input: no c(M), no cosmic baryon fraction from Planck. Not "theory closed". Nothing here says the data favour the framework. No downloads. One thread, nice 15, under 1 GB.

## The rule (FC1's, nothing refit)
- S = max(a₀/2πG, f_c η(M) Σ_coll(M)), f_c = R_nat/(1 + R_nat), η = (4/(3 B(1))) c_f(M)^(5/4), c_f from CE1's median table at the graded f★ (cluster masses ng 48). M = M_fair + M_b,t, as FC1's cluster path has it.
- Smooth core: M_h(r) = π S r₀² B(r/r₀), B(x) = 4[asinh x − x/√(1 + x²)]. r₀ from the grader's `solve_r0(M_fair, r_ta, S)`.
- Budget: M_fair = R_nat M_b,t. M_b,t = (1 + f★) × gas, from X73's `_gc2_ext`: each cluster's own M_gas(R500) and R500, slope 2.7774 beyond R500, to the self-consistent r_ta.
- All of this runs inside FC1's grader text, in its namespace, not re-coded.
- The gas slope 2.7774 is a measurement from X-COP gas, and the rule uses it. X-COP's hydrostatic masses enter nowhere in the prediction.

## Data and grade (HO1's line (a), unchanged)
- CS2's X-COP rows, executed from CS2's source: 7 clusters with stars, x = r/R500 in {0.1, 0.2, 0.3, 0.5, 0.7}, 35 points. M_HSE = `M_FORW`. Baryons at r = measured gas + measured stars.
- Δ = log₁₀[M_HSE / (M_b + M_h)] at each point. Δ > 0 means the model is too light.
- **A run passes iff |mean Δ| ≤ 0.05 dex and rms Δ ≤ 0.10 dex.**
- Graded at f★ 0.034 and 0.0615, on both footings.

## Verdict (headline canonical; FOOTING-SPLIT if alt differs)
- **X-COP PASS:** passes at both f★.
- **F★-DEPENDENT:** passes at exactly one.
- **X-COP FAIL:** passes at neither, naming mean or rms and the sign.

A pass here does not change FC1's frozen label or G-IN-Mall's. It says X-COP agrees with the rule and nothing more.

## Reported, not graded
1. Δ by x, per-cluster mean Δ, S, r₀, M_b,t, r_ta. Comparators: HO1 mean −0.002, rms 0.126; CS2's OS1 rms 0.124 canonical, 0.092 alt; CS2 law rms 0.205.
2. **The disputed band.** Points with 0.15 ≤ r ≤ 0.46 Mpc: n, mean Δ, and R_X = 10^(−mean Δ), model/data. Beside it G-IN-Mall's pred/meas 1.90 (h 0.672, f★ 0.034). Label at each f★: **SHEAR BAND OUTLIER** if R_X ≤ 1.25; **INNER OVER CONFIRMED** if R_X ≥ 1.5; **IN BETWEEN** otherwise. This compares 3D hydrostatic mass with projected shear on different clusters (X-COP is massive, 7 systems), so it can show a conflict between data sets but not settle which is biased.
3. η at 10¹³ and 10¹⁴ × g, 10¹² unchanged, for g = 0.90 and 1.1144 (FC1's `fc1_a4_expect.py` grid), at f★ 0.034 and 0.0615: mean, rms, disputed band.
4. `--A4`, once CE1's A4 tables exist: same grade on them, reported beside this one.

## Checks
- **K0:** FC1's cluster predictions reproduced in this run, against `FC1_med_fs{f★}` JSON, both footings, both h: max |d| ≤ 1e-9.
- **K1:** CS2's X-COP grader, executed from CS2's source, reproduces CS2's committed law mean and rms: ≤ 1e-9.
- **K2:** at every cluster, π S r₀² B(r_ta/r₀) = M_fair within 1e-8, or counted saturated.
- **K3:** M_b,t independent of the starting guess (× 0.3, × 3): ≤ 1e-4.
- **K4:** S / Σ_coll = f_c η(M) on the collapse branch at every cluster, ≤ 1e-9; the number on the floor is reported.
- **MUTATE** (`--mutate`, separate outputs): S × 2. It must move mean Δ by more than 0.02 dex, else the grade is insensitive and the lane is UNDECIDED.
- Any K failure: no verdict, exit 1.
