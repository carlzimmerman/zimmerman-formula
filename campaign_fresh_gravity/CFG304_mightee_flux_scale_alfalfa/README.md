# CFG304: which MIGHTEE-HI flux scale is right? The single-dish ALFALFA fluxes sit above both the catalogue and the raw cubes

*A flux-calibration check, not an a₀ measurement. Criteria frozen in `FROZEN_CRITERIA.md`, committed as `336b36f8f` before any per-galaxy flux was read. κ = ½ is FITTED. No knob scans, no downloads, and no other lane's file was edited. At z ≤ 0.05 nothing here can separate FLAT from a₀ ∝ H(z).*

## Bottom line
1. **Frozen decision: "neither".** The Arecibo single-dish fluxes are higher than both MIGHTEE scales. The primary set is ALFALFA code 1, with the OPT conversion, N = 15:
   - **catalogue / ALFALFA: median log ratio −0.195 dex** (bootstrap 68 % −0.250 to −0.156; 95 % −0.262 to −0.137). The catalogue holds about 0.64 of the single-dish flux.
   - **cube / ALFALFA: median log ratio −0.308 dex** over the 7 CFG302 frozen detections that match (68 % −0.383 to −0.292; 95 % −0.412 to −0.221). The cube holds about 0.49 of the single-dish flux.

   Both votes agree with the primary: confusion-cleaned code 1 gives −0.175 / −0.383 (N 10 / 3) and the brief's REST conversion gives −0.214 / −0.328. The reported variants agree too: codes 1+2 −0.159 / −0.314 (N 23 / 13), RADIO, and matching on ALFALFA's optical-counterpart positions. All of them say "neither", and every decision row of the frozen rule is labelled "firm".
2. **The catalogue is closer to the single-dish scale than the cube is.** On the same 7 galaxies the cube sits only **−0.117 dex** below the catalogue; CFG302 measured −0.30 over its 58 detections. **The cube-scale hypothesis points the wrong way.** The single dish asks for *more* HI than the catalogue has, not less. The chart's hollow diamond (2.29 × 10⁻¹⁰, the cube scale) is therefore not supported by the independent flux.
3. **The matches are real.** W50 catalogue/ALFALFA is **+0.000 dex** on code 1 (robust scatter 0.037), and the median |Δcz| is 11.8 km s⁻¹. 200 shuffles at 10′ give 0.275 matches on average.
4. **What it would mean for CFG301 (reported only; CFG301 was not re-run).** Suppose ALFALFA's scale applied to CFG301's galaxies. Their HI masses would then rise by about 0.2 dex, and CFG301's pooled a₀ (1.046 × 10⁻¹⁰) would **fall**. The figure comes from interpolating CFG301's committed baryon-band rows at τ = +0.195:
   - **(A)** total-baryon reading (how the band rows are defined): **a₀ ≈ 5.97 × 10⁻¹¹** (68 % 4.99–6.76 × 10⁻¹¹);
   - **(B)** gas-only reading (f_g = 0.70; an HI error moves only the gas): **a₀ ≈ 7.00 × 10⁻¹¹** (68 % 6.08–7.60 × 10⁻¹¹).

   Post hoc, the 7 matched pairs that pass CFG301's own frozen cut give R_cat = −0.159, so (A) 6.7 × 10⁻¹¹ and (B) 7.6 × 10⁻¹¹. **This is a signed systematic, not a measurement.** These are the 23 HI-brightest COSMOS sources at z ≤ 0.047, and CFG301's 47 galaxies reach z = 0.093, mostly beyond ALFALFA. Whether the offset carries over to them is an assumption.
5. **Chart note.** The hollow diamond's 2.29 × 10⁻¹⁰ is the −0.30 band row, which lowers stars and gas together. With only the gas lowered (reading B), the same cube-scale case would give **1.70 × 10⁻¹⁰**.

## Process (everything kept)
1. **Criteria** were committed as `336b36f8f` before any flux value was read. The disclosures are in the criteria's section 0: headers, documentation, CFG302's aggregate ratios, CFG301's band rows and gas fraction, and the orchestrator's count of 23.
2. **Dry run.** The script was first run on fabricated fluxes in a scratch folder, which is not part of the lane. Real positions, velocities, widths and frequencies were used. The flux columns were overwritten before saving, with ALFALFA set to the fake catalogue flux and the cube to half of it, and no real flux was printed. The pipeline returned "catalogue scale confirmed", MUTATE=b returned "cube scale confirmed" and MUTATE=a returned "neither", as built. That is the only place where the rule's ability to return each verdict was exercised.
3. **Main run, once,** then **MUTATE=a, b and c, once each.**
4. **Post hoc diagnostics** (`cfg304_posthoc.py`): the reading rules were written in the docstring before its first run. Run 1 is kept as `*_run1*`. Its PH0 demanded 1e-12 against a CSV written to 10 significant figures, so it failed at 2.6e-11; the tolerance is now 1e-9, and nothing else changed.
5. **Determinism:** all four modes and the post hoc script were re-run, and every JSON and CSV came out byte-identical. The `.out` files differ only in the runtime line.

