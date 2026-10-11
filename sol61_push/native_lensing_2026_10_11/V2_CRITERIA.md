# Documented source-count correction, frozen before v2 execution

2026-10-11. First run under de0769647 stopped before numerical fitting because
the published prose counts S=22/B=42 differ from the CDS table S=21/B=43.
The original criteria, check.py, contract.json and failed run remain unchanged.

Root-cause inspection: fixed column 72 is correctly parsed. The versioned
arXiv v2 HTML Table A.1 contains the same 199 image identifiers and the same
quality for EVERY row as CDS, when the class inherited from each galaxy's
first row and explicitly marked image exceptions are read. Both have
G=135/S=21/B=43. The disagreement is with prose, not between table releases.
The gold sample is unchanged. No observational outcome has been computed.

V2 accepts precisely G=135/S=21/B=43 and additionally requires an independent
HTML/CDS class cross-check for all 199 IDs. HTML reader: recognize eight-cell
image rows; explicit g/s/b SVG text overrides the first class of the same
parent galaxy; an unmarked first galaxy entry is an error. No inference from
fitted lensing results. Both original sources remain unchanged.

Everything else in FROZEN_CRITERIA.md remains the same: 49 gold features,
27 galaxies, 172 scalar contrasts, all redshift/coordinate requirements,
four epsilon nodes, numerical and MUTATE tolerances, resource bounds and
non-claims. V2 code/results use separate filenames/directories. The original
strict published-count reproduction remains FAILED, not retroactively passed.
Commit this file ALONE before running V2.
