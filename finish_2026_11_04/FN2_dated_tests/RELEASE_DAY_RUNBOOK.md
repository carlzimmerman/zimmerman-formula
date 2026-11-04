# Release-day runbook: ALMA 2026-11-06 (and GS4_24110 2026-11-28)

Lane FN2_dated_tests (criteria 755f05c3cf). κ = ½ FITTED. Footings never pooled. One disc excludes no model. Not theory closed.

**Nothing below is downloaded until the owner says yes, naming the file, the source and the size.** The sizes are the archive's own listing, read 2026-11-04 before release (`fn2_archive_meta.json`). Every command runs from the repo root.

## 0. What is scored, and by what

| row (PAPER66 v1.4, Table t:card) | galaxy, line | cube | scorer | governing rules |
|---|---|---|---|---|
| A | U4_27928, CO(2-1) at 95.2899 GHz, 7.36″ off-axis | spw23 | `campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_u4.py` | CFG806 plan (1bf70683b), its clarification and addenda A, E, F |
| B0–B5 | U4_28473, CO(3-2) at 98.1108 GHz, phase centre | spw25 | `rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_score.py` | AC1 criteria (57d3ac6b64), ADDENDUM_G1, ADDENDUM_G2 |

The field for each row is in `fn2_scorecard.out` (map, then 7 of 7 known answers against the tex).

## 1. The files (archive listing, 2026-11-04)

Release: **2026-11-06 02:42:31 UTC** (21:42:31 on 5 November, US Eastern). MOUS uid://A001/X3788/Xbfd2, programme 2024.1.00100.L, target name UDS28473. Data rights today: Proprietary; a HEAD request returns 403.

| use | file | bytes | window | channel |
|---|---|---|---|---|
| rows B | `member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw25.cube.I.pbcor.fits` | 34,749,031,680 | 97.5953–98.6216 GHz | 2257.81 kHz (6.9 km/s) |
| row A | `member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw23.cube.I.pbcor.fits` | 38,556,031,680 | 94.7944–96.6657 GHz | 3904.30 kHz (12.3 km/s) |

Source for both: `https://almascience.eso.org/dataPortal/<file>` (mirrors almascience.nrao.edu, almascience.nao.ac.jp).

Shapes inferred from the listed sizes (4500 × 4500 × 429 for spw25, 4500 × 4500 × 476 for spw23); the stream's header gives the truth. The `.pb.fits.gz` files (10.2 and 10.9 GB) are not needed. The whole product tar is 193.5 GB and is not needed.

**Expected sizes on disk.** The stream keeps only the cutout.

| cutout | half-size | at 0.013″ pixels | at 0.0225″ pixels |
|---|---|---|---|
| U4_28473, spw25 | 4.5″ | 0.83 GB | 0.28 GB |
| U4_27928, spw23 | 13″ | 7.62 GB | 2.55 GB |

The pixel scale is unknown until the header is read. Every derived number here is in `fn2_runbook_numbers.out`. AC1's earlier estimate of 115 GB per spw is superseded by the listed 34.7 and 38.6 GB.

**Transfer time.** CFG569 measured 12–17 MB/s from the archive's NRAO mirror (2026-10-09). That gives 34–48 min for spw25 and 38–54 min for spw23. Any of the three hosts may serve the stream.

**Coverage facts (information, `fn2_archive_meta.out`).**
- spw25 covers −1556 to +1560 km/s about CO(3-2). AC1's window (±500) and its MUTATE (+1000 ± 500) are fully inside.
- spw23 covers −4342 to +1573 km/s about CO(2-1). The CFG806 window (±500) is inside. **The CFG806 MUTATE window (+2000 ± 500) is 7 % inside**, so on this spw the U4 MUTATE "bites" for lack of data. It is non-diagnostic; there is no frozen fallback.

## 2. Before the release
1. Environment. The pinned v1.4 environment reproduces the committed v1.4 selftest byte for byte (`fn2_a1_env_pinned.out`: ENV IDENTICAL, 223 s, 0.70 GB). The default `python3` passes 10 of 10 with numbers within 1e-5 (`fn2_a1_env_default.out`: ENV OK, NUMBERS DRIFT, 297 s, 1.05 GB). Use the pinned one if `/tmp/alma_v14_pydeps` still exists (a reboot can clear /tmp):
   ```
   PY_AC1="env PYTHONPATH=/tmp/alma_v14_pydeps /usr/bin/python3"   # else: PY_AC1=python3
   ```
2. The cutout tool and `cfg942_u4.py` use the default `python3` (the tool runs with `-I`, which ignores PYTHONPATH).
3. Scratch outside the repo: `SCR=<a scratch directory outside the repo>`; `mkdir -p "$SCR"`.
4. Nothing else is needed before release. Both scorers check their own frozen files at start (AC1: FROZEN_CRITERIA.md against 57d3ac6b64; CFG942: K1, 27 rows). Do not run `cfg942_u4.py --selftest` on the day: it rewrites CFG942's committed selftest files.

