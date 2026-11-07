# OQ2 RESULT: the one-scalar door with a powered bin rule

Criteria 97fdee2c2e (local d0904b157c), frozen before any script or number. Stage 0 (the M1 null calibration) was committed as
1ab42dcc8d before any main-data run. Successor of OQ1 (criteria 3d8e38ffb2, result 048386c5fb). Kappa = 1/2 FITTED; not theory
closed. Adopts nothing. Both footings graded, never pooled. Every number below is read from `oq2_stage0.json`, `oq2.json`,
`oq2_MUTATE_M*.json` and `oq2_postfix.json`.

## Labels

| Row | canonical | alt | Label |
|---|---|---|---|
| **OQ2 one-scalar door (as frozen)** | no N_min passes | no N_min passes | **NO VERDICT** |
| S1 reading at the frozen fallback N_min = 8 (no label) | DEAD, every start, both f* | DEAD, every start, both f* | (DEAD, see below) |
| **Web row: does the CMB wall need the law's phantom off on the web?** | F_web,max = 0.00481 | F_web,max = 0.00435 | **YES** (F_web,max < 1 both) |
| **SEPARATED: web q below every host q?** | web log q max 0.450 vs lowest host 0.301 | 0.409 vs 0.301 | **NO** (as frozen; see note) |

Known answers all PASS:
- KA1 to 2.9e-7 / 4.5e-7;
- KA2 to 2.5e-7 / 3.2e-7;
- KA3: r(F = 1) 74.7424 / 89.3630, equal to SV5;
- KA4: Sigma_* and web fractions equal to SV5; point-mass phantom ratio 0.99999.

## 1. Stage 0: the M1 null does not certify any N_min

False-conflict runs out of 40 (20 noise seeds, 2 f*, F0 = 1). Seed 21 is OQ1's own twin, run at all 3 starts and both f*.

| N_min | canonical false | alt false | seed 21 no conflict (c / a) | seed 21 S3 holds |
|---|---|---|---|---|
| 1 | 32 | 36 | n / n | n |
| 2 | 12 | 13 | n / n | n |
| 3 | 5 | 4 | n / n | n |
| 4 | 5 | 4 | n / n | n |
| 5 | 4 | 4 | Y / Y | n |
| 6 | 4 | 2 | Y / Y | n |
| 7 | 4 | 0 | Y / Y | n |
| 8 | 2 | 0 | Y / Y | n |

Reading:
- The S1 part of the null is met only at N_min = 8 on canonical (2/40) and from N_min 6 on alt.
  - At N = 8 the canonical false conflicts are seed 1001 only: SPARC vs bright M31 (n 8), gap 0.019 dex.
- S3 fails for seed 21 at every N_min, on both footings. Two classes fail:
  - **SPARC.** S3 builds nodes from every bin where any other class has a band. That includes bins where one class with a wide
    band votes alone. For example, the bright M31 2-sigma band, scaled by sqrt(n_cls/n), gives midpoints near F ~ 55 at
    log q 4.8-5.6, where SPARC's band is about 4-6. So the interpolated F misses SPARC's narrow band (|Z| <= 0.057).
  - **groups.** OQ1's `band_groups` never merges adjacent passing candidates, so every groups band is a set of isolated points.
    An S3 prediction can never land inside one. This is a bug in code written for OQ1.
- **Frozen rule outcome: N_min* = None. Label NO VERDICT.** The frozen method still has no demonstrated power to recognise a true
  one-quantity law. With the occupancy rule the S1 half of the power can be had; the S3 half cannot.

## 2. Main data at N_min = 8 (frozen fallback; reported without a label)

Power at N_min 8 (oq2_MUTATE_*.json):
- M1 seed 21: S1 no conflict in 12/12 runs. S3 fails, as in stage 0.
- M2 planted step: DEAD in every footing and f*. Gaps 0.152-0.197 dex, all SPARC vs groups. One run, alt f*0 F0=0, holds.
- M3 Newton: SPARC Z +0.4308, so G1 fails (the twin bites).

Main-data conflicts (`oq2.json`). Every conflict above 0 dex is SPARC vs groups at log q 3.0-3.4:

| footing | f* | F0 | bin log q | gap (dex) | n SPARC / groups |
|---|---|---|---|---|---|
| canonical | 0 | 1 | 3.2-3.4 | 0.489 | 19 / 15 |
| canonical | 0 | 10 | 3.2-3.4 | 0.497 | 9 / 15 |
| canonical | 1 | 1 | 3.2-3.4 | 0.277 | 19 / 15 |
| canonical | 1 | 10 | 3.2-3.4 | 0.289 | 9 / 16 |
| alt | 0 | 1 | 3.0-3.2 / 3.2-3.4 | 0.483 / 0.372 | 9 / 9; 40 / 9 |
| alt | 0 | 10 | 3.2-3.4 | 0.390 | 26 / 13 |
| alt | 1 | 1 | 3.0-3.2 / 3.2-3.4 | 0.267 / 0.107 | 9 / 10; 40 / 8 |
| alt | 1 | 10 | 3.0-3.2 / 3.2-3.4 | 0.267 / 0.124 | 9 / 8; 26 / 10 |

