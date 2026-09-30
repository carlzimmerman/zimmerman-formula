# SINS/zC-SINF AO Halpha cubes: major-axis velocity profiles (data front, 2026-09-30)

Criteria: FROZEN_CRITERIA_2026-09-30.md (f9290e8d4) + ADDENDUM_1 (empirical noise; written after the frozen-rule run failed). Code: sins_pipeline.py, run_all.py (`python3 run_all.py amend1`), test_injection.py, summarize_controls.py. No a0, g_bar or RAR is computed here.

## Results
| run | C1 (within 25% of published half dV) | C3 median rms A vs B | C4 median dPA |
|---|---|---|---|
| frozen rule as written (`*_FROZENRULE.csv`) | **0 of 35, median ratio 10.2: FAIL** | ~600 km/s | 28 deg |
| amended noise (`*_AMEND1.csv`) | **20 of 35 = 57%: FAIL (line 70%)**, median ratio 0.85 | 14.5 km/s: pass (<20) | 14.4 deg (descriptive) |
| C2 injection, white noise / correlated noise + amendment | 6.7% / 8.2% rms: PASS (<10%) | | |

**Verdict: the method is NOT validated against the published half velocity differences (C1 fails its pre-set line).** Profiles in `sins_ao_profiles_AMEND1.csv` (35 galaxies, variants A and B, V_los and V_rot = V_los/sin i, kpc radii) are the observed, beam-smeared, not asymmetric-drift corrected profiles and are released as such.

## Notes (descriptive, not used to change any pass line)
- The first C2 run failed (recovered PA 13.8 vs 30 deg) because of a flux-scaling bug in the fitter (data ~1e-19, default solver steps); fixed by normalising the flux and continuum slope; the criteria were not touched.
- Line-free-channel scatter is 1.2-4.0x the noise cube; frozen step 1 assumes independent pixels. This is what ADDENDUM_1 replaces.
- Ratios mine/published above 2: GMASS-2540, ZC403741, ZC405501 (outer radii 1.2-1.65 arcsec, possible companion or noise bins, not inspected); below 0.5: Deep3a-6004 (thin, 2 bins), ZC407376, ZC410123 (thin), ZC413597. Excluding the 9 galaxies flagged irregular the count is 17 of 26 (65%), still below 70%, and that split was made after seeing the result, so it is not a pass.
- C3 in run_all.py lost most galaxies to a float mismatch of bin centres; summarize_controls.py recomputes it from the profile CSV with rounded radii (35 of 35 have common bins).
- Axis sign and PA come from a plane fit; C4 uses the better of the two PASINF sign conventions.
