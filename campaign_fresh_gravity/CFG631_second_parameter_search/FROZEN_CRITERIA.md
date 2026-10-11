# CFG631 FROZEN CRITERIA: what besides the law sets a galaxy's cold energy? (one multiplicity-corrected multi-property search)

Committed alone, before any residual-versus-property or lensing-versus-property statistic is computed. Step 0 (residual-free
inventory and pre-flight) is in commit defe92ee8 (`cfg631_inventory.*`, `cfg631_preflight.*`, `cfg631_common.py`).

**Already seen (disclosed).** CFG583 (SPARC f_gas, f_bul: no relation, underpowered), CFG584 (WALLABY mass slope −0.07, Z −2.0,
CONTRADICTED vs SPARC's post-hoc +), CFG534/537 (SPARC early-type outer excess, not replicated in WALLABY), CFG585/586/589 (KiDS f30
early types: redder at fixed M* carry more K9 excess, D ≈ +0.86–0.94, Z +2.65; not environment; jackknife errors ~18–20% too small).
So: the disc single-property results and the KiDS age signal have been seen. **The age signal is a pre-declared CONFIRMATORY
target, not a discovery.** Nothing else in this lane has been looked at.

Law: g = ν(g_bar/a₀) g_bar with the repaired ν_mono (CFG4_common.nu_mono). κ = ½ is fitted. Footings 9.36e-11 (canonical) and
1.13e-10 (alt) are never pooled; every verdict needs both. Υ fixed (SPARC Υ_d 0.5, Υ_b 0.7; WALLABY Υ_K 0.6), as in CFG537.

## 1. Residuals
- **Discs, primary (Δ_out):** CFG537's statistic, from `cfg537_wallaby.py` executed unedited up to its forecast section (functions
  `sparc_rows`, `residual_rows`), with that namespace's kernel `nu` replaced by the repaired ν_mono. Δ_out is the error-weighted
  mean of log(g_obs/g_law) over rings with R ≥ 3 R_d (≥ 2 rings). Positive means the law under-predicts (excess). SPARC: 128 galaxies
  with an outer band; WALLABY DR2: 85.
- **Discs, variant (reported only):** SPARC g_bar < a₀/3 mean residual (CFG583 definition, ≥ 3 points).
- **KiDS, primary:** CFG531's ε (fractional extra enclosed mass over the law + baryons prediction) in band K9; K-in is reported.
  The estimator is `cfg585_age.py`'s head executed unedited (CFG531 estimator, CFG529 f30 environment; constructions A and B;
  error = max(jackknife, quadrature), CFG531's rule).

## 2. Properties (complete list)
Control in every disc model: log M_b (its coefficient is reported as the "gravity strength / mass" term).
- **SPARC core (all 128):** f_gas = 1.33 M_HI/M_b; bul = 1 if f_bul > 0.05 (17 galaxies); log Σ_* = log(0.5 L[3.6]/2πR_d²);
  T (Hubble type); inclination; HF = 1 if the distance is Hubble flow (fD = 1).
- **SPARC add-ons, each in core + itself on its subsample:** colour = B_T⁰ − [3.6] (RC3, 30″; 78 galaxies; age/stellar-population
  proxy); env = log(1+δ) from 2M++ (109).
- **WALLABY core (all 85):** f_gas; log Σ_* (0.6 L_K/2πR_d²); T (RC3); inclination. **WALLABY add-on:** W1 − W2 (AllWISE; 84).
- **KiDS f30 early types (26,568 with all five finite):** u−r (age), r−Ks (metallicity/dust), log sSFR (LePhare), photo-z, CFG509
  companion count `meas` (environment). Each property's **partial residual** = OLS residual on [5 log M* quintile dummies, log M*,
  the other four properties]; HIGH/LOW = top/bottom tertile of the partial residual; D_j = ε_HIGH − ε_LOW (cfg631_common.kids_props).
- Not on disk for any sample: metallicity, H₂, ages. Not used: SPARC SFR (23 galaxies only). Nothing is downloaded.
- Category map for the reading: composition = f_gas, bul, T, r−Ks; time = colour, u−r, sSFR, W1−W2 (weak); gravity strength =
  log Σ_* and the mass coefficient; systematics = inclination, HF, photo-z; environment = env, `meas`.

## 3. Models and multiplicity (discs)
- OLS, equal weights: Δ_out = a + b(log M_b − 10) + Σ c_j x_j, all core properties jointly; add-ons as above. Statistic: the
  classical OLS t of each c_j.
- **Permutation max-T (Westfall–Young single step):** 5000 draws (seed 631); in each draw Δ_out is shuffled within log M_b quintiles
  in SPARC and in WALLABY (the same permutation for both footings), every model is refitted, and max|t| is taken over the whole
  family: SPARC 8 properties + WALLABY 5 properties × 2 footings = 26 t's. Family-wise p_j = P(max|t|_null ≥ |t_j|).
- **DISCOVERED** in a sample: family-wise p < 0.05 on both footings with the same sign.
- **Discovery/confirmation split (symmetric, chosen from the forecast):** the four shared properties (f_gas, log Σ_*, T, inclination)
  can be discovered in either sample. The other sample confirms with a same-sign, one-sided, within-sample permutation p < 0.05 on
  both footings, Holm-corrected over the properties carried into it. **REPLICATED** = discovered in one, confirmed in the other.
  SPARC-only bul, HF, env: DISCOVERED → "UNCONFIRMABLE ON DISK". SPARC colour: confirmation = the KiDS age result (sign:
  redder → more excess). WALLABY-only W1−W2: discovery only.
