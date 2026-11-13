# EUC15 (IMAGE-ARC PREDICTED-SPLIT SOURCE REDSHIFTS): FROZEN CRITERIA

2026-11-12. Committed alone, before any VIS pixel of any lens or grade-X system other than the truth lens has been
fetched or opened, and before any prediction made from an image arc has met any spectrum but the truth lens's. TEST
lane; adopts nothing. κ = ½ FITTED; not theory closed. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded
separately, never pooled. EUC1-F is one-sided; no outcome may be described as the data favouring the framework.

## 0. What this lane is

EUC14 (`../EUC14_predicted_split_source_redshifts/`) predicted each lens's line shift per dither from a catalogued arc
and each dither's dispersion direction. Its prediction recovered the truth lens from an arc measured in the VIS image.
Only 178 of 2,260 lenses with spectra had a usable catalogued arc, and its word was NOT EVALUABLE (its `anyk` twin did
not bite; N(P) = 2). Its RESULT §5 item 3 names the next step, run here: the same image procedure on every system with
a usable spectrum, lenses and grade X alike.

## 1. Inherited verbatim (code imported from `euc14.py`, not copied or edited)

Everything in EUC14's FROZEN_CRITERIA §1b to §6 except the arc source and the `anyk` twin:
- the geometry and field calibration (C0 = 270°, tilt sign +1, DISP = 44.67 Å″⁻¹, k window |k − 1| ≤ 0.30);
- the systems (S, P inside it, grade X with θ_E assigned as in EUC3 §2, and the truth lens L015763), the usable
  spectrum, the usable arc (predicted half-split ≥ 30 Å, opposite signs in the two grism positions);
- the rule (§3: fit, candidate conditions a to d, tiers TA and TB, line identity, guards, SECURE / AMBIGUOUS-OWN /
  CONFLICT);
- the gates (§4): H4 truth, H2 grade-X purity (EUC3's rule), H3 arcs rotated by 90°, H2b sign-flipped, coverage; the
  mirrored prediction reported;
- the reading (§5): EUC1-F exactly as frozen in EUC1 RESULT §8 on P if N(P) ≥ 10, otherwise EARLY READING, NOT A
  GATE; both footings; S beside it. Each HA1 lens is also read as [S III] 9533, [O III] 5008 and [O II] 3727; a word
  that changes under any of them becomes NO VERDICT (IDENTIFICATION-DEPENDENT);
- checks K1, K2, K5, K6, C1, injections I1 to I3, and the `newton` twin.

## 2. The one new input: the arc from the VIS image (frozen)

- **Box.** 64 × 64 pixels (6.4″ at 0.1″ per pixel) of the tile's background-subtracted VIS mosaic (`BGSUB-MOSAIC-VIS`),
  centred on the pixel nearest the lens object's MER position. The tile is the MER tile of the lens object. The mosaic
  file comes from ESA's `dr1.mosaic_product`; where a tile has several (5 of 2,382), the latest processing time in the
  name is used. **Why 64:** the arc search reaches 1.5 θ_E, which fits inside the box for θ_E ≤ 2.13″ (98.4 % of S's
  usable systems, 98.7 % of X's). Each extra row costs one request. Beyond that the annulus is clipped at the box edge,
  the same way on both sides.
- **Usable box:** at least 90 % of its pixels finite and non-zero.
- **Arc:** `euc14.truth_arc`, unchanged. The lens light is modelled as the median in circular 0.1″ annuli about the lens
  object; the residual is smoothed by a Gaussian of 1.5 pixels; the arc is the residual-weighted centroid of positive
  pixels within 0.3″ of the brightest smoothed residual between 0.5 θ_E and 1.5 θ_E.
- **Several blobs:** only the brightest is used. Every system gets exactly one arc, lens or grade X, with no
  significance threshold. A system with no real arc gets the position of its brightest residual, so the search there
  acts as a null of its own. The catalogued arcs of EUC14 are not used.
- **Evaluable:** usable spectrum, usable box, and an arc that is usable in EUC14's sense.
- The truth lens's box is read the same way; it equals EUC14's cutout pixel for pixel (§6).

## 3. Checks and twins (frozen; a failed check or a twin that does not exit 1 makes the lane NOT EVALUABLE)

- Inherited: K1, K2, K5, K6, C1, I1 to I3 (EUC14 §6).
- **K7** (per side, S and X): a VIS box for ≥ 95 % of the usable-spectrum systems, and a usable image arc for ≥ 90 %
  of those boxes.
- **Twin `newton`** (EUC15_MUTATE=newton): as EUC14. **Twin `nowindow`** (EUC15_MUTATE=nowindow) replaces `anyk`. It
  removes the k window as `anyk` did (any |k| ≥ 0.3) and counts a quantity that must move: the number of (system,
  variant) pairs of S and X with a TA candidate before line identity and guards, over four variants (true prediction,
  sign-flipped, rotated, mirrored). Removing a condition can only enlarge each candidate set, so this count cannot
  fall. It must rise; staying equal would mean the window never acts. Each twin writes separate outputs and must exit 1.

## 4. Selection, stated

Only lenses whose brightest residual between 0.5 θ_E and 1.5 θ_E lies at least 0.67″ along the dispersion and inside
the lens object's extraction across it, with a line bright enough in both grism positions, can enter. The reading
describes those lenses, not the median of P. For the null to be like for like, grade-X systems are put through the
identical box, procedure and θ_E-scaled annulus.

## 5. Not claimed

No measurement of a₀ or κ. Nothing about lenses whose arcs show no line. A HOLDS would not confirm the law; a
recovered truth lens validates the geometry, not the purity.

## 6. Seen before freezing (disclosed)

- **EUC14 in full**, including that its `anyk` twin exited 2 (grade-X SECURE at TA 2 → 2) and every number: catalogued
  arcs evaluable S 178, X 103, P 99; TA SECURE S 3, P 2, X 2 (limit 1); TB S 3, X 0; the three certified lenses
  (L001971, L015301, L011858) and the two grade-X hits (L023203, L026011); the early reading (P, N = 2, b_med
  +0.476 / +0.460); the truth lens's recovery (z_s 1.3649, k 1.05). EUC9's record, as listed in EUC14 §7.
- The truth lens's box: identical to EUC14's cutout centre, and its arc unchanged at (−1.10, −1.11)″.
- A dry run of `euc15.py` with only the truth lens's box present: every lens and grade-X count 0, K1, K2, K5, K6 and C1
  pass, H4 recovered as in EUC14.
- Catalogue-only facts: 3,184 lens objects with dither spectra on 2,382 MER tiles, and the θ_E percentiles of the
  usable systems (S: 5 % 0.53″, median 0.88″, 95 % 1.77″).
- The launching session's estimate (evaluable lenses above 1,000; N(P) near 20 if the certified rate stays near 2 %),
  marked by it as unverified.
- **Network so far.** ESA TAP: the mosaic list. One IRSA request meant to test multi-range support was answered with
  the whole 1.47 GB mosaic. curl's 60 s limit stopped it after **144 MB**; the file was deleted unopened. That 144 MB
  counts against this lane's 300 MB cap. The same mosaics are in the public AWS Open Data bucket
  `nasa-irsa-euclid-dr1`, which serves single byte ranges. The boxes come from there: up to 8 keep-alive connections,
  at most 60 requests a second in all, 150 s back-off on any 429 or 5xx, and the box stage stops at 140 MB. Hash
  manifest outside git.
