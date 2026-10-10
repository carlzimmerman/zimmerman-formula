# CFG538 FROZEN CRITERIA ADDENDUM: extension to the combined GHASP 388/500 + 390/466 rotation curves

Dated 2026-10-09. Committed alone, after the criteria (e6eb98396) and BEFORE any GHASP velocity residual has been computed on either set. The frozen text is not edited. The PRIMARY result stays the 390/466-only sample exactly as frozen.

**What changed.** The owner downloaded J/MNRAS/388/500 tablef (Epinat+08a, "Rotation curves for 93 galaxies", 5505 rows, 44-byte records) after the freeze. It is logged in FETCH_LOG.md (sha256 8c528d72...). Its byte layout is one byte wider than 390/466's (ReadMe: Name 1-9, r kpc 11-15, Vrot 33-35, e_Vrot 37-39, NBins 41-42, Side 44). Before this addendum I looked only at its header lines, its row count and the record length; no radius, velocity or residual from it has been used.

**Extension (declared, reported side by side with the primary, same rules).**
1. The same statistic, unchanged (FROZEN_CRITERIA sections 1-8: baryon model, gas rule, bands, bins, `matched()`, shuffle-calibrated Z, adequacy rule, verdict ladder, D1-D3, free M/L, sensitivities), runs on the COMBINED set = 390/466 tablef + 388/500 tablef.
2. **Row checks:** 388/500 tablef 5505 rows; galaxy count reported.
3. **Names:** RC names that are not UGC names (e.g. NGC/IC) are mapped to Korsaga's UGC ID through the RC3 name/altname of the same entry; unmapped galaxies have no Korsaga photometry and drop out (count reported).
4. **Deduplication:** a galaxy (after name normalisation and the RC3 mapping) present in both sets is used once, with its 390/466 curve (the primary set's curve); the count is reported.
5. **SPARC overlaps removed** by the frozen rule; count and names reported. The with-overlap version is reported too.
6. **The extension's ladder label is reported next to the primary's;** the primary headline is the frozen 390/466 result. The extension is an independent-sample enlargement declared after the freeze but before any residual, so its label is quoted as "extension (declared post-freeze, pre-residual)".
7. **MUTATE** (MU1 label shuffle, MU2 +0.071 injection) runs on the extension too, on its primary statistic if adequate, else by the frozen target rule.
8. The section-6 full-GHASP forecast from Korsaga's Rlast/h stays as frozen. The extension's realised coverage is compared with it.
