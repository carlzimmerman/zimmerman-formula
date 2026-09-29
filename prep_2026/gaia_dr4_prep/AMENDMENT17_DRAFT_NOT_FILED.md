# AMENDMENT 17 — DRAFT, NOT FILED (written 2026-09-29; filing needs the owner's explicit go)

This is a draft. `PREREGISTRATION_DR4.md` and every `*_HASH.txt` are untouched. If the owner approves, the text below the line is appended verbatim (append-only) to `PREREGISTRATION_DR4.md` after Amendment 16, with a new `AMENDMENT17_HASH.txt`.

**Why now.** ESA published a draft DR4 data model (zip dated 2026-06-26; sha256 d807eae98acbeec0a0af2ce6a5d7d352298df6f270a1f13207cc8d1becf42c66; candidate names in `data_assembly/DR4_DRAFT_DATAMODEL_COLUMNS_2026-09-29.md`, aa9c48a9f). It lists a table that frozen cut 12, read literally, could apply to the pairs under test themselves. Settling that before release, in the open, is better than settling it in the release-day manifest.

---

> ### 🚨 AMENDMENT 17 — 2026-09-29, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **THIS AMENDMENT FIXES HOW CUT 12 (THE NSS SCREEN) TREATS THE DR4 NON-SINGLE-STAR TABLES THAT ESA'S DRAFT DATA MODEL LISTS, BEFORE ANY DR4 DATA EXIST. IT CHANGES NO CUT VALUE, THRESHOLD, ESTIMATOR SETTING OR DECISION ROW.** Arms A, B and C, the estimator and every frozen number are untouched. Where it conflicts with Amendments 15(b) or 16(c) on cut 12, Amendment 17 governs.
> **κ = ½ FITTED, NOT DERIVED.**
>
> **What was found (draft data model, 2026-06-26; every name is to be confirmed on release day, and ESA states the final model may change).**
>
> 1. The draft's non-single-star group has ten tables: `nss_acceleration_astro`, `nss_epoch_flags` (new), `nss_masses`, `nss_multiple_orbits`, `nss_multiplicity`, `nss_non_linear_spectro`, `nss_resolved_pair`, `nss_two_body_orbit`, `nss_vim_fl` and `optical_pair`.
> 2. `nss_resolved_pair` holds joint astrometric solutions for two resolved sources (`source_id` and `source_id_secondary`, a common parallax, differential positions and proper motions). Frozen row 12 rejects a pair if either component has "ANY DR4 non-single-star solution (astrometric orbit, acceleration, or spectroscopic orbit)". Read literally, a pair of this pipeline that Gaia solved jointly as a resolved pair would be rejected for being the pair under test. That is not what cut 12 is for: its stated ground is undetected inner companions that inflate γ. Whether any pipeline pair appears there is unknown. The sample's pairs are at least 8″ apart (s > 2 kAU, d < 250 pc).
> 3. `nss_epoch_flags` holds per-transit flags attached to NSS solutions (`transit_id`, `al_used` and similar), not solutions of its own. `optical_pair` names chance alignments (by its name and five columns; its content is to be confirmed).
>
> **The amendment.**
>
> **(a) Counted tables.** Cut 12 counts every DR4 table that carries a non-single-star *solution*. In the draft's names these are `nss_acceleration_astro`, `nss_masses`, `nss_multiple_orbits`, `nss_multiplicity`, `nss_non_linear_spectro`, `nss_resolved_pair` (under (b)), `nss_two_body_orbit` and `nss_vim_fl`. Every solution type counts, with no quality threshold, as in Amendment 15(b).
> - `nss_epoch_flags` (flags, not solutions) and `optical_pair` (not physical) are not counted.
> - A table that ESA adds or renames at release is placed by this same rule, and the placement is recorded in the fetch manifest before the data are opened.
>
> **(b) Own-pair exemption.** An `nss_resolved_pair` entry (or an entry of any table that names two sources) whose two `source_id`s are exactly this pipeline pair's two components does not by itself reject that pair. An entry that pairs a component with any **third** source rejects the pair, because that is a physical companion, which is what cut 12 exists to find.
>
> **(c) Reported, never substituted.**
> - Variant V17a: the own-pair entries of (b) are rejected, which is the literal reading.
> - Variant V17b: `nss_resolved_pair` is not counted at all, which is the strict reading of row 12's parenthesis.
> - Both are reported beside the primary with γ̂.
> - The manifest records, before opening: per-table and per-`solution_type` row counts for the sample's components; the number of own-pair entries; and the number of third-source entries.
>
> **(d) Against interest.** The exemption keeps a pair that Gaia solved jointly. If such a pair is also a hierarchical system whose inner companion Gaia did not solve, the exemption keeps a contaminant that V17a would remove. At s > 2 kAU the relative orbit is not expected to show curvature over 66 months, so a joint solution of the pair itself is expected to be linear-motion only. That is an expectation, not a measurement, and V17a measures it.
> - Counting third-source resolved pairs may overlap with cut 13 (resolved triples) and cut 8 (`ipd_frac_multi_peak`). A pair rejected by several cuts is counted once, as in the frozen cut flow.
>
> **Untouched:** the estimator, the cut table's values and thresholds, the error model, the strictness ladder (including its NSS-off rung), the frozen N = 30,000, both a₀ footings, Arms A, B and C, Amendments 14–16's decision rows and cut 9/13 choices. κ = ½ remains fitted.
>
> **Provenance.**
> - `prep_2026/gaia_dr4_prep/AMENDMENT17_DRAFT_NOT_FILED.md` (this draft).
> - `data_assembly/DR4_DRAFT_DATAMODEL_COLUMNS_2026-09-29.md` and `data_assembly/dr4_draft_datamodel/` (the draft data model's table and column lists; zip sha256 above).
> - `prep_2026/gaia_dr4_prep/dr4_ready_1/cut12_nss_union.py` (the loader; its table list is run-time data).

---

**Implementation note (not part of the amendment text).** `cut12_nss_union.py` reads per-table id lists. (b) needs the loader to read `source_id_secondary` for two-source tables and compare each entry with the pipeline pair, and (c) needs per-`solution_type` counts. Both are small changes to new code only, with a synthetic own-pair / third-source test, and should be made whether or not this amendment is filed, so that either reading can run.