## Results (main run, OPT conversion)
| set | N | R_cat median | 68 % | 95 % | N cube | R_cube median | 68 % | paired R_cube − R_cat |
|---|---|---|---|---|---|---|---|---|
| **C1 (primary)** | 15 | **−0.195** | −0.250..−0.156 | −0.262..−0.137 | 7 | **−0.308** | −0.383..−0.292 | −0.117 |
| ALL (codes 1+2) | 23 | −0.159 | −0.195..−0.137 | −0.250..−0.116 | 13 | −0.314 | −0.385..−0.292 | −0.197 |
| CLEAN-C1 (no MIGHTEE neighbour within 3.5′) | 10 | −0.175 | −0.225..−0.137 | −0.262..−0.109 | 3 | −0.383 | −0.412..−0.127 | −0.217 |
| CLEAN-ALL | 16 | −0.146 | −0.210..−0.120 | −0.262..−0.094 | 7 | −0.383 | −0.385..−0.314 | −0.217 |
| code 2 only | 8 | −0.120 | −0.159..−0.039 | −0.276..+0.038 | — | — | — | — |

- **Conventions** (C1, catalogue): OPT −0.195, REST −0.214, RADIO −0.231. No velocity convention closes a factor of 1.57.
- **Units check U1:** the catalogue's log M_HI equals log(49.7 D_L² S_HI) to a median of 0.0027 dex, which confirms S_HI is in Jy Hz.
- **Through the published masses (PH4):** MIGHTEE's log M_HI is **0.22 dex below** ALFALFA's logmhi for the same galaxies (C1). After removing R_cat and the distance term, the residual is +0.002 dex, so the mass and flux comparisons agree.
- **Beam-summed variant** (all MIGHTEE sources inside ALFALFA's beam and window): C1 −0.137, ALL −0.116. It over-counts where two neighbours are matched separately (for example J100048.1 and J100035.1, each summed into the other's beam). Even so, confusion does not close the gap.
- **Pull outliers > 3σ** (published errors): 10 of 15 for the catalogue on C1, and 6 of 7 for the cube. The published errors do not cover the offset.

## Controls
| control | result |
|---|---|
| K1 input sha256 | PASS |
| **K2** catalogue z_HI = ν₀/freq − 1 to ≤ 1e-5 | **FAIL, kept.** The catalogue publishes z_HI to 4 decimals (\|Δz\| ≤ 5e-5) and one row to 3 (MGTH_J100404.9+014303, Δz −3.6e-4, not matched), so the frozen tolerance was tighter than the published precision. No flux effect: the conversion uses freq_MHz, and using z instead would change it by ≤ 4e-5 dex. The matching cz moves by ≤ 15 km s⁻¹. |
| K3 CFG302's S_cat = catalogue S_HI | PASS (190/190, exact) |
| K4 U1 units | PASS (0.0027 dex) |
| K5 match quality | PASS (11.8 km s⁻¹, 14.6″) |
| K6 orchestrator's count | PASS (23 = 23) |
| **C-W50 (control i)** | **PASS: +0.000 dex** (N 15, scatter 0.037) |
| C-W50cube (sanity) | PASS: −0.025 dex (N 7) |
| **C-SHUF (control ii)** | **PASS:** mean 0.275 matches per shuffle; max 3, at the limit; zero matches in 152 of 200 shuffles |
| D-MIN | PASS (15 / 7) |
| **MUTATE=a** (catalogue × 0.5) | R_cat shifts by −0.30103 exactly (5.6e-17), PASS; R_cube unchanged, PASS. **"Decision differs" FAILS, kept:** the run went from "neither" to "neither" (−0.496 / −0.308). That check assumed the main run would confirm a scale. From a state where both ratios are already low, halving the catalogue cannot change "neither". The brief's expected flip to "cube scale confirmed" cannot happen under this rule, as the criteria noted before the run. |
| MUTATE=b (ALFALFA × 0.5) / MUTATE=c (× 2) | These flip tests are undefined from "neither", so they are reported only. b gives "undecided" (R_cat +0.107, R_cube −0.007); c gives "neither" (−0.496 / −0.609). |

Totals: main **9/10**; MUTATE=a **11/13**; b **9/10**; c **9/10** (K2 fails in every mode); post hoc **2/2** (run 1: 1/2).