- The F0 = 0 runs conflict only at log q 0.2-0.4: groups (all 40 at q = 2, F = 0, empty band) vs the web (F <= F_web,max), gap
  0 dex. This is the switched-off fixed point. Every host that starts at F = 0 stays at web-level q.
- Margin against the null: the smallest main gap above 0 is 0.107 dex. The largest M1 false gap at N = 8 is 0.019 dex. The M2
  planted step reads 0.15-0.20 dex. The canonical f*0 SPARC-groups gap (0.49 dex) is larger than the planted 0.3 dex step.
- **What N_min 8 drops.** X-COP never reaches 8 points in a bin (at most 7), so all 35 X-COP points never vote. The
  SPARC vs X-COP conflict, OQ1's widest (0.35-0.53 dex), is therefore not tested here. Also never voting: ellipticals 12-21 of
  21, bright M31 15-25 of 25, Coma UDGs 9 of 9, LG field 13 of 13. Exact counts per run are in `never_vote_points`.

## 3. Web rows

- **Phantom off on the web needed: YES**, both footings.
  - The full law (F = 1) puts the lensing amplitude at r 74.74 / 89.36 against the line 1.0722.
  - The largest uniform F that stays under the line is 0.00481 / 0.00435.
  - So the law's phantom must be switched off on the linear web to at least 99.5 %.
- **SEPARATED: NO as frozen.**
  - At F_web,max the web's largest q is 2.82 / 2.56 (log 0.450 / 0.409).
  - In the F0 = 1 main run, 1 (canonical) / 2 (alt) SPARC points are projected to F = 0 and sit at q = 2 (log 0.301), below
    the web maximum.
  - Without those floor points the lowest host is log q 2.47 / 2.31 (OQ1's post-freeze reading, same machinery), two dex above
    the web.
  - So the scalar can tell the web from hosts that carry their phantom. The self-consistent iteration also admits hosts in the
    off state at web-level q.

## 4. Post-freeze sensitivity (disclosed; no label): `oq2_postfix.py`

One bug fix only: `band_groups` now merges consecutive passing candidates into intervals. The web is excluded here (its bins
sit at log q < 0.7). Everything else is unchanged.
- Seed 21 S3 at N_min 5-6 then fails only for SPARC (groups passes at N 5 on both footings and at N 6 on canonical). The frozen
  rule still finds no N_min*: **NO VERDICT stands with the bug fixed.**
- S1-only calibration with the fix gives N_min 8. At N = 8, main data reads DEAD on every non-F0=0 run:
  - SPARC vs groups, gaps 0.107-0.483 dex, plus one canonical f*0 run at 0 dex;
  - canonical f*0 F0 = 1 and 10 change to 0.000 dex conflicts, a different fixed point after the fix.
- M2 still bites (0.133-0.197 dex). The F0 = 0 runs hold (the web is excluded).

## 5. What this does and does not settle

- The occupancy rule removes the single-point false conflicts that sank OQ1's M1. The S1 part of the null is met at N_min 8.
- At N_min 8 the main data still conflict: SPARC vs groups at the same q, up to 0.49 dex, on both footings. Against M1's
  0.019 dex false gap and M2's 0.15-0.20 dex planted step, that reads as a real conflict.
- It is not graded as DEAD, because the frozen power check also requires S3. OQ1's S3 construction cannot certify even a
  planted law: midpoints of single-class wide bands make bad nodes. A label needs S3's node rule changed, which is a new freeze.
  - Suggested freeze: nodes only from bins with at least two voting classes, plus the `band_groups` fix.
- Web row YES does not show that an action supplies the switch. It says what the web needs.

## Post-freeze disclosures

- `oq2_postfix.py` / `oq2_postfix.json` / `oq2_postfix.out` were written after stage 0 and the main run. They carry no label.
- One addition to the S3 code, within the one change: a class with no bin at or above N_min reads "NO POWERED BIN" and does not
  fail S3. This was written before stage 0 ran and is in the stage-0 commit.
- This session ran OQ1 and had seen OQ1's main bins before the freeze (disclosed in the criteria). N_min came from the M1 null
  by the frozen rule, not by hand.

Kappa = 1/2 FITTED; not theory closed.
