# EUC14 (PREDICTED-SPLIT SOURCE REDSHIFTS): RESULT

2026-11-12. Criteria d537220287 (alone, before any prediction met a lens spectrum). The brief's EUC12 and EUC13 were taken.

## Verdict: NOT EVALUABLE / NOT EVALUABLE (canonical / alt). EUC1-F is not graded.

**The `anyk` mutation twin decides the word.** It did not exit 1: with the k window removed, grade-X SECURE at TA stayed
at 2 (L023203 out, L012407 in at k = −0.4). A twin that does not bite makes the lane NOT EVALUABLE (criteria §6). Had it
bitten, the word would still not be a gate: EARLY READING, NOT A GATE, with **N(P) = 2** against EUC1-F's 10. The
frozen fallback tier TB passes every gate; the primary tier TA fails its grade-X null (2 against a limit of 1). No
secure lens has a single line. The newton twin exits 1.

The prediction itself works. On the truth lens, an arc measured from its VIS image predicts the split, and the line
comes back at k = 1.05 with z_s = 1.3649 (DESI 1.3657). The input limits the lane: only 178 of 2,260 lenses with
spectra have a catalogued arc at a usable position. κ = ½ FITTED. No outcome favours the framework.

## 1. What was built

- **Dispersion direction per dither.** No dither header carries an angle (DITH_ID, PTGID, DET_ID, GWA_POS, GWA_TILT).
  ESA's archive (`dr1.raw_frame`) gives `pa` per pointing; it is exactly the angle of one footprint edge (500 of 500
  frames), so it fixes the focal plane on the sky. A position angle exists for 19,030 of 19,033 dithers.
- **Convention, fixed on 147 field pairs** (none within 30″ of any ECLIPSE system): the neighbour's known line.

  | C0 | 0° | 90° | 180° | 270° |
  |---|---|---|---|---|
  | detections at k = 1, S/N ≥ 6 | 1 | 3 | 2 | **13** |

  The scale is confirmed too: median k̂ = 1.000, robust σ 0.148, n = 9, none on the wrong side. The tilt sign is
  undetermined (13 / 13 / 13), which matters at the 4° level. Frozen: C0 = 270°, k window ±0.30.
- **Arcs:** catalogued MER objects inside the aperture. The truth lens has none, so its arc comes from its VIS pixels
  by a frozen procedure: (−1.10, −1.11)″, 1.57″ from the lens, against θ_E = 1.51″.

## 2. Coverage and checks

Usable spectrum: S 2,260 (36.6 %), X 923 (35.8 %), P 1,164; with an arc candidate S 334, X 162, P 175; **evaluable**
(an arc predicted at least 30 Å along the dispersion) **S 178, X 103, P 99.**
K1 −0.0185 / −0.0439; K2 +0.2314 / +0.2149; K5 20 of 20; K6 19,030 of 19,033; C1 reproduced; all pass.
Injections into 178 evaluable S: I1, a line at the predicted shifts, is returned 163 times (91.6 %); I2, a centred
line, 0 times; I3, a line at the mirrored shifts, 0 times. **Twins:** newton exits 1 (anchor b +0.330 / +0.330 against
+0.231 / +0.215; P rose on both footings). **anyk exits 2**: grade-X SECURE at TA 2 → 2. Every other count rose
(S 3 → 5, sign-flipped 1 → 5, rotated 0 → 2, mirrored 0 → 5, grade-X AMBIGUOUS-OWN 2 → 4); the frozen test counted
the one number that did not. No repair is made: none could grade EUC1-F.

## 3. Gates

| Tier | P | S | X (limit) | arcs rotated 90°, S (limit) | sign-flipped S | mirrored S | truth | |
|---|---|---|---|---|---|---|---|---|
| TA | 2 | 3 | **2 (1.0): FAIL** | 0 (1.0) | 1 (1.0) | 0 | recovered | fails H2 |
| TB | 2 | 3 | 0 (1.0) | 0 (1.0) | 0 (1.0) | 0 | recovered | **all pass** |

