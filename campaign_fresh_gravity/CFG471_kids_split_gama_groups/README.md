# CFG471: the KiDS early/late split by spectroscopic host status (GAMA G3C groups). NON-DISCRIMINATING, underpowered

- **Criteria:** `FROZEN_CRITERIA.md` (0ce400d28), committed before the script and before any lensing number for a GAMA subset.
- **Script:** `cfg471_gama_groups.py`, about 15 s. Main run: 6 of 7 checks pass, 0 load-bearing failures, exit 0.
  MUTATE run: M1 fails as required, exit 1.
- **Data:** GAMA DR4 G3C (`G3CGalv10`, `G3CFoFGroupv10`) from the Data Central TAP service; see `FETCH_LOG.md`. The files sit
  in `_external_data/cfg471/` (git-ignored) and the script checks their sha256.
- κ = ½ is fitted. B's law predicts zero early-minus-late difference in K1 under both footings (+0.0002 in amplitude units,
  canonical and alt). No dark-matter particle; the cold mass is still required.

## Bottom line

**NON-DISCRIMINATING by the frozen rule, and UNDERPOWERED to FAIL** (1/σ_F = 2.4 < 3). This was declared before scoring as
the most likely outcome. GAMA covers only 12 of the 50 June patches, and only 7,207 field early types and 808 group centrals
match. The numbers lean the same way as CFG446 but cannot decide. Early types that GAMA places in no group carry
A_F = 0.89 ± 0.42 (2.1σ from zero, 0.3σ from the full split). Group centrals carry A_C = 1.34 ± 1.82. The difference is
ΔA = +0.45 ± 1.91.

So CFG446's FAIL stays the standing result, at photo-z reach. The spectroscopic check of its caveat is consistent with it
(field early types sit at the full-split level, not the late level), but it does not confirm it at > 3σ. Even a SUPPORTED
verdict would not have discriminated the framework from ΛCDM.

| class (matched to all matched early, (log M*, z) cells 0.2 dex × 0.1) | N | A | A/σ |
|---|---|---|---|
| **F**: GAMA-detected (r < 19.8), in no G3C group | 7,207 | **+0.89 ± 0.42** | +2.1 |
| **C**: IterCen of a big group (N_fof ≥ 3, or ≥ 2 with M_h ≥ 10^12.5 M☉) | 808 | **+1.34 ± 1.82** | +0.7 |
| S: G3C member, not IterCen (reported) | 2,847 | +1.42 ± 0.83 | +1.7 |
| P: IterCen of a low-mass pair (reported) | 239 | +1.39 ± 2.97 | +0.5 |
| ΔA = A_C − A_F | | +0.45 ± 1.91 | +0.2 |

Unmatched gives the same verdict (A_F 0.89 ± 0.42, A_C 1.58 ± 1.49). Reported variants agree: BCG centrals give
A_C 1.70 ± 1.92. The 36-sub-patch jackknife gives A_F 0.89 ± 0.39 and A_C 1.34 ± 1.33. Group-hosted (C+S+P, N 3,894) minus
field is +0.52 ± 0.49.

- **Power fell short of the declared estimate:** σ_F was 0.42 against 0.35 declared, and σ_C 1.82 against 0.89. The declared
  model did not include matching weights or the 12-patch jackknife. The measured P(FAIL | A_F = 1) is about 0.27 (0.44 was
  declared).
- **A finding, not a test:** 25.6% of the matched early "isolated" lenses (2,847 of 11,101) are G3C group members that are not
  their group's IterCen. The photo-z isolation criterion admits spectroscopic group satellites. They are kept in class S, out of
  both test classes.

## Controls

- **C0:** the per-lens sums reproduce CFG88's K1 split to 5 × 10⁻¹⁴ and its χ² of 35.0418/7.
- **C1 (footprint):** all early lenses in the GAMA boxes, against the footprint late reference, give A_box = 0.87 ± 0.42.
  That is consistent with 1 (−0.3σ) and only 2.1σ from zero. CFG446's full-sample amplitude is reproduced inside the
  footprint. The footprint alone carries the split at about 2σ, which caps every subset test here.
- **C2:** the chance-match rate at shifted positions is 0.14% of the real rate. Spec − photo z robust scatter is 0.025.
- **C3:** the classes partition the matched early lenses. **C4:** null calibration std of ΔA/σ is 1.09 (window [0.7, 1.4]).
  **C5:** the sha256 of both G3C files matches the fetch log.
- **MUTATE (class labels shuffled, 20 shuffles):** the median |ΔA|/σ is 0.74 < 1, so M1 fails as required (exit 1). The real
  contrast (0.24σ) is itself null, smaller than the shuffled median, so this control only confirms that the statistic has no
  built-in contrast. It does not show an environment signal.

## Caveats

- The jackknife uses the 12 June patches that touch GAMA, with D_full and C⁻¹ fixed (a departure from CFG446, declared). With
  12 patches the error bars are themselves uncertain by about 20%. There is no photo-z, intrinsic-alignment or satellite-term
  covariance (CFG107: ×1.8).
- The late reference is the footprint's late lenses (17,442), so its noise enters every A.
- G3C completeness and edge effects (GroupEdge) are not modelled. Class F can hold centrals whose companions fall below
  r = 19.8.
- Departures, all declared in the frozen file: coarser matching cells; the union mass branch for "big group" (286 → 808
  centrals, chosen from counts for power); no own-covariance χ².

## Owner items

- None needed for this lane. A decisive spectroscopic version needs more overlap than GAMA's 180 deg² gives. The candidates
  are the KiDS-N overlap with SDSS/BOSS groups (bright end only), or DESI BGS group catalogues when public. Either would be a
  new fetch (owner's go).

Nothing here says the data favour the framework or ΛCDM, or that the theory is closed.
