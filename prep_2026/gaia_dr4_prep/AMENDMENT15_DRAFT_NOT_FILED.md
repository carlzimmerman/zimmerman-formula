# AMENDMENT 15: DRAFT, NOT FILED. The DR4 table mapping for the frozen cuts

**Status: draft.** It is not part of the pre-registration until the owner files it. Filing appends it to `PREREGISTRATION_DR4.md` with a hash record (`AMENDMENT15_HASH.txt`). It must be filed **before the Gaia DR4 release on 2 December 2026**, or it is worthless.

## Why

ESA's DR4 content page (cosmos.esa.int/web/gaia/dr4, read 2026-09-28) describes a catalogue organised differently from DR3's.
- `gaia_source` is a curated subset: about 2 billion of the 2.8 billion processed sources, "considered to have both high-quality astrometry and high-quality photometry". Its parameters are "consolidated from several different processing modules such that the best-suited model has been applied for a given source."
- Four tables cover all of the ~2.8 billion sources: `all_source_astrometry`, `all_source_photometry`, `all_source_rvs` and `all_source_flags`.
- Non-single-star solutions sit in dedicated `nss_*` tables, and epoch data are served via DataLink.
- The full data model is published only with the release.

The frozen cut table (§1.2) defines every cut by a physical quantity, not by a table. The DR3-era pipeline (`catalog_builder/fetch_extract.py`) reads every quantity from `gaia_source`. As written, then, the sample's source table would be chosen after the data exist. This amendment makes that choice now.

## The amendment

**(a) The base sample is `gaiadr4.gaia_source`, the curated subset.**
- Each quantity used by cuts 1–11 and 13–15 comes from `gaia_source` where DR4 carries it there.
- Otherwise it comes from the `all_source_*` table that carries it (astrometry, photometry, radial velocities, or flags such as RUWE and ipd_frac_multi_peak), joined on `source_id`.
- DPAC recommends the consolidated best-suited-model parameters. The frozen cuts (G < 17, ϖ > 4 mas, ϖ/σ_ϖ ≥ 40, RUWE < 1.4) select exactly the sources the curated subset is built to contain.

**(b) Cut 12, the NSS screen, reads the DR4 `nss_*` tables.** A pair is rejected if either component's `source_id` appears in any DR4 non-single-star table carrying an astrometric orbit, an acceleration solution, or a spectroscopic orbit.
- This applies to every solution type, with no quality threshold on the NSS solution.
- It is the frozen text of cut 12, mapped to tables. The NSS-off contamination probe of the strictness ladder is unchanged.

**(c) A sample-definition variant, reported and never substituted.** The same cuts are applied with the `all_source_*` tables as the base (all ~2.8 billion sources). It runs alongside the primary, like the strictness ladder, and measures what the curated base drops.

**(d) Names only on release day.**
- Table and column names are read from the published DR4 data model and recorded in the fetch manifest.
- No cut value, threshold, estimator setting or decision row changes.
- If DR4 lacks a quantity a frozen cut needs, that cut is reported as **unimplementable**. The run proceeds without it and the result is flagged. No substitute quantity is chosen after the data exist.

**(e) Against interest.** The curated base could drop genuine pairs whose photometry DPAC judged low-quality, for example close pairs with BP/RP blending. Variant (c) measures that. A difference between (a) and (c) larger than σ_fit is reported as a systematic and never used to pick one.

**Untouched:** the estimator, the 16-row cut table's values, the error model, the strictness ladder, the NSS screen's definition, the frozen N = 30,000, both a₀ footings, Arms A, B and C, and Amendment 14's decision rows. κ = ½ remains fitted.
