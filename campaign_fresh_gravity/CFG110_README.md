# CFG110 — does the KiDS lensing signal at fixed g_bar depend on lens mass within a colour class?

- **Criteria:** frozen in `CFG110_FROZEN_CRITERIA.md` (f870b217a) before any subset number. The lane is numbered 110 to stay clear of another session's sequential numbering.
- **Scripts:**
  - `CFG110_stage_perlens.py`: one pass of the June KiDS estimator, keeping each lens's per-bin sums; 228 s; log in `CFG110_stage_perlens.out`.
  - `CFG110_kids_mass_split.py`: the scoring, about 140 s.
- **Runs:**
  - The main run passes 12 of 12 and exits 0.
  - The MUTATE run (ΛCDM's mass contrast injected) fails H1 and exits 1.
  - The two runs fail different checks, so the control is informative.

## Bottom line

**Within each colour class, the lensing signal at fixed g_bar shows no detectable dependence on stellar mass.** That is B's law's deep-regime prediction.

- **B's law** (no mass dependence) is consistent: **22.2/14, p = 0.075**.
- **CFG67's colour-split ΛCDM** (Mandelbaum halos) is also consistent: 25.2/14, p = 0.033.
  - Between these two models the test's power is Δχ² = 8.8, just below the declared threshold of 9.
  - So by the frozen map the headline is **NON-DISCRIMINATING between B and colour-split ΛCDM.**
- **The test is decisive against the colour-blind ΛCDM** (the Moster relation). That model predicts a strong rise with mass, which is absent: **105/14, p ≈ 4 × 10⁻¹⁶**. Its power against B is 87.

**Read together with the early/late colour split** (CFG61, CFG67, CFG88, CFG95, CFG96): at fixed g_bar the KiDS signal depends on galaxy type, and not detectably on mass within a type.

| model | colour split (early − late) | within-type mass split (this lane) |
|---|---|---|
| **B's law** (no dependence at fixed g_bar) | fails (4.4σ, jackknife; CFG88) | **consistent** (p = 0.075) |
| colour-blind ΛCDM (Moster) | fits (6.9/7; CFG67), through the mass difference between the classes | **fails** (p ≈ 4 × 10⁻¹⁶) |
| colour-split ΛCDM (Mandelbaum) | fits (6.5/7; CFG67) | consistent (p = 0.033) |

- B gets the mass-independence right and misses the type dependence.
- A colour-blind halo can match the colour split only through mass, and that route is closed here.
- Colour-dependent halos fit both.

**The redshift split (R4, the lens photo-z check):** high-z minus low-z within each class is consistent with zero (19.2/14, p = 0.16) and with both models. So nothing suggests that lens photo-z systematics drive the class split.

## Results (1-halo bins K1; late | early)

| | data D = ESD(high M) − ESD(low M), M☉/pc² |
|---|---|
| data | −5.6, 9.6, −7.7, −9.9, −0.7, −3.6, 20.9 \| 0.2, 0.8, −1.2, 5.5, 15.2, −2.2, 11.0 |
| jackknife σ | 3.5, 3.9, 5.5, 7.7, 9.5, 12.1, 18.3 \| 2.1, 2.6, 3.5, 6.0, 6.1, 9.8, 12.2 |
| B (canonical; alt the same) | 0.04 … 0.00 \| 0.03 … 0.00 |
| colour-split ΛCDM | −4.2 … −10.3 \| 1.4 … 8.0 |
| colour-blind ΛCDM (Moster) | 4.9 … 22.2 \| 6.9 … 26.6 |

**Per class** (7 bins, Hartlap p = 7):

| class | B | colour-split ΛCDM | colour-blind ΛCDM |
|---|---|---|---|
| late | 13.4 (p = 0.062) | 21.8 (p = 0.0027) | 25.2 (p = 7 × 10⁻⁴) |
| early | 6.5 (p = 0.48) | 5.1 (p = 0.65) | 55.0 (p = 1.5 × 10⁻⁹) |

**The mass-split amplitude** (R2b: log10 of the ratio of pair-weighted sums over K1):

| class | data | B | colour-split ΛCDM |
|---|---|---|---|
| late | −0.06 ± 0.08 dex | +0.00 | −0.20 |
| early | +0.03 ± 0.03 dex | +0.00 | +0.06 |

## Controls

- **C1:** the per-lens sums, summed by patch and class, reproduce the June sums to 3 × 10⁻¹¹.
- **C2:** the mass and redshift halves partition each class exactly. The median splits are log M_gal 10.448 (late) and 10.810 (early).
- **C3:** with the full-class masks, the model machinery reproduces CFG61's law stacks and CFG67's ΛCDM stacks exactly.
- **C4:** 200 random within-class halvings give a mean Hartlap χ² of 13.69 against 14, so the covariance is calibrated.
- **MUTATE:** it injects the colour-split ΛCDM's hi/lo contrast into the data: ×0.56–0.81 per bin for late types, ×1.14 for early types. B's law then fails at 33.3/14 (p = 0.0026), so the test can see ΛCDM's predicted mass dependence.

## Caveats

- **The split is coarse:** one median split per class.
- **The weighting differs:** the model stacks weight lenses by M_gal, not by source pairs.
- **Both models' absolute profiles fail** in this machinery (CFG67 H3). The difference statistic cancels part of that.
- **The power between B and colour-split ΛCDM is marginal (8.8).** The colour-blind rejection is the robust part.
- **It depends on CFG67's Moster relation,** as that lane coded it.

## Disclosures

- Before the criteria were frozen, the June memo `agentZ_second_variable.md` was read. It found the same absence of within-class mass dependence in coarse super-bins.
- **R2 as frozen** (a per-bin log ratio) is undefined where a noisy K1 bin's jackknife ESD goes negative: the low-mass late half's last bin has ESD 4.4. It is kept as it fell, with σ = nan.
- **R2b** was added after the first run, reported only. Every other line of both logs is unchanged apart from timing.

## Data requirements (not in git)

- `real_research/data/lensing_rar/cfg110_perlens.npz`, written by the stage from the KiDS-1000 SOM-gold catalogue.
- `lr_lenses.npz` and `lr_esd_jackknife.npz`.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
