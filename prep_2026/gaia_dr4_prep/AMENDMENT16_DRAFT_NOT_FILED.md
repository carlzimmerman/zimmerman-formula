# AMENDMENT 16: DRAFT, NOT FILED. Cut 9 and cut 13 brought into line with the frozen text and the pipeline

**Status: draft.** It is not part of the pre-registration until the owner files it (append to `PREREGISTRATION_DR4.md`, plus `AMENDMENT16_HASH.txt`). It must be filed **before the Gaia DR4 release on 2 December 2026**. Written 2026-09-28 by the orchestrating session after the release-day checklist (`RELEASE_DAY_CHECKLIST.md`, section 0) found that Amendment 15 as filed and the code disagree. Nothing here changes a cut value, threshold or estimator setting except where item (b) says so explicitly.

## What was found (each checked against the committed files)

1. **Cut 9.** Frozen §1.2 row 9 reads "A_V < 0.5 | Banik+24 §2.4.1". The pipeline implements exactly that source: `catalog_builder/build_catalog.py` `av_sfd98` reads the SFD98 maps (A_V = 3.1 E(B−V), raw scale, no ×0.86 recalibration), and its docstring cites Banik+24 §2.4.1. Amendment 15(a) says instead that cut 9 "comes from the DR4 astrophysical-parameter (`ap_*`) table". That clause was added at filing from ESA's content page and was not checked against the cited source or the code. As filed, it would make the primary cut differ from the frozen citation.
2. **Cut 13, catalogue.** Amendment 15(a) says the search runs against the full `all_source_astrometry` (about 2.8 billion sources). `build_catalog.py` `third_star_flags` searches the extract (`parallax > 3.5`, `parallax_over_error > 5`, `parallax_error < 2`, non-null G, |b| > 10) and no all-source query or G < 20 lookup exists yet. The frozen row asks for "a co-moving third Gaia source ... with G < 20", so the full search is what the frozen text needs; the code does not yet do it.
3. **Cut 13, criterion.** Frozen row 13: parallax within 3σ and "proper motion within 5σ of the pair". The code tests `dpar < 3` and `dmu < orb + 2·sdmu`, where `orb = 0.44428 · parallax^1.5 · θ^-0.5` is an orbital-motion allowance (mas/yr; θ in arcsec). For DR4-class proper-motion errors (a few hundredths of mas/yr) the orbital term (about 0.3 mas/yr at 250 pc and 30 kAU) exceeds 5σ, so the code flags more thirds than the literal text (a stricter cut). No earlier amendment declares the orbit-aware form (searched the pre-registration for "orbit", "sdmu" and "5 sigma": only row 13 itself matches).

## The amendment (proposed)

**(a) Cut 9.** The primary cut 9 is SFD98 as implemented (Banik+24 §2.4.1: A_V = 3.1 E(B−V) on the raw SFD scale; both stars). The `ap_*` extinction of Amendment 15(a) is a **reported variant only**, never substituted. Amendment 15(a)'s sentence that cut 9 "comes from the ap_* table" is superseded by this item.

**(b) Cut 13.** The primary criterion is the frozen text read literally: parallax within 3σ and proper motion within 5σ of the pair, G < 20, within projected 30 kAU of either component, searched in the full `all_source_astrometry` with G from `all_source_photometry`. The pipeline's orbit-aware bound (`dmu < orb + 2·sdmu`) runs alongside as a **reported variant**, never substituted, so that the DR3-validated form is still measured. A difference between primary and variant larger than σ_fit is reported as a systematic and not used to choose.
*Open point for the owner before filing:* the alternative is to declare the orbit-aware form primary (it is the physically motivated one, and it is what the DR3 validation used) and the literal 5σ text the variant. Under this draft the literal text is primary because the frozen text was written first; either choice is legitimate if it is recorded before release.

**(c) Implementation is stated as required work, not assumed.** Before release the following must exist and pass a DR3 dry run: the all-source search for cut 13; the variant runs of Amendment 15(c); the cut 12 union over the DR4 `nss_*` tables (the code reads one integer today; the release-day list of counted tables is recorded in the fetch manifest, decided before the data are opened). A cut that cannot be implemented on release day is reported UNIMPLEMENTABLE and flagged, as in Amendment 15(d).

**(d) Against interest.** The literal 5σ criterion may miss a real third star whose orbital motion exceeds 5σ, biasing γ̂ high; the variant measures this. SFD98 is a 2-D total-column map and is conservative at d < 250 pc; `ap_*` extinction is star-specific and may pass more pairs.

**Untouched:** the estimator, the cut table's values and thresholds (row 13's 3σ / 5σ / G < 20 / 30 kAU are read literally), the error model, the strictness ladder, the frozen N = 30,000, both a₀ footings, Arms A, B and C, and Amendment 14's decision rows. κ = ½ remains fitted.

## Before filing

- Owner decision on the open point in (b).
- Filing appends the amendment text and `AMENDMENT16_HASH.txt` (sha256 before = `c8727e42748916afe84bc4c94b7a40fd314836e64ec86dc71fa1ebc0fc7fd33d`, the file after Amendment 15).
