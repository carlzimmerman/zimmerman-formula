# EUC19 (GRADE-B MASK TABLE): DATA NOTE

2026-11-14. A data step, not a graded lane. No statistic, no word, no criteria. Owner's go of 2026-11-14: "fetch
the rest of the grade-B masks too".

**What it is.** EUC17 showed that the Euclid lens catalogue's stellar mass is the mass inside the modelling circle
and fetched that circle's radius for sample P and for the wide grade-B lenses (3,357 lenses,
`closure_2026_11_13/EUC17_mask_aperture_mass_reread/euc17_masks.csv`). This folder holds the same record for the
grade-B lenses of sample S that EUC17's table lacks: grade B passing EUC1's cuts (2,981 lenses) minus the 153 already
held, **2,828 lenses**.

**Source.** `https://euclid-eclipse-lenses.org/files/<lens_model_tile_id>/dataset/info.json`, one file of about
134 bytes per lens (`pixel_scale`, `mask_radius` in arcsec, `mask_centre`). One paced stream, generic client name,
three tries. Raw records outside git with a manifest.

**Files.** `euc19_fetch.py`, `euc19_fetch.out` (counts, bytes, time), `euc19_masks.csv` (same columns as EUC17's
table: identifier, tile id, HTTP status, has_mask, mask radius, mask centre, pixel scale, bytes, sha256).

**Outcome.** 2,828 of 2,828 records fetched (HTTP 200, positive mask radius), 365,217 bytes, 1,183 s. With EUC17's
table, **every one of the 6,173 lenses of sample S now has a mask record.**

**With both tables every lens of sample S has a mask record.** That opens the lanes EUC18
could not grade: EUC4's secondary and complement bins, EUC8's dispersion sample and non-wide classes, EUC5 / EUC5R on
S, EUC6 and LNJ1.

**Nothing has been derived from this table.** No in-mask share, no corrected mass and no statistic was computed
from it before this note was written. A lane that uses it freezes its criteria first.