## 3. On the day, after 02:42:31 UTC

**Step 1. Is it public, and is the size as listed?** HEAD requests only.
```
for s in 25 23; do curl -sSI "https://almascience.eso.org/dataPortal/member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw$s.cube.I.pbcor.fits" | grep -i -E "^HTTP|content-length"; done
```
Expect HTTP 200 and Content-Length 34749031680 (spw25) and 38556031680 (spw23). A 403 means not yet public: wait. A different length goes to the owner as the new size. If the server refuses HEAD, the listed size stands.

**Step 2. Disk and machine.**
```
df -h /System/Volumes/Data      # need >= 10 GB free for both cutouts plus margin; streaming never stores the full cube
ps aux | grep -v grep | grep -E "1024|python" | awk '{print $2, $3, $6/1e6 " GB", $11, $12}'
```
The AC1 scorer peaked at 2.3 GB on a MOCK at 0.013″ pixels (AC1 README). That is above the 1 GB small-job line, so run it alone, with no 1024³ run live.

**Step 3. The owner's yes.** Stop here until the owner answers. The request names each file, its source and its size, for example:
> Download (stream) `member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw25.cube.I.pbcor.fits` from almascience.eso.org/dataPortal, 34,749,031,680 bytes, keeping only a ±4.5″ cutout (0.28–0.83 GB); and `…spw23.cube.I.pbcor.fits`, 38,556,031,680 bytes, keeping a ±13″ cutout (2.55–7.62 GB). Yes?

**Step 4. Stream the U4_28473 cutout (rows B).** No `--retry`: a retried stream would feed repeated bytes into the pipe.
```
set -o pipefail
curl -sSL --fail "https://almascience.eso.org/dataPortal/member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw25.cube.I.pbcor.fits" \
  | python3 -I rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_stream_cutout.py - "$SCR/U4_28473_spw25_cut.fits" 34.422382000017684 -5.181044500002704 4.5
```
Checks on the printed provenance (`$SCR/U4_28473_spw25_cut.fits.provenance.json`): `source_bytes` = 34749031680; `box` is not clipped (x1 − x0 = y1 − y0). A truncated stream is refused and leaves no output; then rerun the step.

**Step 5. Score U4_28473.**
```
OUT=finish_2026_11_04/FN2_dated_tests/release_2026_11_06
OMP_NUM_THREADS=1 nice -n 10 $PY_AC1 -B rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_score.py --cube "$SCR/U4_28473_spw25_cut.fits" --output-dir $OUT/ac1
OMP_NUM_THREADS=1 nice -n 10 $PY_AC1 -B rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_score.py --cube "$SCR/U4_28473_spw25_cut.fits" --mutate --output-dir $OUT/ac1
```
- Writes `ac1_score_RELEASE.out/.json` and `ac1_score_RELEASE_MUTATE.out/.json` in `$OUT/ac1`.
- The true run exits 0. MUTATE exits 1 when it bites. If the true run did not detect the line, the MUTATE exit 1 is trivial and is reported as non-diagnostic.
- G1-3D decides (ADDENDUM_G1); the frozen moment-0 G1 prints beside it. Fits must pass the all-three-starts gate (ADDENDUM_G2).
- Without `--output-dir` the scorer writes to AC1's `validation_2026_11_04/` (its own default). This runbook keeps the release outputs in this lane.

**Step 6. Stream the U4_27928 cutout (row A).** 13″ holds the harness's 8″ box plus the C1 shift east.
```
curl -sSL --fail "https://almascience.eso.org/dataPortal/member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw23.cube.I.pbcor.fits" \
  | python3 -I rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_stream_cutout.py - "$SCR/U4_27928_spw23_cut.fits" 34.42319107055664 -5.182923793792725 13
```
Checks: `source_bytes` = 38556031680; the box is not clipped. A clipped box means the imaged field does not cover this offset (CFG806 note, 2026-11-01): report it and stop row A.

**Step 7. Score U4_27928 (CFG806 plan, verdict kernel ν_mono, then the labelled parallel readings).**
```
H=campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_u4.py
OMP_NUM_THREADS=1 nice -n 10 python3 -B $H --cube "$SCR/U4_27928_spw23_cut.fits"
OMP_NUM_THREADS=1 nice -n 10 python3 -B $H --cube "$SCR/U4_27928_spw23_cut.fits" --mutate
for k in n1 n2 v3aq; do CFG942_KERNEL=$k OMP_NUM_THREADS=1 nice -n 10 python3 -B $H --cube "$SCR/U4_27928_spw23_cut.fits"; done
```
- The harness writes `cfg942_u4_RELEASE[_KERNEL_k][_MUTATE].out/_results.json` in CFG942's folder and byte-identical copies `cfg806_u4[…]` in `CFG806_u4_27928_scoring/` (owner's CLARIFICATION A-X7). These are new files by design; no frozen file is edited.
- G1's selection-aware S/N decides (CFG806 addendum A). The literal S/N is information and is never quoted as the result.
- Expected: G1 FAIL, upper limit (PAPER66 Prediction A).

