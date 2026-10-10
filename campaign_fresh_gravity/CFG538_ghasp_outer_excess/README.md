# CFG538: does GHASP replicate CFG534's SPARC early-type outer excess?

**Frozen verdict (criteria e6eb98396): NO INDEPENDENT SAMPLE on both footings.** That holds for the primary set (390/466 curves) and for the declared extension (388/500 + 390/466 combined, addendum b8f6c1be5). GHASP's Hα curves stop too soon for the frozen outer band. Only **1** early-type disc in either set has ≥ 2 points at R ≥ 3 R_d (Rc scale length), so no matched bin exists. The coverage counts disclosed in the criteria predicted this before scoring.

The test cannot be run on GHASP. It is not a failed replication.

Settings: κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 are never pooled. The kernel is ν(y) = 1/(1 − e^−√y). The cold energy's mass is still required. This is not "theory closed". Nothing was fetched: the owner downloaded the public CDS tables by hand (see `FETCH_LOG.md`). All numbers below come from `cfg538_ghasp_results*.json` and `cfg538_forecast*.json`, given as canonical / alt.

## Files
- `FROZEN_CRITERIA.md` (e6eb98396) and `FROZEN_CRITERIA_ADDENDUM.md` (b8f6c1be5). Each was committed alone, before any residual.
- `cfg538_ghasp.py`: one script for everything.
  - `STAGE=forecast` produces the power forecast with no residual: `cfg538_forecast.out/.json`.
  - The default run produces the scoring: `cfg538_ghasp.out` and `cfg538_ghasp_results.json`.
  - `CFG538_MUTATE=1` produces the `_MUTATE` files.
  - `CFG538_SET=combined` produces the extension: every output gets an `_ext` suffix.
- `cfg538_target*.json`: records which statistic carries the free-M/L, sensitivity and MUTATE work (rule in criteria §8).
- Total run time is about 3 min, at `nice -n 10` with 2 threads.

## Sample and baryon model
| | primary (390/466) | extension (combined) |
|---|---|---|
| RC galaxies | 82 | 173 (93 from 388/500; 2 duplicates kept as their 390/466 curve; 3 non-UGC names with no RC3→UGC map: IC 476, IC 2542, NGC 5296) |
| with Korsaga+19 Rc photometry | 59 | 124 |
| f_ID ≤ 2, i ≥ 30 | 41 | 86 |
| **SPARC overlaps removed** | **10** (13 among the 59) | **14** (18 among the 124) |
| **N used** | **31 (5 early, 26 late)** | **72 (13 early, 59 late)** |
| ≥ 2 pts at R ≤ 1.5 R_d (inner band) | 31/31 | 72/72 |
| ≥ 2 pts at R ≥ 3 R_d (frozen outer band) | 19 (**1 early**) | 36 (**1 early**) |
| ≥ 2 pts at R ≥ 2 R_d (D2) | 27 (3 early) | 57 (8 early) |

Overlap names are in the JSON. They include NGC 3726, 3893, 5985, 6946, 4559, 5055, 5585 and 6015, found through the RC3 UGC↔NGC map.

The inner band is resolved: the median h / seeing is 10.8.

**Stars.** These come from Korsaga's Rc disc (μ0, h) and Sérsic bulge, using the Bell & de Jong colour M/L (Korsaga's fixed-M/L technique). That M/L depends on type, which pushes early-type residuals down, i.e. against H.

**Gas.** GHASP has no HI, so it comes from a scaling relation calibrated on SPARC: log M_HI = 9.478 + 0.679 (log M* − 10) + 0.061 (T − 5), with σ_g = 0.337 dex. The gas is laid out as an exponential sized by Wang+16, times 1.33.

**Gas bias sign.** Missing gas raises residuals most in the gas-rich late types, so it pushes Δ (early − late) **negative, against H**. Measured on the D2 statistic, omitting the gas entirely moves Δ_out by only −0.017 (primary, D3) or −0.0055 (extension). Over 200 draws of the σ_g scatter, Δ_out moves with SD 0.012 / 0.008. So gas is not what limits this test.

**Checks.**
- C1 passes: CFG534 is reproduced (+0.07115 / +0.07215).
- C4 passes: the gas calibration ran.
- C5 passes: row counts match the ReadMes. ADD-1 also passes (5505 rows).
- **C2 FAILS.** The disc profile reproduces Korsaga's L_D, with a median ratio of 1.02. But the tabulated Sérsic (μe, re, n) does not reproduce their L_B: the median ratio is 0.83 (primary) / 0.88 (extension), ranging from 0 to 6. re is given only to 0.01 kpc, so small bulges are unresolved in the table. Bulge masses are uncertain at that level, which matters for the inner band and not the outer.
- **C3 FAILS.** The colour M/L matches Korsaga's M/LfML except for the galaxies whose B−V Korsaga computed from T (flag `*`). For those the difference is up to 0.11 (about 8%), so Korsaga evidently used a slightly different relation. The frozen rule was kept. Neither failure was repaired.

## Results (frozen statistic; Z_cal = shuffle-calibrated, 4000 within-bin shuffles)

