# Authenticated inputs and scope

CDS catalogue DOI: https://doi.org/10.26093/cds/vizier.36980053

Downloaded on 2026-10-24 by HTTPS into data/:

* https://cdsarc.cds.unistra.fr/ftp/J/A+A/698/A53/ReadMe
* https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/A%2bA/698/A53/tabled1&-out.all&-out.max=unlimited

Survey article: https://arxiv.org/html/2504.02787v1 ; published DOI https://doi.org/10.1051/0004-6361/202554176 . The arXiv version and CDS file are separately pinned, not assumed identical. The publisher HTML could not be fetched (HTTP 403). The CDS ReadMe calls the online tables D.1/D.2; arXiv calls them E.1/E.2. The ReadMe's velocity caution in note (2) appears under the D.1 field definitions; it is retained in the raw file and not silently corrected. Its scope is not independently resolved here. These fits are exploratory catalogue-subset analyses, not an exact reproduction of the published member sample or quality pipeline.

Observed file: 612 unique Gaia IDs, 603 with Pmem>0.07, 318 of those with tabulated FLAMES velocity. Explicit S/N>16, G<19.7, 0<e_Vel<5 km/s and finite [Fe/H] leave 298. The publication's summary counts differ; do not relabel 298 as its 312-star sample. Spectra-level EW and cross-correlation quality flags are not rederived. Walker velocities embedded in free-text Notes lack usable corresponding errors here and are not promoted into the likelihood. Thus the FLAMES central coverage gap is retained, not filled with invented uncertainties. Nine Pmem=0 entries are excluded.

Catalogue positions/velocities/errors/metallicities are used directly. No plot is digitized. Full member-ID list, radial percentiles, source hashes and selection code are retained. The preceding LVD, Weisz and E-MILES dataset provenance is in ../cold_data_constraints_2026_10_24/RESULT.md and its input receipt; capture.py records that exact result hash.
