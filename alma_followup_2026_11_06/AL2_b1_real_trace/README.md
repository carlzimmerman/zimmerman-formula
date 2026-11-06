# AL2: row-B I0 collapse traced on the real spw25 cutout. REPRODUCED; COLLAPSE AT THE FIRST STEP IN ALL SIX FITS; TRIGGER UNRESOLVED under the frozen rule

Criteria `FROZEN_CRITERIA.md` and owner approval (c3ea324663), committed before the stream. Diagnosis only: no V_c from any modified start
was computed, nothing scored, no frozen file changed (T0 PASS). κ = ½ FITTED; one disc excludes no model; not theory closed.

## Re-stream
spw25 cube re-streamed once under the owner's 2026-11-06 approval: source 34,749,031,680 B, source sha256 25d79350…2913, same box
[1950, 2552, 1949, 2551]. Cutout sha256 61f147499c28123e… = the release cutout (R0). Cutout deleted after the runs.

## Result (`al2_trace.out/.json`; MUTATE `al2_trace_MUTATE.out/.json`)
- **R1 reproduced exactly:** both fits I0 = 0, params equal to `ac1_score_RELEASE.json` (max relative difference 0), trial chi2 2,626,595.68.
- **R2 trace (replay through a copy of lm_fit equals the frozen output in all six):** in every one of the six trial fits:
  - the start model is worse than an empty model, by +8,758 to +31,022 in chi2;
  - the first LM step (lam 1e-3) drives I0 negative (unclipped −0.003 to −0.024), the bound clips it to 0, and the step is accepted
    because the zero model's cost is lower;
  - then nothing moves (AL1's absorbing state), and the fit stops after 2 steps (status 2).
  The other parameters in the record are the first step's values, so V_c 169/146 (P-B) were never fitted to the data.
- **R3 start decomposition (cost minus zero-model cost):**

  | call | start | I0 → flux-implied | vsys → 3D centroid (−172) | both |
  |---|---|---|---|---|
  | i 36.6, vf0 146 / 300 / 500 | +31,022 / +28,681 / +22,901 | +57,966 / +53,069 / +42,878 | +29,314 / +21,018 / +9,236 | +55,736 / +43,067 / +25,038 |
  | i 58.5, vf0 102 / 300 / 500 | +15,998 / +13,515 / +8,758 | +83,570 / +68,064 / +48,905 | +15,837 / +5,537 / **−2,118** | +83,248 / +52,068 / +27,098 |

  - The frozen I0 start is 0.77x (i 36.6) and 0.50x (i 58.5) the flux-implied value. A brighter start is *worse*, so the start disc is
    putting flux where the data has none.
  - The vsys offset (start −29 vs centroid −172) is a real contributor: correcting it lowers the cost in all six. But it brings the start
    below the empty model only in one call (i 58.5, vf0 500).
  - So no single start component explains the collapse. Under the frozen rule: **TRIGGER UNRESOLVED.**
- **R4 data facts:**
  - continuum residual in r ≤ 1" is −0.002 σ (not the cause);
  - lag-1 channel autocorrelation off source is +0.24 (correlated noise; the fit assumes independent voxels);
  - no fit voxel exceeds 4 σ (peak 4.9 σ).
  The line is detected only in aggregate (G1-3D S/N 24), and per voxel the data is noise-dominated.
- **MUTATE (data × 2):** zero-model cost ratio 4.000000000, and the trace changes (start − zero +124,087 vs +31,022). It bites.

## What this means
- The failure is the fitter, not a fact about the galaxy:
  - with per-voxel S/N below 5, a start disc misplaced in velocity and shape costs more than no disc;
  - the projected LM step then lands exactly on the I0 = 0 bound, which is absorbing.
- AL1's smooth MOCKs never had a start worse than the empty model. That is why they could not reproduce it.
- B1–B4 stay not scored. A repair (for example: refuse a step that zeroes the model, fit log I0, start vsys from the 3D centroid,
  or start from a grid over vsys and PA) must be filed by the owner as a scorer addendum before it runs on this cube.
- Any rescore then needs this cube again: a new stream, which needs the owner's yes.

## Disclosed
- The first MUTATE run crashed after its results were computed, on a JSON key path in AL2's own bookkeeping (`["R2"]` →
  `["results"]["R2"]`). That was fixed and the MUTATE rerun. The main run's numbers come from the same code apart from that line,
  which only the MUTATE branch reads.
- Peak RSS 3.5 GB, 91 s per run. No 1024³ run was live.
