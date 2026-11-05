# NO VERDICT on fully validated stage0; conditional STOP: NOT ENOUGH POWER

Kappa = 1/2 FITTED; not theory closed. Frozen criteria ffc0dd9d60.
The point-source, constant-shape-noise Fisher bound fails the required
0.05 dex precision on both footings. The required rotation-count control
also misses its frozen threshold, so this is not a fully validated FN4e
stage0 verdict. No stage1 measurement or theory rejection follows.

| Quantity | Canonical | Alt |
|---|---:|---:|
| Fisher information upper bound | 4.3677643858 | 5.2784794005 |
| sigma(log10 a0) lower bound, dex | 0.4784872817 | 0.4352568197 |
| 0.09 dex gap significance upper bound | 0.1881 | 0.2068 |
| Separation of the two footings, significance upper bound | 0.1719 | 0.1890 |

These bounds assume the point-baryon law-S response, catalogue masses and
local distance convention, ordinary positive geometry with Dls/Ds<=1,
and the frozen constant component variance. They include all eligible
lenses before isolation. The per-source positive derivative bounds are
summed before squaring, preserving possible shared-source coherence;
removing lenses cannot exceed this bound. Neither an exact isolated
sample nor an exact cosmological geometry was supplied. DESI has no
stellar-mass column for the required neighbour threshold.

The JSON key amplitude_SNR_upper is a deep-MOND amplitude proxy
2*sqrt(F)/ln(10), yielding 1.8153/1.9956. It is NOT an upper bound on the
total Newtonian-plus-modified shear detection S/N. Total stack S/N and
an observed discrepancy are not measured here. The derivative-information
and gap bounds in the table are the meaningful power diagnostics.

## Catalogue and controls

The raw chunk reader recovered all 31,502 ALFALFA rows (K1 PASS), 156,411
FASHI rows, and 21,262,011 usable source rows. Matched finite stellar
masses and AGC deduplication leave 15,925 gas-rich candidates and 660
lenses in the source footprint. Unmatched FASHI systems have no invented
stellar mass. Of those 660, 653 lie in an observed good-redshift DESI pixel;
that is coverage information, not a selection function or isolation test.
The source component variances are 0.07355453 and 0.07399895; their mean
is 0.07377673834. Full counts/hashes are in catalogue_summary.json.

Failed checks retained without changing thresholds:

- K2 provisional area: measured 980.3212 deg2 versus 777 +/-5%.
  All-position and usable-source areas are identical. The original brief
  permits using the measured area after reporting this provisional miss.
- The RA+180-degree mutation leaves 388 lenses, a 41.2121% decrease.
  It fails the required >50% decrease. It does fail original-count
  preservation and changes Fisher to 2.70157/3.26487, but this does not
  repair the separate failed threshold. Forecast and audit scripts exit1
  to expose it, including the main run's frozen-control diagnostic.

Mathematical known answers: 11/11 pass, including Newtonian and deep-MOND
projection limits, derivative inequalities and a two-lens triangle
fixture. The independent 100-SIS noise-only mock/analytic SNR ratio is
0.9977876100, within10%; 128/256 quadrature converges. Catalogue audits:
13/13 numerical/repeatability checks pass, with the failed frozen rotation
control explicitly separate. Chunk10000/20000 footprints and counts
agree exactly; Fisher relative differences are at most1.63e-15 versus
1e-10. An independent same-size preparation and forecast rerun produces
byte-identical scientific JSON. Peak recorded RSS is992,215,040 bytes;
individual full passes take13-19 seconds, one thread.

## Reproduce

Use a Python environment with numpy, scipy, sympy, astropy and healpy
already installed. No downloads or installations are part of this run.
From the repo root, replace LANE with this folder's relative path:

    python LANE/validate_bound.py
    python LANE/prepare.py --chunk 20000 --max-chunks 2000
    python LANE/prepare.py --chunk 10000 --max-chunks 3000
    python LANE/forecast.py --chunk 20000 --max-chunks 2000
    python LANE/forecast.py --chunk 10000 --max-chunks 3000
    python LANE/forecast.py --chunk 20000 --max-chunks 2000 --mutate
    python LANE/forecast.py --chunk 10000 --max-chunks 3000 --mutate
    python LANE/prepare.py --chunk 20000 --tag repeat --max-chunks 2000
    python LANE/forecast.py --chunk 20000 --tag repeat --max-chunks 2000
    python LANE/check_results.py

Expected exits: preparation0, forecast1 (reported frozen control miss),
check_results1 (same miss). Exit75 means resumable checkpoint. Fresh tags
or removal of only this lane's generated checkpoints are needed for a
fresh full reread; completed checkpoints otherwise verify identity and
resume. Scripts never materialize the large FITS tables through .data.
Full intermediate lens rows and packed masks regenerate locally; compact
summaries, final forecasts, input identities and verification hashes are
committed. Exact mass-complete isolation and native distance geometry
remain needed for a full observational forecast, but cannot repair this
conditional point-source information bound by removing sample members.
