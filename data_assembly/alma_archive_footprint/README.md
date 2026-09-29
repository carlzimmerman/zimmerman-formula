# ALMA archive footprint at the 22 KURVS-CDFS positions (read-only metadata query)

Run 2026-09-29 by `query.py` and `lines.py` on the owner's go ("yes, run the ALMA archive footprint query"). Service: ALMA Science Archive TAP (https://almascience.eso.org/tap/sync, table `ivoa.obscore`).
Only metadata rows were retrieved; no data product was downloaded. No flux, no gas mass, no verdict.

## Method and controls
One query per KURVS position (`kurvs_positions.csv`): rows whose `s_region` contains the position. Positive control: the GOODS-ALMA field centre returns both GOODS-ALMA proposals (2015.1.00543.S, 2017.1.00755.S), 40 rows.
Negative control: an empty position (RA 150, Dec +60) returns 0 rows. `lines.py` then tests, for each row, whether a spectral window in the archive's own `frequency_support` string covers CO(2-1), CO(3-2), CO(4-3), [CI](1-0) or [CI](2-1)
redshifted to the galaxy's Hα redshift.

## Files
| file | content |
|---|---|
| `raw/kurvsNN.csv` | the returned rows for each position, as received |
| `alma_footprint_rows.csv` | all rows with the key columns (proposal, PI, band, resolution, exposure, archive sensitivity, release, frequency support, proposal title) |
| `alma_footprint_by_proposal.csv` | proposal-level summary per galaxy |
| `alma_line_coverage.csv` | 30 (galaxy, proposal, line) combinations with a spectral window on the line, with the archive's stated sensitivity |
| `checks.txt`, `query.py`, `lines.py` | provenance |

## Results
24 distinct proposals cover at least one of the 22 positions; all are listed as public in the archive (the latest release date is 2026-02-17). Galaxies with no archival coverage at all: KURVS 1, 3, 7 (the last two lie on the GOODS-ALMA edge).
The GOODS-ALMA proposals (Band 6, 1.1 mm) cover 18 galaxies. Band-3 CO(2-1) at the KURVS Hα redshift is covered by a spectral window for the following, and for **no archival programme** for the others (KURVS 1, 3, 7, 10, 11, 17, 18, 21 have no CO or [CI] window at their redshift):
| KURVS | line and programme (PI, proposal title as filed) | observed freq. | archive sensitivity per 10 km/s | best resolution |
|---|---|---|---|---|
| 15 | CO(2-1): 2019.1.01238.S (Molina, "The kpc-scale view to the molecular gas content in 'typical' star-forming galaxies at z~1.5") | 88.23 GHz | 0.53 mJy/beam | 0.11″ |
| 15 | CO(2-1): 2018.1.00164.S (Ibar, "A survey for the molecular gas content in star-forming galaxies at z~1.5: exploiting the VLT/KMOS and ALMA synergy") | 88.23 GHz | 1.1 mJy/beam | 2.5″ |
| 15 | CO(2-1): 2017.1.00138.S (Decarli, "Wide ASPECS"), 2021.1.00024.S (Bauer, "A Legacy Survey of SMGs in the CDF-S") | 88.23 GHz | 5.0; 2.4 | 0.54″; 0.62″ |
| 9 | CO(2-1): 2017.1.00138.S (Wide ASPECS), 2021.1.00024.S (Bauer) | 90.76 GHz | 5.0; 2.1 | 0.54″; 0.70″ |
| 16 | CO(2-1): 2017.1.00138.S, 2021.1.00024.S | 89.74 GHz | 5.0; 2.4 | 0.54″; 0.62″ |
| 13 | CO(2-1): 2021.1.01500.S (Rosario, "Unravelling the pathways of AGN-driven quenching in high-redshift galaxies") | 98.77 GHz | 0.72 mJy/beam | 1.09″ |
| 8 | CO(2-1): 2017.1.01163.S (Wardlow, "ALESS CO"), 2021.1.00024.S | 90.76 GHz | 1.4; 2.4 | 0.6″ |
Others outside the ten with a CO(2-1) window (2, 4, 5, 6, 12, 14, 19, 20, 22) and a CO(3-2) window (6: 2013.1.00836.S Papovich "Gas-Mass Evolution in Milky Way Progenitors at z~1.3"; 14 and 19: 2021.1.00024.S) are in `alma_line_coverage.csv`.
A [CI](2-1) window covers KURVS-14 in 2018.1.01044.S (Scholtz).
The dust programmes cover: 2015.1.00870.S (Wiklind, "Evolution of the interstellar gas fraction over cosmic time", bands 6/7) covers KURVS 2, 11, 15.

## What this does and does not say
- The position lies **inside the archive's `s_region`** for the observation; the primary-beam response there is not known from this query, and near the mosaic edge the true sensitivity is worse than the stated one.
- The sensitivity is the **archive's own estimate per spectral window**, not a measured map rms; pointing-centre values were used for the best.
- Whether a line is DETECTED at these positions is unknown; a covered window is not a detection. Whether the observers have published gas masses for these galaxies is unknown: a search of arXiv abstracts did not surface a paper from the Molina, Ibar or Wide-ASPECS programmes for these targets, but I did not read their full texts.
- The three deepest windows on KURVS-15 (Molina 0.53 mJy/beam per 10 km/s at 0.11″; Ibar; the wide surveys) and the CO(2-1) window on KURVS-13 are the best archival chance for a measured CO gas mass among the calc thread's ten. Nothing has been downloaded: cubes are large and need the owner's go with filename and size first.