**Step 8. Read the scorecard rows.**
```
python3 -B finish_2026_11_04/FN2_dated_tests/fn2_scorecard.py --read $OUT/ac1/ac1_score_RELEASE.json \
  --u4 campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_u4_RELEASE_results.json --tag release_2026_11_06
```
It prints each row's fields. It evaluates a counter-outcome only where the tex states one: A (G1 passes), B3 (any pair among flat, F-DESI and the band separated), B4 (flat and R-H separated). B1 and B2 have no numeric line in the tex; the reader prints z values and α_CO,req with no call. B2 applies only if the scored radius is 3 kpc. Reading note: the scorer's class FLOOR means stars exceed the requirement even at M★ − 0.2 dex, so a nominal "FLOOR" can print beside class CONSISTENT (seen on the MOCK dry run at V_c 421, lg M★ 11.31, S2). That is the frozen rule, not a fault.

**Step 9. Record the result without editing frozen files.**
1. Copy the two `*.provenance.json` files into `$OUT/`.
2. Write `finish_2026_11_04/FN2_dated_tests/RESULT_2026-11-06.md`: one line per row A, B0–B5 in words, from the reader's fields; the measured noise and beam beside the sister forecast (0.171 mJy/beam per 10 km/s; 0.109″ × 0.085″); every failed control; the MUTATE status of both rows.
3. Never edit: AC1's FROZEN_CRITERIA, ADDENDUM_G1, ADDENDUM_G2; the CFG806 plan and its clarifications; any seal; PAPER66 v1.4 (deposited). A filled scorecard goes into a PAPER66 v1.5 only on the owner's go; depositing is the owner's act. The ledger row is the lead session's.
4. Check outputs for home paths: `grep -rl "$HOME" $OUT campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_u4_RELEASE* campaign_fresh_gravity/CFG806_u4_27928_scoring/cfg806_u4*` must print nothing.
5. Commit with explicit paths only: `git add <paths>` then `git commit -m "…" -- <paths>`. Never commit a FITS file.
6. Delete the cutouts: `rm "$SCR"/U4_*_cut.fits`.

**Not used: the archive's SODA cutout.** The archive also lists a server-side SODA sub-image service for each cube (`#cutout` in the DataLink listing). It would transfer only the box. It has not been tested against these scorers, and it records no full-file SHA-256. Using it would be a departure needing its own known-answer test and the owner's yes.

## 4. GS4_24110, 2026-11-28 18:25:24 UTC (13:25:24 US Eastern)

MOUS uid://A001/X3845/X3a, programme 2025.1.01377.L, target name Pointing-F (0.42″ from GS4_24110), single pointing.

| use | file | bytes |
|---|---|---|
| [CI](2-1) cube, spw31, 269.5896–271.4609 GHz | `member.uid___A001_X3845_X3a.Pointing-F_sci.spw31.cube.I.pbcor.fits` | 7,018,934,400 |
| continuum | `member.uid___A001_X3845_X3a.Pointing-F_sci.spw25_27_29_31.cont.I.pbcor.fits` | 14,777,280 |

- Both fit on disk (7–10 min at 12–17 MB/s); a plain download is enough (`curl -sSL --fail -o "$SCR/<file>" <url>`), after the owner's yes with names and sizes.
- spw31 covers −1615 to +462 km/s about [CI](2-1) at 270.006 GHz. The frozen ±300 window is inside. The continuum (|v| > 600) exists only on the blue side.
- **The frozen MUTATE cannot run.** +2000 and the A-G11 fallback +1000 both lie wholly outside spw31. The harness will exit 2 and print that the run has no MUTATE control (CFG809 addendum A §2). A substitute control would need a dated pre-data owner addendum before 18:25:24 UTC on 2026-11-28.
- Commands:
  ```
  G=campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_gs4.py
  OMP_NUM_THREADS=1 nice -n 10 python3 -B $G --cube "$SCR/<spw31 cube>" --cont "$SCR/<cont file>"
  OMP_NUM_THREADS=1 nice -n 10 python3 -B $G --cube "$SCR/<spw31 cube>" --cont "$SCR/<cont file>" --mutate    # expect exit 2
  for k in n1 n2 v3aq; do CFG942_KERNEL=$k python3 -B $G --cube "$SCR/<spw31 cube>" --cont "$SCR/<cont file>"; done
  ```
- Outputs go to CFG942's folder and, as copies, to `CFG809_gs4_24110_ci21_scoring/` (A-X7). Record and commit as in step 9.
