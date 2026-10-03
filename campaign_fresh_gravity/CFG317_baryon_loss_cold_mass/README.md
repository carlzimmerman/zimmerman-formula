# CFG317 — does the cold component keep the collapse mass of a system's ORIGINAL baryons? Tested with the only non-dynamical baryon-loss estimator on disk: NOT SUPPORTED

> κ = ½ is FITTED. The cold component is collisionless and **its mass is still required**; no dark-matter particle is added. Nothing here says the theory is closed or that the data favour the framework.

- **Criteria:** `FROZEN_CRITERIA.md`, committed before any new score (**c29d82477**).
  - One plumbing prototype was run before freezing (three global R values, timing only); its numbers are disclosed in section 9 of the criteria.
- **Scripts:**
  - `cfg317_baryon_loss.py`, about 6 min. Main run: 7/10 checks pass, exit 1 (T1, T3, C2 fail). `MUTATE=1`: 7/11, exit 1; its MUTATE check passes.
  - `cfg317_posthoc.py`, about 1 min, labelled POST HOC; no frozen verdict depends on it. 2/2 reported rows.
- **Outputs:**
  - `cfg317_baryon_loss.out` / `_results.json`;
  - `cfg317_baryon_loss_MUTATE.out` / `_results.json`;
  - `cfg317_posthoc_POSTHOC.out` / `_results.json`.
- **Method:** CFG313's harness (CFG45 / CFG58 / CFG55 / CFG111 / CFG39 behind it) is exec'd read-only. The only change is the native hook: M_c = R × M_b,now / f_b, where R = M_b,init / M_b,now. Nothing was downloaded and no other lane's file was written.

## Bottom line

1. **The data need very different retention factors for the two red tiles.** The request's "about 7×" is CFG313's minimum switch-on margin, which applies at elliptical masses only.
   - **Ultra-faints:** log R_need = 3.65 (R ≈ 4,500; 1σ range 1,100–45,000; gate passes for R ≈ 280 to 4e5).
   - **SLUGGS:** R_need ≈ 17–28 (V1, by mass route).
2. **On disk, an independent estimator exists only for the dwarfs.** It is the leaky-box effective yield from stellar [Fe/H] and HI.
   - It gives R_ind ≈ 117 for the ultra-faints, 30 for the MW classicals, 22 for the M31 dwarfs and 6 for the gas-rich field dwarfs.
   - The ultra-faints fall short of their need by 1.6 dex (×38). Every satellite population's R_ind lies below the R at which its statistic starts to move.
   - **The re-score with R_ind therefore moves no tile.** Both red tiles stay red: the ultra-faints have no estimator large enough, and SLUGGS has no estimator on disk at all.
3. **The frozen correlation test T2 passes (ρ +0.63, p 1e-4), but post hoc that pass is entirely the common dependence on baryonic mass.**
   - At fixed mass the partial correlation is +0.01 (p 0.45).
   - log M_b alone correlates with R_need more strongly (ρ +0.74) than R_ind does.
   - Read correctly, the metallicity says every dwarf lost most of its baryons: M31 and LV dwarfs included, not only the ultra-faints.
4. **Decision under the frozen rule: NOT SUPPORTED** in all four footing × profile combinations (T1 and T3 fail). The hypothesis remains UNTESTED for the ellipticals, which need data not on disk (listed below).

## (A) R_need: the retention factor the data require (log₁₀ R; zero crossing of the population statistic)

| population | z at R = 1 | V1 canonical | V1 alt | V2 canonical | V2 alt | onset (V1 can.) | gate interval (V1) |
|---|---|---|---|---|---|---|---|
| P1 MW ultra-faints | +3.77 | **3.65** | 3.64 | 3.72 | 3.74 | 2.65 | 2.45–5.60 |
| P2a MW classical | +0.32 | 2.27* | 2.26 | 2.32 | 2.29 | 2.20 | 0–2.75 |
| P2b M31 Collins+13 | +0.78 | 2.46 | 2.46 | 2.55 | 2.54 | 2.30 | 0–3.55 |
| P2c M31 LVD | +0.60 | 2.33 | 2.37 | 2.46 | 2.45 | 2.15 | 0–2.60 |
| P2d LV field | −0.60 | 0 (no extra mass needed) | 0 | 0 | 0 | 2.10 | 0–2.45 |
| P5 SLUGGS h50 | +3.28 | **1.24** | 1.25 | 1.42 | 1.42 | 0.95 | 1.15–1.35 |
| P5J SLUGGS JAM γ = 3 | +3.99 | **1.41** | 1.44 | > 6 † | > 6 † | 0.95 | 1.30–1.60 |
| P5S SLUGGS SLUGGS masses | +2.75 | 1.24 | 1.25 | 1.70 | 1.67 | 0.95 | 1.15–1.35 |
| P5L SLUGGS JAM, literature γ | +3.60 | 1.32 | 1.35 | > 6 † | > 6 † | 0.95 | 1.25–1.50 |
| P6 X-ray ellipticals | +1.70 | 1.60 | 1.60 | 1.63 | 1.64 | 1.00 | 0–2.95 |
| SPARC control | — | R_max: both clauses hold up to log R = 1.05 (V1) / 1.15 (V2) | | | | | |

