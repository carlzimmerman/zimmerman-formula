# L002777 / SILO790 — bounded public DESI coverage check

Checked 2026-11-13 at RA 141.2955 deg, Dec 63.42385 deg. No public DESI DR1 HEALPix target was recovered near this position. This does not establish that DESI never observed the object.

The local strong-lens VAC has no row within 60 arcsec (nearest row 4759.91 arcsec), but that small VAC is not an observation index. Two broader public services were therefore checked:

- The official Legacy Surveys viewer's full DESI DR1 spectrum overlay returns no objects in RA [141.2755,141.3155], Dec [63.41385,63.43385]. Exact response and GET provenance are `viewer_dr1_catalog.json` and its sidecar. The endpoint was read from the saved viewer page, not guessed from a lens VAC.
- Anonymous NOIRLab `desi_dr1.zpix`, queried using `q3c_radial_query(mean_fiber_ra,mean_fiber_dec,141.2955,63.42385,0.01)`, returns zero rows. Radius is 36 arcsec, no quality/spectral-type/redshift cuts, LIMIT 20. Since zero rows were returned, the limit does not truncate matches. Exact successful response and SQL/HTTP provenance are `l002777_anonymous.csv/json`. Incorrect coordinate-column queries are retained as explicitly named error responses; the successful schema uses the measured mean-fiber coordinates.

The same successful Data Lab procedure returns the known independent L017819 DESI target, providing a positive service control (`l017819_anonymous.csv/json`), without using that object's absence from the strong-lens VAC as a coverage proxy.

DESI's current [public release documentation](https://data.desi.lbl.gov/doc/releases/) says DR1 includes reprocessed EDR commissioning/SV data. Its [publications page](https://data.desi.lbl.gov/doc/papers/) explicitly states that the underlying DR2 spectra and redshifts have not yet been released (page discusses Nov 4, 2026 results); a cached copy with request hash is `desi_papers.html`. A direct public DR2 directory request returned HTTP 401, retained in `public_dr2_index.html` and its provenance. No private credentials or proprietary spectra were requested. DR2 cosmology papers/chains are not a public target-spectrum release.

Consequently this route supplies no new independent public DESI confirmation of SILO790's background redshift. The conclusion is limited to the queried public DR1 target coadd/index coverage and the current documented DR2 release limit. It is not a survey-footprint map, an exhaustive sky-fiber search, a search of unreleased observations, or a refutation of the SDSS spectrum.

Requests were individual public metadata GETs with 30–45 second timeout and at most 1–3 MB each. Initial missing-header/token and schema failures are preserved. The guest identity in `query_anonymous.py` is explicitly the [official client's documented anonymous token](https://raw.githubusercontent.com/astro-datalab/datalab/master/dl/Util.py), not a user credential; client header usage is documented in [queryClient.py](https://raw.githubusercontent.com/astro-datalab/datalab/master/dl/queryClient.py).

References: [DESI public data access](https://data.desi.lbl.gov/doc/access/), [NOIRLab DESI DR1 database description](https://datalab.noirlab.edu/data/desi). DESI data are CC BY 4.0; downstream scientific publication should use the release's required acknowledgement and data citations.
