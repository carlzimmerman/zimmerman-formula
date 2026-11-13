# EUC11 (DEEP-FIELD LENSES): RESULT

2026-11-12. Criteria 0a6088cd0a (committed alone, before any script or deep-field row of a lens). Amendments, each
committed alone before any grism row or any `b` was seen: A1 63dbb33bb4 (footprint), A2 650ed9e51b (control annulus
20–100″), A3 a42a20fbca (source search on the 200 lenses whose control candidates the archive returned).

## Verdict: NOT EVALUABLE as frozen, and NOT EVALUABLE under the amendments (both parts, both footings)

- **As frozen:** check K2 fails. Only 460 of the 576 Q1 lenses (79.9 %) have a deep-catalogue object at their position,
  because 77 lie outside the area the DR1 deep catalogue covers. That word stands.
- **Part 1 under A1 (source-free ceiling on the Q1 lenses): NOT EVALUABLE.** The transfer check T1 fails: on ECLIPSE
  itself, replacing the catalogue's stellar mass by this lane's H-flux predictor moves EUC1's f25 from 0.156 / 0.139 to
  0.210 / 0.182 and EUC4's wide-lens f25 from 0.758 / 0.702 to 0.957 / 0.923.
- **Part 2 under A1–A3 (source redshifts from the deep grism tables): NOT EVALUABLE.** The purity null fails at both
  tiers: the rule passes on 7 % of matched non-lens galaxies against 10–12 % of lenses.

The galaxy-scale gate (EUC1-F) and the sealed forecast (EUC5-F) are not touched: this lane uses different lenses.
Both mutation twins exit 1. κ = ½ FITTED. No outcome favours the framework.

## 1. What was searched

The Euclid Deep Fields hold no ECLIPSE lens (the catalogue has holes of 2.4–3.0° at each field centre), so the lane
uses the Q1 Strong Lensing Discovery Engine catalogue (Zenodo 10.5281/zenodo.15025832).

| | N |
|---|---|
| Q1 grade A/B lenses | 576 (309 A, 267 B) |
| inside the DR1 deep catalogue (A1: at least 5 deep objects within 30″) | 499 |
| with a deep-catalogue object within 0.6″ | 460 (92.2 % of those inside) |
| with a usable lens model | 312 |
| Part 1 sample (model, lens object, photo-z, H flux) | 299 (175 A, 124 B) |
| Part 2 lenses (A3) | 200; 177 evaluable (88.5 %) |
| Part 2 matched controls | 278, around 132 of those lenses; 243 evaluable (87.4 %) |

Deep-field spectra are usable for 88 % of lens objects, against 37 % in the wide survey (EUC3).

## 2. Checks

| Check | Result |
|---|---|
| K1 EUC1 reproduced on ECLIPSE | N(P) = 3,192; −0.0185 / −0.0439 (pass) |
| **K2 as frozen** | **79.9 % (460 of 576) against 90 %: FAIL** |
| K2 (A1), lenses inside the footprint | 92.2 % (460 of 499) (pass) |
| K3 controls like the lenses | H flux ratio 0.962; photo-z difference −0.025 (pass) |
| K4 fetch | 1,071 object ids, all queried; re-query identical, 3,861 rows (pass) |
| **T1 transfer** | **P: f25 0.210 / 0.182 (limit 0.156 / 0.139 ± 0.03), median b +0.020 / −0.005 (limit −0.019 / −0.044 ± 0.03); wide grade B: f25 0.957 / 0.923 (limit 0.758 / 0.702 ± 0.05): FAIL** |
| MUTATE newton | f25 on grade A 0.109 / 0.080 → 0.309 / 0.309; exit 1 |
| MUTATE noguard | secure controls 17 → 36; exit 1 |

**Why T1 fails (post hoc, `euc11_t1_posthoc.out`).** The pipeline photo-z is harmless: with it and the catalogue mass,
sample P reads 0.161 / 0.138. The mass predictor is the cause: with it and the catalogue photo-z, 0.215 / 0.191. The
predictor (log M★ from H flux, distance and redshift; scatter 0.213 dex) compresses the mass range: its residual rises
by 0.48 dex per dex of catalogued mass. Heavy galaxies are predicted too light, so their `b` is too high, worst in the
wide class.

## 3. Part 2: the search (NOT EVALUABLE)

EUC3's rule on the deep tables. Tier A: rank-0 solution. Tier B: any rank, two lines.