**Table notes.**
- Onset is the first grid R at which the statistic moves; below it the rule is the bare law.
- \* Post hoc, bisection puts P2a's crossing at 2.284, against the frozen linear interpolation's 2.265 (see C2).
- † Under V2 the two JAM routes are not monotone in R and never reach zero. Their gates pass only in R windows of about 10^2.1 to 10^5.7 (non-contiguous for γ = 3).
- **R_ΛCDM (reported).** The committed ΛCDM collapse masses imply median log R = 4.26 (ultra-faints), 2.7 (classicals and M31), 2.24 (field), 1.13 (SLUGGS) and 1.35 (X-ray).
- **The ultra-faint need sits about 0.6 dex below R_ΛCDM.** That is the CFG42 overshoot (−0.059 dex at R_ΛCDM).

**The elliptical need versus the spiral ceiling.** SLUGGS needs R ≈ 14–40. SPARC's spirals tolerate at most R ≈ 11 (V1). So a retention factor could only fix SLUGGS if it is specific to the ellipticals and absent from the spirals. That is structurally what the hypothesis claims, but nothing on disk measures it.

## (B) R_ind: the estimator and what is not on disk

**B1, the leaky-box effective yield** (instantaneous recycling, outflow ∝ SFR, no inflow; η solved per object so that the model's mean stellar log Z matches the observed mean [Fe/H]).
- Yield: log y_Fe/Z_Fe,⊙ = −0.2, with a bracket from −0.5 to +0.1.
- Data: [Fe/H] from the LVD tables and Collins+13; HI from the LVD.
- R_ind = [(1 + η) M★ + M_g] / (M★ + M_g).

| population | median log R_ind (nominal) | ± boot | n with [Fe/H] | yield −0.5 / +0.1 |
|---|---|---|---|---|
| MW ultra-faints (31 + 9 limits) | **2.07** | 0.02 | 39 of 40 | 1.77 / 2.37 |
| MW classical | 1.48 | 0.13 | 12 of 14 | 1.18 / 1.78 |
| M31 Collins+13 | 1.35 | 0.08 | 14 of 14 | 1.05 / 1.65 |
| M31 LVD | 1.35 | 0.06 | 29 of 34 (Collins fallback for 10) | 1.05 / 1.65 |
| LV field (gas-rich) | 0.77 | 0.12 | 12 of 13 | 0.44 / 1.09 |

**What B1 cannot see.** B1 sees gas that formed stars and was then lost. It cannot see gas removed unprocessed: photo-evaporated at reionization, or stripped wholesale. For the scenario the hypothesis names for the ultra-faints, it is therefore a **lower bound**. In that reading the data are consistent with it: R_need ≥ R_ind for 73% of objects. But the bound predicts nothing about the missing factor of about 40.

**Not on disk (branches stopped; no download made).**
- **SFH quench epochs:** Weisz+2014 ApJ 789, 147, Table 2 (VizieR J/ApJ/789/147, about 20 kB); Brown+2014 ApJ 796, 91 (about 2 kB). The LVD `age` column is empty.
- **Hot-gas masses for the X-ray ellipticals:** the gas-density and temperature profile fits of Humphrey+2006 (arXiv astro-ph/0601301 source, about 1 MB), or Babyk+2018 ApJ 857, 32 (about 20 kB).
- **Stellar metallicities for SLUGGS:** McDermid+2015 MNRAS 448, 3484 (ATLAS3D XXX, VizieR J/MNRAS/448/3484, about 100 kB).
- **Against interest, recalled and not computed:** massive ellipticals have [Z/H] ≈ 0 to +0.3. By B1's own logic that would make them LOW-loss (R_ind ≈ 1–2), the opposite of what SLUGGS needs. Only that table can settle it.

## (C) The frozen tests (V1 canonical primary; all four combinations agree)

| test | result | verdict |
|---|---|---|
| T1 sign | ultra-faints need large R and get large R_ind (ok). SLUGGS, X-ray and SPARC have no R_ind. Collins, M31 LVD and LV field are labelled LOW, but R_ind is "large" (22, 22, 6). | **FAIL** (T1′ restricted to populations with an R_ind also fails; the relative order HIGH > LOW holds) |
| T2 correlation | per object ρ +0.629, p 1e-4 (n 97); population ρ +0.67 | PASS (frozen); **post hoc, a mass correlation** |
| T3 ratio | median log(R_need/R_ind) **+0.98 dex** (std 0.80); ultra-faints +1.58, MW classical +0.78, Collins +1.11, M31 LVD +0.98, field −0.77 | **FAIL** (+0.68 even at the favourable yield +0.1) |
| **Decision** | | **NOT SUPPORTED** (V1/V2 × canonical/alt, and at both yield ends) |

**Post hoc (`cfg317_posthoc.py`): is T2's pass real?**
- log R_need correlates with log M_b at ρ −0.74, and log R_ind with log M_b at ρ −0.84.
- **The partial ρ at fixed mass is +0.011 (p 0.45).**
- A mass-only proxy, −log M_b, gives ρ +0.74, higher than R_ind's +0.63.
- Within the ultra-faints alone, ρ is +0.25 (p 0.08).
- So T2 measures the fact that both quantities fall with mass, for unrelated reasons:
  - R_need is either 0 or at least the switch-on factor, which grows as the law's phantom per baryon grows at low mass;
  - R_ind follows the mass–metallicity relation.
- It is not evidence that baryon loss sets the cold mass.

## (D) Re-score with M_c = R_ind × M_b / f_b

- **No tile moves, under V1 or V2, at any of the three yields.** The largest shift in any statistic is 0 dex at the nominal yield and 3e-4 dex at +0.1.
- **The ultra-faint z moves; its offset does not.** z goes from +3.77 to +2.98 (V1 canonical), and to +2.18 / +2.25 at the favourable yield. The offset stays +0.325 dex.
  - The drop comes from the frozen collapse-floor error term. Its ×10 variant pushes some ultra-faints over their switch-on, which inflates the error.
  - It is error inflation, not closure, and still a FAIL.
- **Everything else is as in CFG313.**
  - SLUGGS (all routes) stays red, at R = 1, because it has no estimator.
  - The classicals, M31, the field dwarfs, the X-ray ellipticals and SPARC stay green.
- Five R-lookup key collisions (identical committed M★: Tri II/Tuc III; Collins And V/XXIII, And XVII/XXVIII; Perseus I/Draco) were resolved by the declared mean. All are far below switch-on, so they are immaterial.

## Controls

- **C1 passes:** at R = 1, 62 values reproduce CFG313's committed native table exactly (deviation 0).
- **C2 FAILS, kept.** The identity control re-runs at R = R_need. Eleven populations give |statistic| ≤ 0.0015 dex; MW classical gives +0.0060 against the 0.005 tolerance. The cause is the frozen linear interpolation on a 0.05-dex grid across a median that jumps. Post hoc, bisection moves P2a's R_need by +0.019 dex. P2a is unlabelled, and the shift is immaterial to T3's 0.3 dex.
- **C3 passes:** the estimator's closed form matches quadrature (1e-15), root residuals are ≤ 4e-14, R_ind ≥ 1 everywhere, and the closed box returns η = 0.
  - *Disclosed:* in the first main run this control's last clause was coded against the wrong case and failed. It was fixed to the frozen case before any interpretation; no estimator value changed.
- **C4 passes.** This is the positive control on synthetic data: R_need,syn = R_ind × 10^N(0, 0.15) gives T2 p 1e-4 and T3 +0.045, i.e. the machinery can say SUPPORTED. Shuffled, T2 fails (p 0.06).
- **MUTATE** shuffles R_ind across satellites (seed 317). T2 fails (ρ −0.22, p 0.99) and T1 fails, so the MUTATE check passes. Because the main run already fails T1, the MUTATE is uninformative for T1; C4 carries the discrimination.
- **PF1 (pre-flight prediction) passes:** every population median R_ind is below its onset, no object's R_ind exceeds its own analytic switch-on, and no satellite tile moves. PF2–PF4 also came out as predicted (ultra-faint ratio +1.6 dex; LOW-labelled dwarfs "large"). PF4's "weak correlation" came out as a strong but mass-driven one.

## What sets the amount of cold mass? What this lane can and cannot say

- **Under B's rule as written, the data fix only a lower edge:** no cold mass beyond the law until R passes switch-on, which is about 10^2.1–10^2.7 for dwarfs and about 10^1 for ellipticals.
- **The only independent clock on disk, metallicity, cannot supply the ultra-faints' factor.** It is about ×40 short at face value.
- **It does not single out the ultra-faints or the M31/LV dwarfs:** every dwarf shows a large yield deficit, smoothly with mass.
- **The ellipticals remain the open half.** Their hot gas or stellar metallicity (the tables above) would decide whether they are high-loss in a non-dynamical sense. The recalled expectation runs against the hypothesis.
- **The CFG34 group/cluster correlation (ρ −0.96) is partly built in** (M_B ∝ M_b in the cosmic-share branch) and is not independent support.

Nothing here closes either red tile, and nothing says the theory is closed.