| | primary (390/466) | extension (combined) |
|---|---|---|
| Δ_out (R ≥ 3 R_d) | untestable, 0 matched bins | untestable, 0 matched bins |
| Δ_out − Δ_in | untestable | untestable |
| **frozen verdict** | **NO INDEPENDENT SAMPLE / NO INDEPENDENT SAMPLE** | **NO INDEPENDENT SAMPLE / NO INDEPENDENT SAMPLE** (extension: declared after the freeze, before any residual) |
| D1 Δ_in, the inner half of H | −0.050 ± 0.229, 1 bin: not testable | **−0.005 ± 0.055 (Z_cal −0.39) / +0.004 ± 0.055 (Z_cal 0.00); 3 bins, 12 early / 31 late: NO INNER DIFFERENCE** |
| D2 Δ_out at R ≥ 2 R_d (SPARC same-band reference +0.059 / +0.060) | 0 matched bins | **+0.086 ± 0.054 (Z 1.59, Z_cal +1.18) / +0.091 ± 0.054 (Z 1.69, Z_cal +1.25); 3 bins, 8 early / 26 late: label CONSISTENT** |
| D2 Δ_out − Δ_in | — | +0.049 ± 0.035 (Z_cal +1.16) / +0.043 (Z_cal +1.08) |
| D3, no f_ID/inclination cuts, 3 R_d | −0.180 ± 0.170, 1 bin (2 early): inadequate | −0.058 ± 0.186, 1 bin: inadequate |
| with overlaps: primary / D2 | untestable / 1 bin, inadequate | untestable / +0.027 ± 0.061 (Z_cal +0.29 / +0.37): CONSISTENT |

**Verifying the D2 lean (no verdict weight).**
- It is carried by the log M_b 11.0–11.4 bin, which holds only 2 early types: +0.19 ± 0.085. The other two bins give +0.04 and −0.02.
- Leave-one-galaxy-out Z runs from +0.22 (dropping UGC 2503) to +1.90 (dropping UGC 4936).
- Shifting the bins by +0.2 dex gives +0.032 (Z 0.51).
- With the T ≤ 2 cut it is −0.06 (1 bin). With T ≤ 4 it is +0.085 (Z 1.58).
- With a single type-independent Υ_Rc (1.03) it rises to +0.162 (Z 2.75). The colour M/L absorbs part of it.
- Keeping the SPARC overlaps drops it to +0.027.
- The realized σ (0.054) was 1.6× the forecast σ (0.033), the same pattern as WALLABY in CFG537.
- So: same sign as SPARC, about 1σ calibrated, not a replication.

**Free stellar M/L** (factor 2 either way of the colour M/L). It ran on D2 for the extension and D3 for the primary, with no verdict weight.
- Extension, B1 global fit: +0.057 ± 0.027 (Z_cal +1.72) / +0.053 (Z_cal +1.55).
- Extension, B2 inner fit: +0.072 ± 0.036 (Z_cal +1.74) / +0.075 (Z_cal +1.85). Label: PARTIAL.
- The fitted M/Ls do not favour heavier early-type stars: early − late Δlog f is +0.03 (B1) and −0.005 (B2).
- B3 (early ×2, late ×0.5) flips the outer value to −0.31, but at an inner residual of −0.47 dex, which the inner data exclude.
- Primary, on D3: ABSORBED BY M/L. That run has 1 bin with 2 early types and is uninformative.

**MUTATE (all pass).**
- Primary (on D3): MU1 mean Z −0.001 / −0.001; MU2 recovers +0.0710.
- Extension (on D2): MU1 mean Z +0.13 / +0.13 (null SD 1.52); MU2 recovers +0.0710.

## What adding the 388/500 curves added
- The pre-scoring forecast from Korsaga's Rlast/h for the full GHASP set (72 non-SPARC, f_ID ≤ 2, i ≥ 30) gave only **2 early types with Rlast ≥ 3 h**. Even the complete GHASP sample cannot test the frozen 3 R_d band. That forecast was confirmed: realized, 1 early.
- At 2 R_d the forecast gave 11 early, σ_fc 0.029, expected Z 2.0. The realized D2 used 8 early and had σ 0.054.
- The combined set therefore adds the first adequate **inner-band** test, which shows no inner difference, and a 2 R_d outer lean of the right sign at about 1σ calibrated.

## What the record now holds
- **The early-type outer excess still rests on SPARC alone** (about 2.1σ calibrated, CFG537).
- **WALLABY (CFG537) and GHASP (this lane) are both consistent in sign and neither replicates.**
  - WALLABY's limit was the inner band, because of its beam.
  - GHASP's limit is the outer band, because of Hα reach in R_d units.
  - GHASP's inner band, adequate in the combined set, shows **no early-type inner excess**. That agrees with the "no inner excess" half of H; it does not confirm the outer half.
- A decisive sample needs HI curves to ≥ 3 R_d for ≥ 8 matched early-type discs outside SPARC, with resolved inner curves. Candidates are BIG-SPARC, or HI curves for the GHASP early types (GHASP was selected from WHISP).
- No sentence here says the data favour the framework or ΛCDM. κ is fitted, and the cold energy's mass is still required.

## Disclosures (dated 2026-10-09)
- **The extension came after the freeze.** The 388/500 curves arrived after e6eb98396. The extension was declared in a separate addendum before any residual was computed. The primary headline is the frozen 390/466 result.
- **Barbosa table4 is not used for the mass model** (stated in the criteria). Korsaga's digest was used instead; Barbosa's data enter only through table1 positions and seeing.
- **A misleading forecast label.** In the extension's forecast output, the field `with_390_466_RC` actually counts galaxies with any loaded curve (combined). The label is misleading; the numbers are correct.
- **The default runs were re-run once after scoring.** The only change was `np.seterr(...)`, so that RuntimeWarnings (which printed home paths) stay out of `.out`; the B3 Δlog f is NaN by construction. The output is byte-identical apart from the removed warning lines.
- **The criteria predicted this verdict.** The criteria disclosed the pre-scoring coverage counts that predicted NO INDEPENDENT SAMPLE. D2 (2 R_d) was pre-declared as descriptive, with a SPARC same-band reference computed in the run (+0.0586 / +0.0600).
