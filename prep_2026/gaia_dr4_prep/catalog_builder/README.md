# DR4 wide-binary catalog chain (built 2026-09-22, validated on DR3)

`wide_binary_pipeline.py --catalog <csv>` needs a wide-binary catalog. On
2 December 2026 nobody will have published one from DR4. El-Badry's DR3-era
catalog took months. This folder builds our own from the raw DR4 source table
with El-Badry's published method and the frozen cuts, and it has been run end
to end on DR3 first.

## Runbook for 2 December 2026

```bash
python3 fetch_extract.py --release dr4      # ~12 sky chunks + the Sigma_18 count map (retries built in)
python3 build_catalog.py --release dr4      # stages A-G, cached, writes the CSV (DR3: 16 min on 16 cores)
python3 build_catalog.py --release dr4 --chance-mode scaled_clean   # declared robustness variant
python3 ../wide_binary_pipeline.py --catalog ../../../real_research/data/widebinaries/dr4_extract/wide_binaries_dr4.csv
```

The primary sample uses El-Badry's chance-alignment recipe as published.
The `scaled_clean` variant is reported alongside it and never substituted.

Then read the `[7(e)]` lines. Never emit a verdict word (Amendment 7(e)).

Before running on DR4, check three things:

- The DR4 `gaia_source` column names match `COLS` in `fetch_extract.py`. They
  are DR3 names; adjust only the names, never the cuts.
- The DR4 NSS screen. DR3's `non_single_star` flag is a sparse proxy, and DR4
  ships a much larger non-single-star catalogue. The frozen cut is "reject any
  DR4 non-single-star solution", so point the flag at the DR4 tables.
- The A_V cut. It needs the SFD98 dust map (see "Not yet applied").

## What each file does

| file | stage |
|---|---|
| `fetch_extract.py` | Archive query (El-Badry+2021 Sec. 2 cuts, plus ϖ > 3.5 mas and \|b\| > 10°), split into 12 HEALPix sky chunks. It also fetches the server-side Σ₁₈ count map. The manifest (`manifest_<release>.json`) records every query, row count and sha256. |
| `build_catalog.py` | A: load. B: El-Badry crowding cut (> 30 phase-space neighbours). C: El-Badry pair search to 1 pc. D: triples and clusters. E: 30 shifted chance-alignment realisations. F: R_chance from El-Badry's 7-feature KDE (Table A1, bandwidth 0.2, leave-10%-out). G: the frozen DR4 cuts, including Banik+2024's Monte-Carlo σ(ṽ) cut (eq. 10), then the CSV. |
| `validate_dr3.py` | DR3 only. Pair recovery and purity against El-Badry's published catalog, agreement of R_chance, and γ̂ on both. |
| `build_report_<release>.json`, `validation_dr3.json` | Cut flow and validation numbers. |

The data go to `real_research/data/widebinaries/<release>_extract/`, which is
gitignored.

## Declared deviations and findings

- **R_chance is computed on this extract**, not on El-Badry's 1-kpc all-sky
  sample, and only for candidates with s < 200 kAU. The excluded candidates
  lie ≥ 3.7 KDE bandwidths from any s ≤ 30 kAU pair. `validate_dr3.py`
  measures the consequence against El-Badry's own R.
- **Shifted pairs** get the star-level crowding cut but not pair-level
  cleaning. El-Badry Sec. 3.1 does not say they do.
- **The frozen "triple search" is redundant with El-Badry's triple
  cleaning.** On the DR3 smoke test it removed 0 pairs after cleaning. Its
  flag fires on 66% of the pairs El-Badry's 1-pc cleaning had already removed
  as triples (the rest have their third star beyond 30 kAU), and on 0% of
  non-triples.
- **Triple-search completeness.** Because of the ϖ > 3.5 mas extract floor,
  the triple search can miss a faint third star whose parallax scatters
  below 3.5 mas near 250 pc.

