# ADVERSARIAL VERIFICATION VERDICT — g_ext vector reconstruction (Phase 3)

Date: 2026-07-16. Verifier: independent re-run, all numbers below recomputed from scratch
(fresh scripts, not the pipeline's own gate code). The physics repo was read-only; only this
file was written into the frozen-exempt gext_vectors_2026 tree.

## VERDICT: **UPHELD** (GATE-A + GATE-B pass independently), with one added caveat
(amplitude slope compression, Sec. 4) that affects amplitudes only, not directions.

## 1. What was re-run

- `src/gext_estimator.py` unit test: **PASSED, exit 0** (synthetic point-mass magnitude and
  direction at machine precision; supergalactic rotation orthonormal).
- GATE-A recomputed from `data/gext_vectors.csv` vs the repo's `chae21_env.csv` with an
  independently written script (own matching, own statistics):
  - **maxclu: Pearson r = 0.8887, Spearman r = 0.826, global offset (Chae−ours, median)
    = +0.0995 dex, scatter after the one offset = 0.1268 dex (std)** — pre-registered
    targets r >~ 0.8, scatter <~ 0.3 dex: PASS.
  - **noclu: Pearson r = 0.860, Spearman 0.766, offset +0.117 dex, scatter 0.146 dex** — PASS.
  - 109/109 Chae Table-3 galaxies matched by name; matches the gate report exactly.
- GATE-B recounted independently: Virgo n=106, median angle 11.6 deg (103/106 under 30 deg,
  105/106 under 90 deg, 103 Virgo-dominated); Coma n=3, median 40.2 deg. Matches the report.
- `validation/check_gates.py` re-run: exit 0, identical numbers.

## 2. Tuning hunt (per-galaxy calibration disguised as global) — CLEAN

- CSV amplitudes are RAW: the +0.10 dex offset is still present in the data (reported, not
  applied). One global constant only, as declared.
- Residual distribution is smooth: |resid| < 0.001 dex for 1/109 (chance level), < 0.01 for
  8/109; percentiles 10/25/50/75/90 = 0.016/0.034/0.072/0.118/0.187 dex. No spike at zero.
- Worst outliers are physically sensible, not clipped: UGC06614 (−0.54), UGC07261 (−0.43),
  NGC5033 (−0.38) — the largest ones sit closest to Virgo, exactly where the omitted
  NSA-resolution local detail matters most.
- Leverage: dropping the top-5/top-10/bottom-5 Chae values keeps r = 0.86–0.87; Spearman
  confirms the correlation is rank-carried, not a two-cluster artifact. Dynamic range is a
  genuine 1.68 dex (ours) / 0.98 dex (Chae).

## 3. Coordinate-frame audit (the silent-poison risk) — CLEAN

- Hand spherical-trig recomputation (no pipeline code) for 5 Virgo-proximate galaxies:
  3D angles between the delivered ICRS unit vector and the direction to Virgo (RA 187.70,
  Dec +12.34, D 16.5) = 18.6 (UGC07261), 17.6 (DDO170), 9.1 (NGC4559), 3.7 (UGC07125),
  35.0 (NGC5033, dominated by a nearer 2M++ galaxy — legitimately non-Virgo) deg.
  Note the 3D geometry: a SPARC galaxy BEHIND Virgo is pulled partly back toward Earth, so
  the vector's sky-projected (ra_dir, dec_dir) need not equal Virgo's RA/Dec — the check is
  the 3D angle, and it passes.
- Anti-check: had the supergalactic vector been mislabeled as ICRS, UGC07261's Virgo angle
  would read 51.1 deg instead of 18.6 — the frames are demonstrably not mixed.
- Independent astropy `SkyCoord ... .supergalactic` conversion of the delivered ICRS unit
  vectors matches the delivered SG columns to <= 0.023 deg (4 galaxies incl. both sky poles
  of the sample); Virgo core lands at SGL 102.9, SGB −2.4, the literature position.
- `ra_dir`/`dec_dir` columns match a by-hand atan2/asin conversion of (ux,uy,uz) to 0.01 deg.
- SPARC coordinates spot-checked vs NED J2000 (NGC2403, NGC3198, NGC2841, DDO154):
  offsets <= 3 arcsec.
- All 175 unit vectors normalized (worst deviation < 1e-4); no duplicate names.

## 4. Added caveat — amplitude SLOPE compression (new, not in gate_report.md)

The pre-registered gate allows one global offset and passes as stated. But a free-slope fit
reveals a second, scale-like systematic: **OLS slope of Chae-on-ours = 0.636** (residual-vs-
ours correlation −0.74; scatter drops from 0.127 to 0.085 dex around the free-slope line).
Our reconstruction spans 1.68 dex where Chae spans 0.98 dex: our lowest-e_N galaxies are too
low relative to Chae (his NSA faint structure + homogeneous-grid component put a FLOOR under
every galaxy's e_N that a 2M++/MCXC-only sum lacks; part of the 0.636 is also plain
regression dilution from the 0.127 dex noise). Consequences:
- A single global constant does NOT fully map our amplitudes onto Chae's; anyone using our
  log_eN as an amplitude should either use Chae's published Table-3 values where available
  (109 galaxies) or treat ours as compressed-scale estimates.
- DIRECTIONS are unaffected: the missing floor is quasi-isotropic (homogeneous grid: ~zero
  net vector; NSA faint structure: enters the soft-flag budget), and GATE-B is independent
  of amplitude calibration entirely.

## 5. Completeness correction NOT doing the work — CONFIRMED

The noclu bracket carries NO completeness up-weight and no x8, yet gates at r = 0.860 /
0.146 dex on its own. Bracket separation: ours 0.920 dex vs Chae 0.912 dex vs log10(8) =
0.903 — the LF up-weight adds only ~0.02 dex differential on top of the isotropic x8, and
residuals of the two brackets correlate at 0.982 (one underlying sum). Both brackets pass
independently; neither is carried by the correction.

## 6. Distance conventions — CLEAN

H0 = 73 km/s/Mpc throughout (Chae Sec. 3.1, "as assumed in SPARC"); SPARC test points use
the SPARC Dist column (what Chae's fits use). Residual-vs-log10(D) correlation = −0.16
(median residual +0.035 dex for D < 18 Mpc vs −0.032 above) — no material distance-frame
error; the mild trend is consistent with the omitted local (Karachentsev/NSA) structure.

## 7. Bottom line for the pre-registered aligned-asymmetry statistic

- **GATE-A: PASS (upheld independently, both brackets), with the Sec. 4 slope caveat on
  amplitudes.** Our residual scatter against Chae (0.127 dex) is well inside his own
  published per-galaxy 1-sigma (median 0.288 dex maxclu).
- **GATE-B: PASS (upheld independently; frames verified by hand and by astropy).**
- **Fit for use: the DIRECTION columns of all 175 rows, with the 94 robust-flag rows
  (dom_share >= 0.5) as the primary sample and robust/soft as a pre-declared stratification
  variable.** The soft rows (81) have direction set by many comparable contributors and no
  per-row direction uncertainty is quantified — use them only in the stratified analysis.
  For any amplitude weighting, prefer Chae's published Table-3 amplitudes (109 galaxies);
  our amplitudes are for the 66 SPARC galaxies he did not publish, with the compressed-scale
  caveat.
- Declared-weak checks stay weak: Coma is n=3 (in the Coma–A1367 wall) and the Great
  Attractor check is inconclusive by construction; neither is load-bearing.

**UPHELD.**
