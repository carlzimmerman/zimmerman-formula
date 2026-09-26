# XR2 — the fixed-cell clearing correction (L379 / L380) and Lean I28: adversarial review

Reviewed at commits 1c5a52dd5 (L379), 4e16ccf58 (L380), 8ad1d1e69 (I28); read-only on all of them. Nothing was
re-run. The numbers below come from `XR2_fixed_cell_estimators.py` (its `.out` in this directory; MUTATE control in
`XR2_fixed_cell_estimators_MUTATE.out`, rc = 1) or are quoted from committed files by path:line.

## 1. Verdict

1. **The correction is sound.** L379 found a real outcome-selection bias in the record's G3, and its fixed-cell measure
   brings the implementation back to G3's written definition.
2. **The fixed-cell measure estimates retention, not the dark fraction at the model's galaxies.** For the RC100 reading
   of G3 it can be biased low. It does not follow the model's baryons, and it does not divide by them. On a synthetic
   field with known truth it understates the dark-to-baryon ratio by 27–34% (S2, S3). Where anything can be measured,
   the baryon-normalised values are about 1.2× the fixed-cell ones (§3.4). A correction that size leaves L380's pooled
   values near 0.07–0.09, far below 0.30. The window would close only if the model keeps less than 20–23% of ΛCDM's
   baryons in ΛCDM's dense cells. That extrapolates across resolution; it is not a measurement.
3. **Selecting on the model's own baryons does not remove the bias in general.** It escapes selection on the carrier
   itself. It does not escape the carrier's gravity (84% of the mass): with a fixed threshold it overstates the ratio
   when baryons stay denser where the carrier stayed (S3). The estimator that is exact in all three synthetic cases is
   Lagrangian: follow the ΛCDM-dense baryons by particle identity.
4. **The committed runs did not save enough.** L379 and L380 deleted their z = 2 fields. L388, as launched, deletes them
   too. The estimator cannot be computed without re-running the particle-mesh boxes. The specification is in §5.
5. **I28 does not match L379's statistic.** Its hypotheses fit the fixed-cell aggregate exactly, but not the
   own-dense-set statistic in three ways (§6). An exact counterexample shows its conclusion does not transfer. I28
   certifies the idealised mechanism only, as its own docstring says ("idealised", I28 line 9).

## 2. What each statistic is (from the code)

