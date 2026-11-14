# AGB5R — blind re-grade of AGB5: my reading of the frozen rules (written before any fit with a mass step)

2026-11-14. Second, independent implementation of lane AGB5, from its `FROZEN_CRITERIA.md` only. Read so far, of the
AGB family: AGB5's `FROZEN_CRITERIA.md`; AGB1's `FROZEN_CRITERIA.md` (for the W1 word table that AGB5 names); AGB4's
`FROZEN_CRITERIA.md` (for "AGB4's fit", which AGB5 names for its one Pantheon+ row); a hand-over note of the AGB1
blind re-grade that holds AGB1's words and nothing of AGB5. Not read: AGB5's amendment, README, scripts or outputs, and
the results, scripts or post hoc files of any AGB folder. Stage 1 follows the frozen file; stage 2 (the amendment) is
opened only after stage 1 is committed.

What I have run before writing this: loaders and row counts only (no fit of any kind). Counts: table 1 199 rows,
table 2 102 rows, 33 ids in both, 268 in all; all 301 rows found in the SDSS-II table by `cid`; FSPS mass
(`logMass_Ravi`) present for 187 and 101; table 1's two residual columns differ in 198 of 199 rows; the 321 Pantheon+
SDSS rows (IDSURVEY 1) hold 196 of the 268 hosts (161 of table 1, 65 of table 2). One table-2 host (3674, typed
pSNIa) has no spectroscopic redshift in the SDSS-II table and no mass, so it is outside every step fit.

## The model, as I read it
Per table, plain line: HR_i = α + β age_i + g (L_i − ½), L_i = 1 if `logMass_Ravi` < 10, else 0; hosts with no mass
are left out of every fit that has the step. Weights w_i = 1/(σ_HR,i² + 0.10²). Weighted least squares; A = β/(−0.030).
The error σ_A is the **formal** one, from (Xᵀ W X)⁻¹ with these weights, not rescaled by χ²/dof. Reason: the file calls
0.17 / 0.13 the "power from the design alone" and quotes "design-only errors of the slope", i.e. the error the weights
alone imply; the word is built on that σ. (K4 is the frozen check of whether that σ is right.) I also print the
χ²/dof-scaled error as a reading, never in a word.

Combined: inverse-variance mean of the two tables' Â with their formal σ_A: Â_c = Σ Â_t/σ_t² / Σ 1/σ_t²,
σ_c = (Σ 1/σ_t²)^(−½). The 33 shared hosts are in both tables (as published).

No-step fits (L0, KA): every row of the table (199, 102), mass or not; g = 0.

## Word L1
Δχ²(A=a) = (Â_c − a)²/σ_c² for a = 0 and 1. AGB1's W1 table: EXCLUDED AT 3 SIGMA if Δχ²(A=1) ≥ 9 and Δχ²(A=0) < 4;
DISFAVOURED if 4 ≤ Δχ²(A=1) < 9 and Δχ²(A=0) < 4; REQUIRED AT 3 SIGMA if Δχ²(A=0) ≥ 9 and Δχ²(A=1) < 4; FAVOURED if
4 ≤ Δχ²(A=0) < 9 and Δχ²(A=1) < 4; UNDECIDED if both < 4; NEITHER if both ≥ 4 (each prefixed "AGE BIAS").
Second word, the same first word under each single change: (1) table 1 alone (its own Â, σ_A); (2) table 2 alone;
(3) the combination with the 33 shared hosts dropped from table 1; (4) the combination with table 1's bracketed
(original) residuals; (5) the combination with a term c·z added to each table's line, z = `z_best_with_BOSS_CMB` of
the SDSS-II table (every host in a step fit has one); (6) the combination with the structural fit (below, step free)
in place of the plain line, each table's σ from the curvature. ROBUST if all six agree, else FRAGILE naming which.
If KA, K1, K3 or K4 fails, the word is NOT EVALUABLE and the words above are printed as a reading only.

