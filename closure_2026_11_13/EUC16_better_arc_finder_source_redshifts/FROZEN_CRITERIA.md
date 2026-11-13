# EUC16 (BETTER ARC FINDER, PREDICTED-SPLIT SOURCE REDSHIFTS): FROZEN CRITERIA

2026-11-13. Committed alone, before any arc from the new finder has met any spectrum of any lens, grade-X system or the
truth lens. TEST lane; adopts nothing, relabels nothing. κ = ½ FITTED; not theory closed. Footings 9.3603e-11
(canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. EUC1-F is one-sided; no outcome may be described as
the data favouring the framework.

## 0. What this lane is, and that it is a second attempt

EUC15 (`../../closure_2026_11_12/EUC15_image_arc_predicted_split/`) certified 5 lenses of P against EUC1-F's 10 (EARLY
READING, NOT A GATE / same). Its RESULT §5 names the limit: the arc is the brightest residual after a circular lens
model, which lands near the inner edge of the 0.5 to 1.5 θ_E annulus (median 0.61 θ_E), shortening predicted splits;
only 536 of 2,259 lenses are evaluable. **This lane is a second attempt at the same gate, made after seeing the first.**
It fixes ONE finder (§2), not a family. There is no third attempt inside this lane: any other finder is at most a
reported reading, never the label. EUC15's certified list and all its numbers are known to this lane (§6).

## 1. Inherited unchanged

Everything EUC15 froze except the arc finder: EUC14's geometry and field calibration (C0 = 270°, ST = +1, DISP 44.67
Å″⁻¹, k window |k − 1| ≤ 0.30), the systems (S, P, grade X with θ_E as EUC3 §2, truth lens L015763), the usable spectrum,
the usable arc (predicted half-split ≥ 30 Å, opposite signs in the two grism positions), the rule (fit, candidate
conditions, tiers TA then TB, line identity, guards, SECURE / AMBIGUOUS-OWN / CONFLICT), the gates H4 truth, H2 grade-X
purity with limit max(1, 0.20 · n_S · E_X / E_S), H3 rotated 90° and H2b sign-flipped with limit max(1, 0.20 · n_S)
(limits scale with the new evaluable counts by these same formulas), the mirrored prediction reported, coverage, checks
K1, K2, K5, K6, K7, C1, injections I1 to I3, the box (EUC15's 64 × 64 VIS boxes already on disk, no new fetch), the
usable box (≥ 90 % finite and non-zero), one arc per system with no significance threshold, and the reading (§5).
EUC14's functions are imported (`euc14.py`, not edited); EUC15's `main` is copied into `euc16.py` with the arc input
replaced and the reports of §4 added. A copy is not an import, so check K8 (§3) proves the copy is faithful.

## 2. The one new input: the EUC16 arc finder (frozen)

Code: `euc16_arc.py`, function `arc_euc16`, sha256 `daca57ac82bc8039a2e836880613141f3db2fd208353ebc25430b34bc39863ff`.
Per system, on its box, with offsets (east, north) in arcsec from the lens object (the extraction centre):
1. **Light centre.** Flux-weighted centroid of positive pixels within 0.3″, iterated 5 times from the lens object; if it
   lands more than 0.5″ from the lens object, the lens object is used.
2. **Lens shape.** About that centre, flux-weighted second moments of positive pixels inside an elliptical aperture of
   semi-major axis max(0.3″, 0.5 θ_E), iterated 5 times from a circle; axis ratio q (floor 0.3) and major-axis angle.
3. **Lens-light model.** The median in elliptical annuli 0.1″ wide in circularised radius √q·x, y/√q about that centre.
4. **Residual.** Box minus model (non-finite and zero pixels set to 0), smoothed by a Gaussian of 1.5 pixels (as EUC15).
5. **Significance.** Residual / √(σ_sky² + (0.03 · M)²): σ_sky = 1.4826 × MAD of the smoothed residual over the box,
   M = the absolute model smoothed by the same Gaussian. The 0.03 is the model-mismatch fraction.
6. **Arc.** The peak of the significance between 0.5 θ_E and 1.5 θ_E of the lens object (as EUC15), then the
   residual-weighted centroid of positive smoothed residual within 0.3″ of that peak (as EUC15).

### 2b. How it was chosen (image evidence only; `euc16_finder_dev.py`, `euc16_finder_dev*.out`)

Ten finders were compared on four kinds of image-only evidence, none touching a spectrum or a dither direction: EUC15's
(v1); recentred (c); recentred + elliptical (ce); ce divided by its annulus's scatter from all residuals (ceM) or from
negative residuals (ceN); ceN without recentring (eN); ce divided by the noise of step 5 with 0.02, 0.03, 0.05, 0.10.
(T) the truth lens's arc; (A) agreement with catalogued arc candidates (EUC14's definition, 334 S systems); (J) singular-
isothermal arcs (Gaussian source, β/θ_E 0.1 to 0.6) injected into grade-X boxes at S/N 15, 30, 60; (R) arc radius / θ_E.
- **Truth:** v1, c, ce, 0.02 and 0.03 put it within 0.07″ of EUC15's (−1.10, −1.11)″ (0.03: (−1.17, −1.10)″); ceN, ceM,
  eN, 0.05 and 0.10 move it 0.66″ outward to a spot beside the ring. The flip lies between 0.03 and 0.05. **So the choice
  of 0.03 is fitted in part to the truth lens; H4 is not independent evidence (it was not before either).**
