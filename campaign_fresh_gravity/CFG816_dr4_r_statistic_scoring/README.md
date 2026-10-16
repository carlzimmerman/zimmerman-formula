# CFG816: the DR4 R statistic (scoring script and controls)

Criteria: `FROZEN_CRITERIA.md` (d9eed26eb, committed alone before this script). Script: `cfg816_r.py`. Status 2026-10-16: **script written; controls C0, C1, C2, C3, C5 and MUTATE run on synthetic
pairs and pass; C4 (the DR3 code-path run) is NOT RUN; no DR3 or DR4 data have been read; no result.** κ = ½ is fitted; the cold mass is still required.

## Use
| command | what it does |
|---|---|
| `python3 cfg816_r.py` | controls C0-C3 and C5 on synthetic pairs (about 40 s, one core); writes `cfg816_r.out`, `cfg816_r_results.json`; exit 0 if all run controls pass |
| `python3 cfg816_r.py --mutate` | MUTATE (×1.2 at x > 1 on a synthetic null); exit 1 = detected = the test bites; writes `*_MUTATE.*` |
| `python3 cfg816_r.py --dr3 TABLE` | C4 on the registered DR3 sample (needs the owner's yes and the download); once only |
| `python3 cfg816_r.py --dr4 TABLE` | THE RUN, once, after DR4 is public and only on the owner's yes; refuses a second run; a change goes under "Departures" below |

Pair table (CSV): `sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc` (the registered `ingest_csv` columns) plus `plx_err_frac, ruwe1, ruwe2, ipd1, ipd2, vt_err, drv_kms` (blank if no RV), `nss1, nss2`.
The script refuses a table that lacks any checklist column. **Building that table from the registered pipeline's stage-G pair array is not written yet.**

## Results of the controls (synthetic; Rayleigh ṽ with median 0.489, x log-uniform 0.05-5, M = 1.8 M☉)
- **C0 (added):** the ṽ computed here equals the registered `wide_binary_pipeline.ingest_csv` ṽ exactly (difference 0).
- **C3:** the class arithmetic reproduces Amendment 22: σ_tot = 0.0896 / 0.0507 / 0.0385 / 0.0276 / 0.0225 at N = 1421 / 5000 / 10⁴ / 3×10⁴ / 10⁵; KILLED needs R ≥ 1.269 / 1.152 / 1.116 / 1.083 / 1.068; CONSISTENT unavailable.
- **C1:** R is recovered within 2σ_R in 200/200 repeats for each R_true ∈ {1.00, 1.05, 1.20} at N = 1421 and 30000 (this is easy to pass, because σ_R carries the 0.02 floor).
- **C2:** the bootstrap σ is calibrated: at N = 1421 its mean is 0.0454 against an empirical scatter of R of 0.0456; coverage 66.9% (target 68% ± 5%); KILLED never fires on 1000 null repeats. Coverage with σ_R is 97.7% (over-covers, by design; interpretation I3).
- **C5 (added):** the CSV path round-trips exactly; a boost carried only by NSS-flagged pairs comes out CONTAMINATION-LIMITED; a boost carried by every pair comes out KILLED.
- **MUTATE:** R = 1.208 at (R − 1)/σ_R = 7.0: detected.

## Interpretations made while implementing the frozen text (none changes a frozen threshold)
I1 N = pairs that enter R (numerator + denominator); numerator-only is printed as a sensitivity. I2 stratified bootstrap (within each regime). I3 C2 coverage is applied to the bootstrap σ alone; σ_tot carries an
assumed 0.02 systematic that synthetic data lack. I4 C2 uses 300 resamples per repeat (the run uses 2000). I5 C4 passes if R − 1 < 2σ_R and (1.20 − R)/σ_R > 1 on the DR3 primary. I6 C0 added. I7 C5 added.
I8 the f_tail z-test applies only if both regimes hold ≥ 5 pairs with ṽ > 2, else "n/a (<5 events)" (found by MUTATE: on a clean sample, one or two stray events gave a spurious 2.1σ).

## Known weaknesses, stated against interest
1. **The frozen f_tail rule can over-flag a genuine boost.** A real 20% broadening of the ṽ distribution also raises the fraction above ṽ = 2, so a significant f_tail difference does not by itself identify contamination. The label is reported with the raw
   numbers and is never the only output, and the rule only ever makes a kill harder, but it is a weakness of the frozen text. Changing it needs a new dated file, not an edit.
2. **f_tail is ≈ 0 in the synthetic samples** (a Rayleigh tail), so the controls cannot exercise it; real data have a percent-level tail.
3. **C4 has not run**, so the full control set is incomplete; the script says so in its own output.
4. **σ_tot is a registered assumption, not a measurement**; at every N it exceeds the bootstrap σ (0.0126 against 0.0298 at N = 30000), so the classes are set by the floor, not by the data's precision.

## Departures
None yet (no data read).
