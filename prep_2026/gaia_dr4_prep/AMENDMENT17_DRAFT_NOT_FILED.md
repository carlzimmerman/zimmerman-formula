# AMENDMENT 17 — DRAFT, NOT FILED (written 2026-09-29; filing needs the owner's explicit go)

This is a draft. `PREREGISTRATION_DR4.md` and every `*_HASH.txt` are untouched. If the owner approves, the text below the line is appended verbatim (append-only) to `PREREGISTRATION_DR4.md` after Amendment 16, with a new `AMENDMENT17_HASH.txt`.

**Why now.** ESA published a draft DR4 data model (zip dated 2026-06-26; sha256 d807eae98acbeec0a0af2ce6a5d7d352298df6f270a1f13207cc8d1becf42c66; PDF issue D rev. 0, 2026-05-20). The candidate names are in `data_assembly/DR4_DRAFT_DATAMODEL_COLUMNS_2026-09-29.md` (aa9c48a9f). It lists a table that frozen cut 12, read literally, could apply to the pairs under test themselves. Settling that before release, in the open, is better than settling it in the release-day manifest.

**Revision 1 (after the fact-check `data_assembly/AMENDMENT17_FACTCHECK_2026-09-29.md`, a87904e3b).** The first draft (76009607a) had four errors:
- It described `nss_resolved_pair` as linear-motion joint solutions. The table also has `ResolvedPairAcceleration`, `ResolvedPairJerk`, `DiverseAcceleration` and `DiverseJerk`; the `Diverse*` types are described as "likely a hierarchical triple or quadruple system".
- Its own-pair exemption would therefore have exempted exactly the contaminants cut 12 exists to catch.
- It counted `nss_multiplicity`, which is a pair-membership list with no solution.
- It counted `nss_masses`, which is derived from other NSS solutions.

The exemption is now limited to the two linear types. The two derived tables are moved to a diagnostic, and the DataLink-only status of `nss_epoch_flags` is recorded. The first draft's text is in git history (76009607a).

**Revision 2 (after the second-pass fact-check `data_assembly/AMENDMENT17_REV1_FACTCHECK_2026-09-29.md`, 2c59e3a22).**
- Page fixes: `nss_multiplicity`'s columns are on p. 776; `optical_pair` is pp. 851–852.
- The `DiverseJerk` wording is quoted separately.
- (a) now says that counting `nss_vim_fl` and `nss_non_linear_spectro` is a reading of row 12's "ANY non-single-star solution", broader than Amendment 15(b)'s wording.
- (b) now requires an unordered pair match that searches both id columns.
- (d) now notes that the stored `solution_type` strings are recorded on release day, and that (b) is moot if no ≥ 8″ pair enters the table.

---

