# SL1_symbolic_law_search: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Does any closed-form pair of operators with no fitted float, built from the listed leaves, clear SPARC's line and tilt, ET1's six S bins, LITTLE THINGS and the 15 cluster keys on half of SPARC, then hold on the other half, the 63 groups and X-COP? Spec relayed by the owner, 2026-11-01; numbers below are the spec's unless marked.

**Disclosed before the freeze.** I have read NR1's PRIMARY record: Υ 0.72 / 0.75, Υ by V_flat 1.20 to 0.57, failing keys G-IN-all, G-MID-T3, G-IN-Mall (Z −2.06, −2.62, −2.89, h 0.672), groups Z +1.47, and ND1's LITTLE THINGS +0.138. So this search is not blind to the baseline. No tree has been evaluated.

## Baseline
Version N at ng 80, as NR1 PRIMARY: η(10¹²) 21.53, ρ₁₀ 1.359, ρ₁₁ 1.131, A4's η at 10¹³ and 10¹⁴, smooth core, f★ 0.034, GS1's gas slope, native Ω_c/Ω_b, eRASS1's measured gas, one template (`fix_cells`, RF3). NR2's ng 80 low-mass runs are still running, so these low-mass ratios remain ANCHOR-DEPENDENT and any result inherits that. Rerun when NR2 lands.

## Operators
- **A**, per system: r₀_eff = A · r₀_native, with cold mass inside R₂₀₀ (r_ta on clusters) held. Leaves: q_diss, v_rel, z_1, eta_native, c_f_native, constants.
- **B**, per radius: g_c_eff = B · g_c(A), so M_c,eff(r) = B · M_c(r; A). Leaves: x_b, x_c, f_local, q_diss, constants. x_c and f_local use the native halo, so A and B stay separable.
- Constants: κ 0.5, f_b 0.15945, R_nat 5.271, 1, 2, π. No other float can enter a tree.
- Operators: + − × ÷ sqrt log1p inv_1p. Depth ≤ 4, nodes ≤ 11, per tree. Any non-finite value, A or B ≤ 0, or A outside [10⁻³, 10³] on any system rejects the tree.

**Ledger inputs (all without a fitted number; by-hand items marked):** E_SN = (M★/100) × 10⁵¹ erg, BE1's budget. E_BH = 0.1 × 0.005 × M★ c², BH1's. M★ = 0.5 L₃₆ (SPARC), f★/(1+f★) M_b(<r_ta) (clusters), SED mass (LITTLE THINGS), group M_b. Both energies at coupling 1, **an upper bound: BY HAND**. |W_core0| = G (π S r₀²)²/r₀ ∫₀¹ B B′/x dx on the native core. v_rel = V₂₀₀/c, z_1 = 1 + z_f from `sigma_coll`, c_f = 4 (η/10.82)^0.8, CE1's map.

## Tier 1, before any data
1. Matching: at q_diss = 0, x_b = 0, f_local = 0, with every other leaf on a stated grid, |A − 1| and |B − 1| < 10⁻¹².
2. Outer bound: B at x_c = 10⁻³⁰, x_b = f_local x_c, f_local = 1/R_nat, q_diss on a grid: |B − 1| < 10⁻¹². Without this the cold mass at r_ta changes.
3. Units: every leaf is dimensionless, so this holds by construction. Recorded, not tested.

## Train gates (62 of 124 galaxies)
Split: `sel`'s 124, stratified on the six V_flat bins, numpy `default_rng(20261101)`, written to `split.json` before any tree runs.
- **G1** both backgrounds: median Υ in [0.50, 0.80] and |Υ(V_flat < 100) − Υ(V_flat > 150)| ≤ 0.15.
- **G2** median S_eff on background A inside each ET1 interval: [52,85], [81,124], [118,200], [98,190], [137,272], [182,596]. S_eff comes from A alone.
- **G3** LITTLE THINGS, 20 galaxies, |median E| ≤ 0.05 on both backgrounds, E as ND1.
- **G4** all 15 keys |Z| ≤ 2, both h, canonical template.

Loss = max(0, |Υ − 0.65| − 0.15) + max(0, |tilt| − 0.15), each background, + Σ max(0, |z_k| − 1.96) with z_k from S_eff against the bin's interval in ln S + max(0, |E| − 0.05) / 0.05 each background + Σ max(0, |Z_j| − 2) at the worse h + 0.02 × nodes. L_gate is the same without the node term.