- **Rule, written after the 150-injection comparison and before the 400-injection one:** among ce, 0.02 and 0.03, keep
  those with the truth within 0.3″ and catalogue agreement within 0.5″ no lower than v1's minus 0.03; take the highest
  injection k-agreement. 400 injections per S/N (k-agree = |found·u / true·u − 1| ≤ 0.3, random u, |true·u| ≥ 0.67″):

| finder | truth | catalogue ≤ 0.3″ / ≤ 0.5″ / azimuth ≤ 20° | k-agree S/N 15 / 30 / 60 | S radius/θ_E median | S radius ≥ 0.67″ |
|---|---|---|---|---|---|
| v1 (EUC15) | kept | 0.713 / 0.793 / 0.830 | 0.158 / 0.333 / 0.618 | 0.61 | 0.457 |
| ce | kept | 0.677 / 0.766 / 0.788 | 0.247 / 0.412 / 0.705 | 1.09 | 0.739 |
| 0.02 | kept | 0.695 / 0.787 / 0.804 | 0.316 / 0.491 / 0.737 | 1.15 | 0.845 |
| **0.03 (frozen)** | kept | 0.698 / 0.790 / 0.810 | **0.335 / 0.509 / 0.756** | 1.18 | 0.863 |

Catalogued candidates sit at median 1.30 θ_E. X's median arc radius rises too (0.62 → 1.04 θ_E), so the grade-X null
gets more evaluable systems and more trials: that is the like-for-like cost of the change and stays in the null.
No evaluable count was computed before this commit (it needs dither directions); no spectrum flux was read.

## 3. Checks and twins (frozen; a failed check or a twin that does not exit 1 makes the lane NOT EVALUABLE)

- Inherited: K1, K2, K5, K6, K7 (S and X), C1, I1 to I3.
- **K8 (new):** `EUC16_FINDER=v1` runs the copied code with EUC15's finder; its coverage, every gate count, pre-guard TA
  count, N(P) and N(S) must equal EUC15's committed `euc15_results.json` exactly. (These are EUC15's known arcs.)
- **Twins:** `EUC16_MUTATE=newton` (b must rise on both footings, sample and anchor) and `EUC16_MUTATE=nowindow` (the
  pre-guard TA (system, variant) count must rise), both as EUC15, separate outputs, each must exit 1.

## 4. Labels and reports (frozen)

- Reading tier: TA if it passes H2, H3, H2b and H4; else TB; else NOT EVALUABLE.
- **N(P) ≥ 10** at that tier: EUC1-F exactly as in EUC1 RESULT §8, per footing, never pooled: **LENS GATE HOLDS** if the
  upper bound of median b (law S, 95 % bootstrap, `euc1.stats`) ≤ 0.15; **LENS GATE FAILS** if the lower bound ≥ 0.25;
  otherwise **NO VERDICT**. If reading HA1 lenses as [S III] 9533, [O III] 5008 or [O II] 3727 changes a footing's
  word, that word is **NO VERDICT (IDENTIFICATION-DEPENDENT)**. Hα stays the primary. **N(P) < 10: EARLY READING, NOT A
  GATE.** A HOLDS is a hit awaiting an independent blind re-grade, not a pass; a FAILS is verified as hard (below).
- Reported beside the label: counts at each stage (boxes, arcs, evaluable, certified in S and in P), the four identity
  readings, how many certified redshifts rest on one line, every certified lens's b, the robustness rows, a
  **selection check** (source-free b of the certified lenses against all of P: medians and each lens's percentile, plus
  θ_E and z_l medians), and **leave-one-out** bounds. A figure per certified lens (`euc16_figs.py`).
- Verification of any graded word: K8 and the twins; the figures inspected; the leave-one-out range stated; nothing
  changes the word.

## 5. EUC15's five certified lenses, stated in advance

Their new arcs (image only, computed before this commit) against EUC15's: L001890, L001520, L001449, L012745 move by
≤ 0.01″; **expected kept** (same predicted shifts to 1 %). L001971 moves 0.11″ ((−0.67, +0.51) → (−0.76, +0.44)″; EUC15
k = 0.90): expected kept, may be lost if its k leaves the window or another candidate dominates. A loss of any of the
five is accepted as the cost of a finder chosen without reference to them; none will be restored by hand.

## 6. Seen before freezing (disclosed)

EUC14 and EUC15 in full (every count, the five and their b, the TA null failures, the early reading +0.589 / +0.574);
EUC1 §8; the launching brief (which repeats EUC15's diagnosis). Image-only work above, including a residual picture of
the truth lens. No spectrum flux, dither direction, evaluable count or certification from a new arc has been seen.
No download or network fetch was made by this lane.

## 7. Not claimed

No measurement of a₀ or κ. A recovered truth lens validates the geometry, not the purity. The reading describes lenses
whose finder arc lies far enough along their field's dispersion, not the median of P.