| | definition | where |
|---|---|---|
| A (record G3) | [Σ_{ρ_m>50} c_m / Σ ρ_m] / [Σ_{ρ_l>50} c_l / Σ ρ_l], each run on its **own** dense set; pooled as Σ_box / Σ_box | L377_full_construction_pm.py:196–198; L380…py:117 |
| B (L379 fixed cells) | Σ_F c_m / Σ_F c_l, F = {ρ_l > 50} (ΛCDM's dense cells at z = 2); pooled by summing | L379…py:135, 144; L380…py:98, 108, 118 |
| C | Σ_F b_m / Σ_F b_l, the baryons kept in the fixed cells | this review |
| D | B / C, the fixed-cell dark-to-baryon ratio relative to ΛCDM | this review |
| E | [Σ_{S_m} c_m / Σ_{S_m} b_m] / (WC/WB), S_m = {b_m > 50 WB}, the model's own baryon-dense cells | this review |
| E_rank | as E, over the \|F\| cells of largest b_m | this review |
| L (Lagrangian) | the carrier-to-baryon ratio at the model positions of the baryon particles that sit in F in ΛCDM | this review |

Here ρ is total matter over the mean, c = WC·rhoc2 is the carrier, and b = ρ − c are the baryons. WB = 0.157112 and
WC = 0.842888 (L366…py:73–74 with L362's h = 0.6736, Ω_m = 0.3138).

In L377's ΛCDM run the two species have identical initial conditions and feel one field (L377 `run()`:
`xcar = xb.copy()`, `pcar = pb.copy()`; mode `none`). So b_l = WB ρ_l exactly. The code-test fields confirm this:
`max|ρ − rhoc2|/max ρ = 0`.

## 3. Is fixed-cell retention the right estimator for G3's target?

**3.1 It repairs a demonstrated bias and matches G3's written definition.** L365 defines G3 as "the carrier mass in dense
cells (1 + delta_mesh > 50) at z = 2 is <= 30% of LCDM's there" (L365_virialization_triggered_carrier.py:29–30). That is a
fixed-position statement. The implementation (L377:196–198) instead compares carrier fractions over each run's own
dense set.

The model keeps 2 of 14,716 galaxy-environment, 69 of 9,383 group and 147 of 1,427 protocluster dense cells at
700 km/s (per-box counts, L379_clearing_by_environment.out:49–53). The own-set value is therefore an average over the
few cells that kept carrier.

**3.2 Retention is not the dark fraction at the model's galaxies.** RC100's question is how much dark mass sits where
the galaxies are. B divides by ΛCDM's carrier, not by the model's baryons, and it counts fixed Eulerian cells. On a
lognormal field with known truth (`.out`, Part 2):

| case | truth | A | B | D | E | E_rank | L |
|---|---|---|---|---|---|---|---|
| S1 cleared in place, baryons fixed | 0.1086 | 0.4412 | **0.1086** | 0.1086 | 0.1086 | 0.1086 | 0.1086 |
| S2 galaxies move one cell with their retained carrier | 0.1086 | 0.4412 | **0.0789** | 0.1104 | 0.1086 | 0.1086 | 0.1086 |
| S3 baryons stay denser where carrier stayed | 0.1656 | 0.5650 | **0.1086** | 0.1656 | 0.1699 | 0.1735 | 0.1656 |

B is exact only in S1. It is biased **low**, toward passing, by 27% in S2 and 34% in S3. So the "bias the other way" is
real in principle.

**3.3 What selecting on the model's own baryons fixes, and what it does not.** E is exact in S1 and S2, because its
selection never looks at the carrier. It is not exact in S3 (+2.6%; E_rank +4.8%). There the carrier is 84% of the
binding mass, so the baryon density itself responds to what was retained.

In that case E is biased **high**, toward failing. That makes E a conservative check, not an unbiased estimator. Only
L, which is selected on the ΛCDM run alone and follows the galaxies' baryons, is exact in all three cases.

**3.4 How large is the effect? Illustration only.** Two field sets from uncommitted L379 development runs survive in
`$TMPDIR`: `L379_8o3o3c8p` at 128³ and `L379_negy1suh` at 64³, the latter with 0–1 dense cells, so unusable. They are
not the committed 256³ runs: the mesh is 2× coarser and the particle number was not recorded. Pooled over three boxes
(`.out`, Part 3):

- **At 675 / 700 km/s:** B = 0.099 / 0.093, C = 0.817 / 0.805, D = 0.122 / 0.115, E = 0.119 / 0.111,
  E_rank = 0.127 / 0.119.
- **Ratios:** E/B = 1.19–1.20 and D/B = 1.22–1.24.
- **Overlap:** 86–94% of the model's baryon-dense cells lie in F.

At L380's pooled B = 0.0699 / 0.0658 / 0.0621 / 0.0587 (600–675 km/s, L380_pooled_window_fixed_cell_clearing.out:54–57),
D exceeds 0.30 only if C < 0.233 / 0.219 / 0.207 / 0.196 (`.out`, flip condition). At the code test's C = 0.81–0.82,
D would be 0.072–0.087. B itself is resolution-dependent: 0.093 at 128³ against about 0.05–0.10 by bin at 256³ for
700 km/s (L379.out:57). So the ratio has to be measured at 256³ before anyone cites it.

**3.5 Resolution.** One mesh cell at z = 2 is 193 kpc physical, 36 times the 5.4 kpc R_e of L376's RC100 host (`.out`;
L376_triggered_carrier_inner_galaxies.out:53–54). No box estimator sees inside galaxies. The RC100 target proper is
L376's resolved result (carrier inside R_e 0.000 of ΛCDM's at z = 1 and 2). G3 in any form is a halo-scale proxy, and
its 0.30 threshold is inherited from L365:29–30.

## 4. Did L379/L380 save enough? No.

- **L379:** its transformed `run_z2` writes the z = 2 total and carrier fields to a temp directory
  (L379_clearing_by_environment.py:65–66) and deletes it (line 158). Its results JSON holds per-bin sums only.
- **L380:** reads those fields (L380…py:98, 108) and deletes them (line 110). Its JSON holds the z = 0 per-halo
  retention and gate tables only.