## Search
- **GA:** population 250, 200 generations, per grammar and seed.
- **Grammars:** SPEC, as listed. NATIVE, without x_b, x_c and κ. Owner's 10-31 rule keeps a₀ out of the cold sector and κ in the a₀ law only, so **a SPEC hit that depends on a₀ violates a standing owner decision and is reported as such, not adopted**. Dependence is tested numerically by regrading at alt's a₀.
- **Seeds:** 3 per grammar.
- **Exhaustive sweep, added by me:** the spec says 50,000 evaluations "exhaust" the grammar. They do not; 11-node trees number far above that. So I also enumerate A alone and B alone up to the largest size that runs in the budget, deduplicated by value, and cross the best of each. Only that sweep may be quoted as exhausted, and only up to its stated size. It is a statement about this grammar and these inputs, **never an impossibility theorem**.
- **Surrogate:** cluster keys run through a linear response per cluster about the baseline, for speed. Every hit, and the 20 lowest-L_gate pairs of each grammar, are regraded through the grader's own `dvecN`.

## Gauntlet, for L_gate = 0 on Train
All on the exact path. Holdout's 62: G1 as above, and G2 against intervals **recomputed from the holdout galaxies' own S_need** in `et1_results.json`, because the spec's intervals contain holdout galaxies (ET1 used 123 of these 124). 63 groups: `grade_groups` statistic, verdict CONSISTENT, as NR1 ("G2" in the spec means these groups, not lane `G2_preinfall_retention`). X-COP: HO1's line, |mean Δ| ≤ 0.05, rms ≤ 0.10, hydrostatic, bracket status as RF3. Full 175: NR1's line. Keys: also on alt's template. Reported, not gated: B at q_diss = 0 against CN1's Blumenthal contraction on SPARC. The spec's §2 names CN1 in the holdout and §3 does not; §3 governs, as "the exact spec".

## Labels
- **SURVIVOR [a₀-FREE | a₀-DEPENDENT]:** passes Train and gauntlet. Written to `SURVIVORS.md`. A survivor is a candidate, selected from a large search with G3 and the keys unsplit; it needs new data before it can be called a law.
- **TRAIN ONLY:** clears Train, fails the gauntlet.
- **NO HIT:** no pair clears Train. Report the minimum L_gate, the gates still failing, and the Pareto front of G4 violation against G1–G3 violation.

## Limits stated now
Keys, LITTLE THINGS and groups are not split, so only SPARC has a true holdout; the spec's §2 split of X-COP into 4 and 3 is not used, since §3 holds X-COP out whole. ET1's S_need assumes no contraction, so G2 is inconsistent for any B ≠ 1. Constants can compose into arbitrary numbers at 11 nodes, so zero floats does not mean zero freedom: report the number of distinct trees evaluated with any hit. Zoom noise on η isn't propagated into the gates.

## Checks (any failure: NOT DECIDED)
- **K1** A = B = 1 reproduces NR1 PRIMARY's Υ and rms on 175, both backgrounds, |d| ≤ 10⁻⁹.
- **K2** same, Υ by V_flat on 124, against `nr1_bins.out` to its rounding.
- **K3** cluster preds at identity against NR1 PRIMARY, both footings, |d| ≤ 10⁻⁶.
- **K4** surrogate against `dvecN` at A = 0.5, A = 2 and one radial B: max |ΔZ| ≤ 0.05 on any key. If it fails, widen the basis, or grade G4 exactly.
- **K5** LITTLE THINGS at ND1's rule against `nd1_ab_results.json`, |d| ≤ 10⁻⁶.
- **K6** groups at identity against NR1 PRIMARY, |d| ≤ 10⁻⁶.
- **K7** X-COP at identity on the fast path against XH1's own `_grade`, |d| ≤ 10⁻⁹.
- **K8** planted law: synthetic data generated from a tree in the grammar. GA must reach L_gate = 0 there. A null means nothing if this fails.
- **MUTATE** shuffled leaves on the identity gate path must change L_gate; scrambling q_diss across systems must change a q_diss-dependent tree's value.

Runs one thread, nice 15, under 1 GB, while NR2 runs. κ = ½ FITTED; footings never pooled; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework.
