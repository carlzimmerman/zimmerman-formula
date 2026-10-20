# CFG887 — is CFG880's "clump σ not universal" driven by measurement systematics?

Criteria: `FROZEN_CRITERIA.md` (1ff227ac7, committed alone before any comparison; owner block 880–889). Run: `python3 cfg887.py`
(`CFG887_MUTATE=1` → differences doubled). About a minute, one core. CFG880's fit is exec'd unchanged. κ = ½ fitted.

## Result — CLASS: **CFG880 STANDS** (both footings, as frozen), with a post-hoc caveat
- **Inter-catalogue extra scatter.** Over 54 pairs (LVD vs McConnachie 2012: 41; LVD vs Collins 2013: 13), the σ values agree
  within their quoted errors: s_x = 0.000 (95% upper 0.106; bootstrap 68% upper 0.14).
- **Floors.** The primary floor (0) and the conservative floor (0) leave CFG880 exactly as committed (s_int 0.380, 95% 0.281–0.510).
  The pessimistic floor (0.075) gives s_int 0.320 (95% 0.231–0.451). Still NOT UNIVERSAL on both footings.
- **Unmatched names** (listed, not forced, as frozen): Segue II, Sextans (I), Andromeda XII, And XXX.
- **Largest single disagreements:** Bootes II −1.70 (err 0.79), Andromeda XV −1.01, Tucana −0.94, Cetus −0.72.

**POST-HOC caveat (disclosed; added after the first run, not graded).** 15 of the 54 pairs carry identical values, because the
catalogues cite the same measurement, and those pairs hide systematics by construction. On the 39 pairs that differ:
- s_x = 0.146 (95% 0–0.278);
- per-catalogue floor 0.103 (95% upper 0.197); unsplit 0.146 (95% upper 0.278).

CFG880's own floor scan flips from NOT UNIVERSAL to UNDECIDED between floors 0.15 and 0.20. So **at the central systematic level
the result holds; at the upper end of the plausible systematic range it would weaken to UNDECIDED.** CFG880 is solid at central
values but not bulletproof against per-dwarf σ systematics of ~20%.

## Controls
- K1 PASS: floor 0 reproduces CFG880's committed s_int and 95% interval exactly (both footings).
- MUTATE (differences ×2): s_x 0.509, floors 0.36 / 0.51 → SYSTEMATICS-LIMITED. The test responds.

## Disclosed limits
M12 is older than LVD: differences mix systematics with improvements from more data (upper-leaning). Shared stars and shared
methods are invisible (lower-leaning); the identical-pair diagnostic shows how large that blind spot is. Symmetrised errors are used.
