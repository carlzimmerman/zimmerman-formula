# AL4: MOCK validation of filed AC1 addendum G4. FROZEN CRITERIA, before any script or number

Written before any AL4 code or run, and committed alone.
- Governing text: `rebuild_2026_10_22/AC1_alma_condor_predictions/ADDENDUM_G4_2026-11-06.md`. The owner filed it in chat on
  2026-11-06 ("File G4"), commit 8ff85f806e. It is byte-identical to draft 2e6bbfe773.
- MOCK cubes only. No ALMA data and no download. Nothing is scored.
- No frozen file, prediction, gate, seal or error floor is changed.
- G3 stays filed, and it stays FAILED VALIDATION (AL3).
- κ = ½ FITTED; one disc excludes no model; not theory closed.

## G4's validation requirements, verbatim from the filed text ("Validation before G4 touches the real cube")
- Settings and seeds as AL3 (release settings: pix 0.015", beam 0.105" × 0.087", dv 6, 0.132 mJy/beam, S dV 0.718, V_c 430,
  Tadaki inclination). AL3's writer passes K0 and is reused. AL3's frozen-fitter records may be reused for the frozen side, by sha256.
- **(C) Calibration of the collapse class, frozen fitter only, before any G4 fit.**
  - Class (e) is class (a) + (c) (offset −172, ρ 0.24) with the gas R_e scaled by f, stepping up the ladder f = 2, 3, 4 (flux fixed).
  - The class used is the smallest f at which the frozen fitter ends at I0 = 0 in ≥ 1 of 6 seeds of the primary branch.
  - The calibration's seeds are new; the class is then re-drawn with six *further* new seeds for V2 and V4.
  - If no f collapses, V4 cannot bite. G4 is then **NOT VALIDATED**, and the owner decides.
- **(V1) No regression**, as AL3 V1. Selftest plus the two G2 §3 power suites. Primary valid count ≥ G2's, and Tadaki P-B RMS ≤ G2 + 0.02.
- **(V2) Recovery and refusal.**
  - Classes (a), (c) and (e): ≥ 4 of 6 valid, and median |V_c,P-B / truth(R_score) − 1| ≤ 0.10. truth(R) is G2's generating curve.
    For (a) and (c), |V/430 − 1| is also printed.
  - Classes (b) and (d), the clumps: no valid fit with |V_c,P-B / truth − 1| > 0.15. Refusal passes; a confident wrong speed fails.
- **(V3) No false fits**, as AL3 V3 (noise-only and line-outside cubes, 0 of 6 scored each).
- **(V4) MUTATE, two parts.** On the V2 class (e) cubes:
  - (i) the frozen fitter collapses (I0 = 0) in ≥ 1 seed;
  - (ii) G4 with rule 1 switched off (linear I0, bound 0, everything else G4) collapses in ≥ 1 seed.
  - If (ii) fails, the log amplitude is not what repairs it. That is reported, and G4 is NOT VALIDATED.
- **Verdict.**
  - G4 VALIDATED iff C, V1, V2, V3 and V4 all pass.
  - If V1, V2 or V3 fails: G4 FAILS VALIDATION. It is not run on the real cube, and the rules are not retuned.

## How each requirement is implemented, fixed here before any code

### G4 in-process
- `al4_g4.py` replaces `cfg942_common.fit_disc` in-process, for main fits only. The C1 injection, which passes `I0`, keeps the frozen
  fitter, as G4 rule 7 requires.
- It wraps `ac1_score.g1_3d` to record the G1-3D centroid, with the same lines as AL3's `al3_g3.py`.
- No frozen or AL3 file is edited.
- **Rule 1.** Index 7 becomes u = ln I0, with bounds [ln(1e-4 I0\*), ln(1e3 I0\*)] and start ln I0\*.
  - The frozen `lm_fit` is called unchanged.
  - Parameters are converted back to I0, and I0's covariance row and column are multiplied by I0, as AL3 did.
- **Rule 2.** vsys start = the G1-3D flux-weighted centroid. If none is finite, it is the frozen vs0, logged.
- **Rule 3.** For each of the three frozen vf starts, the start is the frozen start
  [centre, pa0, vsys, vf0, R_t 1.0, σ0 40, I0, h0], clipped exactly as `fit_disc` clips, with two changes:
  - vsys comes from rule 2;
  - I0\* = ⟨M₁, D⟩ / ⟨M₁, M₁⟩ in the fit's residual units, evaluated at that start and floored at 1e-6 of the frozen I0 start.

  There is no grid.
- **Rule 5.** Δχ² = Σ(D/σ)² − χ²_best in the fit's own units.
  - If Δχ² < 25 × (1 + 2 max(ρ₁, 0)), the covariance is set to NaN, so the frozen validity test fails it.
  - That fit is logged "model no better than empty".