**Reach of the rule (PH6).** On these 7 cube pairs the cube is only 0.114–0.117 dex below the catalogue. Suppose the arbiter were moved exactly onto the catalogue median, or exactly onto the cube median: the frozen rule would return **"undecided"** both times. So with these pairs the rule could never have confirmed either scale. The "neither" verdict does not depend on this, because it says the arbiter sits above both scales.

## Hand estimates (scored as they fell)
HE1 hit (N 23 / 15 / 10 / 7). **HE2 MISS** (R_cat −0.195 against [−0.12, +0.05]). HE3 hit (−0.308). **HE4 MISS** ("neither", not "catalogue scale confirmed"). HE5 hit. HE6 hit. HE7a hit. **HE7b MISS.** **HE8 MISS** (a₀ (A) 5.97 and (B) 7.00 × 10⁻¹¹, not 0.95–1.20). HE9 hit (1.70 × 10⁻¹⁰). HE10 hit.

## Post hoc diagnostics (NOT frozen; no frozen number is changed)
- **PH1, redshift.** The four nearby galaxies (z ≈ 0.006) are the most deficient: −0.274. At z ≥ 0.02 the deficit is −0.137 (ALL, N 19) and −0.120 confusion-clean (N 12), so **it persists** past the 0.10 band.
- **PH2, CFG301-like pairs.** 7 matched pairs pass CFG301's frozen cut; 4 of them are code 1. Their R_cat is −0.159 (68 % −0.192..−0.137), which gives a₀ (A) 6.7 and (B) 7.6 × 10⁻¹¹. Their cube ratio is −0.384 (N 6).
- **PH3, trends.** R_cat shows no trend with HI angular size (ρ +0.12, p 0.58; θ_HI 25–111″) or with W50, SNR_3D or z: *not resolved by these pairs*. The main run's ρ = −0.60 against ALFALFA's S/N shares ALFALFA's own noise, so it is not evidence of a size effect.
- **PH7, width-mismatched pairs** (5 pairs with \|log W50 ratio\| > 0.15, possible ALFALFA confusion that CONF cannot see). Without them: C1 −0.210, ALL −0.175.
- **Context from the catalogue paper** (arXiv:2605.28731, the local PDF already on disk; no download):
  - the fluxes are summed inside an iterated 3σ moment-0 contour mask on a cube with a ~15.5″ beam;
  - they were validated only on sources injected after imaging;
  - the paper shows no single-dish comparison.

  A 3σ mask at 15″ can miss diffuse outer HI, but PH3 does not see the size trend that would predict. CFG302's 75″ r1p0 aperture fluxes are lower still. **The cause stays open:** mask and threshold losses, spectral filtering or continuum subtraction in the released products, the absolute flux scale (MeerKAT against Arecibo), or ALFALFA confusion by neighbours MIGHTEE does not catalogue. ALFALFA selection bias would act most on the low-S/N code 2 pairs, yet code 1 shows the larger deficit.

## What this does not say
- It is not an a₀ measurement and it cannot separate the laws.
- The CFG301 numbers are band-row interpolations, not a re-run. Whether the offset of 23 bright, low-z galaxies applies to CFG301's 47 is an assumption.
- It rests on 15 code-1 pairs, and only 7 of them have cube detections.
- ALFALFA's S21 is assumed to be integrated on its optical cz axis (OPT). Using the brief's REST formula changes the ratios by about 0.02 dex and gives the same decision.
- CONF sees only MIGHTEE-catalogued neighbours.
- Neither survey corrects for self-absorption.
- It does not say the data favour any law.

## Files
- `FROZEN_CRITERIA.md` (committed `336b36f8f`); `cfg304_flux_scale_alfalfa.py` (main run, or `MUTATE=a|b|c`).
- Main run: `cfg304_flux_scale_alfalfa.out`, `cfg304_flux_scale_alfalfa_results.json`, `cfg304_matched_pairs.csv` (23 pairs, all three conventions, CONF, cube columns, beam-summed flux).
- MUTATE runs: `cfg304_flux_scale_alfalfa_MUTATE_{a,b,c}.out`, `..._MUTATE_{a,b,c}_results.json`, `cfg304_matched_pairs_MUTATE_{a,b,c}.csv`.
- Post hoc: `cfg304_posthoc.py`, with `cfg304_posthoc.out` and `cfg304_posthoc_results.json` (final) and `*_run1*` (the first run).
- Reproduce: `python3 cfg304_flux_scale_alfalfa.py; for m in a b c; do MUTATE=$m python3 cfg304_flux_scale_alfalfa.py; done; python3 cfg304_posthoc.py` (under 3 s in total).
