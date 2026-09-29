# CFG40 — the top of the disk mass function: Ogle+2019's super spirals against B's law and rule

Script: `CFG40_super_spirals.py`, about 5 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Observed speeds are multiplied by 0.5, and H1 and H2 both fail (rc = 1).
- The main run exits 1: **H2 failed as declared**, at the margin (2.06σ against a 2σ threshold).

## Question

B's derived cold-mass rule (CFG35–CFG39) leaves star-forming disks on the bare law. SPARC's heaviest spirals reach log M_* ≈ 11.4, and nothing in the campaign had confronted B with the rarer disks above that.

Ogle+2019 (arXiv:1909.09080) measured Hα rotation curves of 23 super spirals (log M_* 11.13–11.74) and reported that the baryonic Tully–Fisher relation breaks above ≈ 340 km/s, "inconsistent with MOND". That claim compares v_max with the asymptote v⁴ = G M_b a₀. But their speeds are **maxima at 14–54 kpc**, where a = v²/r is 0.6–2 a₀: the transition regime, where the law sits above the asymptote. B has to be tested at the radius.

## Data

`real_research/data/ogle2019_super_spirals.tsv` (23 rows, transcribed by script from the arXiv LaTeX source, e-print 3,957,201 bytes; fetched with the owner's approval).
- v_max ± dv at radius r (Hα long-slit, SALT and Hale), R_d and inclination from Simard+2011, M_* from WISE W1 with a constant M/L = 0.6, M_gas from a WISE-W3 Schmidt-law estimate (no HI could be measured).
- The sample is selected on luminosity and size, not on speed, so a velocity-selection bias does not enter. (It does for Di Teodoro+2023, whose sample required v > 300 km/s; that is CFG41.)

## Method (declared before the first run)

- CFG36's machinery exec'd read-only: the Mandelbaum blue collapse masses, the conservation form, x_e = 0.40, ν_mono, both footings.
- Baryons in an exponential disc of scale length R_d. The Newtonian field is Freeman's (headline); a point mass and the spherical enclosed mass bracket it.
- The law is g = ν(g_N/a₀) g_N. The rule adds f_ex (1 − f_b) G M_NFW(<r)/r² from the blue collapse mass.
- Colour is from sSFR (> 10⁻¹¹ / yr is blue). All 23 are blue.
- Offset = log(v_obs / v_pred). Errors: the galaxy-to-galaxy scatter, plus a floor in quadrature from the baryon model, the stellar mass (±0.2 dex) and the gas mass (±0.3 dex). The inclination error is taken as 5° (the paper quotes none).
- **H1:** the bare law fits, |mean| < 2σ.
- **H2 (headline):** B fits, with |mean| < 2σ, |slope against log M_b| < 2σ and |mean of the nine fastest (v > 340)| < 2σ.

## Results

**Controls.**
- C1: the table checks out (23 rows; the fastest galaxy at 568 ± 16 km/s at 41 kpc; every sSFR > 10⁻¹¹).
- C2: the Freeman field reproduces the point-mass limit (1.0018 at 50 R_d), and its peak sits at 2.15 R_d.

| footing | statistic | law = B (f_ex = 0 in all 23) |
|---|---|---|
| canonical | mean log(v_obs / v_pred) | **+0.107 ± 0.075 (1.42σ)** |
| canonical | slope against log M_b | **+0.194 ± 0.100 (1.95σ)** |
| canonical | the nine fastest | **+0.170 (2.06σ)** |
| alt | mean | +0.092 ± 0.074 (1.25σ); fastest nine +0.156 (1.92σ) |

**H1 passed:** the bare law fits at 1.4σ. **H2 failed, marginally:** the fastest-nine clause is at 2.06σ, and the slope is at 1.95σ, 0.05σ short of failing too. Every clause leans the same way. The super spirals rotate faster than the law, and more so at higher mass.

**Where it comes from.**
- The offsets run from −0.03 to +0.31 dex. 21 of 23 are at or above the law, 11 are above +0.10 dex, and 4 are above +0.20 dex: 2MFGC 08638 (+0.31), OGC 0139 (+0.31, but at ± 90 km/s), 2MFGC 12344 (+0.26; 568 ± 16 km/s at 41 kpc against the law's 313) and 2MASX J11232039+0018029 (+0.21). The two below the law are OGC 0926 and 2MASX J22073122-0729223 (each about −0.03).
- The floor is 0.075 dex, mostly the 0.2-dex stellar-mass systematic. On the galaxy-to-galaxy error alone (0.020 dex) the mean offset would be 5σ. The floor decides the reading. This is the post-hoc scale, not a declared result.

**The rule adds nothing.** f_ex = 0 in all 23. The blue collapse masses (M_200m ≈ 6 × 10¹² at log M_* 11.7) are smaller than the law's own phantom at these baryon masses (≈ 10¹³), so the cold fluid is fully consumed building the phantom. That holds at the +1σ collapse masses. (Reported, R2.) With the **red** relation, for scale, the mean offset would be −0.001. But these galaxies are star-forming (sSFR ≈ 10⁻¹⁰·⁷ / yr), so the red relation does not apply to them.

**What Ogle's "break" is.** In the paper's own comparison (the asymptote) the mean offset is +0.144 and the nine fastest are at +0.191. Evaluating the law at the radius, where the data actually are, removes about a quarter of that: the offsets fall to +0.107 and +0.170. The rest remains.

## Independent referee (2026-09-28)

A hostile re-implementation (own code, own arithmetic) reproduced every headline number: mean +0.107, nine fastest +0.170, slope +0.194, alt +0.092 / +0.156, and the asymptotic comparison +0.144 / +0.191. It found no unit, sign or double-counting error. It found that **the reading depends on the baryon structure model**:

| model | mean | nine fastest |
|---|---|---|
| Freeman disc (declared headline) | +0.107 | +0.170 |
| point mass | +0.059 | +0.113 |
| spherical enclosed | +0.141 | +0.201 |

- The nine-fastest clause fails at 2.06σ only under the declared Freeman model. Any centrally concentrated correction (a bulge, which massive spirals have) moves g_N toward the point-mass value and removes the failure. The lane's floor takes only half the spread of the means.
- The offset correlates at −0.68 with r/R_d (+0.155 for r < 2.2 R_d, +0.054 beyond) and at +0.38 with inclination. Simard R_d values for the giants look doubtful (47 kpc for 2MFGC 08638). The signal sits in the galaxies with the least reliable structure inputs.
- The mean shifts by 0.033 dex per 0.1 dex of stellar mass (M/L_W1 = 0.5 gives +0.130). The maximum of a noisy curve is biased upward by about 0.01 dex, not removed here.

**So the marginal fail is a statement about the structure model and the stellar-mass floor, not a robust failure.**

## What changed after the first MUTATE run (disclosed)

The MUTATE control first multiplied the speeds by 0.7. H2 **passed** under it (mean −0.048 ± 0.075), because the floor is too large for a 0.155-dex error to bite. That run also exposed the unmutated offsets (mean about +0.11, slope unchanged) **before the main run**. No hypothesis, clause or threshold was changed. Only the control's strength was raised to 0.5, and under it H1 and H2 both fail.

## Standing

**B fails its declared test on the most massive star-forming disks, but only at the margin (2.06σ on the nine fastest, 1.95σ in the mass trend, 1.4σ in the mean), and only under the declared disc model (the referee's point-mass model gives +0.113 for the nine fastest, which passes).** It is not an established failure: the 0.2-dex stellar-mass floor and the missing inclination and HI data limit it. It is a consistent direction, and the rule cannot cure it, because the measured blue collapse masses are consumed by the phantom.

**What comes next.** Di Teodoro+2023 measured extended HI curves for 15 spirals of similar mass and report no break in the Tully–Fisher relation. Their tracer (HI, flat part) and selection (v > 300 km/s) differ from Ogle's (Hα maxima, luminosity-selected), so whether the two agree is untested. CFG41 scores B on them with the same method.

Nothing here says the theory is closed.

**Update (CFG56):** with Simard+2011's measured bulge-to-total ratios the marginal fail survives (nine fastest +0.164, 2.34σ). The structure-model dependence noted above is not a way out.