> ### 🚨 AMENDMENT 17 — 2026-09-29, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **THIS AMENDMENT FIXES HOW CUT 12 (THE NSS SCREEN) TREATS THE DR4 NON-SINGLE-STAR TABLES THAT ESA'S DRAFT DATA MODEL LISTS, BEFORE ANY DR4 DATA EXIST. IT CHANGES NO CUT VALUE, THRESHOLD, ESTIMATOR SETTING OR DECISION ROW.** Arms A, B and C, the estimator and every frozen number are untouched. Where it conflicts with Amendments 15(b) or 16(c) on cut 12, Amendment 17 governs.
> **κ = ½ FITTED, NOT DERIVED.**
>
> **What was found.** Source: ESA's draft DR4 data model, 2026-06-26, with printed page numbers. Every name is to be confirmed on release day; ESA states the final model may change.
>
> 1. **The ten tables.** Chapter 10 lists ten tables: `nss_acceleration_astro` (p. 725), `nss_epoch_flags` (p. 741), `nss_masses` (p. 744), `nss_multiple_orbits` (p. 750), `nss_multiplicity` (p. 776), `nss_non_linear_spectro` (p. 777), `nss_resolved_pair` (p. 788), `nss_two_body_orbit` (p. 811), `nss_vim_fl` (p. 843) and `optical_pair` (p. 851). `nss_epoch_flags` is served by DataLink, not TAP.
> 2. **`nss_resolved_pair`.** It holds joint solutions of two resolved sources (`source_id`, `source_id_secondary`).
>    - Its solution types (pp. 789–791) are `ResolvedPairFixed` (common proper motion and parallax), `ResolvedPairLinear` (common parallax, different proper motions), `ResolvedPairAcceleration`, `ResolvedPairJerk`, and `DiverseAcceleration` / `DiverseJerk`. `DiverseAcceleration` is "a significant acceleration term not associated with the visible-pair motion ... Likely a hierarchical triple or quadruple system"; `DiverseJerk` says the same of an "acceleration and/or jerk term".
>    - No separation range is stated. This sample's pairs are at least 8″ apart (s > 2 kAU, d < 250 pc). Whether such pairs enter the table is unknown until release.
>    - Frozen row 12 rejects a pair if either component has "ANY DR4 non-single-star solution (astrometric orbit, acceleration, or spectroscopic orbit)". Read literally, a pipeline pair solved jointly as a linear-motion resolved pair would be rejected for being the pair under test. That is not what cut 12 is for: its stated ground is undetected companions that inflate γ.
> 3. **The derived and auxiliary tables.**
>    - `nss_masses` is "masses derived from the non-single stars (NSS) solutions with orbital parameters" (p. 744).
>    - `nss_multiplicity` lists pair membership (`number_of_pairs`, `related_sources`; p. 776), not solutions.
>    - `nss_epoch_flags` holds per-transit flags with a model label, no parameters (p. 741).
>    - `optical_pair` holds chance alignments, whose astrometry is `gaia_source`'s. Its `acceleration_flag` marks a member identified as an unresolved acceleration solution (pp. 851–852).
>
> **The amendment.**
>
> **(a) Counted tables.** Cut 12 counts the tables that carry non-single-star solution parameters. In the draft's names these are `nss_acceleration_astro`, `nss_multiple_orbits`, `nss_non_linear_spectro`, `nss_resolved_pair` (subject to (b)), `nss_two_body_orbit` and `nss_vim_fl`. Every solution type in them counts, with no quality threshold, as in Amendment 15(b).
> - This reads frozen row 12's "ANY DR4 non-single-star solution" as every table of solutions. `nss_vim_fl` (variability-induced mover solutions, p. 843) and `nss_non_linear_spectro` (spectroscopic models "compatible with a trend", p. 777) are counted under that reading. Amendment 15(b)'s narrower wording ("an astrometric orbit, an acceleration solution, or a spectroscopic orbit") would not name them, so counting them is a stated reading, not a restatement.
> - Not counted: `nss_masses` (derived from counted tables), `nss_multiplicity` (a membership list), `nss_epoch_flags` (flags; DataLink) and `optical_pair` (chance alignments).
> - A table that ESA adds or renames at release is placed by this same rule, and the placement is recorded in the fetch manifest before the data are opened.
>
> **(b) Own-pair exemption, linear types only.** An `nss_resolved_pair` entry whose two `source_id`s are exactly this pipeline pair's two components, matched as an UNORDERED pair, does not reject the pair if its type is `ResolvedPairFixed` or `ResolvedPairLinear`. The table does not say which component is the brighter, so every match searches both `source_id` and `source_id_secondary`.
> - An own-pair entry of any other type rejects the pair: `ResolvedPairAcceleration`, `ResolvedPairJerk`, `DiverseAcceleration` or `DiverseJerk`.
> - An entry of any type that pairs a component with a **third** source rejects the pair.
> - *Estimate, not a measurement:* at s = 2 kAU and M = 1.5 M☉, the pair's own relative acceleration moves it by about 2 × 10⁻⁴ AU over 66 months. That is ~0.001 mas at 250 pc and ~0.02 mas at 10 pc, so a significant acceleration or jerk term is not expected from the pair's own orbit.
>
> **(c) Diagnostic and variants: reported, never substituted.**
> - **The manifest records, before the data are opened:**
>   - per-table and per-`solution_type` row counts for the sample's components;
>   - own-pair entries by type;
>   - third-source entries;
>   - the number of sample components that appear only in an uncounted table (`nss_masses`, `nss_multiplicity`), or that carry a nonzero `optical_pair.acceleration_flag` without a counted solution. Expected 0; if not 0, the number is reported and flagged.
> - **Variant V17a:** own-pair linear entries also reject (the literal reading).
> - **Variant V17b:** `nss_resolved_pair` is not counted at all (the strict reading of row 12's parenthesis).
> - Both variants are reported beside the primary with γ̂.
>
> **(d) Against interest.**
> - The linear exemption keeps a pair that Gaia solved jointly. If that pair also hides an inner companion that Gaia did not solve, the exemption keeps a contaminant that V17a would remove.
> - Rejecting own-pair acceleration and jerk entries could drop a genuine pair if the estimate in (b) is wrong for the nearest pairs. V17b brackets that.
> - The stored `solution_type` strings are not printed in the draft; they are recorded on release day, before the data are opened. If no pair ≥ 8″ apart enters `nss_resolved_pair`, (b), V17a and V17b change nothing for this sample.
> - Counting third-source resolved pairs may overlap with cut 13 (resolved triples) and cut 8 (`ipd_frac_multi_peak`). A pair rejected by several cuts is counted once, as in the frozen cut flow.
>
> **Untouched:** the estimator; the cut table's values and thresholds; the error model; the strictness ladder, including its NSS-off rung; the frozen N = 30,000; both a₀ footings; Arms A, B and C; Amendments 14–16's decision rows and cut 9/13 choices. κ = ½ remains fitted.
>
> **Provenance.**
> - `prep_2026/gaia_dr4_prep/AMENDMENT17_DRAFT_NOT_FILED.md`: the draft, revised twice after two fact-checks.
> - `data_assembly/DR4_DRAFT_DATAMODEL_COLUMNS_2026-09-29.md` and `data_assembly/dr4_draft_datamodel/`: the draft data model's table and column lists; zip sha256 above.
> - `data_assembly/AMENDMENT17_FACTCHECK_2026-09-29.md` and `data_assembly/AMENDMENT17_REV1_FACTCHECK_2026-09-29.md`: page-level verification.
> - `prep_2026/gaia_dr4_prep/dr4_ready_1/cut12_nss_union.py`: the loader, whose table list is run-time data.

---

**Implementation note (not part of the amendment text).** `cut12_nss_union.py` reads per-table id lists. (b) needs the loader to:
- read `source_id_secondary` and `solution_type` for two-source tables;
- classify each entry as own-pair or third-source;
- exempt only own-pair `ResolvedPairFixed` / `ResolvedPairLinear`.

(c) needs per-type counts and the uncounted-table diagnostic. All of this is new code only, with synthetic tests (an own-pair linear entry kept, an own-pair `DiverseAcceleration` entry rejected, a third-source entry rejected) and a MUTATE control. It should be built whether or not this amendment is filed, so that every reading can run.