## The structural fit (errors in both variables)
Per host: true age t_i ~ N(μ_k, τ²), k = L_i when the step is free (two means, one shared τ), one μ when it is not;
observed age = t_i + N(0, σ_age,i²); HR_i = α + g (L_i − ½) + β t_i + N(0, σ_int² + σ_HR,i²). The pair
(age_i, HR_i) is bivariate normal with mean (μ_k, α + g(L−½) + β μ_k) and covariance
[[τ² + σ_age², β τ²], [β τ², β² τ² + σ_int² + σ_HR²]]. Maximise the likelihood over (α, β, g, μ_k, τ, σ_int) with
τ ≥ 0, σ_int ≥ 0 (several starts, the best kept). σ_β = √[(H⁻¹)_ββ] with H the numerical Hessian of −ln L at the
maximum over all free parameters; if σ_int sits on 0, it is held at 0 for the Hessian (stated if it happens).
Reported rows: σ_age scaled by 0.5 and by 0 (the latter is the plain regression with a fitted scatter).

## Checks
- **KA.** Plain, no step: |β − (−0.038)| ≤ 0.004 (table 2), |β − (−0.025)| ≤ 0.004 (table 1); combined slope (the
  inverse-variance mean of these two, formal errors) within 0.004 of −0.030. Structural, no step: within 0.004 of
  −0.062 (table 2), −0.047 (table 1), −0.037 (table 1, bracketed residuals). Tolerances on the slope in mag/Gyr.
- **K1.** 199 and 102 rows, 33 shared, every id in the SDSS-II table, and table 1's two residual columns not identical
  (I count the rows that differ).
- **K3.** HR := 0.1 + 0.05 (L − ½) + A_true (−0.030 age), weights as in the real fit, A_true = 1 and 0, both tables,
  plain step-free fit on the step sample: |Â − A_true| ≤ 10⁻⁶. The mode exits 3 if all four pass, 4 if any fails.
- **K4.** Per table, plain step-free fit on the step sample, σ_A its formal error. (a) Shuffle: the pairs (age, L)
  permuted together among the hosts, HR and σ_HR kept, `numpy.random.default_rng(20261118)`, a fresh generator per
  table, 400 permutations: pass if |mean Â| ≤ 0.2 σ_A and the standard deviation (ddof 1) of Â is in [0.8, 1.25] σ_A.
  (b) Bootstrap: hosts resampled with replacement, 400 draws, the file gives no seed, so a fresh
  `default_rng(20261118)` per table: pass if the standard deviation of Â is in [0.8, 1.25] σ_A. K4 passes only if
  (a) and (b) pass for both tables.

## Reported only
The step g per table with and without the age term (step sample); the plain slope inside each mass group
(L = 0 and L = 1 separately, no step); the structural fit with σ_age × 0.5 and × 0, no step and step free, per table
and combined; the Pantheon+ row.

**Pantheon+ row (AGB4's fit).** Hosts of either table among the Pantheon+ IDSURVEY 1 rows, matched by CID = SDSS id
(196). y = mB − μ_fid, μ_fid = 5 log₁₀[(1 + zHEL) D_M(zHD)/10 pc], flat Ω_m = 0.334 (H0 is absorbed by the offsets);
8 equal-count bins in zHD with free offsets; a x1 + b c free; weights 1/C_ii of the Pantheon+ STAT+SYS covariance;
A × (−0.030 × age); with no step and with g (L − ½), L = 1 for Pantheon+ HOST_LOGMASS < 10. **Ambiguity:** the 30
hosts of both tables that are in Pantheon+ have two ages. Primary: table 1's age (the larger sample); also printed:
table 2's age for them, and each table's hosts alone. No word rests on this row.

## Things I think are under-specified (resolved as above)
1. Whether σ_A is formal or rescaled: formal (the file's own "design alone" numbers), with K4 as the guard.
2. No seed for the bootstrap: the shuffle's seed, fresh generator.
3. Which redshift for the z-term: the SDSS-II spectroscopic CMB-frame redshift; the frame barely matters at this level.
4. Two ages for shared Pantheon+ hosts: table 1's, with table 2's as a printed alternative.
5. The structural fit's τ: one τ shared by the two mass groups (the file says "a separate mean age for each mass group",
   nothing about separate widths).
6. "Table 1's two residual columns differ": read as "not identical".

kappa = 1/2 FITTED; not theory closed.