- **σ(ṽ) cut (Banik eq. 10)** is dominated by Gaia's own proper-motion
  noise, not by the modelling choices. On the DR3 smoke test (1,478 pairs,
  median ṽ = 0.59) the pass rate is 66.8% with the full Monte Carlo (Gaia
  3×3 covariance, 5.5% masses, line-of-sight draw), 69.3% without the
  line-of-sight draw, and 69.8% with the Gaia covariance alone. DR4's
  0.37× proper-motion errors should make this cut far less costly.

## A_V (SFD98)

A_V = 3.1 E(B−V) on the raw SFD scale, without the ×0.86 recalibration
(Banik do not state a conversion; this choice is slightly stricter). The
maps are the SFD98 4096² NGP/SGP FITS files from the `kbarbary/sfddata`
mirror, in `real_research/data/dustmaps/sfd/` (gitignored). Harvard
Dataverse returned 403 to `dustmaps.sfd.fetch()`. Spot checks: E(B−V) =
0.012 at the NGP and 0.016 at the SGP.

## DR3 validation (2026-09-22/23)

The full build ran on the DR3 extract: 4,582,547 sources, 380,438 initial
pairs, 214,002 after cleaning, and 6,210 after every frozen cut, in 16
minutes. It was compared with El-Badry, Rix & Heintz (2021) inside the same
volume (`validation_dr3*.json`).

| check | El-Badry recipe (primary) | scaled_clean variant |
|---|---|---|
| V1 El-Badry pairs (R<0.1, s<30 kAU) we recover | 99.40% of 190,785 | 99.40% |
| V2 our pairs (R<0.1, s<30 kAU) in El-Badry | 98.76% | 98.75% |
| V3 R<0.01 decision agreement (191,432 matched) | 98.93% (ours only 0.60%, theirs only 0.46%) | 98.88% (0.76% / 0.36%) |
| V3 Spearman rank corr. of log R | 0.72 | 0.75 |
| final frozen-cut sample | 6,210 | 6,257 |

For **V4, γ̂ with identical frozen cuts** (DR3-noise forward model, which is
what the pipeline's own dry run uses), only the chance-alignment statistic
differs between the two rows:

| R from | N | γ̂ canonical | γ̂ alt |
|---|---|---|---|
| this builder, El-Badry recipe | 6,210 | 1.075 ± 0.058 | 1.060 ± 0.053 |
| this builder, scaled_clean | 6,257 | 1.113 ± 0.053 | 1.075 ± 0.053 |
| El-Badry's published R (run 1 / run 2) | 6,230 | 1.103 / 1.103 ± 0.055 | 1.055 / 1.075 ± 0.053 |

**Estimator jitter.** The El-Badry-R sample is byte-identical in both runs,
yet its alt γ̂ moved by 0.020. The frozen estimator's bootstrap (`boot=200`
in `run_fit`) draws from one shared seeded stream, so the number of fits
run before it changes the draws. Every difference between chance-alignment
methods above (≤ 0.038) is of the same size as this jitter and well inside
σ_fit. The estimator is frozen and is not changed here; this is recorded
so that no DR4 difference of ~0.02 between variants is over-read.

Why the variant exists: a shifted chance-alignment catalog is valid only if
the shift exceeds the search radius. At s < 200 kAU that fails for stars
within 111 pc, and 18.5% of the chance pairs have primaries there. Separately,
the published recipe does not clean shifted pairs of triples, and at s > 50
kAU the shifted pairs outnumber the cleaned candidates 5–6×. Neither issue
changes the R < 0.01 decision at the percent level (see the table).

**These γ̂ are DR3, NON-SCORING, and evidence for nothing.** They carry no
DR4 NSS/epoch screen and no DR4 RVs, and σ_fit here is 3× the DR4 value. They
are recorded only to show that the frozen cut set, applied in full, moves the
DR3 estimate well below the 1.2075 of the looser Banik-like dry run. That is
the contamination direction §1.6 of the pre-registration predicts. No verdict
word applies (Amendment 7(e)).

## Status

This is a DR3 validation of machinery. Every DR3 number here is contaminated
(no DR4 epoch or NSS screen) and NON-SCORING. It tests the chain, not
gravity.