| Tier | Lenses secure | Controls secure | Limit | |
|---|---|---|---|---|
| A | 18 of 177 (10.2 %) | 17 of 243 (7.0 %) | 4.9 | H2 FAIL |
| B | 21 of 177 (11.9 %) | 18 of 243 (7.4 %) | 5.8 | H2 FAIL |

- The lens rate exceeds the control rate by 3.2 % [−2.3, +8.7] in tier A (normal approximation). Depth raised both: the wide survey gave
  1.5 % and 1.3 % (EUC3).
- **Every tier-A hit sits on the central object itself** (18 of 18 lenses, 17 of 17 controls; 20 of 21 and 18 of 18 in
  tier B). The catalogue's redshift for the galaxy lies 0.6–0.9 above its own photo-z interval, with Hα at S/N 7–9
  and a second line in a quarter to a half of cases. That happens in non-lens galaxies of the same brightness and photo-z almost as often as in
  lenses, so a source line inside a deflector's spectrum cannot be told from it in the catalogue tables.
- The printed reading is void and not used (tier A, grade A, 7 lenses: median b +0.43 [−0.14, +0.67]). By the null,
  about 12 of the 18 lens hits are expected to be false.

## 4. Part 1: the source-free ceiling on Q1 lenses (NOT EVALUABLE; numbers shown, not used)

Law S, source at z = 1100, predicted masses. f25 (canonical / alt):

| Einstein radius | N | f25 |
|---|---|---|
| below 1.0″ | 193 | 0.005 / 0.005 |
| 1.0–1.3″ | 58 | 0.086 / 0.069 |
| 1.3–1.7″ | 30 | 0.267 / 0.133 |
| 1.7″ and above | 18 | 0.833 [0.667, 1.000] / 0.778 [0.556, 0.944] |
| grade A (the analogue of EUC1's sample P) | 175 | 0.109 [0.063, 0.154] / 0.080 [0.040, 0.120] |

The rise with Einstein radius seen in ECLIPSE (EUC1, EUC4) appears again in a different lens catalogue with different
lens models. Its size cannot be used: T1 shows this mass substitute inflates f25 by about 0.05 overall and by 0.2 in
the wide class on ECLIPSE itself, and only 18 Q1 lenses are wide (the frozen floor is 30).

## 5. What this says

1. **Depth does not rescue the catalogue route.** With five times the dithers, 88 % of lens objects have a usable
   spectrum and a tenth pass the rule, but so do 7 % of matched non-lenses. Deeper data multiply the false hits as
   fast as the real ones.
2. **The information is not in the redshift tables.** All hits are the central object's own catalogued redshift
   disagreeing with its photo-z. Telling a lensed source from that needs the per-dither spectra and the arc's
   position (the method of EUC14 and EUC15). The deep fields, with about 20 dithers per object and both grisms, are
   where that method should work best; it has not been run on the Q1 lenses.
3. **The Q1 lenses need real stellar masses.** A flux-based mass substitute fails its own transfer check. A
   population-synthesis mass on the scale of ECLIPSE's would make Part 1 a true replication of EUC1 and EUC4.

## 6. Disclosures

- Three amendments, all forced by the archive and all committed before any grism row or `b` was seen. A1: 77 lenses
  are outside the DR1 deep catalogue. A2: the 300″ control query cannot run within the archive's five-minute limit.
  A3: the 100″ query completed for 200 lenses in about three hours and then failed.
- A3 names the list of covered lenses `cand_covered.csv`; the script writes `covered_lenses.csv` (the first name
  collided with the control-chunk file pattern). One control chunk (positions 140–159) returned no rows at the time
  limit twice and is excluded, as A3 states.
- Controls: 866 drawn, 278 kept after the photo-z match (the rule allows up to three per lens; the median lens had
  seven candidates).
- `euc11_fetch.py` changed during the fetch (footprint stage, chunk sizes, the A2 radius, the A3 switch); `euc11.py`
  was written before any grism row was fetched and changed once, for A3, also before.

## 7. Files

`euc11_fetch.py`, `euc11.py`, `euc11.out`, `euc11_results.json`, `euc11_part1_per_lens.csv`, `euc11_sources.csv`
(every secure or conflicting system, lenses and controls), `euc11_MUTATE_newton` / `_noguard` `.out` and
`_results.json`, `euc11_t1_posthoc.py` / `.out`. Tables are outside git (`_external_data/euclid_q1_lenses/`).

    python3 -I euc11_fetch.py --q1-dir <dir> --stage all --cand-covered 0-140,160-220
    python3 -I euc11.py --q1-dir <dir> --eclipse-dir <dir with the ECLIPSE files and nisp_tables/>