- **L388, running now:** same pattern (L388_linear_gate_pooled.py:84, 123). It records neither baryon fields nor
  particle identities. Once it finishes, its z = 2 fields are gone as well. It cannot supply §5 without a relaunch or a
  same-cell follow-up (L380's 15 runs took 13,153 s, L380.out:30).
- **Baryon particle positions:** no run saves them, so L cannot be formed from any existing output.

## 5. Specification for the same-cell re-run (L388 or its successor)

**Record.** Hook into L379's `run_z2`, at `z == 2.0`, beside the existing `np.save` calls:

- keep `{name}_z2_rho.npy` and `{name}_z2_rhoc.npy` as written (float32, 256³);
- add `{name}_z2_bcell.npy`: the NGP cell of every baryon particle at z = 2, as an int32 flat index in `rho.ravel()`
  order (192³ entries, 28 MB);
- compute every sum below **before** the `rmtree`, and write the per-box numerators and denominators into the results
  JSON. The estimators can then be recomputed from committed output without re-running the boxes.

**Sets** (per box). Particle i is the same Lagrangian element in every run of a box, because the initial conditions are
seeded by `rng(sp)` and `xcar = xb.copy()`.

- F = {ρ_l > 50}, as L379/L380.
- S_m = {b_m > 50·WB}.
- S_rank = the \|F\| cells of largest b_m.
- D_m = {ρ_m > 50}, the record's set.
- P = {baryon particles i : bcell_l[i] ∈ F}.

**Estimators.** Pool over the three boxes by summing numerators and denominators, as L380:117–118.

- A, B, C, D, E and E_rank, exactly as in §2.
- L = [Σ_{i∈P} c_m[bcell_m[i]] / Σ_{i∈P} b_m[bcell_m[i]]] / [Σ_{i∈P} c_l[bcell_l[i]] / Σ_{i∈P} b_l[bcell_l[i]]].
- B, D, E and L also per environment bin, using L379's nearest-ΛCDM-peak assignment (L379…py:121–137). The galaxy bin
  is RC100's.

**Diagnostics.**

- \|F\|, \|S_m\|, \|D_m\|.
- The share of S_m inside F, by count and by baryon mass.
- For I28: whether one τ separates the retained fractions c_m/c_l of F∩D_m from those of F∖D_m (min over the first
  against max over the second).

**Controls.**

- **K0 species identity:** ρ_l = rhoc2_l to float32 in each ΛCDM run. This fixes WB, WC and the index order.
- **K1 null:** model := ΛCDM gives every estimator 1 to 1e-6.
- **K2 index order:** the NGP count field `bincount(bcell_l)` must correlate with ρ_l at Pearson > 0.99.
- **K3 synthetic injection on the real ΛCDM z = 2 fields:** in-place retention U(0, 0.2) must give B = D = E = L = truth
  to 1e-10 with A > truth. A one-cell shift of b and of the retained c must give E = L = truth with B < truth. This is
  Part 2 of `XR2_fixed_cell_estimators.py`, run on the real mesh.
- **MUTATE (v_k = 0):** every estimator must exceed 0.30.

**Pass criterion.** Pre-declare this before the run. At a kick, the clearing gate passes iff pooled **L ≤ 0.30**
(the RC100 reading) **and B ≤ 0.30** (the record's retention reading).

- **Report without gating:** D, E and E_rank.
- **Estimator-dependent:** if L and E fall on opposite sides of 0.30, record the gate as estimator-dependent, not
  passed.
- **Galaxy-bin failure:** if the galaxy bin alone has L > 0.30 while the pooled value passes, record a galaxy-bin
  failure.
- **Flag, don't gate:** C < 0.5 means the model's baryons have largely left ΛCDM's dense cells, and a box clearing gate
  of any form is then weak evidence.

## 6. I28 against L379's statistic

**What matches.** I28's fixed-cell aggregate, Σ_s c_m / Σ_s c_l over all of ΛCDM's dense cells (lines 6–9, 39–56),
is exactly L379's measure (b), pooled by summing over boxes.

**What does not match.** I28's "selected" statistic is `s.filter (τ c_l ≤ c_m)` (lines 29–56). That means one uniform
threshold on the retained fraction, a set inside s, and a ratio of carrier masses. L379's (a) = L377's G3 differs on
all three counts:

1. **Different selection variable.** It selects on the model's **total** density, ρ_m = b_m + c_m > 50
   (L377:197). The implied retention threshold (50 − b_m,i)/c_l,i therefore varies from cell to cell with the model's
   baryons.
2. **Set not inside F.** D_m is not a subset of F.
3. **Different normalisation.** It is a ratio of carrier **fractions**, each over the run's own set.

**Consequence.** I28's conclusion does not transfer.

- **Exact counterexample** (`.out` P1, rational arithmetic): fixed 0.2491 against an own-set value of 0.0237 in I28's
  form and 0.0465 in G3's fraction form.
- **Random instances:** in 20,000 instances with the model's baryons varying ×0.2–2 between cells, the I28-form
  reversal occurs 459 times. G3's fraction form reverses 0 times, so the reversal is possible but atypical.
- **The code-test fields break it another way:** the own-set G3 reads 0.065 < B = 0.093 at 700 km/s. Two of the three
  boxes have an **empty** own dense set, which L377:198 scores as 0.

**What supports L379.** The support for the correction is empirical: (a) > (b) in every bin of the committed 256³ data
(L379.out:56–57). `l379_instance` (I28 line 58) is a `norm_num` check of three numbers; it is consistent with the
theorem, not derived from it.

**What would make I28 apply.** It would cover L379's statistic in I28's form, restricted to F, whenever a single τ
separates the selected and unselected cells. §5 records that as a diagnostic.

## 7. Files (this directory)

- `XR2_fixed_cell_estimators.py`: P1/P2 (I28), S1–S3 (synthetic truth), the code-test illustration and the flip
  condition. Numpy only, about 4 s.
- `XR2_fixed_cell_estimators.out` and `_results.json`: main run, 6/6, rc = 0.
- `XR2_fixed_cell_estimators_MUTATE.out` and `_results_MUTATE.json`: E selects on total density; S1 fails, rc = 1.
- `XR2_fixed_cell_review.md`: this document.