- **Omnibus:** per sample and footing, permutation F test (same shuffles) that all core coefficients are 0 beyond mass.
- **Verdict (discs):** SECOND PARAMETER FOUND iff ≥ 1 property is REPLICATED. DISCOVERY ONLY iff something is discovered but none
  replicate. NO SECOND PARAMETER DETECTED iff nothing is discovered AND the omnibus p ≥ 0.05 on both footings in both samples. Otherwise
  INCONCLUSIVE. Each coefficient is reported in "dex across the property's 16–84 range" (binary: the category difference) with a
  95% interval, so a null is stated as an upper limit.

## 4. KiDS (age confirmatory; other properties exploratory)
- D_j in K9 (primary) and K-in, four cells (A/B × canonical/alt), with CFG531's error rule. T_j = mean over the four cells of Z_j.
- **Null:** 200 draws (seed 6310); in each draw the rows of the partial-property block are permuted jointly within log M* quintiles
  among the 26,568 lenses, the tertiles are recut, and all five D_j are recomputed in all cells. Family-wise p_j =
  P(max_k |T_k|_null ≥ |T_j|) for the exploratory family (all five). Age one-sided p = P(T_ur,null ≥ T_ur).
- **Age verdict (u−r):** AGE CONFIRMED iff the one-sided p < 0.05 AND D > 0 in all four cells AND D ≥ 0.5 × CFG585's D(K9) in each
  cell (+0.941 / +0.862 / +0.938 / +0.859 for A-can / A-alt / B-can / B-alt). Sub-label STRENGTHENS if D > CFG585's D in all four
  cells, else HOLDS. AGE FADES iff D < 0.5 × CFG585's D in all four cells. NOT CONFIRMED otherwise.
- **Other KiDS properties:** ASSOCIATED iff family-wise p < 0.05 with the same sign in all four cells (exploratory; no confirming
  sample on disk).
- Reported, no verdict weight: u−r partialled only on M*, photo-z, `meas` (sSFR and r−Ks partly track age, so the primary may
  over-control); companion λ of the u−r HIGH and LOW groups (CFG509 stat); the null's |Z| ≥ 2 rate.

## 5. Power forecast (from step 0, no residuals)
σ_r = 0.130 dex (the CFG584 record); effect = 0.10 dex across the 16–84 range; discovery |t| ≈ 2.89 (Bonferroni stand-in for the max-T).
- SPARC discovery power at 0.10 dex: f_gas 0.08, bul 0.32, log Σ_* 0.15, T 0.10, inclination 0.79, HF 0.76, colour 0.05,
  env 0.78. MDE80 0.10–0.31 dex. The composition/structure terms are collinear with mass (VIF 5–6), so **SPARC cannot discover a
  0.1 dex composition, size or colour effect.**
- WALLABY discovery / confirmation power at 0.10 dex: f_gas 0.41/0.85, log Σ_* 0.28/0.75, T 0.82/0.98, inclination 0.47/0.88,
  W1−W2 0.73/0.97.
- KiDS (σ_D ≈ 0.34 × 1.2 = 0.41): if the age effect is CFG585's size (D ≈ 0.9), P(Z ≥ 2) ≈ 0.58. A 0.1 dex mass difference (D ≈ 0.26)
  has P ≈ 0.09. **LOW POWER for anything below CFG585's amplitude.**

## 6. Controls
- C1: with the exponential kernel the executed CFG537 functions reproduce CFG584's WALLABY slope (−0.072 can / −0.069 alt, ±0.002).
- C2: |median Δ_out| < 0.1 dex in both samples and footings; the kernel swap's maximum |ΔΔ_out| is reported.
- C3: the CFG585 head reproduces CFG585's D(K9, A, canonical) +0.9411 to 0.001 with its own OLD/YOUNG masks.
- C4: the u−r HIGH and LOW groups' median log M* agree within 0.05 dex.
- C5 (disc null calibration): over 200 datasets with Δ_out shuffled within mass quintiles (1000 inner draws each), the fraction
  in which any property reaches family-wise p < 0.05 is 0.05 ± 0.035.

## 7. MUTATE
- **Disc injection (CFG631_MUTATE=1):** Δ_out += 0.20 dex × (log Σ_* − median)/span₁₆₋₈₄ in both samples and footings. It passes iff
  log Σ_* comes out REPLICATED and the coefficient shift equals the injection (OLS linearity, 1e-9). Outputs `*_MUTATE.*`.
- **KiDS shuffle:** the 200-draw null above is the shuffle control. Its |Z| ≥ 2 rate is reported (a calibration of the jackknife errors).
- **KiDS known-signal recovery:** raw log M* tertiles (no partialling) among the same lenses must give D > 0 with Z ≥ 2 in all
  four cells (the recorded early-type mass trend, CFG531). If this fails, the KiDS part has no teeth.

Rules: no ΛCDM or standard-MOND yardstick enters a verdict (the CFG529 environment and the SHMR inside CFG531's own-profile are inherited
lane machinery, as in CFG585/586). "Cold energy". Its mass is still required. Not a closed theory. One process, nice 10, < 1.5 GB.