- **Rule 6.** ρ₁ is measured on the fit's box:
  - all box channels (|v| ≤ 650), and all pixels at r > 2" (none skipped);
  - each pixel's spectrum mean-subtracted, pooled as Σ x_k x_{k+1} / Σ x_k².

  The covariance is multiplied by (1 + 2 max(ρ₁, 0)).
- **Rules 4 and 7:** frozen code.
- **G4-linear (V4 ii only).** Identical to G4 except rule 1: I0 is fitted linearly with bounds [0, ∞) and start I0\*.

### "Collapse (I0 = 0)", one definition for C, V4(i) and V4(ii)
- The reported best fit of the primary branch (incl-Tadaki) ends with I0 ≤ 1e-12.
- 1e-12 is the frozen fitter's own I0 floor; the frozen bound is 0.
- If the cube is not detected (no fits), that seed does not collapse.

### Class (e)
- `rel_spec` exactly as AL3's, with voff −172 and ρ 0.24 (class a + c).
- The disc scale length sp["h"] (= R_e / 1.678 / KPA) is multiplied by f. The flux S dV is unchanged.
- truth(R) is AL3's `truth()`, i.e. G2's generating curve, unchanged by f. The scorer's pressure term uses its frozen R_e.

### Seeds
- Classes (a)–(d), V3 and V1: AL3's seeds and settings.
  - (a)–(d): 83000 + 97 i + 1000 k, k = 0…3.
  - V3: 89000 + 97 i + {0, 1000}.
  - V1: 70000 + 97 i + Σ ord(kind).
- Calibration C (new): 85000 + 97 i + 100 f, i = 0…5, f = 2, 3, 4.
- V2 / V4 class (e) (further new): 87000 + 97 i, i = 0…5, at the f chosen by C.

### Order
1. C runs first, frozen fitter only: f = 2, then f = 3 only if f = 2 shows no collapse, then f = 4.
2. No G4 fit is run on any class-(e) cube before C's f is chosen.
3. The V2 / V4 class-(e) jobs are created only after C finishes.

### Reuse
- For (a)–(d) and V3, cubes are regenerated with AL3's seeds.
- **K1:** each regenerated cube's sha256 must equal the cube_sha256 in AL3's job record.
- No frozen-fitter run is needed on (a)–(d): G4 does not ask for V4 there.

## Checks (`al4_run.py`; per-job JSON; resumable; summary in `al4_validate.out` / `al4_validate.json`)
- **T0.** sha256 identical at start and end of every job and at summary time for:
  - `ac1_score.py`, `ac1_fit_checks.py`, `ac1_predict.py`, `ac1_score_power_results.json`, `FROZEN_CRITERIA.md`;
  - `ADDENDUM_G3_2026-11-06.md`, `ADDENDUM_G4_2026-11-06.md`, `ADDENDUM_G4_FILING_2026-11-06.md`;
  - `cfg942_common.py`;
  - AL3's `al3_g3.py`, `al3_mock.py`, `al3_run.py`.
- **K0.** AL3's writer with options off gives the frozen writer's sha256 (as AL3).
- **K1.** Cubes for (a)–(d) and V3 match AL3's recorded sha256.
- **T1 (G4 is live).** Every G4 run (log amplitude) on a detected cube logs 6 G4 main fits, and every final I0 is > 0.
- **C, V1, V2, V3, V4:** as in the verbatim block, with these implementation details:
  - **V1:** baseline = `reviews/alma_readiness_2026_11_04/revision_v1_4/validation_summary.json` (G2 rerun). Pass rule as AL3 V1.
    The selftest must have all checks PASS.
  - **V2 (a), (c), (e):** "valid" means the primary (incl-Tadaki) branch is valid. The median runs over valid primary fits.
  - **V2 (b), (d):** applied to every valid inclination branch (incl-Tadaki and incl-mom0) at P-B. This is the stricter reading of
    "no valid fit".
- **Verdict.**
  - If T0, K0, K1 or T1 fails: MACHINERY FAIL, and no G4 verdict.
  - Else, if V1, V2 or V3 fails: **G4 FAILS VALIDATION**.
  - Else, if C or V4 (i or ii) fails: **G4 NOT VALIDATED**, with the reason; the owner decides.
  - Else: **G4 VALIDATED**.
- Whatever the verdict, G4 touches the real cube only after a new spw25 stream (34,749,031,680 B), which needs a separate yes from
  the owner. This lane downloads nothing.

## Resources
- At most 6 jobs in parallel, nice 10, one thread each.
- Mock cubes go to the session scratch and are deleted after use.
