# Blinded ECLIPSE sample access audit

Blinded catalogue access and quality audit only. No formula evaluated, no acceleration/model residual computed, no samples selected by agreement. Only the two explicitly authorized small catalogues downloaded; 236-MB model archive and 4-GB image partitions untouched.

The two small archives match the published MD5 checksums. Object catalogue: 26,662 rows / 30 columns. D key catalogue: 15,072 rows / 77 columns; full D FITS: 156 columns.

Join object `Unique_Identifier` to D `unique_identifier`; all D rows join uniquely, with zero grade mismatches.

| Cumulative quality cut | Count |
|---|---:|
| all_AB | 15072 |
| grade_A | 6073 |
| consensus_success | 4098 |
| paper_final_sample | 3202 |
| valid_mass_and_light | 3202 |
| no_large_system_warning | 3202 |
| positive_vetted_deflector_specz | 39 |

**39 is a clean deflector-redshift candidate pool, not a both-redshift gold sample.** The inspected archives have no source redshift or row-level source-redshift linkage. Lines et al. reports 20 paired systems (12 A, 5 B, 3 C), but does not identify the grade-A pairs individually in its aggregate discussion. The clean intersection is currently unascertainable and at most 12 among the reported DESI grade-A pairs.

One independently named pair can be joined: Bergamini Table 1 PS1J1821+7130 matches EUCL-DR1-L015763 within 0.111 arcsec. It is grade A with 4/4 model-success votes and a source redshift 1.366±0.008, independently supported by DESI. It fails the strict sample because `mer_det_quality_flag=386`; other seven-cut checks pass. Do not silently relax the detection-quality cut.

Important definition conflicts found in the released README: SED fits reportedly fix photo-z whereas the paper says spec-z when available; effective radius is described as non-circularized whereas the paper says circularized. Formal lens-model 1-sigma bounds are present but their calibration/systematics are deferred in C. These must be resolved before a precision physical test.

No independent stellar velocity dispersions, rotation curves, gas maps, image/PSF/noise/mask products or full deflector light profiles are in these small tables. A conditional lens-image test needs the row-level vetted source-redshift join, a specified metric/deflection law, targeted imaging products and baryon remeasurement at verified lens redshifts. No formula or acceleration residual was computed.

See `sample_access_audit.json` for hashes, exact cut definitions, all 39 identifiers, archive members and the missing-data checklist.

Selection provenance: no separately persisted pre-inspection freeze or preregistration existed. These quality cuts were specified for this metadata audit before any formula scoring; this is not a sealed prospective experiment.
