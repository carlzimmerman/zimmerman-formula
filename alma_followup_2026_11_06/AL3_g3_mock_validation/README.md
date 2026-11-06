# AL3: MOCK validation of filed addendum G3. VERDICT: G3 FAILS VALIDATION (V1, V2 fail; V4 fails; V3 passes)

Criteria `FROZEN_CRITERIA.md` (6dce9813a6), committed alone before any code. G3 filed 315d8e4eaa. MOCK cubes only, NOT ALMA DATA. Scores
nothing. No frozen file changed (T0 PASS in all 74 jobs). κ = ½ FITTED; one disc excludes no model; not theory closed.

**Per the filed rule, G3 does not run on the real cube, and the rules are not retuned to pass.** Row B1–B4 of the 2026-11-06 release
stay "FIT NOT CONSTRAINED: not scored".

## Result (`al3_validate.out/.json`; per-job records `jobs/`; G3 selftest outputs `v1_selftest/`)
- **Machinery checks pass:**
  - K0: with its options off, AL3's mock writer gives the frozen writer's cube byte for byte (sha256 57413f24…).
  - T1: 246 G3 fits ran in 72 G3 runs, all with final I0 > 0, so the absorbing state is gone.
- **V1 (no regression): FAIL.**
  - Selftest: 10 of 10 checks PASS.
  - Archive compact: G3 valid 2 of 6, against G2's 3 of 6.
  - Sister-like smooth: G3 valid 4 of 6, against G2's 6 of 6.
  - Every other suite × class matches G2; Tadaki P-B RMS is within G2 + 0.02 wherever there is a fit.
  - The cause is rule 3's PA grid.
    - When the start vf0 is small, the coarse grid can pick PA ±45°/90° off. That start then converges to a different local minimum:
      for example vf 10 km/s at PA −1.7 rad, with χ² +4,500 above the other two starts.
    - The frozen three-start gate (15 %) then fails a fit that G2's single PA start got right.
- **V2 (hard classes): FAIL, two of four classes.**

  | class | G3 valid | V_c P-B | median error | verdict |
  |---|---|---|---|---|
  | (a) offset −172 km/s | 6/6 | 420–438 | 1.5 % | PASS |
  | (c) ρ 0.24 | 6/6 | 417–437 | 1.2 % | PASS |
  | (b) 40 % clump | 0/6 | — | — | FAIL |
  | (d) a + b + c | 0/6 | — | — | FAIL |

  - In (b) and (d), the frozen and G3 fitters reach the same solution: V_f at its 800 bound, V_c about 530, h ≈ 0.028". The thin disc
    shrinks to fit the clump.
  - That is model inadequacy (G2 §2 names non-disc structure), not the I0 failure G3 repairs.
- **V3 (no false fits): PASS.** Noise-only and line-at-+1200 cubes give 0 of 6 scored each, and none is detected.
- **V4 (MUTATE): FAIL.**
  - The frozen fitter does not collapse (I0 = 0) in any of the 24 hard-class cubes. In (a) and (c) it already recovers 430 in 6 of 6.
  - So, as in AL1, no mock in this lane reproduces the real-cube collapse, and V2 did not exercise the repair.
  - Mock Δχ² vs empty is 3.8–10.7 × 10⁴ at G1-3D S/N about 28. On the real cube, the frozen start was *worse* than empty
    (AL2 R2). These mocks are far more line-dominated per voxel than the real data, at a similar aggregate S/N.

## Disclosed findings about the filed rules (no rule changed)
- **Rule 6's ρ₁ estimator is biased.** It is AL2 R4's: continuum channels |v| > 600 inside a box kept to |v| ≤ 650.
  - It reads −0.05 to −0.08 on independent-channel mocks at release settings, and −0.17 to −0.21 on the dv 20 G2 mocks, where only a few
    continuum channels survive.
  - It reads 0.13–0.16 on cubes made with ρ 0.24.
  - So (1 + 2ρ₁) shrinks errors on independent noise. The release's +0.24 is probably an underestimate too.
- **Rule 5's threshold direction** (flagged in the criteria): 25/(1 + 2ρ₁) divides where a whitened Δχ² would multiply. It made no
  difference here: 0 of 246 fits fall between the two thresholds.
- **The test job V2_d_0 was run once alone** before the driver, to time it (1,211 s, 3.5 GB). The driver kept that record; it is the
  same code.
- **Resources:** peak 3.6 GB per job, 8 jobs in parallel, 8.8 job-hours in total. No 1024³ run was live. The mock cubes were written to
  the session scratch and deleted after use.

## What this means
- G3's log-amplitude rule works: no fit reached I0 = 0. Its centroid start recovers an offset line, but so did the frozen fitter on
  these mocks.
- G3's PA grid costs validity on smooth discs.
- The filed rules cannot be retuned under G3's own terms. Any further repair is a new addendum, and the owner decides whether to write
  one. Possible next steps, none adopted:
  - drop the PA grid and keep rules 1, 2 and 5;
  - fix the ρ₁ estimator (all channels off source);
  - add a hard class built to reproduce the real collapse, with low per-voxel S/N and a start worse than empty, so that V4 can bite.
- Rows B1–B4 stay unscored. The release record and PAPER66 are unchanged.
