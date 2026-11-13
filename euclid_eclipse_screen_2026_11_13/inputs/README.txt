Euclid DR1: CSV-only collaborator snapshot
==========================================

Snapshot cutoff: 2026-10-29T13:31:28Z
Membership: exactly 15,071 distinct Grade A/B objects of the lens-finding catalogue
v5 (Holloway, 19 Oct 2026), from the consolidated manifest: the 15,072
v5 A/B objects minus one without a usable model (listed below).
This is an interim modelling snapshot, not a fully completed or scientifically
validated model catalogue. No candidate is removed for a missing fit or band.

Start with dr1_catalogue_15072_master.csv: one row per parent v5 A/B object (15,072): the
15,071 modelled candidates plus one placeholder row (inspection_status
not_modelled) for the excluded objects: identity, grade, score and position
only; tile_id, cutout_batch and every model cell blank, flags False. Blank
cells mean unavailable/non-finite measurements, never zero. Semicolons separate list values.
master_columns.csv defines every master column. unique_identifier is the v5
object key; tile_id is the cutout its model was fitted on (sample_manifest.csv).
Objects remodelled on a new v5 cutout (cutout_batch v5; tile names end _v5):
13. Objects whose model was fitted on an earlier
cutout than the v5 one centred on the final position (the fits stand):
69.

Coverage at this snapshot
-------------------------
- Initial parametric-source (vis_lp) fits: 15,009.
- Delaunay-source (vis_pix) fits: 14,984.
- VIS single-Sersic lens/source fits: 14,968.
- Every expected band has a completed SED fit: 14,720.
- Every expected band has all four main photometry medians: 14,620.
- Metadata read errors: 0 (see metadata_errors.csv).

Visual inspection
-----------------
- Inspected models: 14,989. Pending: 82.
- The inspection columns hold the votes of the model-inspection round
  (final_classifications.csv), matched to the modelled cutout (tile_id):
  one count per label and inspection_consensus_75, the label holding at least
  75% of the votes (else No Consensus).
- PENDING rows are placeholders: their models have not been inspected yet
  (never inspected, newly remodelled on a v5 cutout, or a fit that never
  finished). Their vote cells are blank, not zero. The inspection values of
  the pending lenses will be added in a later snapshot.

The completion and photometry flags deliberately differ: a completed search may
lack a latent summary or have non-finite derived quantities. Neither flag is a
visual-inspection success label. grade is a lens-finding grade, not a judgement
of model reliability. Do not treat a blank multiband measurement as a dropout.

Tables and numerical conventions
-------------------------------
- lens_mass.csv: SIE mass and external-shear parameters from vis_pix, effective
  Einstein radius and magnification from that fit's stored derived summaries.
  The effective Einstein radius is derived from the critical curve and differs
  from the SIE einstein_radius parameter.
- lens_sersic.csv / source_sersic.csv: six VIS single-Sersic light parameters.
  effective_radius is the profile's stored half-light-radius parameter (arcsec);
  it is not converted to a circularised radius. Source sizes are source-plane
  sizes. The Sersic fit fixes the lens mass from the initial parametric fit.
- photometry.csv: one row per available candidate/band derived summary. All
  fluxes, including aperture fluxes, are in MICROJANSKYS, not magnitudes.
  lens_flux is foreground light; lensed_source_flux is the observed lensed
  source; source_flux is reconstructed source-plane flux. Magnification is
  dimensionless. Conditional SED-fit uncertainties do not propagate uncertainty
  in the frozen mass model. Fluxes follow the pipeline's modelling masks.
- astrometric_offsets.csv: fitted (y,x) band grid offsets in arcsec relative to
  VIS, subtracted from the band grid before evaluating its model. No prior-edge
  quality flags are inferred in this snapshot.
- wcs.csv: stored fit astrometry for each stage/band. crval_ra_deg/dec_deg are
  the fitted maximum-likelihood lens-light sky centre, not FITS CRVAL headers;
  crpix_x/y refer to the 1-based WCS pixel of the image-plane origin. Columns
  ending _arcsec are angular offsets; _deg are degrees. Other stored fields
  retain their original names. Array cells use semicolons.
- source_clumps.csv: stored clump locations and associated image positions;
  zero-based clump_index is local to the fit, not a cross-band object match.
- result_provenance.csv: selected result IDs, relative paths and timestamps.
  Results are selected independently per candidate/stage/band by newest
  modification time at or before the cutoff, requiring a .completed marker.
  These timestamps record stored files (copies can change modification times).
  Fits completing after the cutoff are reserved for a future snapshot.

An unsuffixed scientific value is a posterior median. _max_lh is the stored
maximum-likelihood value. _lower_1_sigma / _upper_1_sigma and corresponding
3_sigma columns are interval BOUNDS, not +/- errors. The master carries medians
and 1-sigma bounds; the component tables additionally carry maximum-likelihood
values and 3-sigma bounds. Centres use PyAutoLens (y,x) = (centre_0,centre_1).
Ellipticity components, shear components and Sersic indices are dimensionless.
Expected bands are read from the input FITS headers. No new likelihood evaluations
or lens fits were performed for this export.
Witt-Wynne approximations and images/FITS are not regenerated or included here.

Excluded parent-catalogue candidates (1)
---------------------------------------
- EUCL-DR1-L020583 (no_model): sep1 cutout not in the segmentation delivery, so never modelled

These objects have no lens model (never modelled) or a model that is not of the
lens; they are not failed fits or multiband losses. Each has a not_modelled
placeholder row in dr1_catalogue_15072_master.csv; excluded_one_candidates.csv supplies positions, grade,
the reason and the recorded notes.

Validation: membership and uniqueness were checked against the full v5 A/B
parent catalogue and selected manifest. File sizes,
SHA-256 hashes and table row counts are supplied in file_manifest.csv.