**Truth lens** L015763 at both tiers: z_s 1.3649 (DESI 1.3657), k = 1.05, predicted half-split 63.7 Å (EUC9 measured
67.0), S/N 51.6 (RGS000 39.6, RGS180 33.3), Δχ² over a centred line 804. The fainter counter-image sits on the
mirrored side (S/N 17.8 / 19.8), as EUC9 saw. This is necessary, not independent: EUC9's result was known.

**Certified at TB** (each line is on the predicted side in both grism positions; the mirrored side gives S/N ≤ 6.7):

| Lens | in P | line | z_s | k | half-split | S/N | z_l | b canonical / alt |
|---|---|---|---|---|---|---|---|---|
| L001971 | yes | [O III] + 4960 (8.3 σ) | 2.4677 | 0.90 | 0.78″ | 29.3 | 1.060 | +0.151 / +0.134 |
| L015301 | yes | Hα + [S II] (3.7 σ) | 1.6160 | 1.30 | 2.22″ | 8.4 | 0.910 | +0.801 / +0.786 |
| L011858 | no (B) | [O III] + 4960 (5.2 σ) | 2.5052 | 1.05 | 0.83″ | 15.3 | 1.480 | +0.424 / +0.410 |

The two grade-X hits at TA (L023203, L026011: single lines, S/N 6.8 and 6.0) are real lines where a neighbour sits: a
projected emitter at the arc's place is what the prediction cannot remove. Figures: `figs/euc14_secure.png`.

## 4. Early reading (not a gate)

P, N = 2: median b +0.476 [+0.151, +0.801] / +0.460 [+0.134, +0.786]; source-free +0.078 / +0.051. S, N = 3:
+0.424 / +0.410. Two lenses make no statistic; the four identity readings agree (no secure lens is HA1).

## 5. What this means

1. **The method works; the sample is too small and the null is not cleared.** Emitters at the wrong place are gone
   (mirrored, rotated and centred tests give 0) and the truth lens comes back from an image-measured arc. But at TA
   grade X (2 of 103, 1.9 %) is as frequent as the lenses (3 of 178, 1.7 %): a neighbour that emits is found wherever
   it lies, so the prediction alone does not separate lenses from non-lenses. TB passes only because 3 lenses give a
   limit of max(1, …).
2. **The binding input is the arc position.** MER deblends few arcs as objects of their own, and the truth lens's arc
   is not one of them. 2,082 of the 2,260 lenses with spectra get no prediction.
3. **What would close it.** The frozen image procedure that found the truth lens's arc, applied to all ~3,200 lens and
   grade-X systems with spectra. That needs a bulk image route. IBE's cloud host refuses cutout parameters, ESA's file
   service needs a login, and row ranges cost 120 requests per system; one multi-range request per system is untested.
   **EUC1-F stays open; EUC1 stays NO VERDICT / NO VERDICT.**

## 6. Disclosures

- EUC9's whole record was seen before freezing (criteria §7), including the truth lens's dither result.
- The calibrator set grew after a preview of 62 (lines seen only for neighbours almost exactly along the dispersion):
  the second list is aligned with either axis, so the conventions stay equal. A runner-up bug was fixed after it.
- `euc14.out` prints EARLY READING: the script does not know its twins' outcome. The frozen word above includes them.
- **Network.** ESA TAP; IRSA IBE byte ranges only (about 128 MB, one stream, one request a second, one 503 handled by a
  150 s wait), run alongside EUC11's IRSA TAP download with the launching session's agreement. Hashes kept outside git.

## 7. Files

`euc14_fetch.py`, `euc14_cal.py` (`euc14_cal.out`, `_results.json`), `euc14_core.py`, `euc14_geom.py`, `euc14.py`
(`euc14.out`, `_results.json`, `_sources.csv`, `euc14_MUTATE_*`), `euc14_figs.py` (`figs/euc14_secure.png`).

    python3 -I euc14_cal.py --data-dir <dir>;  python3 -I euc14.py --data-dir <dir>
    EUC14_MUTATE=newton|anyk python3 -I euc14.py --data-dir <dir>      (each must exit 1)
